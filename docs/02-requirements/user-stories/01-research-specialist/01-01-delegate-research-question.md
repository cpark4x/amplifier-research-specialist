# 01-01: Delegate Research Question

**Epic:** [01. Research Specialist](../../epics/01-research-specialist.md)
**Status:** ✅ Implemented

---

## User Story

**As an** orchestrator,
**I want** to delegate a research question with a `query_type` and receive a structured `ResearchOutput`,
**So that** I don't mix research execution with decision-making in the same agent.

---

## Done Looks Like

1. Orchestrator calls `specialists:researcher` with a `question` string and a `query_type` (person / company / technical / market / event)
2. Researcher runs its 7-stage pipeline and returns a `ResearchOutput` contract
3. Every finding in the output includes a source URL, tier, and confidence level
4. The orchestrator can parse and act on the output without re-running research

---

## Why This Matters

**The Problem:** Orchestrators that research inline produce shallow results with no structure — no source provenance, no confidence levels, no gaps. Everything is mixed into one agent.

**This Fix:** Delegates research entirely to a specialist with a clean contract. The orchestrator stays focused on decision-making.

**The Result:** Research and decision-making are fully separated. The orchestrator receives structured evidence, not a prose summary to interpret.

---

## Dependencies

**Requires:** Amplifier Foundation, `tool-web`

**Enables:** 01-02 (quality threshold), 01-03 (source inspection), 01-04 (evidence gaps)

---

## Implementation History

| Version | Date | Person | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-02-26 | Chris Park | Initial researcher specialist with 7-stage pipeline and ResearchOutput contract |

---

**Epic:** [01. Research Specialist](../../epics/01-research-specialist.md)
