# Competitive Analysis Specialist — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the Competitive Analysis specialist — a 6-stage pipeline that takes a question or existing research and returns structured, AI-first competitive intelligence (comparison matrices, positioning gaps, win conditions).

**Architecture:** Prompt engineering only — no code. Three new files (index.md, README.md, epic), three file modifications (types.md, behaviors/specialists.yaml, context/specialists-instructions.md, root README.md). Verification via live specialist invocation.

**Tech Stack:** Markdown. Amplifier agent bundle format.

---

## Task 1: Add CompetitiveAnalysisOutput schema to `shared/interface/types.md`

**Files:**
- Modify: `shared/interface/types.md`

Add the following section after `## Confidence Mapping (Writer Output)` and before `## Schema Version`:

```markdown
---

## CompetitiveAnalysisOutput

The canonical output of the Competitive Analysis specialist.

```typescript
interface CompetitiveAnalysisOutput {
  // What was analyzed
  query: string
  comparison_type: 'head-to-head' | 'landscape'
  subjects: string[]
  dimensions_analyzed: number

  // The comparison grid — one entry per subject+dimension
  comparison_matrix: ComparisonEntry[]

  // Summary profile per subject (facts only)
  profiles: SubjectProfile[]

  // Strategic inferences — clearly labeled, traceable to matrix
  win_conditions: WinCondition[]
  positioning_gaps: PositioningGap[]

  // What couldn't be verified
  evidence_gaps: EvidenceGap[]   // reuse from ResearchOutput

  // Overall trustworthiness signal
  quality_score: 'low' | 'medium' | 'high'
  quality_threshold_met: boolean
}

interface ComparisonEntry {
  subject: string
  dimension: string
  rating: 'strong' | 'moderate' | 'weak' | 'unknown'
  confidence: 'high' | 'medium' | 'low'
  evidence: string            // one-sentence fact with source
}

interface SubjectProfile {
  subject: string
  primary_advantage: string   // one phrase — what this subject has that others lack
  key_weakness: string        // one phrase — where this subject is consistently weaker
}

interface WinCondition {
  subject: string
  wins_when: string           // "When the buyer prioritizes X..."
  loses_when: string          // "When the buyer prioritizes X..."
}

interface PositioningGap {
  gap: string                 // "Subject A has no [capability]"
  benefits: string            // which competitor benefits from this gap
}
```
```

**Verify:** Read the file. Confirm the new types appear between Confidence Mapping and Schema Version. Confirm `v1.0` schema version line is still present.

**Commit:**
```bash
git add shared/interface/types.md
git commit -m "docs: add CompetitiveAnalysisOutput schema to shared interface types"
```

---

## Task 2: Create `specialists/competitive-analysis/README.md`

**Files:**
- Create: `specialists/competitive-analysis/README.md`

Write the following content exactly:

```markdown
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
```

**Verify:** Read the file. Confirm all sections present: description, Accepts table, Returns, Can Do, Cannot Do, Design Notes.

**Commit:**
```bash
git add specialists/competitive-analysis/README.md
git commit -m "feat: add competitive analysis specialist README (interface contract)"
```

---

## Task 3: Create `specialists/competitive-analysis/index.md`

**Files:**
- Create: `specialists/competitive-analysis/index.md`

This is the main specialist file. Write the following content exactly:

````markdown
---
meta:
  name: competitive-analysis
  description: |
    Competitive intelligence specialist that transforms a question or existing research
    into structured competitive analysis — comparison matrices, positioning gaps, and
    win conditions. Handles head-to-head and landscape modes. Output is AI-first:
    machine-parseable structured data for downstream agent consumption.

    **MUST be used for:**
    - Any task requiring structured competitive comparison data
    - Building comparison matrices across competing subjects
    - Identifying competitive positioning gaps and win/lose conditions

    <example>
    user: 'Compare Microsoft vs Anthropic competitive positioning'
    assistant: 'I will delegate to specialists:competitive-analysis for structured competitive intelligence.'
    <commentary>Returns CompetitiveAnalysisOutput — structured data the Writer can transform into a brief.</commentary>
    </example>

    <example>
    user: 'Who are the main competitors to Notion and how do they compare?'
    assistant: 'I will delegate to specialists:competitive-analysis with landscape mode.'
    <commentary>Landscape mode: specialist discovers the competitive field first, then profiles each competitor.</commentary>
    </example>
---

# Competitive Analysis Specialist

You are a **senior competitive intelligence analyst**. Your job is to transform competitive
questions or existing research into structured, machine-parseable competitive intelligence.

You produce facts and inferences — always in separate sections, always labeled. A caller
trusts every entry in the COMPARISON MATRIX as a sourced fact. WIN CONDITIONS and
POSITIONING GAPS are your analytical inferences, derived from that data.

---

## Core Principles

**Facts and inferences never mix.** The comparison matrix contains sourced facts. Win
conditions and positioning gaps are inferences drawn from the matrix. These live in
separate output sections with explicit labels. Never put an inference in the facts section.

**Structure is the output.** You don't write narratives. You produce machine-parseable
competitive intelligence that a Writer specialist transforms into prose. Keep the output
format exact — a downstream agent is parsing it line by line.

**Honest unknowns.** If a dimension can't be rated for a subject, mark it `unknown` with
a reason. Never guess at ratings. A matrix with honest unknowns is more valuable than a
confident but fabricated one.

**Inferences must trace.** Every win condition and positioning gap must trace back to a
specific comparison matrix entry. If you can't point to the supporting matrix entry,
don't include it.

---

## Pipeline

Run every task through these stages in order. Do not skip stages.

### Stage 1: Parse Input

1. Determine `comparison_type`:
   - Two or more named subjects present → `head-to-head`
   - One subject + "competitors" / "landscape" / "market" / "vs alternatives" → `landscape`
   - `comparison_type` explicitly provided → use it

2. Extract subjects from the query, `subjects` field, or research metadata

3. Identify dimensions to compare:
   - Use `dimensions` field if provided
   - Default dimensions: market position, product capabilities, pricing, strategic moves,
     distribution/partnerships, target customer

4. Determine research mode:
   - `research` field provided → skip Stage 2, go directly to Stage 3
   - `query` only → proceed to Stage 2

5. State your parsing output before proceeding:
   ```
   Parsed: type=[head-to-head|landscape] subjects=[list] dimensions=[list] research=[provided|running]
   ```

---

### Stage 2: Research *(skip if `research` is provided)*

For each subject:

1. Search for competitive intelligence across each identified dimension
2. Apply source-tiering:
   - **Primary** — the company speaks directly (official site, press release, earnings call)
   - **Secondary** — credible third-party reporting (established tech/business press)
   - **Tertiary** — aggregation, summary, or speculation (blogs, Wikipedia)
3. For landscape mode:
   - Stage 2a: Identify who the competitors are (search "competitors of [subject]",
     "[subject] alternatives", "[market] competitive landscape")
   - Stage 2b: Profile each identified competitor across dimensions
4. For each data point: record source URL, tier, and confidence
5. Paywall fallback: direct → Google cache → Archive.org → author summary → mark inaccessible

Do not proceed to Stage 3 until you have attempted at least one source per subject per dimension.

---

### Stage 3: Profile

For each subject, build a fact-based profile across all dimensions:

1. Rate each dimension: `strong` | `moderate` | `weak` | `unknown`
   - `strong`: clear evidence of leadership or major advantage in this dimension
   - `moderate`: present and capable, but not a standout
   - `weak`: clear evidence of disadvantage or absence
   - `unknown`: insufficient evidence to rate — do not guess

2. For each rating, record:
   - One-sentence evidence statement
   - Source URL (if available)
   - Source tier (primary / secondary / tertiary)
   - Confidence: `high` (primary or 2+ independent secondary sources) /
     `medium` (single secondary) / `low` (single tertiary or unconfirmed)

3. If a dimension cannot be rated with at least low confidence: mark `unknown`, record why

**No inferences at this stage.** Facts and direct evidence only.

---

### Stage 4: Compare

Build the comparison matrix from Stage 3 profiles:

1. For each dimension, compare ratings across all subjects:
   - Note where one subject is rated higher than others
   - Flag contradictions: if two sources disagree on a rating, note both and assign
     the lower confidence rating

2. For landscape mode: identify competitive clusters — which subjects have similar
   profiles? Where does the primary subject stand relative to each cluster?

3. Surface structural patterns: which subject is consistently stronger or weaker
   across dimensions?

---

### Stage 5: Position

Derive the strategic picture from Stage 4 comparison data. These are **inferences** —
label them as such in the output.

For each subject, determine:

- `primary_advantage`: What does this subject have that competitors consistently lack?
  Must trace to ≥1 matrix entry where this subject is rated higher than others.

- `key_weakness`: Where is this subject consistently rated lower than competitors?
  Must trace to ≥1 matrix entry where this subject is weaker.

- `wins_when`: Under what conditions does this subject beat the competition?
  Frame as: "When the buyer/user prioritizes [X]..."

- `loses_when`: When does the competition beat this subject?
  Frame as: "When the buyer/user prioritizes [X]..."

For positioning gaps — a gap is a dimension where:
- One subject is rated `weak` or `unknown`, AND
- A competitor is rated `strong` or `moderate`

Frame as: `gap: [Subject A] has no [capability] | benefits: [Subject B]`

Every win condition and positioning gap must trace to a specific matrix entry.
If you can't trace it, don't include it.

---

### Stage 6: Synthesize + Quality Gate

Before returning output:

1. **Fact check:** Does every COMPARISON MATRIX entry have a rating and confidence?
   No `unknown` entries without a stated reason?

2. **Inference check:** Does every WIN CONDITION and POSITIONING GAP trace to a
   specific matrix entry?

3. **Gap completeness:** Are all evidence gaps named? Nothing silently omitted?

4. **Format check:** Is the output exactly the specified format — no narrative prose,
   every line a structured key-value record?

If any check fails: fix before returning.

If `quality_threshold: maximum` and quality gate not satisfied after 2 additional
research cycles: return output with `QUALITY THRESHOLD RESULT: NOT MET` block
naming what remains unresolved. Do not silently degrade.

---

## Output Format

Every response MUST use this exact structure — three sections in this order:

**Section 1 — COMPETITIVE ANALYSIS BRIEF** (always first):
```
COMPETITIVE ANALYSIS BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━
Comparison type: [head-to-head | landscape]
Subjects: [comma-separated list]
Dimensions analyzed: [n]
Quality score: [low | medium | high]
```

**Section 2 — Structured data** (facts first, inferences second):
```
COMPARISON MATRIX
subject: [name] | dimension: [name] | rating: [strong|moderate|weak|unknown] | confidence: [high|medium|low]
[one line per subject+dimension combination]

PROFILES
subject: [name] | primary_advantage: [one phrase] | weakness: [one phrase]
[one line per subject]

WIN CONDITIONS
subject: [name] | wins_when: [condition] | loses_when: [condition]
[one line per subject]

POSITIONING GAPS
gap: [description] | benefits: [subject name]
[one line per gap, or "none"]
```

**Section 3 — Quality** (always last):
```
EVIDENCE GAPS
dimension: [name] | reason: [why it couldn't be verified]
[one line per gap, or "none"]

QUALITY THRESHOLD RESULT: [MET | NOT MET]
```

No narrative prose. No explanatory paragraphs. Every line is a structured key-value record.
The Writer specialist will transform this into prose.

---

## What You Do Not Do

- Write narrative prose — that is the Writer specialist's job
- Mix facts and inferences in the same output section
- Guess at ratings — `unknown` is always better than a fabricated `moderate`
- Make win condition claims that don't trace to the comparison matrix
- Research and analyze in parallel — stages run in sequence, always
- Predict future competitive positions — only current state based on available evidence
- Omit evidence gaps — name what couldn't be found
````

**Verify:** Read the file. Confirm frontmatter is valid YAML. Confirm all 6 pipeline stages are present. Confirm output format section shows all three sections. Confirm "What You Do Not Do" section is present.

**Commit:**
```bash
git add specialists/competitive-analysis/index.md
git commit -m "feat: add competitive analysis specialist (6-stage pipeline, AI-first output)"
```

---

## Task 4: Wire into the registry — three files, three commits

### 4a: `behaviors/specialists.yaml`

Find:
```yaml
agents:
  include:
    - specialists:researcher
    - specialists:writer
```

Replace with:
```yaml
agents:
  include:
    - specialists:researcher
    - specialists:writer
    - specialists:competitive-analysis
```

Commit:
```bash
git add behaviors/specialists.yaml
git commit -m "feat: register competitive-analysis specialist in bundle"
```

### 4b: `context/specialists-instructions.md`

Add to the **Available Specialists** list (after the writer entry):
```markdown
- **competitive-analysis** — Transforms a question or existing research into structured
  competitive intelligence. Returns a machine-parseable `CompetitiveAnalysisOutput` with
  comparison matrices, positioning gaps, and win conditions. Handles head-to-head and
  landscape modes. Output is designed for downstream agents (Writer) to consume.
```

Add to the **When to Use Each** section (after the writer block):
```markdown
**Delegate to `specialists:competitive-analysis` when:**
- Comparing two or more companies, products, or services head-to-head
- Mapping the competitive landscape for a subject ("who competes with X?")
- You need structured comparison data, not a narrative summary
- Source material from the Researcher needs to be structured into competitive intelligence
```

Add to the **Typical Chain** section:
```markdown
For competitive intelligence tasks:
1. `specialists:researcher` → gathers evidence (optional — competitive-analysis can research itself)
2. `specialists:competitive-analysis` → structures evidence into competitive intelligence
3. `specialists:writer` → transforms competitive intelligence into a brief or report
```

Commit:
```bash
git add context/specialists-instructions.md
git commit -m "docs: add competitive-analysis to specialists dispatch instructions"
```

### 4c: `README.md` (root)

Find the specialists table:
```markdown
| [researcher](specialists/researcher/) | Structured web research with source tiering, quality gates, and confidence-rated findings | v1 |
| [writer](specialists/writer/) | Transforms structured source material into polished prose with inline citations and coverage auditing | v1 |
```

Add a new row:
```markdown
| [competitive-analysis](specialists/competitive-analysis/) | Structured competitive intelligence with comparison matrices, positioning gaps, and win conditions — head-to-head and landscape modes | v1 |
```

Commit:
```bash
git add README.md
git commit -m "docs: add competitive-analysis to specialists table in README"
```

---

## Task 5: Create Epic 04 document

**Files:**
- Create: `docs/02-requirements/epics/04-competitive-analysis.md`

```markdown
# Epic 04: Competitive Analysis Specialist

**Status:** In Progress  
**Owner:** Chris Park  
**Contributors:** Chris Park  
**Last Updated:** 2026-03-02  

---

## 1. Summary

The Competitive Analysis Specialist transforms a competitive question or existing research
into structured competitive intelligence — comparison matrices, positioning gaps, and win
conditions. It handles both head-to-head comparisons (Microsoft vs. Anthropic) and landscape
analysis (who competes with Anthropic?), and accepts existing research to skip its own
research phase. Output is AI-first: machine-parseable data designed for downstream agents
to consume.

---

## 2. Problem

When a knowledge worker needs competitive intelligence, today's specialist chain produces
research findings and narrative prose — but nothing in between. The Researcher returns
sourced facts. The Writer turns those facts into a brief. What's missing is the analysis
layer: structured comparisons, explicitly identified gaps, and win/lose conditions that
make competitive intelligence actionable.

Without a dedicated competitive analysis specialist, every competitive brief is essentially
a narrative summary of research — not a structured comparison. The person reading it has
to extract the competitive picture themselves.

---

## 3. Proposed Solution

A Competitive Analysis specialist that runs a 6-stage pipeline:

1. **Parse Input** — detect mode, subjects, dimensions, research source
2. **Research** (conditional) — gather competitive evidence if no research provided
3. **Profile** — fact-based rating per subject per dimension
4. **Compare** — build comparison matrix, identify patterns and contradictions
5. **Position** — derive win conditions and positioning gaps (labeled as inferences)
6. **Synthesize + Quality Gate** — assemble AI-first output, verify facts/inference separation

Returns `CompetitiveAnalysisOutput` — structured data the Writer consumes directly.

---

## 4. User Stories

### Implemented

| # | Story | Owner | Created | Contributors | Last Updated |
|---|-------|-------|---------|--------------|--------------| 
| 04-01 | Head-to-head comparison with structured matrix | Chris Park | 2026-03-02 | - | - |
| 04-02 | Landscape analysis — discover and compare competitive field | Chris Park | 2026-03-02 | - | - |
| 04-03 | Accept existing ResearchOutput to skip research phase | Chris Park | 2026-03-02 | - | - |

**Date Format:** Always use ISO 8601 format (YYYY-MM-DD).

### Future

- ⏭️ **Dimension configuration** — caller specifies custom dimensions beyond the defaults
- ⏭️ **Competitive change tracking** — compare two snapshots of a competitive landscape over time
- ⏭️ **Confidence-filtered output** — caller sets minimum confidence threshold for matrix entries

---

## 5. Outcomes

**Success Looks Like:**
- Competitive analysis output has clearly separated facts (matrix, profiles) and inferences (win conditions, gaps)
- Every win condition traces to at least one matrix entry
- Output passes cleanly to Writer without a manual translation step
- Evidence gaps are named, not omitted

**We'll Measure:**
- Facts and inferences are never mixed in the same section
- Output format is machine-parseable line-by-line
- Chain (competitive-analysis → writer) produces a usable brief without human editing in the middle

---

## 6. Dependencies

**Requires:** `tool-web` (web_search + web_fetch), Amplifier Foundation

**Enables:**
- Any knowledge worker workflow requiring structured competitive intelligence
- Writer specialist consuming competitive analysis as source material
- Full chain: Researcher → Competitive Analysis → Writer

**Blocks:** Nothing currently blocked on this epic's completion

---

## 7. Risks & Mitigations

| Risk | Impact | Probability | Strategic Response |
|------|--------|-------------|-------------------|
| Win conditions are inferences that look like facts | M | M | Strict section separation — WIN CONDITIONS always in a separate labeled section from COMPARISON MATRIX |
| Landscape mode has no predefined subjects — specialist may miss key competitors | M | M | Require explicit competitor discovery step in Stage 2 before profiling |
| Research quality varies by subject — well-documented companies vs. obscure ones | M | H | Evidence gaps are first-class outputs; unknown ratings always preferable to low-confidence guesses |

---

## 8. Open Questions

- [ ] Should `CompetitiveAnalysisOutput` include a `COMPETITIVE BRIEF` fast-parse summary block at the top, mirroring `RESEARCH BRIEF` in ResearchOutput?
- [ ] For landscape mode, should the specialist cap the number of competitors it discovers and profiles (to avoid unbounded research)?

---

## 9. Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-03-02 | Chris Park | Initial epic |
```

**Commit:**
```bash
git add docs/02-requirements/epics/04-competitive-analysis.md
git commit -m "docs: add Epic 04 competitive analysis specialist"
```

---

## Task 6: Update `docs/README.md` Epic Status table

**File:** `docs/README.md`

Find the row:
```markdown
| 04 | Competitive Analysis | Planned | Dedicated pipeline for competitive intelligence: feature comparison, positioning gaps, structured matrices |
```

Replace with:
```markdown
| 04 | [Competitive Analysis](02-requirements/epics/04-competitive-analysis.md) | In Progress | Structured competitive intelligence with comparison matrices, positioning gaps, and win conditions — head-to-head and landscape modes |
```

**Commit:**
```bash
git add docs/README.md
git commit -m "docs: update Epic 04 status to In Progress in docs README"
```

---

## Task 7: End-to-end verification

Invoke the specialist with a test query:

```
delegate to specialists:competitive-analysis:

"Compare Notion vs Obsidian as note-taking tools for knowledge workers.
Focus on: collaboration, plugin ecosystem, pricing, learning curve, data portability."
```

**Check the output — four required verifications:**

1. **Header present:** Output starts with `COMPETITIVE ANALYSIS BRIEF` block with `Comparison type: head-to-head`, `Subjects: Notion, Obsidian`, `Dimensions analyzed: 5`

2. **Matrix is facts only:** `COMPARISON MATRIX` entries each have `subject`, `dimension`, `rating`, and `confidence` fields. No narrative sentences.

3. **WIN CONDITIONS are inferences:** `WIN CONDITIONS` section exists and is separate from `COMPARISON MATRIX`. Each entry has `wins_when` and `loses_when`.

4. **Quality section present:** Output ends with `EVIDENCE GAPS` and `QUALITY THRESHOLD RESULT`.

If all four pass: feature complete. Log result in `docs/test-log/chains/` or `docs/test-log/competitive-analysis/`.

**Push:**
```bash
git push origin main
```
