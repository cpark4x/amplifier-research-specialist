# Writer Specialist Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the Writer specialist — an agent that transforms researcher output (or any structured source material) into polished prose in the requested format, and wire it into the specialists bundle.

**Architecture:** Thin agent file at `specialists/writer/index.md` following the same pattern as the Researcher. Registered in `behaviors/specialists.yaml`. Also upgrades the Researcher output schema to include a RESEARCH BRIEF section (machine-readable summary for fast downstream parsing) as agreed in the ecosystem design.

**Tech Stack:** Amplifier bundles (YAML + Markdown), specialists bundle

---

## Task 1: Upgrade Researcher output schema — add RESEARCH BRIEF section

The Writer (and all future specialists) need a fast-parse section in Researcher output. Add a RESEARCH BRIEF block between the header and FINDINGS.

**Files:**
- Modify: `specialists/researcher/index.md`

**Step 1: Find the output format block**

In `specialists/researcher/index.md`, locate the Synthesizer output format (around line 160). It currently starts with:

```
RESEARCH OUTPUT

Question: [original question]
Query Type: [type]
Quality Score: [low | medium | high]

SUB-QUESTIONS ADDRESSED:
```

**Step 2: Insert RESEARCH BRIEF section after the header block**

Replace:
```
SUB-QUESTIONS ADDRESSED:
1. [sub-question] — [high/medium/low coverage]
2. ...
```

With:
```
RESEARCH BRIEF:
[5-10 bullets — one discrete claim per bullet, URL in parentheses. Compressed for fast machine consumption. High-confidence claims only.]
- [claim] ([source URL])
- [claim] ([source URL])

SUB-QUESTIONS ADDRESSED:
1. [sub-question] — [high/medium/low coverage]
2. ...
```

**Step 3: Verify the file looks right**

```bash
grep -n "RESEARCH BRIEF\|SUB-QUESTIONS\|FINDINGS" specialists/researcher/index.md
```

Expected: RESEARCH BRIEF appears before SUB-QUESTIONS ADDRESSED, which appears before FINDINGS.

**Step 4: Commit**

```bash
git add specialists/researcher/index.md
git commit -m "feat(researcher): add RESEARCH BRIEF section for machine-readable fast-parse"
```

---

## Task 2: Create the Writer agent

**Files:**
- Create: `specialists/writer/index.md`

**Step 1: Create the file with this exact content**

```markdown
---
meta:
  name: writer
  description: |
    Writer specialist that transforms structured source material (researcher output,
    analyst output, or raw notes) into polished prose in the requested format.
    Never generates claims the source material doesn't support. Use PROACTIVELY when:
    - Turning research findings into a report, brief, or proposal
    - Drafting an executive summary from structured evidence
    - Writing an email or memo from source material
    - Any task where the substance exists but needs to be expressed clearly

    **Authoritative on:** document structure, voice and tone calibration,
    format-specific conventions (report vs brief vs email vs memo),
    coverage auditing (flagging gaps between request and source material).

    **MUST be used for:**
    - Any writing task where source material already exists
    - Transforming researcher or analyst output into human-readable documents

    <example>
    user: 'Write a brief on the Anthropic funding research'
    assistant: 'I will pass the researcher output to specialists:writer with format=brief and let it produce the document.'
    <commentary>Writer takes researcher output as input — do not write prose directly from research findings.</commentary>
    </example>
---

# Writer

You are a **senior editor and writer**. Your job is to transform structured evidence and source material into polished, reader-appropriate prose.

You do not generate new claims. You do not research. You package and articulate what the source material contains.

---

## Core Principles

**Source fidelity above all.** Every claim in your output must trace to the source material. If the source material doesn't support a claim, you do not make it — you name the gap instead.

**Format is a contract.** A brief is not a report. An email is not a memo. Each format has conventions the reader expects. You follow them precisely.

**Audience drives every decision.** Word choice, sentence length, level of detail, what to include and what to cut — all of it is determined by who is reading this, not by what the source material contains.

**Coverage gaps are first-class outputs.** If the source material cannot support the full document the user requested, you name exactly what is missing and why. You do not silently write around gaps.

---

## Pipeline

Run every writing task through these stages in order. Do not skip stages.

### Stage 1: Parse Input

1. Read the METADATA block from the source material (if present)
2. Identify input type: `researcher-output` | `analyst-output` | `raw-notes`
3. Identify requested: format, audience, voice/tone, length constraint (if any)
4. If no METADATA block: infer input type from structure and note the inference

### Stage 2: Audit Coverage

Before writing a single word:

1. Map the requested document structure to the source material
2. For each section you need to write: does the source material support it?
3. Record any gaps — sections or claims the source material cannot support
4. If gaps are critical (the document cannot be written without them): stop and surface this to the caller before proceeding

**A gap is not a reason to invent content. It is a reason to flag and proceed with what you have.**

### Stage 3: Structure

Choose the document structure for the requested format:

**Report:** Executive Summary → Background → Findings (by sub-question) → Conclusions → Recommendations → Appendix (sources)

**Brief:** Summary (3-5 sentences) → Key Points (bullets) → Implications → Next Steps

**Proposal:** Problem → Proposed Solution → Evidence → Expected Outcome → Ask

**Executive Summary:** One paragraph — situation, key findings, recommended action

**Email:** Subject → Context (1 sentence) → Key Points (3 bullets max) → Ask or FYI close

**Memo:** To/From/Date/Re header → Summary → Detail → Action items

### Stage 4: Draft

Write the document. For each claim:
- Draw directly from the RESEARCH BRIEF or FINDINGS in the source material
- Preserve confidence signals where relevant to the audience ("confirmed by multiple sources" vs "reported by a single outlet")
- Do not upgrade confidence — if the source says medium, you do not write it as certain
- Do not add interpretation beyond what the source material contains

### Stage 5: Verify

Before returning output:
1. Every factual claim in the document — can you point to it in the source material?
2. Is the coverage gap list complete and accurate?
3. Does the format match what was requested?
4. Is the voice consistent throughout?

If any check fails: revise before returning.

---

## Output Format

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

---

[DOCUMENT CONTENT]
```

---

## What You Do Not Do

- Generate claims the source material does not contain
- Skip the coverage audit to write faster
- Silently work around coverage gaps — name them
- Treat inference from the Analyst as fact — preserve the label
- Write in a format other than what was requested
- Add recommendations unless specifically asked for and supported by the source
```

**Step 2: Verify the file was created**

```bash
head -5 specialists/writer/index.md
```

Expected: `---` followed by `meta:` on the next line.

**Step 3: Commit**

```bash
git add specialists/writer/index.md
git commit -m "feat(writer): add writer specialist agent"
```

---

## Task 3: Register Writer in the specialists behavior

**Files:**
- Modify: `behaviors/specialists.yaml`

**Step 1: Read the current file**

```bash
cat behaviors/specialists.yaml
```

**Step 2: Add the writer to the agents include list**

Current `agents` section:
```yaml
agents:
  include:
    - specialists:specialists/researcher
```

Replace with:
```yaml
agents:
  include:
    - specialists:specialists/researcher
    - specialists:specialists/writer
```

**Step 3: Verify**

```bash
grep -A5 "agents:" behaviors/specialists.yaml
```

Expected: both researcher and writer listed under include.

**Step 4: Commit**

```bash
git add behaviors/specialists.yaml
git commit -m "feat(specialists): register writer agent in specialists behavior"
```

---

## Task 4: Update context instructions

The root bundle injects `context/researcher-instructions.md` into every session. This needs to cover the writer too.

**Files:**
- Modify: `context/researcher-instructions.md`
- Modify: `bundle.md` (rename context reference if file is renamed)

**Step 1: Rename the context file to cover all specialists**

```bash
mv context/researcher-instructions.md context/specialists-instructions.md
git add context/
```

**Step 2: Replace the content with**

```markdown
# Specialists: Available Agents

This bundle provides domain expert specialist agents for deep, structured work.
Delegate to these agents when quality and trustworthiness matter more than speed.

## Available Specialists

- **researcher** — Deep research with web search + fetch. Returns structured evidence
  with source tiers (primary/secondary/tertiary), per-claim confidence levels, a
  RESEARCH BRIEF for fast machine parsing, and explicit evidence gaps. Optimizes
  for trustworthiness, not speed.

- **writer** — Transforms structured source material into polished prose. Takes
  researcher output, analyst output, or raw notes and produces documents in the
  requested format (report, brief, proposal, executive summary, email, memo).
  Never generates claims the source material doesn't support.

## When to Use Each

**Delegate to `specialists:researcher` when:**
- Researching a person, company, product, or event
- Finding documentation for libraries, APIs, or frameworks
- Any research where source credibility and confidence matter

**Delegate to `specialists:writer` when:**
- Source material exists and needs to become a document
- Turning researcher output into a report, brief, or email
- Any writing task where substance already exists but needs clear expression

## Typical Chain

For most knowledge work tasks:
1. `specialists:researcher` → gathers and validates evidence
2. `specialists:writer` → transforms evidence into the requested document
```

**Step 3: Update bundle.md to reference the renamed file**

In `bundle.md`, find:
```
@specialists:context/researcher-instructions.md
```

Replace with:
```
@specialists:context/specialists-instructions.md
```

**Step 4: Update behaviors/specialists.yaml context reference**

In `behaviors/specialists.yaml`, find:
```yaml
context:
  include:
    - specialists:context/researcher-instructions.md
```

Replace with:
```yaml
context:
  include:
    - specialists:context/specialists-instructions.md
```

**Step 5: Verify no broken references remain**

```bash
grep -r "researcher-instructions" .
```

Expected: no results (all references updated).

**Step 6: Commit**

```bash
git add context/specialists-instructions.md bundle.md behaviors/specialists.yaml
git commit -m "feat(context): rename and expand context to cover all specialists"
```

---

## Task 5: Create Writer epic doc

**Files:**
- Create: `docs/02-requirements/epics/02-writer-specialist.md`

**Step 1: Create the file**

```markdown
# Epic 02: Writer Specialist

**Status:** Complete
**Specialist:** `specialists:writer`
**Depends on:** Epic 01 (Researcher) — Writer consumes Researcher output

---

## What This Enables

Orchestrators can delegate writing tasks to a specialist that:
- Takes researcher output and produces a polished document in the requested format
- Audits coverage before writing — flags what the source material cannot support
- Never adds claims beyond what the source contains
- Produces a machine-readable WRITER METADATA block for downstream consumption

## Formats Supported

Report, brief, proposal, executive summary, email, memo

## Typical Usage

```
specialists:researcher → structured evidence (RESEARCH BRIEF + FINDINGS)
        ↓
specialists:writer → polished document (WRITER METADATA + content)
```

## Output Contract

Every Writer response starts with a WRITER METADATA block:
- Input type, output format, audience, voice, word count
- Coverage: full | partial
- Coverage gaps: explicit list of what couldn't be written from source material

## What It Does Not Do

- Generate claims not in the source material
- Silently work around coverage gaps
- Research on its own
```

**Step 2: Commit**

```bash
git add docs/02-requirements/epics/02-writer-specialist.md
git commit -m "docs: add writer specialist epic"
```

---

## Task 6: Verify end-to-end

**Step 1: Check the bundle list — both agents should appear**

```bash
cd /Users/chrispark/Projects/specialists
amplifier bundle list
```

Expected: `specialists` shows as active.

**Step 2: Run a two-step test — research then write**

```bash
amplifier run "Use the researcher to find Anthropic's most recent funding round, then use the writer to produce a 200-word executive brief for a non-technical audience. Format: executive-summary."
```

Expected:
- Researcher spawns, runs pipeline, returns structured evidence with RESEARCH BRIEF
- Writer spawns, reads RESEARCH BRIEF + FINDINGS, produces WRITER METADATA block + document
- No hallucinated claims
- Coverage gaps noted if any (e.g., individual investor terms not public)

**Step 3: Verify writer metadata block is present**

Check that the output contains:
```
WRITER METADATA
Specialist: writer
...
Coverage: [full | partial]
```

**Step 4: Commit any fixes found during verification**

```bash
git add -A
git commit -m "fix(writer): address issues found during end-to-end verification"
```

---

## Task 7: Push to GitHub

```bash
git push origin main
```

Verify at: https://github.com/cpark4x/specialists

---

## Success Criteria

- [ ] `amplifier bundle list` shows `specialists` as active
- [ ] `/agents` in interactive mode shows both `researcher` and `writer`
- [ ] Researcher output includes RESEARCH BRIEF section
- [ ] Writer produces WRITER METADATA block + document in requested format
- [ ] End-to-end chain (researcher → writer) works in a single `amplifier run`
- [ ] Writer correctly flags coverage gaps when source material is incomplete
- [ ] No claims in Writer output that aren't traceable to Researcher output
