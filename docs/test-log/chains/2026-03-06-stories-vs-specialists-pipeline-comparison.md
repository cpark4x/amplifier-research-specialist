---
specialist: multi-pipeline
chain: "stories (story-researcher → content-strategist → storyteller) vs specialists (researcher → formatter → data-analyzer → writer)"
topic: amplifier-dev-machine-case-study
date: 2026-03-06
quality_signal: partial-pass
action_items_promoted: false
---

# Stories vs Specialists Pipeline Comparison — 2026-03-06

**Task:** Produce a case study about using Amplifier's dev machine to build 22 production features in one day with zero human-written code (the Ridecast2 project).

**Why this run matters:** First direct A/B comparison of the two pipelines on identical input material. Reveals complementary strengths neither pipeline knew it had.

---

## Input Given to Each Pipeline

**Stories pipeline:** story-researcher was pointed at `/Users/chrispark/Projects/ridecast2` and asked to mine git log, STATE.yaml, FEATURE-ARCHIVE.yaml, CONTEXT-TRANSFER.md, working-session-instructions.md for raw story material.

**Specialists pipeline:** researcher was given the verified primary facts (22 features, 8 sessions, 58→151 tests, timestamps, phase breakdown) and asked to research the broader industry context (CMU MSR '26, Devin data, TDD research, spec-driven development literature).

---

## Stories Pipeline Output

### story-researcher
Returned a rich JSON payload with:
- Exact git timestamps for all 22 feature commits (to the second)
- Per-session analysis: features, duration, first-commit latency
- Notable moments: "Session 3: 14:18:27 — 4 features in 11 minutes"
- Machine architecture decisions with source quotes from CONTEXT-TRANSFER.md
- Spec quality improvement analysis (Phase 1 vs Phase 2)
- Key moments for storytelling (with evidence citations)

**Quality:** High for internal data. Timestamp precision unavailable by any other means. No external context.

### content-strategist
Returned a complete story strategy:
- Priority 1 story — "tell immediately, maximum freshness"
- 18-slide structure with explicit slide-by-slide outline
- Strategic sequencing: "Lead with quality, then speed — flips the AI story default"
- Anti-patterns list: "don't lead with AI wrote the code", "don't call it autonomous coding", "don't skip architecture slide"
- Three format recommendations: HTML deck (primary), blog post, executive one-pager
- Audience sequencing: Amplifier community → skeptical devs → AI-curious devs → CTOs

**Quality:** Excellent strategic packaging. Anti-patterns list is genuinely useful. Made good writing decisions explicit rather than leaving them to model inference.

### storyteller
Produced an 18-slide self-contained HTML deck (~77KB). Self-corrected 5 errors during production (invented feature names, invented commit counts, session duration inaccuracies).

After editorial review, deck was condensed to 8 slides. Key cuts: velocity moments slide (absorbed as scorecard line), sources slide (became footnote). Merged role transformation + replicate it into one payoff slide.

Final deck was submitted to `ramparte/amplifier-stories` as PR #70.

**Quality:** Good artifact production. Anti-patterns from content-strategist were applied. Visual quality: 7/10 initially, rose to ~8/10 after editorial condensation and density fixes.

---

## Specialists Pipeline Output

### researcher
Returned ~6,000 words of research synthesis covering:
- Primary source verification (git log, STATE.yaml confirmed)
- CMU MSR '26: +76.6% lines but +39% cognitive complexity from unconstrained agents
- University of Waterloo TGen (2024): TDD with AI → +12-18% correctness, solutions generalize
- Devin 18-month performance review: 67% PR merge rate, acknowledged "needs clear requirements"
- Claude Code: 83.8% of agent PRs merged in open-source
- Anthropic 2026: "engineering roles shifting toward supervision, system design, output review"
- Patrick Debois on spec-driven development: "shifting from micromanagement to delegation"

**Quality:** Excellent depth. The CMU complexity finding as a foil for the Ridecast2 TDD approach was the most analytically valuable insight in either pipeline.

### researcher-formatter
Normalized research to canonical format. **Caught one discrepancy:** build time stated 5.1s in STATE.yaml, measured live at 3.7s. Preserved both with explanation rather than silently adopting either number.

**Quality:** Verification function working correctly. This would have been an unnoticed error in the stories pipeline.

### data-analyzer
Produced labeled FACT/INFERENCE/TENSION/OPEN QUESTION analysis across 5 dimensions:
1. What this proves the industry doesn't yet know
2. Why CMU quality degradation doesn't apply here (constraint architecture, not agent capability)
3. What spec quality means as requirements engineering vs. prompt engineering
4. The role transformation: developer as architect
5. Reproducibility conditions

Core insight: "The constraint architecture is the product" — the five conditions (recipe orchestration, stateless sessions, TDD, health gates, Phase 2 specs) are a conjunction, not a menu.

**Quality:** The FACT/INFERENCE labeling produced the sharpest analysis in either pipeline. The data-analyzer's output was the best single piece of work in either chain.

### writer
Produced a 1,380-word case study. Opening: "Most AI development case studies open with a velocity claim. This one starts with tests." Closing: "For engineering leaders evaluating what machine-executed delivery actually looks like under production conditions, that is the baseline to beat."

**Quality:** Publication-ready. Could go on HN or a dev blog as-is. The writer arrived at the right strategic angle (quality-first) independently, without the content-strategist's explicit instruction.

---

## Head-to-Head Comparison

| Dimension | Stories | Specialists | Winner |
|---|---|---|---|
| Internal data precision | ✅ Git timestamps, commit hashes | ⚠️ Worked from provided facts | Stories |
| External research depth | ❌ None | ✅ CMU, Waterloo, Devin, Anthropic | Specialists |
| Analytical rigor | ⚠️ Descriptive | ✅ FACT/INFERENCE/TENSION labeling | Specialists |
| Written prose quality | Good | Excellent | Specialists |
| Finished artifact | ✅ HTML deck, deployable, PR submitted | ❌ Text essay only | Stories |
| Strategic packaging | ✅ Anti-patterns, audience sequencing, slide outline | ❌ Writer inferred angle independently | Stories |
| Data verification | ❌ None | ✅ Formatter caught build time discrepancy | Specialists |
| Chain length | 3 agents, faster | 4 agents, richer | Tie |

---

## Scores

**Stories pipeline:** 7/10
- Strong: data mining, artifact production, strategic packaging
- Weak: no external research, no analytical depth, no verification

**Specialists pipeline:** 8.5/10
- Strong: research depth, analytical rigor, writing quality, verification
- Weak: no artifact, writer relies on emergent judgment not designed strategy

---

## The Ideal Chain (Not Yet Built)

```
story-researcher → specialists:researcher → formatter → data-analyzer → content-strategist → storyteller
```

Neither pipeline ran this chain. It would combine:
- Timestamp-precise internal data (story-researcher)
- Industry context with citations (specialists:researcher)
- Verification and normalization (formatter)
- Labeled inferences (data-analyzer)
- Deliberate strategic packaging (content-strategist)
- Deployable artifact (storyteller)

This is the highest-value backlog item from today's session.

---

## Action Items

- [ ] **Hybrid pipeline spec** — design the combined chain as a new recipe. Cross-bundle dependency (stories + specialists). Needs design before building. Route to: `docs/BACKLOG.md` Big Ideas section pending tomorrow's review.
- [ ] **Storyteller artifact production in specialists** — specialists pipeline needs a render step. Options: native Presentation Builder (Epic 07) or route to stories:storyteller. Route to: `docs/BACKLOG.md` pending tomorrow's review.
- [ ] **Content-strategist integration** — add content-strategy pre-pass to `narrative-chain.yaml`. Route to: `docs/BACKLOG.md` pending tomorrow's review.
- [ ] **Browser-tester in UI research chains** — for research involving consumer apps, add visual capture step. Route to: `docs/BACKLOG.md` pending tomorrow's review.
- [ ] **Scoped research prompt templates** — ui_patterns / competitive / technical variants. Route to: `docs/BACKLOG.md` pending tomorrow's review.
- [ ] **Formatter side-effect documentation** — when does it write files vs. return inline? Route to: `docs/BACKLOG.md` pending tomorrow's review.
