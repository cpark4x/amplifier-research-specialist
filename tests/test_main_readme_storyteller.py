"""
TDD tests for task-06: Register storyteller in main README.md specialists table.
Validates both acceptance criteria from the spec.

Updated assertions to match the rewritten README format:
- Storyteller appears as | **storyteller** | (bold, no hyperlink) in the
  Specialized tools table alongside competitive-analysis, prioritizer, planner.
- README uses two separate tables: Core pipeline and Specialized tools.
  No "More specialists are planned" line — all shipped specialists are listed
  directly in their respective tables.
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
# Acceptance criterion (1): Storyteller row present in Specialized tools
# table as the 4th row (after competitive-analysis, prioritizer, planner).
# ---------------------------------------------------------------------------


def test_storyteller_row_present_in_table(content: str) -> None:
    """The storyteller row must appear in the specialists tables."""
    assert "| **storyteller** |" in content, (
        "Specialists table must contain a storyteller row"
    )


def test_storyteller_row_mentions_editorial_selection(content: str) -> None:
    """The storyteller table row must mention 'editorial selection record'."""
    assert re.search(r"\| \*\*storyteller\*\*.*editorial selection record", content), (
        "Storyteller row must mention 'editorial selection record'"
    )


def test_storyteller_row_in_specialized_tools_section(content: str) -> None:
    """The storyteller row must appear in the Specialized tools section."""
    assert "**Specialized tools**" in content, (
        "README must contain a '**Specialized tools**' section"
    )
    specialized_section = content.split("**Specialized tools**")[1]
    assert "storyteller" in specialized_section, (
        "Storyteller must appear in the Specialized tools section"
    )


def test_storyteller_is_fourth_row_in_specialized_table(content: str) -> None:
    """Storyteller must be the 4th data row in the Specialized tools table
    (after competitive-analysis, prioritizer, planner)."""
    # Extract only the Specialized tools portion of the document
    specialized_section = content.split("**Specialized tools**")[1]
    table_match = re.search(
        r"\| Specialist \|.*\n\|[-| ]+\|\n((?:\|.*\|\n?)+)",
        specialized_section,
    )
    assert table_match, "Could not locate the Specialized tools table"
    rows_block = table_match.group(1)
    rows = [r for r in rows_block.strip().splitlines() if r.strip().startswith("|")]
    assert len(rows) >= 4, f"Expected at least 4 data rows, found {len(rows)}"
    assert "storyteller" in rows[3], (
        f"4th table row (index 3) must be storyteller, got: {rows[3]}"
    )


def test_table_row_order(content: str) -> None:
    """Specialist table rows must appear in document order across the two tables:
    Core pipeline (researcher, data-analyzer, writer) then
    Specialized tools (competitive-analysis, storyteller)."""
    # Anchor each search to the table-cell prefix so we skip prose mentions
    # of "writer" / "researcher" that appear before the table.
    row_markers = [
        "| **researcher**",
        "| **data-analyzer**",
        "| **writer**",
        "| **competitive-analysis**",
        "| **storyteller**",
    ]
    positions = [content.index(m) for m in row_markers if m in content]
    assert positions == sorted(positions), (
        "Specialist table rows must appear in order: researcher, data-analyzer, "
        "writer (core pipeline), then competitive-analysis, storyteller (specialized tools)"
    )


# ---------------------------------------------------------------------------
# Acceptance criterion (2): README has two specialist subsections — Core
# pipeline and Specialized tools — with shipped specialists listed directly
# (no longer referenced as "planned").
# ---------------------------------------------------------------------------


def test_specialists_section_has_two_subsections(content: str) -> None:
    """README must have both a Core pipeline and a Specialized tools subsection."""
    assert "**Core pipeline**" in content, (
        "README must contain a '**Core pipeline**' section"
    )
    assert "**Specialized tools**" in content, (
        "README must contain a '**Specialized tools**' section"
    )


def test_storyteller_appears_in_specialized_tools(content: str) -> None:
    """Storyteller must appear in the Specialized tools section (shipped, not planned)."""
    specialized_section = content.split("**Specialized tools**")[1]
    assert "storyteller" in specialized_section, (
        "Storyteller must be listed in the Specialized tools section"
    )


def test_competitive_analysis_appears_in_specialized_tools(content: str) -> None:
    """Competitive-analysis must appear in the Specialized tools section (shipped)."""
    specialized_section = content.split("**Specialized tools**")[1]
    assert "competitive-analysis" in specialized_section, (
        "competitive-analysis must be listed in the Specialized tools section"
    )


def test_planner_appears_in_specialized_tools(content: str) -> None:
    """Planner must appear in the Specialized tools section."""
    specialized_section = content.split("**Specialized tools**")[1]
    assert "planner" in specialized_section, (
        "planner must be listed in the Specialized tools section"
    )
