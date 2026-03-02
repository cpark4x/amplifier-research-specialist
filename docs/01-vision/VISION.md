# Specialists — Vision

> **For AI agents:** This document is the authoritative source for WHY this project exists, WHERE it is going, and HOW to make decisions. Read this before touching any code.

---

## The Problem

When an Amplifier orchestrator needs to do something like "research this topic" or "write this document," it has two bad options today:

1. **Do it inline** — the orchestrator searches the web directly, gets shallow results, and returns low-confidence output with no quality gate.
2. **Delegate to a generalist** (e.g., `foundation:web-research`) — gets a readable narrative back, but no source tiering, no per-claim confidence, no corroboration, no structured output that downstream agents can parse.

Both options produce output that *sounds* confident but isn't. There's no way to know what sources were used, how claims were verified, or what wasn't found.

**The cost of not solving this:** developers either accept low-quality specialist output, or build one-off agents from scratch every time they need deep domain work — with no shared contracts, no reusability, and no quality floor.

---

## The Solution

**Specialists** are deep, single-domain agents with:
- Rigorous multi-stage pipelines (not just "search and summarize")
- Explicit quality gates before output is returned
- Structured, machine-parseable output schemas — designed for downstream agents to consume, not just humans to read
- Source tiering and per-claim confidence levels
- Honest evidence gap reporting — gaps are first-class outputs

Specialists are **stateless and UI-independent.** They live as a composable Amplifier bundle that any orchestrator can include and any agent can delegate to.

---

## Philosophy

Three principles drive every design decision:

1. **Philosophy-driven** — like Amplifier itself, specialists are built on explicit principles, not preferences. When a design choice is hard, the philosophy decides it — not taste, not convenience.

2. **Model and platform agnostic** — a specialist works identically regardless of which LLM calls it or which app it runs in. Canvas, CLI, a third-party orchestrator — the contract is the same. No specialist should depend on a specific model's behavior or a specific platform's affordances.

3. **One thing, exceptionally well** — a specialist that does two things is two bad specialists. Each one has a single domain, a rigorous pipeline for that domain, and a quality bar it won't compromise. Breadth is the generalist's job.

---

## Target Audience

**Primary:** Developers building Amplifier orchestration pipelines who need reliable, trustworthy specialist output they can compose into larger workflows.

**Secondary:** Any Amplifier orchestrator that needs to delegate deep domain work — research, writing, analysis — without managing the methodology itself.

---

## Strategic Positioning

Specialists sit between generalist tools (fast, shallow) and custom one-off agents (slow to build, not reusable). They are:

- **More rigorous than general-purpose research agents** — structured pipeline, quality gate, source tiering
- **More reusable than inline orchestrator logic** — shared contracts, composable bundle
- **More trustworthy than one-shot LLM calls** — corroboration, confidence ratings, explicit gaps

The output schema is the contract. Other specialists and orchestrators depend on it. Breaking it is a breaking change.

---

## Roadmap

### V1 — Researcher (complete)
- 7-stage research pipeline (Planner → Source Discoverer → Fetcher → Extractor → Corroborator → Quality Gate → Synthesizer)
- Source tiering (primary/secondary/tertiary) with per-claim confidence
- Paywall fallback ladder
- Wired as Amplifier agent at `specialists:specialists/researcher`

### V2 — Writer + Researcher Upgrade
- **Writer specialist** — takes research output and produces structured content (articles, briefs, reports)
- **Researcher v2** — adopt Canvas researcher's machine-parseable output schema (Research Brief section for fast machine consumption) while keeping the quality gate methodology
- These two together validate the hand-off contract: researcher output → writer input

### V3 — Specialist Framework + More Specialists
- Extract the common framework from researcher + writer patterns (what every specialist shares vs. what's domain-specific)
- Template and docs for adding new specialists
- Candidates: analyst, editor, fact-checker
- **Citation mapping in Writer** — inline `[S1]`-style markers in output prose, mapped back to exact source material in a Citations block; closes the source fidelity gap identified in competitive analysis

---

## What Success Looks Like

- An orchestrator can delegate to `specialists:researcher` and get back structured evidence it can parse and act on — not a narrative to summarize
- A Writer specialist can consume researcher output directly without any translation layer
- Adding a new specialist takes hours, not days, because the framework handles the boilerplate
- Output from specialists is measurably more trustworthy than generalist alternatives (fewer hallucinations, explicit gaps, verified claims)
