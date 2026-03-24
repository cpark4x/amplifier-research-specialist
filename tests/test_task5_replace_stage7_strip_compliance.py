"""
Tests for Task 5: Replace Stage 7 and strip all compliance enforcement sections in agents/researcher.md.

Acceptance criteria (from spec):
- grep -c 'COMPLIANCE NOTE' returns 0
- grep -c 'FINAL SELF-CHECK' returns 0
- grep -c 'MOST COMMON MISTAKE' returns 0
- grep -c 'Stage 7: Synthesize and Return' returns 1
- grep -c 'Do not worry about exact output formatting' returns 1

Additional structural checks from spec:
- Section flow: Stage 6: Quality Gate → Stage 7: Synthesize and Return → --- → Routing Signal
- No remaining Wrong/Right example blocks
- New Stage 7 content is ~15 lines (compact)
"""

import re
from pathlib import Path

import pytest

RESEARCHER_PATH = Path(__file__).parent.parent / "agents" / "researcher.md"


@pytest.fixture
def content():
    return RESEARCHER_PATH.read_text()


# --- Acceptance criteria: things that must NOT be present ---


def test_no_compliance_note(content):
    """COMPLIANCE NOTE must be completely removed."""
    assert content.count("COMPLIANCE NOTE") == 0, (
        "Found 'COMPLIANCE NOTE' — should have been removed"
    )


def test_no_final_self_check(content):
    """FINAL SELF-CHECK must be completely removed."""
    assert content.count("FINAL SELF-CHECK") == 0, (
        "Found 'FINAL SELF-CHECK' — should have been removed"
    )


def test_no_most_common_mistake(content):
    """MOST COMMON MISTAKE must be completely removed."""
    assert content.count("MOST COMMON MISTAKE") == 0, (
        "Found 'MOST COMMON MISTAKE' — should have been removed"
    )


# --- Acceptance criteria: things that MUST be present ---


def test_new_stage7_heading_present(content):
    """New Stage 7 heading 'Stage 7: Synthesize and Return' must exist exactly once."""
    assert content.count("Stage 7: Synthesize and Return") == 1


def test_formatter_delegation_note_present(content):
    """The formatter delegation note must exist exactly once."""
    assert content.count("Do not worry about exact output formatting") == 1


# --- Structural checks from spec ---


def test_old_stage7_heading_gone(content):
    """Old 'Stage 7: Synthesizer' heading must be gone."""
    assert "Stage 7: Synthesizer" not in content


def test_no_wrong_right_examples(content):
    """No 'Wrong —' or 'Right —' example blocks should remain."""
    assert re.search(r"\*\*Wrong\s*—", content) is None, (
        "Found 'Wrong —' example block — should have been removed"
    )
    assert re.search(r"\*\*Right\s*—", content) is None, (
        "Found 'Right —' example block — should have been removed"
    )


def test_no_research_output_template_block(content):
    """The old RESEARCH OUTPUT template block (the rigid format spec) should be gone."""
    # The phrase "RESEARCH OUTPUT" may appear in the Routing Signal as a reference.
    # What must NOT exist is the old rigid template: "RESEARCH BRIEF:", "RESEARCH EVENTS:", etc.
    # These three fields are chosen because they only appeared inside the old Stage 7
    # template block — they are unambiguous markers of the rigid format that was removed.
    # "RESEARCH BRIEF:" is intentionally excluded since the new Stage 7 references
    # "research brief" conceptually (lowercase, in prose) and it could appear elsewhere.
    assert "RESEARCH EVENTS:" not in content, (
        "Found 'RESEARCH EVENTS:' — old template block should have been removed"
    )
    assert "QUALITY THRESHOLD RESULT:" not in content, (
        "Found 'QUALITY THRESHOLD RESULT:' — old template block should have been removed"
    )
    assert "QUALITY SCORE RATIONALE:" not in content, (
        "Found 'QUALITY SCORE RATIONALE:' — old template block should have been removed"
    )


def test_section_flow_order(content):
    """Section flow must be: Stage 6 → Stage 7: Synthesize and Return → --- → Routing Signal."""
    pos_stage6 = content.find("### Stage 6: Quality Gate")
    pos_stage7 = content.find("### Stage 7: Synthesize and Return")
    pos_routing = content.find("## Routing Signal")

    assert pos_stage6 != -1, "Stage 6: Quality Gate not found"
    assert pos_stage7 != -1, "Stage 7: Synthesize and Return not found"
    assert pos_routing != -1, "Routing Signal not found"

    assert pos_stage6 < pos_stage7 < pos_routing, (
        f"Section order wrong: Stage 6 @ {pos_stage6}, Stage 7 @ {pos_stage7}, Routing @ {pos_routing}"
    )

    # Between Stage 7 and Routing Signal, there should be a --- separator
    between = content[pos_stage7:pos_routing]
    assert "\n---\n" in between, (
        "Missing --- separator between Stage 7 and Routing Signal"
    )


def test_new_stage7_content_is_compact(content):
    """New Stage 7 section should be roughly 15 lines, not the old ~135 lines."""
    pos_stage7 = content.find("### Stage 7: Synthesize and Return")
    # Find next --- separator or next ### heading
    rest = content[pos_stage7:]
    next_sep = rest.find("\n---\n")
    stage7_section = rest[:next_sep] if next_sep != -1 else rest
    lines = stage7_section.strip().split("\n")
    assert len(lines) <= 25, (
        f"Stage 7 section is {len(lines)} lines — expected ~15, max 25"
    )
    assert len(lines) >= 10, f"Stage 7 section is {len(lines)} lines — seems too short"
