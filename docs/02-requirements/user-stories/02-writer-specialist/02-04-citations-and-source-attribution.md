# 02-04: Citations and Source Attribution

**Epic:** [02. Writer Specialist](../../epics/02-writer-specialist.md)
**Status:** ✅ Implemented

---

## Capability

Every writer response includes section-level source attribution (> *Sources: S1, S2*) after each factual section and a full CITATIONS index at the end — giving human readers trust signals at the point of reading and agents a parseable citation map.

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

**Created:** 2026-02-28 by Chris Park

**Epic:** [02. Writer Specialist](../../epics/02-writer-specialist.md)
