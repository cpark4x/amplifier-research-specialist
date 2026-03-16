"""
Tests for Task 6: Update identity paragraph, routing signal, and
'What You Do Not Do' sections in researcher/index.md.

Acceptance criteria:
- Identity paragraph mentions 'downstream formatter specialist handles output formatting'
- Routing signal mentions 'researcher-formatter' as the next step
- 'What You Do Not Do' says 'polished documents' instead of 'prose, narratives'
"""

from pathlib import Path

import pytest

RESEARCHER_PATH = Path(__file__).parent.parent / "agents" / "researcher.md"


@pytest.fixture(scope="module")
def content() -> str:
    """Read researcher/index.md once for the entire test module."""
    assert RESEARCHER_PATH.exists(), f"File not found: {RESEARCHER_PATH}"
    return RESEARCHER_PATH.read_text(encoding="utf-8")


# --- Edit 1: Identity paragraph ---


def test_identity_mentions_source_tiered_evidence(content: str) -> None:
    """Identity paragraph should say 'source-tiered evidence'."""
    assert "source-tiered evidence" in content


def test_identity_mentions_downstream_formatter(content: str) -> None:
    """Identity paragraph must mention the downstream formatter specialist."""
    assert "downstream formatter specialist handles output formatting" in content


def test_identity_old_phrasing_removed(content: str) -> None:
    """Old identity phrasing should no longer be present."""
    assert "You do not write the article. You fill the evidence brief." not in content


def test_identity_every_finding_traces(content: str) -> None:
    """New identity paragraph should include traceability statement."""
    assert "Every finding traces to a source" in content


# --- Edit 2: Routing Signal ---


def _routing_signal_section(content: str) -> str:
    """Extract the Routing Signal section with a clear error on missing heading."""
    heading = "## Routing Signal"
    assert heading in content, f"Expected heading '{heading}' not found in file"
    return content.split(heading)[1].split("---")[0]


def test_routing_signal_mentions_researcher_formatter(content: str) -> None:
    """Routing signal must mention researcher-formatter as the next step."""
    section = _routing_signal_section(content)
    assert "researcher-formatter" in section


def test_routing_signal_no_stage7_reference(content: str) -> None:
    """Routing signal should say 'research output' not 'Stage 7 output'."""
    section = _routing_signal_section(content)
    assert "Stage 7" not in section


def test_routing_signal_mentions_tiered_sources(content: str) -> None:
    """Routing signal 'Produced' line should mention tiered sources."""
    section = _routing_signal_section(content)
    assert "tiered sources" in section


# --- Edit 3: What You Do Not Do ---


def _what_you_do_not_do_section(content: str) -> str:
    """Extract the 'What You Do Not Do' section with a clear error on missing heading."""
    heading = "## What You Do Not Do"
    assert heading in content, f"Expected heading '{heading}' not found in file"
    return content.split(heading)[1]


def test_what_you_do_not_do_says_polished_documents(content: str) -> None:
    """'What You Do Not Do' must say 'polished documents'."""
    section = _what_you_do_not_do_section(content)
    assert "polished documents" in section


def test_what_you_do_not_do_old_phrasing_removed(content: str) -> None:
    """Old 'prose, narratives' phrasing should be gone."""
    section = _what_you_do_not_do_section(content)
    assert "prose, narratives" not in section
