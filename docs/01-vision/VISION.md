# Specialists — Vision

> **For AI agents:** This document is the authoritative source for WHY this project exists, WHERE it is going, and HOW to make decisions. Read this before touching any code.

**Owner:** Chris Park  
**Last Updated:** 2026-03-03  

---

## Summary

Canvas Specialists is a library of best-in-class, single-domain AI specialist agents for knowledge worker and consumer scenarios. Each specialist runs a rigorous multi-stage pipeline with explicit quality gates and returns structured, machine-parseable output — filling the gap between shallow generalist tools and custom one-off agents.

The goal is output a user can **stake their reputation on**: output that is defensible, auditable, and honest about its limits. Every finding traces to a source. Every inference traces to a finding. Every limitation is named. Nothing is papered over.

---

## Table of Contents

1. [The Problem](#the-problem)
2. [The Solution](#the-solution)
3. [Philosophy](#philosophy)
4. [Target Audience](#target-audience)
5. [Strategic Positioning](#strategic-positioning)
6. [Roadmap](#roadmap)
7. [What Success Looks Like](#what-success-looks-like)
8. [Related Documentation](#related-documentation)

---

## The Problem

When an Amplifier orchestrator needs to do something like "research this topic" or
"write this document," it has two bad options today:

1. **Do it inline** — the orchestrator searches the web directly, gets shallow results,
   and returns low-confidence output with no quality gate.
2. **Delegate to a generalist** (e.g., `foundation:web-research`) — gets a readable
   narrative back, but no source tiering, no per-claim confidence, no corroboration,
   no structured output that downstream agents can parse.

Both options produce output that *sounds* confident but isn't. There's no way to know
what sources were used, how claims were verified, or what wasn't found.

**The cost of not solving this:** developers either accept low-quality specialist output,
or build one-off agents from scratch every time they need deep domain work — with no
shared contracts, no reusability, and no quality floor.

---

## The Solution

**Specialists** are deep, single-domain agents with:
- Rigorous multi-stage pipelines (not just "search and summarize")
- Explicit quality gates before output is returned
- Structured, machine-parseable output schemas — designed for downstream agents to
  consume, not just humans to read
- Source tiering and per-claim confidence levels
- Honest evidence gap reporting — gaps are first-class outputs

Specialists are **stateless and UI-independent.** They live as a composable Amplifier
bundle that any orchestrator can include and any agent can delegate to.

---

## Philosophy

Three principles drive every design decision:

1. **Philosophy-driven** — like Amplifier itself, specialists are built on explicit
   principles, not preferences. When a design choice is hard, the philosophy decides
   it — not taste, not convenience.

2. **Model and platform agnostic** — a specialist works identically regardless of which
   LLM calls it or which app it runs in. Canvas, CLI, a third-party orchestrator — the
   contract is the same. No specialist should depend on a specific model's behavior or
   a specific platform's affordances.

3. **One thing, exceptionally well** — a specialist that does two things is two bad
   specialists. Each one has a single domain, a rigorous pipeline for that domain, and
   a quality bar it won't compromise. Breadth is the generalist's job.

---

## Target Audience

**Primary:** Knowledge workers and consumers — people doing real work: researching,
writing, analyzing, planning, presenting, communicating. Specialists serve these
scenarios first.

**Secondary:** Developers building Amplifier orchestration pipelines who need reliable,
trustworthy specialist output they can compose into larger workflows.

---

## Strategic Positioning

Specialists sit between generalist tools (fast, shallow) and custom one-off agents
(slow to build, not reusable). They are:

- **More rigorous than general-purpose research agents** — structured pipeline, quality
  gate, source tiering
- **More reusable than inline orchestrator logic** — shared contracts, composable bundle
- **More trustworthy than one-shot LLM calls** — corroboration, confidence ratings,
  explicit gaps

The output schema is the contract. Other specialists and orchestrators depend on it.
Breaking it is a breaking change.

---

## Roadmap

### V1 — Researcher (complete)
- 7-stage research pipeline (Planner → Source Discoverer → Fetcher → Extractor →
  Corroborator → Quality Gate → Synthesizer)
- Source tiering (primary/secondary/tertiary) with per-claim confidence
- Paywall fallback ladder
- Wired as Amplifier agent at `specialists:specialists/researcher`

### V2 — Writer + Researcher Upgrade
- **Writer specialist** — takes research output and produces structured content
  (articles, briefs, reports)
- **Researcher v2** — adopt Canvas researcher's machine-parseable output schema
  (Research Brief section for fast machine consumption) while keeping the quality
  gate methodology
- These two together validate the hand-off contract: researcher output → writer input

### V3 — Specialist Framework + More Specialists
- Extract the common framework from researcher + writer patterns
- Template and docs for adding new specialists
- Candidates: analyst, editor, fact-checker
- **Citation mapping in Writer** — inline `[S1]`-style markers in output prose,
  mapped back to exact source material in a Citations block

---

## What Success Looks Like

- A user delegates to the specialist chain and receives output they are willing to share
  externally, present to a decision-maker, or act on — without needing to verify every
  claim themselves
- Every finding traces to a source. Every inference traces to a finding. Every gap is
  named. The output shows its work.
- The full chain (Researcher → Data Analyzer → Writer) produces a usable document without
  human editing between steps
- Adding a new specialist takes hours, not days, because the framework handles the boilerplate
- Output from specialists is measurably more trustworthy than generalist alternatives:
  explicit sources, explicit confidence, explicit gaps — not confident-sounding prose that
  can't be audited

---

## Related Documentation

**Vision folder (strategic context):**
- [PRINCIPLES.md](PRINCIPLES.md) — Decision framework and recorded design decisions
- [SUCCESS-METRICS.md](SUCCESS-METRICS.md) — How we measure success across V1/V2/V3

**Current features and backlog:**
- [docs/README.md](../README.md) — Epic table showing implementation status
- [docs/BACKLOG.md](../BACKLOG.md) — Strategic planning view with priorities

**Implementation guidance:**
- [Adding a Specialist](../adding-a-specialist.md) — Guide for new specialist authors
- [shared/interface/types.md](../../shared/interface/types.md) — Output schema contracts

---

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.3 | 2026-03-03 | Chris Park | Updated Summary with defensible/auditable goal framing; revised Primary Success Indicator to chain-centric; updated What Success Looks Like to chain-centric outcomes |
| v1.2 | 2026-03-02 | Chris Park | Added metadata, Summary, ToC, Related Documentation, Change History; aligned with VISION_TEMPLATE |
| v1.1 | 2026-03-02 | Chris Park | Added Philosophy section; updated Target Audience to knowledge workers + consumers first |
| v1.0 | 2026-02-26 | Chris Park | Initial vision document |
