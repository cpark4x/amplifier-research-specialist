---
specialist: prioritizer
chain: null
topic: prioritizer-spot-test
date: 2026-03-09
quality_signal: mixed
action_items_promoted: true
---

## What Worked

- **Framework transparency** — Named impact-effort upfront and defined quadrant decision rules before touching any item. The methodology was visible before the output appeared.
- **Meaningful reordering** — Recipe timeouts jumped from #7 (user's input order) to #1. Planner fell from #2 to #6. The framework overrode input anchoring rather than laundering the list back to the user — this is the key test of whether the tool is doing real work.
- **Per-item rationale is auditable** — Each item got specific reasoning traceable to the input context. Output is challengeable: "I disagree that DA Format B is Medium-High impact because..." is a sentence the user can actually form.
- **Third verdict class** — "Design now, build next sprint" for the Planner is a nuanced output that ad-hoc ranking didn't produce. Distinguishes between "wrong priority" and "wrong mode for this sprint."
- **Capacity estimate included** — "4–5 days for Tier 1" was a useful planning signal not prompted by the input.

## What Didn't / Concerns

- **No structured output block** — Every other specialist produces a machine-parseable header block (`STORY OUTPUT`, `RESEARCH OUTPUT`, `ANALYSIS OUTPUT`). The Prioritizer returned markdown prose. This breaks the pipeline parsability contract and means downstream agents cannot parse output the same way they parse other specialists.
- **Within-tier ordering is soft** — The rationale clearly distinguishes tiers (Do First vs. Plan vs. Avoid) but doesn't sharply differentiate positions within a tier. Why is Storyteller #2 and not #3 within Tier 1? The framework doesn't resolve this.
- **Fully dependent on input quality** — The Prioritizer cannot research the items it ranks. It works entirely from what the caller provides. Thin or inaccurate item descriptions produce thin or inaccurate rankings.

## Confidence Accuracy

Not applicable — the Prioritizer does not produce confidence ratings. Impact and Effort ratings were categorical (High / Medium-High / Medium / Very High) rather than numeric. Calibration seemed reasonable for the items given; no obviously wrong calls observed.

## Coverage Assessment

Not applicable — the Prioritizer does not have a coverage gate. All 8 items were ranked; none were flagged as unrankable. The spec says unrankable items should be listed explicitly — this was not tested.

## Coordinator Routing Failure (Separate Finding)

**This is a routing heuristic gap, not a Prioritizer quality issue.**

The coordinator (root session) was presented with a list of 8 priority items at session startup with the explicit goal "maximize usefulness this week." The coordinator did not route to the Prioritizer. Instead it produced an ad-hoc ranked table inline — an OUTPUT CONTRACT violation: the coordinator generated specialist-domain content itself rather than delegating.

The failure required two explicit user prompts to correct ("did you run the prioritizer specialist?" → "yes").

**Root cause:** The routing heuristic table in `context/specialists-instructions.md` has no row for "user arrives with a list to prioritize." Session startup framing ("orient me on the week") suppressed routing awareness. The Prioritizer trigger exists in the When to Use Each section but not in the routing heuristic table that the coordinator checks first.

**Comparison: ad-hoc vs. Prioritizer output**

| Dimension | Ad-hoc (coordinator inline) | Prioritizer |
|---|---|---|
| Framework named | No | Yes (impact-effort) |
| Input order preserved | Yes (anchored) | No (framework overrode) |
| Per-item rationale | Light, implied | Explicit, traceable |
| Verdict nuance | Binary | Three states |
| Auditability | Low | High |
| Score | 3/10 | 7/10 |

## Action Items

- [ ] Add structured output block to Prioritizer spec — `PRIORITIZER OUTPUT` header matching other specialists (`STORY OUTPUT`, `RESEARCH OUTPUT`, `ANALYSIS OUTPUT`). Required for Prioritizer to be usable as a pipeline stage rather than standalone tool.
- [ ] Add routing row to `context/specialists-instructions.md` routing heuristic table: "A list of items to rank or prioritize → Route to Prioritizer." Add note covering session startup case where priority list arrives alongside orientation context.
