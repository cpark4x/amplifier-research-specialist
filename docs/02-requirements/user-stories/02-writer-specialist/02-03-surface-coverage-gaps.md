# 02-03: Surface Coverage Gaps Before Drafting

**Epic:** [02. Writer Specialist](../../epics/02-writer-specialist.md)
**Status:** ✅ Implemented

---

## Capability

The writer audits source material coverage before drafting begins. Critical gaps halt execution and surface to the caller; non-critical gaps are documented in WRITER METADATA. Nothing is silently papered over.

---

## Done Looks Like

1. Writer runs a coverage audit (Stage 2) before writing a single word
2. Writer maps the requested document structure to available source material
3. If a critical gap is found (document cannot be written without it), writer halts and surfaces the gap to the caller
4. Non-critical gaps are flagged in WRITER METADATA's `Coverage gaps` field and the writer proceeds with what it has
5. Writer never silently writes around gaps — every gap is named

---

## Why This Matters

**The Problem:** Inline writing silently fills gaps with invented content or awkward omissions. There's no pre-flight check.

**This Fix:** Coverage audit runs before drafting. Critical gaps stop execution; non-critical gaps are documented.

**The Result:** Orchestrators know what's covered and what isn't before investing in downstream processing.

---

## Dependencies

**Requires:** 02-01 (produce format-faithful document), 02-02 (WRITER METADATA block)

---

**Created:** 2026-02-27 by Chris Park

**Epic:** [02. Writer Specialist](../../epics/02-writer-specialist.md)
