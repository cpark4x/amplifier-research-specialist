# canvas-specialists

**When you ask a generalist AI to research something, you get confident-sounding prose with no way to audit the claims.** canvas-specialists produces structured research and writing outputs where every finding traces to a source, every inference is labeled as an inference, and every gap is named explicitly — output you can hand to a decision-maker without re-verifying everything first.

Battle-tested across 2,500+ agent runs. Used for competitive briefs on AI providers, market analysis, and product research.

---

## What makes it different

Here's what a typical AI research output looks like:

> *"OpenAI holds a dominant position in the enterprise AI market, with strong adoption among Fortune 500 companies. Anthropic is gaining ground, particularly among safety-conscious organizations."*

No sources. No confidence levels. No acknowledgment of what it doesn't know. You can't audit it.

Here's what canvas-specialists produces:

```
FINDING [HIGH CONFIDENCE]
OpenAI holds ~60% share of enterprise API spend among F500 companies.
Sources: [S1] Menlo Ventures Enterprise AI Report 2024 (primary)
          [S2] Bloomberg Technology Survey Q3 2024 (secondary)

FINDING [MEDIUM CONFIDENCE]
Anthropic is the preferred alternative in regulated industries (finance, healthcare).
Source: [S3] Axios Pro Rata, Dec 2024 — based on 3 vendor interviews (secondary)
Note: No published survey data found. Treat as directional, not quantified.

EVIDENCE GAP
No independent data on Anthropic's enterprise contract count or ARR.
Vendor claims only. Treat Anthropic market share figures as unverified until confirmed.
```

Every claim is traceable. Every inference is labeled. Every gap is named.

---

## The specialists

| Specialist | What it produces | Status |
|---|---|---|
| **researcher** | Structured findings with source tiering (primary / secondary / tertiary), per-claim confidence ratings (high / medium / low), and explicit evidence gap reporting | v1 |
| **writer** | Polished documents with inline citations `[S1]`, a `CLAIMS TO VERIFY` block, and audience-calibrated prose | v1 |
| **competitive-analysis** | Comparison matrices, positioning gaps, and win conditions — head-to-head or landscape modes | v1 |
| **data-analyzer** | Labeled inferences that bridge fact and conclusion — explicitly separated from source findings so the reasoning is always visible | v1 |
| [storyteller](specialists/storyteller/) | cognitive mode translation — converts structured findings (AnalysisOutput, ResearchOutput) into narrative-mode artifacts with a documented NARRATIVE SELECTION record | v1 |
| [story-formatter](specialists/story-formatter/) | format normalization for storyteller output — takes narrative prose in any format and produces canonical STORY OUTPUT blocks with NARRATIVE SELECTION classification | v1 |
| [writer-formatter](specialists/writer-formatter/) | format normalization for writer output — takes prose in any format plus source material and produces canonical Writer output with Parsed:, WRITER METADATA, CITATIONS, and CLAIMS TO VERIFY blocks | v1 |

All shipped and production-ready. More specialists are planned, including Presentation Builder — see [docs/BACKLOG.md](docs/BACKLOG.md) for what's coming next.

---

## Quick start

canvas-specialists runs on [Amplifier](https://github.com/microsoft/amplifier) — a lightweight agent framework that handles routing, context passing, and multi-step orchestration. If you're already using Amplifier, specialists drop in as a bundle. If you're not, start there first.

### 1. Add the bundle

Run these two commands from inside your project directory:

```bash
amplifier bundle add git+https://github.com/cpark4x/canvas-specialists@main
amplifier bundle use specialists --project
```

> **Global install** — to make specialists available in every Amplifier session you run, regardless of project:
> ```bash
> amplifier bundle add git+https://github.com/cpark4x/canvas-specialists@main --app
> ```
> The `--app` flag registers canvas-specialists as an app bundle that is automatically composed onto every session. Useful if you use specialists regularly across many projects.

### 2. Invoke a specialist

```python
research = delegate(
    agent="specialists:researcher",
    instruction="Research the enterprise AI infrastructure market. Return structured findings."
)
```

### 3. Chain them together

Specialists are composable by design. Each one's output schema is the next one's input contract.

```python
# Stage 1: gather evidence
research = delegate(
    agent="specialists:researcher",
    instruction="Research X. Return structured findings."
)

# Stage 2: draw inferences
analysis = delegate(
    agent="specialists:data-analyzer",
    instruction=f"Analyze these findings and draw labeled inferences: {research.response}"
)

# Stage 3: produce the document
document = delegate(
    agent="specialists:writer",
    instruction=f"Write an executive brief for a product team. Source material: {analysis.response}"
)
```

See [docs/USING-SPECIALISTS.md](docs/USING-SPECIALISTS.md) for the full practical guide, and [docs/examples/researcher-to-writer.md](docs/examples/researcher-to-writer.md) for a walkthrough with sample inputs and outputs.

---

## How it works

Each specialist runs as a sequence of discrete, auditable stages — not a single prompt. The researcher runs source retrieval, tiering, claim extraction, and confidence rating as separate steps, each with a clean output. Individual stages are improvable, debuggable, and replaceable independently.

**The output schema is the stable contract.** Implementations can evolve freely. The schema does not change without a version bump and coordinated update to callers. Downstream specialists — and your orchestrator — depend on the schema, not the implementation details.

**Gaps are first-class outputs.** Missing evidence is never silently dropped. If the researcher can't find primary source data for a claim, it says so. The writer surfaces that as `CLAIMS TO VERIFY`. You know exactly what needs verification before anything gets published or presented.

---

## Built by

[Chris Park](https://www.linkedin.com/in/chrispark) — Senior PM at Microsoft's Office of the CTO, AI Incubation group, with 17 years of PM experience and an engineering degree from Waterloo. Building the tools he actually uses.
