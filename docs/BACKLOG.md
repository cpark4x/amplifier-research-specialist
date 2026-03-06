# Product Backlog

**Purpose:** Strategic planning view for canvas-specialists — a library of best-in-class, single-domain AI specialist agents for knowledge worker and consumer scenarios  
**Owner:** Chris Park  
**Last Updated:** March 5, 2026  

---

## Strategic Roadmap

See [**2026-03-05-world-class-roadmap.md**](plans/2026-03-05-world-class-roadmap.md) for the 4-phase strategic direction: Phase 1 NOW (solidify foundations), Phase 2 NEXT (expand specialists), Phase 3 LATER (ecosystem synthesis), Phase 4 CI/Polish (production readiness).

---

## Current Status Summary

**11 epics tracked:** ✅ 4 complete, 🔄 1 in progress, ⏸️ 0 paused, 6 planned

- ✅ Epic 01 — Researcher
- ✅ Epic 02 — Writer
- 🔄 Epic 03 — Storyteller
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
| Storyteller specialist | 03 | Chris | 🔄 In Progress | main | Cognitive mode translation — transforms research/analysis into compelling narrative |

### Recently Completed

| Item | Epic | Owner | Completed | Notes |
|------|------|-------|-----------|-------|
| Recipe output file-save step | 01/02/04 | Chris | Mar 3, 2026 | Added `save` step to all three recipes (research-chain, competitive-analysis-brief, competitive-analysis-brief-researched). Uses `foundation:file-ops` to write final_document to `docs/research-output/[kebab-slug].md` — fixes truncation of long documents in recipe summary display. All recipes bumped to v1.1.0. |
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


### Near-term (Next 1-2 Sprints)

| # | Item | Epic | Owner | Effort | Impact | Rationale |
|---|------|------|-------|--------|--------|-----------|

| 2 | Presentation Builder specialist | 07 | Gurkaran Singh | L | H | Closes the research → write → present chain; slide deck output is a top knowledge worker use case |
| 3 | Coverage audit severity levels | 02 | Chris | S | M | `gap_policy` input lets orchestrators decide what gap severity blocks vs. warns vs. passes |
| 5 | Researcher: conservative confidence scoring for analyst estimates | 01 | Chris | S | M | Financial figures (ARR, market share) from secondary/circulated sources rated high confidence alongside audited data — needs stronger source-tier guidance for analyst estimates vs. primary financial data. Add numeric-claim confidence gating for market/competitive briefs *(from test log 2026-03-02; reinforced by mining report 2026-03-05)* |
| 6 | Writer: enforce word budget per format | 02 | Chris | S | H | `brief` produces ~1,500 words — same as a report. Format is a contract, not a label. brief ~600 words, report ~1,500, executive summary ~400. Observed across all 4 runs in 2026-03-04 chain test. |
| 7 | Writer: strengthen audience calibration | 02 | Chris | S | M | `audience: myself` produced identical register to `audience: executive stakeholders` — third-person, formal, presentation-ready. Should shift to direct, first-person, actionable voice. *(from test log 2026-03-04)* |
| 8 | Recipe display: filter internal scaffolding from summary | 01/02/04 | Chris | S | M | Raw claim IDs (S1–S45) from the Analyzer's internal pipeline appeared in the `final_output` recipe summary field. Internal scaffolding should not be user-facing. Display/recipe layer issue. *(from test log 2026-03-04)* |
| 9 | Writer: specificity enforcement | 02 | Chris | S | M | When the research question names a specific subject, the Writer's bottom line and skills sections drifted to generic AI-era conclusions that apply to any tech company. Final layer should pull subject-specific findings through. *(from test log 2026-03-04)* |
| 10 | Platform UX: default chain completion + narrated execution | 01/02/04/08 | Chris | M | H | Two related problems observed across all specialists: (1) conversational invocations (e.g. "run a competitive analysis") return raw intermediate output — `CompetitiveAnalysisOutput`, `ResearchOutput` — instead of a finished document. Users want the polished end product by default; raw output should be opt-in for developers/pipeline use. (2) Users have no visibility into which specialists ran or in what order. Each specialist should narrate its execution so the chain is transparent. Fix should be applied platform-wide across all specialists, not per-specialist. *(observed during session 2026-03-04)* |
| 11 | Recipe timeout resilience: patch research-chain and narrative-chain timeouts | 01/03 | Chris | M | M | Increase `research-chain.yaml` `format-research` step timeout and bound research output to prevent downstream timeouts. Increase `narrative-chain.yaml` `save` step timeout and/or refactor save step to remove LLM agent dependency (use foundation:file-ops directly instead). Note: parallel recipe execution amplifies queueing effects and should be avoided for heavy runs. *(identified after manual A/B/C testing 2026-03-04)* |
| 12 | Researcher: require URL-per-claim in FINDINGS | 01 | Chris | S | M | Source *names* are not sufficient for independent verification; require URLs for each substantive claim to reduce unverifiable assertions. *(from mining report 2026-03-05)* |
| 13 | Writer: document parse-line-first output ordering in spec | 02 | Chris | S | S | The parse-line anchor (`Parsed: ...`) is now the literal first output line, not `WRITER METADATA` directly. Update Output Structure spec (specialists/writer/index.md lines 52, 57) to document this accurately. *(from test log 2026-03-03)* |
| 14 | Writer: enforce required structural sections for analysis-based inputs | 02 | Chris | S | M | If WRITER METADATA / CITATIONS / CLAIMS TO VERIFY are required for analysis-output inputs, enforce or explicitly relax requirements. Run Writer-only test passing AnalysisOutput to confirm behavior. *(from mining report 2026-03-05)* |
| 15 | Writer: add deduplication pass before final output | 02 | Chris | S | M | Lightweight scan to remove duplicated content across sections before conclusion. Prevents repetition across sections observed in chain test outputs. *(from mining report 2026-03-05)* |
| 16 | Data Analyzer: harden Format B detection for narrative markdown | 08 | Chris | S | M | Current detection struggles with fully narrative inputs; improve robustness so claims/sources extraction is consistent across all input types. *(from mining report 2026-03-05)* |
| 17 | Data Analyzer: prevent code-fence wrapping of ANALYSIS OUTPUT | 08 | Chris | S | M | Code-fence wrapping breaks parsers that expect raw section headers/blocks; enforce "no extra fencing" around structured outputs. *(from mining report 2026-03-05)* |
| 18 | Storyteller: surface inferences in NARRATIVE SELECTION for auditability | 03 | Chris | S | S | Clarify whether AnalysisOutput inferences should be listed in NARRATIVE SELECTION (as included/omitted) or treated as background context. Current behavior silently consumes them, reducing auditability of the inference layer. *(from test log 2026-03-04)* |
| 19 | Storyteller: add quality_threshold as optional caller parameter | 03 | Chris | S | S | Accept `quality_threshold` parameter (like Researcher/Analyzer) to let callers request stricter quality gate behavior. Currently hardcoded to `standard`. *(from test log 2026-03-04)* |
| 20 | Require URL-per-claim capture in Researcher outputs | TBD | Chris | TBD | TBD | Source *names* are not sufficient for independent verification; require URLs for each substantive claim to reduce unverifiable assertions. *(from mining report 2026-03-05; id: mine-2026-03-05-require-url-per-claim-capture-in-researcher-outputs)* |
| 21 | Add numeric-claim confidence gating for market/competitive briefs | TBD | Chris | TBD | TBD | ARR/market-share style numbers are repeatedly flagged as the weakest link; add explicit confidence + “cannot verify” handling and push Writer to surface gaps. *(from mining report 2026-03-05; id: mine-2026-03-05-add-numeric-claim-confidence-gating-for-market-competitive-briefs)* |
| 22 | Stabilize Researcher canonical output header/anchor (Stage 0 / “RESEARCH OUTPUT”) | TBD | Chris | TBD | TBD | The “opening block” normalization is not reliably triggering across topics, breaking downstream parsing assumptions. *(from mining report 2026-03-05; id: mine-2026-03-05-stabilize-researcher-canonical-output-header-anchor-stage-0-research-output)* |
| 23 | Harden Data Analyzer Format B detection for narrative markdown | TBD | Chris | TBD | TBD | Current detection struggles with fully narrative inputs; improve robustness so claims/sources extraction is consistent. *(from mining report 2026-03-05; id: mine-2026-03-05-harden-data-analyzer-format-b-detection-for-narrative-markdown)* |
| 24 | Prevent Data Analyzer from wrapping ANALYSIS OUTPUT in code fences | TBD | Chris | TBD | TBD | Code-fence wrapping can break parsers that expect raw section headers/blocks; enforce “no extra fencing” around structured outputs. *(from mining report 2026-03-05; id: mine-2026-03-05-prevent-data-analyzer-from-wrapping-analysis-output-in-code-fences)* |
| 25 | Package common comparison flows as recipes (e.g., competitive-analysis → writer; optionally researcher-first) | TBD | Chris | TBD | TBD | Product comparisons repeatedly benefit from a consistent multi-step pipeline; encode as a single invokable recipe to reduce manual chaining and variance. *(from mining report 2026-03-05; id: mine-2026-03-05-package-common-comparison-flows-as-recipes-e-g-competitive-analysis-writer)* |

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
| 03 — Storyteller | StoryOutput schema, 5-stage pipeline, NARRATIVE SELECTION, narrative-chain recipe | Compound tones, structured NARRATIVE SELECTION format | 90% |
| 04 — Competitive Analysis | 6-stage pipeline, head-to-head + landscape modes, CompetitiveAnalysisOutput schema, 2-step + 3-step recipes, researcher-first default, CLAIMS TO VERIFY block | — | 100% |
| 05 — Design | — | Full specialist implementation | 0% |
| 06 — Demo Generator | — | Full specialist implementation | 0% |
| 07 — Presentation Builder | — | Full specialist implementation | 0% |
| 08 — Data Analyzer | 4-stage pipeline, AnalysisOutput schema, Writer analysis-output integration, 6 E2E tests | Format B detection hardening, code-fence prevention | 100% |
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
| v2.1 | Mar 5, 2026 | Chris | Promoted 6 mining report items (2026-03-05) to Near-term backlog: Require URL-per-claim capture in Researcher output; Add numeric-claim confidence gating for market/com; Stabilize Researcher canonical output header/ancho; Harden Data Analyzer Format B detection for narrat; Prevent Data Analyzer from wrapping ANALYSIS OUTPU; +1 more |
| v2.0 | Mar 5, 2026 | Chris | Promoted mining report recommendations (2026-03-05) into near-term backlog; merged numeric-confidence gating into item #5; added 8 new Researcher/Writer/Data Analyzer/Storyteller near-term items (#12–#19) from mining report; updated Epic 08 future work; closed 4 unpromoted test logs by marking action_items_promoted=true |
| v1.9 | Mar 4, 2026 | Chris | Epic 03 (Storyteller) moved to in-progress; specialist, schema, recipe, epic, user stories, principles, metrics all shipped |
| v1.8 | Mar 4, 2026 | Chris | Added near-term items 6–9 from test log 2026-03-04: Writer word budget, audience calibration, recipe display scaffolding, Writer specificity drift |
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
