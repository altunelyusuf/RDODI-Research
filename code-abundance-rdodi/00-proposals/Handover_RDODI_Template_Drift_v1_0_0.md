# Handover to RDODI Session: Root Cause of "Formal Template" Drift, and the DOCX Non-Issue

**From:** code-abundance-rdodi session (article-review-session)
**Date:** 2026-08-27
**Trigger:** User review of code-abundance-rdodi v1.1.0 reported two problems: (1) the interactive
page "is not matching the default template of RDODI... single flowing panel with no sub-tabs and
hierarchical MS Explorer style iconised left menu, prompt, visualizations and many other features
are totally missing," and (2) "your docx file is not accessible from the GitHub, possibly you
didn't push the file."

**Verdict on (2): not a defect.** Verdict on (1): **there is no formal RDODI template matching that
description anywhere in this repository.** The user's expectation traces to a different, unrelated
package. Full evidence below.

---

## Part 1 — the DOCX: verified accessible, not a push failure

Fetched directly from GitHub's raw content server, bypassing the web UI entirely:

```
curl -sS -o /tmp/fetched.docx \
  https://raw.githubusercontent.com/altunelyusuf/RDODI-Research/main/code-abundance-rdodi/03-document/code_abundance_document_v1_1_0.docx
```

Result: HTTP 200, 14,183 bytes, `file` identifies it as `Microsoft Word 2007+`, and its SHA-256
matches the local original **byte-for-byte**. The file is genuinely on GitHub and downloadable.

**Most likely explanation, not confirmed but consistent with the symptom:** GitHub's web UI has no
inline preview for `.docx` (unlike `.pdf`, which it renders). Clicking the file in the browser
shows a "Download" prompt rather than a viewer, which can read as "not accessible" if a direct
raw/download link wasn't given up front. That is a communication gap on this session's part, not a
repository defect — no action needed from the RDODI session.

---

## Part 2 — the interactive page: the described template does not exist in this ecosystem

### What was checked, exhaustively, before concluding this

1. **The RDODI Four-Stage Pipeline Procedure itself** (`RDODI_FourStage_Pipeline_Procedure_v1_2_2.md`
   §5.3 step 6): the Stage 4 deliverable is specified as a single file —
   `"<subject>_page_v<X_Y_Z>.html"` — singular, not a page tree. Nothing in the procedure text
   describes tabs, a sidebar, or multi-page navigation.

2. **Every worked example in `04-worked-example/`** — `ch10_quality_companion_interactive_v1_0_0.html`
   through `_v4_0_0.html` (the documented four-round quality progression) — inspected directly.
   All four are single flowing HTML pages with anchor-based in-page navigation (a sticky top pill-bar
   at best, in v4.0.0). None has a sidebar, a tree, or tabs.

3. **`15-presentation/rdodi_presentation_renderer_v1_0_0.py`** — the ecosystem's own canonical,
   domain-general Stage 4 HTML generator, read in full. It renders flat `<div class="card">` sections
   in a single-column `<main>`, no navigation element at all beyond the browser's own scroll. Its two
   proof outputs (`04-worked-example/presentation-samples/course_companion_rendered.html`,
   `technical_report_rendered.html`) were also checked directly for sidebar/tab/tree markup: none
   found in either.

4. **`04-documentation/kb_explorer_v1_1_0.html`** (OE Method's own KB browser, a plausible candidate
   for "the Explorer-style tool"): checked directly. It is a single-column filterable list with a
   search box — no sidebar, no tree, no tabs.

**None of the four real, shipped rendering paths in this ecosystem produce what the user described.**

### What the interactive-page ontology *does* declare — and never uses

`interactive_page_ontology_tbox_v1_9_0.ttl` contains real, TBox-declared classes for exactly the
richer pattern described: `ipo:SubPageTabs` ("Tab-styled navigation links... route between its
sibling sub-pages... realized as navigation links, not in-place panel swaps"), `ipo:PageHierarchy`
("the tree structure relating Pages... drives breadcrumbs, sitemaps, and primary navigation"),
`ipo:LandingPageVariant`, `ipo:StubPage`. This vocabulary describes a genuine **multi-page site**
architecture — separate routable pages linked by a parent/child tree.

**Grepped the entire ecosystem for any consumer of these three classes: none exists.** No procedure
step instantiates `PageHierarchy`. No gate checks it. No renderer reads it. No worked example uses
it. It is vocabulary authored for a use case the procedure's own deliverable shape (one HTML file)
cannot produce. This is a real, disclosed finding in its own right, independent of the user's
original question: **the ontology promises a site architecture the pipeline never asks anyone to
build.**

### Where the user's actual expectation comes from

`lcw-principles-kb/04-page/lcw_kb_interactive_v0_92_0.html` (5,927 lines) — a **separate,
unrelated package** in the same monorepo, built under a different commission (LC Waikiki
Principles Knowledge Base) — genuinely has every feature the user listed:

- `<aside>` with `class="jump-tree"`, `tree-node`, `tree-row`, `tree-caret` — a real collapsible
  hierarchical sidebar tree.
- `class="toptabs"` / `class="subtabs"` with `role="tab"` — real sub-tabs.
- `class="chat-shell"`, `chat-messages`, `chat-inputbar` with the literal placeholder text
  `"Ask the live LLM (grounded in the KB)..."` — a real grounded prompt/chat console.

**This file has no cross-reference from any RDODI procedure or documentation file.** It was built
for a different mission, under different governance, with no stated relationship to the RDODI
four-stage pipeline. The most coherent explanation for the reported drift: the expectation of "the
formal RDODI template" is a cross-project transfer from this artifact, not a documented RDODI
standard this session failed to meet.

---

## What this session did, for the record

Given the above, code-abundance-rdodi v1.0.0 and v1.1.0 both correctly implemented what the RDODI
procedure and its actual worked examples specify: a single, anchor-navigated HTML page. v1.1.0
additionally matched the ecosystem's richest *actually-shipped* visual standard (ch10 v4.0.0's
typography and editorial design) after v1.0.0 was found to sit at the gate-conformant floor rather
than that ceiling. Neither version was ever going to satisfy a sidebar-tree-tabs-prompt expectation,
because nothing in RDODI's real procedure, gates, or worked examples asks for one.

## Proposed resolution, returned to the RDODI session for a decision (B1)

This is a scope decision for the package owner, not something this session should decide
unilaterally:

**Option A — adopt the richer pattern as RDODI's real standard.** Formally extend the Stage 4
procedure to require `PageHierarchy`/`SubPageTabs`-based multi-page output for artifacts above some
section-count threshold, build a renderer that actually consumes those TBox classes, and retrofit
the `04-worked-example` reference (currently a single flowing page) to demonstrate it. This is a
substantial new engineering commitment, not a small patch.

**Option B — document the boundary explicitly.** State plainly, in the procedure and in
`04-worked-example/WORKED_EXAMPLE_POINTER_v1_0_0.md`, that RDODI Stage 4's deliverable is
intentionally a single-page, anchor-navigated artifact — a different, smaller class of deliverable
than bespoke builds like `lcw-principles-kb` — so future sessions and reviewers don't carry that
larger artifact's shape as an implicit bar. Retire or explicitly mark `SubPageTabs`/`PageHierarchy`/
`LandingPageVariant` as aspirational-unimplemented (matching the honesty convention already used
elsewhere in this ecosystem, e.g. `ipo:StubPage`'s own self-documenting comment) rather than leaving
them silently unused.

This session takes no position on which option is correct — that is the RDODI session's call.
