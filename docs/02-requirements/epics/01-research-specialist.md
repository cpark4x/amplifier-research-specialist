# Epic 01: Research Specialist

**Owner:** To be assigned

## 1. Summary

The Research Specialist gives orchestrators access to structured, trustworthy evidence rather than raw AI answers. It accepts a research question and returns source-tiered findings with confidence scores, evidence gaps, and a full audit trail — a typed `ResearchOutput` contract any downstream agent can act on with confidence. This is both the first working specialist in the library and the proof-of-pattern that all future specialists will follow.

## 2. Problem

When an orchestrator needs to research a topic, it either does the research inline — producing answers without source provenance, confidence levels, or gaps — or delegates to a generic web research agent that returns prose summaries with no structured contract. The result is output that can't be trusted, can't be composed downstream, and can't be audited. Developers building Amplifier workflows have no way to know whether a research result is based on a primary source or a speculative blog post, whether a claim has been corroborated, or what simply couldn't be found. Quality research demands source verification, honest corroboration, and explicit accounting of what was tried and failed — none of which generic agents provide.

## 3. Proposed Solution

A dedicated Researcher specialist that any orchestrator can delegate to when research quality matters. The Researcher runs a 7-stage structured pipeline (Plan → Discover Sources → Fetch → Extract → Corroborate → Quality Gate → Synthesize) and returns a typed `ResearchOutput` contract. Every finding includes its source, tier (primary / secondary / tertiary), confidence level, and corroboration count. Evidence gaps are explicitly surfaced — the Researcher never hides uncertainty behind confident-sounding prose. A configurable quality threshold gate enforces the standard before output is returned.

Orchestrators receive structured evidence they can trust and compose — not answers they have to second-guess.

## 4. User Stories

### Implemented

- As an orchestrator, I can delegate a research question with a `query_type` and receive a structured `ResearchOutput`, so I don't mix research execution with decision-making in the same agent.
- As an orchestrator, I can set a `quality_threshold` (medium / high / maximum) when delegating research, so I control the depth-vs-speed tradeoff for different use cases.
- As an orchestrator, I can inspect the `source_tier` and `confidence` of each finding, so I know whether a claim came from a primary source or a speculative third-party summary.
- As an orchestrator, I can read `evidence_gaps` in the output to know what the Researcher tried and couldn't verify, so I make decisions with honest uncertainty rather than false completeness.
- As a developer building an Amplifier workflow, I can include the `specialists` bundle to immediately add research capability to any project without building my own research pipeline.

### Future

- As an orchestrator, I can chain the Researcher with a Writer specialist to turn evidence into polished prose, so the full research-to-document pipeline is composable.
- As an orchestrator, I can pass prior `ResearchOutput` as context to a follow-up research task, so multi-session investigations build on previous findings rather than starting over.
- As a developer, I can configure `source_types` to restrict which source categories the Researcher checks, so domain-specific workflows skip irrelevant source buckets.
- As an orchestrator, I can receive structurally contradicted claims (source A vs. source B in direct conflict) as a first-class output type, so conflicting evidence is explicitly surfaced rather than silently resolved.

## 5. Outcomes

**Success Looks Like:**

- Orchestrators receive a `ResearchOutput` contract with source-tiered findings, confidence scores, and explicit evidence gaps for any delegated research question
- No finding enters `ResearchOutput` without a source URL, tier, and confidence level — the contract is enforced, not aspirational
- Quality gate prevents below-threshold output from being returned — honest gaps are surfaced before unverified claims are passed downstream
- Any Amplifier project gains production-quality research capability by adding a single bundle include
- The Researcher establishes the specialist pattern — stateless, contract-first, composable — that all future specialists extend

## 6. Dependencies

**Requires:**
- Amplifier Foundation (bundle system, agent delegation)
- `tool-web` (web_search + web_fetch for source fetching)

**Enables:**
- Writer Specialist — consumes `ResearchOutput` and produces structured prose
- Analyst Specialist — synthesizes findings across multiple `ResearchOutput` objects into recommendations
- Any orchestrator workflow that needs verified, composable evidence before acting

## 7. Open Questions

- [ ] Should `ResearchOutput` include a `recommended_followup` field to explicitly signal when the Researcher believes deeper investigation is warranted before acting?
- [ ] How should structurally contradicted claims be represented — as a dedicated `ContradictedFinding` type, or surfaced within `evidence_gaps` with both sources attached?
- [ ] What is the correct behavior for `quality_threshold: maximum` when a practical ceiling (search count, fetch failures) is hit — hard fail with explanation, or return with a quality warning flag?
- [ ] Should the Researcher support a `focus_sources` parameter to prioritize specific domains or URLs for domain-expert workflows?
