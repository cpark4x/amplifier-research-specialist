"""
TDD tests for docs/02-requirements/epics/03-storyteller.md
Validates the 8-section structure matches the Data Analyzer and Competitive Analysis epics.
Task: task-09
"""

from __future__ import annotations

from pathlib import Path

import pytest

EPIC_PATH = (
    Path(__file__).parent.parent
    / "docs"
    / "02-requirements"
    / "epics"
    / "03-storyteller.md"
)


@pytest.fixture(scope="module")
def content() -> str:
    assert EPIC_PATH.exists(), f"File not found: {EPIC_PATH}"
    return EPIC_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------


def test_file_exists():
    assert EPIC_PATH.exists(), "Epic file 03-storyteller.md must exist"


def test_header_title(content: str):
    assert "# Epic 03: Storyteller Specialist" in content


def test_header_status_in_progress(content: str):
    assert "**Status:** In Progress" in content


def test_header_owner(content: str):
    assert "**Owner:** Chris Park" in content


def test_header_contributors(content: str):
    assert "**Contributors:** Chris Park" in content


def test_header_last_updated(content: str):
    assert "**Last Updated:** 2026-03-04" in content


# ---------------------------------------------------------------------------
# Section 1: Summary
# ---------------------------------------------------------------------------


def test_section_1_summary_heading(content: str):
    assert "## 1. Summary" in content


def test_section_1_cognitive_mode_translation(content: str):
    assert "cognitive mode translation" in content.lower()


def test_section_1_narrative_selection_authorized(content: str):
    assert "narrative selection" in content.lower()


def test_section_1_mentions_researcher_data_analyzer_writer(content: str):
    assert "Researcher" in content
    assert "Data Analyzer" in content
    assert "Writer" in content


# ---------------------------------------------------------------------------
# Section 2: Problem
# ---------------------------------------------------------------------------


def test_section_2_problem_heading(content: str):
    assert "## 2. Problem" in content


def test_section_2_paradigmatic_mode(content: str):
    assert "paradigmatic" in content.lower()


def test_section_2_bruner_reference(content: str):
    assert "Bruner" in content


def test_section_2_two_failure_modes(content: str):
    # Should enumerate 2 problems without storyteller
    assert "1." in content
    assert "2." in content


# ---------------------------------------------------------------------------
# Section 3: Proposed Solution
# ---------------------------------------------------------------------------


def test_section_3_proposed_solution_heading(content: str):
    assert "## 3. Proposed Solution" in content


def test_section_3_pipeline_stages(content: str):
    # Must list the pipeline steps
    assert "Parse" in content
    assert "Draft" in content
    assert "Quality Gate" in content


def test_section_3_narrative_selection_record(content: str):
    assert "NARRATIVE SELECTION" in content


def test_section_3_returns_story_output(content: str):
    assert "StoryOutput" in content


def test_section_3_key_design_decisions(content: str):
    # Selective not faithful narrator
    assert "selective" in content.lower() or "Selective" in content
    # NARRATIVE SELECTION replaces inline citations
    assert (
        "inline citations" in content.lower()
        or "NARRATIVE SELECTION replaces" in content
    )
    # No CLAIMS TO VERIFY block
    assert "CLAIMS TO VERIFY" in content


# ---------------------------------------------------------------------------
# Section 4: User Stories
# ---------------------------------------------------------------------------


def test_section_4_user_stories_heading(content: str):
    assert "## 4. User Stories" in content


def test_section_4_implemented_subsection(content: str):
    assert "### Implemented" in content


def test_section_4_five_implemented_stories(content: str):
    # Stories 03-01 through 03-05 with relative links
    for i in range(1, 6):
        story_id = f"03-0{i}"
        assert story_id in content, f"Story {story_id} must be in the implemented table"


def test_section_4_story_relative_links(content: str):
    # Relative links should point to user-stories/03-storyteller/ directory
    assert "../user-stories/03-storyteller/03-01-" in content
    assert "../user-stories/03-storyteller/03-02-" in content
    assert "../user-stories/03-storyteller/03-03-" in content
    assert "../user-stories/03-storyteller/03-04-" in content
    assert "../user-stories/03-storyteller/03-05-" in content


def test_section_4_future_subsection(content: str):
    assert "### Future" in content


def test_section_4_future_compound_tones(content: str):
    assert "compound tones" in content.lower() or "Compound tones" in content


def test_section_4_future_structured_narrative_selection(content: str):
    assert (
        "structured NARRATIVE SELECTION" in content.lower()
        or "Structured NARRATIVE SELECTION" in content
    )


# ---------------------------------------------------------------------------
# Section 5: Outcomes
# ---------------------------------------------------------------------------


def test_section_5_outcomes_heading(content: str):
    assert "## 5. Outcomes" in content


def test_section_5_success_criteria_st1_st4(content: str):
    # ST1 through ST4 must appear
    for criteria in ["ST1", "ST2", "ST3", "ST4"]:
        assert criteria in content, f"Success criterion {criteria} must be in Outcomes"


def test_section_5_chain_criteria_sc1(content: str):
    assert "SC1" in content


def test_section_5_we_will_measure(content: str):
    assert "We'll Measure" in content or "We\u2019ll Measure" in content


def test_section_5_selection_record_measure(content: str):
    # Should mention INCLUDED + OMITTED = total findings
    assert "INCLUDED" in content and "OMITTED" in content


# ---------------------------------------------------------------------------
# Section 6: Dependencies
# ---------------------------------------------------------------------------


def test_section_6_dependencies_heading(content: str):
    assert "## 6. Dependencies" in content


def test_section_6_requires_amplifier_foundation(content: str):
    assert "Amplifier Foundation" in content


def test_section_6_enables_narrative_chain(content: str):
    assert "narrative-chain" in content.lower() or "narrative-chain.yaml" in content


def test_section_6_enables_researcher_chain(content: str):
    # The chain: Researcher → Formatter → Analyzer → Storyteller
    assert "Researcher" in content
    assert "Storyteller" in content


# ---------------------------------------------------------------------------
# Section 7: Open Questions
# ---------------------------------------------------------------------------


def test_section_7_open_questions_heading(content: str):
    assert "## 7. Open Questions" in content


def test_section_7_compound_tones_open(content: str):
    # Compound tones deferred to v2
    assert "compound tones" in content.lower() or "Compound tones" in content


def test_section_7_structured_narrative_selection_open(content: str):
    # Structured NARRATIVE SELECTION deferred to v2
    assert (
        "structured NARRATIVE SELECTION" in content.lower()
        or "Structured NARRATIVE SELECTION" in content
    )


def test_section_7_resolved_recipe_question(content: str):
    # New recipe vs mode flag — resolved 2026-03-04
    assert "2026-03-04" in content
    assert "new dedicated recipe" in content.lower() or "new recipe" in content.lower()


# ---------------------------------------------------------------------------
# Section 8: Change History
# ---------------------------------------------------------------------------


def test_section_8_change_history_heading(content: str):
    assert "## 8. Change History" in content


def test_section_8_v1_0_initial_entry(content: str):
    assert "v1.0" in content
    assert "2026-03-04" in content
    assert "Initial epic" in content
