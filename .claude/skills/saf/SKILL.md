---
name: saf
description: Open, resume, park or close SAF-governed work and prepare its commit. Invoke at the start and end of each implementation or analysis bracket. The binding method is `@saf-prompt.md`; record forms come from `saf-tools describe`.
---

# SAF — work guardrail

The prompt binds and argues; this is the checklist that projects it. Use only the `saf-tools` facade — never hand-form `.saf/` records or restate the machine contract. Routine lifecycle queries use `describe --type <T> --compact`; reach for the extended `describe` or a verb's `--help` only on an error, an ambiguity, or a capability the compact form doesn't cover.

## Bootstrap (§3)
- Kit missing or incomplete: ask the senior to run `saf-tools init`.
- Otherwise the SessionStart hook already ran `refresh` and `present` — read that output instead of re-running them (run them yourself only if no hook fired, e.g. a mid-session invocation). Resume the active iteration before opening another.
- **Read-through** before concluding on a why or a what-was-decided: `recall` (hits arrive **graph-expanded**) → `get` (content + **currency footer**, already enough for a currency check) → `neighbors` only when the relation graph beyond currency is needed. **Declare the outcome** — the pertinent typed IDs, or "nothing pertinent".
- Query in the **records' language**, not the session's: translate before firing `recall`; identifiers and quoted output stay **verbatim**.

## Open (§4.1)
1. Classify the request: new surface, follow-up, or documentation-only correction.
2. Propose a lane from the project default (`describe --type iteration` prints it): `chore`, `fast` or `complex`. Boundary test: is there a choice or a lesson a future session must recover? For `fast`/`complex` propose purpose, branch, `Area`, `Nature` and oracle too. The senior disposes, and may raise or lower the default per bracket.
3. Branch (never `main`), `next-id` only after the disposition, open through the rail.
4. For analysis, inspect the pertinent registered sources.

**A `chore` needs no round-trip.** "No choice, no lesson" *is* the disposition — commit under the chore kind, no ID, no confirmation asked: asking for one reinstates the ceremony the lane exists to remove. Still binding: the branch, and escalation to an iteration *before* the commit the moment a choice or a lesson surfaces. Two contract limits place a chore, and neither is a reason to open a bracket: it never touches `.saf/` (hygiene there commits under its own kind, `Roadmap:` for the backlog; the `.saf/.kit/` sentinel is the one carve-out), and it is refused while an iteration is in progress.

## Work (§4.2)
Stay within purpose and validate the owed output. A new directional choice escalates rather than silently widening a `fast` bracket. Analysis owes alternatives, rationale and a disposition.

## Autonomous loop (§5)
Only after the senior approves a plan-decision (`## Plan (loop)`, form via `describe --type plan`). One step per commit, progress written to the execution telemetry, the plan cited in `Decisions:`. On any admitted trigger (`describe --type trigger` for the tokens) or plan deviation: `park` and stop; resume only after senior disposition.

## Close and commit (§4.3)
1. Validate the complete bracket.
2. Persist through `close`/`record`: result, `Lesson:`, required links in a `## Relations` block where the type carries one, and a valid `Outcome` for a closed analysis.
3. Check each authored edge before writing: right side (authored once, on its natural side), type in range, target resolvable and current. A wrong edge is silent — the graph answers, just wrongly.
4. Compose trailers with `describe` and keep the commit kinds separate: iteration, backlog, source-capture.
5. Do not refresh after the write: the read path freshens the indices on demand, so the next `recall`/`code` sees the new state and pays for it once, whatever the write count.

Multiline content uses stdin or file options. Hooks are the final safety net, not a substitute for these gates.
