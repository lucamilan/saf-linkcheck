# 005 · linkcheck v3: verification of internal anchors (#section) in links between files

- **Status:** closed
- **Lane:** fast
- **Area:** scanner, report
- **Nature:** new-feature
- **Date:** 2026-08-09
- **Lesson:** The anchor is a contract with the renderer, not with the filesystem: the verification is worth something only if it replicates the algorithm the reader will see (GitHub), accents included. The fixtures with accents and duplicate headings are the oracle that holds this fidelity steady.

Promotion of BL-001: the target of an internal link is verified as a section too, not only as a file. The anchors are computed from the headings of the target file and compared with the fragment; missing anchor = new error type in the report, non-zero exit code. Oracle: test suite (valid anchor passes, missing anchor fails, links without a fragment unchanged, regression green).
