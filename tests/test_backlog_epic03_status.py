"""
Tests for task-12: BACKLOG.md updates reflecting Epic 03 in-progress status.
RED phase: These tests define the expected state AFTER the changes are applied.
They will fail until the changes are made.
"""

from pathlib import Path

BACKLOG_PATH = Path("docs/BACKLOG.md")


def read_backlog() -> str:
    return BACKLOG_PATH.read_text(encoding="utf-8")


def test_epic03_shows_in_progress_emoji():
    """Epic 03 should show 🔄 (in-progress), not 🆕 (new)."""
    content = read_backlog()
    assert "🔄 Epic 03 — Storyteller" in content, (
        "Expected '🔄 Epic 03 — Storyteller' but emoji is still 🆕 or missing"
    )
    assert "🆕 Epic 03 — Storyteller" not in content, (
        "Old '🆕 Epic 03 — Storyteller' still present; should be 🔄"
    )


def test_status_summary_shows_one_in_progress():
    """Status summary should say '1 in progress', not '0 in progress'."""
    content = read_backlog()
    assert "🔄 1 in progress" in content, (
        "Status summary should show '🔄 1 in progress'"
    )
    assert "🔄 0 in progress" not in content, "Old '🔄 0 in progress' still present"


def test_status_summary_shows_four_planned():
    """Status summary should say '4 planned', not '5 planned'."""
    content = read_backlog()
    lines = content.splitlines()
    summary_line = next(
        (line for line in lines if "epics tracked:" in line),
        None,
    )
    assert summary_line is not None, "Could not find status summary line"
    assert "4 planned" in summary_line, (
        f"Expected '4 planned' in summary line, got: {summary_line}"
    )
    assert "5 planned" not in summary_line, (
        f"Old '5 planned' still present in summary line: {summary_line}"
    )


def test_active_work_table_has_storyteller_row():
    """Active Work table should contain the Storyteller row."""
    content = read_backlog()
    active_section = content.split("### Active Work")[1].split(
        "### Recently Completed"
    )[0]
    assert "Storyteller specialist" in active_section, (
        "Storyteller specialist not found in Active Work table section"
    )
    assert "Cognitive mode translation" in content, (
        "Expected 'Cognitive mode translation' in Active Work table"
    )
    assert "No active work" not in content, (
        "'No active work' placeholder row should be removed"
    )


def test_storyteller_removed_from_immediate_next():
    """Storyteller should NOT appear in Immediate Next section."""
    content = read_backlog()
    immediate_next_section = content.split("### Immediate Next")[1].split(
        "### Near-term"
    )[0]
    assert "Storyteller specialist" not in immediate_next_section, (
        "Storyteller specialist row should be removed from Immediate Next section"
    )


def test_storyteller_removed_from_near_term():
    """Storyteller should NOT appear in Near-term section."""
    content = read_backlog()
    near_term_section = content.split("### Near-term")[1].split("### Medium-term")[0]
    assert "Storyteller specialist" not in near_term_section, (
        "Storyteller specialist row should be removed from Near-term section"
    )


def test_epic03_completion_status_shows_90_percent():
    """Epic 03 row in Completion Status table should show 90%."""
    content = read_backlog()
    lines = content.splitlines()
    epic03_row = next(
        (line for line in lines if "03 — Storyteller" in line and "|" in line),
        None,
    )
    assert epic03_row is not None, (
        "Could not find Epic 03 row in completion status table"
    )
    assert "90%" in epic03_row, f"Expected '90%' in Epic 03 row, got: {epic03_row}"
    # Check that standalone "| 0% |" is not present (not a substring check; "90%" contains "0%")
    assert "| 0% |" not in epic03_row, (
        f"Old '| 0% |' still present in Epic 03 row: {epic03_row}"
    )


def test_epic03_completion_status_has_implemented_content():
    """Epic 03 row should list implemented items."""
    content = read_backlog()
    lines = content.splitlines()
    epic03_row = next(
        (line for line in lines if "03 — Storyteller" in line and "|" in line),
        None,
    )
    assert epic03_row is not None, "Could not find Epic 03 row"
    assert "StoryOutput schema" in epic03_row, (
        f"Expected 'StoryOutput schema' in Epic 03 row, got: {epic03_row}"
    )
    assert "5-stage pipeline" in epic03_row, (
        f"Expected '5-stage pipeline' in Epic 03 row, got: {epic03_row}"
    )
    assert "NARRATIVE SELECTION" in epic03_row, (
        f"Expected 'NARRATIVE SELECTION' in Epic 03 row, got: {epic03_row}"
    )


def test_change_history_has_v1_9_entry():
    """Change History table should have a v1.9 entry at the top."""
    content = read_backlog()
    change_history_section = content.split("## Change History")[1]
    assert "v1.9" in change_history_section, "v1.9 entry not found in Change History"
    assert change_history_section.index("v1.9") < change_history_section.index(
        "v1.8"
    ), "v1.9 should appear before v1.8 in Change History (newest first)"


def test_change_history_v1_9_mentions_epic03():
    """v1.9 change history entry should mention Epic 03."""
    content = read_backlog()
    change_history_section = content.split("## Change History")[1]
    lines = change_history_section.splitlines()
    v19_line = next((line for line in lines if "v1.9" in line), None)
    assert v19_line is not None, "v1.9 line not found"
    assert "Epic 03" in v19_line or "Storyteller" in v19_line, (
        f"v1.9 entry should mention Epic 03 or Storyteller: {v19_line}"
    )
