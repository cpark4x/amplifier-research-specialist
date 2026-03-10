# data-analyzer-formatter — Design

**Owner:** Chris Park
**Date:** 2026-03-10
**Status:** Approved

---

## Context

The Data Analyzer (DA) is the inference specialist in the Canvas Specialists pipeline. It draws labeled, traceable conclusions from ResearchOutput and produces a canonical `ANALYSIS OUTPUT` block. Like every other specialist, its format compliance is instruction-based — meaning it fails under certain input conditions.

**Failure mode (2026-03-10 test log):** When input is framed as a raw question rather than "here is research output," the DA falls into narrative analysis mode — producing a competitive essay with `## Section` headers, emoji status indicators, and summary matrices. No `ANALYSIS OUTPUT` block. No `traces_to` fields. No canonical structure.

**Secondary issue (same session):** The DA sometimes leaks stage narration (`**Stage 1: Parse**`, `**Stage 2: Analyze**`) as visible output before the ANALYSIS OUTPUT block.

This is the same root cause as the Writer (#29), Storyteller (#30), and Prioritizer (#31/#33) failures. The architectural fix is the same: a formatter specialist that catches any DA output and normalizes it to the canonical block.

---

## Design

### Name

`data-analyzer-formatter`
*(follows pattern: researcher-formatter, story-formatter, writer-formatter, prioritizer-formatter)*

### Role

Format normalization stage for the DA pipeline. Never re-analyzes. Never draws new inferences. Only extracts, validates, and reformats. Two different cognitive tasks: the DA focuses on inference quality; this specialist focuses on ensuring that output arrives in canonical format every time.

### Inputs

1. **DA output** — in any format (canonical block, partial block, or narrative prose)
2. **Original research** — the `RESEARCH OUTPUT` or Format B narrative that was passed to the DA

**Why 2 inputs:** The DA's `traces_to` fields link inferences to specific finding IDs (F3, F7). When the DA goes narrative, those IDs don't exist in its output. The formatter reconstructs F1-Fn from the original research and uses them as the authoritative reference — the same pattern writer-formatter uses to reconstruct S-numbered claims from source material.

### The Three Input Cases

| Format | Signal | Handling |
|--------|--------|----------|
| **Canonical** | Starts with `ANALYSIS OUTPUT`, all required sections present | Strip stage narration prefix if present; validate fields; pass through with normalization |
| **Partial** | Has `ANALYSIS OUTPUT` header, one or more sections missing | Fill missing sections from original research; normalize present sections |
| **Narrative** | Essay/prose, `## Section` headers, no canonical structure | Extract evaluative statements as inferences; re-extract F1-Fn from original research; mark `traces_to: [narrative-mapped: uncertain]` |

**Stage narration leak:** If the DA response doesn't start with `ANALYSIS OUTPUT`, scan for its first occurrence and strip everything before it.

### Pipeline

**Stage 0 — Open:**
Write `ANALYSIS OUTPUT` as the literal first line of your response. Nothing before it.

**Stage 1 — Parse inputs:**
- Detect DA output format: `canonical` / `partial` / `narrative`
- Strip stage narration prefix if present
- From original research: re-extract F1-Fn as the authoritative finding list
- Emit parse summary: `Parsed: [n] findings | da-format=[canonical|partial|narrative] | [n] inferences detected`

**Stage 2 — Extract inferences:**
- **Canonical / partial:** pull inferences directly from DA output; validate `traces_to` IDs against F1-Fn
- **Narrative:** read DA prose for evaluative/conclusion statements; extract each as an inference; normalize type to `pattern|causal|evaluative|predictive`; mark `traces_to: [narrative-mapped: uncertain]`

**Stage 3 — Produce canonical ANALYSIS OUTPUT block:**
- `ANALYSIS BRIEF` — Question, Focus, Findings received, Inferences drawn, Quality score
- `FINDINGS` — F1-Fn re-extracted from original research (authoritative regardless of DA format)
- `INFERENCES` — extracted and normalized from Stage 2
- `UNUSED FINDINGS` — any finding not in any inference's `traces_to` and not in DA's own UNUSED FINDINGS
- `EVIDENCE GAPS` — from DA if present; from original research if not
- `QUALITY THRESHOLD RESULT` — `MET` if inferences extracted and findings accounted for; `NOT MET` if DA output is too incoherent to extract recognizable inferences

### Key Design Decision: Option A (Strict Extraction)

For `traces_to`: extract what's in the DA output. When `traces_to` cannot be confirmed (narrative failure case), mark as `[narrative-mapped: uncertain]`. Never invent finding IDs. Honest uncertainty is preferable to false precision.

Consistent with the formatter philosophy across the project: **extract, don't generate.**

---

## Scope of Change

Four files total:

| File | Change |
|------|--------|
| `specialists/data-analyzer-formatter/index.md` | **Create** — the formatter specialist |
| `behaviors/specialists.yaml` | **Modify** — register `data-analyzer-formatter` as agent |
| `context/specialists-instructions.md` | **Modify** — Rule 8 (matched-pair mandate), description, Typical Chain entries |
| `recipes/research-chain.yaml` | **Modify** — insert `data-analyzer-formatter` step between DA and Writer |

---

## What This Fixes

| Dimension | Before | After |
|-----------|--------|-------|
| Format Fidelity | DA can silently produce narrative instead of ANALYSIS OUTPUT | Formatter catches and normalizes any DA output |
| Chain Reliability | DA has input-framing sensitivity causing full failure | Chain completes regardless of DA output format |
| Research Trustworthiness | `traces_to` lost in narrative failure case | `traces_to` preserved (confirmed) or flagged (`[narrative-mapped: uncertain]`) — never silently lost |

Closes backlog item **#34**.

---

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-03-10 | Chris Park | Initial design — approved in brainstorming session |
