# Product Backlog

**Purpose:** Strategic planning view for canvas-specialists — a library of best-in-class, single-domain AI specialist agents for knowledge worker and consumer scenarios  
**Owner:** Chris Park  
**Last Updated:** March 26, 2026 (v5.9)  

---

## Strategic Roadmap

See [**2026-03-05-world-class-roadmap.md**](plans/2026-03-05-world-class-roadmap.md) for the 4-phase strategic direction: Phase 1 NOW (solidify foundations), Phase 2 NEXT (expand specialists), Phase 3 LATER (ecosystem synthesis), Phase 4 CI/Polish (production readiness).

---

## Current Status Summary

**11 epics tracked:** ✅ 7 complete, 🔄 0 in progress, ⏸️ 0 paused, 4 planned

- ✅ Epic 01 — Researcher
- ✅ Epic 02 — Writer
- ✅ Epic 03 — Storyteller
- ✅ Epic 04 — Competitive Analysis
- 🆕 Epic 05 — Design
- 🆕 Epic 06 — Demo Generator
- 🆕 Epic 07 — Presentation Builder
- ✅ Epic 08 — Data Analyzer
- ✅ Epic 09 — Planner
- ✅ Epic 10 — Prioritizer
- 🆕 Epic 11 — Platform Integrations

### Active Work

*Next sprint: researcher source diversity via mechanical enforcement (validate-sources recipe step). See #59.*

### Recently Completed

| Item | Epic | Owner | Completed | Notes |
|------|------|-------|-----------|-------|
| DA-formatter specialist (#34) | 08 | Chris | Mar 10, 2026 | `specialists/data-analyzer-formatter/index.md` — fifth formatter, 2-input, 4-stage pipeline, Option A traces_to. Rule 8 in coordinator. `format-analysis` step in research-chain v1.6.0. Spot test PASS. *(test log 2026-03-10-da-formatter-spot-test)* |
| Writer: tier-aware hedging (#37) | 02 | Chris | Mar 18, 2026 | Shipped in commit `86197c6`. Over-hedging of strong evidence eliminated across all 3 test topics. **Partially validated 2026-03-19:** under-hedging inconsistent on tertiary-heavy topics (Wasm 5/10 vs AI coding 8/10). Enhancement: #39 (medium-claim self-check). *(test logs: 2026-03-18-rto-rerun-writer-fixes-37-38, 2026-03-19-writer-fixes-37-38-cross-topic-validation)* |
| Writer: exec decision-support (#38) | 02 | Chris | Mar 18, 2026 | Shipped in commit `86197c6`. Scenario-based "If X → Expect Y" framing. **Fully validated 2026-03-19** across RTO, Wasm, AI coding topics. Decision-support 6→9/10 (+3.0). No further changes needed. *(test logs: 2026-03-18-rto-rerun-writer-fixes-37-38, 2026-03-19-writer-fixes-37-38-cross-topic-validation)* |
| Coordinator: two-path doctrine (#45) | 01/02 | Chris | Mar 19, 2026 | Batch 2. Rule 9 added to coordinator routing. Recipe path: all formatters run (Rules 5–8 unchanged), context variables handle dual inputs. Ad-hoc path: researcher-formatter and DA-formatter always run; writer-formatter and prioritizer-formatter skipped when output goes directly to user. Decision test: "Does the next consumer need canonical structured format?" Unblocks #44. Commit `7a07b66`. |
| Researcher: auto-retry on truncation (#41) | 01 | Chris | Mar 19, 2026 | Batch 2. Soft gate: validate-research outputs PASS/RETRY (no exit 1). New ensure-research retry step: PASS = passthrough (~30s overhead), RETRY = fresh research from scratch. Hard gate: validate-research-final catches double failure. Pipeline auto-recovers from truncation. research-chain v1.12.0. Commit `7a07b66`. **Not yet validated in a live pipeline run.** |
| Context refactor (infrastructure) | — | Chris | Mar 19, 2026 | Split `specialists-instructions.md` (4,924 tokens) into `coordinator-routing.md` (~2,750 tokens). Removed `context.include` from `behaviors/specialists.yaml` — eliminates ~59K tokens/pipeline (no more injecting coordinator routing into 12 specialist spawns). Pinned 3 external deps to HEAD SHAs. Added `model_role: reasoning` to data-analyzer. Updated `adding-a-specialist.md` guide. 5 commits: `946a329`–`0bbd839`. |
| Writer-formatter: graceful degradation (#44) | 02 | Chris | Mar 20, 2026 | Shipped Stage 0.5 source corpus detection + Degraded Mode pass-through. When source corpus (RESEARCH OUTPUT / ANALYSIS OUTPUT) is absent (ad-hoc mode), formatter passes through writer prose unchanged with citation-unavailable notice instead of halting. Rule 9 (#45) also re-added to `coordinator-routing.md` after being lost in context refactor. Commits `6e4ed99`, `00d2ea8`, `46fd324`. **Not yet validated in live ad-hoc session.** |
| Quality improvement loop recipe (infrastructure) | — | Chris | Mar 20, 2026 | Autonomous `while_condition` loop: evaluate pipeline against 3 competitors × 5 topics → triangulate structural gaps → diagnose → fix → revert on regression → re-evaluate. Convergence detection (2 consecutive non-improving rounds). Per-round append-only observability log. Also: wired competitor model routing (`provider_preferences`), added 2 test topics (comparison, technical-analysis), fixed score-history.yaml bug. 39 structural tests. Commits `d329e1b`–`8dbd704`. |
| Coordinator: broaden analyzer trigger (#48) | 01/02/08 | Chris | Mar 19, 2026 | Batch 1. Routing heuristic table + Rule 4 updated to include "strategy" alongside "analysis/insights/investigation" for triggering the deep chain (researcher → analyzer → writer). Strategy requests now route through fact/inference separation. Commit `0991689`. |
| Writer: medium-claim self-check (#39) | 02 | Chris | Mar 19, 2026 | Batch 1. Added Stage 5 item 8 — explicit scan of every medium-confidence sentence for tier-appropriate hedging before returning. Catches under-hedging when most sources share the same tier. Not exercised in validation (24/25 high-confidence sources). Commit `0991689`. |
| Writer: concrete examples over frameworks (#51) | 02 | Chris | Mar 19, 2026 | Batch 1. Added guidance between Stage 3 and Stage 4: when source claims contain case studies, anchor each strategy section to the strongest concrete example. **Validated:** hybrid productivity test anchored every key point to named companies with specific metrics (Trip.com, Gallup, Microsoft, Atlassian). PASS. Commit `0991689`. |
| Writer: cross-strategy synthesis (#52) | 02 | Chris | Mar 19, 2026 | Batch 1. Added guidance after Stage 3: when document has 3+ strategies, add synthesis paragraph showing causal links. **Partially validated:** Implications section connects strategies thematically but doesn't explicitly name causal links ("X enables Y"). Brief format (375 words) likely constrained this. Commit `0991689`. |
| Researcher: iterative deepening (#49) | 01 | Chris | Mar 22, 2026 | Depth check added to Quality Gate (Stage 6). Detects thin sub-questions (< 3 sources OR no primary/academic) and runs targeted deepening passes (academic, official, practitioner). 7 structural tests. Commit `3891989`. |
| Researcher: breadth mode (#46) | 01 | Chris | Mar 22, 2026 | Step D (mode selection) added to Stage 1 — auto-selects `research_mode: breadth` for Survey/Ranking questions with depth override. Stage 5 breadth corroboration: numeric/financial claims fully corroborated, qualitative claims accepted at medium confidence from single source. 8 structural tests. Commits `320aae0`, `205af27`. |
| Writer-formatter: tier-aware hedging (#40) | 02 | Chris | Mar 22, 2026 | Stage 3.5 upgraded with source-tier check before inserting hedges. Primary/secondary claims protected from "reportedly." Tertiary claims hedged as before. Inference unchanged. 5 structural tests. Commit `50be666`. |
| Writer: audience-aware technical depth (#50) | 02 | Chris | Mar 22, 2026 | Audience depth self-check added to Stage 4. Non-technical audiences get mechanism-to-outcome translation. Technical audiences excluded. Self-check: "Would this sentence make sense to someone who doesn't build AI systems?" 5 structural tests. Commit `6ebd7ee`. |
| Writer: confidence labels + coverage-audit pipeline step + quality loop v3 (infrastructure) | 01/02 | Chris | Mar 24, 2026 | `agents/writer.md` +26 lines: confidence label display. `recipes/research-chain.yaml` +64 lines: `coverage-audit` as explicit pipeline step. `recipes/quality-loop.yaml` +31 lines: cross-agent awareness. Quality loop score: **8.17** → targeting **8.5**. Commit `9d33e15`. |
| specialists→agents directory refactor (infrastructure) | — | Chris | Mar 24, 2026 | Renamed `specialists/{name}/index.md` → `agents/{name}.md` across entire codebase. Updated all path references in live recipes, skills, docs, tests. Removed prototype HTML story docs (~3,177 lines), `slide-review.yaml` dev recipe, orphaned test scripts. Added architecture diagrams. 563 tests passing. Commits `ec7a226`–`655a917`. |
| coordinator-routing: move to context.include (infrastructure) | — | Chris | Mar 24, 2026 | Root cause: markdown body entries get REPLACED during bundle composition; `context.include` entries ACCUMULATE. `coordinator-routing.md` was in the body → silently overwritten when composed after another app bundle. Fix: moved to `context.include` in `behaviors/specialists.yaml`. Commit `1ae9e67`. |
| Storyteller: compound tones + Researcher contrarian sweep (#47) | 03/01 | Chris | Mar 23, 2026 | Compound tone support shipped (Epic 03 complete). Researcher contrarian sweep added to Quality Gate. Validated in Mar 24 weight-loss A/B test: surfaced regain rate, adherence gaps, depression moderator, Volumetrics restriction, IF threshold. Commit `7cdef76`. *(test log 2026-03-24-weight-loss-recipes-specialists-vs-direct)* |
| Recipe: fix conditional branching bug (#42) | 01 | Chris | Mar 19, 2026 | Removed smart-skip gates for DA-formatter and writer-formatter in research-chain. Root cause: bash heredoc output with trailing whitespace didn't match condition strings. Reverted to always running formatters — ~6 min slower but 100% reliable. research-chain v1.11.0. Commit `9c855b2`. |
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

Items ordered by impact. Ship these first — they fix the most-flagged quality gaps from the Mar 18–19 testing sprint.

| # | Item | Epic | Owner | Effort | Impact | Why Now |
|---|------|------|-------|--------|--------|---------|
| 59 | **Researcher: mechanical source diversity enforcement (validate-sources recipe step)** | 01 | Chris | M | H | **Source quality (5-6/10) is the binding constraint on pipeline score.** Adding instructions to researcher.md doesn't work — LLM compliance degrades with prompt complexity (tested and reverted Mar 26). Fix must be mechanical: a `validate-sources` recipe step (like `validate-research`) that runs AFTER the researcher, counts distinct domains and source categories, and returns PASS/RETRY with specific search directives for under-represented categories. Design questions: (1) what does validation count and what thresholds? (2) what specific search directives on RETRY? (`"[topic] site:hbr.org"`, `"[topic] site:reuters.com"`, etc.) (3) how many retry cycles? (4) does retry append or replace? Follows the proven `validate-research` → `ensure-research` pattern from #41. |
| ~~48~~ | ~~**Coordinator routing: broaden analyzer trigger for strategy requests**~~ | 01/02/08 | Chris | XS | H | **Shipped 2026-03-19 (Batch 1).** Routing heuristic + Rule 4 updated. Commit `0991689`. |
| ~~45~~ | ~~**Coordinator: two-path doctrine for ad-hoc vs recipe execution**~~ | 01/02 | Chris | S | H | **Shipped 2026-03-19 (Batch 2).** Rule 9 added to coordinator. Recipe path: formatters always run. Ad-hoc path: researcher-formatter and DA-formatter always; writer-formatter and prioritizer-formatter skipped when output goes directly to user. Unblocks #44. Commit `7a07b66`. |
| ~~41~~ | ~~**Researcher: auto-retry on truncation (#35 escalation)**~~ | 01 | Chris | S | H | **Shipped 2026-03-19 (Batch 2).** Soft gate (validate-research → PASS/RETRY) + ensure-research retry step + hard gate (validate-research-final). Pipeline auto-recovers from truncation. research-chain v1.12.0. Commit `7a07b66`. |
| 0 | ~~**Specialist output format compliance — architectural fix**~~ | 01/02 | Chris | — | — | **Partially shipped 2026-03-03.** Researcher-formatter specialist built — two-step approach normalizes any Researcher output to canonical RESEARCH OUTPUT block before DA/Writer. Writer structural blocks remain aspirational — revisit when Amplifier provider supports structured output. |



### Near-term (Next 1-2 Sprints)

Ordered by priority tier then impact. Items marked *(consolidated)* absorbed duplicates — see Consolidation Log below.

**Priority 2 — Quality polish, moderate impact:**

**All 5 quality sprint items shipped 2026-03-25.** #55 → #56 → #57 shipped in commit `07f99c3`. #3 and #58 shipped in same session. Running quality eval to validate the estimated +0.35 to +0.56 lift (gap was 0.33).

| # | Item | Epic | Owner | Effort | Impact | Rationale |
|---|------|------|-------|--------|--------|-----------|
| ~~55~~ | ~~**Writer: per-section structured confidence labels + consolidated confidence table**~~ | 02 | Chris | S | H | **Shipped 2026-03-25.** Inline `[Confidence: HIGH/MEDIUM/LOW — basis]` labels per section + Stage 5 item 11 enforcement. Commit `07f99c3`. |
| ~~56~~ | ~~**Writer: make coverage-manifest MUST-INCLUDE items mandatory**~~ | 02 | Chris | XS | H | **Shipped 2026-03-25.** Stage 2 step 5 coverage manifest check + Stage 5 item 12 enforcement. Commit `07f99c3`. |
| ~~57~~ | ~~**Coverage-audit: raise manifest cap from 8 → 15 items**~~ | 02 | Chris | XS | M | **Shipped 2026-03-25.** Cap raised from 8 to 15 in research-chain.yaml. Commit `07f99c3`. |
| ~~3~~ | ~~**Coverage audit severity levels (`gap_policy` input)**~~ | 02 | Chris | S | M | **Shipped 2026-03-25.** MUST-INCLUDE findings now classified as CRITICAL/HIGH/MEDIUM severity. New `gap_policy` context variable (strict/balanced/relaxed) controls which severities are mandatory. Writer Stage 2 and Stage 5 honor gap_policy. Default: strict (all mandatory). |
| ~~58~~ | ~~**Quality loop: fix score-extraction regex in check step**~~ | — | Chris | S | M | **Shipped 2026-03-25.** Root cause: LLM diagnosis text unreliably outputs `score_before:` field. Fix: (1) aggregate-diagnose now computes and emits `AGGREGATE_PIPELINE_SCORE: X.XX` on its own line, (2) check step tries AGGREGATE_PIPELINE_SCORE first → score_before fallback → current_score fallback, (3) zero-value scores rejected. |
| ~~29~~ | ~~Writer: OUTPUT CONTRACT compliance for informal registers~~ | 02 | Chris | S | M | **Closed 2026-03-10 via formatter architectural fix.** Writer-formatter handles the informal register failure mode: produces `Parsed:`, `WRITER METADATA`, `CITATIONS`, `CLAIMS TO VERIFY` regardless of Writer output format. Two instruction-based fixes (`0508f95`, OUTPUT CONTRACT block) did not hold; formatter is the reliable architectural catch. Validated: `audience=myself` Writer output → writer-formatter → all structural blocks present, clean pass. *(test log 2026-03-10-writer-informal-register-verification)* |
| ~~30~~ | ~~Storyteller: OUTPUT CONTRACT compliance (STORY OUTPUT header + NARRATIVE SELECTION block)~~ | 03 | Chris | S | H | **Closed 2026-03-10 via formatter architectural fix.** Story-formatter handles the document failure mode: produces `STORY OUTPUT` header, all metadata, `NARRATIVE SELECTION` block regardless of Storyteller output format. Storyteller produced a full markdown document with `##` headers and no STORY OUTPUT structure; story-formatter normalized to canonical block, all 9 findings/inferences classified. Clean pass. *(test log 2026-03-10-storyteller-format-compliance-verification)* |
| ~~31~~ | ~~Prioritizer: add structured output block (`PRIORITY OUTPUT` header)~~ | 10 | Chris | S | M | **Resolved by #33 (prioritizer-formatter)** — Shipped 2026-03-10. Architectural fix applied: prioritizer-formatter specialist handles both block format (pass-through) and prose format (extracts rankings, infers priority labels). Handles the prose failure mode that spec-based fixes could not resolve. *(See Recently Completed entry for #33)* |
| ~~32~~ | ~~Coordinator routing: add Prioritizer trigger for priority list requests~~ | 10 | Chris | XS | M | **VALIDATED 2026-03-09.** Routing fix in `4d56283` confirmed working — coordinator routed automatically on message 1 with no prompting. Input order overridden (dark mode listed first, ranked last). Full chain completed cleanly. *(validated in test log 2026-03-09-routing-validation)* |
| ~~33~~ | ~~Prioritizer-formatter specialist~~ | 10 | Chris | S | H | **Shipped 2026-03-10.** See Recently Completed. |
| ~~22~~ | ~~Stabilize Researcher canonical output header/anchor (Stage 0 / "RESEARCH OUTPUT")~~ | 01 | Chris | — | — | **Promoted to Immediate Next and shipped 2026-03-06.** See Immediate Next #22 entry. |
| ~~37~~ | ~~Writer: hedging-to-source-tier mapping~~ | 02 | Chris | S | H | **Shipped 2026-03-18; partially validated 2026-03-19.** Moved to Recently Completed. Enhancement: #39 (medium-claim self-check). |
| ~~38~~ | ~~Writer: decision-support template for executive audiences~~ | 02 | Chris | S | M | **Shipped 2026-03-18; fully validated 2026-03-19.** Moved to Recently Completed. No further changes needed. |
| ~~39~~ | ~~Writer: add medium-claim self-check to Stage 5~~ | 02 | Chris | XS | M | **Shipped 2026-03-19 (Batch 1).** Stage 5 item 8 added. Commit `0991689`. |
| ~~40~~ | ~~Writer-formatter: upgrade Stage 3.5 to tier-aware hedging~~ | 02 | Chris | S | M | **Shipped 2026-03-22.** Stage 3.5 source-tier check. Commit `50be666`. |
| ~~48~~ | ~~Coordinator routing: broaden analyzer trigger for strategy requests~~ | 01/02/08 | Chris | XS | H | **Promoted to Immediate Next.** |
| ~~49~~ | ~~Researcher: iterative deepening for thin sub-questions~~ | 01 | Chris | S | H | **Shipped 2026-03-22.** Depth check in Quality Gate. Commit `3891989`. |
| ~~50~~ | ~~Writer: audience-aware technical depth calibration~~ | 02 | Chris | S | M | **Shipped 2026-03-22.** Stage 4 audience depth self-check. Commit `6ebd7ee`. |
| ~~51~~ | ~~Writer: prioritize concrete examples over frameworks in briefs~~ | 02 | Chris | XS | M | **Shipped 2026-03-19 (Batch 1).** Stage 3 guidance added. Validated: hybrid test anchored every key point to named examples. Commit `0991689`. |
| ~~52~~ | ~~Writer: cross-strategy synthesis for multi-point briefs~~ | 02 | Chris | XS | M | **Shipped 2026-03-19 (Batch 1).** Stage 3 guidance added. Partially validated: synthesis present but causal links not explicit in brief format. Commit `0991689`. |
| ~~41~~ | ~~Researcher: auto-retry on truncation (#35 escalation)~~ | 01 | Chris | S | H | **Shipped 2026-03-19 (Batch 2).** Commit `7a07b66`. |
| ~~42~~ | ~~Recipe engine: investigate conditional branching failure in research-chain v1.10.0~~ | 01 | Chris | S | M | **Shipped 2026-03-19.** Root cause: bash heredoc trailing whitespace. Fix: removed smart-skip gates, always run formatters. research-chain v1.11.0. Commit `9c855b2`. |
| ~~43~~ | ~~Writer: add `decision-brief` format with 1,500–3,000 word budget~~ | 02 | Chris | S | M | **Resolved by v1 loop changes (2026-03-21).** Brief word budget increased from 250-400 to 800-1,200 words (`c305f26`). Auto-escalation to Report format (1,200-1,800 words) when 20+ findings across 5+ entities. Finding coverage floor: 60% of findings referenced for 15+ finding inputs. The original pain point (brief too short for survey topics) is addressed. |
| ~~44~~ | ~~Writer-formatter: graceful degradation when source material unavailable~~ | 02 | Chris | S | M | **Shipped 2026-03-20.** Stage 0.5 detection + Degraded Mode pass-through. Commits `00d2ea8`, `46fd324`. |
| ~~45~~ | ~~Coordinator: two-path doctrine for ad-hoc vs recipe execution~~ | 01/02 | Chris | S | H | **Shipped 2026-03-19 (Batch 2).** Commit `7a07b66`. |
| ~~46~~ | ~~Researcher: add `research_mode: breadth` for survey-type questions~~ | 01 | Chris | M | H | **Shipped 2026-03-22.** Step D mode selection + breadth corroboration. Commits `320aae0`, `205af27`. |

**Priority 3 — Important but not urgent:**

| # | Item | Epic | Owner | Effort | Impact | Rationale |
|---|------|------|-------|--------|--------|-----------|
| ~~3~~ | ~~Coverage audit severity levels~~ | 02 | Chris | S | M | **Promoted to P2** for the 8.5 quality push. See P2 ship order. |
| ~~47~~ | ~~Researcher: add contrarian sweep step for risk/downside coverage~~ | 01 | Chris | S | M | **Shipped in commit `7cdef76` (Mar 23, 2026).** Contrarian sweep added to researcher Quality Gate. Validated in Mar 24 weight-loss A/B test: dedicated contrarian sweep surfaced 50% regain rate, adherence gaps in RCTs, depression as moderator, Volumetrics fat restriction, IF clinical significance threshold. *(test log 2026-03-24-weight-loss-recipes-specialists-vs-direct)* |
| 53 | Writer: skip claim index and confidence tables for human-terminal ad-hoc flows | 02 | Chris | S | M | Reduce overhead for end-user consumption. In ad-hoc coordinator mode, the claim index (S1–S26), confidence assessment table, and CITATIONS block add ~200 words that a human reader won't use. Consider skipping when the next consumer is a human, not a downstream agent. *(test log 2026-03-24-weight-loss-recipes-specialists-vs-direct)* |
| 54 | Researcher: include practitioner-sourced content for practical/advisory questions | 01 | Chris | S | M | When the question is practical/advisory (recipes, how-to, step-by-step) rather than analytical, include practitioner-sourced content (recipe blogs, how-to guides) even without peer-reviewed corroboration. The corroboration requirement causes the researcher to skip useful practitioner content — the direct approach found Real Food Dietitians per-serving macros that the specialist missed. *(test log 2026-03-24-weight-loss-recipes-specialists-vs-direct)* |
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

**Epic 09 — Planner Specialist:** ✅ *Shipped 2026-03-13. Planner V1 built (75 lines, lightweight-first). Remaining: quality_threshold:high validation, pipeline integration testing.*

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
| 01 — Researcher | Researcher V1, source tiering, quality gate, ResearchOutput v1.0, researcher-formatter, research-chain recipe, coverage-audit pipeline step | Source confidence threshold | 97% |
| 02 — Writer | Writer V1, coverage audit, citations + attribution, WRITER METADATA, citation confidence, rendering (pandoc), confidence label display | Brand voice config, audit severity, source confidence threshold | 83% |
| 03 — Storyteller | StoryOutput schema, 5-stage pipeline, NARRATIVE SELECTION, narrative-chain recipe, compound tones | — | 100% |
| 04 — Competitive Analysis | 6-stage pipeline, head-to-head + landscape modes, CompetitiveAnalysisOutput schema, 2-step + 3-step recipes, researcher-first default, CLAIMS TO VERIFY block | — | 100% |
| 05 — Design | — | Full specialist implementation | 0% |
| 06 — Demo Generator | — | Full specialist implementation | 0% |
| 07 — Presentation Builder | — | Full specialist implementation | 0% |
| 08 — Data Analyzer | 4-stage pipeline, AnalysisOutput schema, Writer analysis-output integration, 6 E2E tests | Format B detection hardening, code-fence prevention | 100% |
| 09 — Planner | Planner V1 — structured plans with milestones, dependencies, timelines, risk flags (75 lines, lightweight-first) | quality_threshold:high validation, pipeline integration testing | ~75% |
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
| v5.9 | Mar 26, 2026 | Chris | **Post-sprint analysis + eval infrastructure hardening.** Fixed citation quality regression root cause: quality-eval-iteration.yaml was bypassing research-chain.yaml (missing resolve-urls step crashed citation quality 8.2→4.0). Wired eval to use research-chain recipe (commit `5270bcd`). Added safety gate to quality-loop fix step preventing auto-fix regressions. Spot-checked strategy + competitive-comparison topics — citation quality and confidence calibration confirmed working; source quality (5-6/10) identified as binding constraint. Tested and reverted researcher instruction additions (LLM compliance degrades with prompt complexity). Added #59 (validate-sources recipe step) as P1 for next sprint — mechanical enforcement via PASS/RETRY pattern, not instruction-based. |
| v5.8 | Mar 25, 2026 | Chris | **8.5 quality sprint complete — all 5 items shipped.** #55 (writer per-section confidence labels, Stage 4 + Stage 5 item 11), #56 (writer make coverage-manifest mandatory, Stage 2 step 5 + Stage 5 item 12), #57 (coverage-audit cap 8→15) shipped in commit `07f99c3`. #3 (coverage audit severity levels — CRITICAL/HIGH/MEDIUM classification, `gap_policy` context variable strict/balanced/relaxed, writer honors gap_policy in Stage 2 and Stage 5) shipped same session. #58 (quality loop score-extraction fix — `AGGREGATE_PIPELINE_SCORE:` reliable extraction in aggregate-diagnose + check step 3-tier fallback) shipped same session. 553 tests passing. |
| v5.7 | Mar 25, 2026 | Chris | **8.5 quality sprint decomposition.** Added 4 new P2 items from quality-eval-report gap analysis: #55 (writer per-section confidence labels, S/H, confidence calibration gap −0.6), #56 (writer make coverage-manifest mandatory, XS/H, factual depth gap −1.0), #57 (coverage-audit raise manifest cap 8→12–15, XS/M), #58 (quality loop fix score-extraction regex, S/M). Promoted #3 (coverage audit severity levels) from P3 to P2 as follow-on to #56. Ship order: #55 → #56 → #57 → #3 → #58. Combined estimated lift: +0.35 to +0.56 (gap is 0.33). Updated Active Work with sprint goal and ship order. |
| v5.6 | Mar 25, 2026 | Chris | **Housekeeping.** Closed #47 (researcher contrarian sweep — shipped in `7cdef76`, validated in Mar 24 weight-loss A/B test). Promoted #53 (writer skip claim index for human-terminal flows) and #54 (researcher practitioner content for practical questions) to P3 from Mar 24 test log. Committed untracked test log. |
| v5.5 | Mar 24, 2026 | Chris | **Epic 03 complete + infrastructure hardening.** Storyteller compound tones shipped (commit `7cdef76`) — Epic 03 now ✅. Writer confidence labels + `coverage-audit` pipeline step in research-chain + cross-agent awareness in quality loop (commit `9d33e15`). Quality loop score **8.17 → targeting 8.5**. `specialists/` → `agents/` directory refactor across entire codebase — renamed paths, updated recipes/skills/docs/tests, removed prototype HTML (~3,177 lines) and dev recipes, added architecture diagrams, 563 tests passing (commits `ec7a226`–`655a917`). coordinator-routing moved from `bundle.md` body to `context.include` to survive bundle composition overwrite (commit `1ae9e67`). Epic counts: 7 complete, 0 in progress, 4 planned. |
| v5.4 | Mar 22, 2026 | Chris | **Five backlog items shipped in one session.** #49 (iterative deepening), #46 (breadth mode), #40 (tier-aware hedging), #50 (audience-aware depth) all implemented with structural tests. #43 (decision-brief format) resolved by v1 loop's brief word budget increase + auto-escalation. Bundle context fix applied (`active: specialists` in settings). Quality loop v2 running with retry logic. P2 ship order: all items shipped or resolved. 25+ structural tests added. |
| v5.3 | Mar 20, 2026 | Chris | #44 shipped (writer-formatter graceful degradation). Quality improvement loop recipe built (10 tasks, 39 tests). Rule 9 (#45) restored after being lost in context refactor. Competitor model routing wired. 2 test topics added. Score-history.yaml bug fixed. P2 ship order updated to 5 open items: #49 → #46 → #50 → #43 → #40. |
| v5.2 | Mar 19, 2026 | Chris | **Batch 2 shipped + context refactor.** Moved #45 (two-path doctrine, commit `7a07b66`) and #41 (researcher auto-retry, research-chain v1.12.0, commit `7a07b66`) to Recently Completed. #44 (writer-formatter graceful degradation) now unblocked by #45. Updated P2 recommended ship order to 6 open items: #49 → #46 → #50 → #44 → #43 → #40. Context refactor: split `specialists-instructions.md` into `coordinator-routing.md` (~2,750 tokens, saves ~2,200 tokens coordinator context), removed `context.include` from behavior YAML (~59K tokens/pipeline savings), pinned 3 external deps to HEAD SHAs, added `model_role: reasoning` to data-analyzer, updated `adding-a-specialist.md` guide. 5 commits: `946a329`–`0bbd839`. Neither Batch 2 nor context refactor validated with live pipeline run yet. |
| v5.1 | Mar 19, 2026 | Chris | **Batch 1 shipped.** Moved #48 (coordinator analyzer trigger), #39 (writer medium-claim self-check), #51 (writer concrete examples), #52 (writer cross-strategy synthesis) to Recently Completed. All shipped in commit `0991689`. Fixed #42 (recipe conditional branching bug) — removed smart-skip gates, research-chain v1.11.0, commit `9c855b2`. Validation test: hybrid team productivity research-chain run, 11 steps, 22,959 bytes. #51 PASS (concrete examples anchor every key point). #52 partial (synthesis present, causal links not explicit in brief format). #39 not exercised (24/25 high-confidence source base). #48 code-verified (needs ad-hoc session test). Updated recommended P2 ship order. |
| v5.0 | Mar 19, 2026 | Chris | **Project reset.** Moved #37 (tier-aware hedging, shipped Mar 18, partially validated) and #38 (exec decision-support, shipped Mar 18, fully validated) to Recently Completed. Promoted #48 (XS/H, coordinator analyzer trigger), #45 (S/H, two-path doctrine), #41 (S/H, researcher auto-retry) to Immediate Next based on test evidence. Fixed Epic 09 (Planner) status: 🆕→✅ in summary, 0%→~75% in completion table, Medium-term entry updated. Fixed epic counts: 6 complete, 1 in progress, 4 planned. Added recommended ship order for remaining 10 open P2 items. Updated SCORECARD.md v2.5: Chain Reliability 8→7 (ad-hoc break, conditional branching bug, truncation 4/5), Overall 8→7. |
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
