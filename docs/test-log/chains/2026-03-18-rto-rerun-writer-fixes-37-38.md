---
specialist: multi-pipeline
chain: "researcher → formatter → data-analyzer → da-formatter → writer → writer-formatter"
topic: rto-rerun-writer-fixes-37-38
date: 2026-03-18
quality_signal: pass
action_items_promoted: true
---

# RTO Re-Run: Writer Fixes #37 & #38 Validation — 2026-03-18

**Task:** Re-run the full specialist pipeline on the same RTO research prompt used in the A/B comparison test, after implementing writer spec fixes #37 (tier-aware hedging) and #38 (executive decision-support template). Validate that the fixes close the quality gaps identified in the original run.

**Baseline:** Original specialist pipeline scored 7.5/10 in the A/B test (see `2026-03-18-specialists-vs-direct-rto-research.md`). Primary gaps were hedging accumulation and lack of actionable decision support.

**Commits tested:** `86197c6` (writer spec implementation), `6984d5a` (test log + backlog promotion)

---

## Scores

**Original specialist pipeline:** 7.5/10
**Re-run (post-fix):** 8.5/10 (+1.0)

| Dimension | Original | Re-run | Delta | Driver |
|---|---|---|---|---|
| Hedging calibration | 6/10 | 8.5/10 | +2.5 | #37: Tier-aware mapping |
| Specificity | 8/10 | 8.5/10 | +0.5 | Crisper language overall |
| Decision support | 6/10 | 9/10 | +3.0 | #38: Scenario implications |
| Source attribution | 7/10 | 7.5/10 | +0.5 | Tier-matched language |
| Evidence strength conveyed | 7/10 | 8.5/10 | +1.5 | Less hedging = clearer signal |

---

## What Worked

1. **Tier-aware hedging (#37) eliminated over-hedging on strong evidence.** The original writer applied "reportedly," "available analysis indicates," and "appears to" uniformly — even on a Nature RCT and a 260M-resume causal study. The re-run states strong findings directly:
   - ✅ Re-run: "Full RTO mandates produce 13–14% abnormal turnover increase"
   - ❌ Original: "RTO mandates reportedly increase turnover... available analysis indicates..."

2. **Tier-appropriate hedging preserved for weaker sources.** The writer correctly used "Research indicates" for secondary-tier academic findings (vacancy duration/hire rate data), showing the mapping is calibrated, not just removed.

3. **Executive decision-support template (#38) produced actionable closing.** The re-run included scenario-consequence framing: "If you mandate full RTO → expect 13-14% abnormal turnover concentrated in senior/female populations + 23% vacancy duration increase + 17% lower hire rates." The original ended with conceptual reframing ("adverse selection mechanism").

4. **Pipeline score matched the direct approach.** 8.5/10 for the re-run matches the direct approach score from the A/B test. The quality gap between pipeline and direct approaches is now closed on this topic.

5. **Instruction-based fixes work for voice/tone.** This is evidence that spec-level instructions CAN work — specifically for register, hedging calibration, and template guidance. This contradicts the project pattern where instruction-based fixes failed for format compliance (#29, #30, #31 all required formatter-based fixes). The distinction: **voice/tone calibration = instructions work; format enforcement = formatters required.**

## What Didn't / Concerns

1. **Researcher truncation (#35) recurred.** First response was a conversational summary (~500 words of "The headline for your leadership presentation...") instead of the full RESEARCH OUTPUT block. Required session resumption to get the complete 15-finding structured output. This is the third consecutive run showing this pattern:
   - Run 1 (2026-03-06): truncation observed
   - Run 2 (2026-03-18 A/B test): truncation observed
   - Run 3 (2026-03-18 re-run): truncation observed — 21 tool calls completed, then conversational summary instead of canonical output

2. **Researcher truncation adds latency but not quality loss.** After resumption, the full output was complete and correct. The validate-research gate in research-chain v1.9.0 would catch this, but auto-retry is not yet implemented — manual resumption is still required.

## Confidence Accuracy

Confidence labels were accurately calibrated. The writer's hedging now matches source tier:
- Primary tier (Bloom RCT, Ding et al. 260M resumes): stated directly — no "reportedly"
- Secondary tier (vacancy duration studies): "Research indicates..." — appropriate
- Tertiary tier (BambooHR survey): "survey data suggests..." — appropriate

The hedging-accumulation problem (each agent independently adding caution) is resolved by anchoring the writer's language to source tier rather than to upstream confidence scores.

## Coverage Assessment

Same evidence base as the A/B test researcher run (14 core findings). The re-run researcher found the same studies. The JPMorgan June 2025 survey and Dell 50%-chose-remote stat (found by the direct approach but not the specialist researcher in the A/B test) were again absent — different search strategy, not a regression.

## Action Items

- [x] **Log this re-run as evidence for instruction vs. formatter fix distinction.** Instruction-based fixes work for voice/tone (#37 hedging, #38 templates); formatter-based fixes work for format compliance (#29, #30, #31). This is a design principle for future backlog triage. Route to: this test log (captured here).
- [x] **Add researcher truncation data point to backlog #35.** Three consecutive runs showing identical pattern. Auto-retry should be promoted from deferred note to tracked item. Route to: `docs/BACKLOG.md` #35 entry.
- [ ] **Validate #37/#38 across diverse content types.** Current evidence is RTO-only (market/academic domain). Run hedging calibration on competitive analysis, technical research, and narrative to confirm generalization before declaring stable. Route to: next test session.
- [ ] **Multi-search-strategy research remains unaddressed.** Different search strategies find different evidence (specialist missed JPMorgan/Dell data in both runs). Related to Big Ideas: ecosystem-comparison-chain. Not yet actionable.