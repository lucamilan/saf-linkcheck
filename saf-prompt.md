# SAF — Persistent Cognition

> Binding project method. The host `CLAUDE.md` supplies project-specific `Area` values and senior context. Record shapes, enums and trailer arity belong to the machine spec: query them with `saf-tools describe`; do not duplicate them here.

## 1. Purpose
Amplify the senior's judgment, never replace it. Work follows:

`READ → THINK → (CODE) → WRITE`

READ and WRITE are mechanical; THINK remains the senior × agent core. Work is complete only when another session can reconstruct purpose, choices, validation and learning from the repository.

## 2. Invariants
1. Significant cognition is persisted under `.saf/` as typed, linked artifacts.
2. The graph is derived from artifacts and git trailers; never maintain a second graph store.
3. Decisions are superseded, not rewritten. Closed work is historical; new product work gets a new iteration.
4. Records are composed through `saf-tools`, not hand-shaped. Use `describe` for the current contract.
5. The senior disposes directional choices, classification and autonomous mandates.
6. Validate the owed result: behavior for implementation, reasoning for analysis.
7. Do not work on `main`; one active iteration per worktree.
8. Kit files, hooks, prompts and skills are vendored machinery: change them only through an approved kit upgrade.

## 3. Session bootstrap
If `.saf/` is missing or incomplete, ask the senior to run `saf-tools init`. Otherwise:

1. refresh through the installed hook or `saf-tools refresh`;
2. inspect `saf-tools present` and resume active work before opening more;
3. **read-through** the graph for project cognition: `recall` (concept, records' own lexicon — hits arrive **graph-expanded**, the 1-hop chain marked `via`) → `get` (content + the **currency footer** — who extends/supersedes it, already enough for a currency check) → `neighbors` only when the full relation graph beyond currency is needed. A node found is not the answer until its currency is seen — `get`'s own footer already shows it. **Declare the outcome** before concluding on any why/what-was-decided question: the typed IDs found, or "nothing pertinent — new surface".

The same discipline binds questions about the **current code**, which is indexed and graphed alongside the cognition: `recall --scope code` locates it, and the code-graph verbs — `code callers|calls|impact|path|hubs` — answer the relations between symbols: who calls this, what a change reaches. Their answer is derived from the graph, so an empty one is a result, not a failed search. Text search over files (grep, glob) is an anchor once the engine has answered, never the opening move. Declare the outcome here too, before concluding that something exists, is unused, or is safe to change.

Both are queried in the language of the records, never the language of the session (§6 owns why): translate the question before firing `recall`, and keep identifiers, file names and quoted output verbatim — they are the anchors that survive the crossing.

Use file or keyword fallback only when the semantic engine is unavailable, and say that retrieval is degraded.

## 4. Iteration lifecycle
An iteration is the atomic work bracket and commit-set.

### 4.1 Open
Before allocating an ID, determine whether the request is a new surface, a follow-up to closed work, or a documentation-only correction. Query existing cognition first. That query also covers reuse: check whether a decision already registers a pattern that applies to the work about to start, and cite it rather than re-deciding it.

Propose a lane, starting from the project's default (`SAF_DEFAULT_LANE` in the host `CLAUDE.md`; `fast` when absent or unreadable):

- `chore`: no record and no ID — work that yields neither a choice nor a lesson, committed under the chore kind, which stays out of `.saf/`;
- `fast`: one iteration with cognition deferred — formalize once at close;
- `complex`: alternatives, invariants or directional reasoning are part of the deliverable; track the steps in a running task list, and keep it working state — the record stays essential.

One test draws the first boundary: is there a choice or a lesson a future session must be able to recover? No — `chore`; yes or uncertain — at least `fast`. Once inside an iteration, default to `complex` when uncertain.

For `fast` and `complex`, also propose purpose, branch, `Area`, `Nature` and validation oracle, then allocate IDs mechanically and open the record through the rail with `Status: in-progress`. The senior disposes: the project default is a starting point, not a ceiling, and is raised or lowered per bracket.

No lane suspends session bootstrap. Retrieval stays live everywhere — a low lane doses what is written, never what is read.

### 4.2 Work
Implement or analyze within the approved purpose. A directional choice discovered during a `fast` bracket is an escalation, not an implicit expansion. A choice or a lesson surfacing during `chore` work escalates it to an iteration **before** the commit; work already committed as a chore that later proves relevant earns a new iteration referencing it, never a rewritten history.

Analysis must compare alternatives and argue a recommendation. Scan and reference pertinent registered sources before concluding.

Once judgment is resolved — the classification, what happened, the direction to take —
the remaining mechanical or exploratory sub-work (formalizing the record, an iterative
edit/verify loop) may run in an isolated execution context so its noise does not inflate
the primary one; a single deterministic step stays inline.

When the same oracle or gate fails twice in one session, that isolation stops being
optional: the engine observes the repetition and says so. Isolate the retry loop or park
the bracket — retrying inline is the expensive case, and its trial and error stays in the
session's context long after the bracket closes. Disposing otherwise is the senior's
call; disposing silently is what leaves the threshold unapplied.

### 4.3 Close
Validate the whole bracket, persist the result and links, record a `Lesson:` even when none was learned, then close through the rail. A closed analysis carries a valid `Outcome` (query `describe --type iteration` for the values) and its required existing target.

Every work commit carries the iteration trailer and approved classification. Backlog and source-capture commits are separate kinds and never mix with iteration commits.

## 5. Autonomous loop
Autonomy starts only when the senior explicitly requests and approves a loop plan.

A complex analysis delivers an immutable plan-decision — a `## Plan (loop)` section containing goal, budget, admitted escalation triggers and numbered steps with machine-checkable oracles (`describe --type plan` for the exact form). Execution uses one `fast` iteration: one step per commit, telemetry in the execution record, and the plan referenced through `Decisions:`.

On repeated oracle failure, exhausted budget, invariant change, directional choice or plan deviation: park and stop (`describe --type trigger` for the exact tokens). The senior then resumes, amends or supersedes the plan, or abandons the work. Never mutate the approved plan merely to track progress.

## 6. Artifacts and graph
Use only typed IDs. Author each relation once, in a `## Relations` block, on its natural side; inverse, application and commit relations are derived. Iterations do not author relation blocks.

External material is registered as a source with provenance, then distilled into knowledge or a decision. Do not silently consume raw input or duplicate an existing provenance.

Records are written in English, whatever language the session speaks — and so are the queries that look for them (§3). This is retrieval, not style: the semantic index behind `recall` embeds with English-only models, so a record in another language is reachable by its exact words and by nothing else, and a question asked in another language than the corpus reaches that lexical channel alone. Identifiers, machine tokens and quoted literal output keep their real spelling — cognition that renames the tool describes a tool that does not exist.

## 7. Quality floor
Engineering taste is project-specific: the senior's priorities live in the host `CLAUDE.md`, which is also where a project states what it will not tolerate. What binds everywhere is the reporting: state what was validated and what remains uncertain. Records are pragmatic, not exhaustive: capture the decision, its why and what changed in the fewest words a fresh session needs — verbosity is not rigor.

**Working when:** a fresh session resumes cleanly, every decision has provenance, every closed iteration has validation and a lesson, and the current graph is recoverable from artifacts plus git.
