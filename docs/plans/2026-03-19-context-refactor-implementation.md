# Context Refactor Implementation Plan

> **Execution:** Use the subagent-driven-development workflow to implement this plan.

**Goal:** Refactor the specialists bundle context architecture — split the oversized monolith, eliminate wasteful specialist spawn context, pin external dependencies, and add `model_role: reasoning` to data-analyzer.

**Architecture:** Create `context/coordinator-routing.md` by taking all content from the current `specialists-instructions.md` and merging its two parallel specialist catalog sections ("Available Specialists" + "When to Use Each") into a single compact catalog. Update all references (bundle.md, behaviors/specialists.yaml, 3 test files) to point at the new file, then delete the old one. Separately, pin 3 external deps to current HEAD SHAs and add `model_role` to data-analyzer.

**Tech Stack:** Markdown context files, YAML bundle/behavior configs, pytest

**Design:** `docs/plans/2026-03-19-context-refactor-design.md`

---

## Commit Groups

| Commit | Tasks | Message |
|--------|-------|---------|
| 1 | 1–5 | `refactor: create coordinator-routing.md and update test references` |
| 2 | 6–8 | `refactor: wire coordinator-routing.md, remove specialist spawn context, delete old file` |
| 3 | 9 | `feat: add model_role reasoning to data-analyzer` |
| 4 | 10 | `chore: pin external dependencies to current HEAD SHAs` |
| — | 11 | Validation only, no commit |

---

### Task 1: Create `context/coordinator-routing.md`

**Files:**
- Create: `context/coordinator-routing.md`

This is the biggest task. You are creating one new file that replaces `context/specialists-instructions.md`. The new file takes ALL content from the old file but merges its two parallel specialist sections ("Available Specialists" lines 79–145 and "When to Use Each" lines 146–208) into a single "Available Specialists" section using a compact format. Everything else (Rules 1–8, Typical Chain, Feedback Capture) is copied verbatim. The planner specialist (listed in `behaviors/specialists.yaml` but missing from the old catalog) is added.

**Step 1: Create the file**

Create `context/coordinator-routing.md` with this exact content:

```markdown
# Specialists: Coordinator Routing

This bundle provides domain expert specialist agents for deep, structured work.
Delegate to these agents when quality and trustworthiness matter more than speed.

## Conversational Chain Behavior

**Rule 1 — Chain Completion Default**: Always complete through to the writer before responding. Default output format = `brief`. Never stop at an intermediate specialist and surface the raw structured block. The user gets a finished document. **The coordinator must never generate specialist-domain content (research, analysis, writing) itself** — delegate to the appropriate specialist whenever applicable. After the writer returns, present its output verbatim: do not summarize or rewrite it; do not add any text before `Parsed:` except the mandatory FINAL narration line placed immediately before it.

**Routing heuristic — when to chain vs. answer directly:**

| User's message is about... | Action |
|---|---|
| A factual topic, person, company, product, technology, or concept | **Depth check** (see below), then chain at the appropriate depth. |
| A comparison of two or more things | **Chain** via competitive-analysis → writer. |
| A list of items to rank or prioritize — even framed as orientation ("here's what I want to work on this week") | **Route to prioritizer.** Do not rank inline. Even casual priority lists get the Prioritizer. |
| A request for analysis, insights, investigation, or strategy | **Deep chain** via researcher → analyzer → writer (Rule 4). No depth check — analysis and strategy requests are inherently deep. |
| A request to plan, schedule, break down, or roadmap something | **Route to planner.** Goals → milestones → dependencies → risks. |
| The specialists themselves, the system, or how things work here | Answer directly. |
| A simple follow-up or clarification on a previous response | Answer directly. |
| A meta-question ("what can you do?", "how should I use this?") | Answer directly. |

**Depth check — quick vs. deep research:**

Before running the research pipeline on a factual topic, determine depth:

1. **User already indicated depth → skip the question, route immediately.**
   - **Deep signals**: "deep dive", "full research", "thorough", "sourced", "with citations", "write me a brief", "board-ready", "I need to send this to...", "research this", running the research-chain recipe explicitly
   - **Quick signals**: "quick", "brief answer", "just curious", "what is", "tell me about", "overview", "summary", "in a nutshell", "ELI5"
   - Quick → researcher → writer (2 steps, ~3-5 min, no formatters/analysis)
   - Deep → full research-chain recipe (~16 min, sourced/analyzed/hedged)

2. **Ambiguous intent → ask once, briefly:**
   > "Quick answer or deep research? Quick takes a couple minutes. Deep runs the full sourced pipeline (~15 min)."
   - Then route based on their response.

3. **Never ask twice in the same session.** If the user already chose a depth for a previous research request in this session, default to that depth for subsequent requests unless they indicate otherwise.

**When in doubt, ask.** One question before a 16-minute pipeline prevents wasted time. Err on the side of asking over assuming deep.

**Rule 2 — Per-Step Narration**: Emit narration at three points:
- **BEFORE line** *(best-effort)*: Before each specialist delegation when possible. Template: "🔍 Running <specialist>..." — Example: "🔍 Running researcher..."
- **HANDOFF line** *(mandatory)*: After each intermediate specialist returns and before delegating to the next. Template: "✅ <specialist> complete — passing to <next>..." — Example: "✅ Researcher complete — passing to writer..."
- **FINAL line** *(mandatory)*: After the last specialist returns and before presenting its output. Template: "✏️ Done. Here's your <format>." — Example: "✏️ Done. Here's your brief."

HANDOFF and FINAL lines are required and must appear. BEFORE lines are emitted when possible but are not guaranteed. Every intermediate specialist gets a HANDOFF line after it returns and before the next delegation. The last specialist gets a FINAL line after it returns, placed immediately before the specialist's output.

**No extra text between narration lines.** Do not insert commentary, explanations, or filler between narration lines and specialist delegations. The narration IS the commentary. Go directly from narration line to delegation or output.

Use these exact agent IDs when delegating: `specialists:researcher`, `specialists:data-analyzer`, `specialists:data-analyzer-formatter`, `specialists:competitive-analysis`, `specialists:writer`, `specialists:researcher-formatter`, `specialists:storyteller`, `specialists:story-formatter`, `specialists:writer-formatter`, `specialists:prioritizer`, `specialists:prioritizer-formatter`, `specialists:planner`.

**Rule 3 — Escape Hatch**: If the user explicitly says 'raw output', 'give me the raw research', 'just run the researcher', or 'don't write a document' — stop at that specialist and output the structured block as literal bare text. Your entire response IS that block. **Escape hatch overrides narration**: do NOT emit the narration lines (BEFORE, HANDOFF, FINAL). Start at byte 0 with the specialist's output block. Do NOT prepend a heading, wrap in markdown, or add any text before the block's first line. The very first characters of your response must be the very first characters of the specialist's output block.
  - Correct: `RESEARCH OUTPUT` (plain text, no markdown)
  - Wrong: `# RESEARCH OUTPUT` (markdown heading)
  - Wrong: Any narration, preamble, or explanation before the block

When delegating in escape-hatch mode, prefix the specialist instruction with `[RAW]` to signal escape-hatch mode. The coordinator suppresses all narration output for `[RAW]` delegations.

**Rule 4 — Analysis Signal**: If the user asks for 'analysis', 'insights', 'full analysis', or 'strategy' — chain through data-analyzer before writer: researcher → formatter → data-analyzer → writer. Strategy requests ("research the best strategies for X", "what's the best approach to X") inherently need fact/inference separation — route them through the analyzer chain, not researcher-only.

**Rule 5 — Formatter Is Always In The Path**: The researcher and formatter are a matched pair by design — the researcher produces trustworthy evidence, the formatter canonicalizes it into machine-parseable format. When the researcher's output feeds ANY downstream specialist (writer, data-analyzer, storyteller, competitive-analysis), **always** route through `specialists:researcher-formatter` first. This is the designed architecture, not a workaround. Skip it only if the user explicitly says 'skip formatter' or 'raw research'.

**Mandatory gate — before delegating to writer, data-analyzer, storyteller, or competitive-analysis:** If researcher ran earlier in this chain, stop and answer: "Did I route through researcher-formatter?" If the answer is no — run formatter now before proceeding. Do not continue to the next specialist until this check passes.

**Rule 6 — Writer-Formatter Is Always In The Path**: The writer and writer-formatter are a matched pair by design — the writer produces audience-calibrated prose, the writer-formatter canonicalizes it into the structured output block downstream agents depend on. When the writer's output feeds ANY downstream step or the user, **always** route through `specialists:writer-formatter` first. This is the designed architecture, not optional.

**Mandatory gate — before delivering writer output to the user or any downstream agent:** Stop and answer: "Did I route through writer-formatter?" If the answer is no — run writer-formatter now before proceeding.

**Rule 7 — Prioritizer-Formatter Is Always In The Path**: The prioritizer and prioritizer-formatter are a matched pair by design — the prioritizer produces ranked output with defensible rationale, the prioritizer-formatter canonicalizes it into the structured PRIORITY OUTPUT block downstream agents and parsers depend on. When the prioritizer's output feeds ANY downstream step or the user, **always** route through `specialists:prioritizer-formatter` first. This is the designed architecture, not optional.

**Mandatory gate — before delivering prioritizer output to the user or any downstream agent:** Stop and answer: "Did I route through prioritizer-formatter?" If the answer is no — run prioritizer-formatter now before proceeding.

**Rule 8 — Data-Analyzer-Formatter Is Always In The Path**: The data-analyzer and data-analyzer-formatter are a matched pair by design — the data-analyzer produces labeled inferences from research evidence, the data-analyzer-formatter canonicalizes it into the structured ANALYSIS OUTPUT block downstream agents and parsers depend on. When the data-analyzer's output feeds ANY downstream step or the user, **always** route through `specialists:data-analyzer-formatter` first. This is the designed architecture, not optional.

**Mandatory gate — before delivering data-analyzer output to the user or any downstream agent:** Stop and answer: "Did I route through data-analyzer-formatter?" If the answer is no — run data-analyzer-formatter now before proceeding.

The formatter is invisible to the user — do not mention it in narration unless the user asks about the pipeline. HANDOFF narration should say "✅ Research complete — normalizing format..." (not "passing to formatter").

## Available Specialists

- **researcher** — Deep research with web search + fetch. Produces trustworthy evidence with source tiers (primary/secondary/tertiary), per-claim confidence assessments, and explicit evidence gaps. Optimizes for trustworthiness, not speed. Output format varies — always route through researcher-formatter before downstream specialists. **Use when:** researching a person, company, product, or event; finding documentation for libraries, APIs, or frameworks; any research where source credibility and confidence matter.

- **writer** — Transforms structured source material into polished prose. Takes researcher output, analyst output, or raw notes and produces documents in the requested format (report, brief, proposal, executive summary, email, memo). Never generates claims the source material doesn't support. **Use when:** source material exists and needs to become a document; turning researcher output into a report, brief, or email; any writing task where substance already exists but needs clear expression.

- **competitive-analysis** — Transforms a question or existing research into structured competitive intelligence. Returns a machine-parseable `CompetitiveAnalysisOutput` with comparison matrices, positioning gaps, and win conditions. Handles head-to-head and landscape modes. Output is designed for downstream agents (Writer) to consume. **Use when:** comparing two or more companies, products, or services head-to-head; mapping the competitive landscape for a subject; you need structured comparison data, not a narrative summary; source material from the Researcher needs to be structured into competitive intelligence.

- **data-analyzer** — Draws labeled inferences from ResearchOutput. Returns `AnalysisOutput` — findings projected from ResearchOutput plus explicit inferences that each trace to specific findings. Input must be canonical `ResearchOutput` from the Researcher — not raw notes or narrative summaries. **Use when:** you have ResearchOutput and need conclusions drawn before writing; you want facts and inferences explicitly separated and labeled; the Writer needs more than raw findings — it needs "what the evidence means"; any Researcher → Analyzer → Writer chain.

- **data-analyzer-formatter** — Essential pipeline stage. Receives data-analyzer output in any format (canonical ANALYSIS OUTPUT block, partial block, narrative prose/essay) plus the original research input and produces a canonical ANALYSIS OUTPUT block. Handles stage narration leaks and all three DA output failure modes. Never re-analyzes, never draws inferences — only extracts, validates, and reformats. **Use when:** always after the data-analyzer — mandatory pipeline stage (Rule 8); data-analyzer output is missing the `ANALYSIS OUTPUT` structured block; stage narration is visible in data-analyzer output.

- **researcher-formatter** — Essential pipeline stage. Receives researcher output in any format and produces a canonical RESEARCH OUTPUT block. Validates confidence labels, tier names, and URL format. Never researches, never analyzes — only extracts, validates, and reformats. **Use when:** always after the researcher — mandatory pipeline stage (Rule 5).

- **storyteller** — Transforms research, analysis, or existing documents into compelling narrative using cognitive mode translation. Returns StoryOutput with a clean story, NARRATIVE SELECTION editorial record, and framework/tone metadata. Selects load-bearing findings for the arc — the Writer covers everything, the Storyteller selects. **Use when:** source material needs to become a compelling narrative rather than a structured document; the audience needs to be moved or persuaded, not just informed; you want narrative output instead of document output at the end of a chain.

- **story-formatter** — Essential pipeline stage. Receives storyteller output in any format and produces a canonical STORY OUTPUT block. Classifies which findings from the original input appear in the narrative prose and assigns each a narrative role. Never generates new story content — only extracts, classifies, and reformats. **Use when:** always after the storyteller — mandatory pipeline stage; storyteller output needs to be wrapped in canonical STORY OUTPUT structure; NARRATIVE SELECTION record is missing from storyteller output.

- **writer-formatter** — Essential pipeline stage. Receives writer output in any format plus the original source material and produces a canonical Writer output block with all required structural elements: Parsed: line, S-numbered claims, document prose, CLAIMS TO VERIFY, WRITER METADATA, and CITATIONS. Never rewrites prose — only extracts, wraps, and normalizes. **Use when:** always after the writer — mandatory pipeline stage (Rule 6); writer output is missing Parsed:, WRITER METADATA, CITATIONS, or CLAIMS TO VERIFY blocks.

- **prioritizer** — Ranking specialist that takes a list of items and produces a `PrioritizerOutput` with every item ranked using an explicit framework (MoSCoW, impact-effort, RICE, or weighted scoring), with 2–3 sentence rationale per item traceable to the context provided. Unrankable items listed explicitly. **Use when:** the user has a list of items and needs a ranked, justified order; backlog grooming, roadmap planning, feature triage, vendor selection; any situation where "what should we do first?" needs visible reasoning; the user needs to present or defend a prioritization to a stakeholder.

- **prioritizer-formatter** — Essential pipeline stage. Receives prioritizer output in any format (structured PRIORITY OUTPUT block, markdown prose, numbered list, ranked table) plus the original items list and produces a canonical PRIORITY OUTPUT block. Never re-ranks or re-scores — only extracts, normalizes, and reformats. **Use when:** always after the prioritizer — mandatory pipeline stage (Rule 7); prioritizer output is missing the `PRIORITY OUTPUT` structured block.

- **planner** — Planning specialist that transforms goals and context into structured plans with milestones, dependencies, timelines, and risk flags. **Use when:** the user needs to plan, schedule, break down, or roadmap something; going from goals to a structured plan with visible reasoning.

## Typical Chain

For most knowledge work tasks:
1. `specialists:researcher` → gathers and validates evidence
2. `specialists:researcher-formatter` → normalizes to canonical format (Rule 5 — always)
3. `specialists:writer` → transforms evidence into the requested document
4. `specialists:writer-formatter` → normalizes to canonical Writer output block (Rule 6 — always)

For analytical tasks requiring explicit fact/inference separation:
1. `specialists:researcher` → gathers and validates evidence
2. `specialists:researcher-formatter` → normalizes to canonical format (Rule 5 — always)
3. `specialists:data-analyzer` → draws labeled inferences from the evidence
4. `specialists:data-analyzer-formatter` → normalizes to canonical ANALYSIS OUTPUT block (Rule 8 — always)
5. `specialists:writer` → transforms facts + labeled inferences into the requested document
6. `specialists:writer-formatter` → normalizes to canonical Writer output block (Rule 6 — always)

For competitive intelligence tasks:
1. `specialists:researcher` → gathers evidence (optional — competitive-analysis can research itself)
2. `specialists:researcher-formatter` → normalizes to canonical format (Rule 5 — when researcher is used)
3. `specialists:competitive-analysis` → structures evidence into competitive intelligence
4. `specialists:writer` → transforms competitive intelligence into a brief or report

For narrative output from a research chain:
1. `specialists:researcher` → gathers and validates evidence
2. `specialists:researcher-formatter` → normalizes to canonical RESEARCH OUTPUT block
3. `specialists:data-analyzer` → draws labeled inferences
4. `specialists:data-analyzer-formatter` → normalizes to canonical ANALYSIS OUTPUT block (Rule 8 — always)
5. `specialists:storyteller` → transforms analysis into compelling narrative
6. `specialists:story-formatter` → normalizes to canonical STORY OUTPUT block

For prioritization tasks:
1. `specialists:prioritizer` → ranks items using explicit framework with per-item rationale
2. `specialists:prioritizer-formatter` → normalizes to canonical PRIORITY OUTPUT block (Rule 7 — always)
3. `specialists:writer` → (optional) transforms ranked output into a recommendation brief

## Feedback Capture

After a specialist chain completes, offer once to capture a test log entry:
> "Want to log this run? I can capture what worked, any concerns, and route action items to the backlog."

For the full procedure, load the `feedback-capture` skill.
```

**Step 2: Verify the file was created correctly**

Run: `head -5 context/coordinator-routing.md && echo "---" && wc -l context/coordinator-routing.md`

Expected: First line is `# Specialists: Coordinator Routing`, file is approximately 160–175 lines.

---

### Task 2: Update `tests/conftest.py`

**Files:**
- Modify: `tests/conftest.py` (line 26)

The `SPECIALISTS_INSTRUCTIONS` constant points at the old file. Rename the constant to `COORDINATOR_ROUTING` and point it at the new file. No test file imports this constant (verified by grep), so the rename is safe.

**Step 1: Edit the constant**

In `tests/conftest.py`, change line 26 from:

```python
SPECIALISTS_INSTRUCTIONS = REPO_ROOT / "context" / "specialists-instructions.md"
```

to:

```python
COORDINATOR_ROUTING = REPO_ROOT / "context" / "coordinator-routing.md"
```

**Step 2: Verify the edit**

Run: `grep -n "COORDINATOR_ROUTING\|SPECIALISTS_INSTRUCTIONS" tests/conftest.py`

Expected: One line showing `COORDINATOR_ROUTING = REPO_ROOT / "context" / "coordinator-routing.md"`. No line showing `SPECIALISTS_INSTRUCTIONS`.

---

### Task 3: Update `tests/test_specialists_instructions_storyteller.py`

**Files:**
- Modify: `tests/test_specialists_instructions_storyteller.py` (lines 2, 10–12, and test at line 88)

This file has three things to update:
1. The docstring references the old filename
2. The `INSTRUCTIONS_PATH` constant points at the old file
3. The test `test_delegate_storyteller_appears_after_competitive_analysis_block` (line 88) searches for `**Delegate to \`specialists:competitive-analysis\`` and `**Delegate to \`specialists:storyteller\`` — these "Delegate to" headings from the old "When to Use Each" section no longer exist in the merged catalog format

**Step 1: Update the module docstring**

Change lines 1–4 from:

```python
"""
TDD tests for task-05: Register storyteller in context/specialists-instructions.md.
Validates that all 3 required additions are present in the file.
"""
```

to:

```python
"""
TDD tests for task-05: Register storyteller in context/coordinator-routing.md.
Validates that all 3 required additions are present in the file.
"""
```

**Step 2: Update the path constant**

Change lines 10–12 from:

```python
INSTRUCTIONS_PATH = (
    Path(__file__).parent.parent / "context" / "specialists-instructions.md"
)
```

to:

```python
INSTRUCTIONS_PATH = (
    Path(__file__).parent.parent / "context" / "coordinator-routing.md"
)
```

**Step 3: Update the section comment for Addition (2)**

Change lines 59–61 from:

```python
# ---------------------------------------------------------------------------
# Addition (2): 'Delegate to storyteller when' block in ## When to Use Each
# ---------------------------------------------------------------------------
```

to:

```python
# ---------------------------------------------------------------------------
# Addition (2): storyteller usage triggers in ## Available Specialists (merged)
# ---------------------------------------------------------------------------
```

**Step 4: Update `test_delegate_storyteller_appears_after_competitive_analysis_block`**

The old "When to Use Each" section had separate `**Delegate to \`specialists:...\`` headings. The merged catalog uses `**name**` entries instead. Change lines 88–97 from:

```python
def test_delegate_storyteller_appears_after_competitive_analysis_block() -> None:
    """Delegate-to-storyteller block must appear after the competitive-analysis block."""
    content = load_content()
    ca_pos = content.find("**Delegate to `specialists:competitive-analysis`")
    st_pos = content.find("**Delegate to `specialists:storyteller`")
    assert ca_pos != -1, "competitive-analysis delegate block must exist"
    assert st_pos != -1, "storyteller delegate block must exist"
    assert st_pos > ca_pos, (
        "storyteller delegate block must appear after competitive-analysis block"
    )
```

to:

```python
def test_delegate_storyteller_appears_after_competitive_analysis_block() -> None:
    """Storyteller entry must appear after the competitive-analysis entry."""
    content = load_content()
    ca_pos = content.find("**competitive-analysis**")
    st_pos = content.find("**storyteller**")
    assert ca_pos != -1, "competitive-analysis entry must exist"
    assert st_pos != -1, "storyteller entry must exist"
    assert st_pos > ca_pos, (
        "storyteller entry must appear after competitive-analysis entry"
    )
```

**Step 5: Verify all edits**

Run: `grep -n "specialists-instructions\|When to Use Each\|Delegate to .specialists:" tests/test_specialists_instructions_storyteller.py`

Expected: No matches. All old references are gone.

---

### Task 4: Update `tests/test_conversational_chain_behavior.py`

**Files:**
- Modify: `tests/test_conversational_chain_behavior.py` (lines 5, 12–14)

**Step 1: Update the module docstring**

Change line 5 from:

```python
context/specialists-instructions.md.
```

to:

```python
context/coordinator-routing.md.
```

**Step 2: Update the path constant**

Change lines 12–14 from:

```python
INSTRUCTIONS_PATH = (
    Path(__file__).parent.parent / "context" / "specialists-instructions.md"
)
```

to:

```python
INSTRUCTIONS_PATH = (
    Path(__file__).parent.parent / "context" / "coordinator-routing.md"
)
```

**Step 3: Verify all edits**

Run: `grep -n "specialists-instructions" tests/test_conversational_chain_behavior.py`

Expected: No matches.

---

### Task 5: Run test suite to verify tests pass against new file

**Files:** None (verification only)

Both the old file (`context/specialists-instructions.md`) and new file (`context/coordinator-routing.md`) exist on disk right now. The tests now point at the new file. Run the full test suite to verify the merged content passes all existing tests.

**Step 1: Run the two updated test files**

Run: `cd /Users/chrispark/Projects/specialists/canvas-specialists && python -m pytest tests/test_specialists_instructions_storyteller.py tests/test_conversational_chain_behavior.py -v`

Expected: All tests PASS. If any fail, fix the content in `coordinator-routing.md` — do NOT change the test assertions (they validate real requirements).

**Step 2: Run the full test suite**

Run: `cd /Users/chrispark/Projects/specialists/canvas-specialists && python -m pytest tests/ -v`

Expected: All tests PASS. No regressions.

**Step 3: Do NOT commit yet — wait until after Task 5 passes**

If all tests pass, commit Tasks 1–5 together:

Run:
```bash
cd /Users/chrispark/Projects/specialists/canvas-specialists && \
git add context/coordinator-routing.md tests/conftest.py tests/test_specialists_instructions_storyteller.py tests/test_conversational_chain_behavior.py && \
git commit -m "refactor: create coordinator-routing.md and update test references"
```

Expected: Clean commit with 4 files changed.

---

### Task 6: Update `bundle.md` body reference

**Files:**
- Modify: `bundle.md` (line 16)

**Step 1: Swap the @mention**

In `bundle.md`, change line 16 from:

```
@specialists:context/specialists-instructions.md
```

to:

```
@specialists:context/coordinator-routing.md
```

**Step 2: Verify the edit**

Run: `cat bundle.md`

Expected: Line 16 reads `@specialists:context/coordinator-routing.md`. Line 15 still reads `@specialists:context/session-startup.md`.

---

### Task 7: Remove `context.include` from `behaviors/specialists.yaml`

**Files:**
- Modify: `behaviors/specialists.yaml` (lines 40–42)

The `context.include` section injects the coordinator routing file into every spawned specialist — that's waste. Remove it entirely.

**Step 1: Delete the context section**

In `behaviors/specialists.yaml`, delete lines 40–42:

```yaml
context:
  include:
    - specialists:context/specialists-instructions.md
```

The file should now end at line 39 (the `exclude_tools` line under `spawn:`).

**Step 2: Verify the edit**

Run: `cat behaviors/specialists.yaml`

Expected: File ends with:
```yaml
spawn:
  exclude_tools: [write_file, edit_file, apply_patch]
```

No `context:` section anywhere.

---

### Task 8: Delete `context/specialists-instructions.md`

**Files:**
- Delete: `context/specialists-instructions.md`

All references have been updated (bundle.md, behaviors/specialists.yaml, 3 test files). Safe to delete.

**Step 1: Delete the file**

Run: `rm context/specialists-instructions.md`

**Step 2: Verify it's gone**

Run: `ls context/`

Expected: `coordinator-routing.md` and `session-startup.md` are present. `specialists-instructions.md` is gone.

**Step 3: Run tests to confirm nothing breaks**

Run: `cd /Users/chrispark/Projects/specialists/canvas-specialists && python -m pytest tests/test_specialists_instructions_storyteller.py tests/test_conversational_chain_behavior.py -v`

Expected: All tests PASS (they point at coordinator-routing.md now).

**Step 4: Commit Tasks 6–8 together**

Run:
```bash
cd /Users/chrispark/Projects/specialists/canvas-specialists && \
git add bundle.md behaviors/specialists.yaml && \
git rm context/specialists-instructions.md && \
git commit -m "refactor: wire coordinator-routing.md, remove specialist spawn context, delete old file"
```

Expected: Clean commit — 2 files modified, 1 file deleted.

---

### Task 9: Add `model_role: reasoning` to `agents/data-analyzer.md`

**Files:**
- Modify: `agents/data-analyzer.md` (frontmatter, after the `description:` block)

The data-analyzer is the most analytically demanding agent (416 lines, labeled inference work, fact/inference separation) but has no `model_role` override. The simpler planner (87 lines) already has `model_role: reasoning`. Fix this.

**Step 1: Add model_role to frontmatter**

In `agents/data-analyzer.md`, the frontmatter currently looks like this (abbreviated):

```yaml
---
meta:
  name: data-analyzer
  description: |
    Inference specialist that draws labeled analytical conclusions from ResearchOutput.
    ...
    </example>
---
```

Add `model_role: reasoning` on a new line immediately before the closing `---`. The frontmatter closing `---` is on the line right after the last `</example>` closing. Find the last line before `---` and add `model_role: reasoning` between it and the `---`.

The result should look like (showing just the end of the frontmatter):

```yaml
    assistant: 'I will delegate to specialists:data-analyzer with the ResearchOutput to draw labeled inferences.'
    </example>
model_role: reasoning
---
```

Note: `model_role` is at the top level of the frontmatter (same indentation as `meta:`), NOT nested inside `meta:`. This matches the pattern in `agents/planner.md` where `model_role: reasoning` appears at line 22 at the top level.

**Step 2: Verify the edit**

Run: `head -25 agents/data-analyzer.md`

Expected: You see `model_role: reasoning` on its own line, at column 1 (no indentation), somewhere between the `description` block and the closing `---`.

**Step 3: Commit**

Run:
```bash
cd /Users/chrispark/Projects/specialists/canvas-specialists && \
git add agents/data-analyzer.md && \
git commit -m "feat: add model_role reasoning to data-analyzer"
```

---

### Task 10: Pin external dependencies to current HEAD SHAs

**Files:**
- Modify: `bundle.md` (lines 8, 10)
- Modify: `behaviors/specialists.yaml` (line 8)

Three external dependencies currently reference `@main`, creating exposure to unintentional breaking changes. Pin each to its current HEAD SHA.

**Step 1: Get current HEAD SHAs**

Run all three commands:

```bash
git ls-remote https://github.com/microsoft/amplifier-foundation.git refs/heads/main
git ls-remote https://github.com/cpark4x/amplifier-doc-driven-dev.git refs/heads/main
git ls-remote https://github.com/microsoft/amplifier-module-tool-web.git refs/heads/main
```

Record the full 40-character SHA from each output. At the time this plan was written, they were:
- amplifier-foundation: `1d26e9be0ca7c1e9939a5531f2d4d5485c72fea3`
- amplifier-doc-driven-dev: `dda74c522c7fb7bd092f440fdd5ca656b61a1423`
- amplifier-module-tool-web: `26b6d9030ed0d6c21a4d3a2f77cf59ce99a7cece`

**Use the SHAs you just fetched, not these cached values** — they may have changed since plan creation.

**Step 2: Pin `bundle.md` includes**

In `bundle.md`, change line 8 from:

```yaml
  - bundle: git+https://github.com/microsoft/amplifier-foundation@main
```

to (using YOUR fetched SHA):

```yaml
  - bundle: git+https://github.com/microsoft/amplifier-foundation@1d26e9be0ca7c1e9939a5531f2d4d5485c72fea3
```

Change line 10 from:

```yaml
  - bundle: git+https://github.com/cpark4x/amplifier-doc-driven-dev@main
```

to (using YOUR fetched SHA):

```yaml
  - bundle: git+https://github.com/cpark4x/amplifier-doc-driven-dev@dda74c522c7fb7bd092f440fdd5ca656b61a1423
```

**Step 3: Pin `behaviors/specialists.yaml` tool source**

In `behaviors/specialists.yaml`, change line 8 from:

```yaml
    source: git+https://github.com/microsoft/amplifier-module-tool-web@main
```

to (using YOUR fetched SHA):

```yaml
    source: git+https://github.com/microsoft/amplifier-module-tool-web@26b6d9030ed0d6c21a4d3a2f77cf59ce99a7cece
```

**Step 4: Verify no `@main` references remain**

Run: `grep "@main" bundle.md behaviors/specialists.yaml`

Expected: No output. All three `@main` references are replaced.

**Step 5: Commit**

Run:
```bash
cd /Users/chrispark/Projects/specialists/canvas-specialists && \
git add bundle.md behaviors/specialists.yaml && \
git commit -m "chore: pin external dependencies to current HEAD SHAs"
```

---

### Task 11: Final validation

**Files:** None (verification only). No commit.

**Step 1: Run full test suite**

Run: `cd /Users/chrispark/Projects/specialists/canvas-specialists && python -m pytest tests/ -v`

Expected: All tests PASS.

**Step 2: Verify coordinator-routing.md is under 4,000 tokens**

Run: `wc -w context/coordinator-routing.md`

Expected: Word count is approximately 2,200–2,600 words. At ~0.75 words/token for English prose, this corresponds to roughly 2,900–3,500 tokens — well under the 4,000-token guideline.

**Step 3: Verify no stale references to the deleted file in source files**

Run: `grep -r "specialists-instructions" bundle.md behaviors/specialists.yaml tests/conftest.py tests/test_specialists_instructions_storyteller.py tests/test_conversational_chain_behavior.py`

Expected: No output. All five source/test files are clean.

**Step 4: Verify git log shows 4 clean commits**

Run: `git log --oneline -4`

Expected (newest first):
```
<sha> chore: pin external dependencies to current HEAD SHAs
<sha> feat: add model_role reasoning to data-analyzer
<sha> refactor: wire coordinator-routing.md, remove specialist spawn context, delete old file
<sha> refactor: create coordinator-routing.md and update test references
```

**Step 5: Verify specialist spawn context is gone**

Run: `grep -A5 "context:" behaviors/specialists.yaml`

Expected: No output. The `context:` section was removed entirely.

---

## Deferred

- **`docs/adding-a-specialist.md`** references `context/specialists-instructions.md` in 4 places — this is a living contributor guide that should be updated in a follow-up to reference `coordinator-routing.md` and the merged catalog format. Not in scope for this refactor.
- **`session-startup.md` dev-session gating** — explicitly deferred in design to a future refactor.
