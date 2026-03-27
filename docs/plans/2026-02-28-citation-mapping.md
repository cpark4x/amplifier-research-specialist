# Citation Mapping — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal:** Add inline citation markers (`[S1]`, `[S2]`, ...) to writer output so every factual claim traces to an exact source passage, with a Citations block in WRITER METADATA mapping each marker back to its source.

**Architecture:** The writer already enforces source fidelity at the behavior level. Citation mapping makes that fidelity explicit and auditable. During Stage 1, source claims are labeled. During Stage 4, inline markers are added to prose. The WRITER METADATA block gains a Citations field listing every marker, the source text it refers to, and where it appears in the document.

**Tech Stack:** Markdown instruction files only — no code. Changes are to `specialists/writer/index.md` (pipeline behavior), `specialists/writer/README.md` (interface contract), and the WRITER METADATA output format.

---

## Task 1: Update Stage 1 (Parse Input) — label source claims

**Files:**
- Modify: `specialists/writer/index.md` — Stage 1: Parse Input section

**What to change:**
Add a step to Stage 1 that assigns citation labels to source claims as they are parsed. Every discrete factual claim, finding, or evidence item in the source material gets a unique label (`[S1]`, `[S2]`, ...) before drafting begins. This label is internal working state used in Stage 4.

**Step 1: Open the file and find Stage 1**

```
specialists/writer/index.md — lines ~52-58 (Stage 1: Parse Input)
```

**Step 2: Add citation labeling step to Stage 1**

After the existing Stage 1 steps, add:

```markdown
5. Assign citation labels to source claims: scan the source material for discrete
   factual claims, findings, and evidence items. Label each one sequentially:
   [S1], [S2], [S3], etc. Keep an internal citation map:
   [Sn] → source text snippet (≤ 20 words) + location (section heading or field name)
   This map is used in Stage 4 and reported in WRITER METADATA.
```

**Step 3: Verify**

Read the file back. Stage 1 should now have 5 steps, ending with the citation labeling step.

---

## Task 2: Update Stage 4 (Draft) — add inline markers

**Files:**
- Modify: `specialists/writer/index.md` — Stage 4: Draft section

**What to change:**
Add an instruction to Stage 4 that places inline citation markers in prose. When a sentence draws on a labeled source claim, the marker appears at the end of the sentence in brackets.

**Step 1: Find Stage 4**

```
specialists/writer/index.md — lines ~86-93 (Stage 4: Draft)
```

**Step 2: Add inline citation instruction to Stage 4**

After the existing Stage 4 bullet points, add:

```markdown
- For each sentence that draws on a labeled source claim: append the citation
  marker inline — e.g., "The pipeline runs a quality gate before returning output. [S3]"
  - One marker per sentence maximum (use the most specific claim label)
  - If a sentence synthesizes multiple claims: use the primary one; note others in
    the Citations block
  - Non-factual sentences (transitions, structural language) do not get markers
```

**Step 3: Verify**

Read Stage 4 back. It should now include the inline marker instruction alongside the existing source fidelity rules.

---

## Task 3: Update Stage 5 (Verify) — add citation completeness check

**Files:**
- Modify: `specialists/writer/index.md` — Stage 5: Verify section

**What to change:**
Add a citation completeness check to Stage 5. Before returning output, verify that every factual claim in the document has a citation marker, and every marker in the Citations block maps to a real source passage.

**Step 1: Find Stage 5**

```
specialists/writer/index.md — lines ~94-103 (Stage 5: Verify)
```

**Step 2: Add citation check to Stage 5**

After the existing 4 verify checks, add:

```markdown
5. Citation completeness: every factual sentence in the document has an inline
   marker. Every marker in the Citations block maps to a real source passage.
   No marker appears in the document without an entry in the Citations block.
   If any factual sentence is unmarked: add the marker before returning.
```

---

## Task 4: Update WRITER METADATA output format — add Citations block

**Files:**
- Modify: `specialists/writer/index.md` — Output Format section

**What to change:**
Add a `Citations:` field to the WRITER METADATA block. This maps each `[Sn]` marker to the source text it refers to and the document location where it appears.

**Step 1: Find the Output Format section**

```
specialists/writer/index.md — lines ~106-123 (Output Format section)
```

**Step 2: Replace the existing WRITER METADATA template**

Old template ends at:
```
Coverage gaps: [what could not be written from source material — "none" if full coverage]
```

Add after Coverage gaps, before the closing `---`:

```markdown
Citations:
  [S1] "[source text snippet ≤20 words]" → [document location, e.g., "Background, para 1"]
  [S2] "[source text snippet ≤20 words]" → [document location]
  ... (one line per marker used)
```

**Step 3: Verify**

Read the Output Format section back. The Citations block should appear in the template between Coverage gaps and the closing `---`.

---

## Task 5: Update writer/README.md — reflect Citations in Returns

**Files:**
- Modify: `specialists/writer/README.md` — Returns section

**What to change:**
Add `Citations` to the list of key fields in the Returns section, describing what the field contains and why it exists.

**Step 1: Find the Returns section**

```
specialists/writer/README.md — lines ~22-30 (Returns section)
```

**Step 2: Add Citations field**

After the existing key fields (Input type, Output format, Audience, Voice, Word count, Coverage, Coverage gaps), add:

```markdown
- `Citations` — one entry per inline `[Sn]` marker: source text snippet (≤20 words) + document location where the marker appears; enables callers to verify any output claim against source material
```

**Step 3: Verify**

Read the Returns section back. Citations should appear as the last item in the key fields list.

---

## Task 6: Test — invoke writer and verify citations appear

**Step 1: Invoke the writer specialist**

Pass a short piece of structured source material (3-5 distinct factual claims) and request a brief. This can be done via the delegate tool in the current session:

```
delegate(
  agent="specialists:writer",
  instruction="""
  Source material:
  - The amplifier-research-specialist writer runs a 5-stage pipeline.
  - Stage 2 is a coverage audit that runs before drafting begins.
  - Every output starts with a WRITER METADATA block.
  - The writer never generates claims not present in the source.
  - The researcher runs a 7-stage pipeline ending in a Quality Gate.

  Format: brief
  Audience: developer
  Voice: conversational
  """
)
```

**Step 2: Verify the output contains**

- [ ] Inline `[S1]`, `[S2]`, etc. markers in the prose
- [ ] A `Citations:` field in the WRITER METADATA block
- [ ] Every marker in prose has a matching entry in Citations
- [ ] Non-factual sentences (transitions) do not have markers

**Step 3: If any check fails**

Re-read `specialists/writer/index.md` and find which instruction is ambiguous or missing. Fix the specific stage before re-testing. Do not patch around it.

---

## Task 7: Commit and push

**Step 1: Stage all changed files**

```bash
cd /Users/chrispark/Projects/amplifier-research-specialist
git add specialists/writer/index.md specialists/writer/README.md docs/01-vision/VISION.md docs/plans/2026-02-28-citation-mapping.md
```

**Step 2: Commit**

```bash
git commit -m "feat(writer): add citation mapping to pipeline

- Stage 1: label source claims [S1], [S2], ... as input is parsed
- Stage 4: inline markers appended to factual sentences in prose
- Stage 5: citation completeness check added to verify pass
- WRITER METADATA: Citations block maps markers to source passages
- writer/README.md: Citations field documented in Returns contract

Closes the source fidelity gap identified in competitive analysis (8.5 → 9.5/10)."
```

**Step 3: Push**

```bash
git push origin main
```
