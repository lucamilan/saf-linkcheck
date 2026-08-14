#!/usr/bin/env python3
"""saf-migrate-lang — the deterministic half of a language migration of a `.saf/` corpus.

The method asks for records in English because the semantic index behind `recall` embeds with
English-only models: a record written in another language is reachable by its exact words and by
nothing else, and the hybrid search collapses to its lexical channel. The rule binds what a
project writes next, so an instance whose corpus predates it is never migrated automatically —
migrating is opt-in and the senior's call.

Translation itself is model work. This harness owns everything around it:

    plan       inventory the corpus — what each type holds, which files read as non-English,
               what the policy says to translate and what to leave alone
    snapshot   freeze the pre-translation state: per file its citations, its relations block,
               its header fields and a digest; globally the graph size and the signal counts
    verify     prove the post-translation corpus lost nothing. The failure mode measured on a
               real migration was not bad prose — it was translators inventing citation
               brackets around bare id mentions and silently dropping real ones
    rename     re-slug filenames from the new titles through `git mv`, id prefix untouched

Nothing here judges whether a record is *well* translated. It judges whether the migration was
lossless, which is the half a reader cannot check by reading.

Pure stdlib, no imports from the engine: it runs inside an instance that has only the binary.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

SAF_DIR = ".saf"

# Where each record type lives. The contract is stable across instances; `saf-tools describe
# --type T` prints the same paths. Kept as a literal so the harness needs no engine to inventory
# a corpus (a broken index is one of the reasons to reach for it).
TYPE_DIRS = {
    "decision": ".saf/.decisions",
    "knowledge": ".saf/.knowledge",
    "source": ".saf/.sources",
    "iteration": ".saf/.iterations",
}
ROADMAP_DIR = ".saf/.roadmap"

# Policy per type, from the method's own migration:
#   translate — cognition queried by concept, where the retrieval gain lands
#   hold      — closed work is the historical log and is not rewritten; the rule binds new records
POLICY = {
    "decision": "translate",
    "knowledge": "translate",
    "source": "translate",
    "roadmap": "translate",
    "iteration": "hold",
}
POLICY_WHY = {
    "translate": "queried by concept — this is where the retrieval gain lands",
    "hold": "historical log; closed work is not rewritten (the rule binds new records)",
}

NODE_TYPES = tuple(TYPE_DIRS)
_TYPED_REF = re.compile(r"\[\[(" + "|".join(NODE_TYPES) + r"):0*(\d+)\]\]")
_BL_REF = re.compile(r"\[\[BL-0*(\d+)\]\]")
_FENCE = re.compile(r"^\s*(```|~~~)")
_INLINE_SPAN = re.compile(r"`[^`]*`")
_HEADER_FIELD = re.compile(r"^-\s*\*\*([^:*]+):\*\*\s*(.*)$")
_TITLE = re.compile(r"^#\s+0*(\d+)\s*[·.\-—–]\s*(.+)$")
_FILE_ID = re.compile(r"^0*(\d+)_")
_RELATIONS_HEAD = re.compile(r"^##\s+Relations\s*$")
# The autonomous-loop plan form is matched by regex from the kit's contract: its headings and
# field keys are machine tokens, not prose. Only the text inside them is translated.
_PLAN_HEAD = re.compile(r"^##\s+\S+\s*\(loop\)\s*$")

# A header value of more than this many words reads as prose (a Lesson), and prose is expected to
# change. Shorter ones are enums, dates, ids and provenance — contract, where a change is a defect.
# Words, not characters: a provenance line is long but says little, a lesson is the opposite.
PROSE_VALUE_WORDS = 12

# --- Language triage --------------------------------------------------------
# A stopword ratio, not a language detector. It exists to ORDER the work — which files to look
# at first — never to decide anything. The method deliberately has no mechanical language gate:
# a detector fires on records that legitimately quote foreign source material, on identifiers,
# and on the machine tokens the record form itself prescribes.

_EN_WORDS = {
    "the", "and", "of", "to", "is", "that", "it", "for", "not", "with", "as", "this", "but",
    "are", "be", "on", "by", "from", "or", "an", "was", "which", "what", "when", "than", "its",
    "has", "have", "does", "do", "only", "same", "never", "always", "already", "because",
    "before", "after", "each", "every", "without", "into", "more", "less", "still", "they",
    "their", "would", "could", "should", "there", "here", "then", "where", "while", "how",
}
_OTHER_WORDS = {
    # it
    "che", "non", "per", "con", "una", "del", "della", "dei", "delle", "sono", "questo",
    "questa", "quando", "anche", "perché", "già", "dove", "quello", "tutto", "essere", "stato",
    "senza", "prima", "dopo", "nel", "nella", "gli", "alla", "sulla", "ma", "se", "più",
    # es
    "que", "los", "las", "por", "para", "este", "esta", "cuando", "porque", "todo", "ser",
    "sin", "antes", "después", "pero", "muy",
    # pt
    "não", "uma", "com", "quando", "onde", "tudo", "sem", "depois", "mas", "pelo", "pela",
    # fr
    "les", "des", "une", "dans", "cette", "parce", "où", "tout", "être", "avant", "après",
    "mais", "avec", "pour",
    # de
    "und", "der", "die", "das", "nicht", "für", "mit", "eine", "wenn", "weil", "alles", "sein",
    "ohne", "nach", "aber", "oder",
}
_WORD = re.compile(r"[a-zà-ÿ]{2,}")
MIN_WORDS_FOR_VERDICT = 40


def strip_code(text: str) -> str:
    """Blank out markdown code so what remains is prose. A `[[...]]` inside code is code.

    Conservative on the inline pass, deliberately: a span wrapping across lines leaves an odd
    backtick count on each, and pairing the wrong delimiters would swallow the prose between and
    drop a real citation. Those lines keep their spans — at worst a false positive survives.
    """
    out, in_fence = [], False
    for line in text.splitlines():
        if _FENCE.match(line):
            in_fence = not in_fence
            out.append("")
        elif in_fence:
            out.append("")
        elif line.count("`") % 2 == 0:
            out.append(_INLINE_SPAN.sub(" ", line))
        else:
            out.append(line)
    return "\n".join(out)


def language_signal(text: str) -> dict:
    """(verdict, ratios, sample size) — a triage signal, never a verdict about a record."""
    words = _WORD.findall(strip_code(text).lower())
    total = len(words)
    if total < MIN_WORDS_FOR_VERDICT:
        return {"verdict": "too-short", "en": 0.0, "other": 0.0, "words": total}
    en = sum(1 for w in words if w in _EN_WORDS) / total
    other = sum(1 for w in words if w in _OTHER_WORDS) / total
    if other > en:
        verdict = "non-english"
    elif en > other * 2 and en > 0.04:
        verdict = "english"
    else:
        verdict = "mixed"
    return {"verdict": verdict, "en": round(en, 4), "other": round(other, 4), "words": total}


# --- Record parsing ---------------------------------------------------------


def split_relations(lines: list[str]) -> tuple[list[str], list[str]]:
    """(body, relations-block) — the relations block is authored contract, never prose."""
    body, relations, in_rel = [], [], False
    for line in lines:
        if _RELATIONS_HEAD.match(line):
            in_rel = True
            relations.append(line)
            continue
        if in_rel and line.startswith("## "):
            in_rel = False
        (relations if in_rel else body).append(line)
    return body, relations


def citations(text: str) -> dict[str, int]:
    """Every resolvable citation in prose, WITH its multiplicity."""
    text = strip_code(text)
    counts: dict[str, int] = {}
    for m in _TYPED_REF.finditer(text):
        key = f"{m.group(1)}:{int(m.group(2)):03d}"
        counts[key] = counts.get(key, 0) + 1
    for m in _BL_REF.finditer(text):
        key = f"BL-{int(m.group(1)):03d}"
        counts[key] = counts.get(key, 0) + 1
    return counts


def header_fields(lines: list[str]) -> dict[str, str]:
    """The `- **Key:** value` block under the title, continuation lines folded in.

    A wrapped value belongs to its key: a Lesson runs over several indented lines, and reading
    only the first one would compare a truncated prefix and call the rest unchanged.
    """
    out: dict[str, str] = {}
    key: str | None = None
    for line in lines:
        if line.startswith("## "):
            break
        m = _HEADER_FIELD.match(line)
        if m:
            key = m.group(1).strip()
            out[key] = m.group(2).strip()
        elif key and line.strip() and line[:1].isspace():
            out[key] = f"{out[key]} {line.strip()}".strip()
        elif not line.strip():
            key = None
    return out


def is_prose_value(value: str) -> bool:
    """Whether a header value is prose the translation is expected to move."""
    return len(value.split()) > PROSE_VALUE_WORDS


def slugify(text: str) -> str:
    """The engine's own slug rule — a filename must land where `record` would have put it."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "untitled"


def fingerprint(path: Path, repo: Path, rtype: str) -> dict:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    body, relations = split_relations(lines)
    title_m = next((_TITLE.match(ln) for ln in lines if _TITLE.match(ln)), None)
    file_m = _FILE_ID.match(path.name)
    return {
        "type": rtype,
        "policy": POLICY[rtype],
        "id": f"{int(file_m.group(1)):03d}" if file_m else None,
        "title": title_m.group(2).strip() if title_m else None,
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "bytes": len(text.encode("utf-8")),
        "relations": hashlib.sha256("\n".join(
            ln.rstrip() for ln in relations).encode("utf-8")).hexdigest() if relations else None,
        "header": header_fields(lines),
        "citations": citations("\n".join(body)),
        "plan_headings": [ln.strip() for ln in lines if _PLAN_HEAD.match(ln)],
        "language": language_signal("\n".join(body)),
    }


def corpus(repo: Path) -> dict[str, dict]:
    """Every record file in the instance, keyed by repo-relative posix path."""
    out: dict[str, dict] = {}
    for rtype, rel in TYPE_DIRS.items():
        d = repo / rel
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.md")):
            out[p.relative_to(repo).as_posix()] = fingerprint(p, repo, rtype)
    d = repo / ROADMAP_DIR
    if d.is_dir():
        for p in sorted(d.glob("*.md")):
            out[p.relative_to(repo).as_posix()] = fingerprint(p, repo, "roadmap")
    return out


# --- Engine-derived globals -------------------------------------------------


def run_engine(cmd: list[str], args: list[str], repo: Path) -> str | None:
    """Call the facade; None when it is unavailable or fails. A missing engine degrades the
    global invariants, it does not stop the migration — say so rather than assume."""
    if not cmd:
        return None
    try:
        proc = subprocess.run(cmd + args, cwd=str(repo), capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=600)
    except (OSError, subprocess.SubprocessError):
        return None
    return (proc.stdout or "") + (proc.stderr or "")


def globals_snapshot(cmd: list[str], repo: Path) -> dict:
    """Graph size and signal counts — the coarse proof that a translation moved no edges."""
    out: dict = {"engine": " ".join(cmd) if cmd else None}
    status = run_engine(cmd, ["status"], repo)
    if status:
        m = re.search(r"graph:\s*([\d,]+)\s*node\(s\)\s*[·.]\s*([\d,]+)\s*edge\(s\)", status)
        if m:
            out["graph_nodes"] = int(m.group(1).replace(",", ""))
            out["graph_edges"] = int(m.group(2).replace(",", ""))
    consc = run_engine(cmd, ["conscience"], repo)
    if consc:
        m = re.search(r"(\d+)\s+signal\(s\)", consc)
        if m:
            out["conscience_signals"] = int(m.group(1))
    return out


# --- Output helpers ---------------------------------------------------------

FAIL, WARN, INFO = "FAIL", "warn", "info"


def emit(findings: list[tuple[str, str, str]], level: str, where: str, msg: str) -> None:
    findings.append((level, where, msg))


def print_findings(findings: list[tuple[str, str, str]]) -> int:
    order = {FAIL: 0, WARN: 1, INFO: 2}
    for level, where, msg in sorted(findings, key=lambda f: (order[f[0]], f[1])):
        print(f"  [{level:>4}] {where}: {msg}")
    hard = sum(1 for level, _, _ in findings if level == FAIL)
    warn = sum(1 for level, _, _ in findings if level == WARN)
    print(f"\n{len(findings)} finding(s) — {hard} blocking, {warn} to judge.")
    return hard


# --- Commands ---------------------------------------------------------------


def cmd_plan(args, repo: Path, engine: list[str]) -> int:
    files = corpus(repo)
    if not files:
        print(f"no records found under {repo / SAF_DIR} — is this a SAF instance?")
        return 2
    by_type: dict[str, list[tuple[str, dict]]] = {}
    for rel, fp in files.items():
        by_type.setdefault(fp["type"], []).append((rel, fp))
    if args.json:
        print(json.dumps({"repo": str(repo), "files": files}, ensure_ascii=False, indent=2))
        return 0
    print(f"saf-migrate-lang plan — {repo}\n")
    for rtype in sorted(by_type):
        items = by_type[rtype]
        policy = POLICY[rtype]
        verdicts: dict[str, int] = {}
        for _, fp in items:
            v = fp["language"]["verdict"]
            verdicts[v] = verdicts.get(v, 0) + 1
        kb = sum(fp["bytes"] for _, fp in items) / 1024
        spread = ", ".join(f"{v}: {n}" for v, n in sorted(verdicts.items()))
        print(f"{rtype:>10}  {len(items):>4} file(s)  {kb:>7.0f} KB  [{policy}]  {spread}")
        print(f"{'':>10}  {POLICY_WHY[policy]}")
        if args.verbose or policy == "translate":
            candidates = [(rel, fp) for rel, fp in items
                          if fp["language"]["verdict"] in ("non-english", "mixed")]
            for rel, fp in candidates if args.verbose else candidates[:5]:
                lang = fp["language"]
                flag = " [carries a loop-plan form]" if fp["plan_headings"] else ""
                print(f"{'':>12}{lang['verdict']:>12}  {rel}{flag}")
            if not args.verbose and len(candidates) > 5:
                print(f"{'':>12}{'':>12}  … {len(candidates) - 5} more (--verbose)")
        print()
    total = sum(1 for fp in files.values()
                if POLICY[fp["type"]] == "translate"
                and fp["language"]["verdict"] in ("non-english", "mixed"))
    print(f"{total} file(s) in scope read as non-English or mixed.")
    print("The verdict is a stopword ratio: it orders the work, it does not judge a record.")
    print("Next: snapshot, then translate, then rename, then verify.")
    return 0


def cmd_snapshot(args, repo: Path, engine: list[str]) -> int:
    files = corpus(repo)
    if not files:
        print(f"no records found under {repo / SAF_DIR} — is this a SAF instance?")
        return 2
    snap = {
        "tool": "saf-migrate-lang",
        "version": 1,
        "created": date.today().isoformat(),
        "repo": str(repo),
        "globals": {} if args.no_globals else globals_snapshot(engine, repo),
        "files": files,
    }
    out = Path(args.snapshot)
    if not out.is_absolute():
        out = repo / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print(f"snapshot: {len(files)} file(s) frozen -> {out}")
    g = snap["globals"]
    if g.get("graph_nodes") is not None:
        print(f"  graph: {g['graph_nodes']} node(s), {g['graph_edges']} edge(s)"
              + (f", conscience: {g['conscience_signals']} signal(s)"
                 if g.get("conscience_signals") is not None else ""))
    elif not args.no_globals:
        print("  graph/conscience counts UNAVAILABLE — the engine did not answer.")
        print("  Pass --saf-tools if the facade is not on PATH; verify will say the same.")
    return 0


def _load_snapshot(args, repo: Path) -> dict | None:
    p = Path(args.snapshot)
    if not p.is_absolute():
        p = repo / p
    if not p.is_file():
        print(f"no snapshot at {p} — run `snapshot` BEFORE translating.")
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _match_renames(before: dict, after: dict) -> dict[str, str]:
    """Pair a vanished path with a new one carrying the same type and id prefix."""
    gone = {rel: fp for rel, fp in before.items() if rel not in after}
    fresh = {rel: fp for rel, fp in after.items() if rel not in before}
    pairs: dict[str, str] = {}
    for rel, fp in gone.items():
        for new_rel, new_fp in fresh.items():
            if new_rel in pairs.values():
                continue
            if fp["type"] == new_fp["type"] and fp["id"] and fp["id"] == new_fp["id"]:
                pairs[rel] = new_rel
                break
    return pairs


def cmd_verify(args, repo: Path, engine: list[str]) -> int:
    snap = _load_snapshot(args, repo)
    if snap is None:
        return 2
    before, after = snap["files"], corpus(repo)
    renames = _match_renames(before, after)
    findings: list[tuple[str, str, str]] = []

    for rel, fp in before.items():
        now_rel = renames.get(rel, rel)
        now = after.get(now_rel)
        if now is None:
            emit(findings, FAIL, rel, "file is gone and no file with the same id took its place")
            continue
        if now_rel != rel:
            emit(findings, INFO, rel, f"renamed -> {now_rel}")
        if now["sha256"] == fp["sha256"]:
            continue  # untouched: nothing below can have changed

        if fp["policy"] == "hold" and not args.allow_holds:
            emit(findings, FAIL, now_rel,
                 "modified, but this type is held: closed work is the historical log "
                 "(--allow-holds to accept it deliberately)")

        lost = sorted(set(fp["citations"]) - set(now["citations"]))
        added = sorted(set(now["citations"]) - set(fp["citations"]))
        if lost:
            emit(findings, FAIL, now_rel, f"citation dropped: {', '.join(lost)}")
        if added:
            emit(findings, FAIL, now_rel,
                 f"citation invented: {', '.join(added)} — a translator bracketing a bare "
                 "id mention creates an edge the record never authored")
        for cid, n in sorted(fp["citations"].items()):
            m = now["citations"].get(cid)
            if m is not None and m != n:
                level = FAIL if args.strict_counts else WARN
                emit(findings, level, now_rel,
                     f"{cid} cited {n}x before, {m}x now (condensing may explain it)")

        if fp["relations"] != now["relations"]:
            what = ("relations block appeared" if not fp["relations"] else
                    "relations block vanished" if not now["relations"] else
                    "relations block changed")
            emit(findings, FAIL, now_rel, f"{what} — authored edges are contract, not prose")

        old_keys, new_keys = set(fp["header"]), set(now["header"])
        if old_keys != new_keys:
            emit(findings, FAIL, now_rel,
                 f"header field keys changed: -{sorted(old_keys - new_keys)} "
                 f"+{sorted(new_keys - old_keys)} — the keys are machine tokens")
        for key in sorted(old_keys & new_keys):
            old_v, new_v = fp["header"][key], now["header"][key]
            if old_v == new_v:
                continue
            if is_prose_value(old_v):
                emit(findings, WARN, now_rel, f"header '{key}' changed (reads as prose)")
            else:
                emit(findings, FAIL, now_rel,
                     f"header '{key}': {old_v!r} -> {new_v!r} — short header values are "
                     "enums, dates and ids, not prose")

        if fp["plan_headings"] != now["plan_headings"]:
            emit(findings, FAIL, now_rel,
                 "loop-plan heading changed — it is matched by regex from the kit's contract; "
                 "only the text inside it is translated")

        if (fp["policy"] == "translate"
                and now["language"]["verdict"] == "non-english"
                and fp["language"]["verdict"] == "non-english"):
            emit(findings, WARN, now_rel, "still reads as non-English (triage signal)")

        # Only warn where `rename` would actually act: on a held type it moves nothing unless
        # the same `--allow-holds` is passed to it, and pointing at a command that then skips
        # the file is worse than saying nothing.
        if now["title"] and now["id"] and (fp["policy"] == "translate" or args.allow_holds):
            expected = f"{now['id']}_{slugify(now['title'])}.md"
            if Path(now_rel).name != expected:
                hint = "rename --allow-holds" if fp["policy"] != "translate" else "rename"
                emit(findings, WARN, now_rel,
                     f"filename no longer matches its title (expected {expected}) — run `{hint}`")

    for rel in sorted(set(after) - set(before) - set(renames.values())):
        emit(findings, WARN, rel, "new file, absent from the snapshot — outside this migration?")

    print(f"saf-migrate-lang verify — {len(before)} file(s) in the snapshot, "
          f"{len(after)} on disk\n")
    hard = print_findings(findings) if findings else (print("  nothing lost.") or 0)

    # Global invariants: a translation moves no edges and creates no coherence signals.
    g_before = snap.get("globals") or {}
    if args.no_globals or not g_before:
        print("\nglobal invariants: not checked (no baseline in the snapshot).")
    else:
        g_now = globals_snapshot(engine, repo)
        print()
        for key, label, blocking in (("graph_nodes", "graph nodes", True),
                                     ("graph_edges", "graph edges", True),
                                     ("conscience_signals", "conscience signals", False)):
            old, new = g_before.get(key), g_now.get(key)
            if old is None or new is None:
                print(f"  [info] {label}: unavailable — the engine did not answer")
            elif old == new:
                print(f"  [  ok] {label}: {new} (unchanged)")
            else:
                print(f"  [{'FAIL' if blocking else 'warn'}] {label}: {old} -> {new}")
                hard += 1 if blocking else 0

    for verb in ("audit", "fmt-lint"):
        out = run_engine(engine, [verb], repo)
        if out is None:
            print(f"  [info] {verb}: not run — the engine did not answer")
            continue
        tail = [ln for ln in out.strip().splitlines() if ln.strip()][-1:]
        print(f"  [ ---] {verb}: {tail[0] if tail else '(no output)'}")

    print("\n" + ("MIGRATION LOSSY — resolve the blocking findings above." if hard else
                  "MIGRATION LOSSLESS on every mechanical invariant."))
    return 1 if hard else 0


def cmd_rename(args, repo: Path, engine: list[str]) -> int:
    snap = _load_snapshot(args, repo)
    if snap is None:
        return 2
    before = snap.get("files") or {}
    after = corpus(repo)
    moves: list[tuple[str, str]] = []
    untouched = 0
    for rel, fp in sorted(after.items()):
        if not fp["title"] or not fp["id"]:
            continue
        # A held type is not re-slugged by default. When the senior deliberately edited one
        # (`--allow-holds`, the same door `verify` opens), the address follows the title: an
        # English title over a filename in the old language is the one state nobody disposed.
        # The flag authorizes the records the pass TOUCHED, never the whole type — a held file
        # the translation never opened keeps its name, however far that name is from the
        # current slug convention. Re-addressing closed work nobody edited is the move the
        # hold policy exists to refuse.
        if fp["policy"] != "translate":
            if not args.allow_holds:
                continue
            was = before.get(rel)
            if was is not None and was["sha256"] == fp["sha256"]:
                untouched += 1
                continue
        expected = f"{fp['id']}_{slugify(fp['title'])}.md"
        if Path(rel).name != expected:
            moves.append((rel, (Path(rel).parent / expected).as_posix()))
    if untouched:
        # Said out loud: a narrowing the caller cannot see reads as a bug the next time the
        # count does not match what `verify` reported.
        print(f"{untouched} held file(s) left alone — unchanged since the snapshot.\n")
    if not moves:
        print("every filename already matches its title.")
        return 0
    print(f"{len(moves)} file(s) to re-slug from their new titles "
          f"({'applying' if args.apply else 'dry run'}):\n")
    failed = 0
    for old, new in moves:
        print(f"  {old}\n  -> {new}")
        if not args.apply:
            continue
        proc = subprocess.run(["git", "mv", old, new], cwd=str(repo),
                              capture_output=True, text=True, encoding="utf-8", errors="replace")
        if proc.returncode != 0:
            failed += 1
            print(f"     git mv FAILED: {(proc.stderr or '').strip()}")
    if not args.apply:
        print("\nnothing moved. Re-run with --apply.")
        return 0
    if failed:
        print(f"\n{failed} move(s) failed — nothing was renamed for those.")
        return 1
    # Keep the snapshot addressable: verify pairs by id anyway, but a coherent snapshot is
    # cheaper to read than a diff full of renames.
    moved = dict(moves)
    snap["files"] = {moved.get(rel, rel): fp for rel, fp in snap["files"].items()}
    p = Path(args.snapshot)
    if not p.is_absolute():
        p = repo / p
    p.write_text(json.dumps(snap, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print(f"\n{len(moves)} file(s) renamed; snapshot paths remapped.")
    return 0


# --- Entry point ------------------------------------------------------------


def find_repo(start: Path) -> Path | None:
    for p in [start] + list(start.parents):
        if (p / SAF_DIR).is_dir():
            return p
    return None


def resolve_engine(spec: str | None) -> list[str]:
    if spec:
        return shlex.split(spec)
    found = shutil.which("saf-tools")
    return [found] if found else []


COMMANDS = {"plan": cmd_plan, "snapshot": cmd_snapshot, "verify": cmd_verify,
            "rename": cmd_rename}


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        reconf = getattr(stream, "reconfigure", None)
        if reconf:
            reconf(encoding="utf-8")

    ap = argparse.ArgumentParser(
        prog="migrate_lang.py",
        description="Deterministic harness around a language migration of a .saf/ corpus: "
                    "inventory, freeze, prove lossless, re-slug.")
    ap.add_argument("--repo", help="instance root (default: the nearest .saf/ above the cwd)")
    ap.add_argument("--snapshot", default=".saf/.cache/lang-migration.json",
                    help="where the pre-translation state lives (default: %(default)s)")
    ap.add_argument("--saf-tools", dest="saf_tools",
                    help="how to call the facade when it is not on PATH, e.g. \"python "
                         "path/to/facade.py\". Only the global invariants need it.")
    sub = ap.add_subparsers(dest="command", required=True)

    p = sub.add_parser("plan", help="inventory the corpus and what the policy says to touch")
    p.add_argument("--verbose", action="store_true", help="list every candidate file")
    p.add_argument("--json", action="store_true", help="machine-readable inventory")

    p = sub.add_parser("snapshot", help="freeze the pre-translation state (run this FIRST)")
    p.add_argument("--no-globals", action="store_true",
                   help="skip the graph and signal counts (they need the facade)")

    p = sub.add_parser("verify", help="prove the translated corpus lost nothing")
    p.add_argument("--strict-counts", action="store_true",
                   help="treat a changed citation multiplicity as blocking, not as a warning")
    p.add_argument("--allow-holds", action="store_true",
                   help="accept edits to held types (closed work) as deliberate")
    p.add_argument("--no-globals", action="store_true", help="skip the global invariants")

    p = sub.add_parser("rename", help="re-slug filenames from the new titles via git mv")
    p.add_argument("--apply", action="store_true", help="perform the moves (default: dry run)")
    p.add_argument("--allow-holds", action="store_true",
                   help="also re-slug the held records this pass edited (unchanged ones keep "
                        "their name) — the same door `verify --allow-holds` opens")

    args = ap.parse_args(argv)
    repo = Path(args.repo).resolve() if args.repo else find_repo(Path.cwd().resolve())
    if repo is None or not (repo / SAF_DIR).is_dir():
        print("no .saf/ found — run this inside an instance, or pass --repo.", file=sys.stderr)
        return 2
    return COMMANDS[args.command](args, repo, resolve_engine(args.saf_tools))


if __name__ == "__main__":
    raise SystemExit(main())
