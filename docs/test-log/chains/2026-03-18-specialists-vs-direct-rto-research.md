---
specialist: multi-pipeline
chain: "specialists (researcher → formatter → data-analyzer → da-formatter → writer → writer-formatter) vs direct (web-research → manual synthesis)"
topic: rto-mandates-retention-productivity
date: 2026-03-18
quality_signal: mixed
action_items_promoted: true
---

# Specialists Pipeline vs Direct Approach — RTO Research Brief — 2026-03-18

**Task:** Research the real impact of return-to-office mandates on employee retention and productivity. Produce an executive brief for leadership presentation. Focus on evidence, not opinion. Adjudicate conflicting sources. Flag evidence gaps.

**Why this run matters:** First controlled A/B test of the full specialist pipeline against a non-specialist approach (foundation:web-research + manual synthesis) on identical input. Reveals where the pipeline adds value, where it adds overhead, and what architectural improvements would close the gap.

---

## Input Given to Each Approach

**Specialists pipeline:** Identical research prompt delegated to `specialists:researcher`. Output passed through the full 6-agent chain: researcher → researcher-formatter → data-analyzer → da-formatter → writer → writer-formatter.

**Direct approach:** Same research prompt delegated to `foundation:web-research` (single agent, no specialist pipeline). Analysis and brief written directly by the orchestrating session — no specialist writer, no formatters.

---

## Specialists Pipeline Output

### researcher
Returned ~6,000 words covering 14 discrete findings across retention (4), productivity (5), who-leaves (4), and management intent (1). Source tier assessment table included. 7 evidence gaps documented. Quality gate: PASS.

**Quality:** Thorough. Found the same core academic studies as the direct approach. Missed the JPMorgan June 2025 internal survey data and the Dell 50%-chose-remote stat.

### researcher-formatter
Normalized to canonical RESEARCH OUTPUT block. 14 claims with tier/confidence labels. Sub-question coverage table added.

**Quality:** Clean format conversion. No value-add beyond structural normalization.

### data-analyzer
Drew 3 labeled inferences from 14 findings:
1. Hybrid ≠ fully remote (high confidence, traces to F2/F5/F6)
2. Adverse selection mechanism — senior talent to competitors (medium, traces to F1/F4/F9/F11/F12)
3. Financial neutrality from replacement cost offset (medium, traces to F1/F3/F7)

Explicitly excluded 4 findings (F8, F10, F13, F14) with documented reasons.

**Quality:** The best single step in the pipeline. Inference separation and exclusion documentation are genuinely valuable for audit trail. The adverse selection framing was analytically sharper than the direct approach's treatment.

### da-formatter
Normalized to canonical ANALYSIS OUTPUT block.

**Quality:** Structural pass-through. No value-add.

### writer
Produced a 490-word brief in 5 sections: Summary, What Is Well-Established, What Is Contested or Unknown, Source Quality, What the Evidence Suggests.

**Quality:** Clean, scannable, well-structured. But over-hedged — "reportedly," "available analysis indicates," "according to available research" on findings backed by RCTs and large-scale causal studies. The hedging diluted the strength of the evidence for an executive audience.

### writer-formatter
Produced canonical Writer output block with CLAIMS TO VERIFY and CITATIONS.

**Quality:** Structural pass-through. CLAIMS TO VERIFY block is useful for fact-checking but invisible to the end reader.

---

## Direct Approach Output

### foundation:web-research
Single research agent returned ~4,500 words of synthesized evidence. Found the same core studies plus:
- JPMorgan Chase June 2025 internal survey (~284,000 employees, morale decline, satisfaction decline, leadership acknowledged link to RTO)
- Dell 50%-chose-remote stat (workers chose remote despite explicit promotion penalty)
- BambooHR detail: 37% of managers/directors/executives believed their org enacted layoffs because fewer employees quit than expected during RTO

**Quality:** Comparable depth to specialist researcher. Different search strategy surfaced different evidence.

### Manual synthesis (orchestrator session)
~1,200 words. Four sections: What the Evidence Clearly Shows, What Is Genuinely Contested, Where Evidence Simply Doesn't Exist, What This Means for Policy Decisions.

**Quality:** More direct voice. Richer explanation of why conflicts exist (e.g., Richmond Fed survey's headcount-vs-quality distinction). "Three scenarios" ending gave leadership concrete expected outcomes per policy choice.

---

## Head-to-Head Comparison

| Dimension | Specialists Pipeline | Direct Approach | Winner |
|---|---|---|---|
| Evidence found | 14 findings, 12+ sources | Same core + 3 additional findings | Direct |
| Source tiering | Formal tier labels + confidence per claim | Informal but equivalent quality table | Tie |
| Analytical depth | Explicit inference separation with traceability | Analysis embedded in narrative | Specialists |
| Exclusion documentation | 4 findings excluded with reasons | Contested evidence discussed but no formal exclusions | Specialists |
| Writing quality (exec audience) | Over-hedged, diluted strong findings | Direct voice, appropriate for decision-makers | Direct |
| Actionability | Conceptual closing ("how much flexibility") | Three concrete scenarios with expected outcomes | Direct |
| Auditability | Full claim traceability chain (S1→F1→I1) | Source table, inline citations, but no formal chain | Specialists |
| Latency | 6 sequential agent calls | 1 agent call + direct writing | Direct |
| Machine consumption | Canonical blocks parseable by downstream agents | Prose only | Specialists |

---

## Scores

**Specialists pipeline:** 7.5/10
- Strong: analytical rigor, audit trail, inference separation, exclusion documentation
- Weak: missed evidence, hedging accumulation, formatter overhead, less actionable ending

**Direct approach:** 8.5/10
- Strong: more evidence found, direct voice, richer conflict explanations, actionable scenarios, faster
- Weak: no formal traceability, analysis embedded not separated, slightly longer

---

## What Worked

- **Data-analyzer inference separation is the pipeline's clearest value-add.** The three labeled inferences — especially the "adverse selection mechanism" framing — were analytically sharper than the direct approach's narrative treatment. This step justifies the pipeline for analytical work.
- **Exclusion documentation** (UNUSED FINDINGS with reasons) is valuable for high-stakes deliverables where someone might challenge "why didn't you include X?"
- **Researcher found the same core studies** as the direct approach — the academic evidence base is consistent regardless of search method.
- **Direct approach found more evidence** because the web-research agent used a different search strategy. Not a specialist design flaw — just different search paths.
- **Direct approach produced better executive writing** because there was no hedging accumulation through the chain.

## What Didn't / Concerns

1. **Hedging compounds through the pipeline.** Researcher says "high confidence." Analyzer says "medium quality score" (because not all inferences are high). Writer adds "reportedly" and "available analysis indicates." By the end, a Nature RCT reads like a tentative suggestion. This is the most impactful quality issue — it changes how an executive perceives the evidence strength.

2. **Formatters add latency without adding insight.** Four of six pipeline steps were formatters or structural passes. They consumed time and tokens to convert output into canonical blocks that the next agent expected. The final human-facing output contained none of that scaffolding. For human-terminal workflows, formatters are overhead.

3. **Writer's executive calibration needs work.** The specialist writer hedged more than the source confidence warranted. "According to available research, senior employee share reportedly declined" — the word "reportedly" is wrong here; it's from a study analyzing 260M resumes, not a rumor. The writer should match hedging to source tier, not apply blanket epistemic caution.

4. **Pipeline missed evidence the direct approach found.** The JPMorgan internal survey (June 2025) and the Dell 50%-chose-remote stat were absent from the specialist researcher's output. Different search strategy, not a design flaw, but worth noting — a single research agent doesn't guarantee comprehensive coverage.

5. **No actionable decision framework in pipeline output.** The writer ended with a conceptual reframe ("how much structured flexibility, and for whom") rather than concrete scenario analysis. The direct approach's three-scenario ending (mandate → expect X; hybrid → expect Y; fully remote → expect Z) is what decision-makers actually need.

## Confidence Accuracy

- Researcher confidence labels were accurate. High-confidence claims (Bloom RCT, Ding et al. turnover) are genuinely well-supported. Medium-confidence claims (financial performance, gender impact) correctly flagged uncertainty.
- Data-analyzer's "medium quality score" was technically correct (only 1 of 3 inferences at high confidence) but misleading — the overall evidence base is strong. The quality score measures inference confidence, not evidence quality.
- Writer's hedging language did not match the source confidence tiers. This is the hedging accumulation problem — each agent adds caution independently.

## Coverage Assessment

- **Retention/turnover:** Both approaches found the core Ding et al. and Van Dijcke et al. studies. Comprehensive.
- **Productivity:** Both found Bloom RCT, Gibbs et al., Barrero/Bloom/Davis. Comprehensive.
- **Who leaves:** Both found senior/skilled employee concentration. Direct approach added the Dell choice data.
- **Financial impact:** Both found Ding & Ma S&P 500 analysis. Direct approach added JPMorgan internal survey.
- **Conflicting evidence:** Both found Richmond Fed and BambooHR. Direct approach provided richer explanation of why conflicts exist.
- **Evidence gaps:** Both identified the same 7 gaps. Comprehensive.

## Action Items

- [x] **Hedging preservation rule** — Add instruction to writer: "Match hedging level to source tier. Primary tier (peer-reviewed) = state directly. Secondary tier (working papers) = 'research indicates.' Tertiary tier (surveys) = 'survey data suggests.' Do not apply blanket epistemic caution." Route to: `docs/BACKLOG.md` as new item.
- [x] **Skip-formatters mode for human-terminal workflows** — When no downstream agent consumes the output, offer a `depth=quick` path: researcher → writer (skip formatters and analyzer). Cuts latency roughly in half for direct-to-human use cases. Route to: `docs/BACKLOG.md` as enhancement to #36.
- [x] **Decision-support template for executive audiences** — Add a "Scenario Implications" section template to writer for `audience=executive`: "If you choose X → expect Y." Concrete outcomes per option, not conceptual reframes. Route to: `docs/BACKLOG.md` as new item.
- [x] **Confidence-to-hedging mapping table** — Define explicit mapping: source tier → allowed hedging language. Prevents each agent from independently adding caution. Route to: writer specialist instruction update.
- [ ] **Multi-search-strategy research** — The fact that two different research approaches found different evidence suggests value in running multiple search strategies and merging. Related to Big Ideas: ecosystem-comparison-chain concept (fan-out research). Not yet actionable — note for future design.
