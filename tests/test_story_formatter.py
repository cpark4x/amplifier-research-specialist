"""Structural tests for agents/story-formatter.md."""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
STORY_FORMATTER = REPO_ROOT / "agents" / "story-formatter.md"
BEHAVIORS_YAML = REPO_ROOT / "behaviors" / "specialists.yaml"


def _load():
    assert STORY_FORMATTER.exists(), f"Missing {STORY_FORMATTER}"
    return STORY_FORMATTER.read_text()


content = _load()


# --- Frontmatter ---

def test_frontmatter_has_meta_key():
    """Frontmatter must contain a meta: key."""
    assert "meta:" in content

def test_frontmatter_has_name():
    """meta.name must be 'story-formatter'."""
    fm = re.search(r"---\n(.*?)\n---", content, re.DOTALL)
    assert fm, "No YAML frontmatter found"
    assert "name: story-formatter" in fm.group(1)


# --- Document structure ---

def test_has_heading():
    """Must have a # Story Formatter heading."""
    assert "# Story Formatter" in content

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

def test_stage_0_story_output_header():
    """Stage 0 must specify STORY OUTPUT as literal first output."""
    assert "STORY OUTPUT" in content

def test_has_stage_1():
    """Must have Stage 1: Parse inputs."""
    assert "### Stage 1" in content

def test_has_stage_2():
    """Must have Stage 2: Classify findings."""
    assert "### Stage 2" in content

def test_has_stage_3():
    """Must have Stage 3: Produce the complete STORY OUTPUT block."""
    assert "### Stage 3" in content

def test_stages_in_order():
    """Stages must appear in order: 0, 1, 2, 3."""
    positions = []
    for stage in ["### Stage 0", "### Stage 1", "### Stage 2", "### Stage 3"]:
        pos = content.find(stage)
        assert pos >= 0, f"{stage} not found"
        positions.append(pos)
    assert positions == sorted(positions), "Stages are not in order"


# --- Output block structure ---

def test_output_has_narrative_selection():
    """Output block must contain NARRATIVE SELECTION section."""
    assert "NARRATIVE SELECTION" in content

def test_output_has_included_findings():
    """Output block must contain INCLUDED FINDINGS section."""
    assert "INCLUDED FINDINGS" in content

def test_output_has_omitted_findings():
    """Output block must contain OMITTED FINDINGS section."""
    assert "OMITTED FINDINGS" in content

def test_output_has_quality_threshold():
    """Output block must contain QUALITY THRESHOLD RESULT."""
    assert "QUALITY THRESHOLD RESULT" in content


# --- Finding classification ---

def test_included_finding_roles():
    """Included findings must support narrative roles: hook, complication, evidence, peak, resolution."""
    for role in ["hook", "complication", "evidence", "peak", "resolution"]:
        assert role in content, f"Missing narrative role: {role}"

def test_omitted_finding_rationales():
    """Omitted findings must support rationales: off-arc, redundant, undermines-tone."""
    for rationale in ["off-arc", "redundant", "undermines-tone"]:
        assert rationale in content, f"Missing omission rationale: {rationale}"


# --- What You Do Not Do ---

def test_has_what_you_do_not_do():
    """Must have a What You Do Not Do section."""
    assert "## What You Do Not Do" in content

def test_does_not_generate_new_prose():
    """Must state it does not generate new story prose."""
    assert re.search(r"[Gg]enerate new story prose", content)

def test_does_not_reselect_findings():
    """Must state it does not re-select findings."""
    lower = content.lower()
    assert "re-select" in lower or "reselect" in lower


# --- Registration ---

def test_registered_in_behaviors():
    """specialists:story-formatter must be registered in behaviors/specialists.yaml."""
    behaviors = BEHAVIORS_YAML.read_text()
    assert "specialists:story-formatter" in behaviors
