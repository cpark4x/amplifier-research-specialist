"""
TDD tests for the Routing Signal section in specialists/data-analyzer/index.md
Validates acceptance criteria for task-5: Add Routing Hint to Data Analyzer.
"""

from functools import lru_cache
from pathlib import Path

SPEC_FILE = Path(__file__).parent.parent / "specialists" / "data-analyzer" / "index.md"


@lru_cache(maxsize=None)
def _content() -> str:
    assert SPEC_FILE.exists(), f"File not found: {SPEC_FILE}"
    return SPEC_FILE.read_text(encoding="utf-8")


def test_routing_signal_section_exists() -> None:
    assert "## Routing Signal (for orchestrator use only)" in _content()


def test_routing_signal_after_stage4_format_block() -> None:
    c = _content()
    # The Stage 4 output format block closes before the routing signal
    assert c.index("QUALITY THRESHOLD RESULT") < c.index("## Routing Signal")


def test_routing_signal_before_what_you_do_not_do() -> None:
    c = _content()
    assert c.index("## Routing Signal") < c.index("## What You Do Not Do")


def test_routing_signal_content_natural_next_step() -> None:
    assert "writer (format=brief)" in _content()


def test_routing_signal_content_produced_analysis_output() -> None:
    # The routing signal should mention ANALYSIS OUTPUT as the produced artifact
    assert "ANALYSIS OUTPUT" in _content().split("## Routing Signal")[1]


def test_routing_signal_content_quality() -> None:
    assert "[quality_score]" in _content()


def test_routing_signal_orchestrator_only_note() -> None:
    assert "orchestrator routing and narration only" in _content()


def test_stage4_output_starts_with_analysis_output() -> None:
    # The specialist's actual output must still start with ANALYSIS OUTPUT
    # Verify it is the very first non-blank line inside the Stage 4 format block
    c = _content()
    stage4_section = c.split("### Stage 4: Synthesize")[1].split("## Routing Signal")[0]
    # Extract content inside the ``` code fence (between opening and closing markers)
    format_block = stage4_section.split("```")[1]
    lines = [line.strip() for line in format_block.splitlines() if line.strip()]
    assert lines[0] == "ANALYSIS OUTPUT"


def test_separator_structure_around_routing_signal() -> None:
    c = _content()
    signal_block = c.split("## Routing Signal")[1].split("## What You Do Not Do")[0]
    assert signal_block.strip().endswith("---")
