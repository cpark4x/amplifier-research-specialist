# Writer-Formatter Graceful Degradation Design

## Goal

The writer-formatter should not halt when the source corpus is missing in ad-hoc coordinator mode — instead, it passes through the writer's prose unchanged with a notice explaining that citations are unavailable.

## Background

Bug #44: The writer-formatter has a two-input contract — it needs both the writer's prose AND the original ~15K token source corpus (research output + analysis output) to build the full CITATIONS block with S-numbered claims. In recipe mode, both arrive as interpolated context variables. In ad-hoc mode, the coordinator sends only the writer's prose, and the formatter halts requesting material it never received.

Issue #45 (Two-Path Doctrine, shipped in 7a07b66) sidesteps this by skipping the writer-formatter entirely in ad-hoc terminal steps. But that means ad-hoc output has no citation block at all — a quality gap. Issue #44 is the deeper fix: graceful degradation when the source corpus is missing.

## Approach

**Pass-through with notice (Option D).** When the source corpus is missing, the formatter emits the writer's prose unchanged with a brief notice appended. Zero extraction logic. The formatter doesn't halt, the output is honest about what's missing, and the implementation is trivial.

Alternatives considered and rejected:

- **(a) Partial CITATIONS block** — Extract source references from the writer's inline attributions, list them without the full S-numbered claim mapping. Adds real complexity to detect missing corpus, switch extraction strategy, and produce a different output structure. Unnecessary for solving the actual problem.
- **(b) Source list only** — List URLs/source names mentioned in the writer's prose as a "Sources Referenced" appendix. Still requires extraction logic for minimal benefit.
- **(c) Full CITATIONS block with best-effort claim mapping** — Reconstruct S-numbered claims from prose and map to inline attributions. Fragile, and the output looks authoritative when it's actually guesswork.

Why Option D wins:

- Solves the actual problem: formatter doesn't halt in ad-hoc mode
- Honest — doesn't pretend to have traceability it doesn't have
- Trivial to implement — one conditional check in the agent file
- Validates immediately — one ad-hoc run proves it works
- YAGNI — partial citation extraction can be added later if users request it

## Architecture

Single-file change to `agents/writer-formatter.md`. No new components, no coordination changes, no recipe modifications.

## Detection Mechanism

The formatter checks for structural markers in its input:

- Looks for `RESEARCH OUTPUT` or `ANALYSIS OUTPUT` headers
- **Headers found** → full mode (proceed with complete extraction as today)
- **Headers absent** → degraded mode (pass-through with notice)

Why marker detection over an explicit flag:

- Self-contained — the formatter figures it out from what it received
- No changes needed to the coordinator or recipe
- Markers are reliable — they're canonical block headers that upstream formatters always produce

## Behavior

### Full Mode (source corpus present)

Proceed exactly as today — extract S-numbered claims, build the complete CITATIONS block, produce canonical formatted output. No changes.

### Degraded Mode (source corpus absent)

1. Skip all extraction logic
2. Return the writer's prose verbatim
3. Append a single notice:

```
---
[Citation block omitted — source corpus not available in this session.
Run via research-chain recipe for full citations and source traceability.]
```

## Scope

### Changes

- `agents/writer-formatter.md` — add degraded mode detection and pass-through behavior

### No Changes To

- The recipe (`research-chain.yaml`)
- The coordinator
- The Two-Path Doctrine (#45 in `context/specialists-instructions.md`)
- Any other agent file

### What This Does NOT Do

- Extract partial citations from inline attributions
- Reconstruct S-numbered claims from prose
- Produce a partial CITATIONS block
- Those are future upgrades if users request them

## Testing Strategy

1. **Structural test:** Confirm the degradation instructions exist in the agent file — marker detection language, pass-through behavior, notice text.
2. **Live validation:** One ad-hoc session where the coordinator triggers the writer-formatter without source corpus. Expected result: prose + notice returned instead of halting.

## Impact

Fixes #44 (writer-formatter graceful degradation in ad-hoc mode). Combined with validation of #42 and #41, this should push Chain Reliability from 7/10 back to 8/10.