# Epic 08: Data Analyzer Specialist

**Status:** In Progress
**Owner:** Chris Park
**Contributors:** Chris Park
**Last Updated:** 2026-03-02

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

- [ ] Should the Analyzer accept CompetitiveAnalysisOutput as well as ResearchOutput, or is that a separate specialist's job?

---

## 8. Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-03-02 | Chris Park | Initial epic |
