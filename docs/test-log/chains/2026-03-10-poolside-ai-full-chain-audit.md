---
specialist: researcher
chain: "researcher → researcher-formatter → data-analyzer → da-formatter → writer → writer-formatter → save"
topic: poolside-ai-full-chain-audit
date: 2026-03-10
quality_signal: mixed
action_items_promoted: false
---

## Purpose

End-to-end validation of the full 8-step research-chain recipe (v1.6.0).
This is the first run of the complete R→RF→DA→DAF→W→WF chain as a single
end-to-end pipeline. The goal is to validate two scorecard dimensions:
Chain Reliability (does the chain complete?) and Research Trustworthiness
(do trust signals survive to the final document?).

**Research question:** "What is Poolside AI and how does it compare to other AI coding assistants?"
**Output format:** brief | **Audience:** technical decision-maker | **Voice:** executive

**Recipe session:** `26c3ae8d90404f9e-20260310-173051_recipe`

---

## What Worked

- **Full chain completion.** All 8 steps completed with no manual intervention,
  no timeouts, no errors. File saved at 13,764 bytes. This is the first validated
  end-to-end run of the longest chain variant.
- **Structural completeness.** Final document has all required blocks: `Parsed:` line,
  S-numbered claim inventory (45 claims), body with inline `[S#]` citations,
  CLAIMS TO VERIFY block, WRITER METADATA block, CITATIONS block.
- **Formatter pipeline fired at every link.** Researcher-formatter, DA-formatter,
  and Writer-formatter all executed as designed pipeline stages.
- **Internal cross-referencing.** 18 body claims, all 18 have inline S-citations.
  Zero uncited claims in the body.
- **CLAIMS TO VERIFY block present.** Fragile claims explicitly flagged for
  verification (e.g., Series C close status).

## What Didn't / Concerns

### FAIL: Inference trace preservation (`traces_to`)

The critical provenance test failed. The Data Analyzer produces inferences with
`traces_to` fields pointing to specific findings (F1, F2, etc.). These traces
did not survive to the final document.

- In the intermediate `formatted_analysis`: 15 inferences present, all 15 have
  `traces_to` fields, but **all 15 are `[narrative-mapped: uncertain]`** — no
  specific F# references.
- In the final document: zero `traces_to` markers, zero F# references. Inference
  provenance is completely absent.
- **Root cause hypothesis:** The DA produced narrative prose (not structured output),
  so the DA-formatter couldn't map inferences to specific findings. It correctly
  used `[narrative-mapped: uncertain]` as the honest fallback. But the Writer then
  dropped even that signal — the Writer has no mechanism to carry `traces_to` into
  the final document.

### FAIL: Claim-to-source traceability (URLs)

Body claims are internally cited with S-numbers, but the CITATIONS block has
**zero URLs**. Nothing traces all the way to an external source.

- CITATIONS entries contain: S-number, paraphrased claim text, `used in` section,
  confidence level.
- CITATIONS entries do NOT contain: source name, URL, tier.
- Example: `S23: "Cursor $900M at $9B, $4M to $300M ARR" → used in: Implications | confidence: medium (0.6)` — no URL.
- **Root cause hypothesis:** The Writer-formatter produces a CITATIONS block
  structured around claim usage, not source attribution. The source URLs exist
  in the `formatted_research` output (Researcher-formatter) but are not carried
  forward through the DA and Writer steps. The Writer has no instruction to map
  S-claims back to original source URLs.

### PARTIAL: Confidence level preservation

Confidence labels are preserved in CITATIONS metadata (high/medium/inference),
but the prose often upgrades medium and inference claims to definitive statements.

- Good hedging examples:
  - "reported $2B Series C at $12B pre-money not confirmed closed [S29]"
  - "Confirm Series C close... most fragile data point [S29, S35]"
- Confidence upgrade examples:
  - "Cursor ($9B with $300M ARR) and Windsurf ($3B acquisition, 700K+ users)" —
    uses S23 and S24, both medium confidence, stated as hard facts.
  - "Project Horizon... a commitment preceding proven demand [S30, S37]" —
    S37 is an inference, stated definitively.
  - "Its valuation matches peers with proven traction while disclosing none of
    the same evidence [S38]" — S38 is an inference, stated as fact.

## Confidence Accuracy

CITATIONS metadata preserves confidence labels (high/medium/inference). The
metadata layer is accurate. The prose layer is not — medium and inference
claims are frequently presented without hedging language. The confidence
signal exists in the machine-parseable output but is lost in the human-readable
prose.

## Coverage Assessment

CLAIMS TO VERIFY block fired and flagged the correct fragile claims (Series C
close status). Coverage audit appears to have run. Evidence gaps from the
original research were preserved through the DA-formatter into the analysis.

No obvious coverage misses.

## Action Items

- [ ] **Writer: carry source URLs into CITATIONS block.** Currently CITATIONS
  has S-number + claim + confidence but no source URL. The URL exists in
  `formatted_research` but is not passed through DA→Writer. Either the Writer
  needs to receive and map URLs, or the Writer-formatter needs to cross-reference
  the original research output to inject them.
- [ ] **Writer: hedge inference-backed claims in prose.** Medium and inference
  confidence claims should use hedging language ("evidence suggests", "appears to",
  "points to") rather than definitive framing. Currently the prose upgrades
  confidence silently.
- [ ] **DA-formatter: investigate why all traces_to are `narrative-mapped: uncertain`.**
  In this run, 15/15 inferences had placeholder traces instead of specific F#
  references. Is this because the DA produced narrative prose (expected for the
  `narrative` format detection path), or is the DA-formatter not attempting to
  semantically map inferences to findings? If the latter, this is a gap in the
  formatter's mapping logic.
- [ ] **Writer-formatter: preserve traces_to in CITATIONS or a separate block.**
  Even if traces_to arrives as `[narrative-mapped: uncertain]`, that signal should
  survive to the final document rather than being silently dropped. The reader
  should know which claims are inference-backed vs. directly sourced.

---

## Overall: MIXED

**Chain Reliability: PASS.** The chain completes end-to-end, all formatters fire,
structural output is correct. This validates Chain Reliability for the longest
chain variant.

**Research Trustworthiness: FAIL on provenance.** The trust promise — "every finding
traces to a source, every inference traces to a finding" — is broken at two points:
(1) inference→finding traces die between DA-formatter and Writer, and (2) claim→source
URLs die between Researcher-formatter and Writer. The final document is internally
cross-referenced but not externally traceable.

**Scorecard impact:**
- Chain Reliability: 7→8 (full chain proven end-to-end, clean handoffs)
- Research Trustworthiness: stays 4 (provenance doesn't survive to final document)
- Format Fidelity: no change (structural blocks all present)
- Overall: (4+8+7+6)/4 = 6.25 → 6
