"""Tests that prioritizer is correctly registered in behaviors/specialists.yaml"""
from __future__ import annotations

from pathlib import Path

import yaml

SPECIALISTS_YAML_PATH = Path(__file__).parent.parent / "behaviors" / "specialists.yaml"


def _load_yaml() -> dict:
    assert SPECIALISTS_YAML_PATH.exists(), f"File not found: {SPECIALISTS_YAML_PATH}"
    return yaml.safe_load(SPECIALISTS_YAML_PATH.read_text(encoding="utf-8"))


def test_prioritizer_in_agents_include_list() -> None:
    """31. Prioritizer is in agents include list."""
    data = _load_yaml()
    include_list = data["agents"]["include"]
    assert "specialists:prioritizer" in include_list, (
        "agents.include must contain 'specialists:prioritizer'"
    )


def test_prioritizer_is_last_entry() -> None:
    """32. Prioritizer is last entry (it was added most recently)."""
    data = _load_yaml()
    include_list = data["agents"]["include"]
    assert include_list[-1] == "specialists:planner", (
        f"Last entry in agents.include must be 'specialists:planner', "
        f"got '{include_list[-1]}'"
    )


def test_full_ordered_list_matches_expected() -> None:
    """33. Full ordered list matches expected (all 12 agents in order)."""
    data = _load_yaml()
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
        f"agents.include list does not match expected full ordered list.\n"
        f"Expected: {expected}\n"
        f"Got:      {include_list}"
    )
