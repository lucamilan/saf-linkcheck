# 004 · Plan execution: cache of the results of external checks

- **Status:** closed
- **Lane:** fast
- **Area:** scanner, report
- **Nature:** new-feature
- **Date:** 2026-08-09
- **Lesson:** Time is a hidden input: an oracle with a cache is validated by observing what does not happen — the network left untouched — and the 'dalla cache' signal exists precisely to make that non-happening observable.

Executes the loop plan of [[decision:004]]: step 1 the expiring cache in linkcheck.py, step 2 the regression over the whole scope. One step per commit, stop on the contract's triggers.

## Amendments (append-only)
- 2026-08-09 · [park:directional-choice] · Step 1 halfway: the cache has to live somewhere and the plan does not say where. Inside the checked folder it pollutes the manuscript's repository; outside (the user's home) it makes the outcome non-reproducible across machines. Directional choice: the Senior disposes.
- 2026-08-09 · [resume] · The Senior disposes: the cache lives in the checked folder as .linkcheck-cache.json, documented as a file to ignore in Git. The locality of the tool is worth more than reproducibility across machines.
- 2026-08-09 · [new-feature] · ## Telemetria (loop)

- Step 1 — green on the first pass: the second run reads from the cache, outcome unchanged. 1 commit.
- Step 2 — green: regression 1/0/0 over the whole scope. 1 commit.
- Budget: 2 commits used out of 3. Parks: 1 (directional-choice on the location of the cache, resolved by the Senior on resume).
