# 01-04: Read Evidence Gaps

**Epic:** [01. Research Specialist](../../epics/01-research-specialist.md)
**Status:** ✅ Implemented

---

## User Story

**As an** orchestrator,
**I want** to read `evidence_gaps` in the output to know what the Researcher tried and couldn't verify,
**So that** I make decisions with honest uncertainty rather than false completeness.

---

## Done Looks Like

1. `ResearchOutput` includes an `evidence_gaps` section listing every claim that could not be verified and why
2. Paywall encounters, fetch failures, and contradicted claims are all surfaced as gaps — never silently dropped
3. Orchestrator can read gaps to decide whether to re-run with different parameters, accept the partial output, or escalate
4. A short honest output with named gaps is preferred over a long confident-sounding one that papers over failures

---

## Why This Matters

**The Problem:** Generic research agents return prose that sounds authoritative. There's no way to know what wasn't found.

**This Fix:** Gaps are first-class outputs. The Researcher never hides uncertainty.

**The Result:** Orchestrators make decisions knowing exactly what evidence exists and what doesn't.

---

## Dependencies

**Requires:** 01-01 (delegate research question)

---

## Implementation History

| Version | Date | Person | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-02-26 | Chris Park | Evidence gaps as first-class output; paywall fallback ladder logged |

---

**Epic:** [01. Research Specialist](../../epics/01-research-specialist.md)
