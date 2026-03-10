---
specialist: writer
topic: writer-informal-register
date: 2026-03-09
quality_signal: fail
action_items_promoted: true
---

# Writer — Informal Register OUTPUT CONTRACT Compliance

Verifies that the Writer produces `Parsed:`, `WRITER METADATA`, `CITATIONS`, and
`CLAIMS TO VERIFY` when called with `audience: myself` (informal register), after
the fix landed in commit `0508f95`.

Input: Jina AI RESEARCH OUTPUT — 3 findings, 1 evidence gap, quality score high.
Format requested: brief. Audience: myself.

## What Worked

- Informal register was correctly applied — prose was conversational, first-person,
  relaxed. The audience calibration fix from the Mar 6 session held. ✅
- Content accuracy — facts from source material represented correctly with no
  hallucination ✅
- Evidence gap (revenue figures) was surfaced at the end of the document ✅

## What Didn't / Concerns

- **OUTPUT CONTRACT completely ignored.** Response started with:
  `So, Jina AI — here's what I've got on them.`
  — a direct spec violation. The very first characters must be `Parsed:`.
- No `Parsed:` line
- No S-numbered claims list
- No `CLAIMS TO VERIFY` block
- No `WRITER METADATA` block
- No `CITATIONS` section

This is backlog #29. Commit `0508f95` was supposed to fix this — the OUTPUT
CONTRACT block now appears at lines 36–40 of `specialists/writer/index.md` with
explicit language: *"The very first characters of your response are `Parsed:` — no
title, no markdown header, no blank line before it."* The instruction is present
in the spec. The model ignored it anyway.

The informal register context appears to override the structural instruction even
when the contract is explicit. The fix strengthened the wording but not the
enforcement mechanism.

## Confidence Accuracy

N/A — writer test, not a researcher test.

## Coverage Assessment

N/A — not applicable to writer structural compliance tests.

## Action Items

- [ ] Re-open #29: fix in commit `0508f95` did not hold for informal register —
  `Parsed:` line and all three structural blocks (WRITER METADATA, CITATIONS,
  CLAIMS TO VERIFY) still absent. The OUTPUT CONTRACT block exists and is explicit,
  but the model ignores it when register is informal. A stronger enforcement
  mechanism is required — likely a WRONG/RIGHT example pair directly in the
  OUTPUT CONTRACT block showing informal prose with structural blocks intact.
  Consider also adding a Stage 5 structural self-check that fires regardless of
  register: "Does my response start with `Parsed:`? If not, stop and rewrite."
