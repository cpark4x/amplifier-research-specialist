# 03-04: Audit Editorial Choices

**Epic:** [03. Storyteller](../../epics/03-storyteller.md)
**Status:** ✅ Implemented

---

## Capability

A caller can review `NARRATIVE SELECTION` to see which findings were included (with role) and omitted (with rationale) — making editorial decisions fully auditable.

---

## Done Looks Like

1. Every StoryOutput includes a `NARRATIVE SELECTION` block
2. `INCLUDED FINDINGS` lists each finding used with its narrative role
3. `OMITTED FINDINGS` lists each finding set aside with rationale for omission
4. Sum of included + omitted equals total findings from the source
5. Caller can verify no findings were silently dropped

---

## Why This Matters

**The Problem:** Narrative generation is a black box — callers cannot tell which evidence was used, which was dropped, or why. This makes narrative outputs untrustworthy for high-stakes audiences.

**This Fix:** Every StoryOutput declares its full editorial ledger. Inclusion is justified by narrative role; omission is justified by explicit rationale. No finding disappears without explanation.

**The Result:** Narrative outputs are fully auditable. Callers can verify coverage, challenge omissions, and trust that the story is grounded in the complete evidence set.

---

## Dependencies

**Requires:** 03-01 (transform analysis to narrative)

**Enables:** Trust in narrative outputs for high-stakes and compliance-sensitive audiences

---

**Created:** 2026-03-04 by Chris Park

**Epic:** [03. Storyteller](../../epics/03-storyteller.md)
