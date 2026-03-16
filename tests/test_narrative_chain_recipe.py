"""
TDD tests for task-11: Create narrative-chain.yaml recipe.
Validates the structure, metadata, context variables, and all 5 steps
of recipes/narrative-chain.yaml.
"""

from __future__ import annotations

from pathlib import Path

import yaml

RECIPE_PATH = Path(__file__).parent.parent / "recipes" / "narrative-chain.yaml"


def load_recipe() -> dict:
    assert RECIPE_PATH.exists(), f"Recipe file not found: {RECIPE_PATH}"
    with RECIPE_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------


def test_recipe_file_exists() -> None:
    """recipes/narrative-chain.yaml must exist."""
    assert RECIPE_PATH.exists(), "recipes/narrative-chain.yaml must exist"


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------


def test_recipe_name() -> None:
    """Recipe name must be 'narrative-chain'."""
    recipe = load_recipe()
    assert recipe["name"] == "narrative-chain", (
        f"Expected name='narrative-chain', got {recipe.get('name')!r}"
    )


def test_recipe_version() -> None:
    """Recipe version must be '1.3.0'."""
    recipe = load_recipe()
    assert recipe["version"] == "1.3.0", (
        f"Expected version='1.3.0', got {recipe.get('version')!r}"
    )


def test_recipe_description_contains_pipeline() -> None:
    """Recipe description must reference Researcher → Formatter → Data Analyzer → Storyteller → Save."""
    recipe = load_recipe()
    desc = recipe.get("description", "")
    assert "Researcher" in desc, "Description must mention 'Researcher'"
    assert "Formatter" in desc, "Description must mention 'Formatter'"
    assert "Data Analyzer" in desc, "Description must mention 'Data Analyzer'"
    assert "Storyteller" in desc, "Description must mention 'Storyteller'"
    assert "Save" in desc, "Description must mention 'Save'"


def test_recipe_description_mentions_narrative() -> None:
    """Recipe description must mention 'narrative'."""
    recipe = load_recipe()
    desc = recipe.get("description", "")
    assert "narrative" in desc.lower(), "Description must mention 'narrative'"


def test_recipe_tags() -> None:
    """Recipe tags must include research, analysis, narrative, storytelling, chain."""
    recipe = load_recipe()
    tags = recipe.get("tags", [])
    for required_tag in ["research", "analysis", "narrative", "storytelling", "chain"]:
        assert required_tag in tags, f"Tags must include '{required_tag}'"


# ---------------------------------------------------------------------------
# Context variables
# ---------------------------------------------------------------------------


def test_context_has_research_question() -> None:
    """Context must have 'research_question' variable."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert "research_question" in context, "Context must have 'research_question'"


def test_context_research_question_default_is_empty() -> None:
    """research_question must default to empty string (required field marker)."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert context["research_question"] == "" or context["research_question"] is None, (
        "research_question must have empty default"
    )


def test_context_has_audience() -> None:
    """Context must have 'audience' variable."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert "audience" in context, "Context must have 'audience'"


def test_context_has_tone() -> None:
    """Context must have 'tone' variable (not 'voice')."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert "tone" in context, "Context must have 'tone' variable"
    assert "voice" not in context, "Context must NOT have 'voice' — use 'tone' instead"


def test_context_has_quality_threshold() -> None:
    """Context must have 'quality_threshold' variable with default 'medium'."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert "quality_threshold" in context, "Context must have 'quality_threshold'"
    assert context["quality_threshold"] == "medium", (
        f"quality_threshold must default to 'medium', got {context.get('quality_threshold')!r}"
    )


# ---------------------------------------------------------------------------
# Steps — count and order
# ---------------------------------------------------------------------------


def test_recipe_has_nine_steps() -> None:
    """Recipe must have exactly 9 steps (including validate-research, story-format, normalize-header, normalize-quality-gate)."""
    recipe = load_recipe()
    steps = recipe.get("steps", [])
    assert len(steps) == 9, f"Expected 9 steps, got {len(steps)}"


def test_step_ids_in_order() -> None:
    """Steps must be in order: research, validate-research, format-research, analyze, narrate, story-format, normalize-header, normalize-quality-gate, save."""
    recipe = load_recipe()
    steps = recipe.get("steps", [])
    ids = [s["id"] for s in steps]
    expected = [
        "research",
        "validate-research",
        "format-research",
        "analyze",
        "narrate",
        "story-format",
        "normalize-header",
        "normalize-quality-gate",
        "save",
    ]
    assert ids == expected, f"Step IDs must be {expected}, got {ids}"


# ---------------------------------------------------------------------------
# Step 1 — research (must match research-chain.yaml exactly)
# ---------------------------------------------------------------------------


def test_step1_agent() -> None:
    """Step 1 must use agent 'specialists:researcher'."""
    recipe = load_recipe()
    step = recipe["steps"][0]
    assert step["agent"] == "specialists:researcher"


def test_step1_output() -> None:
    """Step 1 output must be 'research_output'."""
    recipe = load_recipe()
    step = recipe["steps"][0]
    assert step["output"] == "research_output"


def test_step1_timeout() -> None:
    """Step 1 timeout must be 4500 (increased to accommodate scope-constrained research runs)."""
    recipe = load_recipe()
    step = recipe["steps"][0]
    assert step["timeout"] == 4500


def test_step1_prompt_contains_research_question() -> None:
    """Step 1 prompt must reference {{research_question}}."""
    recipe = load_recipe()
    step = recipe["steps"][0]
    assert "{{research_question}}" in step["prompt"]


def test_step1_prompt_contains_quality_threshold() -> None:
    """Step 1 prompt must reference {{quality_threshold}}."""
    recipe = load_recipe()
    step = recipe["steps"][0]
    assert "{{quality_threshold}}" in step["prompt"]


# ---------------------------------------------------------------------------
# Step 2 — format-research (must match research-chain.yaml exactly)
# ---------------------------------------------------------------------------


def test_step2_agent() -> None:
    """Step 2 (format-research, index 2) must use agent 'specialists:researcher-formatter'."""
    recipe = load_recipe()
    step = recipe["steps"][2]
    assert step["agent"] == "specialists:researcher-formatter"


def test_step2_output() -> None:
    """Step 2 (format-research) output must be 'formatted_research'."""
    recipe = load_recipe()
    step = recipe["steps"][2]
    assert step["output"] == "formatted_research"


def test_step2_timeout() -> None:
    """Step 2 (format-research) timeout must be 1200 (raised from 600 — formatter processes largest payload)."""
    recipe = load_recipe()
    step = recipe["steps"][2]
    assert step["timeout"] == 1200


def test_step2_prompt_contains_research_output() -> None:
    """Step 2 (format-research) prompt must reference {{research_output}}."""
    recipe = load_recipe()
    step = recipe["steps"][2]
    assert "{{research_output}}" in step["prompt"]


# ---------------------------------------------------------------------------
# Step 3 — analyze (must match research-chain.yaml exactly)
# ---------------------------------------------------------------------------


def test_step3_agent() -> None:
    """Step 3 (analyze, index 3) must use agent 'specialists:data-analyzer'."""
    recipe = load_recipe()
    step = recipe["steps"][3]
    assert step["agent"] == "specialists:data-analyzer"


def test_step3_output() -> None:
    """Step 3 (analyze) output must be 'analysis_output'."""
    recipe = load_recipe()
    step = recipe["steps"][3]
    assert step["output"] == "analysis_output"


def test_step3_timeout() -> None:
    """Step 3 (analyze) timeout must be 900."""
    recipe = load_recipe()
    step = recipe["steps"][3]
    assert step["timeout"] == 900


def test_step3_prompt_contains_formatted_research() -> None:
    """Step 3 (analyze) prompt must reference {{formatted_research}}."""
    recipe = load_recipe()
    step = recipe["steps"][3]
    assert "{{formatted_research}}" in step["prompt"]


# ---------------------------------------------------------------------------
# Step 4 — narrate (storyteller, not writer)
# ---------------------------------------------------------------------------


def test_step4_agent_is_storyteller() -> None:
    """Step 4 (narrate, index 4) must use specialists:storyteller (NOT writer)."""
    recipe = load_recipe()
    step = recipe["steps"][4]
    assert step["agent"] == "specialists:storyteller", (
        f"Step 4 must use 'specialists:storyteller', got {step.get('agent')!r}"
    )


def test_step4_agent_is_not_writer() -> None:
    """Step 4 must NOT use the writer agent."""
    recipe = load_recipe()
    step = recipe["steps"][4]
    assert "writer" not in step.get("agent", ""), "Step 4 must NOT use the writer agent"


def test_step4_output() -> None:
    """Step 4 (narrate) output must be 'final_narrative'."""
    recipe = load_recipe()
    step = recipe["steps"][4]
    assert step["output"] == "final_narrative", (
        f"Step 4 output must be 'final_narrative', got {step.get('output')!r}"
    )


def test_step4_timeout() -> None:
    """Step 4 (narrate) timeout must be 900."""
    recipe = load_recipe()
    step = recipe["steps"][4]
    assert step["timeout"] == 900


def test_step4_prompt_contains_analysis_output() -> None:
    """Step 4 (narrate) prompt must reference {{analysis_output}}."""
    recipe = load_recipe()
    step = recipe["steps"][4]
    assert "{{analysis_output}}" in step["prompt"]


def test_step4_prompt_contains_audience() -> None:
    """Step 4 prompt must reference {{audience}} context variable."""
    recipe = load_recipe()
    step = recipe["steps"][4]
    assert "{{audience}}" in step["prompt"], "Step 4 prompt must reference {{audience}}"


def test_step4_prompt_contains_tone() -> None:
    """Step 4 prompt must reference {{tone}} context variable."""
    recipe = load_recipe()
    step = recipe["steps"][4]
    assert "{{tone}}" in step["prompt"], "Step 4 prompt must reference {{tone}}"


def test_step4_prompt_mentions_five_stage_pipeline() -> None:
    """Step 4 prompt must reference the 5-stage storytelling pipeline."""
    recipe = load_recipe()
    step = recipe["steps"][4]
    prompt = step["prompt"]
    assert (
        "5-stage" in prompt or "five" in prompt.lower() or "5 stage" in prompt.lower()
    ), "Step 4 prompt must mention the 5-stage pipeline"


def test_step4_prompt_mentions_story_output_block() -> None:
    """Step 4 prompt must mention STORY OUTPUT block."""
    recipe = load_recipe()
    step = recipe["steps"][4]
    assert "STORY OUTPUT" in step["prompt"], (
        "Step 4 prompt must mention 'STORY OUTPUT' block"
    )


def test_step4_prompt_has_vocabulary_constraint() -> None:
    """Step 4 (narrate) prompt must include explicit MET/NOT MET vocabulary constraint."""
    recipe = load_recipe()
    step = recipe["steps"][4]
    prompt = step["prompt"]
    assert "MET" in prompt and "NOT MET" in prompt, (
        "Narrate prompt must reference MET and NOT MET vocabulary"
    )
    # Must prohibit synonym vocabulary
    assert "PASS" in prompt or "FAIL" in prompt, (
        "Narrate prompt must reference PASS/FAIL synonyms to prohibit them"
    )


# ---------------------------------------------------------------------------
# Step 5 — normalize-header (bash post-processing)
# ---------------------------------------------------------------------------


def test_step5_is_bash_type() -> None:
    """Step 5 (normalize-header, index 6) must be a bash step."""
    recipe = load_recipe()
    step = recipe["steps"][6]
    assert step.get("type") == "bash", (
        f"Step 5 must be type='bash', got {step.get('type')!r}"
    )


def test_step5_id_is_normalize_header() -> None:
    """Step 5 id must be 'normalize-header'."""
    recipe = load_recipe()
    step = recipe["steps"][6]
    assert step["id"] == "normalize-header"


def test_step5_output_is_final_narrative_normalized() -> None:
    """Step 5 output must be 'final_narrative_normalized'."""
    recipe = load_recipe()
    step = recipe["steps"][6]
    assert step["output"] == "final_narrative_normalized", (
        f"Expected output='final_narrative_normalized', got {step.get('output')!r}"
    )


def test_step5_command_references_final_narrative() -> None:
    """Step 5 command must reference {{formatted_narrative}} for normalization."""
    recipe = load_recipe()
    step = recipe["steps"][6]
    assert "{{formatted_narrative}}" in step["command"], (
        "normalize-header command must reference {{formatted_narrative}}"
    )


def test_step5_command_strips_heading_prefix() -> None:
    """Step 5 command must strip markdown heading prefix from first line."""
    recipe = load_recipe()
    step = recipe["steps"][6]
    cmd = step["command"]
    assert "sed" in cmd, "normalize-header must use sed"
    assert "STORY OUTPUT" in cmd, "sed pattern must reference STORY OUTPUT"
    # Must target only line 1 (1s/ pattern)
    assert "1s/" in cmd, "sed must target only the first line (1s/...)"


def test_step5_timeout() -> None:
    """Step 5 timeout must be 30 (trivial bash operation)."""
    recipe = load_recipe()
    step = recipe["steps"][6]
    assert step["timeout"] == 30


# ---------------------------------------------------------------------------
# Step 6 — normalize-quality-gate (bash post-processing)
# ---------------------------------------------------------------------------


def test_step6_normalize_quality_gate_exists() -> None:
    """Step 6 (normalize-quality-gate, index 7) must exist with id 'normalize-quality-gate'."""
    recipe = load_recipe()
    step = recipe["steps"][7]
    assert step["id"] == "normalize-quality-gate", (
        f"Step 6 id must be 'normalize-quality-gate', got {step.get('id')!r}"
    )


def test_step6_normalize_quality_gate_is_bash_type() -> None:
    """Step 6 must be a bash step."""
    recipe = load_recipe()
    step = recipe["steps"][7]
    assert step.get("type") == "bash", (
        f"Step 6 must be type='bash', got {step.get('type')!r}"
    )


def test_step6_normalize_quality_gate_output() -> None:
    """Step 6 output must be 'final_narrative_validated'."""
    recipe = load_recipe()
    step = recipe["steps"][7]
    assert step["output"] == "final_narrative_validated", (
        f"Step 6 output must be 'final_narrative_validated', got {step.get('output')!r}"
    )


def test_step6_normalize_quality_gate_references_input_variable() -> None:
    """Step 6 command must reference {{final_narrative_normalized}} as input."""
    recipe = load_recipe()
    step = recipe["steps"][7]
    assert "{{final_narrative_normalized}}" in step["command"], (
        "normalize-quality-gate command must reference {{final_narrative_normalized}}"
    )


def test_step6_normalize_quality_gate_has_pass_to_met_normalization() -> None:
    """Step 6 command must normalize PASS/PASSED to MET."""
    recipe = load_recipe()
    step = recipe["steps"][7]
    cmd = step["command"]
    assert "PASS" in cmd and "MET" in cmd, (
        "normalize-quality-gate must contain PASS->MET normalization"
    )


def test_step6_normalize_quality_gate_has_fail_to_not_met_normalization() -> None:
    """Step 6 command must normalize FAIL/FAILED to NOT MET."""
    recipe = load_recipe()
    step = recipe["steps"][7]
    cmd = step["command"]
    assert "FAIL" in cmd and "NOT MET" in cmd, (
        "normalize-quality-gate must contain FAIL->NOT MET normalization"
    )


def test_step6_normalize_quality_gate_appends_missing_line() -> None:
    """Step 6 command must append NOT MET and note when QUALITY THRESHOLD RESULT line is absent."""
    recipe = load_recipe()
    step = recipe["steps"][7]
    cmd = step["command"]
    assert "quality gate line was missing" in cmd, (
        "normalize-quality-gate must handle missing QUALITY THRESHOLD RESULT line"
    )


def test_step6_normalize_quality_gate_timeout() -> None:
    """Step 6 timeout must be 30 (trivial bash operation)."""
    recipe = load_recipe()
    step = recipe["steps"][7]
    assert step["timeout"] == 30


# ---------------------------------------------------------------------------
# Step 7 — save
# ---------------------------------------------------------------------------


def test_step6_agent_is_file_ops() -> None:
    """Step 7 (save, index 8) must use agent 'foundation:file-ops'."""
    recipe = load_recipe()
    step = recipe["steps"][8]
    assert step["agent"] == "foundation:file-ops"


def test_step6_output() -> None:
    """Step 7 (save) output must be 'output_path'."""
    recipe = load_recipe()
    step = recipe["steps"][8]
    assert step["output"] == "output_path"


def test_step6_timeout() -> None:
    """Step 7 (save) timeout must be 300."""
    recipe = load_recipe()
    step = recipe["steps"][8]
    assert step["timeout"] == 300


def test_step6_saves_to_docs_research_output() -> None:
    """Step 7 must save to docs/research-output/ directory."""
    recipe = load_recipe()
    step = recipe["steps"][8]
    assert "docs/research-output/" in step["prompt"], (
        "Step 7 must save to docs/research-output/"
    )


def test_step6_prompt_contains_final_narrative_validated() -> None:
    """Step 7 prompt must reference {{final_narrative_validated}} (output of normalize-quality-gate)."""
    recipe = load_recipe()
    step = recipe["steps"][8]
    assert "{{final_narrative_validated}}" in step["prompt"], (
        "Save step must use the validated variable {{final_narrative_validated}}"
    )


def test_step6_prompt_contains_research_question() -> None:
    """Step 7 prompt must reference {{research_question}} to derive filename."""
    recipe = load_recipe()
    step = recipe["steps"][8]
    assert "{{research_question}}" in step["prompt"]
