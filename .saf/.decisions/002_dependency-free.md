# 002 · Dependency-free: standard library regular expression, not a Markdown parser

- **Status:** accepted
- **Date:** 2026-08-09

Link extraction uses a Python standard library regular expression, line by line. Why: the tool is small and must stay installable anywhere without dependency management; a full Markdown parser brings more fidelity but also a maintenance cost that the current scope does not repay. Accepted and declared limit: links split across several lines are not seen.

## Relations
- delivered-by → [[iteration:001]]
