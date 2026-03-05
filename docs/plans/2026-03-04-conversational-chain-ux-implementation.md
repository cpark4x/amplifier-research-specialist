# Conversational Chain UX Implementation Plan

> **Execution:** Use the subagent-driven-development workflow to implement this plan.

**Goal:** Fix two UX problems — raw intermediate output surfacing to users instead of finished documents, and zero visibility into which specialists ran — by editing instruction/prompt files only.

**Architecture:** Two file surfaces are touched: the orchestrator's routing brain (`context/specialists-instructions.md`) gets 4 new rules that govern all conversational invocations, and each of 5 specialist `index.md` files gets a routing hint in its final stage so the orchestrator knows what was produced and what comes next. No Python code, no new files, no schema changes.

**Tech Stack:** Markdown instruction files only. No code, no tests, no dependencies.

**Design doc:** `docs/plans/2026-03-04-conversational-chain-ux-design.md`

---

## Critical Constraints (Read First)

### Output Schema Constraint
From `docs/01-vision/PRINCIPLES.md` — "Output schema is the contract": every specialist's output must start with its machine-parse signal as the very first characters (`RESEARCH OUTPUT`, `COMPETITIVE ANALYSIS BRIEF`, `Parsed:`, `ANALYSIS OUTPUT`, etc.). The routing hints added to specialist `index.md` files are **orchestrator instructions** — they tell the orchestrator what to announce on the specialist's behalf. They are **NOT additions to the specialist's output text**. They do not change what the specialist produces.

### TDD Adaptation for Prompt Files
These are instruction/prompt file changes — NOT Python code. There are no unit tests. The TDD cycle is adapted:
- **RED**: Document the expected behavior scenario + describe the current wrong behavior
- **GREEN**: Edit the instruction file, then run a short conversational verification to confirm the new behavior
- **COMMIT**: After each file change passes verification

Do NOT write Python unit tests for any task in this plan.

### Task Ordering Is Mandatory
Task 1 must complete before all others — it's the routing brain. Task 2 must be verified as a checkpoint before Tasks 3–6 — it validates the pattern. Tasks 3–6 are independent of each other after that.

---

## Task 1: Add Conversational Chain Behavior Rules to Routing Brain

**Files:**
- Modify: `context/specialists-instructions.md` (insert between lines 5 and 6)

**Current behavior (RED):** When a user says "Research edge AI for me" in conversation, the orchestrator delegates to the researcher and surfaces the raw `RESEARCH OUTPUT` block directly. The user sees machine-formatted structured data instead of a finished document. There is no narration about what's running.

**Expected behavior after change:** The orchestrator always completes through to the writer (default format = brief), narrates each step, and only surfaces raw output if the user explicitly asks for it.

---

**Step 1: Edit `context/specialists-instructions.md`**

Open `context/specialists-instructions.md`. Find this blank line between the intro paragraph and the `## Available Specialists` heading:

```
Delegate to these agents when quality and trustworthiness matter more than speed.

## Available Specialists
```

Insert the following new section in that blank line — so it appears AFTER line 4 ("Delegate to these agents...") and BEFORE `## Available Specialists`:

```markdown

## Conversational Chain Behavior

These rules apply to all conversational specialist invocations. Read this section first.

**Rule 1 — Chain Completion Default**
Always complete through to the writer before responding. Default output format = `brief`. Never stop at an intermediate specialist and surface the raw structured block. The user gets a finished document.

**Rule 2 — Per-Step Narration**
Before each delegation announce what's running. After each delegation announce what completed:
- Before: "🔍 Running researcher..."
- After: "✅ Researcher complete — passing to writer..."
- Final: "✍️ Done. Here's your brief."

**Rule 3 — Escape Hatch**
If the user explicitly says "raw output", "give me the raw research", "just run the researcher", or "don't write a document" — stop at that specialist and surface the structured block directly.

**Rule 4 — Analysis Signal**
If the user asks for "analysis", "insights", or "full analysis" — chain through data-analyzer before writer: researcher → data-analyzer → writer.

```

After the edit, the file should read (lines 1–27):
```
# Specialists: Available Agents

This bundle provides domain expert specialist agents for deep, structured work.
Delegate to these agents when quality and trustworthiness matter more than speed.

## Conversational Chain Behavior

These rules apply to all conversational specialist invocations. Read this section first.

**Rule 1 — Chain Completion Default**
Always complete through to the writer before responding. Default output format = `brief`. Never stop at an intermediate specialist and surface the raw structured block. The user gets a finished document.

**Rule 2 — Per-Step Narration**
Before each delegation announce what's running. After each delegation announce what completed:
- Before: "🔍 Running researcher..."
- After: "✅ Researcher complete — passing to writer..."
- Final: "✍️ Done. Here's your brief."

**Rule 3 — Escape Hatch**
If the user explicitly says "raw output", "give me the raw research", "just run the researcher", or "don't write a document" — stop at that specialist and surface the structured block directly.

**Rule 4 — Analysis Signal**
If the user asks for "analysis", "insights", or "full analysis" — chain through data-analyzer before writer: researcher → data-analyzer → writer.

## Available Specialists
```

**Step 2: Verify the escape hatch works**

Run this conversational test: say "Give me the raw research output on edge AI" to the orchestrator.

Expected behavior:
- The orchestrator reads Rule 3 and recognizes "raw research output" as an escape hatch signal
- It delegates to the researcher only
- It surfaces the `RESEARCH OUTPUT` block directly to the user
- It does NOT chain to the writer

If the orchestrator chains to the writer anyway, Rule 3 wording needs adjustment. Stop and fix before proceeding.

**Step 3: Commit**

```bash
git add context/specialists-instructions.md && git commit -m "feat: add conversational chain behavior rules to routing brain"
```

---

## Task 2: Add Routing Hint to Researcher + Verify Chain Narration

**Files:**
- Modify: `specialists/researcher/index.md` (insert between lines 285 and 287)

**Current behavior (RED):** The researcher's `index.md` has no signal telling the orchestrator what was produced or what should come next. The orchestrator has to guess.

**Expected behavior after change:** The researcher's final stage includes a routing signal section that the orchestrator can read to know: (1) a RESEARCH OUTPUT block was produced, (2) the quality score, and (3) the natural next step is the writer or data-analyzer.

---

**Step 1: Edit `specialists/researcher/index.md`**

Open `specialists/researcher/index.md`. Find the end of the Stage 7 compliance note section. Look for this exact sequence around lines 280–287:

```
Right:
```
RESEARCH OUTPUT

Question: What is the current state of WebAssembly...
```

---

## Source Tiers — Reference
```

Insert the following new section AFTER the closing ``` of the "Right:" example (after line 285) and BEFORE the `---` separator (line 287). There is currently a blank line 286 between them — replace that blank line with the new section:

```markdown

---

## Routing Signal (for orchestrator use only)

When your Stage 7 output is complete, this information is available to the orchestrator:
- Produced: RESEARCH OUTPUT block with sourced findings
- Quality: [quality_score] — [MET/NOT MET]
- Natural next step: writer (format=brief) or data-analyzer → writer if analysis was requested

This signal is for orchestrator routing and narration only — it does not appear in your output block.

```

After the edit, the area around the insertion should read:
```
Right:
```
RESEARCH OUTPUT

Question: What is the current state of WebAssembly...
```

---

## Routing Signal (for orchestrator use only)

When your Stage 7 output is complete, this information is available to the orchestrator:
- Produced: RESEARCH OUTPUT block with sourced findings
- Quality: [quality_score] — [MET/NOT MET]
- Natural next step: writer (format=brief) or data-analyzer → writer if analysis was requested

This signal is for orchestrator routing and narration only — it does not appear in your output block.

---

## Source Tiers — Reference
```

**Step 2: CHECKPOINT — Verify researcher → writer chain narrates correctly**

This is a mandatory checkpoint. Run this conversational test: say "Research edge AI for me" to the orchestrator.

Expected behavior (all four must pass):
1. The orchestrator narrates: "🔍 Running researcher..." (or similar) BEFORE delegating
2. The researcher runs and produces a `RESEARCH OUTPUT` block (the specialist output itself is unchanged)
3. The orchestrator narrates: "✅ Researcher complete — passing to writer..." (or similar) AFTER researcher finishes
4. The orchestrator delegates to the writer with format=brief, then narrates: "✍️ Done. Here's your brief." (or similar)
5. The user sees a finished brief — NOT a raw `RESEARCH OUTPUT` block

**If any of these fail:** Stop. Do NOT proceed to Tasks 3–6. Debug the routing brain rules (Task 1) or the routing hint wording. The pattern established here will be repeated five more times — get it right now.

**Step 3: Commit**

```bash
git add specialists/researcher/index.md && git commit -m "feat: add routing hint to researcher Stage 7"
```

---

## Task 3: Add Routing Hint to Writer

**Files:**
- Modify: `specialists/writer/index.md` (insert between lines 316 and 317)

**Current behavior (RED):** The writer's `index.md` has no signal telling the orchestrator that the chain is complete and the document should be delivered to the user.

**Expected behavior after change:** The writer's final stage includes a routing signal section that tells the orchestrator: (1) a finished document was produced, (2) coverage and confidence metadata is available, and (3) the chain is complete — deliver to the user.

---

**Step 1: Edit `specialists/writer/index.md`**

Open `specialists/writer/index.md`. Find the end of the Output Format section. Look for this exact sequence around lines 313–319:

```
**Why document first, metadata after:** Word count, coverage, and confidence distribution
are only known after writing. CITATIONS require knowing which claims you used. Producing
these blocks after the document means you have accurate values at the moment you need them.

---

## What You Do Not Do
```

Insert the following new section AFTER the "Why document first" paragraph (after line 315) and BEFORE the `---` separator (line 317). Replace the blank line 316 with the new section:

```markdown

---

## Routing Signal (for orchestrator use only)

When your Stage 5 output is complete, this information is available to the orchestrator:
- Produced: finished document in requested format with WRITER METADATA, CITATIONS, and CLAIMS TO VERIFY blocks
- Quality: coverage=[full/partial], confidence distribution in metadata
- Natural next step: chain complete — deliver to user

This signal is for orchestrator routing and narration only — it does not appear in your output block.

```

After the edit, the area around the insertion should read:
```
**Why document first, metadata after:** Word count, coverage, and confidence distribution
are only known after writing. CITATIONS require knowing which claims you used. Producing
these blocks after the document means you have accurate values at the moment you need them.

---

## Routing Signal (for orchestrator use only)

When your Stage 5 output is complete, this information is available to the orchestrator:
- Produced: finished document in requested format with WRITER METADATA, CITATIONS, and CLAIMS TO VERIFY blocks
- Quality: coverage=[full/partial], confidence distribution in metadata
- Natural next step: chain complete — deliver to user

This signal is for orchestrator routing and narration only — it does not appear in your output block.

---

## What You Do Not Do
```

**Step 2: Verify writer output is unchanged**

Quick sanity check: the writer's actual output format must still start with `Parsed:` as the very first line. The routing signal section is orchestrator metadata — it does NOT change what the writer produces. Confirm by re-reading the Output Structure section (lines 48–93) — the parse line instruction is still intact and unmodified.

**Step 3: Commit**

```bash
git add specialists/writer/index.md && git commit -m "feat: add routing hint to writer Stage 5"
```

---

## Task 4: Add Routing Hint to Competitive Analysis

**Files:**
- Modify: `specialists/competitive-analysis/index.md` (insert between lines 244 and 246)

**Current behavior (RED):** The competitive-analysis specialist has no signal telling the orchestrator what was produced or what should come next.

**Expected behavior after change:** The specialist's output format section includes a routing signal that tells the orchestrator: (1) a COMPETITIVE ANALYSIS BRIEF was produced, (2) the quality score, and (3) the natural next step is the writer.

---

**Step 1: Edit `specialists/competitive-analysis/index.md`**

Open `specialists/competitive-analysis/index.md`. Find the end of the Output Format section. Look for this exact sequence around lines 243–248:

```
No narrative prose. No explanatory paragraphs. Every line is a structured key-value record.
The Writer specialist will transform this into prose.

---

## What You Do Not Do
```

Insert the following new section AFTER "The Writer specialist will transform this into prose." (after line 244) and BEFORE the `---` separator (line 246). Replace the blank line 245 with the new section:

```markdown

---

## Routing Signal (for orchestrator use only)

When your Stage 6 output is complete, this information is available to the orchestrator:
- Produced: COMPETITIVE ANALYSIS BRIEF with comparison matrix, profiles, win conditions, and positioning gaps
- Quality: [quality_score] — [MET/NOT MET]
- Natural next step: writer (format=brief) to transform structured intelligence into a finished document

This signal is for orchestrator routing and narration only — it does not appear in your output block.

```

After the edit, the area around the insertion should read:
```
No narrative prose. No explanatory paragraphs. Every line is a structured key-value record.
The Writer specialist will transform this into prose.

---

## Routing Signal (for orchestrator use only)

When your Stage 6 output is complete, this information is available to the orchestrator:
- Produced: COMPETITIVE ANALYSIS BRIEF with comparison matrix, profiles, win conditions, and positioning gaps
- Quality: [quality_score] — [MET/NOT MET]
- Natural next step: writer (format=brief) to transform structured intelligence into a finished document

This signal is for orchestrator routing and narration only — it does not appear in your output block.

---

## What You Do Not Do
```

**Step 2: Verify output schema is unchanged**

Quick sanity check: the specialist's output must still start with `COMPETITIVE ANALYSIS BRIEF` as the very first line. Confirm by re-reading the Output Format section (lines 201–244) — the `COMPETITIVE ANALYSIS BRIEF` opening is still intact and unmodified.

**Step 3: Commit**

```bash
git add specialists/competitive-analysis/index.md && git commit -m "feat: add routing hint to competitive-analysis Stage 6"
```

---

## Task 5: Add Routing Hint to Data Analyzer

**Files:**
- Modify: `specialists/data-analyzer/index.md` (insert between lines 240 and 242)

**Current behavior (RED):** The data-analyzer has no signal telling the orchestrator what was produced or what should come next.

**Expected behavior after change:** Stage 4 includes a routing signal that tells the orchestrator: (1) an ANALYSIS OUTPUT was produced, (2) the quality score, and (3) the natural next step is the writer.

---

**Step 1: Edit `specialists/data-analyzer/index.md`**

Open `specialists/data-analyzer/index.md`. Find the end of the Stage 4 format block. Look for this exact sequence around lines 239–244:

```
QUALITY THRESHOLD RESULT: [MET | NOT MET]
Note: if any claim text contains | replace it with /
```

---

## What You Do Not Do
```

Insert the following new section AFTER the closing ``` of the Stage 4 format block (after line 240) and BEFORE the `---` separator (line 242). Replace the blank line 241 with the new section:

```markdown

---

## Routing Signal (for orchestrator use only)

When your Stage 4 output is complete, this information is available to the orchestrator:
- Produced: ANALYSIS OUTPUT with findings passthrough, labeled inferences, and unused findings
- Quality: [quality_score] — [MET/NOT MET]
- Natural next step: writer (format=brief) to transform analysis into a finished document

This signal is for orchestrator routing and narration only — it does not appear in your output block.

```

After the edit, the area around the insertion should read:
```
QUALITY THRESHOLD RESULT: [MET | NOT MET]
Note: if any claim text contains | replace it with /
```

---

## Routing Signal (for orchestrator use only)

When your Stage 4 output is complete, this information is available to the orchestrator:
- Produced: ANALYSIS OUTPUT with findings passthrough, labeled inferences, and unused findings
- Quality: [quality_score] — [MET/NOT MET]
- Natural next step: writer (format=brief) to transform analysis into a finished document

This signal is for orchestrator routing and narration only — it does not appear in your output block.

---

## What You Do Not Do
```

**Step 2: Verify output schema is unchanged**

Quick sanity check: the specialist's output must still start with `ANALYSIS OUTPUT` as the very first line. Confirm by re-reading the Stage 4 Synthesize section (lines 200–240) — the `ANALYSIS OUTPUT` opening is still intact and unmodified.

**Step 3: Commit**

```bash
git add specialists/data-analyzer/index.md && git commit -m "feat: add routing hint to data-analyzer Stage 4"
```

---

## Task 6: Add Routing Hint to Researcher Formatter

**Files:**
- Modify: `specialists/researcher-formatter/index.md` (insert between lines 118 and 120)

**Current behavior (RED):** The researcher-formatter has no signal telling the orchestrator what was produced or what should come next.

**Expected behavior after change:** Stage 2 includes a routing signal that tells the orchestrator: (1) a canonical RESEARCH OUTPUT block was produced, (2) the quality score, and (3) the natural next step is data-analyzer or writer.

---

**Step 1: Edit `specialists/researcher-formatter/index.md`**

Open `specialists/researcher-formatter/index.md`. Find the end of the Stage 2 format block. Look for this exact sequence around lines 117–122:

```
RESEARCH EVENTS:
[Condensed log of source attempts if mentioned — otherwise "not provided in input"]
```

---

## What You Do Not Do
```

Insert the following new section AFTER the closing ``` of the Stage 2 format block (after line 118) and BEFORE the `---` separator (line 120). Replace the blank line 119 with the new section:

```markdown

---

## Routing Signal (for orchestrator use only)

When your Stage 2 output is complete, this information is available to the orchestrator:
- Produced: canonical RESEARCH OUTPUT block (normalized from input format)
- Quality: [quality_score] from quality score rationale
- Natural next step: data-analyzer for inference drawing, or writer (format=brief) for direct document output

This signal is for orchestrator routing and narration only — it does not appear in your output block.

```

After the edit, the area around the insertion should read:
```
RESEARCH EVENTS:
[Condensed log of source attempts if mentioned — otherwise "not provided in input"]
```

---

## Routing Signal (for orchestrator use only)

When your Stage 2 output is complete, this information is available to the orchestrator:
- Produced: canonical RESEARCH OUTPUT block (normalized from input format)
- Quality: [quality_score] from quality score rationale
- Natural next step: data-analyzer for inference drawing, or writer (format=brief) for direct document output

This signal is for orchestrator routing and narration only — it does not appear in your output block.

---

## What You Do Not Do
```

**Step 2: Verify output schema is unchanged**

Quick sanity check: the specialist's output must still start with the parse summary line followed by `RESEARCH OUTPUT`. Confirm by re-reading Stage 2 (lines 69–118) — the `RESEARCH OUTPUT` opening is still intact and unmodified.

**Step 3: Commit**

```bash
git add specialists/researcher-formatter/index.md && git commit -m "feat: add routing hint to researcher-formatter Stage 2"
```

---

## Task 7: Full Stress Test — All 6 Scenarios

**Files:** None — this is a manual verification task.

**Prerequisite:** Tasks 1–6 must all be committed before running this.

Run each scenario below conversationally. For each one, document: (1) what you said, (2) what happened, (3) whether it matches expected behavior.

---

**Scenario 1: Clear request**

Say: "Run a competitive analysis on Notion vs Coda"

Expected:
- Orchestrator narrates: "🔍 Running competitive analysis..."
- Competitive-analysis specialist runs, produces COMPETITIVE ANALYSIS BRIEF
- Orchestrator narrates: "✅ Competitive analysis complete — passing to writer..."
- Writer runs with format=brief, produces finished brief
- Orchestrator narrates: "✍️ Done. Here's your brief."
- User sees a finished brief — NOT a raw COMPETITIVE ANALYSIS BRIEF block

---

**Scenario 2: Explicit escape hatch**

Say: "Give me the raw research output on edge AI"

Expected:
- Orchestrator recognizes "raw research output" as escape hatch (Rule 3)
- Researcher runs, produces RESEARCH OUTPUT block
- Orchestrator surfaces the raw block directly — does NOT chain to writer
- User sees the structured RESEARCH OUTPUT block

---

**Scenario 3: Previously ambiguous — now fixed**

Say: "Research edge AI for me"

Expected:
- Orchestrator reads Rule 1 — chain must complete to writer
- Narration at each step
- Researcher runs → writer runs with format=brief
- User sees a finished brief — NOT a raw RESEARCH OUTPUT block

---

**Scenario 4: No format specified — now fixed**

Say: "Research quantum computing and write something up"

Expected:
- Orchestrator reads Rule 1 — default format = brief
- Researcher runs → writer runs with format=brief
- User sees a finished brief (not a report, not a memo — brief is the default)

---

**Scenario 5: Writer request with no prior research**

Say: "Write a brief about quantum computing"

Expected:
- Orchestrator recognizes writer needs upstream research (Rule 1 — chain completion)
- Orchestrator auto-chains: researcher → writer
- User sees a finished brief

---

**Scenario 6: Analysis signal**

Say: "Research AI chip manufacturing and give me a full analysis"

Expected:
- Orchestrator reads Rule 4 — "full analysis" detected
- Routes through: researcher → data-analyzer → writer (format=brief)
- Narration at each step (three specialists announced)
- User sees a finished brief with analytical conclusions

---

**Pass criteria:** All 6 scenarios must match expected behavior. If any scenario fails, identify which rule or routing hint is at fault, fix it, re-commit, and re-run the failing scenario.

**Step: Commit (if any fixes were needed)**

```bash
git add -A && git commit -m "fix: adjust routing rules based on stress test results"
```

If all 6 passed with no fixes needed, no commit is required for this task.