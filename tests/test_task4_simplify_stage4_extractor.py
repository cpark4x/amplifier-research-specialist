"""Test that Stage 4 extractor has been simplified in agents/researcher.md.

Task-4: Remove the rigid format template from Stage 4, keep data quality rules.
The format template pre-committed the model to a specific output structure at
extraction time. Format is now owned by the formatter/synthesizer. Stage 4 should
focus on what to capture and data quality, not how to format it.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RESEARCHER_INDEX = REPO_ROOT / "agents" / "researcher.md"


def _read_content() -> str:
    return RESEARCHER_INDEX.read_text()


def _extract_stage4(content: str) -> str:
    """Extract the Stage 4 section (from its heading to the next ### heading)."""
    start = content.index("### Stage 4: Extractor")
    # Find the next ### heading after Stage 4
    next_heading = content.index("### Stage 5:", start + 1)
    return content[start:next_heading]


# --- Removed content tests ---


def test_no_format_enforcement_rules():
    """'Format enforcement rules' must not appear anywhere in the file."""
    content = _read_content()
    assert "Format enforcement rules" not in content, (
        "'Format enforcement rules' text still present in researcher/index.md"
    )


def test_no_rigid_format_template():
    """The rigid Claim:/Source:/Tier: template block must be gone from Stage 4."""
    stage4 = _extract_stage4(_read_content())
    # The old template had lines like "- Claim: [specific, falsifiable statement"
    # and "  Source: [URL]" as a code block template
    assert "- Claim: [specific, falsifiable" not in stage4, (
        "Rigid format template still present in Stage 4"
    )
    assert "Corroborated by: [count]" not in stage4, (
        "Corroborated by template line still present in Stage 4"
    )


def test_no_format_enforcement_bullets():
    """The three format enforcement bullet points must be gone from Stage 4."""
    stage4 = _extract_stage4(_read_content())
    assert "`Source` must be a full" not in stage4, (
        "Format enforcement bullet about Source still present"
    )
    assert "`Confidence` must be `high`" not in stage4, (
        "Format enforcement bullet about Confidence still present"
    )


def test_no_note_financial_figure_code_block():
    """The 'Note: financial figure' code block must be gone from Stage 4."""
    stage4 = _extract_stage4(_read_content())
    assert "Note: financial figure" not in stage4, (
        "'Note: financial figure' code block still present in Stage 4"
    )


def test_no_write_directly_in_findings_block():
    """The old 'write it directly in FINDINGS block format' instruction is gone."""
    stage4 = _extract_stage4(_read_content())
    assert "write it directly in FINDINGS block format" not in stage4, (
        "Old 'write directly in FINDINGS block format' instruction still present"
    )


# --- Retained content tests ---


def test_stage4_header_retained():
    """The Stage 4 header must still exist."""
    content = _read_content()
    assert "### Stage 4: Extractor" in content


def test_stage4_first_instruction_retained():
    """The first instruction line must be preserved."""
    stage4 = _extract_stage4(_read_content())
    assert (
        "From each successfully fetched source, extract discrete claims. One claim per finding."
        in stage4
    )


# --- New content tests ---


def test_for_each_claim_capture():
    """Stage 4 must contain the new 'For each claim, capture:' instruction."""
    stage4 = _extract_stage4(_read_content())
    assert "For each claim, capture:" in stage4


def test_capture_list_items():
    """Stage 4 must list the six items to capture."""
    stage4 = _extract_stage4(_read_content())
    assert "The specific, falsifiable claim (not a vague summary)" in stage4
    assert "The source URL (full `https://`" in stage4
    assert "The source tier (primary / secondary / tertiary)" in stage4
    assert "Your confidence assessment (high / medium / low)" in stage4
    assert "Whether it's a direct quote" in stage4
    assert "Publication date if known" in stage4


def test_data_quality_rules_heading():
    """Stage 4 must contain '**Data quality rules:**' heading."""
    stage4 = _extract_stage4(_read_content())
    assert "**Data quality rules:**" in stage4


def test_data_quality_url_rule():
    """The URL data quality rule must be present."""
    stage4 = _extract_stage4(_read_content())
    assert "cannot recover the source URL, that source is inaccessible" in stage4
    assert "log it in evidence gaps, do not extract claims from it" in stage4


def test_data_quality_financial_rule():
    """The financial claims data quality rule must be present."""
    stage4 = _extract_stage4(_read_content())
    assert "Numeric and financial claims" in stage4
    assert (
        "`low` confidence unless backed by a primary source or 2+ independent secondary sources"
        in stage4
    )


def test_do_not_synthesize():
    """The 'Do not synthesize' instruction must be present."""
    stage4 = _extract_stage4(_read_content())
    assert "Do not synthesize at this stage. Only extract." in stage4
