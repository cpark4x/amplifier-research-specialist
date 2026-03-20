# Presentation Builder Evaluation Harness

Test scenarios and LLM-as-judge evaluation for the presentation builder specialist.

## Scenarios

| # | Name | Input Type | Audience | Purpose | Framework |
|---|------|-----------|----------|---------|-----------| 
| 01 | QBR Status Update | writer-output | team | update | Status/Operational |
| 02 | Competitive Landscape | competitive-analysis-output | executive | decide | SCQA->Pyramid (decision) |
| 03 | Sales Pitch | researcher-output | external | persuade | 5-Element Narrative |
| 04 | Technical Training | analysis-output | teaching | teach | Discovery |
| 05 | Project Retrospective | raw-notes | team | reflect | Retrospective |
| 07 | Startup Pitch (Investors) | raw-notes (founder) | external | persuade | 5-Element Narrative |
| 08 | Technical Intro (LLMs) | raw-notes (speaker outline) | teaching | teach | Discovery |
| 09 | Fabrication Guardrail | raw-notes (vague email) | executive | decide | SCQA->Pyramid |
| 10 | Data Overload | raw-notes (metrics dump) | executive | inform | Answer-first |

Coverage: 4 input types (writer-output, competitive-analysis, researcher-output, raw-notes),
4 audience types (team, executive, external, teaching), 6 purposes (update, decide, persuade,
teach, reflect, inform), 5 frameworks. Raw-notes scenarios (05, 07, 08) test the builder's
ability to impose structure on unstructured input without a prior specialist pipeline.
Guardrail scenarios (09, 10) test edge cases: 09 tests fabrication resistance with
deliberately vague input containing no hard numbers; 10 tests D11/D12 with a raw metrics
dump containing no prose or interpretation.

## Quick Start

### Run everything (CLI)

```bash
./tests/presentation-builder/run-all.sh
```

### Generate decks only

```bash
./tests/presentation-builder/run-all.sh --generate-only
```

### Evaluate existing decks only

```bash
./tests/presentation-builder/run-all.sh --evaluate-only
```

### Run a single scenario

```bash
# Generate
amplifier tool invoke recipes operation=execute \
  recipe_path=tests/presentation-builder/generate-decks.yaml \
  context='{"scenario_path": "tests/presentation-builder/scenarios/01-qbr-status-update.md"}'

# Evaluate
amplifier tool invoke recipes operation=execute \
  recipe_path=tests/presentation-builder/evaluate-deck.yaml \
  context='{
    "scenario_path": "tests/presentation-builder/scenarios/01-qbr-status-update.md",
    "deck_path": "tests/presentation-builder/outputs/01-qbr-status-update-output.html"
  }'
```

### Run from a session (interactive, parallel)

In an Amplifier session, you can run all scenarios in parallel:

```
Run the generate-decks recipe for all scenarios in tests/presentation-builder/scenarios/
```

Then evaluate:

```
Now evaluate all generated decks against the rubric
```

## How it works

```
scenarios/*.md          Source material + parameters
        |
        v
generate-decks.yaml     Delegates to presentation-builder specialist
        |                (model produces complete HTML with CSS + JS + navigation)
        v
outputs/*-output.html   Generated decks (open directly in browser)
        |
        v
screenshot-slides.py    Per-slide PNGs via headless Chromium
        |
        v
evaluate-deck.yaml      zen-architect REVIEW mode judges against rubric.md
        |                (with visual analysis from nano-banana VLM)
        v
outputs/*-evaluation.md Structured 12-dimension scores + verdict
```

## Evaluation Dimensions

The rubric scores across 12 weighted dimensions using explanation-before-score
evaluation method (analysis paragraph first, then numeric score):

| Dimension | Weight | What it checks |
|-----------|--------|---------------|
| D1: Narrative Coherence | 15% | Newspaper Test — do titles alone tell the story? |
| D2: Framework Adherence | 10% | Correct framework for audience x purpose? |
| D3: Content Fidelity | 15% | All claims traceable to source? No fabrication? |
| D4: Density Discipline | 8% | Word limits respected? |
| D5: Visual Rhythm | 8% | No consecutive heavy slides? Layout variety? |
| D6: Audience Calibration | 12% | Vocabulary and depth match the audience? |
| D7: Completeness | 8% | Source material coverage? Content map? |
| D8: Speaker Notes | 7% | 4-field structured notes? |
| D9: Structural Mechanics | 5% | Title slide, dividers, closing, metadata? |
| D10: HTML Quality | 5% | Self-contained? Navigation? Theme? |
| D11: Insight Density | 10% | "So what" factor — implications stated, not just data? |
| D12: Information Design | 10% | Data displayed visually (tables, stat cards) vs prose? |

Verdicts:
- **PASS**: overall >= 4.0, no dimension below 3
- **MARGINAL**: overall >= 3.0, no dimension below 2
- **FAIL**: overall < 3.0 or any dimension at 1

## Interpreting Results

After a run, look for patterns across scenarios:

- **Low D1 scores across the board** = headline writing needs prompt improvement
- **Low D3 on structured-input scenarios** = content tracing from findings is breaking
- **Low D3 on raw-notes scenarios** = builder is fabricating beyond what source provides
- **Low D6 on executive vs team** = audience calibration logic needs tuning
- **Low D8 everywhere** = speaker notes generation needs work
- **Low D11 everywhere** = builder is displaying data without stating implications
- **Low D12 on data-heavy scenarios** = builder defaults to prose instead of visual display
- **PASS on all** = the builder is ready for production use

## Adding New Scenarios

Create a new `.md` file in `scenarios/` following the format:

```markdown
# Scenario NN: [Title]

## Parameters
- **audience**: [who]
- **audience_type**: executive|team|external|teaching|general
- **purpose**: inform|persuade|decide|teach|update|reflect
- **tone**: formal|conversational|executive
- **output_format**: html|blueprint
...

## Expected Framework
[framework name]

## Source Material
[Structured output in one of: WRITER METADATA, RESEARCH OUTPUT,
ANALYSIS OUTPUT, COMPETITIVE ANALYSIS OUTPUT, or raw notes]
```

Scenarios are auto-discovered by `run-all.sh` from the `scenarios/` directory.
No script changes needed when adding or removing scenarios.