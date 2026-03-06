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

*As of 2026-03-06 — after session 1*

| Dimension | Score | Status | Key Gaps |
|---|---|---|---|
| **Research Trustworthiness** | 5/10 | *(spec)* | Confidence tiers + URL enforcement added (#5). Not yet validated by test run. |
| **Chain Reliability** | 4/10 | — | Formatter step skipped in Mar 6 log (#27 open). Timeout fragility (#11 open). |
| **Format Fidelity** | 3/10 | — | Brief = ~1500w (should be ~400–600w). Audience undifferentiated. CLAIMS TO VERIFY buried. |
| **Specialist Coverage** | 4/10 | — | 5/11 epics complete. Most Phase 1 roadmap gates open. |
| **Overall** | **4.0/10** | | |

---

## Session Log

| Date | Session | Changes | Dimension Deltas | Overall |
|---|---|---|---|---|
| 2026-03-06 | Session 1 | Added session startup procedure (`context/session-startup.md`). Researcher trustworthiness overhaul — backlog #5: explicit `unrated` ban, URL capture enforcement, numeric/financial claim handling (Stage 3 + Stage 4 + Core Principles). | Research Trust: 2→5 *(spec)* | 3.0 → 4.0 *(spec)* |

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
| v1.0 | 2026-03-06 | Initial scorecard — first session baseline |
