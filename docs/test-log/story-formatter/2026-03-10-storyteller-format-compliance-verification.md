---
specialist: story-formatter
chain: "storyteller (document failure mode) → story-formatter"
topic: storyteller-format-compliance-verification
date: 2026-03-10
quality_signal: pass
closes: "#30 (Storyteller OUTPUT CONTRACT compliance), #18 (inference auditability), #19 (quality_threshold parameter)"
action_items_promoted: true
---

## Purpose

Verify that story-formatter handles the Storyteller's documented failure mode: output is a
fully-formed markdown document (## headers, bold section titles, footnote citation) with no
`STORY OUTPUT` header, no `NARRATIVE SELECTION` block, and no `QUALITY THRESHOLD RESULT` line.
This is the failure mode documented in backlog #30 from test log 2026-03-06-storyteller-fixes-validation.

Also validates #18 (inference auditability in NARRATIVE SELECTION) and #19 (quality_threshold parameter).

## Test Setup

- **Input to Storyteller:** AnalysisOutput from data-analyzer on Acme Corp enterprise retention
  (6 findings F1–F6, 3 inferences I1–I3, quality score: medium)
- **Storyteller output:** Markdown document with `## Situation`, `## What the Data Shows`,
  `## The Root Cause` section headers — no STORY OUTPUT header, no NARRATIVE SELECTION block.
  Classic #30 failure mode.
- **Input to story-formatter:** Storyteller's prose document + original AnalysisOutput

## What Worked

- **STORY OUTPUT header on line 1** — Response began with exact text `STORY OUTPUT` (plain text,
  no `#` prefix). Clean pass on the primary format requirement.
- **All five structural elements present:**
  1. `STORY OUTPUT` header ✅
  2. Metadata lines (Input type: analysis-output, Audience: board, Tone: trustworthy,
     Framework: scqa, Quality threshold: standard) ✅
  3. `NARRATIVE SELECTION` with dramatic question, protagonist, framework rationale ✅
  4. Story prose (cleaned — markdown headers stripped, bold inline removed, content preserved) ✅
  5. `QUALITY THRESHOLD RESULT: MET` ✅
- **Format detection correct** — `storyteller-format=document` identified correctly from
  `## Section` headers and `**Bold Title**` inline — not treated as partial block or prose.
- **All 9 items classified** — 6 findings (F1–F6) + 3 inferences (I1–I3) all present in
  INCLUDED FINDINGS. Zero silently dropped.
- **#18 VERIFIED — Inference labels in NARRATIVE SELECTION:**
  Story-formatter correctly surfaced all three inferences with `(inference)` label in INCLUDED FINDINGS:
  ```
  - I1: v3.0 UI redesign is primary driver, not competitive pricing (inference) | role: resolution
  - I2: Enterprise workflows have higher complexity dependency on old UI (inference) | role: evidence
  - I3: Without UX remediation, competitive pricing will amplify churn (inference) | role: resolution
  ```
  Inferences are NOT silently consumed as background context — they are explicitly listed as
  INCLUDED or OMITTED. This is the defensibility requirement from the vision: every inference
  traces to a finding in the audit trail.
- **Dramatic question inferred correctly** — "Is the v3.0 UI redesign the true driver of
  enterprise retention decline, and what must management do to reverse it?" — correctly captures
  the central tension of the board narrative.
- **SCQA framework identified correctly** — Situation (retention decline) → Complication
  (three UX signals converge) → Question (pricing or UX?) → Answer (UX, with SMB/enterprise
  divergence as the pivot).
- **Prose cleaning correct** — All `##`/`###` section headers stripped, all `**bold**` inline
  formatting removed, sentence content preserved exactly.

## What Didn't / Concerns

- **Normalization notes appended outside block** — Story-formatter added a markdown table
  ("Normalization notes (outside the block — for your reference)") after `QUALITY THRESHOLD RESULT: MET`.
  This violates the spec's "What You Do Not Do" rule: "Add explanatory text outside the block."
  The canonical STORY OUTPUT block itself is complete and correct, so this doesn't break downstream
  parsing (a parser stops at QUALITY THRESHOLD RESULT: MET). But it's a spec violation.
  Recommended fix: add "Do not append normalization notes or metadata tables after QUALITY THRESHOLD
  RESULT" to the What You Do Not Do section. Low priority — non-breaking.

## #18 Verification: PASS

**Item:** Storyteller: surface inferences in NARRATIVE SELECTION for auditability.
**Verdict:** VERIFIED. Story-formatter surfaces all inferences from AnalysisOutput input
with `(inference)` label in INCLUDED FINDINGS. Inferences are not silently consumed —
they appear explicitly with their narrative role documented. The spec change from v3.0
(2026-03-06) is confirmed working end-to-end via the formatter chain.

## #19 Verification: SPEC-COMPLETE (partial)

**Item:** Storyteller: add `quality_threshold` as optional caller parameter.
**Verdict:** The Storyteller spec (Stage 1, line 196) already detects `quality_threshold: high`
from caller input with `standard` default. This run used default standard — `Quality threshold: standard`
appeared correctly in story-formatter output metadata. The `high` threshold path (0 revision cycles
for structural failures) was not explicitly tested in this run. Spec implementation is complete;
high-threshold behavior is a deferred validation.

## #30 Closure Verdict

**Backlog #30 is closed via formatter architectural fix.** The Storyteller itself will continue
to occasionally produce unstructured markdown documents rather than STORY OUTPUT blocks — this
is a known LLM generation reliability issue that instruction-based enforcement cannot fully resolve.
The story-formatter is the architectural catch: it handles any Storyteller output format (block,
document, prose) and produces a canonical STORY OUTPUT block. This is the same pattern used for
the Researcher (researcher-formatter) and Writer (writer-formatter).

The production mechanism is the `narrative-chain` recipe, which includes story-formatter as a
mandatory step. For ad-hoc coordinator use, Rule 7 in specialists-instructions.md enforces routing.

## Action Items

- [ ] Minor: add "Do not append normalization notes or metadata tables after QUALITY THRESHOLD RESULT"
  to story-formatter What You Do Not Do section. Non-breaking; low priority.
- [ ] Deferred: run a follow-up test with `quality_threshold: high` to confirm NOT MET fires on
  first structural failure with zero revision cycles. #19 full verification.
