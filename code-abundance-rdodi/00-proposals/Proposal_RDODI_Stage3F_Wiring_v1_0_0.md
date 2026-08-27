# Proposal to RDODI: Wire Stage3.F (Reference Rule), and Disambiguate It from Stage3.G

**From:** code-abundance-rdodi session (article-review-session)
**Date:** 2026-08-27
**Status:** PROPOSAL, not an edit (B1: rdodi-ecosystem is owned by another session lineage; this
session found the defect while consuming the pipeline, and is proposing the fix for the owning
session to apply, per the OE Operating Discipline's B1 boundary).
**Severity:** Medium-high -- the same class of defect CHANGELOG_v1_95_0.md already fixed once for
Stage1.B, now found recurring at Stage3.F, plus a distinct, real user-facing confusion it caused.

---

## The real problem

Two separate defects, discovered together while running a real subject through the pipeline and
having a user directly question a reported number.

### 1. Stage3.F has no orchestration slot -- but unlike Stage1.B, a slot alone won't fix it

`RDODI_FourStage_Pipeline_Procedure_v1_2_1.md` names Stage3.F in its own gate table (SS4.4):
*"every external claim cited, every citation BP-D41-verified or flagged, no dangling citations."*
Confirmed by reading `rdodi_pipeline_validator_v1_5_0.py`'s `validate()` directly: it calls
Stage3.A, Stage3.B, Stage3.E.cov, Stage3.E.sub, Stage3.src -- **never Stage3.F.**

This looks identical to the Stage1.B gap CHANGELOG_v1_95_0.md already found and fixed ("the gate
the procedure's own table claims exists had no orchestration slot, not even a skipped one"). It is
not identical underneath: Stage1.B just needed `gate_shacl()` called with an existing SHACL file --
trivial wiring. Stage3.F is different: `02-gates/reference_rule_gate_v1_0_0.py` **already exists,
is already correct, and already has a passing adversarial test** (`reference_rule_adversarial_test_v1_0_0.py`,
verified by re-running it, 6/6 checks pass). But `reference_rule()` takes **structured Python
data** (`refs: [{id, status}]`, `claims: [{text, needs_cite, cites}]`) -- and **no code anywhere in
the repository extracts that shape from a TTL document ABox.** The gate has been fully built and
tested in isolation since it was authored, and has never been reachable from a real pipeline run,
because the bridge between "a Stage 3 document" and "this function's input" was never written.

### 2. Stage3.G was mistaken for Stage3.F's answer -- by both a downstream user and this session

Stage3.G (`"≥25% of substantive paragraphs carry in-line (Surname, Year) citations"`) is a
retained, narrow floor: a real *reference number* (not a count target), but only for one specific
citation *form* -- parenthetical. This session's own Stage 3 report cited Staples (2026) in
**narrative** form (`"Staples (2026) argues..."`) in roughly half its sections and in
**parenthetical** form (`"(Gray, 2026)"`) in the other half. Both are equally valid citations. But
because Stage3.F was silently absent, this session reported Stage3.G's 50% as if it answered the
completeness question -- until the user asked, correctly, "how can 50% pass if all resources
should be cited?" A manual re-audit then found Stage3.G's number was itself an undercount (missing
narrative-form citations entirely), *and* surfaced one real dangling reference (a section reading
"the article's argument" without naming the article in that paragraph) that no gate had caught.

Both defects compound: because Stage3.F never ran, there was no second, correctly-scoped number
to catch the confusion Stage3.G's narrow floor invites.

---

## Concrete instance (this session, verified by running)

- `code_abundance_document_v1_0_0.ttl`, section "Industry Implementation": prior text read *"Four
  concrete, named systems anchor **the article's argument**"* -- no citation marker of either form.
  Caught only by a user's question and a manual re-read, not by any gate.
- Corrected to name Staples (2026) explicitly; the REFERENCE_ONLY bridge below now reports the
  corrected document PASS and the pre-fix text FAIL, proving the gate (once reachable) would have
  caught this without a user needing to ask.

---

## Proposed systemic fix

**(a) Write the missing TTL-to-`reference_rule()` bridge and wire it as Stage3.F.**
A worked, tested starting point is attached at
`code-abundance-rdodi/00-proposals/REFERENCE_ONLY_stage3f_ttl_bridge_v1_0_0.py`
(explicitly labeled REFERENCE_ONLY -- NOT_A_RELEASE, per B1). It:
  - Extracts `refs` from a Stage 1 research ABox's `res:Publication` individuals.
  - Extracts `claims` from a Stage 3 document ABox's structural individuals, detecting citation
    markers in **both** narrative (`Surname (Year)`) and parenthetical (`(Surname, Year)`) form.
  - Verified against this session's own document: **PASS** on the corrected version, **FAIL**
    (correctly, adversarially) when the pre-fix "Industry Implementation" text is substituted back
    in (`1 external claim(s) uncited`).
  - **Known, disclosed simplification**: `cites` maps any detected marker to the primary source's
    ref id rather than resolving which specific Publication each marker names -- enough to exercise
    Stage3.F's "uncited" dimension (this proposal's actual finding) but not its "dangling citation"
    dimension. A real per-claim citation-attribution parser is follow-on work, not solved here.

**(b) Give Stage 1 Publications a machine-readable status, not only prose.**
This session's Stage 1 research artifact already disclosed two figures (Amplitude's bug-count and
PR-cycle-time claims) as unverifiable, but only as free-text inside a `skos:note` quality
scorecard. For (a)'s `refs[].status` to be more than a hardcoded `"verified"`, Stage 1's
`res:Publication` individuals need an actual status property (`verified` /
`unavailable_flagged` / `unverified`) that BP-D41 verification work sets directly, rather than a
downstream reader having to parse prose to reconstruct it.

**(c) Disambiguate Stage3.G's own reported message so this confusion can't recur even before (a)
ships.** A one-line, low-risk fix independent of (a)/(b): change Stage3.G's detail string (wherever
it's computed) to state explicitly that it counts parenthetical-form citations only and is a floor,
not a completeness measure -- e.g. appending `"(parenthetical-form only; see Stage3.F for
completeness)"` to whatever prints the percentage. This is the cheapest fix and should ship
regardless of how long (a) takes, since it directly addresses how the confusion actually happened:
a reader (this session, then a user) saw one number and reasonably assumed it meant more than it does.

## Verification method (for the owning session to run)

1. Run `reference_rule_adversarial_test_v1_0_0.py` unchanged first, to confirm the gate's own
   logic is still sound before touching orchestration (it is: 6/6, re-verified this session).
2. Add a fixture pairing analogous to the existing `02-gates/fixtures/` pattern: a document ABox
   with one deliberately uncited structural individual, proving the *wired* Stage3.F (not just the
   isolated function) fails on it end-to-end.
3. Re-run this session's `code_abundance_document_v1_0_0.ttl` through the wired gate and confirm it
   reports PASS with the same detail the REFERENCE_ONLY bridge already produces.
4. For (c), confirm by inspection that Stage3.G's printed output, run against any document, carries
   the disambiguating clause verbatim -- not a paraphrase a future reader could still misread.

## Attached evidence

- `code-abundance-rdodi/00-proposals/REFERENCE_ONLY_stage3f_ttl_bridge_v1_0_0.py` -- runs standalone,
  produces the PASS/FAIL pair cited above.
