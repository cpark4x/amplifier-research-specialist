# QUALITY EVALUATION GAP REPORT

**Evaluation Date:** 2026-03-21
**Topics Evaluated:** 5
**Target Score:** 9.0
**Evaluation Mode:** Competitive (all competitor outputs null — absolute scoring only)

---

## OVERALL SCORES

| Topic | Pipeline Score | Best Competitor | Delta | Gap to 9.0 |
|---|:---:|:---:|:---:|:---:|
| factual-deep-dive (Jina AI) | 7.67 | N/A | — | −1.33 |
| strategy (Hybrid Teams) | 8.00 | N/A | — | −1.00 |
| survey (Retire Abroad) | 7.17 | N/A | — | −1.83 |
| competitive-comparison (Cursor vs Copilot) | 7.00 | N/A | — | −2.00 |
| technical-analysis (Wasm Security) | 8.17 | N/A | — | −0.83 |
| **Cross-Topic Average** | **7.60** | **N/A** | **—** | **−1.40** |

> **Note:** All 15 competitor slots (3 per topic × 5 topics) returned `null`. No competitive delta can be computed. All gap analysis is against the absolute rubric ceiling and the 9.0 target. This is itself a structural evaluation infrastructure issue — see Recommended Actions.

### Per-Dimension Cross-Topic Breakdown

| Dimension | factual-deep-dive | strategy | survey | competitive-comparison | technical-analysis | **Avg** | **Gap to 9** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Source quality | 7 | 7 | 6 | 6 | 8 | **6.8** | **−2.2** |
| Factual depth | 8 | 7 | 7 | 7 | 8 | **7.4** | **−1.6** |
| Analytical insight | 7 | 8 | 7 | 8 | 9 | **7.8** | **−1.2** |
| Confidence calibration | 8 | 9 | 8 | 8 | 9 | **8.4** | **−0.6** |
| Structure & readability | 9 | 9 | 8 | 8 | 8 | **8.4** | **−0.6** |
| Citation quality | 7 | 8 | 7 | 5 | 7 | **6.8** | **−2.2** |

The two largest drags on the pipeline average are **Source quality (6.8)** and **Citation quality (6.8)**, each 2.2 points below target. Together they account for ~52% of the total gap to 9.0.

---

## STRUCTURAL GAPS (2+ topics)

### 1. Source Quality — CRITICAL

- **Dimension average:** 6.8/10
- **Topics affected:** 5/5 (scores: 6, 6, 7, 7, 8)
- **Below 7 in:** survey (6), competitive-comparison (6)
- **At exactly 7 in:** factual-deep-dive, strategy

**Evidence:**

- **survey:** *"4 of 10 sources are commercial blogs (AIHR, Tango Analytics, Worklytics, Gable.to) with unclear methodology. No meta-analyses, no organizational psychology journals beyond Nature."* Source concentration: 6 of 22 claims from a single site (expatsi.com).
- **competitive-comparison:** *"Zero references to Gartner, Forrester, IDC, or similar analyst coverage… 10 of 13 sources are blogs or product pages. No developer surveys (Stack Overflow, JetBrains), no academic papers, no conference talks."*
- **factual-deep-dive:** *"Two claims (S21, S23) are listed as 'unattributed'… competitor benchmark data relies on awesomeagents.ai, a low-tier aggregator rather than primary MTEB leaderboard data."*
- **strategy:** *"The tail of the source distribution includes commercial blogs of uncertain methodology… missing entirely are longitudinal studies, meta-analyses, and peer-reviewed organizational psychology journals beyond the single Nature paper."*

**Root cause hypothesis:** The research stage prioritizes web-accessible, freely available sources and does not enforce a minimum source-tier diversity gate. Blog and aggregator sources are easier to retrieve than gated academic databases, analyst reports, or government statistical tables. The pipeline lacks a hard constraint like "≥N claims must originate from primary/institutional sources."

---

### 2. Citation Quality — CRITICAL

- **Dimension average:** 6.8/10
- **Topics affected:** 4/5 below 8 (scores: 5, 7, 7, 7, 8)
- **Below 7 in:** competitive-comparison (5)

**Evidence:**

- **competitive-comparison:** *"The METR study is referenced three times in the body but is absent from the citation table… No inline citations. The body text makes specific factual claims without linking to which of the 13 sources supports each."* Also: *"No access dates… Missing key canonical sources."*
- **factual-deep-dive:** *"S21 and S23 are 'unattributed' — these make competitive claims without any URL or source… S11's URL appears to be the wrong page… S14 and S15 cite awesomeagents.ai for competitor benchmark numbers rather than vendor documentation."*
- **survey:** *"S14 cites the FBAR page for a worldwide-taxation claim — the IRS page on citizen taxation obligations would be more precisely aligned… several claims trace to the same source (expatsi.com accounts for 6 of 22 claims), creating concentration risk that isn't flagged."*
- **technical-analysis:** *"Six claims (S15, S16, S18, S19, S20, S25) all cite the same URL — a secondary survey paper — rather than their original publications. No DOI links for any academic paper."*

**Root cause hypothesis:** The pipeline treats citation assembly as a post-hoc formatting step rather than tracking source-to-claim linkage during the research phase. The researcher collects findings efficiently (sometimes through survey papers or aggregators) but doesn't resolve back to primary publication URLs. The writer-formatter catches structural issues but cannot retroactively inject missing URLs or inline references. The pipeline has no citation-completeness gate between the research and analysis stages.

---

### 3. Factual Depth — MAJOR

- **Dimension average:** 7.4/10
- **Topics affected:** 3/5 at exactly 7 (strategy, survey, competitive-comparison)

**Evidence:**

- **strategy:** *"Several important dimensions are absent: technology and tooling, cultural and geographic variation, industry-specific evidence, and financial ROI modeling."*
- **survey:** *"63 of 81 source findings went unused — a 22% utilization rate. Major topical gaps self-identified: healthcare quality/access; effective tax-rate modeling; cost-of-living trend data; visa processing timelines."*
- **competitive-comparison:** *"No benchmark data (HumanEval, SWE-bench, MBPP), no completion accuracy comparisons, no latency measurements… Developer adoption metrics missing."*

**Root cause hypothesis:** The research stage achieves adequate breadth on the primary question but does not probe adjacent literatures or secondary dimensions systematically. The pipeline likely issues searches derived directly from the research question surface rather than expanding into adjacent domains (e.g., "distributed team tooling" for hybrid work, "SWE-bench cursor" for the coding comparison). The brief format's word budget (~400 words) then forces heavy triage, but the upstream finding set is already missing key dimensions before triage occurs.

---

### 4. Analytical Insight — MINOR

- **Dimension average:** 7.8/10
- **Topics affected:** 2/5 at 7 (factual-deep-dive, survey)

**Evidence:**

- **factual-deep-dive:** *"The analysis stays close to Jina's own framing. There is no adversarial analysis (e.g., what happens if OpenAI or Google releases a similarly efficient model? What are the risks of the Elastic acquisition for existing API users?)."*
- **survey:** *"S22 (trend acceleration) is weakly supported — extrapolating from an 8-year growth trend to predict 3–5 year acceleration requires more evidence… The analysis would benefit from scenario modeling and explicit decision matrices."*

**Root cause hypothesis:** The data-analyzer stage draws inferences from available findings but does not systematically generate adversarial or counterfactual questions. The inference protocol rewards well-supported pattern recognition but doesn't prompt for "what could undermine this conclusion?" or "what would a skeptic ask?" This produces sound but non-adversarial analysis.

---

## TOPIC NOISE (1 topic only)

### 1. Citation Quality = 5 in competitive-comparison

- **Dimension:** Citation quality
- **Topic:** competitive-comparison (Cursor vs Copilot)
- **Evidence:** The METR randomized controlled trial — the output's most distinctive independent evidence — was cited three times in the body but entirely absent from the citation table. Zero inline source-to-claim linkage existed anywhere in the document. This dropped citation quality 2 points below the structural baseline (~7).
- **Verdict:** **Warrants investigation, but partially structural.** The 5 is an amplification of the structural citation weakness, not pure noise. The specific trigger was that the writer stage produced a longer-than-typical document (~1,800 words vs ~400) which exposed the lack of inline citation tracking more severely. The pipeline's citation weakness is structural (see above); the severity at 5 is topic-specific due to document length and the METR omission.

### 2. Source Quality = 8 in technical-analysis (outlier high)

- **Dimension:** Source quality
- **Topic:** technical-analysis (WebAssembly security)
- **Evidence:** This was the only topic to score 8, driven by "official specifications (webassembly.org), primary runtime documentation and security advisories (Wasmtime, Node.js), peer-reviewed academic research including a USENIX Security Distinguished Paper, and a comprehensive 121-paper survey."
- **Verdict:** **Likely topic-specific advantage, not generalizable.** The WebAssembly security domain has an unusually concentrated, high-quality primary source ecosystem (CVE advisories, spec documents, peer-reviewed security papers). The research stage performed well when authoritative sources were readily web-accessible. This confirms the root cause hypothesis for the structural source-quality gap: the pipeline succeeds when primary sources are freely available online and struggles when they are gated or require domain-specific search strategies.

---

## PIPELINE STRENGTHS

### 1. Confidence Calibration — Consistently Excellent

- **Scores:** 8, 9, 8, 8, 9 → **Average: 8.4**
- **Gap to 9.0:** only −0.6
- **Appears in 5/5 topics as a top-2 dimension**

**Evidence:**

- **strategy (9):** *"The 18-row claims-to-verify table is an extraordinary accountability mechanism rarely seen in research briefs. Per-citation confidence scoring (0.6–0.9), explicit inference labeling with traces_to provenance, and calibrated hedging language create a multi-layered epistemic honesty system."*
- **technical-analysis (9):** *"Every claim carries an explicit confidence tag (high/medium/inference) — this is rare and valuable. The three inferences are clearly labeled as such and include traces_to fields linking back to supporting evidence."*
- **competitive-comparison (8):** *"Inclusion of the METR study — which actively undermines the value proposition of both tools — signals intellectual honesty over advocacy."*

This is the pipeline's most distinctive capability. No evaluator across any topic questioned the calibration methodology itself — only edge cases of specific ratings.

### 2. Structure & Readability — Consistently Strong

- **Scores:** 9, 9, 8, 8, 8 → **Average: 8.4**
- **Gap to 9.0:** only −0.6

**Evidence:**

- **factual-deep-dive (9):** *"Summary → Key Points → Implications → Next Steps → Claims to Verify → Citations → Writer Metadata. Each section serves a distinct function."*
- **strategy (9):** *"Purpose-built for a 'technical decision-maker' audience. Bold lead sentences, inline S# references, and blockquote source summaries enable both scanning and deep reading."*
- **competitive-comparison (8):** *"The BLUF → Architecture → Capabilities → Pricing → Enterprise → Risks → Decision → Limitations flow is logical and complete. Four comparison tables enable rapid scanning."*

The pipeline's output format and information architecture are production-ready. The 8s (vs 9s) in three topics correlate with minor structural suggestions (missing threat model framing, long back-matter, missing visual summaries) rather than fundamental format problems.

---

## RECOMMENDED ACTIONS

Prioritized by impact on closing the 1.40-point gap to target 9.0:

### 1. Add a Source-Tier Diversity Gate to the Research Stage — CRITICAL

**Addresses:** Source quality (−2.2 gap), cascading improvement to Citation quality and Factual depth
**Expected impact:** HIGH (+1.0 to +1.5 points on Source quality; +0.5 cascade to Citation quality)

Implement a hard constraint in the researcher specialist: before research is declared complete, enforce a minimum distribution such as ≥3 claims from government/institutional primary sources, ≥2 from peer-reviewed or analyst sources, and flag any single source contributing >25% of total claims. This forces the research stage to diversify beyond web blogs without requiring access to gated databases — it simply requires the researcher to search more specifically for authoritative sources.

### 2. Implement Source-to-Claim Linkage During Research (not post-hoc) — CRITICAL

**Addresses:** Citation quality (−2.2 gap)
**Expected impact:** HIGH (+1.5 to +2.0 points on Citation quality for worst-case topics)

Require the researcher to produce inline claim→URL mappings at collection time. The writer-formatter currently assembles citations after the fact, which means unreferenced sources (like the METR study) and misaligned URLs (like the FBAR page) propagate uncaught. Adding a citation-completeness validation step between research-formatter and data-analyzer — checking that every finding has a resolvable, claim-aligned URL and that no body reference lacks a citation table entry — would catch the most damaging citation failures.

### 3. Add Adjacent-Domain Search Expansion to the Research Stage — MAJOR

**Addresses:** Factual depth (−1.6 gap)
**Expected impact:** MEDIUM (+0.5 to +1.0 on Factual depth)

After the initial research pass, add a structured "what dimensions are missing?" self-check that generates 2–3 adjacent-domain search queries. For example: the hybrid-work topic would trigger "distributed team tooling productivity" and "remote work ROI meta-analysis"; the Cursor comparison would trigger "SWE-bench cursor copilot" and "AI coding tools developer survey 2025." This addresses the root cause of the depth gap: the pipeline explores the question surface but not its periphery.

### 4. Add Adversarial Inference Prompting to the Analysis Stage — MINOR

**Addresses:** Analytical insight (−1.2 gap)
**Expected impact:** LOW-MEDIUM (+0.5 on Analytical insight)

After the data-analyzer draws its inferences, add a mandatory adversarial pass: "For each inference, state the strongest counterargument or the condition under which it would be false." This would have caught the Jina evaluator's complaint about missing competitive risk analysis and the survey evaluator's concern about unsupported trend extrapolation. Low implementation cost, moderate quality uplift.

### 5. Fix Competitor Evaluation Infrastructure — OPERATIONAL

**Addresses:** Inability to compute competitive delta (all 15 competitor slots returned null)
**Expected impact:** HIGH for evaluation validity (no score impact, but enables the competitive evaluation mode to function)

The entire competitive evaluation layer produced no data. Every competitor result across all 5 topics was `null`. This means the "competitive" evaluation mode operated as absolute-only scoring, and no gap analysis against actual competitor outputs was possible. Diagnose and fix the competitor agent dispatch mechanism before the next evaluation cycle — without it, the evaluation cannot validate whether pipeline scores reflect genuine quality or merely the absence of a baseline.

---

## SUMMARY

The pipeline produces well-structured, epistemically honest research briefs (confidence calibration: 8.4, structure: 8.4) but is held back by two critical structural weaknesses: **source-tier diversity (6.8 avg)** and **citation completeness (6.8 avg)**, which together account for over half the 1.40-point gap to the 9.0 target. These weaknesses appeared in 4–5 of 5 topics, confirming they are pipeline-level defects rather than topic-specific noise. The single highest-priority action is **adding a source-tier diversity gate to the research stage** — enforcing minimum primary/institutional source counts before research is declared complete — which would lift Source quality, cascade improvements into Citation quality and Factual depth, and is estimated to close 0.5–0.7 points of the overall 1.40-point gap with a single intervention.
