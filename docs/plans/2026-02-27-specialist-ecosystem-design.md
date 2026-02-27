# Specialist Ecosystem Design

**Date:** 2026-02-27
**Status:** Approved

---

## Context

Target user: prototypical M365 knowledge worker — someone who spends their day in Word, Excel, Outlook, PowerPoint, and Teams. Their core job is to find, understand, and communicate information to other people.

The specialists system is a library of deep, single-domain agents that an orchestrator coordinates. The orchestrator acts as a **chief of staff** — it reads the task, decides which specialists to invoke and in what order, assembles the result into the requested deliverable.

---

## The Specialists

### 1. Researcher ✅ (complete)

**Role:** Find and validate information from the web. Return structured, source-tiered evidence with per-claim confidence ratings and explicit evidence gaps.

**Input:** A research question + query type (person/company/technical/market/event) + quality threshold

**Output:** Structured evidence block — FINDINGS (with source tier, confidence, corroboration), EVIDENCE GAPS, QUALITY THRESHOLD RESULT

**Key constraint:** Never synthesizes into prose. Returns discrete, falsifiable claims only.

---

### 2. Writer (next)

**Role:** Transform structured input (research output, data, bullet points) into polished prose in the requested format and voice.

**Input:** Source material (researcher output, analyst output, or raw notes) + target format + audience + voice/tone

**Output:** Structured document — sections with headers, body prose, and a machine-readable metadata block (word count, format, audience, key claims made)

**Key constraint:** Never generates claims the source material doesn't support. Flags any gap between what was asked for and what the source material can support.

**Formats it handles:** Report, brief, proposal, executive summary, email, memo

---

### 3. Analyst

**Role:** Transform research findings or raw data into structured conclusions — patterns, comparisons, recommendations, risk assessments.

**Input:** Researcher output OR raw data + analytical frame (competitive analysis, risk assessment, trend analysis, etc.)

**Output:** Structured analysis — KEY FINDINGS (ranked by importance), PATTERNS, CONCLUSIONS (with confidence), OPEN QUESTIONS, RECOMMENDED NEXT STEPS

**Key constraint:** Separates facts (from source material) from inferences (its own reasoning). Both are labeled explicitly. Never presents inference as fact.

---

### 4. Presenter

**Role:** Transform Writer or Analyst output into a presentation structure — slide-by-slide outline with narrative arc, speaker notes, and key visuals callouts.

**Input:** Document or analysis output + audience + time available + goal (inform / persuade / decide)

**Output:** Structured deck outline — slide title, body content (3 bullets max per slide), speaker notes, suggested visual type, narrative arc label (setup/conflict/resolution)

**Key constraint:** Never adds claims not in the source material. The Presenter structures and packages — it does not generate new substance.

---

### 5. Communicator

**Role:** Transform any specialist output into a targeted communication — email, Slack message, Teams update, executive summary.

**Input:** Source material (any specialist output) + recipient + communication goal + length constraint

**Output:** Ready-to-send communication — subject line (if email), body, and a brief note on what was omitted and why

**Key constraint:** Optimizes for the recipient, not the source material. Will deliberately leave things out. Flags what was cut and why so the sender can decide.

---

## The Orchestrator

The orchestrator is not a specialist — it is the coordination layer. It:

1. Reads the task and identifies the deliverable (document / deck / email / analysis)
2. Determines which specialists are needed and in what order
3. Manages hand-offs — passes each specialist's output as input to the next
4. Assembles the final result

**Decision logic (by deliverable):**

| Task | Specialist chain |
|---|---|
| "Write a report on X" | Researcher → Writer |
| "Analyze the competitive landscape for X" | Researcher → Analyst → Writer |
| "Build a deck on X for leadership" | Researcher → Analyst → Writer → Presenter |
| "Send an update to stakeholders on X" | Researcher → Communicator |
| "Summarize this document" | (no researcher needed) Writer → Communicator |
| "What should we do about X?" | Researcher → Analyst → Communicator |

The orchestrator is responsible for choosing the right chain. Specialists are not responsible for knowing who comes next.

---

## Dependency Graph

```
Researcher ──────────────────→ Writer ──→ Presenter
     │                           ↑              
     └──→ Analyst ───────────────┘         
                                           
     (any output) ──────────────────────→ Communicator
```

- **Writer** depends on: Researcher (for research-backed content) or Analyst (for data-driven content) or raw input
- **Analyst** depends on: Researcher output or raw data
- **Presenter** depends on: Writer output
- **Communicator** depends on: any specialist output (wraps anything)
- **Researcher** depends on: nothing (entry point)

---

## Build Order

| Order | Specialist | Why |
|---|---|---|
| 1 | Researcher | ✅ Done |
| 2 | Writer | Foundational — all other deliverables depend on prose |
| 3 | Analyst | Parallel value — unlocks data-driven chains |
| 4 | Presenter | Depends on Writer output; highest-value M365 deliverable |
| 5 | Communicator | Writer with a different mode; last because it wraps others |

Writer and Analyst could be built in parallel but Writer is higher priority — it unblocks Presenter and validates the hand-off contract pattern that all subsequent specialists will follow.

---

## Inter-Specialist Contracts

Each specialist's output becomes the next specialist's input. For this to work without a translation layer, the contracts must be compatible.

**Rule:** Every specialist output includes a `METADATA` block at the top:

```
METADATA
Specialist: [name]
Version: [version]
Input type: [what was passed in]
Output type: [document | analysis | deck-outline | communication | evidence]
Format: [specific format name]
Confidence: [overall confidence level]
Gaps: [yes | no — whether evidence gaps exist]
```

This lets the orchestrator (and any downstream specialist) understand what it's receiving without parsing the full content.

---

## Key Design Principles (additions to PRINCIPLES.md)

1. **Specialists only do one thing** — a Writer never researches, a Researcher never writes prose. Single responsibility is what makes them composable.

2. **Never add claims** — every specialist that transforms or packages content may only work with what it was given. Presenter does not invent slide content. Communicator does not add context the source doesn't contain.

3. **Orchestrator owns the chain** — specialists don't know who comes next. The orchestrator decides the chain based on the task. This keeps specialists independently testable.

4. **METADATA block is required** — every specialist output starts with a METADATA block. This is the machine-readable contract that makes orchestration reliable.

---

## Open Questions (resolve before building Analyst)

1. **Analyst input format** — does the Analyst always receive Researcher output, or can it receive raw data (CSV, table, numbers)? If both, it needs two input modes.

2. **Presenter output format** — outline only (for human to build deck) or full structured JSON a tool could use to generate slides? The answer changes the complexity significantly.
