# 04-02: Landscape Analysis

**Epic:** [04. Competitive Analysis Specialist](../../epics/04-competitive-analysis.md)
**Status:** ✅ Implemented

---

## User Story

**As an** orchestrator,
**I want** to request a landscape analysis for a subject area,
**So that** I receive a structured map of all relevant competitors and how they compare — without needing to specify them upfront.

---

## Done Looks Like

1. Orchestrator passes a subject (e.g. "AI writing tools") without pre-specifying competitors
2. Specialist runs a discovery step to identify relevant competitors in the landscape
3. Each discovered competitor is profiled and compared on key dimensions
4. Output is a `CompetitiveAnalysisOutput` with a full landscape matrix, not just a list
5. Unknown competitors are explicitly noted as evidence gaps

---

## Dependencies

**Requires:** `tool-web`, Amplifier Foundation, 04-01 (head-to-head comparison infrastructure)

---

## Implementation History

| Version | Date | Person | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-03-02 | Chris Park | Landscape mode with competitor discovery step before profiling |

---

**Epic:** [04. Competitive Analysis Specialist](../../epics/04-competitive-analysis.md)
