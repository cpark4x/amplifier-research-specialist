"""
TDD tests for task-06: Register storyteller in main README.md specialists table.
Validates both acceptance criteria from the spec.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

README_PATH = Path(__file__).parent.parent / "README.md"


@pytest.fixture(scope="module")
def content() -> str:
    assert README_PATH.exists(), f"File not found: {README_PATH}"
    return README_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Acceptance criterion (1): Storyteller row present in Available Specialists
# table as the 5th row (after researcher, writer, competitive-analysis,
# data-analyzer).
# ---------------------------------------------------------------------------


def test_storyteller_row_present_in_table(content: str) -> None:
    """The storyteller row must appear in the Available Specialists table."""
    assert "| [storyteller](specialists/storyteller/) |" in content, (
        "Available Specialists table must contain a storyteller row"
    )


def test_storyteller_row_mentions_cognitive_mode_translation(content: str) -> None:
    """The storyteller table row must mention 'cognitive mode translation'."""
    assert re.search(r"\| \[storyteller\].*cognitive mode translation", content), (
        "Storyteller row must mention 'cognitive mode translation'"
    )


def test_storyteller_row_has_v1_status(content: str) -> None:
    """The storyteller table row must have 'v1' status."""
    assert re.search(
        r"\| \[storyteller\]\(specialists/storyteller/\).*v1 \|", content
    ), "Storyteller row must have 'v1' status"


def test_storyteller_is_fifth_row_in_table(content: str) -> None:
    """Storyteller must be the 5th data row in the Available Specialists table
    (after researcher, writer, competitive-analysis, data-analyzer)."""
    # Extract the table block
    table_match = re.search(
        r"\| Specialist \|.*\n\|[-| ]+\|\n((?:\|.*\|\n?)+)",
        content,
    )
    assert table_match, "Could not locate the Available Specialists table"
    rows_block = table_match.group(1)
    rows = [r for r in rows_block.strip().splitlines() if r.strip().startswith("|")]
    assert len(rows) >= 5, f"Expected at least 5 data rows, found {len(rows)}"
    assert "storyteller" in rows[4], (
        f"5th table row (index 4) must be storyteller, got: {rows[4]}"
    )


def test_table_row_order(content: str) -> None:
    """Rows must appear in order: researcher, writer, competitive-analysis,
    data-analyzer, storyteller."""
    expected_order = [
        "researcher",
        "writer",
        "competitive-analysis",
        "data-analyzer",
        "storyteller",
    ]
    positions = [content.index(name) for name in expected_order if name in content]
    assert positions == sorted(positions), (
        "Table rows must appear in order: researcher, writer, competitive-analysis, "
        "data-analyzer, storyteller"
    )


# ---------------------------------------------------------------------------
# Acceptance criterion (2): "More specialists" line no longer mentions
# Storyteller or Competitive Analysis.
# ---------------------------------------------------------------------------


def test_more_specialists_line_present(content: str) -> None:
    """The 'More specialists are planned' sentence must still exist."""
    assert "More specialists are planned" in content, (
        "The 'More specialists are planned' sentence must be present"
    )


def test_more_specialists_line_does_not_mention_storyteller(content: str) -> None:
    """The 'More specialists are planned' line must NOT mention 'Storyteller'."""
    more_line_match = re.search(r"More specialists are planned.*", content)
    assert more_line_match, "Could not find 'More specialists are planned' line"
    more_line = more_line_match.group(0)
    assert "Storyteller" not in more_line, (
        f"'More specialists' line must NOT mention 'Storyteller' (now shipped): {more_line}"
    )


def test_more_specialists_line_does_not_mention_competitive_analysis(
    content: str,
) -> None:
    """The 'More specialists are planned' line must NOT mention 'Competitive Analysis'."""
    more_line_match = re.search(r"More specialists are planned.*", content)
    assert more_line_match, "Could not find 'More specialists are planned' line"
    more_line = more_line_match.group(0)
    assert "Competitive Analysis" not in more_line, (
        f"'More specialists' line must NOT mention 'Competitive Analysis' (now shipped): {more_line}"
    )


def test_more_specialists_line_mentions_new_planned_items(content: str) -> None:
    """The updated 'More specialists' line must mention the new planned specialists."""
    more_line_match = re.search(r"More specialists are planned.*", content)
    assert more_line_match, "Could not find 'More specialists are planned' line"
    more_line = more_line_match.group(0)
    assert "Presentation Builder" in more_line, (
        "Updated 'More specialists' line must mention 'Presentation Builder'"
    )
