---
specialist: researcher-formatter
chain: "researcher → resolve-urls → researcher-formatter → data-analyzer → da-formatter → writer → writer-formatter → save"
topic: url-recovery-validation
date: 2026-03-10
quality_signal: pass
action_items_promoted: false
---

## Purpose

Validate two architectural fixes for source URL recovery in the research pipeline
(research-chain v1.7.0). These fixes target the primary Research Trustworthiness
gap identified in the full chain audit (2026-03-10-poolside-ai-full-chain-audit):
CITATIONS block had zero source URLs because the Researcher doesn't emit them.

**Research question:** "What is Poolside AI and how does it compare to other AI coding assistants?"
**Output format:** brief | **Audience:** technical decision-maker | **Voice:** executive

**Recipe session:** `ccc896e44bbf43db-20260310-235357_recipe`

---

## Fixes Validated

**Fix 1 — Researcher-Formatter URL Recovery (Stage 1.5) (`af858f6`):**
New pipeline stage in researcher-formatter spec. Three recovery patterns:
bare domain fragments, well-known publication URL patterns, company official
domains. Reconstructed URLs marked `[reconstructed]`. Falls back to `unknown`.

**Fix 2 — Pipeline URL Capture (`af858f6`):**
New `resolve-urls` step in research-chain v1.7.0 between research and
format-research. Uses `foundation:web-research` to search for verified URLs
matching source names. Produces SOURCE_URL_MAP consumed by researcher-formatter.
Defense in depth with Fix 1.

---

## Results

### Source URLs in CITATIONS: PASS

| Metric | Count |
|--------|-------|
| Total citations | 27 |
| Sourceable claims (findings) | 15 |
| Claims with real https:// URLs | **15** |
| Claims marked [reconstructed] | 0 |
| Claims with "unattributed" or "unknown" | **0** |
| Inference-type citations (traces_to instead) | 12 |

**Source URL rate for sourceable claims: 15/15 = 100%**

All 15 URLs point to plausible domains matching claim content:
- techcrunch.com (funding coverage)
- en.wikipedia.org (founding facts)
- www.poolside.ai / poolside.ai/blog (company source)
- research.contrary.com (VC research)
- www.reuters.com (Nvidia investment)
- aws.amazon.com/bedrock/poolside (AWS product page)
- press.aboutamazon.com (AWS press release)
- www.businesswire.com (PR wire)
- www.helicone.ai/blog (third-party blog)

Zero fabricated domains. URLs are unique where claims are unique, shared where
claims share a source.

### Confidence Hedging: PASS

14/14 medium + inference claims used in prose are hedged. Zero misses.

- Medium claims: `reportedly` applied consistently
- Inference claims: `Evidence suggests`, `the evidence suggests`, `appears to be`,
  `could constitute`, `may ultimately prove`
- Low claims: appropriate absence framing

Stage 3.5 audit trail documented one insertion (S23: "Evidence suggests" prepended),
confirmed present in output.

### Structural Completeness: PASS

All 9 required blocks present:
- Parsed line, S-claims header, Summary, Key Points, Implications, Next Steps
  (all with `> Sources:` attribution), CLAIMS TO VERIFY, WRITER METADATA, CITATIONS

Minor: formatter reasoning preamble (lines 1-11) leaks into output file.
Cosmetic, not structural.

### Inference traces_to: EXPECTED LIMITATION

12/12 inference citations have `type: inference` and `traces_to:` fields
(structural PASS). All 12 values are `[narrative-mapped: uncertain]`
(semantic limitation — upstream DA-formatter issue, not in scope of URL fixes).

---

## Comparison with Previous Runs

| Criterion | Run 1 (pre-fix) | Run 2 (hedging only) | Run 3 (URL recovery) |
|-----------|-----------------|---------------------|---------------------|
| Source URLs | 0/50 (FAIL) | 0/50 (FAIL) | **15/15 (PASS)** |
| Confidence hedging | 0% hedged (FAIL) | 100% hedged (PASS) | **100% hedged (PASS)** |
| Structural blocks | PASS | PASS | **PASS** |
| Inference traces_to | all placeholders | all placeholders | all placeholders |

---

## Action Items

- [ ] **Strip formatter reasoning preamble from output.** Lines 1-11 contain
  "Now I have the full spec..." reasoning that leaks into the saved file.
  Minor cosmetic issue — could be handled by the save step or a post-processing
  rule in the writer-formatter.
- [ ] **Validate on 2+ additional diverse topics.** URL recovery validated on
  1 topic (Poolside AI). Rubric requires 5+ topics for Research Trustworthiness
  6+. Next validation runs should use different domains (non-tech, non-company).

---

## Scorecard Impact

- **Research Trustworthiness: 4→5.** Source URLs now present (15/15). Confidence
  hedging validated. Architecture correct and validated on 1 topic. Rubric 3-5:
  "Architecture correct, some validation. Most claims rated, URLs present, gaps
  disclosed. Not validated across diverse topics." — solidly at 5 now.
- **Chain Reliability: stays 8.** 9-step chain completed cleanly.
- **Format Fidelity: stays 7.** No change in format validation scope.
- **Specialist Coverage: stays 6.** No new specialists.
- **Overall: (5+8+7+6)/4 = 6.5 → 7/10.** Up from 6.
