---
specialist: all
chain: "researcher → formatter → data-analyzer → writer → derive-filename → save"
topic: research-chain-v130-save-fix
date: 2026-03-09
quality_signal: pass
action_items_promoted: true
---

# Research-Chain v1.3.0 Save Fix — Validation Run — 2026-03-09

**Context:** Confirmation run after shipping `fd6e521` (split save step) to verify the fix resolves the reliable 120s timeout on the save step. Test question: "What is Mistral AI and what models have they released?" with `quality_threshold: low` to minimize research time and focus the test on the save path.

**Fix being validated:** research-chain.yaml v1.2.0 → v1.3.0. Single `save` step (120s, filename derivation + file write combined) replaced with two steps: `derive-filename` (120s, slug only) + `save` (300s, mechanical write).

## Result

**All 6 steps completed. Pipeline terminated with `status: completed` for the first time.**

| Step | Status |
|------|--------|
| research | ✅ |
| format-research | ✅ |
| analyze | ✅ |
| write | ✅ |
| derive-filename | ✅ — slug: `mistral-ai-models-released` |
| save | ✅ — `docs/research-output/mistral-ai-models-released.md` (16,320 bytes) |

## What Worked

- **Split step resolved the timeout.** Separating filename derivation from the file write gave each step a single, bounded responsibility. Both completed within their ceilings.
- **derive-filename output was correct.** Slug `mistral-ai-models-released` is accurate, well-formed kebab-case, and appropriate length (3–4 words).
- **save step wrote cleanly.** 16,320 bytes, correct path, no errors. File contains full Parsed block, brief body, Citations, and Claims to Verify.
- **Pipeline context variable `filename_slug` threaded correctly** between the two new steps — `{{filename_slug}}` interpolation in the save prompt worked as expected.

## What Didn't / Concerns

None. This was a clean pass. No issues to document.

## Confidence Accuracy

Not evaluated — this run was a fix validation, not a quality assessment of the research output.

## Coverage Assessment

Not evaluated — same reason.

## Action Items

None. Fix confirmed working. Backlog item #11 closed.
