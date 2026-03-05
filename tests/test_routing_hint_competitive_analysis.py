"""
TDD tests for the Routing Signal section in specialists/competitive-analysis/index.md
Validates acceptance criteria for task-4: Add Routing Hint to Competitive Analysis.
"""

from __future__ import annotations

from pathlib import Path

SPEC_FILE = (
    Path(__file__).parent.parent / "specialists" / "competitive-analysis" / "index.md"
)


def _content() -> str:
    assert SPEC_FILE.exists(), f"File not found: {SPEC_FILE}"
    return SPEC_FILE.read_text(encoding="utf-8")


def test_routing_signal_section_exists() -> None:
    assert "## Routing Signal (for orchestrator use only)" in _content()


def test_routing_signal_after_output_format() -> None:
    c = _content()
    assert c.index("Writer specialist will transform") < c.index("## Routing Signal")


def test_routing_signal_before_what_you_do_not_do() -> None:
    c = _content()
    assert c.index("## Routing Signal") < c.index("## What You Do Not Do")


def test_routing_signal_content_natural_next_step() -> None:
    assert "writer (format=brief)" in _content()


def test_routing_signal_content_produced() -> None:
    assert "COMPETITIVE ANALYSIS BRIEF" in _content().split("## Routing Signal")[1]


def test_routing_signal_content_quality() -> None:
    assert "[quality_score]" in _content()


def test_routing_signal_orchestrator_only_note() -> None:
    assert "orchestrator routing and narration only" in _content()


def test_output_format_starts_with_competitive_analysis_brief() -> None:
    section = _content().split("## Output Format")[1].split("## Routing Signal")[0]
    assert "COMPETITIVE ANALYSIS BRIEF" in section


def test_separator_structure_around_routing_signal() -> None:
    signal_block = (
        _content().split("## Routing Signal")[1].split("## What You Do Not Do")[0]
    )
    assert signal_block.strip().endswith("---")
