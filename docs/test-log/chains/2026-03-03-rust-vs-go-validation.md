---
specialist: researcher → data-analyzer → writer
chain: "researcher → data-analyzer → writer"
topic: rust-vs-go
date: 2026-03-03
quality_signal: mixed
action_items_promoted: true
---

# Validation Chain: Rust vs Go for Backend Services

**Purpose:** Validate three-specialist compliance hardening commit (a4f6b6c)
**Audience:** VP of Engineering
**Format:** Brief

---

## What Worked

**Data Analyzer: full compliance, excellent output** ✅
Given structured Format B input (findings with explicit Claim:/Source:/Tier:/Confidence:
labels), the Data Analyzer produced a perfect canonical ANALYSIS OUTPUT block:
- `ANALYSIS OUTPUT / Specialist: data-analyzer / Version: 1.0` ✅
- Parse summary shown: 17 findings, 8 inferences ✅
- All 8 inferences with explicit `type:` labels from the enum
  (pattern × 3, evaluative × 2, causal × 2, predictive × 1) ✅
- All 17 findings accounted for; UNUSED FINDINGS: none ✅
- EVIDENCE GAPS and QUALITY THRESHOLD RESULT: MET ✅
- Strong analytical quality: inference B correctly identified that aggregate
  performance claims without workload context are unreliable ✅

**Writer content quality: high** ✅
Despite missing structural blocks, the brief was genuinely publication-quality —
decision framework, risk flags, and evidence gap note were all accurate and useful.

---

## What Didn't / Concerns

### Researcher: canonical format still not reliable ❌
Response began with `# Rust vs Go for Backend Services in 2025: Real-World
Tradeoffs` — full narrative markdown with embedded tables and section headers.
The Stage 0 hardening (commit a4f6b6c) did not prevent this. The Researcher
produced rich research content with complete sourcing across 4 dimensions, but
not in the RESEARCH OUTPUT block format. **Manual reformatting of Researcher
output into structured Claim:/Source:/Tier:/Confidence: blocks was required
before the Data Analyzer could process it.**

This means the chain is NOT automated end-to-end: the Researcher → Data Analyzer
handoff still requires human intervention for this topic.

### Writer: parse-line still not firing ❌
Response began with `# Engineering Decision Brief` — markdown header, no
`Parsed:` line, no WRITER METADATA, no CITATIONS, no CLAIMS TO VERIFY.
The "unconditional" parse-line hardening (commit a4f6b6c) did not trigger.

**Possible contributing factor:** The Data Analyzer wrapped its ANALYSIS OUTPUT
inside a triple-backtick code fence (```). When passed to the Writer, the
ANALYSIS OUTPUT content was inside a code block rather than as bare text. This
may have caused the Writer to interpret the input as code/documentation rather
than as an analysis-output to transform, bypassing the pipeline signal.

### Both fixes from a4f6b6c failed to hold
Despite increasingly explicit spec instructions ("The first two characters of your
response are `RE`" / "The first two characters are `Pa`"), both Researcher and
Writer fell back to markdown output. The spec-instructions-only approach has
reached its limit: 6+ attempts across both specialists with diminishing returns.

---

## Pattern Confirmed

Across three full chain runs (ai-pair-programming, graphql-vs-rest, rust-vs-go):
- **Data Analyzer:** consistent format compliance when given structured input ✅
- **Researcher:** inconsistent — passes ~1 in 3 times, always with the same topic
  (PostgreSQL vs MongoDB) and fails on others
- **Writer:** inconsistent — fires correctly when given bare ANALYSIS OUTPUT text
  but not when given narrative or code-block-wrapped analysis input

The Researcher and Writer have a fundamental "write rich markdown" prior that spec
instructions alone cannot reliably override. The approach needs to change.

---

## Confidence Accuracy

Data Analyzer inference confidence calibration was excellent: correctly flagged
F1-F4 performance benchmarks as medium confidence (different workload types,
different optimization levels); correctly rated safety guarantees (F11, F13) as
high. All confidence labels matched the underlying evidence quality.

Writer evidence quality note ("treat as directional — no controlled benchmark
exists") was correct and well-placed.

---

## Coverage Assessment

All high-confidence findings appeared in the Writer brief. Evidence gaps (no
controlled head-to-head benchmark, no longitudinal productivity data) were
surfaced correctly in the "Risk Flags" and footnote sections.

---

## Action Items

- [ ] **Reconsider the compliance approach for Researcher and Writer.** Six-plus
  spec instruction attempts have not produced reliable compliance. Consider
  architectural alternatives: (a) explicit post-processing normalization step
  between Researcher and Data Analyzer, (b) making the Data Analyzer the "source
  of truth" format — it reliably produces canonical output regardless of input
  format, so accept the Researcher's narrative and rely on Data Analyzer to
  normalize, (c) accept that Writer structural blocks require structured input and
  document this as a known limitation.
  *(route → docs/BACKLOG.md as consistent quality gap)*

- [ ] **Data Analyzer code fence wrapping.** The Data Analyzer wrapped its
  ANALYSIS OUTPUT inside a triple-backtick code fence. This may have contributed
  to the Writer not recognizing it as analysis-output input. Investigate whether
  the Data Analyzer should produce its output as bare text (no code fence) and
  whether this affects the Writer's input detection.
  *(route → docs/02-requirements/epics/08-data-analyzer.md)*
