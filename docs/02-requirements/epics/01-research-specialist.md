# Epic 01: Research Specialist

**Status:** Complete
**Owner:** Chris Park
**Contributors:** Chris Park
**Last Updated:** 2026-02-27

<!--
Derive ownership and history from git - don't guess or assume:

Contributors by commit count:
git log --format="%an" -- <relevant-files> | sort | uniq -c | sort -rn

Full history with dates:
git log --format="%ad %an - %s" --date=short -- <relevant-files>

Example: git log --format="%an" -- "backend/src/agent/*.ts" | sort | uniq -c | sort -rn
-->

---

## 1. Summary

The Research Specialist gives orchestrators access to structured, trustworthy evidence rather than raw AI answers. It accepts a research question and returns source-tiered findings with confidence scores, evidence gaps, and a full audit trail — a typed `ResearchOutput` contract any downstream agent can act on with confidence. This is both the first working specialist in the library and the proof-of-pattern that all future specialists will follow.

---

## 2. Problem

When an orchestrator needs to research a topic, it either does the research inline — producing answers without source provenance, confidence levels, or gaps — or delegates to a generic web research agent that returns prose summaries with no structured contract. The result is output that can't be trusted, can't be composed downstream, and can't be audited. Developers building Amplifier workflows have no way to know whether a research result is based on a primary source or a speculative blog post, whether a claim has been corroborated, or what simply couldn't be found. Quality research demands source verification, honest corroboration, and explicit accounting of what was tried and failed — none of which generic agents provide.

---

## 3. Proposed Solution

A dedicated Researcher specialist that any orchestrator can delegate to when research quality matters. The Researcher runs a 7-stage structured pipeline (Plan → Discover Sources → Fetch → Extract → Corroborate → Quality Gate → Synthesize) and returns a typed `ResearchOutput` contract. Every finding includes its source, tier (primary / secondary / tertiary), confidence level, and corroboration count. Evidence gaps are explicitly surfaced — the Researcher never hides uncertainty behind confident-sounding prose. A configurable quality threshold gate enforces the standard before output is returned.

Orchestrators receive structured evidence they can trust and compose — not answers they have to second-guess.

---

## 4. User Stories

**IMPORTANT:** Only includes user stories for implemented features.

### Implemented

| # | Story | Owner | Created | Last Updated |
|---|-------|-------|---------|--------------| 
| [01-01](../user-stories/01-research-specialist/01-01-delegate-research-question.md) | Delegate research question and receive structured ResearchOutput | Chris Park | 2026-02-26 | — |
| [01-02](../user-stories/01-research-specialist/01-02-set-quality-threshold.md) | Set quality threshold (medium / high / maximum) per request | Chris Park | 2026-02-26 | — |
| [01-03](../user-stories/01-research-specialist/01-03-inspect-source-tier-confidence.md) | Inspect source tier and confidence of each finding | Chris Park | 2026-02-26 | — |
| [01-04](../user-stories/01-research-specialist/01-04-read-evidence-gaps.md) | Read evidence gaps — what was tried but couldn't be verified | Chris Park | 2026-02-26 | — |
| [01-05](../user-stories/01-research-specialist/01-05-add-research-via-bundle.md) | Add research capability to any project via bundle include | Chris Park | 2026-02-26 | — |

### Future

- ⏭️ **Chain with Writer** — pass `ResearchOutput` directly to the Writer specialist for research-to-document pipelines
- ⏭️ **Prior output as context** — pass prior `ResearchOutput` as context to a follow-up research task so multi-session investigations build on previous findings
- ⏭️ **Source type filtering** — configure `source_types` to restrict which source categories are checked for domain-specific workflows
- ⏭️ **Contradicted claims as first-class output** — receive structurally contradicted claims (source A vs. source B in direct conflict) as a dedicated output type

---

## 5. Outcomes

**Success Looks Like:**
- Orchestrators receive a `ResearchOutput` contract with source-tiered findings, confidence scores, and explicit evidence gaps for any delegated research question
- No finding enters `ResearchOutput` without a source URL, tier, and confidence level — the contract is enforced, not aspirational
- Quality gate prevents below-threshold output from being returned — honest gaps are surfaced before unverified claims are passed downstream
- Any Amplifier project gains production-quality research capability by adding a single bundle include
- The Researcher establishes the specialist pattern — stateless, contract-first, composable — that all future specialists extend

**We'll Measure:**
- Quality gate fires on every session (not bypassed for speed)
- Evidence gaps are always disclosed, never omitted
- ResearchOutput schema requires no breaking changes after v1.0

---

## 6. Dependencies

**Requires:**
- Amplifier Foundation (bundle system, agent delegation)
- `tool-web` (web_search + web_fetch for source fetching)

**Enables:**
- Writer Specialist — consumes `ResearchOutput` and produces structured prose
- Competitive Analysis Specialist — consumes `ResearchOutput` for structured comparisons
- Any orchestrator workflow that needs verified, composable evidence before acting

**Blocks:** Nothing

---

## 7. Open Questions

- [ ] Should `ResearchOutput` include a `recommended_followup` field to explicitly signal when the Researcher believes deeper investigation is warranted before acting?
- [ ] How should structurally contradicted claims be represented — as a dedicated `ContradictedFinding` type, or surfaced within `evidence_gaps` with both sources attached?
- [ ] What is the correct behavior for `quality_threshold: maximum` when a practical ceiling (search count, fetch failures) is hit — hard fail with explanation, or return with a quality warning flag?
- [ ] Should the Researcher support a `focus_sources` parameter to prioritize specific domains or URLs for domain-expert workflows?
