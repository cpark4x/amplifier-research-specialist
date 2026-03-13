---
specialist: writer-formatter
chain: "researcher → researcher-formatter → data-analyzer → da-formatter → writer → writer-formatter → save"
topic: research-trustworthiness-fixes
date: 2026-03-10
quality_signal: mixed
action_items_promoted: true
---

## Purpose

Validate three Research Trustworthiness fixes targeting the gaps identified in
the full chain audit (2026-03-10-poolside-ai-full-chain-audit):
1. Source URLs in CITATIONS (writer-formatter + researcher)
2. Confidence hedging in prose (writer-formatter Stage 3.5)
3. Inference traces_to preservation (writer-formatter)

---

## Fixes Applied

**Writer-formatter (`0cf75c5`):**
- Edit A: Stage 1 extraction extended with `source:` URL and `traces_to:` fields
- Edit B: New Stage 3.5 — Confidence-Hedge Audit (medium→"reportedly",
  low→"According to unconfirmed reports", inference→"Evidence suggests")
- Edit C: Stage 5 CITATIONS template extended with source, type: inference, traces_to
- Edit D: Output Format examples updated
- Edit E: "What You Do Not Do" carve-out for Stage 3.5

**Researcher (`9737912`):**
- "URLs are evidence, not formatting" reinforcement in Stage 7
- Self-check expanded to verify https:// URLs per finding

**Recipe:**
- Writer-formatter timeout bumped 600s → 1200s (new Stage 3.5 adds processing time)

---

## Validation Run 1: Full Chain (recipe session `b50488a0ddba4883`)

Topic: "What is Poolside AI and how does it compare to other AI coding assistants?"
Format: brief | Audience: technical decision-maker | Voice: executive

### Results

**Confidence Hedging: PASS**
- 100% of medium/low/inference claims hedged in prose
- Medium claims: `reportedly` applied consistently (e.g., "reportedly pursuing $2B more",
  "reportedly 40,000+ GB300 NVL72s", "reportedly multi-agent orchestration")
- Low claims: `According to unconfirmed reports` (e.g., "According to unconfirmed reports,
  revenue is approximately $50M")
- Inference claims: `Evidence suggests` (e.g., "Evidence suggests this verification vacuum
  is a deliberate strategic choice", "Evidence suggests Poolside inverts Copilot on every axis")
- Zero unhedged medium/low/inference claims found
- Hedging scaled appropriately by confidence tier

**Source URLs in CITATIONS: FAIL**
- 0/50 citations carry source URLs
- All non-inference citations: `source: unattributed`
- The `source:` field is structurally present (writer-formatter fix worked)
  but filled with defaults because the upstream data doesn't exist

**Inference traces_to: FAIL (expected)**
- 12/12 inference citations have `type: inference` and `traces_to:` fields (structural PASS)
- All 12 traces_to values: `[narrative-mapped: uncertain]` (semantic FAIL)
- This is the DA-formatter being honest — DA produced narrative prose,
  mapper couldn't identify specific F# references

### Root Cause for URL Failure

Traced URLs through every pipeline stage:

| Step | https:// URLs present? |
|------|----------------------|
| 1. Researcher output | **0** — 12 named sources, zero actual URLs |
| 2. Researcher-Formatter | 0 — fell back to `Source: unknown` |
| 3. Data Analyzer | 0 |
| 4. DA-Formatter | 0 |
| 5. Writer | 0 |
| 6. Writer-Formatter | 0 → emits `source: unattributed` |

The Researcher visited URLs during web_fetch/web_search tool calls but did not
include them in its output text. The Source Registry has names and tiers but no
URL column. Every downstream step faithfully passed through nothing.

## Validation Run 2: Researcher-Only (standalone delegation)

Ran the Researcher standalone with tighter scope constraints (3 sub-questions,
8 URLs, 1 QG cycle, 1500 words). Result: Source Registry still has source names
and tiers but **zero full https:// URLs**. Output also didn't start with
`RESEARCH OUTPUT` despite the self-check instruction.

**Confirms the project pattern: instruction-level fixes to primary specialists
don't hold under long-context generation.** Same root cause as Writer format
compliance (#29), Storyteller OUTPUT CONTRACT (#30), DA code fences (#17),
and Researcher format compliance (#22). All required architectural (formatter)
fixes.

---

## Summary

| Fix | Verdict | Notes |
|-----|---------|-------|
| Confidence hedging (Stage 3.5) | **PASS** | Formatter fix — holds reliably |
| Source URLs (writer-formatter structural) | **PASS** (structural) | Field present, correctly defaults |
| Source URLs (researcher output) | **FAIL** | Instruction fix — doesn't hold |
| Inference traces_to (structural) | **PASS** (structural) | Field present, carries upstream value |
| Inference traces_to (semantic) | **FAIL** | Upstream DA-formatter limitation |

**Net: 1 clear win (hedging), 2 structural wins (fields present), 2 upstream
problems requiring architectural solutions.**

---

## Action Items

- [ ] **Architectural fix for Researcher URL emission.** Instruction-based fixes
  confirmed not holding (6th instance of this pattern). Options: (a) Researcher-formatter
  enhancement to extract URLs from source names + research narrative, (b) pipeline
  change to capture tool-call URLs, (c) new "URL extraction" step in recipe.
  Requires design session.
- [ ] **DA structured output for traces_to.** The `[narrative-mapped: uncertain]`
  placeholder is honest but limits traceability. Either the DA needs to produce
  structured output with F# traces (instruction fix — likely won't hold), or the
  DA-formatter needs better semantic mapping of narrative inferences to findings.
  Lower priority than URLs — the placeholder is at least honest about uncertainty.

---

## Scorecard Impact

- Research Trustworthiness: stays **4/10** — hedging is a real quality improvement
  but the two provenance gaps (URLs, traces_to) keep the score in the 3-5 band
  ("Architecture correct, some validation. Not validated across diverse topics.")
- Chain Reliability: stays **8/10** — timeout hit on validation run 1 (DA at 900s)
  but this is infrastructure, not architectural. Writer-formatter timeout bumped
  to 1200s.
- Format Fidelity: no change at **7/10**
- Overall: stays **6/10**
