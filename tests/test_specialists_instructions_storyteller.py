"""
TDD tests for task-05: Register storyteller in context/specialists-instructions.md.
Validates that all 3 required additions are present in the file.
"""

from __future__ import annotations

from pathlib import Path

INSTRUCTIONS_PATH = (
    Path(__file__).parent.parent / "context" / "specialists-instructions.md"
)


def load_content() -> str:
    assert INSTRUCTIONS_PATH.exists(), f"File not found: {INSTRUCTIONS_PATH}"
    return INSTRUCTIONS_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Addition (1): storyteller bullet in ## Available Specialists
# ---------------------------------------------------------------------------


def test_storyteller_bullet_present_in_available_specialists() -> None:
    """Storyteller entry must appear in the Available Specialists section."""
    content = load_content()
    assert "**storyteller**" in content, (
        "Available Specialists section must contain a '**storyteller**' bullet"
    )


def test_storyteller_bullet_mentions_story_output() -> None:
    """Storyteller bullet must reference StoryOutput."""
    content = load_content()
    assert "StoryOutput" in content, "Storyteller bullet must mention 'StoryOutput'"


def test_storyteller_bullet_mentions_narrative_selection() -> None:
    """Storyteller bullet must reference NARRATIVE SELECTION editorial record."""
    content = load_content()
    assert "NARRATIVE SELECTION" in content, (
        "Storyteller bullet must mention 'NARRATIVE SELECTION'"
    )


def test_storyteller_bullet_appears_after_researcher_formatter() -> None:
    """Storyteller bullet must appear after the researcher-formatter entry."""
    content = load_content()
    rf_pos = content.find("**researcher-formatter**")
    st_pos = content.find("**storyteller**")
    assert rf_pos != -1, "researcher-formatter bullet must exist"
    assert st_pos != -1, "storyteller bullet must exist"
    assert st_pos > rf_pos, (
        "storyteller bullet must appear after researcher-formatter bullet"
    )


# ---------------------------------------------------------------------------
# Addition (2): 'Delegate to storyteller when' block in ## When to Use Each
# ---------------------------------------------------------------------------


def test_delegate_to_storyteller_block_present() -> None:
    """'Delegate to storyteller when' block must exist in When to Use Each section."""
    content = load_content()
    assert "specialists:storyteller" in content, (
        "When to Use Each section must contain a delegate block for storyteller"
    )


def test_delegate_storyteller_mentions_compelling_narrative() -> None:
    """Delegate block must mention compelling narrative."""
    content = load_content()
    assert "compelling narrative" in content, (
        "Storyteller delegate block must mention 'compelling narrative'"
    )


def test_delegate_storyteller_mentions_moved_or_persuaded() -> None:
    """Delegate block must mention audience being moved or persuaded."""
    content = load_content()
    assert "moved or persuaded" in content, (
        "Storyteller delegate block must mention 'moved or persuaded'"
    )


def test_delegate_storyteller_appears_after_competitive_analysis_block() -> None:
    """Delegate-to-storyteller block must appear after the competitive-analysis block."""
    content = load_content()
    ca_pos = content.find("**Delegate to `specialists:competitive-analysis`")
    st_pos = content.find("**Delegate to `specialists:storyteller`")
    assert ca_pos != -1, "competitive-analysis delegate block must exist"
    assert st_pos != -1, "storyteller delegate block must exist"
    assert st_pos > ca_pos, (
        "storyteller delegate block must appear after competitive-analysis block"
    )


# ---------------------------------------------------------------------------
# Addition (3): Narrative chain in ## Typical Chain
# ---------------------------------------------------------------------------


def test_narrative_chain_present_in_typical_chain() -> None:
    """Typical Chain section must contain a narrative output chain."""
    content = load_content()
    assert "narrative output" in content.lower(), (
        "Typical Chain section must contain a narrative output chain"
    )


def test_narrative_chain_mentions_storyteller_step() -> None:
    """Narrative chain must reference the storyteller as a step."""
    content = load_content()
    # Should appear in the chain steps context
    assert "storyteller" in content.lower(), (
        "Narrative chain must mention storyteller as a step"
    )


def test_narrative_chain_appears_after_competitive_intelligence_chain() -> None:
    """Narrative chain must appear after the competitive intelligence chain block."""
    content = load_content()
    ci_pos = content.find("competitive intelligence")
    # Find second occurrence (first is in section header/desc, second is in chain)
    nc_pos = content.find("narrative output", ci_pos)
    assert ci_pos != -1, "competitive intelligence chain block must exist"
    assert nc_pos != -1, (
        "narrative output chain must appear after competitive intelligence chain"
    )


# ---------------------------------------------------------------------------
# Storyteller index.md: STORY OUTPUT literal first-line enforcement
# ---------------------------------------------------------------------------

STORYTELLER_INDEX_PATH = Path(__file__).parent.parent / "agents" / "storyteller.md"


def load_storyteller_index() -> str:
    assert STORYTELLER_INDEX_PATH.exists(), f"File not found: {STORYTELLER_INDEX_PATH}"
    return STORYTELLER_INDEX_PATH.read_text(encoding="utf-8")
