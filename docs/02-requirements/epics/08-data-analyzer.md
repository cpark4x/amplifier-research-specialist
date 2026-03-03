# Epic 08: Data Analyzer Specialist

**Status:** Complete
**Owner:** Chris Park
**Contributors:** Chris Park
**Last Updated:** 2026-03-03

---

## 1. Summary

The Data Analyzer fills the authorization gap in the Researcher → Writer pipeline.
The Researcher refuses to make inferences (facts only). The Writer refuses to add
interpretation (source fidelity above all). The Data Analyzer is the specialist
explicitly authorized to say "based on this evidence, I conclude X" — with every
conclusion labeled as an inference and traceable to specific findings.

---

## 2. Problem

The Researcher returns sourced facts. The Writer turns facts into prose. But neither
specialist can say what the evidence *means*. The Writer's core principle is source
fidelity — it won't add interpretation beyond what's in the source material.

Without the Data Analyzer, either:
1. The orchestrator does the analytical thinking inline (low quality, no quality gate)
2. Inferences bleed unlabeled into the Writer's output (a trust violation)

**Secondary:** The Data Analyzer also serves direct consumers — humans reviewing
inferences before deciding whether to write a document, or orchestrators making
decisions based on analysis without needing a final document. The chain use case
(→ Writer) is primary; direct use is a valid secondary use case the spec supports.

---

## 3. Proposed Solution

A focused inference layer. Single job: read sourced facts, draw labeled conclusions
traceable to specific findings, hand back findings + conclusions together.

Pipeline:
1. **Parse** — number all findings F1...Fn, note confidence, apply focus_question if provided
2. **Analyze** — attempt inferences from clusters of related findings
3. **Quality Gate** — verify every inference traces, every finding is accounted for
4. **Synthesize** — assemble AnalysisOutput

Returns `AnalysisOutput` — defined in `shared/interface/types.md`.

---

## 4. User Stories

### Implemented

| # | Story | Owner | Created | Contributors | Last Updated |
|---|-------|-------|---------|--------------|--------------|
| 08-01 | Researcher → Data Analyzer → Writer chain | Chris Park | 2026-03-02 | - | - |

### Future

- ✏️ **focus_question parameter** — sharpen inferences toward a specific question
- ✏️ **quality_threshold parameter** — caller controls minimum inference confidence

---

## 5. Outcomes

**Success Looks Like:**
- Every inference in AnalysisOutput traces to specific findings
- Every finding is accounted for — used in an inference or listed as unused with reason
- AnalysisOutput passes to Writer as `analysis-output` without translation
- Writer labels inferences as conclusions in prose, not as facts
- Full chain Researcher → Data Analyzer → Writer produces a usable document

**We'll Measure:**
- Inference traceability: every inference has finding IDs in `traces_to`
- Finding coverage: FINDINGS count = inference traces_to count + UNUSED FINDINGS count
- Chain quality: Researcher → Analyzer → Writer produces a document without human editing

---

## 6. Dependencies

**Requires:** Amplifier Foundation, ResearchOutput from Researcher specialist

**Enables:**
- Researcher → Data Analyzer → Writer chain (core pipeline)
- Any workflow requiring explicit fact/inference separation

---

## 7. Open Questions

- [x] **Should the Analyzer accept CompetitiveAnalysisOutput as well as ResearchOutput?** — **CLOSED 2026-03-03: deferred, no change.** CompetitiveAnalysisOutput has a different structure (comparison matrices, win conditions, positioning gaps) that doesn't map cleanly to the Analyzer's inference-from-findings model. If competitive analysis needs inference drawing, that belongs inside the Competitive Analysis specialist's own pipeline — not as a second input type for the Data Analyzer. Keeping the Analyzer's input contract to ResearchOutput preserves the "one thing, exceptionally well" principle.
- [x] **Format compliance with non-standard input** — ~~Post-build registration test (2026-03-03) with simplified inline findings produced narrative prose.~~ **CLOSED 2026-03-03:** Follow-up test with canonical ResearchOutput format confirmed full compliance — `ANALYSIS OUTPUT / Specialist: data-analyzer / Version: 1.0` block, all sections, `type:` labels on every inference. Prose output was input-format-dependent, not a regression. See `docs/test-log/data-analyzer/2026-03-03-format-compliance.md`.
- [x] **Behavior for non-ResearchOutput input** — **CLOSED 2026-03-03: accepted, no change.** In real pipeline use the Researcher always produces canonical ResearchOutput; informal-input edge cases are testing artifacts, not production scenarios. README already states the contract ("only processes ResearchOutput"). No Stage 0 validation added — keeping the spec minimal.

---

## 8. Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-03-02 | Chris Park | Initial epic |
| v1.2 | 2026-03-03 | Chris Park | Status → Complete; added Tier 2 consumer use case to Problem section; closed CompetitiveAnalysisOutput open question |
| v1.1 | 2026-03-03 | Chris Park | Add open questions from build-session feedback capture |
