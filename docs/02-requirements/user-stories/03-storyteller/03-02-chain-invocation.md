# 03-02: Chain Invocation

**Epic:** [03. Storyteller](../../epics/03-storyteller.md)
**Status:** ✅ Implemented

---

## Capability

An orchestrator can invoke Storyteller as the final step in a Researcher → Formatter → Analyzer → Storyteller chain, producing narrative without manual reformatting between steps.

---

## Done Looks Like

1. Orchestrator runs narrative-chain recipe or manually chains the four specialists in sequence
2. Each step's output passes directly as input to the next without manual translation
3. Storyteller receives AnalysisOutput and produces StoryOutput
4. Final output is a compelling narrative — not a structured document

---

## Why This Matters

**The Problem:** Chaining specialists manually requires translating output formats between each step — research output to formatted document, document to analysis, analysis to narrative. Each translation is a point of failure and loss of fidelity.

**This Fix:** Each specialist in the chain accepts the prior specialist's output contract directly. Storyteller closes the chain by converting structured analysis into narrative.

**The Result:** Orchestrators run end-to-end research-to-narrative pipelines with a single recipe invocation and zero manual reformatting.

---

## Dependencies

**Requires:** 03-01 (transform analysis to narrative), narrative-chain.yaml recipe

**Enables:** Full end-to-end research-to-narrative automation

---

**Created:** 2026-03-04 by Chris Park

**Epic:** [03. Storyteller](../../epics/03-storyteller.md)
