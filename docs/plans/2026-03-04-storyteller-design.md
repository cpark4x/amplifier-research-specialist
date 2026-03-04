# Storyteller Specialist — Design

**Date:** 2026-03-04
**Status:** Approved
**Epic:** 03 — Storyteller Specialist
**Grounded in:** docs/01-vision/VISION.md, specialist-ecosystem-design, cross-domain narrative research

---

## The Problem

The pipeline produces excellent analytical artifacts — sourced findings, labeled inferences,
structured competitive intelligence. But these artifacts live in what Jerome Bruner (1986)
called the **paradigmatic mode**: logical, categorical, evaluated by truth and falsehood.

The people who need to act on this work — executives, boards, stakeholders, customers —
often need it in the **narrative mode**: sequential, causal, emotional, evaluated by
verisimilitude and coherence. These are not the same cognitive system. You cannot get from
one to the other by reformatting. It requires structural transformation.

Today, that transformation either doesn't happen (the analyst ships the analysis as-is),
or happens informally (someone rewrites it in a way that loses traceability). Neither
outcome is acceptable.

---

## The Solution

A specialist that performs **cognitive mode translation** — converting paradigmatic-mode
artifacts into narrative-mode artifacts through deliberate structural transformation.

> **The Writer covers. The Storyteller selects.**

The Writer covers everything and flags gaps. The Storyteller selects the load-bearing
findings for a narrative arc, builds a story around them, and documents what it chose
to leave out. These are different authorizations, not overlapping ones.

---

## Research Foundation

This design is grounded in a comprehensive research report spanning cognitive neuroscience,
experimental psychology, business communication, screenwriting theory, and computational
narrative analysis. The cross-domain consensus shaped every design decision.

**Core theoretical basis:**
- **Jerome Bruner** (1986) — Two cognitively incommensurable modes: paradigmatic
  (logical, analytical) and narrative (sequential, causal, emotional). Translation
  between them requires structural transformation, not reformatting.
- **Paul Zak** (2009–2015) — Narratives with dramatic arc produce simultaneous cortisol
  (attention) + oxytocin (empathy) release; flat narrative produces neither. Behavior
  change requires both.
- **Green & Brock** (2000) — Narrative transportation theory: transportation mediates all
  narrative persuasion through reduced counterarguing + character identification +
  emotional engagement.

**Craft principles with empirical grounding:**
- **Heath & Heath** (2007) — The Curse of Knowledge: experts systematically cannot
  simulate what it's like not to know what they know. The dominant failure mode of
  expert communication.
- **Slovic et al.** (2007) — Identifiable Victim Effect: adding statistics to a story
  reduces its emotional impact. Selection matters — more data is not better narrative.
- **Minto** (1987) — SCQA/Pyramid Principle: answer-first structure reduces cognitive
  load for expert audiences.
- **Duarte** (2010/2019) — Sparkline structure, audience-as-hero principle, DataStory
  narrative moves.

**Cross-domain consensus (high confidence across all surveyed domains):**
- Tension/gap required for narrative engagement
- Specificity beats abstraction
- Protagonist identification drives empathy and action
- Stakes must be explicit, not implied
- Causal chain is the skeleton of story comprehension
- Peak + ending dominate memory (peak-end rule)

---

## Core Identity and Authorization

The Storyteller is the only specialist in the chain authorized to make **narrative
selection decisions** — choosing which findings are load-bearing for the arc and which
ones to set aside.

**Authorized:**
- Select which findings serve the narrative arc
- Omit findings that don't serve the arc (with documented rationale)
- Choose narrative framework, sequencing, emotional register
- Reframe findings for the audience's journey (not the analyst's)

**Not authorized:**
- Add content not present in the source material — no fabricated examples, no invented
  analogies, no illustrative fiction
- Present uncertain claims as load-bearing story elements
- Produce inline citations in the story body (breaks narrative transportation)

The creative work is in selection, sequencing, and framing — not invention. Source
fidelity is maintained.

---

## Input Contract

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| source | Yes | See below | The material to transform into narrative |
| audience | No | string | Who this is for — inferred from content if not provided |
| tone | No | string | `dramatic` / `trustworthy` / `creative` / `persuasive` — inferred if not provided |

**Accepted input types:**
- `analysis-output` — from Data Analyzer (primary use case)
- `research-output` — from Researcher/Formatter
- `competitive-analysis-output` — from Competitive Analysis specialist
- `document` — any existing document (Writer output, external docs)

When audience or tone can't be determined from the source material and the user didn't
specify: ask one targeted question. Not a questionnaire.

---

## Output Schema — `StoryOutput`

**Header block** (machine-parseable, first thing emitted):

```
STORY OUTPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━
Input type: analysis-output | research-output | competitive-analysis-output | document
Audience: [detected or user-specified]
Tone: dramatic | trustworthy | creative | persuasive
Framework: SCQA | three-act | story-spine | sparkline | kishotenketsu
Quality threshold: met | not met
```

**NARRATIVE SELECTION** — the editorial record and auditability layer:

```
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
```

This replaces inline citations. Citations break the narrative mode — adding analytical
markers to a story activates paradigmatic reading and suppresses narrative transportation
(Green & Brock; Slovic identifiable victim effect). The selection record preserves
traceability without breaking the story.

**STORY** — the narrative itself. Clean prose, no citation markers, no structural
interruptions. Evaluated by verisimilitude and coherence, not source coverage.

**QUALITY THRESHOLD RESULT** — explicit pass/fail with rationale.

**Deliberate omission:** No `CLAIMS TO VERIFY` block. The Writer needs this because it
covers everything including low-confidence claims. The Storyteller only builds its arc
from findings it can stand behind — uncertain claims don't become load-bearing story
elements. This rules out the failure mode where narrative pressure forces weak evidence
into prominent positions.

---

## Pipeline — 5 Stages

### Stage 1: Parse

1. Detect input type (`analysis-output`, `research-output`, `competitive-analysis-output`,
   `document`)
2. Extract the findings, claims, and arguments the story will be built from
3. Detect audience and tone from the content if not specified
4. Confirm with the user only when genuinely ambiguous — not as a default

### Stage 2: Find the Drama

Identify the central dramatic question buried in the source material: what is the gap,
risk, surprise, or unresolved tension the research has revealed?

Select the narrative framework based on content + audience + tone (see Framework
Selection Logic below). This stage produces the **narrative blueprint** — not prose yet.

### Stage 3: Select and Structure

The core craft stage. Apply the 7 transformation decisions:

1. What is the central dramatic question?
2. Who is the protagonist?
3. What is the gap/complication?
4. What evidence actually serves the story?
5. What is the sequencing order? (answer-first vs. discovery-led vs. tension-first)
6. What is the emotional register?
7. Where is the single memorable peak moment?

Build the `NARRATIVE SELECTION` record here — every included finding named, every
omitted finding named with brief rationale. This makes the editorial work auditable
**before** the draft is written.

### Stage 4: Draft

Write the story using the selected framework, chosen tone, and structural blueprint
from Stage 3. Clean prose — no citation markers, no structural interruptions. The story
is evaluated by coherence and verisimilitude, not coverage.

### Stage 5: Quality Gate

Check against the cross-domain checklist (see Quality Gate below). Max 2 revision
cycles. Fails loud with `QUALITY THRESHOLD RESULT: NOT MET` if the source material
can't support a complete narrative arc.

---

## Framework Selection Logic

The Storyteller selects the narrative framework internally. Users never pick a framework
directly. Selection is based on three independent axes:

### Axis 1 — Primary Goal (most determinative)

| Goal | Framework | Rationale |
|------|-----------|-----------|
| Decision/action needed | **SCQA** | Answer-first, executive-friendly (Minto) |
| Persuasion or belief change | **Three-act** or **Sparkline** | Build evidence toward conclusion (Duarte) |
| Insight or surprise reveal | **Kishotenketsu** | No conflict structure required — twist-based |
| Change narrative (was X, now Y) | **Story Spine** | Causal chain emphasis |

### Axis 2 — Audience

| Audience | Effect |
|----------|--------|
| Expert, time-constrained | Reinforces SCQA |
| Skeptical, needs convincing | Reinforces three-act (build evidence toward conclusion) |
| General audience | Emotional-first structures |

### Axis 3 — Tone (affects register, not framework)

| Tone | Effect on Storytelling |
|------|----------------------|
| **Trustworthy** | Conservative selection, explicitly grounded in high-confidence findings, doesn't overstate |
| **Dramatic** | Amplifies tension in Stage 3, stronger peak engineering, higher emotional register |
| **Creative** | More experimental sequencing, kishotenketsu more likely, unexpected juxtaposition |
| **Persuasive** | Sparkline or three-act, audience-as-protagonist foregrounded |

**Key principle:** Framework and tone are independent. A SCQA story can be told with a
dramatic or trustworthy tone. Framework determines *structure*; tone determines *register*.
Both are recorded in the output header block so the selection is fully transparent.

---

## Quality Gate

Runs after Stage 4 (Draft). Every checklist item has empirical grounding from at least
one surveyed domain; most from several.

### Structural Checklist (must pass all)

- **Dramatic question** — Is there a clear, felt gap or complication? Does the audience
  know what question is being answered?
- **Protagonist** — Is there an identifiable entity whose situation changes? Can the
  audience identify with them?
- **Stakes** — What happens if the complication is not resolved? Stated explicitly,
  not implied.
- **Causal chain** — Does each narrative beat *cause* the next, or merely follow it?
- **Peak moment** — Is there one most powerful moment? Placed near the climax, not buried.
- **Resolution** — Is the dramatic question answered? Does the ending leave the audience
  in the intended state?

### Craft Checklist (must pass all)

- **Concreteness** — Are abstract claims replaced with specific instances wherever possible?
- **Curse of Knowledge** — Has jargon been defined? Are no explanatory steps assumed away?
- **Audience-as-protagonist** — Is the narrative framed for the audience's journey, not
  the analyst's?

### Auditability Checklist (must pass all)

- **Selection record complete** — Does every included finding trace to source? Does every
  omitted finding appear in `NARRATIVE SELECTION` with rationale?

### Failure Behavior

Max 2 revision cycles. If the source material genuinely cannot support a complete
narrative arc — the dramatic question isn't answerable, or the findings are too sparse —
the Storyteller fails loud: `QUALITY THRESHOLD RESULT: NOT MET` with specific explanation
of what's missing. It does not silently produce a weakened story.

---

## Usage Patterns

### Human, in conversation

> *"Use the Storyteller to transform this analysis into a compelling narrative for our
> board. Tone: trustworthy."*

Audience and tone are optional — inferred from content when not provided. One targeted
question only when genuinely ambiguous. Human gets clean story + NARRATIVE SELECTION
record they can review.

### AI agent (machine caller)

Another specialist or orchestrator passes a structured `analysis-output` or
`research-output` block directly. The machine-readable header block (`STORY OUTPUT` +
metadata fields) enables downstream agents to parse type, framework, tone, and quality
result without reading the prose.

### Standalone CLI

```bash
# Transform an existing document
amplifier run specialists:storyteller --tone dramatic < existing-report.md

# With specific providers
amplifier run specialists:storyteller --provider anthropic < analysis.txt
amplifier run specialists:storyteller --provider openai < analysis.txt
amplifier run specialists:storyteller --provider gemini < analysis.txt
```

### As part of a chain (new recipe: `narrative-chain.yaml`)

```
Researcher → Formatter → Analyzer → Storyteller
```

Parallel to the existing `research-chain.yaml` (which ends at Writer). Same first three
steps, different final specialist depending on desired output — document or narrative.

### Model agnosticism

No structured output APIs, no provider-specific features — pure text in, text out. Works
identically on Anthropic, OpenAI, Gemini, or anything else. The quality gate is
self-contained within the specialist's own pipeline. Consistent with the project's core
philosophy.

---

## How It Chains

**Analyzer → Storyteller:**
Pass `AnalysisOutput` as source material. The Storyteller selects the load-bearing
inferences and builds a narrative arc. Primary use case.

**Researcher → Storyteller:**
Pass `ResearchOutput` directly. The Storyteller works with raw findings — no inference
layer needed when the story is about the evidence itself.

**Competitive Analysis → Storyteller:**
Pass `CompetitiveAnalysisOutput`. Win conditions and positioning gaps become natural
dramatic material.

**Writer → Storyteller:**
Pass any document. The Storyteller re-renders an existing document as narrative — useful
when a report needs to become a presentation story or stakeholder communication.

**Full chain:**
`Researcher → Formatter → Analyzer → Storyteller`

---

## New Principles for PRINCIPLES.md

Three Storyteller-specific principles to add when implementing:

1. **"The Writer covers. The Storyteller selects."** — The Writer surfaces all findings
   and flags gaps. The Storyteller chooses the load-bearing findings for the narrative
   arc and documents what was left out. These are different authorizations, not
   overlapping ones.

2. **Citations break the narrative mode.** — The Storyteller produces no inline citations
   in the story body. Inline citations activate the analytical/paradigmatic reading mode
   and suppress narrative transportation (Green & Brock; Slovic identifiable victim
   effect). The NARRATIVE SELECTION record provides auditability without breaking
   the story.

3. **Framework and tone are independent.** — Narrative framework (SCQA, three-act,
   Story Spine, etc.) determines structure. Tone (trustworthy, dramatic, creative,
   persuasive) determines register. They are set on separate axes. Any framework can
   be rendered in any tone.

---

## Open Questions

1. **New recipe or mode flag?** — Should `narrative-chain.yaml` be a new recipe or a
   mode flag on `research-chain.yaml`? Current recommendation: new dedicated recipe.
   The output shape and final-stage prompt are distinct enough to warrant separation.

2. **Multiple tones per invocation?** — Should the Storyteller accept compound tones
   (e.g., "trustworthy but with a dramatic opening")? Current recommendation: single
   tone for V1. Simplicity first — revisit when real usage patterns emerge.

3. **NARRATIVE SELECTION format** — Does the selection block need structured format
   (like the CITATIONS block in Writer) or is prose rationale sufficient? Current
   recommendation: prose rationale for V1. Structured format adds complexity before
   we know what downstream consumers need.