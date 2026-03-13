# Evaluation Scoring Rubric

## Three Adversarial Critics

### 1. Fact-Checker (weight: 0.40)

For each finding in the research output:
1. Fetch the source URL
2. Extract page content (first 8000 chars if large)
3. Compare the claim text against the source content

**Verdicts:**
- VERIFIED — source content supports the claim
- MISREPRESENTED — source content exists but claim distorts it
- FABRICATED — source content does not contain or support the claim
- UNREACHABLE — source URL returned error (403, 404, timeout, etc.)

**Score:** verified_count / total_findings × 10
UNREACHABLE findings are excluded from the denominator (they indicate source
access problems, not pipeline quality problems).

### 2. Inference Challenger (weight: 0.35)

For each inference in the analysis output:
1. **Independent derivation:** Give only the supporting findings (traces_to)
   to a fresh evaluator. What conclusions would they draw?
2. **Adversarial challenge:** Present the actual inference and ask for the
   strongest counterargument.
3. **Verdict based on both phases.**

**Verdicts:**
- ROBUST — inference adds genuine analytical lift; counterargument is weak
- SUPPORTED_BUT_OBVIOUS — a competent reader would reach the same conclusion
  from the findings alone (no analytical lift)
- WEAK — inference overclaims, overgeneralizes, or has an equally plausible
  alternative explanation

**Score:** robust_count / total_inferences × 10
OBVIOUS inferences score 0 — they are padding, not analysis.

**Quality criteria (from data-analyzer prompt):**
A robust inference must: (1) add analytical lift, (2) combine 2+ findings,
(3) stay within the evidence, (4) survive challenge. See data-analyzer.md
"Inference Quality Criteria" section for the full rubric.

### 3. Consistency Auditor (weight: 0.25)

For each claim in the writer output:
1. Look up the source confidence (from analysis output findings/inferences)
2. Check whether the prose language matches the confidence level

**Violation types:**
- CONFIDENCE_UPGRADE — LOW or MEDIUM confidence stated as definitive fact
- MISSING_HEDGE — MEDIUM confidence without hedging or source attribution
- INFERENCE_AS_FACT — inference-sourced claim presented without analytical qualifier

**Score:** (1 − violations / total_claims) × 10

**Hedging rules (from writer prompt):**
- HIGH confidence → definitive language OK
- MEDIUM confidence → MUST hedge: "according to...", "reportedly", "suggests"
- LOW confidence → MUST use strong hedges: "unconfirmed reports suggest..."
- Inference-sourced → MUST use analytical qualifier: "analysis suggests..."
See writer.md "HEDGE BY DEFAULT" section for the full rule.

## Composite Score

Per topic: 0.40 × fact_checker + 0.35 × inference_challenger + 0.25 × consistency_auditor

**Content score = MINIMUM composite across ALL topics** (not average).
The pipeline is only as strong as its weakest performance.

## Score History

Each eval run appends to `specs/evaluation/score-history.yaml`:
- timestamp, topic_id, fact_score, inference_score, consistency_score, composite
