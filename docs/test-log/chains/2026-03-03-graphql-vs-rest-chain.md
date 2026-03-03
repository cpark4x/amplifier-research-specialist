---
specialist: researcher → data-analyzer → writer
chain: "researcher → data-analyzer → writer"
topic: graphql-vs-rest
date: 2026-03-03
quality_signal: mixed
action_items_promoted: true
---

# Researcher → Data Analyzer → Writer — GraphQL vs REST

**Topic:** GraphQL vs REST for building modern APIs in 2025
**Audience:** VP of Engineering
**Format:** Brief

Second full chain run. No manual intervention at any step — pipeline completed
automatically. However, format compliance broke down at all three stages, revealing
that the compliance fixes are not yet reliably consistent across topics.

---

## What Worked

**Chain completed without manual intervention** ✅
Each specialist's output was passed verbatim to the next stage. No reformatting,
no manual editing at any step.

**Content quality was strong across all three specialists.**
- Researcher: rich, well-sourced research across 7 dimensions with real statistics
- Data Analyzer: comprehensive analysis with decision matrices, performance charts,
  and data reliability assessment — genuinely useful output
- Writer: high-quality executive brief with scenario guidance, risk register, and
  honest evidence quality note

**Data Analyzer produced strong analytical content.**
Even without the canonical ANALYSIS OUTPUT block, the data analyzer extracted key
signals, identified vendor bias in Apollo-sourced stats, flagged the Shopify
break-even as an n=1 data point, and correctly noted the absence of controlled
benchmarks. The analytical reasoning was sound.

**Writer produced useful, actionable content.**
The brief included a bottom line up front, structural tradeoffs table, scenario
guidance, and risk register — all appropriate for a VP of Engineering audience.

---

## What Didn't / Concerns

### Researcher: format compliance inconsistent — non-canonical opening ❌
Response began with `---` (markdown horizontal rule) then `# RESEARCH OUTPUT`
(markdown header) — not the bare `RESEARCH OUTPUT` required on the literal first
line. The previous chain test (PostgreSQL vs MongoDB) produced correct canonical
format; this run did not. The fix is not reliably applied across topics. This
suggests the Stage 0 fix and OUTPUT CONTRACT note are working sometimes but not
consistently — the Researcher may be sensitive to topic complexity or research
volume.

### Data Analyzer: did not produce canonical ANALYSIS OUTPUT block ❌
When given the Researcher's non-canonical narrative input, the Data Analyzer
produced a rich narrative analysis document instead of the structured
`ANALYSIS OUTPUT / Specialist: data-analyzer / Version: 1.0` block. This confirms
that the Format A/B detection works when the input has clear structural signals
(explicit Claim: / Source: / Tier: / Confidence: labels), but does not trigger
when the input is more narrative with embedded statistics. The partially-canonical
Researcher output in this run fell into a third format — neither clean Format A
nor the fully-narrative Format B we tested — and the Data Analyzer defaulted to
narrative prose.

### Writer: parse-line anchor did not trigger ❌
Response began with `# API Architecture Decision Brief` — a markdown header —
instead of the required `Parsed: [n] claims | ...` parse line. No WRITER METADATA,
CITATIONS, or CLAIMS TO VERIFY sections were produced. The previous test
(PostgreSQL vs MongoDB AnalysisOutput) worked correctly with the parse-line anchor.
Inconsistency suggests the anchor triggers reliably when given structured
ANALYSIS OUTPUT block input, but fails when the input is narrative — the agent
treats narrative input as a signal to produce narrative output.

---

## Pattern Identified

**All three format compliance fixes share the same failure mode:** they work
reliably when input is clean and structured, but fail when input is narrative
or semi-structured. Format compliance cascades downstream:

```
Researcher produces non-canonical (---\n# RESEARCH OUTPUT)
  → Data Analyzer sees narrative input → falls back to narrative output
    → Writer sees narrative input → falls back to narrative output
```

The root issue is Researcher consistency, not individual specialist specs.
When the Researcher produces canonical Format A, the entire chain holds.
When it doesn't, everything downstream degrades.

---

## Confidence Accuracy

The Data Analyzer correctly flagged vendor bias in Apollo-sourced statistics,
identified the Shopify break-even as an n=1 data point, and dropped the
uncorroborated 56% documentation burden reduction claim from its primary
narrative. These are accurate calibration calls.

The Writer's evidence quality note was well-placed: it distinguished
high-confidence findings (GitHub bandwidth reduction, security vectors, Shopify
break-even directional) from caution-warranted data (Apollo DX stats, 340%
configuration overhead).

---

## Coverage Assessment

All high-confidence findings (GitHub 60% bandwidth reduction, GraphQL's three
security attack vectors, Shopify migration economics) appeared in the final brief.
Evidence gaps (no controlled benchmarks, no multi-company TCO data) were surfaced
prominently. No high-confidence claims appeared without sourcing context.

---

## Action Items

- [ ] **Researcher consistency** — Stage 0 fix is not reliably triggering across
  topics. The `---\n# RESEARCH OUTPUT` opening is the failure mode: the Researcher
  outputs a markdown separator before the RESEARCH OUTPUT header. Investigate whether
  a more targeted Stage 0 instruction can prevent the `---` prefix specifically.
  *(route → docs/02-requirements/epics/01-research-specialist.md)*

- [ ] **Data Analyzer Format B edge case** — The Format B detection handles fully
  narrative markdown (explicit Claim: / Source: / Tier: labels) but not partially-
  canonical input (section-structured narrative without explicit per-finding labels).
  Consider adding a Format C handling rule: "If input contains RESEARCH OUTPUT
  header but findings are in narrative tables rather than key-value blocks, apply
  Format B extraction to the structured sections."
  *(route → specialists/data-analyzer/index.md)*

- [ ] **Writer parse-line consistency** — Parse-line anchor triggers reliably for
  ANALYSIS OUTPUT block input but not for narrative input. The Writer needs to
  produce the parse line regardless of input format. Consider strengthening the
  Stage 1 parse-line instruction to fire independently of whether the input looks
  structured or not. *(route → docs/02-requirements/epics/02-writer-specialist.md)*
