# Product Backlog

**Purpose:** Strategic planning view for canvas-specialists — a library of best-in-class, single-domain AI specialist agents for knowledge worker and consumer scenarios  
**Owner:** Chris Park  
**Last Updated:** March 19, 2026 (v4.2)  

---

## Strategic Roadmap

See [**2026-03-05-world-class-roadmap.md**](plans/2026-03-05-world-class-roadmap.md) for the 4-phase strategic direction: Phase 1 NOW (solidify foundations), Phase 2 NEXT (expand specialists), Phase 3 LATER (ecosystem synthesis), Phase 4 CI/Polish (production readiness).

---

## Current Status Summary

**11 epics tracked:** ✅ 5 complete, 🔄 1 in progress, ⏸️ 0 paused, 5 planned

- ✅ Epic 01 — Researcher
- ✅ Epic 02 — Writer
- 🔄 Epic 03 — Storyteller
- ✅ Epic 04 — Competitive Analysis
- 🆕 Epic 05 — Design
- 🆕 Epic 06 — Demo Generator
- 🆕 Epic 07 — Presentation Builder
- ✅ Epic 08 — Data Analyzer
- 🆕 Epic 09 — Planner
- ✅ Epic 10 — Prioritizer
- 🆕 Epic 11 — Platform Integrations

### Active Work

| Item | Epic | Owner | Status | Branch | Purpose |
|------|------|-------|--------|--------|---------|
| Storyteller specialist | 03 | Chris | 🔄 In Progress | main | Cognitive mode translation — transforms research/analysis into compelling narrative |

### Recently Completed

| Item | Epic | Owner | Completed | Notes |
|------|------|-------|-----------|-------|
| DA-formatter specialist (#34) | 08 | Chris | Mar 10, 2026 | `specialists/data-analyzer-formatter/index.md` — fifth formatter, 2-input, 4-stage pipeline, Option A traces_to. Rule 8 in coordinator. `format-analysis` step in research-chain v1.6.0. Spot test PASS. *(test log 2026-03-10-da-formatter-spot-test)* |
| DA Format B hardening (#16) | 08 | Chris | Mar 10, 2026 | Conditional close. Added "Special handling — pure prose inputs" to Format B detection: sentence-by-sentence, min 3 findings/paragraph, compound-sentence splitting. Format B with labels validated. Pure prose (no labels) deferred. *(test log 2026-03-10-da-format-hardening)* |
| DA code-fence prevention (#17) | 08 | Chris | Mar 10, 2026 | Stage 4 self-check added. ANALYSIS OUTPUT emitted as bare text, no code fences, on second test run. *(test log 2026-03-10-da-format-hardening)* |
| Writer informal register compliance (#29) | 02 | Chris | Mar 10, 2026 | Closed via formatter architectural fix. Writer-formatter handles `audience=myself` failure mode (no structural blocks) — produces canonical Writer output block regardless. Two previous instruction-based fixes did not hold; formatter is the reliable catch. Validated clean pass. *(test log 2026-03-10-writer-informal-register-verification)* |
| Storyteller OUTPUT CONTRACT compliance (#30) | 03 | Chris | Mar 10, 2026 | Closed via formatter architectural fix. Story-formatter handles markdown document failure mode (no STORY OUTPUT header, no NARRATIVE SELECTION) — normalizes to canonical block. Validated clean pass on full Acme Corp board narrative test. *(test log 2026-03-10-storyteller-format-compliance-verification)* |
| Storyteller inference auditability in NARRATIVE SELECTION (#18) | 03 | Chris | Mar 10, 2026 | Verified via story-formatter chain. All 3 inferences from AnalysisOutput appeared in INCLUDED FINDINGS with `(inference)` label and narrative role. Spec change from 2026-03-06 confirmed working end-to-end. *(test log 2026-03-10-storyteller-format-compliance-verification)* |
| Storyteller quality_threshold parameter (#19) | 03 | Chris | Mar 10, 2026 | Spec-complete. `standard` path validated; Stage 1 detection and Stage 5 behavior correct. `high` threshold deferred validation. *(test log 2026-03-10-storyteller-format-compliance-verification)* |
| Prioritizer-formatter specialist (#33) | 10 | Chris | Mar 10, 2026 | `specialists/prioritizer-formatter/index.md` built from formatter template (fourth application of established pattern). Handles both `block` format (pass-through with normalization) and `prose` format (the failure mode — extracts rankings from markdown prose, infers priority labels from impact/effort language). Registered in `behaviors/specialists.yaml`. Added Rule 7 to `context/specialists-instructions.md` (mandatory gate + matched-pair description + agent ID + Typical Chain entry). Test: prose-format prioritizer input → canonical PRIORITY OUTPUT block, PASS. *(test log 2026-03-10-prioritizer-formatter-spot-test)* |
| Researcher output truncation gate (#35) | 01 | Chris | Mar 10, 2026 | Researcher output truncation — ~50% of runs produce truncated metadata summary instead of full research. `validate-research` gate added to research-chain v1.9.0 and narrative-chain v1.3.0. Monitors GATE_FAIL rate and provides signal for future auto-retry logic if frequent. Priority 1, Effort S, Impact H. *(status: monitoring, contingent on auto-retry investigation)* **Update 2026-03-18:** 3/3 consecutive runs (2026-03-06, 2026-03-18 A/B, 2026-03-18 re-run) show identical truncation pattern — researcher completes 21+ tool calls, then emits conversational summary instead of canonical RESEARCH OUTPUT block. Recovers on session resumption every time. Auto-retry should be promoted from deferred note to tracked backlog item. *(test log 2026-03-18-rto-rerun-writer-fixes-37-38)* |
| Recipe timeout resilience: research-chain save step (#11) | 01 | Chris | Mar 9, 2026 | Split monolithic `save` step into `derive-filename` (120s, slug only) + `save` (300s, mechanical write). Root cause: combined filename derivation + 20k-byte document write exceeded 120s ceiling every run. format-research and write timeouts fixed earlier in `07c7c38`; this closes the last open piece. research-chain bumped to v1.3.0. Validated: full 6-step pipeline completed cleanly on Mistral AI test run. *(test log 2026-03-09-research-chain-v130-save-fix)* |
| Prioritizer specialist | 10 | Chris | Mar 9, 2026 | 4-stage pipeline (Parse → Analyze → Quality Gate → Synthesize); PrioritizerOutput schema with per-item ranked output using explicit frameworks (MoSCoW, impact-effort, RICE, weighted scoring); 2–3 sentence rationale per item; unrankable items listed explicitly. Wired as Amplifier agent at `specialists:prioritizer`. |
| Writer quality fixes: CLAIMS TO VERIFY surfacing, audience calibration, specificity enforcement | 02 | Chris | Mar 6, 2026 | Backlog #28, #7, #9. Three surgical edits to `specialists/writer/index.md`: (1) CLAIMS TO VERIFY moved before WRITER METADATA/CITATIONS and extended to all input types including researcher-output (medium/low confidence claims now flagged); (2) `myself`/`me` audience no longer remapped to `technical decision-maker` — first-person direct register; audience register table added to Stage 4; Stage 5 voice check expanded with audience differentiation test; (3) Specificity gate added to Stage 5 — bottom line must not survive [SUBJECT] substitution. Validated: #7 and #9 confirmed working in Mistral AI test run. #28 partial — inline caveat surfacing worked, formal block absent due to `myself` register slip; patched register table immediately. |
| Researcher-Formatter architecture refactor | 01 | Chris | Mar 6, 2026 | Backlog #22. Architectural reframe: stripped ~150 lines of format enforcement from researcher (OUTPUT CONTRACT, Stage 0, Stage 7 template, COMPLIANCE NOTE, SELF-CHECK, wrong/right examples). Added compact output expectations ("do not worry about exact output formatting — the formatter handles that"). Promoted formatter from optional cleanup to essential pipeline stage with validation rules (numeric→categorical confidence mapping ≥0.8→high/0.5–0.79→medium/<0.5→low, T1→primary tier normalization, URL validation, removed pass-through mode). Updated coordinator Rule 5 from apologetic (~1 in 3 framing) to intentional (matched pair by design). Updated recipe prompt, types.md, SUCCESS-METRICS.md. Root cause: format enforcement doesn't work after 10-20+ tool calls of narrative research context. Solution: accept researcher produces evidence naturally, formatter produces format — two different cognitive tasks. Validated: 43 claims, all confidence categorical, all tiers full labels on "What is Jina AI?" run. |
| Coordinator: enforce formatter step (Rule 5) | 01/02 | Chris | Mar 6, 2026 | Backlog #27. Strengthened Rule 5 in `context/specialists-instructions.md` from a rule statement into an explicit mandatory gate. Added self-check paragraph: coordinator must stop and verify "Did I route through researcher-formatter?" before delegating to writer, data-analyzer, storyteller, or competitive-analysis. Root cause: rule existed but lacked a checkpoint forcing explicit verification. |
| Researcher trustworthiness overhaul — confidence tiers + URL-per-claim + numeric gating | 01 | Chris | Mar 6, 2026 | Backlog #5. Three surgical edits to `specialists/researcher/index.md`: explicit `unrated` ban (Core Principles), full https:// URL required before extracting claims (Stage 3), format enforcement block covering URL rule + `unrated` ban + numeric/financial claim Note field (Stage 4). Fixes 142/142 unrated confidence observed in Mar 6 test log. |
| Writer word budget enforcement | 02 | Chris | Mar 6, 2026 | Backlog #6. Added word budgets for all 6 formats in Stage 3 (Report: 1,200–1,800w · Brief: 250–400w · Proposal: 500–700w · Exec Summary: 150–250w · Email: 100–200w · Memo: 300–500w). Added budget check + trim-from-least-important instruction to Stage 5 step 3. |
| Chain reliability hardening (routing heuristic + narration rules) | 01/02/04/08 | Chris | Mar 5, 2026 | PR #16. Routing heuristic table, "when in doubt, chain" default, tightened narration rules, Writer story-output support. Smoke test: 5/5 scenarios pass, >90% reliability. Closes backlog #10 and #26. |
| promote-mining-items recipe + backlog promotion + module compliance | 01/02 | Chris | Mar 5, 2026 | PR #15. 3-stage promotion recipe (extract → apply → commit), promoted 6 items from 2026-03-05 mining report to backlog #20–#25, fixed hook-specialist-narration and tool-canvas-renderer for module compliance (15/15 health tests pass). |
| Cold-start reliability scaffolding | 01/02 | Chris | Mar 5, 2026 | PR #14. Module health tests, packaging fixes, behavior YAML source path corrections. |
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

Items ordered by impact. Ship these first — they fix the most-flagged quality gaps.

| # | Item | Epic | Owner | Effort | Impact | Why Now |
|---|------|------|-------|--------|--------|---------|
| 0 | ~~**Specialist output format compliance — architectural fix**~~ | 01/02 | Chris | — | — | **Partially shipped 2026-03-03.** Researcher-formatter specialist built — two-step approach normalizes any Researcher output to canonical RESEARCH OUTPUT block before DA/Writer. Researcher format compliance resolved architecturally. Writer structural blocks (WRITER METADATA / CITATIONS / CLAIMS TO VERIFY) remain aspirational — revisit when Amplifier provider supports structured output (PR #38 closed upstream as premature; orchestrator layer must propagate response_format first). |



### Near-term (Next 1-2 Sprints)

Ordered by priority tier then impact. Items marked *(consolidated)* absorbed duplicates — see Consolidation Log below.

**Priority 2 — Quality polish, moderate impact:**

| # | Item | Epic | Owner | Effort | Impact | Rationale |
|---|------|------|-------|--------|--------|-----------|
| ~~29~~ | ~~Writer: OUTPUT CONTRACT compliance for informal registers~~ | 02 | Chris | S | M | **Closed 2026-03-10 via formatter architectural fix.** Writer-formatter handles the informal register failure mode: produces `Parsed:`, `WRITER METADATA`, `CITATIONS`, `CLAIMS TO VERIFY` regardless of Writer output format. Two instruction-based fixes (`0508f95`, OUTPUT CONTRACT block) did not hold; formatter is the reliable architectural catch. Validated: `audience=myself` Writer output → writer-formatter → all structural blocks present, clean pass. *(test log 2026-03-10-writer-informal-register-verification)* |
| ~~30~~ | ~~Storyteller: OUTPUT CONTRACT compliance (STORY OUTPUT header + NARRATIVE SELECTION block)~~ | 03 | Chris | S | H | **Closed 2026-03-10 via formatter architectural fix.** Story-formatter handles the document failure mode: produces `STORY OUTPUT` header, all metadata, `NARRATIVE SELECTION` block regardless of Storyteller output format. Storyteller produced a full markdown document with `##` headers and no STORY OUTPUT structure; story-formatter normalized to canonical block, all 9 findings/inferences classified. Clean pass. *(test log 2026-03-10-storyteller-format-compliance-verification)* |
| ~~31~~ | ~~Prioritizer: add structured output block (`PRIORITY OUTPUT` header)~~ | 10 | Chris | S | M | **Resolved by #33 (prioritizer-formatter)** — Shipped 2026-03-10. Architectural fix applied: prioritizer-formatter specialist handles both block format (pass-through) and prose format (extracts rankings, infers priority labels). Handles the prose failure mode that spec-based fixes could not resolve. *(See Recently Completed entry for #33)* |
| ~~32~~ | ~~Coordinator routing: add Prioritizer trigger for priority list requests~~ | 10 | Chris | XS | M | **VALIDATED 2026-03-09.** Routing fix in `4d56283` confirmed working — coordinator routed automatically on message 1 with no prompting. Input order overridden (dark mode listed first, ranked last). Full chain completed cleanly. *(validated in test log 2026-03-09-routing-validation)* |
| ~~33~~ | ~~Prioritizer-formatter specialist~~ | 10 | Chris | S | H | **Shipped 2026-03-10.** See Recently Completed. |
| ~~22~~ | ~~Stabilize Researcher canonical output header/anchor (Stage 0 / "RESEARCH OUTPUT")~~ | 01 | Chris | — | — | **Promoted to Immediate Next and shipped 2026-03-06.** See Immediate Next #22 entry. |
| 37 | Writer: hedging-to-source-tier mapping | 02 | Chris | S | H | **Shipped 2026-03-18; partially validated 2026-03-19.** Tier-aware hedging mapping implemented in `agents/writer.md` (commit `86197c6`). Over-hedging of strong evidence eliminated across all 3 test topics (RTO, Wasm, AI coding). Under-hedging of medium-confidence tertiary claims inconsistent — works well when tier contrast is visible (AI coding: 8/10) but drops when source base is mostly tertiary (Wasm: 5/10). Enhancement: add medium-claim self-check to Stage 5 (see #39). *(test logs: 2026-03-18-rto-rerun-writer-fixes-37-38, 2026-03-19-writer-fixes-37-38-cross-topic-validation)* |
| 38 | Writer: decision-support template for executive audiences | 02 | Chris | S | M | **Shipped 2026-03-18; fully validated 2026-03-19.** Scenario-based decision implications added to executive register row in `agents/writer.md` (commit `86197c6`). Produces concrete "If X → expect Y" framing across all 3 test topics. No further changes needed. *(test logs: 2026-03-18-rto-rerun-writer-fixes-37-38, 2026-03-19-writer-fixes-37-38-cross-topic-validation)* |
| 39 | Writer: add medium-claim self-check to Stage 5 | 02 | Chris | XS | M | Enhancement to #37. Before returning, writer should scan every medium-confidence claim to verify it has a visible hedge matching the source tier. Current spec explains the mapping but doesn't enforce a self-check scan. Addresses inconsistent under-hedging when source base is predominantly tertiary (Wasm validation: 5/10 hedging accuracy vs AI coding: 8/10). *(test log 2026-03-19-writer-fixes-37-38-cross-topic-validation)* |
| 40 | Writer-formatter: upgrade Stage 3.5 to tier-aware hedging | 02 | Chris | S | M | Stage 3.5 currently applies "reportedly" uniformly to all medium-confidence unhedged claims regardless of source tier. Should differentiate: "research indicates" for primary/secondary medium, "according to [source]"/"reportedly" for tertiary medium. The formatter is the safety net — its hedging model should match the writer spec's tier-aware mapping. *(test log 2026-03-19-writer-fixes-37-38-cross-topic-validation)* |
| 48 | Coordinator routing: broaden analyzer trigger for strategy requests | 01/02/08 | Chris | XS | H | Rule 4 triggers data-analyzer only on "analysis" or "insights." Strategy/research requests ("research the best strategies for X") inherently need fact/inference separation and cross-finding synthesis but don't trigger the analyzer chain. Broaden routing heuristic to include strategy-type requests. Biggest single quality lever in the 9+ gap analysis (~0.5 pts). *(test log 2026-03-19-ai-first-team-collaboration)* |
| 49 | Researcher: iterative deepening for thin sub-questions | 01 | Chris | S | H | When evidence gaps are logged and a sub-question has coverage but lacks practitioner depth (e.g., "no primary sources on internal practices at AI-native companies"), automatically run a second targeted search round (engineering blogs, conference talks, internal practice accounts) before declaring done. Second-biggest quality lever (~0.4 pts). *(test log 2026-03-19-ai-first-team-collaboration)* |
| 50 | Writer: audience-aware technical depth calibration | 02 | Chris | S | M | When audience is not "AI engineers" or "technical practitioners," the writer should translate mechanism-level details (token windows, compaction, sub-agent architectures) into outcome-level language. Strengthen audience calibration gate in writer spec — add a self-check: "Would this sentence make sense to someone who doesn't build AI systems?" (~0.3 pts). *(test log 2026-03-19-ai-first-team-collaboration)* |
| 51 | Writer: prioritize concrete examples over frameworks in briefs | 02 | Chris | XS | M | When the source claim index contains concrete case studies (e.g., enterprise examples with specific metrics), the writer should weave them into strategy sections rather than leaving them in unused claims. Practitioners trust stories > frameworks. Add to Stage 3 structure: "For each strategy, identify the strongest concrete example from the claim index." (~0.2 pts). *(test log 2026-03-19-ai-first-team-collaboration)* |
| 52 | Writer: cross-strategy synthesis for multi-point briefs | 02 | Chris | XS | M | When a brief has 3+ strategies/key points, add a synthesis paragraph (in Implications or a new Connections section) showing how they form a system, not just a list. E.g., "trust enables context sharing → enables orchestration → while coordination practices require people investment." Partly an analyzer gap (#48) and partly a writer instruction gap. (~0.1 pts). *(test log 2026-03-19-ai-first-team-collaboration)* |
| 41 | Researcher: auto-retry on truncation (#35 escalation) | 01 | Chris | S | H | Promote from monitoring to active work. 4/5 pipeline runs show researcher truncation (conversational summary instead of canonical RESEARCH OUTPUT block). validate-research gate catches it correctly but without auto-retry the pipeline cannot self-serve. Implement retry logic: on GATE_FAIL, resume researcher session and request full structured output. *(test logs: 2026-03-18-rto-rerun-writer-fixes-37-38, 2026-03-19-writer-fixes-37-38-cross-topic-validation)* |
| 42 | Recipe engine: investigate conditional branching failure in research-chain v1.10.0 | 01 | Chris | S | M | Smart-skip gates (`check-analysis-format` → `passthrough-analysis` / `format-analysis`) failed — bash step output doesn't match condition syntax (likely trailing whitespace/newline). Both conditions failed, leaving `formatted_analysis` undefined. Wasm validation used linear recipe workaround. *(test log 2026-03-19-writer-fixes-37-38-cross-topic-validation)* |
| 43 | Writer: add `decision-brief` format with 1,500–3,000 word budget | 02 | Chris | S | M | Current "brief" format has 250–400 word budget — impossible for comparative/survey research (13+ subjects). Writer correctly overrode budget in retirement test. Add `decision-brief` format: 1,500–3,000 words, structured for multi-subject comparison with tables. Alternative: make word budgets per-subject (brief = 250–400 × N subjects, capped at 3,000). *(test log 2026-03-19-retirement-research-specialists-vs-direct)* |
| 44 | Writer-formatter: graceful degradation when source material unavailable | 02 | Chris | S | M | Writer-formatter broke in ad-hoc mode — requested original RESEARCH OUTPUT as second input, which the coordinator couldn't re-send (~15K tokens). Formatter should degrade gracefully: if source material not provided, format what you have (extract claims from writer's inline `> *Sources: S1, S2*` attributions, produce partial CITATIONS block, skip S-numbered extraction). Don't block the pipeline. *(test log 2026-03-19-retirement-research-specialists-vs-direct)* |
| 45 | Coordinator: two-path doctrine for ad-hoc vs recipe execution | 01/02 | Chris | S | H | Rules 5–8 (mandatory formatter gates) assume recipe execution where context variables pass dual inputs. In ad-hoc coordinator mode, re-sending ~15K token research output to formatters defeats delegation's token-conservation purpose. Add doctrine: **recipe path** = formatters always (context variables handle handoffs); **ad-hoc path** = formatters optional for human-terminal flows (writer output goes directly to user). Expands #36 lever 5 from "skip-formatters mode" to a first-class coordinator routing concept. *(test log 2026-03-19-retirement-research-specialists-vs-direct)* |
| 46 | Researcher: add `research_mode: breadth` for survey-type questions | 01 | Chris | M | H | Researcher's structured methodology (corroboration requirements, quality gates) prioritizes trustworthiness over breadth. For survey questions ("best places to retire"), breadth matters as much as depth. Direct approach covered 15 destinations vs researcher's 13 because it wasn't constrained by "2+ independent sources per claim." Breadth mode: wider net, lighter corroboration (1 credible source per claim, flag as medium confidence), relaxed quality gate. *(test log 2026-03-19-retirement-research-specialists-vs-direct)* |

**Priority 3 — Important but not urgent:**

| # | Item | Epic | Owner | Effort | Impact | Rationale |
|---|------|------|-------|--------|--------|-----------|
| 3 | Coverage audit severity levels | 02 | Chris | S | M | `gap_policy` input lets orchestrators decide what gap severity blocks vs. warns vs. passes |
| 47 | Researcher: add contrarian sweep step for risk/downside coverage | 01 | Chris | S | M | After the main research loop, run one targeted search for "risks of [subject]" or "downsides of [subject]" to catch deteriorating conditions that positive-framing guides don't emphasize. In the retirement A/B test, the direct approach caught Ecuador's safety deterioration while the researcher missed it — the researcher's sources (retirement guides) are positively framed by default. A contrarian sweep would balance this. *(test log 2026-03-19-retirement-research-specialists-vs-direct)* |
| ~~16~~ | ~~Data Analyzer: harden Format B detection for narrative markdown~~ | 08 | Chris | S | M | **Conditionally closed 2026-03-10.** Added "Special handling — pure prose inputs" section to Format B: sentence-by-sentence extraction, minimum 3 findings per paragraph, compound-sentence splitting. Format B with inline Source/Tier labels validated. Pure-prose extraction (no labels) deferred. *(test log 2026-03-10-da-format-hardening)* |
| ~~17~~ | ~~Data Analyzer: prevent code-fence wrapping of ANALYSIS OUTPUT~~ | 08 | Chris | S | M | **Closed 2026-03-10.** Added Stage 4 self-check: zero-tolerance code-fence verification before emitting. Validated: ANALYSIS OUTPUT produced as bare text, no fences. *(test log 2026-03-10-da-format-hardening)* |
| ~~34~~ | ~~Data Analyzer: da-formatter specialist (architectural fix)~~ | 08 | Chris | S | H | **Shipped 2026-03-10.** `specialists/data-analyzer-formatter/index.md` built — fifth application of formatter pattern. 2-input (DA output + original research). Handles canonical/partial/narrative DA output; strips stage narration prefix; Option A `traces_to: [narrative-mapped: uncertain]`. Registered in `behaviors/specialists.yaml`. Rule 8 added to `context/specialists-instructions.md`. `format-analysis` step added to `recipes/research-chain.yaml` v1.6.0. Spot test: narrative DA input → canonical ANALYSIS OUTPUT block, PASS. *(test log 2026-03-10-da-formatter-spot-test)* |
| 14 | Writer: enforce required structural sections for analysis-based inputs | 02 | Chris | S | M | If WRITER METADATA / CITATIONS / CLAIMS TO VERIFY are required for analysis-output inputs, enforce or explicitly relax requirements. Run Writer-only test passing AnalysisOutput to confirm behavior. *(from mining report 2026-03-05)* |
| 15 | Writer: add deduplication pass before final output | 02 | Chris | S | M | Lightweight scan to remove duplicated content across sections before conclusion. Prevents repetition across sections observed in chain test outputs. *(from mining report 2026-03-05)* |
| 13 | Writer: document parse-line-first output ordering in spec | 02 | Chris | S | S | The parse-line anchor (`Parsed: ...`) is now the literal first output line, not `WRITER METADATA` directly. Update Output Structure spec (specialists/writer/index.md lines 52, 57) to document this accurately. *(from test log 2026-03-03)* **Update 2026-03-05:** Smoke test confirmed `Parsed:` line appears inconsistently — present in competitive→writer chain (Test 3) but absent in researcher→writer chain (Test 1). May be input-type-dependent. |
| ~~18~~ | ~~Storyteller: surface inferences in NARRATIVE SELECTION for auditability~~ | 03 | Chris | S | S | **Verified 2026-03-10.** Spec change shipped 2026-03-06 (v3.0). Verified via story-formatter chain: all 3 inferences from AnalysisOutput input (I1–I3) appeared in INCLUDED FINDINGS with `(inference)` label and narrative role. Not silently consumed. *(test log 2026-03-10-storyteller-format-compliance-verification)* |
| ~~19~~ | ~~Storyteller: add quality_threshold as optional caller parameter~~ | 03 | Chris | S | S | **Spec-complete 2026-03-06; validated 2026-03-10 (standard path).** Stage 1 line 196 detects `quality_threshold: high` from caller; Stage 5 behavior defined for standard vs. high. `standard` path confirmed correct in test run. `high` threshold path (0 revision cycles on structural failure) deferred validation — spec implementation correct. *(test log 2026-03-10-storyteller-format-compliance-verification)* |
| ~~11~~ | ~~Recipe timeout resilience: patch research-chain and narrative-chain timeouts~~ | 01/03 | Chris | — | — | **Shipped 2026-03-09.** See Recently Completed. |

**Priority 4 — Separate track (new capabilities / UX):**

| # | Item | Epic | Owner | Effort | Impact | Rationale |
|---|------|------|-------|--------|--------|-----------|
| 2 | Presentation Builder specialist | 07 | Gurkaran Singh | L | H | Closes the research → write → present chain; slide deck output is a top knowledge worker use case |
| 25 | Package common comparison flows as recipes | 04 | Chris | S | M | Product comparisons repeatedly benefit from a consistent multi-step pipeline; encode as a single invokable recipe to reduce manual chaining and variance. *(from mining report 2026-03-05)* |
| 8 | Recipe display: filter internal scaffolding from summary | 01/02/04 | Chris | S | M | Raw claim IDs (S1–S45) from the Analyzer's internal pipeline appeared in the `final_output` recipe summary field. Internal scaffolding should not be user-facing. Display/recipe layer issue. *(from test log 2026-03-04)* |
| 36 | Pipeline token/cost optimization | 01/02/03/08 | — | M | H | Deep chain spawns 5+ agent sessions sequentially; formatters add 3–4 sessions that may not need heavy models. Five levers: (1) **Formatter consolidation** — run formatting as tool call within preceding specialist's session instead of spawning new agent, cutting 3–4 sessions from deep chain; (2) **Model routing** — route formatters to `fast` tier (Haiku-class) since they extract/reformat, not reason; (3) **Smart depth detection** — reduce accidental deep-chain triggers via better UX routing; (4) **Research caching** — cache ResearchOutput with TTL to cut repeat queries to near-zero cost; (5) **Skip-formatters mode** — for human-terminal workflows where no downstream agent consumes output, offer `depth=quick` path (researcher → writer, skip formatters and analyzer), cutting latency roughly in half. Levers 1–2 are low-hanging fruit; 3 is UX; 4–5 are higher effort/higher payoff. **Update 2026-03-19:** Lever 5 urgency elevated — retirement A/B test demonstrated writer-formatter breaking in ad-hoc mode (two-input contract not satisfiable when coordinator can't re-send ~15K token research output). See #45 for two-path doctrine design. *(from pitch discussion 2026-03-16; lever 5 from A/B tests 2026-03-18 and 2026-03-19)* |

**Shipped / Closed:**

| # | Item | Status |
|---|------|--------|
| ~~10~~ | ~~Platform UX: default chain completion + narrated execution~~ | **Shipped in PR #16 (Mar 5, 2026).** |
| ~~26~~ | ~~Clarify ambiguity boundary for casual prompts in chain instructions~~ | **Shipped in PR #16 (Mar 5, 2026).** |

### Consolidation Log

Items merged during prioritization pass (2026-03-06):

| Absorbed | Into | Rationale |
|----------|------|-----------|
| #12 (Researcher URL-per-claim) | **#5** | Same root cause: researcher trustworthiness. URL-per-claim is one facet of the overhaul. |
| #20 (Require URL-per-claim — mining report duplicate) | **#5** | Duplicate of #12, both now in #5. |
| #21 (Numeric-claim confidence gating) | **#5** | Confidence gating is inseparable from confidence tiers — same implementation scope. |
| #23 (Harden DA Format B — mining report duplicate) | **#16** | Exact duplicate of #16. |
| #24 (Prevent DA code fences — mining report duplicate) | **#17** | Exact duplicate of #17. |

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
| 10 — Prioritizer | Prioritizer V1 — 4-stage pipeline, PrioritizerOutput schema, impact-effort + MoSCoW + RICE + weighted scoring, prioritizer-formatter specialist | quality_threshold:high validation, pipeline integration testing | 95% |
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
| v4.2 | Mar 19, 2026 | Chris | AI-first team collaboration research chain test (researcher → formatter → writer → writer-formatter). Scored 7.5/10; post-run "9+ gap analysis" identified 5 specific improvements mapped to responsible specialists. Added #48 (coordinator analyzer trigger broadening), #49 (researcher iterative deepening), #50 (writer audience-aware depth calibration), #51 (writer concrete examples over frameworks), #52 (writer cross-strategy synthesis). Test log: 2026-03-19-ai-first-team-collaboration. |
| v4.1 | Mar 19, 2026 | Chris | Retirement A/B test (specialists 4-agent chain vs direct web-research). Writer-formatter broke in ad-hoc mode — two-input contract not satisfiable when coordinator can't re-send ~15K token research output. Added #43 (decision-brief format), #44 (writer-formatter graceful degradation), #45 (two-path doctrine for coordinator), #46 (researcher breadth mode), #47 (researcher contrarian sweep). Updated #36 with lever 5 urgency elevation. Test log: 2026-03-19-retirement-research-specialists-vs-direct. |
| v4.0 | Mar 19, 2026 | Chris | Cross-topic validation of #37/#38 across Wasm and AI coding topics. #38 fully validated; #37 partially validated (over-hedging fixed, under-hedging inconsistent on tertiary-heavy sources). Added #39 (writer medium-claim self-check), #40 (writer-formatter tier-aware Stage 3.5), #41 (researcher auto-retry escalation from #35), #42 (recipe conditional branching bug). Updated #37/#38 status with validation results. Two test logs added. |
| v3.9 | Mar 19, 2026 | Chris | Added re-run test log for #37/#38 validation (2026-03-18-rto-rerun-writer-fixes-37-38). Updated #35 with 3/3 truncation data points — auto-retry promotion recommended. |
| v3.8 | Mar 18, 2026 | Chris | Added #37 (Writer hedging-to-source-tier mapping) and #38 (Writer decision-support template for exec audiences) from A/B pipeline comparison test. Updated #36 with lever 5 (skip-formatters mode for human-terminal workflows). All items from test log 2026-03-18-specialists-vs-direct-rto-research. |
| v3.7 | Mar 10, 2026 | Chris | Shipped #34 (da-formatter specialist) — moved to Recently Completed. Built `specialists/data-analyzer-formatter/index.md`; registered in `behaviors/specialists.yaml`; Rule 8 added to `context/specialists-instructions.md`; `format-analysis` step added to `recipes/research-chain.yaml` v1.6.0. Spot test PASS. Scorecard: Format Fidelity 10/10, Chain Reliability 9/10, Research Trustworthiness 4/10. |
| v3.6 | Mar 10, 2026 | Chris | Conditionally closed #16 (DA Format B hardening) and closed #17 (DA code-fence prevention). Added #34 (da-formatter specialist — new finding from DA test: produces prose narrative for ambiguous inputs, same root cause as #29/#30). DA spec changes committed. Test log in docs/test-log/data-analyzer/. |
| v3.5 | Mar 10, 2026 | Chris | Closed #29 (Writer informal register), #30 (Storyteller OUTPUT CONTRACT), #18 (Storyteller inference auditability), #19 (quality_threshold param) — all via formatter architectural fix or spec verification. Both formatters (story-formatter, writer-formatter) confirmed handling their respective failure modes in clean test runs. #18 verified: inferences surface in NARRATIVE SELECTION with `(inference)` label. Test logs in docs/test-log/story-formatter/ and docs/test-log/writer-formatter/. |
| v3.4 | Mar 10, 2026 | Chris | Shipped #33 (prioritizer-formatter specialist) — moved to Recently Completed. Built `specialists/prioritizer-formatter/index.md`; registered in `behaviors/specialists.yaml`; added Rule 7 + description + chain to `specialists-instructions.md`. Test: prose-format input → canonical PRIORITY OUTPUT block, PASS. |
| v3.3 | Mar 9, 2026 | Chris | Added #33 (prioritizer-formatter specialist) to near-term Priority 2 — architectural fix for Prioritizer output block, same pattern as researcher/story/writer-formatter. Updated #31 with spec-fix failure note (`01e137a` did not hold). Closed #32 — routing validation passed clean (test log 2026-03-09-routing-validation). |
| v3.2 | Mar 9, 2026 | Chris | Marked Epic 10 (Prioritizer) complete — added to recently completed. Added #31 (Prioritizer structured output block) and #32 (coordinator routing hook for priority lists) to near-term Priority 2 from test log 2026-03-09-prioritizer-spot-test. Routing heuristic in specialists-instructions.md updated with Prioritizer trigger row. |
| v3.1 | Mar 6, 2026 | Chris | Added #30 (Storyteller OUTPUT CONTRACT compliance) to near-term after failed format validation run. #18 and #19 unverified pending this fix. |
| v3.0 | Mar 6, 2026 | Chris | Shipped #28, #7, #9 as single Writer quality commit. Moved to Recently Completed. Added #29 (OUTPUT CONTRACT compliance for informal registers) to near-term. Storyteller: shipped #18 (inference auditability in NARRATIVE SELECTION) and #19 (quality_threshold param). |
| v2.9 | Mar 6, 2026 | Chris | Shipped #22 as architectural reframe — researcher stripped to evidence-only, formatter promoted to essential pipeline stage with validation rules. Moved to Recently Completed. |
| v2.8 | Mar 6, 2026 | Chris | Promoted #22 from near-term to Immediate Next after validation test (3/3 researcher runs produced non-canonical output). Shipped format enforcement fix: 5-point FINAL SELF-CHECK, explicit wrong/right examples for FINDINGS blocks, numeric confidence ban, tier label ban. Struck through #22 in near-term. |
| v2.7 | Mar 6, 2026 | Chris | Marked #27 as shipped — moved to Recently Completed. Sprint complete: Immediate Next is now empty. |
| v2.6 | Mar 6, 2026 | Chris | Marked #5 and #6 as shipped — moved to Recently Completed. #27 is now the sole Immediate Next item. |
| v2.5 | Mar 6, 2026 | Chris | **Prioritization pass.** Consolidated 5 duplicates: #12/#20/#21 merged into #5 (researcher trustworthiness overhaul, bumped to M effort / H impact); #23 merged into #16; #24 merged into #17. Restructured near-term into 4 priority tiers. Moved #5, #6, #27 to Immediate Next. Filled TBD effort/impact ratings. Added Consolidation Log. Separated shipped items (#10, #26) into Shipped/Closed table. Net: 28 items → 20 unique items (5 absorbed, 2 shipped, 1 partially shipped). |
| v2.4 | Mar 6, 2026 | Chris | Routed 3 action items from sports-betting-specialists chain test log (2026-03-06): reinforced #5 with 142/142 unrated confidence evidence; added #27 (coordinator Rule 5 formatter enforcement); added #28 (writer CLAIMS TO VERIFY surfacing in user-facing output). Narration BEFORE-line tracking noted in test log but not promoted (best-effort, low priority). |
| v2.3 | Mar 6, 2026 | Chris | Session-close doc sweep: closed #10 (shipped instructions-level in PR #16, hook deferred), closed #26 (shipped routing heuristic + "when in doubt, chain" in PR #16), added PRs #14/#15/#16 to Recently Completed, annotated #13 with smoke test finding |
| v2.2 | Mar 5, 2026 | Chris | Routed 3 action items from chain-reliability smoke test: updated #10 with hook stub finding + smoke test results; updated #13 with Parsed: line inconsistency; added #26 (ambiguity boundary for casual prompts) |
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
