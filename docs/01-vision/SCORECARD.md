# Canvas Specialists: Progress Scorecard

**How far we are from best in class — tracked per session.**

**Owner:** Chris Park
**Last Updated:** 2026-03-06

---

## How to Read This

**Scores are 0–10 per dimension.** 10/10 means the vision doc's definition of success is fully met and validated by test evidence. Scores are honest — a spec change is not the same as a validated improvement.

**Score labels:**
- *(spec)* — instructions updated, not yet confirmed by a test log run
- *(validated)* — confirmed by test log evidence

**Overall score** = average of the four dimensions, rounded to one decimal.

**When to update:** At the end of each session, add one row to the Session Log and update Current State if scores changed.

---

## The Goal (10/10 Across All Dimensions)

Anchored to `SUCCESS-METRICS.md` and `VISION.md`:

| Dimension | What 10/10 Looks Like |
|---|---|
| **Research Trustworthiness** | 100% of claims have high/medium/low confidence (zero `unrated`), 100% have verifiable URLs, quality gate demonstrably returns NOT MET, evidence gaps always disclosed — validated across 5+ test runs |
| **Chain Reliability** | Formatter step fires on every chain run, zero timeout failures, ResearchOutput passes to Writer without preprocessing — validated end-to-end |
| **Format Fidelity** | Brief = 250–400 words, report = ~1500 words, audience calibration produces distinct output, CLAIMS TO VERIFY surfaced — validated across all formats |
| **Specialist Coverage** | All 11 epics complete, Phase 1–3 roadmap gates checked, full chain validated end-to-end |

---

## Current State

*As of 2026-03-06 — end of session 2 (post-validation, writer quality fixes)*

| Dimension | Score | Status | Key Gaps |
|---|---|---|---|
| **Research Trustworthiness** | 5/10 | *(validated)* | Architecture fix validated. Researcher produces natural narrative; formatter canonicalizes to categorical confidence + full tier labels on every run. Remaining gaps: quality gate NOT MET path untested across 5+ topics; coverage depth varies by topic. |
| **Chain Reliability** | 5/10 | *(validated)* | Researcher→Formatter→Writer chain completed end-to-end without manual intervention. Formatter fired on all 43 claims. Rule 5 confirmed operational. Recipe timeout (#11) still open but not hit in this run. |
| **Format Fidelity** | 6/10 | *(validated)* | #7, #9, #28 shipped. Audience calibration confirmed working (first-person register for `myself`). Specificity gate confirmed. CLAIMS TO VERIFY inline surfacing confirmed. OUTPUT CONTRACT compliance for informal registers still fragile (#29). |
| **Specialist Coverage** | 4/10 | — | 5/11 epics complete. Most Phase 1 roadmap gates open. |
| **Overall** | **5.1/10** | | |

---

## Session Log

| Date | Session | Changes | Dimension Deltas | Overall |
|---|---|---|---|---|
| 2026-03-06 | Session 1 | **Shipped:** session startup procedure, SCORECARD.md, #5 (researcher `unrated` ban + URL enforcement), #6 (writer word budgets all formats + Stage 5 enforcement), #27 (formatter mandatory gate). **Validated:** Writer brief = 316w (PASS). Researcher `unrated` gone + URLs present (PARTIAL — format compliance still broken: narrative output, numeric confidence, wrong tier labels). Recipe timeout confirmed at writer step. **Net:** #6 validated, #5 partially validated, #27 untested in live session. #22 promoted to sprint priority. | Research Trust: 2→5→3, Format Fidelity: 3→5 *(validated for writer)*, Chain: 4→5→4 | 3.0 → 4.8 → 4.0 |
| 2026-03-06 | Session 2 cont. | **Shipped:** #28 (CLAIMS TO VERIFY surfacing + scope extended to researcher-output), #7 (audience calibration — `myself` register, Stage 4 register table), #9 (specificity gate in Stage 5), #18 (Storyteller inference auditability in NARRATIVE SELECTION), #19 (Storyteller quality_threshold param). **Validated:** #7 and #9 PASS on Mistral AI test run. #28 PARTIAL — inline caveat surfacing works, formal block absent for `myself` audience; OUTPUT CONTRACT slip logged as #29. Format Fidelity 5→6. | Format Fidelity: 5→6 *(validated)* | 4.8 → 5.1 |
| 2026-03-06 | Session 2 | **Shipped:** #22 architectural reframe — stripped ~150 lines of format enforcement from researcher (OUTPUT CONTRACT, Stage 0, Stage 7 template, COMPLIANCE NOTE, SELF-CHECK, wrong/right examples), added compact output expectations. Promoted formatter to essential pipeline stage with validation rules (numeric→categorical confidence mapping, T1→primary tier normalization, URL validation, removed pass-through mode). Updated coordinator Rule 5, recipe prompt, types.md, SUCCESS-METRICS.md. Fixed canvas-renderer module rename. **Validated:** Full researcher→formatter→writer chain on "What is Jina AI?" — 43 claims, all confidence categorical, all tiers full labels, zero numeric values, EVIDENCE GAPS present, writer brief with 10 citations + 5 CLAIMS TO VERIFY. Architecture thesis confirmed: researcher focuses on evidence, formatter handles format. | Research Trust: 3→5 *(validated)*, Chain Reliability: 4→5 *(validated)* | 4.0 → 4.8 |

---

## Dimension Reference

### Research Trustworthiness
*Criteria: V1 Leading + Lagging Indicators in `SUCCESS-METRICS.md`*

| Score | Meaning |
|---|---|
| 0–2 | Core mechanisms broken — confidence tiers absent, no URLs, quality gate decorative |
| 3–5 | Spec correct, some validation. Most claims rated, URLs present, gaps disclosed |
| 6–8 | Validated across multiple topics. Quality gate returns NOT MET. Caller can audit any claim. |
| 9–10 | Full V1 success criteria met and validated. "I trusted it because I could see every source." |

### Chain Reliability
*Criteria: `SUCCESS-METRICS.md` V2 Composability + chain success criteria*

| Score | Meaning |
|---|---|
| 0–2 | Chain breaks frequently — formatter skipped, timeouts, parsing failures |
| 3–5 | Chain works most of the time. Known fragility points exist but workarounds in place. |
| 6–8 | Rule 5 compliance consistent. No timeouts in standard runs. Formatter never needed to rescue. |
| 9–10 | Full chain end-to-end validated. Zero preprocessing needed between specialists. |

### Format Fidelity
*Criteria: `SUCCESS-METRICS.md` V2 Format Fidelity + universal baseline U1*

| Score | Meaning |
|---|---|
| 0–2 | Format is a label only — brief and report indistinguishable in practice |
| 3–5 | Formats partially distinct. Word budgets wrong. Audience undifferentiated. |
| 6–8 | Word budgets enforced. Audience register distinct. CLAIMS TO VERIFY surfaced. |
| 9–10 | 100% format fidelity validated. "The brief was exactly right — not a report in brief clothing." |

### Specialist Coverage
*Criteria: Roadmap phases in `VISION.md` + epic status in `BACKLOG.md`*

| Score | Meaning |
|---|---|
| 0–2 | Fewer than 3 epics complete |
| 3–5 | Core specialists built (Researcher, Writer, DA, CA). Phase 1 mostly done. |
| 6–8 | Phase 2 complete. Design, Planner, Prioritizer specialists added. |
| 9–10 | All 11 epics complete. Full roadmap delivered. Pattern proven repeatable. |

---

## Change History

| Version | Date | Changes |
|---|---|---|
| v1.3 | 2026-03-06 | Session 2 continued — Writer quality fixes #28/#7/#9 shipped and partially validated. Storyteller #18/#19 shipped. Format Fidelity 5→6 (validated). Overall 4.8→5.1. |
| v1.2 | 2026-03-06 | Session 2 complete — Shipped #22 as architectural reframe. Research Trustworthiness 3→5 (validated). Chain Reliability 4→5 (validated). Overall 4.0→4.8 (validated). |
| v1.1 | 2026-03-06 | Session 1 complete — Format Fidelity 3→5 (spec) after #6. Overall 4.0→4.5 (spec). Session log updated to include both #5 and #6. |
| v1.0 | 2026-03-06 | Initial scorecard — first session baseline |
