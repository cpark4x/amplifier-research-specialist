# Epic 07: Presentation Builder Specialist

**Status:** In Progress
**Owner:** Gurkaran Singh
**Contributors:** Gurkaran Singh
**Last Updated:** 2026-03-03

---

## 1. Summary

The Presentation Builder closes the research → write → present chain. It transforms
structured source material (writer output, analysis output, research output, competitive
analysis output, or raw notes) into machine-parseable slide deck blueprints that a
downstream renderer can turn into PPTX, Google Slides, or HTML.

The core differentiator: argument-first structure using proven narrative frameworks
(SCQA/Pyramid, Sparkline, 5-Element Narrative, Discovery), assertion-evidence slides
instead of topic + bullets, and a Ghost Deck stage that no other AI presentation tool uses.

---

## 2. Problem

The pipeline currently covers: gather evidence (Researcher) → draw conclusions (Data
Analyzer) → write prose (Writer). But knowledge workers frequently need the next step:
transform content into a slide presentation.

Every AI presentation tool (Gamma, Tome, Copilot, ChatGPT) produces Title + Bullets
organized by topic, not by argument. They optimize for "get slides faster" when the real
problem is "communicate more effectively."

Without the Presentation Builder, either:
1. The user manually reformats Writer output into slides (slow, inconsistent)
2. A generic AI produces topic-organized bullet decks (low quality, no narrative arc)

---

## 3. Proposed Solution

A focused transformation layer. Single job: read structured source material, decompose
it into a slide-by-slide deck blueprint with narrative arc, assertion-evidence layouts,
speaker notes, and full content tracing.

Pipeline:
1. **Parse Input** — detect input type, number content units, apply "So What?" test
2. **Narrative Framework Selection** — select framework by audience type + purpose
3. **Ghost Deck** — produce title-only slide sequence, apply Newspaper Test
4. **Draft Slides** — fill assertion-evidence content, speaker notes, source references
5. **Appendix** — organize supplementary content linked to main deck
6. **Quality Gate + Synthesize** — run 15-point self-verification checklist, assemble PresentationOutput

Returns `PresentationOutput` — defined in `shared/interface/types.md`.

---

## 4. User Stories

### Implemented

| # | Story | Owner | Created | Contributors | Last Updated |
|---|-------|-------|---------|--------------|--------------|
| 07-01 | Researcher → Writer → Presentation Builder chain | Gurkaran Singh | 2026-03-03 | - | - |

### Future

- E2E validation with all 5 input types (writer-output, analysis-output, researcher-output, competitive-analysis-output, raw-notes)
- E2E validation of all 4 narrative frameworks (SCQA, Sparkline, 5-Element, Discovery)
- Downstream renderer integration (PresentationOutput → PPTX)
- Recipe: `presentation-from-research.yaml` (Researcher → Writer → Presentation Builder chain)

---

## 5. Outcomes

**Success Looks Like:**
- Ghost Deck titles pass the Newspaper Test — titles alone tell a coherent argument
- No slide uses topic-label titles ("Overview", "Key Findings")
- Every content unit accounted for — used in main deck, appendix, or cut with reason
- PresentationOutput passes to a downstream renderer without translation
- Full chain Researcher → Writer → Presentation Builder produces a usable deck blueprint
- Speaker notes include transitions, anticipated objections, and confidence qualifiers

**We'll Measure:**
- Newspaper Test pass rate: slide titles in sequence form a coherent argument
- Content coverage: content_map count = main deck sources + appendix sources + unused content count
- Framework adherence: selected narrative arc followed through the deck
- Assertion quality: zero topic-label titles in output

---

## 6. Dependencies

**Requires:** Amplifier Foundation, source material from upstream specialists (Researcher, Writer, Data Analyzer, Competitive Analysis) or raw notes

**Enables:**
- Full research → present pipeline (Researcher → Writer → Presentation Builder)
- Competitive deck pipeline (Researcher → Competitive Analysis → Presentation Builder)
- Any workflow requiring structured slide output from existing content

**Blocks:**
- Downstream renderer tool (PresentationOutput → PPTX/Google Slides/HTML)

---

## 7. Open Questions

- [ ] Should the Sparkline framework be more prescriptive about oscillation structure, or is the current description sufficient for models to execute well?
- [ ] Is the Content Map tracking practical at scale (30+ content units), or does it need simplification?
- [ ] Should the specialist accept a `theme` or `style` hint to pass through to the downstream renderer?

---

## 8. Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-03-03 | Gurkaran Singh | Initial epic |
