# Canvas Specialists — PR/FAQ

## Press Release

**Canvas Specialists gives Amplifier users research they can stake their reputation on.** Today, when you ask an AI to research something, you get a confident-sounding paragraph — but no sources, no confidence levels, and no way to tell what was verified versus invented. Canvas Specialists replaces that single-pass guess with a multi-agent pipeline where every claim traces to a source, every inference traces to a finding, and every gap in the evidence is named rather than papered over. Install the bundle, ask your question, and get output that's auditable — not just readable.

**Two speeds let you match the tool to the stakes.** Quick mode (3–5 minutes) runs a researcher and writer for orientation and exploration. Deep mode (~15 minutes) adds source corroboration, fact/inference separation, and quality gates that fail loud when evidence is thin. The system routes automatically based on how you ask — "what is X" stays quick, "write me a brief on X" goes deep — and you can always override. Canvas Specialists ships with researchers, writers, analysts, a competitive analysis specialist, a prioritizer, a storyteller, and a planner, all composable through natural language or recipes.

---

## Frequently Asked Questions

### 1. What does Canvas Specialists actually do?

It's a bundle of specialist AI agents for Amplifier that handle knowledge work — research, analysis, competitive intelligence, writing, prioritization, and planning. Instead of one LLM doing everything in a single pass, each specialist handles one stage of the work and passes structured output to the next. The researcher finds and tiers sources. The analyzer draws labeled inferences. The writer produces the document. Each stage has a defined contract, so the output is traceable end to end.

### 2. How do I install it?

One command: `amplifier bundle add git+https://github.com/cpark4x/canvas-specialists@main`. After that, just ask naturally — "research the competitive landscape for X" or "write me a brief on Y." The system handles routing, chaining, and output formatting automatically.

### 3. How is this different from just asking Amplifier to research something?

Default Amplifier research gives you a readable answer with no source accountability. Canvas Specialists gives you structured output where every claim has a confidence label (high/medium/low), a source URL, and a tier (primary/secondary/tertiary). The pipeline includes a corroboration stage that searches for a second independent source for every claim. When evidence is thin, the output says so explicitly instead of writing a confident paragraph anyway.

### 4. What specialists are included?

Seven domain specialists: **Researcher** (sourced evidence gathering), **Writer** (audience-calibrated documents in 6 formats), **Data Analyzer** (labeled inferences from evidence), **Competitive Analysis** (structured comparison matrices), **Prioritizer** (ranked lists with defensible rationale), **Planner** (structured plans with milestones and risks), and **Storyteller** (narrative from structured findings). Each has a matched formatter that ensures consistent output between stages.

### 5. Is it slow?

Quick mode takes 3–5 minutes. Deep mode takes about 15 minutes. That's the cost of corroboration, multi-stage processing, and quality gates. For casual questions — "what is X?" — just ask Amplifier directly; you don't need this. Canvas Specialists is for the work where someone will read your output critically and ask where you got it.

### 6. Does it cost more to run?

Yes. The deep chain spawns multiple specialist agents in sequence, which means more API calls and more tokens than a single-pass answer. The tradeoff is auditability — you're paying for source verification, fact/inference separation, and quality gates. For teams watching spend, use quick mode for exploration and reserve deep mode for deliverables.

### 7. What if the evidence doesn't support a confident answer?

The pipeline tells you. Quality gates at multiple stages produce explicit `QUALITY THRESHOLD RESULT: NOT MET` outputs when evidence is thin. Evidence gaps are named in the output as `EVIDENCE GAP` entries. This is a feature — a honest "I don't have enough to be confident" is more valuable than a polished paragraph built on nothing.

### 8. Can I use individual specialists without the full chain?

Yes. You can delegate directly to any specialist — `delegate(agent="specialists:researcher", ...)` — or run pre-built recipes for common chains (research-chain, competitive-analysis-brief, narrative-chain). You can also chain specialists manually in any order. The pipeline is composable, not monolithic.