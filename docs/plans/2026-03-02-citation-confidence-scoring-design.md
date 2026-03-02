# Citation Confidence Scoring — Design

**Date:** 2026-03-02  
**Status:** Approved  
**Epic:** 02 — Writer Specialist  

---

## What We're Building

Expose per-claim confidence as structured data in the Writer's CITATIONS block, plus a confidence distribution summary in WRITER METADATA. No new LLM calls. Confidence values are derived directly from the Researcher's existing categorical assessments.

---

## Design Decisions

### Confidence format: both categorical and numeric

`confidence: high (0.9)`

Rationale: categorical label is human-readable at a glance; numeric enables machine filtering (e.g., downstream agents applying a threshold). The numeric is a fixed mapping — not a computed score — and must be documented as such to prevent false precision.

### Fixed confidence mapping

| Researcher assessment | Numeric |
|-----------------------|---------|
| High                  | 0.9     |
| Medium                | 0.6     |
| Low                   | 0.3     |
| No signal (non-Researcher source) | unrated |

These are categorical-to-numeric mappings, not measured probabilities. Documented as constants in `shared/interface/types.md`.

### Non-Researcher sources → `unrated`

When source material is raw notes, analyst output, or any input without a Researcher confidence signal: `confidence: unrated`. Never fabricate a number or default to a value.

### WRITER METADATA summary field

Add `Confidence distribution` to the WRITER METADATA block:

```
Confidence distribution: 3 high · 1 medium · 0 low · 2 unrated
```

Lets callers assess overall document trustworthiness without parsing all CITATIONS entries.

---

## Output Format Changes

### CITATIONS block (before)

```
[S1] "Remote workers average 4.2 hours/day in meetings"
     → Source: Microsoft Work Trend Index 2024 (Primary, High)
     → Used in: The Meeting Trap
```

### CITATIONS block (after)

```
[S1] "Remote workers average 4.2 hours/day in meetings"
     → Source: Microsoft Work Trend Index 2024 (Primary, High)
     → Used in: The Meeting Trap
     → confidence: high (0.9)
```

### WRITER METADATA block (before)

```
WRITER METADATA
Input type: ResearchOutput
Output format: executive-summary
...
Coverage: full
Coverage gaps: none
```

### WRITER METADATA block (after)

```
WRITER METADATA
Input type: ResearchOutput
Output format: executive-summary
...
Coverage: full
Coverage gaps: none
Confidence distribution: 3 high · 1 medium · 0 low · 0 unrated
```

---

## Files to Change

| File | Change |
|------|--------|
| `specialists/writer/index.md` | Stage 1: capture confidence label per claim. Stage 5: include `→ confidence: X (Y)` in each CITATIONS entry and compute distribution for WRITER METADATA. Output template: update CITATIONS and WRITER METADATA blocks. |
| `specialists/writer/README.md` | Update `Citations` field description to document confidence field. Add `Confidence distribution` to WRITER METADATA fields list. |
| `shared/interface/types.md` | Add confidence mapping constants with explicit note that these are fixed mappings, not measured scores. |

---

## Out of Scope

- Confidence labels on section attribution lines (`> *Sources: ...*`) — separate feature
- Prose hedging based on confidence level — separate feature
- Configurable confidence thresholds on input — separate feature (P6 backlog item)
