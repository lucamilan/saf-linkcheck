---
name: saf-migrate-lang
description: Migrate an existing `.saf/` corpus written in another language to English, the language the semantic index can actually read. Opt-in and senior-disposed — the method's language rule binds new records, never past ones. Invoke as /saf-migrate-lang when a project's records predate the rule and the senior wants the retrieval gain. Covers what to translate and what to leave alone, which fields are prose and which are contract, and runs the harness that proves the migration lost nothing.
---

# Migrating a corpus to the language of retrieval

Invoke as `/saf-migrate-lang`. One instance, one bracket, senior-disposed.

The method asks for records in English for one reason: the semantic index behind `recall` embeds
with English-only models. A record in another language is reachable by its exact words and by
nothing else — the hybrid search silently collapses to its lexical channel, and answers worse
without ever saying so.

That rule binds what a project writes **next**. A corpus that predates it is never migrated
automatically, and migrating is not owed. This skill is the path for a senior who wants the gain
on a corpus already in production.

## Decide first whether it is worth it

Two measurements exist, and the smaller one is the honest one. On a **parallel corpus of 31
documents** — identical content, two arcs differing only in language — recall@5 went from 13/21 to
19/21. Repeated on the **live corpus of ~394 indexed files** after the migration actually shipped:
9/21 before, 12/21 after. Same queries, same configuration; the difference between the two pairs
is corpus size, not language. Size turned out to be the dominant term.

Both runs agree on where the gain lands: the **paraphrased** and **vague** query families
(on the live corpus 1/7 → 3/7 and 1/7 → 2/7). Exact-word queries scored 7/7 in every arc ever
run — the lexical channel has no opinion about language.

So: if the corpus is only ever queried with the words already written in it, the migration buys
little. If it is queried by concept — *why did we decide this*, months later, in different words —
it buys a third of the queries the read layer exists for, and nothing else on offer buys them.

**Mid-migration, and after it, queries are asked in English.** The third arm of the same
measurement is the one to know before starting: questions asked in the old language against a
migrated corpus scored **4/21** — below the 9/21 the corpus scored before any of this began, with
the paraphrased and vague families at zero. A half-migrated corpus is not a half-gain, it is two
corpora; finish the pass, and ask in English from the moment it starts.

Two caveats worth stating to the senior before starting. The measurements' translations and
queries were written by the same author, which aligns vocabulary more than real use would; and a
corpus born in English is not the same thing as a translated one.

## Scope — which records

| Records | Action | Why |
|---|---|---|
| decisions | translate — first | the *why*, and what a future session searches for by paraphrase |
| knowledge | translate — second | distilled concepts, reached by vague queries |
| sources, roadmap | translate — third | short, cheap, completes the queryable surface |
| closed iterations | **leave** | the historical log; closed work is not rewritten |
| the iteration in progress | close it first | rewriting a bracket mid-flight muddies its commit set |

Decisions and knowledge alone take most of the gain. On a tight budget, stop there.

**The partial pass on closed iterations** — their titles and `Lesson:` lines only, everything
else left alone — is a deliberate exception the senior may dispose, and it is worth less than the
figures above. Measured on a corpus of roughly 2000 indexed files: of four probes phrased as
paraphrases of closed brackets, two moved (one from absent to rank 2, one to first on its own
lesson) and two did not. The reason is structural and predictable — the `Lesson:` is one chunk
while every other chunk of the same record stays in the source language, so the record goes from
unreachable to reachable, not to reliably first. If you later weigh translating those bodies too,
weigh them against this number and not against the full-migration figures. Such a pass needs
`--allow-holds` on both `rename` and `verify`.

Outside `.saf/` nothing is touched: the host `CLAUDE.md`, the language the session speaks, and
editorial or user-facing content are not the method's business and never were.

## Fields — what moves and what must not

**Moves:** the title, and the body prose — context, decision, consequences, alternatives,
amendments.

**Must not move:**

- the `## Relations` block — authored edges are contract, not prose;
- typed citations and backlog ids, in count as well as in identity;
- header field **keys**, and the short values under them: status, date, area, nature, outcome,
  lane, provenance. A `Lesson:` is the exception — that one is prose;
- the id prefix of a filename;
- identifiers quoted inside prose: flags, file names, literal command output. Cognition that
  renames the tool describes a tool that does not exist;
- the machine tokens of the autonomous-loop plan form — its heading, its contract field, its step
  keywords are matched by regex from the kit's own contract. Only the text *inside* them is
  translated, and an approved plan is never edited merely to improve it.

**Re-slug the filename from the new title**, keeping the id prefix, and move it with `git mv`.
The harness does this; do not do it by hand.

## Procedure

Open a bracket first — this is product work with a directional choice in it, and `/saf` governs
how it opens and closes. Then, from the instance root:

```
python .claude/skills/saf-migrate-lang/migrate_lang.py plan
```

**1 · plan.** Inventories the corpus by type: how many records, how much text, which files read
as non-English, and what the policy above says to do with each. The language verdict is a
stopword ratio — it orders the work, it does not judge a record. Files carrying a loop-plan form
are flagged, because those are the ones with machine tokens inside.

**2 · snapshot — before any edit.**

```
python .claude/skills/saf-migrate-lang/migrate_lang.py snapshot
```

Freezes the pre-translation state: per file its citations with multiplicity, its relations block,
its header fields and a digest; globally the graph size and the coherence signal count. Nothing
downstream works without this. If the facade is not on `PATH`, pass `--saf-tools "<how to call
it>"`; without it the global invariants are skipped and the harness says so.

**3 · translate, and condense while translating.** In batches, by type, in the priority order
above. Condensing is half the value: records are pragmatic, not exhaustive, and a translation
pass is the one moment the whole corpus is being read anyway. Keep the identifiers and the
machine tokens exactly as they are spelled.

**4 · rename.** Dry run first, then apply:

```
python .claude/skills/saf-migrate-lang/migrate_lang.py rename
python .claude/skills/saf-migrate-lang/migrate_lang.py rename --apply
```

Held types are skipped: their titles were not supposed to change. If they did change, deliberately
and under `--allow-holds`, pass the same flag here so the address follows the title — a filename in
the old language over an English title is the one state nobody disposed.

The flag authorizes the held records **this pass edited**, compared against the snapshot — never
the whole type. A closed record the translation never opened keeps its filename however far that
name has drifted from the current slug convention: re-addressing history nobody touched is what
the hold policy is for. The count of those is printed, so a narrowing is never silent.

**5 · verify.**

```
python .claude/skills/saf-migrate-lang/migrate_lang.py verify
```

Blocking findings are defects, not opinions — resolve them before committing. Two flags exist for
deliberate exceptions: `--allow-holds` accepts an edit to a held record type, and
`--strict-counts` turns a changed citation multiplicity from a warning into a blocker (use it
when the pass was a pure translation with no condensing).

**6 · rebuild the read layer** with `saf-tools refresh --force`, then spot-check: run two or three
`recall` queries phrased the way you would actually ask them, not with the words in the records.
That is the thing the migration was for. If the backend serves more than this project, prune by
path and never by title — the store is shared.

**7 · commit and close.** One migration commit set, the bracket's own trailer, and a lesson.

## What verify proves, and what it does not

It proves the migration was **lossless**: no citation gained or lost, no relation moved, no
contract field translated, no record silently dropped, the graph the same size it was. That is
the half a reader cannot check by reading.

It says nothing about whether the translation is *good*. Nobody but a reader can.

## The defect to expect

On the first migration of this kind the prose came out fine and the graph nearly did not. The
translators wrapped bare id mentions in citation brackets — minting edges the record never
authored — and dropped a few real ones. Both are invisible on reading and both are exactly what
`verify` blocks on. Expect it, and repair against the snapshot rather than by memory.
