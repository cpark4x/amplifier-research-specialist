# Product Backlog

**Purpose:** Strategic planning view for canvas-specialists — a library of best-in-class, single-domain AI specialist agents for knowledge worker and consumer scenarios  
**Owner:** Chris Park  
**Last Updated:** March 3, 2026 (evening)  

---

## Current Status Summary

**11 epics tracked:** ✅ 4 complete, 🔄 0 in progress, ⏸️ 0 paused, 7 planned

- ✅ Epic 01 — Researcher
- ✅ Epic 02 — Writer
- 🆕 Epic 03 — Storyteller
- ✅ Epic 04 — Competitive Analysis
- 🆕 Epic 05 — Design
- 🆕 Epic 06 — Demo Generator
- 🆕 Epic 07 — Presentation Builder
- ✅ Epic 08 — Data Analyzer
- 🆕 Epic 09 — Planner
- 🆕 Epic 10 — Prioritizer
- 🆕 Epic 11 — Platform Integrations

### Active Work

| Item | Epic | Owner | Status | Branch | Purpose |
|------|------|-------|--------|--------|---------|
| — | — | — | — | — | No active work |

### Recently Completed

| Item | Epic | Owner | Completed | Notes |
|------|------|-------|-----------|-------|
| researcher-formatter specialist | 01 | Chris | Mar 3, 2026 | Format conversion specialist — receives any research narrative, produces canonical RESEARCH OUTPUT block. Architectural fix for Researcher format compliance. Registered in agent registry. |
| research-chain recipe | 01 | Chris | Mar 3, 2026 | Full four-step pipeline: Researcher → Formatter → Data Analyzer → Writer. Normalizes format at Step 2 before DA/Writer. |
| USING-SPECIALISTS.md | 01/02/04/08 | Chris | Mar 3, 2026 | Practical guide: invoking each specialist, understanding output, chaining patterns, real examples, known limitations. |
| 10 competitive decision briefs | 04 | Chris | Mar 3, 2026 | docs/examples/competitive-briefs/ — real examples from 10-way parallel CA + Writer chain test covering AI providers, CI/CD, IaC, project management, frontend deployment, agent infra, BaaS, dev docs, database, observability. |
| Data Analyzer specialist | 08 | Chris | Mar 3, 2026 | 4-stage pipeline (Parse → Analyze → Quality Gate → Synthesize); AnalysisOutput schema; Writer analysis-output input type; 6 E2E tests passed |
| Researcher-first default for product comparisons | 04 | Chris | Mar 3, 2026 | Implemented as `competitive-analysis-brief-researched` recipe — 3-step chain with Researcher pre-pass |
| CLAIMS TO VERIFY block (Writer) | 02 | Chris | Mar 3, 2026 | Writer flags specific numerical claims from upstream without cited sources |
| competitive-analysis-brief recipes (x2) | 04 | Chris | Mar 3, 2026 | 2-step chain (competitive-analysis → writer) and 3-step with Researcher pre-pass |
| Template improvements | 01/02/04 | Chris | Mar 3, 2026 | Trimmed to 7 sections; Capability format; Why This Matters required; Created line |
| tool-canvas-renderer | 02 | Chris | Mar 3, 2026 | Local pandoc tool module; markdown → DOCX; full Amplifier Tool protocol |
| Section-level source attribution | 02 | Chris | Mar 3, 2026 | `> *Sources: S1, S2*` after each factual section; trust signals at point of reading |
| Competitive Analysis specialist | 04 | Chris | Mar 2, 2026 | 6-stage pipeline; head-to-head + landscape modes; CompetitiveAnalysisOutput schema |
| Citation confidence scoring | 02 | Chris | Mar 2, 2026 | Per-claim confidence in CITATIONS block; no new LLM calls |
| Inline citations | 02 | Chris | Feb 28, 2026 | Post-document CITATIONS block with S1/S2 numbered source claims |
| Writer specialist | 02 | Chris | Feb 27, 2026 | 5-stage pipeline: parse → audit coverage → structure → draft → verify & cite |
| WRITER METADATA block | 02 | Chris | Feb 27, 2026 | Machine-readable header block for downstream agent parsing |
| Coverage auditing | 02 | Chris | Feb 27, 2026 | Pre-write gap analysis surfaces critical gaps before drafting begins |
| Researcher specialist | 01 | Chris | Feb 26, 2026 | 7-stage pipeline with source tiering, quality gate, ResearchOutput v1.0 schema |

---

## Prioritized Future Work

### Immediate Next (This Sprint)

| # | Item | Epic | Owner | Effort | Impact | Why Now |
|---|------|------|-------|--------|--------|---------|
| 0 | ~~**Specialist output format compliance — architectural fix**~~ | 01/02 | Chris | — | — | **Partially shipped 2026-03-03.** Researcher-formatter specialist built — two-step approach normalizes any Researcher output to canonical RESEARCH OUTPUT block before DA/Writer. Researcher format compliance resolved architecturally. Writer structural blocks (WRITER METADATA / CITATIONS / CLAIMS TO VERIFY) remain aspirational — revisit when Amplifier provider supports structured output (PR #38 closed upstream as premature; orchestrator layer must propagate response_format first). |
| 1 | Storyteller specialist | 03 | Chris | L | H | Transforms research/analysis into compelling narratives; natural next specialist after Researcher → Analyzer → Writer chain is complete |

### Near-term (Next 1-2 Sprints)

| # | Item | Epic | Owner | Effort | Impact | Rationale |
|---|------|------|-------|--------|--------|-----------|
| 1 | Storyteller specialist | 03 | Chris | L | H | Transforms research/analysis into compelling narratives; high-demand for knowledge workers |
| 2 | Presentation Builder specialist | 07 | Gurkaran Singh | L | H | Closes the research → write → present chain; slide deck output is a top knowledge worker use case |
| 3 | Coverage audit severity levels | 02 | Chris | S | M | `gap_policy` input lets orchestrators decide what gap severity blocks vs. warns vs. passes |
| 5 | Researcher: conservative confidence scoring for analyst estimates | 01 | Chris | S | M | Financial figures (ARR, market share) from secondary/circulated sources rated high confidence alongside audited data — needs stronger source-tier guidance for analyst estimates vs. primary financial data *(from test log 2026-03-02)* |

### Medium-term (Next Quarter)

**Epic 05 — Design Specialist:**
- Design specialist — translates briefs and research into structured design direction: principles, visual language, component guidance, constraints

**Epic 06 — Demo Generator Specialist:**
- Demo generator — reverse-engineers a persuasive arc from a product; identifies wow moments, sequences for impact, generates script and talking points

**Epic 09 — Planner Specialist:**
- Planner specialist — transforms goals and context into structured plans: milestones, dependencies, timelines, risk flags

**Epic 10 — Prioritizer Specialist:**
- Prioritizer specialist — takes a list of items and context, applies a prioritization framework (impact/effort, MoSCoW, RICE, etc.), returns a ranked, justified output

**Epic 02 — Writer Enhancements:**
- Brand voice / style configuration (`voice_config` input: prohibited terms, tone directives, required terminology)
- Source confidence threshold (`min_source_confidence` filter; claims below threshold flagged in coverage audit)

### Long-term (Future Quarters)

**Epic 11 — Platform Integrations:**
- LangChain / LangGraph wrapper package (thin wrapper for Writer; closes ecosystem presence gap)
- Additional platform integrations TBD

**Future Specialists:**
- Fact-checker specialist
- Editor specialist
- Additional domain specialists TBD

---

### Big Ideas

High-potential concepts worth designing properly when the time is right. Not yet sized or scheduled.

#### 💡 Ecosystem Comparison Recipe (`ecosystem-comparison-chain`)

**Origin:** Emerged from a session running `research-chain` three times in parallel (Microsoft, Anthropic/Claude Code, OpenAI, AI coding tools) and synthesizing cross-ecosystem signals by hand. The cross-chain consensus signals — findings that appeared independently across all three runs — proved more trustworthy than any single chain's output, because they came from independent research with no shared sourcing. That's triangulation, and it should be built into the tool.

**The idea:** A new `ecosystem-comparison-chain.yaml` recipe that accepts a research question + list of ecosystems, fans out to a Researcher per ecosystem, aggregates all outputs, and passes them to a synthesis Writer that leads with cross-ecosystem consensus, then surfaces ecosystem-specific differentiated signals.

**Proposed pipeline:**
```
Input: research_question + ecosystems [{name, question}]
  ↓
[foreach ecosystem] Researcher → Formatter → Analyzer
  ↓ (all results aggregated)
Synthesis Writer → cross-ecosystem comparative brief
  - Leads with signals appearing across ALL ecosystems (highest confidence)
  - Surfaces ecosystem-specific differentiated findings
  - Ends with unified verdict and skill/decision priority ranking
```

**Design decisions to resolve before building:**
1. Does the recipe system support `foreach` at the step level? (parallel vs. sequential matters significantly for runtime)
2. How does the synthesis Writer handle N aggregated inputs of variable size? Needs explicit prompt design, not just summarization
3. Keep `research-chain.yaml` clean (Option A: separate recipe) vs. add `comparison_mode` flag to existing recipe (Option B: backwards-compatible but adds complexity)
4. Recommendation: Option A — new dedicated recipe; the use case is distinct enough in output shape and Writer prompt to deserve its own file

**Why this matters:** Single-chain research surfaces what's true for one ecosystem. Cross-chain synthesis surfaces what's *structurally* true — the signals robust enough to appear independently across multiple research contexts. That's a meaningfully higher confidence tier, and it currently requires manual orchestration.

---

## Epic Completion Status

| Epic | Implemented | Future | % Complete |
|------|-------------|--------|------------|
| 01 — Researcher | Researcher V1, source tiering, quality gate, ResearchOutput v1.0, researcher-formatter, research-chain recipe | Source confidence threshold | 95% |
| 02 — Writer | Writer V1, coverage audit, citations + attribution, WRITER METADATA, citation confidence, rendering (pandoc) | Brand voice config, audit severity, source confidence threshold | 80% |
| 03 — Storyteller | — | Full specialist implementation | 0% |
| 04 — Competitive Analysis | 6-stage pipeline, head-to-head + landscape modes, CompetitiveAnalysisOutput schema, 2-step + 3-step recipes, researcher-first default, CLAIMS TO VERIFY block | — | 100% |
| 05 — Design | — | Full specialist implementation | 0% |
| 06 — Demo Generator | — | Full specialist implementation | 0% |
| 07 — Presentation Builder | — | Full specialist implementation | 0% |
| 08 — Data Analyzer | 4-stage pipeline, AnalysisOutput schema, Writer analysis-output integration, 6 E2E tests | — | 100% |
| 09 — Planner | — | Full specialist implementation | 0% |
| 10 — Prioritizer | — | Full specialist implementation | 0% |
| 11 — Platform Integrations | — | LangChain wrapper, rendering integrations | 0% |

**Overall: 4 specialists shipped, 6 planned, 1 integrations epic**

---

## How to Use This Backlog

**For Planning Sessions:**
1. Review Current Status Summary to know what's active and recently completed
2. Pull from Immediate Next for this sprint's work
3. Move completed items to Recently Completed with date and notes

**For Team:**
- Immediate Next = committed to shipping this sprint
- Near-term = scoped and ready, next up after current sprint
- Medium/Long-term = directional, not yet sized or scheduled

**For Stakeholders:**
- Epic Completion Status shows overall progress across the specialist library
- Immediate Next shows what's shipping soonest

---

## Effort Legend
- **S (Small):** 1–3 days
- **M (Medium):** 1–2 weeks
- **L (Large):** 2–4 weeks

## Impact Legend
- **H (High):** Core differentiator or major user value
- **M (Medium):** Valuable but not critical
- **L (Low):** Nice to have

---

## Change History

| Version | Date | Person | Changes |
|---------|------|--------|---------|
| v1.7 | Mar 3, 2026 | Chris | Added Big Ideas section; first entry: ecosystem-comparison-chain recipe (cross-ecosystem research synthesis) |
| v1.6 | Mar 3, 2026 | Chris | Added researcher-formatter + research-chain to recently completed; updated Item #0 to partially shipped; Epic 01 to 95%; USING-SPECIALISTS.md and 10 competitive briefs logged |
| v1.5 | Mar 3, 2026 | Chris | Marked Epic 08 complete; Data Analyzer added to recently completed; Storyteller promoted to Immediate Next; 4 specialists shipped |
| v1.4 | Mar 2, 2026 | Chris | Moved researcher-first default to recently completed (implemented as 3-step recipe); removed from near-term; updated Epic 04 completion row to reflect all shipped work |
| v1.3 | Mar 3, 2026 | Chris | Marked Epic 04 complete; added tool-canvas-renderer, section attribution, citation confidence to recently completed; removed shipped items from future work; updated Epic 02 to 80%, Epic 04 to 100%; 3 specialists shipped |
| v1.2 | Mar 2, 2026 | Chris | Added 3 near-term items from Notion/Obsidian test log: recipe encoding, researcher-first default, writer confidence gap surfacing |
| v1.1 | Mar 2, 2026 | Chris | Expanded to 10 specialists; updated target audience to knowledge workers + consumers; retired ROADMAP.md |
| v1.0 | Mar 2, 2026 | Chris | Initial backlog |

---

*This backlog is the strategic planning view. Epic Future sections contain details.*
