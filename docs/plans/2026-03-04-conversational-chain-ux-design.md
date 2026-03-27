# Conversational Chain UX Design

## Goal

Fix the two UX problems that affect all conversational specialist invocations: raw intermediate output surfacing to users instead of finished documents, and zero visibility into which specialists ran or in what order.

## Background

When a user asks the Amplifier Research Specialist platform something like "run a competitive analysis on X vs Y", the orchestrator delegates to the appropriate specialist — but then surfaces the raw structured block (`COMPETITIVE ANALYSIS BRIEF`, `RESEARCH OUTPUT`, etc.) directly to the user. These blocks are machine-readable intermediate formats designed for downstream specialists, not human consumption.

At the same time, the user has no idea what happened behind the scenes. They don't know which specialists ran, in what order, or whether the chain completed. The result feels like a black box that returns an ugly format.

Both problems are routing-layer issues. The specialists themselves work correctly. The orchestrator just stops too early and stays silent while it works.

## Approach

**Chosen: Option B — Fix routing brain + add per-specialist routing hints.**

Two file surfaces are touched: `context/specialists-instructions.md` (the orchestrator's routing brain) and each specialist's `index.md` (5 files). No new files, no new recipes, no schema changes.

**Why not Option A (routing brain only):** Fragile — if the orchestrator drifts, nothing catches it. Option B is self-reinforcing because specialists carry their own routing metadata.

**Why not Option C (new conversational recipes):** Over-engineered. The existing recipes work. The problem is purely conversational routing.

## Architecture

The fix operates at a single layer: the orchestrator's routing decisions. Specialists remain unchanged in behavior and output format.

```
User request
  → Orchestrator (reads specialists-instructions.md rules FIRST)
    → Narration: "Running researcher..."
    → Specialist 1 (returns structured block + routing hint in index.md)
    → Narration: "Researcher complete — passing to writer..."
    → Specialist 2 (writer, default format = brief)
    → Narration: "Done. Here's your brief."
  → User receives finished document
```

The routing hints in each specialist's `index.md` tell the orchestrator what was produced and what the natural next step is. The orchestrator uses this to drive narration and chain completion. Specialists never speak to the user directly.

## Components

### Component 1: Conversational Chain Rules (specialists-instructions.md)

A new `## Conversational Chain Behavior` section is added at the top of `context/specialists-instructions.md` — before the specialist menu — so rules are read first and apply globally.

Four rules live in this section:

**Rule 1 — Chain Completion Default**
When a user invokes a specialist conversationally, always complete through to the writer before responding. Default output format = `brief`. Do not stop at an intermediate specialist and surface the raw structured block. The user gets a finished document.

**Rule 2 — Per-Step Narration**
Before each delegation, announce what's about to run. After each delegation, announce what completed. Simple one-line signals at the orchestrator level:
- Before: "Running researcher..."
- After: "Researcher complete — passing to writer..."
- Final: "Done. Here's your brief."

**Rule 3 — Escape Hatch**
If the user explicitly signals they want intermediate output — "give me the raw research", "just run the researcher", "don't write a document", "raw output" — stop at that specialist and surface the structured block directly. Raw output is opt-in, not opt-out.

**Rule 4 — Analysis Signal**
If the user asks for "analysis", "insights", or "full analysis", chain through data-analyzer before writer: researcher → data-analyzer → writer.

### Component 2: Per-Specialist Routing Hints (5 index.md files)

Each specialist's `index.md` gets a closing instruction in its final stage:

> "When your output is complete, signal to the orchestrator: [what you produced] + [what the natural next step is in the chain]."

Files changed:
- `specialists/researcher/index.md`
- `specialists/writer/index.md`
- `specialists/competitive-analysis/index.md`
- `specialists/data-analyzer/index.md`
- `specialists/researcher-formatter/index.md`

**Critical constraint from PRINCIPLES.md — "Output schema is the contract":**
These hints are routing metadata for the orchestrator, NOT additions to the specialist's output format. Every specialist's output must still start with its machine-parse signal as the very first characters. No preamble. No narration inside the output block.

## Data Flow

### Default Chain (most requests)

```
User: "Research edge AI for me"
  1. Orchestrator reads Rule 1 → chain must complete to writer
  2. Orchestrator narrates: "Running researcher..."
  3. Researcher runs → produces RESEARCH OUTPUT block
  4. Researcher's routing hint tells orchestrator: "produced research, natural next = writer"
  5. Orchestrator narrates: "Researcher complete — passing to writer..."
  6. Writer runs with format=brief → produces finished brief
  7. Orchestrator narrates: "Done. Here's your brief."
  8. User sees the brief
```

### Analysis Chain (triggered by Rule 4)

```
User: "Research X and give me a full analysis"
  1. Orchestrator reads Rule 4 → "analysis" detected → longer chain
  2. Researcher → data-analyzer → writer (format=brief)
  3. Narration at each step
  4. User sees finished brief with analysis
```

### Escape Hatch

```
User: "Give me the raw research output on edge AI"
  1. Orchestrator reads Rule 3 → "raw" detected → escape hatch
  2. Researcher runs → produces RESEARCH OUTPUT block
  3. Orchestrator surfaces the raw block directly
  4. User sees structured RESEARCH OUTPUT
```

## Error Handling

No new error handling is introduced. The existing specialist error handling and quality gates remain untouched. If a specialist fails mid-chain, existing failure behavior applies — the orchestrator surfaces the error as it does today.

## Testing Strategy

The design was validated through scenario stress-testing during the brainstorm session:

| Scenario | Input | Expected Behavior | Status |
|----------|-------|-------------------|--------|
| Clear request | "Run a competitive analysis on X vs Y" | Completes to writer, user gets brief | Validated |
| Explicit escape hatch | "Give me the raw research output on X" | Escape hatch fires, stops at researcher | Validated |
| Previously ambiguous | "Research edge AI for me" | Aggressive default fires, user gets brief | Validated |
| No format specified | "Research X and write something up" | Default format = brief, consistent output | Validated |
| Writer with no research | "Write a brief about quantum computing" | Auto-chains researcher first, then writer | Validated |
| Analysis signal | "Research X and give me a full analysis" | Routes through data-analyzer before writer | Validated |

Implementation testing: after changes are applied, each scenario above should be run conversationally to confirm behavior matches expectations.

## Principles Alignment

- **Output schema is the contract:** PRESERVED — no changes to output formats, machine-parse signals, or field names
- **Quality gates fail loud, not silent:** UNTOUCHED
- **Specialists use tools directly:** UNTOUCHED
- Narration is orchestrator-only — specialists never speak to the user directly

## What This Does NOT Change

- Output schemas (`RESEARCH OUTPUT`, `COMPETITIVE ANALYSIS BRIEF`, `ANALYSIS OUTPUT`)
- Machine-parse signals (must remain first characters of each specialist output)
- Recipe files (`research-chain.yaml`, `competitive-analysis-brief.yaml`, etc.)
- Shared interface types (`shared/interface/types.md`)
- Any specialist pipeline stages or quality gates

## Open Questions

None — design fully validated.
