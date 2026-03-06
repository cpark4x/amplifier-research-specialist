---
specialist: researcher
chain: "researcher → writer"
topic: sports-betting-specialists
date: 2026-03-06
quality_signal: mixed
action_items_promoted: true
---

# Researcher → Writer Chain: Sports Betting Specialists — 2026-03-06

**Context:** User asked to research the best sports gambling specialists to track and learn from. Chain ran researcher (18 turns, research model role) → writer (4 turns, writing model role). Formatter step was skipped — Rule 5 violation. No data-analyzer step was used (appropriate for this query type — informational, not analytical).

## What Worked

- **Research depth was strong.** The researcher ran 18 turns of web search and content fetching, producing 142 distinct claims covering legends, active sharps, educators, quant analysts, media, tools, and books. Breadth across categories was excellent — not just "famous bettors" but the full ecosystem a learner would need.
- **Writer editorial decisions elevated the output.** The writer didn't just reformat — it created a "Start Here" section (picking top 5 from 30+ candidates), a week-by-week learning path, and a credibility red flags framework. These weren't in the research; the writer synthesized them from the evidence. This is the writer operating at its best.
- **Source traceability was complete.** Every claim in the final brief traced back to a numbered source statement (S1–S142). The writer's CITATIONS block mapped each source to the section where it was used. Full audit trail.
- **Model role routing worked correctly.** Researcher got `research` (deep investigation), writer got `writing` (long-form content). Both appropriate for the task.
- **Token conservation was effective.** The 18-turn research phase and 4-turn writing phase consumed agent context, not root session context. Root session stayed lean enough for the subsequent meta-discussion about specialist performance.

## What Didn't / Concerns

### Medium: Formatter step skipped (Rule 5 violation)
The coordinator routed directly from researcher to writer, skipping `researcher-formatter`. Rule 5 in `specialists-instructions.md` states: "When the researcher's output feeds ANY downstream specialist, always route through researcher-formatter first." The researcher's output happened to be well-structured this time, but the rule exists because ~1 in 3 topics produces non-canonical output. This was a protocol miss by the coordinator, not a specialist issue.

### Medium: All 142 confidence levels were "unrated"
The researcher returned every claim as `confidence: unrated` — no high/medium/low tiers, no source tier classification (primary/secondary/tertiary). For a topic where many claims are journalistic estimates or self-reported figures (e.g., "Walters won hundreds of millions," "Benter won $1 billion+"), confidence tiers would have been genuinely useful for the writer and the end user.

### Low: Writer's "Claims to Verify" section buried at the bottom
The writer correctly identified 17 claims needing verification (specific dollar amounts, staff counts, net worth figures), but these were appended after the citations block in metadata — not surfaced in the user-facing document. A reader of the brief has no signal about which claims are soft.

### Low: No BEFORE narration line emitted
Rule 2 requires three narration points: BEFORE (best-effort), HANDOFF (mandatory), FINAL (mandatory). The coordinator emitted HANDOFF ("✅ Researcher complete — passing to writer...") and FINAL ("✏️ Done. Here's your brief.") but no BEFORE line ("🔍 Running researcher..."). This is marked as best-effort in the rules, so not a violation — but it's a pattern worth noting.

## Confidence Accuracy

All 142 claims were marked `confidence: unrated`. This is a calibration gap — the researcher should be assigning tiers, especially when:
- Dollar/net worth figures are journalistic estimates with no primary source (S2, S8, S12, S13, S18, S22, S81, S95, S99)
- Staff counts come from unverified reports (S11, S21)
- Twitter handles may have changed since last verified (S19, S27, S48)
- Track record claims are self-reported or industry lore (S3, S28, S29)

The writer's CLAIMS TO VERIFY section caught 17 of these, which shows the writer is compensating for the researcher's confidence gap — but this compensation shouldn't be necessary.

## Coverage Assessment

Coverage was strong for the requested scope. No `Coverage: partial` flag was raised, and the research genuinely covered the full landscape:
- Historical legends (Walters, Benter, Bloom, Ranogajec, Voulgaris)
- Active sharps (Spanky, Fezzik, Peabody, Andrews)
- Educators (Pizzola, Miller/Davidow, Appelbaum, Wong, OddsJam)
- Quant analysts (Silver, Feng, PFF, Massey-Peabody)
- Media (Purdum, Fuhrman, Everson, Action Network, VSiN, LSR)
- Tools (Unabated, OddsJam, Action Network, betstamp, DarkHorse, PFF)

**Minor gap:** International coverage was thin. Bloom (UK/global football) and Ranogajec (Australia) were included, but no Asian market specialists, no cricket/kabaddi betting experts, and limited European soccer betting beyond Starlizard. For a US-focused learner this is fine; for global coverage it's a gap.

## Action Items

- [ ] **Coordinator: enforce formatter step (Rule 5)** — The coordinator skipped `researcher-formatter` in this chain. This is the same class of issue that Rule 5 was written to prevent. Investigate whether coordinator instructions need stronger enforcement language or whether this is a model-level compliance issue.
- [ ] **Researcher: implement confidence tiers** — 142/142 claims returned as `unrated` is a systemic gap. The researcher instructions should require at minimum high/medium/low confidence and primary/secondary/tertiary source classification for each claim.
- [ ] **Writer: surface verification needs in user-facing output** — The writer's CLAIMS TO VERIFY section is useful but buried in metadata. Consider adding a "Note on Sources" or inline confidence markers in the brief itself so readers know which figures are soft.
- [ ] **Narration: track BEFORE line emission rate** — Not a violation (best-effort), but worth monitoring across runs to see if BEFORE lines are consistently missing.
