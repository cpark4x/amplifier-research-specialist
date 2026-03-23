# Writer Audience-Aware Technical Depth Design (#50)

## Goal

Add an audience-aware technical depth self-check to the writer's Stage 4 (Draft) so that when the audience is not technical, the writer translates mechanism-level details into outcome-level language.

## Background

The writer currently produces the same level of technical detail regardless of audience. For technical practitioners, this is appropriate. For executives or general audiences, mechanism-level language (architecture details, API specifics, model parameters, code-level concepts) reduces readability and misses the audience.

The competitive eval showed structure & readability at 8.25 — adequate but with room for improvement, especially on topics where the pipeline produced overly technical output for the stated audience.

Backlog entry: "When audience is not 'AI engineers' or 'technical practitioners,' translate mechanism-level details into outcome-level language. Add self-check: 'Would this sentence make sense to someone who doesn't build AI systems?' (~0.3 pts)."

## Approach

Add a self-check at the end of Stage 4 (Draft) in `agents/writer.md`. The self-check runs after the writer finishes drafting, before the document moves to the writer-formatter. It checks whether the audience (detected in Stage 2) is technical or not, and if not, scans for mechanism-level language that should be translated to outcome-level language.

Why a self-check rather than a new pipeline stage:

- The writer already has audience detection in Stage 2 — the data is available
- The self-check is additive — it doesn't change existing behavior for technical audiences
- No new pipeline stages, no new files, no downstream changes
- The writer-formatter already handles the output, so nothing else needs to change

## Architecture

Single-file change within the writer pipeline. Stage 2 already detects the audience. Stage 4 already has hedging rules and confidence-appropriate language. The audience depth self-check slots in at the end of Stage 4, after the existing hedging section — no new data flow required.

## What Changes

### Stage 4 (Draft) — Add Audience Depth Self-Check

After the existing hedging rules and confidence-appropriate language section in Stage 4, add a new self-check section:

**Audience depth self-check (non-technical audiences only):**

This self-check runs when the audience detected in Stage 2 is NOT one of: "AI engineers", "technical practitioners", "developers", "software engineers", or similar technical roles. For technical audiences, skip this check — current behavior is appropriate.

For non-technical audiences:

1. Scan each key point for mechanism-level language: architecture details, API names, model parameter counts, embedding dimensions, training methodology specifics, code-level concepts, internal system names.
2. For each mechanism-level detail found, translate to outcome-level language: what it does for the reader, not how it works internally.
   - Example: "jina-embeddings-v3 uses a 768-dimensional dense vector space with late interaction scoring" → "Jina's latest model produces highly accurate search results by comparing meaning rather than keywords"
   - Example: "The WASI capability-based security model restricts file system access through pre-opened file descriptors" → "WebAssembly's security design prevents programs from accessing files they weren't explicitly given permission to read"
3. Self-check question: "Would this sentence make sense to someone who doesn't build AI systems?" If no, translate it.

## What Does NOT Change

- Technical audiences get current behavior — no depth translation
- Stage 2 audience detection — unchanged
- Stage 3 structure selection — unchanged
- The writer-formatter — unchanged
- The output format — unchanged
- No new pipeline stages, no new recipe files, no changes to any other specialist

## Data Flow

No change to data flow. Stage 2 detects the audience. Stage 4 uses it for the self-check. No new inputs or outputs.

```
Stage 2 (audience detection)
  → Stage 3 (structure selection)
  → Stage 4 existing hedging rules
  → Stage 4 [NEW: audience depth self-check for non-technical audiences]
  → remaining stages unchanged
```

## Scope

### Changes

- `agents/writer.md` — add audience depth self-check section at the end of Stage 4

### No Changes To

- No new pipeline stages
- No new recipe files
- No changes to any other specialist or agent file
- No changes to the output format

## Error Handling

If the audience is ambiguous or not clearly detected in Stage 2, default to technical behavior (skip the self-check). This is the conservative default — it's better to preserve technical detail for an unknown audience than to strip it for someone who needs it.

## Testing Strategy

1. Structural test confirming the audience depth self-check exists in Stage 4
2. Test that the self-check mentions non-technical audiences
3. Test that the self-check mentions mechanism-level vs outcome-level language
4. Test that the self-check includes the "Would this sentence make sense" question
5. Test that technical audiences are excluded from the check

## Expected Impact

~0.3 point improvement on structure & readability for non-technical audience topics. The pipeline currently scores 8.25 on structure — this should push closer to 8.5–9.0 for general/executive audiences while preserving technical depth for practitioner audiences.

## Open Questions

None — design is fully specified and validated.