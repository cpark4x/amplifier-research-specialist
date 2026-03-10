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
| 06 | Market Research | researcher-output | executive | inform | SCQA->Pyramid |

Coverage: all 5 input types, 4 audience types, 5 purposes, all 6 frameworks.

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

In an Amplifier session, you can run all 6 scenarios in parallel:

```
Run the generate-decks recipe for all 6 scenarios in tests/presentation-builder/scenarios/
```

Then evaluate:

```
Now evaluate all 6 generated decks against the rubric
```

## How it works

```
scenarios/*.md          Source material + parameters
        |
        v
generate-decks.yaml     Delegates to presentation-builder specialist
        |
        v
outputs/*-output.html   Generated decks
        |
        v
evaluate-deck.yaml      zen-architect REVIEW mode judges against rubric.md
        |
        v
outputs/*-evaluation.md Structured 10-dimension scores + verdict
```

## Evaluation Dimensions

The rubric scores across 10 weighted dimensions:

| Dimension | Weight | What it checks |
|-----------|--------|---------------|
| D1: Narrative Coherence | 15% | Newspaper Test — do titles alone tell the story? |
| D2: Framework Adherence | 10% | Correct framework for audience x purpose? |
| D3: Content Fidelity | 15% | All claims traceable to source? No fabrication? |
| D4: Density Discipline | 10% | Word limits respected? |
| D5: Visual Rhythm | 10% | No consecutive heavy slides? Layout variety? |
| D6: Audience Calibration | 10% | Vocabulary and depth match the audience? |
| D7: Completeness | 10% | Source material coverage? Content map? |
| D8: Speaker Notes | 10% | 4-field structured notes? |
| D9: Structural Mechanics | 5% | Title slide, dividers, closing, metadata? |
| D10: HTML Quality | 5% | Self-contained? Navigation? Theme? |

Verdicts:
- **PASS**: overall >= 4.0, no dimension below 3
- **MARGINAL**: overall >= 3.0, no dimension below 2
- **FAIL**: overall < 3.0 or any dimension at 1

## Interpreting Results

After a run, look for patterns across scenarios:

- **Low D1 scores across the board** = headline writing needs prompt improvement
- **Low D3 on researcher-output scenarios** = content tracing from findings is breaking
- **Low D6 on executive vs team** = audience calibration logic needs tuning
- **Low D8 everywhere** = speaker notes generation needs work
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
