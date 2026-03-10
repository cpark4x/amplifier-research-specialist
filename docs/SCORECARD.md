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
| **Research Trustworthiness** | 4/10 | 4/10 | — | 2026-03-10 |
| **Chain Reliability** | 7/10 | 9/10 | -2 ↓ | 2026-03-10 |
| **Format Fidelity** | 7/10 | 10/10 | -3 ↓ | 2026-03-10 |
| **Specialist Coverage** | 6/10 | 6/10 | — | 2026-03-09 |
| **Overall** | 6/10 | 7/10 | -1 ↓ | 2026-03-10 |

---

## Score History

| Date | Research Trust | Chain Reliability | Format Fidelity | Coverage | Overall | Session Notes |
|------|---------------|-------------------|-----------------|----------|---------|---------------|
| 2026-03-09 | 3/10 | 7/10 | 8/10 | 6/10 | 6/10 | Scorecard established. 13 commits shipped in parallel sprint. Prioritizer built. Routing validation #32 PASS. |
| 2026-03-10 | 3/10 | 8/10 | 9/10 | 6/10 | 7/10 | Format Fidelity: closed #33 (prioritizer-formatter), #29 (writer informal), #30 (Storyteller format), verified #18/#19. Chain Reliability: prioritizer chain complete, DA hardening. Research Trustworthiness: DA improvements but new #34 finding; no net change. |
| 2026-03-10 | 4/10 | 9/10 | 10/10 | 6/10 | 7/10 | Shipped #34 (da-formatter). *(Scores below were overclaimed — see reconciliation row.)* |
| 2026-03-10 | 4/10 | 7/10 | 7/10 | 6/10 | **6/10** | **Reconciliation.** Consolidated two diverged scorecards. Anchored dimension definitions to SUCCESS-METRICS.md § Scoring Rubric. Re-scored against reconciled rubric. Chain Reliability 9→7: full R→RF→DA→DAF→W chain not validated end-to-end; individual links proven but longest chain unproven. Format Fidelity 10→7: all 5 formatter pairs complete, but Writer word budgets not validated across all 6 formats, audience calibration not systematic, writer-formatter with analysis-output input (#14) untested, CLAIMS TO VERIFY surfacing inconsistent. Research Trustworthiness stays 4. Coverage stays 6. |

---

## What Moves Each Dimension

### Research Trustworthiness (currently 4/10)

**What moved it from 3 to 4:**
- da-formatter (#34) built and spot-tested — closes the architectural gap for DA format failures
- `traces_to` fields now preserved (confirmed) or honestly flagged (`[narrative-mapped: uncertain]`) — never silently lost

**What's keeping it at 4:**
- Full end-to-end chain (Researcher → Formatter → DA → da-formatter → Writer) not yet validated
- Not validated across 5+ diverse topics (rubric requires this for 6+)
- Quality gate NOT MET path untested
- Source confidence threshold not implemented (backlog #3 area)

**What would move it to 5–6:**
- Run full research chain end-to-end and confirm inference traces preserved through to final document
- Validate confidence ratings in final Writer output trace back to source confidence
- Run across 3+ diverse topics with consistent results

### Chain Reliability (currently 7/10)

**What supports 7:**
- Individual chain variants validated: R→RF→W (Jina AI, Mar 6), Storyteller chain (Acme Corp, Mar 10), Prioritizer chain (routing validation, Mar 9), DA chain (da-formatter spot test, Mar 10)
- Formatter fires on every chain run (Rules 5/6/7/8 operational)
- Recipe timeouts fixed (#11, Mar 9)

**What's keeping it from 8+:**
- Full 5-link chain (R→RF→DA→DAF→W) not validated as a single end-to-end run
- Story-formatter appends normalization notes outside the STORY OUTPUT block

**What would move it to 8–9:**
- Run full R→RF→DA→DAF→W chain end-to-end, confirm clean handoff at every link
- Fix story-formatter normalization notes
- Validate all chain variants in a single test session

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
| Prioritizer-formatter (#33) | prose→PRIORITY OUTPUT: PASS *(2026-03-10-prioritizer-formatter-spot-test)* | Format Fidelity |
| Story-formatter handles Storyteller failure mode (#30) | document→STORY OUTPUT: PASS *(2026-03-10-storyteller-format-compliance-verification)* | Format Fidelity |
| Inferences in NARRATIVE SELECTION (#18) | I1–I3 with `(inference)` labels in INCLUDED FINDINGS: PASS | Format Fidelity |
| Writer-formatter handles informal register (#29) | audience=myself→canonical blocks: PASS *(2026-03-10-writer-informal-register-verification)* | Format Fidelity |
| DA Format B labeled extraction (#16 partial) | 9 findings from labeled narrative: PASS | Chain Reliability |
| DA code-fence prevention (#17) | ANALYSIS OUTPUT as bare text: PASS | Chain Reliability |
| da-formatter (#34) | narrative DA→canonical ANALYSIS OUTPUT: PASS *(2026-03-10-da-formatter-spot-test)* | Chain Reliability, Format Fidelity |

---

## Change History

| Version | Date | Changes |
|---------|------|---------|
| v2.0 | 2026-03-10 | **Reconciliation.** Consolidated two diverged scorecards into one. Retired `docs/01-vision/SCORECARD.md`. Anchored all dimension definitions to `SUCCESS-METRICS.md` § Scoring Rubric (new section added there). Added Scoring Rules to prevent future drift. Re-scored against reconciled rubric: Chain Reliability 9→7 (full chain unproven), Format Fidelity 10→7 (word budgets, audience calibration, #14 untested). Overall 7→6. |
| v1.2 | 2026-03-10 | Shipped #34 (da-formatter). Format Fidelity 9→10, Chain Reliability 8→9, Research Trustworthiness 3→4. |
| v1.1 | 2026-03-10 | Closed #33, #29, #30, verified #18/#19. Format Fidelity 8→9, Chain Reliability 7→8. |
| v1.0 | 2026-03-09 | Scorecard established. Initial scores: 3/7/8/6 = 6/10. |
