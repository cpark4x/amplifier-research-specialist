"""
TDD tests for task-04: Register storyteller in behaviors/specialists.yaml.
Validates that specialists:storyteller is present in agents.include.
"""

from __future__ import annotations

from pathlib import Path

import yaml

SPECIALISTS_YAML_PATH = Path(__file__).parent.parent / "behaviors" / "specialists.yaml"


def load_yaml() -> dict:
    assert SPECIALISTS_YAML_PATH.exists(), f"File not found: {SPECIALISTS_YAML_PATH}"
    return yaml.safe_load(SPECIALISTS_YAML_PATH.read_text(encoding="utf-8"))


def test_specialists_yaml_exists() -> None:
    assert SPECIALISTS_YAML_PATH.exists(), "behaviors/specialists.yaml must exist"


def test_agents_include_contains_storyteller() -> None:
    data = load_yaml()
    include_list = data["agents"]["include"]
    assert "specialists:storyteller" in include_list, (
        "agents.include must contain 'specialists:storyteller'"
    )


def test_storyteller_is_last_entry_in_agents_include() -> None:
    data = load_yaml()
    include_list = data["agents"]["include"]
    assert include_list[-1] == "specialists:planner", (
        f"Last entry in agents.include must be 'specialists:planner', "
        f"got '{include_list[-1]}'"
    )


def test_agents_include_full_ordered_list() -> None:
    """Verify the complete ordered list of agents.include matches the spec."""
    data = load_yaml()
    include_list = data["agents"]["include"]
    expected = [
        "specialists:researcher",
        "specialists:writer",
        "specialists:competitive-analysis",
        "specialists:data-analyzer",
        "specialists:data-analyzer-formatter",
        "specialists:researcher-formatter",
        "specialists:storyteller",
        "specialists:story-formatter",
        "specialists:writer-formatter",
        "specialists:prioritizer",
        "specialists:prioritizer-formatter",
        "specialists:planner",
    ]
    assert include_list == expected, (
        f"agents.include list does not match spec.\n"
        f"Expected: {expected}\n"
        f"Got:      {include_list}"
    )


def test_raw_line_present_in_file() -> None:
    """Acceptance criterion: raw line '    - specialists:storyteller' is in the file."""
    content = SPECIALISTS_YAML_PATH.read_text(encoding="utf-8")
    assert "    - specialists:storyteller" in content, (
        "The exact line '    - specialists:storyteller' must appear in the file"
    )
