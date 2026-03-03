# 01-04: Read Evidence Gaps

**Epic:** [01. Research Specialist](../../epics/01-research-specialist.md)
**Status:** ✅ Implemented

---

## Capability

ResearchOutput includes an evidence_gaps section listing everything the Researcher tried and couldn't verify, so the orchestrator makes decisions with honest uncertainty rather than false completeness.

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

**Created:** 2026-02-26 by Chris Park

**Epic:** [01. Research Specialist](../../epics/01-research-specialist.md)
