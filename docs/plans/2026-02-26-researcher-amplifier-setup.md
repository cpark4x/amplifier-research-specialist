# Researcher Specialist — Amplifier Setup Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Wire the Researcher specialist as a working Amplifier agent so it can be run with `amplifier run` and invoked from any orchestrator.

**Architecture:** Thin root bundle inherits from foundation, composes a `specialists` behavior that declares `tool-web` (web search + fetch) and registers the researcher agent. The researcher's `index.md` acts as a context sink — heavy instructions load only when the agent is spawned.

**Tech Stack:** Amplifier bundles (YAML + Markdown), `tool-web` module, `amplifier-foundation`

---

## Task 1: Add .gitignore

**Files:**
- Create: `.gitignore`

**Step 1: Create the file**

```
.amplifier/settings.local.yaml
.amplifier/cache/
*.local.yaml
```

**Step 2: Commit**

```bash
cd /Users/chrispark/Projects/specialists
git add .gitignore
git commit -m "chore: add gitignore for local Amplifier config"
```

---

## Task 2: Create Amplifier project settings

**Files:**
- Create: `.amplifier/settings.yaml`
- Create: `.amplifier/settings.local.yaml` (gitignored — never commit)

**Step 1: Create .amplifier/settings.yaml**

```yaml
bundle: specialists
```

**Step 2: Create .amplifier/settings.local.yaml**

```yaml
# Local API key — never commit
providers:
  - module: provider-anthropic
    config:
      api_key: ${ANTHROPIC_API_KEY}
```

**Step 3: Commit settings.yaml only**

```bash
cd /Users/chrispark/Projects/specialists
git add .amplifier/settings.yaml
git commit -m "chore: add Amplifier project settings"
```

---

## Task 3: Create the specialists behavior

**Files:**
- Create: `behaviors/specialists.yaml`

**Step 1: Create the file**

```yaml
bundle:
  name: specialists-behavior
  version: 1.0.0
  description: Adds researcher specialist with web capabilities

tools:
  - module: tool-web
    source: git+https://github.com/microsoft/amplifier-module-tool-web@main

agents:
  include:
    - specialists:specialists/researcher

context:
  include:
    - specialists:context/researcher-instructions.md
```

Note: `tool-web` provides both `web_search` and `web_fetch` — one declaration, both tools.

**Step 2: Commit**

```bash
cd /Users/chrispark/Projects/specialists
git add behaviors/specialists.yaml
git commit -m "feat: add specialists behavior with tool-web and researcher agent"
```

---

## Task 4: Create researcher context instructions

**Files:**
- Create: `context/researcher-instructions.md`

**Step 1: Create the file**

```markdown
# Specialists: Research Capabilities

This bundle provides the **researcher** specialist agent for deep,
structured web research with source tiering and confidence-rated evidence.

## Available Specialists

- **researcher** — Deep research with web search + fetch. Returns
  structured evidence with source tiers (primary/secondary/tertiary),
  per-claim confidence levels, and explicit evidence gaps. Optimizes
  for trustworthiness, not speed.

## When to Use the Researcher

Delegate to `specialists:researcher` when:
- Researching a person, company, product, or event
- Finding documentation for libraries, APIs, or frameworks
- Researching best practices with evidence from authoritative sources
- Any research where source credibility and confidence matter
```

**Step 2: Commit**

```bash
cd /Users/chrispark/Projects/specialists
git add context/researcher-instructions.md
git commit -m "feat: add researcher context instructions"
```

---

## Task 5: Create the root bundle

**Files:**
- Create: `bundle.md`

**Step 1: Create the file**

```markdown
---
bundle:
  name: specialists
  version: 1.0.0
  description: Domain expert specialist agents — independent of any UI

includes:
  - bundle: git+https://github.com/microsoft/amplifier-foundation@main
  - bundle: specialists:behaviors/specialists
---

# Specialists

@specialists:context/researcher-instructions.md
```

**Step 2: Commit**

```bash
cd /Users/chrispark/Projects/specialists
git add bundle.md
git commit -m "feat: add root specialists bundle"
```

---

## Task 6: Update researcher index.md agent description

**Files:**
- Modify: `specialists/researcher/index.md`

The current `index.md` has deep instructions but needs the `meta.description`
updated to match the Amplifier orchestrator pattern — this is what orchestrators
read to decide when to delegate to this agent.

**Step 1: Replace the `meta:` frontmatter section with:**

```yaml
---
meta:
  name: researcher
  description: |
    Deep research specialist that returns structured, source-tiered evidence
    with per-claim confidence ratings and explicit evidence gaps. Optimizes
    for trustworthiness over speed. Use PROACTIVELY when:
    - Researching a person, company, product, or event
    - Finding documentation for libraries, APIs, or frameworks
    - Multi-source synthesis where source credibility matters
    - Any research where "what sources support this?" matters

    **Authoritative on:** web research, source tiering, confidence
    calibration, evidence gap analysis, multi-round search loops.

    **MUST be used for:**
    - Any research task where source quality and confidence matter
    - Competitive analysis, market research, fact-checking

    <example>
    user: 'Research recent updates from Sam Altman'
    assistant: 'I will delegate to specialists:researcher to search authoritative sources and return structured findings with citations.'
    <commentary>Multi-angle research with source quality requirements.</commentary>
    </example>
---
```

Keep all existing instructions below the frontmatter unchanged.

**Step 2: Commit**

```bash
cd /Users/chrispark/Projects/specialists
git add specialists/researcher/index.md
git commit -m "feat(researcher): update agent description for Amplifier orchestrator pattern"
```

---

## Task 7: Verify setup and run first test

**Step 1: Verify Amplifier is installed**

```bash
amplifier --version
```

If not installed: check Amplifier installation docs.

**Step 2: Register the bundle**

```bash
cd /Users/chrispark/Projects/specialists
amplifier bundle add ./bundle.md --project
amplifier bundle list
```

Expected: `specialists` appears in the list.

**Step 3: Run a test query**

```bash
cd /Users/chrispark/Projects/specialists
amplifier run "Use the researcher to find recent updates from Sam Altman at OpenAI. Query type: person. Quality threshold: high."
```

Expected: researcher runs the pipeline and returns structured findings with source tiers and confidence levels.

**Step 4: Verify agent loads in interactive mode**

```bash
amplifier
# At the prompt:
/agents
```

Expected: `researcher` appears in the agent list.

**Step 5: Commit any fixes**

```bash
git add -A
git commit -m "fix(researcher): address issues found during first run"
```

---

## Task 8: Push to GitHub

```bash
cd /Users/chrispark/Projects/specialists
git push origin main
```

Verify at: https://github.com/cpark4x/specialists

---

## Success Criteria

- [ ] `amplifier bundle list` shows `specialists`
- [ ] `amplifier run` invokes the researcher agent
- [ ] `/agents` in interactive mode shows `researcher`
- [ ] Test query returns structured output with findings, source tiers, confidence levels, and evidence gaps
- [ ] All commits pushed to `cpark4x/specialists`
