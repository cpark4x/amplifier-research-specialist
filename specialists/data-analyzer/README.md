# Data Analyzer

Takes ResearchOutput and produces AnalysisOutput — findings projected from ResearchOutput
plus labeled inferences drawn from the evidence. Sits between Researcher and Writer in the
pipeline. The only specialist authorized to draw conclusions from sourced facts.

---

## Accepts

| Field | Required | Type | Description |
|---|---|---|---|
| `research` | Yes | ResearchOutput | Output from the Researcher specialist |
| `focus_question` | No | string | Aim inferences at a specific question. If omitted, analyzes all findings. |
| `quality_threshold` | No | `low \| medium \| high` | Minimum confidence for inferences. Default: `medium`. Note: `maximum` (ResearchOutput vocabulary) is treated as `high`. |

---

## Returns

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
- **QUALITY THRESHOLD RESULT** — `MET` or `NOT MET`

---

## Can Do

- Draw pattern, causal, evaluative, and predictive inferences from research findings
- Rate inference confidence based on the quality of supporting findings
- Identify which findings don't support inferences and explain why
- Focus inference work on a specific question via `focus_question`
- Accept any ResearchOutput regardless of domain (market, person, technical, event)
- Coerce `quality_threshold: maximum` from ResearchOutput vocabulary to `high`

---

## Cannot Do

- Research new facts — use Researcher
- Write prose or produce documents — use Writer
- Draw inferences without traceable findings — no ungrounded conclusions
- Accept raw notes or unstructured input — only processes ResearchOutput
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

---

## Downstream

**Writer** consumes AnalysisOutput as input type `analysis-output`. When it sees
this input type:
- Findings are treated with their Researcher confidence ratings (high→0.9, medium→0.6, low→0.3)
- Inferences are presented as labeled conclusions in prose ("the evidence suggests...", "this points to...")
- CITATIONS distinguishes facts (`confidence: high (0.9)`) from inferences (`type: inference | confidence: ...`)
- CLAIMS TO VERIFY fires for inferences containing specific numerical values
