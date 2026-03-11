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

## Current Scores (as of 2026-03-10)

| Dimension | Score | Previous | Change | Last Updated |
|-----------|-------|----------|--------|--------------|
| **Research Trustworthiness** | 5/10 | 4/10 | +1 ↑ | 2026-03-10 |
| **Chain Reliability** | 8/10 | 8/10 | — | 2026-03-10 |
| **Format Fidelity** | 7/10 | 7/10 | — | 2026-03-10 |
| **Specialist Coverage** | 6/10 | 6/10 | — | 2026-03-09 |
| **Overall** | 7/10 | 6/10 | +1 ↑ | 2026-03-10 |

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

---

## What Moves Each Dimension

### Research Trustworthiness (currently 5/10)

**What moved it from 4 to 5:**
- Source URLs now present in CITATIONS: 15/15 sourceable claims have real https:// URLs (100%), zero "unattributed" — via two-layer architectural fix: resolve-urls pipeline step (verified URL lookup) + researcher-formatter Stage 1.5 (pattern-based reconstruction) *(2026-03-10-url-recovery-validation)*
- Confidence hedging validated: 14/14 medium/inference claims hedged in prose via writer-formatter Stage 3.5. `reportedly` for medium, `According to unconfirmed reports` for low, `Evidence suggests` for inference *(2026-03-10-research-trustworthiness-fixes)*

**What's keeping it at 5:**
- Inference `traces_to` fields are `[narrative-mapped: uncertain]` (12/12) — honest placeholder from DA-formatter when DA produces narrative prose, but no specific F# references survive to final document
- Validated on only 1 topic (Poolside AI) — rubric requires 5+ diverse topics for 6+
- Quality gate NOT MET path untested

**What would move it to 6:**
- Run across 4+ more diverse topics with consistent URL recovery and hedging results
- Investigate DA structured output to get specific F# traces (or accept `[narrative-mapped: uncertain]` as honest ceiling for narrative DA output)
- Test quality gate NOT MET path

### Chain Reliability (currently 8/10)

**What moved it from 7 to 8:**
- Full 8-step chain (R→RF→DA→DAF→W→WF→save) validated end-to-end on "Poolside AI" topic — all steps completed, no manual intervention, file saved at 13,764 bytes *(2026-03-10-poolside-ai-full-chain-audit)*
- All formatters fired as designed pipeline stages at every link
- Individual chain variants previously validated: R→RF→W (Jina AI, Mar 6), Storyteller (Acme Corp, Mar 10), Prioritizer (routing validation, Mar 9)
- Recipe timeouts fixed (#11, Mar 9)

**What's keeping it from 9+:**
- Story-formatter appends normalization notes outside the STORY OUTPUT block (minor)
- Only one full-chain end-to-end run validated (rubric 9–10 requires "every chain variant proven")

**What would move it to 9:**
- Fix story-formatter normalization notes
- Validate narrative-chain (Storyteller variant) end-to-end
- Validate competitive-analysis-brief chains end-to-end
- Run full research-chain on 2+ more diverse topics to confirm consistency

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

## Validated Evidence Summary (2026-03-10)

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

---

## Change History

| Version | Date | Changes |
|---------|------|---------|
| v2.2 | 2026-03-10 | **URL recovery + hedging validated.** Shipped three architectural fixes: researcher-formatter Stage 1.5 (URL reconstruction), resolve-urls pipeline step (verified URL lookup), writer-formatter Stage 3.5 (confidence hedging). Research-chain v1.7.0 (9 steps). Validation: 15/15 sourceable claims with URLs (100%), 14/14 claims hedged, zero "unattributed". Research Trustworthiness 4→5, Overall 6→7. *(test log 2026-03-10-url-recovery-validation)* |
| v2.1 | 2026-03-10 | **Full chain validation.** Ran research-chain v1.6.0 end-to-end (Poolside AI topic). Chain Reliability 7→8: longest chain variant proven. Research Trustworthiness stays 4: inference traces, source URLs, and confidence hedging all fail to survive to final document. Four new action items logged. *(test log 2026-03-10-poolside-ai-full-chain-audit)* |
| v2.0 | 2026-03-10 | **Reconciliation.** Consolidated two diverged scorecards into one. Retired `docs/01-vision/SCORECARD.md`. Anchored all dimension definitions to `SUCCESS-METRICS.md` § Scoring Rubric (new section added there). Added Scoring Rules to prevent future drift. Re-scored against reconciled rubric: Chain Reliability 9→7 (full chain unproven), Format Fidelity 10→7 (word budgets, audience calibration, #14 untested). Overall 7→6. |
| v1.2 | 2026-03-10 | Shipped #34 (da-formatter). Format Fidelity 9→10, Chain Reliability 8→9, Research Trustworthiness 3→4. |
| v1.1 | 2026-03-10 | Closed #33, #29, #30, verified #18/#19. Format Fidelity 8→9, Chain Reliability 7→8. |
| v1.0 | 2026-03-09 | Scorecard established. Initial scores: 3/7/8/6 = 6/10. |
