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
    """Recipe version must be '1.0.0'."""
    recipe = load_recipe()
    assert recipe["version"] == "1.0.0", (
        f"Expected version='1.0.0', got {recipe.get('version')!r}"
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


def test_recipe_has_five_steps() -> None:
    """Recipe must have exactly 5 steps."""
    recipe = load_recipe()
    steps = recipe.get("steps", [])
    assert len(steps) == 5, f"Expected 5 steps, got {len(steps)}"


def test_step_ids_in_order() -> None:
    """Steps must be in order: research, format-research, analyze, narrate, save."""
    recipe = load_recipe()
    steps = recipe.get("steps", [])
    ids = [s["id"] for s in steps]
    assert ids == ["research", "format-research", "analyze", "narrate", "save"], (
        f"Step IDs must be ['research', 'format-research', 'analyze', 'narrate', 'save'], got {ids}"
    )


# ---------------------------------------------------------------------------
# Step 1 — research (must match research-chain.yaml exactly)
# ---------------------------------------------------------------------------


def test_step1_agent() -> None:
    """Step 1 must use agent 'specialists:specialists/researcher'."""
    recipe = load_recipe()
    step = recipe["steps"][0]
    assert step["agent"] == "specialists:specialists/researcher"


def test_step1_output() -> None:
    """Step 1 output must be 'research_output'."""
    recipe = load_recipe()
    step = recipe["steps"][0]
    assert step["output"] == "research_output"


def test_step1_timeout() -> None:
    """Step 1 timeout must be 2700."""
    recipe = load_recipe()
    step = recipe["steps"][0]
    assert step["timeout"] == 2700


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
    """Step 2 must use agent 'specialists:specialists/researcher-formatter'."""
    recipe = load_recipe()
    step = recipe["steps"][1]
    assert step["agent"] == "specialists:specialists/researcher-formatter"


def test_step2_output() -> None:
    """Step 2 output must be 'formatted_research'."""
    recipe = load_recipe()
    step = recipe["steps"][1]
    assert step["output"] == "formatted_research"


def test_step2_timeout() -> None:
    """Step 2 timeout must be 600."""
    recipe = load_recipe()
    step = recipe["steps"][1]
    assert step["timeout"] == 600


def test_step2_prompt_contains_research_output() -> None:
    """Step 2 prompt must reference {{research_output}}."""
    recipe = load_recipe()
    step = recipe["steps"][1]
    assert "{{research_output}}" in step["prompt"]


# ---------------------------------------------------------------------------
# Step 3 — analyze (must match research-chain.yaml exactly)
# ---------------------------------------------------------------------------


def test_step3_agent() -> None:
    """Step 3 must use agent 'specialists:specialists/data-analyzer'."""
    recipe = load_recipe()
    step = recipe["steps"][2]
    assert step["agent"] == "specialists:specialists/data-analyzer"


def test_step3_output() -> None:
    """Step 3 output must be 'analysis_output'."""
    recipe = load_recipe()
    step = recipe["steps"][2]
    assert step["output"] == "analysis_output"


def test_step3_timeout() -> None:
    """Step 3 timeout must be 900."""
    recipe = load_recipe()
    step = recipe["steps"][2]
    assert step["timeout"] == 900


def test_step3_prompt_contains_formatted_research() -> None:
    """Step 3 prompt must reference {{formatted_research}}."""
    recipe = load_recipe()
    step = recipe["steps"][2]
    assert "{{formatted_research}}" in step["prompt"]


# ---------------------------------------------------------------------------
# Step 4 — narrate (storyteller, not writer)
# ---------------------------------------------------------------------------


def test_step4_agent_is_storyteller() -> None:
    """Step 4 must use specialists:specialists/storyteller (NOT writer)."""
    recipe = load_recipe()
    step = recipe["steps"][3]
    assert step["agent"] == "specialists:specialists/storyteller", (
        f"Step 4 must use 'specialists:specialists/storyteller', got {step.get('agent')!r}"
    )


def test_step4_agent_is_not_writer() -> None:
    """Step 4 must NOT use the writer agent."""
    recipe = load_recipe()
    step = recipe["steps"][3]
    assert "writer" not in step.get("agent", ""), "Step 4 must NOT use the writer agent"


def test_step4_output() -> None:
    """Step 4 output must be 'final_narrative'."""
    recipe = load_recipe()
    step = recipe["steps"][3]
    assert step["output"] == "final_narrative", (
        f"Step 4 output must be 'final_narrative', got {step.get('output')!r}"
    )


def test_step4_timeout() -> None:
    """Step 4 timeout must be 900."""
    recipe = load_recipe()
    step = recipe["steps"][3]
    assert step["timeout"] == 900


def test_step4_prompt_contains_analysis_output() -> None:
    """Step 4 prompt must reference {{analysis_output}}."""
    recipe = load_recipe()
    step = recipe["steps"][3]
    assert "{{analysis_output}}" in step["prompt"]


def test_step4_prompt_contains_audience() -> None:
    """Step 4 prompt must reference {{audience}} context variable."""
    recipe = load_recipe()
    step = recipe["steps"][3]
    assert "{{audience}}" in step["prompt"], "Step 4 prompt must reference {{audience}}"


def test_step4_prompt_contains_tone() -> None:
    """Step 4 prompt must reference {{tone}} context variable."""
    recipe = load_recipe()
    step = recipe["steps"][3]
    assert "{{tone}}" in step["prompt"], "Step 4 prompt must reference {{tone}}"


def test_step4_prompt_mentions_five_stage_pipeline() -> None:
    """Step 4 prompt must reference the 5-stage storytelling pipeline."""
    recipe = load_recipe()
    step = recipe["steps"][3]
    prompt = step["prompt"]
    assert (
        "5-stage" in prompt or "five" in prompt.lower() or "5 stage" in prompt.lower()
    ), "Step 4 prompt must mention the 5-stage pipeline"


def test_step4_prompt_mentions_story_output_block() -> None:
    """Step 4 prompt must mention STORY OUTPUT block."""
    recipe = load_recipe()
    step = recipe["steps"][3]
    assert "STORY OUTPUT" in step["prompt"], (
        "Step 4 prompt must mention 'STORY OUTPUT' block"
    )


# ---------------------------------------------------------------------------
# Step 5 — save
# ---------------------------------------------------------------------------


def test_step5_agent_is_file_ops() -> None:
    """Step 5 must use agent 'foundation:file-ops'."""
    recipe = load_recipe()
    step = recipe["steps"][4]
    assert step["agent"] == "foundation:file-ops"


def test_step5_output() -> None:
    """Step 5 output must be 'output_path'."""
    recipe = load_recipe()
    step = recipe["steps"][4]
    assert step["output"] == "output_path"


def test_step5_timeout() -> None:
    """Step 5 timeout must be 120."""
    recipe = load_recipe()
    step = recipe["steps"][4]
    assert step["timeout"] == 120


def test_step5_saves_to_docs_research_output() -> None:
    """Step 5 must save to docs/research-output/ directory."""
    recipe = load_recipe()
    step = recipe["steps"][4]
    assert "docs/research-output/" in step["prompt"], (
        "Step 5 must save to docs/research-output/"
    )


def test_step5_prompt_contains_final_narrative() -> None:
    """Step 5 prompt must reference {{final_narrative}}."""
    recipe = load_recipe()
    step = recipe["steps"][4]
    assert "{{final_narrative}}" in step["prompt"]


def test_step5_prompt_contains_research_question() -> None:
    """Step 5 prompt must reference {{research_question}} to derive filename."""
    recipe = load_recipe()
    step = recipe["steps"][4]
    assert "{{research_question}}" in step["prompt"]
