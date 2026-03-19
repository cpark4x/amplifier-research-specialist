---
specialist: multi-pipeline
chain: "researcher → formatter → data-analyzer → da-formatter → writer → writer-formatter"
topic: writer-fixes-37-38-cross-topic-validation
date: 2026-03-19
quality_signal: mixed
action_items_promoted: true
---

# Cross-Topic Validation: Writer Fixes #37 & #38 — 2026-03-19

**Task:** Validate that writer spec fixes #37 (tier-aware hedging) and #38 (executive decision-support template) generalize beyond the RTO research domain. Run the full specialist pipeline on two diverse topics with different source-tier distributions.

**Baseline:** RTO re-run scored 8.5/10 (see `2026-03-18-rto-rerun-writer-fixes-37-38.md`). Fixes worked on market/academic domain with predominantly primary-tier sources.

**Commits tested:** `86197c6` (writer spec implementation)

---

## Topics Selected

| Topic | Why this tests the fix | Expected source-tier mix |
|---|---|---|
| WebAssembly for backend services (CTO assessment) | Technical domain with blog-heavy sources and fewer academic studies | Mostly tertiary (blogs, surveys), some primary (spec docs, official announcements) |
| AI coding assistant productivity (engineering leadership brief) | Has both RCTs and vendor marketing — maximum tier diversity within one document | Primary (RCTs, field experiments), secondary (working papers), tertiary (vendor surveys) |

---

## Scores

| Topic | Score | #37 Hedging | #38 Decision-Support |
|---|---|---|---|
| RTO re-run (baseline) | 8.5/10 | ✅ Pass | ✅ Pass |
| WebAssembly | 7/10 | ⚠️ Partial pass | ✅ Strong pass |
| AI coding assistants | 8/10 | ✅ Validated | ✅ Strong pass |
| **Cross-topic average** | **7.8/10** | **Partially validated** | **Fully validated** |

---

## Topic 1: WebAssembly for Backend Services

### Decision-Support (#38) — ✅ PASS

Three concrete, differentiated scenarios produced:
1. "Adopt now for general backend services →" with specific consequences (toolchain friction, WASI 0.3 breaking changes, observability gaps, Rust-only language support)
2. "Adopt now for sandboxed plugin/edge-function system →" with alignment to proven patterns + specific limitations
3. "Wait 12–18 months →" with expected capabilities + competitive risk trade-off

All scenarios use the "→ Expect" pattern. Outcomes name specific technologies, timelines, and operational consequences. No conceptual reframes.

### Hedging (#37) — ⚠️ PARTIAL PASS

**What worked:**
- High-confidence primary-tier claims (spec docs, production announcements) stated definitively — no over-hedging ✅
- Two medium-tertiary claims correctly hedged: "Industry surveys cite..." (S20), "According to industry analysis..." (S28) ✅
- Zero instances of "reportedly" applied to strong evidence ✅

**What didn't:**
- Low-confidence tertiary claim (S3: "3–5% of native speed" from a personal blog) stated as definitive fact ❌
- Three medium-confidence tertiary claims (S6, S17, S19) stated without source attribution ❌
- Two inferences (S32 production pattern, S33 ecosystem timing) stated as facts without analytical qualifiers ❌
- Writer-formatter Stage 3.5 compensated but used confidence-only model, not tier-aware — applies "reportedly" uniformly regardless of source tier

**Hedging calibration: 5/10.** Over-hedging eliminated (the critical #37 win). But under-hedging persists for ~60% of medium-confidence tertiary claims and inferences.

### Researcher Truncation (#35)

No truncation observed on this run. ✅

---

## Topic 2: AI Coding Assistant Productivity

### Decision-Support (#38) — ✅ PASS

Two-layer decision structure:
1. **Implications section** with if/then framing: "If your teams spend significant time on clearly defined tasks, expect measurable gains — particularly among junior developers. If they primarily tackle complex work in mature codebases, expect uncertain returns."
2. **Next Steps section** with three decision paths: "If investing" (specific pilot design), "If already deployed" (specific metrics to instrument), "For tool selection" (evidence-based guidance)

All branches have concrete actions, specific metrics named (cycle time, merge rate, defect rate), and specific timeframes (3+ months). No conceptual reframes.

### Hedging (#37) — ✅ VALIDATED

**Sentence-level audit results:**

| Tier/Confidence | Claims tested | Correct hedging | Verdict |
|---|---|---|---|
| Primary/high (RCTs, field experiments) | 6 | 6 — definitive language, no "reportedly" | ✅ PASS |
| Primary/medium (suggestive evidence) | 2 | 1 exact match ("research indicates"), 1 acceptable ("suggest") | ✅ PASS |
| Tertiary/low (vendor surveys) | 1 | 1 — structural framing (scare quotes + "lack independent controls") | ⚠️ Functional equivalent, not exact spec formula |
| Inference | 3 | 3 — "evidence suggests," "evidence indicates" | ✅ PASS |

**Key examples:**
- ✅ "A controlled experiment found developers completed a defined JavaScript task 55.8% faster" — definitive for high/primary
- ✅ "The same research indicates junior developers gained most (27–39%)" — exact spec formula for medium/primary
- ✅ "The evidence suggests these tools amplify routine, well-scoped work" — correct inference qualifier
- ⚠️ "Vendor-funded surveys (e.g., GitHub's 88% 'felt more productive') lack independent controls" — achieves tertiary-tier signaling via structural framing rather than spec's "survey data suggests" formula

**Hedging calibration: 8/10.** Excellent tier-aware differentiation. Minor imprecision on 2 of 14 findings (structural vs lexical hedging for tertiary sources).

### Researcher Truncation (#35)

Truncation occurred — validate-research gate caught it correctly. Manual workaround used (direct web research → hand-built analysis → writer). Gate works as designed; underlying truncation persists.

---

## Cross-Topic Analysis

### #38 (Decision-Support) — FULLY VALIDATED ✅

Consistent across all 3 topics:
- RTO: 3 scenarios with policy consequences
- Wasm: 3 scenarios with technology-specific outcomes
- AI coding: 2-layer structure with if/then implications + prescriptive next steps

The executive decision-support template fix generalizes reliably. The writer produces concrete, specific, actionable scenario-consequence framing regardless of domain.

### #37 (Hedging) — PARTIALLY VALIDATED ⚠️

The critical win holds: **the writer no longer over-hedges strong evidence.** Zero instances of "reportedly" or "may possibly" applied to RCTs, field experiments, or spec documents across all 3 topics. This was the primary problem identified in the A/B test.

**The gap: under-hedging of medium-confidence tertiary claims is inconsistent.**

| Topic | Source-tier mix | Hedging accuracy |
|---|---|---|
| RTO (market/academic) | Mostly primary | 8.5/10 — few tertiary claims to test |
| Wasm (technical/blogs) | Mostly tertiary | 5/10 — ~60% of medium-tertiary claims unhedged |
| AI coding (mixed) | Balanced primary + tertiary | 8/10 — excellent differentiation |

**Pattern:** When the source base is predominantly tertiary (Wasm topic), the writer's hedging compliance drops. When there's a clear tier contrast within the document (AI coding: RCTs vs vendor surveys), the writer differentiates well. The spec's tier-aware instructions work best when the writer can see the contrast — they work less well when most sources are at the same tier.

**Root cause hypothesis:** The writer's self-check doesn't explicitly enumerate medium-confidence claims and verify each has a hedge. The current spec explains the *what* (tier-aware mapping) but doesn't enforce a *scan* (check every medium claim before returning). The AI coding topic worked because the tier contrast was obvious; the Wasm topic failed because blog-sourced claims "felt" factual in a technical context.

### #35 (Researcher Truncation) — CONFIRMED SYSTEMIC

| Run | Truncation? | Recovery |
|---|---|---|
| 2026-03-06 | Yes | Manual resumption |
| 2026-03-18 A/B test | Yes | Manual resumption |
| 2026-03-18 re-run | Yes | Manual resumption |
| 2026-03-19 Wasm | No | — |
| 2026-03-19 AI coding | Yes (gate caught) | Manual workaround |

**4 out of 5 runs show truncation.** The validate-research gate catches it correctly, but without auto-retry the pipeline cannot self-serve. This should be promoted from monitoring to active backlog.

---

## What Worked

1. **#38 generalizes cleanly.** No adjustments needed. The executive decision-support template produces correct output across market, technical, and mixed domains.
2. **Over-hedging is eliminated.** The primary #37 fix (don't apply "reportedly" to RCTs) holds across all topics and source-tier mixes. This was the A/B test's main quality complaint.
3. **AI coding topic showed excellent tier differentiation.** "Shows" for high/primary → "research indicates" for medium/primary → structural framing for low/tertiary → "evidence suggests" for inferences. This is the spec working as designed.
4. **Writer-formatter Stage 3.5 acts as safety net.** Even when the writer under-hedges, the formatter catches most gaps — though with a cruder confidence-only model.

## What Didn't / Concerns

1. **Under-hedging medium-tertiary claims when source base is mostly tertiary.** The Wasm topic showed the writer treating blog-sourced technical claims as factual. The tier-aware mapping works when tier contrast is visible (AI coding) but not when most sources are at the same tier.
2. **Inference-as-fact in Wasm topic.** Two analytical inferences stated without "evidence suggests" qualifier. The AI coding topic correctly qualified all 3 inferences. Inconsistent.
3. **Writer-formatter uses confidence-only hedging, not tier-aware.** Stage 3.5 applies "reportedly" uniformly to all medium-confidence claims. The spec calls for tier-differentiated language. This is a separate fix from the writer spec.

## Confidence Accuracy

Source confidence labels were accurate across both topics. The accuracy issue is in the writer's translation of those labels to prose language, not in the labels themselves.

## Coverage Assessment

Both topics had appropriate evidence bases. Evidence gaps were correctly identified and disclosed in both briefs. No false coverage flags.

## Action Items

- [x] **#37 is partially validated — no further writer spec changes yet.** The fix works for the primary complaint (over-hedging strong evidence). Under-hedging of medium-tertiary is inconsistent and may improve with a self-check addition, but should be observed over more runs before adding complexity. Route to: this test log (noted).
- [x] **#38 is fully validated.** No changes needed. Route to: backlog (can be closed after one more sprint of observation).
- [ ] **Writer spec: add medium-claim self-check.** After Stage 5 verification, add: "Scan every medium-confidence claim — does it have a visible hedge? Does the hedge match the source tier?" This addresses the Wasm under-hedging gap without changing the tier-aware mapping itself. Route to: `docs/BACKLOG.md` as enhancement to #37.
- [ ] **Writer-formatter: upgrade Stage 3.5 to tier-aware hedging.** Currently applies "reportedly" uniformly. Should differentiate: "research indicates" for primary/secondary medium, "according to [source]"/"reportedly" for tertiary medium. Route to: `docs/BACKLOG.md` as new item.
- [ ] **Promote #35 auto-retry to tracked backlog item.** 4/5 runs show truncation. Monitoring phase is complete — the pattern is confirmed systemic. Route to: `docs/BACKLOG.md`.
- [ ] **Investigate research-chain v1.10.0 conditional branching bug.** Wasm validation used a linear recipe workaround because smart-skip gates failed (likely whitespace mismatch in bash output vs condition syntax). Route to: `docs/BACKLOG.md` as recipe-engine item.