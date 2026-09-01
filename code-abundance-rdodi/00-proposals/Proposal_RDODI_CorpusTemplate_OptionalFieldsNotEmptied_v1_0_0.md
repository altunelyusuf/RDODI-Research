# Handover to the corpus-template mechanism: optional fields left with the prior subject's data when a new corpus omits them

**From:** code-abundance-rdodi session (article-review-session)
**Date:** 2026-09-01
**Trigger:** STORY-3's real cleaning pass (patching the source page after instantiation, per direct
user finding that Definitions of Done had not considered the actual effect on real artifacts).

## What was checked, precisely

`instantiate_corpus_v1_0_0.py`'s own `CONTRACT_OPTIONAL` list (`COMPANY_DATA`, `SKOS_TTL`, `BIAS_TTL`,
`AGENTIC_TTL`, `PROV_TTL`, `SNIPPETS`) is only replaced when the incoming corpus contract supplies a
value for that key. This is reasonable on its own -- optional means optional. But this session's real
corpus contract correctly omits all six (this subject has no comparative-company dataset, no bespoke
SKOS scheme, etc.), and the instantiation left the *source page's own* values for three of them
completely untouched in the output:

- `COMPANY_DATA`: 7365 bytes of the source subject's company-comparison dataset (Amazon/Musk-Tesla/
  Nvidia/Google/Apple), rendered live in a "Company Comparison" tab.
- `SKOS_TTL`: 6615 bytes of the source subject's own SKOS concept scheme.
- `LINEAGE_TTL`: 236063 bytes -- the source subject's entire embedded lineage history (this field is
  separately documented `governed_by_lineage_not_corpus`, "regenerated from the real governed TTL,
  never hand-edited" -- so leaving the *prior* subject's lineage in place is a sharper version of the
  same gap, not just a missing dataset but actively wrong governance data presented as current).

## Consequence, demonstrated directly, including a real bug this session found and fixed

Silently carrying the prior subject's optional-field data is not merely stale content -- it produced a
genuine functional bug. `buildCompanyView()`'s own logic hardcodes a 5-company key list
(`["amazon","musk","nvidia","google","apple"]`) and indexes into `COMPANY_DATA.companies[key]`
unconditionally. This session's own first fix attempt (`COMPANY_DATA = {"themes": []}`, correctly
addressing the visible data) still crashed on real page load -- `Cannot read properties of undefined
(reading 'amazon')` -- confirmed via real headless Playwright execution with a full JS stack trace,
because the `companies` key was silently expected to exist. The eventual correct fix required both
supplying `companies: {}` **and** changing `buildCompanyView` to derive its key list from
`Object.keys(companies)` rather than a hardcoded list -- the hardcoded list is itself a second,
independent instance of exactly this bug class (assuming a specific prior subject's data shape rather
than deriving from whatever the corpus actually provides).

## Not fixed here

Both `instantiate_corpus_v1_0_0.py`'s handling of absent optional fields and the source page's own
hardcoded-assumption bugs are inside `08-brsf-corpus-template`, owned by another session lineage (B1).
Worked around locally for this instantiation (each optional field the corpus omits was explicitly
emptied by hand, and the one discovered hardcoded-shape bug was fixed), documented in this package's
own lineage register, not applied upstream.

## Suggested fix, offered as a starting point

1. When a corpus contract omits an optional field, the instantiation script should explicitly empty
   the source page's own value for it (a real, neutral default per field), not merely skip replacing
   it -- silence should mean "nothing here," not "keep whatever was here before."
2. Audit the source page for other hardcoded assumptions about a specific field's shape (the
   `compKeys` pattern found here) and derive from the actual data instead.
3. `LINEAGE_TTL` specifically should probably default to empty rather than stale-prior-subject data
   whenever the new development's own lineage_audit-equivalent tool has not yet run against it.
