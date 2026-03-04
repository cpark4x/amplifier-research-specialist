# Epic 03: Storyteller Specialist

**Status:** In Progress
**Owner:** Chris Park
**Contributors:** Chris Park
**Last Updated:** 2026-03-04

---

## 1. Summary

The Storyteller fills the cognitive mode translation gap in the pipeline. The Researcher
gathers sourced facts. The Data Analyzer draws labeled inferences. The Writer turns everything
into a structured document with full coverage. But none of these specialists can transform
analytical output into narrative — a story with dramatic arc, protagonist, stakes, and resolution
that moves an audience to action.

The Storyteller is the specialist explicitly authorized to make **narrative selection decisions**
— choosing which findings are load-bearing for the arc and which to set aside, with documented
rationale.

---

## 2. Problem

The pipeline produces excellent paradigmatic-mode artifacts — sourced findings, labeled
inferences, structured competitive intelligence. But the people who need to act on this
work — executives, boards, stakeholders — often need it in narrative mode: sequential,
causal, emotional. These are not the same cognitive system (Bruner, 1986). You cannot get
from one to the other by reformatting.

Without the Storyteller, either:
1. The analysis ships as-is (the audience doesn't act on it because it's in the wrong
   cognitive mode)
2. Someone rewrites it informally (losing traceability — you can't tell what was selected,
   what was left out, or why)

---

## 3. Proposed Solution

A cognitive mode translation specialist. Single job: take paradigmatic-mode artifacts and
produce narrative-mode artifacts through deliberate structural transformation.

Pipeline:
1. **Parse** — detect input type, extract findings, detect audience and tone
2. **Find the Drama** — identify central dramatic question, select framework (3-axis logic)
3. **Select and Structure** — 7 transformation decisions, build NARRATIVE SELECTION record
4. **Draft** — clean prose, no citation markers
5. **Quality Gate** — structural + craft + auditability checklists, max 2 cycles, fails loud

Returns `StoryOutput` — defined in `shared/interface/types.md`.

**Key design decisions:**
- **Selective narrator, not faithful narrator.** The Writer covers everything. The Storyteller
  selects what serves the arc and documents what was set aside. Different authorization.
- **NARRATIVE SELECTION replaces inline citations.** Citations break narrative transportation.
  Traceability lives in the editorial record, not in the story body.
- **Framework and tone are independent.** Framework (SCQA, three-act, Story Spine, Sparkline,
  kishōtenketsu) determines structure. Tone (trustworthy, dramatic, creative, persuasive)
  determines register. Any framework in any tone.
- **No CLAIMS TO VERIFY block.** The Storyteller only builds its arc from findings it can
  stand behind. Uncertain claims don't become load-bearing story elements.

---

## 4. User Stories

**IMPORTANT:** Only include user stories for IMPLEMENTED features. Do NOT create user story files for future work.

### Implemented

| # | Story | Owner | Created | Contributors | Last Updated |
|---|-------|-------|---------|--------------|--------------| 
| [03-01](../user-stories/03-storyteller/03-01-transform-analysis-to-narrative.md) | Transform analysis into compelling board narrative | Chris Park | 2026-03-04 | - | - |
| [03-02](../user-stories/03-storyteller/03-02-chain-invocation.md) | Invoke Storyteller at end of research chain | Chris Park | 2026-03-04 | - | - |
| [03-03](../user-stories/03-storyteller/03-03-existing-document-narrative.md) | Transform existing document with tone preference | Chris Park | 2026-03-04 | - | - |
| [03-04](../user-stories/03-storyteller/03-04-audit-editorial-choices.md) | Audit editorial choices via NARRATIVE SELECTION | Chris Park | 2026-03-04 | - | - |
| [03-05](../user-stories/03-storyteller/03-05-model-agnostic-cli.md) | Invoke from CLI with any LLM provider | Chris Park | 2026-03-04 | - | - |

### Future

- ⏭️ **Compound tones** — accept compound tone instructions (e.g., "trustworthy but with a dramatic opening"). Single tone only in v1.
- ⏭️ **Structured NARRATIVE SELECTION format** — machine-parseable selection record (like CITATIONS block). Prose rationale only in v1.

---

## 5. Outcomes

**Success Looks Like:**
- Every story has a dramatic question, protagonist, stakes, causal chain, peak moment, resolution (ST1)
- Every finding is accounted for — included with role, or omitted with rationale (ST2)
- Zero fabricated claims in story body (ST3)
- Framework and tone selected independently (ST4)
- AnalysisOutput passes to Storyteller without manual translation (SC1)
- Narrative chain recipe runs end-to-end (SC1)

**We'll Measure:**
- Narrative arc completeness: structural checklist passes on every output
- Selection record completeness: INCLUDED + OMITTED = total findings
- Source fidelity: zero claims not traceable to source material
- Chain quality: Researcher → Formatter → Analyzer → Storyteller produces output without human editing

---

## 6. Dependencies

**Requires:** Amplifier Foundation, source material (AnalysisOutput, ResearchOutput,
CompetitiveAnalysisOutput, or any document)

**Enables:**
- Researcher → Formatter → Analyzer → Storyteller chain (narrative pipeline)
- Any workflow requiring compelling narrative output from analytical input
- `narrative-chain.yaml` recipe

---

## 7. Open Questions

- [ ] **Compound tones** — Should the Storyteller accept compound tone instructions (e.g., "trustworthy but with a dramatic opening")? Deferred to v2. Single tone for v1.
- [ ] **Structured NARRATIVE SELECTION** — Should the selection record use machine-parseable structured format (like the CITATIONS block in Writer)? Deferred to v2. Prose rationale for v1.
- [x] **New recipe or mode flag?** — Should `narrative-chain.yaml` be a new recipe or a mode flag on `research-chain.yaml`? **Resolved 2026-03-04:** new dedicated recipe. Output shape and final-stage prompt are distinct enough to warrant separation.

---

## 8. Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-03-04 | Chris Park | Initial epic |
