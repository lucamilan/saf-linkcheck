# Backlog

> **Negative space**: features and decisions **deferred over time**. Each entry has a
> `BL-NNN` id and may be promoted to an iteration or decision, leaving a trace of the
> deferral. A commit touching only this file: trailer `Roadmap: BL-NNN`.

<!-- Format: ### BL-NNN · title / Status: open | promoted | dropped / Note -->

### BL-003 · Verification of #section fragments within the same file
- **Status:** open
- **Note:** Limit accepted in [[decision:005]] and not yet tracked: #section fragments without a path stay out of scope, but a manuscript uses them in the internal indexes of the chapters. The anchor algorithm already exists ([[iteration:005]]): applying it to the current file closes the gap with the same fixture oracle, without new dependencies.