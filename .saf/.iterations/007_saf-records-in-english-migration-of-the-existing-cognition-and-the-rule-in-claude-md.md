# 007 · SAF records in English: migration of the existing cognition and the rule in CLAUDE.md

- **Status:** closed
- **Lane:** fast
- **Area:** cognition
- **Nature:** docs
- **Date:** 2026-08-13
- **Lesson:** A cognition corpus can be translated, but only down to where prose ends and the contract begins: the loop-plan tokens are regex-matched from contract.toml and the NNN_ prefix resolves the node, so the slug is free and the prefix is not. The boundary is not a matter of taste — reading the machine contract first is what keeps a translation from silently unparsing the records it rewrites.

The .saf/ records were written in Italian. The semantic backend behind saf-tools recall indexes and retrieves English optimally, so an Italian corpus degrades read-through — the retrieval leg of READ -> THINK -> (CODE) -> WRITE. This bracket translates every existing record (decisions, iterations, knowledge, source, backlog) to English, renames the files to English slugs keeping the NNN_ prefix that resolves the nodes, states the rule in CLAUDE.md for records yet to be written, and rebuilds the mimir docs collections from scratch so the renamed files leave no orphan chunks. Oracle: saf-tools audit clean, get/present resolve every node after the rename, and a recall in English hits the translated records.
