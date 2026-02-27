# Adding a Specialist

This guide walks through creating a new specialist in this repo.

## Before You Start

A specialist is a domain expert agent with a **focused persona, domain-specific tools, deep instructions, and a clean interface**. Before building one, be clear on:

1. **What is the specialist's single job?** If you need "and" to describe it, it's two specialists.
2. **What does it accept?** Define the input contract before writing instructions.
3. **What does it return?** Define the output schema before writing instructions. If the output type already exists in `shared/interface/types.md`, use it. If not, define it there first.
4. **What can it do?** List the tools it needs. Don't include tools it doesn't need.

## Structure

Create a folder under `specialists/[name]/`:

```
specialists/
└── [specialist-name]/
    ├── index.md      # Amplifier agent bundle — persona + deep instructions
    ├── README.md     # Interface contract — what it accepts, returns, can do
    └── tools/        # Specialist-specific tools (if any)
```

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

[Deep instructions. This is where quality lives. Be specific.]

---

## What You Do Not Do

[Explicit boundaries. What the specialist does NOT do.]
```

## README.md Format

The README is the **interface contract** — what callers need to know. It does not contain instructions for the specialist. It documents the boundary.

Sections:
- One-line description of the specialist's job
- **Accepts** — table of input fields, types, required/optional, defaults, descriptions
- **Returns** — the output type from `shared/interface/types.md`, with key fields called out
- **Can Do** — tool capabilities
- **Cannot Do** — explicit boundaries (important for orchestrators choosing specialists)
- **Design Notes** — any behavior a caller should be aware of (e.g., "takes longer by design")

## Shared Interface Types

If your specialist introduces a new output type, define it in `shared/interface/types.md` first. The schema is the stable contract — define it carefully before writing instructions, because it's harder to change later.

## Design Principles to Follow

Every specialist in this repo follows these:

**Outcome over speed.** Default to quality. Expose speed as an opt-in parameter.

**Honest gaps.** Never silently skip failures or inaccessible content. Name what couldn't be done.

**Stateless.** No specialist manages its own memory or session state. Load context in, produce output out.

**No UI knowledge.** A specialist never knows it's being called from Canvas, a CLI, or anywhere else. The interface contract is the only boundary it knows.

## Adding to the Registry

Once your specialist is ready, add it to the table in `README.md`.
