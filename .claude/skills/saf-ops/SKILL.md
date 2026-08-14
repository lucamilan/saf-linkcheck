---
name: saf-ops
description: Read and maintain SAF operational state through five modes — retrieve, health, sal, conscience and groom. All use `saf-tools`; only groom changes persistent SAF content.
---

# SAF operations bench

Invoke as `/saf-ops <retrieve|health|sal|conscience|groom>`. Prefer facade commands over reconstructing state from raw `.saf/` files. When semantic retrieval is unavailable, use the remaining structural or keyword commands and report degraded coverage.

## retrieve
*(named `retrieve`, not `memory` — that name is taken by the `saf-tools memory` verb (decisions in force). This mode is neither; it's the general lookup guide.)*

Refresh when needed, then choose the cheapest query:
- meaning: `recall`; active work: `present`; in-force decisions: `memory`;
- exact text: `search`; node/edges: `get` / `neighbors`;
- structure: `chains`, `applies`, `relations`, `nodes`, `orphans`, `pending`;
- provenance between two nodes, or around one: `path`;
- history/code: `history`, `outline`, `peek`, `code`.
Judge pertinence; do not infer relevance from hit count.

`recall` defaults to `--scope cognition` — the `.saf/` doc graph only, never the codebase.
When a question might be settled by current code rather than by prior decisions (e.g. "does
X already work like Y", "is this implemented"), pass `--scope code` or `--scope all`
explicitly, or run a separate code search — a cognition-only miss is not "nothing pertinent".

`path` answers provenance, not connectivity: it walks chains that keep a single currency
direction, so `no provenance chain` is an **answer** — the two nodes are unrelated *in that
sense*. Two nodes under a common parent are connected without either descending from the
other, and that shape is not walked. Neighborhood mode is bounded twice, in hops and in
size, and says what it left out.

For relations between symbols, `code callers|calls|impact|path|hubs` beats any text search: they
resolve over the call graph, so `no callers found` is an **answer** (nothing calls it), not a
miss to double-check by grepping. Use `recall --scope code` to locate a concept, the `code`
reports to qualify it — is this dead, who breaks if I change it — and grep only to anchor an
exact string or to reach what the index does not cover.

`backlog` carries both halves: bare it **lists** the registered entries (`--all` to reach the terminal archive too), and with `--id`/`--title` it composes a new one on the write rail. Enumerate the negative space through the verb, never by reading the backlog file — the raw read is the anchoring stage, not the way to ask what is open. For any other unfamiliar verb, `saf-tools describe --type T` / `<verb> --help` before invoking it: a verb's name does not settle whether it reads or writes.

## health
Read-only operational snapshot. Lead with `healthy`, `degraded` or `attention`, based on:
1. indexing/backend status (`status`) and a liveness check;
2. artifact counts, open work and graph hygiene;
3. recent history;
4. summarized method telemetry from `stats` — sessions/verbs, and (iteration:193) the
   feedback-cycle axis: `cycles` (recovery rate, latency p50/p95/max, recidiva, escape
   rate — each with its denominator, never a bare percentage), `gaps` (sessions missing
   SessionStart/SessionEnd) and the `anomalies` list `stats` already derives from
   both. A non-empty `anomalies` list is itself the `attention` trigger for this axis —
   read it, don't re-derive the thresholds. Pass `--by-kit-version` when comparing the
   method's behavior across a kit upgrade.
5. what the ceremony costs, when that is the question asked: `stats --by-lane` answers it in
   one call — spend per bracket by lane and how much of it is the read bootstrap — with
   `--brackets` (cost joined to outcome, per iteration) and `--turns` (where the context
   grows, turn by turn) for the detail behind it. Each of the three prints that view and
   nothing else. Two figures are labelled and must stay labelled when reported: `active`
   (input+output+cache_creation, what a bracket spends) is not `drag` (cache_read, a context
   already paid for and re-read every turn), and the bootstrap `proxy` share is an estimate
   from `out_chars`, never a measure. A lane with no bracket yet makes the comparison
   unanswerable, which the answer line says outright — do not fill the gap with the lanes
   that do have data.
Report remedies (`stats`'s own anomaly lines already read as recommended actions) but do
not execute them.

## sal
Build `done / doing / will-do candidates` from recent closed work, `present` and open backlog. Cite typed IDs internally; omit them for client prose. Never turn backlog entries into commitments.

## conscience
Run the coherence critique and separate soft findings from hard audit failures. Findings are proposals for senior disposition, never blockers by themselves. Requested reports live outside `.saf/`.

**Fixing what these two modes surface.** A finding that resolves into a safe mechanical patch
is committed under the **chore** kind — no iteration, no lane to weigh: apply it and move on.
Ceremony returns only when the fix carries a choice or a lesson, which escalates it to an
iteration before the commit. The chore's own contract limits — what it may stage, and when it
is refused — belong to `/saf`; read them there rather than from a copy that can drift.

## groom
The only persistent-writing mode. Scope: backlog hygiene.

**Backlog:**
1. Run format lint, duplicate-ID checks, conscience and audit.
2. Propose any semantic consolidation or revival to the senior.
3. Apply only lossless, contract-valid maintenance; preserve IDs, rationale and graph meaning
   (`link` retrofits a missing edge; `fmt-lint --fix` normalizes headings).
4. An item the senior turns terminal (`promoted`/`dropped`) moves out of `BACKLOG.md` into
   `.saf/.roadmap/BACKLOG_PROMOTED.md` (decision:065) — `BACKLOG.md` holds only `open` items.
   No archive file yet: create it with its own header, then append the stub. Archive already
   exists: append only, never rewrite what's there. Citations stay resolvable either way —
   the engine reads both files.
5. Commit using the machine-defined backlog contract (`Roadmap:` trailer); never mix external
   reports into that commit.

Listing under this mode is read-only — `groom` is a mode of this skill, not a `saf-tools` verb.
Process lifecycle and ordinary commits belong to `/saf`, not this skill.
