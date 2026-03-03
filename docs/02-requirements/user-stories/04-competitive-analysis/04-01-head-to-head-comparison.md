# 04-01: Head-to-Head Comparison

**Epic:** [04. Competitive Analysis Specialist](../../epics/04-competitive-analysis.md)
**Status:** ✅ Implemented

---

## Capability

The specialist produces a structured CompetitiveAnalysisOutput with a comparison matrix and win conditions for two or more subjects, with facts and inferences explicitly separated — not a narrative summary.

---

## Done Looks Like

1. Orchestrator calls the competitive analysis specialist with two or more subjects and optional dimensions to compare
2. Specialist runs its 6-stage pipeline and returns a `CompetitiveAnalysisOutput` with a structured comparison matrix
3. Facts (sourced claims) and inferences (analyst conclusions) are explicitly labeled and never mixed
4. Win conditions, positioning gaps, and matrix entries all trace to evidence
5. Output is machine-parseable and can be passed directly to the Writer specialist for a formatted brief

---

## Why This Matters

**The Problem:** Competitive briefs are narrative summaries. There's no structured way to parse who wins on which dimension, or to trace claims back to sources.

**This Fix:** A dedicated pipeline that structures competitive intelligence into a machine-parseable contract — matrix, gaps, win conditions — separate from any prose.

**The Result:** Orchestrators receive structured competitive data they can act on, filter, or route to the Writer for human-readable output.

---

## Dependencies

**Requires:** `tool-web`, Amplifier Foundation

**Enables:** 04-02 (landscape analysis), 04-03 (accept existing research)

---

**Created:** 2026-03-02 by Chris Park

**Epic:** [04. Competitive Analysis Specialist](../../epics/04-competitive-analysis.md)
