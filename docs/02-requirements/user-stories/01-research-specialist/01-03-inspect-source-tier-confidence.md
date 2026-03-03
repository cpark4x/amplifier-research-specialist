# 01-03: Inspect Source Tier and Confidence

**Epic:** [01. Research Specialist](../../epics/01-research-specialist.md)
**Status:** ✅ Implemented

---

## User Story

**As an** orchestrator,
**I want** to inspect the `source_tier` and `confidence` of each finding,
**So that** I know whether a claim came from a primary source or a speculative third-party summary.

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

## Implementation History

| Version | Date | Person | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-02-26 | Chris Park | Source tiering (primary/secondary/tertiary) and per-finding confidence levels in ResearchOutput |

---

**Epic:** [01. Research Specialist](../../epics/01-research-specialist.md)
