"""
TDD tests for specialists/storyteller/README.md
Validates all acceptance criteria from the spec (task-03).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

README_PATH = Path(__file__).parent.parent / "specialists" / "storyteller" / "README.md"


@pytest.fixture(scope="module")
def content() -> str:
    assert README_PATH.exists(), f"File not found: {README_PATH}"
    return README_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Acceptance criterion: one-line description is present
# ---------------------------------------------------------------------------


def test_opening_paragraph_mentions_cognitive_mode_translation(content: str) -> None:
    assert "cognitive mode translation" in content, (
        "Opening paragraph must mention 'cognitive mode translation'"
    )


def test_opening_paragraph_mentions_paradigmatic_and_narrative(content: str) -> None:
    assert "paradigmatic" in content.lower(), (
        "Opening paragraph must mention 'paradigmatic' mode artifacts"
    )
    assert "narrative" in content.lower(), (
        "Opening paragraph must mention 'narrative' mode artifacts"
    )


def test_opening_paragraph_mentions_dramatic_arc(content: str) -> None:
    assert "dramatic arc" in content.lower() or "dramatic" in content.lower(), (
        "Opening paragraph must mention dramatic arc"
    )


def test_opening_paragraph_mentions_narrative_selection(content: str) -> None:
    assert (
        "narrative selection" in content.lower() or "NARRATIVE SELECTION" in content
    ), "Opening paragraph must mention narrative selection decisions"


def test_opening_paragraph_mentions_authorized_for_selection(content: str) -> None:
    assert "authorized" in content.lower(), (
        "Opening paragraph must say Storyteller is the only specialist authorized to make narrative selection decisions"
    )


# ---------------------------------------------------------------------------
# Acceptance criterion: ## Interface Contract section exists
# ---------------------------------------------------------------------------


def test_interface_contract_section_present(content: str) -> None:
    assert re.search(r"^## Interface Contract", content, re.MULTILINE), (
        "Document must have '## Interface Contract' section"
    )


# ---------------------------------------------------------------------------
# Acceptance criterion: ### Accepts table has source/audience/tone
# ---------------------------------------------------------------------------


def test_accepts_subsection_present(content: str) -> None:
    assert re.search(r"^### Accepts", content, re.MULTILINE), (
        "Interface Contract must have '### Accepts' subsection"
    )


def test_accepts_table_has_source_required(content: str) -> None:
    assert re.search(r"`source`.*Yes", content), (
        "Accepts table must list 'source' as Required"
    )


def test_accepts_table_has_audience_optional(content: str) -> None:
    assert re.search(r"`audience`.*No", content), (
        "Accepts table must list 'audience' as optional (No)"
    )


def test_accepts_table_has_tone_optional(content: str) -> None:
    assert re.search(r"`tone`.*No", content), (
        "Accepts table must list 'tone' as optional (No)"
    )


def test_accepts_lists_analysis_output_input_type(content: str) -> None:
    assert "analysis-output" in content, (
        "Accepts section must list 'analysis-output' as an accepted input type"
    )


def test_accepts_lists_research_output_input_type(content: str) -> None:
    assert "research-output" in content, (
        "Accepts section must list 'research-output' as an accepted input type"
    )


def test_accepts_lists_competitive_analysis_output_input_type(content: str) -> None:
    assert "competitive-analysis-output" in content, (
        "Accepts section must list 'competitive-analysis-output' as an accepted input type"
    )


def test_accepts_lists_document_input_type(content: str) -> None:
    assert "document" in content, (
        "Accepts section must list 'document' as an accepted input type"
    )


# ---------------------------------------------------------------------------
# Acceptance criterion: ### Returns references StoryOutput from types.md
# ---------------------------------------------------------------------------


def test_returns_subsection_present(content: str) -> None:
    assert re.search(r"^### Returns", content, re.MULTILINE), (
        "Interface Contract must have '### Returns' subsection"
    )


def test_returns_references_story_output(content: str) -> None:
    assert "StoryOutput" in content, "Returns section must reference 'StoryOutput'"


def test_returns_references_types_md(content: str) -> None:
    assert "shared/interface/types.md" in content, (
        "Returns section must reference 'shared/interface/types.md'"
    )


def test_returns_shows_output_header_block(content: str) -> None:
    assert "STORY OUTPUT" in content, (
        "Returns section must show the output header block with 'STORY OUTPUT'"
    )


def test_returns_mentions_narrative_selection_section(content: str) -> None:
    assert "NARRATIVE SELECTION" in content, (
        "Returns section must mention NARRATIVE SELECTION as a key section"
    )


def test_returns_mentions_dramatic_question(content: str) -> None:
    assert "dramatic question" in content.lower(), (
        "Returns section must mention 'dramatic question' in NARRATIVE SELECTION"
    )


def test_returns_mentions_protagonist(content: str) -> None:
    assert "protagonist" in content.lower(), (
        "Returns section must mention 'protagonist' in NARRATIVE SELECTION"
    )


def test_returns_mentions_nothing_silently_dropped(content: str) -> None:
    assert re.search(r"silent", content, re.IGNORECASE), (
        "Returns section must note that nothing is silently dropped"
    )


def test_returns_mentions_quality_threshold_result(content: str) -> None:
    assert "QUALITY THRESHOLD RESULT" in content, (
        "Returns section must mention QUALITY THRESHOLD RESULT"
    )


def test_returns_mentions_met_and_not_met(content: str) -> None:
    assert "MET" in content and "NOT MET" in content, (
        "Returns section must mention both 'MET' and 'NOT MET' for quality threshold"
    )


# ---------------------------------------------------------------------------
# Acceptance criterion: ### Can Do lists exactly 6 capabilities
# ---------------------------------------------------------------------------


def test_can_do_subsection_present(content: str) -> None:
    assert re.search(r"^### Can Do", content, re.MULTILINE), (
        "Interface Contract must have '### Can Do' subsection"
    )


def test_can_do_has_six_items(content: str) -> None:
    m = re.search(r"### Can Do\n(.*?)(?=\n### |\n## |\Z)", content, re.DOTALL)
    assert m, "Could not extract 'Can Do' section"
    section = m.group(1)
    items = re.findall(r"^\s*[-*]\s+\S", section, re.MULTILINE)
    assert len(items) == 6, f"'Can Do' must have exactly 6 items, found {len(items)}"


# ---------------------------------------------------------------------------
# Acceptance criterion: ### Cannot Do lists exactly 6 boundaries
# ---------------------------------------------------------------------------


def test_cannot_do_subsection_present(content: str) -> None:
    assert re.search(r"^### Cannot Do", content, re.MULTILINE), (
        "Interface Contract must have '### Cannot Do' subsection"
    )


def test_cannot_do_has_six_items(content: str) -> None:
    m = re.search(r"### Cannot Do\n(.*?)(?=\n### |\n## |\Z)", content, re.DOTALL)
    assert m, "Could not extract 'Cannot Do' section"
    section = m.group(1)
    items = re.findall(r"^\s*[-*]\s+\S", section, re.MULTILINE)
    assert len(items) == 6, f"'Cannot Do' must have exactly 6 items, found {len(items)}"


# ---------------------------------------------------------------------------
# Acceptance criterion: ## Design Notes section present with required topics
# ---------------------------------------------------------------------------


def test_design_notes_section_present(content: str) -> None:
    assert re.search(r"^## Design Notes", content, re.MULTILINE), (
        "Document must have '## Design Notes' section"
    )


def test_design_notes_covers_writer_storyteller_distinction(content: str) -> None:
    m = re.search(r"## Design Notes\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    assert m, "Could not extract Design Notes section"
    section = m.group(1)
    assert re.search(
        r"(writer|storyteller).*(distinction|different|authorization)",
        section,
        re.IGNORECASE,
    ) or re.search(r"(authorization|authoriz)", section, re.IGNORECASE), (
        "Design Notes must cover Writer/Storyteller distinction (different authorizations)"
    )


def test_design_notes_covers_framework_tone_independence(content: str) -> None:
    m = re.search(r"## Design Notes\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    assert m, "Could not extract Design Notes section"
    section = m.group(1)
    assert re.search(
        r"framework.*tone.*independent|tone.*framework.*independent",
        section,
        re.IGNORECASE,
    ) or re.search(
        r"(structure|framework).*(register|tone).*independent", section, re.IGNORECASE
    ), (
        "Design Notes must cover framework/tone independence (framework=structure, tone=register)"
    )


def test_design_notes_narrative_selection_replaces_citations(content: str) -> None:
    m = re.search(r"## Design Notes\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    assert m, "Could not extract Design Notes section"
    section = m.group(1)
    assert "citation" in section.lower(), (
        "Design Notes must explain that NARRATIVE SELECTION replaces inline citations"
    )
    assert re.search(
        r"(narrative transportation|Green.*Brock|Slovic|transportation)",
        section,
        re.IGNORECASE,
    ), (
        "Design Notes must reference narrative transportation theory (Green & Brock 2000 and/or Slovic 2007)"
    )


def test_design_notes_no_claims_to_verify(content: str) -> None:
    m = re.search(r"## Design Notes\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    assert m, "Could not extract Design Notes section"
    section = m.group(1)
    assert "CLAIMS TO VERIFY" in section, (
        "Design Notes must mention that there is no CLAIMS TO VERIFY block (unlike Writer)"
    )


def test_design_notes_no_tools_required(content: str) -> None:
    m = re.search(r"## Design Notes\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    assert m, "Could not extract Design Notes section"
    section = m.group(1)
    assert re.search(
        r"no tools|tools.*(required|needed|none)", section, re.IGNORECASE
    ), "Design Notes must state that no tools are required"


# ---------------------------------------------------------------------------
# Acceptance criterion: ## Downstream section present with chain info
# ---------------------------------------------------------------------------


def test_downstream_section_present(content: str) -> None:
    assert re.search(r"^## Downstream", content, re.MULTILINE), (
        "Document must have '## Downstream' section"
    )


def test_downstream_describes_typical_chain(content: str) -> None:
    m = re.search(r"## Downstream\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    assert m, "Could not extract Downstream section"
    section = m.group(1)
    assert "Researcher" in section and "Storyteller" in section, (
        "Downstream must describe the typical chain including Researcher and Storyteller"
    )


def test_downstream_storyteller_is_last_step(content: str) -> None:
    m = re.search(r"## Downstream\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    assert m, "Could not extract Downstream section"
    section = m.group(1)
    assert re.search(r"last", section, re.IGNORECASE), (
        "Downstream must state that Storyteller is typically the last step"
    )
