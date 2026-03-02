# Competitive Analysis Specialist — Design

**Date:** 2026-03-02  
**Status:** Approved  
**Epic:** 04 — Competitive Analysis Specialist  

---

## What It Does

Given a question or existing research, return structured competitive intelligence — comparison matrices, positioning gaps, and win conditions — for any set of competing subjects.

The output is **AI-first**: machine-parseable structured data designed for downstream agents (Writer, orchestrators) to consume. Human-readable as a side effect.

---

## Comparison Modes

**Head-to-head:** Two or more named subjects compared directly. Example: "Compare Microsoft vs Anthropic."

**Landscape:** One subject compared against a discovered competitive field. Example: "Who competes with Anthropic in enterprise AI?"

**Auto-detected** from the query if not explicitly provided.

---

## Input Contract

| Field | Required | Description |
|-------|----------|-------------|
| `query` | If no `research` | Natural language question — "Compare X vs Y" or "Who competes with X in Z?" |
| `comparison_type` | No | `head-to-head` or `landscape` — auto-detected if not provided |
| `subjects` | No | Explicit list of subjects to compare — extracted from query if not provided |
| `research` | No | Existing `ResearchOutput` to use instead of running fresh research |
| `dimensions` | No | Focus areas: pricing, features, positioning, market share, etc. |
| `quality_threshold` | No | `medium` / `high` / `maximum` — defaults to `high` |

**Auto-detection logic:**
- Has `research` → skip Stage 2 (Research), go straight to Stage 3 (Profile)
- No `research` + has `query` → run Stage 2 first
- `comparison_type` inferred: two named subjects = head-to-head; one subject + "competitors/landscape" = landscape

---

## Pipeline

Six stages. Stage 2 is conditional.

### Stage 1: Parse Input
Detect `comparison_type`, extract subjects, identify dimensions to compare, determine whether to run research or use what's provided. Output: structured task definition for subsequent stages.

### Stage 2: Research *(skipped if `research` is provided)*
Gather competitive intelligence for each subject using web search and fetch. Source-tiering methodology mirrors the Researcher specialist. Focus on competitive dimensions: market position, product capabilities, pricing, strategic moves, partnerships, customer base. Output: raw competitive evidence per subject.

### Stage 3: Profile
Build a fact-based profile for each subject across the identified dimensions. Every data point gets a source, tier (primary/secondary/tertiary), and confidence level. No inferences at this stage — facts only.

### Stage 4: Compare
Build the comparison matrix. For each dimension, rate each subject (`strong` / `moderate` / `weak` / `unknown`), record supporting evidence, flag contradictions between sources. For landscape mode: identify which competitors cluster together and where the primary subject stands relative to each cluster.

### Stage 5: Position
Derive the strategic picture from the comparison data. For each subject: primary advantage, key weakness, win condition, lose condition. These are **inferences** — clearly labeled as such, never presented as facts. Must trace back to comparison data.

### Stage 6: Synthesize + Quality Gate
Check confidence floor, surface evidence gaps, verify every win/lose condition is traceable to Stage 4 comparison data. Assemble `CompetitiveAnalysisOutput`. If quality threshold not met after 2 cycles: return output with explicit `QUALITY THRESHOLD RESULT: NOT MET` block.

---

## Output: CompetitiveAnalysisOutput

AI-first format — structured, parseable line-by-line. Every section machine-readable.

```
COMPETITIVE ANALYSIS BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━
Comparison type: [head-to-head | landscape]
Subjects: [comma-separated list]
Dimensions analyzed: [n]
Quality score: [low | medium | high]

COMPARISON MATRIX
subject: [name] | dimension: [name] | rating: [strong|moderate|weak|unknown] | confidence: [high|medium|low]
subject: [name] | dimension: [name] | rating: [strong|moderate|weak|unknown] | confidence: [high|medium|low]
...

PROFILES
subject: [name] | primary_advantage: [one phrase] | weakness: [one phrase]
...

WIN CONDITIONS
subject: [name] | wins_when: [condition] | loses_when: [condition]
...

POSITIONING GAPS
gap: [description] | benefits: [subject name]
...

EVIDENCE GAPS
dimension: [name] | reason: [why it couldn't be verified]
...

QUALITY THRESHOLD RESULT: [MET | NOT MET]
```

**Key principles:**
- Facts (COMPARISON MATRIX, PROFILES) and inferences (WIN CONDITIONS, POSITIONING GAPS) are in separate sections — never mixed
- Every rating has a confidence level
- Evidence gaps are first-class outputs, never omitted
- `quality_threshold: maximum` fails loud, not silent — same contract as Researcher

---

## How It Chains

**Researcher → Competitive Analysis:**
Pass `ResearchOutput` as the `research` input. Stage 2 is skipped.

**Competitive Analysis → Writer:**
Pass `CompetitiveAnalysisOutput` as source material. The Writer transforms structured competitive intelligence into a brief, report, or executive summary.

**Full chain:**
`Researcher → Competitive Analysis → Writer`

**Standalone:**
Pass a `query` — the specialist handles research and analysis in one call.

---

## Output Schema

Defined in `shared/interface/types.md` before implementation begins.

Key types to define:
- `CompetitiveAnalysisOutput` (top-level)
- `ComparisonRating` (`strong` | `moderate` | `weak` | `unknown`)
- `WinCondition` (subject, wins_when, loses_when)
- `PositioningGap` (gap description, benefits)

Reuse from Researcher: `EvidenceGap`, confidence levels, source tiers.

---

## Files to Create

```
specialists/
└── competitive-analysis/
    ├── index.md      # Agent persona + 6-stage pipeline instructions
    └── README.md     # Interface contract

shared/interface/types.md    # Add CompetitiveAnalysisOutput schema
behaviors/specialists.yaml   # Add agents.include entry
context/specialists-instructions.md  # Add to available specialists + when-to-use
README.md                    # Add to specialists table
```
