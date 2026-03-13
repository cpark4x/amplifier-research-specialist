---
specialist: writer-formatter
chain: "writer (audience=myself failure mode) → writer-formatter"
topic: writer-informal-register-verification
date: 2026-03-10
quality_signal: pass
closes: "#29 (Writer OUTPUT CONTRACT compliance for informal registers)"
action_items_promoted: true
---

## Purpose

Verify that writer-formatter handles the Writer's documented informal-register failure mode:
output is clean informal prose (bottom-line-up-front brief, first-person register, casual
tone) with NO structural blocks — no `Parsed:` line, no `WRITER METADATA`, no `CITATIONS`,
no `CLAIMS TO VERIFY`. This is the failure mode documented in backlog #29 (update 2026-03-09).

## Test Setup

- **Input to Writer:** RESEARCH OUTPUT on Jina AI Reader and Embeddings APIs (4 findings,
  medium quality score)
- **Audience:** myself
- **Writer output:** Informal brief with `**Bottom line:**`, bold section headers,
  first-person "So what" synthesis — no structural blocks whatsoever.
- **Input to writer-formatter:** Writer's brief + original RESEARCH OUTPUT

## What Worked

- **Parsed: line on line 1** — `Parsed: 4 claims | input=researcher-output | format=brief | audience=myself`.
  Clean pass on Stage 0 requirement.
- **All five structural elements present:**
  1. `Parsed:` line (Stage 0) ✅
  2. S1–S4 claims extracted from source RESEARCH OUTPUT ✅
  3. Document prose (preserved exactly, no rewriting) ✅
  4. `CLAIMS TO VERIFY` block (S2 and S4 flagged for specific numbers: "8,192-token", "0.8 on MTEB") ✅
  5. `WRITER METADATA` with `Audience: myself`, `Voice: direct`, coverage info ✅
  6. `CITATIONS` block (all 4 S-numbers, used/not-used, confidence scores) ✅
- **Audience correctly identified** — `audience=myself` detected from first-person prose
  register ("If I'm building a RAG pipeline..."). Formatter did not remap to `technical decision-maker`.
- **Claims extracted correctly** — All 4 findings from the RESEARCH OUTPUT mapped to S1–S4.
  Confidence levels preserved exactly (high/medium per original).
- **CLAIMS TO VERIFY flagging accurate** — Two specific numeric claims correctly flagged:
  - S2: "8,192-token context window" — specific number ✅
  - S4: "Scores 0.8 on MTEB" — specific number ✅
- **Prose preserved exactly** — The informal register (bold bottom line, casual section headers,
  "So what:" framing) preserved verbatim. Formatter did not rewrite or formalize.
- **Coverage: full** — All 4 source claims used in the prose. Zero gaps.
- **All S-numbers in CITATIONS** — S1–S4 all accounted for as `used in: [section]` with
  appropriate confidence scores (high=0.9, medium=0.6).

## What Didn't / Concerns

- None. Clean pass on all structural requirements. The informal register failure mode is
  fully handled by the writer-formatter.

## #29 Closure Verdict

**Backlog #29 is closed via formatter architectural fix.** The Writer itself will continue
to produce unstructured informal prose for `audience=myself` requests — this is a known
LLM generation reliability issue that two separate instruction-based fixes (`0508f95` and
the earlier OUTPUT CONTRACT block) could not resolve. The writer-formatter is the
architectural catch: it handles any Writer output format (structured report, informal prose,
partially-formed blocks) and produces a canonical Writer output block with all required
structural elements.

The writer-formatter already passed an informal-register test (`ebda55e`, 2026-03-09).
This test run reconfirms that result against the specific failure mode documented in #29.

The production mechanism is the recipe chains (research-chain.yaml, narrative-chain.yaml),
which include writer-formatter as a mandatory step. For ad-hoc coordinator use, Rule 6 in
specialists-instructions.md enforces routing.

## Action Items

None. Architectural fix is in place and validated.
