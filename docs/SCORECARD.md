# Canvas Specialists — Quality Scorecard

**Purpose:** Tracks validated quality scores across key dimensions. Scores are updated
when test evidence exists; not updated on spec changes alone.

**Dimension definitions and scoring rubric:** [`docs/01-vision/SUCCESS-METRICS.md` § Scoring Rubric](01-vision/SUCCESS-METRICS.md#scoring-rubric)

---

## Scoring Rules

1. **Definitions live in SUCCESS-METRICS.md, not here.** This file tracks scores and evidence. It does not define what scores mean. If a dimension definition needs to change, change it in SUCCESS-METRICS.md — that's a visible, auditable act in the vision folder.
2. **Scores move on validated test evidence only.** A spec change is not a score change. A passing test log is.
3. **One scorecard.** This file (`docs/SCORECARD.md`) is the single scorecard. No other file tracks scores. (Previously `docs/01-vision/SCORECARD.md` existed and diverged — it has been retired.)
4. **Overall = unweighted average** of the four dimensions, rounded to nearest integer.
5. **Re-score when rubric changes.** If SUCCESS-METRICS.md updates a dimension definition, re-evaluate current scores against the new definition in the same commit.

---

## Current Scores (as of 2026-03-19)

| Dimension | Score | Previous | Change | Last Updated |
|-----------|-------|----------|--------|--------------|
| **Research Trustworthiness** | 8/10 | 8/10 | — | 2026-03-19 |
| **Chain Reliability** | 7/10 | 8/10 | -1 ↓ | 2026-03-19 |
| **Format Fidelity** | 7/10 | 7/10 | — | 2026-03-19 |
| **Specialist Coverage** | 7/10 | 7/10 | — | 2026-03-19 |
| **Overall** | 7/10 | 8/10 | -1 ↓ | 2026-03-19 |

---

## Score History

| Date | Research Trust | Chain Reliability | Format Fidelity | Coverage | Overall | Session Notes |
|------|---------------|-------------------|-----------------|----------|---------|---------------|
| 2026-03-09 | 3/10 | 7/10 | 8/10 | 6/10 | 6/10 | Scorecard established. 13 commits shipped in parallel sprint. Prioritizer built. Routing validation #32 PASS. |
| 2026-03-10 | 3/10 | 8/10 | 9/10 | 6/10 | 7/10 | Format Fidelity: closed #33 (prioritizer-formatter), #29 (writer informal), #30 (Storyteller format), verified #18/#19. Chain Reliability: prioritizer chain complete, DA hardening. Research Trustworthiness: DA improvements but new #34 finding; no net change. |
| 2026-03-10 | 4/10 | 9/10 | 10/10 | 6/10 | 7/10 | Shipped #34 (da-formatter). *(Scores below were overclaimed — see reconciliation row.)* |
| 2026-03-10 | 4/10 | 7/10 | 7/10 | 6/10 | **6/10** | **Reconciliation.** Consolidated two diverged scorecards. Anchored dimension definitions to SUCCESS-METRICS.md § Scoring Rubric. Re-scored against reconciled rubric. Chain Reliability 9→7: full R→RF→DA→DAF→W chain not validated end-to-end; individual links proven but longest chain unproven. Format Fidelity 10→7: all 5 formatter pairs complete, but Writer word budgets not validated across all 6 formats, audience calibration not systematic, writer-formatter with analysis-output input (#14) untested, CLAIMS TO VERIFY surfacing inconsistent. Research Trustworthiness stays 4. Coverage stays 6. |
| 2026-03-10 | 4/10 | 8/10 | 7/10 | 6/10 | **6/10** | **Full chain validation.** Ran research-chain v1.6.0 end-to-end on "Poolside AI" topic (R→RF→DA→DAF→W→WF→save). All 8 steps completed, no manual intervention, file saved at 13,764 bytes. Chain Reliability 7→8: longest chain variant proven. Research Trustworthiness stays 4: inference traces_to degraded to `[narrative-mapped: uncertain]` (15/15), URLs absent from CITATIONS block, confidence upgrades in prose. Two new gaps identified: Writer needs source URLs in CITATIONS, Writer needs inference hedging. *(test log 2026-03-10-poolside-ai-full-chain-audit)* |
| 2026-03-10 | 5/10 | 8/10 | 7/10 | 6/10 | **7/10** | **URL recovery + hedging validated.** Shipped three architectural fixes: (1) writer-formatter Stage 3.5 confidence-hedge audit — 14/14 medium/inference claims hedged, PASS. (2) researcher-formatter Stage 1.5 URL recovery — pattern-based reconstruction from source names. (3) resolve-urls pipeline step — verified URL lookup via web_search before formatting. Research-chain v1.7.0 (9 steps). Validation: 15/15 sourceable claims have real https:// URLs (100%), zero "unattributed". Research Trustworthiness 4→5. Overall 6→7. *(test log 2026-03-10-url-recovery-validation)* |
| 2026-03-11 | **7/10** | 8/10 | 7/10 | 6/10 | **7/10** | **Diverse topic validation + traces_to fix.** Shipped research-chain v1.8.2 (11 steps): (1) strip-parsed-prefix bash step — strips `Parsed:` prefix so DA hits Format A → real F# traces. (2) strip-formatter-notes bash step v3 — citation-boundary approach strips all artifact variants. 6 diverse topics validated across 6 domains (history, humanities, arts, medicine, tech, physics). URL recovery 181/182 = 99.5%. F-number traces 52/53 = 98.1%. Hedging consistent across all topics. Research Trustworthiness 5→7. Overall stays 7 (now exactly 7.0 vs 6.5). *(test log 2026-03-11-research-trustworthiness-diverse-validation)* |
| 2026-03-13 | **8/10** | 8/10 | 7/10 | **7/10** | **8/10** | **Quality gate validation + truncation gate + planner + specialist trims.** (1) Quality gate NOT MET paths validated: storyteller sparse-input trigger fires correctly (2 findings → NOT MET), DA high-threshold-with-low-evidence fires correctly (all low/tertiary → NOT MET), storyteller evidence-collapse borderline passes correctly (2/6 omitted = 33%, below 50% threshold). 3/3 tests PASS. *(test log 2026-03-13-quality-threshold-not-met-validation)* (2) Researcher truncation gate: validate-research bash step added to research-chain v1.9.0 and narrative-chain v1.3.0 — checks minimum byte count + evidence markers, fails fast on truncated output. (3) Planner specialist built (Epic 09, 75 lines, lightweight-first). (4) Specialist trims: writer 424→206, storyteller 419→285, researcher 276→237, DA 309→296 — removed format enforcement now handled by formatters. (5) WriterOutput added to types.md v1.3. Research Trustworthiness 7→8: both listed blockers resolved (quality gates validated, truncation gate shipped). Coverage 6→7: Planner built (Epic 09). Overall 7→8 (7.5 rounded up). |
| 2026-03-19 | 8/10 | **7/10** | 7/10 | 7/10 | **7/10** | **Mar 18–19 testing sprint (5 runs, 14 backlog items).** Shipped #37 (tier-aware hedging) and #38 (exec decision-support). A/B tests: RTO specialists 7.5 vs direct 8.5; RTO re-run after fixes 8.5 (+1.0); cross-topic avg 7.8 (#38 fully validated, #37 partial — Wasm under-hedging 5/10); retirement A/B (specialists better doc, writer-formatter broke in ad-hoc mode); team collab 7.5 (9+ gap analysis). Chain Reliability 8→7: writer-formatter breaks in ad-hoc mode (#44, two-input contract unsatisfiable outside recipes), conditional branching bug in smart-skip gates (#42), researcher truncation 4/5 runs with no auto-retry (#41). Research Trustworthiness holds at 8: hedging improved, quality gates still valid. Overall 8→7. *(test logs: 2026-03-18-specialists-vs-direct-rto-research, 2026-03-18-rto-rerun-writer-fixes-37-38, 2026-03-19-writer-fixes-37-38-cross-topic-validation, 2026-03-19-retirement-research-specialists-vs-direct, 2026-03-19-ai-first-team-collaboration)* |

---

## What Moves Each Dimension

### Research Trustworthiness (currently 8/10)

**What moved it from 7 to 8 (Mar 13):**
- Quality gate NOT MET path validated: 3/3 tests PASS. *(2026-03-13-quality-threshold-not-met-validation)*
- Researcher truncation gate shipped: validate-research bash step in research-chain v1.9.0.

**What reinforced 8 (Mar 18–19):**
- #37 (tier-aware hedging) shipped: over-hedging of strong evidence eliminated across all 3 topics. Nature RCT no longer gets "reportedly."
- #38 (exec decision-support) shipped and fully validated: "If X → Expect Y" framing across RTO, Wasm, AI coding.
- RTO re-run scored 8.5/10 (+1.0 from 7.5 baseline) after #37/#38.

**What's keeping it at 8:**
- #37 only partially validated — under-hedging inconsistent on tertiary-heavy topics (Wasm: 5/10 hedging accuracy vs AI coding: 8/10). Root cause: writer self-check doesn't scan medium claims when most sources are at the same tier.
- Researcher truncation confirmed systemic: 4/5 runs produce conversational summary instead of canonical RESEARCH OUTPUT block. Gate catches it but no auto-retry (#41).
- Minor formatting inconsistencies: bracket notation and meta-observation convention not standardized.

**What would move it to 9:**
- #39 medium-claim self-check — **shipped** (commit `0991689`), not yet exercised (24/25 high-confidence sources in validation run). Needs a tertiary-heavy topic test.
- #41 auto-retry on truncation — **shipped** (research-chain v1.12.0, commit `7a07b66`). Needs pipeline run that hits truncation to validate.
- Standardize traces_to bracket notation and meta-observation convention

### Chain Reliability (currently 7/10)

**What moved it from 8 to 7 (Mar 18–19):**
- Writer-formatter breaks in ad-hoc mode (#44) — two-input contract (writer output + original ~15K token research output) is designed for recipe pipelines where context variables pass both inputs. In coordinator-driven ad-hoc mode, re-sending the research corpus defeats delegation's token-conservation purpose. Formatter halted requesting material the coordinator couldn't re-send. **Shipped 2026-03-20:** Stage 0.5 detection + Degraded Mode pass-through (commits `00d2ea8`, `46fd324`). *(2026-03-19-retirement-research-specialists-vs-direct)*
- Conditional branching bug in research-chain v1.10.0 (#42) — smart-skip gates failed (bash output doesn't match condition syntax, likely trailing whitespace). Both conditions failed, leaving `formatted_analysis` undefined. *(2026-03-19-writer-fixes-37-38-cross-topic-validation)*
- Researcher truncation confirmed systemic: 4/5 pipeline runs produce conversational summary instead of canonical RESEARCH OUTPUT block (#41). Gate catches it but no auto-retry — pipeline cannot self-serve. *(2026-03-18 and 2026-03-19 test runs)*

**What supports 7 (still working):**
- Full chain (recipe mode) still completes: 11-step research-chain v1.8.2+ validated across 6+ topics
- All 5 formatter pairs fire correctly in recipe pipelines
- Recipe timeouts fixed (#11)

**What would move it back to 8 (all four shipped, pending validation):**
- #45 two-path doctrine — **shipped** (commit `7a07b66`). Makes ad-hoc mode work — recipe path keeps formatters, ad-hoc path makes them optional. Needs live ad-hoc test to validate.
- #41 auto-retry on truncation — **shipped** (research-chain v1.12.0, commit `7a07b66`). Soft gate → retry step → hard gate. Needs pipeline run that hits truncation to validate.
- #42 conditional branching fix — **shipped** (research-chain v1.11.0, commit `9c855b2`). Removed smart-skip gates, always run formatters.
- #44 writer-formatter graceful degradation — **shipped** (commits `00d2ea8`, `46fd324`). Stage 0.5 detection + Degraded Mode pass-through with citation notice. Needs live ad-hoc session test to validate.

### Format Fidelity (currently 7/10)

**What supports 7:**
- All 5 specialist-formatter pairs complete and producing canonical output: researcher, writer, storyteller, prioritizer, data-analyzer
- DA stage narration prefix stripped architecturally by the formatter
- Structural blocks reliable across tested scenarios

**What's keeping it from 8+:**
- Writer word budgets not validated across all 6 formats (only brief at 316w confirmed)
- Audience calibration validated for `myself` register only, not systematically across all audiences
- Writer-formatter with analysis-output input type (#14) untested
- CLAIMS TO VERIFY surfacing inconsistent (present in some runs, absent in others)
- Story-formatter normalization notes (cosmetic)

**What would move it to 8–9:**
- Validate Writer word budgets across all 6 formats (report, brief, proposal, exec summary, email, memo)
- Test audience calibration across 3+ distinct audience registers
- Test writer-formatter with analysis-output input (#14)
- Confirm CLAIMS TO VERIFY surfaces consistently across input types

### Specialist Coverage (currently 7/10)

**What moved it from 6 to 7:**
- Planner specialist built (Epic 09) — 75 lines, lightweight-first pattern. Takes goals + context, produces structured plans with milestones, dependencies, timelines, risk flags. Tested successfully on Canvas 6-week product launch scenario. *(2026-03-13)*

**What supports 7:**
- 7 specialist domains shipped: Researcher, Writer, Competitive Analysis, Data Analyzer, Storyteller (90%), Prioritizer, Planner
- 5 formatter pairs complete
- Phase 1 roadmap mostly done

**What's keeping it from 8+:**
- Design specialist (Epic 05) not built
- Demo Generator (Epic 06), Presentation Builder (Epic 07) not built
- Storyteller at 90% (compound tones, structured NARRATIVE SELECTION remaining)

**What would move it:**
- Complete Storyteller to 100% → solidifies 7
- Build Design specialist (Epic 05) → 8/10
- Build Presentation Builder (Epic 07) → 8–9/10

---

## Validated Evidence Summary (2026-03-13)

| Item | Evidence | Dimension |
|------|----------|-----------|
| **Full chain end-to-end (Poolside AI)** | 8-step R→RF→DA→DAF→W→WF→save completed, no manual intervention, 13,764 bytes saved. PASS for chain completion. *(2026-03-10-poolside-ai-full-chain-audit)* | **Chain Reliability** |
| Full chain: inference traces | 15/15 inferences degraded to `[narrative-mapped: uncertain]`, zero F# refs in final doc. FAIL. | Research Trustworthiness |
| Full chain: source URLs | Zero URLs in CITATIONS block. Claims trace to S-numbers but not external sources. FAIL. | Research Trustworthiness |
| Full chain: confidence preservation | Labels preserved in CITATIONS metadata, but prose upgrades medium/inference to definitive statements. PARTIAL. | Research Trustworthiness |
| Full chain: structural completeness | Parsed line, S-numbered claims (45), CLAIMS TO VERIFY, WRITER METADATA, CITATIONS — all present. PASS. | Format Fidelity |
| Prioritizer-formatter (#33) | prose→PRIORITY OUTPUT: PASS *(2026-03-10-prioritizer-formatter-spot-test)* | Format Fidelity |
| Story-formatter handles Storyteller failure mode (#30) | document→STORY OUTPUT: PASS *(2026-03-10-storyteller-format-compliance-verification)* | Format Fidelity |
| Inferences in NARRATIVE SELECTION (#18) | I1–I3 with `(inference)` labels in INCLUDED FINDINGS: PASS | Format Fidelity |
| Writer-formatter handles informal register (#29) | audience=myself→canonical blocks: PASS *(2026-03-10-writer-informal-register-verification)* | Format Fidelity |
| DA Format B labeled extraction (#16 partial) | 9 findings from labeled narrative: PASS | Chain Reliability |
| DA code-fence prevention (#17) | ANALYSIS OUTPUT as bare text: PASS | Chain Reliability |
| da-formatter (#34) | narrative DA→canonical ANALYSIS OUTPUT: PASS *(2026-03-10-da-formatter-spot-test)* | Chain Reliability, Format Fidelity |
| **URL recovery (resolve-urls + Stage 1.5)** | 15/15 sourceable claims have real https:// URLs, zero "unattributed". PASS *(2026-03-10-url-recovery-validation)* | **Research Trustworthiness** |
| **Confidence hedging (Stage 3.5)** | 14/14 medium/inference claims hedged in prose, zero misses. PASS *(2026-03-10-research-trustworthiness-fixes)* | **Research Trustworthiness** |
| Full 9-step chain (v1.7.0) | R→resolve-urls→RF→DA→DAF→W→WF→save completed, 17,892 bytes saved. PASS | Chain Reliability |
| **Diverse topic validation (6 topics)** | 6 domains (history, humanities, arts, medicine, tech, physics). URL recovery 181/182 = 99.5%. F-number traces 52/53 = 98.1%. Hedging consistent. PASS *(2026-03-11-research-trustworthiness-diverse-validation)* | **Research Trustworthiness** |
| **Inference traces_to fix (strip-parsed-prefix)** | DA now receives RESEARCH OUTPUT on line 1 → Format A → real F# references. 52/53 inferences carry F-numbers, zero `narrative-mapped: uncertain`. PASS *(2026-03-11-research-trustworthiness-diverse-validation)* | **Research Trustworthiness** |
| **Formatter artifact stripping (v1.8.2)** | Citation-boundary approach: extract Parsed: through last S-entry. Eliminates all artifact variants without pattern enumeration. v1.8.2 runs (Printing Press, Higgs Boson) clean. PASS | **Format Fidelity** |
| Full 11-step chain (v1.8.2) | R→resolve-urls→RF→strip-prefix→DA→DAF→W→WF→strip-notes→slug→save. 6 successful end-to-end runs. PASS | Chain Reliability |
| **Quality gate NOT MET — storyteller sparse input** | 2 findings input → mechanical fail trigger fires immediately, pipeline halted at Stage 1, NOT MET with specific failing items. PASS *(2026-03-13-quality-threshold-not-met-validation)* | **Research Trustworthiness** |
| **Quality gate NOT MET — DA high threshold** | 3 low-confidence tertiary findings + quality_threshold: high → zero inferences drawn, all findings UNUSED, NOT MET with clear rationale. PASS *(2026-03-13-quality-threshold-not-met-validation)* | **Research Trustworthiness** |
| **Quality gate MET — storyteller evidence collapse borderline** | 6 findings, 2 omitted with insufficient-evidence (33%, below 50% threshold) → correctly passes, builds narrative around single high-confidence finding with hedged low-confidence supporting claims. PASS *(2026-03-13-quality-threshold-not-met-validation)* | **Research Trustworthiness** |
| **Researcher truncation gate** | validate-research bash step in research-chain v1.9.0 + narrative-chain v1.3.0. Checks min 500 bytes + 3 evidence markers. Fails fast with GATE_FAIL. Shipped, not yet validated in production run. | **Chain Reliability** |
| **Planner specialist (Epic 09)** | 75-line lightweight-first specialist. Tested on Canvas 6-week launch scenario — produced structured PLAN OUTPUT with 5 milestones, dependency map, 7 risks, 8 assumptions, 7 open questions. Hit schema on first try, no formatter needed. PASS | **Specialist Coverage** |
| **Writer #37 tier-aware hedging** | Over-hedging eliminated across 3 topics (RTO, Wasm, AI coding). Nature RCT no longer gets "reportedly." Under-hedging inconsistent on tertiary-heavy topics (Wasm 5/10, AI coding 8/10). PARTIAL. *(2026-03-18-rto-rerun, 2026-03-19-cross-topic)* | **Research Trustworthiness** |
| **Writer #38 exec decision-support** | "If X → Expect Y" scenario framing validated across all 3 topics. RTO re-run: decision-support 6→9/10 (+3.0). PASS. *(2026-03-18-rto-rerun, 2026-03-19-cross-topic)* | **Research Trustworthiness** |
| **RTO A/B: specialists vs direct** | Specialists 7.5/10, Direct 8.5/10. DA inference separation is clearest value-add ("adverse selection mechanism"). Hedging accumulates through chain. Direct found 3 additional evidence items. *(2026-03-18-specialists-vs-direct-rto-research)* | **Chain Reliability** |
| **RTO re-run after #37/#38** | 8.5/10 (+1.0). Hedging calibration 6→8.5, decision support 6→9. Researcher truncation recurred (3/3 runs). *(2026-03-18-rto-rerun-writer-fixes-37-38)* | **Research Trustworthiness, Chain Reliability** |
| **Cross-topic validation (Wasm + AI coding)** | Avg 7.8/10. #38 fully validated. #37 partial (Wasm 5/10 hedging, AI coding 8/10). Researcher truncation 4/5 runs. Conditional branching bug discovered (#42). *(2026-03-19-writer-fixes-37-38-cross-topic-validation)* | **Research Trustworthiness, Chain Reliability** |
| **Retirement A/B: specialists vs direct** | Specialists: better writing quality, unique insights (France Roth IRA, FATCA), per-claim source transparency. Direct: more breadth (15 vs 13 destinations), per-destination depth, faster/more reliable. Writer-formatter broke in ad-hoc mode — two-input contract unsatisfiable outside recipes. FAIL for ad-hoc chain completion. *(2026-03-19-retirement-research-specialists-vs-direct)* | **Chain Reliability** |
| **Team collaboration 9+ gap analysis** | 7.5/10. 5 specific gaps mapped to responsible specialists: coordinator didn't trigger analyzer (~0.5 pts), single research round (~0.4 pts), technical depth miscalibrated (~0.3 pts), case studies unused (~0.2 pts), strategies as list not system (~0.1 pts). *(2026-03-19-ai-first-team-collaboration)* | **Research Trustworthiness, Chain Reliability** |

---

## Change History

| Version | Date | Changes |
|---------|------|---------|
| v2.6 | 2026-03-19 | **Batch 2 shipped (no score change — pending validation).** Updated "What would move it back to 8" (Chain Reliability) and "What would move it to 9" (Research Trustworthiness) to note #45, #41, #39 all shipped but awaiting live pipeline validation. Scores remain 7/10 overall per Scoring Rule 2 (scores move on test evidence only). |
| v2.5 | 2026-03-19 | **Mar 18–19 testing sprint re-score.** Added 5 test runs to evidence table and score history. Chain Reliability 8→7: writer-formatter ad-hoc break (#44), conditional branching bug (#42), researcher truncation 4/5 (#41). Research Trustworthiness holds at 8: #37/#38 shipped, hedging improved but partially validated. Overall 8→7. Updated "What Moves Each Dimension" for Research Trustworthiness and Chain Reliability with Mar 18–19 evidence. |
| v2.4 | 2026-03-13 | **Quality gate validation + truncation gate + planner + specialist trims.** Quality gate NOT MET paths validated: 3/3 tests PASS (storyteller sparse-input, DA high-threshold, storyteller evidence-collapse borderline). Researcher truncation gate shipped (research-chain v1.9.0, narrative-chain v1.3.0). Planner specialist built (Epic 09, 75 lines, lightweight-first). Specialist trims: writer 424→206, storyteller 419→285, researcher 276→237, DA 309→296 — removed format enforcement now handled by formatters. WriterOutput added to types.md v1.3. Backlog hygiene: #31 closed, Epic 10 updated to 95%, 8 test logs promoted. Research Trustworthiness 7→8, Coverage 6→7, Overall 7→8. *(test log 2026-03-13-quality-threshold-not-met-validation)* |
| v2.3 | 2026-03-11 | **Diverse topic validation + traces_to fix.** Shipped research-chain v1.8.2 (11 steps) with three new fixes: strip-parsed-prefix (DA Format A → real F# traces), strip-formatter-notes v3 (citation-boundary approach strips all artifact variants), fallback guards (prevent empty output on format variation). 6 diverse topics validated across 6 domains. URL recovery 181/182 = 99.5%. F-number traces 52/53 = 98.1%. Hedging consistent. Formatter artifacts eliminated architecturally. Research Trustworthiness 5→7, Overall stays 7 (now exactly 7.0). *(test log 2026-03-11-research-trustworthiness-diverse-validation)* |
| v2.2 | 2026-03-10 | **URL recovery + hedging validated.** Shipped three architectural fixes: researcher-formatter Stage 1.5 (URL reconstruction), resolve-urls pipeline step (verified URL lookup), writer-formatter Stage 3.5 (confidence hedging). Research-chain v1.7.0 (9 steps). Validation: 15/15 sourceable claims with URLs (100%), 14/14 claims hedged, zero "unattributed". Research Trustworthiness 4→5, Overall 6→7. *(test log 2026-03-10-url-recovery-validation)* |
| v2.1 | 2026-03-10 | **Full chain validation.** Ran research-chain v1.6.0 end-to-end (Poolside AI topic). Chain Reliability 7→8: longest chain variant proven. Research Trustworthiness stays 4: inference traces, source URLs, and confidence hedging all fail to survive to final document. Four new action items logged. *(test log 2026-03-10-poolside-ai-full-chain-audit)* |
| v2.0 | 2026-03-10 | **Reconciliation.** Consolidated two diverged scorecards into one. Retired `docs/01-vision/SCORECARD.md`. Anchored all dimension definitions to `SUCCESS-METRICS.md` § Scoring Rubric (new section added there). Added Scoring Rules to prevent future drift. Re-scored against reconciled rubric: Chain Reliability 9→7 (full chain unproven), Format Fidelity 10→7 (word budgets, audience calibration, #14 untested). Overall 7→6. |
| v1.2 | 2026-03-10 | Shipped #34 (da-formatter). Format Fidelity 9→10, Chain Reliability 8→9, Research Trustworthiness 3→4. |
| v1.1 | 2026-03-10 | Closed #33, #29, #30, verified #18/#19. Format Fidelity 8→9, Chain Reliability 7→8. |
| v1.0 | 2026-03-09 | Scorecard established. Initial scores: 3/7/8/6 = 6/10. |
