# 004 · Expiring cache for the results of external checks (loop plan)

- **Status:** accepted
- **Date:** 2026-08-09

Checking external links stays optional but becomes repeatable: results are kept in an expiring cache next to the checked folder, so two runs close together do not query the network twice. The scope without --esterni does not change. The decision is motivated by the knowledge distilled on link rot and by the limits of the network oracle that surfaced in iteration 002. Promotes BL-002.

## Piano (loop)

- **Contratto:** promote BL-002 — cache of the results of external checks · budget: 3 commits · trigger: oracle-failure-repeated, directional-choice
- 1. Expiring cache of external results in linkcheck.py — oracolo: two runs with --esterni on fixture-esterni (verde = the second one prints 'dalla cache' for every external link and the outcome does not change)
- 2. Regression over the whole scope — oracolo: broken fixture, healthy fixture, fixture-esterni without the option (verde = exit 1, 0, 0 in that order)

## Relations
- informed-by → [[knowledge:001]]
- delivered-by → [[iteration:003]]

## Amendments (append-only)
- 2026-08-12 · [docs] · Correction disposed by the Senior on the location of the cache. The body of this decision writes «next to the checked folder»; the plan, the disposition recorded on resuming from the park and the implementation put it inside the checked folder, as .linkcheck-cache.json. The implementation prevails: the cache sits inside. The body stays as it was written, because the history of the imprecision is itself a trace.
