# 02-02: Return WRITER METADATA Block

**Epic:** [02. Writer Specialist](../../epics/02-writer-specialist.md)
**Status:** ✅ Implemented

---

## User Story

**As an** orchestrator,
**I want** every writer response to begin with a machine-readable WRITER METADATA block,
**So that** I can parse coverage status, gaps, and format without reading the full document.

---

## Done Looks Like

1. Every writer response begins with a `WRITER METADATA` block before the document content
2. Block includes: `Specialist`, `Version`, `Input type`, `Output format`, `Audience`, `Voice`, `Word count`, `Coverage`, `Coverage gaps`
3. Orchestrator can check `Coverage: full | partial` and act on `Coverage gaps` without parsing the document body
4. Block is consistent across all formats and invocations — no exceptions

---

## Why This Matters

**The Problem:** Agents consuming writer output have no structured signal about document quality or completeness without parsing prose.

**This Fix:** The WRITER METADATA block is a machine-readable quality certificate on every output.

**The Result:** Downstream agents can route, log, or quality-assert based on metadata fields — no natural language parsing required.

---

## Dependencies

**Requires:** 02-01 (produce format-faithful document)

---

## Implementation History

| Version | Date | Person | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-02-27 | Chris Park | WRITER METADATA block as first element of every response |

---

**Epic:** [02. Writer Specialist](../../epics/02-writer-specialist.md)
