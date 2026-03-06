"""Test that the OUTPUT CONTRACT block has been removed from researcher/index.md.

Task-2: The OUTPUT CONTRACT block pre-committed the model to a rigid output format
before any research began. It didn't work after 10+ tool calls. The formatter now
owns format compliance, so this block is removed.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RESEARCHER_INDEX = REPO_ROOT / "specialists" / "researcher" / "index.md"


def test_no_output_contract_text_in_researcher():
    """The string 'OUTPUT CONTRACT' must not appear anywhere in researcher/index.md."""
    content = RESEARCHER_INDEX.read_text()
    assert "OUTPUT CONTRACT" not in content, (
        "OUTPUT CONTRACT text still present in researcher/index.md"
    )


def test_single_separator_between_intro_and_core_principles():
    """Where the OUTPUT CONTRACT block was, there should be a single --- separator.

    The structure should be:
      ...You fill the evidence brief.
      (blank line)
      ---
      (blank line)
      ## Core Principles

    There must NOT be two --- separators with content between them in that region.
    """
    content = RESEARCHER_INDEX.read_text()
    # The text before the separator
    assert "You do not write the article. You fill the evidence brief." in content
    # The text after the separator
    assert "## Core Principles" in content

    # Extract the region between "evidence brief" and "Core Principles"
    brief_idx = content.index("You fill the evidence brief.")
    core_idx = content.index("## Core Principles")
    between = content[brief_idx:core_idx]

    # Count --- separators in that region (must be exactly 1)
    separator_count = between.count("\n---\n")
    assert separator_count == 1, (
        f"Expected exactly 1 '---' separator between intro and Core Principles, "
        f"found {separator_count}. Content between:\n{between}"
    )
