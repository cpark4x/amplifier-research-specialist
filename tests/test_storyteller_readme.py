"""
Tests for specialists/storyteller/README.md — REMOVED.

The specialists/storyteller/README.md file no longer exists. The agents/ refactor
flattened the directory structure (specialists/AGENT/index.md → agents/AGENT.md)
and README companion files were not carried over. All tests that validated README.md
content have been removed to prevent false failures.

The index.md content is covered by test_storyteller_index.py which has been updated
to point to agents/storyteller.md.
"""

from __future__ import annotations


def test_placeholder_readme_removed() -> None:
    """Placeholder: specialists/storyteller/README.md was removed in the agents/ refactor."""
    pass
