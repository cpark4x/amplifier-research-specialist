# 02-04: Citations and Source Attribution

**Epic:** [02. Writer Specialist](../../epics/02-writer-specialist.md)
**Status:** ✅ Implemented

---

## User Story

**As an** orchestrator or human reader,
**I want** every factual claim in the document to be traceable to its source material,
**So that** I can verify any claim without re-reading the entire source.

---

## Done Looks Like

1. Writer numbers source claims at parse time (S1, S2, S3 ...)
2. Every factual section ends with a `> *Sources: S1 (label), S2 (label)*` attribution blockquote
3. Every response ends with a `CITATIONS` section mapping each Sn to its source text and the document section that used it
4. Human readers see trust signals at the point of reading (section attribution); agents get a parseable citation index at the end
5. Writer verifies citation completeness before returning — no factual section is left without attribution

---

## Why This Matters

**The Problem:** Documents produced by AI agents look authoritative but provide no way to verify individual claims. Trust is all-or-nothing.

**This Fix:** Two-layer citation architecture — section attribution for human readers, CITATIONS index for agents.

**The Result:** Every claim is verifiable. Downstream consumers can audit without re-reading source material.

---

## Dependencies

**Requires:** 02-01 (produce format-faithful document), 02-02 (WRITER METADATA block), 02-03 (coverage gaps)

---

## Implementation History

| Version | Date | Person | Changes |
|---------|------|--------|---------|
| v1.1 | 2026-03-02 | Chris Park | Section-level attribution blockquotes added (`> *Sources: Sn*` after each factual section) |
| v1.0 | 2026-02-28 | Chris Park | Post-document CITATIONS section; source claims numbered S1, S2... at parse time |

---

**Epic:** [02. Writer Specialist](../../epics/02-writer-specialist.md)
