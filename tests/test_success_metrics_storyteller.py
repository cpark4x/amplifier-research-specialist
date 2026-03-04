"""
TDD tests for docs/01-vision/SUCCESS-METRICS.md
Validates all acceptance criteria from the spec (task-08):
  (1) ## Storyteller Metrics section exists between Data Analyzer Metrics and V3 Metrics
  (2) Table of Contents is updated with Storyteller Metrics at #5 and renumbered items
  (3) Change History has v1.3 entry
  (4) Last Updated date changed to 2026-03-04
"""

from __future__ import annotations

from pathlib import Path

import pytest

METRICS_PATH = Path(__file__).parent.parent / "docs" / "01-vision" / "SUCCESS-METRICS.md"


@pytest.fixture(scope="module")
def content() -> str:
    assert METRICS_PATH.exists(), f"File not found: {METRICS_PATH}"
    return METRICS_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Change (4): Last Updated date
# ---------------------------------------------------------------------------


def test_last_updated_date(content: str) -> None:
    assert "**Last Updated:** 2026-03-04" in content, (
        "Last Updated should be 2026-03-04"
    )


# ---------------------------------------------------------------------------
# Change (3): Change History v1.3 entry
# ---------------------------------------------------------------------------


def test_change_history_has_v1_3(content: str) -> None:
    assert "| v1.3 |" in content, "Change History must have a v1.3 row"


def test_change_history_v1_3_date(content: str) -> None:
    assert "| v1.3 | 2026-03-04 |" in content, (
        "v1.3 row must have date 2026-03-04"
    )


def test_change_history_v1_3_author(content: str) -> None:
    assert "| v1.3 | 2026-03-04 | Chris Park |" in content, (
        "v1.3 row must have author Chris Park"
    )


def test_change_history_v1_3_mentions_storyteller(content: str) -> None:
    # Find the v1.3 row and check it mentions Storyteller Metrics
    lines = content.splitlines()
    v13_line = next((l for l in lines if l.startswith("| v1.3 |")), None)
    assert v13_line is not None, "v1.3 row not found"
    assert "Storyteller Metrics" in v13_line, (
        "v1.3 row must mention 'Storyteller Metrics'"
    )
    assert "ST1" in v13_line and "ST4" in v13_line, (
        "v1.3 row must mention ST1 and ST4"
    )
    assert "SC1" in v13_line and "SC2" in v13_line, (
        "v1.3 row must mention SC1 and SC2"
    )


def test_change_history_v1_3_appears_before_v1_2(content: str) -> None:
    assert content.index("| v1.3 |") < content.index("| v1.2 |"), (
        "v1.3 row must appear before v1.2 row (newest first)"
    )


# ---------------------------------------------------------------------------
# Change (2): Table of Contents
# ---------------------------------------------------------------------------


def test_toc_has_storyteller_metrics_at_5(content: str) -> None:
    assert "5. [Storyteller Metrics]" in content, (
        "Table of Contents item 5 must be Storyteller Metrics"
    )


def test_toc_has_v3_metrics_at_6(content: str) -> None:
    assert "6. [V3 Metrics: Ecosystem Maturity]" in content, (
        "Table of Contents item 6 must be V3 Metrics: Ecosystem Maturity"
    )


def test_toc_has_what_we_dont_measure_at_7(content: str) -> None:
    assert "7. [What We Don't Measure]" in content, (
        "Table of Contents item 7 must be What We Don't Measure"
    )


def test_toc_has_success_criteria_at_8(content: str) -> None:
    assert "8. [Success Criteria by Phase]" in content, (
        "Table of Contents item 8 must be Success Criteria by Phase"
    )


def test_toc_has_the_standard_at_9(content: str) -> None:
    assert "9. [The Standard]" in content, (
        "Table of Contents item 9 must be The Standard"
    )


def test_toc_v3_no_longer_at_5(content: str) -> None:
    assert "5. [V3 Metrics: Ecosystem Maturity]" not in content, (
        "V3 Metrics must NOT be at position 5 in the ToC"
    )


# ---------------------------------------------------------------------------
# Change (1): ## Storyteller Metrics section
# ---------------------------------------------------------------------------


def test_storyteller_metrics_section_exists(content: str) -> None:
    assert "## Storyteller Metrics" in content, (
        "## Storyteller Metrics section must exist"
    )


def test_storyteller_metrics_between_data_analyzer_and_v3(content: str) -> None:
    da_pos = content.index("## Data Analyzer Metrics")
    st_pos = content.index("## Storyteller Metrics")
    v3_pos = content.index("## V3 Metrics: Ecosystem Maturity")
    assert da_pos < st_pos < v3_pos, (
        "## Storyteller Metrics must appear after Data Analyzer Metrics "
        "and before V3 Metrics"
    )


def test_storyteller_phase_goal(content: str) -> None:
    assert "cognitive mode translation" in content, (
        "Storyteller phase goal must mention 'cognitive mode translation'"
    )
    assert "moves audiences to action" in content, (
        "Storyteller phase goal must mention 'moves audiences to action'"
    )


# Specialist-Specific Success Criteria ST1–ST4

def test_st1_criterion_exists(content: str) -> None:
    assert "ST1" in content, "ST1 criterion must be present"
    assert "Narrative arc completeness" in content, (
        "ST1 must reference 'Narrative arc completeness'"
    )
    assert "dramatic question" in content, "ST1 must mention 'dramatic question'"
    assert "structural checklist" in content, "ST1 must mention 'structural checklist'"


def test_st2_criterion_exists(content: str) -> None:
    assert "ST2" in content, "ST2 criterion must be present"
    assert "Selection record complete" in content, (
        "ST2 must reference 'Selection record complete'"
    )
    assert "NARRATIVE SELECTION" in content, (
        "ST2 must mention 'NARRATIVE SELECTION'"
    )
    assert "INCLUDED + OMITTED" in content, (
        "ST2 must mention 'INCLUDED + OMITTED = total findings'"
    )


def test_st3_criterion_exists(content: str) -> None:
    assert "ST3" in content, "ST3 criterion must be present"
    assert "Source fidelity" in content, "ST3 must reference 'Source fidelity'"
    assert "zero claims" in content.lower() or "Zero claims" in content, (
        "ST3 must mention zero claims not traceable to source"
    )
    assert "fabricated" in content, (
        "ST3 must mention 'fabricated examples'"
    )


def test_st4_criterion_exists(content: str) -> None:
    assert "ST4" in content, "ST4 criterion must be present"
    assert "Framework-tone independence" in content, (
        "ST4 must reference 'Framework-tone independence'"
    )
    assert "separate axes" in content, "ST4 must mention 'separate axes'"


# Chain Success Criteria SC1–SC2

def test_sc1_criterion_exists(content: str) -> None:
    assert "SC1" in content, "SC1 criterion must be present"
    assert "without translation" in content, (
        "SC1 must mention passing without translation"
    )
    assert "narrative-chain recipe" in content, (
        "SC1 must mention 'narrative-chain recipe'"
    )


def test_sc2_criterion_exists(content: str) -> None:
    assert "SC2" in content, "SC2 criterion must be present"
    assert "Narrative beats document" in content, (
        "SC2 must reference 'Narrative beats document'"
    )
    assert "audience engagement" in content, (
        "SC2 must mention 'audience engagement'"
    )
    assert "qualitative signal" in content, (
        "SC2 must mention 'qualitative signal, human review'"
    )


# Qualitative Signals

def test_storyteller_qualitative_signals_want_to_hear(content: str) -> None:
    assert "I could actually send this to the board without editing" in content, (
        "Qualitative signals must include board-ready signal"
    )
    assert "It picked the three things that mattered and built a story around them" in content, (
        "Qualitative signals must include picking signal"
    )
    assert "The selection record showed me exactly what it left out and why" in content, (
        "Qualitative signals must include selection record signal"
    )
    assert "The story felt like a story, not a report with a dramatic opening" in content, (
        "Qualitative signals must include story-not-report signal"
    )


def test_storyteller_qualitative_signals_red_flags(content: str) -> None:
    assert "It just rewrote the analysis with better words" in content, (
        "Red flags must include 'rewrote the analysis' flag"
    )
    assert "I couldn't tell what it left out" in content, (
        "Red flags must include 'left out' flag"
    )
    assert "The story felt like a document in disguise" in content, (
        "Red flags must include 'document in disguise' flag"
    )
    assert "It added things that weren't in the source material" in content, (
        "Red flags must include 'added things' flag"
    )
