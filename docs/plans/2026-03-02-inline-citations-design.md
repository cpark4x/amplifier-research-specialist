# Inline Citations Design — Section-Level Source Attribution

**Date:** 2026-03-02
**Status:** Approved
**Goal:** Add claim-level trust signals to writer output that work for both human readers and downstream agents.

---

## Problem

The current WRITER METADATA block provides document-level trust ("Coverage: full, gaps: none"). It does not provide claim-level trust — a reader or agent cannot tell, while reading a specific section, whether the claims there are source-backed without consulting the post-doc CITATIONS section separately.

The primary trust signal needed: **"what backed this section?"** visible at the point of reading.

---

## Design Decision

**Rejected: Sentence-level inline markers `[S1]`**
LLMs write prose fluidly and consistently fail to interrupt sentences with markers — proven in prior implementation attempt. Clutters prose and feels academic.

**Chosen: Section-level source attribution blockquotes**

After each section of the document, the writer appends a lightweight attribution line:

```
> *Sources: S1 (pipeline stages), S2 (coverage audit)*
```

This serves both audiences:
- **Human reader**: finishes a section, immediately sees what backed it — no need to flip to end
- **Agent/developer**: parseable blockquote pattern, consistent across all sections

---

## Output Structure

Every writer response has three layers (in order):

**Layer 1 — WRITER METADATA block** (document-level trust)
```
WRITER METADATA
Specialist: writer
...
Coverage: full
Coverage gaps: none
```

**Layer 2 — Document with section attribution** (claim-level trust)
```markdown
## Section Heading

Prose drawn from source material...

> *Sources: S1 (exact quote ≤10 words), S3 (exact quote ≤10 words)*

## Next Section

More prose...

> *Sources: S2 (exact quote ≤10 words)*
```

**Layer 3 — CITATIONS index** (agent/programmatic trust)
```
CITATIONS
S1: "full source claim text" → used in: [Section Heading]
S2: "full source claim text" → used in: [Next Section]
S3: "full source claim text" → used in: [Section Heading]
```

---

## Attribution Line Rules

- Format: `> *Sources: Sn (brief label), Sn (brief label)*`
- The brief label is 3–6 words from the source claim — enough to identify it at a glance
- Appears after every section that contains factual claims
- Sections with no factual claims (e.g. pure transitions) do not get an attribution line
- If a section draws on more than 4 source claims, group by theme: `> *Sources: S1–S3 (pipeline), S5 (quality gate)*`

---

## Changes Required

### `specialists/writer/index.md`

1. **Stage 1**: No change — source claim numbering already in place (S1, S2, S3...)

2. **Stage 4 (Draft)**: Add instruction — after drafting each section, append the attribution blockquote before moving to the next section. Write the section, then immediately note which source claims it drew from.

3. **Stage 5 (Verify & Cite)**: Add check — every section with factual content has an attribution line. Every Sn referenced in attribution lines appears in the CITATIONS block.

4. **Output Format template**: Update to show attribution blockquotes in the document body example.

### `specialists/writer/README.md`

- Update Returns section to describe the section-level attribution lines as part of the output contract.

---

## What Does Not Change

- Post-doc CITATIONS block: retained as-is (agent-parseable full index)
- WRITER METADATA block: retained as-is (document-level trust)
- Source claim numbering (S1, S2...): retained as-is
- All pipeline stages 1, 2, 3: unchanged

---

## Success Criteria

1. Writer output contains `> *Sources: ...*` after every factual section
2. Every Sn in attribution lines appears in the CITATIONS block with full text
3. Prose reads naturally — attribution lines feel like footnotes, not academic clutter
4. A developer can grep for `^> \*Sources:` to extract all section-level citations programmatically
