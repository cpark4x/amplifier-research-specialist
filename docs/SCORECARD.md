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

## Current Scores (as of 2026-03-11)

| Dimension | Score | Previous | Change | Last Updated |
|-----------|-------|----------|--------|--------------|
| **Research Trustworthiness** | 7/10 | 5/10 | +2 ↑ | 2026-03-11 |
| **Chain Reliability** | 8/10 | 8/10 | — | 2026-03-10 |
| **Format Fidelity** | 7/10 | 7/10 | — | 2026-03-10 |
| **Specialist Coverage** | 6/10 | 6/10 | — | 2026-03-09 |
| **Overall** | 7/10 | 7/10 | — | 2026-03-11 |

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

---

## What Moves Each Dimension

### Research Trustworthiness (currently 7/10)

**What moved it from 5 to 7:**
- Inference `traces_to` fix: strip-parsed-prefix bash step (v1.8.0) strips `Parsed:` prefix so DA receives `RESEARCH OUTPUT` on line 1 → Format A → canonical ANALYSIS OUTPUT with real F# finding references. 52/53 inference claims now carry real F-numbers (98.1%), zero `narrative-mapped: uncertain`. *(2026-03-11-research-trustworthiness-diverse-validation)*
- Diverse topic validation: 6 topics across 6 domains (history, humanities, arts, medicine, tech, physics). URL recovery 181/182 = 99.5%. Hedging consistent across all topics. Formatter artifacts addressed architecturally via citation-boundary stripping (v1.8.2).
- Recipe evolved v1.8.0 → v1.8.1 → v1.8.2 during validation, each iteration hardening the bash strip steps against edge cases found in real runs.

**What moved it from 4 to 5 (previous session):**
- Source URLs: 15/15 sourceable claims have real https:// URLs (100%), zero "unattributed" — via resolve-urls pipeline step + researcher-formatter Stage 1.5 *(2026-03-10-url-recovery-validation)*
- Confidence hedging: 14/14 medium/inference claims hedged in prose via writer-formatter Stage 3.5 *(2026-03-10-research-trustworthiness-fixes)*

**What's keeping it at 7:**
- Quality gate NOT MET path untested
- Researcher output truncation is stochastic (~50% of runs produce pipeline failure briefs instead of research) — reliability concern at the step level
- Minor formatting inconsistencies: bracket notation (`[F1, F2]` vs `F1, F2`) and meta-observation convention (`[meta]` vs `uncertain`) not standardized

**What would move it to 8:**
- Test quality gate NOT MET path (high threshold on thin-output topic)
- Reduce researcher truncation failure rate (content-presence gate after research step)
- Standardize traces_to bracket notation and meta-observation convention

### Chain Reliability (currently 8/10)

**What moved it from 7 to 8:**
- Full 8-step chain (R→RF→DA→DAF→W→WF→save) validated end-to-end on "Poolside AI" topic — all steps completed, no manual intervention, file saved at 13,764 bytes *(2026-03-10-poolside-ai-full-chain-audit)*
- All formatters fired as designed pipeline stages at every link
- Individual chain variants previously validated: R→RF→W (Jina AI, Mar 6), Storyteller (Acme Corp, Mar 10), Prioritizer (routing validation, Mar 9)
- Recipe timeouts fixed (#11, Mar 9)

**What's keeping it from 9+:**
- Story-formatter appends normalization notes outside the STORY OUTPUT block (minor)
- Narrative-chain and competitive-analysis-brief chains not validated end-to-end
- Researcher output truncation (~50% of runs) is a step-level reliability concern

**What would move it to 9:**
- Fix story-formatter normalization notes
- Validate narrative-chain (Storyteller variant) end-to-end
- Validate competitive-analysis-brief chains end-to-end
- Reduce researcher truncation failure rate (content-presence gate)

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

### Specialist Coverage (currently 6/10)

**What supports 6:**
- 6 specialist domains shipped: Researcher, Writer, Competitive Analysis, Data Analyzer, Storyteller (90%), Prioritizer
- 5 formatter pairs complete
- Phase 1 roadmap mostly done

**What's keeping it from 7+:**
- Planner specialist (Epic 09) not built
- Design specialist (Epic 05) not built
- Demo Generator (Epic 06), Presentation Builder (Epic 07) not built
- Storyteller at 90% (compound tones, structured NARRATIVE SELECTION remaining)

**What would move it:**
- Complete Storyteller to 100% → confirms 6, solidifies it
- Build Planner specialist (Epic 09) → 7/10
- Build Design specialist (Epic 05) → 7–8/10

---

## Validated Evidence Summary (2026-03-11)

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

---

## Change History

| Version | Date | Changes |
|---------|------|---------|
| v2.3 | 2026-03-11 | **Diverse topic validation + traces_to fix.** Shipped research-chain v1.8.2 (11 steps) with three new fixes: strip-parsed-prefix (DA Format A → real F# traces), strip-formatter-notes v3 (citation-boundary approach strips all artifact variants), fallback guards (prevent empty output on format variation). 6 diverse topics validated across 6 domains. URL recovery 181/182 = 99.5%. F-number traces 52/53 = 98.1%. Hedging consistent. Formatter artifacts eliminated architecturally. Research Trustworthiness 5→7, Overall stays 7 (now exactly 7.0). *(test log 2026-03-11-research-trustworthiness-diverse-validation)* |
| v2.2 | 2026-03-10 | **URL recovery + hedging validated.** Shipped three architectural fixes: researcher-formatter Stage 1.5 (URL reconstruction), resolve-urls pipeline step (verified URL lookup), writer-formatter Stage 3.5 (confidence hedging). Research-chain v1.7.0 (9 steps). Validation: 15/15 sourceable claims with URLs (100%), 14/14 claims hedged, zero "unattributed". Research Trustworthiness 4→5, Overall 6→7. *(test log 2026-03-10-url-recovery-validation)* |
| v2.1 | 2026-03-10 | **Full chain validation.** Ran research-chain v1.6.0 end-to-end (Poolside AI topic). Chain Reliability 7→8: longest chain variant proven. Research Trustworthiness stays 4: inference traces, source URLs, and confidence hedging all fail to survive to final document. Four new action items logged. *(test log 2026-03-10-poolside-ai-full-chain-audit)* |
| v2.0 | 2026-03-10 | **Reconciliation.** Consolidated two diverged scorecards into one. Retired `docs/01-vision/SCORECARD.md`. Anchored all dimension definitions to `SUCCESS-METRICS.md` § Scoring Rubric (new section added there). Added Scoring Rules to prevent future drift. Re-scored against reconciled rubric: Chain Reliability 9→7 (full chain unproven), Format Fidelity 10→7 (word budgets, audience calibration, #14 untested). Overall 7→6. |
| v1.2 | 2026-03-10 | Shipped #34 (da-formatter). Format Fidelity 9→10, Chain Reliability 8→9, Research Trustworthiness 3→4. |
| v1.1 | 2026-03-10 | Closed #33, #29, #30, verified #18/#19. Format Fidelity 8→9, Chain Reliability 7→8. |
| v1.0 | 2026-03-09 | Scorecard established. Initial scores: 3/7/8/6 = 6/10. |
