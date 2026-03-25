---
specialist: multi-pipeline
chain: "specialists (researcher → researcher-formatter → writer) vs direct (orchestrator web_search + web_fetch)"
topic: weight-loss-recipes-busy-professional
date: 2026-03-24
quality_signal: pass
action_items_promoted: true
---

# Specialists Pipeline vs Direct Approach — Weight Loss Recipes — 2026-03-24

**Task:** Research the best recipes for losing weight, personalized for a busy tech professional with no known dietary restrictions.

**Why this run matters:** Third controlled A/B test in the specialists-vs-direct series. Unlike the Mar 18 RTO test (6-agent deep chain with data-analyzer) and the Mar 19 retirement test (4-agent chain where writer-formatter broke), this test ran a **3-agent chain** (researcher → researcher-formatter → writer) with the writer-formatter intentionally skipped per the two-path doctrine (Rule 9 — ad-hoc coordinator, human-terminal flow). Tests the pipeline on a **practical/advisory question** (actionable recipes, not comparative analysis) and validates the two-path doctrine fix from backlog item #45.

---

## Input Given to Each Approach

**Specialists pipeline:** Research prompt delegated to `specialists:researcher` with context about the user being a busy tech professional with no dietary restrictions. Output passed through 3-agent chain: researcher → researcher-formatter → writer. Coordinator-driven (ad-hoc delegation), not recipe-driven. Writer-formatter skipped per two-path doctrine (Rule 9).

**Direct approach:** Same research topic. Orchestrator session ran 6 parallel web_search queries + 6 parallel web_fetch calls, then wrote the brief directly from the fetched content.

---

## Specialists Pipeline Output

### researcher
Returned ~8,000 words covering 28 individually cited findings across 6 sub-questions: (1) Evidence-based dietary approaches, (2) Key nutritional principles, (3) Specific practical recipes, (4) Recent research 2024–2026, (5) Meal prep strategies, (6) Risks/downsides/failure modes. 14 turns of internal searching. 14+ distinct source domains.

**Quality:** Strong. Structured sub-question decomposition ensured comprehensive coverage. Found the key PMC12255039 paper (2025 narrative review) which provided the 30-30-30 framework and peer-reviewed sample daily menu with exact macro breakdowns. Dedicated contrarian sweep surfaced: 50% regain rate, adherence gaps in RCTs, depression as moderator of weight loss success, Volumetrics restricting healthy fats, IF's failure to meet clinical significance threshold.

**Source rigor:** 57% primary (peer-reviewed/institutional), 39% secondary, 4% tertiary. Every finding tagged with tier, confidence (high/medium), corroboration count, and date. 5 explicit evidence gaps documented (EatingWell 403, U.S. News timeout, Reddit not reached, per-recipe macro data truncated, Academy of Nutrition keto article snippet only).

### researcher-formatter
Normalized to canonical RESEARCH OUTPUT block. 28 claims with tier/confidence labels. Sub-question coverage table (6 sub-questions, all High or Moderate).

**Quality:** Clean format conversion. Single-input formatter — no two-input contract issue (unlike the retirement test's writer-formatter failure).

### writer
Produced ~1,200-word brief in 6 sections: Summary, 30-30-30 Framework, Weekly Recipe Playbook (table + swap-ins + pantry MVPs), Sunday Meal Prep, What to Skip, The Real Risk: Regain, Next Steps. Friendly expert tone ("smart friend who's also a registered dietitian").

**Quality:** Good. Recipes were the star as requested — the macro table was the centerpiece. Practical next steps ("This weekend: grocery shop..."). Slight formality from the pipeline — confidence assessment table and claim index at the bottom added overhead a human reader wouldn't use.

### writer-formatter
**Intentionally skipped** per two-path doctrine (Rule 9, backlog item #45). Writer output went directly to the user. No canonical formatting issues — the writer's prose was clean and readable for a human consumer.

**Validation:** The two-path doctrine fix works correctly. No formatter failure, no token waste re-sending research output.

---

## Direct Approach Output

### Orchestrator direct research
6 parallel web_search queries + 6 parallel web_fetch calls. Fetched: PMC12255039 (100K bytes, truncated), Profolus (Cochrane review), Mayo Clinic Diet, Skinnytaste meal plan, Real Food Dietitians recipes, Healthline meal prep guide. Orchestrator synthesized and wrote the brief directly.

**Quality:** Found the same core evidence (PMC12255039, Cochrane 2026, Mayo Clinic) as the specialist pipeline. Slightly tighter prose — more conversational, less structured overhead. Added Real Food Dietitians recipes with specific per-serving macros (Beef Skillet Enchiladas 31g protein/8g fiber, Crockpot Hamburger Soup 25g protein/8g fiber) that the specialist pipeline didn't surface.

**Missed vs specialists:** No formal source tiering. No confidence ratings per claim. No evidence gaps documented. No contrarian sweep (covered regain and keto but missed depression-as-moderator, adherence gaps in RCTs, Volumetrics healthy fat restriction). Sources listed at bottom without per-claim traceability.

---

## Head-to-Head Comparison

| Dimension | Specialists | Direct | Winner |
|---|---|---|---|
| **Source count** | 28 findings, 14+ domains | ~8 sources fetched | **Specialists** |
| **Source rigor** | Per-claim tier + confidence + date + corroboration | Sources listed at end | **Specialists** |
| **Evidence gaps** | 5 explicit gaps documented | Not tracked | **Specialists** |
| **Contrarian coverage** | Dedicated sweep: regain, depression, adherence gaps, Volumetrics fats, keto risks | Regain + keto only | **Specialists** |
| **Recipe specificity** | PMC12255039 Table 1 + Mayo Clinic + RD recipes | Same core + Real Food Dietitians per-serving macros | Tie |
| **Practical usefulness** | Strong — next steps, meal prep system | Strong — same content | Tie |
| **Readability** | Good but some pipeline overhead (confidence tables, claim numbering) | Tighter, more conversational | **Direct** (slight) |
| **Speed** | ~8–10 minutes (3 sequential delegations) | ~2 minutes (2 parallel batches) | **Direct** |
| **Token cost (main session)** | ~3K tokens (summaries only) | ~150K+ tokens (raw web fetches in context) | **Specialists** |
| **Pipeline reliability** | No failures (writer-formatter correctly skipped) | No failures | Tie |

**Overall: Specialists produced more rigorous, auditable research. Direct was 4–5x faster with slightly better readability.**

---

## What Worked

1. **Two-path doctrine (Rule 9) validated.** Writer-formatter intentionally skipped in ad-hoc mode. No failure, no token waste. This is the fix for the Mar 19 retirement test's writer-formatter crash. Backlog item #45 works as designed.
2. **Researcher's structured methodology** surfaced the PMC12255039 paper and its peer-reviewed sample menu — the single highest-value finding for this topic. The 14-turn search loop with corroboration requirements found authoritative sources the direct approach also found, plus additional contrarian evidence.
3. **Researcher-formatter is lightweight and reliable.** Single-input contract works cleanly in ad-hoc mode every time.
4. **Writer produced good recipe-focused output** with the macro table as centerpiece. Responded well to the instruction to make recipes the star.

## What Didn't / Concerns

1. **Writer pipeline overhead.** The confidence assessment table, claim index (S1–S26), and CITATIONS block at the bottom are invisible to the user but consumed writer tokens. For human-terminal flows, the writer could skip these.
2. **Direct approach found unique recipes** (Real Food Dietitians with per-serving macros) that the specialist didn't. The researcher's corroboration requirements may cause it to skip practitioner-only content that doesn't have peer-reviewed backing but is still useful.
3. **Direct approach's massive context cost** (~150K tokens) is unsustainable in a long session. This is the primary argument for the specialist pipeline — context conservation, not quality per se.
4. **Slight over-formality in specialist output.** The "smart friend who's also a dietitian" tone instruction was partially followed but the structured pipeline adds formality that pure conversational output doesn't have.

## Confidence Accuracy

Not directly testable — claims are based on peer-reviewed sources. Both approaches found the same core evidence (PMC12255039, Cochrane 2026) and presented it accurately. The specialist pipeline's per-claim confidence ratings (high/medium) were appropriate — high for meta-analyses, medium for single small studies (iDip n=22) and secondary sources.

## Coverage Assessment

| Sub-question | Specialists | Direct |
|---|---|---|
| Evidence-based dietary approaches | High (6+ sources) | Moderate (3 sources) |
| Nutritional principles (protein, fiber, calorie density) | High (5+ sources) | High (same core PMC paper) |
| Specific recipes with macros | High (PMC + Mayo + RDs) | High (PMC + Mayo + RDs + Real Food Dietitians) |
| Recent research 2024–2026 | High (4 sources, 2024–2026) | Moderate (2 sources) |
| Meal prep strategies | Moderate (3 RD sources) | Moderate (Healthline guide) |
| Risks/downsides | High (dedicated contrarian sweep) | Low (regain + keto only) |

## Action Items

| # | Item | Route to | Priority |
|---|---|---|---|
| — | Two-path doctrine (Rule 9) works. No new items from this. | N/A — validates #45 | — |
| 53 | Writer: consider skipping claim index and confidence tables for human-terminal ad-hoc flows (reduce overhead) | BACKLOG | P3 |
| 54 | Researcher: consider including practitioner-sourced recipes/content even without peer-reviewed corroboration when the question is practical/advisory (not analytical) | BACKLOG | P3 |

---

## Scoring (User-Requested)

| Dimension | Specialists | Direct |
|---|---|---|
| Accuracy | 9 | 8 |
| Depth | 9 | 6 |
| Source rigor | 9.5 | 5 |
| Completeness | 8.5 | 7 |
| Practical usefulness | 8 | 8.5 |
| Readability | 7.5 | 8.5 |
| Speed | 4 | 9 |
| Context efficiency | 9 | 3 |
| Vault-worthiness | 8.5 | 7 |
| **Overall** | **8.5** | **7** |

---

## Test Metadata

| Field | Value |
|---|---|
| Date | 2026-03-24 |
| Topic | Best weight loss recipes for a busy professional |
| Pipeline | researcher → researcher-formatter → writer (writer-formatter skipped per Rule 9) |
| Comparison | Orchestrator direct (6x web_search + 6x web_fetch) |
| Execution mode | Ad-hoc coordinator delegation (not recipe) |
| Writer format | brief (~1,200 words) |
| Writer audience | Individual (busy tech professional, practical tone) |
| Researcher claims | 28 |
| Researcher turns | 14 |
| Direct tool calls | 14 (6 search + 6 fetch + 2 bash) |
| Wall clock: specialists | ~8–10 minutes |
| Wall clock: direct | ~2 minutes |
| Two-path doctrine | Validated — writer-formatter correctly skipped |
