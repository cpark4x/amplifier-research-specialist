# Data Analyzer Specialist — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task.

**Goal:** Build the Data Analyzer specialist — an inference layer that sits between Researcher and Writer, drawing labeled conclusions from ResearchOutput and handing them back in AnalysisOutput.

**Architecture:** 8 independent files to create/modify + 1 smoke test. Tasks 1–4 and 8 are fully independent and can run in parallel. Tasks 5–7 require Task 2 to exist first. Task 9 requires everything.

**Design doc:** `docs/plans/2026-03-02-data-analyzer-design.md`

---

## Task 1: Add AnalysisOutput to `shared/interface/types.md`

**Files:**
- Modify: `shared/interface/types.md`

**Step 1: Read the file first**
```bash
cat shared/interface/types.md
```

**Step 2: Add AnalysisOutput after the CompetitiveAnalysisOutput section**

Find this text (end of file, before Schema Version):
```
---

## Schema Version
```

Insert this block immediately before it:

```markdown
## AnalysisOutput

The canonical output of the Data Analyzer specialist.

```typescript
interface AnalysisOutput {
  // What was analyzed
  question: string
  focus_question: string | null   // null if not provided by caller
  quality_threshold: 'low' | 'medium' | 'high'

  // Findings passed through from ResearchOutput — unchanged, numbered F1...Fn
  findings: AnalysisFinding[]

  // The inference layer — new work by the Analyzer
  inferences: Inference[]

  // Findings that didn't yield inferences — every finding is accounted for
  unused_findings: UnusedFinding[]

  // Passed through from ResearchOutput — unchanged
  evidence_gaps: EvidenceGap[]   // reuse from ResearchOutput

  // Overall signal
  quality_score: 'low' | 'medium' | 'high'
  quality_threshold_met: boolean
}

interface AnalysisFinding {
  id: string                    // "F1", "F2", "F3"...
  claim: string                 // from ResearchOutput.Finding.claim — unchanged
  source_url: string
  source_tier: 'primary' | 'secondary' | 'tertiary'
  confidence: 'high' | 'medium' | 'low'
  is_direct_quote: boolean
}

interface Inference {
  claim: string                 // the conclusion — specific and falsifiable
  type: 'pattern' | 'causal' | 'evaluative' | 'predictive'
  confidence: 'high' | 'medium' | 'low'
  traces_to: string[]           // finding IDs: ["F3", "F7", "F12"]
}

interface UnusedFinding {
  finding_id: string            // "F5"
  reason: 'contradicted' | 'insufficient_evidence' | 'out_of_scope'
  detail: string                // one sentence explaining why
}
```
```

**Step 3: Verify the section was added**
```bash
grep -n "AnalysisOutput\|AnalysisFinding\|UnusedFinding\|Inference" shared/interface/types.md
```
Expected: 8+ matches across the new section.

**Step 4: Commit**
```bash
git add shared/interface/types.md
git commit -m "feat: add AnalysisOutput schema to shared interface types"
```

---

## Task 2: Create `specialists/data-analyzer/index.md`

**Files:**
- Create: `specialists/data-analyzer/index.md`

**Step 1: Create the directory**
```bash
mkdir -p specialists/data-analyzer
```

**Step 2: Create the file with this exact content**

```markdown
---
meta:
  name: data-analyzer
  description: |
    Inference specialist that draws labeled analytical conclusions from ResearchOutput.
    Takes sourced facts and produces AnalysisOutput — findings passed through unchanged
    plus explicit inferences that trace to specific findings. Use when you need facts
    and inferences explicitly separated before writing.

    **MUST be used for:**
    - Drawing inferences from research findings before passing to Writer
    - Explicitly labeling what is fact vs. what is concluded from the evidence

    <example>
    user: 'Analyze the research findings on enterprise AI market consolidation'
    assistant: 'I will delegate to specialists:data-analyzer with the ResearchOutput to draw labeled inferences.'
    <commentary>Returns AnalysisOutput — findings passthrough + labeled inferences traceable to specific findings. Writer consumes this as analysis-output input type.</commentary>
    </example>
---

# Data Analyzer

You are a **senior analyst**. Your job is to draw explicit, labeled conclusions from
sourced research findings — and hand those conclusions back alongside the original facts.

You do not research. You do not write prose. You analyze what's already been found.

---

## Core Principles

**Inference authority with attribution obligation.** You are the only specialist
explicitly authorized to say "based on this evidence, I conclude X." But every
conclusion must trace to specific findings. If you can't trace it, you don't say it.

**Every finding is accounted for.** Either a finding appears in an inference's
`traces_to` list, or it appears in UNUSED FINDINGS with a reason. Nothing is
silently omitted. An honest "insufficient evidence" is more valuable than a
forced conclusion.

**Facts and inferences never mix.** Findings are passed through unchanged — not
paraphrased, not upgraded. Inferences are clearly labeled as inferences. These live
in separate output sections.

**Fails loud, not silent.** When findings don't support confident inferences, that is
stated explicitly. The caller asked for analysis; if the evidence is thin they need
to know — not a confident-sounding output that isn't warranted.

---

## Pipeline

Run every task through these stages in order. Do not skip stages.

### Stage 1: Parse

1. Number each finding from ResearchOutput: F1, F2, F3...
2. Note confidence level of each finding (high / medium / low)
3. Note which sub-questions are well-evidenced (2+ findings) vs. thin (1 or zero)
4. If `focus_question` provided: identify which findings are relevant to it;
   note the rest as lower priority but still process them
5. Note the `quality_threshold` (default: `medium` if not provided)
6. State your parse summary before proceeding:
   ```
   Parsed: [n] findings | [n] sub-questions | focus=[question or "full research"] | threshold=[level]
   ```

### Stage 2: Analyze

Work through all findings, looking for inference opportunities.

For each cluster of related findings:

1. Attempt to draw an inference — what conclusion do these findings, taken together, support?

2. If the evidence supports a conclusion at or above `quality_threshold`:
   - State the inference as a clear, specific, falsifiable claim
   - Assign confidence:
     - `high` — 2+ high/medium findings from independent sources confirm it
     - `medium` — 1 high finding or 2 medium findings support it
     - `low` — only low-confidence findings support it
   - Assign type:
     - `pattern` — multiple findings pointing the same direction
     - `causal` — a finding that explains another ("X because Y")
     - `evaluative` — a judgment the evidence supports ("X is strong/weak/ready/not-ready")
     - `predictive` — a forward-looking conclusion the evidence warrants
   - Record the specific finding IDs it traces to (e.g., F3, F7, F12)

3. If the evidence does NOT support a confident inference:
   - Mark the findings as unused
   - Record reason: `contradicted` | `insufficient_evidence` | `out_of_scope`
   - State why in one sentence

**Never force an inference.** An honest unused finding is more valuable than a
fabricated conclusion.

### Stage 3: Quality Gate

Before synthesizing:

1. **Traceability check:** Does every inference trace to at least one finding at or above
   `quality_threshold`? If not — downgrade confidence or drop the inference.

2. **Coverage check:** Is every finding accounted for — either used in an inference
   (`traces_to`) or listed as unused? If any are missing — add them to unused findings.

3. **Contradiction check:** Are any inferences contradicted by other findings? If yes —
   note the contradiction, lower confidence, or drop.

4. **Threshold check:** If `quality_threshold: high` and inferences only trace to
   medium/low findings — return `QUALITY THRESHOLD RESULT: NOT MET`. Do not silently
   return lower-quality output.

### Stage 4: Synthesize

Assemble AnalysisOutput. Return this exact structure — no narrative prose:

```
ANALYSIS BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━
Question: [original question from ResearchOutput]
Focus: [focus_question value, or "full research" if not provided]
Findings received: [n]
Inferences drawn: [n]
Quality score: [low | medium | high]

FINDINGS
F1: claim: [exact text] | source: [URL] | tier: [primary|secondary|tertiary] | confidence: [high|medium|low]
F2: ...
[one line per finding]

INFERENCES
inference: [claim] | type: [pattern|causal|evaluative|predictive] | confidence: [high|medium|low] | traces_to: [F3, F7, F12]
[one line per inference — or "none" if no inferences could be drawn]

UNUSED FINDINGS
F5: reason: contradicted — conflicts with F8, no tiebreaker source available
F14: reason: insufficient_evidence — single tertiary source, corroboration not found
[one line per unused finding — or "none" if all findings yielded inferences]

EVIDENCE GAPS
[passthrough from ResearchOutput evidence_gaps, unchanged — or "none"]

QUALITY THRESHOLD RESULT: [MET | NOT MET]
```

---

## What You Do Not Do

- Research new facts — that is the Researcher's job
- Write prose or narratives — that is the Writer's job
- Draw inferences without traceable findings — no ungrounded conclusions
- Silently omit findings — every finding is accounted for in INFERENCES or UNUSED FINDINGS
- Upgrade finding confidence — the Researcher's ratings are preserved unchanged
- Reorganize or theme findings — document structure is the Writer's job
```

**Step 3: Verify the file was created**
```bash
wc -l specialists/data-analyzer/index.md
```
Expected: 130+ lines

**Step 4: Commit**
```bash
git add specialists/data-analyzer/index.md
git commit -m "feat: add Data Analyzer specialist (index.md)"
```

---

## Task 3: Create `specialists/data-analyzer/README.md`

**Files:**
- Create: `specialists/data-analyzer/README.md`

**Step 1: Create the file with this exact content**

```markdown
# Data Analyzer

Takes ResearchOutput and produces AnalysisOutput — findings passed through unchanged
plus labeled inferences drawn from the evidence. Sits between Researcher and Writer
in the pipeline.

---

## Accepts

| Field | Required | Type | Description |
|---|---|---|---|
| `research` | Yes | ResearchOutput | Output from the Researcher specialist |
| `focus_question` | No | string | Aim inferences at a specific question. If omitted, analyzes all findings. |
| `quality_threshold` | No | `low \| medium \| high` | Minimum confidence for inferences. Default: `medium` |

---

## Returns

`AnalysisOutput` — defined in `shared/interface/types.md`

Key sections:
- **FINDINGS** — all findings from ResearchOutput, passed through unchanged and numbered F1...Fn
- **INFERENCES** — conclusions drawn from the evidence, each with type, confidence, and finding IDs they trace to
- **UNUSED FINDINGS** — findings that didn't yield an inference, with the reason why
- **EVIDENCE GAPS** — passed through from ResearchOutput, unchanged
- **QUALITY THRESHOLD RESULT** — MET or NOT MET

---

## Can Do

- Draw pattern, causal, evaluative, and predictive inferences from research findings
- Rate inference confidence based on underlying finding confidence
- Identify which findings don't support inferences and explain why
- Focus inference work on a specific question via `focus_question`
- Accept any ResearchOutput regardless of domain (market, person, technical, event)

---

## Cannot Do

- Research new facts — use Researcher
- Write prose or produce documents — use Writer
- Draw inferences without traceable findings
- Guarantee inferences when evidence is thin — will return NOT MET rather than force conclusions

---

## Design Notes

**Findings are passed through unchanged.** The Researcher's sourcing, tier, and
confidence ratings are preserved exactly. The Data Analyzer does not re-source,
re-tier, or modify finding confidence.

**Every finding is accounted for.** Either a finding appears in an inference's
`traces_to` field, or it appears in UNUSED FINDINGS with a reason. This is how
callers verify analytical completeness.

**Takes longer by design.** The Quality Gate reviews inference traceability before
output is returned. Speed is not the optimization target — inference trustworthiness is.

---

## Downstream

**Writer** consumes AnalysisOutput as input type `analysis-output`. When it sees
this input type:
- Findings are treated with their Researcher confidence ratings (high/medium/low)
- Inferences are presented as labeled conclusions in prose ("the evidence suggests...")
- CITATIONS distinguishes facts from inferences (`type: inference`)
```

**Step 2: Verify**
```bash
grep -n "Accepts\|Returns\|Can Do\|Cannot Do" specialists/data-analyzer/README.md
```
Expected: 4 matches

**Step 3: Commit**
```bash
git add specialists/data-analyzer/README.md
git commit -m "feat: add Data Analyzer README (interface contract)"
```

---

## Task 4: Update Writer for `analysis-output` input type

**Files:**
- Modify: `specialists/writer/index.md`

Three targeted edits. Read the file first.

---

### Edit A — Stage 1 Step 2: Add `analysis-output` to input types

Find:
```
2. Identify input type: `researcher-output` | `analyst-output` | `raw-notes`
```

Replace with:
```
2. Identify input type: `researcher-output` | `analyst-output` | `raw-notes` | `analysis-output`
```

---

### Edit B — Stage 1 Step 5: Add confidence handling for `analysis-output`

Find:
```
   - If input type is `researcher-output`: read the `confidence` field from the corresponding Finding
   - If input type is `analyst-output` or `raw-notes`: mark every claim as `unrated`
```

Replace with:
```
   - If input type is `researcher-output`: read the `confidence` field from the corresponding Finding
   - If input type is `analyst-output` or `raw-notes`: mark every claim as `unrated`
   - If input type is `analysis-output`:
     - For findings (F1, F2...): read confidence from the finding's confidence field (high|medium|low)
     - For inferences: mark as `confidence: inference` — these are labeled conclusions, not unrated facts
```

---

### Edit C — Stage 4: Add inference prose guidance

Find:
```
- Do not add interpretation beyond what the source material contains
```

Replace with:
```
- Do not add interpretation beyond what the source material contains
- For inferences from `analysis-output` input: the Analyzer has already done the
  interpretive work. Present each inference as a conclusion the evidence supports —
  not as established fact. Use framing like "the evidence suggests...", "this points
  to...", "based on [X], it appears...". Never present an inference as a sourced fact.
```

---

### Edit D — Stage 5 Step 6: Add inference handling in CITATIONS

Find:
```
   Every Sn that appears in an attribution line must appear in the CITATIONS block.
```

Replace with:
```
   Every Sn that appears in an attribution line must appear in the CITATIONS block.
   For `analysis-output` input: inferences appear in CITATIONS with `type: inference`:
     Sx: "[inference claim]" → used in: [section] | type: inference | confidence: high (0.9)
   Use the numeric mapping as normal (high→0.9, medium→0.6, low→0.3) but add `type: inference`
   to distinguish these from sourced facts.
```

---

### Edit E — Stage 5 Step 8: Expand CLAIMS TO VERIFY to cover analysis-output

Find:
```
8. Produce the CLAIMS TO VERIFY block — only when `input type` is `analyst-output`
   or `raw-notes`. When input type is `researcher-output`, skip this step entirely.
```

Replace with:
```
8. Produce the CLAIMS TO VERIFY block — only when `input type` is `analyst-output`,
   `raw-notes`, or `analysis-output`. When input type is `researcher-output`, skip
   this step entirely.
   For `analysis-output`: flag both unrated findings AND any inferences containing
   specific numerical values, measurements, percentages, or named statistics.
```

---

**Verify all 5 edits landed:**
```bash
grep -n "analysis-output" specialists/writer/index.md
```
Expected: 5+ matches

**Commit:**
```bash
git add specialists/writer/index.md
git commit -m "feat: add analysis-output input type to Writer specialist"
```

---

## Task 5: Register in `behaviors/specialists.yaml`

**Files:**
- Modify: `behaviors/specialists.yaml`

**Step 1: Read the file first**
```bash
cat behaviors/specialists.yaml
```

**Step 2: Add data-analyzer to agents.include**

Find:
```yaml
    - specialists:competitive-analysis
```

Replace with:
```yaml
    - specialists:competitive-analysis
    - specialists:data-analyzer
```

**Step 3: Verify**
```bash
grep "data-analyzer" behaviors/specialists.yaml
```
Expected: 1 match

**Step 4: Commit**
```bash
git add behaviors/specialists.yaml
git commit -m "feat: register data-analyzer in specialists behavior bundle"
```

---

## Task 6: Add to `context/specialists-instructions.md`

**Files:**
- Modify: `context/specialists-instructions.md`

**Step 1: Read the file first**
```bash
cat context/specialists-instructions.md
```

**Step 2: Add data-analyzer to Available Specialists list**

Find:
```
- **competitive-analysis** — Transforms a question or existing research into structured
  competitive intelligence. Returns a machine-parseable `CompetitiveAnalysisOutput` with
  comparison matrices, positioning gaps, and win conditions. Handles head-to-head and
  landscape modes. Output is designed for downstream agents (Writer) to consume.
```

Replace with:
```
- **competitive-analysis** — Transforms a question or existing research into structured
  competitive intelligence. Returns a machine-parseable `CompetitiveAnalysisOutput` with
  comparison matrices, positioning gaps, and win conditions. Handles head-to-head and
  landscape modes. Output is designed for downstream agents (Writer) to consume.

- **data-analyzer** — Draws labeled inferences from ResearchOutput. Returns
  `AnalysisOutput` — findings passed through unchanged plus explicit inferences that
  each trace to specific findings. Use between Researcher and Writer when you need
  facts and conclusions explicitly separated.
```

**Step 3: Add when-to-use section**

Find:
```
**Delegate to `specialists:competitive-analysis` when:**
```

Add this block immediately before it:
```
**Delegate to `specialists:data-analyzer` when:**
- You have ResearchOutput and need conclusions drawn before writing
- You want facts and inferences explicitly separated and labeled
- The Writer needs more than raw findings — it needs "what the evidence means"
- Any Researcher → Analyzer → Writer chain

```

**Step 4: Add data-analyzer to the Typical Chain section**

Find:
```
For most knowledge work tasks:
1. `specialists:researcher` → gathers and validates evidence
2. `specialists:writer` → transforms evidence into the requested document
```

Replace with:
```
For most knowledge work tasks:
1. `specialists:researcher` → gathers and validates evidence
2. `specialists:writer` → transforms evidence into the requested document

For analytical tasks requiring explicit fact/inference separation:
1. `specialists:researcher` → gathers and validates evidence
2. `specialists:data-analyzer` → draws labeled inferences from the evidence
3. `specialists:writer` → transforms facts + labeled inferences into the requested document
```

**Step 5: Verify**
```bash
grep -n "data-analyzer" context/specialists-instructions.md
```
Expected: 3+ matches

**Step 6: Commit**
```bash
git add context/specialists-instructions.md
git commit -m "feat: add data-analyzer to specialists dispatch guide"
```

---

## Task 7: Add to root `README.md`

**Files:**
- Modify: `README.md`

**Step 1: Read the file first**
```bash
cat README.md
```

**Step 2: Find the specialists table and add data-analyzer**

Find the row:
```
| [competitive-analysis](specialists/competitive-analysis/) | ...
```

Add after it:
```
| [data-analyzer](specialists/data-analyzer/) | Draws labeled inferences from ResearchOutput — fills the fact/inference gap between Researcher and Writer | v1 |
```

**Step 3: Verify**
```bash
grep "data-analyzer" README.md
```
Expected: 1 match

**Step 4: Commit**
```bash
git add README.md
git commit -m "docs: add data-analyzer to root specialists table"
```

---

## Task 8: Create Epic file

**Files:**
- Create: `docs/02-requirements/epics/08-data-analyzer.md`

**Step 1: Create the file with this exact content**

```markdown
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
1. **Parse** — number all findings F1...Fn, note confidence, note focus if provided
2. **Analyze** — attempt inferences from clusters of related findings
3. **Quality Gate** — verify every inference traces, every finding is accounted for
4. **Synthesize** — assemble AnalysisOutput

Returns `AnalysisOutput` — defined in `shared/interface/types.md`.

---

## 4. User Stories

### Implemented

| # | Story | Owner | Created | Contributors | Last Updated |
|---|-------|-------|---------|--------------|--------------|

**None yet — to be added as stories are implemented.**

### Future

- ✏️ **Researcher → Data Analyzer → Writer chain** — full end-to-end pipeline
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
- Finding coverage: FINDINGS count = INFERENCES traces_to count + UNUSED FINDINGS count
- Chain quality: Researcher → Analyzer → Writer produces a document without human editing

---

## 6. Dependencies

**Requires:** Amplifier Foundation, ResearchOutput from Researcher specialist

**Enables:**
- Researcher → Data Analyzer → Writer chain (core pipeline)
- Any workflow requiring explicit fact/inference separation

---

## 7. Open Questions

- [ ] Should AnalysisOutput include a fast-parse ANALYSIS BRIEF summary block at the top (mirroring RESEARCH BRIEF)? Already included in current design — confirm this is the right call.
- [ ] Should the Analyzer accept CompetitiveAnalysisOutput as well as ResearchOutput? Or is that a separate specialist's job?

---

## 8. Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.0 | 2026-03-02 | Chris Park | Initial epic |
```

**Step 2: Verify**
```bash
wc -l docs/02-requirements/epics/08-data-analyzer.md
```
Expected: 80+ lines

**Step 3: Commit**
```bash
git add docs/02-requirements/epics/08-data-analyzer.md
git commit -m "docs: add Epic 08 — Data Analyzer specialist"
```

---

## Task 9: Smoke Test

Run after all previous tasks are complete.

**Step 1: Verify all files exist**
```bash
ls specialists/data-analyzer/
# Expected: index.md  README.md

grep "data-analyzer" behaviors/specialists.yaml
# Expected: 1 match

grep "data-analyzer" context/specialists-instructions.md
# Expected: 3+ matches

grep "analysis-output" specialists/writer/index.md
# Expected: 5+ matches

grep "AnalysisOutput" shared/interface/types.md
# Expected: 5+ matches
```

**Step 2: Invoke the Data Analyzer with a test input**

Delegate to the specialist with minimal ResearchOutput:
```
delegate(
  agent="specialists:data-analyzer",
  instruction="""
  Analyze these research findings:

  Research question: What is the state of open-source LLM adoption in enterprise?

  Findings:
  - Claim: 67% of enterprise AI teams report using at least one open-source LLM in production
    Source: https://example.com/survey2025  Tier: secondary  Confidence: medium
  - Claim: Llama 3 is the most deployed open-source model, cited by 44% of respondents
    Source: https://example.com/survey2025  Tier: secondary  Confidence: medium
  - Claim: Security and data privacy are cited as the primary reason for preferring open-source
    Source: https://example.com/cto-interviews  Tier: primary  Confidence: high
  - Claim: Microsoft and Meta both report enterprise customers requesting on-premises deployment
    Source: https://example.com/earnings  Tier: primary  Confidence: high
  - Claim: Average fine-tuning cost dropped 73% between 2023 and 2025
    Source: https://example.com/blog  Tier: tertiary  Confidence: low

  quality_threshold: medium
  """
)
```

**Step 3: Verify output structure**

The response MUST contain:
- `ANALYSIS BRIEF` block with question, findings received, inferences drawn, quality score
- `FINDINGS` section with F1...Fn numbered entries
- `INFERENCES` section with at least one inference containing `traces_to: [F...]`
- `UNUSED FINDINGS` section (F5 with the tertiary low-confidence finding should appear here)
- `QUALITY THRESHOLD RESULT: MET`

**Step 4: Verify inference traceability**

Check manually:
- Does every inference reference finding IDs?
- Is F5 (low confidence blog finding) in UNUSED FINDINGS since quality_threshold is medium?
- Is F3 (primary, high confidence, security motivation) used in at least one inference?

**Step 5: Quick Writer chain test**

Pass the AnalysisOutput to the Writer:
```
delegate(
  agent="specialists:writer",
  instruction="Transform the following AnalysisOutput into a brief for enterprise technology leaders.
  [paste AnalysisOutput from Step 2]
  Format: brief. Audience: enterprise CTO."
)
```

Verify Writer output:
- WRITER METADATA shows `Input type: analysis-output`
- Inferences appear in prose with hedged framing ("the evidence suggests...", "this points to...")
- CITATIONS includes entries with `type: inference` for inference-sourced claims
- CLAIMS TO VERIFY fires for the specific numerical claim ("73% cost drop") from the inference or findings

**Step 6: Final commit if any fixes were made**
```bash
git status
# Should be clean. If any fixes were needed, commit them with:
# git commit -m "fix: [description of what needed fixing during smoke test]"
```
