---
name: saf
description: Open, resume, park or close SAF-governed work and prepare its commit. Invoke at the start and end of each implementation or analysis bracket. The binding method is `@saf-prompt.md`; record forms come from `saf-tools describe`.
---

# SAF — work guardrail

Use only the `saf-tools` facade. Do not hand-form `.saf/` records or restate the machine contract.
Routine lifecycle queries use `describe --type <T> --compact` (location, id verb, required fields, enums, closing gate, relations policy — derived from the same spec as the extended form). Reach for the extended `describe` or a verb's `--help` only on an error, an ambiguity, or a capability the compact form doesn't cover.

## Bootstrap (§3)
- Missing/incomplete kit: ask the senior to run `saf-tools init`.
- Otherwise: the SessionStart hook already ran `refresh` and `present` — read that output rather than re-running them (only run them yourself if no hook fired, e.g. a mid-session invocation). Resume the active iteration before opening another.
- **Read-through** for prior choices or lessons: `recall` (hits arrive **graph-expanded**) → `get` (content + **currency footer**, already enough for a currency check) → `neighbors` only when the full relation graph beyond currency is needed. A node found is not the answer until its currency is seen. **Declare the outcome** — the pertinent typed IDs, or "nothing pertinent" — before concluding.
- **The query is in the records' language, not the session's** (§3): translate the question into English before firing `recall`, identifiers and quoted output verbatim. Asking in the session's language when the corpus is English is the worst of the four cases, not a neutral one.

## Open (§4.1)
1. Query history and classify the request as new surface, follow-up, or documentation-only correction.
2. Propose a lane, starting from the project default (`describe --type iteration` prints it, read from the host `CLAUDE.md`): `chore` (no record — commit under the chore kind), `fast` (record deferred to close) or `complex`. Boundary test: is there a choice or a lesson a future session must recover? For `fast`/`complex` also propose purpose, branch, `Area`, `Nature` and oracle; the senior disposes, and may raise or lower the default per bracket.
3. Create a dedicated non-`main` branch, allocate with `next-id` (only after the senior disposes), and open through the rail.
4. For analysis, inspect pertinent registered sources.

**A `chore` needs no round-trip.** When the boundary test answers "no choice, no lesson", that
answer *is* the disposition: commit under the chore kind and move on — no ID, no record, no
confirmation asked. Asking for one reinstates the ceremony the lane exists to remove. What still
binds is the branch (never `main`) and the escalation: the moment a choice or a lesson surfaces it
becomes an iteration *before* the commit. Two contract limits decide where a chore lands, and
neither is a reason to open a bracket: it never touches `.saf/` (hygiene inside it commits under
its own kind, `Roadmap:` for the backlog; the `.saf/.kit/` sentinel is the one carve-out), and it
is refused while an iteration is in progress.

## Work (§4.2)
- Stay within purpose and validate the owed output.
- A new directional choice escalates rather than silently widening a `fast` bracket.
- For analysis, produce alternatives, rationale and a disposition.

## Autonomous loop (§5)
Only after the senior approves a plan-decision (`## Plan (loop)`, form via `describe --type plan`). Execute one step per commit, write progress to execution telemetry, and cite the plan in `Decisions:`. On any admitted trigger (`describe --type trigger` for the tokens) or plan deviation: `park` and stop; resume only after senior disposition.

## Close and commit (§4.3)
1. Validate the complete bracket.
2. Persist result — a closed analysis needs a valid `Outcome` — required links (in a `## Relations` block where the type carries one) and `Lesson:` through `close`/`record` commands.
3. Before writing, check each authored edge for coherence: right side (authored once, on its natural side), type in range, target resolvable and current. A wrong edge is silent — the graph answers, just wrongly.
4. Use `saf-tools describe` to compose valid trailers and keep commit kinds separate: iteration, backlog or source capture.
5. Do not refresh after the write: the read path freshens the indices on demand, so the next `recall`/`code` sees the new state and pays for it once, whatever the write count.

Multiline content uses stdin or file options. Hooks are the final safety net, not a substitute for these gates.
