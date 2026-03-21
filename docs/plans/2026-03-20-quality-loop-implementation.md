# Quality Loop Implementation Plan

> **Execution:** Use the subagent-driven-development workflow to implement this plan.

**Goal:** Build an autonomous quality improvement loop recipe that evaluates the specialists pipeline against competitors, diagnoses structural gaps, fixes them, and re-evaluates until a target score is reached — reverting any change that doesn't improve the score.

**Architecture:** A `while_condition` recipe (`quality-loop.yaml`) wraps the existing `quality-eval.yaml` orchestrator. Each iteration: evaluate → aggregate → diagnose → fix → check. The check step compares scores — if the fix helped, keep it; if not, `git revert`. A plateau counter (2 consecutive non-improving rounds) triggers early exit. All decisions are logged per-round in an append-only YAML file.

**Tech Stack:** Amplifier recipe YAML, `while_condition`/`break_when` loop syntax, bash steps with `parse_json: true`, `git revert` for rollback, pytest for structural tests.

**Design doc:** `docs/plans/2026-03-19-quality-loop-design.md`

---

## Phase 0: Fix Evaluation Foundation

Three prerequisite fixes to existing files. The quality loop depends on these being correct — without them, evaluation results are unreliable.

---

### Task 1: Fix `score-history.yaml` YAML Syntax Bug

**Why:** Line 3 has a stray `[]` that makes the file unparseable. Any recipe or script that loads this file will crash. Trivial fix, big impact.

**Files:**
- Modify: `specs/evaluation/score-history.yaml`

**Step 1: Verify the bug exists**

Run:
```bash
python3 -c "import yaml; yaml.safe_load(open('specs/evaluation/score-history.yaml'))" 2>&1
```
Expected: Error or unexpected parse result (the `[]` on line 3 makes the YAML parser treat it as an empty list, ignoring the entries below).

**Step 2: Fix the YAML**

The file currently looks like this:
```yaml
# Score history for eval-harness runs.
# Each entry is appended by the eval-harness recipe's save-scores step.
[]
- topic_id: well-documented
  timestamp: "2026-03-14T08:58:51Z"
  ...
```

Remove the `[]` on line 3. The file should be:
```yaml
# Score history for eval-harness runs.
# Each entry is appended by the eval-harness recipe's save-scores step.
- topic_id: well-documented
  timestamp: "2026-03-14T08:58:51Z"
  fact_checker_score: 10.00
  inference_challenger_score: 6.67
  consistency_auditor_score: 9.55
  composite_score: 8.72
  research_question: "What is Anthropic and what is their approach to AI safety?"
```

**Step 3: Verify the fix**

Run:
```bash
python3 -c "
import yaml
with open('specs/evaluation/score-history.yaml') as f:
    data = yaml.safe_load(f)
assert isinstance(data, list), f'Expected list, got {type(data)}'
assert len(data) >= 1, 'Expected at least 1 entry'
assert data[0]['topic_id'] == 'well-documented'
print('OK: score-history.yaml parses correctly')
"
```
Expected: `OK: score-history.yaml parses correctly`

**Step 4: Commit**
```bash
git add specs/evaluation/score-history.yaml && git commit -m "fix: remove stray [] from score-history.yaml that prevented parsing"
```

---

### Task 2: Add 2 Missing Test Topics

**Why:** The design specifies 5 competitive-eval topics but `test-topics.yaml` only has 3. The missing topics (comparison, technical analysis) stress pipeline capabilities that the existing 3 don't cover. With only 3 topics, the triangulation rule (gap in 2+ topics = structural) has a 67% threshold; with 5 topics it's 40% — much better at separating signal from noise.

**Files:**
- Modify: `specs/evaluation/test-topics.yaml`

**Step 1: Add the two new topics**

Append these two entries to the `topics:` list in `specs/evaluation/test-topics.yaml`, right after the existing `survey` entry (after line 119). Follow the exact same structure as the existing `competitive-eval` topics:

```yaml

  - id: comparison
    profile: competitive-eval
    query: "Compare Cursor vs GitHub Copilot Workspace for AI-assisted development"
    expected_traits:
      - competitive_analysis
      - comparison_matrix
      - multiple_entities
      - technical_depth
    purpose: >
      Competitive eval — head-to-head comparison. Tests structured comparison
      reasoning, consistent dimension coverage across entities, and balanced
      technical assessment. Stresses the pipeline's ability to evaluate tools
      rather than just describe them.

  - id: technical-analysis
    profile: competitive-eval
    query: "What are the security implications of WebAssembly outside the browser?"
    expected_traits:
      - technical_depth
      - evidence_gaps_expected
      - evaluative_inferences
      - moderate_gaps
    purpose: >
      Competitive eval — deep technical analysis. Tests the pipeline's ability
      to handle a niche technical topic requiring security reasoning and
      inference from limited sources. Confidence calibration matters when
      the evidence base is thin.
```

**Step 2: Verify the new topics load correctly**

Run:
```bash
python3 -c "
import yaml
with open('specs/evaluation/test-topics.yaml') as f:
    data = yaml.safe_load(f)
topics = [t for t in data['topics'] if t.get('profile') == 'competitive-eval']
ids = [t['id'] for t in topics]
print(f'Competitive-eval topics ({len(topics)}): {ids}')
assert len(topics) == 5, f'Expected 5, got {len(topics)}'
assert 'comparison' in ids, 'Missing: comparison'
assert 'technical-analysis' in ids, 'Missing: technical-analysis'
print('OK: All 5 competitive-eval topics present')
"
```
Expected: `OK: All 5 competitive-eval topics present`

**Step 3: Commit**
```bash
git add specs/evaluation/test-topics.yaml && git commit -m "feat: add comparison and technical-analysis topics for competitive eval"
```

---

### Task 3: Wire Competitor Model Routing

**Why:** The `run-competitors` step in `quality-eval-iteration.yaml` currently uses `agent: "foundation:web-research"` for all 3 competitors with no model differentiation. Each competitor has `provider` and `model` fields in `competitors.yaml` (e.g., anthropic/claude-sonnet-4-5-*, google/gemini-2.5-pro, openai/gpt-4o), but those fields are loaded and then ignored. Without routing, all 3 "competitors" use the same default model, making triangulation meaningless.

**Files:**
- Modify: `recipes/quality-eval-iteration.yaml` (the `run-competitors` step, lines 88–112)
- Modify: `tests/test_quality_eval_iteration_recipe.py` (add test for `provider_preferences`)

**Step 1: Write the failing test**

Add this test to the end of `tests/test_quality_eval_iteration_recipe.py`:

```python


def test_run_competitors_has_provider_preferences() -> None:
    """run-competitors must have provider_preferences referencing competitor config."""
    recipe = load_recipe()
    step = _get_step(recipe, "run-competitors")
    pp = step.get("provider_preferences", {})
    assert pp, (
        "run-competitors must have 'provider_preferences' to route each "
        "competitor to its configured model provider"
    )
    # Must reference the competitor's provider field from the foreach variable
    pp_str = str(pp)
    assert "competitor" in pp_str, (
        "provider_preferences must reference the '{{competitor.*}}' loop "
        f"variable for dynamic routing, got: {pp}"
    )
```

**Step 2: Run test to verify it fails**

Run:
```bash
pytest tests/test_quality_eval_iteration_recipe.py::test_run_competitors_has_provider_preferences -v
```
Expected: FAIL — the current step has no `provider_preferences` key.

**Step 3: Add `provider_preferences` to the `run-competitors` step**

In `recipes/quality-eval-iteration.yaml`, modify the `run-competitors` step (lines 88–112). Add `provider_preferences` that routes each competitor to its configured provider/model. The step currently looks like:

```yaml
  - id: "run-competitors"
    foreach: "{{competitors}}"
    as: "competitor"
    parallel: 3
    collect: "competitor_results"
    agent: "foundation:web-research"
    prompt: |
      ...
    output: "competitor_result"
    timeout: 2700
    on_error: "continue"
```

Add `provider_preferences` right after `agent:`:

```yaml
  - id: "run-competitors"
    foreach: "{{competitors}}"
    as: "competitor"
    parallel: 3
    collect: "competitor_results"
    agent: "foundation:web-research"
    provider_preferences:
      provider: "{{competitor.provider}}"
      model: "{{competitor.model}}"
    prompt: |
      ...
    output: "competitor_result"
    timeout: 2700
    on_error: "continue"
```

Do NOT change anything else about this step — keep the existing prompt, output, timeout, and on_error exactly as they are.

**Step 4: Run test to verify it passes**

Run:
```bash
pytest tests/test_quality_eval_iteration_recipe.py::test_run_competitors_has_provider_preferences -v
```
Expected: PASS

**Step 5: Run the full existing test suite to check for regressions**

Run:
```bash
pytest tests/test_quality_eval_iteration_recipe.py -v
```
Expected: All tests pass (the existing `test_run_competitors_uses_foundation_web_research_agent` test should still pass because we didn't change the `agent` field).

**Step 6: Commit**
```bash
git add recipes/quality-eval-iteration.yaml tests/test_quality_eval_iteration_recipe.py && git commit -m "feat: wire competitor model routing via provider_preferences in quality-eval-iteration"
```

---

## Phase 1: Quality Loop Recipe

Build the loop recipe and its tests. Tasks 4–10 build up the recipe incrementally — each task adds one step (or a tightly coupled pair), with tests written first.

---

### Task 4: Write Structural Tests for `quality-loop.yaml`

**Why:** TDD — write all the structural tests first. These tests validate the recipe's shape (metadata, context variables, step IDs, step ordering, output declarations) without executing it. They follow the exact same patterns as `tests/test_quality_eval_recipe.py`.

**Files:**
- Create: `tests/test_quality_loop_recipe.py`

**Step 1: Create the test file**

Create `tests/test_quality_loop_recipe.py` with the full structural test suite:

```python
"""Validation tests for recipes/quality-loop.yaml.

Ensures the autonomous quality improvement loop recipe is structurally correct
and implements: while_condition loop, evaluate, aggregate+diagnose, fix, check,
and observability logging — with revert-on-regression and convergence detection.
"""

from __future__ import annotations

from pathlib import Path

import yaml

RECIPE_PATH = Path(__file__).parent.parent / "recipes" / "quality-loop.yaml"


def load_recipe() -> dict:
    assert RECIPE_PATH.exists(), f"Recipe file not found: {RECIPE_PATH}"
    with RECIPE_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------


def test_recipe_file_exists() -> None:
    """recipes/quality-loop.yaml must exist."""
    assert RECIPE_PATH.exists(), "recipes/quality-loop.yaml must exist"


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------


def test_recipe_name() -> None:
    """Recipe name must be 'quality-loop'."""
    recipe = load_recipe()
    assert recipe["name"] == "quality-loop", (
        f"Expected name='quality-loop', got {recipe.get('name')!r}"
    )


def test_recipe_has_required_fields() -> None:
    """Recipe has required fields: name, description, version, steps, context."""
    recipe = load_recipe()
    required = {"name", "description", "version", "steps", "context"}
    missing = required - set(recipe.keys())
    assert not missing, f"Recipe missing required fields: {missing}"


def test_recipe_version() -> None:
    """Recipe version must be '1.0.0'."""
    recipe = load_recipe()
    assert recipe["version"] == "1.0.0", (
        f"Expected version='1.0.0', got {recipe.get('version')!r}"
    )


def test_recipe_tags_include_quality() -> None:
    """Recipe tags must include 'quality'."""
    recipe = load_recipe()
    tags = recipe.get("tags", [])
    assert "quality" in tags, f"Tags must include 'quality', got {tags}"


def test_recipe_tags_include_loop() -> None:
    """Recipe tags must include 'loop'."""
    recipe = load_recipe()
    tags = recipe.get("tags", [])
    assert "loop" in tags, f"Tags must include 'loop', got {tags}"


# ---------------------------------------------------------------------------
# Context variables
# ---------------------------------------------------------------------------


def test_context_has_target_score() -> None:
    """Context must have 'target_score'."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert "target_score" in context, "Context must have 'target_score'"


def test_context_has_current_score() -> None:
    """Context must have 'current_score' initialized to 0."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert "current_score" in context, "Context must have 'current_score'"
    assert context["current_score"] == 0, (
        f"current_score must default to 0, got {context['current_score']!r}"
    )


def test_context_has_plateau_counter() -> None:
    """Context must have 'plateau_counter' initialized to 0."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert "plateau_counter" in context, "Context must have 'plateau_counter'"
    assert context["plateau_counter"] == 0, (
        f"plateau_counter must default to 0, got {context['plateau_counter']!r}"
    )


def test_context_has_converged() -> None:
    """Context must have 'converged' initialized to 'false'."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert "converged" in context, "Context must have 'converged'"
    assert context["converged"] == "false", (
        f"converged must default to 'false', got {context['converged']!r}"
    )


def test_context_has_evaluation_mode() -> None:
    """Context must have 'evaluation_mode' defaulting to 'competitive'."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert "evaluation_mode" in context, "Context must have 'evaluation_mode'"
    assert context["evaluation_mode"] == "competitive", (
        f"evaluation_mode must default to 'competitive', got {context['evaluation_mode']!r}"
    )


# ---------------------------------------------------------------------------
# While-loop structure
# ---------------------------------------------------------------------------


def test_has_while_condition() -> None:
    """Recipe must have a while_condition step for the improvement loop."""
    recipe = load_recipe()
    loop_steps = [s for s in recipe.get("steps", []) if "while_condition" in s]
    assert len(loop_steps) == 1, (
        f"Expected exactly 1 while_condition step, found {len(loop_steps)}"
    )


def test_while_condition_compares_score_to_target() -> None:
    """while_condition must compare current_score < target_score."""
    recipe = load_recipe()
    loop_step = [s for s in recipe["steps"] if "while_condition" in s][0]
    wc = loop_step["while_condition"]
    assert "current_score" in wc, (
        f"while_condition must reference 'current_score', got: {wc}"
    )
    assert "target_score" in wc, (
        f"while_condition must reference 'target_score', got: {wc}"
    )


def test_break_when_checks_converged() -> None:
    """break_when must check the converged flag."""
    recipe = load_recipe()
    loop_step = [s for s in recipe["steps"] if "while_condition" in s][0]
    bw = loop_step.get("break_when", "")
    assert "converged" in bw, (
        f"break_when must reference 'converged', got: {bw}"
    )


def test_max_while_iterations_is_5() -> None:
    """max_while_iterations must be 5."""
    recipe = load_recipe()
    loop_step = [s for s in recipe["steps"] if "while_condition" in s][0]
    assert loop_step.get("max_while_iterations") == 5, (
        f"max_while_iterations must be 5, got {loop_step.get('max_while_iterations')!r}"
    )


# ---------------------------------------------------------------------------
# Loop body steps — presence and uniqueness
# ---------------------------------------------------------------------------


def _get_loop_steps(recipe: dict) -> list:
    loop_step = [s for s in recipe["steps"] if "while_condition" in s][0]
    return loop_step.get("steps", [])


def _get_loop_step(recipe: dict, step_id: str) -> dict:
    for step in _get_loop_steps(recipe):
        if step["id"] == step_id:
            return step
    raise AssertionError(f"Loop step '{step_id}' not found")


def _loop_step_index(recipe: dict, step_id: str) -> int:
    step_ids = [s["id"] for s in _get_loop_steps(recipe)]
    assert step_id in step_ids, f"Step '{step_id}' not found in loop body"
    return step_ids.index(step_id)


def test_loop_has_required_step_ids() -> None:
    """Loop body must include: evaluate, aggregate-diagnose, fix, check, log-round."""
    recipe = load_recipe()
    step_ids = [s["id"] for s in _get_loop_steps(recipe)]
    required = {"evaluate", "aggregate-diagnose", "fix", "check", "log-round"}
    missing = required - set(step_ids)
    assert not missing, f"Loop body missing required step IDs: {missing}"


def test_loop_step_ids_unique() -> None:
    """No duplicate step IDs in loop body."""
    recipe = load_recipe()
    step_ids = [s["id"] for s in _get_loop_steps(recipe)]
    assert len(step_ids) == len(set(step_ids)), (
        f"Duplicate step IDs: {[s for s in step_ids if step_ids.count(s) > 1]}"
    )


def test_all_loop_steps_have_output() -> None:
    """Every loop step declares an output variable."""
    recipe = load_recipe()
    for step in _get_loop_steps(recipe):
        assert "output" in step, (
            f"Loop step '{step.get('id', '<unknown>')}' missing 'output' declaration"
        )


# ---------------------------------------------------------------------------
# Loop body step ordering
# ---------------------------------------------------------------------------


def test_evaluate_before_aggregate_diagnose() -> None:
    """evaluate must come before aggregate-diagnose."""
    recipe = load_recipe()
    assert _loop_step_index(recipe, "evaluate") < _loop_step_index(recipe, "aggregate-diagnose")


def test_aggregate_diagnose_before_fix() -> None:
    """aggregate-diagnose must come before fix."""
    recipe = load_recipe()
    assert _loop_step_index(recipe, "aggregate-diagnose") < _loop_step_index(recipe, "fix")


def test_fix_before_check() -> None:
    """fix must come before check."""
    recipe = load_recipe()
    assert _loop_step_index(recipe, "fix") < _loop_step_index(recipe, "check")


def test_check_before_log_round() -> None:
    """check must come before log-round."""
    recipe = load_recipe()
    assert _loop_step_index(recipe, "check") < _loop_step_index(recipe, "log-round")


# ---------------------------------------------------------------------------
# evaluate step
# ---------------------------------------------------------------------------


def test_evaluate_invokes_quality_eval() -> None:
    """evaluate must invoke quality-eval.yaml as a sub-recipe."""
    recipe = load_recipe()
    step = _get_loop_step(recipe, "evaluate")
    assert step.get("type") == "recipe", (
        f"evaluate must be type='recipe', got {step.get('type')!r}"
    )
    recipe_ref = step.get("recipe", "")
    assert "quality-eval" in recipe_ref, (
        f"evaluate must reference 'quality-eval', got {recipe_ref!r}"
    )


def test_evaluate_passes_context() -> None:
    """evaluate must pass evaluation_mode and target_score in context."""
    recipe = load_recipe()
    step = _get_loop_step(recipe, "evaluate")
    ctx = step.get("context", {})
    assert "evaluation_mode" in ctx, "evaluate context must include 'evaluation_mode'"
    assert "target_score" in ctx, "evaluate context must include 'target_score'"


# ---------------------------------------------------------------------------
# aggregate-diagnose step
# ---------------------------------------------------------------------------


def test_aggregate_diagnose_references_eval_result() -> None:
    """aggregate-diagnose prompt must reference the evaluation output."""
    recipe = load_recipe()
    step = _get_loop_step(recipe, "aggregate-diagnose")
    prompt = step.get("prompt", "")
    assert "{{eval_result}}" in prompt, (
        "aggregate-diagnose prompt must reference '{{eval_result}}'"
    )


def test_aggregate_diagnose_mentions_triangulation() -> None:
    """aggregate-diagnose prompt must describe the triangulation rule."""
    recipe = load_recipe()
    step = _get_loop_step(recipe, "aggregate-diagnose")
    prompt = step.get("prompt", "")
    assert "structural" in prompt.lower(), (
        "aggregate-diagnose prompt must mention 'structural' gaps"
    )
    assert "2" in prompt, (
        "aggregate-diagnose prompt must mention the 2+ topics threshold"
    )


def test_aggregate_diagnose_requires_target_file() -> None:
    """aggregate-diagnose prompt must require identifying a specific target file."""
    recipe = load_recipe()
    step = _get_loop_step(recipe, "aggregate-diagnose")
    prompt = step.get("prompt", "")
    assert "target" in prompt.lower() and "file" in prompt.lower(), (
        "aggregate-diagnose prompt must require a target file for the fix"
    )


# ---------------------------------------------------------------------------
# fix step
# ---------------------------------------------------------------------------


def test_fix_references_diagnosis() -> None:
    """fix prompt must reference the diagnosis output."""
    recipe = load_recipe()
    step = _get_loop_step(recipe, "fix")
    prompt = step.get("prompt", "")
    assert "{{diagnosis}}" in prompt, (
        "fix prompt must reference '{{diagnosis}}'"
    )


def test_fix_requires_git_commit() -> None:
    """fix prompt must require a git commit after the change."""
    recipe = load_recipe()
    step = _get_loop_step(recipe, "fix")
    prompt = step.get("prompt", "")
    assert "commit" in prompt.lower(), (
        "fix prompt must require a git commit"
    )


# ---------------------------------------------------------------------------
# check step
# ---------------------------------------------------------------------------


def test_check_is_bash_type() -> None:
    """check must be type: bash."""
    recipe = load_recipe()
    step = _get_loop_step(recipe, "check")
    assert step.get("type") == "bash", (
        f"check must be type='bash', got {step.get('type')!r}"
    )


def test_check_has_parse_json() -> None:
    """check must have parse_json: true."""
    recipe = load_recipe()
    step = _get_loop_step(recipe, "check")
    assert step.get("parse_json") is True, (
        f"check must have parse_json=true, got {step.get('parse_json')!r}"
    )


def test_check_command_references_score_variables() -> None:
    """check command must reference score_before and score_after."""
    recipe = load_recipe()
    step = _get_loop_step(recipe, "check")
    command = step.get("command", "")
    assert "score_before" in command, "check must reference score_before"
    assert "score_after" in command, "check must reference score_after"


def test_check_command_handles_revert() -> None:
    """check command must include git revert logic."""
    recipe = load_recipe()
    step = _get_loop_step(recipe, "check")
    command = step.get("command", "")
    assert "git revert" in command or "git reset" in command, (
        "check must include git revert logic for regression rollback"
    )


def test_check_command_handles_plateau() -> None:
    """check command must handle plateau counter and convergence."""
    recipe = load_recipe()
    step = _get_loop_step(recipe, "check")
    command = step.get("command", "")
    assert "plateau" in command.lower(), (
        "check must reference plateau counter"
    )
    assert "converged" in command.lower(), (
        "check must set converged flag"
    )


# ---------------------------------------------------------------------------
# log-round step
# ---------------------------------------------------------------------------


def test_log_round_is_bash_type() -> None:
    """log-round must be type: bash."""
    recipe = load_recipe()
    step = _get_loop_step(recipe, "log-round")
    assert step.get("type") == "bash", (
        f"log-round must be type='bash', got {step.get('type')!r}"
    )


def test_log_round_writes_to_reports_dir() -> None:
    """log-round command must write to specs/evaluation/reports/."""
    recipe = load_recipe()
    step = _get_loop_step(recipe, "log-round")
    command = step.get("command", "")
    assert "specs/evaluation/reports" in command, (
        "log-round must write to 'specs/evaluation/reports/'"
    )


def test_log_round_appends_not_overwrites() -> None:
    """log-round command must append (>>), not overwrite (>)."""
    recipe = load_recipe()
    step = _get_loop_step(recipe, "log-round")
    command = step.get("command", "")
    assert ">>" in command, (
        "log-round must use append (>>) not overwrite"
    )


# ---------------------------------------------------------------------------
# Termination summary step (outside loop)
# ---------------------------------------------------------------------------


def test_has_termination_summary_step() -> None:
    """Recipe must have a termination-summary step after the loop."""
    recipe = load_recipe()
    top_step_ids = [s.get("id") for s in recipe.get("steps", []) if s.get("id")]
    assert "termination-summary" in top_step_ids, (
        "Recipe must have a 'termination-summary' step after the loop"
    )


def test_termination_summary_has_output() -> None:
    """termination-summary must have an output declaration."""
    recipe = load_recipe()
    for step in recipe.get("steps", []):
        if step.get("id") == "termination-summary":
            assert "output" in step, (
                "termination-summary must have an 'output' declaration"
            )
            return
    raise AssertionError("termination-summary step not found")
```

**Step 2: Run tests to verify they fail**

Run:
```bash
pytest tests/test_quality_loop_recipe.py -v 2>&1 | head -60
```
Expected: First test (`test_recipe_file_exists`) fails because `recipes/quality-loop.yaml` doesn't exist yet. All subsequent tests also fail.

**Step 3: Commit the tests**
```bash
git add tests/test_quality_loop_recipe.py && git commit -m "test: add structural tests for quality-loop recipe (all failing — TDD)"
```

---

### Task 5: Build Loop Skeleton

**Why:** Create the recipe file with metadata, context variables, and the `while_condition` loop structure. No step implementations yet — just the shell that makes the structural/metadata tests pass.

**Files:**
- Create: `recipes/quality-loop.yaml`

**Step 1: Create the recipe skeleton**

Create `recipes/quality-loop.yaml`:

```yaml
name: "quality-loop"
description: "Autonomous quality improvement loop — evaluates the specialists pipeline against competitors, diagnoses structural gaps, fixes them, and re-evaluates until target score is reached."
version: "1.0.0"
tags: [quality, loop, evaluation, competitive, autonomous]

context:
  target_score: 8.0
  current_score: 0
  plateau_counter: 0
  converged: "false"
  evaluation_mode: "competitive"

steps:
  # ===========================================================================
  # QUALITY IMPROVEMENT LOOP
  # ===========================================================================
  - id: "improvement-loop"
    while_condition: "{{current_score}} < {{target_score}}"
    break_when: "{{converged}} == 'true'"
    max_while_iterations: 5
    update_context:
      current_score: "{{check_result.current_score}}"
      plateau_counter: "{{check_result.plateau_counter}}"
      converged: "{{check_result.converged}}"
    steps:
      # --- Placeholder steps (filled in Tasks 6-10) ---

      - id: "evaluate"
        type: "recipe"
        recipe: "./quality-eval.yaml"
        context:
          evaluation_mode: "{{evaluation_mode}}"
          target_score: "{{target_score}}"
        output: "eval_result"
        timeout: 21600
        on_error: "continue"

      - id: "aggregate-diagnose"
        agent: "self"
        prompt: |
          PLACEHOLDER — will be replaced in Task 7.
          {{eval_result}}
          Identify structural gaps (appearing in 2+ topics out of N).
          Map the top gap to a specific target file and change.
        output: "diagnosis"
        timeout: 1800

      - id: "fix"
        agent: "self"
        prompt: |
          PLACEHOLDER — will be replaced in Task 8.
          {{diagnosis}}
          Implement the change and commit.
        output: "fix_result"
        timeout: 1800

      - id: "check"
        type: "bash"
        command: |
          echo '{"current_score": 0, "plateau_counter": 0, "converged": "false", "score_before": 0, "score_after": 0, "decision": "kept"}'
        parse_json: true
        output: "check_result"
        timeout: 60

      - id: "log-round"
        type: "bash"
        command: |
          echo "placeholder" >> specs/evaluation/reports/quality-loop-log.yaml
        output: "log_result"
        timeout: 30

  # ===========================================================================
  # TERMINATION SUMMARY (runs after loop exits)
  # ===========================================================================
  - id: "termination-summary"
    type: "bash"
    command: |
      echo "Quality loop terminated. Final score: {{current_score}}, Target: {{target_score}}"
    output: "summary"
    timeout: 30
```

**Step 2: Run the structural tests**

Run:
```bash
pytest tests/test_quality_loop_recipe.py -v
```
Expected: Most tests pass. Some will still fail because the placeholder step content doesn't match the detailed assertions (e.g., `test_check_command_handles_revert` — the placeholder `check` command doesn't have `git revert`). That's expected — Tasks 6-10 fill in the real content.

Note which tests pass and which still fail. The following categories should pass now:
- File existence
- Metadata (name, version, tags, required fields)
- Context variables (target_score, current_score, plateau_counter, converged, evaluation_mode)
- While-loop structure (while_condition, break_when, max_while_iterations)
- Loop step presence, uniqueness, ordering, output declarations
- evaluate step (type=recipe, context)
- termination-summary existence and output

**Step 3: Commit**
```bash
git add recipes/quality-loop.yaml && git commit -m "feat: add quality-loop recipe skeleton with while_condition loop structure"
```

---

### Task 6: Build Evaluate Step

**Why:** The evaluate step invokes `quality-eval.yaml` as a sub-recipe. The skeleton already has this wired correctly from Task 5, but let's verify and ensure the full test suite agrees.

**Files:**
- Modify: `recipes/quality-loop.yaml` (verify evaluate step)

**Step 1: Run the evaluate-specific tests**

Run:
```bash
pytest tests/test_quality_loop_recipe.py -k "evaluate" -v
```
Expected: `test_evaluate_invokes_quality_eval` and `test_evaluate_passes_context` both pass (they were wired in the skeleton).

If they already pass, no code changes needed. If not, fix the evaluate step to match:

```yaml
      - id: "evaluate"
        type: "recipe"
        recipe: "./quality-eval.yaml"
        context:
          evaluation_mode: "{{evaluation_mode}}"
          target_score: "{{target_score}}"
        output: "eval_result"
        timeout: 21600
        on_error: "continue"
```

**Step 2: Commit (only if changes were needed)**
```bash
git add recipes/quality-loop.yaml && git commit -m "feat: wire evaluate step to invoke quality-eval sub-recipe"
```

---

### Task 7: Build Aggregate + Diagnose Step

**Why:** This step synthesizes evaluation results across topics, applies the triangulation rule (gap in 2+ topics = structural), ranks all gap candidates, selects the top one with reasoning, and maps it to a specific file and change.

**Files:**
- Modify: `recipes/quality-loop.yaml` (replace the `aggregate-diagnose` placeholder)

**Step 1: Replace the `aggregate-diagnose` step**

In `recipes/quality-loop.yaml`, replace the `aggregate-diagnose` step (the one with `PLACEHOLDER — will be replaced in Task 7`) with:

```yaml
      - id: "aggregate-diagnose"
        agent: "self"
        prompt: |
          QUALITY GAP DIAGNOSTICIAN — you are an expert at identifying structural
          weaknesses in AI pipelines and mapping them to precise fixes.

          EVALUATION RESULTS FROM THIS ROUND:
          {{eval_result}}

          CURRENT LOOP STATE:
          - Round: {{_loop_iteration}} of max 5
          - Current score: {{current_score}}
          - Target score: {{target_score}}
          - Plateau counter: {{plateau_counter}}

          =====================================================================
          STEP 1: TRIANGULATE GAPS
          =====================================================================

          From the evaluation results, extract all gaps where the pipeline scored
          lower than competitors. For each gap dimension:
          1. Count how many topics show this gap (score delta >= 2 points)
          2. Classify: STRUCTURAL (appears in 2 or more out of N topics) or
             TOPIC NOISE (appears in only 1 topic)
          3. For structural gaps, rank by severity (largest average delta first)

          =====================================================================
          STEP 2: LIST ALL CANDIDATES
          =====================================================================

          List EVERY gap candidate — structural and noise — with:
          - Dimension name
          - Classification (STRUCTURAL / TOPIC NOISE)
          - Topics affected (list each)
          - Average score delta vs best competitor
          - Root cause hypothesis

          Do NOT cap or truncate this list. Include every candidate.

          =====================================================================
          STEP 3: SELECT TOP GAP AND MAP TO FIX
          =====================================================================

          Select the single highest-priority STRUCTURAL gap to fix this round.

          Explain your selection reasoning:
          - Why this gap over others?
          - What is the expected impact on the aggregate score?

          Map the gap to a SPECIFIC fix:
          - target_file: The exact file path to modify (e.g., agents/researcher.md,
            agents/data-analyzer.md, agents/writer.md). Use flat paths — agents
            are at agents/<name>.md, NOT agents/<name>/<name>.md.
          - edit_plan: What specific change to make (e.g., "Add a breadth gate
            that scales claim budget to question scope")
          - gap_name: Short name for the gap being addressed
          - all_candidates: The full candidate list from Step 2

          =====================================================================
          OUTPUT FORMAT (required):
          =====================================================================

          End your response with a structured block:

          ## DIAGNOSIS
          - gap_name: [short name]
          - target_file: [exact path]
          - edit_plan: [what to change]
          - chosen_because: [why this gap over others]
          - all_candidates: [list every candidate considered]
          - score_before: [current aggregate pipeline score from evaluation]
        output: "diagnosis"
        timeout: 1800
```

**Step 2: Run the aggregate-diagnose tests**

Run:
```bash
pytest tests/test_quality_loop_recipe.py -k "aggregate_diagnose" -v
```
Expected: `test_aggregate_diagnose_references_eval_result`, `test_aggregate_diagnose_mentions_triangulation`, and `test_aggregate_diagnose_requires_target_file` all PASS.

**Step 3: Commit**
```bash
git add recipes/quality-loop.yaml && git commit -m "feat: implement aggregate-diagnose step with triangulation and candidate ranking"
```

---

### Task 8: Build Fix Step

**Why:** This step reads the diagnosis, opens the target file, implements the minimal change, and commits with a descriptive message.

**Files:**
- Modify: `recipes/quality-loop.yaml` (replace the `fix` placeholder)

**Step 1: Replace the `fix` step**

In `recipes/quality-loop.yaml`, replace the `fix` step (the one with `PLACEHOLDER — will be replaced in Task 8`) with:

```yaml
      - id: "fix"
        agent: "self"
        prompt: |
          PIPELINE FIXER — you implement precisely targeted quality improvements
          to specialist agent files.

          DIAGNOSIS FROM THIS ROUND:
          {{diagnosis}}

          =====================================================================
          YOUR TASK:
          =====================================================================

          1. READ the target file identified in the diagnosis
          2. UNDERSTAND the current behavior and why it produces the identified gap
          3. IMPLEMENT the minimal change described in the edit_plan
             - Change ONLY what the diagnosis specifies
             - Do NOT refactor, reorganize, or "improve" unrelated sections
             - Do NOT add features beyond what the edit_plan describes
          4. VERIFY the change is syntactically valid
          5. COMMIT with a descriptive message:
             git commit -am "fix(quality-loop): [gap_name] — [one-line description of change]"

          =====================================================================
          CONSTRAINTS:
          =====================================================================

          - ONE file change per round. If the diagnosis mentions multiple files,
            change only the primary target_file.
          - The commit message must start with "fix(quality-loop):" so it's
            identifiable for revert.
          - Report the git commit hash in your response.

          =====================================================================
          OUTPUT FORMAT:
          =====================================================================

          End your response with:
          - commit_hash: [the actual hash from git commit]
          - file_changed: [path]
          - change_summary: [one-line description]
        output: "fix_result"
        timeout: 1800
```

**Step 2: Run the fix-specific tests**

Run:
```bash
pytest tests/test_quality_loop_recipe.py -k "fix" -v
```
Expected: `test_fix_references_diagnosis` and `test_fix_requires_git_commit` both PASS.

**Step 3: Commit**
```bash
git add recipes/quality-loop.yaml && git commit -m "feat: implement fix step with single-file change and git commit"
```

---

### Task 9: Build Check Step

**Why:** This is the safety net. After every fix, the check step compares scores. If the score dropped or stayed flat, it reverts the fix via `git revert`. It also manages the plateau counter and convergence detection.

**Files:**
- Modify: `recipes/quality-loop.yaml` (replace the `check` placeholder)

**Step 1: Replace the `check` step**

In `recipes/quality-loop.yaml`, replace the entire `check` step (the one with the placeholder JSON echo) with:

```yaml
      - id: "check"
        type: "bash"
        command: |
          cat <<'__CHECK__' > /dev/null
          {{fix_result}}
          __CHECK__

          cat <<'__DIAG__' > /dev/null
          {{diagnosis}}
          __DIAG__

          # --- Extract score_before from diagnosis output ---
          score_before="{{current_score}}"

          # Parse score_before from the diagnosis (it reports the current aggregate)
          diag_score=$(cat <<'__EXTRACT__' | grep -oP 'score_before:\s*\K[0-9]+\.?[0-9]*' | head -1
          {{diagnosis}}
          __EXTRACT__
          )
          if [ -n "$diag_score" ]; then
            score_before="$diag_score"
          fi

          # score_after starts equal to score_before (will be updated by next eval)
          score_after="${score_before}"

          # Current plateau_counter
          plateau_counter={{plateau_counter}}

          # Get the latest commit (the fix commit)
          fix_commit=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")

          # --- Decision logic ---
          # On round 1, we have no prior score to compare — always keep.
          # On subsequent rounds, if score hasn't improved, revert and bump plateau.
          decision="kept"
          new_plateau=$plateau_counter
          converged="false"

          if [ "{{_loop_iteration}}" -gt 1 ] && [ "$score_before" != "0" ]; then
            # Compare: if score hasn't improved from last known score
            improved=$(python3 -c "print('yes' if float('${score_after}') > float('${score_before}') else 'no')" 2>/dev/null || echo "no")

            if [ "$improved" = "no" ]; then
              # Revert the fix
              git revert --no-edit HEAD 2>/dev/null || true
              decision="reverted"
              new_plateau=$((plateau_counter + 1))

              # Check convergence: 2 consecutive non-improving rounds
              if [ $new_plateau -ge 2 ]; then
                converged="true"
              fi
            else
              new_plateau=0
            fi
          fi

          # Output JSON for update_context
          cat <<EOF
          {
            "current_score": ${score_after:-0},
            "score_before": ${score_before:-0},
            "score_after": ${score_after:-0},
            "plateau_counter": ${new_plateau},
            "converged": "${converged}",
            "decision": "${decision}",
            "fix_commit": "${fix_commit}"
          }
          EOF
        parse_json: true
        output: "check_result"
        timeout: 60
```

**Step 2: Run the check-specific tests**

Run:
```bash
pytest tests/test_quality_loop_recipe.py -k "check" -v
```
Expected: `test_check_is_bash_type`, `test_check_has_parse_json`, `test_check_command_references_score_variables`, `test_check_command_handles_revert`, and `test_check_command_handles_plateau` all PASS.

**Step 3: Commit**
```bash
git add recipes/quality-loop.yaml && git commit -m "feat: implement check step with revert-on-regression and convergence detection"
```

---

### Task 10: Build Observability (Log Round + Termination Summary)

**Why:** Every round writes a structured log entry to an append-only file. This survives interruptions — if the loop crashes, you have logs for every completed round. The termination summary provides the final scorecard.

**Files:**
- Modify: `recipes/quality-loop.yaml` (replace `log-round` placeholder and update `termination-summary`)

**Step 1: Replace the `log-round` step**

In `recipes/quality-loop.yaml`, replace the `log-round` step (the one with `echo "placeholder"`) with:

```yaml
      - id: "log-round"
        type: "bash"
        command: |
          mkdir -p specs/evaluation/reports

          cat <<'__DIAG__' > /tmp/quality-loop-diag-extract.txt
          {{diagnosis}}
          __DIAG__

          cat <<'__FIX__' > /tmp/quality-loop-fix-extract.txt
          {{fix_result}}
          __FIX__

          # Extract fields from diagnosis and check_result
          gap_name=$(grep -oP 'gap_name:\s*\K.*' /tmp/quality-loop-diag-extract.txt | head -1 || echo "unknown")
          target_file=$(grep -oP 'target_file:\s*\K.*' /tmp/quality-loop-diag-extract.txt | head -1 || echo "unknown")
          edit_plan=$(grep -oP 'edit_plan:\s*\K.*' /tmp/quality-loop-diag-extract.txt | head -1 || echo "unknown")
          chosen_because=$(grep -oP 'chosen_because:\s*\K.*' /tmp/quality-loop-diag-extract.txt | head -1 || echo "unknown")

          # Write the round log entry (append-only)
          cat >> specs/evaluation/reports/quality-loop-log.yaml <<ENTRY
          ---
          round: {{_loop_iteration}}
          gap: "${gap_name}"
          candidates: "see diagnosis output for full list"
          chosen_because: "${chosen_because}"
          target: "${target_file}"
          edit_plan: "${edit_plan}"
          commit: "{{check_result.fix_commit}}"
          score_before: {{check_result.score_before}}
          score_after: {{check_result.score_after}}
          decision: "{{check_result.decision}}"
          plateau_counter: {{check_result.plateau_counter}}
          ENTRY

          echo "Round {{_loop_iteration}} logged to specs/evaluation/reports/quality-loop-log.yaml"
        output: "log_result"
        timeout: 30
```

**Step 2: Replace the `termination-summary` step**

Replace the `termination-summary` step (outside the loop, at the bottom of the file) with:

```yaml
  # ===========================================================================
  # TERMINATION SUMMARY (runs after loop exits)
  # ===========================================================================
  - id: "termination-summary"
    type: "bash"
    command: |
      echo "============================================================="
      echo "QUALITY LOOP TERMINATED"
      echo "============================================================="
      echo ""
      echo "Final score:       {{current_score}}"
      echo "Target score:      {{target_score}}"
      echo "Plateau counter:   {{plateau_counter}}"
      echo "Converged:         {{converged}}"
      echo ""

      # Determine exit reason
      if [ "{{converged}}" = "true" ]; then
        echo "Exit reason: CONVERGENCE — score did not improve for 2 consecutive rounds"
      elif python3 -c "exit(0 if float('{{current_score}}') >= float('{{target_score}}') else 1)" 2>/dev/null; then
        echo "Exit reason: TARGET REACHED — score >= target"
      else
        echo "Exit reason: MAX ITERATIONS — reached 5 iteration cap"
      fi

      echo ""
      echo "Round-by-round log:"
      echo "-------------------------------------------------------------"
      if [ -f specs/evaluation/reports/quality-loop-log.yaml ]; then
        cat specs/evaluation/reports/quality-loop-log.yaml
      else
        echo "(no rounds logged)"
      fi
      echo "-------------------------------------------------------------"
    output: "summary"
    timeout: 30
```

**Step 3: Run the observability tests**

Run:
```bash
pytest tests/test_quality_loop_recipe.py -k "log_round or termination" -v
```
Expected: `test_log_round_is_bash_type`, `test_log_round_writes_to_reports_dir`, `test_log_round_appends_not_overwrites`, `test_has_termination_summary_step`, and `test_termination_summary_has_output` all PASS.

**Step 4: Run the FULL test suite**

Run:
```bash
pytest tests/test_quality_loop_recipe.py -v
```
Expected: ALL tests pass. If any fail, fix them before committing.

**Step 5: Also run the existing test suites to confirm no regressions**

Run:
```bash
pytest tests/test_quality_eval_recipe.py tests/test_quality_eval_iteration_recipe.py tests/test_competitors_config.py -v
```
Expected: All existing tests still pass.

**Step 6: Commit**
```bash
git add recipes/quality-loop.yaml && git commit -m "feat: implement observability logging and termination summary for quality loop"
```

---

## Final Verification

After all 10 tasks are complete, run the full test suite one last time:

```bash
pytest tests/ -v --tb=short 2>&1 | tail -30
```

All tests should pass. The following files should have been created or modified:

| File | Action |
|------|--------|
| `specs/evaluation/score-history.yaml` | Modified — removed stray `[]` |
| `specs/evaluation/test-topics.yaml` | Modified — added 2 competitive-eval topics |
| `recipes/quality-eval-iteration.yaml` | Modified — added `provider_preferences` |
| `tests/test_quality_eval_iteration_recipe.py` | Modified — added routing test |
| `tests/test_quality_loop_recipe.py` | Created — 39 structural tests |
| `recipes/quality-loop.yaml` | Created — the quality loop recipe |
