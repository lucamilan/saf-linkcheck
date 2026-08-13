# 001 · Link rot is structural: the result of an external check is a snapshot, not a property

- **Status:** confirmed
- **Date:** 2026-08-09

From the W3C source and the lesson of iteration 002: external links decay because content gets reorganized, so a positive result today does not guarantee tomorrow; and the network oracle (HEAD with a timeout) is itself volatile. Operational consequence: the external check is to be treated as a dated snapshot — repeatable at low cost (expiring cache) and always optional, never as a stable property of the manuscript.

## Relations
- learned-from → [[iteration:002]]

## Amendments (append-only)
- 2026-08-09 · [docs] · advanced candidate -> confirmed
