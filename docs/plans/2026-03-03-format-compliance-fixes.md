# Format Compliance Fixes — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal:** Fix format compliance gaps in Researcher and Writer so the full Researcher → Data Analyzer → Writer chain runs automated without any manual reformatting between steps.

**Context:** First full chain test (2026-03-03) confirmed the Data Analyzer is spec-compliant.
Two specialists have format compliance gaps: the Researcher produces narrative markdown
instead of the canonical `RESEARCH OUTPUT` block (breaking automated pipeline parsing),
and the Writer omits `WRITER METADATA`, `CITATIONS`, and `CLAIMS TO VERIFY` when given
`analysis-output` input (breaking downstream callers that rely on these blocks). Both gaps
are instruction-only fixes — no new files, no schema changes.

**Files:**
- `specialists/researcher/index.md` — Stage 7 (Synthesizer) output format instruction
- `specialists/writer/index.md` — Stage 5 (Verify and Cite) pre-return compliance check
- `docs/test-log/researcher/` — Sprint 1 test log
- `docs/test-log/writer/` — Sprint 2 test log
- `docs/test-log/chains/` — Sprint 3 chain test log

---

## Sprint 1 — Fix Researcher format compliance

---

## Task 1: Read `specialists/researcher/index.md` and locate Stage 7

**Files:**
- Read: `specialists/researcher/index.md`

**Step 1: Read the full Researcher spec**
```bash
cat specialists/researcher/index.md
```

**Step 2: Locate Stage 7 (Synthesizer) and map its structure**

Find the section that begins:
```
### Stage 7: Synthesizer

Assemble the final structured output. This is NOT a narrative. It is structured evidence.
```

Identify:
- The opening instruction line before the format code block
- The last line inside the format block (`RESEARCH EVENTS:` section)
- The closing triple-backtick that ends the format block
- The `---` separator that follows Stage 7 before `## Source Tiers`

**Step 3: Confirm the gap**

The spec already says "This is NOT a narrative" but the instruction is not strong enough to
prevent narrative output — it describes the desired format without explicitly prohibiting
the wrong format or requiring a machine-readable opening line. The fix: a compliance note
after the format block that names the opening line requirement, the FINDINGS key-value
format requirement, and explicitly states that narrative prose output is a spec violation.

No file changes in this task. Proceed to Task 2.

---

## Task 2: Strengthen Stage 7 output format in `specialists/researcher/index.md`

**Files:**
- Modify: `specialists/researcher/index.md`

One targeted insertion. Read the file first (Task 1 covers this).

**Step 1: Find the exact insertion point**

Locate this exact text — it is the last line inside the Stage 7 format code block, followed
by the closing triple-backtick:

```
RESEARCH EVENTS:
[Condensed log of what was attempted — sources hit, paywalls encountered, corroboration found]
```

The closing ``` appears on the very next line. The `---` separator and `## Source Tiers`
section follow after that.

**Step 2: Insert the compliance note immediately after the closing triple-backtick**

Find this sequence (closing ``` of the format block followed by the section separator):
```
RESEARCH EVENTS:
[Condensed log of what was attempted — sources hit, paywalls encountered, corroboration found]
```

After the closing triple-backtick of the code block (and before the `---` separator),
insert the following block exactly:

```markdown
**COMPLIANCE NOTE — machine-parseable output required:**

The block format above is the only acceptable Stage 7 output format. This is a pipeline
contract, not a style preference — downstream specialists parse this structure automatically.

- **Your response MUST begin with `RESEARCH OUTPUT`** — no preamble, no markdown headers,
  no executive summary before it. The first four characters of your output are `RESE`.
- **FINDINGS must use the exact multi-line key-value format:** `Claim:` / `Source:` /
  `Tier:` / `Confidence:` — one finding per block, blank line between findings. Do not
  convert FINDINGS into a table, a prose paragraph, or a single-line format.
- **Narrative prose output is a spec violation.** Thematic section headers, embedded
  markdown tables, and flowing paragraph summaries are not acceptable — they break
  automated parsing by the Data Analyzer.
- **RESEARCH BRIEF bullets are single-line claims with an inline URL in parentheses.**
  One bullet per claim. Not multi-paragraph descriptions. Not grouped by theme.
- **The opening `RESEARCH OUTPUT` line is a machine signal.** Write nothing before it —
  not even a blank line.

If your draft response begins with anything other than `RESEARCH OUTPUT`, reformat it
before returning.
```

**Step 3: Verify the compliance note was added**
```bash
grep -n "COMPLIANCE NOTE\|machine-parseable\|reformat it" specialists/researcher/index.md
```
Expected: 3 matches

**Step 4: Verify Stage 7 structure is intact**
```bash
grep -n "Stage 7\|Synthesizer\|COMPLIANCE NOTE\|Source Tiers\|---" specialists/researcher/index.md | head -20
```
Expected: Stage 7 and Synthesizer appear together, COMPLIANCE NOTE appears after them,
`---` separator appears between COMPLIANCE NOTE and Source Tiers.

**Step 5: Verify the format block itself is unchanged**
```bash
grep -n "RESEARCH OUTPUT\|RESEARCH BRIEF\|SUB-QUESTIONS\|FINDINGS\|EVIDENCE GAPS\|QUALITY SCORE RATIONALE\|FOLLOW-UP QUESTIONS\|RESEARCH EVENTS" specialists/researcher/index.md
```
Expected: all eight section headers from the format block are present.

**Step 6: Commit**
```bash
git add specialists/researcher/index.md
git commit -m "fix: add compliance note to Researcher Stage 7 — enforce RESEARCH OUTPUT block format"
```

---

## Task 3: Test Researcher compliance on a new topic

Run after Task 2 is committed.

**Step 1: Invoke the Researcher with a new topic**

Delegate to the Researcher specialist:
```
delegate(
  agent="specialists:researcher",
  instruction="""
  Research question: What is the current state of WebAssembly adoption for production
  web applications — what are real-world use cases, performance benchmarks, and
  developer adoption signals as of 2025?
  """
)
```

**Step 2: Check the opening line — this is the primary pass/fail signal**

The very first line of the response MUST be exactly:
```
RESEARCH OUTPUT
```

If the response begins with any of the following — the fix did not work:
- A markdown header (`# Research...`, `## Overview...`)
- A prose paragraph ("WebAssembly has emerged as...")
- An executive summary section
- Any whitespace or blank line before `RESEARCH OUTPUT`

Do not proceed to Task 4 if this check fails. Return to Task 2 and strengthen the
compliance note. Add the text "The very first character of your response is R, not #."

**Step 3: Check FINDINGS format**

In the `FINDINGS:` section, every entry must use the multi-line key-value format:
```
- Claim: [specific, discrete, falsifiable statement]
  Source: [URL]
  Tier: [primary | secondary | tertiary]
  Confidence: [high | medium | low]
  Corroborated by: [n] independent sources
  Direct quote: [yes | no]
```

Fail conditions:
- Findings formatted as a markdown table
- Findings formatted as prose sentences with sources inline
- Findings on a single pipe-separated line

**Step 4: Check RESEARCH BRIEF format**

The `RESEARCH BRIEF:` section must be a flat bullet list:
```
- [claim text] ([source URL])
- [claim text] ([source URL])
```

Fail conditions:
- Multi-paragraph finding descriptions
- Sub-bullets or nested structure
- Thematic groupings with headers

**Step 5: Verify remaining required sections are present**
```bash
# Run this grep against the actual output (save it to a temp file first if needed)
# Sections that must appear:
# RESEARCH OUTPUT / RESEARCH BRIEF / SUB-QUESTIONS ADDRESSED / FINDINGS /
# EVIDENCE GAPS / QUALITY SCORE RATIONALE / QUALITY THRESHOLD RESULT / RESEARCH EVENTS
```

Check manually that all eight section names from the format block are present in the output.

**Step 6: Record pass/fail**

- **PASS** — all of: response begins with `RESEARCH OUTPUT`, FINDINGS in multi-line
  key-value format, RESEARCH BRIEF in single-line bullet format, all eight sections present
- **FAIL** — any deviation. Strengthen Task 2 and retest before proceeding.

Proceed to Task 4 only on PASS.

---

## Task 4: Record Researcher compliance test log

**Files:**
- Create: `docs/test-log/researcher/2026-03-03-format-compliance-fix.md`

**Step 1: Create the test log file with results from Task 3**

Fill in the observed results from the test run. Replace bracketed placeholders with
what actually happened:

```markdown
---
specialist: researcher
topic: format-compliance-fix
date: 2026-03-03
quality_signal: pass
action_items_promoted: false
---

# Researcher — Format Compliance Fix Validation

Verifies that the strengthened Stage 7 compliance note produces canonical `RESEARCH OUTPUT`
block format on a new topic (WebAssembly adoption for production web applications).

## What Worked

- [Record whether response began with `RESEARCH OUTPUT` on the first line]
- [Record whether FINDINGS used multi-line key-value format (Claim / Source / Tier / Confidence)]
- [Record whether RESEARCH BRIEF used single-line bullets with inline URLs]
- [Record whether all eight section headers from the format spec were present]

## What Didn't / Concerns

- [Record any remaining deviations from the canonical format, or "None — format fully compliant"]

## Confidence Accuracy

N/A — compliance test, not a quality run.

## Coverage Assessment

N/A — compliance test.

## Action Items

- [ ] [Any follow-up items, or "None — test passed cleanly. Researcher format gap resolved."]
```

**Step 2: Verify the file was created**
```bash
cat docs/test-log/researcher/2026-03-03-format-compliance-fix.md | head -8
```
Expected: YAML frontmatter showing `specialist: researcher` and `quality_signal: pass`

**Step 3: Commit**
```bash
git add docs/test-log/researcher/2026-03-03-format-compliance-fix.md
git commit -m "docs: log Researcher format compliance fix validation"
```

---

## Sprint 2 — Fix Writer format compliance for analysis-output

---

## Task 5: Read `specialists/writer/index.md` and locate Stage 5

**Files:**
- Read: `specialists/writer/index.md`

**Step 1: Read the full Writer spec**
```bash
cat specialists/writer/index.md
```

**Step 2: Locate Stage 5 (Verify and Cite) and map its steps**

Find the section `### Stage 5: Verify and Cite` and identify:
- Steps 1–8 and their content
- Step 6 — produces the CITATIONS section
- Step 7 — adds `Confidence distribution` to WRITER METADATA
- Step 8 — produces the CLAIMS TO VERIFY block for `analysis-output` input
- The line `   - If no claims match: produce \`CLAIMS TO VERIFY: none\`` — end of Step 8
- The line `If any check fails: revise before returning.` — closing instruction of Stage 5

**Step 3: Locate the Output Format section**

Find `## Output Format` and verify it defines four blocks:
- Block 1: WRITER METADATA
- Block 2: Document content
- Block 3: CITATIONS
- Block 4: CLAIMS TO VERIFY (analyst-output, raw-notes, analysis-output only)

**Step 4: Confirm the gap**

The spec defines all three required blocks in Steps 6, 7, and 8 and in the Output Format
section. But the Writer omits them in practice because there is no final compliance check
that explicitly verifies all required blocks are present before the response is returned.
The fix: add Step 9 — a structural checklist that must pass before returning.

No file changes in this task. Proceed to Task 6.

---

## Task 6: Add Stage 5 Step 9 compliance check to `specialists/writer/index.md`

**Files:**
- Modify: `specialists/writer/index.md`

One targeted edit. Read the file first (Task 5 covers this).

**Step 1: Find the exact edit location**

Find this exact text (the last line of Step 8 followed by the Stage 5 closing instruction):

```
   - If no claims match: produce `CLAIMS TO VERIFY: none`

If any check fails: revise before returning.
```

**Step 2: Insert Step 9 between Step 8 and the closing instruction**

Replace the text found in Step 1 with:

```
   - If no claims match: produce `CLAIMS TO VERIFY: none`

9. **Final structure compliance check.** Before returning, verify all required blocks
   are present in your response. Omitting a required block is a spec violation — downstream
   callers (specialists, evaluators, and human reviewers) depend on these blocks to
   distinguish facts from inferences and to know what claims need verification.

   Run this checklist against your draft output before returning:
   - [ ] `WRITER METADATA` block is present and appears **first** — must include an
     `Input type:` line and a `Confidence distribution:` line. If absent: produce it.
   - [ ] Document content (sections and prose) follows WRITER METADATA, separated by `---`.
   - [ ] `CITATIONS` block follows the document — every Sn from your Stage 1 numbered list
     is present, marked either `used in: [section]` or `not used`. If absent: produce it.
   - [ ] For `analysis-output` input: every inference-sourced claim in CITATIONS carries
     `type: inference`. If any inference entry is missing the `type: inference` label:
     add it before returning.
   - [ ] `CLAIMS TO VERIFY` block follows CITATIONS for `analyst-output`, `raw-notes`,
     or `analysis-output` input. If absent: produce it (even if the result is
     `CLAIMS TO VERIFY: none`).
   - [ ] For `researcher-output` input: `CLAIMS TO VERIFY` is omitted entirely.

   If any block is missing from your draft, produce it now. Do not return a response
   that omits any required block.

If any check fails: revise before returning.
```

**Step 3: Verify Step 9 was added**
```bash
grep -n "Final structure compliance\|required block\|Run this checklist" specialists/writer/index.md
```
Expected: 3 matches

**Step 4: Verify Stage 5 is intact and all steps are present**
```bash
grep -n "Stage 5\|Step 6\|Step 7\|Step 8\|Step 9\|CLAIMS TO VERIFY: none\|If any check fails" specialists/writer/index.md
```
Expected: all step references present, `CLAIMS TO VERIFY: none` appears once (inside
Step 9, now), `If any check fails` appears once at the end of Stage 5.

**Step 5: Verify the Output Format section is unchanged**
```bash
grep -n "Block 1\|Block 2\|Block 3\|Block 4\|WRITER METADATA\|CITATIONS\|CLAIMS TO VERIFY" specialists/writer/index.md
```
Expected: all four block references present, plus multiple hits for each section name.

**Step 6: Commit**
```bash
git add specialists/writer/index.md
git commit -m "fix: add Stage 5 Step 9 compliance check to Writer — enforce WRITER METADATA, CITATIONS, CLAIMS TO VERIFY"
```

---

## Task 7: Test Writer compliance with a known AnalysisOutput

Run after Task 6 is committed.

**Step 1: Construct the test AnalysisOutput**

Use the TypeScript AnalysisOutput derived from the canonical ResearchOutput in
`docs/test-log/data-analyzer/2026-03-03-format-compliance.md`. Construct it as follows:

```
ANALYSIS OUTPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Specialist: data-analyzer
Version: 1.0

ANALYSIS BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Question: Is TypeScript worth adopting for a mid-size engineering team?
Focus: full research
Findings received: 3
Inferences drawn: 2
Quality score: medium

FINDINGS
F1: claim: Teams using TypeScript report 40% fewer runtime type errors in production compared to plain JavaScript teams | source: https://2023.stateofjs.com/en-US/usage/ | tier: secondary | confidence: high
F2: claim: TypeScript compilation adds approximately 10-15% build time overhead compared to JavaScript-only builds | source: https://esbuild.github.io/faq/#typescript | tier: primary | confidence: medium
F3: claim: 78% of developers surveyed in the State of JS report that TypeScript improves long-term maintainability of codebases | source: https://2023.stateofjs.com/en-US/usage/ | tier: secondary | confidence: medium

INFERENCES
inference: TypeScript meaningfully reduces production defect rates for mid-size engineering teams | type: evaluative | confidence: high | traces_to: [F1, F3]
inference: Adoption carries a measurable but bounded build-time cost of 10-15%, not a prohibitive overhead | type: evaluative | confidence: medium | traces_to: [F2]

UNUSED FINDINGS: none

EVIDENCE GAPS
gap: No controlled study isolating TypeScript impact on onboarding time for new engineers | reason: Available data is survey-based; no published RCT found

QUALITY THRESHOLD RESULT: MET
```

**Step 2: Pass the AnalysisOutput to the Writer**

Delegate to the Writer specialist:
```
delegate(
  agent="specialists:writer",
  instruction="""
  Transform the following AnalysisOutput into a brief for a VP of Engineering
  evaluating TypeScript adoption.
  Format: brief. Audience: VP of Engineering. Voice: executive.

  [paste the full AnalysisOutput from Step 1]
  """
)
```

**Step 3: Verify WRITER METADATA block**

The response MUST begin with a block that starts `WRITER METADATA` and includes:
```
WRITER METADATA
Specialist: writer
Version: 1.0
Input type: analysis-output
Output format: brief
Audience: VP of Engineering
...
Confidence distribution: [n] high · [n] medium · [n] low · [n] unrated · [n] inference
```

Fail conditions:
- Response begins with prose or a markdown header before `WRITER METADATA`
- `Input type:` line is missing or shows a different type
- `Confidence distribution:` line is missing or has no `inference` bucket

**Step 4: Verify CITATIONS block**

After the document content, verify a `CITATIONS` section is present containing:
- All S-numbered claims from the Stage 1 parse, marked used or not used
- At least two entries with `type: inference` label (one per inference from the input):
  ```
  Sx: "[inference claim]" → used in: [section] | type: inference | confidence: high (0.9)
  Sy: "[inference claim]" → used in: [section] | type: inference | confidence: medium (0.6)
  ```

Fail conditions:
- No CITATIONS section
- Inference-sourced entries missing `type: inference`
- S-numbered claims present in the document but absent from CITATIONS

**Step 5: Verify CLAIMS TO VERIFY block**

After CITATIONS, a `CLAIMS TO VERIFY` block must be present. It must flag the
specific numerical values in the input. At minimum, look for:
- The "40% fewer runtime type errors" figure — type: percentage
- The "10-15% build time overhead" figure — type: percentage
- The "78% of developers" figure — type: percentage

These appear in both the findings (F1, F2, F3) and in the inferences, so they must be
flagged since the input type is `analysis-output`.

Fail condition: no CLAIMS TO VERIFY block, or block is present but all three percentage
figures are omitted.

**Step 6: Record pass/fail**

- **PASS** — all of: WRITER METADATA present and first, CITATIONS present with
  `type: inference` entries, CLAIMS TO VERIFY present with numeric claims flagged
- **FAIL** — any block missing. Return to Task 6 and strengthen Step 9. Retest.

Proceed to Task 8 only on PASS.

---

## Task 8: Record Writer compliance test log

**Files:**
- Create: `docs/test-log/writer/2026-03-03-format-compliance-fix.md`

**Step 1: Create the test log file with results from Task 7**

Fill in the observed results. Replace bracketed placeholders with what actually happened:

```markdown
---
specialist: writer
topic: format-compliance-fix
date: 2026-03-03
quality_signal: pass
action_items_promoted: false
---

# Writer — Format Compliance Fix Validation (analysis-output)

Verifies that the Writer produces `WRITER METADATA`, `CITATIONS` (with `type: inference`
entries), and `CLAIMS TO VERIFY` when given `analysis-output` input type.

Input: TypeScript AnalysisOutput — 3 findings (F1–F3), 2 inferences. Derived from the
canonical ResearchOutput in `docs/test-log/data-analyzer/2026-03-03-format-compliance.md`.

## What Worked

- [Record whether WRITER METADATA block appeared first with `Input type: analysis-output`]
- [Record whether `Confidence distribution:` included an `inference` bucket]
- [Record whether CITATIONS appeared with `type: inference` labels on inference entries]
- [Record whether CLAIMS TO VERIFY flagged the percentage/numeric claims]

## What Didn't / Concerns

- [Record any remaining gaps, or "None — all three required blocks present and correctly formed"]

## Confidence Accuracy

N/A — compliance test, not a quality run.

## Coverage Assessment

N/A — compliance test.

## Action Items

- [ ] [Any follow-up items, or "None — test passed cleanly. Writer format gap resolved."]
```

**Step 2: Verify the file was created**
```bash
cat docs/test-log/writer/2026-03-03-format-compliance-fix.md | head -8
```
Expected: YAML frontmatter showing `specialist: writer` and `quality_signal: pass`

**Step 3: Commit**
```bash
git add docs/test-log/writer/2026-03-03-format-compliance-fix.md
git commit -m "docs: log Writer format compliance fix validation"
```

---

## Sprint 3 — Full automated chain validation

Run after Sprint 1 and Sprint 2 are both complete and both test logs show `quality_signal: pass`.

---

## Task 9: Run full Researcher → Data Analyzer → Writer chain

**Step 1: Invoke the Researcher on a new topic**

Use a topic not tested in any prior run. Use:
```
delegate(
  agent="specialists:researcher",
  instruction="""
  Research question: What are the real-world tradeoffs between PostgreSQL and MongoDB
  for new SaaS applications in 2025 — when should a team choose one over the other?
  """
)
```

**Step 2: Check Researcher output before passing downstream**

Before passing to the Data Analyzer, verify all three format signals:

| Check | Expected |
|---|---|
| First line of response | `RESEARCH OUTPUT` (exactly — nothing before it) |
| FINDINGS format | Multi-line key-value: `Claim:` / `Source:` / `Tier:` / `Confidence:` |
| RESEARCH BRIEF format | Single-line bullets: `- [claim] ([URL])` |

**If any check fails: stop.** Do not manually reformat the Researcher output to continue.
Record the failure. The chain quality signal is `fail` if manual intervention was required
at this step. Return to Task 2 and fix before continuing.

**Step 3: Pass Researcher output directly to Data Analyzer — verbatim, no reformatting**

Copy the full Researcher response without modification and pass it to the Data Analyzer:
```
delegate(
  agent="specialists:data-analyzer",
  instruction="""
  Analyze the following research output. quality_threshold: medium

  [paste Researcher output verbatim — no editing, no reformatting]
  """
)
```

**Step 4: Verify Data Analyzer output**

| Check | Expected |
|---|---|
| First line | `ANALYSIS OUTPUT` |
| ANALYSIS BRIEF block | Present with: Question, Focus, Findings received, Inferences drawn, Quality score |
| FINDINGS | F1, F2, F3... numbered, pipe-separated format |
| INFERENCES | At least one inference with `type:` from enum and `traces_to: [F...]` |
| UNUSED FINDINGS | Section present (value: specific entries or `none`) |
| Final line | `QUALITY THRESHOLD RESULT: MET` or `NOT MET` |

If the Data Analyzer output looks wrong, record the issue — this is a pre-existing
compliance baseline, not a fix introduced in this plan.

**Step 5: Pass Data Analyzer output directly to Writer — verbatim, no reformatting**

Copy the full Data Analyzer response without modification and pass it to the Writer:
```
delegate(
  agent="specialists:writer",
  instruction="""
  Transform the following AnalysisOutput into a brief for a senior technology leader
  evaluating database technology choices for a new SaaS product.
  Format: brief. Audience: CTO. Voice: executive.

  [paste Data Analyzer output verbatim — no editing, no reformatting]
  """
)
```

**Step 6: Verify Writer output — all three structural blocks present**

| Check | Expected |
|---|---|
| Block 1: WRITER METADATA | First in response; includes `Input type: analysis-output`; includes `Confidence distribution:` with `inference` bucket |
| Block 2: Document content | Brief sections with prose, inference framing ("the evidence suggests...") |
| Block 3: CITATIONS | Present; inference entries carry `type: inference`; every Sn accounted for |
| Block 4: CLAIMS TO VERIFY | Present; numeric inference claims (percentages, counts, measurements) flagged |

**Step 7: Assess the chain quality signal**

Assign one of three values:

**`pass`** — all of the following are true:
- Researcher output began with `RESEARCH OUTPUT` — no manual reformatting needed at Step 2
- Data Analyzer consumed Researcher output directly — no intervention at Step 3
- Writer consumed Data Analyzer output directly — no intervention at Step 5
- All three required Writer blocks are present (WRITER METADATA, CITATIONS, CLAIMS TO VERIFY)

**`mixed`** — any of the following:
- Researcher output required manual reformatting before Data Analyzer could process it
- Writer omitted one of the three required blocks
- Any step required human intervention to proceed (even minor)

**`fail`** — chain could not complete, or output quality is too low to be usable

---

## Task 10: Record chain test log

**Files:**
- Create: `docs/test-log/chains/2026-03-03-postgres-vs-mongodb-chain-compliance.md`

(If a different topic was used in Task 9, adjust the filename slug accordingly.)

**Step 1: Create the chain test log file with results from Task 9**

Fill in the observed results. Replace bracketed placeholders with what actually happened:

```markdown
---
specialist: researcher → data-analyzer → writer
chain: "researcher → data-analyzer → writer"
topic: postgres-vs-mongodb
date: 2026-03-03
quality_signal: [pass | mixed | fail]
action_items_promoted: false
---

# Researcher → Data Analyzer → Writer — Format Compliance Chain Validation

**Topic:** What are the real-world tradeoffs between PostgreSQL and MongoDB for new SaaS
applications in 2025?
**Audience:** CTO
**Format:** Brief

---

## What Worked

- [Record each step that completed without manual intervention]
- [Note whether Researcher output began with `RESEARCH OUTPUT` on the first line]
- [Note whether Data Analyzer consumed Researcher output directly (no reformatting)]
- [Note whether Writer produced WRITER METADATA, CITATIONS, and CLAIMS TO VERIFY]

## What Didn't / Concerns

- [Record any step that required manual intervention or produced non-compliant output]
- [Or: "None — all three steps produced spec-compliant structured output. No manual
  reformatting required at any step."]

## Confidence Accuracy

- [Note whether confidence ratings across the chain were well-calibrated for the topic]
- [Note whether any inference confidence felt over- or under-stated given the findings]

## Coverage Assessment

- [Note whether high-confidence findings appeared in the final brief]
- [Note whether evidence gaps were surfaced correctly by the Writer]

## Action Items

- [ ] [Any remaining gaps, or "None — full chain passed. Pipeline is automated end-to-end."]
```

**Step 2: Verify the file was created and quality signal is set**
```bash
head -10 docs/test-log/chains/2026-03-03-postgres-vs-mongodb-chain-compliance.md
```
Expected: YAML frontmatter with `quality_signal:` set to `pass`, `mixed`, or `fail`.

**Step 3: Commit**
```bash
git add docs/test-log/chains/2026-03-03-postgres-vs-mongodb-chain-compliance.md
git commit -m "docs: log Researcher → Data Analyzer → Writer chain compliance validation"
```

---

## Success Criteria

All of the following must be true before this plan is complete:

| Check | Pass Condition |
|---|---|
| Researcher opening line | Response begins with `RESEARCH OUTPUT` — no preamble |
| Researcher FINDINGS format | Multi-line key-value: `Claim:` / `Source:` / `Tier:` / `Confidence:` |
| Writer WRITER METADATA | Block present, first, with `Input type: analysis-output` and `Confidence distribution:` |
| Writer CITATIONS | Block present; inference-sourced claims carry `type: inference` |
| Writer CLAIMS TO VERIFY | Block present; numeric inference claims flagged |
| Chain automation | Full R → DA → W chain completes — no manual reformatting at any step |
| Chain quality signal | `pass` (not `mixed` or `fail`) |

---

## Files Changed

| File | Change |
|---|---|
| `specialists/researcher/index.md` | COMPLIANCE NOTE added after Stage 7 format block |
| `specialists/writer/index.md` | Step 9 structural compliance checklist added to Stage 5 |
| `docs/test-log/researcher/2026-03-03-format-compliance-fix.md` | Created — Sprint 1 test log |
| `docs/test-log/writer/2026-03-03-format-compliance-fix.md` | Created — Sprint 2 test log |
| `docs/test-log/chains/2026-03-03-postgres-vs-mongodb-chain-compliance.md` | Created — Sprint 3 chain test log |
