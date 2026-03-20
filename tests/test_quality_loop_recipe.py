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
