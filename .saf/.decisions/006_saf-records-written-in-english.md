# 006 · SAF records are written in English, file names included

- **Status:** accepted
- **Date:** 2026-08-13

Every file under .saf/ is written in English: record bodies, titles, lessons, backlog entries, and the slug after the NNN_ prefix in the file name. Why: the semantic backend behind saf-tools recall indexes and retrieves English optimally, so a non-English corpus degrades read-through — and read-through is the leg the method leans on hardest, since a node that recall does not surface is cognition the next session cannot reconstruct. The rule binds new records too: compose them in English even when the session with the senior runs in another language, which is the normal case here. Scope and accepted limits: the NNN_ numeric prefix stays untouched because node resolution depends on it; the README.md files in each .saf/ subfolder are vendored kit machinery and out of this rule's reach; the host CLAUDE.md and the product code keep their own language, since neither is indexed as cognition. Translating the closed records is a form migration, not a rewrite of judgment — no decision changes its content, so invariant 3 is not in play.

## Relations
- delivered-by → [[iteration:007]]

## Amendments (append-only)
- 2026-08-13 · [docs] · Accepted exception found during the migration: the autonomous-loop plan form is matched by regex from the kit's contract.toml — the heading '## Piano (loop)', the 'Contratto:' line, the 'oracolo:'/'verde =' step keywords and the executing iteration's '## Telemetria (loop)' are machine tokens, not prose. They stay as the kit spells them; only the text inside them is English. Same reasoning covers real identifiers quoted in a record (flags, file names, literal output strings): they name things that exist, and translating them would make the cognition describe a tool that does not.
