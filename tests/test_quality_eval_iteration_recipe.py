"""Validation tests for recipes/quality-eval-iteration.yaml.

Ensures the quality-eval-iteration sub-recipe is structurally correct and
implements the full competitive evaluation loop: load competitors, run pipeline,
capture output, run competitors in parallel, evaluate all outputs.
"""

from __future__ import annotations

from pathlib import Path

import yaml

RECIPE_PATH = Path(__file__).parent.parent / "recipes" / "quality-eval-iteration.yaml"


def load_recipe() -> dict:
    assert RECIPE_PATH.exists(), f"Recipe file not found: {RECIPE_PATH}"
    with RECIPE_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------


def test_recipe_file_exists() -> None:
    """recipes/quality-eval-iteration.yaml must exist."""
    assert RECIPE_PATH.exists(), "recipes/quality-eval-iteration.yaml must exist"


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------


def test_recipe_name() -> None:
    """Recipe name must be 'quality-eval-iteration'."""
    recipe = load_recipe()
    assert recipe["name"] == "quality-eval-iteration", (
        f"Expected name='quality-eval-iteration', got {recipe.get('name')!r}"
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


def test_context_has_research_question() -> None:
    """Context must have 'research_question' variable."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert "research_question" in context, "Context must have 'research_question'"


def test_context_has_topic_id() -> None:
    """Context must have 'topic_id' variable."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert "topic_id" in context, "Context must have 'topic_id'"


def test_context_research_question_default_empty() -> None:
    """research_question must default to empty string."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert (
        context.get("research_question") == ""
        or context.get("research_question") is None
    ), "research_question must have empty default"


def test_context_topic_id_default_empty() -> None:
    """topic_id must default to empty string."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert context.get("topic_id") == "" or context.get("topic_id") is None, (
        "topic_id must have empty default"
    )


# ---------------------------------------------------------------------------
# Steps — presence and uniqueness
# ---------------------------------------------------------------------------


def test_has_required_step_ids() -> None:
    """Steps must include: load-competitors, mark-pipeline-start, run-pipeline, capture-pipeline-output, run-competitors, evaluate."""
    recipe = load_recipe()
    step_ids = [s["id"] for s in recipe.get("steps", [])]
    required = {
        "load-competitors",
        "mark-pipeline-start",
        "run-pipeline",
        "capture-pipeline-output",
        "run-competitors",
        "evaluate",
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


def test_load_competitors_before_run_competitors() -> None:
    """load-competitors must come before run-competitors."""
    recipe = load_recipe()
    load_idx = _step_index(recipe, "load-competitors")
    run_idx = _step_index(recipe, "run-competitors")
    assert load_idx < run_idx, (
        f"load-competitors (index {load_idx}) must come before "
        f"run-competitors (index {run_idx})"
    )


def test_mark_pipeline_start_before_run_pipeline() -> None:
    """mark-pipeline-start must come before run-pipeline."""
    recipe = load_recipe()
    mark_idx = _step_index(recipe, "mark-pipeline-start")
    pipeline_idx = _step_index(recipe, "run-pipeline")
    assert mark_idx < pipeline_idx, (
        f"mark-pipeline-start (index {mark_idx}) must come before "
        f"run-pipeline (index {pipeline_idx})"
    )


def test_run_pipeline_before_evaluate() -> None:
    """run-pipeline must come before evaluate."""
    recipe = load_recipe()
    pipeline_idx = _step_index(recipe, "run-pipeline")
    eval_idx = _step_index(recipe, "evaluate")
    assert pipeline_idx < eval_idx, (
        f"run-pipeline (index {pipeline_idx}) must come before evaluate (index {eval_idx})"
    )


def test_run_competitors_before_evaluate() -> None:
    """run-competitors must come before evaluate."""
    recipe = load_recipe()
    competitors_idx = _step_index(recipe, "run-competitors")
    eval_idx = _step_index(recipe, "evaluate")
    assert competitors_idx < eval_idx, (
        f"run-competitors (index {competitors_idx}) must come before "
        f"evaluate (index {eval_idx})"
    )


def test_capture_pipeline_output_between_run_pipeline_and_evaluate() -> None:
    """capture-pipeline-output must come after run-pipeline and before evaluate."""
    recipe = load_recipe()
    pipeline_idx = _step_index(recipe, "run-pipeline")
    capture_idx = _step_index(recipe, "capture-pipeline-output")
    eval_idx = _step_index(recipe, "evaluate")
    assert pipeline_idx < capture_idx < eval_idx, (
        f"capture-pipeline-output (index {capture_idx}) must be between "
        f"run-pipeline (index {pipeline_idx}) and evaluate (index {eval_idx})"
    )


# ---------------------------------------------------------------------------
# mark-pipeline-start step
# ---------------------------------------------------------------------------


def test_mark_pipeline_start_is_bash_type() -> None:
    """mark-pipeline-start must be type: bash."""
    recipe = load_recipe()
    step = _get_step(recipe, "mark-pipeline-start")
    assert step.get("type") == "bash", (
        f"mark-pipeline-start must be type='bash', got {step.get('type')!r}"
    )


def test_mark_pipeline_start_has_output() -> None:
    """mark-pipeline-start must declare an output variable."""
    recipe = load_recipe()
    step = _get_step(recipe, "mark-pipeline-start")
    assert "output" in step, "mark-pipeline-start must have an 'output' declaration"


def test_mark_pipeline_start_records_marker() -> None:
    """mark-pipeline-start command must create a marker (touch or timestamp)."""
    recipe = load_recipe()
    step = _get_step(recipe, "mark-pipeline-start")
    command = step.get("command", "")
    # Must either touch a marker file or record a timestamp
    assert "touch" in command or "date" in command or "epoch" in command.lower(), (
        "mark-pipeline-start must create a marker file (touch) or record a timestamp (date)"
    )


# ---------------------------------------------------------------------------
# load-competitors step
# ---------------------------------------------------------------------------


def _get_step(recipe: dict, step_id: str) -> dict:
    for step in recipe.get("steps", []):
        if step["id"] == step_id:
            return step
    raise AssertionError(f"Step '{step_id}' not found in recipe")


def test_load_competitors_is_bash_type() -> None:
    """load-competitors must be type: bash."""
    recipe = load_recipe()
    step = _get_step(recipe, "load-competitors")
    assert step.get("type") == "bash", (
        f"load-competitors must be type='bash', got {step.get('type')!r}"
    )


def test_load_competitors_reads_competitors_yaml() -> None:
    """load-competitors command must read specs/evaluation/competitors.yaml."""
    recipe = load_recipe()
    step = _get_step(recipe, "load-competitors")
    command = step.get("command", "")
    assert "competitors.yaml" in command, (
        "load-competitors command must reference 'competitors.yaml'"
    )


def test_load_competitors_has_parse_json() -> None:
    """load-competitors must have parse_json: true."""
    recipe = load_recipe()
    step = _get_step(recipe, "load-competitors")
    assert step.get("parse_json") is True, (
        f"load-competitors must have parse_json=true, got {step.get('parse_json')!r}"
    )


def test_load_competitors_timeout() -> None:
    """load-competitors timeout must be 10."""
    recipe = load_recipe()
    step = _get_step(recipe, "load-competitors")
    assert step.get("timeout") == 10, (
        f"load-competitors timeout must be 10, got {step.get('timeout')!r}"
    )


# ---------------------------------------------------------------------------
# run-pipeline step
# ---------------------------------------------------------------------------


def test_run_pipeline_is_recipe_type() -> None:
    """run-pipeline must delegate to agent 'self'."""
    recipe = load_recipe()
    step = _get_step(recipe, "run-pipeline")
    assert step.get("agent") == "self", (
        f"run-pipeline must use agent='self', got {step.get('agent')!r}"
    )


def test_run_pipeline_references_specialists_researcher() -> None:
    """run-pipeline prompt must reference 'specialists:researcher' for direct chain orchestration."""
    recipe = load_recipe()
    step = _get_step(recipe, "run-pipeline")
    prompt = step.get("prompt", "")
    assert "specialists:researcher" in prompt, (
        f"run-pipeline prompt must reference 'specialists:researcher', got {prompt!r}"
    )


def test_run_pipeline_passes_research_question_in_context() -> None:
    """run-pipeline prompt must pass {{research_question}} template variable."""
    recipe = load_recipe()
    step = _get_step(recipe, "run-pipeline")
    prompt = step.get("prompt", "")
    assert "{{research_question}}" in prompt, (
        "run-pipeline prompt must contain '{{research_question}}'"
    )


def test_run_pipeline_research_question_references_template_var() -> None:
    """run-pipeline prompt must reference {{research_question}} template variable."""
    recipe = load_recipe()
    step = _get_step(recipe, "run-pipeline")
    prompt = step.get("prompt", "")
    assert "{{research_question}}" in prompt, (
        f"run-pipeline prompt must use '{{{{research_question}}}}', got {prompt!r}"
    )


# ---------------------------------------------------------------------------
# capture-pipeline-output step
# ---------------------------------------------------------------------------


def test_capture_pipeline_output_is_bash_type() -> None:
    """capture-pipeline-output must be type: bash."""
    recipe = load_recipe()
    step = _get_step(recipe, "capture-pipeline-output")
    assert step.get("type") == "bash", (
        f"capture-pipeline-output must be type='bash', got {step.get('type')!r}"
    )


def test_capture_pipeline_output_reads_docs_research_output() -> None:
    """capture-pipeline-output command must read from docs/research-output/."""
    recipe = load_recipe()
    step = _get_step(recipe, "capture-pipeline-output")
    command = step.get("command", "")
    assert "docs/research-output" in command, (
        "capture-pipeline-output must read from 'docs/research-output/'"
    )


def test_capture_pipeline_output_handles_missing_file() -> None:
    """capture-pipeline-output must handle no output file gracefully."""
    recipe = load_recipe()
    step = _get_step(recipe, "capture-pipeline-output")
    command = step.get("command", "")
    assert "PIPELINE_ERROR" in command, (
        "capture-pipeline-output must output 'PIPELINE_ERROR' when no file is found"
    )


def test_capture_pipeline_output_detects_stale_output() -> None:
    """capture-pipeline-output must detect stale output using the pipeline start marker."""
    recipe = load_recipe()
    step = _get_step(recipe, "capture-pipeline-output")
    command = step.get("command", "")
    # Must reference the marker output from mark-pipeline-start
    mark_step = _get_step(recipe, "mark-pipeline-start")
    marker_output_var = mark_step.get("output", "")
    assert marker_output_var in command, (
        f"capture-pipeline-output must reference the mark-pipeline-start output "
        f"variable '{{{{ {marker_output_var} }}}}' to detect stale files, "
        f"but it was not found in the command"
    )
    assert "Stale output" in command or "stale" in command.lower(), (
        "capture-pipeline-output must output a stale-output error message"
    )


def test_capture_pipeline_output_timeout() -> None:
    """capture-pipeline-output timeout must be 30."""
    recipe = load_recipe()
    step = _get_step(recipe, "capture-pipeline-output")
    assert step.get("timeout") == 30, (
        f"capture-pipeline-output timeout must be 30, got {step.get('timeout')!r}"
    )


# ---------------------------------------------------------------------------
# run-competitors step
# ---------------------------------------------------------------------------


def test_run_competitors_has_foreach() -> None:
    """run-competitors must have a foreach clause."""
    recipe = load_recipe()
    step = _get_step(recipe, "run-competitors")
    assert "foreach" in step, "run-competitors must have 'foreach'"


def test_run_competitors_foreach_references_competitors() -> None:
    """run-competitors foreach must reference {{competitors}}."""
    recipe = load_recipe()
    step = _get_step(recipe, "run-competitors")
    foreach_val = step.get("foreach", "")
    assert "competitors" in str(foreach_val), (
        f"run-competitors foreach must reference 'competitors', got {foreach_val!r}"
    )


def test_run_competitors_has_parallel() -> None:
    """run-competitors must have a parallel setting."""
    recipe = load_recipe()
    step = _get_step(recipe, "run-competitors")
    assert "parallel" in step, "run-competitors must have 'parallel'"


def test_run_competitors_parallel_is_at_least_3() -> None:
    """run-competitors parallel must be >= 3 (or true)."""
    recipe = load_recipe()
    step = _get_step(recipe, "run-competitors")
    parallel = step.get("parallel")
    # Accept: True (meaning unlimited), or integer >= 3
    if parallel is True:
        pass  # fully parallel — acceptable
    else:
        assert int(parallel) >= 3, (
            f"run-competitors parallel must be >= 3, got {parallel!r}"
        )


def test_run_competitors_has_collect() -> None:
    """run-competitors must collect results into 'competitor_results'."""
    recipe = load_recipe()
    step = _get_step(recipe, "run-competitors")
    assert step.get("collect") == "competitor_results", (
        f"run-competitors collect must be 'competitor_results', "
        f"got {step.get('collect')!r}"
    )


def test_run_competitors_uses_foundation_web_research_agent() -> None:
    """run-competitors must use agent 'foundation:web-research'."""
    recipe = load_recipe()
    step = _get_step(recipe, "run-competitors")
    assert step.get("agent") == "foundation:web-research", (
        f"run-competitors must use agent 'foundation:web-research', "
        f"got {step.get('agent')!r}"
    )


def test_run_competitors_prompt_references_research_question() -> None:
    """run-competitors prompt must reference {{research_question}}."""
    recipe = load_recipe()
    step = _get_step(recipe, "run-competitors")
    prompt = step.get("prompt", "")
    assert "{{research_question}}" in prompt, (
        "run-competitors prompt must reference '{{research_question}}'"
    )


# ---------------------------------------------------------------------------
# evaluate step
# ---------------------------------------------------------------------------


def test_evaluate_uses_self_agent() -> None:
    """evaluate must use agent: 'self'."""
    recipe = load_recipe()
    step = _get_step(recipe, "evaluate")
    assert step.get("agent") == "self", (
        f"evaluate must use agent='self', got {step.get('agent')!r}"
    )


def test_evaluate_prompt_references_pipeline_output() -> None:
    """evaluate prompt must reference {{pipeline_output}}."""
    recipe = load_recipe()
    step = _get_step(recipe, "evaluate")
    prompt = step.get("prompt", "")
    assert "{{pipeline_output}}" in prompt, (
        "evaluate prompt must reference '{{pipeline_output}}'"
    )


def test_evaluate_prompt_references_competitor_results() -> None:
    """evaluate prompt must reference {{competitor_results}}."""
    recipe = load_recipe()
    step = _get_step(recipe, "evaluate")
    prompt = step.get("prompt", "")
    assert "{{competitor_results}}" in prompt, (
        "evaluate prompt must reference '{{competitor_results}}'"
    )


def test_evaluate_prompt_references_topic_id() -> None:
    """evaluate prompt must reference {{topic_id}}."""
    recipe = load_recipe()
    step = _get_step(recipe, "evaluate")
    prompt = step.get("prompt", "")
    assert "{{topic_id}}" in prompt, "evaluate prompt must reference '{{topic_id}}'"


def test_evaluate_prompt_references_research_question() -> None:
    """evaluate prompt must reference {{research_question}}."""
    recipe = load_recipe()
    step = _get_step(recipe, "evaluate")
    prompt = step.get("prompt", "")
    assert "{{research_question}}" in prompt, (
        "evaluate prompt must reference '{{research_question}}'"
    )


def test_evaluate_prompt_scores_six_dimensions() -> None:
    """evaluate prompt must score at least 6 evaluation dimensions."""
    recipe = load_recipe()
    step = _get_step(recipe, "evaluate")
    prompt = step.get("prompt", "")
    # Check for the six required dimensions
    dimensions = [
        "source quality",
        "factual depth",
        "analytical insight",
        "confidence calibration",
        "structure",
        "citation",
    ]
    for dim in dimensions:
        assert dim.lower() in prompt.lower(), (
            f"evaluate prompt must reference dimension '{dim}'"
        )


def test_evaluate_prompt_produces_gap_list() -> None:
    """evaluate prompt must produce a gap list."""
    recipe = load_recipe()
    step = _get_step(recipe, "evaluate")
    prompt = step.get("prompt", "")
    assert "gap" in prompt.lower(), (
        "evaluate prompt must reference 'gap' for gap list output"
    )


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


def test_run_competitors_provider_preferences_is_list() -> None:
    """provider_preferences must be a YAML sequence (list), not a mapping (dict).

    The recipe engine expects a list of provider/model dicts so it can iterate
    over routing preferences. A bare dict is silently ignored at runtime.
    """
    recipe = load_recipe()
    step = _get_step(recipe, "run-competitors")
    pp = step.get("provider_preferences")
    assert isinstance(pp, list), (
        f"provider_preferences must be a list (YAML sequence), got {type(pp).__name__}: {pp!r}"
    )
