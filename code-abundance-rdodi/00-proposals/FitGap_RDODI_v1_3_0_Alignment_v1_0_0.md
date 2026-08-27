# Fit-Gap Analysis: code-abundance-rdodi v1.2.0 vs. RDODI Ecosystem v1.98.0 / Procedure v1.3.0

**From:** code-abundance-rdodi session (article-review-session)
**Date:** 2026-08-27
**Trigger:** rdodi-ecosystem updated to v1.98.0 (procedure v1.3.0) with a real owner ruling: the
rich sidebar/tabs/chat pattern (`08-brsf-corpus-template/`) is now the RDODI **default** Stage 4
deliverable — a direct outcome of this package's own template-drift handover. The single flowing
anchor-page and the native S6 generator are **retained as named Variations**, not deprecated.

**Purpose of this document:** lay out what changed, what already fits, and what's a genuine gap
under each of the two viable paths — before committing engineering effort to either.

---

## 1. What changed, verified against the actual new bytes

- `RDODI_FourStage_Pipeline_Procedure_v1_3_0.md` §5.3: default Stage 4 deliverable is now the
  rich, single-file page (hierarchical sidebar, top+sub tabs, grounded chat console), built via
  `08-brsf-corpus-template/02-tooling/instantiate_corpus_v1_0_0.py` against a corpus JSON.
- Honest disclosure carried through the ruling, not dropped: the rich pattern is confirmed
  (`grep`, 0 routing constructs) to be in-page JS panel-swapping over **one HTML file**, not
  separate routable pages. `ipo:SubPageTabs`/`ipo:PageHierarchy` still describe a routable
  multi-page architecture this pattern does not have and do not become correctly-used vocabulary
  just because the pattern was promoted to default.
- **My existing v1.1.0 page is not obsolete or wrong.** It is now explicitly the "single flowing
  anchor-page" Variation, still valid, still named in the procedure, "for smaller artifacts or
  minimal-dependency contexts."
- Stage4.D's old count floors (≥25 buttons, ≥12 tables, etc.) remain retired (v1.1.0, unchanged);
  Stage4.H–K (widget warrant / content-grounding / design-test / intention-coverage) remain the
  real mechanical bar regardless of which Stage 4 path is chosen.

## 2. Fit — unaffected by this update, verified not assumed

| Item | Status |
|---|---|
| Stage 1 research artifact | Unaffected. No vocabulary this update touches. |
| Stage 2 domain TBox/ABox v1.1.0 (25-class taxonomy incl. Critical Analysis apparatus) | Unaffected. |
| Stage 3 document v1.2.0 (25 sections, mechanism-level depth) | Unaffected structurally. This is the actual input to whichever Stage 4 path is chosen. |
| Single flowing anchor-page as a legitimate Stage 4 shape | **Still fits** — explicitly retained as a named Variation, not superseded. |

## 3. Gap — exists regardless of which Stage 4 path is chosen

My current Stage 4 artifacts (`code_abundance_page_v1_1_0.html`, `code_abundance_page_abox_v1_1_0.ttl`)
were built against **Stage 3 v1.1.0's 21-section structure**. Stage 3 has since grown to 25 sections
(the Critical Analysis and Conclusion apparatus, added in the same turn that fixed the report's
content-quality gap). Concretely:

- Stage4.E (page section count = Stage 3 section count) would **FAIL**: 21 ≠ 25.
- Cross.B (page → document → domain provenance) would **FAIL** for any section added since v1.1.0,
  because those page regions don't exist yet.
- This is independent of the template-drift question — it would need fixing even if RDODI's
  Stage 4 default had never changed.

**Second, path-independent finding, checked fresh per BP-D34 rather than assumed:** of the 25
current section titles, 2 exceed BP-D34's 30-character pill threshold ("Critical Analysis and
Conclusion," 32 chars; "Metric Validity and Selection Bias Critique," 43 chars). Per BP-D34's own
decision rule, this places the artifact in the **"26-50 sections OR long titles → grouped
permanent top-bar with sub-section sidebar"** band, not the flat inline pill-bar my v1.1.0 page
actually used. That was a real navigation-shape defect in v1.1.0, independent of the default/
Variation question, caught only by re-checking BP-D34 fresh rather than from memory of the earlier
21-section, all-short-titles state.

## 4. Gap — specific to adopting the new Default (rich corpus-instantiated pattern)

Checked against `08-brsf-corpus-template/BUILD_INSTRUCTIONS_v1_0_0.md` and the actual schema
(`corpus_contract_v1_0_0.json`), not assumed from the procedure's summary:

**What would be inherited for free** (73% of the page, corpus-independent, unchanged by
instantiation): all 11 registered agents, the full BRSF 11-stage pipeline, the TF-IDF/embeddings/
WebLLM/Oxigraph/Pyodide engine layer, real in-browser SHACL via pySHACL/micropip, the UI shell and
stylesheet.

**What is genuinely new authoring work** (the corpus contract, ~27% of the page, replaced per
subject):
- `MISSION` — a one-line standing mission statement for this specific companion.
- `CATEGORIES` — map my 7 Stage 2 top-level classes to category keys with valid stylesheet CSS
  classes.
- `PRINCIPLES` — my 18 leaf concepts, each needing `id`, `cat`, `short`, `en`, `en_short`, `apply`,
  `fw`, `reinforces`, `roles` — richer per-entry structure than my current Stage 2 exemplars carry.
- `CITATIONS` — my 15 Stage 1 Publications, renumbered to match this schema's own numbering
  exactly (the contract warns this must match the research document's numbering or the Citations
  tab misattributes).
- `RELATIONS` — typed edges between concepts with `evidence` fields; I have implicit relations
  (e.g., Cost Per Accepted Change → Theory of Constraints) that would need to become explicit,
  auditable edges for the first time.
- **`EPICS`/`LINEAGE_TASKS`/`OBJECTIVES` must be emptied, not carried over** — the build
  instructions are explicit that these mirror the *source page's own* governed lineage and
  carrying them into a new corpus would assert a governed history that never happened for this
  subject. My own lineage ceremony would need to run separately to repopulate them honestly.

**Content this package does not currently have at all**, required by procedure §5.3 step 5
(mandatory section roles: Introduction, Body, Quiz, **Glossary**, **References**): I have no quiz
questions and no dedicated glossary authored anywhere in this package. This is new content
authoring, not re-templating — a materially larger scope than reformatting existing prose.

**Proportionality check, verified against a real precedent rather than assumed too small or too
large:** RDODI's own existing corpus instantiation (`04-rdodi-corpus/rdodi_corpus_v1_0_0.json`)
has 21 `PRINCIPLES`, 4 `CATEGORIES`, 4 `CITATIONS`, 6 `RELATIONS`, and renders as a working
1,222,455-byte page. My subject (18 leaf concepts, 7 categories, 15 citations) is comparable in
scale — this is not disproportionate to attempt, but it is a genuinely larger undertaking than a
page rebuild: it is closer to standing up a small internal application than authoring a report
render.

## 5. Two paths, stated plainly, not defaulted to either

**Path A — Fix the Variation (smaller, bounded effort).** Rebuild the existing single flowing
anchor-page pattern for the current 25-section Stage 3 structure, correcting the navigation shape
to the grouped top-bar + sub-section sidebar BP-D34 actually calls for at this title-length mix.
Re-verify Stage4.A/B/E/F/G plus Stage4.H–K. This closes the path-independent gap only; it does not
adopt the new ecosystem default.

**Path B — Adopt the new Default (larger, open-ended effort).** Author a full corpus contract
(`MISSION`, `CATEGORIES`, `PRINCIPLES`, `FRAMEWORKS`, `RELATIONS`, `CITATIONS`), including new quiz
and glossary content this package has never had, run `instantiate_corpus_v1_0_0.py` against a real
source page, and verify per the build instructions' five reference checks (renders; old corpus
fully gone; 11 agents intact; SHACL >100KB present; zero page errors). This aligns with the
ecosystem's stated preference and inherits substantially more machinery, at a real cost in new
content authoring (quiz + glossary in particular) that Path A does not require at all.

This session takes no position on which to pursue — that is a scope and effort decision for you to
make with the trade-off stated plainly above, per the same B1/B2 discipline already applied to the
earlier template-drift handover.
