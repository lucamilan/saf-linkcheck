"""linkcheck — valida i link interni di un manoscritto Markdown.

Uso: python linkcheck.py <cartella> [--esterni]

Percorre i file .md della cartella, estrae i link e verifica che i
bersagli interni (percorsi relativi) esistano. Di default i link
esterni (http, https, mailto) restano fuori perimetro; con --esterni
i link http e https vengono verificati in rete con una richiesta
HEAD. Esce con 1 se trova almeno un link rotto, con 0 altrimenti.
"""

import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)\)")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:")


def iter_links(text):
    for lineno, line in enumerate(text.splitlines(), start=1):
        for match in LINK_RE.finditer(line):
            yield lineno, match.group(1)


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


def check_file(md_file, root, esterni=False):
    broken = []
    text = md_file.read_text(encoding="utf-8")
    for lineno, target in iter_links(text):
        if target.startswith(("http://", "https://")):
            if esterni and not check_external(target):
                broken.append((md_file.relative_to(root), lineno, target))
            continue
        if target.startswith(EXTERNAL_PREFIXES) or target.startswith("#"):
            continue
        path_part = target.split("#", 1)[0]
        if not path_part:
            continue
        resolved = (md_file.parent / path_part).resolve()
        if not resolved.exists():
            broken.append((md_file.relative_to(root), lineno, target))
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
    broken = []
    for md_file in sorted(root.rglob("*.md")):
        broken.extend(check_file(md_file, root, esterni=esterni))
    for rel, lineno, target in broken:
        print(f"{rel}:{lineno}: link rotto -> {target}")
    print(f"linkcheck: link rotti: {len(broken)}")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
