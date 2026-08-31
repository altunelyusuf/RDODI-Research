# Handover to BRSF: `Layer_Product` has no functional/non-functional subdivision

**From:** code-abundance-rdodi session (article-review-session)
**Date:** 2026-08-27
**Trigger:** User asked directly whether BRSF distinguishes product scope's functional and
non-functional features the way it distinguishes product scope from project scope. Checked before
answering: it does not. This is filed as a proposal, not a fix — this session has no authority over
`backlog-roadmap-framework`'s own files and has never edited one (verified, no commits from this
session touch that directory).

## What was checked, precisely, before concluding this is real

`backlog_tbox_v1_62_0.ttl`'s `ScopeLayer` class is real and well-grounded:

> "Whether a boundary statement is about WHAT IS DELIVERED or about WHAT WORK IS DONE. PMBOK
> separates product scope from project scope..." — `dcterms:source`: *"PMBOK: product scope
> (features and functions) versus project scope (work required)"*

`owl:oneOf (Layer_Product Layer_Work)` — a closed, two-member enumeration. Searched the entire TBox
for `functional`, `non-functional`, `FURPS`, `ISO 25010`, `quality attribute`: the only hits were
the unrelated OWL reserved term `FunctionalProperty`. No further subdivision of `Layer_Product`
exists anywhere in the shipped vocabulary.

## Why this is a real gap, not a preference, demonstrated against this session's own register

This package's three `Layer_Product`-tagged `ScopeDeliverable`s, read as originally written, are not
homogeneous:

1. *"Research, domain, document, and interactive-page artifacts each pass every gate... re-run and
   verified, not asserted"* — a **verification/reliability** attribute: not a capability the
   artifact has, but a quality claim about how trustworthy it is.
2. *"The Amplitude citation-verification gap, the GitLab-conflict-of-interest note... remain visible
   and unweakened"* — a **transparency/integrity** attribute: also not a capability, a quality claim
   about what the artifact doesn't hide.
3. *"A working HTML page produced via... a real corpus contract... verified per that mechanism's
   five reference checks"* — this one **is** a functional capability: the artifact does a specific
   thing (instantiates a specific pattern with specific mechanisms).

All three currently sit under one undifferentiated `Layer_Product` tag. A framework that can ask
"did every Area get a Goal" (G29) and "did the Scope test every taxonomy cell" (G28) has no way to
ask the parallel, equally real completeness question: *did this scope cover both what the thing
does and how well/safely/transparently it does it* — because it has no vocabulary that distinguishes
the two in the first place. The same class of failure `ScopeLayer` itself was built to catch
("a framework carrying only one of them cannot tell those apart") recurs one level down, inside
`Layer_Product` alone.

## Proposed extension, offered as a starting point, not a mandate

A sibling closed enumeration mirroring `ScopeLayer`'s own pattern exactly:

```turtle
backlog:ProductScopeKind a owl:Class ;
    rdfs:subClassOf backlog:BacklogConcept ;
    owl:oneOf ( backlog:Kind_Functional backlog:Kind_NonFunctional ) ;
    rdfs:label "Product Scope Kind"@en ;
    skos:definition "Within product scope, whether a deliverable names a capability the artifact
        has (functional) or a quality it exhibits while having it (non-functional). A product-scope
        error of the first kind ships the wrong capability; of the second, ships the right
        capability unreliably, opaquely, or unsafely -- the two fail as differently as product and
        work scope already do." ;
    dcterms:source "ISO/IEC 25010: System and Software Quality Requirements and Evaluation --
        functional suitability versus the eight non-functional quality characteristics"@en .

backlog:hasProductScopeKind a owl:ObjectProperty, owl:FunctionalProperty ;
    rdfs:domain backlog:ScopeDeliverable ; rdfs:range backlog:ProductScopeKind ;
    rdfs:label "has product scope kind"@en .
```

Domain restricted to `ScopeDeliverable` (not `ScopeArea`/`ScopeExclusion`, which name places and
work-boundaries respectively, not capabilities-or-qualities) — narrower than `hasScopeLayer`'s own
three-class domain, deliberately, since only a Deliverable makes the kind of claim this axis
distinguishes.

## Verification method, for the owning session to run

1. Confirm `ISO 25010`'s functional-suitability/quality-characteristics split is the right external
   anchor (an alternative, equally defensible: IEEE 830 / ISO/IEC/IEEE 29148's functional/
   non-functional requirement split — this session takes no position on which citation the owner
   prefers).
2. Re-classify this session's own three Deliverables as a first real test case: Deliverable 1 and 2
   as `Kind_NonFunctional`, Deliverable 3 as `Kind_Functional` — a mixed result on real data, not a
   fixture built to pass.
3. Add a completeness shape analogous to `AreaUnmeasuredShape`/`GoalMeasurabilityShape`'s own pattern
   if useful: flag a Scope whose Deliverables are all one `ProductScopeKind`, the way an existing
   advisory already flags a Scope whose Areas and Deliverables sit in a single `ScopeLayer`.
