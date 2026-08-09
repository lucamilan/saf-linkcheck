"""linkcheck — valida i link interni di un manoscritto Markdown.

Uso: python linkcheck.py <cartella> [--esterni]

Percorre i file .md della cartella, estrae i link e verifica che i
bersagli interni (percorsi relativi) esistano; se il link porta un
frammento (#sezione) verso un file .md, il frammento viene confrontato
con le ancore derivate dai titoli del bersaglio (stile GitHub:
minuscole, punteggiatura rimossa, spazi in trattini, accenti
conservati, duplicati con suffisso -1, -2). Le ancore HTML esplicite
(<a id=...>) e i frammenti nello stesso file restano fuori perimetro.
Di default i link
esterni (http, https, mailto) restano fuori perimetro; con --esterni
i link http e https vengono verificati in rete con una richiesta
HEAD. Gli esiti esterni vengono conservati per un giorno in
.linkcheck-cache.json dentro la cartella controllata (file da
ignorare in Git). Esce con 1 se trova almeno un link rotto, con 0
altrimenti.
"""

import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import unquote

CACHE_NAME = ".linkcheck-cache.json"
CACHE_TTL = 24 * 60 * 60

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:")


def iter_links(text):
    for lineno, line in enumerate(text.splitlines(), start=1):
        for match in LINK_RE.finditer(line):
            yield lineno, match.group(1)


def slugify(title):
    slug = re.sub(r"[^\w\- ]", "", title.strip().lower())
    return slug.replace(" ", "-")


def file_anchors(md_file):
    anchors = set()
    counts = {}
    for line in md_file.read_text(encoding="utf-8").splitlines():
        match = HEADING_RE.match(line)
        if not match:
            continue
        slug = slugify(match.group(1))
        seen = counts.get(slug, 0)
        counts[slug] = seen + 1
        anchors.add(slug if seen == 0 else f"{slug}-{seen}")
    return anchors


def check_external(url, timeout=5):
    import urllib.error
    import urllib.request

    request = urllib.request.Request(
        url, method="HEAD", headers={"User-Agent": "linkcheck"}
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout):
            return True
    except Exception:
        return False


def load_cache(root):
    path = root / CACHE_NAME
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_cache(root, cache):
    (root / CACHE_NAME).write_text(
        json.dumps(cache, indent=2), encoding="utf-8"
    )


def check_external_cached(url, cache):
    entry = cache.get(url)
    if entry is not None and time.time() - entry["ts"] < CACHE_TTL:
        print(f"linkcheck: dalla cache: {url}")
        return entry["ok"]
    ok = check_external(url)
    cache[url] = {"ok": ok, "ts": time.time()}
    return ok


def check_file(md_file, root, esterni=False, cache=None, anchors_cache=None):
    broken = []
    text = md_file.read_text(encoding="utf-8")
    for lineno, target in iter_links(text):
        if target.startswith(("http://", "https://")):
            if esterni and not check_external_cached(target, cache):
                broken.append((md_file.relative_to(root), lineno, target, "link rotto"))
            continue
        if target.startswith(EXTERNAL_PREFIXES) or target.startswith("#"):
            continue
        path_part, _, fragment = target.partition("#")
        if not path_part:
            continue
        resolved = (md_file.parent / path_part).resolve()
        if not resolved.exists():
            broken.append((md_file.relative_to(root), lineno, target, "link rotto"))
            continue
        if fragment and resolved.suffix == ".md":
            if anchors_cache is None:
                anchors_cache = {}
            if resolved not in anchors_cache:
                anchors_cache[resolved] = file_anchors(resolved)
            if unquote(fragment) not in anchors_cache[resolved]:
                broken.append(
                    (md_file.relative_to(root), lineno, target, "ancora mancante")
                )
    return broken


def main(argv):
    esterni = "--esterni" in argv
    argv = [arg for arg in argv if arg != "--esterni"]
    if len(argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    root = Path(argv[1]).resolve()
    if not root.is_dir():
        print(f"linkcheck: cartella non trovata: {root}", file=sys.stderr)
        return 2
    cache = load_cache(root) if esterni else None
    anchors_cache = {}
    broken = []
    for md_file in sorted(root.rglob("*.md")):
        broken.extend(
            check_file(
                md_file, root, esterni=esterni, cache=cache,
                anchors_cache=anchors_cache,
            )
        )
    if esterni:
        save_cache(root, cache)
    for rel, lineno, target, kind in broken:
        print(f"{rel}:{lineno}: {kind} -> {target}")
    print(f"linkcheck: link rotti: {len(broken)}")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
