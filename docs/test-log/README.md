# Canvas-Specialists Test-Log System

## Purpose

Test logs are the human-judgment layer on top of raw specialist sessions. They turn "someone ran prompts" into structured, comparable evidence that drives concrete improvements to specialist instructions, routing rules, and output contracts. Every meaningful run should leave a trace; periodic mining of those traces feeds the backlog.

## When to Create a Test Log

Create an entry after any run where you can articulate what worked, what didn't, or what should change. This includes:

- Single-specialist runs (researcher, writer, data-analyzer, storyteller, etc.)
- Multi-specialist chain runs (e.g., `researcher → data-analyzer → writer`)
- Format-compliance or contract-verification tests
- Build-session logs (mark N/A sections accordingly)

You do not need to log trivial or throwaway runs. A few sentences per section is enough.

## Running the Flow

**Preferred method:** execute the recipe: `recipes/capture-feedback.yaml`.

The recipe walks through: collect metadata → capture body → assess quality → write file → triage + commit. The `.amplifier/skills/feedback-capture/` skill documents the same protocol for manual/conversational use.

## Directory Layout & Naming

```
docs/test-log/
├── researcher/        # Single-specialist: researcher
├── writer/            # Single-specialist: writer
├── data-analyzer/     # Single-specialist: data-analyzer
├── storyteller/       # Single-specialist: storyteller
├── chains/            # Any multi-specialist chain
└── README.md
```

**File naming:** `{YYYY-MM-DD}-{topic-slug}.md`

- Single specialist → `docs/test-log/{specialist}/{date}-{topic}.md`
- Chain → `docs/test-log/chains/{date}-{topic}.md`

## Required YAML Front Matter

```yaml
---
specialist: researcher                        # entry-point specialist
chain: "researcher → data-analyzer → writer"  # full chain; omit line if single specialist (or set to null)
topic: graphql-vs-rest                        # URL-safe slug
date: 2026-03-03                              # ISO date
quality_signal: pass                          # pass | mixed | fail
action_items_promoted: false                  # false → true | partial after triage
---
```

### `quality_signal` Allowed Values

| Value | Meaning |
|-------|---------|
| **pass** | Output met expectations; usable with minor or no adjustments |
| **mixed** | Partial concerns; notable gaps that matter |
| **fail** | Significant problems; unusable result |

## Required Body Sections

Every entry must include these five headings, in order:

1. `## What Worked`
2. `## What Didn't / Concerns`
3. `## Confidence Accuracy`
4. `## Coverage Assessment`
5. `## Action Items`

Mark sections `N/A` for compliance-only or build-session logs where they don't apply.

## Action Item Routing

After writing the file, triage each `- [ ]` item to its destination:

| Finding type | Destination |
|---|---|
| Consistent quality gap (any topic) | `docs/BACKLOG.md` |
| Edge case in one specialist | `docs/02-requirements/epics/` |
| Pattern across multiple runs | `docs/adding-a-specialist.md` |
| Confidence systematically off | `specialists/{specialist}/index.md` |

After routing, update `action_items_promoted` in the front matter to `true` (all routed), `partial` (some routed), or leave `false` (nothing needed routing).

## Canonical Workflow

```
1. Capture    → Walk through metadata + 5 body sections + quality signal
2. Write      → Save as Markdown with YAML front matter to the correct path
3. Triage     → Route each action item; update action_items_promoted
4. Commit     → Stage the log file + all modified destination files together
```

## Mining / Periodic Review

Weekly or on-demand, scan all entries under `docs/test-log/` and produce a short report covering:

- Themes: recurring issues across entries
- Trends: pass/mixed/fail distribution over time
- Unresolved items: `action_items_promoted != true` and unchecked boxes
- Recommended backlog additions (with links to evidence entries)

A contributor reviews the report before any backlog changes are committed.

## vNext: Portable Schema + Better Mining

Add three optional front matter fields:

```yaml
author: chris
subject: "format compliance"
tags: [compliance, chain, storyteller]
```
