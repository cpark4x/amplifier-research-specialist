# 02-01: Produce Format-Faithful Document

**Epic:** [02. Writer Specialist](../../epics/02-writer-specialist.md)
**Status:** ✅ Implemented

---

## User Story

**As an** orchestrator,
**I want** the writer to produce a document in the exact format I requested (report, brief, proposal, executive summary, email, memo),
**So that** I don't have to reformat or post-process the output before using it.

---

## Done Looks Like

1. Orchestrator passes `format: report | brief | proposal | executive-summary | email | memo` in the request
2. Writer applies format-specific structure and conventions (e.g. Brief = Summary → Key Points → Implications → Next Steps)
3. Output matches the requested format — a brief is not a report in brief clothing
4. WRITER METADATA block declares the output format so downstream agents can verify without parsing prose

---

## Why This Matters

**The Problem:** Inline writing produces generic prose regardless of format. A brief written inline looks like a shortened report, not a brief.

**This Fix:** Format is a contract. The writer knows and applies the conventions for each of 6 document types.

**The Result:** Downstream consumers receive correctly-formatted documents without manual reformatting.

---

## Dependencies

**Requires:** Amplifier Foundation

---

## Implementation History

| Version | Date | Person | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-02-27 | Chris Park | 5-stage pipeline with format-specific structure for 6 document types |

---

**Epic:** [02. Writer Specialist](../../epics/02-writer-specialist.md)
