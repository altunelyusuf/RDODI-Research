# Proposal to backlog-roadmap-framework: two gaps found running backlog_lineage_completeness against an adopter register

**From:** code-abundance-rdodi session (article-review-session)
**Date:** 2026-08-27
**Trigger:** A direct challenge from the user to prove lineage compliance was actually
comprehensively checked, not just asserted. Auditing which of this framework's ~29 tools had
actually been run against this package's register found only 2 of them ever had. Running a third
(`backlog_lineage_completeness_v1_1_0.py`) surfaced two real findings, both about the tool/data,
not about this package's register.

## Finding 1: LineageLayer data is not shipped where an adopter's tooling can reach it

`backlog_lineage_completeness_v1_1_0.py` requires the ontology to declare `backlog:LineageLayer`
individuals (the 18-row LAYERS table). Running it against this session's register produced:

```
FATAL: the ontology declares no LineageLayer. The layer table was exported at v1.111.0 and this
script reads it rather than holding one.
```

Checked before reporting: `backlog_tbox_v1_62_0.ttl` (the file every adopter loads) contains
**zero** `LineageLayer` individuals. They exist -- 18 of them -- but only in
`backlog_framework_register_abox_v9_8_0.ttl`, this package's own internal working register, which
an adopter has no reason to load. The tool's own `PKG`-relative glob only ever searches
`01-ontologies/backlog_tbox_v*.ttl`, so it cannot find them there either.

**Consequence measured directly:** the tool is currently unusable by any adopter without manually
locating and merging framework-internal data most adopters would not know exists. Verified by
reproducing: it works once the 18 individuals are copied into a local TBox copy, and fails
identically (the exact FATAL above) without that manual step.

**Not proposing the fix myself** (B1/L-110): the natural fix is shipping the LAYERS table in the
shared TBox rather than the framework's internal register, but that's a packaging decision for the
framework's own owner.

## Finding 2: the LAYERS table's "fails at level" tier does not match at least one current shape's actual severity

Once the data gap above was worked around, the tool reported (against this session's fully L2-
conformant register): `MetricObservation -- fails at L2`.

Checked directly against `backlog_shacl_v1_72_0.ttl`: the shape enforcing an Objective's
`MetricObservation` (`backlog:MetricObservationShape`'s consumer, the L2572 constraint quoted
below) fires at **L4**, not L2:

> "L4: this objective has no MetricObservation against it... At L4 an objective must have been
> measured at least once, whatever the reading said."

This session's register genuinely, correctly reports 0 violations at its declared L2 level with no
`MetricObservation` present -- confirmed by running `backlog_validate_v1_4_0.py` directly. The
completeness tool's tier annotation for this layer is stale relative to the shapes file it should
be describing.

**Scope of the check performed, disclosed rather than overstated:** only `MetricObservation` was
verified byte-for-byte against the shapes file's actual severity (spot-checked, not exhaustive
across all 9 "absent" layers this tool reports). `hasEvidence`'s referential-integrity clause was
also checked and found to be L1, consistent with the tool's framing there. The other 7 tier claims
were not individually re-verified against `backlog_shacl_v1_72_0.ttl`'s actual severities in this
session; this proposal states what was checked and not more.

**Not proposing the fix myself**, same reasoning as Finding 1: reconciling the LAYERS table against
the shapes file (or generating it from the shapes file directly, removing the duplicate source of
truth) is this package's own decision.
