"""Structural tests for agents/prioritizer-formatter.md."""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PRIORITIZER_FORMATTER = REPO_ROOT / "agents" / "prioritizer-formatter.md"
BEHAVIORS_YAML = REPO_ROOT / "behaviors" / "specialists.yaml"


def _load():
    assert PRIORITIZER_FORMATTER.exists(), f"Missing {PRIORITIZER_FORMATTER}"
    return PRIORITIZER_FORMATTER.read_text()


content = _load()


# --- Frontmatter ---

def test_frontmatter_has_meta_key():
    """Frontmatter must contain a meta: key."""
    assert "meta:" in content

def test_frontmatter_has_name():
    """meta.name must be 'prioritizer-formatter'."""
    fm = re.search(r"---\n(.*?)\n---", content, re.DOTALL)
    assert fm, "No YAML frontmatter found"
    assert "name: prioritizer-formatter" in fm.group(1)


# --- Document structure ---

def test_has_heading():
    """Must have a # Prioritizer Formatter heading."""
    assert "# Prioritizer Formatter" in content

def test_has_core_principle():
    """Must have a Core Principle section."""
    assert "## Core Principle" in content

def test_core_principle_extract_not_generate():
    """Core principle must state extract, don't generate."""
    assert "Extract, don't generate" in content


# --- Pipeline stages ---

def test_has_stage_0():
    """Must have Stage 0: Open your response."""
    assert "### Stage 0" in content

def test_stage_0_priority_output_header():
    """Stage 0 must specify PRIORITY OUTPUT as literal first output."""
    assert "PRIORITY OUTPUT" in content

def test_has_stage_1():
    """Must have Stage 1: Parse inputs."""
    assert "### Stage 1" in content

def test_has_stage_2():
    """Must have Stage 2: Extract rankings."""
    assert "### Stage 2" in content

def test_has_stage_3():
    """Must have Stage 3: Produce the canonical PRIORITY OUTPUT block."""
    assert "### Stage 3" in content

def test_stages_in_order():
    """Stages must appear in order: 0, 1, 2, 3."""
    positions = []
    for stage in ["### Stage 0", "### Stage 1", "### Stage 2", "### Stage 3"]:
        pos = content.find(stage)
        assert pos >= 0, f"{stage} not found"
        positions.append(pos)
    assert positions == sorted(positions), "Stages are not in order"


# --- Input format detection ---

def test_detects_block_format():
    """Must describe block format detection."""
    assert "block" in content.lower()

def test_detects_prose_format():
    """Must describe prose format detection."""
    assert "prose" in content.lower()


# --- Output block structure ---

def test_output_has_rankings():
    """Output block must contain RANKINGS section."""
    assert "RANKINGS" in content

def test_output_has_unrankable_items():
    """Output block must contain UNRANKABLE ITEMS section."""
    assert "UNRANKABLE ITEMS" in content

def test_output_has_quality_threshold():
    """Output block must contain QUALITY THRESHOLD RESULT."""
    assert "QUALITY THRESHOLD RESULT" in content

def test_output_has_framework():
    """Output block must include Framework field."""
    assert re.search(r"Framework:", content)

def test_output_has_parsed_line():
    """Output must include a Parsed: summary line."""
    assert "Parsed:" in content


# --- Priority labels ---

def test_priority_labels():
    """Must support priority labels: must, should, could, wont."""
    for label in ["must", "should", "could", "wont"]:
        assert label in content, f"Missing priority label: {label}"


# --- What You Do Not Do ---

def test_has_what_you_do_not_do():
    """Must have a What You Do Not Do section."""
    assert "## What You Do Not Do" in content

def test_does_not_rerank():
    """Must state it does not re-rank items."""
    lower = content.lower()
    assert "re-rank" in lower or "rerank" in lower

def test_does_not_generate_rationale():
    """Must state it does not generate new rationale."""
    assert re.search(r"[Gg]enerate new rationale", content)


# --- Registration ---

def test_registered_in_behaviors():
    """specialists:prioritizer-formatter must be registered in behaviors/specialists.yaml."""
    behaviors = BEHAVIORS_YAML.read_text()
    assert "specialists:prioritizer-formatter" in behaviors
