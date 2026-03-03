# Epic 04: Competitive Analysis Specialist

**Status:** In Progress  
**Owner:** Chris Park  
**Contributors:** Chris Park  
**Last Updated:** 2026-03-02  

<!--
Derive ownership and history from git - don't guess or assume:

Contributors by commit count:
git log --format="%an" -- specialists/competitive-analysis/ | sort | uniq -c | sort -rn

Full history with dates:
git log --format="%ad %an - %s" --date=short -- specialists/competitive-analysis/
-->

---

## 1. Summary

The Competitive Analysis Specialist transforms a competitive question or existing research
into structured competitive intelligence — comparison matrices, positioning gaps, and win
conditions. It handles both head-to-head comparisons (Microsoft vs. Anthropic) and landscape
analysis (who competes with Anthropic?), and accepts existing research to skip its own
research phase. Output is AI-first: machine-parseable data designed for downstream agents
to consume.

---

## 2. Problem

When a knowledge worker needs competitive intelligence, today's specialist chain produces
research findings and narrative prose — but nothing in between. The Researcher returns
sourced facts. The Writer turns those facts into a brief. What's missing is the analysis
layer: structured comparisons, explicitly identified gaps, and win/lose conditions that
make competitive intelligence actionable.

Without a dedicated competitive analysis specialist, every competitive brief is essentially
a narrative summary of research — not a structured comparison. The person reading it has
to extract the competitive picture themselves.

---

## 3. Proposed Solution

A Competitive Analysis specialist that runs a 6-stage pipeline:

1. **Parse Input** — detect mode, subjects, dimensions, research source
2. **Research** (conditional) — gather competitive evidence if no research provided
3. **Profile** — fact-based rating per subject per dimension
4. **Compare** — build comparison matrix, identify patterns and contradictions
5. **Position** — derive win conditions and positioning gaps (labeled as inferences)
6. **Synthesize + Quality Gate** — assemble AI-first output, verify facts/inference separation

Returns `CompetitiveAnalysisOutput` — structured data the Writer consumes directly.

---

## 4. User Stories

**IMPORTANT:** Only include user stories for IMPLEMENTED features. Do NOT create user story files for future work.

### Implemented

| # | Story | Owner | Created | Contributors | Last Updated |
|---|-------|-------|---------|--------------|--------------| 
| [04-01](../user-stories/04-competitive-analysis/04-01-head-to-head-comparison.md) | Head-to-head comparison with structured matrix | Chris Park | 2026-03-02 | - | - |
| [04-02](../user-stories/04-competitive-analysis/04-02-landscape-analysis.md) | Landscape analysis — discover and compare competitive field | Chris Park | 2026-03-02 | - | - |
| [04-03](../user-stories/04-competitive-analysis/04-03-accept-existing-research-output.md) | Accept existing ResearchOutput to skip research phase | Chris Park | 2026-03-02 | - | - |

**Date Format:** Always use ISO 8601 format (YYYY-MM-DD).

### Future

- ⏭️ **Dimension configuration** — caller specifies custom dimensions beyond the defaults
- ⏭️ **Competitive change tracking** — compare two snapshots of a competitive landscape over time
- ⏭️ **Confidence-filtered output** — caller sets minimum confidence threshold for matrix entries

---

## 5. Outcomes

**Success Looks Like:**
- Competitive analysis output has clearly separated facts (matrix, profiles) and inferences (win conditions, gaps)
- Every win condition traces to at least one matrix entry
- Output passes cleanly to Writer without a manual translation step
- Evidence gaps are named, not omitted

**We'll Measure:**
- Facts and inferences are never mixed in the same section
- Output format is machine-parseable line-by-line
- Chain (competitive-analysis → writer) produces a usable brief without human editing in the middle

---

## 6. Dependencies

**Requires:** `tool-web` (web_search + web_fetch), Amplifier Foundation

**Enables:**
- Any knowledge worker workflow requiring structured competitive intelligence
- Writer specialist consuming competitive analysis as source material
- Full chain: Researcher → Competitive Analysis → Writer

**Blocks:** Nothing currently blocked on this epic's completion

---

## 7. Risks & Mitigations

| Risk | Impact | Probability | Strategic Response |
|------|--------|-------------|-------------------|
| Win conditions are inferences that look like facts | M | M | Strict section separation — WIN CONDITIONS always in a separate labeled section from COMPARISON MATRIX |
| Landscape mode has no predefined subjects — specialist may miss key competitors | M | M | Require explicit competitor discovery step in Stage 2 before profiling |
| Research quality varies by subject — well-documented vs. obscure subjects | M | H | Evidence gaps are first-class outputs; unknown ratings always preferable to low-confidence guesses |

---

## 8. Open Questions

- [ ] Should `CompetitiveAnalysisOutput` include a `COMPETITIVE BRIEF` fast-parse summary block at the top, mirroring `RESEARCH BRIEF` in ResearchOutput?
- [ ] For landscape mode, should the specialist cap the number of competitors it discovers and profiles (to avoid unbounded research)?
- [ ] Should the chain encode Researcher as a default first step for product comparisons? The self-research path skips source tiering and confidence scoring — a Researcher pre-pass would surface those explicitly before competitive-analysis runs. *(Surfaced: Notion/Obsidian test, 2026-03-02)*
- [ ] Should the Writer surface a "claims to verify" block when the upstream `CompetitiveAnalysisOutput` contains highly specific numerical claims with no cited source? Currently those claims pass through at uniform confidence. *(Surfaced: Notion/Obsidian test, 2026-03-02)*
- [ ] Should the `competitive-analysis → writer` chain be encoded as a single invokable recipe so callers don't have to manually dispatch both agents? *(Surfaced: Notion/Obsidian test, 2026-03-02)*

---

## 9. Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.1 | 2026-03-02 | Chris Park | Added 3 open questions from live test run (Notion/Obsidian): recipe encoding, researcher-first default, writer confidence gap surfacing |
| v1.0 | 2026-03-02 | Chris Park | Initial epic |
