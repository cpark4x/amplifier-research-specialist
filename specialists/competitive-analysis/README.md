# Competitive Analysis Specialist

Transforms a competitive question or existing research into structured competitive
intelligence — comparison matrices, positioning gaps, and win conditions. Handles
both head-to-head comparisons and landscape analysis. Output is AI-first: structured
for downstream agent consumption, not narrative prose.

## Accepts

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `query` | string | If no `research` | "Compare X vs Y" or "Who competes with X in Z?" |
| `comparison_type` | string | No | `head-to-head` or `landscape` — auto-detected if not provided |
| `subjects` | string[] | No | Explicit subjects — extracted from query if not provided |
| `research` | ResearchOutput | No | Existing research — skips Stage 2 if provided |
| `dimensions` | string[] | No | Focus areas — defaults to: market position, product capabilities, pricing, strategic moves, distribution/partnerships, target customer |
| `quality_threshold` | string | No | `medium` / `high` / `maximum` — defaults to `high` |

## Returns

`CompetitiveAnalysisOutput` — see `shared/interface/types.md` for full schema.

Key fields returned:
- `comparison_matrix` — rating per subject+dimension with confidence and one-sentence evidence
- `profiles` — primary advantage and key weakness per subject (facts only)
- `win_conditions` — when each subject beats the competition (inferences, labeled as such)
- `positioning_gaps` — structural gaps between subjects' competitive positions (inferences)
- `evidence_gaps` — what couldn't be verified

## Can Do

- Head-to-head comparison of two or more named subjects
- Landscape analysis: discover and compare competitors for one subject
- Accept existing `ResearchOutput` to skip the research phase
- Auto-detect comparison type from the query
- Rate competitive positions across default or custom dimensions
- Surface evidence gaps honestly rather than filling them with speculation

## Cannot Do

- Write narrative prose — that is the Writer specialist's job
- Mix facts and inferences in the same output section
- Predict future competitive positions — analyzes current state only
- Rate dimensions without traceable evidence — uses `unknown` instead

## Design Notes

- **Facts and inferences are always separate.** `COMPARISON MATRIX` and `PROFILES` are
  facts. `WIN CONDITIONS` and `POSITIONING GAPS` are inferences, clearly labeled.
- **Takes longer than research alone.** Six pipeline stages with quality gates. By design.
- **Landscape mode discovers competitors first.** If subjects aren't specified, the
  specialist identifies the competitive field before profiling each competitor.
- **Chains naturally.** Accepts `ResearchOutput` as input; returns `CompetitiveAnalysisOutput`
  that the Writer specialist consumes directly.
