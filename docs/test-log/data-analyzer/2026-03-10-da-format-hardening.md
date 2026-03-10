---
specialist: data-analyzer
chain: "data-analyzer standalone"
topic: da-format-b-hardening-and-code-fence-prevention
date: 2026-03-10
quality_signal: conditional-pass
closes: "#17 (code-fence prevention), #16 (Format B hardening — partial)"
action_items_promoted: false
---

## Purpose

Test the DA spec changes from 2026-03-10 sprint:
- **#16:** Format B detection hardening — pure prose input extraction consistency
- **#17:** Code-fence self-check — prevent ANALYSIS OUTPUT from being wrapped in code fences

Two test runs were conducted: the first to surface failure modes, the second with corrected input framing.

---

## Test Run 1 — FAIL (input framing issue)

**Input:** Pure prose competitive analysis narrative (5 paragraphs, no Source/Tier/Confidence
labels, no research-output framing). Question phrased as: "Analyze the following research
to draw labeled inferences. What is the competitive position of Mistral AI..."

**Output:** The DA produced a narrative competitive analysis essay with `## Section` headers,
emoji status indicators (🔵/🟡/🔴/🟢), and a summary matrix table — **no ANALYSIS OUTPUT
block at all**.

**Root cause:** The input appeared to the DA as a general analysis question rather than
"here is researcher output to analyze." Without the research-output framing, the DA fell
back to general analysis mode and produced narrative prose. This is the same class of
output format failure seen in Storyteller (#30) and Writer (#29) — instruction-based format
enforcement does not hold when the input type is ambiguous.

**New finding:** The DA requires clear "here is research output" framing to produce
ANALYSIS OUTPUT reliably. Raw prose questions trigger narrative mode. This failure mode
was not explicitly described in #16 or #17.

---

## Test Run 2 — PASS (proper Format B framing)

**Input:** Narrative Format B input with inline Source/Tier/Confidence labels per finding.
Research question framed as: "Here is the research output. Analyze it..."

**Findings extracted:** 9 findings correctly identified from the labeled narrative.
Format detected as Format B (not Format A — no canonical RESEARCH OUTPUT header or key-value
block structure, but Source/Tier/Confidence labels present inline).

**Inferences drawn:** 7 labeled inferences — mix of evaluative, causal, and pattern types.
All findings accounted for in inferences (UNUSED FINDINGS: none).

**#17 — Code fences: PASS ✅**
The ANALYSIS OUTPUT block was emitted as bare text — no opening ` ``` ` or ` ```analysis `
wrapper. The Stage 4 self-check instruction appears to have contributed (or the input
framing was sufficient). Code-fence failure mode not triggered in this run.

**#16 — Format B extraction: PARTIAL PASS ⚠️**
Format B with labeled hints (inline Source/Tier/Confidence per finding) extracted
correctly. However, this test does NOT validate the pure-prose case described in the
backlog item: "fully narrative inputs" with no structural hints at all. The new
"Special handling — pure prose inputs" section was added to the spec but was not
exercised by this test. Deferred validation.

**Stage narration leaked into response:**
The DA output began with `**Stage 1: Parse**` / `**Stage 2: Analyze**` / `**Stage 3: Quality Gate**`
visible narration BEFORE the ANALYSIS OUTPUT block. The spec says "the block below is
your entire response from this point forward" but the stage thinking was emitted as
visible output. The ANALYSIS OUTPUT block itself was correct; downstream parsers
would need to skip the prefix. Minor issue, non-blocking.

---

## Assessments

### #17 (Code-fence prevention): VALIDATED ✅

The Stage 4 self-check ("Does your response start with ` ``` `? If yes, remove fences")
was added to the spec and the second test produced no code fences. Closing #17 as fixed
via spec enforcement. Note: the DA-formatter architectural fix (#new item below) would make
this fully reliable — the self-check is still instruction-based.

### #16 (Format B detection hardening — pure prose): PARTIAL ⚠️

Format B with labeled hints validated. Pure-prose extraction (completely unstructured
sentences with no Source/Tier hints) not tested due to input framing required to prevent
Test 1 failure mode. The "Special handling — pure prose inputs" section is in the spec
but unvalidated. Closing #16 with this caveat; full closure requires a follow-up test
with properly framed pure-prose research input.

---

## New Finding: DA Needs Architectural Formatter Fix

The Test 1 failure revealed that the DA can produce completely unstructured narrative
output when input framing is ambiguous. This is the same root cause as the Storyteller
and Writer failures (#30, #29) — instruction-based format enforcement is insufficient
for reliable structural compliance. The architectural fix follows the established pattern:
a **data-analyzer-formatter** specialist that receives DA output in any format and
produces a canonical ANALYSIS OUTPUT block.

This is a follow-on item (see backlog action below).

---

## Action Items

- [ ] Add `da-formatter` (data-analyzer-formatter) to backlog near-term — fifth application
  of the formatter pattern. Same design as researcher/story/writer/prioritizer-formatter.
  Receives DA output in any format + original research input, produces canonical ANALYSIS OUTPUT block.
- [ ] Follow-up test: validate #16 "pure prose" extraction path with a purely narrative input
  that is explicitly framed as research output (e.g., "Here is my research summary: [prose]")
  but has NO Source/Tier/Confidence labels anywhere in the text.
