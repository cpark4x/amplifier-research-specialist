---
specialist: data-analyzer-formatter
chain: "data-analyzer-formatter standalone"
topic: da-formatter-spot-test
date: 2026-03-10
quality_signal: pass
closes: "#34 (da-formatter specialist — architectural fix)"
action_items_promoted: true
---

## Purpose

Spot test for the newly built `data-analyzer-formatter` specialist.
Tests the primary failure mode: DA produced unstructured narrative prose (emoji-annotated
sections, markdown table, no ANALYSIS OUTPUT block) instead of a canonical block.

Validates that the formatter:
1. Detects `da-format=narrative` correctly
2. Strips the stage narration prefix (`**Stage 1: Parse**`)
3. Re-extracts F1-Fn from original research (not from DA narrative)
4. Extracts inferences from DA prose with `traces_to: [narrative-mapped: uncertain]`
5. Accounts for all findings (used or UNUSED with `narrative-untraced` reason)
6. Produces a complete ANALYSIS OUTPUT block with no code fences

---

## Test Inputs

**DA output (narrative failure mode):**
- Stage narration prefix: `**Stage 1: Parse**` visible before any content
- DA body: 3 emoji-annotated prose sections (`## Competitive Position`, `## Key Strengths`,
  `## Strategic Risk`) plus a markdown summary table
- No `ANALYSIS OUTPUT` block, no `FINDINGS` section, no `traces_to` fields anywhere

**Original research:**
- Canonical `RESEARCH OUTPUT` block (Format A)
- 5 findings: funding round, benchmark performance, hybrid deployment, EU HQ/GDPR, commoditization risk
- 1 evidence gap: revenue/commercial traction data not publicly disclosed

---

## Results

**Format detection: PASS ✅**
- `da-format=narrative` correctly detected
- Stage narration prefix stripped — `ANALYSIS OUTPUT` header appears as first output line
- `Parsed: 5 findings | da-format=narrative | 5 inferences detected`

**FINDINGS extraction: PASS ✅**
- F1–F5 extracted from original RESEARCH OUTPUT, not from DA narrative
- All claim texts, sources, tiers, and confidence levels match original research exactly

**Inference extraction: PASS ✅**
- 5 inferences extracted from DA prose sections
- Types correctly assigned: `evaluative` for positioning/competitive judgments, `causal` for driver-based conclusions
- All `traces_to: [narrative-mapped: uncertain]` — no invented finding IDs

**Finding coverage: PASS ✅**
- F3, F4, F5 semantically referenced by inferences (narrative-mapped)
- F1 (funding round) and F2 (benchmark specifics) correctly routed to UNUSED FINDINGS
  with `reason: narrative-untraced` — DA narrative didn't reference these specific facts

**Evidence gaps: PASS ✅**
- Gap preserved from original research: revenue/commercial traction data

**Output contract: PASS ✅**
- No code fences
- No explanatory text outside block
- `QUALITY THRESHOLD RESULT: MET` present
- All required sections present: ANALYSIS BRIEF, FINDINGS, INFERENCES, UNUSED FINDINGS,
  EVIDENCE GAPS, QUALITY THRESHOLD RESULT

---

## Overall: PASS ✅

The formatter correctly handles the primary failure mode — narrative DA output normalized
to canonical ANALYSIS OUTPUT block with all contract requirements met. Option A
(`traces_to: [narrative-mapped: uncertain]`) correctly preserves honest uncertainty
rather than inventing finding IDs.

---

## Action Items

None. #34 closed. Scorecard update pending in Task 6.
