# Canvas Specialists: Success Metrics

**How we measure if Canvas Specialists is achieving its vision**

**Last Updated:** 2026-02-28

---

## Summary

Success for Canvas Specialists is measured by one thing: does delegating to a specialist produce better output than an orchestrator doing the work inline? Metrics are organized by phase (V1/V2/V3) and distinguish leading indicators (things that predict quality) from lagging ones (things that confirm it). We optimize for trustworthiness and composability, not speed or volume.

---

## Primary Success Indicator

**Does an orchestrator that delegates to specialists produce more trustworthy, better-structured output than one that doesn't?**

Every other metric is downstream of this. A specialist that doesn't improve on inline work isn't worth the delegation overhead.

---

## V1 Metrics: Research Quality

**Phase Goal:** Validate that the Researcher produces structured, source-tiered evidence that an orchestrator cannot produce inline.

### Leading Indicators

**Source coverage:**
- Researcher consults ≥3 distinct source types per query
- Source discovery checklist is populated before fetching begins
- Paywall fallback ladder is attempted before marking a source as inaccessible

**Evidence structure:**
- Every finding has a source, tier (primary/secondary/tertiary), and confidence level
- Evidence gaps are named explicitly, not omitted
- Quality Gate fires at least once per session (proving it's not a rubber stamp)

### Lagging Indicators

**Output trustworthiness:**
- Caller can trace every claim in a downstream document back to a finding in ResearchOutput
- Zero invented claims in findings (sourced vs unsourced claims ratio = 100%)
- Quality score accurately predicts downstream usefulness

**Composability:**
- ResearchOutput passes to Writer without preprocessing
- Schema version has not needed a breaking change

### Qualitative Signals

**Signals we want to hear:**
- "The gaps section told me exactly what I needed to search next"
- "I trusted the output because I could see where every claim came from"
- "It found sources I wouldn't have thought to check"

**Red flags:**
- "I had to verify everything anyway"
- "The confidence ratings felt arbitrary"
- "It returned findings but I couldn't tell where they came from"

---

## V2 Metrics: Writing Quality

**Phase Goal:** Validate that the Writer produces better documents from structured input than an orchestrator writing prose directly from research findings.

### Leading Indicators

**Coverage audit:**
- Writer runs coverage audit before drafting on every task
- Coverage gaps are surfaced to the caller, not silently omitted
- Writer stops and flags critical gaps before producing a partial document

**Format fidelity:**
- Output format matches requested format on every invocation
- WRITER METADATA block is present and complete on every output

### Lagging Indicators

**Source fidelity:**
- Zero claims in output that aren't traceable to source material
- Confidence signals from source (medium/high) are preserved in prose, not upgraded

**Chain quality:**
- Researcher → Writer chain produces a usable document without intermediate human editing
- Writer output requires fewer revisions than inline-written documents

### Qualitative Signals

**Signals we want to hear:**
- "I handed it the research and got back something I could actually send"
- "It flagged a gap I hadn't noticed before I wasted time on the wrong document"
- "The brief format was exactly right — not a report in brief clothing"

**Red flags:**
- "It added things that weren't in the research"
- "The format said brief but it read like a report"
- "It just ignored the gaps and wrote confidently anyway"

---

## V3 Metrics: Ecosystem Maturity

**Phase Goal:** Validate that the specialist pattern is repeatable — new specialists (Analyst, Presenter, Communicator) can be added without breaking the framework, and the ecosystem composes cleanly.

### Leading Indicators

**Framework stability:**
- New specialists added using `docs/adding-a-specialist.md` without requiring changes to shared infrastructure
- `shared/interface/types.md` schema version has not required a breaking change across the V3 specialists

**Inter-specialist composability:**
- Analyst output passes to Writer without schema adaptation
- Full chain (Researcher → Analyst → Writer) produces coherent output

### Lagging Indicators

**Ecosystem adoption:**
- Orchestrators choose the correct specialist for a task without prompting
- Context file (`context/specialists-instructions.md`) accurately guides delegation decisions

---

## What We Don't Measure

### ❌ Speed / latency
**Why not:** The Researcher runs a Quality Gate that may trigger additional passes. Faster output that skips the gate is worse output. We optimize for trustworthiness, not time-to-response.

### ❌ Number of sources fetched
**Why not:** Three high-quality primary sources beat fifteen low-quality ones. Volume of sources is not a proxy for research quality.

### ❌ Word count of output
**Why not:** A short honest output with named gaps is more valuable than a long confident-sounding one that papers over them. Length is not quality.

### ❌ Number of specialists built
**Why not:** Five excellent composable specialists beat ten mediocre ones. The ecosystem design doc defines the right build order — we don't accelerate it at the cost of quality.

---

## Success Criteria by Phase

### V1 Success = Researcher Is Trustworthy

**Must achieve:**
- Every finding is sourced, tiered, and confidence-rated
- Evidence gaps are always disclosed, never omitted
- ResearchOutput schema is stable (no breaking changes needed after v1.0)

**Qualitative validation:**
- A caller can audit any output and verify every claim traces to a source
- The Researcher's output is more useful as Writer input than an inline research summary

### V2 Success = Writer Closes the Chain

**Must achieve:**
- Researcher → Writer chain produces a usable document without human editing in the middle
- Coverage audit fires on every task (not skipped for speed)
- Format fidelity is 100% (output matches requested format)

**Qualitative validation:**
- Documents produced by the chain require fewer revisions than inline-written equivalents
- Coverage gaps are flagged before drafting, not discovered after

### V3 Success = The Pattern Is Repeatable

**Must achieve:**
- Analyst and Presenter specialists built using the same contributor guide, no framework changes needed
- Full chain (Researcher → Analyst → Writer) composes without schema adaptation

**Qualitative validation:**
- A new contributor can add a specialist by following `docs/adding-a-specialist.md` alone
- Orchestrators route to the correct specialist without explicit instruction

---

## The Standard

**If a metric doesn't help us answer "does the specialist produce more trustworthy output than inline work?", we don't track it.**

Specialists exist to raise the quality floor. Every measurement should connect back to that.
