# Session Learnings — 2026-03-06

**Context:** Long ridecast2 build day. Used amplifier-research-specialist pipeline (competitive analysis, mobile UI research) and the stories pipeline (story production) extensively. Also ran a direct comparison between stories and specialists on the same task. Reviewing tomorrow with fresh eyes before promoting to backlog.

---

## What We Learned

### 1. The Hybrid Pipeline Gap — Biggest Finding

Running both pipelines on the same story made the complementarity undeniable. Neither pipeline does both halves of the job.

**Stories pipeline strengths:**
- story-researcher mines internal artifacts (git log, STATE.yaml, CONTEXT-TRANSFER.md) with timestamp precision
- content-strategist produces deliberate strategy: slide-by-slide outline, explicit anti-patterns, audience sequencing
- storyteller produces a deployable artifact (self-contained HTML deck, opens in browser, submittable to amplifier-stories)

**Stories pipeline weaknesses:**
- No web access / external research — story-researcher is blind to industry context
- No FACT/INFERENCE rigor — content is descriptive, not analytically evaluated
- No formatter verification — data discrepancies can slip through

**Specialists pipeline strengths:**
- researcher went wide: CMU MSR '26, Waterloo TGen, Devin performance review, Anthropic 2026 report, Patrick Debois
- data-analyzer produced the sharpest insights: FACT/INFERENCE/TENSION/OPEN QUESTION labeling, with the core finding that "the CMU quality degradation finding is about unconstrained agents, not agents per se"
- writer was publication-ready: opened with "Most AI development case studies open with a velocity claim. This one starts with tests."
- formatter caught a real data discrepancy (stated 5.1s build vs live 3.7s)

**Specialists pipeline weaknesses:**
- No artifact production — writer produces text, not a shareable file
- Writer had to infer the strategic angle ("lead with quality") that content-strategist designed explicitly
- No internal data mining — researcher worked from provided facts, not from source files

**The ideal hybrid chain (not yet built):**
```
story-researcher (internal data mining)
    ↓
specialists:researcher (external industry context)
    ↓
specialists:researcher-formatter (normalize + verify)
    ↓
specialists:data-analyzer (labeled inferences)
    ↓
stories:content-strategist (packaging strategy, anti-patterns, audience)
    ↓
stories:storyteller (artifact production — deployable HTML)
```

---

### 2. Storyteller Produces Artifacts — Specialists Doesn't

The storyteller's HTML deck went directly into a PR to `ramparte/amplifier-stories` today. The specialist writer output needed extra steps to become shareable. For any task where the goal is a shareable artifact, specialists needs a render/produce step at the end.

**Open question:** Does amplifier-research-specialist build a native Presentation Builder (Epic 07) or route to stories:storyteller as a dependency?

---

### 3. Content Strategy Before Writing — Deliberate vs. Emergent

The content-strategist explicitly designed "lead with quality proof, not speed claims" as a constraint. The specialist writer arrived at the same decision independently — but by inference, not design. Both got there. But designed is more reliable than lucky across different model runs.

**Implication:** Consider a content-strategy pre-pass in `narrative-chain.yaml` before the storyteller runs.

---

### 4. Browser-Tester Belongs in UI Research Chains

Mobile UI research produced visual claims about Overcast, Spotify, ElevenReader — all text-derived, none visually verified. For research involving apps/websites/UI, a browser-tester step after the researcher would ground claims in actual screenshots.

Not after every research run — specifically when `research_type: ui_research` or when the topic involves consumer apps.

---

### 5. Research Scope Management

The mobile UI researcher returned ~5,000 words. The chain absorbed the waste, but it's still waste — more tokens, more time, less precise formatter output.

**Three scope templates worth designing:**
- `research_scope: ui_patterns` — visual/interaction patterns only
- `research_scope: competitive` — positioning, pricing, differentiation
- `research_scope: technical` — architecture, performance, integration

---

### 6. Formatter Side-Effect Behavior — Undocumented

The formatter wrote output files to the user's project both times it ran today. Useful, but invisible and undocumented. Should document: when does it write files vs. return inline content?

---

## Scores From Today

| Chain | Task | Score | Notes |
|---|---|---|---|
| Competitive analysis (researcher → formatter → CA → writer) | Ridecast2 competitive brief | 9/10 | Rich, decision-quality. Directly changed product strategy. |
| Mobile UI research (researcher → formatter → DA → writer) | Podcast/audio app UI patterns | 8/10 | Good output, excess verbosity. No visual verification. |
| Stories pipeline (story-researcher → content-strategist → storyteller) | Amplifier dev machine case study | 7/10 | Excellent data mining, good artifact. No external research or analytical rigor. |
| Specialists pipeline (researcher → formatter → DA → writer) | Same case study | 8.5/10 | Excellent research depth, sharp analysis, publication-ready prose. No artifact output. |

---

## Unresolved Questions — For Tomorrow

1. **Hybrid pipeline:** Big Ideas section or Immediate Next? Has cross-bundle dependency on stories:storyteller.
2. **Presentation Builder epic (07):** Accelerate with reference from stories:storyteller, or stay at 0% as planned?
3. **#30 Storyteller OUTPUT CONTRACT:** Promote to Immediate Next or stay Priority 2?
4. **stories:storyteller as dependency:** Build native Presentation Builder or compose with stories bundle?
5. **Content-strategist integration:** Should `narrative-chain.yaml` include a content-strategy pre-pass?

---

## What's Working Well — Don't Change

- FACT/INFERENCE/TENSION/OPEN QUESTION labeling — most analytically valuable output in any chain today
- Formatter catching data discrepancies — quality check working correctly
- Researcher going wide on external sources — depth is what makes output publishable
- Chain completion default (Rule 1) — user gets finished document, not raw research
- Researcher-formatter as matched pair — architectural fix held up across multiple runs
