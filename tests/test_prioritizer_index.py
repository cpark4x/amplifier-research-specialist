"""
Static tests for specialists/prioritizer/index.md
Validates that the Prioritizer specialist spec follows all required patterns.
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

import pytest

SPEC_FILE = Path(__file__).parent.parent / "agents" / "prioritizer.md"


@lru_cache(maxsize=None)
def content() -> str:
    assert SPEC_FILE.exists(), f"File not found: {SPEC_FILE}"
    return SPEC_FILE.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Frontmatter
# ---------------------------------------------------------------------------


def test_frontmatter_uses_meta_key() -> None:
    """1. File has YAML frontmatter with `meta:` key (not `bundle:`)."""
    m = re.match(r"^---\n(.*?)\n---", content(), re.DOTALL)
    assert m, "No YAML frontmatter found"
    frontmatter = m.group(1)
    assert frontmatter.strip().startswith("meta:"), (
        "Frontmatter must start with 'meta:' key, not 'bundle:' or anything else"
    )


def test_frontmatter_meta_name_is_prioritizer() -> None:
    """2. meta.name is `prioritizer`."""
    m = re.match(r"^---\n(.*?)\n---", content(), re.DOTALL)
    assert m, "No YAML frontmatter found"
    assert "name: prioritizer" in m.group(1), "meta.name must be 'prioritizer'"


def test_frontmatter_has_example_block() -> None:
    """3. Frontmatter has <example> block."""
    m = re.match(r"^---\n(.*?)\n---", content(), re.DOTALL)
    assert m, "No YAML frontmatter found"
    frontmatter = m.group(1)
    assert "<example>" in frontmatter, (
        "Frontmatter description must contain an <example> block"
    )


def test_frontmatter_description_mentions_prioritizer_output() -> None:
    """4. Frontmatter description mentions `PrioritizerOutput`."""
    m = re.match(r"^---\n(.*?)\n---", content(), re.DOTALL)
    assert m, "No YAML frontmatter found"
    assert "PrioritizerOutput" in m.group(1), (
        "Frontmatter description must mention 'PrioritizerOutput'"
    )


# ---------------------------------------------------------------------------
# Identity and framing
# ---------------------------------------------------------------------------


def test_identity_as_ranking_and_justification_stage() -> None:
    """5. Spec opens with identity-as-transformation-stage ('ranking and justification stage')."""
    assert "ranking and justification stage" in content(), (
        "Spec must identify the agent as 'ranking and justification stage'"
    )


def test_categorical_negation_you_do_not_research() -> None:
    """6. Categorical negation present ('You do not research')."""
    assert "You do not research" in content(), (
        "Spec must contain categorical negation 'You do not research'"
    )


def test_categorical_negation_you_do_not_write_documents() -> None:
    """7. 'You do not write documents' present."""
    assert "You do not write documents" in content(), (
        "Spec must contain 'You do not write documents'"
    )


# ---------------------------------------------------------------------------
# OUTPUT CONTRACT
# ---------------------------------------------------------------------------


def test_output_contract_blockquote_present() -> None:
    """8. OUTPUT CONTRACT blockquote present (starts with `> **OUTPUT CONTRACT`)."""
    assert re.search(r"> \*\*OUTPUT CONTRACT", content()), (
        "Spec must contain an OUTPUT CONTRACT blockquote"
    )


def test_output_contract_appears_before_stage_1() -> None:
    """9. OUTPUT CONTRACT appears before Stage 1."""
    c = content()
    assert "OUTPUT CONTRACT" in c, "OUTPUT CONTRACT must be present"
    assert "Stage 1" in c, "Stage 1 must be present"
    assert c.index("OUTPUT CONTRACT") < c.index("Stage 1"), (
        "OUTPUT CONTRACT must appear before Stage 1"
    )


def test_output_contract_mentions_parsed_as_first_output() -> None:
    """10. OUTPUT CONTRACT mentions `PRIORITY OUTPUT` as the required first output."""
    output_contract_block = content().split("OUTPUT CONTRACT")[1].split("---")[0]
    assert "PRIORITY OUTPUT" in output_contract_block, (
        "OUTPUT CONTRACT must mention 'PRIORITY OUTPUT' as the required first output"
    )


# ---------------------------------------------------------------------------
# Pipeline stages
# ---------------------------------------------------------------------------


def test_all_four_stages_present() -> None:
    """11. All 4 stages present: Stage 1 (Parse), Stage 2 (Score), Stage 3 (Rank), Stage 4 (Quality Gate)."""
    c = content()
    assert re.search(r"Stage 1.*Parse", c, re.IGNORECASE), (
        "Stage 1: Parse must be present"
    )
    assert re.search(r"Stage 2.*Score", c, re.IGNORECASE), (
        "Stage 2: Score must be present"
    )
    assert re.search(r"Stage 3.*Rank", c, re.IGNORECASE), (
        "Stage 3: Rank must be present"
    )
    assert re.search(r"Stage 4.*Quality Gate", c, re.IGNORECASE), (
        "Stage 4: Quality Gate must be present"
    )


def test_stages_appear_in_order() -> None:
    """12. Stages appear in order (Stage 1 before Stage 2 before Stage 3 before Stage 4)."""
    c = content()
    m1 = re.search(r"### Stage 1", c)
    m2 = re.search(r"### Stage 2", c)
    m3 = re.search(r"### Stage 3", c)
    m4 = re.search(r"### Stage 4", c)
    assert m1 and m2 and m3 and m4, "All 4 stage headings must be present"
    assert m1.start() < m2.start() < m3.start() < m4.start(), (
        "Stages must appear in order: Stage 1 < Stage 2 < Stage 3 < Stage 4"
    )


# ---------------------------------------------------------------------------
# Framework support
# ---------------------------------------------------------------------------


def test_moscow_framework_described() -> None:
    """13. MoSCoW framework described."""
    assert re.search(r"MoSCoW", content(), re.IGNORECASE), (
        "Spec must describe the MoSCoW prioritization framework"
    )


def test_impact_effort_framework_described() -> None:
    """14. Impact-effort framework described."""
    assert re.search(r"[Ii]mpact.{0,5}[Ee]ffort", content()), (
        "Spec must describe the impact-effort prioritization framework"
    )


def test_rice_framework_described() -> None:
    """15. RICE framework described."""
    assert "RICE" in content(), "Spec must describe the RICE prioritization framework"


def test_weighted_scoring_framework_described() -> None:
    """16. Weighted-scoring framework described."""
    assert re.search(r"[Ww]eighted.{0,10}[Ss]coring", content()), (
        "Spec must describe the weighted-scoring prioritization framework"
    )


# ---------------------------------------------------------------------------
# Output block
# ---------------------------------------------------------------------------


def test_prioritizer_output_block_present_in_stage_4() -> None:
    """17. PRIORITY OUTPUT block present in Stage 4."""
    c = content()
    stage4_section = c.split("### Stage 4")[1] if "### Stage 4" in c else ""
    assert "PRIORITY OUTPUT" in stage4_section, (
        "PRIORITY OUTPUT block must be present in Stage 4"
    )


def test_output_block_has_framework_rationale() -> None:
    """18. Framework rationale field present in output block."""
    c = content()
    # Use Stage 4 section to avoid matching prose references to "PRIORITY OUTPUT"
    stage4_section = c.split("### Stage 4")[1] if "### Stage 4" in c else ""
    assert "Framework rationale:" in stage4_section, (
        "PRIORITY OUTPUT block in Stage 4 must contain a 'Framework rationale:' field"
    )


def test_output_block_has_rankings_section() -> None:
    """19. RANKINGS section present in output block."""
    c = content()
    # Use Stage 4 section to avoid matching prose references to "PRIORITIZER OUTPUT"
    stage4_section = c.split("### Stage 4")[1] if "### Stage 4" in c else ""
    assert "RANKINGS" in stage4_section, (
        "PRIORITIZER OUTPUT block in Stage 4 must contain a RANKINGS section"
    )


def test_output_block_has_unrankable_items_section() -> None:
    """20. UNRANKABLE ITEMS section present in output block."""
    assert "UNRANKABLE ITEMS" in content(), (
        "PRIORITIZER OUTPUT block must contain an UNRANKABLE ITEMS section"
    )


def test_output_block_has_quality_threshold_result() -> None:
    """21. QUALITY THRESHOLD RESULT line present in output block."""
    assert "QUALITY THRESHOLD RESULT" in content(), (
        "PRIORITIZER OUTPUT block must contain a QUALITY THRESHOLD RESULT line"
    )


def test_output_block_emitted_in_stage_4_not_earlier() -> None:
    """22. Output block emitted in Stage 4 (not Stage 0 or Stage 1)."""
    c = content()
    stage4_start = c.find("### Stage 4")
    assert stage4_start != -1, "Stage 4 must be present"
    stage4_section = c[stage4_start:]
    # The full PRIORITY OUTPUT block (divider line + Goal: field) must appear within Stage 4.
    # Stage 0 emits only the stub; Stage 4 emits the complete block with Framework rationale.
    block_header_match = re.search(r"\nPRIORITY OUTPUT\n[━]+\nGoal:", stage4_section)
    assert block_header_match is not None, (
        "Full PRIORITY OUTPUT block (with divider and 'Goal:') must appear in Stage 4"
    )


# ---------------------------------------------------------------------------
# Core principles
# ---------------------------------------------------------------------------


def test_rationale_is_the_product_principle_present() -> None:
    """23. 'The rationale is the product' principle present."""
    assert "rationale is the product" in content().lower(), (
        "Core principles must include 'The rationale is the product'"
    )


def test_every_item_accounted_for_principle_present() -> None:
    """24. 'Every item accounted for' principle present."""
    assert re.search(r"[Ee]very item accounted for", content()), (
        "Core principles must include 'Every item accounted for'"
    )


def test_fails_loud_not_silent_principle_present() -> None:
    """25. 'Fails loud, not silent' principle present."""
    assert re.search(r"[Ff]ails loud, not silent", content()), (
        "Core principles must include 'Fails loud, not silent'"
    )


# ---------------------------------------------------------------------------
# Routing signal
# ---------------------------------------------------------------------------


def test_routing_signal_section_present() -> None:
    """26. Routing signal section present."""
    assert "## Routing Signal" in content(), (
        "Spec must contain a '## Routing Signal' section"
    )


def test_routing_signal_mentions_prioritizer_output() -> None:
    """27. Routing signal mentions PRIORITY OUTPUT."""
    c = content()
    routing_block = c.split("## Routing Signal")[1] if "## Routing Signal" in c else ""
    assert "PRIORITY OUTPUT" in routing_block, (
        "Routing signal section must mention PRIORITY OUTPUT"
    )


def test_routing_signal_mentions_writer_format_brief() -> None:
    """28. Routing signal mentions `writer (format=brief)` as natural next step."""
    assert "writer (format=brief)" in content(), (
        "Routing signal must mention 'writer (format=brief)' as natural next step"
    )


def test_routing_signal_says_orchestrator_routing_only() -> None:
    """29. Routing signal says 'orchestrator routing' only."""
    assert re.search(r"orchestrator routing", content(), re.IGNORECASE), (
        "Routing signal must state it is for 'orchestrator routing' only"
    )


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------


def test_prioritizer_registered_in_specialists_yaml() -> None:
    """30. `specialists:specialists/prioritizer` is in `behaviors/specialists.yaml`."""
    yaml_path = Path(__file__).parent.parent / "behaviors" / "specialists.yaml"
    assert yaml_path.exists(), f"behaviors/specialists.yaml not found: {yaml_path}"
    yaml_content = yaml_path.read_text(encoding="utf-8")
    assert "specialists:prioritizer" in yaml_content, (
        "'specialists:prioritizer' must be registered in behaviors/specialists.yaml"
    )
