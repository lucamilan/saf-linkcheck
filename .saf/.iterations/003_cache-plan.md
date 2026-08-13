# 003 · Analysis: promotion of BL-002, cache of external results

- **Status:** closed
- **Lane:** complex
- **Area:** scanner, report
- **Nature:** analysis
- **Date:** 2026-08-09
- **Outcome:** implemented
- **Lesson:** A plan executable autonomously is born from an analysis that compares alternatives, not from a list of things to do: the contract (budget and triggers) is the part that makes the loop stoppable, the steps are the easy part.

Question: the external check introduced in iteration 002 is volatile (network, imperfect HEAD) and the registered W3C source shows that link decay is structural, not occasional. Is it worth promoting BL-002 to work executable in a loop? Alternatives compared: (a) leave the external check as it is, volatile but simple; (b) an expiring cache of the results, repeatable and gentle towards the sites; (c) move the external check into a separate service, out of scope for a single-file tool. Recommendation: (b), executed in an autonomous loop with small steps and mechanical oracles.

## Amendments (append-only)
- 2026-08-09 · [analysis] · The analysis delivers the loop plan recorded in [[decision:004]], which promotes BL-002.
