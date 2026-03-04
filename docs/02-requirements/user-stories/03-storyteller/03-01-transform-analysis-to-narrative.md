# 03-01: Transform Analysis to Narrative

**Epic:** [03. Storyteller](../../epics/03-storyteller.md)
**Status:** ✅ Implemented

---

## Capability

A knowledge worker can pass AnalysisOutput to Storyteller with audience and receive compelling narrative with auditable editorial choices — not just reformatting.

---

## Done Looks Like

1. Caller passes AnalysisOutput with audience (e.g. `board of directors`)
2. Storyteller runs 5-stage pipeline and returns StoryOutput
3. Output includes `STORY OUTPUT` header, `NARRATIVE SELECTION`, clean story prose, `QUALITY THRESHOLD RESULT`
4. Story has dramatic question, protagonist, stakes, causal chain, peak moment, resolution
5. Every finding accounted for — included with role or omitted with rationale

---

## Why This Matters

**The Problem:** Analysis outputs are structured and accurate but inert — they list findings without a through-line, stakes, or resolution. Readers disengage before reaching the key insight.

**This Fix:** Storyteller runs a deliberate 5-stage pipeline that selects, sequences, and renders findings as narrative — with every editorial choice documented.

**The Result:** Audiences receive a compelling story grounded in evidence, not a reformatted list. Editorial decisions are fully visible and auditable.

---

## Dependencies

**Requires:** Amplifier Foundation, AnalysisOutput contract

**Enables:** 03-02 (chain invocation), 03-03 (existing document narrative), 03-04 (audit editorial choices)

---

**Created:** 2026-03-04 by Chris Park

**Epic:** [03. Storyteller](../../epics/03-storyteller.md)
