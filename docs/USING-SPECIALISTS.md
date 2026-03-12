---
title: Using Canvas Specialists
audience: new users, orchestrator authors
last_updated: 2026-03-03
---

# Using Canvas Specialists

A practical guide to invoking specialists, understanding their output, and chaining them together.

---

## Why specialists instead of just asking an LLM?

When you ask an LLM to "research X and write me a report," it does both in one pass — with no separation between facts and inferences, no explicit source tiering, no stated confidence, and no honest accounting of what it couldn't find. The output sounds authoritative. You have no way to verify it is.

Specialists solve this by enforcing role separation:

- The **Researcher** gathers facts. It cites every claim, rates every source, and names every gap. It never infers.
- The **Data Analyzer** draws conclusions. Every inference traces to specific findings. It never fabricates.
- The **Writer** writes prose. Every sentence traces to source material. It never adds interpretation.

The result: output you can audit. You know what was found, what wasn't, what's a fact, what's a conclusion, and how confident each claim is.

---

## The Specialists

### Researcher

**Job:** Find, source, and confidence-rate discrete factual claims. Return structured evidence — not a summary, not an analysis.

**When to use:** Anytime you need sourced evidence you can defend. Market research, competitive intelligence, technical due diligence, fact-checking.

**What it does that a one-shot LLM call won't:**
- Runs a structured source discovery pass before fetching anything
- Attempts paywall fallbacks before giving up
- Rates every finding (primary / secondary / tertiary source, high / medium / low confidence)
- Corroborates claims across independent sources before marking them high-confidence
- Names what it couldn't find, with fallbacks tried — evidence gaps are first-class output

**Invoke:**
```python
research = delegate(
    agent="specialists:researcher",
    instruction="""
    Research question: [your question]
    quality_threshold: medium   # low | medium | high
    """
)
```

**Parameters:**
- `quality_threshold` — sets the bar for how much corroboration the quality gate requires before returning. Default: `medium`.

---

### Data Analyzer

**Job:** Read sourced findings. Draw labeled, traceable conclusions. Return findings + inferences together — clearly separated.

**When to use:** You have research findings and need to know what they *mean* — not just what they say. Between the Researcher and the Writer in a chain, or standalone when you have your own findings.

**What it does that a one-shot LLM call won't:**
- Every inference traces to specific finding IDs — no ungrounded conclusions
- Every finding is accounted for: either used in an inference or listed as unused with a typed reason
- Inference types are explicit: `pattern` | `causal` | `evaluative` | `predictive`
- Fails loud — if evidence doesn't support a confident inference, it says so

**Invoke:**
```python
analysis = delegate(
    agent="specialists:data-analyzer",
    instruction="""
    Analyze the following research findings.

    Research question: [your question]

    Findings:
    - Claim: [...]  Source: [...] | Tier: [primary|secondary|tertiary] | Confidence: [high|medium|low]
    - Claim: [...]  Source: [...] | Tier: [...] | Confidence: [...]

    quality_threshold: medium   # low | medium | high
    """
)
```

Or pass the Researcher's full output directly:
```python
analysis = delegate(
    agent="specialists:data-analyzer",
    instruction=f"Analyze the following research. quality_threshold: medium\n\n{research.response}"
)
```

**Parameters:**
- `quality_threshold` — minimum confidence for an inference to be included. Default: `medium`.
- `focus_question` — optional. Sharpens inferences toward a specific sub-question. Findings outside scope are marked `out_of_scope` in unused findings.

**Inference types:**
| Type | When it fires |
|---|---|
| `pattern` | Multiple findings point the same direction ("consistently true across sources") |
| `causal` | One finding explains another ("X because Y") |
| `evaluative` | A judgment the evidence supports ("X is ready / not ready") |
| `predictive` | A forward-looking conclusion the evidence warrants ("X suggests Y will...") |

---

### Writer

**Job:** Transform structured evidence or analysis into polished, format-faithful prose. Never adds claims the source material doesn't support.

**When to use:** You have research or analysis output and need it turned into a document a human can read and act on.

**What it does that a one-shot LLM call won't:**
- Audits coverage before writing — flags what can't be supported before drafting
- Every factual sentence has an inline source marker
- CITATIONS block maps every marker back to its source and confidence
- Inferences are labeled as conclusions in prose ("the evidence suggests...") — not stated as facts
- Surfaces coverage gaps explicitly — doesn't write around missing evidence

**Invoke:**
```python
document = delegate(
    agent="specialists:writer",
    instruction=f"""
    Format: brief           # report | brief | email | memo | proposal | executive-summary
    Audience: [who's reading this]
    Voice: executive        # formal | conversational | executive

    Source material:
    {research.response}     # or analysis.response
    """
)
```

---

### Competitive Analysis

**Job:** Structure competitive intelligence — comparison matrices, positioning gaps, win conditions. Two modes: head-to-head and landscape.

**When to use:** Comparing products, vendors, or competitors. Returns structured data designed for decision-making, not narrative.

**Invoke:**
```python
comp = delegate(
    agent="specialists:competitive-analysis",
    instruction="""
    Compare [A] vs [B] for [use case].
    Mode: head-to-head      # head-to-head | landscape
    """
)
```

---

## The Three Chains

### Chain 1: Research only
Use when you need sourced evidence and will write or analyze it yourself.

```python
research = delegate(
    agent="specialists:researcher",
    instruction="Research question: [your question]"
)
# research.response contains structured findings, source citations, evidence gaps
```

---

### Chain 2: Research → Write
Use when you need a document from sourced evidence, without drawing explicit conclusions. The Writer stays close to the facts.

```python
research = delegate(
    agent="specialists:researcher",
    instruction="Research question: [your question]"
)

document = delegate(
    agent="specialists:writer",
    instruction=f"""
    Format: brief
    Audience: [your audience]

    Source material:
    {research.response}
    """
)
```

---

### Chain 3: Research → Analyze → Write
Use when you need a document that contains *conclusions*, not just facts. The Analyzer explicitly labels what's a finding vs what's an inference, so the Writer can represent each correctly in prose.

```python
research = delegate(
    agent="specialists:researcher",
    instruction="Research question: [your question]"
)

analysis = delegate(
    agent="specialists:data-analyzer",
    instruction=f"Analyze the following research. quality_threshold: medium\n\n{research.response}"
)

document = delegate(
    agent="specialists:writer",
    instruction=f"""
    Format: brief
    Audience: [your audience]

    Source material:
    {analysis.response}
    """
)
```

**When does Chain 3 matter over Chain 2?**

Chain 2 produces a document that reports what was found. Chain 3 produces a document that also says what it *means*. If the document needs a "recommendation" or "so what" section grounded in the evidence — use Chain 3.

---

## Real Example: Data Analyzer in Action

**Input (5 findings on monolith → microservices migration):**

```
- 40% faster deployment cycles post-migration (primary, high confidence)
- Operational complexity increases significantly (secondary, high confidence)
- 65% of adopters cite team autonomy as top benefit (secondary, medium confidence)
- 12–24 month average migration timeline (secondary, medium confidence)
- Companies with < 50 engineers rarely see net productivity gains (secondary, medium confidence)
```

**What the Data Analyzer produced:**

> *Teams that migrated to microservices reported 40% faster independent deployment cycles.*
> *Microservices increase operational complexity — teams need service mesh, distributed tracing, and container orchestration expertise.*

It recognized the core tension immediately:

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

This is what the specialist adds. A one-shot "analyze these findings" call produces a verdict. The Analyzer produces a *traceable* verdict with typed inferences, explicit unused findings, and named gaps — the difference between an answer and a defensible answer.

---

## What Good Output Looks Like

**Researcher:** Every finding has a source URL, tier (primary/secondary/tertiary), confidence (high/medium/low), and corroboration count. Evidence gaps are named with fallbacks attempted. The output is auditable — you can trace every claim.

**Data Analyzer:** Every inference says which findings support it (`traces_to: F1, F3`), its type (`evaluative`), and its confidence. Findings that didn't yield inferences appear in UNUSED FINDINGS with a reason. Nothing is silently dropped.

**Writer:** Every factual sentence has an inline source marker. A CITATIONS block at the end maps every marker back to its source and location in the document. Coverage gaps appear before the document begins — the Writer surfaces what it couldn't write, rather than writing around it.

---

## Known Limitations

**Format compliance on complex topics.** When given a highly engaging research question, the Researcher and Writer sometimes produce rich narrative output rather than the exact structured block format (RESEARCH OUTPUT, WRITER METADATA). The content is high quality — sources, citations, and confidence ratings are present — but the machine-parseable block structure may not be perfectly formed. This affects automated downstream parsing more than human readability.

**The Data Analyzer accepts both formats.** It can process canonical RESEARCH OUTPUT block format and narrative Researcher output. If the Researcher produces narrative, the Analyzer still works.

**Mitigation in progress.** A provider-level fix (PR #38 against amplifier-module-provider-anthropic) implements Anthropic's native structured output API, which will enforce format compliance at the API level rather than relying on prompt instructions. Until that merges, treat structured block format as best-effort for the Researcher and Writer, and reliable for the Data Analyzer.

---

## Common Questions

**Can I use the Data Analyzer without running the Researcher first?**
Yes. Pass your own findings directly in the instruction. The format is flexible — you can provide findings as bullet points, a structured block, or even notes from your own research.

**Can I use the Writer without the Researcher?**
Yes. Pass any source material — notes, a document, findings — and specify `input type: raw-notes`. The Writer will audit coverage and write from whatever you give it.

**What if the Researcher can't find sources?**
Evidence gaps are explicit in the output, not hidden. The Researcher will name what it couldn't find, what fallbacks it attempted, and why it was inaccessible. A partial result with honest gaps is more useful than a confident-sounding complete result.

**What quality_threshold should I use?**
- `low` — return findings even with single-source, low-confidence claims. Good for exploratory research.
- `medium` — default. Requires corroboration for high-priority claims.
- `high` — triggers additional corroboration passes. Slower, stricter. Use when you need to stake something important on the findings.
