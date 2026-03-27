"""Structural tests for agents/data-analyzer-formatter.md."""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DATA_ANALYZER_FORMATTER = REPO_ROOT / "agents" / "data-analyzer-formatter.md"
BEHAVIORS_YAML = REPO_ROOT / "behaviors" / "specialists.yaml"


def _load():
    assert DATA_ANALYZER_FORMATTER.exists(), f"Missing {DATA_ANALYZER_FORMATTER}"
    return DATA_ANALYZER_FORMATTER.read_text()


content = _load()


# --- Frontmatter ---

def test_frontmatter_has_meta_key():
    """Frontmatter must contain a meta: key."""
    assert "meta:" in content

def test_frontmatter_has_name():
    """meta.name must be 'data-analyzer-formatter'."""
    fm = re.search(r"---\n(.*?)\n---", content, re.DOTALL)
    assert fm, "No YAML frontmatter found"
    assert "name: data-analyzer-formatter" in fm.group(1)

def test_frontmatter_has_model_role():
    """DA formatter should declare model_role: coding."""
    fm = re.search(r"---\n(.*?)\n---", content, re.DOTALL)
    assert fm, "No YAML frontmatter found"
    assert "model_role: coding" in fm.group(1)


# --- Document structure ---

def test_has_heading():
    """Must have a # Data Analyzer Formatter heading."""
    assert "# Data Analyzer Formatter" in content

def test_has_core_principle():
    """Must have a Core Principle section."""
    assert "## Core Principle" in content

def test_core_principle_extract_not_generate():
    """Core principle must state extract, don't generate."""
    assert "Extract, don't generate" in content


# --- Pipeline stages ---

def test_has_stage_0():
    """Must have Stage 0: Open your response."""
    assert "### Stage 0" in content

def test_stage_0_analysis_output_header():
    """Stage 0 must specify ANALYSIS OUTPUT as literal first output."""
    assert "ANALYSIS OUTPUT" in content

def test_has_stage_1():
    """Must have Stage 1: Parse inputs."""
    assert "### Stage 1" in content

def test_has_stage_2():
    """Must have Stage 2: Extract inferences."""
    assert "### Stage 2" in content

def test_has_stage_3():
    """Must have Stage 3: Produce canonical ANALYSIS OUTPUT block."""
    assert "### Stage 3" in content

def test_stages_in_order():
    """Stages must appear in order: 0, 1, 2, 3."""
    positions = []
    for stage in ["### Stage 0", "### Stage 1", "### Stage 2", "### Stage 3"]:
        pos = content.find(stage)
        assert pos >= 0, f"{stage} not found"
        positions.append(pos)
    assert positions == sorted(positions), "Stages are not in order"


# --- Format detection ---

def test_detects_canonical_format():
    """Must describe canonical format detection."""
    stage1 = re.search(r"### Stage 1.*?(?=### Stage 2)", content, re.DOTALL)
    assert stage1, "Stage 1 not found"
    assert "canonical" in stage1.group(0).lower()

def test_detects_partial_format():
    """Must describe partial format detection."""
    stage1 = re.search(r"### Stage 1.*?(?=### Stage 2)", content, re.DOTALL)
    assert stage1, "Stage 1 not found"
    assert "partial" in stage1.group(0).lower()

def test_detects_narrative_format():
    """Must describe narrative format detection."""
    stage1 = re.search(r"### Stage 1.*?(?=### Stage 2)", content, re.DOTALL)
    assert stage1, "Stage 1 not found"
    assert "narrative" in stage1.group(0).lower()


# --- Output block structure ---

def test_output_has_findings():
    """Output block must contain FINDINGS section."""
    assert "FINDINGS" in content

def test_output_has_inferences():
    """Output block must contain INFERENCES section."""
    assert "INFERENCES" in content

def test_output_has_unused_findings():
    """Output block must contain UNUSED FINDINGS section."""
    assert "UNUSED FINDINGS" in content

def test_output_has_evidence_gaps():
    """Output block must contain EVIDENCE GAPS section."""
    assert "EVIDENCE GAPS" in content

def test_output_has_quality_threshold():
    """Output block must contain QUALITY THRESHOLD RESULT."""
    assert "QUALITY THRESHOLD RESULT" in content

def test_output_has_parsed_line():
    """Output must include a Parsed: summary line."""
    assert "Parsed:" in content


# --- Inference handling ---

def test_inference_types():
    """Must support inference types: pattern, causal, evaluative, predictive."""
    for itype in ["pattern", "causal", "evaluative", "predictive"]:
        assert itype in content, f"Missing inference type: {itype}"

def test_traces_to_field():
    """Must reference traces_to for inference provenance."""
    assert "traces_to" in content


# --- Stage narration stripping ---

def test_stage_narration_stripping():
    """Must handle stage narration prefix leaks from DA."""
    assert "narration" in content.lower() or "Stage 1: Parse" in content


# --- What You Do Not Do ---

def test_has_what_you_do_not_do():
    """Must have a What You Do Not Do section."""
    assert "## What You Do Not Do" in content

def test_does_not_reanalyze():
    """Must state it does not re-analyze findings."""
    lower = content.lower()
    assert "re-analyze" in lower or "reanalyze" in lower

def test_does_not_draw_inferences():
    """Must state it does not draw new inferences."""
    assert re.search(r"[Dd]raw new inferences", content)


# --- Routing signal ---

def test_has_routing_signal():
    """Must have a Routing Signal section for orchestrator."""
    assert "## Routing Signal" in content


# --- Registration ---

def test_registered_in_behaviors():
    """specialists:data-analyzer-formatter must be registered in behaviors/specialists.yaml."""
    behaviors = BEHAVIORS_YAML.read_text()
    assert "specialists:data-analyzer-formatter" in behaviors
