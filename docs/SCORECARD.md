# Canvas Specialists — Quality Scorecard

**Purpose:** Tracks validated quality scores across key dimensions. Scores are updated
when test evidence exists; not updated on spec changes alone.

---

## Current Scores (as of 2026-03-10)

| Dimension | Score | Previous | Change | Last Updated |
|-----------|-------|----------|--------|--------------|
| **Research Trustworthiness** | 3/10 | 3/10 | — | 2026-03-09 |
| **Chain Reliability** | 8/10 | 7/10 | +1 ↑ | 2026-03-10 |
| **Format Fidelity** | 9/10 | 8/10 | +1 ↑ | 2026-03-10 |
| **Specialist Coverage** | 6/10 | 6/10 | — | 2026-03-09 |
| **Overall** | 7/10 | 6/10 | +1 ↑ | 2026-03-10 |

---

## Dimension Definitions

**Research Trustworthiness** — Can the caller trace every claim back to a source? Are
confidence levels accurate? Do evidence gaps surface explicitly? Is the research chain
end-to-end reliable? Measures the Researcher, Formatter, and DA pipeline quality.

**Chain Reliability** — Do specialist handoffs complete cleanly without errors or format
translation? Do recipes run to completion? Do formatters normalize output reliably?
Measures the "does the chain work" axis.

**Format Fidelity** — Do specialists produce structurally complete output on every run?
Are output contracts honored? Are machine-parseable headers and blocks present?
Measures output format compliance across all specialists.

**Specialist Coverage** — How many specialist types are functional, tested, and
production-ready? Coverage includes the full chain (specialist + formatter pairs).

**Overall** — Weighted average across the four dimensions. Equal weights currently.

---

## Score History

| Date | Research Trust | Chain Reliability | Format Fidelity | Coverage | Overall | Session Notes |
|------|---------------|-------------------|-----------------|----------|---------|---------------|
| 2026-03-09 | 3/10 | 7/10 | 8/10 | 6/10 | 6/10 | Scorecard established. 13 commits shipped in parallel sprint. Prioritizer built. Routing validation #32 PASS. |
| 2026-03-10 | 3/10 | 8/10 | 9/10 | 6/10 | **7/10** | Format Fidelity: closed #33 (prioritizer-formatter), #29 (writer informal), #30 (Storyteller format), verified #18/#19. Chain Reliability: prioritizer chain complete, DA hardening. Research Trustworthiness: DA improvements but new #34 finding; no net change. |

---

## What Moves Each Dimension

### Research Trustworthiness (currently 3/10)

**What's keeping it at 3:**
- DA can produce unstructured prose output for ambiguous inputs (new #34 finding)
- DA-formatter (#34) not yet built — no architectural catch for DA format failures
- Source confidence threshold not implemented (backlog #3 area)

**What would move it:**
- Build da-formatter specialist (#34) — closes the DA output format gap architecturally
- Run full research chain (Researcher → Formatter → DA → Writer) end-to-end and confirm
  all inference traces are preserved through to the final document
- Validate that confidence ratings in final Writer output trace back to source confidence

### Chain Reliability (currently 8/10)

**What's keeping it from 10:**
- DA chain has a known input-framing sensitivity (Test 1 failure in 2026-03-10 session)
- story-formatter appends normalization notes outside the STORY OUTPUT block (minor)
- Stage narration leaks into DA response (stage thinking visible in output)

**What would move it:**
- Build da-formatter (#34)
- Investigate stage narration leak in DA response

### Format Fidelity (currently 9/10)

**What's keeping it from 10:**
- Story-formatter appends normalization notes outside the canonical block (violation of
  "no explanatory text outside the block" rule — non-breaking but technically a violation)
- DA stage narration appears before ANALYSIS OUTPUT (minor prefix leakage)
- writer-formatter not tested with analysis-output input type (#14 still open)

**What would move it:**
- Fix story-formatter to suppress normalization notes for non-debug use
- Fix DA to suppress stage narration from response output

### Specialist Coverage (currently 6/10)

**What's keeping it at 6:**
- Planner specialist (Epic 09) not built
- Ecosystem Comparison recipe (Big Ideas) not built
- Design, Demo Generator, Presentation Builder (Epics 05, 06, 07) not built

**What would move it:**
- Build Planner specialist (Epic 09) — +1 point
- Build Ecosystem Comparison recipe — +0.5 (recipe, not full specialist)

---

## Validated Evidence Summary (2026-03-10)

| Item | Evidence | Dimension |
|------|----------|-----------|
| Prioritizer-formatter (#33) | prose→PRIORITY OUTPUT: PASS *(2026-03-10-prioritizer-formatter-spot-test)* | Format Fidelity |
| Story-formatter handles Storyteller failure mode (#30) | document→STORY OUTPUT: PASS *(2026-03-10-storyteller-format-compliance-verification)* | Format Fidelity |
| Inferences in NARRATIVE SELECTION (#18) | I1–I3 with `(inference)` labels in INCLUDED FINDINGS: PASS | Format Fidelity |
| Writer-formatter handles informal register (#29) | audience=myself→canonical blocks: PASS *(2026-03-10-writer-informal-register-verification)* | Format Fidelity |
| DA Format B labeled extraction (#16 partial) | 9 findings from labeled narrative: PASS | Chain Reliability |
| DA code-fence prevention (#17) | ANALYSIS OUTPUT as bare text: PASS | Chain Reliability |
