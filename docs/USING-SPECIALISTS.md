---
title: Using Amplifier Research Specialist
audience: new users, orchestrator authors, AI agents
last_updated: 2026-03-14
---

# Using Amplifier Research Specialist

A practical guide to getting research done with specialists.

---

## How to use it

Three paths, from simplest to most control.

### Just ask

In any Amplifier session with specialists installed, ask your question:

*"Research Anthropic's approach to AI safety. I need to send this to my VP."*

The system determines depth from your request:

| Your message signals... | What happens | Time |
|---|---|---|
| Exploration — "what is X", "overview of Y", "quick summary" | Researcher → Writer | 3–5 min |
| Work product — "write me a brief", "deep dive", "I need to send this to..." | Full research-chain pipeline | ~15 min |
| Ambiguous | System asks once: "Quick answer or deep research?" | — |

You can always override: "go deeper" or "just give me a quick answer."

### Run the recipe

For the full sourced pipeline directly:

```bash
amplifier tool invoke recipes operation=execute \
  recipe_path=recipes/research-chain.yaml \
  context='{"research_question": "Your question here"}'
```

### Chain manually

For full control over which specialists run and what you pass between them:

```python
research = delegate(agent="specialists:researcher", instruction="Research X")
analysis = delegate(agent="specialists:data-analyzer", instruction=f"Analyze: {research.response}")
document = delegate(agent="specialists:writer", instruction=f"Brief for product team: {analysis.response}")
```

Each specialist's output schema is the next one's input contract. Skip stages when you don't need them — the Writer works fine with raw research, no analysis required.

---

## Specialist reference

### Researcher

**Job:** Find, source, and confidence-rate factual claims.

**When to use:** You need sourced evidence you can defend — market research, competitive intelligence, due diligence, fact-checking.

**Invoke:**
```python
research = delegate(
    agent="specialists:researcher",
    instruction="Research question: [your question]\nquality_threshold: medium"
)
```

**quality_threshold:** `low` (exploratory, single-source OK) | `medium` (default, corroboration required) | `high` (additional passes, slower, for high-stakes work)

---

### Data Analyzer

**Job:** Draw labeled, traceable inferences from research findings. Every conclusion traces to specific evidence.

**When to use:** You have findings and need to know what they *mean* — not just what they say. Works between the Researcher and Writer, or standalone with your own findings.

**Invoke:**
```python
analysis = delegate(
    agent="specialists:data-analyzer",
    instruction=f"Analyze the following research.\n\n{research.response}"
)
```

**Inference types:** `pattern` (multiple findings converge) | `causal` (X because Y) | `evaluative` (X is ready / not ready) | `predictive` (X suggests Y will...)

---

### Writer

**Job:** Transform structured evidence or analysis into polished, format-faithful prose. Never adds claims the source material doesn't support.

**When to use:** You have research or analysis output and need a document a human can read and act on.

**Invoke:**
```python
document = delegate(
    agent="specialists:writer",
    instruction=f"Format: brief\nAudience: [who reads this]\nVoice: executive\n\n{analysis.response}"
)
```

**Formats:** `brief` | `report` | `email` | `memo` | `proposal` | `executive-summary`

Every document ends with a provenance footer: *"Based on N sourced findings from M sources. K analytical inferences drawn from cross-finding synthesis."*

---

### Competitive Analysis

**Job:** Comparison matrices, positioning gaps, win conditions.

**When to use:** Comparing products, vendors, or competitors. Returns structured data for decision-making.

**Invoke:**
```python
comp = delegate(
    agent="specialists:competitive-analysis",
    instruction="Compare [A] vs [B] for [use case].\nMode: head-to-head"
)
```

**Modes:** `head-to-head` | `landscape`

---

### Prioritizer

**Job:** Rank items with explicit framework scores and defensible rationale.

**When to use:** Backlog grooming, roadmap decisions, vendor selection — any list that needs justified ordering.

**Invoke:**
```python
ranked = delegate(
    agent="specialists:prioritizer",
    instruction="Prioritize these items for next sprint:\n[your items]"
)
```

**Frameworks:** MoSCoW | impact-effort | RICE | weighted scoring (auto-selected or specify)

---

### Planner

**Job:** Structured plans with milestones, dependencies, timelines, and risk flags.

**When to use:** Going from "here's what I want" to "here's the plan."

**Invoke:**
```python
plan = delegate(
    agent="specialists:planner",
    instruction="Plan the migration to microservices. Timeline: 6 months."
)
```

---

### Storyteller

**Job:** Convert structured findings into narrative with a documented editorial selection record.

**When to use:** The audience needs to be moved, not just informed — board narratives, executive briefings, change communications.

**Invoke:**
```python
story = delegate(
    agent="specialists:storyteller",
    instruction=f"Board narrative. Audience: board. Tone: trustworthy.\n\n{analysis.response}"
)
```

---

## Example: Data Analyzer in action

**Input (5 findings on monolith → microservices migration):**

```
- 40% faster deployment cycles post-migration (primary, high confidence)
- Operational complexity increases significantly (secondary, high confidence)
- 65% of adopters cite team autonomy as top benefit (secondary, medium confidence)
- 12–24 month average migration timeline (secondary, medium confidence)
- Companies with < 50 engineers rarely see net productivity gains (secondary, medium confidence)
```

The Analyzer recognized the core tension immediately:

> **"The question isn't 'do microservices work?' The question is 'are we in the band where they work?'"**

And produced a decision framework:

```
Gate 1 — Team size ≥ 50 engineers?
  NO  → Do not migrate. Net productivity gain is unlikely.
  YES → Proceed to Gate 2.

Gate 2 — Is the primary pain organizational (team coupling, deployment bottlenecks)?
  NO  → Microservices are the wrong tool.
  YES → Proceed to Gate 3.
...
```

And named what the findings couldn't answer:

> *No failure / stall rate data. No cost-of-inaction data. F5's threshold is a heuristic, not a studied cutoff.*

A direct LLM call produces a verdict. The Analyzer produces a *traceable* verdict with typed inferences, explicit unused findings, and named gaps — the difference between an answer and a defensible answer.

---

## Common questions

**Can I use any specialist standalone?**
Yes. Each specialist accepts direct input. Pass findings to the Analyzer, notes to the Writer, items to the Prioritizer. No chaining required.

**What if the Researcher can't find sources?**
Gaps are explicit output, not failures. The Researcher names what it couldn't find, what it tried, and why. A partial result with honest gaps is more useful than a confident-sounding complete result.

**Quick or deep — how do I choose?**
Quick for orientation ("is this topic worth digging into?"). Deep for anything someone else will read. When in doubt, the system asks.

**What are the formatters?**
Internal pipeline stages (researcher-formatter, data-analyzer-formatter, writer-formatter) that normalize specialist output into canonical format. You never invoke them directly — the pipeline handles them automatically, and skips them when the output is already well-formed.
