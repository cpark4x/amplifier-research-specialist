"""
Structural tests for writer-formatter tier-aware hedging (#40).
Validates that Stage 3.5 checks source tiers before inserting hedges,
protecting primary/secondary source claims from inappropriate "reportedly."

Fixes #40: writer-formatter tier-aware hedging in Stage 3.5.
"""

from functools import lru_cache
from pathlib import Path

SPEC_FILE = Path(__file__).parent.parent / "agents" / "writer-formatter.md"


@lru_cache(maxsize=None)
def _content() -> str:
    assert SPEC_FILE.exists(), f"File not found: {SPEC_FILE}"
    return SPEC_FILE.read_text(encoding="utf-8")


def _stage_35_section() -> str:
    """Extract the Stage 3.5 section text."""
    c = _content()
    start = c.index("Stage 3.5")
    # Stage 3.5 ends before Stage 4 or "Claims to Verify"
    end_markers = ["Stage 4", "CLAIMS TO VERIFY"]
    end = len(c)
    for marker in end_markers:
        try:
            idx = c.index(marker, start)
            if idx < end:
                end = idx
        except ValueError:
            continue
    return c[start:end]


def test_tier_check_exists_in_stage_35() -> None:
    """Stage 3.5 must contain tier-aware or source-tier language."""
    section = _stage_35_section()
    has_tier = (
        "source tier" in section.lower()
        or "tier-aware" in section.lower()
        or "primary" in section.lower() and "secondary" in section.lower()
    )
    assert has_tier, (
        "Stage 3.5 must contain source-tier-aware language"
    )


def test_primary_secondary_protected() -> None:
    """Stage 3.5 must mention that primary/secondary claims are protected from weak hedges."""
    section = _stage_35_section()
    has_protection = (
        "do not insert" in section.lower()
        or "skip" in section.lower() and "primary" in section.lower()
        or "protect" in section.lower()
    )
    assert has_protection, (
        "Stage 3.5 must mention primary/secondary claims are protected from 'reportedly'"
    )


def test_tertiary_still_hedged() -> None:
    """Stage 3.5 must mention that tertiary claims still get hedged."""
    section = _stage_35_section()
    has_tertiary = (
        "tertiary" in section.lower()
    )
    assert has_tertiary, (
        "Stage 3.5 must mention tertiary claims still get hedged"
    )


def test_tier_check_in_stage_35() -> None:
    """The tier check must be within the Stage 3.5 section."""
    section = _stage_35_section()
    has_tier_logic = (
        "source tier" in section.lower()
        or "primary" in section.lower()
    )
    assert has_tier_logic, (
        "The tier check must be within the Stage 3.5 section"
    )


def test_inference_unchanged() -> None:
    """Stage 3.5 must mention that inference claims are unchanged."""
    section = _stage_35_section()
    has_inference = (
        "inference" in section.lower()
    )
    assert has_inference, (
        "Stage 3.5 must mention inference claim handling is unchanged"
    )
