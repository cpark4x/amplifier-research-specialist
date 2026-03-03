# 02-01: Produce Format-Faithful Document

**Epic:** [02. Writer Specialist](../../epics/02-writer-specialist.md)
**Status:** ✅ Implemented

---

## Capability

The writer produces a document in the exact format requested (report, brief, proposal, executive summary, email, memo) with format-specific structure and conventions applied — not a generic output labelled with the requested format.

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

**Created:** 2026-02-27 by Chris Park

**Epic:** [02. Writer Specialist](../../epics/02-writer-specialist.md)
