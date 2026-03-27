# Section-Level Source Attribution — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal:** Add `> *Sources: Sn (label), Sn (label)*` attribution blockquotes after every factual section in writer output, giving human readers claim-level trust signals at the point of reading.

**Architecture:** The writer already numbers source claims in Stage 1 and produces a post-doc CITATIONS block. This plan adds one new output element — section-level attribution lines appended after drafting each section in Stage 4, with a verification check in Stage 5. No new pipeline stages. No new LLM calls. Changes are to `specialists/writer/index.md` and `specialists/writer/README.md` only.

**Tech Stack:** Markdown instruction files. No code.

---

### Task 1: Update Stage 4 — append attribution after each section

**File:**
- Modify: `specialists/writer/index.md` — Stage 4: Draft section

**Current Stage 4 ending (lines ~97–103):**
```
- Do not add interpretation beyond what the source material contains
```

**Step 1: Read the file to confirm exact current text**
```bash
grep -n "Stage 4" /Users/chrispark/Projects/specialists/specialists/writer/index.md
```

**Step 2: Add attribution instruction to Stage 4**

After the last bullet in Stage 4, add:

```markdown
After drafting each section, immediately append a source attribution line before
moving to the next section:

  > *Sources: S1 (3–6 word label), S2 (3–6 word label)*

  Rules:
  - The label is a short phrase from the source claim that identifies it at a glance
  - Include every Sn drawn on in that section
  - If a section draws on more than 4 claims, group: `> *Sources: S1–S3 (pipeline), S5 (quality gate)*`
  - Sections with no factual claims (pure transitions, headings) do not get an attribution line
  - Write the section first, then append the attribution — do not interrupt prose
```

**Step 3: Verify**
Read Stage 4 back. Attribution instruction should appear after the existing draft bullets.

**Step 4: Commit**
```bash
cd /Users/chrispark/Projects/specialists
git add specialists/writer/index.md
git commit -m "feat(writer): add section-level source attribution in Stage 4"
```

---

### Task 2: Update Stage 5 — verify attribution lines

**File:**
- Modify: `specialists/writer/index.md` — Stage 5: Verify and Cite section

**Current Stage 5 check 5 (lines ~112–115):**
```
5. Produce the CITATIONS section: for each source claim S1, S2, S3 ... from Stage 1,
   state which section of the document used it, or mark it as unused.
```

**Step 1: Replace check 5 with two checks**

Replace the current check 5 with:
```markdown
5. Attribution completeness: every section with factual content has a
   `> *Sources: ...*` line. If any factual section is missing one, add it
   before returning.
6. Produce the CITATIONS section: for each source claim S1, S2, S3 ... from Stage 1,
   state which section of the document used it, or mark it as unused. Every Sn that
   appears in an attribution line must appear in the CITATIONS block.
```

**Step 2: Verify**
Read Stage 5. Should now have 6 checks with attribution completeness as #5 and CITATIONS as #6.

**Step 3: Commit**
```bash
git add specialists/writer/index.md
git commit -m "feat(writer): add attribution completeness check to Stage 5"
```

---

### Task 3: Update Output Format template

**File:**
- Modify: `specialists/writer/index.md` — Output Format section

**Goal:** Show attribution blockquotes in the document body example so the writer has a concrete template to follow.

**Step 1: Find the Output Format section**
```bash
grep -n "Output Format\|DOCUMENT CONTENT\|Block 2" /Users/chrispark/Projects/specialists/specialists/writer/index.md
```

**Step 2: Update Block 2 example**

The current Block 2 shows:
```
---

[DOCUMENT CONTENT HERE]
```

Replace with:
```markdown
**Block 2 — Document content** (the actual document, with section attribution):
```
---

## [Section Heading]

[Prose content drawn from source material...]

> *Sources: S1 (brief label), S2 (brief label)*

## [Next Section]

[More prose...]

> *Sources: S3 (brief label)*
```
```

**Step 3: Verify**
Read the Output Format section back. Block 2 should now show the attribution pattern inline.

**Step 4: Commit**
```bash
git add specialists/writer/index.md
git commit -m "feat(writer): update output format template with attribution example"
```

---

### Task 4: Update writer/README.md — document attribution in Returns

**File:**
- Modify: `specialists/writer/README.md` — Returns section

**Step 1: Find Returns section**
```bash
grep -n "Returns\|Citations\|Coverage" /Users/chrispark/Projects/specialists/specialists/writer/README.md
```

**Step 2: Add attribution to key fields**

After the `Citations` bullet, add:
```markdown
- `Section attribution` — after every factual section in the document, a blockquote `> *Sources: Sn (label)*` lists the source claims used in that section; enables trust verification at the point of reading without consulting the full CITATIONS index
```

**Step 3: Verify**
Read the Returns section. Section attribution should appear after Citations.

**Step 4: Commit**
```bash
git add specialists/writer/README.md
git commit -m "docs(writer): add section attribution to README contract"
```

---

### Task 5: Test — invoke writer and verify attribution appears

**Step 1: Invoke the writer**

Use the delegate tool to call `specialists:writer` with this input:

```
Source material:
- The amplifier-research-specialist writer runs a 5-stage pipeline.
- Stage 2 is a coverage audit that runs before drafting begins.
- Every output starts with a WRITER METADATA block.
- The writer never generates claims not present in the source.
- The researcher runs a 7-stage pipeline ending in a Quality Gate.

Format: brief
Audience: developer
Voice: conversational
```

**Step 2: Verify the output contains all three layers**

- [ ] WRITER METADATA block at top (document-level trust)
- [ ] `> *Sources: ...*` attribution line after each factual section (claim-level trust)
- [ ] CITATIONS block at end (agent-parseable index)
- [ ] Every Sn in attribution lines appears in CITATIONS block
- [ ] Prose reads naturally — attribution feels like a footnote, not clutter

**Step 3: If attribution lines are missing**
Re-read Stage 4 in `index.md`. Check whether the instruction is clear enough. Fix the specific wording — do NOT add more complexity. Re-test.

---

### Task 6: Commit ROADMAP.md and push everything

**Step 1: Create ROADMAP.md if it doesn't exist**
```bash
ls /Users/chrispark/Projects/specialists/docs/ROADMAP.md
```
If missing, the file needs to be created (see content in design doc session notes).

**Step 2: Stage all remaining changes**
```bash
cd /Users/chrispark/Projects/specialists
git status
git add -A
```

**Step 3: Final commit and push**
```bash
git commit -m "feat(writer): section-level source attribution complete"
git push origin main
```

**Step 4: Verify on GitHub**
```bash
gh repo view cpark4x/amplifier-research-specialist --web
```
Confirm latest commit is on main.
