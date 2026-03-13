---
specialist: prioritizer
chain: "prioritizer → writer → writer-formatter"
topic: prioritizer-routing-validation
date: 2026-03-09
quality_signal: pass
action_items_promoted: true
---

## What Worked

- **Automatic routing on message 1** — Coordinator received a 6-item task list with the goal "ship as much useful functionality as possible" and immediately delegated to the Prioritizer. No inline ranking, no hedging, no preamble. Clean pass against the pass condition.
- **Framework named upfront** — "impact-effort scoring" declared before any item was touched, with explicit rules defined (broken features get a negative-value multiplier). Methodology was visible before the output appeared.
- **Per-item rationale is auditable** — All 6 items received specific reasoning traceable to the goal context. Each rationale is challengeable: "I disagree that the export button is Low effort because..." is a sentence the user can actually form.
- **Input order overridden** — Dark mode was listed first by the user and ranked last by the Prioritizer. Framework overrode input anchoring rather than laundering the list back with a thin justification layer.
- **Routing fix validated** — The previous spot test (`2026-03-09-prioritizer-spot-test.md`) found a routing failure and produced an action item to add a prioritizer row to the routing heuristic table. That row is now present in `context/specialists-instructions.md` ("A list of items to rank or prioritize — even framed as orientation — Route to prioritizer. Do not rank inline."). This run confirms the fix works.
- **Full chain completed cleanly** — Prioritizer → Writer → Writer-Formatter ran without errors. Writer produced a usable brief; Writer-Formatter canonicalized it.

## What Didn't / Concerns

- **Structured output block still absent** — Commit `01e137a` claims `Prioritizer output block (#31)` was added, but the Prioritizer output in this session was markdown prose, not a structured `PRIORITIZER OUTPUT` block. Either the fix wasn't applied to the specialist instructions in this session's context, or the implementation is partial. The previous spot test flagged this as a pipeline parsability contract violation — that concern is unresolved.
- **Within-tier differentiation still soft** — The framework distinguishes tiers well (fix broken → fix degraded → build new) but doesn't sharply justify ordering within a tier. Why is the export button ranked above the DB query rather than the reverse? Both are "restore/protect value" fixes. The rationale implies it but doesn't explicitly resolve the tie.

## Confidence Accuracy

Not applicable — the Prioritizer does not produce confidence ratings. Impact and Effort ratings were categorical (Critical / High / Medium / Low). Calibration looked correct for the context provided; no obviously wrong calls. Dark mode at rank 6 (highest effort, lowest impact) is the clearest signal — the framework handled it correctly.

## Coverage Assessment

Not applicable — the Prioritizer does not have a coverage gate. All 6 items were ranked; none were flagged as unrankable. Input was well-specified enough that the framework could apply cleanly.

## Action Items

- [ ] Verify Prioritizer output block fix from #31 — run a follow-up session and check whether the Prioritizer produces a structured `PRIORITIZER OUTPUT` header block or markdown prose. If prose, the fix did not land in the deployed specialist instructions and the backlog item should be reopened.
