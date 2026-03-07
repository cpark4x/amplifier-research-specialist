---
specialist: writer
chain: "researcher → researcher-formatter → writer"
topic: writer-quality-fixes-validation
date: 2026-03-06
quality_signal: mixed
action_items_promoted: true
---

# Test Log: Writer Quality Fixes Validation — #28, #7, #9

**Date:** 2026-03-06
**Type:** Validation — testing three Writer fixes shipped in commit d411933
**Chain:** researcher → researcher-formatter → writer (format=brief, audience=myself)
**Topic:** What is Mistral AI?

## What Worked

- **#7 (Audience calibration): PASS.** `audience: myself` produced genuinely different output — direct, note-like, table-first structure, inline caveats in italic (`*Note: unaudited*`, `*Company-stated; unverified*`). No presentation framing, no third-person stakeholder language. The register distinction is real and visible.
- **#9 (Specificity enforcement): PASS.** Every section is Mistral-specific. The closing gaps paragraph ("No audited financials, no official press release confirming $13.8B Series C valuation, no current benchmarks vs. OpenAI/Anthropic/Gemini") names specific evidence gaps unique to this company. The [SUBJECT] substitution test fails throughout the document — no generic AI-era conclusions.
- **Inline soft claim surfacing (emergent).** For `myself` audience, the writer surfaced soft claims inline within the document body rather than in a formal block. This is better UX for personal notes format — caveats appear next to the claims they qualify, not buried in a separate section at the end.

## What Didn't / Concerns

- **#28 (CLAIMS TO VERIFY): PARTIAL.** Formal structural blocks (Parsed:, CLAIMS TO VERIFY, WRITER METADATA, CITATIONS) were completely absent. The writer started with `# Mistral AI` (markdown header) — a direct OUTPUT CONTRACT violation. Root cause: the register table's "skip formality; personal notes" language was interpreted as permission to skip structural requirements, not just informal prose style.
- **Patch applied immediately:** Register table `myself`/`me` row updated to clarify "informal prose, personal notes register — **structural blocks still required**." This should prevent recurrence.
- **Pre-existing format compliance fragility.** The OUTPUT CONTRACT (`Parsed:` line mandatory) has never been reliably enforced. The new register table language likely exacerbated a pre-existing slip pattern. This is a known fragility; it pre-dates this session.

## Confidence Accuracy

Not assessed in this run — output lacked the CITATIONS and CLAIMS TO VERIFY blocks that carry confidence metadata. The inline italic notes (*Note: unaudited*) suggest the model did identify medium/low confidence claims correctly, just surfaced them in prose rather than structured blocks.

## Coverage Assessment

Coverage was appropriate for a brief format. The revenue and valuation gap (no audited financials, Series C valuation unconfirmed by primary source) was correctly identified and surfaced. Employee count and diversity stats were flagged as company-stated and unverified. All four evidence gaps from the formatter output were reflected in the document.

## Action Items

- [x] Register table `myself`/`me` row patched: added "structural blocks still required" caveat — applied in same session, committed with test log.
- [x] #28, #7, #9 moved to Recently Completed in backlog.
- [ ] Structural block reliability (OUTPUT CONTRACT compliance for `Parsed:` line) is a pre-existing fragility — consider adding an explicit "WRONG / RIGHT" example for `myself` audience to the OUTPUT CONTRACT block, showing that structural blocks are required even for informal registers. Route to near-term backlog as #29.
