"""
Task 7: Verify researcher refactoring — grep checks, file length, and content integrity.

Acceptance criteria:
- All grep checks for removed content return 0 matches.
- All grep checks for kept content return >= 1 match.
- File length is approximately 240–260 lines (hard fail if >300 or <200).
- (Live researcher test is run separately via delegation.)
"""

from __future__ import annotations

from pathlib import Path

import pytest

RESEARCHER_PATH = (
    Path(__file__).parent.parent / "specialists" / "researcher" / "index.md"
)


@pytest.fixture(scope="module")
def content() -> str:
    """Read researcher/index.md once for the entire test module."""
    assert RESEARCHER_PATH.exists(), f"File not found: {RESEARCHER_PATH}"
    return RESEARCHER_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def line_count() -> int:
    """Count lines in researcher/index.md."""
    assert RESEARCHER_PATH.exists(), f"File not found: {RESEARCHER_PATH}"
    return len(RESEARCHER_PATH.read_text(encoding="utf-8").splitlines())


# ─── Step 1: Removed content must be absent ─────────────────────────────


class TestRemovedContent:
    """Strings that were removed during refactoring must not appear."""

    def test_no_output_contract(self, content: str) -> None:
        """'OUTPUT CONTRACT' must not appear anywhere."""
        assert "OUTPUT CONTRACT" not in content

    def test_no_stage_0(self, content: str) -> None:
        """'Stage 0' must not appear anywhere."""
        assert "Stage 0" not in content

    def test_no_compliance_note(self, content: str) -> None:
        """'COMPLIANCE NOTE' must not appear anywhere."""
        assert "COMPLIANCE NOTE" not in content

    def test_no_final_self_check(self, content: str) -> None:
        """'FINAL SELF-CHECK' must not appear anywhere."""
        assert "FINAL SELF-CHECK" not in content

    def test_no_most_common_mistake(self, content: str) -> None:
        """'MOST COMMON MISTAKE' must not appear anywhere."""
        assert "MOST COMMON MISTAKE" not in content

    def test_no_format_enforcement_rules(self, content: str) -> None:
        """'Format enforcement rules' must not appear anywhere."""
        assert "Format enforcement rules" not in content


# ─── Step 2: Kept content must be present ────────────────────────────────


class TestKeptContent:
    """Core pipeline stages and reference sections must still be present."""

    def test_stage_1_planner(self, content: str) -> None:
        assert "Stage 1: Planner" in content

    def test_stage_2_source_discoverer(self, content: str) -> None:
        assert "Stage 2: Source Discoverer" in content

    def test_stage_3_fetcher(self, content: str) -> None:
        assert "Stage 3: Fetcher" in content

    def test_stage_4_extractor(self, content: str) -> None:
        assert "Stage 4: Extractor" in content

    def test_stage_5_corroborator(self, content: str) -> None:
        assert "Stage 5: Corroborator" in content

    def test_stage_6_quality_gate(self, content: str) -> None:
        assert "Stage 6: Quality Gate" in content

    def test_stage_7_synthesize_and_return(self, content: str) -> None:
        assert "Stage 7: Synthesize and Return" in content

    def test_source_tiers(self, content: str) -> None:
        assert "Source Tiers" in content

    def test_confidence_levels(self, content: str) -> None:
        assert "Confidence Levels" in content

    def test_do_not_worry_about_formatting(self, content: str) -> None:
        """The new Stage 7 instruction about format delegation must be present."""
        assert "Do not worry about exact output formatting" in content


# ─── Step 3: File length ────────────────────────────────────────────────


class TestFileLength:
    """File should be ~240–260 lines. Hard fail if >300 or <200."""

    def test_not_too_long(self, line_count: int) -> None:
        """File must be under 300 lines (was 393 before refactoring)."""
        assert line_count < 300, (
            f"File is {line_count} lines — above 300. "
            f"Refactoring may not have removed enough content."
        )

    def test_not_too_short(self, line_count: int) -> None:
        """File must be at least 200 lines — core pipeline content must remain."""
        assert line_count >= 200, (
            f"File is {line_count} lines — below 200. "
            f"Too much content may have been removed."
        )

    def test_approximate_target(self, line_count: int) -> None:
        """File should be approximately 220–270 lines after refactoring.

        The spec targets 240–260, but the hard bounds are 200–300.
        We use a slightly wider band (220–270) to allow minor variation
        in the refactoring while still catching major drift.
        """
        assert 220 <= line_count <= 270, (
            f"File is {line_count} lines — outside the 220–270 target band. "
            f"Expected approximately 240–260 after refactoring."
        )


# ─── Step 4: Live test output criteria (checked programmatically) ───────
# The live researcher delegation is run outside pytest.
# These helpers validate the output when called from the agent.


def check_researcher_output(output: str) -> dict[str, bool]:
    """Evaluate researcher output against pass/fail criteria.

    Returns a dict of criterion -> pass/fail.
    Called by the agent after delegation, not by pytest.
    """
    return {
        "has_sources": "http" in output.lower(),
        "has_confidence": "confidence" in output.lower(),
        "has_evidence_gaps": "gap" in output.lower(),
        "no_final_self_check": "FINAL SELF-CHECK" not in output,
        "no_compliance_note": "COMPLIANCE NOTE" not in output,
    }
