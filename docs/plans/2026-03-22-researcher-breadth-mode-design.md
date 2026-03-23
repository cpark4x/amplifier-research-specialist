# Researcher Breadth Mode Design (#46)

## Goal

Add a `research_mode: breadth` option to the researcher specialist so that survey-type questions automatically use lighter corroboration, allowing coverage of 15-20 entities instead of 10-13 in the same runtime.

## Background

The researcher's structured methodology prioritizes trustworthiness over breadth. For survey questions ("best places to retire"), breadth matters as much as depth. In A/B tests, the direct approach covered 15 destinations vs the researcher's 13. The bottleneck: the researcher corroborates every claim, spending search budget on verifying qualitative statements like "Portugal has great weather" instead of discovering additional entities.

The v1 quality loop already added a question-type classifier (Stage 1) that detects "Survey/Ranking" questions. And #49 (just shipped) adds iterative deepening for thin sub-questions. But neither changes the fundamental corroboration methodology — the researcher still does full corroboration on every claim, which limits entity coverage.

## Approach: Automatic with Override

The question-type classifier (already in Stage 1) detects "Survey/Ranking" and automatically sets `research_mode: breadth`. The caller can override with `research_mode: depth` if they want full corroboration even for surveys. All other question types default to `research_mode: depth` (current behavior).

Why automatic with override:
- Most of the time you want breadth for surveys — saves the caller from having to know about research modes
- Occasionally you might want deep corroboration on a survey topic (e.g., "best countries for tax planning" where accuracy matters more than breadth)
- The question-type classifier already exists and correctly identifies Survey/Ranking questions

## Components

### Stage 1 (Planner) — Mode Selection

After the existing question-type classifier (Step A), add a mode selection step:

- If question type is "Survey/Ranking" AND no explicit `research_mode` was provided → set `research_mode: breadth`
- If caller explicitly passed `research_mode: depth` → use depth regardless of question type
- All other question types default to `research_mode: depth` (current behavior)

### Stage 5 (Corroborator) — Breadth Mode Logic

The Corroborator currently corroborates every low/medium confidence claim. In breadth mode:

- **Numeric/financial claims** (dollar amounts, percentages, statistics, dates, rankings, index scores) → full corroboration (same as depth mode). These are the claims most likely to be wrong and most damaging if inaccurate.
- **Qualitative claims** (descriptions, lifestyle observations, cultural assessments, general characterizations, subjective evaluations) → accept at medium confidence from a single credible source, skip corroboration. Flag as `single-source, medium confidence, breadth-mode`.

Why corroborate only numeric/financial claims:
- The competitive eval showed that factual accuracy on specific numbers matters most (the pipeline cited a 2025 International Living index when the 2026 was available)
- Qualitative claims about "Portugal has great weather" don't need corroboration
- But "cost of living in Portugal is $2,000/month" does
- This saves ~40 corroboration searches per survey topic, freeing the researcher to discover more entities

## Data Flow

1. **Stage 1 (Planner)** classifies question type → detects "Survey/Ranking" → sets `research_mode: breadth`
2. Stages 2-4 proceed unchanged (Source Discovery, Fetch, Extract)
3. **Stage 5 (Corroborator)** checks `research_mode`:
   - `depth` → corroborate all low/medium confidence claims (current behavior)
   - `breadth` → classify each claim as numeric/financial or qualitative → corroborate only numeric/financial → flag qualitative claims as `single-source, medium confidence, breadth-mode`
4. Stage 6 (Quality Gate) proceeds unchanged

## What Does NOT Change

- Stage 2 (Source Discoverer) — same search strategy
- Stage 3 (Fetcher) — same fetch behavior
- Stage 4 (Extractor) — same extraction
- Stage 6 (Quality Gate) — same gates, including the depth check from #49
- Output format — same structure, just more claims at medium confidence in breadth mode
- No new pipeline stages
- No new recipe files
- No changes to any other specialist or agent file
- No changes to the recipe (research_mode can be passed as a context variable if the caller wants to override)

## Error Handling

- If the question-type classifier fails to classify, default to `research_mode: depth` (safe fallback — current behavior)
- If a claim can't be clearly classified as numeric vs qualitative in breadth mode, treat it as numeric and corroborate (err on the side of accuracy)
- All single-source qualitative claims are explicitly flagged as `breadth-mode` so downstream consumers (writer hedging logic) can apply appropriate hedging language

## Runtime Impact

Breadth mode doesn't add time — it saves time. The researcher currently corroborates ~60 claims for a survey topic. In breadth mode, only ~15-20 numeric/financial claims get corroborated. The other ~40 qualitative claims skip corroboration. The researcher can then use the saved search budget to discover additional entities, covering 15-20 instead of 10-13 in the same total runtime.

## Scope

### Changes

- `agents/researcher.md` — modify Stage 1 (add mode selection after question-type classifier) and Stage 5 (add breadth mode corroboration logic)

### No Changes

- No new pipeline stages or files
- No changes to any other specialist or agent
- No changes to the output format
- No changes to the recipe

## Testing Strategy

1. Structural test confirming the mode selection language exists in Stage 1 after the question-type classifier
2. Structural test confirming the breadth mode corroboration logic exists in Stage 5
3. Test that "Survey/Ranking" trigger is documented
4. Test that numeric/financial vs qualitative distinction is documented
5. Test that `breadth-mode` flag is mentioned for single-source claims

## Expected Impact

The researcher can cover 15-20 entities in survey topics instead of 10-13, closing the breadth gap identified in the competitive eval. Source quality stays high for numeric claims. Qualitative claims are flagged as medium confidence from single sources — the writer's hedging logic (Stage 4 in writer.md) already handles medium-confidence claims with appropriate hedging language.