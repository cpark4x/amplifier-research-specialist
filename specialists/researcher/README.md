# Researcher Specialist

A domain expert agent for producing **trustworthy structured evidence**.

The Researcher's job is precisely: return structured, source-tiered, confidence-rated evidence — not answers, not narratives, not reports. The answer layer is the job of downstream specialists (Writer, Briefer). The Researcher produces the evidence they consume.

---

## Interface Contract

### Accepts

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `question` | string | Yes | — | The research question |
| `query_type` | `person \| company \| technical \| market \| event` | Yes | — | Shapes the source discovery checklist |
| `quality_threshold` | `medium \| high \| maximum` | No | `high` | Acceptable confidence floor before returning |
| `source_types` | array | No | all | Which source categories to check |
| `context` | string | No | — | Additional context from memory or project |

### Returns

`ResearchOutput` — see `shared/interface/types.md` for the full typed schema.

Key fields:
- `findings[]` — discrete claims, each with source, tier, and confidence
- `evidence_gaps[]` — what couldn't be verified and why
- `quality_score` — overall trustworthiness signal
- `follow_up_questions[]` — what to research next
- `research_events[]` — full observability trail of what was attempted

### Can Do

- Web search
- Web fetch (with paywall workarounds: cache → archive.org → quote search → author summary)
- Document and PDF retrieval

### Cannot Do

- Write narratives, reports, or articles — that's the Writer specialist
- Make recommendations or decisions — that's the orchestrator
- Manage memory or session state — stateless by design
- Access paywalled content without workarounds (gaps are disclosed explicitly)

---

## Design Notes

**Outcome over speed.** The Researcher runs a Quality Gate before returning output. If Low confidence claims exist or closeable gaps remain, it runs additional passes. It will take longer than a simple search. That's correct behavior.

**Evidence, not answers.** The output is structured evidence for downstream consumption — not prose. The Writer specialist turns evidence into prose.

**Honest gaps.** The Researcher never silently skips inaccessible content. Every gap is named, with fallback attempts logged. A short honest output is more valuable than a long confident-sounding one.

---

## Source Discovery

The Researcher uses query type to build a canonical source checklist before fetching begins:

**Person research:** personal blog, X/Twitter, LinkedIn, official company blog, congressional testimony, interview transcripts, YouTube/podcast appearances

**Company research:** press releases, company blog, SEC/regulatory filings, earnings call transcripts, official partnership announcements, wire services

**Technical research:** official documentation, arXiv, GitHub repository, RFC/specification documents, Hacker News

**Market research:** industry analyst reports, competitor official sites, trade press, job postings

**Event/news research:** primary wire reports, official statements, video/transcript, cross-referenced across 2+ outlets
