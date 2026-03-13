# Quality Gate Validation: NOT MET Path Testing

**Date:** 2026-03-13
**Tester:** Chris (via Amplifier session)
**Quality signal:** PASS — all gates fired correctly
**Action items promoted:** true

---

## Purpose

Validate that mechanical fail triggers in the storyteller and data-analyzer specialists actually fire NOT MET when evidence quality is insufficient. These gates were defined in spec but had never been tested.

---

## Test 1: Storyteller — Sparse Input Trigger

**Input:** 2 findings (both low confidence, tertiary), 1 low-confidence inference. Audience: board.

**Expected:** QUALITY THRESHOLD RESULT: NOT MET — sparse input trigger (fewer than 3 findings).

**Result:** PASS

- Correctly identified 2 discrete findings at Stage 1
- Mechanical fail trigger fired immediately — pipeline halted, no story drafted, no revision cycles
- Emitted NOT MET with specific failing items: "Sparse input — only 2 discrete findings available; minimum is 3"
- Bonus: provided actionable recommendation to upstream about what evidence is missing (competitive landscape, value proposition, performance indicators)

**Observation:** The storyteller correctly treated the single inference as derivative of the 2 findings and did not count it as a third finding. Correct behavior.

---

## Test 2: Data Analyzer — High Threshold with Low Evidence

**Input:** 3 findings, all tertiary tier, all low confidence. quality_threshold: high. Upstream QUALITY THRESHOLD RESULT: NOT MET.

**Expected:** QUALITY THRESHOLD RESULT: NOT MET — all inferences would trace only to low-confidence findings.

**Result:** PASS

- Correctly parsed 3 findings and identified all as low-confidence tertiary
- Drew zero inferences — refused to force conclusions from thin evidence
- All 3 findings routed to UNUSED FINDINGS with specific reasons
- Emitted NOT MET with clear rationale: "All three findings are tertiary-tier with low confidence... The high quality threshold requires at least some findings at primary or secondary tier"

**Observation:** The DA correctly chose to draw no inferences rather than produce low-confidence ones under a high threshold. This is the designed behavior — "never force an inference."

---

## Test 3: Storyteller — Evidence Collapse (Borderline)

**Input:** 6 findings (5 low confidence/unattributed, 1 high confidence primary source — AlphaFold). Audience: general. Tone: dramatic.

**Expected:** Borderline test — 2 of 6 findings insufficient, below 50% collapse threshold. Should produce a story but lean heavily on the one strong finding.

**Result:** PASS (MET — correctly did not trigger evidence collapse)

- Extracted 6 findings at Stage 1 — sparse trigger did not fire (correct)
- Omitted 2 findings (F1, F4) with insufficient-evidence rationale — 33%, below 50% threshold
- Included 4 findings — built narrative around the single high-confidence finding (AlphaFold)
- Explicitly hedged all low-confidence claims with "reportedly," "said to be," "suggest"
- Made the evidence weakness the narrative theme: "The One Proof in a Sea of Promises"
- Quality gate correctly calculated: "2 of 6 findings omitted with insufficient-evidence (33%). Threshold is >50%. PASS."

**Observation:** The storyteller's response to weak evidence was sophisticated — it didn't just pass the gate, it used the gap between strong and weak evidence as the dramatic tension. The trust architecture worked at both the mechanical level (gate math was correct) and the narrative level (hedging language preserved confidence signals).

---

## Summary

| Test | Specialist | Trigger | Expected | Actual | Verdict |
|------|-----------|---------|----------|--------|---------|
| 1 | Storyteller | Sparse input (2 findings) | NOT MET | NOT MET | PASS |
| 2 | Data Analyzer | High threshold + low evidence | NOT MET | NOT MET | PASS |
| 3 | Storyteller | Evidence collapse (borderline) | MET | MET | PASS |

**Conclusion:** Quality gates are functional. Both specialists correctly refuse to produce output when evidence doesn't warrant it, and both explain why in actionable terms. The evidence collapse trigger's 50% threshold is correctly calculated. No spec changes needed.

**Remaining untested paths:**
- Storyteller: upstream NOT MET trigger (source material has NOT MET and fewer than 3 medium+ findings)
- Storyteller: evidence collapse at >50% (needs input with 4+ of 6+ findings genuinely insufficient)
- Researcher: quality_threshold: maximum with low confidence claims after 3 QG cycles (requires live research, not mockable in isolation)
- Prioritizer: quality_threshold: high path (untested)