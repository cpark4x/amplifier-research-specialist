"""Validation tests for recipes/quality-eval.yaml.

Ensures the main quality-eval orchestrator recipe is structurally correct and
implements the full competitive evaluation loop: load topics, run per-topic
iterations as a sub-recipe, aggregate cross-topic results, and save the gap report.
"""

from __future__ import annotations

from pathlib import Path

import yaml

RECIPE_PATH = Path(__file__).parent.parent / "recipes" / "quality-eval.yaml"


def load_recipe() -> dict:
    assert RECIPE_PATH.exists(), f"Recipe file not found: {RECIPE_PATH}"
    with RECIPE_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------


def test_recipe_file_exists() -> None:
    """recipes/quality-eval.yaml must exist."""
    assert RECIPE_PATH.exists(), "recipes/quality-eval.yaml must exist"


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------


def test_recipe_name() -> None:
    """Recipe name must be 'quality-eval'."""
    recipe = load_recipe()
    assert recipe["name"] == "quality-eval", (
        f"Expected name='quality-eval', got {recipe.get('name')!r}"
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


def test_recipe_tags_include_evaluation() -> None:
    """Recipe tags must include 'evaluation'."""
    recipe = load_recipe()
    tags = recipe.get("tags", [])
    assert "evaluation" in tags, f"Tags must include 'evaluation', got {tags}"


def test_recipe_tags_include_competitive() -> None:
    """Recipe tags must include 'competitive'."""
    recipe = load_recipe()
    tags = recipe.get("tags", [])
    assert "competitive" in tags, f"Tags must include 'competitive', got {tags}"


# ---------------------------------------------------------------------------
# Context variables
# ---------------------------------------------------------------------------


def test_context_has_evaluation_mode() -> None:
    """Context must have 'evaluation_mode' variable."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert "evaluation_mode" in context, "Context must have 'evaluation_mode'"


def test_context_evaluation_mode_defaults_to_competitive() -> None:
    """evaluation_mode must default to 'competitive'."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert context.get("evaluation_mode") == "competitive", (
        f"evaluation_mode must default to 'competitive', "
        f"got {context.get('evaluation_mode')!r}"
    )


def test_context_has_target_score() -> None:
    """Context must have 'target_score' variable."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert "target_score" in context, "Context must have 'target_score'"


# ---------------------------------------------------------------------------
# Steps — presence and uniqueness
# ---------------------------------------------------------------------------


def test_has_required_step_ids() -> None:
    """Steps must include: load-topics, run-topic-iterations, aggregate-results, save-gap-report."""
    recipe = load_recipe()
    step_ids = [s["id"] for s in recipe.get("steps", [])]
    required = {
        "load-topics",
        "run-topic-iterations",
        "aggregate-results",
        "save-gap-report",
    }
    missing = required - set(step_ids)
    assert not missing, f"Recipe missing required step IDs: {missing}"


def test_step_ids_unique() -> None:
    """No duplicate step IDs."""
    recipe = load_recipe()
    step_ids = [s["id"] for s in recipe.get("steps", [])]
    assert len(step_ids) == len(set(step_ids)), (
        f"Duplicate step IDs found: {[s for s in step_ids if step_ids.count(s) > 1]}"
    )


def test_all_steps_have_output() -> None:
    """Every step declares an output variable."""
    recipe = load_recipe()
    for step in recipe.get("steps", []):
        assert "output" in step, (
            f"Step '{step.get('id', '<unknown>')}' is missing 'output' declaration"
        )


# ---------------------------------------------------------------------------
# Step ordering constraints
# ---------------------------------------------------------------------------


def _step_index(recipe: dict, step_id: str) -> int:
    step_ids = [s["id"] for s in recipe.get("steps", [])]
    assert step_id in step_ids, f"Step '{step_id}' not found in recipe"
    return step_ids.index(step_id)


def test_load_topics_before_run_topic_iterations() -> None:
    """load-topics must come before run-topic-iterations."""
    recipe = load_recipe()
    load_idx = _step_index(recipe, "load-topics")
    run_idx = _step_index(recipe, "run-topic-iterations")
    assert load_idx < run_idx, (
        f"load-topics (index {load_idx}) must come before "
        f"run-topic-iterations (index {run_idx})"
    )


def test_run_topic_iterations_before_aggregate_results() -> None:
    """run-topic-iterations must come before aggregate-results."""
    recipe = load_recipe()
    run_idx = _step_index(recipe, "run-topic-iterations")
    agg_idx = _step_index(recipe, "aggregate-results")
    assert run_idx < agg_idx, (
        f"run-topic-iterations (index {run_idx}) must come before "
        f"aggregate-results (index {agg_idx})"
    )


def test_aggregate_results_before_save_gap_report() -> None:
    """aggregate-results must come before save-gap-report."""
    recipe = load_recipe()
    agg_idx = _step_index(recipe, "aggregate-results")
    save_idx = _step_index(recipe, "save-gap-report")
    assert agg_idx < save_idx, (
        f"aggregate-results (index {agg_idx}) must come before "
        f"save-gap-report (index {save_idx})"
    )


# ---------------------------------------------------------------------------
# load-topics step
# ---------------------------------------------------------------------------


def _get_step(recipe: dict, step_id: str) -> dict:
    for step in recipe.get("steps", []):
        if step["id"] == step_id:
            return step
    raise AssertionError(f"Step '{step_id}' not found in recipe")


def test_load_topics_is_bash_type() -> None:
    """load-topics must be type: bash."""
    recipe = load_recipe()
    step = _get_step(recipe, "load-topics")
    assert step.get("type") == "bash", (
        f"load-topics must be type='bash', got {step.get('type')!r}"
    )


def test_load_topics_reads_test_topics_yaml() -> None:
    """load-topics command must read specs/evaluation/test-topics.yaml."""
    recipe = load_recipe()
    step = _get_step(recipe, "load-topics")
    command = step.get("command", "")
    assert "test-topics.yaml" in command, (
        "load-topics command must reference 'test-topics.yaml'"
    )


def test_load_topics_filters_competitive_eval() -> None:
    """load-topics command must filter for profile == 'competitive-eval'."""
    recipe = load_recipe()
    step = _get_step(recipe, "load-topics")
    command = step.get("command", "")
    assert "competitive-eval" in command, (
        "load-topics command must filter for 'competitive-eval' profile"
    )


def test_load_topics_has_parse_json() -> None:
    """load-topics must have parse_json: true."""
    recipe = load_recipe()
    step = _get_step(recipe, "load-topics")
    assert step.get("parse_json") is True, (
        f"load-topics must have parse_json=true, got {step.get('parse_json')!r}"
    )


def test_load_topics_timeout() -> None:
    """load-topics timeout must be 10."""
    recipe = load_recipe()
    step = _get_step(recipe, "load-topics")
    assert step.get("timeout") == 10, (
        f"load-topics timeout must be 10, got {step.get('timeout')!r}"
    )


# ---------------------------------------------------------------------------
# run-topic-iterations step
# ---------------------------------------------------------------------------


def test_run_topic_iterations_has_foreach() -> None:
    """run-topic-iterations must have a foreach clause."""
    recipe = load_recipe()
    step = _get_step(recipe, "run-topic-iterations")
    assert "foreach" in step, "run-topic-iterations must have 'foreach'"


def test_run_topic_iterations_foreach_references_topics() -> None:
    """run-topic-iterations foreach must reference {{topics}}."""
    recipe = load_recipe()
    step = _get_step(recipe, "run-topic-iterations")
    foreach_val = step.get("foreach", "")
    assert "topics" in str(foreach_val), (
        f"run-topic-iterations foreach must reference 'topics', got {foreach_val!r}"
    )


def test_run_topic_iterations_has_collect_topic_results() -> None:
    """run-topic-iterations must collect results into 'topic_results'."""
    recipe = load_recipe()
    step = _get_step(recipe, "run-topic-iterations")
    assert step.get("collect") == "topic_results", (
        f"run-topic-iterations collect must be 'topic_results', "
        f"got {step.get('collect')!r}"
    )


def test_run_topic_iterations_is_recipe_type() -> None:
    """run-topic-iterations must be type: recipe."""
    recipe = load_recipe()
    step = _get_step(recipe, "run-topic-iterations")
    assert step.get("type") == "recipe", (
        f"run-topic-iterations must be type='recipe', got {step.get('type')!r}"
    )


def test_run_topic_iterations_invokes_quality_eval_iteration() -> None:
    """run-topic-iterations must invoke quality-eval-iteration.yaml."""
    recipe = load_recipe()
    step = _get_step(recipe, "run-topic-iterations")
    recipe_ref = step.get("recipe", "")
    assert "quality-eval-iteration" in recipe_ref, (
        f"run-topic-iterations must reference 'quality-eval-iteration', "
        f"got {recipe_ref!r}"
    )


def test_run_topic_iterations_passes_research_question_in_context() -> None:
    """run-topic-iterations context must pass research_question."""
    recipe = load_recipe()
    step = _get_step(recipe, "run-topic-iterations")
    context = step.get("context", {})
    assert "research_question" in context, (
        "run-topic-iterations context must include 'research_question'"
    )


def test_run_topic_iterations_passes_topic_id_in_context() -> None:
    """run-topic-iterations context must pass topic_id."""
    recipe = load_recipe()
    step = _get_step(recipe, "run-topic-iterations")
    context = step.get("context", {})
    assert "topic_id" in context, "run-topic-iterations context must include 'topic_id'"


def test_run_topic_iterations_supports_parallel() -> None:
    """run-topic-iterations should run topics in parallel for speed (topics are independent)."""
    recipe = load_recipe()
    step = _get_step(recipe, "run-topic-iterations")
    parallel = step.get("parallel")
    assert parallel is not None and parallel > 1, (
        f"run-topic-iterations should have parallel >= 2 for speed "
        f"(topics are independent, no shared state), got parallel={parallel!r}"
    )


# ---------------------------------------------------------------------------
# aggregate-results step
# ---------------------------------------------------------------------------


def test_aggregate_results_uses_self_agent() -> None:
    """aggregate-results must use agent: 'self'."""
    recipe = load_recipe()
    step = _get_step(recipe, "aggregate-results")
    assert step.get("agent") == "self", (
        f"aggregate-results must use agent='self', got {step.get('agent')!r}"
    )


def test_aggregate_results_prompt_references_topic_results() -> None:
    """aggregate-results prompt must reference {{topic_results}}."""
    recipe = load_recipe()
    step = _get_step(recipe, "aggregate-results")
    prompt = step.get("prompt", "")
    assert "{{topic_results}}" in prompt, (
        "aggregate-results prompt must reference '{{topic_results}}'"
    )


def test_aggregate_results_prompt_references_evaluation_mode() -> None:
    """aggregate-results prompt must reference {{evaluation_mode}}."""
    recipe = load_recipe()
    step = _get_step(recipe, "aggregate-results")
    prompt = step.get("prompt", "")
    assert "{{evaluation_mode}}" in prompt, (
        "aggregate-results prompt must reference '{{evaluation_mode}}'"
    )


def test_aggregate_results_prompt_references_target_score() -> None:
    """aggregate-results prompt must reference {{target_score}}."""
    recipe = load_recipe()
    step = _get_step(recipe, "aggregate-results")
    prompt = step.get("prompt", "")
    assert "{{target_score}}" in prompt, (
        "aggregate-results prompt must reference '{{target_score}}'"
    )


def test_aggregate_results_prompt_mentions_structural_gaps() -> None:
    """aggregate-results prompt must describe structural gap triangulation logic."""
    recipe = load_recipe()
    step = _get_step(recipe, "aggregate-results")
    prompt = step.get("prompt", "")
    assert "structural" in prompt.lower(), (
        "aggregate-results prompt must mention 'structural' gaps"
    )


def test_aggregate_results_prompt_produces_gap_report() -> None:
    """aggregate-results prompt must produce a gap report."""
    recipe = load_recipe()
    step = _get_step(recipe, "aggregate-results")
    prompt = step.get("prompt", "")
    assert "gap report" in prompt.lower() or "gap" in prompt.lower(), (
        "aggregate-results prompt must reference 'gap report' output"
    )


# ---------------------------------------------------------------------------
# save-gap-report step
# ---------------------------------------------------------------------------


def test_save_gap_report_uses_file_ops_agent() -> None:
    """save-gap-report must use agent: 'foundation:file-ops'."""
    recipe = load_recipe()
    step = _get_step(recipe, "save-gap-report")
    assert step.get("agent") == "foundation:file-ops", (
        f"save-gap-report must use agent='foundation:file-ops', "
        f"got {step.get('agent')!r}"
    )


def test_save_gap_report_targets_reports_directory() -> None:
    """save-gap-report must save to specs/evaluation/reports/."""
    recipe = load_recipe()
    step = _get_step(recipe, "save-gap-report")
    prompt = step.get("prompt", "")
    assert "specs/evaluation/reports" in prompt, (
        "save-gap-report prompt must target 'specs/evaluation/reports/'"
    )


def test_save_gap_report_saves_quality_eval_report_md() -> None:
    """save-gap-report must save to quality-eval-report.md."""
    recipe = load_recipe()
    step = _get_step(recipe, "save-gap-report")
    prompt = step.get("prompt", "")
    assert "quality-eval-report.md" in prompt, (
        "save-gap-report prompt must reference 'quality-eval-report.md'"
    )
