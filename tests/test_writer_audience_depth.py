"""
Structural tests for writer audience-aware technical depth (#50).
Validates that the writer agent file contains an audience depth self-check
in Stage 4 that translates mechanism-level language to outcome-level
for non-technical audiences.

Fixes #50: writer audience-aware technical depth calibration.
"""

from functools import lru_cache
from pathlib import Path

SPEC_FILE = Path(__file__).parent.parent / "agents" / "writer.md"


@lru_cache(maxsize=None)
def _content() -> str:
    assert SPEC_FILE.exists(), f"File not found: {SPEC_FILE}"
    return SPEC_FILE.read_text(encoding="utf-8")


def _stage_4_section() -> str:
    """Extract the Stage 4 section text."""
    c = _content()
    start = c.index("Stage 4")
    end_markers = ["Stage 5", "## Routing Signal", "## What You Do Not Do"]
    end = len(c)
    for marker in end_markers:
        try:
            idx = c.index(marker, start)
            if idx < end:
                end = idx
        except ValueError:
            continue
    return c[start:end]


def test_audience_depth_check_exists() -> None:
    """Stage 4 must contain an audience depth self-check."""
    section = _stage_4_section()
    has_check = (
        "audience depth" in section.lower()
        or "technical depth" in section.lower()
        or "non-technical audience" in section.lower()
    )
    assert has_check, (
        "Stage 4 must contain an audience depth self-check"
    )


def test_mechanism_vs_outcome_language() -> None:
    """Stage 4 must mention mechanism-level vs outcome-level language."""
    section = _stage_4_section()
    has_mechanism = "mechanism" in section.lower()
    has_outcome = "outcome" in section.lower()
    assert has_mechanism and has_outcome, (
        "Stage 4 must mention mechanism-level vs outcome-level language"
    )


def test_self_check_question() -> None:
    """Stage 4 must include the 'Would this sentence make sense' self-check."""
    section = _stage_4_section()
    has_question = (
        "would this sentence make sense" in section.lower()
        or "make sense to someone" in section.lower()
    )
    assert has_question, (
        "Stage 4 must include 'Would this sentence make sense to someone who doesn't build AI systems?'"
    )


def test_technical_audiences_excluded() -> None:
    """Stage 4 must mention that technical audiences are excluded from the check."""
    section = _stage_4_section()
    has_exclusion = (
        "technical practitioners" in section.lower()
        or "ai engineers" in section.lower()
        or "developers" in section.lower()
        or "skip this check" in section.lower()
    )
    assert has_exclusion, (
        "Stage 4 must mention technical audiences are excluded from the depth check"
    )


def test_audience_check_in_stage_4() -> None:
    """The audience depth check must be within Stage 4."""
    section = _stage_4_section()
    has_audience_logic = (
        "audience" in section.lower()
        and "depth" in section.lower()
    )
    assert has_audience_logic, (
        "The audience depth check must be within Stage 4"
    )
