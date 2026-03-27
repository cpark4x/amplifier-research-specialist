"""Structural tests for agents/planner.md."""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PLANNER = REPO_ROOT / "agents" / "planner.md"
BEHAVIORS_YAML = REPO_ROOT / "behaviors" / "specialists.yaml"


def _load():
    assert PLANNER.exists(), f"Missing {PLANNER}"
    return PLANNER.read_text()


content = _load()


# --- Frontmatter ---

def test_frontmatter_has_meta_key():
    """Frontmatter must contain a meta: key."""
    assert "meta:" in content

def test_frontmatter_has_name():
    """meta.name must be 'planner'."""
    fm = re.search(r"---\n(.*?)\n---", content, re.DOTALL)
    assert fm, "No YAML frontmatter found"
    assert "name: planner" in fm.group(1)

def test_frontmatter_has_example():
    """Description must include at least one <example> block."""
    fm = re.search(r"---\n(.*?)\n---", content, re.DOTALL)
    assert fm, "No YAML frontmatter found"
    assert "<example>" in fm.group(1)

def test_frontmatter_has_model_role():
    """Planner should declare model_role: reasoning."""
    fm = re.search(r"---\n(.*?)\n---", content, re.DOTALL)
    assert fm, "No YAML frontmatter found"
    assert "model_role: reasoning" in fm.group(1)


# --- Document structure ---

def test_has_heading():
    """Must have a # Planner heading."""
    assert "# Planner" in content

def test_has_output_contract():
    """Must have an Output Contract section."""
    assert "## Output Contract" in content

def test_output_contract_has_plan_output():
    """Output contract must specify PLAN OUTPUT block."""
    assert "PLAN OUTPUT" in content

def test_output_contract_sections():
    """PLAN OUTPUT block must contain MILESTONES, DEPENDENCIES, RISKS, OPEN QUESTIONS."""
    for section in ["MILESTONES", "DEPENDENCIES", "RISKS", "OPEN QUESTIONS"]:
        assert section in content, f"Missing {section} in output contract"

def test_output_contract_has_assumptions():
    """PLAN OUTPUT block must contain ASSUMPTIONS section."""
    assert "ASSUMPTIONS" in content


# --- Principles ---

def test_has_principles_section():
    """Must have a Principles section."""
    assert "## Principles" in content

def test_principles_count():
    """Must have at least 4 numbered principles."""
    principles_section = re.search(r"## Principles\n(.*?)(?=## |$)", content, re.DOTALL)
    assert principles_section, "No Principles section found"
    numbered = re.findall(r"^\d+\.", principles_section.group(1), re.MULTILINE)
    assert len(numbered) >= 4, f"Expected >= 4 principles, found {len(numbered)}"


# --- What You Don't Do ---

def test_has_what_you_dont_do():
    """Must have a What You Don't Do section."""
    assert "## What You Don" in content

def test_dont_do_items():
    """What You Don't Do must have at least 4 items."""
    section = re.search(r"## What You Don.*?\n(.*?)(?=## |$)", content, re.DOTALL)
    assert section, "No What You Don't Do section found"
    items = re.findall(r"^- ", section.group(1), re.MULTILINE)
    assert len(items) >= 4, f"Expected >= 4 items, found {len(items)}"


# --- Identity ---

def test_identity_framing():
    """Must identify as a planning specialist."""
    assert "planning specialist" in content.lower()

def test_scope_boundaries():
    """Must state it doesn't research."""
    assert re.search(r"don.t research", content, re.IGNORECASE)


# --- Registration ---

def test_registered_in_behaviors():
    """specialists:planner must be registered in behaviors/specialists.yaml."""
    behaviors = BEHAVIORS_YAML.read_text()
    assert "specialists:planner" in behaviors
