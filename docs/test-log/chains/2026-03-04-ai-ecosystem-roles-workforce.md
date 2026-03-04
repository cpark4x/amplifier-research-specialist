---
specialist: researcher
chain: "researcher → researcher-formatter → data-analyzer → writer → save"
topic: ai-ecosystem-roles-workforce
date: 2026-03-04
quality_signal: mixed
action_items_promoted: true
---

# Test Log: AI Ecosystem Roles & Workforce (research-chain)

**Runs:** 4 total — Microsoft workforce (single), then Anthropic/Claude Code + AI Coding Tools + OpenAI (3 parallel)
**Recipe version:** 1.1.0 (save step added during this session after truncation was caught)

---

## What Worked

**Source discipline is the chain's clearest differentiator.** All four runs consistently and correctly flagged unverifiable claims: the "8% cloud-infra self-identification" figure (no source, date, or URL), Kevin Scott's "95% AI-written code" (single executive statement, no methodology), the Gartner "$2.5T cybersecurity" figure (implausible as annual), and the Onward Search concentration risk (multiple "independent" stats potentially flowing through one undisclosed methodology). This is exactly what the pipeline is supposed to do and it held across 4 independent runs with no coaching.

**Labeled inferences were the most valuable output.** The analyst layer surfaced non-obvious, well-argued insights that don't appear in surface-level reporting: the "peer programmer" framing in Microsoft's Annual Report as legal pre-positioning for future SWE headcount reductions; the absence of internal reskilling data in investor communications as a signal (if large-scale transition were happening, it would be a positive investor narrative); the self-reinforcing loop (build tools → study displacement → cut jobs → fund more tools → repeat). These came through in all four runs.

**Parallel execution worked cleanly.** Three chains ran simultaneously, all completed, no collisions. The foreach recipe design is viable.

**Cross-chain consensus is a higher-confidence tier.** The most important methodological finding of the session: when the same signal appeared independently in all three parallel runs — agentic systems engineering, AI security, CAIO/governance, credential deflation, prompt engineering decline, mid-level specialist risk — those signals are demonstrably more trustworthy than any single chain's output. This is triangulation, and it emerged organically from the workflow before any recipe was designed for it.

**CLAIMS TO VERIFY block fired correctly.** Specific numerical claims without traced sources were surfaced and flagged in every run. The pipeline is honest about what it can't verify.

---

## What Didn't / Concerns

**"Brief" isn't brief.** Every run produced ~1,500 words. That's a report, not a brief. The Writer has no word budget per format — `output_format: brief` is treated as a label, not a constraint.

**Audience calibration is weak.** `audience: myself` produced third-person, formal, presentation-ready prose — indistinguishable from `audience: executive stakeholders`. The audience input doesn't meaningfully change register or voice.

**Specificity drift in the Writer.** The skills/advice sections drifted to generic AI-era conclusions ("AI/ML and security are durable positions") that apply equally to Google, Amazon, and any other tech company. The Researcher found Microsoft-specific data; the Writer didn't always pull subject-specific insight through to the final layer. The bottom line should have named the self-reinforcing loop (a Microsoft-specific structural finding) rather than restating generic AI-era advice.

**Raw claim IDs leaked into recipe summary display.** The S1–S45 claim identifiers from the Analyzer's internal scaffolding appeared in the `final_output` field of the recipe summary. Users shouldn't see internal pipeline artifacts. This is a display/recipe issue — the content is clean but the wrong field is being surfaced as the summary.

**Section redundancy.** "Three Asymmetries" in the Microsoft brief substantially repeated content already in "Key Points." No dedup pass in the Writer before final output.

**Zero source URLs across all four runs.** Every claim has a source name but no URL for independent verification. Epic 01's success criteria states "No finding enters ResearchOutput without a source URL" — that contract is aspirational, not enforced.

---

## Confidence Accuracy

Well-calibrated overall. Low confidence was assigned correctly to unverifiable claims. The Onward Search concentration risk was appropriately flagged as potentially collapsing multiple "independent" statistics into a single undisclosed methodology. Financial claims anchored to primary sources (FY26 Q2 earnings call, H-1B filings) were rated high-confidence correctly. Medium-confidence claims were clearly labeled throughout.

No evidence of systematic over- or under-confidence. The CLAIMS TO VERIFY flags were accurate — each flagged claim genuinely lacked traceable verification.

---

## Coverage Assessment

CLAIMS TO VERIFY flags fired at the right time for the right claims. No false positives observed.

The zero-URL issue means every claim technically lacks an independently traceable source. The pipeline is handling this correctly in spirit — it flags specific claims with low confidence rather than blanket-flagging everything — but the underlying gap (source URLs not captured) means the high-confidence claims also can't be independently verified without additional research.

No coverage flags that should have fired but didn't were identified.

---

## Action Items

- [ ] Writer: enforce word budget per format — brief ~600 words, report ~1,500, executive summary ~400. Format is a contract, not a label.
- [ ] Writer: strengthen audience calibration — `myself` should shift to direct, first-person, actionable voice; not produce the same register as an external stakeholder brief
- [ ] Writer: add dedup pass before final output — scan for repeated content across sections before writing the closing material
- [ ] Researcher: require URL capture for every claim — source name alone is insufficient for independent verification; Epic 01 success criteria states this is required but it's not being enforced
- [ ] Recipe display: filter raw claim IDs (S1–S45) from recipe summary layer — internal Analyzer scaffolding should not appear in user-facing output
- [ ] Writer: specificity enforcement — when research question names a specific subject, verify final document's bottom line and skills sections are subject-specific, not generic AI-era conclusions
