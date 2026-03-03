# Specialists

A library of best-in-class, single-domain AI specialist agents for knowledge worker and consumer scenarios — each built with a focused pipeline, rigorous quality gates, and a clean interface contract.

> A specialist is like a consultant with a toolbox. A skill is a textbook. A specialist *does the work.*

---

## Quick Start

### Prerequisites

- [Amplifier](https://github.com/microsoft/amplifier) installed and configured
- An API key for a supported LLM provider (Anthropic, OpenAI, Azure, etc.)

### 1. Add this bundle to your project

In your project's `.amplifier/settings.yaml`:

```yaml
bundles:
  - source: git+https://github.com/[owner]/canvas-specialists@main
    name: specialists
```

### 2. Use a specialist

In any Amplifier session, specialists are available for delegation:

```
"Research the competitive landscape for async Python frameworks and return structured findings"
```

The orchestrator routes to the right specialist automatically. To invoke directly:

```python
delegate(agent="specialists:specialists/researcher", instruction="Research X...")
delegate(agent="specialists:specialists/writer", instruction="Write a brief from this research...")
```

### 3. Chain researcher → writer

```python
# Step 1: gather evidence
research = delegate(
    agent="specialists:specialists/researcher",
    instruction="Research X. Return structured findings."
)

# Step 2: turn evidence into a document
document = delegate(
    agent="specialists:specialists/writer",
    instruction=f"Write an executive brief for a product team. Source material: {research.response}"
)
```

See [docs/USING-SPECIALISTS.md](docs/USING-SPECIALISTS.md) for the full practical guide — invoking each specialist, understanding output, and chaining them together.

For a detailed walkthrough of the researcher → writer chain with sample inputs and outputs, see [docs/examples/researcher-to-writer.md](docs/examples/researcher-to-writer.md).

---

## Available Specialists

| Specialist | Domain | Status |
|---|---|---|
| [researcher](specialists/researcher/) | Structured web research with source tiering, quality gates, and confidence-rated findings | v1 |
| [writer](specialists/writer/) | Transforms structured source material into polished prose with inline citations and coverage auditing | v1 |
| [competitive-analysis](specialists/competitive-analysis/) | Structured competitive intelligence with comparison matrices, positioning gaps, and win conditions — head-to-head and landscape modes | v1 |
| [data-analyzer](specialists/data-analyzer/) | Draws labeled inferences from ResearchOutput — fills the fact/inference gap between Researcher and Writer | v1 |

More specialists are planned — see [docs/BACKLOG.md](docs/BACKLOG.md) for the full roadmap (Storyteller, Competitive Analysis, Presentation Builder, and more).

---

## How Specialists Work

Specialists are **stateless domain experts**. Each one:

- Has a single job and a focused multi-stage pipeline for that job
- Exposes a defined interface contract — what it accepts, what it returns, what it won't do
- Is UI-independent — callable identically from Canvas, CLI, another agent, or any orchestrator
- Never manages its own memory — loads context in, produces structured output out
- Is honest about gaps — missing evidence and coverage failures are first-class outputs, never silently dropped

**The specialist never knows where it's being called from.** The interface contract is the only boundary it knows.

---

## Shared Interface

`shared/interface/types.md` defines the stable output contracts all specialists follow. Orchestrators and downstream specialists depend on these — they do not change when implementations evolve.

---

## Design Principles

**Outcome over speed.** The primary design constraint is quality of output, not time-to-output. Speed is what you opt into. Quality is the default.

**The output schema is the center.** Each specialist's output schema is its stable contract. Implementations evolve freely. The schema does not change without a version bump and coordinated update to callers.

**Mechanism, not policy.** Specialists expose their behavior as configurable parameters. Defaults are tuned for quality. Callers opt into speed or alternative behavior.

**Composable stages.** Specialists run as sequences of discrete stages — each with one job and a clean output. Individual stages are improvable, debuggable, and swappable independently.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) to get started.
To add a new specialist, follow [docs/adding-a-specialist.md](docs/adding-a-specialist.md).
