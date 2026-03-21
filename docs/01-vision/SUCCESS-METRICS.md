# Canvas Specialists: Success Metrics

**How we measure if Canvas Specialists is achieving its vision**

**Owner:** Chris Park  
**Last Updated:** 2026-03-04  

---

## Table of Contents

1. [Summary](#summary)
2. [Primary Success Indicator](#primary-success-indicator)
3. [V1 Metrics: Research Quality](#v1-metrics-research-quality)
4. [V2 Metrics: Writing Quality](#v2-metrics-writing-quality)
5. [Storyteller Metrics](#storyteller-metrics)
6. [V3 Metrics: Ecosystem Maturity](#v3-metrics-ecosystem-maturity)
7. [What We Don't Measure](#what-we-dont-measure)
8. [Success Criteria by Phase](#success-criteria-by-phase)
9. [The Standard](#the-standard)

---

## Summary

Success for Canvas Specialists is measured by one thing: does delegating to a specialist produce better output than an orchestrator doing the work inline? Metrics are organized by phase (V1/V2/V3) and distinguish leading indicators (things that predict quality) from lagging ones (things that confirm it). We optimize for trustworthiness and composability, not speed or volume.

---

## Primary Success Indicator

**Does including this specialist in the chain produce better output at the end of the chain than a chain that leaves it out — and does it do so by filling a role no other link in the chain is authorized to fill?**

Every other metric is downstream of this. The comparison is not against inline work — it is against the chain without this link. A specialist that doesn't improve the final output, or whose job could be done by an adjacent specialist, isn't worth the delegation overhead.

---

## Universal Baseline Criteria

Every specialist — regardless of domain — must satisfy all four before it is considered production-ready. These are the admission criteria for being called a specialist.

**U1 — Output schema is a contract.**
Whatever the specialist returns, downstream consumers can depend on it. Schema changes require coordinating all downstream consumers. Changing field names or removing sections is a breaking change.

**U2 — Quality gate is real, not decorative.**
Every specialist has a quality gate. The gate must be capable of returning NOT MET. A gate that always returns MET is not gating anything — it is providing false assurance.

**U3 — Fails loud, not silent.**
When the specialist cannot meet the requested quality level, that is stated explicitly. It never silently returns lower-quality output as if nothing happened.

**U4 — Fills a role no other link in the chain is authorized to fill.**
There must be at least one thing this specialist does that an adjacent specialist is explicitly prohibited from doing. If its job could be done by another specialist without violating that specialist's core principles, it is not a specialist — it is a duplicate.

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
- Researcher → Formatter → Writer chain produces canonical output without manual intervention
- Formatter successfully normalizes researcher output on every run
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

## Formatter Metrics

**Phase Goal:** Validate that the Formatter reliably converts any researcher output into canonical ResearchOutput format — the essential bridge between research and all downstream specialists.

### Leading Indicators

**Format compliance:**
- Every finding in formatter output uses categorical confidence (high/medium/low — never numeric)
- Every finding uses full tier labels (primary/secondary/tertiary — never abbreviated)
- Every source field is a full `https://` URL or explicitly marked `unknown`

**Normalization reliability:**
- Formatter produces canonical RESEARCH OUTPUT block on every run regardless of researcher output format
- Zero claims lost during format conversion (input claim count = output claim count)

### Lagging Indicators

**Pipeline trust:**
- Downstream specialists (Writer, Data Analyzer) never receive non-canonical input
- Zero parsing failures in Writer or Data Analyzer traced to format issues

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

## Data Analyzer Metrics

**Phase Goal:** Validate that the Data Analyzer fills the authorization gap between Researcher and Writer — drawing labeled, traceable inferences that neither adjacent specialist is authorized to produce.

### Specialist-Specific Success Criteria

**A1 — Inference traceability:** Every inference in AnalysisOutput traces to specific finding IDs. No ungrounded conclusions.

**A2 — Finding coverage:** Every finding is accounted for — either in `traces_to` of an inference, or in UNUSED FINDINGS with a typed reason (`contradicted` | `insufficient_evidence` | `out_of_scope`). Nothing is silently omitted.

**A3 — Threshold enforcement:** `QUALITY THRESHOLD RESULT: NOT MET` fires when evidence doesn't support inferences at the requested confidence level. The Analyzer never silently returns lower-quality output.

**A4 — Inferences are specific and falsifiable:** Each inference must make a claim a skeptic could reasonably disagree with. An inference true by definition ("LLMs have security risks") fails this criterion regardless of traceability.

### Chain Success Criteria (tested in full chain, not Analyzer alone)

**C1 — AnalysisOutput passes to Writer without translation:** The Writer receives AnalysisOutput as `analysis-output` input type and produces a compliant document without manual reformatting between steps.

**C2 — Writer labels inferences as conclusions, not facts:** Every inference-sourced claim in the Writer's document uses hedged framing ("the evidence suggests...", "this points to...") and carries `type: inference` in the CITATIONS block.

### Qualitative Signals

**Signals we want to hear:**
- "The inference gave me something I wouldn't have drawn from reading the findings myself"
- "I could see exactly which findings supported which conclusion"
- "It told me what it couldn't conclude — and why"

**Red flags:**
- "The inferences were things I already knew from reading the findings"
- "I couldn't tell which findings mattered to which conclusion"
- "It just said 'the evidence is mixed' without naming the tension"

---

## Storyteller Metrics

**Phase Goal:** Validate that the Storyteller performs cognitive mode translation — producing narrative that moves audiences to action in ways the Writer's structured documents cannot.

### Specialist-Specific Success Criteria

**ST1 — Narrative arc completeness:** Every story has dramatic question, protagonist, stakes, causal chain, peak moment, resolution; structural checklist (6 items) passes on every output.

**ST2 — Selection record complete:** Every included finding traces to source; every omitted finding appears in NARRATIVE SELECTION with rationale; INCLUDED + OMITTED = total findings from Stage 1.

**ST3 — Source fidelity:** Zero claims in story body that don't trace to source material in NARRATIVE SELECTION; no fabricated examples or invented analogies.

**ST4 — Framework-tone independence:** Framework and tone in output header set on separate axes; selected framework appropriate to content+audience+goal (not tone alone).

### Chain Success Criteria

**SC1 — Analyzer → Storyteller passes without translation:** StoryOutput produced directly from AnalysisOutput without manual reformatting; narrative-chain recipe runs end-to-end.

**SC2 — Narrative beats document for audience engagement:** Chain ending in Storyteller produces output that moves target audience to action more effectively than same chain ending in Writer (qualitative signal, human review).

### Qualitative Signals

**Signals we want to hear:**
- "I could actually send this to the board without editing"
- "It picked the three things that mattered and built a story around them"
- "The selection record showed me exactly what it left out and why"
- "The story felt like a story, not a report with a dramatic opening"

**Red flags:**
- "It just rewrote the analysis with better words"
- "I couldn't tell what it left out"
- "The story felt like a document in disguise"
- "It added things that weren't in the source material"

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
- Context file (`context/coordinator-routing.md`) accurately guides delegation decisions

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

### V1 Success = Research Pipeline Is Trustworthy

**Must achieve:**
- Every finding is sourced, tiered, and confidence-rated (validated via formatter output)
- Evidence gaps are always disclosed, never omitted
- ResearchOutput schema is stable (no breaking changes needed after v1.0)
- Formatter normalizes researcher output to canonical format on every run

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

## Scoring Rubric

The scorecard (`docs/SCORECARD.md`) tracks current scores against these definitions. **This file owns the rubric.** The scorecard references it — the scorecard does not redefine what scores mean. Changing a rubric definition here is a deliberate, auditable act. Changing it in the scorecard is definition drift.

Scores are 0–10 per dimension. Scores move only on **validated test evidence**, not spec changes alone.

### Research Trustworthiness

*Criteria: V1 Leading + Lagging Indicators above; Formatter Metrics; Data Analyzer A1–A4*

| Score | Meaning |
|---|---|
| 0–2 | Core mechanisms broken — confidence tiers absent, no URLs, quality gate decorative |
| 3–5 | Architecture correct, some validation. Most claims rated, URLs present, gaps disclosed. Not validated across diverse topics. |
| 6–8 | Validated across 5+ diverse topics. Quality gate demonstrably returns NOT MET. Caller can audit any claim end-to-end. Inference traces preserved through full chain. |
| 9–10 | Full V1 success criteria met and validated. "I trusted it because I could see every source." Zero `unrated` confidence, 100% verifiable URLs, evidence gaps always disclosed — across all test evidence. |

### Chain Reliability

*Criteria: V2 Composability indicators; chain success criteria (C1, SC1); recipe completion*

| Score | Meaning |
|---|---|
| 0–2 | Chain breaks frequently — formatters skipped, timeouts, parsing failures |
| 3–5 | Individual links work. Known fragility points exist. Some chains validated, not all. |
| 6–8 | All individual chain variants validated. Formatter fires on every run as designed pipeline stage. No timeouts in standard runs. Recipe completion reliable. |
| 9–10 | Full chain (R→RF→DA→DAF→W) validated end-to-end. Zero preprocessing between specialists. Every chain variant proven in test evidence. "It just works." |

### Format Fidelity

*Criteria: V2 Format Fidelity indicators; Universal Baseline U1 (output schema is a contract)*

| Score | Meaning |
|---|---|
| 0–2 | Format is a label only — brief and report indistinguishable in practice |
| 3–5 | Formats partially distinct. Structural blocks present inconsistently. Word budgets not enforced. |
| 6–8 | All specialist-formatter pairs produce canonical output. Structural blocks reliable. Word budgets enforced. Audience calibration produces distinct output for different registers. |
| 9–10 | 100% format fidelity validated across all formats and input types. CLAIMS TO VERIFY surfaced consistently. "The brief was exactly right — not a report in brief clothing." |

### Specialist Coverage

*Criteria: Roadmap phases in VISION.md; epic status in BACKLOG.md*

| Score | Meaning |
|---|---|
| 0–2 | Fewer than 3 specialist domains shipped |
| 3–5 | Core specialists built (Researcher, Writer, DA, CA). Phase 1 mostly done. |
| 6 | Phase 2 in progress — most Phase 2 specialists shipped (e.g., Storyteller, Prioritizer), at least one pending (e.g., Planner). Formatter pattern established across all shipped specialists. |
| 7–8 | All Phase 2 specialists shipped. Pattern proven repeatable — new specialist from guide alone. |
| 9–10 | All 11 epics complete. Full roadmap Phases 1–3 delivered. Ecosystem composition validated. |

---

## The Standard

**If a metric doesn't help us answer "does the specialist produce more trustworthy output than inline work?", we don't track it.**

Specialists exist to raise the quality floor. Every measurement should connect back to that.

---

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.4 | 2026-03-10 | Chris Park | Added Scoring Rubric section — single source of truth for dimension definitions (0–10 scales for Research Trustworthiness, Chain Reliability, Format Fidelity, Specialist Coverage). Scorecard references this file; cannot redefine. Updated Chain Reliability rubric to reflect formatters as architectural design (not rescue). |
| v1.3 | 2026-03-04 | Chris Park | Added Storyteller Metrics section (ST1–ST4, SC1–SC2, qualitative signals) |
| v1.2 | 2026-03-03 | Chris Park | Updated Primary Success Indicator to chain-centric; added Universal Baseline Criteria (U1–U4); added Data Analyzer Metrics section (A1–A4, C1–C2, qualitative signals) |
| v1.1 | 2026-03-02 | Chris Park | Added Owner, Table of Contents, Change History; aligned with SUCCESS_METRICS_TEMPLATE |
| v1.0 | 2026-02-28 | Chris Park | Initial success metrics document |
