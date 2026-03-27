# amplifier-research-specialist — PR/FAQ

## Press Release

**amplifier-research-specialist gives Amplifier users research they can stake their reputation on.** Today, when you ask an AI to research something, you get a confident paragraph — but no sources, no confidence levels, and no way to tell what was verified versus invented. amplifier-research-specialist replaces that single-pass guess with a multi-agent pipeline where every claim traces to a source, every inference traces to a finding, and every gap in the evidence is named rather than papered over. It's for the work where someone will read your output critically and ask where you got it — board briefs, vendor evaluations, competitive analyses, anything with a skeptical audience.

**Two speeds match the tool to the stakes.** Quick mode (3–5 minutes) runs a researcher and writer for exploration — "what is X" gets a sourced answer fast. Deep mode (~15 minutes) adds source corroboration, fact/inference separation, and quality gates that fail loud when evidence is thin — "write me a brief on X for my VP" triggers the full pipeline automatically. You can always override in either direction.

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

## Frequently Asked Questions

### 1. What does amplifier-research-specialist actually do?

It's a bundle of specialist AI agents for Amplifier that handle knowledge work — research, analysis, competitive intelligence, writing, prioritization, and planning. Instead of one LLM doing everything in a single pass, each specialist handles one stage of the work and passes structured output to the next. The researcher finds and tiers sources. The analyzer draws labeled inferences. The writer produces the document. Each stage has a defined contract, so the output is traceable end to end.

### 2. How do I install it?

Two commands:

```bash
amplifier bundle add git+https://github.com/cpark4x/amplifier-research-specialist@main
amplifier bundle use specialists --app
```

Then ask naturally — "research the competitive landscape for X" or "write me a brief on Y." The system handles routing, chaining, and output formatting automatically.

### 3. Can I try it in 5 minutes?

Yes. After installing, start a session and say: "Quick research on [any topic you're curious about]." You'll get a sourced brief in 3–5 minutes with confidence labels and source tiers. That's enough to see the difference from a default LLM answer. If you want to see the full pipeline, say "deep research on [topic]" — that takes ~15 minutes but shows every stage at work.

### 4. How is this different from just asking Amplifier to research something?

Default Amplifier research gives you a readable answer with no source accountability. amplifier-research-specialist gives you structured output where every claim has a confidence label (high/medium/low), a source URL, and a tier (primary/secondary/tertiary). The pipeline includes a corroboration stage that searches for a second independent source for every claim. When evidence is thin, the output says so explicitly instead of writing a confident paragraph anyway.

### 5. What specialists are included?

**Core pipeline** — these work together on research chains:

| Specialist | What it does |
|---|---|
| **researcher** | Finds and sources evidence — source tiering, per-claim confidence, explicit evidence gaps |
| **data-analyzer** | Draws labeled inferences from findings — every conclusion traces to specific evidence |
| **writer** | Produces audience-calibrated prose — facts cited, inferences hedged, gaps surfaced |

**Specialized tools** — invoke directly for specific tasks:

| Specialist | What you get |
|---|---|
| **competitive-analysis** | A comparison matrix your VP can read without asking follow-up questions |
| **prioritizer** | A ranked backlog you can defend to stakeholders — every item scored with visible rationale |
| **planner** | A plan with milestones, dependencies, and risks flagged before they surprise you |
| **storyteller** | Board decks and change comms that tell a story instead of dumping data |

### 6. Is it slow?

Quick mode takes 3–5 minutes. Deep mode takes about 15 minutes. That's the cost of corroboration, multi-stage processing, and quality gates. For casual questions — "what is X?" — just ask Amplifier directly; you don't need this. amplifier-research-specialist is for the work where getting it wrong has consequences.

### 7. Does it cost more to run?

Yes. The deep chain spawns multiple specialist agents in sequence, which means more API calls and more tokens than a single-pass answer. The tradeoff is auditability — you're paying for source verification, fact/inference separation, and quality gates. For teams watching spend, use quick mode for exploration and reserve deep mode for deliverables.

### 8. What are the limitations?

- **Public web only.** The pipeline can't reach behind paywalls, internal wikis, or private repositories. If your evidence lives in places the web can't reach, you'll get evidence gaps instead of findings.
- **Structured for traceability, not presentation.** RESEARCH OUTPUT and ANALYSIS OUTPUT blocks are machine-parseable but don't paste cleanly into Slack or email. You'll need to reformat before sharing outside Amplifier.
- **Deep chain is token-heavy.** Five or more agent sessions in sequence means real API spend. Quick mode handles most exploratory work at a fraction of the cost.

### 9. What would cause this to fail?

Two scenarios. You run a 15-minute deep research chain, get a sourced brief with trace references and confidence labels — then spend 10 minutes stripping all of that out so you can paste it into Slack. The time saved on research gets eaten by formatting. If that happens often enough, people stop using deep mode. Output presentation is an active area of improvement.

The other scenario: you research a niche topic with legitimately sparse public evidence. The quality gates fire `NOT MET` on every finding because nothing has two independent sources. You override the gates, get your brief anyway, and next time you skip the gates entirely. Once people learn to ignore the gates, the whole trust architecture collapses. The gates need to be calibrated tightly enough to catch real gaps without crying wolf on every emerging-market query.

### 10. Can I use individual specialists without the full chain?

Yes. Delegate directly to any specialist — `delegate(agent="specialists:researcher", ...)` — or run pre-built recipes for common chains (research-chain, competitive-analysis-brief, narrative-chain). You can also chain specialists manually in any order. The pipeline is composable, not monolithic.
