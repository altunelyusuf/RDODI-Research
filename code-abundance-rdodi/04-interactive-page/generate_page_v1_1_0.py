import rdflib, html, json
from rdflib.namespace import RDF, RDFS, OWL

SKOS = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
DCT = rdflib.Namespace("http://purl.org/dc/terms/")
CA = rdflib.Namespace("http://example.org/rdodi/code-abundance/domain#")
DOC = rdflib.Namespace("http://example.org/rdodi/document-ontology#")

BASE = "/home/claude/RDODI-Research/code-abundance-rdodi"
gdoc = rdflib.Graph(); gdoc.parse(f"{BASE}/03-document/code_abundance_document_v1_1_0.ttl", format="turtle")
gdom = rdflib.Graph(); gdom.parse(f"{BASE}/02-domain/code_abundance_domain_tbox_v1_0_0.ttl", format="turtle")
gab = rdflib.Graph(); gab.parse(f"{BASE}/02-domain/code_abundance_domain_abox_v1_0_0.ttl", format="turtle")

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

exemplar_by_class = {}
for ind in gab.subjects(RDF.type, OWL.NamedIndividual):
    types = [t for t in gab.objects(ind, RDF.type) if str(t).startswith(str(CA))]
    if types:
        cls = str(types[0])
        elbl = str(gab.value(ind, RDFS.label))
        esrc = str(gab.value(ind, DCT.source))
        exemplar_by_class[cls] = (elbl, esrc)

def esc(t): return html.escape(t)

nav_links = []
sections_html = []
widget_records = []
sec_num = 0

for c, parent in order:
    key = str(c)
    slug, lbl, txt, is_leaf = sec_by_class[key]
    anchor = slug.replace("Sec_", "sec-").lower()

    if parent is None:
        sec_num += 1
        nav_links.append(f'<a data-t="{anchor}" href="#{anchor}">{esc(lbl)}</a>')
        sec_no_html = f'<div class="sec-no">{sec_num:02d}</div>'
    else:
        sec_no_html = '<div class="sec-no"></div>'

    widget_html = ""
    if is_leaf:
        exemplar = exemplar_by_class.get(key)
        detail_id = f"detail-{anchor}"
        btn_id = f"toggle-{anchor}"
        if exemplar:
            elbl, esrc = exemplar
            detail_text = f"<strong>Exemplar:</strong> {esc(elbl)}<br><strong>Source:</strong> {esc(esrc)}"
        else:
            detail_text = "No exemplar recorded."
        widget_html = f'''
        <div class="viz">
          <div class="viz-h"><div class="t">Grounding evidence</div><h4>{esc(lbl)}</h4></div>
          <div class="viz-b">
            <button id="{btn_id}" class="more-btn" aria-expanded="false" aria-controls="{detail_id}">Show grounding evidence</button>
            <div id="{detail_id}" hidden style="margin-top:10px;">{detail_text}</div>
          </div>
        </div>'''
        widget_records.append({"slug": slug, "anchor": anchor, "btn_id": btn_id, "detail_id": detail_id})

    # Special widget: citation-verification status bar, injected into the Industry Implementation overview
    if slug == "Sec_IndustryImplementation":
        widget_html += '''
        <div class="viz">
          <div class="viz-h"><div class="t">Visual &middot; verification status</div><h4>Citation verification across this report's 15 concept exemplars</h4></div>
          <div class="viz-b">
            <div class="coq-bar" role="img" aria-label="13 of 15 citations independently verified, 1 partially verified, 1 flagged unavailable">
              <span class="prev" style="width:86.7%;background:#1f6f5c;">13</span><span class="fail" style="width:6.7%;background:#c79a3a;">1</span><span class="fail" style="width:6.6%;background:#bd5a36;">1</span>
            </div>
            <div class="coq-row"><span>&#9679; Verified (13) &mdash; independently confirmed via live web search/fetch</span></div>
            <div class="coq-row"><span>&#9679; Partial (1) &mdash; figure cited by the primary source but not independently located</span></div>
            <div class="coq-row"><span>&#9679; Unavailable (1) &mdash; Amplitude PR-cycle-time figure, flagged rather than assumed</span></div>
          </div>
        </div>'''

    level_class = "sec" if parent is None else "sec sub"
    heading_tag = "h2" if parent is None else "h3"
    sections_html.append(f'''
    <section id="{anchor}" class="{level_class}" tabindex="-1">
      <div class="sec-head">{sec_no_html}<{heading_tag}>{esc(lbl)}</{heading_tag}></div>
      <div class="lead"><p>{esc(txt)}</p></div>
      {widget_html}
    </section>''')

with open("/home/claude/docx-build/ch10_style.txt") as f:
    ch10_css = f.read()

html_doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>When Code Is Abundant: A Research Companion</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,900&family=Newsreader:ital,opsz@0,6..72;1,6..72&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
{ch10_css}
</head>
<body>
<div class="progress" id="prog"></div>
<div class="topbar"><div class="topbar-in">
  <div class="brand">Code Abundance<small>RDODI Companion</small></div>
  <nav class="top" id="topnav">{''.join(nav_links)}</nav>
</div></div>
<div class="wrap">
<div class="hero">
  <div class="kicker">RDODI Stage 4 &middot; Interactive Companion</div>
  <h1>When Code Is Abundant</h1>
  <p class="lede">A research companion to Staples (2026), grounded in Stage 1&ndash;3 research, domain and document artifacts.</p>
  <div class="metrics">
    <div class="metric"><b>21</b><span>Sections</span></div>
    <div class="metric"><b>15</b><span>Grounded concepts</span></div>
    <div class="metric"><b>15</b><span>Cited sources</span></div>
    <div class="metric"><b>1</b><span>Disclosed gap</span></div>
  </div>
  <div class="abstract"><p>This page renders the code-abundance-rdodi research companion as a navigable single-page artifact. Every leaf section carries a grounding-evidence widget; the Industry Implementation overview carries a citation-verification status visualization.</p></div>
</div>
{''.join(sections_html)}
<footer class="foot">Generated from code_abundance_document_v1_1_0.ttl and code_abundance_domain_abox_v1_0_0.ttl. Not a substitute for reading the primary source.</footer>
</div>
<script>
const prog=document.getElementById('prog'),links=[...document.querySelectorAll('#topnav a')];
const tgts=links.map(l=>document.getElementById(l.dataset.t)).filter(Boolean);
function spy(){{const h=document.documentElement,s=h.scrollTop/(h.scrollHeight-h.clientHeight);prog.style.width=(s*100)+'%';
 let cur=tgts[0]?.id;for(const t of tgts){{if(t.getBoundingClientRect().top<120)cur=t.id;}}links.forEach(l=>l.classList.toggle('active',l.dataset.t===cur));}}
addEventListener('scroll',spy,{{passive:true}});spy();
document.querySelectorAll('.more-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    const target = document.getElementById(btn.getAttribute('aria-controls'));
    const isHidden = target.hasAttribute('hidden');
    if (isHidden) {{ target.removeAttribute('hidden'); btn.setAttribute('aria-expanded','true'); btn.textContent='Hide grounding evidence'; }}
    else {{ target.setAttribute('hidden',''); btn.setAttribute('aria-expanded','false'); btn.textContent='Show grounding evidence'; }}
  }});
}});
</script>
</body>
</html>
'''

with open(f"{BASE}/04-interactive-page/code_abundance_page_v1_1_0.html", "w") as f:
    f.write(html_doc)
with open(f"{BASE}/04-interactive-page/widget_records_v1_1_0.json", "w") as f:
    json.dump(widget_records, f, indent=2)

print(f"Generated v1.1.0 HTML: {len(order)} sections, {len(widget_records)} reveal widgets + 1 status-bar widget")
