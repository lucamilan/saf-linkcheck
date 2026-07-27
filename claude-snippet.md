# Snippet for the host project's CLAUDE.md

> **Install = two steps:** put the **`saf-tools`** binary in a global location on your
> `PATH` (no python needed), then run **`saf-tools init`** in the project root (a git
> repo). It materializes the whole kit — this prompt, the `.saf/` cognition seed, the
> hooks, the `saf*` skills, `.claude/settings.json` — wires `core.hooksPath`, and creates
> `CLAUDE.md` from the block below if the project has none (otherwise: paste the block
> yourself). The agent **scaffolds nothing**; on first run it reads the installed `.saf/`
> and asks you to fill the `<...>` parts.
>
> The seed includes the kit **sentinel** `.saf/.kit/VERSION` (stamped with the installed
> kit version), which **arms** the consumer freeze: the `pre-commit` refuses hand-edits to
> the vendored machinery (this prompt, `.githooks/`, `.claude/skills/saf*`,
> `.claude/settings.json`) — the method changes only by re-deploying a newer kit:
> **`saf-tools init --force`** (never touches your `.saf/`). Measure drift with
> **`saf-tools init --check`** — it also runs by itself at every session start (a
> `SessionStart` hook in the shipped settings, warn-only: it reports, never blocks).
> Intentional override is explicit and tracked (`git commit --no-verify`).

---

<!-- ▼▼▼ PASTE FROM HERE ▼▼▼ -->

# SAF method (imported)

@saf-prompt.md

> The method above is **binding**. The project's live state lives in `.saf/`.
> To enable formal commit validation: `bash install-hooks.sh`
> (or `git config core.hooksPath .githooks`).
>
> The kit includes the **`saf*` skill family** (`.claude/skills/`): `saf` (process guardrail —
> the third pillar; invoke at open/close of each iteration) and `saf-ops` (operations bench,
> five modes: `/saf-ops retrieve|health|sal|conscience|groom`). Copy `.claude/skills/` with the kit.
>
> **Read-through (§3).** When the project ships the SAF **query engine**, the agent **queries it
> instead of reading raw `.saf/`** (`saf-tools present` stays direct; files are write-target +
> fallback). The facade is the **`saf-tools`** binary, **CLI only** — one verb per capability, no
> resident server (the MCP transport was retired):
>
> ```
> saf-tools present · recall · search · get · neighbors · history · next-id
>           record · close · amend · supersede · commit · backlog · describe
>           refresh · status · outline · peek · code · audit · conscience · telemetry · stats
> ```
>
> The kit's `.claude/settings.json` (copied to the repo root) ships the Claude wiring: the
> `Bash(saf-tools:*)` allowlist (zero permission prompts), `SessionStart` hooks running
> **`saf-tools refresh`** and the kit drift check (**`saf-tools init --check --warn`**),
> and session telemetry (**`saf-tools telemetry`** on `SessionStart`/`Stop`/`SessionEnd`):
> a local, gitignored JSONL (`.saf/.cache/telemetry.jsonl`) of sessions and tokens spent —
> never leaves the machine and **OFF by default**: the hooks ship, the switch does not.
> Opt in per project with an `env` block (`"SAF_TELEMETRY": "1"`) in your
> `.claude/settings.local.json`; read the summary with **`saf-tools stats`**. Prerequisites: **git** installed, repo is a **git repository**, the
> **`saf-tools`** binary on `PATH` (no python needed — it's a single compiled binary). No engine →
> read `.saf/` directly (graceful degradation). Name your project's concrete engine under `## Project`.
>
> **Optional semantic/code backend.** `saf-tools recall` (by meaning) and the code verbs
> (`outline`/`peek`/`code`) are powered by a swappable local index backend behind the facade.
> Just make the backend resolvable: **put it on `PATH`** (the normal case) or, as a fallback, set
> **`SAF_MIMIR_BIN`** to its binary in your **local** settings (`.claude/settings.local.json` — never
> committed; that's where machine-specific paths belong). Run `mimir project init` once and commit the
> `.mimir` marker for a stable cross-machine id. Without a backend, `recall` falls back to keyword,
> the code verbs report unavailable, and the hook is a safe no-op (graceful). `SAF_NO_BACKEND=1` forces it off.

## Project

Senior profile: `<name, priorities — e.g. resilience, robustness, observability>`.

**`Area`** enum (where in the system — project-specific, extensible on proposal):

- `<area-1>` — `<what it covers>`
- `<area-2>` — `<what it covers>`

<!-- AREA_ENUM: <area-1> <area-2> -->

**`Nature`** enum (universal): `new-feature · bug · refactor · resilience ·
performance · security · docs · analysis`.

**Default lane** — which lane the agent's proposal starts from when you don't classify the
work yourself (§4.1). Ships as `fast`: SAF stays the rule, and exempting a project is an
explicit local choice.

<!-- SAF_DEFAULT_LANE: fast -->


<!-- ▲▲▲ UP TO HERE ▲▲▲ -->

---

Note: the `<!-- AREA_ENUM: ... -->` line is the **hook-readable source of truth**: keep
it aligned with the `Area` list above. It is the only place where `Area` values must be
written for validation.

Note: the `<!-- SAF_DEFAULT_LANE: ... -->` line is how you **dose the method for this
project** — one of `chore | fast | complex`, read by the agent before it allocates an id.
Absent or unreadable, it falls back to `fast` (nothing breaks on an older `CLAUDE.md`).

- `fast` (shipped) — every bracket gets an iteration; the record is written **once at
  close**, not per step. SAF is the rule.
- `complex` — the agent argues alternatives by default. For repos where nearly all work is
  directional; rarely the right project-wide setting.
- `chore` — **SAF becomes the exception.** The agent works, commits with a `Chore:` trailer
  and stays quiet. No record, no id, no ceremony. Pick this on a high-frequency repo where
  most commits are routine (targeted fixes, mechanical refactors, obvious tests, bumps,
  config tweaks) and iteration records would be noise that dilutes the significant ones.

Lowering it silences the **write rail only** — never the read layer. Whatever the lane, the
agent still refreshes and queries the graph before concluding: that part
is nearly free (cached context) and it *is* the amplification. "Quiet" means ceremony on
demand, not a graph you stopped consulting.

Two guarantees make a low lane safe:

- **Promotion on the spot.** The moment work produces a directional choice or a lesson a
  future session would need, the agent escalates to `fast` **before** committing — it does
  not quietly file it as a chore. The test is one question: *is there a choice or a lesson
  a future session must be able to recover?*
- **You can always override per bracket.** The marker sets the *default*, not a ceiling:
  "register this one" opens a full iteration on a `chore` project, and "keep this quiet"
  does the opposite. The senior disposes (invariant 5).

Promotion is prospective, never retroactive: work already committed as a chore that later
turns out to matter earns a **new** iteration referencing it — the history is not touched.
