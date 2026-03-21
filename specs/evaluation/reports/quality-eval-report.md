# QUALITY EVALUATION GAP REPORT

## OVERALL SCORES

| Topic | Topic ID | Pipeline Composite | Best Competitor | Delta |
|---|---|:---:|:---:|:---:|
| Jina AI Embedding Provider Comparison | factual-deep-dive | **1.0** ⚠️ | N/A (null) | — |
| Hybrid Team Productivity Strategies | strategy | **7.7** | N/A (null) | — |
| Best Places to Retire Abroad | survey | **7.3** | N/A (null) | — |
| Cursor vs. GitHub Copilot Workspace | competitive-comparison | **6.7** | N/A (null) | — |
| WebAssembly Security Outside Browser | technical-analysis | **8.2** | N/A (null) | — |

**Pipeline average (all 5 topics):** 6.18
**Pipeline average (4 scorable topics, excluding infrastructure failure):** 7.48
**Best competitor average:** N/A — all 15 competitor runs returned `null`
**Delta:** Not computable (no competitor baselines)
**Gap to target (scorable only):** 9.0 − 7.48 = **1.52 points**
**Gap to target (all 5):** 9.0 − 6.18 = **2.82 points**

> ⚠️ **Topic 1 (factual-deep-dive) is an infrastructure failure**, not a content quality result. The pipeline ran all 7 steps successfully (per `pipeline_run_result`), but `pipeline_output` captured the integer `[1]` — a serialization artifact — instead of research content. The evaluator correctly scored this 1/10 on all dimensions since it received no content. All subsequent analysis uses the **4 scorable topics** unless otherwise noted.

> ⚠️ **All 15 competitor runs returned `null`** across all 5 topics. No competitive comparison is possible. Scores below are absolute quality assessments against the 1–10 rubric.

---

### Per-Dimension Averages (4 Scorable Topics)

| Dimension | Strategy | Survey | Comp. Comparison | Tech Analysis | **Mean** | **Gap to 9.0** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| 1. Source quality | 7 | 7 | 5 | 8 | **6.75** | **−2.25** |
| 2. Factual depth | 7 | 6 | 6 | 8 | **6.75** | **−2.25** |
| 3. Analytical insight | 8 | 7 | 7 | 9 | **7.75** | **−1.25** |
| 4. Confidence calibration | 7 | 8 | 8 | 7 | **7.50** | **−1.50** |
| 5. Structure & readability | 9 | 8 | 7 | 9 | **8.25** | **−0.75** |
| 6. Citation quality | 8 | 8 | 7 | 8 | **7.75** | **−1.25** |

---

## STRUCTURAL GAPS (2+ topics)

### CRITICAL-1: Competitor Evaluation Harness Failure

- **Severity:** CRITICAL (INFRASTRUCTURE)
- **Topics affected:** All 5/5
- **Evidence:** All 15 competitor slots (`anthropic-claude`, `google-gemini`, `openai-gpt4o`) returned `null` across every topic. Every per-topic evaluator noted: *"All three competitor results returned null"*; *"No comparative conclusions are possible."*
- **Root cause hypothesis:** The competitor delegate runs were either not configured, not executed, or their results were not captured by the evaluation harness. This is an orchestration/recipe infrastructure defect — the `competitor_results` array is never populated regardless of topic, indicating the failure is in the harness, not in any individual competitor.
- **Impact:** The entire competitive evaluation mode is non-functional. No gap analysis, no competitive wins, and no delta computation is possible. This renders the "competitive" evaluation mode equivalent to absolute-only scoring.

### CRITICAL-2: Pipeline Output Capture Failure

- **Severity:** CRITICAL (INFRASTRUCTURE)
- **Topics affected:** 1/5 (factual-deep-dive), but systemic risk applies to all topics
- **Evidence:** The `pipeline_run_result` describes a successful 7-step execution (15 turns, 62 findings, 4 inferences, file saved at 10,122 bytes), yet `pipeline_output` contains `[1]` — a bare integer array. The evaluator stated: *"The output is the bare integer 1 — it contains zero research content. The pipeline likely failed silently, returned a status code or step count instead of research content."*
- **Root cause hypothesis:** The output extraction step captured a return value, step count, or status code rather than the actual research document. The `pipeline_output` field was serialized from a non-content object. This may be an intermittent serialization bug since 4/5 topics captured output correctly.
- **Impact:** 20% output loss rate. Even one occurrence means the pipeline cannot be trusted to reliably deliver results without a post-capture validation gate.

### MAJOR-1: Source Quality (Dimension 1)

- **Severity:** MAJOR
- **Dimension mean:** 6.75 / 10 (gap to 9.0: −2.25)
- **Topics affected:** 4/4 scorable topics (3/4 below 8, 1/4 at 5)
- **Evidence:**
  - **Strategy (7):** *"Total source count (5) is narrow for a comprehensive topic. Absent: major consulting firm research (McKinsey, Deloitte, BCG), academic management journals, technology company workplace research (Microsoft Work Trend Index)."*
  - **Survey (7):** *"No academic, statistical, or intergovernmental sources (WHO, OECD, Numbeo, World Bank). Cost-of-living claims lean heavily on a single specialist publisher (International Living provides 5 of 23 claims)."*
  - **Competitive-comparison (5):** *"4 of 16 sources are from aitooldiscovery.com (an SEO aggregator). No analyst reports, no empirical studies, no tier-1 trade press primary reporting. Reddit sentiment is cited via intermediary."*
  - **Technical-analysis (8):** *"S16 attributed to a personal blog (wingolog.org). S8 cites arXiv preprint. No vendor-neutral industry reports (NIST, CISA, ENISA)."*
- **Root cause hypothesis:** The researcher stage accepts whatever web search results are ranked by SEO without a source-tier diversity gate. There is no minimum representation requirement for primary sources, peer-reviewed research, or institutional reports. The researcher optimizes for claim volume, not source authority distribution.

### MAJOR-2: Factual Depth (Dimension 2)

- **Severity:** MAJOR
- **Dimension mean:** 6.75 / 10 (gap to 9.0: −2.25)
- **Topics affected:** 4/4 scorable topics (2/4 at 6, 1/4 at 7, 1/4 at 8)
- **Evidence:**
  - **Strategy (7):** *"No coverage of technology infrastructure (async tooling, meeting load, platform fatigue), proximity bias and equity/inclusion effects, industry- or function-specific variation."*
  - **Survey (6):** *"Healthcare quality, safety/crime statistics, climate, language barriers, cultural adjustment, housing markets, banking access absent. Only 3 of 10 ranked countries get visa details."*
  - **Competitive-comparison (6):** *"No security/compliance features, enterprise deployment models, context window sizes, supported languages, latency metrics, debugging/testing workflow support, offline functionality."*
  - **Technical-analysis (8):** *"Supply chain security mentioned but zero sourced claims. Comparison with alternative isolation (containers, microVMs) absent. Networking/I/O attack surface not addressed."*
- **Root cause hypothesis:** The researcher synthesizes from available search results rather than working from a predetermined comparison framework or coverage checklist for the topic type. No "dimensions coverage" gate verifies all material axes are addressed before proceeding to analysis. Good depth within covered scope, but systematically narrow aperture.

### MAJOR-3: Confidence Calibration (Dimension 4)

- **Severity:** MAJOR
- **Dimension mean:** 7.50 / 10 (gap to 9.0: −1.50)
- **Topics affected:** 4/4 scorable topics (2/4 at 7, 2/4 at 8)
- **Evidence:**
  - **Strategy (7):** *"The Nature RCT was conducted at a single company (Trip.com) — the brief presents its findings with high confidence and no generalizability caveat. Gallup claims receive 0.9 but its methodology (online panel surveys) has known limitations."*
  - **Survey (8):** *"The 0.9 confidence assigned to International Living claims (S1, S2, S7–S9) may be slightly generous — IL is an advocacy publication with commercial interests."*
  - **Competitive-comparison (8):** *"Some 'high (0.9)' ratings seem generous for sources like the-decoder.com reporting financial figures without SEC filings."*
  - **Technical-analysis (7):** *"Uniform 0.9 floor regardless of source tier; uniform 0.6 for all inferences despite varying evidence strength. No uncertainty language surfaces in the prose."*
- **Root cause hypothesis:** The confidence assignment uses a binary heuristic: sourced → 0.9, inference → 0.6. There is no per-claim evaluation of evidence quality, source authority, methodological rigor, or generalizability. The writer stage does not consume confidence metadata to modulate hedging language in prose. This creates a disconnect between the metadata's precision and the brief's rhetorical certainty.

### MINOR-1: Analytical Insight — Quantification Weakness (Dimension 3)

- **Severity:** MINOR
- **Dimension mean:** 7.75 / 10 (gap to 9.0: −1.25)
- **Topics affected:** 2/4 topics below 8 (survey: 7, competitive-comparison: 7)
- **Evidence:**
  - **Survey (7):** *"I1 asserts costs are 'materially understated' but provides no estimate of the understatement. Private health insurance (~€200–€400/month) and tax prep fees (~$500–$2,000/year) are readily estimable."*
  - **Competitive-comparison (7):** *"The analysis doesn't model scenarios (what if Cursor adds JetBrains support?), doesn't address team/org-level adoption dynamics, and the Implications section is only one paragraph."*
  - **Strategy (8) and Technical-analysis (9):** Both scored well; qualitative synthesis is strong.
- **Root cause hypothesis:** The data-analyzer stage synthesizes themes but does not perform second-order research to quantify the gaps it identifies. It detects the *existence* of patterns but stops short of *sizing* them. The pipeline reliably produces "what" insights but inconsistently produces "how much" insights.

---

## TOPIC NOISE (1 topic only)

### Structure & Readability Below 8 — Competitive-Comparison Only

- **Dimension:** Structure & readability (scored 7 in competitive-comparison; 8–9 in all others)
- **Topic:** competitive-comparison
- **Evidence:** *"No structured feature-comparison table (the most expected artifact in a product comparison). The 'Key Points' section mixes factual claims with sentiment and financial data without sub-grouping."*
- **Verdict:** **Warrants investigation.** Product comparisons have a genre-specific structural expectation (comparison matrix/table) that the writer template doesn't accommodate. This may indicate the pipeline needs topic-type-aware output formatting, or it may resolve if factual depth improves (more data → natural tabular structure).

### Citation Quality Below 8 — Competitive-Comparison Only

- **Dimension:** Citation quality (scored 7 in competitive-comparison; 8 in all others)
- **Topic:** competitive-comparison
- **Evidence:** *"Several URLs point to aggregator intermediaries rather than primary sources. Gap between '45 sourced findings' claimed and 21 citations shown in the table suggests findings were consolidated — mapping not fully transparent."*
- **Verdict:** **Likely noise, downstream of source quality.** If source quality improves (MAJOR-1), citation quality will improve as a consequence. The finding-to-citation consolidation transparency issue is minor and topic-specific.

### Source Quality at 5 — Competitive-Comparison Only (Severity Outlier)

- **Dimension:** Source quality (scored 5; nearest other topic scored 7)
- **Topic:** competitive-comparison
- **Evidence:** *"4 of 16 sources from aitooldiscovery.com (an SEO aggregator). No analyst reports, no empirical studies, no tier-1 trade press."*
- **Verdict:** **Warrants investigation.** The 2-point gap below the next-worst topic (7) suggests competitive-comparison topics are particularly vulnerable to SEO-optimized aggregator content dominating search results. The source-tier diversity gate (MAJOR-1 fix) should address this, but competitive-comparison may need an additional heuristic to de-weight aggregator sources.

---

## PIPELINE STRENGTHS

| Dimension | Mean | Evidence |
|---|:---:|---|
| **Structure & readability** | **8.25** | Consistently the highest-scoring dimension. Two topics scored 9/10. The Summary→Key Points→Implications→Next Steps flow, inline citation tags, bold scanning aids, and per-section source attribution blocks were praised across all evaluations. *"Matches executive audience specification precisely"* (strategy). *"The metadata block enables downstream automation"* (tech-analysis). |
| **Analytical insight (qualitative)** | **7.75** | The pipeline's inferences are consistently rated as genuinely additive and non-obvious. Tech-analysis's "security inversion" concept scored 9/10: *"a genuinely original synthesis — it reframes Wasm security as a tradeoff rather than a binary safe/unsafe assessment"*. Strategy's "leader bottleneck paradox" and "coordination hierarchy" were called *"original analytical contributions not found in any single source."* |
| **Citation quality** | **7.75** | S-numbered claim inventories, per-claim confidence scores, section-placement mapping, `traces_to` inference traceability, and "Claims to Verify" sections were praised in every evaluation. *"This level of citation metadata is uncommon even in professional research outputs"* (strategy). *"Systematic ID scheme with inference traceability"* (competitive-comparison). |
| **Inference traceability** | **N/A (unscored)** | Noted as a distinguishing capability across all 4 topics. Every inference includes explicit `traces_to` chains mapping to supporting claims. *"Rare in research outputs"* (tech-analysis). This is a unique pipeline differentiator that competitors would struggle to match. |

---

## RECOMMENDED ACTIONS

Prioritized by impact (critical infrastructure first, then structural content gaps):

| # | Action | Addresses | Expected Impact |
|---|---|---|:---:|
| **1** | **Fix competitor evaluation harness** — debug why all 15 competitor delegate runs return `null`. Validate competitor agent/provider/model configuration, ensure results are captured and serialized. Add a pre-evaluation gate that aborts scoring if <1 competitor produces output. | CRITICAL-1 | **HIGH** — Restores the entire competitive evaluation mode. Without this, the "competitive" recipe is absolute-only scoring disguised as comparative. |
| **2** | **Add pipeline output validation gate** — before the evaluate step, verify `pipeline_output` is non-empty well-formed text (not a status code, integer, or empty array). Reject and re-extract if validation fails. | CRITICAL-2 | **HIGH** — Prevents 20% output loss. Simple guard, high reliability payoff. |
| **3** | **Implement source-tier diversity gate in researcher** — require minimum representation: ≥1 primary/institutional source, ≥1 peer-reviewed or empirical source, and reject or down-weight SEO aggregator intermediaries. The recent commit `ad1d3d8` ("add source-tier diversity gate") may already address this; verify it is active and enforced. | MAJOR-1 (Source quality, mean 6.75) | **HIGH** — Directly lifts the weakest content dimension. Evaluators across 3/4 topics named this as their #1 improvement. Expected lift: +1.0–1.5 points on source quality, with cascading improvements to factual depth and confidence calibration. |
| **4** | **Add topic-type coverage checklist to researcher** — for each research type (survey, comparison, technical-analysis, strategy), define required coverage dimensions (e.g., "comparison" requires: features, pricing, security, enterprise, ecosystem). Gate research output against the checklist before proceeding to analysis. | MAJOR-2 (Factual depth, mean 6.75) | **HIGH** — Prevents the "deep but narrow" pattern. Expected lift: +1.0–1.5 points on factual depth. |
| **5** | **Implement source-tier-aware confidence scoring** — replace the binary heuristic (sourced→0.9, inference→0.6) with a graduated model: peer-reviewed→0.9, government/institutional→0.85, established press→0.75, blog/aggregator→0.6, inference→variable by chain strength. Have the writer stage surface hedging language for claims below 0.8. | MAJOR-3 (Confidence calibration, mean 7.50) | **MEDIUM** — Closes the gap between metadata precision and rhetorical certainty. Expected lift: +0.5–1.0 points on confidence calibration. |
| **6** | **Add quantification pass to data-analyzer** — when an inference identifies a gap or hidden cost, attempt to size it (even as a range) using available evidence or flagging it as "quantification needed" in the evidence gaps. | MINOR-1 (Analytical insight quantification) | **MEDIUM** — Transforms "what" insights into "how much" insights. Expected lift: +0.5 points on analytical insight in weaker topics. |
| **7** | **Add topic-type-aware output templates** — for "comparison" research types, the writer should produce a structured comparison matrix alongside the narrative brief. | Topic noise (structure in comparisons) | **LOW** — Addresses a genre-specific expectation. Only affects comparison-type topics. |

---

## SUMMARY

The pipeline produces analytically strong, well-structured research briefs (content composite: **7.48/10** across 4 scorable topics) with standout capabilities in structure & readability (8.25), analytical inference (7.75), and citation traceability. However, **two critical infrastructure failures prevent the evaluation from functioning as designed**: the competitor harness returned `null` for all 15 competitor runs (making competitive comparison impossible), and one topic's output was lost to a serialization bug. The **gap to the 9.0 target is 1.52 points** on content quality alone, driven primarily by two co-equal structural weaknesses: **source quality (6.75)** and **factual depth (6.75)** — both stemming from the researcher's reliance on unfiltered web search results without diversity gates or coverage checklists. The single highest-priority first action is **fixing the competitor evaluation harness** (without competitive baselines, the quality loop cannot measure progress), followed immediately by **enforcing the source-tier diversity gate** already committed at `ad1d3d8` — if functional, this one change is expected to lift the composite by 0.5–0.75 points through cascading improvements across source quality, factual depth, and confidence calibration.