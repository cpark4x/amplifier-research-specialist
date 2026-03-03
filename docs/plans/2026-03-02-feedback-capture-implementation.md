# Feedback Capture System — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement the feedback capture system from `docs/plans/2026-03-02-feedback-capture-system-design.md` — a skill, context nudge, recipe, and front matter migration that closes the test log loop from capture to backlog promotion.

**Architecture:** A project-scoped skill carries the full protocol. A 3-line nudge in `context/specialists-instructions.md` ensures agents offer capture after chain runs. A recipe automates the full loop. Two existing test log entries are migrated to include structured YAML front matter.

**Tech Stack:** Amplifier skill system, Amplifier recipe YAML, Markdown

---

### Task 1: Migrate existing test log entries

**Files:**
- Modify: `docs/test-log/chains/2026-03-02-microsoft-anthropic-competitive-brief.md`
- Modify: `docs/test-log/chains/2026-03-02-notion-vs-obsidian-competitive-brief.md`

**Step 1: Add front matter to the microsoft-anthropic entry**

The file currently starts with `# Microsoft vs. Anthropic Competitive Positioning`. Insert this YAML block before that line:

```yaml
---
specialist: researcher
chain: "researcher → writer"
topic: microsoft-anthropic-competitive-brief
date: 2026-03-02
quality_signal: mixed
action_items_promoted: false
---
```

**Step 2: Add front matter to the notion-vs-obsidian entry**

The file currently starts with `# Notion vs. Obsidian — Knowledge Worker Comparison`. Insert this YAML block before that line:

```yaml
---
specialist: competitive-analysis
chain: "competitive-analysis → writer"
topic: notion-vs-obsidian
date: 2026-03-02
quality_signal: mixed
action_items_promoted: true
---
```

**Step 3: Verify both files**

Read the first 10 lines of each file. Confirm: front matter block appears before the `#` heading, `---` delimiters are correct, no extra blank lines between front matter and heading.

**Step 4: Commit**

```bash
git add docs/test-log/chains/
git commit -m "docs: add front matter schema to existing test log entries"
```

---

### Task 2: Create the feedback-capture skill

**Files:**
- Create: `.amplifier/skills/feedback-capture.md`

Note: `.amplifier/` exists but `skills/` subdirectory may not. Create it if needed:
```bash
mkdir -p .amplifier/skills
```

**Step 1: Create the skill file**

Create `.amplifier/skills/feedback-capture.md` with this exact content:

```markdown
# feedback-capture

Structured protocol for capturing test log feedback after specialist runs and routing findings to the right destinations in the repo.

## When to Use

**Auto-nudge (light):** After a specialist chain completes, offer once:
> "Want to log this run? I can capture what worked, any concerns, and route action items to the backlog."

If declined, do not ask again in the session. If the user says yes — or requests feedback capture at any time — follow this protocol in full.

**On demand:** Any time the user asks to "capture feedback", "log this run", "write a test log entry", or similar.

## Capture Flow

Work through these sections conversationally, one at a time. Infer what you can from session context; confirm with the user before writing.

### 1. Collect Metadata (infer + confirm)

- **specialist** — entry-point specialist tested (`researcher`, `writer`, or `competitive-analysis`)
- **chain** — full chain if multi-step (e.g. `"researcher → writer"`), `null` if single specialist
- **topic** — slug identifying the subject (e.g. `notion-vs-obsidian`)
- **date** — today's date (YYYY-MM-DD)

### 2. What Worked?

Prompt: *"What worked well in this run? Consider: output quality, accuracy, schema usefulness, any synthesis that surprised you."*

### 3. What Didn't / Concerns?

Prompt: *"Any concerns or gaps? Consider: missing behaviors, wrong calls, confidence miscalibration, anything you'd flag for improvement."*

### 4. Confidence Accuracy

Prompt: *"Were confidence ratings calibrated correctly? Over-confident on hard-to-verify claims? Under-confident on solid ones?"*

### 5. Coverage Assessment

Prompt: *"Did coverage flags fire at the right time? Were gaps named correctly, or were they missed?"*

### 6. Action Items

Prompt: *"What should change? Capture as `- [ ]` checkboxes, one per distinct finding."*

### 7. Quality Signal

Prompt: *"Overall signal for this run — pass, mixed, or fail?"*
- **pass** — output met the quality bar
- **mixed** — partial concerns, some things to address
- **fail** — significant quality issues

## Writing the File

**File location:**
- Single specialist: `docs/test-log/{specialist}/{date}-{topic}.md`
- Chain: `docs/test-log/chains/{date}-{topic}.md`

**Required front matter:**

```yaml
---
specialist: {specialist}
chain: "{chain}"        # omit this line entirely if null
topic: {topic}
date: {date}
quality_signal: {pass|mixed|fail}
action_items_promoted: false
---
```

Follow with the full log body using the standard 5-section structure:
`## What Worked` / `## What Didn't / Concerns` / `## Confidence Accuracy` / `## Coverage Assessment` / `## Action Items`

## Triage: Routing Action Items

After writing the file, route each `- [ ]` action item using this table:

| Finding type | Destination |
|---|---|
| Consistent quality gap | New item in `BACKLOG.md` |
| Edge case in one specialist | Open question in `docs/02-requirements/epics/0{N}-{specialist}.md` |
| Pattern across multiple runs | Note in `docs/adding-a-specialist.md` |
| Confidence systematically off | Issue in `specialists/{specialist}/index.md` |

After routing, update `action_items_promoted` in the front matter:
- `true` — all action items promoted
- `partial` — some promoted, some deferred
- `false` — no items needed routing (rare)

## Commit

Commit the test log file and all updated destination files together:

```
git commit -m "docs: add test log entry for {chain or specialist} ({topic})"
```
```

**Step 2: Verify the skill loads**

```
load_skill(skill_name="feedback-capture")
```

Expected: skill loads successfully, all sections present (When to Use, Capture Flow, Writing the File, Triage, Commit).

**Step 3: Commit**

```bash
git add .amplifier/skills/feedback-capture.md
git commit -m "feat: add feedback-capture skill"
```

---

### Task 3: Add context nudge to specialists-instructions

**Files:**
- Modify: `context/specialists-instructions.md`

**Step 1: Read the current file**

Read `context/specialists-instructions.md`. It currently ends at line 50:
`3. \`specialists:writer\` → transforms competitive intelligence into a brief or report`

**Step 2: Append the nudge section**

Add this block at the very end of the file (after a blank line):

```markdown

## Feedback Capture

After a specialist chain completes, offer once to capture a test log entry:
> "Want to log this run? I can capture what worked, any concerns, and route action items to the backlog."

For the full procedure, load the `feedback-capture` skill.
```

**Step 3: Verify**

Read the last 10 lines of `context/specialists-instructions.md`. Confirm: the `## Feedback Capture` section is present, the blockquote is correctly formatted, and the skill reference is on its own line.

**Step 4: Commit**

```bash
git add context/specialists-instructions.md
git commit -m "feat: add feedback capture nudge to specialists-instructions context"
```

---

### Task 4: Create the capture-feedback recipe

**Files:**
- Create: `recipes/capture-feedback.yaml`

**Step 1: Create the recipes directory**

```bash
mkdir -p recipes
```

**Step 2: Create the recipe file**

Create `recipes/capture-feedback.yaml` with this content:

```yaml
name: capture-feedback
description: >
  Capture a structured test log entry for a specialist chain run,
  triage action items to the right destinations, and commit everything.

steps:
  - name: collect-metadata
    agent: self
    instruction: |
      You are starting a feedback capture session for a specialist run in the
      canvas-specialists project.

      Infer from session context:
      - specialist: entry-point specialist tested (researcher, writer, or competitive-analysis)
      - chain: full chain if multi-step (e.g. "researcher → writer"), or null if single
      - topic: a short slug for the subject (e.g. "notion-vs-obsidian")
      - date: today's date in YYYY-MM-DD format

      Confirm each value with the user before proceeding. Output confirmed metadata
      for use by subsequent steps.

  - name: capture-body
    agent: self
    instruction: |
      Walk through the 5 feedback sections with the user, one at a time:

      1. What worked? (output quality, accuracy, schema usefulness, synthesis)
      2. What didn't / concerns? (gaps, wrong calls, missing behaviors)
      3. Confidence accuracy — were ratings calibrated correctly?
      4. Coverage assessment — did coverage flags fire at the right time?
      5. Action items — collect as `- [ ]` checkboxes, one per distinct finding

      Collect all responses and output the full log body text.

  - name: assess-quality
    agent: self
    instruction: |
      Ask the user for a top-level quality signal:
      - pass: output met the quality bar
      - mixed: partial concerns, things to address
      - fail: significant quality issues

      Prompt: "Overall signal for this run — pass, mixed, or fail?"
      Store result as quality_signal.

  - name: write-log
    agent: self
    instruction: |
      Write the test log file.

      File path:
      - Chain run: docs/test-log/chains/{date}-{topic}.md
      - Single specialist: docs/test-log/{specialist}/{date}-{topic}.md

      File must begin with YAML front matter:

        ---
        specialist: {specialist}
        chain: "{chain}"        # omit line if null
        topic: {topic}
        date: {date}
        quality_signal: {quality_signal}
        action_items_promoted: false
        ---

      Follow with the full 5-section log body from the capture-body step.

  - name: triage-action-items
    agent: self
    instruction: |
      Route each `- [ ]` action item from the log using this table:

        Consistent quality gap         → new item in BACKLOG.md
        Edge case in one specialist    → open question in docs/02-requirements/epics/
        Pattern across multiple runs   → note in docs/adding-a-specialist.md
        Confidence systematically off  → issue in specialists/{specialist}/index.md

      Make all edits. Then update action_items_promoted in the test log front matter:
        true    — all items promoted
        partial — some promoted, some deferred
        false   — no items needed routing

  - name: commit
    agent: foundation:git-ops
    instruction: |
      Commit all touched files: the new test log entry plus any updated
      BACKLOG.md, epic files, or specialist index.md files.

      Commit message:
        Chain run:         "docs: add test log entry for {chain} chain ({topic})"
        Single specialist: "docs: add test log entry for {specialist} ({topic})"
```

**Step 3: Validate the recipe**

```
recipes tool operation=validate recipe_path=specialists:recipes/capture-feedback.yaml
```

Expected: validation passes with no schema errors.

**Step 4: Commit**

```bash
git add recipes/capture-feedback.yaml
git commit -m "feat: add capture-feedback recipe"
```

---

### Task 5: Final verification

**Step 1: Confirm all new files exist**

```bash
ls .amplifier/skills/feedback-capture.md && echo "skill ok"
ls recipes/capture-feedback.yaml && echo "recipe ok"
```

Expected: both lines print their `ok` confirmation.

**Step 2: Confirm context nudge is in place**

```bash
tail -8 context/specialists-instructions.md
```

Expected: output shows the `## Feedback Capture` section.

**Step 3: Confirm test log front matter**

```bash
head -10 docs/test-log/chains/2026-03-02-microsoft-anthropic-competitive-brief.md
head -10 docs/test-log/chains/2026-03-02-notion-vs-obsidian-competitive-brief.md
```

Expected: both files start with `---`, contain the 6 front matter fields, and close with `---` before the `#` heading.

**Step 4: Confirm git log**

```bash
git log --oneline -6
```

Expected (newest first):
```
<hash> feat: add capture-feedback recipe
<hash> feat: add feedback-capture skill
<hash> feat: add feedback capture nudge to specialists-instructions context
<hash> docs: add front matter schema to existing test log entries
f69e5e7 docs: add feedback capture system design doc
```
