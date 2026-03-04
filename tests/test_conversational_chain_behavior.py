"""
TDD tests for task-1: Add Conversational Chain Behavior Rules to Routing Brain.
Validates that the new ## Conversational Chain Behavior section is inserted
between the intro paragraph and ## Available Specialists in
context/specialists-instructions.md.
"""

from __future__ import annotations

from pathlib import Path

INSTRUCTIONS_PATH = Path(__file__).parent.parent / "context" / "specialists-instructions.md"


def load_content() -> str:
    assert INSTRUCTIONS_PATH.exists(), f"File not found: {INSTRUCTIONS_PATH}"
    return INSTRUCTIONS_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Section presence
# ---------------------------------------------------------------------------


def test_conversational_chain_behavior_section_present() -> None:
    """## Conversational Chain Behavior section must exist in the file."""
    content = load_content()
    assert "## Conversational Chain Behavior" in content, (
        "File must contain a '## Conversational Chain Behavior' section"
    )


# ---------------------------------------------------------------------------
# Section placement: after intro, before ## Available Specialists
# ---------------------------------------------------------------------------


def test_section_appears_after_intro_paragraph() -> None:
    """Conversational Chain Behavior section must appear after the intro paragraph."""
    content = load_content()
    intro_pos = content.find(
        "Delegate to these agents when quality and trustworthiness matter more than speed."
    )
    section_pos = content.find("## Conversational Chain Behavior")
    assert intro_pos != -1, "Intro paragraph must exist"
    assert section_pos != -1, "Conversational Chain Behavior section must exist"
    assert section_pos > intro_pos, (
        "## Conversational Chain Behavior must appear after the intro paragraph"
    )


def test_section_appears_before_available_specialists() -> None:
    """Conversational Chain Behavior section must appear before ## Available Specialists."""
    content = load_content()
    section_pos = content.find("## Conversational Chain Behavior")
    available_pos = content.find("## Available Specialists")
    assert section_pos != -1, "Conversational Chain Behavior section must exist"
    assert available_pos != -1, "## Available Specialists must exist"
    assert section_pos < available_pos, (
        "## Conversational Chain Behavior must appear before ## Available Specialists"
    )


# ---------------------------------------------------------------------------
# Rule 1 — Chain Completion Default
# ---------------------------------------------------------------------------


def test_rule_1_chain_completion_default_present() -> None:
    """Rule 1 (Chain Completion Default) must be present in the section."""
    content = load_content()
    assert "Chain Completion Default" in content, (
        "Rule 1 'Chain Completion Default' must appear in the Conversational Chain Behavior section"
    )


def test_rule_1_mentions_writer() -> None:
    """Rule 1 must mention completing through to the writer."""
    content = load_content()
    section_start = content.find("## Conversational Chain Behavior")
    section_end = content.find("## Available Specialists")
    assert section_start != -1 and section_end != -1
    section = content[section_start:section_end]
    assert "writer" in section.lower(), (
        "Rule 1 must mention completing through to the writer"
    )


def test_rule_1_mentions_brief_output_format() -> None:
    """Rule 1 must mention default output format = brief."""
    content = load_content()
    section_start = content.find("## Conversational Chain Behavior")
    section_end = content.find("## Available Specialists")
    section = content[section_start:section_end]
    assert "brief" in section.lower(), (
        "Rule 1 must mention default output format = brief"
    )


# ---------------------------------------------------------------------------
# Rule 2 — Per-Step Narration
# ---------------------------------------------------------------------------


def test_rule_2_per_step_narration_present() -> None:
    """Rule 2 (Per-Step Narration) must be present."""
    content = load_content()
    assert "Per-Step Narration" in content, (
        "Rule 2 'Per-Step Narration' must appear in the Conversational Chain Behavior section"
    )


def test_rule_2_contains_running_researcher_announcement() -> None:
    """Rule 2 must include the 'Running researcher' announcement."""
    content = load_content()
    section_start = content.find("## Conversational Chain Behavior")
    section_end = content.find("## Available Specialists")
    section = content[section_start:section_end]
    assert "Running researcher" in section, (
        "Rule 2 must include '🔍 Running researcher...' announcement"
    )


def test_rule_2_contains_researcher_complete_announcement() -> None:
    """Rule 2 must include the 'Researcher complete' announcement."""
    content = load_content()
    section_start = content.find("## Conversational Chain Behavior")
    section_end = content.find("## Available Specialists")
    section = content[section_start:section_end]
    assert "Researcher complete" in section, (
        "Rule 2 must include '✅ Researcher complete — passing to writer...' announcement"
    )


def test_rule_2_contains_done_final_announcement() -> None:
    """Rule 2 must include the final 'Done' announcement."""
    content = load_content()
    section_start = content.find("## Conversational Chain Behavior")
    section_end = content.find("## Available Specialists")
    section = content[section_start:section_end]
    assert "Done" in section, (
        "Rule 2 must include '✍️ Done. Here's your brief.' final announcement"
    )


# ---------------------------------------------------------------------------
# Rule 3 — Escape Hatch
# ---------------------------------------------------------------------------


def test_rule_3_escape_hatch_present() -> None:
    """Rule 3 (Escape Hatch) must be present."""
    content = load_content()
    assert "Escape Hatch" in content, (
        "Rule 3 'Escape Hatch' must appear in the Conversational Chain Behavior section"
    )


def test_rule_3_mentions_raw_output_trigger() -> None:
    """Rule 3 must include 'raw output' as a trigger phrase."""
    content = load_content()
    section_start = content.find("## Conversational Chain Behavior")
    section_end = content.find("## Available Specialists")
    section = content[section_start:section_end]
    assert "raw output" in section.lower(), (
        "Rule 3 must mention 'raw output' as an escape hatch trigger"
    )


def test_rule_3_mentions_dont_write_a_document_trigger() -> None:
    """Rule 3 must include 'don't write a document' as a trigger phrase."""
    content = load_content()
    section_start = content.find("## Conversational Chain Behavior")
    section_end = content.find("## Available Specialists")
    section = content[section_start:section_end]
    assert "don't write a document" in section.lower() or "don\u2019t write a document" in section.lower(), (
        "Rule 3 must mention \"don't write a document\" as an escape hatch trigger"
    )


def test_rule_3_says_stop_at_that_specialist() -> None:
    """Rule 3 must instruct stopping at that specialist and surfacing the block."""
    content = load_content()
    section_start = content.find("## Conversational Chain Behavior")
    section_end = content.find("## Available Specialists")
    section = content[section_start:section_end]
    assert "structured block" in section.lower(), (
        "Rule 3 must mention surfacing the structured block directly"
    )


# ---------------------------------------------------------------------------
# Rule 4 — Analysis Signal
# ---------------------------------------------------------------------------


def test_rule_4_analysis_signal_present() -> None:
    """Rule 4 (Analysis Signal) must be present."""
    content = load_content()
    assert "Analysis Signal" in content, (
        "Rule 4 'Analysis Signal' must appear in the Conversational Chain Behavior section"
    )


def test_rule_4_mentions_data_analyzer_in_chain() -> None:
    """Rule 4 must include data-analyzer in the chain."""
    content = load_content()
    section_start = content.find("## Conversational Chain Behavior")
    section_end = content.find("## Available Specialists")
    section = content[section_start:section_end]
    assert "data-analyzer" in section, (
        "Rule 4 must chain through data-analyzer"
    )


def test_rule_4_chain_is_researcher_analyzer_writer() -> None:
    """Rule 4 must specify the chain: researcher → data-analyzer → writer."""
    content = load_content()
    section_start = content.find("## Conversational Chain Behavior")
    section_end = content.find("## Available Specialists")
    section = content[section_start:section_end]
    researcher_pos = section.find("researcher")
    analyzer_pos = section.find("data-analyzer")
    writer_pos = section.rfind("writer")
    assert researcher_pos < analyzer_pos < writer_pos, (
        "Rule 4 chain must be: researcher → data-analyzer → writer (in order)"
    )


def test_rule_4_triggers_on_analysis_keyword() -> None:
    """Rule 4 must trigger on 'analysis' or 'insights' keywords."""
    content = load_content()
    section_start = content.find("## Conversational Chain Behavior")
    section_end = content.find("## Available Specialists")
    section = content[section_start:section_end]
    assert "analysis" in section.lower(), (
        "Rule 4 must be triggered by 'analysis' keyword"
    )
    assert "insights" in section.lower(), (
        "Rule 4 must be triggered by 'insights' keyword"
    )
