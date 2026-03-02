# Citation Confidence Scoring — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add `confidence: high (0.9)` to each CITATIONS entry and a `Confidence distribution` summary to WRITER METADATA — no new LLM calls, values derived from existing Researcher confidence signals.

**Architecture:** Three files change. `shared/interface/types.md` gets the mapping constants. `specialists/writer/index.md` gets updated Stage 1 (capture confidence per claim) and Stage 5 (output confidence in CITATIONS + distribution in WRITER METADATA) instructions plus an updated output format template. `specialists/writer/README.md` gets updated field descriptions.

**Tech Stack:** Markdown prompt engineering. No code. Verification is via specialist invocation.

---

## Task 1: Add confidence mapping constants to `shared/interface/types.md`

**File:** `shared/interface/types.md`

Add a new section after the existing `## Confidence Levels` section (after line 78, before `## Schema Version`):

```markdown
## Confidence Mapping (Writer Output)

When the Writer produces CITATIONS, it maps Researcher confidence levels to numeric values.
These are **fixed categorical-to-numeric mappings**, not measured probabilities.

| Categorical | Numeric | Notes |
|-------------|---------|-------|
| `high`      | `0.9`   | Primary source or 2+ independent secondary sources |
| `medium`    | `0.6`   | Single secondary source |
| `low`       | `0.3`   | Single tertiary or unconfirmed source |
| `unrated`   | —       | Source has no Researcher confidence signal (raw notes, analyst output) |

The numeric values are intentionally spaced to reflect the categorical gap — they are not
interchangeable with a continuously-measured confidence score.

```

**Verify:** Read the file. Confirm the table appears between Confidence Levels and Schema Version. Confirm `v1.0` schema version line is still present and unchanged.

**Commit:**
```bash
git add shared/interface/types.md
git commit -m "docs: add confidence mapping constants to shared interface types"
```

---

## Task 2: Update Stage 1 — capture confidence label per claim

**File:** `specialists/writer/index.md`

Find this block (lines 58–65):

```
5. Number each discrete factual claim in the source material: S1, S2, S3, etc.
   Write out the numbered list — this is output, not internal state:

   S1: [claim text]
   S2: [claim text]
   ...

   You will reference these numbers in the CITATIONS section after the document.
```

Replace with:

```
5. Number each discrete factual claim in the source material: S1, S2, S3, etc.
   Write out the numbered list — this is output, not internal state:

   S1: [claim text] | confidence: [high|medium|low|unrated]
   S2: [claim text] | confidence: [high|medium|low|unrated]
   ...

   - If input type is `researcher-output`: read the `confidence` field from the corresponding Finding
   - If input type is `analyst-output` or `raw-notes`: mark every claim as `unrated`

   You will reference these numbers in the CITATIONS section after the document.
```

**Verify:** Read the file. Confirm the Stage 1 step 5 block now includes the `| confidence:` column and the two-bullet rule about researcher-output vs other input types.

**Commit:**
```bash
git add specialists/writer/index.md
git commit -m "feat(writer): capture confidence label per claim in Stage 1"
```

---

## Task 3: Update Stage 5 — add confidence to CITATIONS entries

**File:** `specialists/writer/index.md`

Find step 6 in Stage 5 (lines 122–124):

```
6. Produce the CITATIONS section: for each source claim S1, S2, S3 ... from Stage 1,
   state which section of the document used it, or mark it as unused. Every Sn that
   appears in an attribution line must appear in the CITATIONS block.
```

Replace with:

```
6. Produce the CITATIONS section: for each source claim S1, S2, S3 ... from Stage 1,
   state which section of the document used it (or mark it as unused), and include
   the confidence from your Stage 1 list. Use the fixed mapping:
     high → 0.9 | medium → 0.6 | low → 0.3 | unrated → unrated (no numeric)
   Every Sn that appears in an attribution line must appear in the CITATIONS block.
```

**Verify:** Read the file. Confirm step 6 now includes the confidence mapping inline and the format instruction.

**Commit:**
```bash
git add specialists/writer/index.md
git commit -m "feat(writer): include confidence field in CITATIONS entries (Stage 5)"
```

---

## Task 4: Update Stage 5 — add confidence distribution to WRITER METADATA

**File:** `specialists/writer/index.md`

In Stage 5, after step 6 (the CITATIONS step), add step 7:

```
7. Add `Confidence distribution` to WRITER METADATA: count high/medium/low/unrated
   from your Stage 1 claim list (include all claims, used and unused).
   Format: `Confidence distribution: [n] high · [n] medium · [n] low · [n] unrated`
```

**Verify:** Read the file. Confirm stage 5 now has 7 steps, and step 7 describes the distribution calculation.

**Commit:**
```bash
git add specialists/writer/index.md
git commit -m "feat(writer): add confidence distribution to WRITER METADATA (Stage 5)"
```

---

## Task 5: Update the output format template

**File:** `specialists/writer/index.md`

**Change 1 — Block 1 (WRITER METADATA):**

Find (lines 135–146):
```
WRITER METADATA
Specialist: writer
Version: 1.0
Input type: [researcher-output | analyst-output | raw-notes]
Output format: [report | brief | proposal | executive-summary | email | memo]
Audience: [specified audience]
Voice: [formal | conversational | executive]
Word count: [approximate]
Coverage: [full | partial]
Coverage gaps: [what could not be written from source material — "none" if full coverage]
```

Replace with:
```
WRITER METADATA
Specialist: writer
Version: 1.0
Input type: [researcher-output | analyst-output | raw-notes]
Output format: [report | brief | proposal | executive-summary | email | memo]
Audience: [specified audience]
Voice: [formal | conversational | executive]
Word count: [approximate]
Coverage: [full | partial]
Coverage gaps: [what could not be written from source material — "none" if full coverage]
Confidence distribution: [n high · n medium · n low · n unrated]
```

**Change 2 — Block 3 (CITATIONS):**

Find (lines 166–173):
```
---

CITATIONS
S1: "[source claim text]" → used in: [section/paragraph]
S2: "[source claim text]" → used in: [section/paragraph]
S3: "[source claim text]" → not used
```

Replace with:
```
---

CITATIONS
S1: "[source claim text]" → used in: [section/paragraph] | confidence: high (0.9)
S2: "[source claim text]" → used in: [section/paragraph] | confidence: medium (0.6)
S3: "[source claim text]" → not used | confidence: low (0.3)
S4: "[source claim text]" → used in: [section/paragraph] | confidence: unrated
```

**Verify:** Read the output format section. Confirm WRITER METADATA template has `Confidence distribution` as the last field. Confirm CITATIONS template shows `| confidence: X (Y)` on each entry with an `unrated` example.

**Commit:**
```bash
git add specialists/writer/index.md
git commit -m "feat(writer): update output format template with confidence fields"
```

---

## Task 6: Update `specialists/writer/README.md`

**File:** `specialists/writer/README.md`

Find the `Citations` bullet in the WRITER METADATA fields list:

```
- `Citations` — one entry per inline `[Sn]` marker: source text snippet (≤20 words) + document location where the marker appears; enables callers to verify any output claim against source material
```

Replace with:

```
- `Citations` — one entry per inline `[Sn]` marker: source text snippet (≤20 words) + document location + confidence (`high (0.9)`, `medium (0.6)`, `low (0.3)`, or `unrated`); enables callers to filter or weight output claims by source trustworthiness
- `Confidence distribution` — count of high/medium/low/unrated citations (e.g. `3 high · 1 medium · 0 low · 2 unrated`); enables quick assessment of overall document trustworthiness without reading all CITATIONS entries
```

**Verify:** Read the file. Confirm the Citations bullet now mentions confidence values. Confirm the new `Confidence distribution` bullet is present directly after it.

**Commit:**
```bash
git add specialists/writer/README.md
git commit -m "docs(writer): update README to document confidence fields in CITATIONS and WRITER METADATA"
```

---

## Task 7: End-to-end verification

Invoke the writer specialist with a sample ResearchOutput that has at least one high, one medium, and one unrated source claim:

```
Pass this to specialists:writer:

Source material (researcher-output):
FINDINGS
S1: "Remote workers average 4.2 hours/day in meetings" | source: Microsoft Work Trend Index | tier: primary | confidence: high
S2: "Context-switching costs ~2 hours/day" | source: HBR article | tier: secondary | confidence: medium
S3: Raw note — "Teams report declining morale over 6 months" (no source)

Write a brief for an HR leadership team.
```

**Check the output:**

1. Stage 1 list shows `| confidence: high`, `| confidence: medium`, `| confidence: unrated`
2. WRITER METADATA includes `Confidence distribution: 1 high · 1 medium · 0 low · 1 unrated`
3. CITATIONS block has `| confidence: high (0.9)`, `| confidence: medium (0.6)`, `| confidence: unrated`
4. No numeric value appears next to `unrated` — just the word

If all four checks pass: feature is complete.

**Final commit (if any fixes made):**
```bash
git add -A
git commit -m "fix(writer): citation confidence scoring verification fixes"
```

**Push:**
```bash
git push origin main
```
