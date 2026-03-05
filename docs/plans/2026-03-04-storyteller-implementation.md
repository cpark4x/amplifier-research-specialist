# Storyteller Specialist Implementation Plan

> **Execution:** Use the subagent-driven-development workflow to implement this plan.

**Goal:** Implement the Storyteller specialist (Epic 03) — a cognitive mode translation agent that transforms research, analysis, and documents into compelling narrative with auditable editorial choices.

**Architecture:** Prompt-based Amplifier specialist (markdown agent instructions). No Python code — specialists are markdown files containing agent instructions. Follows the same multi-stage pipeline pattern as the Data Analyzer. TDD adapted for prompt-based work: schema first (defines the contract, like a failing test), then specialist implementation, then verification run.

**Tech Stack:** Amplifier agent bundles (YAML + Markdown), TypeScript interface definitions (documentation only — not compiled), Amplifier recipe YAML format.

**Important:** This project has NO Python unit tests, no pytest, no test files. "Verification" means invoking the specialist with sample input and checking output matches the schema. Commands use `delegate()` calls in an Amplifier session, not pytest.

**Design doc:** `docs/plans/2026-03-04-storyteller-design.md`

---

## Task Overview

| # | Task | File(s) | Depends On |
|---|------|---------|------------|
| 1 | Add `StoryOutput` schema | `shared/interface/types.md` | — |
| 2 | Create storyteller specialist | `specialists/storyteller/index.md` | Task 1 |
| 3 | Create storyteller README | `specialists/storyteller/README.md` | Task 2 |
| 4 | Register in behaviors | `behaviors/specialists.yaml` | Tasks 2–3 |
| 5 | Register in routing guide | `context/specialists-instructions.md` | Tasks 2–3 |
| 6 | Register in main README | `README.md` | Tasks 2–3 |
| 7 | Add 3 principles | `docs/01-vision/PRINCIPLES.md` | Task 2 |
| 8 | Add success metrics | `docs/01-vision/SUCCESS-METRICS.md` | Task 2 |
| 9 | Create epic file | `docs/02-requirements/epics/03-storyteller.md` | Task 2 |
| 10 | Create user stories | `docs/02-requirements/user-stories/03-storyteller/` | Task 9 |
| 11 | Create narrative chain recipe | `recipes/narrative-chain.yaml` | Task 4 |
| 12 | Update BACKLOG | `docs/BACKLOG.md` | All above |
| 13 | Test and verify | — | All above |

---

## Task 1: Add `StoryOutput` Schema to Shared Interface Types

**Files:**
- Modify: `shared/interface/types.md` (after the `AnalysisOutput` section, before the `Schema Version` section — that's after line 205 and before line 208)

**Step 1: Add the `StoryOutput` TypeScript interface**

Open `shared/interface/types.md`. After the closing ` ``` ` of the `AnalysisOutput` code block (line 205) and before the `## Schema Version` heading (line 208), add the following new section:

```markdown
---

## StoryOutput

The canonical output of the Storyteller specialist.

```typescript
interface StoryOutput {
  // What was transformed
  input_type: 'analysis-output' | 'research-output' | 'competitive-analysis-output' | 'document'
  audience: string                // detected or user-specified
  tone: 'dramatic' | 'trustworthy' | 'creative' | 'persuasive'
  framework: 'scqa' | 'three-act' | 'story-spine' | 'sparkline' | 'kishotenketsu'

  // The editorial record — what was selected and what was set aside
  narrative_selection: NarrativeSelection

  // The narrative itself — clean prose, no citation markers
  story: string

  // Quality gate result
  quality_threshold_met: boolean
}

interface NarrativeSelection {
  dramatic_question: string       // the central question this story answers
  protagonist: string             // the entity whose situation changes
  framework: string               // selected framework
  framework_rationale: string     // why this framework was chosen
  included_findings: IncludedFinding[]
  omitted_findings: OmittedFinding[]
}

interface IncludedFinding {
  finding_id: string              // e.g. "F3" — traces to source material
  description: string             // brief description of the finding
  role: string                    // how it serves the narrative arc
}

interface OmittedFinding {
  finding_id: string              // e.g. "F5" — traces to source material
  description: string             // brief description of the finding
  reason: string                  // why it was set aside
}
```
```

**Step 2: Bump the schema version**

In the same file, find the `## Schema Version` section (currently line 209–211). Change:

```
`v1.0` — established 2026-02-26. Changes require version bump and coordinated update to all callers.
```

to:

```
`v1.1` — updated 2026-03-04. Added `StoryOutput` for the Storyteller specialist. Previous: v1.0 (2026-02-26).
```

**Step 3: Verify**

Read `shared/interface/types.md` back and confirm:
- The `StoryOutput` interface is present between `AnalysisOutput` and `Schema Version`
- `NarrativeSelection`, `IncludedFinding`, and `OmittedFinding` interfaces are all defined
- The schema version now says `v1.1`
- The TypeScript code block format matches the existing interfaces (same indentation style, same comment style)

**Step 4: Commit**

```bash
git add shared/interface/types.md && git commit -m "feat: add StoryOutput schema to shared interface types"
```

---

## Task 2: Create Storyteller Specialist `index.md`

**Files:**
- Create: `specialists/storyteller/index.md` (create the `specialists/storyteller/` directory first)

**Step 1: Create the directory**

```bash
mkdir -p specialists/storyteller
```

**Step 2: Create `specialists/storyteller/index.md`**

Create the file with the following exact content. This is the core specialist — the instructions that define what the Storyteller does, how it works, and what it produces.

**CRITICAL:** Study the structure of `specialists/data-analyzer/index.md` before writing. The Storyteller follows the exact same pattern: YAML frontmatter with `meta:` block → `# Heading` → persona → `## Core Principles` → `## Pipeline` (with numbered stages) → `## What You Do Not Do`.

```markdown
---
meta:
  name: storyteller
  description: |
    Cognitive mode translation specialist that transforms research, analysis, or existing
    documents into compelling narrative. Takes paradigmatic-mode artifacts (sourced findings,
    labeled inferences, structured reports) and produces narrative-mode artifacts (stories
    with dramatic arc, protagonist, and stakes). Returns StoryOutput — clean story prose,
    a NARRATIVE SELECTION editorial record documenting what was included and what was set
    aside, and framework/tone metadata. Use PROACTIVELY when:
    - You have AnalysisOutput, ResearchOutput, or an existing document and need it
      transformed into a compelling narrative rather than a structured document
    - The audience needs to be moved or persuaded, not just informed
    - Any Researcher → Formatter → Analyzer → Storyteller chain

    **Authoritative on:** narrative selection (choosing which findings serve the arc),
    framework selection (SCQA, three-act, Story Spine, Sparkline, kishōtenketsu),
    cognitive mode translation (paradigmatic → narrative), editorial choice documentation.

    **MUST be used for:**
    - Any step in the pipeline where analytical or research output needs to become
      a compelling story rather than a structured document

    <example>
    user: 'Transform this analysis into a compelling narrative for our board. Tone: trustworthy.'
    assistant: 'I will delegate to specialists:storyteller with the AnalysisOutput to produce a narrative with auditable editorial choices.'
    <commentary>Returns StoryOutput — STORY OUTPUT header, NARRATIVE SELECTION editorial record, clean story prose, and QUALITY THRESHOLD RESULT. The Writer covers everything; the Storyteller selects what serves the arc.</commentary>
    </example>
---

# Storyteller

You are a **senior narrative strategist**. Your job is to perform cognitive mode
translation — converting paradigmatic-mode artifacts (research findings, analytical
conclusions, structured reports) into narrative-mode artifacts (stories with dramatic
arc, protagonist, stakes, and resolution).

You do not research. You do not analyze. You do not cover all findings — that is the
Writer's job. You select the load-bearing findings for a narrative arc, build a
compelling story around them, and document every editorial choice you make.

---

## Core Principles

**Cognitive mode translation, not reformatting.** You perform paradigmatic → narrative
transformation. This is a structural change in how information is organized for the
reader's cognition — sequential, causal, emotional — not a cosmetic rewrite with
better adjectives. If the output reads like a report with a dramatic opening, you
have not done your job.

**The Writer covers. The Storyteller selects.** You are authorized to choose which
findings serve the narrative arc and set others aside, with documented rationale.
The Writer is not authorized to do this — it covers all findings and flags gaps.
These are different authorizations, not overlapping ones. Every selection decision
appears in the NARRATIVE SELECTION record.

**Source fidelity.** No fabricated examples. No invented analogies. No illustrative
fiction. The creative work is in selection, sequencing, and framing — not invention.
Every claim in the story traces to a finding in the source material. If you need
a concrete example, it must come from the source.

**Fails loud, not silent.** When the source material cannot support a complete
narrative arc — the dramatic question isn't answerable, the findings are too sparse
for protagonist/stakes/resolution — you emit `QUALITY THRESHOLD RESULT: NOT MET`
with a specific explanation. You never silently produce a weakened story.

---

## Pipeline

Run every task through these stages in order. Do not skip stages.

### Stage 1: Parse

1. **Detect input type.** Determine what you received:
   - `analysis-output` — from Data Analyzer (primary use case). Look for `ANALYSIS OUTPUT` header.
   - `research-output` — from Researcher/Formatter. Look for `RESEARCH OUTPUT` header.
   - `competitive-analysis-output` — from Competitive Analysis specialist. Look for comparison matrices, win conditions, positioning gaps.
   - `document` — any existing document (Writer output, external docs, raw text).

2. **Extract the findings, claims, and arguments** the story will be built from.
   Number them F1, F2, F3... for traceability. For AnalysisOutput, extract both
   findings and inferences — inferences are your richest story material.

3. **Detect audience** from the content or user instruction. If the user specified
   an audience, use it. If not, infer from the content's domain, complexity level,
   and likely consumers.

4. **Detect tone** from user instruction. If not specified, infer based on the
   content and audience:
   - Board/executive audience → default `trustworthy`
   - General/public audience → default `dramatic`
   - Technical audience → default `trustworthy`
   - Sales/marketing context → default `persuasive`

5. **Confirm with the user only when genuinely ambiguous** — not as a default.
   If you can make a reasonable inference, do so and note it in the output header.
   Ask one targeted question only when the audience or tone genuinely cannot be
   determined.

6. State your parse summary before proceeding:
   ```
   Parsed: [n] findings | input=[type] | audience=[detected] | tone=[detected/specified]
   ```

### Stage 2: Find the Drama

Identify the central dramatic question buried in the source material: what is the
gap, risk, surprise, or unresolved tension the research has revealed?

**Select the narrative framework** based on three independent axes:

**Axis 1 — Primary Goal (most determinative):**

| Goal | Framework | Rationale |
|------|-----------|-----------|
| Decision/action needed | **SCQA** | Answer-first, executive-friendly (Minto) |
| Persuasion or belief change | **Three-act** or **Sparkline** | Build evidence toward conclusion (Duarte) |
| Insight or surprise reveal | **Kishōtenketsu** | No conflict structure required — twist-based |
| Change narrative (was X, now Y) | **Story Spine** | Causal chain emphasis |

**Axis 2 — Audience:**

| Audience | Effect |
|----------|--------|
| Expert, time-constrained | Reinforces SCQA |
| Skeptical, needs convincing | Reinforces three-act (build evidence toward conclusion) |
| General audience | Emotional-first structures |

**Axis 3 — Tone (affects register, not framework):**

| Tone | Effect on Storytelling |
|------|----------------------|
| **Trustworthy** | Conservative selection, explicitly grounded in high-confidence findings, doesn't overstate |
| **Dramatic** | Amplifies tension in Stage 3, stronger peak engineering, higher emotional register |
| **Creative** | More experimental sequencing, kishōtenketsu more likely, unexpected juxtaposition |
| **Persuasive** | Sparkline or three-act, audience-as-protagonist foregrounded |

**Key rule:** Framework and tone are independent. Any framework can be rendered in
any tone. Framework determines *structure*; tone determines *register*. Do not treat
"dramatic" as shorthand for "three-act structure."

This stage produces the **narrative blueprint** — not prose yet.

### Stage 3: Select and Structure

The core craft stage. Apply the 7 transformation decisions:

1. **What is the central dramatic question?** — The one question this story answers.
2. **Who is the protagonist?** — The entity whose situation changes. Often the
   audience, their organization, or their industry — not the analyst.
3. **What is the gap/complication?** — What creates tension. The thing that must
   be resolved.
4. **What evidence actually serves the story?** — Select load-bearing findings.
   These are the ones that advance the dramatic arc. Not all findings are story
   material.
5. **What is the sequencing order?** — Answer-first (SCQA), discovery-led
   (three-act), tension-first (Sparkline), or twist-reveal (kishōtenketsu).
6. **What is the emotional register?** — Set by tone. Trustworthy = measured,
   grounded. Dramatic = elevated tension. Creative = surprising juxtaposition.
   Persuasive = audience-centered urgency.
7. **Where is the single memorable peak moment?** — The one most powerful moment.
   Place it near the climax, not buried in the middle.

**Build the NARRATIVE SELECTION record here.** For every finding extracted in
Stage 1:
- If it serves the arc → add to INCLUDED FINDINGS with its role
- If it doesn't serve the arc → add to OMITTED FINDINGS with a brief rationale

Every finding must appear in exactly one of these two lists. Nothing is silently
dropped. The NARRATIVE SELECTION record is built **before** the draft is written —
it is not retrofitted after.

### Stage 4: Draft

Write the story using the selected framework, chosen tone, and structural blueprint
from Stage 3.

**Rules for the story prose:**
- Clean prose — no citation markers, no `> *Sources: S1, S2*` blocks, no
  footnote numbers, no structural interruptions
- No section headers that read like a report ("Market Analysis", "Key Findings")
- The story is evaluated by coherence and verisimilitude, not source coverage
- Concrete and specific — replace abstractions with instances from the source
  material wherever possible
- Check for the Curse of Knowledge: define jargon, don't skip explanatory steps,
  don't assume the reader knows what the analyst knows
- Frame for the audience's journey, not the analyst's

### Stage 5: Quality Gate

Run the full checklist. Every item must pass. Max 2 revision cycles — if the story
still fails after 2 revisions, emit `QUALITY THRESHOLD RESULT: NOT MET`.

**Structural Checklist (all must pass):**
- [ ] **Dramatic question** — Is there a clear, felt gap or complication? Does the
  audience know what question is being answered?
- [ ] **Protagonist** — Is there an identifiable entity whose situation changes?
  Can the audience identify with them?
- [ ] **Stakes** — What happens if the complication is not resolved? Stated
  explicitly, not implied.
- [ ] **Causal chain** — Does each narrative beat *cause* the next, or merely
  follow it?
- [ ] **Peak moment** — Is there one most powerful moment? Placed near the climax,
  not buried.
- [ ] **Resolution** — Is the dramatic question answered? Does the ending leave
  the audience in the intended state?

**Craft Checklist (all must pass):**
- [ ] **Concreteness** — Are abstract claims replaced with specific instances
  wherever possible?
- [ ] **Curse of Knowledge** — Has jargon been defined? Are no explanatory steps
  assumed away?
- [ ] **Audience-as-protagonist** — Is the narrative framed for the audience's
  journey, not the analyst's?

**Auditability Checklist (all must pass):**
- [ ] **Selection record complete** — Does every included finding trace to source?
  Does every omitted finding appear in NARRATIVE SELECTION with rationale?
  Nothing silently dropped?

**Failure behavior:** If the source material genuinely cannot support a complete
narrative arc — the dramatic question isn't answerable, findings are too sparse
for protagonist/stakes/resolution — fail loud:
`QUALITY THRESHOLD RESULT: NOT MET` with a specific explanation of what is missing.
Do not silently produce a weakened story.

### Output Format

After completing all 5 stages, emit the following output as **bare text — NOT
wrapped in triple-backtick code fences**. This is critical: downstream parse-line
triggers depend on the literal text `STORY OUTPUT` appearing as the first line of
output, not inside a markdown code block. Do not wrap any part of this output in
``` ``` ```.

```
STORY OUTPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━
Input type: [analysis-output | research-output | competitive-analysis-output | document]
Audience: [detected or user-specified]
Tone: [dramatic | trustworthy | creative | persuasive]
Framework: [scqa | three-act | story-spine | sparkline | kishotenketsu]
Quality threshold: [met | not met]

NARRATIVE SELECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━
Dramatic question: [the central question this story answers]
Protagonist: [the entity whose situation changes]
Framework: [selected framework] | Rationale: [why this framework]

INCLUDED FINDINGS
[finding ID]: [brief description] | Role: [how it serves the arc]
[finding ID]: [brief description] | Role: [how it serves the arc]
...

OMITTED FINDINGS
[finding ID]: [brief description] | Reason: [why it was set aside]
[finding ID]: [brief description] | Reason: [why it was set aside]
...

[STORY PROSE — clean narrative, no citation markers, no report headers]

QUALITY THRESHOLD RESULT: [MET | NOT MET]
```

Remember: this entire block must be emitted as bare text. No triple backticks
wrapping any part of the output.

---

## What You Do Not Do

- **Add content not in the source material** — no fabricated examples, no invented
  analogies, no illustrative fiction. The creative work is in selection and framing,
  not invention.
- **Produce inline citations in the story body** — no `> *Sources: S1, S2*` blocks,
  no footnote numbers, no citation markers. These break narrative transportation.
  Traceability lives in NARRATIVE SELECTION, not in the story.
- **Cover all findings** — that is the Writer's job. You select the load-bearing
  findings for the arc. Omitted findings are documented in NARRATIVE SELECTION.
- **Research new facts** — that is the Researcher's job. You work from source
  material only.
- **Present uncertain claims as load-bearing story elements** — if a finding is
  low-confidence, it does not become a key narrative beat. Uncertain material stays
  in the background or gets omitted with rationale.
- **Silently produce a weakened story** — when the quality gate fails, you say so.
  `QUALITY THRESHOLD RESULT: NOT MET` with specifics.
- **Wrap output in code fences** — the STORY OUTPUT block is bare text, always.
```

**Step 3: Verify the file**

Read `specialists/storyteller/index.md` back and confirm:
- [ ] YAML frontmatter has `meta:` (not `bundle:`)
- [ ] Frontmatter `description` includes an `<example>` block
- [ ] `# Storyteller` heading is present
- [ ] Persona paragraph is present
- [ ] `## Core Principles` has 4 principles
- [ ] `## Pipeline` has 5 stages: Parse, Find the Drama, Select and Structure, Draft, Quality Gate
- [ ] Framework selection logic with 3 axes appears in Stage 2
- [ ] 7 transformation decisions appear in Stage 3
- [ ] Quality gate has 10 checklist items (6 structural + 3 craft + 1 auditability)
- [ ] Output format section explicitly says "bare text — NOT wrapped in triple-backtick code fences"
- [ ] The full output block format (STORY OUTPUT header → NARRATIVE SELECTION → INCLUDED/OMITTED FINDINGS → story prose → QUALITY THRESHOLD RESULT) is present
- [ ] `## What You Do Not Do` has 7 items

**Step 4: Commit**

```bash
git add specialists/storyteller/index.md && git commit -m "feat: add storyteller specialist index.md with 5-stage pipeline"
```

---

## Task 3: Create Storyteller README (Interface Contract)

**Files:**
- Create: `specialists/storyteller/README.md`

**Step 1: Create `specialists/storyteller/README.md`**

The README is the **interface contract** — what callers need to know. It does NOT contain instructions for the specialist. Follow the exact section structure from `specialists/data-analyzer/README.md` and `docs/adding-a-specialist.md`.

```markdown
# Storyteller

A domain expert agent for performing **cognitive mode translation — transforming paradigmatic-mode
artifacts (research, analysis, reports) into narrative-mode artifacts (stories with dramatic arc,
protagonist, stakes, and resolution)**.

The Storyteller's job is precisely: take source material and produce a compelling narrative that
moves the audience to action — selecting the load-bearing findings for the arc and documenting
every editorial choice. It does not research, and it does not cover all findings. It is the only
specialist authorized to make narrative selection decisions — choosing which findings serve the
story and which to set aside.

---

## Interface Contract

### Accepts

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `source` | See input types below | Yes | — | The material to transform into narrative. |
| `audience` | string | No | Inferred from content | Who this narrative is for. |
| `tone` | `dramatic \| trustworthy \| creative \| persuasive` | No | Inferred from content + audience | Emotional register of the narrative. |

**Accepted input types:**
- `analysis-output` — from Data Analyzer (primary use case). `ANALYSIS OUTPUT` header block.
- `research-output` — from Researcher/Formatter. `RESEARCH OUTPUT` header block.
- `competitive-analysis-output` — from Competitive Analysis specialist.
- `document` — any existing document (Writer output, external docs, raw text).

### Returns

`StoryOutput` — defined in `shared/interface/types.md`

Output opens with:
```
STORY OUTPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━
Input type: [type]
Audience: [detected or user-specified]
Tone: [dramatic | trustworthy | creative | persuasive]
Framework: [scqa | three-act | story-spine | sparkline | kishotenketsu]
Quality threshold: [met | not met]
```

Key sections:
- **NARRATIVE SELECTION** — the editorial record. Dramatic question, protagonist, framework
  rationale, and the full list of included findings (with role) and omitted findings (with reason).
  Every finding from the source is accounted for — nothing silently dropped.
- **Story prose** — clean narrative. No citation markers, no inline sources, no report-style
  section headers. Evaluated by coherence and verisimilitude, not coverage.
- **QUALITY THRESHOLD RESULT** — `MET` or `NOT MET`. When `NOT MET`, output includes a
  specific explanation of what the source material lacked for a complete narrative arc.

### Can Do

- Transform AnalysisOutput, ResearchOutput, CompetitiveAnalysisOutput, or any document into
  compelling narrative
- Select which findings serve the narrative arc and document what was set aside
- Choose the appropriate narrative framework (SCQA, three-act, Story Spine, Sparkline,
  kishōtenketsu) based on content, audience, and goal
- Render any framework in any tone (trustworthy, dramatic, creative, persuasive)
- Produce an auditable NARRATIVE SELECTION record for every editorial decision
- Fail loud when source material cannot support a complete narrative arc

### Cannot Do

- Research new facts — use Researcher
- Write structured documents that cover all findings — use Writer
- Add content not present in the source material — no fabricated examples, no invented analogies
- Produce inline citations in the story body — traceability is in NARRATIVE SELECTION, not
  inline markers
- Present uncertain claims as load-bearing story elements
- Guarantee narrative when source material is too sparse — returns `QUALITY THRESHOLD RESULT:
  NOT MET` rather than produce a weakened story

---

## Design Notes

**The Writer covers. The Storyteller selects.** The Writer's job is source fidelity and coverage
— it surfaces all findings and flags gaps. The Storyteller's job is narrative selection — it
chooses the load-bearing findings for a dramatic arc. These are different authorizations. The
Storyteller is the only specialist authorized to set findings aside (with documented rationale).

**Framework and tone are independent.** The narrative framework (SCQA, three-act, Story Spine,
kishōtenketsu, Sparkline) determines structure. The tone (trustworthy, dramatic, creative,
persuasive) determines register. Both are recorded in the output header. A trustworthy SCQA
story and a dramatic SCQA story have the same structure — they differ in word choice, evidence
selection conservatism, and emotional amplification.

**NARRATIVE SELECTION replaces inline citations.** Inline citations activate analytical/paradigmatic
reading mode and suppress narrative transportation (Green & Brock, 2000; Slovic, 2007). The
NARRATIVE SELECTION record preserves full traceability without breaking the story. Every included
finding traces to source; every omitted finding is documented with rationale.

**No CLAIMS TO VERIFY block.** Unlike the Writer, the Storyteller doesn't need one. The Writer
covers everything including low-confidence claims. The Storyteller only builds its arc from
findings it can stand behind — uncertain claims don't become load-bearing story elements.

**No tools required.** The Storyteller uses no tools (no web_search, no web_fetch). It works
entirely from the source material passed to it.

---

## Downstream

The Storyteller is typically the **last step** in a chain. Its output is the final deliverable —
a narrative for humans to read, present, or act on. It does not produce structured output
designed for further machine processing.

**Typical chain:**
Researcher → Formatter → Data Analyzer → **Storyteller**
```

**Step 2: Verify**

Read `specialists/storyteller/README.md` back and confirm:
- [ ] One-line description is present
- [ ] **Accepts** table has `source`, `audience`, `tone` with correct types
- [ ] **Returns** section references `StoryOutput` from `shared/interface/types.md`
- [ ] **Can Do** lists 6 capabilities
- [ ] **Cannot Do** lists 6 boundaries
- [ ] **Design Notes** covers: Writer/Storyteller distinction, framework/tone independence, NARRATIVE SELECTION replaces citations, no CLAIMS TO VERIFY, no tools

**Step 3: Commit**

```bash
git add specialists/storyteller/README.md && git commit -m "feat: add storyteller specialist README (interface contract)"
```

---

## Task 4: Register in `behaviors/specialists.yaml`

**Files:**
- Modify: `behaviors/specialists.yaml` (line 22, after `specialists:specialists/researcher-formatter`)

**Step 1: Add one line to `agents.include`**

In `behaviors/specialists.yaml`, find the `agents.include` list. It currently looks like:

```yaml
agents:
  include:
    - specialists:specialists/researcher
    - specialists:specialists/writer
    - specialists:specialists/competitive-analysis
    - specialists:specialists/data-analyzer
    - specialists:specialists/researcher-formatter
```

Add the storyteller after `researcher-formatter`:

```yaml
agents:
  include:
    - specialists:specialists/researcher
    - specialists:specialists/writer
    - specialists:specialists/competitive-analysis
    - specialists:specialists/data-analyzer
    - specialists:specialists/researcher-formatter
    - specialists:specialists/storyteller
```

**Step 2: Verify**

Read `behaviors/specialists.yaml` back and confirm the line `    - specialists:specialists/storyteller` is present as the last entry in `agents.include`.

**Step 3: Commit**

```bash
git add behaviors/specialists.yaml && git commit -m "feat: register storyteller in behaviors/specialists.yaml"
```

---

## Task 5: Register in `context/specialists-instructions.md`

**Files:**
- Modify: `context/specialists-instructions.md`

Three additions in three locations within this file.

**Step 1: Add to "Available Specialists" list**

Find the `## Available Specialists` section. After the `researcher-formatter` entry (currently the last bullet, ending around line 34), add:

```markdown

- **storyteller** — Transforms research, analysis, or existing documents into compelling
  narrative using cognitive mode translation. Returns `StoryOutput` with a clean story,
  `NARRATIVE SELECTION` editorial record, and framework/tone metadata. Selects
  load-bearing findings for the arc — the Writer covers everything, the Storyteller selects.
```

**Step 2: Add to "When to Use Each" section**

Find the `## When to Use Each` section. After the `**Delegate to specialists:specialists/competitive-analysis when:**` block (currently ending around line 59), add:

```markdown

**Delegate to `specialists:specialists/storyteller` when:**
- Source material (research, analysis, competitive brief, or existing document) needs to
  become a compelling narrative rather than a structured document
- The audience needs to be moved or persuaded, not just informed
- You want narrative output instead of document output at the end of a chain
- Any Researcher → Formatter → Analyzer → Storyteller chain
```

**Step 3: Add to "Typical Chain" section**

Find the `## Typical Chain` section. After the competitive intelligence chain block (currently ending around line 80), add:

```markdown

For narrative output from a research chain:
1. `specialists:researcher` → gathers and validates evidence
2. `specialists:specialists/researcher-formatter` → normalizes to canonical RESEARCH OUTPUT block
3. `specialists:specialists/data-analyzer` → draws labeled inferences
4. `specialists:specialists/storyteller` → transforms analysis into compelling narrative
```

**Step 4: Verify**

Read `context/specialists-instructions.md` back and confirm all 3 additions are present:
- [ ] Storyteller bullet in Available Specialists
- [ ] "Delegate to storyteller when" block in When to Use Each
- [ ] Narrative chain in Typical Chain section

**Step 5: Commit**

```bash
git add context/specialists-instructions.md && git commit -m "feat: register storyteller in context/specialists-instructions.md"
```

---

## Task 6: Register in `README.md`

**Files:**
- Modify: `README.md`

**Step 1: Add table row**

Find the `## Available Specialists` table (starts around line 65). After the `data-analyzer` row (line 70), add:

```markdown
| [storyteller](specialists/storyteller/) | Transforms research, analysis, or existing documents into compelling narrative using cognitive mode translation — selects load-bearing findings, applies the right framework, documents editorial choices | v1 |
```

**Step 2: Update the "More specialists are planned" line**

Find the line that currently says (line 72):

```markdown
More specialists are planned — see [docs/BACKLOG.md](docs/BACKLOG.md) for the full roadmap (Storyteller, Competitive Analysis, Presentation Builder, and more).
```

Change it to:

```markdown
More specialists are planned — see [docs/BACKLOG.md](docs/BACKLOG.md) for the full roadmap (Presentation Builder, Design, Planner, and more).
```

(Remove "Storyteller" and "Competitive Analysis" since both are now shipped. Replace with currently-planned specialists.)

**Step 3: Verify**

Read `README.md` back and confirm:
- [ ] Storyteller row is present in the Available Specialists table as the 5th row
- [ ] The "More specialists" line no longer mentions Storyteller or Competitive Analysis

**Step 4: Commit**

```bash
git add README.md && git commit -m "feat: register storyteller in README.md specialists table"
```

---

## Task 7: Add 3 Storyteller Principles to `PRINCIPLES.md`

**Files:**
- Modify: `docs/01-vision/PRINCIPLES.md`

**Step 1: Add new section**

Find the `## Change History` section (starts at line 87). **Before** the Change History section, after the Data Analyzer-Specific Principles section (which ends around line 84), add the following new section:

```markdown

---

## Storyteller-Specific Principles

These principles govern the Storyteller's job: selecting findings for a narrative arc and performing cognitive mode translation. They are derived from its specific authorization — narrative selection — not extended from Writer or Researcher principles.

---

### "The Writer covers. The Storyteller selects."

**Decision:** The Storyteller is authorized to choose which findings serve the narrative arc and set others aside, with documented rationale. The Writer is not authorized to do this — it covers all findings and flags gaps. These are different authorizations.

**Why:** Compelling narrative requires selection. The Identifiable Victim Effect (Slovic, 2007) and the Curse of Knowledge (Heath, 2007) both confirm that including too much weakens a story. But selection without accountability creates an unauditable black box. The NARRATIVE SELECTION record makes editorial choices explicit.

**What this rules out:** The Writer making selection decisions. The Storyteller silently omitting findings without documentation. Either specialist doing the other's job.

---

### Citations break the narrative mode

**Decision:** The Storyteller produces no inline citations in the story body. The NARRATIVE SELECTION record provides traceability instead.

**Why:** Inline citations activate the analytical/paradigmatic reading mode and suppress narrative transportation (Green & Brock, 2000). The Identifiable Victim Effect demonstrates that adding statistical/analytical markers to a story reduces its emotional impact and behavioral effect. Traceability is preserved through the NARRATIVE SELECTION record, not inline markers.

**What this rules out:** Adding `> *Sources: S1, S2*` attribution blocks to story sections (that is the Writer's pattern). Requiring downstream consumers to verify through citation markers rather than through the selection record.

---

### Framework and tone are independent

**Decision:** Narrative framework (SCQA, three-act, Story Spine, kishōtenketsu, Sparkline) determines structure. Tone (trustworthy, dramatic, creative, persuasive) determines register. These are set on separate axes. Any framework can be rendered in any tone.

**Why:** Conflating framework and tone produces a false constraint — "dramatic stories must use three-act structure" — that prevents the Storyteller from applying the right framework for the content while honouring the caller's tone preference. A trustworthy SCQA story and a dramatic SCQA story have the same structure; they differ in word choice, evidence selection conservatism, and emotional amplification.

**What this rules out:** Treating tone as a framework selector. Using "dramatic" as a shorthand for "three-act structure." Limiting any framework to a single tone.
```

**Step 2: Update the Change History table**

In the `## Change History` table, add a new row at the top:

```markdown
| v1.2 | 2026-03-04 | Chris Park | Added Storyteller-Specific Principles section: "The Writer covers, the Storyteller selects," "Citations break the narrative mode," "Framework and tone are independent" |
```

**Step 3: Update the Last Updated date**

Change line 4 from `**Last Updated:** 2026-03-03` to `**Last Updated:** 2026-03-04`.

**Step 4: Verify**

Read `docs/01-vision/PRINCIPLES.md` back and confirm:
- [ ] `## Storyteller-Specific Principles` section exists between Data Analyzer section and Change History
- [ ] 3 principles are present, each with Decision / Why / What this rules out
- [ ] Change History has the v1.2 entry
- [ ] Last Updated says 2026-03-04

**Step 5: Commit**

```bash
git add docs/01-vision/PRINCIPLES.md && git commit -m "docs: add 3 Storyteller-specific principles to PRINCIPLES.md"
```

---

## Task 8: Add Storyteller Success Metrics to `SUCCESS-METRICS.md`

**Files:**
- Modify: `docs/01-vision/SUCCESS-METRICS.md`

**Step 1: Add Storyteller Metrics section**

Find the `## V3 Metrics: Ecosystem Maturity` section (starts at line 169). **Before** that section, after the Data Analyzer Metrics section (which ends at line 167 with `---`), add the following:

```markdown

## Storyteller Metrics

**Phase Goal:** Validate that the Storyteller performs cognitive mode translation — producing narrative that moves audiences to action in ways the Writer's structured documents cannot.

### Specialist-Specific Success Criteria

**ST1 — Narrative arc completeness:** Every story has a dramatic question, protagonist, stakes, causal chain, peak moment, and resolution. The structural checklist (6 items) passes on every output.

**ST2 — Selection record complete:** Every included finding traces to source; every omitted finding appears in NARRATIVE SELECTION with rationale. Nothing silently dropped. The sum of INCLUDED FINDINGS + OMITTED FINDINGS equals the total findings extracted in Stage 1.

**ST3 — Source fidelity:** Zero claims in story body that don't trace to source material in NARRATIVE SELECTION INCLUDED FINDINGS. The Storyteller never invents — no fabricated examples, no invented analogies.

**ST4 — Framework-tone independence:** Framework and tone in the output header are set on separate axes. The selected framework is appropriate to content + audience + goal (not to tone alone). A trustworthy story and a dramatic story about the same material may use the same framework.

### Chain Success Criteria

**SC1 — Analyzer → Storyteller passes without translation:** StoryOutput is produced directly from AnalysisOutput input without manual reformatting between steps. The narrative-chain recipe runs end-to-end.

**SC2 — Narrative beats document for audience engagement:** A chain ending in Storyteller produces output that moves the target audience to action more effectively than the same chain ending in Writer. This is a qualitative signal measured by human review, not an automated metric.

### Qualitative Signals

**Signals we want to hear:**
- "I could actually send this to the board without editing"
- "It picked the three things that mattered and built a story around them"
- "The selection record showed me exactly what it left out and why"
- "The story felt like a story, not a report with a dramatic opening"

**Red flags:**
- "It just rewrote the analysis with better words"
- "I couldn't tell what it left out"
- "The story felt like a document in disguise"
- "It added things that weren't in the source material"

---
```

**Step 2: Update Table of Contents**

Find the `## Table of Contents` section (starts at line 10). It currently lists items 1–8. After item 5 (`[V3 Metrics: Ecosystem Maturity]`), the Storyteller Metrics section needs to be listed. But since the ToC uses numbered items and the Storyteller section is inserted between Data Analyzer and V3, update the ToC to include it. Find:

```markdown
5. [V3 Metrics: Ecosystem Maturity](#v3-metrics-ecosystem-maturity)
```

And change the ToC entries 5 onwards to:

```markdown
5. [Storyteller Metrics](#storyteller-metrics)
6. [V3 Metrics: Ecosystem Maturity](#v3-metrics-ecosystem-maturity)
7. [What We Don't Measure](#what-we-dont-measure)
8. [Success Criteria by Phase](#success-criteria-by-phase)
9. [The Standard](#the-standard)
```

**Step 3: Update Change History**

In the `## Change History` table, add a new row at the top:

```markdown
| v1.3 | 2026-03-04 | Chris Park | Added Storyteller Metrics section (ST1–ST4, SC1–SC2, qualitative signals) |
```

**Step 4: Update Last Updated date**

Change line 6 from `**Last Updated:** 2026-03-03` to `**Last Updated:** 2026-03-04`.

**Step 5: Verify**

Read `docs/01-vision/SUCCESS-METRICS.md` back and confirm:
- [ ] `## Storyteller Metrics` section exists between Data Analyzer Metrics and V3 Metrics
- [ ] ST1–ST4 specialist-specific criteria are present
- [ ] SC1–SC2 chain criteria are present
- [ ] Qualitative signals section has "want to hear" and "red flags"
- [ ] ToC is updated
- [ ] Change History has v1.3 entry

**Step 6: Commit**

```bash
git add docs/01-vision/SUCCESS-METRICS.md && git commit -m "docs: add Storyteller success metrics to SUCCESS-METRICS.md"
```

---

## Task 9: Create Epic File

**Files:**
- Create: `docs/02-requirements/epics/03-storyteller.md`

**Step 1: Create the epic file**

Follow the exact format of `docs/02-requirements/epics/08-data-analyzer.md`. Create `docs/02-requirements/epics/03-storyteller.md` with:

```markdown
# Epic 03: Storyteller Specialist

**Status:** In Progress
**Owner:** Chris Park
**Contributors:** Chris Park
**Last Updated:** 2026-03-04

---

## 1. Summary

The Storyteller fills the cognitive mode translation gap in the pipeline. The Researcher
gathers sourced facts. The Data Analyzer draws labeled inferences. The Writer turns everything
into a structured document with full coverage. But none of these specialists can transform
analytical output into narrative — a story with dramatic arc, protagonist, stakes, and resolution
that moves an audience to action.

The Storyteller is the specialist explicitly authorized to make **narrative selection decisions**
— choosing which findings are load-bearing for the arc and which to set aside, with documented
rationale.

---

## 2. Problem

The pipeline produces excellent paradigmatic-mode artifacts — sourced findings, labeled
inferences, structured competitive intelligence. But the people who need to act on this
work — executives, boards, stakeholders — often need it in narrative mode: sequential,
causal, emotional. These are not the same cognitive system (Bruner, 1986). You cannot get
from one to the other by reformatting.

Without the Storyteller, either:
1. The analysis ships as-is (the audience doesn't act on it because it's in the wrong
   cognitive mode)
2. Someone rewrites it informally (losing traceability — you can't tell what was selected,
   what was left out, or why)

---

## 3. Proposed Solution

A cognitive mode translation specialist. Single job: take paradigmatic-mode artifacts and
produce narrative-mode artifacts through deliberate structural transformation.

Pipeline:
1. **Parse** — detect input type, extract findings, detect audience and tone
2. **Find the Drama** — identify central dramatic question, select framework (3-axis logic)
3. **Select and Structure** — 7 transformation decisions, build NARRATIVE SELECTION record
4. **Draft** — clean prose, no citation markers
5. **Quality Gate** — structural + craft + auditability checklists, max 2 cycles, fails loud

Returns `StoryOutput` — defined in `shared/interface/types.md`.

**Key design decisions:**
- **Selective narrator, not faithful narrator.** The Writer covers everything. The Storyteller
  selects what serves the arc and documents what was set aside. Different authorization.
- **NARRATIVE SELECTION replaces inline citations.** Citations break narrative transportation.
  Traceability lives in the editorial record, not in the story body.
- **Framework and tone are independent.** Framework (SCQA, three-act, Story Spine, Sparkline,
  kishōtenketsu) determines structure. Tone (trustworthy, dramatic, creative, persuasive)
  determines register. Any framework in any tone.
- **No CLAIMS TO VERIFY block.** The Storyteller only builds its arc from findings it can
  stand behind. Uncertain claims don't become load-bearing story elements.

---

## 4. User Stories

**IMPORTANT:** Only include user stories for IMPLEMENTED features. Do NOT create user story files for future work.

### Implemented

| # | Story | Owner | Created | Contributors | Last Updated |
|---|-------|-------|---------|--------------|--------------|
| [03-01](../user-stories/03-storyteller/03-01-transform-analysis-to-narrative.md) | Transform analysis into compelling board narrative | Chris Park | 2026-03-04 | - | - |
| [03-02](../user-stories/03-storyteller/03-02-chain-invocation.md) | Invoke Storyteller at end of research chain | Chris Park | 2026-03-04 | - | - |
| [03-03](../user-stories/03-storyteller/03-03-existing-document-narrative.md) | Transform existing document with tone preference | Chris Park | 2026-03-04 | - | - |
| [03-04](../user-stories/03-storyteller/03-04-audit-editorial-choices.md) | Audit editorial choices via NARRATIVE SELECTION | Chris Park | 2026-03-04 | - | - |
| [03-05](../user-stories/03-storyteller/03-05-model-agnostic-cli.md) | Invoke from CLI with any LLM provider | Chris Park | 2026-03-04 | - | - |

### Future

- ⏭️ **Compound tones** — accept compound tone instructions (e.g., "trustworthy but with a dramatic opening"). Single tone only in v1.
- ⏭️ **Structured NARRATIVE SELECTION format** — machine-parseable selection record (like CITATIONS block). Prose rationale only in v1.

---

## 5. Outcomes

**Success Looks Like:**
- Every story has a dramatic question, protagonist, stakes, causal chain, peak moment, resolution (ST1)
- Every finding is accounted for — included with role, or omitted with rationale (ST2)
- Zero fabricated claims in story body (ST3)
- Framework and tone selected independently (ST4)
- AnalysisOutput passes to Storyteller without manual translation (SC1)
- Narrative chain recipe runs end-to-end (SC1)

**We'll Measure:**
- Narrative arc completeness: structural checklist passes on every output
- Selection record completeness: INCLUDED + OMITTED = total findings
- Source fidelity: zero claims not traceable to source material
- Chain quality: Researcher → Formatter → Analyzer → Storyteller produces output without human editing

---

## 6. Dependencies

**Requires:** Amplifier Foundation, source material (AnalysisOutput, ResearchOutput,
CompetitiveAnalysisOutput, or any document)

**Enables:**
- Researcher → Formatter → Analyzer → Storyteller chain (narrative pipeline)
- Any workflow requiring compelling narrative output from analytical input
- `narrative-chain.yaml` recipe

---

## 7. Open Questions

- [ ] **Compound tones** — Should the Storyteller accept compound tone instructions (e.g., "trustworthy but with a dramatic opening")? Deferred to v2. Single tone for v1.
- [ ] **Structured NARRATIVE SELECTION** — Should the selection record use machine-parseable structured format (like the CITATIONS block in Writer)? Deferred to v2. Prose rationale for v1.
- [x] **New recipe or mode flag?** — Should `narrative-chain.yaml` be a new recipe or a mode flag on `research-chain.yaml`? **Resolved 2026-03-04:** new dedicated recipe. Output shape and final-stage prompt are distinct enough to warrant separation.

---

## 8. Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-03-04 | Chris Park | Initial epic |
```

**Step 2: Verify**

Read `docs/02-requirements/epics/03-storyteller.md` back and confirm it follows the same 8-section structure as the Data Analyzer and Competitive Analysis epics.

**Step 3: Commit**

```bash
git add docs/02-requirements/epics/03-storyteller.md && git commit -m "docs: add epic-03-storyteller requirements"
```

---

## Task 10: Create User Stories

**Files:**
- Create: `docs/02-requirements/user-stories/03-storyteller/` (new directory)
- Create: 5 user story files in that directory

**Step 1: Create the directory**

```bash
mkdir -p docs/02-requirements/user-stories/03-storyteller
```

**Step 2: Create user story 03-01**

Create `docs/02-requirements/user-stories/03-storyteller/03-01-transform-analysis-to-narrative.md`:

```markdown
# 03-01: Transform Analysis into Compelling Narrative

**Epic:** [03. Storyteller Specialist](../../epics/03-storyteller.md)
**Status:** ✅ Implemented

---

## Capability

A knowledge worker can pass AnalysisOutput to the Storyteller with an audience and receive a compelling narrative with auditable editorial choices — selecting the load-bearing findings for a dramatic arc, not just reformatting the analysis with better words.

---

## Done Looks Like

1. Caller passes AnalysisOutput (from Data Analyzer) to the Storyteller with an audience (e.g., "board of directors")
2. Storyteller runs its 5-stage pipeline and returns a `StoryOutput` contract
3. Output includes STORY OUTPUT header, NARRATIVE SELECTION editorial record, clean story prose, and QUALITY THRESHOLD RESULT
4. The story has a dramatic question, protagonist, stakes, causal chain, peak moment, and resolution
5. Every finding from the source is accounted for — included with role or omitted with rationale

---

## Why This Matters

**The Problem:** Analytical output lives in paradigmatic mode — logical, categorical. Executives and boards need narrative mode — sequential, causal, emotional. You cannot get from one to the other by reformatting.

**This Fix:** A dedicated specialist that performs cognitive mode translation — structural transformation, not cosmetic rewriting.

**The Result:** Source material becomes a story that moves the audience to action, with every editorial choice documented.

---

## Dependencies

**Requires:** Amplifier Foundation, AnalysisOutput from Data Analyzer

**Enables:** 03-02 (chain invocation), 03-03 (existing document), 03-04 (audit editorial choices)

---

**Created:** 2026-03-04 by Chris Park

**Epic:** [03. Storyteller Specialist](../../epics/03-storyteller.md)
```

**Step 3: Create user story 03-02**

Create `docs/02-requirements/user-stories/03-storyteller/03-02-chain-invocation.md`:

```markdown
# 03-02: Invoke Storyteller at End of Research Chain

**Epic:** [03. Storyteller Specialist](../../epics/03-storyteller.md)
**Status:** ✅ Implemented

---

## Capability

An orchestrator agent can invoke the Storyteller as the final step in a Researcher → Formatter → Analyzer → Storyteller chain, producing narrative output instead of a structured document — without manual reformatting between any steps.

---

## Done Looks Like

1. Orchestrator runs the narrative-chain recipe or manually chains Researcher → Formatter → Analyzer → Storyteller
2. Each step's output passes directly as input to the next without manual translation
3. The Storyteller receives AnalysisOutput and produces StoryOutput
4. The final output is a compelling narrative, not a structured document

---

## Why This Matters

**The Problem:** The existing research chain ends at Writer — which produces structured documents with full coverage. There's no way to get narrative output from the same pipeline.

**This Fix:** The Storyteller slots in as an alternative final step. Same research, different output mode.

**The Result:** One pipeline, two output modes — document (Writer) or narrative (Storyteller) — chosen by the caller.

---

## Dependencies

**Requires:** 03-01 (core Storyteller), narrative-chain.yaml recipe

**Enables:** End-to-end narrative pipeline

---

**Created:** 2026-03-04 by Chris Park

**Epic:** [03. Storyteller Specialist](../../epics/03-storyteller.md)
```

**Step 4: Create user story 03-03**

Create `docs/02-requirements/user-stories/03-storyteller/03-03-existing-document-narrative.md`:

```markdown
# 03-03: Transform Existing Document with Tone Preference

**Epic:** [03. Storyteller Specialist](../../epics/03-storyteller.md)
**Status:** ✅ Implemented

---

## Capability

A user can pass any existing document to the Storyteller with a tone preference, and it re-renders the document as a narrative for a specific audience — without requiring the document to have been produced by the pipeline.

---

## Done Looks Like

1. User passes an existing document (Writer output, external report, raw text) with `tone: dramatic` and `audience: engineering team`
2. Storyteller detects input type as `document`, extracts findings, and runs the full pipeline
3. Output is a narrative in the requested tone, with NARRATIVE SELECTION record showing what was selected from the document
4. The story respects source fidelity — no fabricated content beyond what was in the document

---

## Why This Matters

**The Problem:** Existing reports and documents need to be re-rendered as narratives for different audiences. Today this requires manual rewriting.

**This Fix:** The Storyteller accepts any document as input — not just pipeline output.

**The Result:** Any document becomes narrative material, with the same quality gate and auditability as pipeline-sourced stories.

---

## Dependencies

**Requires:** 03-01 (core Storyteller)

**Enables:** Standalone Storyteller use (no pipeline required)

---

**Created:** 2026-03-04 by Chris Park

**Epic:** [03. Storyteller Specialist](../../epics/03-storyteller.md)
```

**Step 5: Create user story 03-04**

Create `docs/02-requirements/user-stories/03-storyteller/03-04-audit-editorial-choices.md`:

```markdown
# 03-04: Audit Editorial Choices via NARRATIVE SELECTION

**Epic:** [03. Storyteller Specialist](../../epics/03-storyteller.md)
**Status:** ✅ Implemented

---

## Capability

A caller can review the NARRATIVE SELECTION record to see exactly which findings were included in the story (and their role in the arc) and which were omitted (and why) — making the Storyteller's editorial decisions fully auditable.

---

## Done Looks Like

1. Every StoryOutput includes a NARRATIVE SELECTION block
2. INCLUDED FINDINGS lists each finding used, with its role in the narrative arc
3. OMITTED FINDINGS lists each finding set aside, with a brief rationale
4. The sum of included + omitted equals the total findings extracted from the source
5. Caller can verify that no findings were silently dropped

---

## Why This Matters

**The Problem:** Narrative requires selection — you can't include everything. But selection without accountability creates an unauditable black box.

**This Fix:** NARRATIVE SELECTION makes every editorial decision explicit. The reader knows what was chosen, what was left out, and why.

**The Result:** Full traceability without inline citations that would break the narrative.

---

## Dependencies

**Requires:** 03-01 (core Storyteller)

**Enables:** Trust in narrative output — callers can verify editorial decisions

---

**Created:** 2026-03-04 by Chris Park

**Epic:** [03. Storyteller Specialist](../../epics/03-storyteller.md)
```

**Step 6: Create user story 03-05**

Create `docs/02-requirements/user-stories/03-storyteller/03-05-model-agnostic-cli.md`:

```markdown
# 03-05: Invoke from CLI with Any LLM Provider

**Epic:** [03. Storyteller Specialist](../../epics/03-storyteller.md)
**Status:** ✅ Implemented

---

## Capability

A developer can invoke the Storyteller from the Amplifier CLI with any supported LLM provider (Anthropic, OpenAI, Gemini) and receive identical StoryOutput regardless of provider — no provider-specific features or structured output APIs are required.

---

## Done Looks Like

1. Developer runs `amplifier run specialists:storyteller --provider anthropic < analysis.txt`
2. Storyteller produces StoryOutput with all required sections
3. Same command with `--provider openai` or `--provider gemini` produces equivalent output
4. No provider-specific features are used — pure text in, text out

---

## Why This Matters

**The Problem:** Provider lock-in limits where specialists can run. Provider-specific features (structured output APIs, function calling schemas) create hard dependencies.

**This Fix:** The Storyteller uses no provider-specific features. Its quality gate is self-contained within the specialist's own pipeline.

**The Result:** Model-agnostic narrative generation. Works identically on any supported provider.

---

## Dependencies

**Requires:** 03-01 (core Storyteller), Amplifier CLI

**Enables:** Multi-provider deployment, provider comparison testing

---

**Created:** 2026-03-04 by Chris Park

**Epic:** [03. Storyteller Specialist](../../epics/03-storyteller.md)
```

**Step 7: Verify**

Confirm all 5 files exist:
```bash
ls -la docs/02-requirements/user-stories/03-storyteller/
```

Expected: 5 files (03-01 through 03-05).

**Step 8: Commit**

```bash
git add docs/02-requirements/user-stories/03-storyteller/ && git commit -m "docs: add user stories for Epic 03 (Storyteller)"
```

---

## Task 11: Create `narrative-chain.yaml` Recipe

**Files:**
- Create: `recipes/narrative-chain.yaml`

**Step 1: Create the recipe file**

Follow the exact format of `recipes/research-chain.yaml`. Create `recipes/narrative-chain.yaml`:

```yaml
name: "narrative-chain"
description: "Full research-to-narrative pipeline — Researcher → Formatter → Data Analyzer → Storyteller → Save. Produces compelling narrative output instead of a structured document."
version: "1.0.0"
tags: ["research", "analysis", "narrative", "storytelling", "chain"]

context:
  research_question: ""      # Required: the question or topic to research
  audience: ""               # Optional: target audience for the narrative
  tone: ""                   # Optional: narrative tone (dramatic, trustworthy, creative, persuasive)
  quality_threshold: "medium" # Optional: quality bar for the research run (low, medium, high)

steps:
  - id: "research"
    agent: "specialists:specialists/researcher"
    prompt: |
      Research the following question thoroughly. Follow your full research pipeline
      and return your complete research narrative with sourced evidence, confidence
      scores, and source tiering.

      Research question: {{research_question}}

      Quality threshold: {{quality_threshold}}
    output: "research_output"
    timeout: 2700

  - id: "format-research"
    agent: "specialists:specialists/researcher-formatter"
    prompt: |
      Normalize the following research narrative into your canonical RESEARCH OUTPUT
      block format. Apply all standard formatting rules: structured sections, source
      tiering, per-claim confidence scores, and gap flags.

      Research narrative to format:
      {{research_output}}
    output: "formatted_research"
    timeout: 600

  - id: "analyze"
    agent: "specialists:specialists/data-analyzer"
    prompt: |
      Analyze the following formatted research output. Draw inferences, identify
      patterns, surface key insights, and flag confidence gaps. Follow your full
      analysis pipeline.

      Formatted research:
      {{formatted_research}}
    output: "analysis_output"
    timeout: 900

  - id: "narrate"
    agent: "specialists:specialists/storyteller"
    prompt: |
      Transform the following analysis into a compelling narrative. Follow your full
      5-stage pipeline: Parse, Find the Drama, Select and Structure, Draft, and
      Quality Gate. Return the complete STORY OUTPUT block with NARRATIVE SELECTION
      record, story prose, and QUALITY THRESHOLD RESULT.

      Analysis:
      {{analysis_output}}

      Audience: {{audience}}
      Tone: {{tone}}

      If audience is empty, infer from the content.
      If tone is empty, infer from the content and audience.
    output: "final_narrative"
    timeout: 900

  - id: "save"
    agent: "foundation:file-ops"
    prompt: |
      Save the following narrative to disk.

      1. Derive a short kebab-case filename (3-5 words) from this research question:
         "{{research_question}}"
         Example: if the question is about AI market consolidation, use "ai-market-consolidation-narrative"

      2. Save the content to: docs/research-output/[your-derived-filename].md
         Create the docs/research-output/ directory if it does not exist.

      3. Report the full file path you saved to.

      Content to save:
      {{final_narrative}}
    output: "output_path"
    timeout: 120
```

**Step 2: Verify**

Read `recipes/narrative-chain.yaml` back and confirm:
- [ ] 5 steps: research → format-research → analyze → narrate → save
- [ ] Steps 1–3 are identical to `research-chain.yaml` (same agents, same prompts)
- [ ] Step 4 uses `specialists:specialists/storyteller` (not writer)
- [ ] Step 4 passes `audience` and `tone` context variables
- [ ] Step 5 saves to `docs/research-output/`
- [ ] Context variables include `research_question` (required), `audience`, `tone`, `quality_threshold`

**Step 3: Commit**

```bash
git add recipes/narrative-chain.yaml && git commit -m "feat: add narrative-chain recipe (Researcher → Formatter → Analyzer → Storyteller)"
```

---

## Task 12: Update BACKLOG

**Files:**
- Modify: `docs/BACKLOG.md`

**Step 1: Change Epic 03 status**

Find line 15:
```markdown
- 🆕 Epic 03 — Storyteller
```

Change to:
```markdown
- 🔄 Epic 03 — Storyteller
```

**Step 2: Update the status summary count**

Find line 11:
```markdown
**11 epics tracked:** ✅ 4 complete, 🔄 0 in progress, ⏸️ 0 paused, 7 planned
```

Change to:
```markdown
**11 epics tracked:** ✅ 4 complete, 🔄 1 in progress, ⏸️ 0 paused, 6 planned
```

**Step 3: Add to Active Work table**

Find the Active Work table (starts at line 27). Replace:

```markdown
| — | — | — | — | — | No active work |
```

with:

```markdown
| Storyteller specialist | 03 | Chris | 🔄 In Progress | main | Cognitive mode translation — transforms research/analysis into compelling narrative |
```

**Step 4: Move Storyteller from Immediate Next**

Find Immediate Next item #1 (line 64):
```markdown
| 1 | Storyteller specialist | 03 | Chris | L | H | Transforms research/analysis into compelling narratives; natural next specialist after Researcher → Analyzer → Writer chain is complete |
```

Remove this row entirely (it's now in Active Work).

Also find the Near-term item #1 (line 70):
```markdown
| 1 | Storyteller specialist | 03 | Chris | L | H | Transforms research/analysis into compelling narratives; high-demand for knowledge workers |
```

Remove this row (duplicate of the Immediate Next entry — now active).

**Step 5: Update Epic Completion Status**

Find the Epic 03 row in the Epic Completion Status table (line 149):
```markdown
| 03 — Storyteller | — | Full specialist implementation | 0% |
```

Change to:
```markdown
| 03 — Storyteller | StoryOutput schema, 5-stage pipeline, NARRATIVE SELECTION, narrative-chain recipe | Compound tones, structured NARRATIVE SELECTION format | 90% |
```

**Step 6: Update Change History**

Add a new row at the top of the Change History table:

```markdown
| v1.9 | Mar 4, 2026 | Chris | Epic 03 (Storyteller) moved to in-progress; specialist, schema, recipe, epic, user stories, principles, metrics all shipped |
```

**Step 7: Verify**

Read `docs/BACKLOG.md` back and confirm:
- [ ] Epic 03 shows 🔄 (not 🆕)
- [ ] Status summary says "1 in progress" and "6 planned"
- [ ] Active Work table has the Storyteller row
- [ ] Storyteller is removed from Immediate Next and Near-term
- [ ] Epic Completion Status shows 90% for Epic 03
- [ ] Change History has v1.9 entry

**Step 8: Commit**

```bash
git add docs/BACKLOG.md && git commit -m "docs: update BACKLOG - Epic 03 now in progress"
```

---

## Task 13: Test and Verify (Pre-Merge Checklist)

This task validates everything from `docs/adding-a-specialist.md` pre-merge checklist. Each sub-step is one verification action.

### 13.1: Local Invocation Test

In an Amplifier session with the bundle active, invoke the Storyteller directly with sample AnalysisOutput:

```python
delegate(
    agent="specialists:specialists/storyteller",
    instruction="""Transform this analysis into a compelling narrative for a board of directors. Tone: trustworthy.

ANALYSIS OUTPUT
Specialist: data-analyzer
Version: 1.0

ANALYSIS BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━
Question: What is the state of enterprise AI adoption?
Focus: full research
Findings received: 5
Inferences drawn: 3
Quality score: high
   Derivation: high = all inferences are high confidence

FINDINGS
F1: claim: 78% of Fortune 500 companies have at least one AI project in production | source: https://example.com/fortune500 | tier: secondary | confidence: high
F2: claim: Average enterprise AI project takes 18 months from prototype to production | source: https://example.com/timeline | tier: secondary | confidence: medium
F3: claim: Companies with dedicated AI teams ship 3x faster than those using ad-hoc approaches | source: https://example.com/teams | tier: primary | confidence: high
F4: claim: 60% of AI projects fail to move past the pilot stage | source: https://example.com/failures | tier: secondary | confidence: high
F5: claim: The most common failure mode is lack of executive sponsorship, not technical complexity | source: https://example.com/sponsors | tier: primary | confidence: high

INFERENCES
inference: Enterprise AI adoption has crossed the early-adopter threshold but most organizations are stuck in pilot purgatory — they can start projects but cannot finish them | type: pattern | confidence: high | traces_to: F1, F4
inference: The bottleneck is organizational, not technical — executive sponsorship and dedicated teams predict success more reliably than technical sophistication | type: causal | confidence: high | traces_to: F3, F5
inference: Organizations that invest in AI team structure now will compound their advantage as competitors remain stuck in pilot cycles | type: predictive | confidence: medium | traces_to: F1, F3, F4

UNUSED FINDINGS
none

EVIDENCE GAPS
none

QUALITY THRESHOLD RESULT: MET"""
)
```

**Expected result:** The Storyteller returns output starting with bare text `STORY OUTPUT` (not inside a code fence), followed by the header fields, NARRATIVE SELECTION, story prose, and QUALITY THRESHOLD RESULT.

### 13.2: Output Contract Verification

After receiving the output from 13.1, verify:
- [ ] Output starts with bare text `STORY OUTPUT` — not wrapped in ` ``` `
- [ ] `Input type:` field is present and says `analysis-output`
- [ ] `Audience:` field is present
- [ ] `Tone:` field says `trustworthy`
- [ ] `Framework:` field is present with one of: scqa, three-act, story-spine, sparkline, kishotenketsu
- [ ] `Quality threshold:` field says `met` or `not met`
- [ ] `NARRATIVE SELECTION` section is present
- [ ] `Dramatic question:` is filled in
- [ ] `Protagonist:` is filled in
- [ ] `INCLUDED FINDINGS` lists finding IDs with roles
- [ ] `OMITTED FINDINGS` lists any omitted findings with reasons (or is empty if all were used)
- [ ] Story prose is present — clean narrative, no citation markers, no `> *Sources:*` blocks
- [ ] `QUALITY THRESHOLD RESULT:` line is present at the end

### 13.3: Boundary Case Test

Invoke the Storyteller with deliberately insufficient input — too sparse for a complete narrative arc:

```python
delegate(
    agent="specialists:specialists/storyteller",
    instruction="""Transform this into a compelling narrative.

ANALYSIS OUTPUT
Specialist: data-analyzer
Version: 1.0

ANALYSIS BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━
Question: Unknown topic
Focus: full research
Findings received: 1
Inferences drawn: 0
Quality score: low

FINDINGS
F1: claim: Something might be true | source: unknown | tier: tertiary | confidence: low

INFERENCES
none

UNUSED FINDINGS
F1: reason: insufficient_evidence — single tertiary source, no corroboration

EVIDENCE GAPS
gap: Almost everything | reason: no research conducted

QUALITY THRESHOLD RESULT: NOT MET"""
)
```

**Expected result:** The Storyteller should either:
- Return `QUALITY THRESHOLD RESULT: NOT MET` with a specific explanation of what's missing (preferred), OR
- Ask a clarifying question about what the user needs (acceptable if the input is genuinely ambiguous)

It should NOT produce a full narrative from this sparse input.

### 13.4: Chain Test

Run the full `narrative-chain.yaml` recipe end-to-end:

```bash
amplifier recipe run recipes/narrative-chain.yaml --set research_question="What is the current state of enterprise AI adoption and what predicts success?" --set audience="board of directors" --set tone="trustworthy"
```

**Expected result:** The recipe completes all 5 steps (research → format → analyze → narrate → save) and produces a saved narrative file in `docs/research-output/`. The final output should be a StoryOutput with all required sections.

**Verify:** Read the saved file and confirm it contains STORY OUTPUT header, NARRATIVE SELECTION, story prose, and QUALITY THRESHOLD RESULT.

---

## Summary: All Files Created or Modified

| Action | File |
|--------|------|
| Modified | `shared/interface/types.md` |
| Created | `specialists/storyteller/index.md` |
| Created | `specialists/storyteller/README.md` |
| Modified | `behaviors/specialists.yaml` |
| Modified | `context/specialists-instructions.md` |
| Modified | `README.md` |
| Modified | `docs/01-vision/PRINCIPLES.md` |
| Modified | `docs/01-vision/SUCCESS-METRICS.md` |
| Created | `docs/02-requirements/epics/03-storyteller.md` |
| Created | `docs/02-requirements/user-stories/03-storyteller/03-01-transform-analysis-to-narrative.md` |
| Created | `docs/02-requirements/user-stories/03-storyteller/03-02-chain-invocation.md` |
| Created | `docs/02-requirements/user-stories/03-storyteller/03-03-existing-document-narrative.md` |
| Created | `docs/02-requirements/user-stories/03-storyteller/03-04-audit-editorial-choices.md` |
| Created | `docs/02-requirements/user-stories/03-storyteller/03-05-model-agnostic-cli.md` |
| Created | `recipes/narrative-chain.yaml` |
| Modified | `docs/BACKLOG.md` |

## Pre-Merge Checklist Mapping

From `docs/adding-a-specialist.md`:

- [x] `specialists/storyteller/index.md` — persona + pipeline instructions (Task 2)
- [x] `specialists/storyteller/README.md` — interface contract (Task 3)
- [x] `shared/interface/types.md` — StoryOutput type defined (Task 1)
- [x] `README.md` — added to specialists table (Task 6)
- [x] `behaviors/specialists.yaml` — added to agents.include (Task 4)
- [x] `context/specialists-instructions.md` — added to available specialists + when-to-use (Task 5)
- [x] Local invocation tested (Task 13.1)
- [x] Output contract verified (Task 13.2)
- [x] Boundary case tested (Task 13.3)
- [x] Chain tested end-to-end (Task 13.4)