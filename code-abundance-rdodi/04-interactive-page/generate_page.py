import rdflib, html, json
from rdflib.namespace import RDF, RDFS, OWL

SKOS = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
DCT = rdflib.Namespace("http://purl.org/dc/terms/")
CA = rdflib.Namespace("http://example.org/rdodi/code-abundance/domain#")
DOC = rdflib.Namespace("http://example.org/rdodi/document-ontology#")

gdoc = rdflib.Graph(); gdoc.parse("code-abundance-rdodi/03-document/code_abundance_document_v1_0_0.ttl", format="turtle")
gdom = rdflib.Graph(); gdom.parse("code-abundance-rdodi/02-domain/code_abundance_domain_tbox_v1_0_0.ttl", format="turtle")
gab = rdflib.Graph(); gab.parse("code-abundance-rdodi/02-domain/code_abundance_domain_abox_v1_0_0.ttl", format="turtle")

tops = sorted([c for c in gdom.subjects(RDF.type, OWL.Class) if str(c).startswith(str(CA)) and not list(gdom.objects(c, RDFS.subClassOf))],
              key=lambda c: str(gdom.value(c, RDFS.label)))
order = []
for t in tops:
    order.append((t, None))
    children = sorted([c for c in gdom.subjects(RDF.type, OWL.Class) if (c, RDFS.subClassOf, t) in gdom],
                       key=lambda c: str(gdom.value(c, RDFS.label)))
    for ch in children:
        order.append((ch, t))

sec_by_class = {}
for s, p, o in gdoc.triples((None, DCT.source, None)):
    if str(o).startswith(str(CA)):
        lbl = str(gdoc.value(s, RDFS.label))
        txt = str(gdoc.value(s, SKOS.definition))
        types = list(gdoc.objects(s, RDF.type))
        is_leaf = DOC.ConceptSection in types
        sec_by_class[str(o)] = (str(s).split('#')[-1], lbl, txt, is_leaf)

# exemplar individual + source per leaf class, for the widget's revealed detail
exemplar_by_class = {}
for ind in gab.subjects(RDF.type, OWL.NamedIndividual):
    types = [t for t in gab.objects(ind, RDF.type) if str(t).startswith(str(CA))]
    if types:
        cls = str(types[0])
        elbl = str(gab.value(ind, RDFS.label))
        esrc = str(gab.value(ind, DCT.source))
        exemplar_by_class[cls] = (elbl, esrc)

nav_items = []
sections_html = []
widget_records = []  # for the ABox + Playwright tests

def esc(t): return html.escape(t)

for c, parent in order:
    key = str(c)
    slug, lbl, txt, is_leaf = sec_by_class[key]
    anchor = slug.replace("Sec_", "sec-").lower()
    nav_items.append(f'<a href="#{anchor}" class="pill">{esc(lbl)}</a>')

    if is_leaf:
        exemplar = exemplar_by_class.get(key)
        detail_id = f"detail-{anchor}"
        btn_id = f"toggle-{anchor}"
        if exemplar:
            elbl, esrc = exemplar
            detail_text = f"Exemplar: {esc(elbl)} &mdash; source: {esc(esrc)}"
        else:
            detail_text = "No exemplar recorded."
        widget_html = f'''
        <button id="{btn_id}" class="reveal-btn" aria-expanded="false" aria-controls="{detail_id}">
          Show grounding evidence
        </button>
        <div id="{detail_id}" class="detail-box" hidden>{detail_text}</div>
        '''
        widget_records.append({"slug": slug, "anchor": anchor, "btn_id": btn_id, "detail_id": detail_id, "class_local": key.split('#')[-1]})
    else:
        widget_html = ""

    level_class = "h1-section" if parent is None else "h2-section"
    sections_html.append(f'''
    <section id="{anchor}" class="{level_class}" tabindex="-1">
      <h{2 if parent is None else 3}>{esc(lbl)}</h{2 if parent is None else 3}>
      <p>{esc(txt)}</p>
      {widget_html}
    </section>
    ''')

html_doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>When Code Is Abundant: A Research Companion</title>
<style>
  body {{ font-family: -apple-system, Segoe UI, sans-serif; max-width: 860px; margin: 0 auto; padding: 1rem; line-height: 1.55; color: #1a1a1a; }}
  nav.pillbar {{ position: sticky; top: 0; background: #fff; padding: 0.75rem 0; border-bottom: 1px solid #ddd; display: flex; flex-wrap: wrap; gap: 0.4rem; z-index: 10; }}
  nav.pillbar a.pill {{ font-size: 0.78rem; padding: 0.25rem 0.6rem; border-radius: 999px; background: #f0f0f0; text-decoration: none; color: #333; }}
  nav.pillbar a.pill:hover, nav.pillbar a.pill:focus {{ background: #d8e8ff; }}
  section.h1-section {{ margin-top: 2.5rem; border-top: 3px solid #333; padding-top: 0.5rem; }}
  section.h2-section {{ margin-top: 1.5rem; margin-left: 0.5rem; }}
  .reveal-btn {{ margin-top: 0.5rem; padding: 0.4rem 0.8rem; border-radius: 6px; border: 1px solid #888; background: #fafafa; cursor: pointer; }}
  .reveal-btn:hover {{ background: #eef; }}
  .detail-box {{ margin-top: 0.5rem; padding: 0.6rem; background: #f6f6fa; border-left: 3px solid #6677cc; font-size: 0.92rem; }}
</style>
</head>
<body>
<header>
  <h1>When Code Is Abundant: A Research Companion</h1>
  <p><em>An RDODI interactive companion to Staples (2026), grounded in Stage 1&ndash;3 research, domain and document artifacts.</em></p>
</header>
<nav class="pillbar" aria-label="Section navigation">
  {''.join(nav_items)}
</nav>
<main>
  {''.join(sections_html)}
</main>
<footer>
  <p style="font-size:0.8rem;color:#666;">Generated from code_abundance_document_v1_0_0.ttl and code_abundance_domain_abox_v1_0_0.ttl. Not a substitute for reading the primary source.</p>
</footer>
<script>
document.querySelectorAll('.reveal-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    const target = document.getElementById(btn.getAttribute('aria-controls'));
    const isHidden = target.hasAttribute('hidden');
    if (isHidden) {{
      target.removeAttribute('hidden');
      btn.setAttribute('aria-expanded', 'true');
      btn.textContent = 'Hide grounding evidence';
    }} else {{
      target.setAttribute('hidden', '');
      btn.setAttribute('aria-expanded', 'false');
      btn.textContent = 'Show grounding evidence';
    }}
  }});
}});
</script>
</body>
</html>
'''

with open("code-abundance-rdodi/04-interactive-page/code_abundance_page_v1_0_0.html", "w") as f:
    f.write(html_doc)

with open("code-abundance-rdodi/04-interactive-page/widget_records.json", "w") as f:
    json.dump(widget_records, f, indent=2)

print(f"Generated HTML with {len(order)} sections, {len(widget_records)} interactive widgets")
print(f"Widget records: {[w['slug'] for w in widget_records]}")
