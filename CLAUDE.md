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

**linkcheck** — a command-line tool that validates the links of a Markdown
manuscript: internal links between files, anchors, images. Born for the manuscript
of «Il Senior amplificato»; it must stay small, deterministic and usable in CI.

Senior profile: `Luca — simplicity, determinism, few justified dependencies`.

**`Area`** enum (where in the system — project-specific, extensible on proposal):

- `scanner` — reading the Markdown files, extracting and classifying the links
- `report` — the outcome of the check: output format, exit code, CI integration
- `cognition` — the `.saf/` records themselves: form, language, indexing and retrieval

<!-- AREA_ENUM: scanner report cognition -->

**`Nature`** enum (universal): `new-feature · bug · refactor · resilience ·
performance · security · docs · analysis`.

**Default lane** — which lane the agent's proposal starts from when you don't classify the
work yourself (§4.1). Ships as `fast`: SAF stays the rule, and exempting a project is an
explicit local choice.

<!-- SAF_DEFAULT_LANE: fast -->
