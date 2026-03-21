# QUALITY EVALUATION GAP REPORT

**Pipeline:** canvas-specialists research pipeline (6-step: researcher → formatter → analyzer → DA-formatter → writer → writer-formatter)
**Evaluation mode:** Competitive (vs. Claude Sonnet, Gemini 2.5 Pro, GPT-4o)
**Topics evaluated:** 3 (factual-deep-dive, strategy, survey)
**Target score:** 8.0 / 10.0

---

## OVERALL SCORES

| Topic | Topic ID | Pipeline Score | Best Competitor | Best Comp Score | Delta |
|---|---|:---:|---|:---:|:---:|
| Jina AI & Embedding Providers | factual-deep-dive | **8.33** | C2 (Gemini) | 7.50 | **+0.83** |
| Hybrid Team Productivity | strategy | **8.67** | C2 (Gemini) | 7.50 | **+1.17** |
| Best Places to Retire Abroad | survey | **7.17** | C3 (GPT-4o) | 7.50 | **−0.33** |
| **AVERAGE** | | **8.06** | | **7.50** | **+0.56** |

**Gap to target:** 8.0 − 8.06 = **−0.06** (pipeline meets target by a hair)

**Per-dimension pipeline averages (across 3 topics):**

| Dimension | Avg Score | Trend |
|---|:---:|---|
| Source quality | 7.00 | Weakest dimension |
| Factual depth | 7.33 | Second weakest |
| Analytical insight | 8.67 | Consistent strength |
| Confidence calibration | 9.00 | Dominant strength |
| Structure & readability | 7.67 | Adequate |
| Citation quality | 8.67 | Consistent strength |

---

## STRUCTURAL GAPS (2+ topics)

### Gap 1: Factual Depth

| Field | Value |
|---|---|
| **Dimension** | Factual depth |
| **Severity** | **MAJOR** |
| **Topics affected** | 2/3 — factual-deep-dive (7 vs 9), survey (6 vs 9) |
| **Pipeline avg** | 7.33 |
| **Best competitor avg** | 8.67 |
| **Deficit** | −1.33 avg, with individual gaps of −2 and −3 |

**Evidence:**

*Topic 1 (Jina AI):* "C1 covers material the pipeline omits entirely: model evolution v1→v5, Agentset ELO leaderboard data, deployment ecosystem (AWS SageMaker, Azure, GCP; 10+ vector store integrations), SOC 2 certification, research publication record (ICLR 2026, NeurIPS, ICML)." — Evaluator notes the pipeline's brief format limits factual breadth.

*Topic 3 (Retirement):* "The pipeline names the IL Top 10 but provides substantive cost, visa, and healthcare data for only ~6 countries. Competitor 3 provides structured profiles for 20+ countries." Additionally: "Uses the 2025 International Living index. Competitor 3 uses the 2026 index, which shows Greece displacing Panama as #1." Critical missing facts include Medicare non-coverage abroad, Portugal's NHR termination, and FEIE/FTC/FATCA thresholds.

*Topic 2 (Hybrid):* No gap — pipeline scored 9 (highest). This topic had a narrower, more focused scope where deep-not-broad research sufficed.

**Root cause hypothesis:** The pipeline's research phase terminates once minimum claim coverage is achieved (~25–31 claims), without enforcing a **breadth gate** proportional to question scope. Narrow questions (Topic 2: "strategies for X") are well-served; broad survey questions (Topic 3: "best places for X across 20+ countries") and deep technical topics (Topic 1: full product evolution + ecosystem) exhaust the claim budget on a subset of the answer space. The ~400-word brief format then cannot surface breadth even if it existed upstream.

---

## TOPIC NOISE (1 topic only)

### Source Quality — Topic 3 (survey)

| Field | Value |
|---|---|
| **Dimension** | Source quality |
| **Topic** | survey (Retirement abroad) |
| **Pipeline score** | 5 |
| **Best competitor** | 7 (C2, C3) |
| **Gap** | −2 |

**Evidence:** "The pipeline draws from 6 unique sources, of which 4 are blog-tier aggregators: expatsi.com, brighttax.com, eatwanderexplore.com. Only irs.gov and ssa.gov are authoritative primary sources." Competitors cited embassy sites (embassyofpanama.org), the International Living index directly, and travel.state.gov.

**Verdict:** **Warrants investigation.** While source quality scored 8 on both other topics (where academic/official sources like Nature, Gallup, IRS, and SSA were available), the survey topic forced the researcher into a domain with fewer authoritative sources. However, competitors found government and embassy sources the pipeline missed, suggesting the research phase's source-seeking strategy may lack a **primary-source pursuit heuristic** — it settles on whatever aggregator answers the question first rather than tracing claims upstream to authoritative origins. This could become structural if tested on more survey-type topics.

---

## PIPELINE STRENGTHS

### Strength 1: Confidence Calibration — 9.0 avg (dominant, +2.0 over best competitor avg)

Scores: 9, 9, 9 across all three topics. No competitor scored above 8 on any topic.

**Evidence:**
- Per-claim confidence tags (high/medium/low/inference) with numeric scores on every claim across all topics.
- Distinct `inference` type with `traces_to` fields linking analytical conclusions to constituent source claims (e.g., Topic 2 I1 traces to 8 source claims; Topic 3 S34 traces to 5 source claims).
- Aggregate confidence distributions reported in metadata (e.g., "16 high · 8 medium · 1 low · 3 inference").
- Calibrated hedging language: "high" claims use direct assertions; "medium" claims use "reports indicate" or "reportedly."
- "Claims to Verify" sections flag specific numerical claims for downstream fact-checking.

No competitor separates inference from sourced fact, traces inferences to source claims, or reports aggregate confidence distributions.

### Strength 2: Citation Quality — 8.67 avg (+1.67 over best competitor avg)

Scores: 9, 9, 8 across all three topics. Best competitor never exceeded 7.

**Evidence:**
- Every claim carries a unique S-identifier, verbatim quote, confidence rating, and source URL.
- Every prose section includes source-trace footers (e.g., "> *Sources: S1, S2, S5, I1, I2*").
- Full citation index at document end maps each S-reference to: quoted claim, sections used, confidence, and URL.
- Unused claims explicitly listed with "not used" designation — full transparency on collected-but-unsurfaced evidence.

### Strength 3: Analytical Insight — 8.67 avg (+0.67 over best competitor avg)

Scores: 9, 9, 8 across all three topics.

**Evidence:**
- Topic 1: Four original inferences (licensing-as-moat, research-to-production asymmetry, market fragmentation thesis, cross-acquisition pattern). Evaluator: "represent genuine synthesis not found in any competitor."
- Topic 2: Three traced inferences identifying binding constraints. Evaluator: "The 'binding constraint' framing (I1) and the quantified adoption gap (I2: '<10% implement the most effective form') compress multi-source evidence into actionable executive claims."
- Topic 3: Four structural inferences including the "visa income tier" framework and "territorial tax + worldwide tax = clean posture" insight.

---

## RECOMMENDED ACTIONS

### 1. Add a research breadth gate scaled to question scope

**Addresses:** Factual depth (STRUCTURAL, MAJOR)
**Expected impact:** HIGH

The research phase should classify the question scope (narrow/focused vs. broad/survey vs. deep/technical) and enforce minimum breadth targets:
- **Narrow** (e.g., "strategies for X"): current 25–31 claims sufficient
- **Broad survey** (e.g., "best places for X"): minimum 40–50 claims across ≥10 substantive entities
- **Deep technical** (e.g., "what is X and how does it compare"): minimum 35 claims covering product evolution, ecosystem, and independent benchmarks

Alternatively, add a second research pass ("breadth sweep") that runs after the initial depth pass, specifically seeking coverage of entities/subtopics not yet represented.

### 2. Add a source-tier diversity gate to the researcher

**Addresses:** Source quality (TOPIC NOISE, but warrants proactive fix)
**Expected impact:** MEDIUM

Require the researcher to confirm minimum source diversity before completing:
- ≥2 government/official sources (e.g., .gov, embassy sites, official program pages)
- ≥1 primary index/benchmark publisher (not an aggregator reporting on it)
- ≥2 specialist sources (domain experts, not general content marketing)

If thresholds are not met, trigger an additional search pass specifically targeting primary sources.

### 3. Add a data-currency check for time-sensitive topics

**Addresses:** Factual depth (specifically the 2025-vs-2026 index miss in Topic 3)
**Expected impact:** MEDIUM

For topics involving rankings, indices, or annual publications, the researcher should explicitly search for the most recent edition (e.g., "[topic] 2026" or "[index name] latest") and flag when the most recent data differs materially from earlier editions found.

### 4. Consider an optional "extended brief" format for broad topics

**Addresses:** Factual depth (format constraint component)
**Expected impact:** LOW-MEDIUM

The ~400-word executive brief format is optimal for focused topics but structurally cannot surface breadth for survey-type questions. An optional "extended brief" (800–1,200 words) or a "brief + appendix" format would allow the writer to maintain analytical density while covering more ground.

---

## SUMMARY

The pipeline averages **8.06/10** across three topics, meeting the 8.0 target by a narrow margin (+0.06) and outperforming the best competitor average by **+0.56**. Its dominant strengths are confidence calibration (9.0 avg, unmatched) and citation quality (8.67 avg), which together make it the most epistemically trustworthy output in every evaluation. The single **structural weakness is factual depth** (7.33 avg, MAJOR), which manifests when question scope is broad or technically deep — the research phase exhausts its claim budget on a subset of the answer space, and the brief format cannot compensate. **The highest-priority action is adding a scope-aware breadth gate to the research phase**, which would directly address the 2-of-3-topic factual depth deficit and likely push the pipeline average above 8.5.
