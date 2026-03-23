"""
Structural tests for researcher iterative deepening (#49).
Validates that the researcher agent file contains a depth check
in the Quality Gate that detects thin sub-questions and runs
targeted deepening passes.

Fixes #49: iterative deepening for thin sub-questions.
"""

from functools import lru_cache
from pathlib import Path

SPEC_FILE = Path(__file__).parent.parent / "agents" / "researcher.md"


@lru_cache(maxsize=None)
def _content() -> str:
    assert SPEC_FILE.exists(), f"File not found: {SPEC_FILE}"
    return SPEC_FILE.read_text(encoding="utf-8")


def test_depth_check_exists() -> None:
    """Quality Gate must contain a depth check for thin sub-questions."""
    c = _content()
    has_depth_check = (
        "depth check" in c.lower()
        or "iterative deepening" in c.lower()
        or "thin sub-question" in c.lower()
    )
    assert has_depth_check, (
        "Quality Gate must contain a depth check — "
        "expected 'depth check', 'iterative deepening', or 'thin sub-question'"
    )


def test_depth_check_after_breadth_gate() -> None:
    """Depth check must come after the factual breadth gate in the file."""
    c = _content()
    assert c.index("Factual breadth gate") < c.index("Depth check"), (
        "Depth check must come after the factual breadth gate"
    )


def test_depth_check_source_count_trigger() -> None:
    """Depth check must mention fewer than 3 sources as a trigger."""
    c = _content()
    has_count_trigger = (
        "fewer than 3" in c
        or "< 3" in c
        or "less than 3" in c
    )
    assert has_count_trigger, (
        "Depth check must mention 'fewer than 3' or '< 3' sources as a trigger"
    )


def test_depth_check_tier_trigger() -> None:
    """Depth check must mention no primary or no academic sources as a trigger."""
    c = _content()
    has_tier_trigger = (
        "no primary" in c.lower()
        or "no academic" in c.lower()
        or "lacks primary" in c.lower()
        or "lacks academic" in c.lower()
    )
    assert has_tier_trigger, (
        "Depth check must mention 'no primary' or 'no academic' sources as a trigger"
    )


def test_depth_check_academic_search() -> None:
    """Depth check must mention academic sources as a deepening strategy."""
    c = _content()
    has_academic = (
        "arxiv" in c.lower()
        or "google scholar" in c.lower()
        or "conference proceedings" in c.lower()
    )
    assert has_academic, (
        "Depth check must mention arxiv, Google Scholar, or conference proceedings"
    )


def test_depth_check_official_search() -> None:
    """Depth check must mention official sources as a deepening strategy."""
    c = _content()
    has_official = (
        "official doc" in c.lower()
        or "gov site" in c.lower()
        or "vendor page" in c.lower()
        or ".gov" in c.lower()
    )
    assert has_official, (
        "Depth check must mention official docs, gov sites, or vendor pages"
    )


def test_depth_check_practitioner_search() -> None:
    """Depth check must mention practitioner sources as a deepening strategy."""
    c = _content()
    has_practitioner = (
        "engineering blog" in c.lower()
        or "case stud" in c.lower()
        or "conference talk" in c.lower()
    )
    assert has_practitioner, (
        "Depth check must mention engineering blogs, case studies, or conference talks"
    )
