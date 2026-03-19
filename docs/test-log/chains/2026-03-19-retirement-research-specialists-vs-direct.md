---
specialist: multi-pipeline
chain: "specialists (researcher → researcher-formatter → writer → writer-formatter) vs direct (web-research single-agent)"
topic: retirement-destinations-seattle-american
date: 2026-03-19
quality_signal: mixed
action_items_promoted: true
---

# Specialists Pipeline vs Direct Approach — Retirement Research — 2026-03-19

**Task:** Research the best places in the world for an American currently living in Seattle to retire. Cover destinations, costs vs Seattle, healthcare, visas, taxes, financial logistics, SEA-TAC access, emerging destinations, and risks.

**Why this run matters:** Second controlled A/B test. Unlike the Mar 18 RTO test (which used the full 6-agent deep chain including data-analyzer), this test ran a **4-agent chain** (researcher → formatter → writer → writer-formatter) — the standard research-to-brief path without analysis. Tests the pipeline on a survey-type question (breadth matters) rather than an analytical question (depth matters). Also the first test where the **writer-formatter broke** in ad-hoc (coordinator-driven) mode, revealing a structural gap in the two-input contract.

---

## Input Given to Each Approach

**Specialists pipeline:** Research prompt delegated to `specialists:researcher`. Output passed through 4-agent chain: researcher → researcher-formatter → writer → writer-formatter (attempted). Coordinator-driven (ad-hoc delegation), not recipe-driven.

**Direct approach:** Same research prompt delegated to `foundation:web-research` (single agent). Brief written directly by the orchestrating session from the agent's findings.

---

## Specialists Pipeline Output

### researcher
Returned ~8,000 words covering 13 destinations (Portugal, Mexico, Costa Rica, Greece, Panama, Spain, Italy, Thailand, Malaysia, France, Colombia, Belize, Philippines) plus 4 emerging (Montenegro, Northern Cyprus, Albania, Uruguay). Financial logistics section covering Social Security, Medicare, health insurance, banking/FATCA, and US tax obligations. Seattle-specific section with SEA-TAC flight data and WA no-income-tax analysis.

**Quality:** Strong. Found unique high-value insights the direct approach missed: (1) France preserves Roth IRA tax-exempt status under US-France treaty, (2) US brokerages increasingly closing expat accounts due to FATCA, (3) Mexico non-resident tax strategy (>50% US-sourced income = no Mexican tax), (4) new 2026 SEA-TAC routes to Rome, Barcelona, Hong Kong, (5) $6,000 Senior Deduction for 65+ (2025-2028). Used International Living 2026 index (Greece #1) — more current than direct approach's 2025 index (Panama #1).

**Missed vs direct:** Ecuador (safety deterioration detail), Malta (WHO #5 healthcare), specific insurance provider pricing ranges (Cigna $3K-$12K, IMG $2.5K-$8K vs researcher's single $5,900 average), Ecuador's use of US dollar.

### researcher-formatter
Normalized to canonical RESEARCH OUTPUT block. 45+ claims with tier/confidence labels. Sub-question coverage table (10 sub-questions, all High or Medium-High).

**Quality:** Clean format conversion. Massive output (~15K tokens) — this became a problem downstream when the writer-formatter needed it as a second input.

### writer
Produced ~2,500-word decision brief in 6 sections: Executive Summary, Destination Profiles (3 tiers), Your Seattle Advantage, Financial Logistics, Quick-Pick Recommendations (8 priority profiles), Comparative Summary Table. Advisory tone ("your biggest logistical hurdle isn't choosing where to go — it's the financial plumbing").

**Quality:** The clear star of the pipeline. Markedly better than the direct approach in:
- **Structure**: Decision-oriented (organized by reader's priorities, not by country encyclopedia)
- **Synthesis**: Executive summary that actually synthesizes ("strongest options cluster in Latin America for barrier-to-entry, Southern Europe for tax incentives, Southeast Asia for cost savings")
- **Voice**: Advisory/consultative rather than encyclopedic
- **Hedging**: Source-tier-aware ("reports indicate" for medium-confidence, definitive for high-confidence)
- **Actionability**: Star ratings for SEA-TAC access, quick-pick table by priority
- **Coverage gaps**: Explicitly names what's missing (safety data, climate details, real estate forecasts)

Correctly overrode the 250-400 word "brief" budget — a 13-destination comparison cannot fit in 400 words. See backlog item #43.

### writer-formatter (FAILED)
**Broke.** Requested the original RESEARCH OUTPUT as its second input. In ad-hoc (coordinator-driven) mode, the coordinator had already consumed the research output ~15K tokens ago and could not reasonably re-send it. The formatter asked for the source material and halted.

**Root cause:** Writer-formatter's two-input contract (writer output + original source material) is designed for the recipe pipeline, where `{{formatted_research}}` and `{{final_document}}` are passed as context variables. In ad-hoc coordinator mode, the coordinator would need to re-send the entire research corpus — defeating the purpose of delegation as a context-conservation strategy.

**Impact:** The writer's output was presented directly to the user without canonical formatting (no Parsed: header, no S-numbered claims extraction, no CITATIONS block, no CLAIMS TO VERIFY). For a human-terminal flow, this had zero practical impact — the writer's prose was excellent. For a downstream agent consumer, it would have been a problem.

**Conclusion:** This is not a formatter bug — it's an **architectural gap** in how the coordinator instructions (Rules 5-8) handle ad-hoc vs recipe execution. See backlog items #44 and #45.

---

## Direct Approach Output

### foundation:web-research
Single research agent returned ~6,000 words covering 15 destinations with deep profiles per country. Used International Living 2025 index (Panama #1 — one year older than specialists' 2026 source).

**Quality:** Broader coverage (15 vs 13 full profiles). More granular per-country detail — specific hospital names (Johns Hopkins-affiliated Punta Pacifica in Panama), specific insurance pricing ranges per provider, Malta WHO ranking, Ecuador safety deterioration narrative. Less source-tier awareness — all facts presented with equal confidence.

### Manual synthesis (orchestrator session)
~3,000-word brief. Country profiles with emoji flags, risk matrix table, profile-based recommendations, comparative table.

**Quality:** Encyclopedia-style — comprehensive but flat. Every country gets the same template treatment. No synthesis across countries. No advisory framing. Sources listed in a table at end rather than traced per-claim.

---

## Head-to-Head Comparison

| Dimension | Specialists | Direct | Winner |
|---|---|---|---|
| **Breadth (# destinations)** | 13 + 5 emerging | 15 full profiles | Direct |
| **Depth per destination** | Strong on tax/visa/financial | More granular (hospital names, provider pricing) | Direct |
| **Unique insights** | France Roth IRA, FATCA closures, Mexico non-resident tax, 2026 SEA-TAC routes, Senior Deduction | Ecuador safety detail, Malta WHO ranking, specific insurance ranges | **Specialists** (higher value) |
| **Source currency** | 2026 index | 2025 index | **Specialists** |
| **Source transparency** | Per-claim tier + confidence labels throughout | Source table at end | **Specialists** |
| **Writing quality** | Advisory, decision-oriented, synthesized | Encyclopedic, template-driven | **Specialists** |
| **Hedging/calibration** | Tier-aware ("reports indicate" vs definitive) | Uniform confidence on all claims | **Specialists** |
| **Structure** | Organized by reader decisions | Organized by country | **Specialists** |
| **Actionability** | Star ratings, quick-pick table, "establish banking before you move" | Risk matrix, profile recommendations | **Specialists** (slight) |
| **Speed** | 4 agent calls, writer-formatter broke | 1 agent call | **Direct** |
| **Token cost** | ~40K+ tokens across agents | ~15K tokens | **Direct** |
| **Pipeline reliability** | Writer-formatter failed (ad-hoc mode) | No failures | **Direct** |

**Overall: Specialists produced a better document. Direct was faster and more reliable.**

---

## Key Findings

### 1. Writer-Formatter Two-Input Contract Breaks in Ad-Hoc Mode
The formatter needs both the writer output and the original research output. The recipe passes both via context variables. The coordinator cannot efficiently re-send ~15K tokens of research output to the formatter — it defeats delegation's token-conservation purpose. **New backlog item: #44 (writer-formatter graceful degradation) and #45 (two-path doctrine for coordinator).**

### 2. Researcher Breadth vs Depth Tradeoff
The researcher's structured methodology (corroboration requirements, quality gates) prioritizes trustworthiness over breadth. For survey-type questions ("what are the best places"), breadth matters as much as depth. The direct approach covered more destinations because it wasn't constrained by corroboration requirements. **New backlog item: #46 (researcher breadth mode).**

### 3. Writer "Brief" Format Budget Inadequate for Comparative Research
The writer correctly ignored the 250-400 word budget because 13 destinations cannot fit in 400 words. The format taxonomy needs a comparative/decision brief variant. **New backlog item: #43 (decision-brief format).**

### 4. Researcher-Formatter Output Size Inflates Downstream Cost
The formatter canonicalized 45+ claims into ~15K tokens of structured output. This entire block must be passed to the writer. For human-terminal flows, the writer doesn't need S-numbered claim extraction — it needs the findings. The canonical format adds token overhead without proportional value when no downstream agent will parse the S-numbers.

### 5. Researcher Found Higher-Value Unique Insights
Despite lower breadth, the researcher's structured tax-treaty investigation path surfaced non-obvious findings (France Roth IRA, FATCA closures) that the direct approach missed. The methodology pays for itself on depth — it just needs a breadth mode for survey questions.

### 6. The Writer Is the Pipeline's Clear Value-Add
The separation of research from writing produced a demonstrably better document. The writer's advisory tone, decision framing, and source-tier-aware hedging are genuine quality advantages that justify the pipeline's existence.

---

## Action Items

| # | Item | Route to | Priority |
|---|---|---|---|
| 43 | Writer: add `decision-brief` format with 1,500-3,000 word budget for comparative/survey research | BACKLOG near-term | P2 |
| 44 | Writer-formatter: graceful degradation when source material unavailable (format what you have, don't block) | BACKLOG near-term | P2 |
| 45 | Coordinator: two-path doctrine — recipe path = formatters always; ad-hoc path = formatters optional for human-terminal flows | BACKLOG near-term (expands #36 lever 5) | P1 |
| 46 | Researcher: add `research_mode: breadth` for survey-type questions (wider net, lighter corroboration) | BACKLOG near-term | P2 |
| 47 | Researcher: add contrarian sweep step for risk/downside coverage | BACKLOG Priority 3 | P3 |

---

## Test Metadata

| Field | Value |
|---|---|
| Date | 2026-03-19 |
| Topic | Best retirement destinations for Seattle-based American |
| Pipeline | researcher → researcher-formatter → writer → writer-formatter (broke) |
| Comparison | foundation:web-research (single agent) |
| Execution mode | Ad-hoc coordinator delegation (not recipe) |
| Writer format | brief (overrode to ~2,500 words) |
| Writer audience | individual retiree (practical, decision-oriented) |
| Researcher claims | 45+ |
| Destinations covered | Specialists: 13 + 5 emerging; Direct: 15 full profiles |
| Writer-formatter | FAILED — two-input contract not satisfiable in ad-hoc mode |