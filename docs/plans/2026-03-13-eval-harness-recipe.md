# Eval Harness Recipe Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a recipe-based adversarial evaluation harness that runs the canvas-specialists pipeline on test topics and scores output quality using three critic agents ported from the specials evaluation architecture.

**Architecture:** The eval harness is a YAML recipe (`recipes/eval-harness.yaml`) that replicates the research-chain pipeline steps, then appends three adversarial critic steps (fact-checker, inference-challenger, consistency-auditor) and a scoring step. Each critic is an inline agent prompt within the recipe — no new specialist agents needed. A separate `specs/evaluation/test-topics.yaml` defines the topic bank. Score history is appended to `specs/evaluation/score-history.yaml` after each run.

**Tech Stack:** YAML recipes, existing specialist agents, `foundation:web-research` (for fact-checking URL fetches), bash steps (for score computation and history append)

**Design reference:** Ported from the specials 5-layer adversarial evaluation architecture (`/Users/chrispark/Projects/specialists/src/specials/evaluation/`). V1 implements Layer 1 only (three adversarial critics). Layers 2–5 (failure patterns, A/B testing, multi-judge consensus, adaptive self-improvement) are out of scope for this plan.

---

## Task 1: Create Test Topics Bank

**Files:**
- Create: `specs/evaluation/test-topics.yaml`

**Step 1: Create the specs/evaluation directory**

```bash
mkdir -p specs/evaluation
```

**Step 2: Write test-topics.yaml with 5 initial topics**

Create `specs/evaluation/test-topics.yaml` with 5 topics adapted from the specials test bank. These are chosen to stress-test different pipeline behaviors:

```yaml
# =============================================================================
# Test Topic Bank for Pipeline Evaluation
# =============================================================================
#
# 5 initial topics that exercise different pipeline behaviors. Each topic
# probes specific weaknesses in the research → analysis → writing chain.
#
# Each topic has:
#   - id: stable identifier (used in score-history.yaml)
#   - query: the literal string passed to the pipeline as research_question
#   - expected_traits: behaviors we expect to see in output (for critic context)
#   - purpose: why this topic was chosen (what dimension it stress-tests)
#
# Scoring: MINIMUM across ALL topics, not average.
# The pipeline is only as strong as its weakest performance.
# =============================================================================

topics:
  - id: well-documented
    query: "What is Anthropic and what is their approach to AI safety?"
    expected_traits:
      - high_confidence_findings
      - multiple_primary_sources
      - minimal_gaps
    purpose: >
      Baseline — lots of sources available, should produce high-quality output
      across all dimensions. If this topic fails, something fundamental is broken.

  - id: recent-event
    query: "What are the key provisions and implications of the EU AI Act as enacted?"
    expected_traits:
      - recency_matters
      - secondary_sources_dominant
      - moderate_gaps
      - regulatory_complexity
    purpose: >
      Tests handling of recent/evolving information where primary sources are
      regulatory documents and secondary sources dominate commentary. Confidence
      calibration matters when information is still settling.

  - id: niche-topic
    query: "What is the current state of neuromorphic computing hardware?"
    expected_traits:
      - evidence_gaps_expected
      - tertiary_sources_common
      - low_confidence_acceptable
    purpose: >
      Tests evidence gap disclosure and honest confidence calibration when sources
      are thin. The pipeline should NOT paper over gaps or inflate confidence.

  - id: controversial
    query: "What are the arguments for and against open-sourcing large language models?"
    expected_traits:
      - contradictions_expected
      - multiple_perspectives
      - evaluative_inferences
      - balanced_coverage_required
    purpose: >
      Tests contradiction handling and evaluative inference quality. The pipeline
      must present both sides. Inferences should be evaluative, not just summarizing
      positions. The writer must hedge appropriately for contested claims.

  - id: comparison
    query: "Compare React, Vue, and Angular as frontend JavaScript frameworks"
    expected_traits:
      - competitive_analysis
      - comparison_matrix
      - multiple_entities
    purpose: >
      Tests structured comparison across multiple entities with consistent
      dimensions. Source tier assignment is tricky — official docs are primary,
      developer surveys are secondary, blog opinions are tertiary.
```

**Step 3: Commit**

```bash
git add specs/evaluation/test-topics.yaml
git commit -m "eval: add test topics bank — 5 topics stress-testing different pipeline behaviors"
```

---

## Task 2: Create Scoring Rubric

**Files:**
- Create: `specs/evaluation/scoring-rubric.md`

**Step 1: Write scoring-rubric.md**

This documents the three critics' methodology and composite scoring formula. The rubric is referenced by the eval recipe's critic prompts.

```markdown
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
```

**Step 2: Commit**

```bash
git add specs/evaluation/scoring-rubric.md
git commit -m "eval: add scoring rubric — three critics, composite formula, hedge/inference quality criteria"
```

---

## Task 3: Create the Eval Harness Recipe

This is the core deliverable. The recipe runs the full research-chain pipeline on a single topic, then evaluates the output with three critic agents.

**Files:**
- Create: `recipes/eval-harness.yaml`

**Step 1: Write the recipe header and context**

```yaml
# =============================================================================
# eval-harness: Adversarial Evaluation for Specialists Pipeline
# =============================================================================
#
# Runs the full research-chain pipeline on a single test topic, then evaluates
# the output with three adversarial critics:
#   1. Fact-checker — verifies claims against source URLs
#   2. Inference challenger — challenges inference robustness
#   3. Consistency auditor — checks confidence-language matching
#
# Produces a structured evaluation report with per-critic scores and a
# composite content score.
#
# Usage:
#   Run for one topic:
#     recipe execute recipes/eval-harness.yaml \
#       --context '{"research_question": "What is Anthropic...", "topic_id": "well-documented"}'
#
#   Run for all topics: invoke once per topic in test-topics.yaml
#
# Scoring: see specs/evaluation/scoring-rubric.md
# =============================================================================

name: "eval-harness"
description: "Adversarial evaluation — run research pipeline + three critics on a single topic"
version: "1.0.0"
tags: ["evaluation", "adversarial", "quality", "scoring"]

context:
  research_question: ""        # Required: the topic query
  topic_id: ""                 # Required: stable topic ID for score tracking
  quality_threshold: "medium"  # Pipeline quality threshold
```

**Step 2: Write the pipeline execution steps**

These replicate research-chain.yaml v1.9.0 steps exactly (research → validate → resolve-urls → format → strip → analyze → format-analysis → write → format-writer → strip-formatter-notes). Copy them verbatim from `recipes/research-chain.yaml`. The only changes:
- Remove the `derive-filename` and `save` steps (we don't need to save to disk)
- Keep all intermediate output variables — critics need them

All steps from research-chain.yaml through `strip-formatter-notes` are included unchanged. The `formatted_document_clean` variable contains the final writer output; `formatted_research_clean` contains the canonical research; `formatted_analysis` contains the canonical analysis.

**Step 3: Write the fact-checker critic step**

```yaml
  # ===========================================================================
  # CRITIC 1: Fact-Checker
  # ===========================================================================
  - id: "fact-check"
    agent: "foundation:web-research"
    prompt: |
      You are an adversarial FACT-CHECKER evaluating a research pipeline's output.
      Your job: verify each finding's claim against its source URL.

      RESEARCH OUTPUT TO EVALUATE:
      {{formatted_research_clean}}

      INSTRUCTIONS:
      For each finding (lines starting with "- Claim:"):
        1. Extract the Claim text and Source URL
        2. Fetch the source URL using web_fetch
        3. Read the page content (first 8000 chars if large)
        4. Compare: does the source content support the claim?
        5. Assign a verdict:
           - VERIFIED: source content supports the claim as stated
           - MISREPRESENTED: source exists but claim distorts/exaggerates it
           - FABRICATED: source content does not contain or support the claim
           - UNREACHABLE: URL returned error (403, 404, timeout, no content)

      If a source URL is "unknown" or "unattributed", mark UNREACHABLE.
      If the page content is a login wall or paywall, mark UNREACHABLE.
      Do NOT mark FABRICATED just because the source is behind a paywall.

      Return your report in this exact format:

      FACT-CHECK REPORT
      ━━━━━━━━━━━━━━━━━━━━━━━━━━
      Findings checked: [N]
      Verified: [N]
      Misrepresented: [N]
      Fabricated: [N]
      Unreachable: [N]
      Score: [verified / (total - unreachable) * 10, to 2 decimal places]

      VERDICTS:
      - F1: [VERDICT] — [1-sentence evidence: what the source said vs. the claim]
      - F2: [VERDICT] — [evidence]
      ...

      Rules:
      - Check EVERY finding. Do not skip any.
      - Score denominator excludes UNREACHABLE (they're access problems, not quality)
      - If all findings are UNREACHABLE, score = 0.0 with note "all sources unreachable"
      - Be strict: VERIFIED means the source actually says what the claim says.
        A claim that is "close but exaggerated" is MISREPRESENTED, not VERIFIED.
    output: "fact_check_report"
    timeout: 1800
```

**Step 4: Write the inference-challenger critic step**

```yaml
  # ===========================================================================
  # CRITIC 2: Inference Challenger
  # ===========================================================================
  - id: "challenge-inferences"
    agent: "self"
    prompt: |
      You are an adversarial INFERENCE CHALLENGER evaluating analysis quality.
      Your job: determine whether each inference adds genuine analytical value.

      ANALYSIS OUTPUT TO EVALUATE:
      {{formatted_analysis}}

      RESEARCH FINDINGS (the evidence base):
      {{formatted_research_clean}}

      For EACH inference in the INFERENCES section, run this TWO-PHASE protocol:

      PHASE 1 — INDEPENDENT DERIVATION:
      Read ONLY the findings listed in the inference's traces_to field.
      Ask yourself: "What conclusions would a competent analyst draw from ONLY
      these findings?" Write your independent conclusions.

      PHASE 2 — ADVERSARIAL CHALLENGE:
      Now read the actual inference claim. Ask:
      a) Does it add insight beyond what Phase 1 produced? (analytical lift)
      b) What is the strongest counterargument or alternative explanation?
      c) Does the claim language match the evidence strength?

      Assign a verdict:
      - ROBUST: Genuine analytical lift. Phase 1 didn't produce this exact insight.
        Counterargument is weaker than the inference. Claim language is calibrated.
      - SUPPORTED_BUT_OBVIOUS: Phase 1 independently reached the same conclusion.
        The inference is valid but adds no analytical value — it's a summary
        masquerading as synthesis. A competent reader would derive this from the
        findings alone.
      - WEAK: One or more of:
        * Causal overclaim (asserts causation from correlation)
        * Scope overgeneralization (specific examples → universal claims)
        * Unsupported temporal leap ("inflection point" without trend data)
        * Intent/strategy attribution without direct evidence
        * Trivial restatement of a single finding
        * Equally plausible alternative explanation exists

      Return your report in this exact format:

      INFERENCE CHALLENGE REPORT
      ━━━━━━━━━━━━━━━━━━━━━━━━━━
      Inferences challenged: [N]
      Robust: [N]
      Obvious: [N]
      Weak: [N]
      Score: [robust_count / total * 10, to 2 decimal places]

      VERDICTS:
      - I1: [VERDICT]
        Phase 1 derivation: [what you concluded from the findings alone]
        Challenge: [strongest counterargument]
        Rationale: [1-2 sentences explaining verdict]
      - I2: [VERDICT]
        ...

      If there are zero inferences, return score = 0.0 with note "no inferences to evaluate".
      OBVIOUS inferences score 0 — they are padding, not analysis.
    output: "inference_challenge_report"
    timeout: 900
```

**Step 5: Write the consistency-auditor critic step**

```yaml
  # ===========================================================================
  # CRITIC 3: Consistency Auditor
  # ===========================================================================
  - id: "audit-consistency"
    agent: "self"
    prompt: |
      You are an adversarial CONSISTENCY AUDITOR evaluating whether the writer's
      prose language matches the confidence level of each claim's source.

      WRITER OUTPUT TO EVALUATE:
      {{formatted_document_clean}}

      ANALYSIS OUTPUT (source of confidence levels):
      {{formatted_analysis}}

      For EACH factual claim in the writer output, perform this check:

      1. Identify the claim in the prose
      2. Trace it to its source in the analysis output (finding or inference)
      3. Determine the source confidence level (high/medium/low) and source type
         (finding vs inference)
      4. Check whether the prose language matches:

         HIGH confidence finding:
           ✓ Definitive language OK: "X is", "X has achieved"
           ✗ Over-hedging is a minor issue, not a violation

         MEDIUM confidence finding:
           ✓ MUST have hedging or source attribution: "according to", "reportedly",
             "suggests that", "[source] states"
           ✗ VIOLATION (MISSING_HEDGE): bare "X is" without any qualifier
           ✗ VIOLATION (CONFIDENCE_UPGRADE): definitive language for medium source

         LOW confidence finding:
           ✓ MUST have strong hedges: "unconfirmed reports suggest", "may possibly"
           ✗ VIOLATION (CONFIDENCE_UPGRADE): any definitive or moderate language

         Inference-sourced claim (any confidence):
           ✓ MUST have analytical qualifier: "analysis suggests", "evidence points to",
             "patterns suggest", "findings imply"
           ✗ VIOLATION (INFERENCE_AS_FACT): presented as established fact

         Contradicted finding:
           ✓ MUST acknowledge the contradiction
           ✗ VIOLATION (MISSING_HEDGE): stated without noting the dispute

      Return your report in this exact format:

      CONSISTENCY AUDIT REPORT
      ━━━━━━━━━━━━━━━━━━━━━━━━━━
      Claims audited: [N]
      Clean: [N]
      Violations: [N]
        CONFIDENCE_UPGRADE: [N]
        MISSING_HEDGE: [N]
        INFERENCE_AS_FACT: [N]
      Score: [(1 - violations/total) * 10, to 2 decimal places]

      FINDINGS:
      - S1: CLEAN — [brief note]
      - S2: VIOLATION (MISSING_HEDGE) — "medium confidence claim stated as: '[exact quote]'
        without hedging. Should use: 'According to [source], ...'"
      - S3: VIOLATION (INFERENCE_AS_FACT) — "inference presented as: '[exact quote]'
        without analytical qualifier"
      ...

      Rules:
      - Audit EVERY factual claim. Transition sentences and structural elements are exempt.
      - Be strict on MEDIUM confidence: every sentence needs a visible hedge signal.
      - Be strict on inferences: NEVER presented as established fact.
      - A single sentence can have multiple violations (e.g., both CONFIDENCE_UPGRADE
        and MISSING_HEDGE).
      - If the writer output has zero factual claims, score = 10.0.
    output: "consistency_audit_report"
    timeout: 900
```

**Step 6: Write the score computation step**

```yaml
  # ===========================================================================
  # SCORE COMPUTATION
  # ===========================================================================
  - id: "compute-scores"
    type: "bash"
    command: |
      # Extract scores from the three critic reports using grep
      _fc_score=$(echo '{{fact_check_report}}' | grep -oP 'Score: \K[0-9]+\.?[0-9]*' | head -1)
      _ic_score=$(echo '{{inference_challenge_report}}' | grep -oP 'Score: \K[0-9]+\.?[0-9]*' | head -1)
      _ca_score=$(echo '{{consistency_audit_report}}' | grep -oP 'Score: \K[0-9]+\.?[0-9]*' | head -1)

      # Default to 0.0 if extraction failed
      _fc_score=${_fc_score:-0.0}
      _ic_score=${_ic_score:-0.0}
      _ca_score=${_ca_score:-0.0}

      # Compute composite: 0.40 * fact + 0.35 * inference + 0.25 * consistency
      _composite=$(python3 -c "
      fc = float('${_fc_score}')
      ic = float('${_ic_score}')
      ca = float('${_ca_score}')
      composite = 0.40 * fc + 0.35 * ic + 0.25 * ca
      print(f'{composite:.2f}')
      ")

      _timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)

      cat <<EOF
      EVAL SCORES
      ━━━━━━━━━━━━━━━━━━━━━━━━━━
      Topic: {{topic_id}}
      Timestamp: ${_timestamp}
      Fact-checker score: ${_fc_score}/10 (weight: 0.40)
      Inference challenger score: ${_ic_score}/10 (weight: 0.35)
      Consistency auditor score: ${_ca_score}/10 (weight: 0.25)
      Composite score: ${_composite}/10
      EOF
    output: "eval_scores"
    timeout: 30
```

**Step 7: Write the score history append step**

```yaml
  # ===========================================================================
  # SAVE SCORE HISTORY
  # ===========================================================================
  - id: "save-scores"
    type: "bash"
    command: |
      mkdir -p specs/evaluation

      _fc_score=$(echo '{{fact_check_report}}' | grep -oP 'Score: \K[0-9]+\.?[0-9]*' | head -1)
      _ic_score=$(echo '{{inference_challenge_report}}' | grep -oP 'Score: \K[0-9]+\.?[0-9]*' | head -1)
      _ca_score=$(echo '{{consistency_audit_report}}' | grep -oP 'Score: \K[0-9]+\.?[0-9]*' | head -1)
      _fc_score=${_fc_score:-0.0}
      _ic_score=${_ic_score:-0.0}
      _ca_score=${_ca_score:-0.0}
      _composite=$(python3 -c "
      fc = float('${_fc_score}')
      ic = float('${_ic_score}')
      ca = float('${_ca_score}')
      print(f'{0.40*fc + 0.35*ic + 0.25*ca:.2f}')
      ")
      _timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)

      cat >> specs/evaluation/score-history.yaml <<EOF
      - topic_id: {{topic_id}}
        timestamp: "${_timestamp}"
        fact_checker_score: ${_fc_score}
        inference_challenger_score: ${_ic_score}
        consistency_auditor_score: ${_ca_score}
        composite_score: ${_composite}
        research_question: "{{research_question}}"
      EOF

      echo "Score appended to specs/evaluation/score-history.yaml"
    output: "save_result"
    timeout: 30
```

**Step 8: Write the final save-reports step**

```yaml
  # ===========================================================================
  # SAVE FULL EVALUATION REPORT
  # ===========================================================================
  - id: "save-report"
    agent: "foundation:file-ops"
    prompt: |
      Save the following evaluation report to disk.

      File path: specs/evaluation/reports/{{topic_id}}-eval.md
      Create the specs/evaluation/reports/ directory if it does not exist.
      Report the full file path you saved to.

      Content to save:
      # Evaluation Report: {{topic_id}}

      **Research question:** {{research_question}}

      ---

      {{eval_scores}}

      ---

      ## Fact-Checker Report

      {{fact_check_report}}

      ---

      ## Inference Challenge Report

      {{inference_challenge_report}}

      ---

      ## Consistency Audit Report

      {{consistency_audit_report}}
    output: "report_path"
    timeout: 300
```

**Step 9: Assemble the complete recipe file**

Combine all parts into `recipes/eval-harness.yaml`:
1. Recipe header (Step 1)
2. Pipeline steps copied from research-chain.yaml: `research`, `validate-research`, `resolve-urls`, `format-research`, `strip-parsed-prefix`, `analyze`, `format-analysis`, `write`, `format-writer`, `strip-formatter-notes` (Steps 2)
3. Three critic steps (Steps 3–5)
4. Score computation (Step 6)
5. Score history append (Step 7)
6. Report save (Step 8)

**Step 10: Commit**

```bash
git add recipes/eval-harness.yaml
git commit -m "eval: add eval-harness recipe — pipeline + 3 adversarial critics + scoring"
```

---

## Task 4: Create Recipe Validation Tests

**Files:**
- Create: `tests/test_eval_harness.py`

**Step 1: Write the failing tests**

```python
"""Tests for eval harness infrastructure — recipe structure and test topics."""

import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent


class TestTestTopics:
    """Validate test-topics.yaml schema and content."""

    def setup_method(self):
        topics_path = REPO_ROOT / "specs" / "evaluation" / "test-topics.yaml"
        assert topics_path.exists(), f"Missing: {topics_path}"
        with open(topics_path) as f:
            self.data = yaml.safe_load(f)

    def test_has_topics_key(self):
        assert "topics" in self.data
        assert isinstance(self.data["topics"], list)

    def test_minimum_topic_count(self):
        """At least 5 topics to cover baseline + edge cases."""
        assert len(self.data["topics"]) >= 5

    def test_topic_schema(self):
        """Every topic has required fields."""
        required_fields = {"id", "query", "expected_traits", "purpose"}
        for topic in self.data["topics"]:
            missing = required_fields - set(topic.keys())
            assert not missing, f"Topic {topic.get('id', '?')} missing: {missing}"

    def test_topic_ids_unique(self):
        ids = [t["id"] for t in self.data["topics"]]
        assert len(ids) == len(set(ids)), f"Duplicate topic IDs: {ids}"

    def test_topic_queries_non_empty(self):
        for topic in self.data["topics"]:
            assert topic["query"].strip(), f"Topic {topic['id']} has empty query"

    def test_expected_traits_are_lists(self):
        for topic in self.data["topics"]:
            assert isinstance(topic["expected_traits"], list), (
                f"Topic {topic['id']}: expected_traits must be a list"
            )


class TestEvalHarnessRecipe:
    """Validate eval-harness.yaml recipe structure."""

    def setup_method(self):
        recipe_path = REPO_ROOT / "recipes" / "eval-harness.yaml"
        assert recipe_path.exists(), f"Missing: {recipe_path}"
        with open(recipe_path) as f:
            self.recipe = yaml.safe_load(f)

    def test_has_required_recipe_fields(self):
        for field in ("name", "description", "version", "steps", "context"):
            assert field in self.recipe, f"Missing recipe field: {field}"

    def test_context_has_required_inputs(self):
        ctx = self.recipe["context"]
        assert "research_question" in ctx
        assert "topic_id" in ctx

    def test_has_pipeline_steps(self):
        """Recipe must include the core pipeline steps."""
        step_ids = {s["id"] for s in self.recipe["steps"]}
        required_pipeline = {"research", "validate-research", "analyze", "write"}
        missing = required_pipeline - step_ids
        assert not missing, f"Missing pipeline steps: {missing}"

    def test_has_critic_steps(self):
        """Recipe must include all three adversarial critic steps."""
        step_ids = {s["id"] for s in self.recipe["steps"]}
        required_critics = {"fact-check", "challenge-inferences", "audit-consistency"}
        missing = required_critics - step_ids
        assert not missing, f"Missing critic steps: {missing}"

    def test_has_scoring_step(self):
        step_ids = {s["id"] for s in self.recipe["steps"]}
        assert "compute-scores" in step_ids

    def test_has_save_steps(self):
        step_ids = {s["id"] for s in self.recipe["steps"]}
        assert "save-scores" in step_ids
        assert "save-report" in step_ids

    def test_critic_steps_after_pipeline_steps(self):
        """Critics must come after pipeline execution."""
        step_ids = [s["id"] for s in self.recipe["steps"]]
        pipeline_last = max(
            step_ids.index(s) for s in step_ids
            if s in {"write", "format-writer", "strip-formatter-notes"}
        )
        critic_first = min(
            step_ids.index(s) for s in step_ids
            if s in {"fact-check", "challenge-inferences", "audit-consistency"}
        )
        assert critic_first > pipeline_last, (
            "Critic steps must come after all pipeline steps"
        )

    def test_step_ids_unique(self):
        step_ids = [s["id"] for s in self.recipe["steps"]]
        assert len(step_ids) == len(set(step_ids)), f"Duplicate step IDs"

    def test_all_steps_have_output(self):
        """Every step must declare an output variable."""
        for step in self.recipe["steps"]:
            assert "output" in step, f"Step {step['id']} missing output"


class TestScoringRubric:
    """Validate scoring rubric exists and covers all three critics."""

    def test_rubric_exists(self):
        rubric_path = REPO_ROOT / "specs" / "evaluation" / "scoring-rubric.md"
        assert rubric_path.exists()

    def test_rubric_covers_all_critics(self):
        rubric_path = REPO_ROOT / "specs" / "evaluation" / "scoring-rubric.md"
        content = rubric_path.read_text()
        assert "Fact-Checker" in content
        assert "Inference Challenger" in content
        assert "Consistency Auditor" in content

    def test_rubric_documents_composite_formula(self):
        rubric_path = REPO_ROOT / "specs" / "evaluation" / "scoring-rubric.md"
        content = rubric_path.read_text()
        assert "0.40" in content
        assert "0.35" in content
        assert "0.25" in content
```

**Step 2: Run tests to verify they fail (nothing exists yet)**

```bash
cd /Users/chrispark/Projects/canvas-specialists
python -m pytest tests/test_eval_harness.py -v
```

Expected: FAIL — test-topics.yaml, eval-harness.yaml, scoring-rubric.md don't exist yet.

**Step 3: After Tasks 1–3 are complete, run tests to verify they pass**

```bash
python -m pytest tests/test_eval_harness.py -v
```

Expected: ALL PASS

**Step 4: Commit**

```bash
git add tests/test_eval_harness.py
git commit -m "test: add eval harness validation tests — topic schema, recipe structure, rubric coverage"
```

---

## Task 5: Initialize Score History File

**Files:**
- Create: `specs/evaluation/score-history.yaml`

**Step 1: Create empty score history**

```yaml
# Score history for eval-harness runs.
# Each entry is appended by the eval-harness recipe's save-scores step.
# Content score = MINIMUM composite across all topics in a full eval run.
[]
```

**Step 2: Commit**

```bash
git add specs/evaluation/score-history.yaml
git commit -m "eval: initialize empty score history"
```

---

## Task 6: Smoke-Test the Recipe (Manual Validation)

This task validates the recipe runs end-to-end on the simplest topic.

**Step 1: Validate recipe YAML parses**

```bash
python3 -c "import yaml; yaml.safe_load(open('recipes/eval-harness.yaml'))" && echo "YAML valid"
```

**Step 2: Run recipe on the well-documented topic**

```bash
recipe execute recipes/eval-harness.yaml \
  --context '{"research_question": "What is Anthropic and what is their approach to AI safety?", "topic_id": "well-documented"}'
```

Expected: Full pipeline runs, three critic reports generated, composite score computed, results saved to `specs/evaluation/score-history.yaml` and `specs/evaluation/reports/well-documented-eval.md`.

**Step 3: Verify outputs exist**

```bash
cat specs/evaluation/score-history.yaml
cat specs/evaluation/reports/well-documented-eval.md
```

**Step 4: Review critic quality**

Read the eval report. Check:
- Fact-checker: did it actually fetch URLs and compare content?
- Inference challenger: did it run both phases (derive + challenge)?
- Consistency auditor: did it cross-reference confidence levels?
- Are the scores plausible (not all 10.0 or all 0.0)?

**Step 5: Commit smoke test results**

```bash
git add specs/evaluation/
git commit -m "eval: smoke test — well-documented topic eval complete"
```

---

## Execution Order

| Task | Depends on | Estimated time |
|------|-----------|---------------|
| Task 4 (tests) | None — write first (TDD) | 5 min |
| Task 1 (test topics) | None | 5 min |
| Task 2 (scoring rubric) | None | 5 min |
| Task 5 (score history init) | None | 2 min |
| Task 3 (eval recipe) | Tasks 1, 2 | 30 min |
| Task 4 re-run (verify) | Tasks 1, 2, 3, 5 | 2 min |
| Task 6 (smoke test) | All above | 45–60 min (pipeline runtime) |

**TDD order:** Write tests first (Task 4), then implement (Tasks 1–3, 5), then verify (Task 4 re-run), then smoke test (Task 6).

---

## Future Work (Not In Scope)

These are natural next steps after V1 is stable:

- **Batch runner recipe** — Runs eval-harness on ALL test topics, computes MIN composite, generates aggregate report
- **Layer 2: Failure patterns** — Track recurring critic findings across runs
- **Layer 3: A/B testing** — Compare prompt variants (e.g., before/after hedge-by-default port)
- **Layer 4: Multi-judge consensus** — Run critics with 3 different models, take median
- **Layer 5: Adaptive test bank** — Automatically generate new topics probing weakest dimensions
- **Cross-project bridge** — Import specials evaluation Python critics for comparison scoring against the same rubric
