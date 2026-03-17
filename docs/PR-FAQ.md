# canvas-specialists — PR/FAQ

## Press Release

**canvas-specialists gives Amplifier users research they can stake their reputation on.** Today, when you ask an AI to research something, you get a confident paragraph — but no sources, no confidence levels, and no way to tell what was verified versus invented. canvas-specialists replaces that single-pass guess with a multi-agent pipeline where every claim traces to a source, every inference traces to a finding, and every gap in the evidence is named rather than papered over. It's for the work where someone will read your output critically and ask where you got it — board briefs, vendor evaluations, competitive analyses, anything with a skeptical audience.

**Two speeds match the tool to the stakes.** Quick mode (3–5 minutes) runs a researcher and writer for exploration — "what is X" gets a sourced answer fast. Deep mode (~15 minutes) adds source corroboration, fact/inference separation, and quality gates that fail loud when evidence is thin — "write me a brief on X for my VP" triggers the full pipeline automatically. You can always override in either direction.

---

## What the output looks like

A typical AI research response:

> *"OpenAI holds a dominant position in the enterprise AI market, with strong adoption among Fortune 500 companies. Anthropic is gaining ground, particularly among safety-conscious organizations."*

canvas-specialists on the same question:

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

## Frequently Asked Questions

### 1. What does canvas-specialists actually do?

It's a bundle of specialist AI agents for Amplifier that handle knowledge work — research, analysis, competitive intelligence, writing, prioritization, and planning. Instead of one LLM doing everything in a single pass, each specialist handles one stage of the work and passes structured output to the next. The researcher finds and tiers sources. The analyzer draws labeled inferences. The writer produces the document. Each stage has a defined contract, so the output is traceable end to end.

### 2. How do I install it?

Two commands:

```bash
amplifier bundle add git+https://github.com/cpark4x/canvas-specialists@main
amplifier bundle use specialists --app
```

Then ask naturally — "research the competitive landscape for X" or "write me a brief on Y." The system handles routing, chaining, and output formatting automatically.

### 3. Can I try it in 5 minutes?

Yes. After installing, start a session and say: "Quick research on [any topic you're curious about]." You'll get a sourced brief in 3–5 minutes with confidence labels and source tiers. That's enough to see the difference from a default LLM answer. If you want to see the full pipeline, say "deep research on [topic]" — that takes ~15 minutes but shows every stage at work.

### 4. How is this different from just asking Amplifier to research something?

Default Amplifier research gives you a readable answer with no source accountability. canvas-specialists gives you structured output where every claim has a confidence label (high/medium/low), a source URL, and a tier (primary/secondary/tertiary). The pipeline includes a corroboration stage that searches for a second independent source for every claim. When evidence is thin, the output says so explicitly instead of writing a confident paragraph anyway.

### 5. What specialists are included?

**Core pipeline** — these work together on research chains:

| Specialist | What it does |
|---|---|
| **researcher** | Finds and sources evidence — source tiering, per-claim confidence, explicit evidence gaps |
| **data-analyzer** | Draws labeled inferences from findings — every conclusion traces to specific evidence |
| **writer** | Produces audience-calibrated prose — facts cited, inferences hedged, gaps surfaced |

**Specialized tools** — invoke directly for specific tasks:

| Specialist | When to use it |
|---|---|
| **competitive-analysis** | Comparing vendors, products, or companies — produces structured comparison matrices |
| **prioritizer** | Ranking a backlog, roadmap items, or options — produces defensible ranked lists with rationale |
| **planner** | Breaking a goal into milestones — produces plans with dependencies, timelines, and risk flags |
| **storyteller** | Turning structured findings into narrative — for board decks, change comms, or persuasive briefs |

### 6. Is it slow?

Quick mode takes 3–5 minutes. Deep mode takes about 15 minutes. That's the cost of corroboration, multi-stage processing, and quality gates. For casual questions — "what is X?" — just ask Amplifier directly; you don't need this. canvas-specialists is for the work where getting it wrong has consequences.

### 7. Does it cost more to run?

Yes. The deep chain spawns multiple specialist agents in sequence, which means more API calls and more tokens than a single-pass answer. The tradeoff is auditability — you're paying for source verification, fact/inference separation, and quality gates. For teams watching spend, use quick mode for exploration and reserve deep mode for deliverables.

### 8. What if the evidence doesn't support a confident answer?

The pipeline tells you. Quality gates at multiple stages produce explicit `QUALITY THRESHOLD RESULT: NOT MET` outputs when evidence is thin. Evidence gaps are named in the output as `EVIDENCE GAP` entries. This is a feature — an honest "I don't have enough to be confident" is more valuable than a polished paragraph built on nothing.

### 9. Can I use individual specialists without the full chain?

Yes. Delegate directly to any specialist — `delegate(agent="specialists:researcher", ...)` — or run pre-built recipes for common chains (research-chain, competitive-analysis-brief, narrative-chain). You can also chain specialists manually in any order. The pipeline is composable, not monolithic.
