# Researcher–Formatter Architecture Refactor — Implementation Plan

> **Execution:** Use the subagent-driven-development workflow to implement this plan.

**Goal:** Strip format enforcement from the researcher (which demonstrably doesn't work after 4 independent test runs), promote the formatter to an essential pipeline stage, and align all surrounding infrastructure.

**Architecture:** The researcher and formatter become a matched pair. The researcher focuses exclusively on evidence quality (finding sources, tiering them, assessing confidence, identifying gaps). The formatter focuses exclusively on canonicalizing that evidence into the machine-parseable RESEARCH OUTPUT block. This replaces the current architecture where the researcher tries to do both jobs and fails at formatting 100% of the time.

**Tech Stack:** Markdown specialist prompts (Amplifier bundle), YAML recipe definitions, TypeScript interface documentation.

---

## Background

The researcher specialist prompt is 393 lines. Approximately 150 of those lines (~39%) are format enforcement instructions: an OUTPUT CONTRACT, a Stage 0 "write RESEARCH OUTPUT right now" command, a rigid Stage 7 template, a COMPLIANCE NOTE, a FINAL SELF-CHECK, and wrong/right examples. Six separate layers of "please format your output this way."

**All six layers fail.** Across 4 independent test runs on 3 different topics, the researcher has NEVER produced canonical RESEARCH OUTPUT format. It always produces narrative markdown documents with numeric confidence values (0.97 instead of "high"), markdown headers, abbreviated tier labels (T1/T2/T3), and prose sections instead of structured FINDINGS blocks.

**Root cause:** The researcher does 10-20+ tool calls (web_search, web_fetch) between reading the format spec and producing output. By synthesis time, the format instructions are overwhelmed by thousands of tokens of narrative content from web sources. The Writer works because its cognitive flow aligns with its format. The Researcher fails because its format contradicts its cognitive flow.

**The fix:** Accept that "research" and "format" are two different cognitive tasks. The researcher-formatter specialist already exists — it was built on March 3 as an "architectural mitigation." This refactor promotes it from mitigation to designed architecture.

---

## File Inventory

Every file this plan touches, with its role:

| File | Lines | Role in This Plan |
|---|---|---|
| `specialists/researcher/index.md` | 393 | **PRIMARY TARGET.** Strip ~150 lines of format enforcement, add ~15 lines of output expectations. |
| `specialists/researcher-formatter/index.md` | 140 | Add validation rules (numeric→categorical confidence, abbreviated→full tiers), remove pass-through logic. |
| `context/specialists-instructions.md` | 146 | Reframe Rule 5 from apologetic ("format is inconsistent") to intentional ("matched pair by design"). Update specialist descriptions. |
| `recipes/research-chain.yaml` | 86 | Update research step prompt to stop asking for format compliance. |
| `shared/interface/types.md` | 257 | Add comment clarifying downstream consumers depend on formatter output. |
| `docs/01-vision/SUCCESS-METRICS.md` | 295 | Split V1 metrics: researcher = evidence quality, formatter = format compliance. Add Formatter Metrics section. |
| `docs/01-vision/SCORECARD.md` | 108 | Update after validation test. |
| `docs/BACKLOG.md` | 274 | Mark #22 as shipped with architectural reframe. |
| `docs/test-log/chains/2026-03-06-architecture-refactor-validation.md` | new | Capture validation test results. |

---

## Phase 1: Researcher Prompt Refactoring

**What this phase does:** Remove all format enforcement from the researcher. Replace it with a short output expectations section that says "focus on evidence quality, the formatter handles format." Keep all research quality content untouched.

**Commit message:** `refactor: strip format enforcement from researcher — formatter handles format`

---

### Task 1: Read the researcher file

**Files:**
- Read: `specialists/researcher/index.md`

**Step 1: Read the full file**

Read `specialists/researcher/index.md` from top to bottom. Understand the structure:

| Section | Lines | Keep or Remove? |
|---|---|---|
| YAML frontmatter | 1–25 | KEEP (unchanged) |
| Title + identity paragraph | 27–31 | MODIFY (update identity) |
| OUTPUT CONTRACT block | 35–41 | **REMOVE** (format enforcement) |
| Core Principles | 44–53 | KEEP (research quality) |
| Research Pipeline intro | 56–58 | KEEP |
| Stage 0: Open your response | 60–80 | **REMOVE** (format enforcement) |
| Stage 1: Planner | 82–91 | KEEP |
| Stage 2: Source Discoverer | 92–131 | KEEP |
| Stage 3: Fetcher | 132–146 | KEEP (URL requirement is data quality) |
| Stage 4: Extractor | 148–173 | MODIFY (keep extraction, remove format template) |
| Stage 5: Corroborator | 175–185 | KEEP |
| Stage 6: Quality Gate | 187–201 | KEEP |
| Stage 7: Synthesizer | 203–257 | **REPLACE** with short output expectations |
| COMPLIANCE NOTE | 259–280 | **REMOVE** (format enforcement) |
| FINAL SELF-CHECK | 282–290 | **REMOVE** (format enforcement) |
| Wrong/right examples | 292–339 | **REMOVE** (format enforcement) |
| Routing Signal | 343–350 | MODIFY (update to reflect formatter) |
| Source Tiers Reference | 354–361 | KEEP |
| Confidence Levels Reference | 364–371 | KEEP |
| What You Do Not Do | 374–382 | MODIFY (one line) |
| On Indirect Social Sources | 386–393 | KEEP |

No file changes in this task. Proceed to Task 2.

---

### Task 2: Remove OUTPUT CONTRACT block

**Files:**
- Modify: `specialists/researcher/index.md`

**Step 1: Remove the OUTPUT CONTRACT**

Find this exact text (it spans two `---` separators with the OUTPUT CONTRACT between them):

```
---

> **OUTPUT CONTRACT — read before Stage 1:**
> Your entire response is a single structured block that begins with `RESEARCH OUTPUT` on
> the very first line. There is no surrounding document, no title, no markdown headers,
> no executive summary before or after it. The literal string `RESEARCH OUTPUT` is the
> first thing in your response. Your Stage 7 output IS your complete response — nothing
> wraps it. See Stage 7 for the exact format and compliance rules.

---
```

Replace with just the single separator:

```
---
```

**Why:** This block pre-committed the model to a rigid output format before any research began. It didn't work — the model ignored it after 10+ tool calls. The formatter now owns format compliance.

---

### Task 3: Remove Stage 0

**Files:**
- Modify: `specialists/researcher/index.md`

**Step 1: Delete Stage 0 entirely**

Find the text that starts with `### Stage 0: Open your response` and ends just before `### Stage 1: Planner`. Delete all of Stage 0, leaving Stage 1 as the first pipeline stage.

Specifically, find this text:

```
### Stage 0: Open your response

**Do this before any research.** Write the following right now as the first lines of your response — not at the end, not after thinking, right now:
```

Delete everything from `### Stage 0: Open your response` through the line that ends with `Proceed to Stage 1.` and the blank line that follows it. Keep `### Stage 1: Planner` and everything after it.

The result should be that immediately after the Research Pipeline intro (`You run every research task through these stages in order. Do not skip stages.`), the next heading is `### Stage 1: Planner`.

**Why:** Stage 0 asked the model to write `RESEARCH OUTPUT` as its literal first output before doing any research. The model never complied. The formatter now produces this opening.

---

### Task 4: Simplify Stage 4 extractor

**Files:**
- Modify: `specialists/researcher/index.md`

**Step 1: Replace Stage 4 extraction instructions**

Find this text (starts after the "One claim per finding." line in Stage 4):

```
For each claim, write it directly in FINDINGS block format as you extract it — not as prose first, formatted later. Each extracted claim becomes one entry in your final FINDINGS section:
```

And everything after it through the end of the format enforcement rules (ending with the code block containing `Note: financial figure — single source, independent corroboration required`).

Replace ALL of that content (from "For each claim, write it directly..." through the closing of the `Note:` code block) with:

```
For each claim, capture:
- The specific, falsifiable claim (not a vague summary)
- The source URL (full `https://` — a publication name is not a URL)
- The source tier (primary / secondary / tertiary)
- Your confidence assessment (high / medium / low)
- Whether it's a direct quote
- Publication date if known

**Data quality rules:**
- If you cannot recover the source URL, that source is inaccessible — log it in evidence gaps, do not extract claims from it.
- Numeric and financial claims (dollar amounts, percentages, revenue figures) get `low` confidence unless backed by a primary source or 2+ independent secondary sources.

Do not synthesize at this stage. Only extract.
```

**What stays:** The Stage 4 header (`### Stage 4: Extractor`) and the first instruction (`From each successfully fetched source, extract discrete claims. One claim per finding.`).

**What's removed:** The rigid `Claim:` / `Source:` / `Tier:` / `Confidence:` format template, the "Format enforcement rules" block, and all three format enforcement bullet points.

**What's kept as data quality:** URL requirement (data quality, not format) and financial claims special handling (research quality, not format).

**Why:** The format template told the model to produce findings in a rigid key-value format. The model never did. Data quality rules (URL capture, financial claim caution) stay because they affect evidence quality, not just output formatting.

---

### Task 5: Replace Stage 7 and strip compliance enforcement

**Files:**
- Modify: `specialists/researcher/index.md`

This is the biggest single edit. You are replacing ~135 lines with ~15 lines.

**Step 1: Identify the section to replace**

Find the text starting with `### Stage 7: Synthesizer` and ending just before the `---` separator that precedes `## Routing Signal (for orchestrator use only)`. This section includes:
- Stage 7: Synthesizer (the full template block)
- COMPLIANCE NOTE
- FINAL SELF-CHECK
- All wrong/right examples (narrative format, numeric confidence, abbreviated tiers)

**Step 2: Replace the entire section**

Delete everything from `### Stage 7: Synthesizer` through the last wrong/right example's closing code fence. Replace with:

```
### Stage 7: Synthesize and Return

Assemble your findings into a complete research output. Include all of the following:

1. The original research question and query type
2. A research brief — your highest-confidence findings as compact bullets with source URLs
3. Which sub-questions you addressed and to what coverage level
4. All findings with their source URLs, tiers, confidence levels, and corroboration counts
5. All evidence gaps with what you attempted
6. Your quality score rationale
7. Quality threshold result (MET / NOT MET)
8. Follow-up questions that would most improve confidence

**Do not worry about exact output formatting.** The downstream formatter specialist will canonicalize your output into the machine-parseable format the pipeline requires. Focus on completeness and accuracy of the evidence, not on matching a rigid template.
```

**Verify after this edit:** The section flow should now be:
- `### Stage 6: Quality Gate` → (existing content) → `### Stage 7: Synthesize and Return` → (new 15-line content) → `---` → `## Routing Signal`

There should be NO remaining `COMPLIANCE NOTE`, `FINAL SELF-CHECK`, or `Wrong —` / `Right —` example blocks anywhere in the file.

**Why:** All ~135 lines of format enforcement (template, compliance note, self-check, examples) demonstrably didn't work across 4 test runs. The new section tells the model what content to include but lets the formatter handle the exact structure.

---

### Task 6: Update identity and minor sections

**Files:**
- Modify: `specialists/researcher/index.md`

Three small edits to align the rest of the file with the new architecture.

**Step 1: Update the identity paragraph**

Find:

```
You are a **senior research analyst**. Your job is to return trustworthy structured evidence — not answers, not narratives, not reports.

You do not write the article. You fill the evidence brief.
```

Replace with:

```
You are a **senior research analyst**. Your job is to produce trustworthy, source-tiered evidence — not opinions, not recommendations, not speculation.

Every finding traces to a source. Every confidence assessment is justified. Every gap is named. The downstream formatter specialist handles output formatting — your job is evidence quality.
```

**Why:** The old identity said "not narratives" — but we now allow the model to produce narrative-style output since the formatter canonicalizes it. The new identity focuses on evidence quality, which is the researcher's actual job.

**Step 2: Update the Routing Signal section**

Find:

```
When your Stage 7 output is complete, this information is available to the orchestrator:
- Produced: RESEARCH OUTPUT block with sourced findings
- Quality: [quality_score] — [MET/NOT MET]
- Natural next step: writer (format=brief) or data-analyzer → writer if analysis was requested
```

Replace with:

```
When your research output is complete, this information is available to the orchestrator:
- Produced: research evidence with sourced findings, tiered sources, and confidence assessments
- Quality: [quality_score] — [MET/NOT MET]
- Natural next step: researcher-formatter → writer (format=brief), or researcher-formatter → data-analyzer → writer
```

**Why:** The routing signal now reflects that the formatter is always the next step, and the output is "research evidence" not a "RESEARCH OUTPUT block."

**Step 3: Update "What You Do Not Do"**

Find:

```
- Write prose, narratives, reports, or articles — that is the Writer specialist's job
```

Replace with:

```
- Write polished documents, reports, or articles — that is the Writer specialist's job
```

**Why:** "not narratives" conflicts with letting the model output naturally. The real boundary is "don't write the final document" — the Writer does that.

---

### Task 7: Verify researcher refactoring

**Files:**
- Read: `specialists/researcher/index.md` (verify edits)

**Step 1: Verify removed content is gone**

Run these searches against `specialists/researcher/index.md`. Each should return **zero matches**:

```bash
grep -c "OUTPUT CONTRACT" specialists/researcher/index.md
grep -c "Stage 0" specialists/researcher/index.md
grep -c "COMPLIANCE NOTE" specialists/researcher/index.md
grep -c "FINAL SELF-CHECK" specialists/researcher/index.md
grep -c "MOST COMMON MISTAKE" specialists/researcher/index.md
grep -c "Format enforcement rules" specialists/researcher/index.md
```

Expected: all return `0`.

**Step 2: Verify kept content is present**

Run these searches. Each should return **at least one match**:

```bash
grep -c "Stage 1: Planner" specialists/researcher/index.md
grep -c "Stage 2: Source Discoverer" specialists/researcher/index.md
grep -c "Stage 3: Fetcher" specialists/researcher/index.md
grep -c "Stage 4: Extractor" specialists/researcher/index.md
grep -c "Stage 5: Corroborator" specialists/researcher/index.md
grep -c "Stage 6: Quality Gate" specialists/researcher/index.md
grep -c "Stage 7: Synthesize and Return" specialists/researcher/index.md
grep -c "Source Tiers" specialists/researcher/index.md
grep -c "Confidence Levels" specialists/researcher/index.md
grep -c "Do not worry about exact output formatting" specialists/researcher/index.md
```

Expected: all return `1`.

**Step 3: Verify file length**

```bash
wc -l specialists/researcher/index.md
```

Expected: approximately 240–260 lines (down from 393). If it's still above 300 or below 200, something went wrong — re-read the file and check.

**Step 4: Run the researcher on a test topic**

Delegate to `specialists:specialists/researcher` with this prompt:

```
Research the following question thoroughly. Follow your full research pipeline.
Focus on finding trustworthy evidence with source tiering and confidence
assessments. Do not worry about output format — the formatter handles that.

Research question: What is Jina AI?

Quality threshold: medium
```

**What to check in the output (pass/fail criteria):**

| Criterion | Pass | Fail |
|---|---|---|
| Contains findings with sources | Discrete claims with URLs | No sources cited |
| Contains confidence reasoning | Some form of confidence assessment per finding | No confidence mentioned |
| Contains evidence gaps | At least one gap named | No gaps section |
| Does NOT contain "FINAL SELF-CHECK" | Absent | Present (old content leaked) |
| Does NOT contain "COMPLIANCE NOTE" | Absent | Present (old content leaked) |

**Important:** The output format does NOT matter for this check. Narrative markdown is fine. Structured blocks are fine. Tables are fine. The researcher's job is now evidence quality, not format. The formatter (Phase 2) handles format.

---

### Task 8: Commit Phase 1

**Step 1: Stage and commit**

```bash
git add specialists/researcher/index.md
git commit -m "refactor: strip format enforcement from researcher — formatter handles format"
```

Do NOT push yet. We push after all 4 phases.

---

## Phase 2: Formatter Promotion

**What this phase does:** Upgrade the formatter from "cleanup step that sometimes passes through" to "essential pipeline stage that always validates and normalizes." Add the validation rules the researcher used to own (categorical confidence, full tier labels, URL validation).

**Commit message:** `refactor: promote formatter to essential pipeline stage with validation rules`

---

### Task 9: Update formatter identity and description

**Files:**
- Read: `specialists/researcher-formatter/index.md`
- Modify: `specialists/researcher-formatter/index.md`

**Step 1: Read the full formatter file**

Read `specialists/researcher-formatter/index.md` top to bottom. It's 140 lines — small file.

**Step 2: Update the YAML frontmatter description**

Find:

```
  description: |
    Format conversion specialist. Receives raw research narrative (in any format)
    and produces a canonical RESEARCH OUTPUT block. Never researches, never
    analyzes, never invents — only extracts and reformats.

    Use AFTER the researcher specialist when canonical block format is required
    for machine parsing or downstream pipeline steps. The researcher produces
    excellent content; this specialist ensures it arrives in the format downstream
    agents and parsers depend on.

    Input: any research narrative — canonical RESEARCH OUTPUT block (Format A)
           or structured narrative markdown with inline citations (Format B)
    Output: canonical RESEARCH OUTPUT block, always
```

Replace with:

```
  description: |
    Essential pipeline stage — always runs after the researcher. Receives
    researcher output in any format and produces a canonical RESEARCH OUTPUT
    block. Validates confidence labels, tier names, and URL format. Never
    researches, never analyzes, never invents — only extracts, validates,
    and reformats.

    The researcher focuses on evidence quality. This specialist focuses on
    ensuring that evidence arrives in the exact format downstream agents
    and parsers depend on. These are two different cognitive tasks.

    Input: researcher output in any format (narrative markdown, structured
           sections, mixed formats)
    Output: canonical RESEARCH OUTPUT block, always
```

**Why:** The old description said "Use AFTER the researcher when canonical format is required" — framing it as optional. The new description says "always runs after the researcher" — framing it as essential architecture.

**Step 3: Update the identity paragraph**

Find:

```
You are a **format conversion specialist**. Your only job is to receive research
narrative and produce a canonical RESEARCH OUTPUT block.

You do not research. You do not analyze. You do not add information that isn't
in the input. You only extract and reformat.
```

Replace with:

```
You are the **format normalization stage** of the research pipeline. Every researcher
output passes through you before reaching any downstream specialist. Your job is to
receive researcher evidence and produce a canonical RESEARCH OUTPUT block — validated,
normalized, and ready for machine parsing.

You do not research. You do not analyze. You do not add information that isn't
in the input. You extract, validate, and reformat.
```

**Why:** "format conversion specialist" sounds optional. "format normalization stage of the research pipeline" sounds essential. The word "validate" is added because the formatter now owns validation of confidence labels, tier names, and URLs.

---

### Task 10: Add validation rules to formatter

**Files:**
- Modify: `specialists/researcher-formatter/index.md`

**Step 1: Replace the Core Principle section**

Find the entire Core Principle section, starting with `## Core Principle` and ending just before the `---` that precedes `## Pipeline`:

```
## Core Principle

**Extract, don't invent.**

- If a source URL is not in the input, mark it `unknown`
- If confidence is not explicitly stated, infer from language: "primary research" →
  high, "reportedly" / "some sources suggest" → low, most else → medium
- If a finding already has a source tier label, preserve it; otherwise infer:
  academic paper / direct research publication → primary,
  credible third-party reporting / surveys → secondary,
  blog posts / forums / indirect → tertiary
- If a field cannot be determined, mark it explicitly rather than omitting it

If the input is already a canonical RESEARCH OUTPUT block, pass it through
with only the minimum corrections needed for compliance. Do not rewrite good
content.
```

Replace with:

```
## Core Principle

**Extract, don't invent. Normalize everything.**

Every input — regardless of how well-formatted it appears — gets the full normalization pass. There is no pass-through mode. The researcher produces excellent evidence; your job is to ensure it arrives in canonical format every time.

**Validation rules (apply to every finding):**

- **Confidence must be categorical:** `high`, `medium`, or `low` — nothing else.
  - If the input uses numeric confidence (e.g., 0.97, 0.85): map it — >=0.8 → `high`, 0.5–0.79 → `medium`, <0.5 → `low`
  - If confidence is not explicitly stated: infer from language — "primary research" → high, "reportedly" / "some sources suggest" → low, most else → medium
  - `unrated` is never valid. If confidence cannot be determined, assign `low`.
- **Tier must be a full label:** `primary`, `secondary`, or `tertiary` — nothing else.
  - If the input uses abbreviations (T1, T2, T3, Tier 1, etc.): normalize — T1/Tier 1 → `primary`, T2/Tier 2 → `secondary`, T3/Tier 3 → `tertiary`
  - If no tier label is present: infer — academic paper / official publication → primary, credible third-party reporting → secondary, blog posts / forums / indirect → tertiary
- **Source must be a full `https://` URL or explicitly `unknown`.** A publication name is not a URL.
- If a field cannot be determined, mark it explicitly rather than omitting it
```

**What changed:**
1. **Pass-through logic removed.** The old version said "If the input is already canonical, pass it through." The new version says "Every input gets the full normalization pass. There is no pass-through mode."
2. **Numeric confidence mapping added.** The researcher consistently outputs values like 0.97. The formatter now has an explicit mapping: >=0.8 → high, 0.5–0.79 → medium, <0.5 → low.
3. **Abbreviated tier normalization added.** The researcher outputs T1/T2/T3. The formatter now normalizes these to primary/secondary/tertiary.
4. **`unrated` ban added.** Moved from the researcher's Core Principles to here — the formatter is the last line of defense.
5. **URL validation explicit.** Publication names are not URLs.

---

### Task 11: Verify formatter normalization

**Files:**
- Read: `specialists/researcher-formatter/index.md` (verify edits)

**Step 1: Verify edits**

Run these searches against `specialists/researcher-formatter/index.md`:

```bash
# Should be GONE:
grep -c "pass it through" specialists/researcher-formatter/index.md
# Expected: 0

# Should be PRESENT:
grep -c "no pass-through mode" specialists/researcher-formatter/index.md
# Expected: 1

grep -c "Confidence must be categorical" specialists/researcher-formatter/index.md
# Expected: 1

grep -c "Tier must be a full label" specialists/researcher-formatter/index.md
# Expected: 1

grep -c "0.97" specialists/researcher-formatter/index.md
# Expected: 1 (in the numeric mapping rule)
```

**Step 2: Run the formatter on researcher output**

Take the researcher output from Task 7 Step 4 (the "What is Jina AI?" run). Pass it to the formatter.

Delegate to `specialists:specialists/researcher-formatter` with this prompt:

```
Normalize the following research narrative into your canonical RESEARCH OUTPUT
block format. Apply all standard formatting rules: structured sections, source
tiering, per-claim confidence scores, and gap flags.

Research narrative to format:
[paste the FULL output from the Task 7 researcher run here]
```

**What to check in the formatter output (pass/fail criteria):**

| Criterion | Pass | Fail |
|---|---|---|
| Starts with `Parsed:` line | `Parsed: N claims \| format=...` | Missing parse summary |
| Contains `RESEARCH OUTPUT` | Plain text, not markdown header | `# RESEARCH OUTPUT` or missing |
| FINDINGS use structured blocks | `- Claim:` / `Source:` / `Tier:` / `Confidence:` per finding | Narrative sections |
| Confidence is categorical | Every value is `high`, `medium`, or `low` | Any numeric value (0.97) or `unrated` |
| Tiers are full labels | `primary`, `secondary`, `tertiary` | `T1`, `T2`, `T3`, `Tier 1` |
| Sources are URLs or `unknown` | `https://...` or `unknown` | Publication names without URL |
| EVIDENCE GAPS section present | At least the section header exists | Missing |

**This is the critical validation.** The formatter must produce canonical output from the researcher's natural narrative. If it doesn't, the architecture doesn't work and we need to debug the formatter before proceeding.

---

### Task 12: Commit Phase 2

**Step 1: Stage and commit**

```bash
git add specialists/researcher-formatter/index.md
git commit -m "refactor: promote formatter to essential pipeline stage with validation rules"
```

Do NOT push yet.

---

## Phase 3: Infrastructure Alignment

**What this phase does:** Update all surrounding files that reference the researcher/formatter relationship. Reframe the coordinator's Rule 5, update the recipe prompt, clarify types.md, and split SUCCESS-METRICS.md into researcher quality vs formatter compliance.

**Commit message:** `refactor: align infrastructure with researcher-formatter architecture`

---

### Task 13: Update coordinator instructions

**Files:**
- Read: `context/specialists-instructions.md`
- Modify: `context/specialists-instructions.md`

**Step 1: Reframe Rule 5**

Find:

```
**Rule 5 — Formatter Is Always In The Path**: When the researcher's output feeds ANY downstream specialist (writer, data-analyzer, storyteller, competitive-analysis), **always** route through `specialists:specialists/researcher-formatter` first. The researcher produces excellent content but its format is inconsistent (~1 in 3 topics produces canonical output). The formatter normalizes it in seconds. This is not optional — skip it only if the user explicitly says 'skip formatter' or 'raw research'.

**Mandatory gate — before delegating to writer, data-analyzer, storyteller, or competitive-analysis:** If researcher ran earlier in this chain, stop and answer: "Did I route through researcher-formatter?" If the answer is no — run formatter now before proceeding. Do not continue to the next specialist until this check passes. Skipping formatter means ~1 in 3 runs the downstream specialist receives non-canonical input and parsing fails silently.
```

Replace with:

```
**Rule 5 — Formatter Is Always In The Path**: The researcher and formatter are a matched pair by design — the researcher produces trustworthy evidence, the formatter canonicalizes it into machine-parseable format. When the researcher's output feeds ANY downstream specialist (writer, data-analyzer, storyteller, competitive-analysis), **always** route through `specialists:specialists/researcher-formatter` first. This is the designed architecture, not a workaround. Skip it only if the user explicitly says 'skip formatter' or 'raw research'.

**Mandatory gate — before delegating to writer, data-analyzer, storyteller, or competitive-analysis:** If researcher ran earlier in this chain, stop and answer: "Did I route through researcher-formatter?" If the answer is no — run formatter now before proceeding. Do not continue to the next specialist until this check passes.
```

**What changed:**
- Removed "its format is inconsistent (~1 in 3 topics produces canonical output)" — old apologetic framing.
- Added "matched pair by design" — new intentional framing.
- Removed "Skipping formatter means ~1 in 3 runs..." — old apologetic framing.
- The mandatory gate stays exactly as-is (it works).

**Step 2: Update researcher description in Available Specialists**

Find:

```
- **researcher** — Deep research with web search + fetch. Returns structured evidence
  with source tiers (primary/secondary/tertiary), per-claim confidence levels, a
  RESEARCH BRIEF for fast machine parsing, and explicit evidence gaps. Optimizes
  for trustworthiness, not speed.
```

Replace with:

```
- **researcher** — Deep research with web search + fetch. Produces trustworthy evidence
  with source tiers (primary/secondary/tertiary), per-claim confidence assessments,
  and explicit evidence gaps. Optimizes for trustworthiness, not speed. Output format
  varies — always route through researcher-formatter before downstream specialists.
```

**Why:** The old description implied the researcher "returns structured evidence" in a specific format. The new description is honest: "Output format varies."

**Step 3: Update formatter description in Available Specialists**

Find:

```
- **researcher-formatter** — Format conversion specialist. Receives raw research
  narrative in any format (canonical RESEARCH OUTPUT block or narrative markdown
  with inline citations) and produces a canonical RESEARCH OUTPUT block. Use after
  the researcher when guaranteed canonical format is required for machine parsing
  or downstream pipeline steps. Never researches, never analyzes — only extracts
  and reformats.
```

Replace with:

```
- **researcher-formatter** — Essential pipeline stage. Receives researcher output
  in any format and produces a canonical RESEARCH OUTPUT block. Always runs after
  the researcher — this is the designed architecture, not optional. Validates
  confidence labels, tier names, and URL format. Never researches, never
  analyzes — only extracts, validates, and reformats.
```

**Why:** "Format conversion specialist" and "Use after the researcher when canonical format is required" framed it as optional. "Essential pipeline stage" and "Always runs after the researcher" frame it as required.

---

### Task 14: Update recipe prompt

**Files:**
- Read: `recipes/research-chain.yaml`
- Modify: `recipes/research-chain.yaml`

**Step 1: Update the research step prompt**

Find:

```
    prompt: |
      Research the following question thoroughly. Follow your full research pipeline
      and return your complete research narrative with sourced evidence, confidence
      scores, and source tiering.

      Research question: {{research_question}}

      Quality threshold: {{quality_threshold}}
```

Replace with:

```
    prompt: |
      Research the following question thoroughly. Follow your full research pipeline.
      Focus on finding trustworthy evidence with source tiering and confidence
      assessments. Do not worry about output format — the formatter handles that.

      Research question: {{research_question}}

      Quality threshold: {{quality_threshold}}
```

**What changed:** Removed "return your complete research narrative with sourced evidence, confidence scores, and source tiering" (which implicitly asks for a specific format). Added "Do not worry about output format — the formatter handles that" (which explicitly tells the model to focus on evidence, not format).

---

### Task 15: Update types.md and SUCCESS-METRICS.md

**Files:**
- Read: `shared/interface/types.md`
- Read: `docs/01-vision/SUCCESS-METRICS.md`
- Modify: `shared/interface/types.md`
- Modify: `docs/01-vision/SUCCESS-METRICS.md`

**Step 1: Update ResearchOutput description in types.md**

Find:

```
## ResearchOutput

The canonical output of the Researcher specialist.
```

Replace with:

```
## ResearchOutput

The canonical output of the research pipeline (Researcher → Formatter). The Researcher
produces evidence in whatever format is natural for the research task; the Formatter
normalizes it into this schema. Downstream consumers depend on formatter output, not
raw researcher output.
```

**Why:** types.md is the contract documentation. Downstream specialists read this to understand what they'll receive. It now clearly states the formatter produces the canonical output, not the researcher directly.

**Step 2: Update V1 Composability metrics in SUCCESS-METRICS.md**

Find:

```
**Composability:**
- ResearchOutput passes to Writer without preprocessing
- Schema version has not needed a breaking change
```

Replace with:

```
**Composability:**
- Researcher → Formatter → Writer chain produces canonical output without manual intervention
- Formatter successfully normalizes researcher output on every run
- Schema version has not needed a breaking change
```

**Why:** "passes to Writer without preprocessing" was aspirational — the formatter IS the preprocessing step. The new metric honestly describes the architecture.

**Step 3: Add Formatter Metrics section to SUCCESS-METRICS.md**

Find the `---` separator between the V1 section and V2 section. The V1 section ends with the "Red flags" list. Look for this transition:

```
- "It returned findings but I couldn't tell where they came from"

---

## V2 Metrics: Writing Quality
```

Replace with:

```
- "It returned findings but I couldn't tell where they came from"

---

## Formatter Metrics

**Phase Goal:** Validate that the Formatter reliably converts any researcher output into canonical ResearchOutput format — the essential bridge between research and all downstream specialists.

### Leading Indicators

**Format compliance:**
- Every finding in formatter output uses categorical confidence (high/medium/low — never numeric)
- Every finding uses full tier labels (primary/secondary/tertiary — never abbreviated)
- Every source field is a full `https://` URL or explicitly marked `unknown`

**Normalization reliability:**
- Formatter produces canonical RESEARCH OUTPUT block on every run regardless of researcher output format
- Zero claims lost during format conversion (input claim count = output claim count)

### Lagging Indicators

**Pipeline trust:**
- Downstream specialists (Writer, Data Analyzer) never receive non-canonical input
- Zero parsing failures in Writer or Data Analyzer traced to format issues

---

## V2 Metrics: Writing Quality
```

**Step 4: Update V1 Success Criteria heading in SUCCESS-METRICS.md**

Find:

```
### V1 Success = Researcher Is Trustworthy

**Must achieve:**
- Every finding is sourced, tiered, and confidence-rated
- Evidence gaps are always disclosed, never omitted
- ResearchOutput schema is stable (no breaking changes needed after v1.0)
```

Replace with:

```
### V1 Success = Research Pipeline Is Trustworthy

**Must achieve:**
- Every finding is sourced, tiered, and confidence-rated (validated via formatter output)
- Evidence gaps are always disclosed, never omitted
- ResearchOutput schema is stable (no breaking changes needed after v1.0)
- Formatter normalizes researcher output to canonical format on every run
```

**Why:** V1 success is about the pipeline, not just the researcher. The formatter is now part of the V1 success criteria.

---

### Task 16: Verify infrastructure alignment

**Step 1: Sanity-check all modified files**

Read each modified file and confirm the edits look correct:

```bash
# Coordinator: "matched pair by design" should be present, "~1 in 3" should be gone
grep "matched pair" context/specialists-instructions.md
grep "1 in 3" context/specialists-instructions.md

# Recipe: "Do not worry about output format" should be present
grep "Do not worry about output format" recipes/research-chain.yaml

# Types: "Researcher → Formatter" should be present
grep "Researcher → Formatter" shared/interface/types.md

# Metrics: "Formatter Metrics" section should exist
grep "## Formatter Metrics" docs/01-vision/SUCCESS-METRICS.md

# Metrics: "Research Pipeline Is Trustworthy" should replace "Researcher Is Trustworthy"
grep "Research Pipeline Is Trustworthy" docs/01-vision/SUCCESS-METRICS.md
```

Expected: all `grep` commands return matches. The `grep "1 in 3"` should return zero matches.

---

### Task 17: Commit Phase 3

**Step 1: Stage and commit**

```bash
git add context/specialists-instructions.md recipes/research-chain.yaml shared/interface/types.md docs/01-vision/SUCCESS-METRICS.md
git commit -m "refactor: align infrastructure with researcher-formatter architecture"
```

Do NOT push yet.

---

## Phase 4: Validation

**What this phase does:** Run a full chain test (researcher → formatter → writer brief), capture results in a test log, update the scorecard and backlog to reflect the architectural reframe.

**Commit message:** `test: validate researcher-formatter architecture refactor — #22 shipped`

---

### Task 18: Run full chain test

Run three sequential delegations to test the full pipeline. Use "What is Jina AI?" as the test topic (same as the Session 1 validation for comparability).

**Step 1: Run the researcher**

Delegate to `specialists:specialists/researcher` with:

```
Research the following question thoroughly. Follow your full research pipeline.
Focus on finding trustworthy evidence with source tiering and confidence
assessments. Do not worry about output format — the formatter handles that.

Research question: What is Jina AI?

Quality threshold: medium
```

Save the full output — you'll need it for Step 2.

**Step 2: Run the formatter on that output**

Delegate to `specialists:specialists/researcher-formatter` with:

```
Normalize the following research narrative into your canonical RESEARCH OUTPUT
block format. Apply all standard formatting rules: structured sections, source
tiering, per-claim confidence scores, and gap flags.

Research narrative to format:
[paste the FULL researcher output from Step 1 here]
```

Save the full output — you'll need it for Step 3.

**Check the formatter output against these criteria:**

| Criterion | Pass | Fail |
|---|---|---|
| Opens with `RESEARCH OUTPUT` (plain text) | Yes | Missing or markdown header |
| FINDINGS use `Claim:` / `Source:` / `Tier:` / `Confidence:` blocks | Yes | Narrative sections |
| All confidence values are `high`, `medium`, or `low` | Yes | Any numeric (0.97) or `unrated` |
| All tier values are `primary`, `secondary`, or `tertiary` | Yes | Any T1/T2/T3 or abbreviated |
| All sources are `https://` URLs or `unknown` | Yes | Publication names |
| EVIDENCE GAPS section present | Yes | Missing |
| Zero claims invented (not in researcher output) | Yes | New claims appear |

**Step 3: Run the writer on formatter output**

Delegate to `specialists:specialists/writer` with:

```
Transform the following research output into a polished document. Follow your full
writing pipeline and return WRITER METADATA, the document body with section
attribution lines, CITATIONS, and CLAIMS TO VERIFY blocks.

Research output:
[paste the FULL formatter output from Step 2 here]

Output format: brief
Audience: technical decision-maker
Voice: executive
```

**Check the writer output against these criteria:**

| Criterion | Pass | Fail |
|---|---|---|
| Starts with `Parsed:` line | Yes | Missing |
| Word count 250–400 | Yes | Over 400 or under 200 |
| Brief structure (Summary → Key Points → sections) | Yes | Report-length narrative |
| CITATIONS block present | Yes | Missing |
| Source references trace to formatter findings | Yes | Invented sources |

---

### Task 19: Capture test log

**Files:**
- Create: `docs/test-log/chains/2026-03-06-architecture-refactor-validation.md`

**Step 1: Write the test log**

Create the file with this structure (fill in actual results from Task 18):

```markdown
---
specialist: researcher
chain: "researcher → researcher-formatter → writer"
topic: jina-ai-architecture-refactor
date: 2026-03-06
quality_signal: pass  # or mixed or fail — based on actual results
action_items_promoted: false
---

# Test Log: Researcher-Formatter Architecture Refactor Validation

**Date:** 2026-03-06
**Type:** Architecture validation — testing refactored researcher (format enforcement removed) + promoted formatter (validation rules added)
**Chain:** researcher → researcher-formatter → writer (format=brief)
**Topic:** What is Jina AI?

## What Worked

[Fill in based on actual results. Look for:]
- Did the researcher produce evidence with sources and confidence reasoning?
- Did the formatter successfully normalize the output to canonical format?
- Did the writer produce a brief within word budget?
- Did confidence values end up categorical (high/medium/low) after formatter?
- Did tier labels end up full (primary/secondary/tertiary) after formatter?

## What Didn't / Concerns

[Fill in based on actual results. Look for:]
- Any claims lost between researcher → formatter?
- Any confidence values still numeric after formatter?
- Any tier labels still abbreviated after formatter?
- Writer word count outside budget?
- Any evidence gaps silently dropped?

## Confidence Accuracy

[Fill in: Did the confidence levels in the final output feel calibrated? Were high-confidence claims actually well-sourced? Were low-confidence claims appropriately cautious?]

## Coverage Assessment

[Fill in: Did the researcher find the key facts about Jina AI? Compare against the Session 1 run on the same topic. Better, worse, or same coverage?]

## Action Items

[Fill in based on findings. Route per docs/test-log/README.md:]
- Consistent quality gap → docs/BACKLOG.md
- Edge case in one specialist → docs/02-requirements/epics/
- Confidence systematically off → specialists/{specialist}/index.md
```

---

### Task 20: Update scorecard and backlog

**Files:**
- Read: `docs/01-vision/SCORECARD.md`
- Read: `docs/BACKLOG.md`
- Modify: `docs/01-vision/SCORECARD.md`
- Modify: `docs/BACKLOG.md`

**Step 1: Update the scorecard Current State**

Based on the Task 18 test results, update the scores in `docs/01-vision/SCORECARD.md`.

**If the formatter successfully canonicalized the output (all validation criteria pass):**
- Research Trustworthiness: 3 → 5 *(validated)* — evidence quality good, formatter canonicalizes
- Chain Reliability: 4 → 5 *(validated)* — researcher→formatter→writer chain works end-to-end
- Format Fidelity: 5 → 5 (no change)
- Specialist Coverage: 4 → 4 (no change)
- Overall: 4.0 → 4.8 *(validated)*

**If the formatter did NOT successfully canonicalize (some criteria fail):**
- Scores stay the same or adjust down. Be honest — the spec/validated distinction exists for this.

Update the `*As of*` date and status labels (replace `*(spec)*` with `*(validated)*` where test evidence supports it).

Add a new row to the Session Log table:

```
| 2026-03-06 | Session 2 | **Shipped:** #22 architectural reframe — stripped ~150 lines of format enforcement from researcher, promoted formatter to essential pipeline stage with validation rules (numeric→categorical confidence, T1→primary tier normalization, URL validation), aligned coordinator/recipe/types/metrics. **Validated:** [fill in actual results]. | [fill in dimension deltas] | [fill in new overall] |
```

**Step 2: Update the backlog**

In `docs/BACKLOG.md`, move #22 from Immediate Next to Recently Completed.

Find the #22 entry in the Immediate Next table and remove it from there.

Add this row to the Recently Completed table (adjust based on actual test results):

```
| Researcher-Formatter architecture refactor | 01 | Chris | Mar 6, 2026 | Backlog #22. Architectural reframe: stripped ~150 lines of format enforcement from researcher (OUTPUT CONTRACT, Stage 0, Stage 7 template, COMPLIANCE NOTE, SELF-CHECK, wrong/right examples). Added short output expectations section. Promoted formatter from optional cleanup to essential pipeline stage with validation rules (numeric→categorical confidence mapping, T1→primary tier normalization, URL validation, removed pass-through mode). Updated coordinator Rule 5, recipe prompt, types.md, SUCCESS-METRICS.md. Root cause: format enforcement doesn't work after 10-20+ tool calls of narrative research context. Solution: accept researcher produces evidence, formatter produces format — two different cognitive tasks. |
```

Add a new Change History entry:

```
| v2.9 | Mar 6, 2026 | Chris | Shipped #22 as architectural reframe — researcher stripped to evidence-only, formatter promoted to essential pipeline stage with validation rules. Moved to Recently Completed. Immediate Next is now empty. |
```

---

### Task 21: Commit and push

**Step 1: Stage and commit**

```bash
git add docs/test-log/chains/2026-03-06-architecture-refactor-validation.md docs/01-vision/SCORECARD.md docs/BACKLOG.md
git commit -m "test: validate researcher-formatter architecture refactor — #22 shipped"
```

**Step 2: Push all 4 phases**

```bash
git push origin main
```

**Step 3: Verify push**

```bash
git log --oneline -5
```

Expected: 4 new commits on main, all pushed:
1. `refactor: strip format enforcement from researcher — formatter handles format`
2. `refactor: promote formatter to essential pipeline stage with validation rules`
3. `refactor: align infrastructure with researcher-formatter architecture`
4. `test: validate researcher-formatter architecture refactor — #22 shipped`

---

## Summary

| Phase | Commit | Files Changed | What Happens |
|---|---|---|---|
| **1. Researcher** | `refactor: strip format enforcement...` | `specialists/researcher/index.md` | Remove ~150 lines of format enforcement, add ~15 lines of output expectations |
| **2. Formatter** | `refactor: promote formatter...` | `specialists/researcher-formatter/index.md` | Add validation rules, remove pass-through, reframe identity |
| **3. Infrastructure** | `refactor: align infrastructure...` | `context/specialists-instructions.md`, `recipes/research-chain.yaml`, `shared/interface/types.md`, `docs/01-vision/SUCCESS-METRICS.md` | Align all references to new architecture |
| **4. Validation** | `test: validate...` | `docs/test-log/chains/...`, `docs/01-vision/SCORECARD.md`, `docs/BACKLOG.md` | Run chain test, capture results, update tracking |

**Estimated total time:** 60–90 minutes across 21 tasks.

**The core insight this plan implements:** Research and formatting are two fundamentally different cognitive tasks. After 4 test runs proving prompt-based format enforcement doesn't survive contact with 10-20+ tool calls of web research, we stop fighting the model and let each specialist do one thing exceptionally well.