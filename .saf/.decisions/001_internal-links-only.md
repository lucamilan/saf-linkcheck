# 001 · Internal links only: external HTTP links stay out of scope

- **Status:** superseded
- **Date:** 2026-08-09

> **Superseded by [[decision:003]]** (2026-08-09)

linkcheck validates only internal targets (relative paths between files). External links are recognized by their prefix (http, https, mailto) and skipped. Why: the oracle must stay deterministic and the tool must run in CI without a network; an HTTP check introduces outcomes that depend on the moment (timeout, 429, DNS) and turns a check of the manuscript into a check of the network. Alternative considered and deferred: HTTP verification behind a dedicated option, with timeout and a result cache.

## Relations
- delivered-by → [[iteration:001]]
