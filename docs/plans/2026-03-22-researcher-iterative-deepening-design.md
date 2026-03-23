# Researcher Iterative Deepening Design

## Goal

Add iterative deepening to the researcher specialist so that when a sub-question has thin evidence coverage, the researcher automatically runs a second targeted search pass before declaring done. This is the second-biggest quality lever (~0.4 pts) and directly addresses the factual depth (6.2) and source quality (6.4) structural gaps identified by the competitive eval.

## Background

The researcher currently does one pass — decompose into sub-questions, search, fetch, extract, corroborate, quality gate. The v1 quality loop added source diversity gates (Stage 2) and coverage dimension checklists (Stage 1) that ensure breadth. But the researcher still doesn't go deeper on thin areas — if a sub-question has only surface-level blog coverage and no practitioner depth, it accepts that and moves on.

The competitive eval showed this clearly: competitors found engineering blogs, conference talks, practitioner accounts, and academic papers that the pipeline missed — not because they searched differently, but because they kept looking when initial results were thin.

Backlog entry (#49): "When evidence gaps are logged and a sub-question has coverage but lacks practitioner depth, automatically run a second targeted search round (engineering blogs, conference talks, internal practice accounts) before declaring done."

## Approach

Add a new "depth check" inside the existing Quality Gate (Stage 6) of `agents/researcher.md`. No new pipeline stages, no new files, no output format changes. Single file change.

## How It Works

The depth check runs after the existing Quality Gate checks (low-confidence claims, closeable gaps, under-sourced sub-questions, source-tier diversity, factual breadth). It evaluates each sub-question for depth.

### Thin Sub-Question Triggers

A sub-question is "thin" if either condition is true:

1. **Source count trigger:** The sub-question has fewer than 3 distinct findings addressing it.
2. **Source tier trigger:** The sub-question has no findings from primary or academic sources (all tertiary/blog).

Both triggers apply — a sub-question with 2 blog posts is thin even if count seems adequate, and a sub-question with 5 tertiary sources but no authoritative ones is thin in quality.

### Targeted Deepening Pass

For each thin sub-question, run a targeted search pass that fills whatever source type is missing:

- **No academic sources** → search arxiv, Google Scholar, conference proceedings for the sub-question topic
- **No official/primary sources** → search official docs, gov sites, vendor pages, specs
- **No practitioner depth** → search engineering blogs, case studies, conference talks, practitioner accounts with specific metrics

The deepening pass is not a fixed strategy — it targets the specific gap for each thin sub-question. A sub-question about WebAssembly security needs arxiv papers. A sub-question about retirement visa requirements needs official embassy docs. A sub-question about team productivity needs practitioner case studies.

### Integration with Existing Quality Gate

- The depth check is a new item in the Stage 6 Quality Gate, after the existing source-tier diversity gate (item 4) and factual breadth gate (item 5)
- Max 1 deepening pass per Quality Gate cycle. The Quality Gate already has a max of 3 cycles, so worst case the deepening pass runs 3 times
- If the deepening pass finds new sources, they go through the normal extract → corroborate flow before the Quality Gate re-evaluates

## Scope

### Changes

- `agents/researcher.md` — add the depth check as a new item (item 6) in the Stage 6 Quality Gate

### No Changes To

- No new pipeline stages
- No new recipe files
- No changes to any other specialist or agent file
- No changes to the output format
- No changes to the Planner's question-type classifier or coverage checklists

### What This Does NOT Do

- Does not add a separate "second pass" stage to the pipeline
- Does not change how the researcher searches on the initial pass
- Does not change the output format or add new metadata fields

## Testing Strategy

1. **Structural test:** Confirm the depth check language exists in the Quality Gate section of `agents/researcher.md`
2. **Ordering test:** Verify the depth check comes after the existing diversity and breadth gates
3. **Trigger test:** Confirm the thin sub-question triggers (source count < 3, no primary/academic) are documented
4. **Strategy test:** Confirm the targeted deepening strategies (academic, official, practitioner) are documented

## Expected Impact

~0.4 point improvement on the pipeline's composite score, primarily through:

- **Source quality improvement:** thin sub-questions gain authoritative sources
- **Factual depth improvement:** thin sub-questions gain practitioner depth and specific metrics
- **Cascading improvement to analytical insight:** better source material enables better inferences