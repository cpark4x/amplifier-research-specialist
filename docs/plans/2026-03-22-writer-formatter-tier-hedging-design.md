# Writer-Formatter Tier-Aware Hedging Design (#40)

## Goal

Upgrade Stage 3.5 (Confidence-Hedge Audit) in the writer-formatter to check source tiers before inserting hedges, preventing inappropriate over-hedging of strong evidence.

## Background

The writer's Stage 4 (Draft) already defines tier-aware hedging language:

- **Primary/Secondary:** "Research indicates...", "A study of [N] found...", "[University] analysis shows..."
- **Tertiary:** "According to [source]...", "survey data suggests...", "[source] states that..."

The writer-formatter's Stage 3.5 is the safety net that catches claims the writer missed hedging. But it currently undermines strong evidence by applying "reportedly" to peer-reviewed studies — the competitive eval showed confidence calibration at 7.50, partly because the pipeline over-hedges strong evidence.

This complements the breadth mode work (#46) — breadth mode produces more medium-confidence single-source claims, and the hedging needs to be tier-appropriate for those claims.

## Approach: Simplified Tier Gate

Stage 3.5 acts as a gate: check the source tier of the claim before inserting hedges. Don't add new hedging language — just prevent inappropriate hedging on strong sources. Let the writer's Stage 4 handle the nuanced language.

Why simplified over full tier-aware language mapping:

- Stage 3.5 is a safety net, not the primary hedging engine
- The writer (Stage 4) does the heavy lifting on hedging language
- Less duplication, less chance of conflicting hedging rules between writer and formatter
- Simpler to implement and test

## Architecture

Single-file change within the writer-formatter pipeline. Stage 3.5 already collects S-numbers with confidence levels from Stage 1 output, and each S-number includes source tier metadata. The tier data is available at the point where hedging decisions are made — no new data flow required.

## What Changes

### Stage 3.5 (Confidence-Hedge Audit) — Modify Step 5

Currently, step 5 says: "If not hedged, insert a minimal qualifier by confidence tier" and uniformly applies hedges.

Add a source-tier check before inserting hedges:

- **Primary/Secondary source claims (academic, institutional, established press):** Do NOT insert "reportedly" or similar weak hedges. If the writer used definitive language for a medium-confidence claim backed by a peer-reviewed study or institutional data, that's appropriate — "reportedly" would undermine the evidence. Leave the prose as-is. If hedging is genuinely needed for these claims, it should be tier-appropriate language that the writer's Stage 4 should have already applied.
- **Tertiary source claims (blogs, aggregators, vendor content):** "Reportedly," "according to [source]," "some sources suggest" are appropriate. Current behavior is correct for these — proceed with hedge insertion.
- **Inference claims:** Current behavior is correct — analytical qualifying language ("analysis suggests," "the evidence points to") regardless of source tier.

## What Does NOT Change

- Does not add new hedging language — just prevents inappropriate hedging on strong sources
- Does not change the writer's Stage 4 hedging rules
- Does not change any other stage of the writer-formatter
- Does not change the output format
- Does not change any other specialist or recipe file

## Data Flow

No change to data flow. Stage 3.5 already receives S-numbered claims from Stage 1 with their source tiers and confidence levels. The tier check is applied in-place at step 5 before hedge insertion — no new inputs or outputs.

```
Stage 1 (S-numbers with tier + confidence)
  → Stage 3.5 step 1-4 (collect medium/low/inference claims, scan prose)
  → Stage 3.5 step 5 [MODIFIED: tier gate before hedge insertion]
  → remaining stages unchanged
```

## Scope

### Changes

- `agents/writer-formatter.md` — modify Stage 3.5 step 5 to add a source-tier check before inserting hedges

### No Changes To

- No new pipeline stages
- No new recipe files
- No changes to any other specialist or agent file
- No changes to the output format

## Error Handling

If source tier is missing or ambiguous for a claim, fall back to current behavior (insert the hedge). This is the conservative default — it's better to over-hedge an unknown claim than to leave a weak-source claim unhedged.

## Testing Strategy

1. Structural test confirming tier-aware language exists in Stage 3.5
2. Test that primary/secondary claims are protected from "reportedly"
3. Test that tertiary claims still get hedged as before
4. Test that the tier check comes before hedge insertion

## Expected Impact

Improvement to confidence calibration score (currently 7.50) by preventing over-hedging of strong evidence. The pipeline's confidence calibration was already its signature strength at 9.0 in the first eval but dropped to 7.50 in subsequent evals partly due to uniform hedge insertion undermining peer-reviewed and institutional sources.

## Open Questions

None — design is fully specified and validated.