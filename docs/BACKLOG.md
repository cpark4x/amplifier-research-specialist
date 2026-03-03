# Product Backlog

**Purpose:** Strategic planning view for canvas-specialists — a library of best-in-class, single-domain AI specialist agents for knowledge worker and consumer scenarios  
**Owner:** Chris Park  
**Last Updated:** March 3, 2026  

---

## Current Status Summary

**11 epics tracked:** ✅ 3 complete, 🔄 0 in progress, ⏸️ 0 paused, 8 planned

- ✅ Epic 01 — Researcher
- ✅ Epic 02 — Writer
- 🆕 Epic 03 — Storyteller
- ✅ Epic 04 — Competitive Analysis
- 🆕 Epic 05 — Design
- 🆕 Epic 06 — Demo Generator
- 🆕 Epic 07 — Presentation Builder
- 🆕 Epic 08 — Data Analyzer
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
| 1 | Data Analyzer specialist | 08 | Chris | L | H | Unlocks the core pipeline: Researcher → Analyzer → Writer; facts vs. inferences explicitly labeled |

### Near-term (Next 1-2 Sprints)

| # | Item | Epic | Owner | Effort | Impact | Rationale |
|---|------|------|-------|--------|--------|-----------|
| 1 | Storyteller specialist | 03 | Chris | L | H | Transforms research/analysis into compelling narratives; high-demand for knowledge workers |
| 2 | Presentation Builder specialist | 07 | Chris | L | H | Closes the research → write → present chain; slide deck output is a top knowledge worker use case |
| 3 | Recipe: encode competitive-analysis → writer chain | 04 | Chris | S | H | Chain is proven but manually dispatched; a single invokable recipe removes orchestration friction *(from test log 2026-03-02)* |
| 4 | Researcher-first default for product comparisons | 04 | Chris | S | H | Self-research path skips source tiering; Researcher pre-pass surfaces per-claim confidence before competitive-analysis runs *(from test log 2026-03-02)* |
| 5 | Writer: "claims to verify" block for unsourced specifics | 02 | Chris | S | M | When upstream output contains specific numerical claims without citations, Writer should flag them rather than passing at uniform confidence *(from test log 2026-03-02)* |
| 6 | Coverage audit severity levels | 02 | Chris | S | M | `gap_policy` input lets orchestrators decide what gap severity blocks vs. warns vs. passes |
| 7 | Researcher: conservative confidence scoring for analyst estimates | 01 | Chris | S | M | Financial figures (ARR, market share) from secondary/circulated sources rated high confidence alongside audited data — needs stronger source-tier guidance for analyst estimates vs. primary financial data *(from test log 2026-03-02)* |

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

## Epic Completion Status

| Epic | Implemented | Future | % Complete |
|------|-------------|--------|------------|
| 01 — Researcher | Researcher V1, source tiering, quality gate, ResearchOutput v1.0 | Source confidence threshold | 90% |
| 02 — Writer | Writer V1, coverage audit, citations + attribution, WRITER METADATA, citation confidence, rendering (pandoc) | Brand voice config, audit severity, source confidence threshold | 80% |
| 03 — Storyteller | — | Full specialist implementation | 0% |
| 04 — Competitive Analysis | 6-stage pipeline, head-to-head + landscape modes, CompetitiveAnalysisOutput schema | Recipe encoding, researcher-first default | 100% |
| 05 — Design | — | Full specialist implementation | 0% |
| 06 — Demo Generator | — | Full specialist implementation | 0% |
| 07 — Presentation Builder | — | Full specialist implementation | 0% |
| 08 — Data Analyzer | — | Full specialist implementation | 0% |
| 09 — Planner | — | Full specialist implementation | 0% |
| 10 — Prioritizer | — | Full specialist implementation | 0% |
| 11 — Platform Integrations | — | LangChain wrapper, rendering integrations | 0% |

**Overall: 3 specialists shipped, 7 planned, 1 integrations epic**

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
| v1.3 | Mar 3, 2026 | Chris | Marked Epic 04 complete; added tool-canvas-renderer, section attribution, citation confidence to recently completed; removed shipped items from future work; updated Epic 02 to 80%, Epic 04 to 100%; 3 specialists shipped |
| v1.2 | Mar 2, 2026 | Chris | Added 3 near-term items from Notion/Obsidian test log: recipe encoding, researcher-first default, writer confidence gap surfacing |
| v1.1 | Mar 2, 2026 | Chris | Expanded to 10 specialists; updated target audience to knowledge workers + consumers; retired ROADMAP.md |
| v1.0 | Mar 2, 2026 | Chris | Initial backlog |

---

*This backlog is the strategic planning view. Epic Future sections contain details.*
