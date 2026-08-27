# RDODI-Research

A dedicated repository for RDODI (Research → Domain → Document → Interactive) four-stage
pipeline research outputs — one governed package per subject.

**Governance is inherited, not duplicated.** The OE Operating Discipline, the OE ABox (best
practices and lessons), the Lineage Operating Discipline, and the RDODI four-stage pipeline
procedure and gate implementations all live in
[`altunelyusuf/Ontologies`](https://github.com/altunelyusuf/Ontologies) — this repository does not
carry a second copy of any of them. Sessions working here resolve the governing documents from
that repository by highest SemVer, exactly as if they were attached, per the OE discipline's own
pointer-resolution rule.

## Packages

| Package | Subject | Version | Status |
|---|---|---|---|
| `code-abundance-rdodi/` | Staples (2026), "When Code Is Abundant" — economics and governance of AI-native software development | v1.0.0 | All four stages complete; all mechanically-implemented gates pass; one cross-session proposal filed against `rdodi-ecosystem` for a gap found during Stage 3 (`00-proposals/`) |

Each package ships its own `VERSION.txt`, self-verifying `MANIFEST_SHA256_v*.txt`, and
`PUBLISH_RECORD.ttl` recording the gate transcript that authorized its publication. Verification is
by running the gates against the tree, never by assertion — see `PUBLISH_RECORD.ttl`'s
`rdfs:comment` in each package for exactly what was run.

## Structure per package

```
<subject>/
  00-proposals/          cross-session findings/proposals raised against rdodi-ecosystem (if any)
  01-research/           Stage 1: research ABox (concept inventory, citations, quality scorecard)
  02-domain/             Stage 2: domain TBox + ABox + SHACL (the subject's own taxonomy)
  03-document/           Stage 3: document ABox (1:1 sections against the Stage 2 taxonomy)
  04-interactive-page/   Stage 4: interactive HTML page + page ABox + widget test records
  MANIFEST_SHA256_v*.txt
  VERSION.txt
  PUBLISH_RECORD.ttl
```

## One session, one package

Following `altunelyusuf/Ontologies`' own convention: a session publishes only the package(s) it
authored. Cross-package or cross-repository findings are raised as proposals (see
`code-abundance-rdodi/00-proposals/` for a worked example), not committed directly into another
package.
