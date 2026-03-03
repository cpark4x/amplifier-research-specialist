# 01-05: Add Research Capability via Bundle

**Epic:** [01. Research Specialist](../../epics/01-research-specialist.md)
**Status:** ✅ Implemented

---

## User Story

**As a** developer building an Amplifier workflow,
**I want** to include the `specialists` bundle to immediately add research capability to any project,
**So that** I don't have to build my own research pipeline from scratch.

---

## Done Looks Like

1. Developer adds a single `includes` line to their `bundle.md` referencing `canvas-specialists`
2. The `specialists:researcher` agent is immediately available to any orchestrator in that project
3. No additional configuration required beyond the bundle include
4. The researcher works with any Amplifier provider — not locked to a specific LLM

---

## Dependencies

**Requires:** Amplifier Foundation

---

## Implementation History

| Version | Date | Person | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-02-26 | Chris Park | Bundle registered and wired; researcher available as `specialists:specialists/researcher` |

---

**Epic:** [01. Research Specialist](../../epics/01-research-specialist.md)
