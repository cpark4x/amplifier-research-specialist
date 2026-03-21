# QUALITY EVALUATION GAP REPORT

**Pipeline:** canvas-specialists research pipeline (researcher → formatter → analyzer → formatter → writer → formatter)
**Evaluation mode:** Competitive (all 3 competitor slots returned `null` — no comparative data available)
**Target score:** 9.0
**Topics evaluated:** 5
**Date:** 2026-03-21

---

## OVERALL SCORES

| Topic | Type | Pipeline Composite | Best Competitor | Delta |
|---|---|:---:|:---:|:---:|
| Jina AI (factual-deep-dive) | Factual | **7.67** | N/A (null) | — |
| Hybrid Productivity (strategy) | Strategy | **7.67** | N/A (null) | — |
| Retiring Abroad (survey) | Survey | **7.50** | N/A (null) | — |
| Cursor vs Copilot (competitive-comparison) | Comparison | **7.00** | N/A (null) | — |
| Wasm Security (technical-analysis) | Technical | **7.67** | N/A (null) | — |
| **Pipeline Average** | | **7.50** | **N/A** | **—** |
| **Gap to Target (9.0)** | | **−1.50** | | |

> **Competitor note:** All 15 competitor invocations (3 per topic × 5 topics) returned `null`. The competitive benchmark is uninformative. All analysis below is absolute assessment against the 1–10 rubric.

### Per-Dimension Heatmap

| Dimension | T1 Factual | T2 Strategy | T3 Survey | T4 Comparison | T5 Technical | **Avg** | **Gap to 9** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Source quality | 7 | 8 | 7 | 7 | 7 | **7.2** | −1.8 |
| Factual depth | 7 | 7 | 7 | 7 | 7 | **7.0** | −2.0 |
| Analytical insight | 8 | 8 | 7 | 7 | 8 | **7.6** | −1.4 |
| Confidence calibration | 8 | 8 | 8 | 6 | 8 | **7.6** | −1.4 |
| Structure & readability | 8 | 8 | 8 | 8 | 9 | **8.2** | −0.8 |
| Citation quality | 8 | 7 | 8 | 7 | 7 | **7.4** | −1.6 |

---

## STRUCTURAL GAPS (2+ topics)

### 1. Factual Depth — CRITICAL

- **Dimension:** Factual depth
- **Severity:** CRITICAL
- **Score:** 7 in **5/5 topics** (floor-score universality)
- **Gap to target:** −2.0 (largest single gap)
- **Topics affected:** All five

**Evidence:**

| Topic | Missing Dimensions Cited by Evaluator |
|---|---|
| Jina AI | "no latency or throughput benchmarks — a critical dimension for production embedding decisions"; "omits BGE/BAAI, Nomic, Mixedbread, and AWS Titan Embeddings" |
| Hybrid Productivity | "no coverage of sector-specific variation, team-size effects, or task-type moderators (creative vs. routine work)"; "'2.2× collaboration' stated without baseline context" |
| Retiring Abroad | "Missing entire decision dimensions: language barriers, cultural adjustment, property ownership, banking, climate, proximity to US"; "No city-level granularity"; "No retiree-profile segmentation" |
| Cursor vs Copilot | "no developer productivity benchmarks, no code-completion quality metrics, no latency or performance comparisons, no context-window or codebase-indexing depth analysis" |
| Wasm Security | "misleading kernel-CVE statistic"; limited to 7 unique sources for a deeply technical topic |

**Root cause hypothesis:** The researcher stage optimizes for **breadth of claims** (coverage across many surface dimensions) rather than **depth within dimensions** (moderators, baselines, worked examples, segment-specific data). The question-decomposition step does not generate sub-questions for performance benchmarks, dimensional moderators, or segment-specific analysis. This is a planner/researcher architectural issue, not a sourcing issue — the pipeline doesn't *know* what it's missing.

---

### 2. Source Quality — MAJOR

- **Dimension:** Source quality
- **Severity:** MAJOR
- **Score:** 7 in **4/5 topics** (T2 strategy is the sole 8)
- **Gap to target:** −1.8
- **Topics affected:** factual-deep-dive, survey, competitive-comparison, technical-analysis

**Evidence:**

| Topic | Weak Source Cited | What Primary Source Exists |
|---|---|---|
| Jina AI | `awesomeagents.ai` for pricing; `app.ailog.fr` for MTEB scores | Official vendor pricing pages; `huggingface.co/spaces/mteb/leaderboard` |
| Retiring Abroad | `getwherenext.com` blog for all healthcare scores; `401kspecialistmag.com` for SS statistics | WHO/OECD primary data; `ssa.gov` publications; official immigration authority pages |
| Cursor vs Copilot | `swimm.io` for IP indemnity; `forum.cursor.com` for legal-entitlement claim | GitHub's official legal terms; Cursor's ToS |
| Wasm Security | `softwareseni.com` (Tier 3 content-marketing blog) for 4 claims (S13–S16) | NVD for CVE data; published academic benchmarks |

**Root cause hypothesis:** The researcher stage prefers **aggregator pages** (which consolidate data into one page, reducing search-and-fetch turns) over **primary sources** (which require per-entity lookups). This is a rational optimization for context-window efficiency that systematically degrades source tier. The pipeline lacks a **source-tier validation gate** that checks whether a primary source exists before accepting a secondary/tertiary one.

---

### 3. Citation Quality — MAJOR

- **Dimension:** Citation quality
- **Severity:** MAJOR
- **Score:** 7 in **3/5 topics**
- **Gap to target:** −1.6
- **Topics affected:** strategy, competitive-comparison, technical-analysis

**Evidence:**

| Topic | Issue |
|---|---|
| Strategy | "`nbloom.people.stanford.edu/research` is a landing page, not the specific 2024 paper"; "no DOIs for the Nature or MDPI articles"; "S6 Gartner URL discusses meetings, not the attributed culture-building claim" (potential misattribution) |
| Competitive | "S16 is missing from the sequence (S15 jumps to S17) with no explanation"; "S22 URL cites $500M ARR but claim says $1B" (citation-claim mismatch); "no archive.org fallback or access-date notation" |
| Technical | "S14 inaccuracy" (misleading kernel-CVE statistic sourced from softwareseni.com); concentration risk — 4 claims from single Tier 3 source |

**Root cause hypothesis:** The formatter stage captures **base-domain or landing-page URLs** rather than resolving to specific document permalinks. No DOI-extraction step exists. No citation-claim verification step exists (i.e., checking that the cited URL actually contains the claimed data). These are three missing pipeline stages, not behavioral flaws.

---

### 4. Analytical Insight — MINOR

- **Dimension:** Analytical insight
- **Severity:** MINOR
- **Score:** 7 in **2/5 topics** (survey, competitive-comparison); 8 in remaining 3
- **Gap to target:** −1.4
- **Topics affected:** survey, competitive-comparison

**Evidence:**

| Topic | Issue |
|---|---|
| Retiring Abroad | "No decision framework. A simple 2×2 matrix, a tiered recommendation by income level, or a weighted scoring model would dramatically increase actionability"; "No contrarian analysis" |
| Cursor vs Copilot | "analysis stays at the strategic/positioning level and does not explore second-order effects, scenario modeling, or trade-off quantification"; "Next Steps are actionable but generic" |

**Root cause hypothesis:** The data-analyzer stage draws inferences **across** findings (pattern/causal/evaluative) but does not generate **decision frameworks** or **scenario models**. The writer stage does not have an explicit instruction to produce audience-specific decision aids. This gap is less severe because the pipeline scores 8 in 3/5 topics, indicating the analytical capability exists but is inconsistently activated — likely dependent on whether the research findings naturally lend themselves to cross-cutting synthesis.

---

## TOPIC NOISE (1 topic only)

### 1. Confidence Calibration — competitive-comparison (score: 6)

- **Dimension:** Confidence calibration
- **Topic:** Cursor vs Copilot (competitive-comparison)
- **Score:** 6 (vs. 8 in all other topics)
- **Evidence:** "Uniform 0.9 across all 25 non-inference claims; S22 URL cites $500M but claim says $1B; forum source (S13) rated at 0.9 for a legal-entitlement claim." Evaluator calls confidence scoring "a cosmetic layer rather than a genuine epistemic assessment."
- **Verdict:** **Warrants investigation.** While the other 4 topics score 8, the underlying tendency toward high-confidence defaults may be a latent pipeline issue that was exposed by the competitive-comparison topic's mix of volatile (pricing), legal (IP indemnity), and fast-moving (financial metrics) claims. The same static-default behavior may exist in other topics but cause less visible damage when claims happen to be genuinely high-confidence. Recommend adding a per-claim calibration pass to the formatter stage to prevent recurrence.

---

## PIPELINE STRENGTHS

### 1. Structure & Readability — Consistently Strong (avg 8.2)

Scores: 8, 8, 8, 8, **9**. The only dimension averaging above 8.0.

**Evidence across topics:**
- "Clear Summary → Key Points → Implications → Next Steps hierarchy" (all 5 topics)
- "Claims to Verify table is an excellent accountability mechanism" (T4)
- "Professional dual-audience design: the brief body serves the executive reader; the citation metadata serves the fact-checker" (T3)
- "Bold lead sentences enable scanning" (T1)
- Technical analysis topic achieved the run's highest single-dimension score (9)

**Assessment:** The writer + writer-formatter stages produce reliably well-structured output. This is a genuine pipeline advantage that would be difficult for a single-shot competitor to match.

### 2. Confidence Calibration — Strong with One Outlier (avg 7.6, mode 8)

Scores: 8, 8, 8, **6**, 8. Four of five topics demonstrate mature epistemic hygiene.

**Evidence:**
- "Per-citation confidence scores (0.3–0.9); explicit exclusion of 2 findings for weak evidence; stated evidence gaps" (T2)
- "Explicit 27/5/0/3 distribution; inferences labeled and traced to source findings; hedging language throughout" (T3)
- "Explicit separation of 14 high-confidence sourced claims, 1 medium-confidence claim, and 4 inferences at 0.6 confidence" (T1)
- Inference citations consistently trace back to finding IDs with `traces_to` references

**Assessment:** When working correctly, the pipeline's confidence calibration is its second-strongest dimension and "significantly above the standard seen in typical research outputs" (T2 evaluator). The T4 outlier is a regression, not a baseline.

### 3. Analytical Insight — Good with Upside (avg 7.6, mode 8)

Scores: 8, 8, 7, 7, 8. Three topics demonstrate genuine synthesis.

**Evidence:**
- "The market-consolidation thesis synthesizes across two independent acquisitions to derive a structural market trend" (T1)
- "The causal chain — structured schedules → norm-setting → reduced managerial ambiguity → outcome-based evaluation — is genuine synthesis, not a restatement" (T2)
- "The performance-security structural tension insight is non-obvious and high-value" (T5)

---

## RECOMMENDED ACTIONS

Prioritized by impact on closing the −1.50 gap to target score 9.0:

| Priority | Action | Addresses | Expected Impact |
|---|---|---|---|
| **1** | **Add a coverage-dimension checklist to the Planner/Researcher stage** that generates sub-questions for: performance/latency benchmarks, segment-specific analysis, dimensional moderators, and worked examples — keyed to question type (factual, strategy, survey, comparison, technical). | Factual depth (CRITICAL, −2.0 gap) | **HIGH** — would lift all 5 topics from 7→8+, adding ~1.0 to pipeline average. This is the single highest-leverage fix. |
| **2** | **Add a source-tier validation gate to the Researcher stage** that checks whether a primary source exists before accepting a secondary/tertiary aggregator. For each claim sourced from Tier 2/3, the gate should attempt one primary-source lookup (official docs, government sites, canonical databases). | Source quality (MAJOR, −1.8 gap) | **HIGH** — would lift 4/5 topics from 7→8, adding ~0.6 to pipeline average. |
| **3** | **Add a citation-resolution step to the Writer-Formatter stage** that (a) verifies each URL resolves to the specific document containing the cited claim, (b) extracts DOIs where available, (c) records access dates, and (d) flags citation-claim mismatches. | Citation quality (MAJOR, −1.6 gap) | **MEDIUM** — would lift 3/5 topics from 7→8, adding ~0.4 to pipeline average. |
| **4** | **Add a per-claim confidence calibration pass** to the Researcher-Formatter or DA-Formatter that adjusts confidence downward for: pricing claims (high temporal volatility), forum-sourced claims, single-source claims, and claims where the URL domain doesn't match the claim domain (e.g., legal claims from forums). | Confidence calibration (TOPIC NOISE, but latent risk) | **LOW-MEDIUM** — fixes the T4 outlier (6→8) and hardens all topics against regression. Adds ~0.1 to pipeline average but prevents future outliers. |
| **5** | **Add a decision-framework instruction to the Writer stage** for survey and comparison question types: produce at least one structured decision aid (matrix, tiered recommendation, or scoring model) in addition to the narrative brief. | Analytical insight (MINOR, −1.4 gap) | **LOW** — would lift 2/5 topics from 7→8. The 3 topics already at 8 suggest this is a question-type-specific gap, not a universal one. |

### Projected Impact

If Actions 1–3 are implemented and achieve the expected lift:

| Dimension | Current Avg | Projected Avg | Lift |
|---|:---:|:---:|:---:|
| Factual depth | 7.0 | 8.2 | +1.2 |
| Source quality | 7.2 | 8.0 | +0.8 |
| Citation quality | 7.4 | 8.0 | +0.6 |
| **Pipeline composite** | **7.50** | **~8.2** | **+0.7** |

Remaining gap to 9.0 after top-3 fixes: ~0.8 (addressable through Actions 4–5 and continued iteration).

---

## SUMMARY

The pipeline produces **structurally excellent, well-calibrated research briefs** (structure avg 8.2, confidence avg 7.6) but is held back by a **universal factual-depth ceiling of 7** — the single dimension that scored 7 in all five topics with zero exceptions. This is the defining structural weakness: the researcher stage optimizes for breadth of claims across surface dimensions rather than depth within them, consistently missing performance benchmarks, segment-specific analysis, and dimensional moderators regardless of topic type. Source quality (7.2 avg) and citation quality (7.4 avg) are the secondary structural gaps, both rooted in a preference for aggregator pages over primary sources and an absence of citation-verification steps. The pipeline's current composite of **7.50 is 1.50 points below the 9.0 target**; the single highest-leverage first action is **adding a coverage-dimension checklist to the Planner stage** that forces sub-question generation for depth-critical dimensions (performance data, segment analysis, moderators), which alone is projected to close ~0.7 of the 1.5-point gap.
