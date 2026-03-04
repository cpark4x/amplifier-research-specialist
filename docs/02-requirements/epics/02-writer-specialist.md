# Epic 02: Writer Specialist

**Status:** Complete  
**Owner:** Chris Park  
**Contributors:** Chris Park  
**Last Updated:** 2026-03-03  

<!--
Derive ownership and history from git - don't guess or assume:

Contributors by commit count:
git log --format="%an" -- specialists/writer/ | sort | uniq -c | sort -rn

Full history with dates:
git log --format="%ad %an - %s" --date=short -- specialists/writer/
-->

---

## 1. Summary

The Writer Specialist transforms structured source material into polished prose in the requested format. It accepts researcher output, analyst output, or raw notes and returns a format-faithful document with full citation mapping — without generating claims beyond what the source contains. This closes the Researcher → Writer handoff and validates that specialist output can chain without human editing in the middle.

---

## 2. Problem

When an orchestrator has research output, it has no structured way to turn that evidence into a polished document. Doing it inline produces three consistent failures: poor format fidelity (a "brief" that reads like a report), silent gap handling (important omissions aren't surfaced before the document is written), and no traceability (no way to verify that every claim in the output actually came from source material).

The result is documents that look authoritative but can't be audited — the same trust problem the Researcher was built to solve, now appearing downstream in the writing step.

---

## 3. Proposed Solution

A Writer specialist that runs a 5-stage pipeline before returning a document:

1. **Parse Input** — identify input type, requested format/audience/voice, and label every discrete factual claim in the source (S1, S2, S3…)
2. **Audit Coverage** — map the requested document structure against the source material; surface critical gaps *before* drafting begins
3. **Structure** — apply format-specific conventions (brief ≠ report ≠ executive summary)
4. **Draft** — write prose with inline `[Sn]` citation markers on every factual sentence
5. **Verify & Cite** — confirm every factual claim traces to source; produce post-document CITATIONS section

Every response begins with a machine-readable **WRITER METADATA** block (format, coverage status, gaps) and ends with a **CITATIONS** section mapping each `[Sn]` marker back to the source location.

---

## 4. User Stories

**IMPORTANT:** Only include user stories for IMPLEMENTED features. Do NOT create user story files for future work.

### Implemented

| # | Story | Owner | Created | Contributors | Last Updated |
|---|-------|-------|---------|--------------|--------------| 
| [02-01](../user-stories/02-writer-specialist/02-01-produce-format-faithful-document.md) | Produce format-faithful document from source material | Chris Park | 2026-02-27 | - | - |
| [02-02](../user-stories/02-writer-specialist/02-02-return-writer-metadata-block.md) | Return WRITER METADATA block on every response | Chris Park | 2026-02-27 | - | - |
| [02-03](../user-stories/02-writer-specialist/02-03-surface-coverage-gaps.md) | Surface coverage gaps before drafting begins | Chris Park | 2026-02-27 | - | - |
| [02-04](../user-stories/02-writer-specialist/02-04-citations-and-source-attribution.md) | Citations and source attribution (section attribution + CITATIONS index) | Chris Park | 2026-02-28 | - | 2026-03-02 |

**Date Format:** Always use ISO 8601 format (YYYY-MM-DD).

### Future

- ⏭️ **Citation confidence scoring** — per-claim confidence exposed as structured data in CITATIONS block; no new LLM calls
- ⏭️ **Brand voice / style configuration** — `voice_config` input for prohibited terms, tone directives, required terminology
- ⏭️ **Coverage audit severity levels** — `gap_policy` input lets orchestrators decide what gap severity blocks vs. warns vs. passes
- ⏭️ **Rendering integration** — pipe output to Documentero or Box DocGen for PDF/DOCX

---

## 5. Outcomes

**Success Looks Like:**
- Researcher → Writer chain produces a usable document without human editing in the middle
- Zero claims in output that aren't traceable to source material via `[Sn]` markers
- Coverage gaps are surfaced before drafting — never discovered after the document is written
- Output format matches the requested format on every invocation (brief is a brief, not a report)

**We'll Measure:**
- Coverage audit fires on every task (not skipped for speed)
- WRITER METADATA block is present and complete on every output
- Documents produced by the chain require fewer revisions than inline-written equivalents

---

## 6. Dependencies

**Requires:**
- Epic 01 (Researcher) — Writer consumes `ResearchOutput` as its primary input type
- Epic 08 (Data Analyzer) — Writer also consumes `AnalysisOutput` as input type `analysis-output`; inferences are labeled as conclusions in prose rather than facts

**Enables:**
- Presentation Builder specialist — consumes Writer output as slide source
- Storyteller specialist — same input contract, different output format
- Any orchestrator workflow that needs verified, composable prose from structured evidence

**Blocks:** Nothing currently blocked on Writer completion

---

## 7. Open Questions

- [ ] Should `WRITER METADATA` include a structured `citations_count` field so downstream agents can assess citation density without parsing the full CITATIONS section?
- [ ] When source material confidence is `low`, should the Writer degrade prose confidence signals or flag it in WRITER METADATA?
- [x] **Writer output format compliance for `analysis-output` input** — Parse-line anchor fix (commit a714348) resolved this for structured ANALYSIS OUTPUT block input (PostgreSQL vs MongoDB test: pass). **Partially closed.**
- [ ] **Writer parse-line anchor inconsistency** — Chain test (2026-03-03, graphql-vs-rest) found the parse-line anchor did not trigger when the input was narrative markdown (Data Analyzer's rich analysis document). The anchor fires reliably for canonical ANALYSIS OUTPUT block input but falls back to markdown output for narrative input. The Writer needs to produce the parse line regardless of input format. Consider strengthening Stage 1 to require the parse-line unconditionally as the very first token — independent of whether input appears structured or narrative. *(from test log 2026-03-03)*
