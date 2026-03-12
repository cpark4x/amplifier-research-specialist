# Competitive Analysis Follow-ups Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal:** Add two recipes for the competitive-analysis → writer chain and a "claims to verify" block to the Writer specialist.

**Architecture:** Three independent tasks — two new YAML recipe files, one targeted edit to an existing Markdown specialist file. No changes to the competitive-analysis specialist. No shared state between tasks; all three can be executed in parallel.

**Design doc:** `docs/plans/2026-03-02-competitive-analysis-followups-design.md`

---

## Task 1: Create `recipes/competitive-analysis-brief.yaml`

**Files:**
- Create: `recipes/competitive-analysis-brief.yaml`

**Step 1: Create the file with this exact content**

```yaml
name: "competitive-analysis-brief"
description: "Transform a competitive question into a polished document. Runs competitive-analysis then writer in sequence. For higher-fidelity runs with Researcher pre-pass, use competitive-analysis-brief-researched."
version: "1.0.0"
tags: ["competitive-analysis", "writing", "chain"]

steps:
  - id: "analyze"
    agent: "specialists:competitive-analysis"
    prompt: |
      Run a full competitive analysis on the following question.

      Query: {{query}}

      If subjects or dimensions were provided, use them:
      Subjects: {{subjects}}
      Dimensions: {{dimensions}}

      Follow your full 6-stage pipeline. Return your output in the standard
      CompetitiveAnalysisOutput format.
    output: "competitive_analysis_output"
    timeout: 1800

  - id: "write"
    agent: "specialists:writer"
    prompt: |
      Transform the following competitive analysis output into a polished document.

      Source material:
      {{competitive_analysis_output}}

      Output format: {{format}}
      Audience: {{audience}}

      If format or audience are empty, default to: format=report, audience=general.

      Follow your full 5-stage pipeline. Return WRITER METADATA, document content
      with section attribution lines, CITATIONS, and CLAIMS TO VERIFY blocks.
    output: "final_document"
    timeout: 900
```

**Step 2: Verify the recipe is valid YAML**

```bash
python3 -c "import yaml; yaml.safe_load(open('recipes/competitive-analysis-brief.yaml'))" && echo "VALID"
```
Expected: `VALID`

**Step 3: Run a quick end-to-end smoke test**

Invoke via the recipes tool with a minimal query:
```
recipes tool -> operation=execute, recipe_path=specialists:recipes/competitive-analysis-brief.yaml
context: {"query": "Compare Notion vs Linear as project management tools"}
```
Expected: Recipe runs both steps without error; `final_document` output contains WRITER METADATA block.

**Step 4: Commit**
```bash
git add recipes/competitive-analysis-brief.yaml
git commit -m "feat: add competitive-analysis-brief recipe (2-step chain)"
```

---

## Task 2: Create `recipes/competitive-analysis-brief-researched.yaml`

**Files:**
- Create: `recipes/competitive-analysis-brief-researched.yaml`

**Step 1: Create the file with this exact content**

```yaml
name: "competitive-analysis-brief-researched"
description: "High-fidelity competitive brief with Researcher pre-pass. Researcher gathers sourced evidence first, competitive-analysis builds the matrix from that evidence, writer produces the document."
version: "1.0.0"
tags: ["competitive-analysis", "research", "writing", "chain"]

steps:
  - id: "research"
    agent: "specialists:researcher"
    prompt: |
      Research the following competitive question. Gather sourced evidence for all
      relevant subjects across key competitive dimensions.

      Query: {{query}}

      Follow your full research pipeline. Return your standard ResearchOutput format
      with source tiering and per-claim confidence scores.
    output: "research_output"
    timeout: 2700

  - id: "analyze"
    agent: "specialists:competitive-analysis"
    prompt: |
      Run a competitive analysis using the pre-gathered research below.
      Skip Stage 2 (Research) — the research field is provided.

      Query: {{query}}
      Research: {{research_output}}

      If subjects or dimensions were provided, use them:
      Subjects: {{subjects}}
      Dimensions: {{dimensions}}

      Begin at Stage 3 (Profile). Return your output in the standard
      CompetitiveAnalysisOutput format.
    output: "competitive_analysis_output"
    timeout: 1800

  - id: "write"
    agent: "specialists:writer"
    prompt: |
      Transform the following competitive analysis output into a polished document.

      Source material:
      {{competitive_analysis_output}}

      Output format: {{format}}
      Audience: {{audience}}

      If format or audience are empty, default to: format=report, audience=general.

      Follow your full 5-stage pipeline. Return WRITER METADATA, document content
      with section attribution lines, CITATIONS, and CLAIMS TO VERIFY blocks.
    output: "final_document"
    timeout: 900
```

**Step 2: Verify valid YAML**
```bash
python3 -c "import yaml; yaml.safe_load(open('recipes/competitive-analysis-brief-researched.yaml'))" && echo "VALID"
```
Expected: `VALID`

**Step 3: Commit** (smoke test is covered by Task 1; these recipes share the same write step)
```bash
git add recipes/competitive-analysis-brief-researched.yaml
git commit -m "feat: add competitive-analysis-brief-researched recipe (3-step chain with Researcher pre-pass)"
```

---

## Task 3: Add `CLAIMS TO VERIFY` block to Writer specialist

**Files:**
- Modify: `specialists/writer/index.md`

Two targeted edits to this file. Read it before editing.

---

### Edit A — Stage 5: Add step 8

Find this text (end of Stage 5, step 7):
```
7. Add `Confidence distribution` to WRITER METADATA: count high/medium/low/unrated
   from your Stage 1 claim list (include all claims, used and unused).
   Format: `Confidence distribution: [n] high · [n] medium · [n] low · [n] unrated`
```

Add immediately after it:
```
8. Produce the CLAIMS TO VERIFY block — only when `input type` is `analyst-output`
   or `raw-notes`. When input type is `researcher-output`, skip this step entirely.
   - From your Stage 1 claim list, scan all `unrated` claims
   - Flag any claim containing a specific value: a number with a unit (87ms, 50-row,
     $10/mo, 2,000ms), a percentage (40%, 60%), a count with magnitude (200+, 8,000+),
     or a named statistic presented as fact
   - For each flagged claim: record the claim number, a short quote of the specific
     value, and its type (specific measurement | specific number | percentage |
     named statistic)
   - If no claims match: produce `CLAIMS TO VERIFY: none`
```

---

### Edit B — Output Format: Add Block 4

Find this text (end of Output Format section):
```
List every source claim from Stage 1. Mark each one as used (with location) or not used.
```

Add immediately after it:
```
**Block 4 — CLAIMS TO VERIFY** (analyst-output or raw-notes only; omit entirely for researcher-output):
```
CLAIMS TO VERIFY
Unrated claims containing specific values — verify before citing externally.
S3: "87ms load time" | type: specific measurement
S7: "50-row database cap" | type: specific number
S12: "8,000+ Zapier integrations" | type: specific count

(or: CLAIMS TO VERIFY: none)
```
```

---

**Step 3: Verify the edits look correct**

Read back `specialists/writer/index.md` and confirm:
- Stage 5 now has 8 steps (was 7)
- Output Format now has 4 blocks (was 3)
- No existing text was accidentally removed

**Step 4: Run a smoke test**

Invoke the Writer with competitive-analysis output containing specific numerical claims.
The output should include a `CLAIMS TO VERIFY` block listing at least one flagged claim.

```
delegate -> specialists:writer
instruction: "Transform this competitive analysis output into a brief.
  Source: [paste any CompetitiveAnalysisOutput that contains specific numbers]
  Format: brief. Audience: general."
```
Expected: Output contains `CLAIMS TO VERIFY` block (not `CLAIMS TO VERIFY: none`)

**Step 5: Commit**
```bash
git add specialists/writer/index.md
git commit -m "feat: add CLAIMS TO VERIFY block to Writer for unrated specific-value claims"
```

---

## Final Verification

After all 3 tasks are complete:

```bash
git log --oneline -5
```
Expected: 3 new commits on top of `daa480b`.

Confirm both recipe files exist:
```bash
ls recipes/
```
Expected: `capture-feedback.yaml  competitive-analysis-brief.yaml  competitive-analysis-brief-researched.yaml`

Confirm Writer has Block 4:
```bash
grep -n "CLAIMS TO VERIFY" specialists/writer/index.md
```
Expected: At least 3 matches (step 8 instruction + Block 4 header + example block).
