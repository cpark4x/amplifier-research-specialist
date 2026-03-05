"""
TDD tests for specialists/storyteller/index.md
Validates all acceptance criteria from the spec (task-02).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

INDEX_PATH = Path(__file__).parent.parent / "specialists" / "storyteller" / "index.md"


@pytest.fixture(scope="module")
def content() -> str:
    assert INDEX_PATH.exists(), f"File not found: {INDEX_PATH}"
    return INDEX_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def frontmatter(content: str) -> str:
    """Extract raw YAML frontmatter between the opening --- delimiters."""
    m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    assert m, "No YAML frontmatter block found"
    return m.group(1)


# ---------------------------------------------------------------------------
# Acceptance criterion 1: YAML frontmatter has meta: (not bundle:)
# ---------------------------------------------------------------------------


def test_frontmatter_uses_meta_key(frontmatter: str) -> None:
    assert frontmatter.strip().startswith("meta:"), (
        "Frontmatter must start with 'meta:' key, not 'bundle:' or anything else"
    )


def test_frontmatter_has_no_bundle_key(frontmatter: str) -> None:
    lines = frontmatter.splitlines()
    top_level_keys = [
        line for line in lines if line and not line.startswith(" ") and ":" in line
    ]
    assert not any(line.startswith("bundle:") for line in top_level_keys), (
        "Frontmatter must NOT have a top-level 'bundle:' key"
    )


def test_frontmatter_meta_name_is_storyteller(frontmatter: str) -> None:
    assert "name: storyteller" in frontmatter, "meta.name must be 'storyteller'"


# ---------------------------------------------------------------------------
# Acceptance criterion 2: frontmatter description includes <example> block
# ---------------------------------------------------------------------------


def test_frontmatter_description_has_example_block(frontmatter: str) -> None:
    assert "<example>" in frontmatter, (
        "Frontmatter description must contain an <example> block"
    )
    assert "</example>" in frontmatter or "<commentary>" in frontmatter, (
        "Frontmatter <example> block must contain commentary"
    )


# ---------------------------------------------------------------------------
# Acceptance criterion 3: # Storyteller heading is present
# ---------------------------------------------------------------------------


def test_storyteller_heading_present(content: str) -> None:
    assert re.search(r"^# Storyteller", content, re.MULTILINE), (
        "Document must have a '# Storyteller' heading"
    )


# ---------------------------------------------------------------------------
# Acceptance criterion 4: persona paragraph is present
# ---------------------------------------------------------------------------


def test_persona_paragraph_present(content: str) -> None:
    assert "senior narrative strategist" in content, (
        "Persona must identify the agent as 'senior narrative strategist'"
    )
    assert "cognitive mode translation" in content.lower(), (
        "Persona must mention 'cognitive mode translation'"
    )


# ---------------------------------------------------------------------------
# Acceptance criterion 5: ## Core Principles has 4 principles
# ---------------------------------------------------------------------------


def test_core_principles_section_present(content: str) -> None:
    assert re.search(r"^## Core Principles", content, re.MULTILINE), (
        "Document must have '## Core Principles' section"
    )


def test_core_principles_has_four_items(content: str) -> None:
    # Extract Core Principles section up to the next ## heading
    m = re.search(r"## Core Principles\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    assert m, "Could not extract Core Principles section"
    section = m.group(1)
    # Bold markers (** ) or numbered items signal each principle
    principles = re.findall(r"\*\*[^*]+\*\*", section)
    assert len(principles) >= 4, (
        f"Core Principles must have 4 bold-titled principles, found {len(principles)}: {principles}"
    )


# ---------------------------------------------------------------------------
# Acceptance criterion 6: ## Pipeline has 5 stages
# ---------------------------------------------------------------------------


def test_pipeline_section_present(content: str) -> None:
    assert re.search(r"^## Pipeline", content, re.MULTILINE), (
        "Document must have '## Pipeline' section"
    )


def test_pipeline_stage_1_parse(content: str) -> None:
    assert re.search(r"Stage 1.*Parse", content, re.IGNORECASE), (
        "Pipeline must contain Stage 1: Parse"
    )


def test_pipeline_stage_2_find_the_drama(content: str) -> None:
    assert re.search(r"Stage 2.*Find the Drama", content, re.IGNORECASE), (
        "Pipeline must contain Stage 2: Find the Drama"
    )


def test_pipeline_stage_3_select_and_structure(content: str) -> None:
    assert re.search(r"Stage 3.*Select and Structure", content, re.IGNORECASE), (
        "Pipeline must contain Stage 3: Select and Structure"
    )


def test_pipeline_stage_4_draft(content: str) -> None:
    assert re.search(r"Stage 4.*Draft", content, re.IGNORECASE), (
        "Pipeline must contain Stage 4: Draft"
    )


def test_pipeline_stage_5_quality_gate(content: str) -> None:
    assert re.search(r"Stage 5.*Quality Gate", content, re.IGNORECASE), (
        "Pipeline must contain Stage 5: Quality Gate"
    )


# ---------------------------------------------------------------------------
# Acceptance criterion 7: framework selection with 3 axes in Stage 2
# ---------------------------------------------------------------------------


def test_stage_2_has_three_axes(content: str) -> None:
    assert "Axis 1" in content, "Stage 2 must describe Axis 1"
    assert "Axis 2" in content, "Stage 2 must describe Axis 2"
    assert "Axis 3" in content, "Stage 2 must describe Axis 3"


def test_stage_2_framework_and_tone_independent(content: str) -> None:
    assert "framework" in content.lower() and "tone" in content.lower(), (
        "Stage 2 must mention both framework and tone"
    )
    assert re.search(
        r"(independent|tone.*independent|framework.*tone)", content, re.IGNORECASE
    ), "Stage 2 must state that framework and tone are independent"


# ---------------------------------------------------------------------------
# Acceptance criterion 8: 7 transformation decisions in Stage 3
# ---------------------------------------------------------------------------


def test_stage_3_has_seven_transformation_decisions(content: str) -> None:
    # Extract Stage 3 section
    m = re.search(
        r"Stage 3.*?Select and Structure(.*?)(?=### Stage 4|\Z)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    assert m, "Could not extract Stage 3 section"
    section = m.group(1)
    # Count numbered decisions: lines starting with a digit followed by .
    decisions = re.findall(r"^\s*\(?[1-7]\)?[\.\)]\s+\S", section, re.MULTILINE)
    assert len(decisions) >= 7, (
        f"Stage 3 must have 7 transformation decisions, found {len(decisions)}"
    )


# ---------------------------------------------------------------------------
# Acceptance criterion 9: quality gate has 10 checklist items
# (6 structural + 3 craft + 1 auditability)
# ---------------------------------------------------------------------------


def test_stage_5_structural_checklist_has_six_items(content: str) -> None:
    m = re.search(
        r"Stage 5.*?Quality Gate(.*?)(?=## What You Do Not Do|\Z)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    assert m, "Could not extract Stage 5 section"
    section = m.group(1)
    assert re.search(r"structural", section, re.IGNORECASE), (
        "Stage 5 must have a structural checklist"
    )
    assert (
        re.search(r"6\s*(item|check|criteria)?", section, re.IGNORECASE)
        or len(
            re.findall(
                r"(?i)(dramatic question|protagonist|stakes|causal chain|peak moment|resolution)",
                section,
            )
        )
        >= 6
    ), "Structural checklist must reference 6 items"


def test_stage_5_craft_checklist_has_three_items(content: str) -> None:
    m = re.search(
        r"Stage 5.*?Quality Gate(.*?)(?=## What You Do Not Do|\Z)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    assert m, "Could not extract Stage 5 section"
    section = m.group(1)
    assert re.search(r"craft", section, re.IGNORECASE), (
        "Stage 5 must have a craft checklist"
    )
    assert re.search(
        r"3\s*(item|check|criteria)?", section, re.IGNORECASE
    ) or re.search(
        r"(concreteness|curse of knowledge|audience)", section, re.IGNORECASE
    ), "Craft checklist must reference 3 items"


def test_stage_5_auditability_checklist_has_one_item(content: str) -> None:
    m = re.search(
        r"Stage 5.*?Quality Gate(.*?)(?=## What You Do Not Do|\Z)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    assert m, "Could not extract Stage 5 section"
    section = m.group(1)
    assert re.search(r"auditability", section, re.IGNORECASE), (
        "Stage 5 must have an auditability checklist"
    )


# ---------------------------------------------------------------------------
# Acceptance criterion 10: output format section says bare text not code fences
# ---------------------------------------------------------------------------


def test_output_format_says_bare_text_not_code_fences(content: str) -> None:
    assert re.search(
        r"bare text",
        content,
        re.IGNORECASE,
    ), "Output format section must say 'bare text'"
    assert re.search(
        r"NOT wrapped in triple.backtick code fences",
        content,
        re.IGNORECASE,
    ), (
        "Output format section must explicitly say 'NOT wrapped in triple-backtick code fences'"
    )


# ---------------------------------------------------------------------------
# Acceptance criterion 11: full output block format present
# ---------------------------------------------------------------------------


def test_output_block_has_story_output_header(content: str) -> None:
    assert "STORY OUTPUT" in content, "Output block must have STORY OUTPUT header"


def test_output_block_has_narrative_selection(content: str) -> None:
    assert "NARRATIVE SELECTION" in content, (
        "Output block must have NARRATIVE SELECTION section"
    )


def test_output_block_has_included_findings(content: str) -> None:
    assert "INCLUDED FINDINGS" in content, (
        "Output block must have INCLUDED FINDINGS section"
    )


def test_output_block_has_omitted_findings(content: str) -> None:
    assert "OMITTED FINDINGS" in content, (
        "Output block must have OMITTED FINDINGS section"
    )


def test_output_block_has_quality_threshold_result(content: str) -> None:
    assert "QUALITY THRESHOLD RESULT" in content, (
        "Output block must have QUALITY THRESHOLD RESULT line"
    )


# ---------------------------------------------------------------------------
# Acceptance criterion 12: ## What You Do Not Do has 7 items
# ---------------------------------------------------------------------------


def test_what_you_do_not_do_section_present(content: str) -> None:
    assert re.search(r"^## What You Do Not Do", content, re.MULTILINE), (
        "Document must have '## What You Do Not Do' section"
    )


def test_what_you_do_not_do_has_seven_items(content: str) -> None:
    m = re.search(r"## What You Do Not Do\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    assert m, "Could not extract 'What You Do Not Do' section"
    section = m.group(1)
    # Count bullet list items (lines starting with -)
    items = re.findall(r"^\s*[-*]\s+\S", section, re.MULTILINE)
    assert len(items) >= 7, (
        f"'What You Do Not Do' must have 7 items, found {len(items)}"
    )
