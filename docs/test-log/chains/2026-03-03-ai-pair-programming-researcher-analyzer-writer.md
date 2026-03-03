---
specialist: researcher → data-analyzer → writer
chain: "researcher → data-analyzer → writer"
topic: ai-pair-programming
date: 2026-03-03
quality_signal: mixed
action_items_promoted: true
---

# Researcher → Data Analyzer → Writer Chain
**Topic:** Should engineering teams adopt AI pair programming tools (GitHub Copilot, Cursor, etc.)?
**Audience:** Engineering leaders at mid-size companies
**Format:** Brief

---

## What Worked

**The chain ran end-to-end for the first time.** All three specialists executed, each
step consumed the previous step's output, and the final brief is publication-quality.

**Data Analyzer: flawless.** Given canonical ResearchOutput input, it produced the full
`ANALYSIS OUTPUT` block perfectly — 14 findings numbered, 7 inferences with explicit
type labels (`pattern`, `causal`, `evaluative`), all findings accounted for, clear
Stage 1–4 pipeline narration, QUALITY THRESHOLD RESULT: MET. This is exactly what the
spec requires.

**The inferences themselves were strong.** The Analyzer correctly identified the
individual-vs.-org divergence (I2), the compounding technical debt causal chain (I3),
and the "mirror and multiplier" moderating condition (I5) — all non-obvious conclusions
that required synthesizing multiple findings.

**The Writer brief was genuinely useful.** The decision framework table, the guardrails
section, and the "most important signal" callout for mid-size companies are the kind of
content an engineering leader would actually act on. Inferences were properly hedged
("the evidence suggests," "this will compound") rather than stated as facts.

**Coverage of evidence gaps was correct.** Both gaps surfaced in the Writer output
under "Evidence Gaps to Monitor" — the onboarding time gap and the longitudinal debt
study gap. The Writer didn't paper over them.

---

## What Didn't / Concerns

### Researcher: format compliance gap
The Researcher produced rich narrative markdown (executive summary, sub-question
sections, embedded tables) instead of the canonical `RESEARCH OUTPUT` block format
specified in the researcher spec (Stage 7: Synthesizer). The canonical format requires:

```
RESEARCH OUTPUT
Question: [...]
Query Type: [...]
Quality Score: [...]

RESEARCH BRIEF:
[5-10 bullets]

SUB-QUESTIONS ADDRESSED:
...

FINDINGS:
- Claim: [...]
  Source: [...]
  Tier: [...]
  Confidence: [...]
...
```

The Researcher's output was high quality as a document but would not be machine-parseable
by a downstream Data Analyzer without manual reformatting (which was done manually for
this test run). In a fully automated pipeline, this would break.

### Writer: format compliance gap
The Writer produced a polished brief but omitted the structural metadata sections
required by the spec:

- No `WRITER METADATA` block (expected: `Input type: analysis-output`, source count,
  format, audience)
- No `CITATIONS` section (expected: inference-sourced claims labeled with
  `type: inference | confidence: ...`)
- No `CLAIMS TO VERIFY` section (expected: specific numerical claims flagged for
  verification — e.g., the 32.8% security vulnerability rate, the 19% slowdown figure)

These are not cosmetic — downstream callers (other specialists, evaluators, or humans
reviewing for accuracy) rely on CITATIONS to distinguish facts from inferences, and on
CLAIMS TO VERIFY to flag what needs human checking before publication.

### Pipeline automation requires manual reformatting today
Because the Researcher output is in narrative format rather than canonical RESEARCH
OUTPUT blocks, the current chain is semi-automated: a human (or the orchestrating
session) must reformat Researcher output before passing it to the Data Analyzer. This
is a gap for fully automated chain runs.

---

## Confidence Accuracy

Generally well-calibrated:
- I1 (productivity conditioned on experience) rated high confidence — appropriate.
  Two RCTs from independent teams, different populations, both high-confidence sources.
- I7 (cost justification) rated medium confidence — appropriate. Depends on F13
  (medium, single secondary source) and the productivity inversion for senior devs.
- No over-confidence observed. Evidence gaps were surfaced correctly.

One minor concern: the Writer's bottom line ("conditionally yes") goes slightly beyond
what a strict reading of I2 and I3 would support at medium quality score. The evidence
for compounding technical debt (I3, causal, high) and organizational instability (I2,
pattern, high) is strong enough that a "lean cautious" framing would be equally
defensible. Not a calibration error — more an editorial call that reasonable people
could evaluate differently.

---

## Coverage Assessment

No `Coverage: partial` flag was raised. Checking manually:

- The 32.8% Python vulnerability rate (F7, primary, high) — appeared in Writer output
  under "Quality: Surface Metrics Up, Structural Health Down." ✅
- The DORA 7.2% system stability drop (F4/F8, secondary, high) — appeared correctly. ✅
- The 19% slowdown for experienced devs (F3, secondary, high) — surfaced prominently
  in the brief. ✅
- Developer trust decline (F11/F12) — covered in its own section. ✅
- The $19–$39 licensing cost (F9, primary, high) — included in Cost section. ✅

All high-confidence findings are represented in the brief. No high-confidence claims
appeared without traceable sourcing.

---

## Action Items

### Researcher format compliance
- [ ] Verify the Researcher spec's Stage 7 (Synthesizer) output format requirement —
  does it specify the canonical `RESEARCH OUTPUT` block? If yes, the Researcher is not
  following it and the spec needs a compliance fix or the output format needs updating.
- [ ] Determine whether the Researcher's narrative output is intentional (rich output for
  human readers) or a drift from spec. If intentional, the pipeline design needs an
  explicit "format adapter" step between Researcher and Data Analyzer.

### Writer format compliance
- [ ] Verify whether the Writer spec requires `WRITER METADATA`, `CITATIONS`, and
  `CLAIMS TO VERIFY` sections for `analysis-output` input type. If yes, the Writer
  did not comply and needs a fix.
- [ ] If Writer output format sections are required: run a targeted Writer-only test
  passing AnalysisOutput to confirm whether the gap is consistent or situational.

---

## Quality Signal

**mixed** — the chain produces high-quality, usable output for a human reader.
The format compliance gaps in Researcher and Writer output are real and would break
fully automated pipelines. The Data Analyzer is the only specialist currently
producing fully spec-compliant structured output.
