"""
TDD tests for docs/01-vision/PRINCIPLES.md
Validates acceptance criteria from task-07: Storyteller-Specific Principles section.
"""

from __future__ import annotations

from pathlib import Path

import pytest

PRINCIPLES_PATH = Path(__file__).parent.parent / "docs" / "01-vision" / "PRINCIPLES.md"


@pytest.fixture(scope="module")
def content() -> str:
    assert PRINCIPLES_PATH.exists(), f"File not found: {PRINCIPLES_PATH}"
    return PRINCIPLES_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Last Updated date
# ---------------------------------------------------------------------------


def test_last_updated_is_2026_03_04(content: str) -> None:
    """Line 4 should reflect the updated date 2026-03-04."""
    assert "**Last Updated:** 2026-03-04" in content, (
        "Expected '**Last Updated:** 2026-03-04' but not found"
    )


# ---------------------------------------------------------------------------
# Section existence and placement
# ---------------------------------------------------------------------------


def test_storyteller_section_exists(content: str) -> None:
    """## Storyteller-Specific Principles section must exist."""
    assert "## Storyteller-Specific Principles" in content


def test_storyteller_section_before_change_history(content: str) -> None:
    """Storyteller section must appear before ## Change History."""
    storyteller_pos = content.index("## Storyteller-Specific Principles")
    change_history_pos = content.index("## Change History")
    assert storyteller_pos < change_history_pos, (
        "Storyteller-Specific Principles section must come before Change History"
    )


def test_storyteller_section_after_data_analyzer_section(content: str) -> None:
    """Storyteller section must appear after ## Data Analyzer-Specific Principles."""
    data_analyzer_pos = content.index("## Data Analyzer-Specific Principles")
    storyteller_pos = content.index("## Storyteller-Specific Principles")
    assert data_analyzer_pos < storyteller_pos, (
        "Storyteller-Specific Principles must come after Data Analyzer-Specific Principles"
    )


# ---------------------------------------------------------------------------
# Principle 1: The Writer covers. The Storyteller selects.
# ---------------------------------------------------------------------------


def test_principle_1_title(content: str) -> None:
    """Principle 1 title must be present."""
    assert "The Writer covers. The Storyteller selects." in content


def test_principle_1_decision(content: str) -> None:
    """Principle 1 Decision subsection must mention NARRATIVE SELECTION record and authorization."""
    # Check key concepts from the Decision
    assert "NARRATIVE SELECTION" in content
    assert "Storyteller authorized" in content or "Storyteller" in content


def test_principle_1_why(content: str) -> None:
    """Principle 1 Why subsection must reference Slovic 2007 and Heath 2007."""
    assert "Slovic" in content and "2007" in content
    assert "Heath" in content


def test_principle_1_what_rules_out(content: str) -> None:
    """Principle 1 must have a 'What this rules out' subsection."""
    # Count occurrences — there should be at least one for principle 1
    assert content.count("**What this rules out:**") >= 1


# ---------------------------------------------------------------------------
# Principle 2: Citations break the narrative mode
# ---------------------------------------------------------------------------


def test_principle_2_title(content: str) -> None:
    """Principle 2 title must be present."""
    assert "Citations break the narrative mode" in content


def test_principle_2_why_green_brock(content: str) -> None:
    """Principle 2 Why must reference Green & Brock 2000."""
    assert "Green" in content and "Brock" in content and "2000" in content


def test_principle_2_what_rules_out_citation_blocks(content: str) -> None:
    """Principle 2 What this rules out must mention attribution blocks."""
    assert "> *Sources:" in content or "Sources:" in content


# ---------------------------------------------------------------------------
# Principle 3: Framework and tone are independent
# ---------------------------------------------------------------------------


def test_principle_3_title(content: str) -> None:
    """Principle 3 title must be present."""
    assert "Framework and tone are independent" in content


def test_principle_3_decision_frameworks(content: str) -> None:
    """Principle 3 Decision must list the frameworks."""
    assert "SCQA" in content
    assert "three-act" in content
    assert "Story Spine" in content or "Sparkline" in content


def test_principle_3_what_rules_out(content: str) -> None:
    """Principle 3 must have a 'What this rules out' subsection."""
    assert content.count("**What this rules out:**") >= 3


# ---------------------------------------------------------------------------
# All three principles have Decision / Why / What this rules out
# ---------------------------------------------------------------------------


def test_three_decision_subsections(content: str) -> None:
    """There must be at least 3 Decision subsections in the Storyteller section."""
    storyteller_start = content.index("## Storyteller-Specific Principles")
    change_history_start = content.index("## Change History")
    storyteller_block = content[storyteller_start:change_history_start]
    assert storyteller_block.count("**Decision:**") >= 3


def test_three_why_subsections(content: str) -> None:
    """There must be at least 3 Why subsections in the Storyteller section."""
    storyteller_start = content.index("## Storyteller-Specific Principles")
    change_history_start = content.index("## Change History")
    storyteller_block = content[storyteller_start:change_history_start]
    assert storyteller_block.count("**Why:**") >= 3


def test_three_what_rules_out_subsections(content: str) -> None:
    """There must be at least 3 'What this rules out' subsections in the Storyteller section."""
    storyteller_start = content.index("## Storyteller-Specific Principles")
    change_history_start = content.index("## Change History")
    storyteller_block = content[storyteller_start:change_history_start]
    assert storyteller_block.count("**What this rules out:**") >= 3


# ---------------------------------------------------------------------------
# Change History
# ---------------------------------------------------------------------------


def test_change_history_v1_2_entry(content: str) -> None:
    """Change History table must contain v1.2 entry."""
    assert "v1.2" in content


def test_change_history_v1_2_date(content: str) -> None:
    """v1.2 entry must have date 2026-03-04."""
    assert "2026-03-04" in content


def test_change_history_v1_2_author(content: str) -> None:
    """v1.2 entry must credit Chris Park."""
    # Chris Park appears in the v1.2 row
    lines = content.splitlines()
    v12_lines = [line for line in lines if "v1.2" in line]
    assert len(v12_lines) >= 1, "No line containing 'v1.2' found"
    assert "Chris Park" in v12_lines[0]


def test_change_history_v1_2_mentions_storyteller_principles(content: str) -> None:
    """v1.2 Change History entry must mention the Storyteller-Specific Principles."""
    lines = content.splitlines()
    v12_lines = [line for line in lines if "v1.2" in line]
    assert len(v12_lines) >= 1
    row = v12_lines[0]
    assert "Storyteller" in row or "storyteller" in row.lower()


def test_change_history_v1_2_is_top_row(content: str) -> None:
    """v1.2 entry must appear before v1.1 in the Change History table (top row)."""
    v12_pos = content.index("v1.2")
    v11_pos = content.index("v1.1")
    assert v12_pos < v11_pos, "v1.2 row must appear before v1.1 row in Change History"
