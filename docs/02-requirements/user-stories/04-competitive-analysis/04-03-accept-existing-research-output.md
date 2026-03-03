# 04-03: Accept Existing ResearchOutput

**Epic:** [04. Competitive Analysis Specialist](../../epics/04-competitive-analysis.md)
**Status:** ✅ Implemented

---

## User Story

**As an** orchestrator,
**I want** to pass existing `ResearchOutput` from the Researcher specialist into the competitive analysis specialist,
**So that** I skip the research phase and get structured competitive intelligence from evidence I've already gathered.

---

## Done Looks Like

1. Orchestrator passes a `ResearchOutput` object alongside the analysis request
2. Specialist detects the provided research and skips its internal research phase
3. Analysis runs directly on the provided evidence — no redundant web searches
4. The full Researcher → Competitive Analysis chain works without manual handoff

---

## Why This Matters

**The Problem:** Research is expensive. Running separate research inside every specialist wastes time and produces inconsistent evidence bases.

**This Fix:** The competitive analysis specialist accepts upstream `ResearchOutput` as a first-class input, enabling clean specialist chaining.

**The Result:** `Researcher → Competitive Analysis → Writer` is a composable pipeline. Each specialist does one job.

---

## Dependencies

**Requires:** 04-01 (head-to-head comparison), Epic 01 (Researcher specialist — ResearchOutput contract)

**Enables:** Full Researcher → Competitive Analysis → Writer chain

---

## Implementation History

| Version | Date | Person | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-03-02 | Chris Park | Conditional research phase — skipped when ResearchOutput is provided |

---

**Epic:** [04. Competitive Analysis Specialist](../../epics/04-competitive-analysis.md)
