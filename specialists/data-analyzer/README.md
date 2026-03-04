# Data Analyzer

A domain expert agent for producing **traceable, labeled inferences from structured research evidence**.

The Data Analyzer's job is precisely: take ResearchOutput and return grounded conclusions —
pattern, causal, evaluative, or predictive — each traced to the findings that support them.
It does not research, and it does not write. It is the only specialist authorized to draw
conclusions from sourced facts.

---

## Interface Contract

### Accepts

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `research` | ResearchOutput | Yes | — | Output from the Researcher specialist. See input format note below. |
| `focus_question` | string | No | null | Aim inferences at a specific question. If omitted, analyzes all findings. |
| `quality_threshold` | `low \| medium \| high` | No | `medium` | Minimum confidence for inferences to be included. |

**Input format note:** Canonical `ResearchOutput` block (Format A — starts with bare
`RESEARCH OUTPUT` on the first line, with `Claim:` / `Source:` / `Tier:` /
`Confidence:` fields) is required for guaranteed `ANALYSIS OUTPUT` block compliance.
Fully-narrative input with explicit `Claim:` / `Source:` / `Tier:` labels (Format B)
is accepted and handled, but output format compliance is not contractually guaranteed.
Partially-canonical input (Format C: section headers + narrative tables without
per-finding labels) may produce narrative output instead of the canonical block.

### Returns

`AnalysisOutput` — defined in `shared/interface/types.md`

Output opens with:
```
ANALYSIS OUTPUT
Specialist: data-analyzer
Version: 1.0
```

Key sections:
- **FINDINGS** — findings projected from ResearchOutput, numbered F1...Fn. Subset of ResearchOutput.Finding fields with Analyzer-assigned IDs.
- **INFERENCES** — conclusions drawn from the evidence. Each has type (pattern/causal/evaluative/predictive), confidence, and the finding IDs they trace to.
- **UNUSED FINDINGS** — findings that didn't yield an inference. Every finding is accounted for here or in INFERENCES.
- **EVIDENCE GAPS** — normalized to single-line `gap: [...] | reason: [...]` format; passthrough from ResearchOutput.
- **QUALITY THRESHOLD RESULT** — `MET` or `NOT MET`. When `NOT MET`, output is still returned and structured normally — callers may use it with awareness that confidence is below the requested floor, lower the threshold, or pass `focus_question` to narrow scope.

### Can Do

- Draw pattern, causal, evaluative, and predictive inferences from research findings
- Rate inference confidence based on the quality of supporting findings
- Identify which findings don't support inferences and explain why
- Focus inference work on a specific question via `focus_question`
- Accept any ResearchOutput regardless of domain (market, person, technical, event)

### Cannot Do

- Research new facts — use Researcher
- Write prose or produce documents — use Writer
- Draw inferences without traceable findings — no ungrounded conclusions
- Guarantee canonical `ANALYSIS OUTPUT` block for non-canonical input — only Format A
  (canonical `ResearchOutput` block) guarantees full compliance. Narrative input is
  accepted but output format compliance is not guaranteed.
- Guarantee inferences when evidence is thin — returns `QUALITY THRESHOLD RESULT: NOT MET` rather than force conclusions

---

## Design Notes

**Every finding is accounted for.** Either a finding appears in an inference's
`traces_to` list, or it appears in UNUSED FINDINGS with a reason. The sum of
inference `traces_to` references plus UNUSED FINDINGS count equals the total
findings received. Callers can verify analytical completeness.

**Findings are projected, not passed through.** The Analyzer assigns IDs (F1, F2...)
and selects a subset of ResearchOutput.Finding fields. The Researcher's confidence
ratings are preserved unchanged. The Analyzer does not re-source or re-tier findings.

**Takes longer by design.** The Quality Gate reviews inference traceability before
output is returned. Speed is not the optimization target — inference trustworthiness is.

**`quality_threshold: maximum` is accepted.** This value (ResearchOutput vocabulary) is treated as `high`. Prevents pipeline breakage when ResearchOutput is passed directly without threshold translation.

---

## Downstream

**Writer** consumes AnalysisOutput as input type `analysis-output`. When it sees
this input type:
- Findings are treated with their Researcher confidence ratings (high→0.9, medium→0.6, low→0.3)
- Inferences are presented as labeled conclusions in prose ("the evidence suggests...", "this points to...")
- CITATIONS distinguishes facts (`confidence: high (0.9)`) from inferences (`type: inference | confidence: ...`)
- CLAIMS TO VERIFY fires for inferences containing specific numerical values
