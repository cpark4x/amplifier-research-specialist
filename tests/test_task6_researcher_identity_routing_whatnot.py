"""
Tests for Task 6: Update identity paragraph, routing signal, and
'What You Do Not Do' sections in researcher/index.md.

Acceptance criteria:
- Identity paragraph mentions 'downstream formatter specialist handles output formatting'
- Routing signal mentions 'researcher-formatter' as the next step
- 'What You Do Not Do' says 'polished documents' instead of 'prose, narratives'
"""

from pathlib import Path

RESEARCHER_PATH = (
    Path(__file__).parent.parent / "specialists" / "researcher" / "index.md"
)


def _content() -> str:
    assert RESEARCHER_PATH.exists(), f"File not found: {RESEARCHER_PATH}"
    return RESEARCHER_PATH.read_text(encoding="utf-8")


# --- Edit 1: Identity paragraph ---


def test_identity_mentions_source_tiered_evidence():
    """Identity paragraph should say 'source-tiered evidence'."""
    content = _content()
    assert "source-tiered evidence" in content


def test_identity_mentions_downstream_formatter():
    """Identity paragraph must mention the downstream formatter specialist."""
    content = _content()
    assert "downstream formatter specialist handles output formatting" in content


def test_identity_old_phrasing_removed():
    """Old identity phrasing should no longer be present."""
    content = _content()
    assert "You do not write the article. You fill the evidence brief." not in content


def test_identity_every_finding_traces():
    """New identity paragraph should include traceability statement."""
    content = _content()
    assert "Every finding traces to a source" in content


# --- Edit 2: Routing Signal ---


def test_routing_signal_mentions_researcher_formatter():
    """Routing signal must mention researcher-formatter as the next step."""
    content = _content()
    signal_section = content.split("## Routing Signal")[1].split("---")[0]
    assert "researcher-formatter" in signal_section


def test_routing_signal_no_stage7_reference():
    """Routing signal should say 'research output' not 'Stage 7 output'."""
    content = _content()
    signal_section = content.split("## Routing Signal")[1].split("---")[0]
    assert "Stage 7" not in signal_section


def test_routing_signal_mentions_tiered_sources():
    """Routing signal 'Produced' line should mention tiered sources."""
    content = _content()
    signal_section = content.split("## Routing Signal")[1].split("---")[0]
    assert "tiered sources" in signal_section


# --- Edit 3: What You Do Not Do ---


def test_what_you_do_not_do_says_polished_documents():
    """'What You Do Not Do' must say 'polished documents'."""
    content = _content()
    section = content.split("## What You Do Not Do")[1]
    assert "polished documents" in section


def test_what_you_do_not_do_old_phrasing_removed():
    """Old 'prose, narratives' phrasing should be gone."""
    content = _content()
    section = content.split("## What You Do Not Do")[1]
    assert "prose, narratives" not in section
