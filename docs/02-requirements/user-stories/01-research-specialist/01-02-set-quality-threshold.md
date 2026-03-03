# 01-02: Set Quality Threshold

**Epic:** [01. Research Specialist](../../epics/01-research-specialist.md)
**Status:** ✅ Implemented

---

## User Story

**As an** orchestrator,
**I want** to set a `quality_threshold` (medium / high / maximum) when delegating research,
**So that** I control the depth-vs-speed tradeoff for different use cases.

---

## Done Looks Like

1. Orchestrator passes `quality_threshold: medium | high | maximum` alongside the research question
2. Researcher adjusts corroboration cycles and source requirements based on the threshold
3. At `maximum`, if the quality gate cannot be satisfied after 3 cycles, output includes an explicit `QUALITY THRESHOLD RESULT: NOT MET` block — it does not silently degrade
4. At `medium` or `high`, output is returned once the threshold is met

---

## Why This Matters

**The Problem:** Research depth is one-size-fits-all. A quick competitive check and a legal due diligence task need different standards but get the same treatment.

**This Fix:** A single parameter controls the rigor-speed tradeoff. The orchestrator decides; the specialist enforces it.

**The Result:** Fast answers when speed matters, rigorous evidence when accuracy matters — with an explicit failure signal when maximum quality can't be achieved.

---

## Dependencies

**Requires:** 01-01 (delegate research question)

---

## Implementation History

| Version | Date | Person | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-02-26 | Chris Park | Quality threshold with 3-cycle gate; `maximum` fails loud not silent |

---

**Epic:** [01. Research Specialist](../../epics/01-research-specialist.md)
