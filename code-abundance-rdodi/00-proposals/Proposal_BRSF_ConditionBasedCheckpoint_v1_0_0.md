# Proposal to backlog-roadmap-framework: ObjectiveCheckpoint needs a condition-based form

**From:** code-abundance-rdodi session (article-review-session)
**Date:** 2026-08-27
**Trigger:** Adapting this package's lineage to discipline v7.0.0. G31 (*"'when to measure' is a
condition, not a fabricated date, unless the timing is genuinely calendar-bound"*) directly
describes a defect this session was about to commit: an `ObjectiveCheckpoint` with a calendar date
invented for `ObjRDODIDefaultGatesPassing`, whose real timing depends on when Story 1 (an
engineering task with no calendar commitment) closes — not on any date.

**Checked before proposing:** `backlog_tbox_v1_62_0.ttl`'s `ObjectiveCheckpoint` class carries only
`checkpointDate` (`xsd:dateTime`) and `expectedValue`. No condition-based alternative exists.

**Resolution taken here:** removed the fabricated checkpoint rather than keep false precision (not
required at this package's declared L2 level). Not proposing new vocabulary myself — this package
is owned by another session lineage (B1), and L-110 governs against minting on single-producer
evidence.

**What a condition-based form might look like**, offered as a starting point rather than a
demand: a sibling class or an alternative property on `ObjectiveCheckpoint` — e.g.
`checkpointCondition` (range `WorkItem` or `xsd:string`) alongside `checkpointDate`, so a checkpoint
can read *"expected once STORY-1 reaches Done"* as a first-class fact instead of an invented date
standing in for it. Left as a proposal, not a request, since the right shape is a judgement for the
framework's own owner.
