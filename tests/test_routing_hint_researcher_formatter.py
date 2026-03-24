"""
TDD tests for the Routing Signal section in agents/researcher-formatter.md
Validates acceptance criteria for task-6: Add Routing Hint to Researcher Formatter.
"""

from functools import lru_cache
from pathlib import Path

SPEC_FILE = Path(__file__).parent.parent / "agents" / "researcher-formatter.md"


@lru_cache(maxsize=None)
def _content() -> str:
    assert SPEC_FILE.exists(), f"File not found: {SPEC_FILE}"
    return SPEC_FILE.read_text(encoding="utf-8")


def test_routing_signal_section_exists() -> None:
    assert "## Routing Signal (for orchestrator use only)" in _content()


def test_routing_signal_after_stage2_format_block() -> None:
    c = _content()
    # The Stage 2 output format block closes before the routing signal
    assert c.index("RESEARCH EVENTS:") < c.index("## Routing Signal")


def test_routing_signal_before_what_you_do_not_do() -> None:
    c = _content()
    assert c.index("## Routing Signal") < c.index("## What You Do Not Do")


def test_routing_signal_content_natural_next_step_data_analyzer() -> None:
    c = _content()
    signal_section = c.split("## Routing Signal")[1].split("## What You Do Not Do")[0]
    assert "data-analyzer" in signal_section


def test_routing_signal_content_natural_next_step_writer() -> None:
    c = _content()
    signal_section = c.split("## Routing Signal")[1].split("## What You Do Not Do")[0]
    assert "writer (format=brief)" in signal_section


def test_routing_signal_content_produced_research_output() -> None:
    # The routing signal should mention RESEARCH OUTPUT as the produced artifact
    assert "RESEARCH OUTPUT" in _content().split("## Routing Signal")[1]


def test_routing_signal_content_quality() -> None:
    c = _content()
    signal_section = c.split("## Routing Signal")[1].split("## What You Do Not Do")[0]
    assert "[quality_score]" in signal_section


def test_routing_signal_orchestrator_only_note() -> None:
    assert "orchestrator routing and narration only" in _content()


def test_stage2_output_starts_with_research_output() -> None:
    # The specialist's actual output format must still start with RESEARCH OUTPUT
    # Verify it is the very first non-blank line inside the Stage 2 format block
    c = _content()
    stage2_section = c.split("### Stage 2: Produce RESEARCH OUTPUT")[1].split(
        "## Routing Signal"
    )[0]
    # Extract content inside the ``` code fence (between opening and closing markers)
    format_block = stage2_section.split("```")[1]
    lines = [line.strip() for line in format_block.splitlines() if line.strip()]
    assert lines[0] == "RESEARCH OUTPUT"


def test_separator_structure_around_routing_signal() -> None:
    c = _content()
    signal_block = c.split("## Routing Signal")[1].split("## What You Do Not Do")[0]
    assert signal_block.strip().endswith("---")
