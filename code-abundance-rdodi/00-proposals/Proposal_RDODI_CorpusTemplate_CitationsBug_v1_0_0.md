# Handover to the corpus-template mechanism: CITATIONS is documented required but never replaced

**From:** code-abundance-rdodi session (article-review-session)
**Date:** 2026-09-01
**Trigger:** Running `instantiate_corpus_v1_0_0.py` for real (STORY-3) against a real corpus contract
containing all 6 schema-declared fields, including 15 real CITATIONS. The generated output's
Citations tab still showed the *source page's own* citation table (Doerr, Grove, et al.) verbatim.

## What was checked, precisely, before concluding this is real

`01-schema/corpus_contract_v1_0_0.json`'s `required` block lists 6 keys: `MISSION`, `CATEGORIES`,
`PRINCIPLES`, `FRAMEWORKS`, `RELATIONS`, `CITATIONS` -- with `CITATIONS`'s own role text stating it
"must match the research document's own numbering exactly or the Citations tab misattributes."

`02-tooling/instantiate_corpus_v1_0_0.py`'s own hardcoded list:
```python
CONTRACT_REQUIRED = ["MISSION","CATEGORIES","PRINCIPLES","FRAMEWORKS","RELATIONS"]
```
`CITATIONS` is absent from it. The `--check` plan output confirms this directly: it reports
replacing exactly 5 constants, never 6, regardless of what the corpus JSON contains.

**Separately confirmed the reason it can never work anyway**, even if added to the list: the actual
source page's Citations tab (`id="view-research"`) is not driven by any `const CITATIONS` at all --
it is static HTML, a hand-written `<table class="cite">` with rows specific to the source page's own
subject. There is no JS constant for the replacement mechanism to find and swap, so this is two
compounding gaps, not one: the tool's own required-list omission, and the source page never having
made this section data-driven in the first place.

## Consequence, demonstrated directly

Every corpus instantiated from this source page silently keeps the *previous* subject's citation
list, regardless of what CITATIONS content the new corpus contract supplies. This is not a cosmetic
issue -- the schema's own text warns that a numbering mismatch "misattributes" the Citations tab,
and the actual failure mode found here is worse: it's not mismatched, it's the wrong subject's
citations entirely.

## Not fixed here

Both the required-list omission and the underlying static-HTML gap are inside
`08-brsf-corpus-template`, owned by another session lineage (B1). Not fixed directly; this session
worked around it locally for its own instantiation (manual post-processing of the generated output,
documented in this package's own lineage register) rather than leaving the gap silently unaddressed.

## Suggested fix, offered as a starting point

1. Add `"CITATIONS"` to `CONTRACT_REQUIRED` in `instantiate_corpus_v1_0_0.py`.
2. Make the source page's Citations tab data-driven from a real `const CITATIONS` array, the same
   pattern already used for `PRINCIPLES`/`FRAMEWORKS`/`RELATIONS`, so the replacement mechanism has
   something to find.
