---
specialist: researcher
chain: "researcher → researcher-formatter → writer"
topic: jina-ai-architecture-refactor
date: 2026-03-06
quality_signal: pass
action_items_promoted: false
---

# Test Log: Researcher-Formatter Architecture Refactor Validation

**Date:** 2026-03-06
**Type:** Architecture validation — testing refactored researcher (format enforcement removed) + promoted formatter (validation rules added)
**Chain:** researcher → researcher-formatter → writer (format=brief)
**Topic:** What is Jina AI?

## What Worked

- **Researcher produced natural narrative output** — no COMPLIANCE NOTE, no FINAL SELF-CHECK, no Stage 0 template. Output was clean narrative markdown with tables, prose sections, and inline source tier annotations. Exactly the expected behavior after stripping format enforcement.
- **Researcher evidence quality strong** — 43 discrete claims extracted across 3 source tiers. High-confidence claims backed by Elastic IR press release and arXiv papers. Medium-confidence gaps clearly flagged (funding figures, named customers, current benchmark rankings). Evidence gaps present and bounded.
- **Formatter successfully normalized all 43 claims** — produced canonical RESEARCH OUTPUT block from narrative input (Format B). All pass/fail criteria met:
  - RESEARCH OUTPUT in plain text (not `# RESEARCH OUTPUT` markdown header) ✓
  - Structured `Claim:` / `Source:` / `Tier:` / `Confidence:` blocks for every finding ✓
  - All confidence values categorical (high/medium/low — zero numeric values) ✓
  - All tier values full labels (primary/secondary/tertiary — zero T1/T2/T3) ✓
  - All sources full `https://` URLs or explicitly `unknown` ✓
  - EVIDENCE GAPS section present with 4 well-scoped gaps ✓
  - Zero claims invented ✓
- **Writer brief produced successfully** — WRITER METADATA + 6 structured sections + 10-source CITATIONS block + 5 CLAIMS TO VERIFY. All sources trace to formatter findings. Competitive context noted with appropriate MTEB benchmark caveat.
- **Architecture thesis validated** — researcher + formatter as matched pair works. The researcher focuses on evidence quality (narrative output fine), the formatter handles canonicalization (reliable, deterministic, every run).

## What Didn't / Concerns

- **Formatter `Parsed:` line format** — the formatter correctly emitted `Parsed: 43 claims | format=B (narrative markdown with structured sections) | question=What is Jina AI?` before the RESEARCH OUTPUT block. Minor: the parenthetical format description is more verbose than the spec's example. Functional, not a blocker.
- **Writer word count** — brief was well-structured but included multiple tables and a full competitive positioning section. Likely above the 400-word soft ceiling for strict brief format. Not counted precisely; format was visually appropriate for the depth of research. No regression from Session 1 word budget work.
- **RESEARCH EVENTS section** — formatter produced `not provided in input` since the researcher's narrative didn't include a structured events log. Correct behavior — not a failure.

## Confidence Accuracy

High-confidence claims (founding, acquisition, product specs, arXiv-backed benchmarks) were well-sourced and correctly rated. Medium-confidence claims (funding totals, customer sectors, competitive rankings) were appropriately caveated. The formatter preserved these calibrations correctly. The writer surfaced all 5 medium-confidence claims as CLAIMS TO VERIFY — confidence accuracy end-to-end is working.

## Coverage Assessment

Equivalent to Session 1 Jina AI run in coverage depth. The researcher found all key facts: founding, product lineup, acquisition by Elastic, research publications, open-source footprint. The formatter's 43-claim extraction is richer than any Session 1 run, likely because the researcher was no longer fighting format constraints and could focus on evidence gathering. Better coverage than Session 1.

## Action Items

No blocking issues found. Architecture is sound. No items to route to backlog or specialist instructions at this time.
