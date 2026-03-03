# Data Analyzer Specialist — Design

**Date:** 2026-03-02
**Status:** Approved
**Grounded in:** docs/01-vision/VISION.md, PRINCIPLES.md, SUCCESS-METRICS.md

---

## The Problem

The pipeline has an authorization gap.

The Researcher explicitly refuses to draw inferences — its job is facts only. The Writer
explicitly refuses to add interpretation beyond source material. So nobody in the chain
is authorized to say "based on this evidence, I conclude X."

The result: either the orchestrator does the analytical thinking itself (inline, low
quality), or inferences bleed quietly into the Writer's output unlabeled — which is worse.

---

## The Solution

A focused inference layer. One job:

> **Read sourced facts. Draw labeled conclusions. Hand them back alongside the facts.**

The Data Analyzer is explicitly authorized to say "based on findings F3, F7, F12, I
conclude X." But every conclusion must trace to specific findings. If it can't trace
it, it doesn't say it. Same rule as the Competitive Analysis specialist.

This fills the authorization gap without creating a new trust problem.

---

## Design Principles Applied

**One thing, exceptionally well.** The Analyzer does not organize by themes (that's the
Writer's job), research new facts (that's the Researcher's job), or write prose. It
draws inferences and labels them.

**Inference authority with attribution obligation.** The Analyzer is the only specialist
authorized to say what the evidence means — but it must show its work. Every inference
traces to specific findings. Every finding that didn't yield an inference is listed with
a reason.

**Fails loud, not silent.** When findings don't support a confident inference, that's
stated explicitly — not quietly omitted. The caller asked for analysis; if the evidence
is thin, they need to know.

**Output schema is the contract.** AnalysisOutput is a new stable type in
shared/interface/types.md. It passes cleanly to the Writer without a translation step.

---

## What It Does Not Do

- Organize findings into themes — Writer handles document structure
- Research new facts — Researcher's job
- Draw inferences it can't trace — no ungrounded conclusions
- Silently omit findings that didn't yield inferences — must list them as unused
- Write prose — that is the Writer's job

---

## Input Contract

| Field | Required | Type | Description |
|---|---|---|---|
| `research` | Yes | ResearchOutput | Output from the Researcher specialist |
| `focus_question` | No | string | Sharpen inferences toward a specific question. If omitted, analyzes the full research. |
| `quality_threshold` | No | low \| medium \| high | Minimum confidence for inferences to be included. Default: medium |

---

## Output Contract — `AnalysisOutput`

Self-contained package: findings passed through unchanged + inferences added on top.
The Writer receives AnalysisOutput as a new input type `analysis-output`.

```
ANALYSIS BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━
Question: [what was analyzed]
Focus: [focus_question if provided, or "full research"]
Findings received: [n]
Inferences drawn: [n]
Quality score: [low | medium | high]

FINDINGS
[All findings from ResearchOutput, passed through unchanged]
F1: claim: [...] | source: [...] | tier: [...] | confidence: [...]
F2: ...

INFERENCES
inference: [...] | confidence: [high|medium|low] | traces_to: [F3, F7, F12]
[one line per inference]

UNUSED FINDINGS
F5: reason: contradicted — conflicts with F8, no tiebreaker source available
F14: reason: insufficient evidence — single tertiary source, corroboration not found

EVIDENCE GAPS
[passthrough from ResearchOutput, unchanged]

QUALITY THRESHOLD RESULT: [MET | NOT MET]
```

---

## Pipeline — 4 Stages

### Stage 1: Parse

1. Read all findings from ResearchOutput
2. Number each finding F1, F2, F3... for traceability
3. Note which sub-questions are well-evidenced (2+ findings) vs. thin (1 or zero)
4. If `focus_question` provided: identify which findings are relevant to it
5. State parse summary before proceeding:
   ```
   Parsed: [n] findings | [n] sub-questions | focus=[question or "full"] | quality_threshold=[level]
   ```

### Stage 2: Analyze

For each cluster of related findings:

1. Attempt to draw an inference — what conclusion do these findings, taken together, support?
2. If the evidence supports a conclusion at or above `quality_threshold`:
   - State the inference clearly
   - Assign confidence: high (supported by 2+ high/medium findings from independent sources),
     medium (supported by 1 high or 2 medium findings), low (supported by low-confidence findings only)
   - Record the finding IDs it traces to
3. If the evidence does not support a confident inference:
   - Mark the findings as unused
   - Record the reason: `contradicted` | `insufficient_evidence` | `out_of_scope`
4. Never force an inference — an honest "unused finding" is more valuable than a
   fabricated conclusion

**Inference types to attempt:**
- **Pattern:** multiple findings pointing the same direction ("X is consistently true across sources")
- **Causal:** a finding that explains another ("X because Y")
- **Evaluative:** a judgment the evidence supports ("X is strong/weak/ready/not-ready")
- **Predictive:** a forward-looking conclusion the evidence warrants ("X suggests Y will...")

### Stage 3: Quality Gate

Before synthesizing:

1. Does every inference trace to at least one finding at or above `quality_threshold`?
   If not: downgrade or drop
2. Is every finding accounted for — either used in an inference or listed as unused?
   If not: add to unused findings
3. Are any inferences contradicted by other findings?
   If yes: note the contradiction, lower confidence or drop

If `quality_threshold: high` and inferences only trace to medium/low findings: return
`QUALITY THRESHOLD RESULT: NOT MET` — do not silently return lower-quality output.

### Stage 4: Synthesize

Assemble AnalysisOutput:
- Pass through all findings, unchanged, numbered F1...Fn
- List all inferences with traces
- List all unused findings with reasons
- Pass through evidence gaps from ResearchOutput unchanged
- Record quality score based on confidence distribution of inferences drawn

---

## Writer Integration

Writer receives a new input type: `analysis-output`.

When input type is `analysis-output`, the Writer pipeline changes in one place:

**Stage 1 (Parse):** Number claims as before. For findings: read confidence from
ResearchOutput tier (high/medium/low). For inferences: mark as `inference` with its
stated confidence — do NOT treat inferences as facts.

**Stage 4 (Draft):** When drawing on an inference, label it in prose:
*"The evidence suggests..." / "Based on [X], it appears..." / "This points to..."*
Do not present inferences as established facts.

**Stage 5 (Verify and Cite):** CITATIONS block distinguishes:
- Findings → `confidence: high (0.9)` etc. as normal
- Inferences → `type: inference | confidence: [stated confidence]`

CLAIMS TO VERIFY fires on inferences as well as unrated facts — inferences with specific
numerical values should be flagged.

---

## New Type: AnalysisOutput

To be added to `shared/interface/types.md`:

```typescript
interface AnalysisOutput {
  // What was analyzed
  question: string
  focus_question: string | null
  quality_threshold: 'low' | 'medium' | 'high'

  // Findings passed through from ResearchOutput — unchanged
  findings: AnalysisFinding[]     // ResearchOutput.findings, numbered F1...Fn

  // The inference layer — new work by the Analyzer
  inferences: Inference[]

  // Findings that didn't yield inferences
  unused_findings: UnusedFinding[]

  // Passed through from ResearchOutput — unchanged
  evidence_gaps: EvidenceGap[]

  // Overall signal
  quality_score: 'low' | 'medium' | 'high'
  quality_threshold_met: boolean
}

interface AnalysisFinding {
  id: string                    // F1, F2, F3...
  claim: string                 // from ResearchOutput.Finding.claim
  source_url: string
  source_tier: 'primary' | 'secondary' | 'tertiary'
  confidence: 'high' | 'medium' | 'low'
  is_direct_quote: boolean
}

interface Inference {
  claim: string                 // the conclusion
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

---

## Files to Create / Modify

| Action | File | What |
|---|---|---|
| Create | `specialists/data-analyzer/index.md` | Persona + 4-stage pipeline instructions |
| Create | `specialists/data-analyzer/README.md` | Interface contract (accepts, returns, can/cannot do) |
| Modify | `shared/interface/types.md` | Add AnalysisOutput, Inference, UnusedFinding types |
| Modify | `specialists/writer/index.md` | Add `analysis-output` input type handling |
| Modify | `behaviors/specialists.yaml` | Register `specialists:specialists/data-analyzer` |
| Modify | `context/specialists-instructions.md` | Add data-analyzer to dispatch guide |
| Modify | `README.md` | Add to specialists table |
| Create | `docs/02-requirements/epics/08-data-analyzer.md` | Epic file |

---

## Success Criteria

1. Data Analyzer produces INFERENCES that trace to specific findings
2. Every finding is accounted for — either used or listed as unused with reason
3. AnalysisOutput passes cleanly to Writer as `analysis-output` without translation
4. Writer labels inferences as inferences in prose — not as facts
5. Full chain Researcher → Data Analyzer → Writer produces a usable document
6. Quality threshold: NOT MET fires loud when evidence doesn't support confident inferences
