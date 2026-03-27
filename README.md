# amplifier-research-specialist

You ask an AI to research something and write it up. It reads well. Then someone asks "where did this number come from?" and you don't know. The document is fluent and completely unverifiable.

amplifier-research-specialist is a different architecture for AI research. Separate agents handle research, analysis, and writing independently — the researcher finds and sources evidence, the analyzer draws inferences and labels each one with the specific findings that support it, the writer produces prose where facts read like facts and conclusions read like conclusions. No single model doing everything in one pass with no accountability.

What it won't do matters as much as what it will. Missing evidence is reported, not hidden. Low-confidence claims are hedged, not asserted. Inferences that don't survive adversarial challenge don't ship. The output is trustworthy because it's honest about its limits.

Two speeds. **Quick** (3–5 min): researcher → writer, for exploration. **Deep** (~15 min): full pipeline with source verification, cross-finding analysis, and confidence calibration — for work someone will push back on.

Quality is measured, not claimed. Three adversarial critics — fact-checker, inference challenger, consistency auditor — score every pipeline run. On baseline evaluation: zero fabricated claims, zero misrepresented sources. Inference quality is the hardest dimension — it tests whether conclusions add genuine analytical value beyond restating the evidence — and it's actively improving with each pipeline iteration.

---

## What the output looks like

A typical AI research response:

> *"OpenAI holds a dominant position in the enterprise AI market, with strong adoption among Fortune 500 companies. Anthropic is gaining ground, particularly among safety-conscious organizations."*

amplifier-research-specialist on the same question:

```
FINDING [HIGH CONFIDENCE]
OpenAI holds ~60% share of enterprise API spend among F500 companies.
Sources: [S1] Menlo Ventures Enterprise AI Report 2024 (primary)
         [S2] Bloomberg Technology Survey Q3 2024 (secondary)

FINDING [MEDIUM CONFIDENCE]
Anthropic is the preferred alternative in regulated industries.
Source: [S3] Axios Pro Rata, Dec 2024 — 3 vendor interviews (secondary)
Note: No published survey data found. Treat as directional.

INFERENCE [traces to: F1, F3]
The enterprise AI market is bifurcating along risk tolerance lines —
regulated industries selecting for safety positioning over capability benchmarks.
Confidence: medium. Type: pattern.

EVIDENCE GAP
No independent data on Anthropic enterprise contract count or ARR.
Vendor claims only. Treat market share figures as unverified.
```

Every claim sourced. Inferences traced to the findings that support them. Gaps named, not hidden.

---

## The specialists

**Core pipeline** — these work together:

| Specialist | What it does |
|---|---|
| **researcher** | Finds and sources evidence — source tiering, per-claim confidence ratings, explicit evidence gaps |
| **data-analyzer** | Draws labeled inferences from findings — every conclusion traces to specific evidence |
| **writer** | Produces audience-calibrated prose — facts cited, inferences hedged, gaps surfaced, provenance footer |

**Specialized tools** — invoke directly for specific tasks:

| Specialist | What it does |
|---|---|
| **competitive-analysis** | Comparison matrices, positioning gaps, win conditions — head-to-head or landscape |
| **prioritizer** | Ranked lists with explicit framework scores and defensible rationale per item |
| **planner** | Structured plans with milestones, dependencies, timelines, and risk flags |
| **storyteller** | Converts structured findings into narrative with editorial selection record |

---

## Quick start

amplifier-research-specialist runs on [Amplifier](https://github.com/microsoft/amplifier).

```bash
amplifier bundle add git+https://github.com/cpark4x/amplifier-research-specialist@main
amplifier bundle use specialists --app
```

Then, in any Amplifier session:

*"Research Anthropic's approach to AI safety. I need to send this to my VP."*

The system detects that's a deep research request, runs the full pipeline, and returns a sourced brief in about 15 minutes. If you'd said *"quick overview of Anthropic"* instead, you'd get a lighter answer in 3–5 minutes.

That's it. The routing, specialist selection, and formatting happen automatically.

For direct control, see the [full usage guide](docs/USING-SPECIALISTS.md) — manual chaining, recipe invocation, and per-specialist parameters.

---

## How it works

**Quick path** — you ask something exploratory ("what is X", "overview of Y"). The researcher gathers evidence, the writer turns it into a brief. Two agents, 3–5 minutes.

**Deep path** — you ask for work product ("write me a brief on X", "I need to send this to my VP"). The full research-chain pipeline runs: research, source verification, analysis, writing. Each stage has one job and a typed output. The researcher only finds evidence. The analyzer only draws inferences. The writer only produces prose. No stage does another's job. About 15 minutes.

The system reads your intent and picks the right path. If it's ambiguous, it asks once. You can always say "go deeper" or "just give me a quick answer" to override.

Output schemas are the stable contract between stages. Implementations evolve freely — swap the researcher without touching the writer.

---

## Built by

[Chris Park](https://www.linkedin.com/in/chrispark) — Microsoft Office of the CTO, AI Incubation. Building the tools he actually uses.
