# 04-02: Landscape Analysis

**Epic:** [04. Competitive Analysis Specialist](../../epics/04-competitive-analysis.md)
**Status:** ✅ Implemented

---

## Capability

The specialist can discover and profile all relevant competitors in a subject area without the caller specifying them upfront, returning a full landscape matrix.

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

**Created:** 2026-03-02 by Chris Park

**Epic:** [04. Competitive Analysis Specialist](../../epics/04-competitive-analysis.md)
