# 03-03: Existing Document Narrative

**Epic:** [03. Storyteller](../../epics/03-storyteller.md)
**Status:** ✅ Implemented

---

## Capability

A user can pass any existing document to Storyteller with a tone preference and receive it re-rendered as narrative for a specific audience — without requiring a pipeline-sourced document.

---

## Done Looks Like

1. User passes existing document with `tone: dramatic` and `audience: engineering team`
2. Storyteller detects input type as `document`, extracts findings, runs full pipeline
3. Output is narrative in the requested tone with `NARRATIVE SELECTION` showing what was selected
4. Story respects source fidelity — no fabricated content beyond what the document contains

---

## Why This Matters

**The Problem:** Existing documents — reports, briefs, analyses — are locked in their original format. Re-rendering them for a different audience requires manual rewriting with no guardrails against fabrication.

**This Fix:** Storyteller accepts any document as input, extracts its findings, and applies the full narrative pipeline with tone and audience parameters — keeping output grounded in the source.

**The Result:** Any document can be re-rendered as audience-appropriate narrative with source fidelity guaranteed and editorial choices fully visible.

---

## Dependencies

**Requires:** 03-01 (transform analysis to narrative)

**Enables:** Ad-hoc narrative rendering without requiring full research pipeline

---

**Created:** 2026-03-04 by Chris Park

**Epic:** [03. Storyteller](../../epics/03-storyteller.md)
