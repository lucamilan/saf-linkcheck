# 002 · linkcheck v2: optional checking of external links

- **Status:** closed
- **Lane:** fast
- **Area:** scanner, report
- **Nature:** new-feature
- **Date:** 2026-08-09
- **Lesson:** A HEAD request with a timeout is not a perfect oracle: some sites refuse HEAD or answer intermittently. The external check stays indicative and optional; the manuscript's real oracle remains the deterministic internal check.

Purpose: the Senior disposes that external links be included in the check. Inclusion happens behind the --esterni option: the default behavior stays deterministic and network-free. Verification uses urllib from the standard library, consistent with the decision on the absence of dependencies. Validation oracle: on a fixture with a nonexistent external domain (.invalid) and a reachable one, with --esterni the tool reports only the first; without --esterni it exits with 0 as before.
