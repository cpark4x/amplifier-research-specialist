# Adding a Specialist

This guide walks through creating a new specialist in this repo — from the first file to the final wiring that makes it callable.

---

## Before You Start

A specialist is a domain expert agent with a **focused persona, domain-specific tools, deep instructions, and a clean interface**. Before building one, be clear on:

1. **What is the specialist's single job?** If you need "and" to describe it, it's two specialists.
2. **What does it accept?** Define the input contract before writing instructions.
3. **What does it return?** Define the output schema before writing instructions. If the output type already exists in `shared/interface/types.md`, use it. If not, define it there first.
4. **What can it do?** List the tools it needs. Don't include tools it doesn't need.

---

## Bundle Architecture

Before writing any files, understand how the pieces connect:

```
bundle.md
└── behaviors/specialists.yaml       ← declares tools, registers agents, injects context
    ├── tools: tool-web              ← web_search + web_fetch for all specialists
    ├── agents.include:              ← which specialists are loaded and callable
    │   ├── specialists/researcher
    │   ├── specialists/writer
    │   ├── specialists/competitive-analysis
    │   └── specialists/data-analyzer
    └── context.include:             ← injected into every session using this bundle
        └── context/specialists-instructions.md
```

**`bundle.md`** — the entry point. Declares the bundle identity and includes the behavior.

**`behaviors/specialists.yaml`** — the wiring layer. Tools are provided here and agents are registered here. A specialist that exists in `specialists/` but isn't in this file is **invisible to callers**.

**`context/specialists-instructions.md`** — the runtime dispatch guide. Injected into every session. Tells the orchestrator which specialists exist and when to route to each. A specialist missing from here **won't be selected automatically**.

---

## Structure

Create a folder under `specialists/[name]/`:

```
specialists/
└── [specialist-name]/
    ├── index.md      # Amplifier agent bundle — persona + deep instructions
    ├── README.md     # Interface contract — what it accepts, returns, can do
    └── tools/        # Specialist-specific tools (if any)
```

---

## index.md Format

```markdown
---
meta:
  name: [specialist-name]
  description: "[One sentence. What it does and what it returns.]"
---

# [Specialist Name]

[Persona — who this specialist is and what they do]

---

## Core Principles

[2–4 principles that govern behavior. Make tradeoffs explicit.]

---

## [Main methodology / pipeline / approach]

[Deep instructions. This is where quality lives. Be specific about each stage.]

---

## What You Do Not Do

[Explicit boundaries. What the specialist does NOT do.]
```

---

## README.md Format

The README is the **interface contract** — what callers need to know. It does not contain instructions for the specialist. It documents the boundary.

Sections:
- One-line description of the specialist's job
- **Accepts** — table of input fields, types, required/optional, defaults, descriptions
- **Returns** — the output type from `shared/interface/types.md`, with key fields called out
- **Can Do** — tool capabilities
- **Cannot Do** — explicit boundaries (important for orchestrators choosing specialists)
- **Design Notes** — any behavior a caller should be aware of (e.g., "takes longer by design")

---

## Shared Interface Types

If your specialist introduces a new output type, define it in `shared/interface/types.md` first. The schema is the stable contract — define it carefully before writing instructions, because it's harder to change later.

When to define a new type vs. reuse an existing one:
- Reuse `ResearchOutput` if your specialist produces source-tiered evidence
- Define a new type if the output structure is meaningfully different
- Always bump the schema version and update all callers if you change an existing type

---

## Design Principles to Follow

Every specialist in this repo follows these:

**Outcome over speed.** Default to quality. Expose speed as an opt-in parameter.

**Honest gaps.** Never silently skip failures or inaccessible content. Name what couldn't be done.

**Stateless.** No specialist manages its own memory or session state. Load context in, produce output out.

**No UI knowledge.** A specialist never knows it's being called from Canvas, a CLI, or anywhere else. The interface contract is the only boundary it knows.

---

## Adding to the Registry

Once your specialist files are complete, register it in **three places**. Missing any one means the specialist won't work.

### 1. Add to `README.md`

Add a row to the Specialists table:

```markdown
| [specialist-name](specialists/specialist-name/) | [one-line domain description] | v1 |
```

### 2. Wire into `behaviors/specialists.yaml`

Add your specialist to the `agents.include` list:

```yaml
agents:
  include:
    - specialists:specialists/researcher
    - specialists:specialists/writer
    - specialists:specialists/[your-specialist-name]   # ← add this line
```

Without this step, the specialist file exists but is never loaded when the bundle is included.

### 3. Add to `context/specialists-instructions.md`

Add your specialist to the **Available Specialists** list and the **When to Use Each** section:

```markdown
- **[specialist-name]** — [One sentence: what it does and what it returns.]

**Delegate to `specialists:[specialist-name]` when:**
- [Trigger condition 1]
- [Trigger condition 2]
```

Without this step, the orchestrator won't know the specialist exists and won't route to it automatically.

---

## Testing Your Specialist

Before opening a PR:

### 1. Invoke locally

Start an Amplifier session with the bundle active and call your specialist directly:

```python
delegate(
    agent="specialists:specialists/[your-name]",
    instruction="[test input that matches your input contract]"
)
```

### 2. Verify the output contract

Check that:
- Every required field defined in `shared/interface/types.md` is present in the output
- Evidence/coverage gaps are explicitly listed, not silently omitted
- The output passes cleanly as input to any downstream specialist it's designed to feed
- The output's header block (e.g., `ANALYSIS OUTPUT`, `RESEARCH OUTPUT`) is produced
  as **bare text, not wrapped in a triple-backtick code fence** — fenced output breaks
  downstream parse-line triggers in consumer specialists

### 3. Test a boundary case

Run at least one input that should hit your "What You Do Not Do" section — confirm the specialist declines or redirects gracefully rather than attempting the task badly.

### 4. Test the chain (if applicable)

If your specialist is designed to feed into another (e.g., feeds Writer), run the full chain and verify output passes through without a manual translation step.

### 5. Run N parallel chains on the same question (cross-chain consensus)

For research-heavy specialists, run the same question against 2–3 independent topics or subject variations in parallel. Signals that appear consistently across all N runs are more trustworthy than signals from a single run — this is triangulation.

**Pattern:** A finding that appears independently in 3 parallel chains with no shared sourcing is a higher-confidence tier than any single chain's output. Use this to distinguish structural conclusions (robust enough to plan around) from topic-specific findings (treat as directional only).

**Practical use:** When a chain test surfaces an insight that surprises you, run 2 more variants. If the signal holds across all 3, it's worth promoting to a documented finding. If it only appears in one, it may be topic noise. *(emerged from test log 2026-03-04, ai-ecosystem-roles-workforce)*

---

## Pre-Merge Checklist

- [ ] `specialists/[name]/index.md` — persona + pipeline instructions complete
- [ ] `specialists/[name]/README.md` — interface contract documented (accepts, returns, can do, cannot do)
- [ ] `shared/interface/types.md` — output type defined (if new) or existing type reused
- [ ] `README.md` — added to specialists table
- [ ] `behaviors/specialists.yaml` — added to `agents.include`
- [ ] `context/specialists-instructions.md` — added to available specialists + when-to-use section
- [ ] Local invocation tested
- [ ] Output contract verified
- [ ] Boundary case tested
- [ ] Chain tested end-to-end (if applicable)
