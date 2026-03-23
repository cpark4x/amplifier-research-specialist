"""
Structural tests for researcher breadth mode (#46).
Validates that the researcher agent file contains mode selection
in Stage 1 and breadth-aware corroboration logic in Stage 5.

Fixes #46: researcher breadth mode for survey questions.
"""

from functools import lru_cache
from pathlib import Path

SPEC_FILE = Path(__file__).parent.parent / "agents" / "researcher.md"


@lru_cache(maxsize=None)
def _content() -> str:
    assert SPEC_FILE.exists(), f"File not found: {SPEC_FILE}"
    return SPEC_FILE.read_text(encoding="utf-8")


def test_breadth_mode_selection_exists() -> None:
    """Stage 1 must contain breadth mode selection language."""
    c = _content()
    has_mode_selection = (
        "research_mode" in c.lower()
        or "breadth mode" in c.lower()
        or "research mode" in c.lower()
    )
    assert has_mode_selection, (
        "Stage 1 must contain mode selection language — "
        "expected 'research_mode', 'breadth mode', or 'research mode'"
    )


def test_breadth_mode_after_question_type_classifier() -> None:
    """Mode selection must come after the question-type classifier in Stage 1."""
    c = _content()
    assert c.index("Step A") < c.index("research_mode"), (
        "Mode selection must come after the question-type classifier (Step A)"
    )


def test_breadth_mode_survey_trigger() -> None:
    """Mode selection must mention Survey/Ranking as the trigger for breadth mode."""
    c = _content()
    # Find the mode selection section and check for Survey/Ranking
    has_survey_trigger = (
        "survey" in c.lower() and "breadth" in c.lower()
    )
    assert has_survey_trigger, (
        "Mode selection must mention Survey/Ranking as the trigger for breadth mode"
    )


def test_breadth_mode_depth_override() -> None:
    """Mode selection must mention that caller can override with research_mode: depth."""
    c = _content()
    has_override = (
        "research_mode: depth" in c
        or "research_mode:depth" in c
        or "override" in c.lower() and "depth" in c.lower()
    )
    assert has_override, (
        "Mode selection must mention caller can override with research_mode: depth"
    )


def test_breadth_mode_corroboration_exists() -> None:
    """Stage 5 must contain breadth mode corroboration logic."""
    c = _content()
    stage5_section = c[c.index("Stage 5"):c.index("Stage 6")]
    has_breadth_logic = (
        "breadth" in stage5_section.lower()
        or "research_mode" in stage5_section.lower()
    )
    assert has_breadth_logic, (
        "Stage 5 (Corroborator) must contain breadth mode corroboration logic"
    )


def test_breadth_mode_numeric_corroboration() -> None:
    """Stage 5 must mention numeric/financial claims still get full corroboration."""
    c = _content()
    stage5_section = c[c.index("Stage 5"):c.index("Stage 6")]
    has_numeric = (
        "numeric" in stage5_section.lower()
        or "financial" in stage5_section.lower()
        or "dollar" in stage5_section.lower()
    )
    assert has_numeric, (
        "Stage 5 must mention numeric/financial claims still get full corroboration in breadth mode"
    )


def test_breadth_mode_qualitative_skip() -> None:
    """Stage 5 must mention qualitative claims skip corroboration in breadth mode."""
    c = _content()
    stage5_section = c[c.index("Stage 5"):c.index("Stage 6")]
    has_qualitative = (
        "qualitative" in stage5_section.lower()
        or "skip corroboration" in stage5_section.lower()
        or "single credible source" in stage5_section.lower()
    )
    assert has_qualitative, (
        "Stage 5 must mention qualitative claims skip corroboration in breadth mode"
    )


def test_breadth_mode_flag() -> None:
    """Stage 5 must mention breadth-mode as a flag for single-source claims."""
    c = _content()
    assert "breadth-mode" in c, (
        "Stage 5 must mention 'breadth-mode' as a flag for single-source claims"
    )
