# 001 · linkcheck v1: checking the internal links of the manuscript

- **Status:** closed
- **Lane:** fast
- **Area:** scanner, report
- **Nature:** new-feature
- **Date:** 2026-08-09
- **Lesson:** A scope exclusion has to be validated, not merely declared: the healthy fixture deliberately contains an external link, so the oracle proves the exclusion works instead of taking it for granted.

Purpose: first working tool that walks the Markdown files of a folder, extracts the links and reports the broken internal ones (missing target file). v1 scope: relative links between files; external HTTP links excluded. Validation oracle: run on a fixture with a known broken link, the tool lists it and exits with code 1; on a healthy fixture it exits with code 0.
