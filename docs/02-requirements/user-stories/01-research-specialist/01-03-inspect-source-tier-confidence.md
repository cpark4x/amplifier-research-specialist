# 01-03: Inspect Source Tier and Confidence

**Epic:** [01. Research Specialist](../../epics/01-research-specialist.md)
**Status:** ✅ Implemented

---

## Capability

Every finding in ResearchOutput includes a source_tier (primary / secondary / tertiary) and confidence level, so the orchestrator knows the quality of each claim before acting on it.

---

## Done Looks Like

1. Every finding in `ResearchOutput` includes `source_tier` (primary / secondary / tertiary) and `confidence` (high / medium / low)
2. Primary sources (official docs, SEC filings, direct transcripts) are distinguished from secondary and tertiary
3. Orchestrator can filter or weight findings by tier before acting on them
4. No finding enters the output without both fields populated — the contract is enforced, not aspirational

---

## Dependencies

**Requires:** 01-01 (delegate research question)

---

**Created:** 2026-02-26 by Chris Park

**Epic:** [01. Research Specialist](../../epics/01-research-specialist.md)
