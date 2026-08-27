"""
REFERENCE_ONLY -- NOT_A_RELEASE

Worked bridge from a Stage 3 document ABox + Stage 1 research ABox to the input
shape expected by rdodi-ecosystem/02-gates/reference_rule_gate_v1_0_0.py.

Authored by the code-abundance-rdodi session as evidence for
Proposal_RDODI_Stage3F_Wiring_v1_0_0.md. This is a demonstration of feasibility
and a starting point, not a submitted patch to rdodi-ecosystem (B1: that package
is owned by another session; this session can propose, not edit it).

KNOWN SIMPLIFICATION, disclosed rather than hidden: `cites` maps any detected
citation marker to the primary source's ref id rather than resolving which
specific Publication each marker names. This is sufficient to test the
"uncited" dimension of the reference rule (which is what this proposal's
finding is about) but NOT sufficient to exercise the "dangling citation"
dimension meaningfully -- a real implementation needs per-claim citation
attribution, not just citation-marker presence. See proposal body for the
follow-on this implies for Stage 1's Publication modeling.
"""
import re
import rdflib
from rdflib import RDFS
from rdflib.namespace import RDF


def extract_ttl_to_reference_rule_input(document_ttl_path, research_ttl_path):
    """Returns (refs, claims) in the shape reference_rule_gate_v1_0_0.reference_rule() expects.

    refs: every res:Publication in the Stage 1 research ABox, status 'verified'.
          (Enhancement implied by this proposal: Stage 1 Publications should carry
          an explicit status property so a citation the research artifact itself
          flagged unavailable -- as this session's Stage 1 quality scorecard did
          in prose for two Amplitude figures -- can be represented as
          'unavailable_flagged' here rather than only as free-text prose.)

    claims: every structural individual's skos:definition in the Stage 3 document,
            needs_cite=True always (Stage3.F: "every external claim cited"),
            cites=[] if no citation marker detected, else a match.
            Detects BOTH forms deliberately: narrative "Surname (Year)" and
            parenthetical "(Surname, Year)" -- the distinction whose conflation
            with Stage3.G (a parenthetical-only floor) motivated this proposal.
    """
    SKOS = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")
    RES = rdflib.Namespace("http://example.org/rdodi/research-ontology#")

    g = rdflib.Graph()
    g.parse(document_ttl_path, format="turtle")
    gr = rdflib.Graph()
    gr.parse(research_ttl_path, format="turtle")

    pub_ids = [str(p).split('#')[-1] for p in gr.subjects(RDF.type, RES.Publication)]
    refs = [{"id": pid, "status": "verified"} for pid in pub_ids]

    cite_pattern = re.compile(r"[A-Z][a-zA-Z\.\' ]+\(\d{4}\)|\([A-Z][a-zA-Z\.\' ]+,\s*\d{4}\)")

    claims = []
    seen = set()
    primary_source_id = pub_ids[0] if pub_ids else "unknown_primary_source"
    for s in g.subjects(RDF.type, None):
        d = g.value(s, SKOS.definition)
        if not d or str(s) in seen:
            continue
        seen.add(str(s))
        text = str(d)
        has_citation = bool(cite_pattern.search(text))
        claims.append({
            "text": str(g.value(s, RDFS.label)) or str(s).split('#')[-1],
            "needs_cite": True,
            "cites": [primary_source_id] if has_citation else [],
        })
    return refs, claims


if __name__ == "__main__":
    import sys
    sys.path.insert(0, "/home/claude/Ontologies/rdodi-ecosystem/02-gates")
    from reference_rule_gate_v1_0_0 import reference_rule

    doc = "/home/claude/Ontologies/code-abundance-rdodi/03-document/code_abundance_document_v1_0_0.ttl"
    research = "/home/claude/Ontologies/code-abundance-rdodi/01-research/code_abundance_research_v1_0_0.ttl"

    refs, claims = extract_ttl_to_reference_rule_input(doc, research)
    result = reference_rule(refs, claims)
    print(f"Stage3.F (via this bridge) against code_abundance_document_v1_0_0.ttl: {result.verdict} -- {result.detail}")
