"""
Structural tests for writer-formatter degraded mode (graceful degradation).
Validates that the writer-formatter agent file contains degraded mode
detection, pass-through behavior, and citation-unavailable notice text.

Fixes #44: writer-formatter halts in ad-hoc mode when source corpus is missing.
"""

from functools import lru_cache
from pathlib import Path

SPEC_FILE = Path(__file__).parent.parent / "agents" / "writer-formatter.md"


@lru_cache(maxsize=None)
def _content() -> str:
    assert SPEC_FILE.exists(), f"File not found: {SPEC_FILE}"
    return SPEC_FILE.read_text(encoding="utf-8")


def test_degraded_mode_section_exists() -> None:
    """A 'Stage 0.5' or 'Degraded Mode' section heading must exist."""
    c = _content()
    assert "Stage 0.5" in c or "Degraded Mode" in c


def test_degraded_mode_detection_before_stage1() -> None:
    """The detection step must come before Stage 1 in the file."""
    c = _content()
    assert c.index("Stage 0.5") < c.index("Stage 1: Extract source claims")


def test_degraded_mode_checks_research_output_marker() -> None:
    """Stage 0.5 must mention RESEARCH OUTPUT as a detection marker."""
    c = _content()
    stage05_section = c.split("Stage 0.5")[1].split("Stage 1")[0]
    assert "RESEARCH OUTPUT" in stage05_section


def test_degraded_mode_checks_analysis_output_marker() -> None:
    """Stage 0.5 must mention ANALYSIS OUTPUT as a detection marker."""
    c = _content()
    stage05_section = c.split("Stage 0.5")[1].split("Stage 1")[0]
    assert "ANALYSIS OUTPUT" in stage05_section


def test_degraded_mode_notice_text() -> None:
    """The exact citation-unavailable notice must appear in the file."""
    assert "Citation block omitted" in _content()


def test_degraded_mode_pass_through() -> None:
    """Degraded mode must describe passing through the writer's prose unchanged."""
    c = _content()
    has_pass_through = (
        "pass-through" in c.lower()
        or "pass through" in c.lower()
        or "verbatim" in c.lower()
        or "unchanged" in c.lower()
    )
    assert has_pass_through, "Degraded mode must mention pass-through/verbatim/unchanged"


def test_full_mode_still_exists() -> None:
    """Stage 1 two-input contract language must still be present (full mode intact)."""
    c = _content()
    assert "You receive two inputs" in c
    assert "Writer output" in c
    assert "Original source material" in c
