# Quality Evaluation Harness Implementation Plan (Phase 1)

> **Execution:** Use the subagent-driven-development workflow to implement this plan.

**Goal:** Build an automated competitive evaluation harness that runs the research-chain pipeline alongside 3 competitor tools on the same research questions, compares outputs head-to-head, and produces a structured gap report with scores.

**Architecture:** A two-recipe composition. `quality-eval.yaml` (main orchestrator) loads topics and iterates through them sequentially. For each topic, it invokes `quality-eval-iteration.yaml` (sub-recipe), which runs the specialists research-chain pipeline, runs 3 competitors in parallel via `foreach` with `parallel: 3`, then delegates to an evaluator agent that compares all outputs and produces a structured gap list. After all topics complete, the main recipe delegates to an aggregator agent that triangulates cross-topic results — gaps in 2+/3 topics are structural, gaps in 1/3 are topic noise — and produces a final gap report.

**Tech Stack:** Amplifier recipe YAML, Python (pytest), YAML config files

**Design document:** `docs/plans/2026-03-19-quality-loop-design.md`

**Deferred to Phase 2:** `while_condition` convergence loop, fix step + revert-on-regression, scoring criteria evolution/persistence, dev-machine-bundle integration.

---

## File Overview

| Action | File | Purpose |
|--------|------|---------|
| Create | `tests/test_competitors_config.py` | Tests for competitor config schema |
| Create | `specs/evaluation/competitors.yaml` | 3 competitor definitions (Anthropic, Gemini, OpenAI) |
| Modify | `tests/test_eval_harness.py` | Add assertions for competitive eval topics |
| Modify | `specs/evaluation/test-topics.yaml` | Add 3 competitive eval topics |
| Create | `tests/test_quality_eval_iteration_recipe.py` | Tests for iteration sub-recipe structure |
| Create | `recipes/quality-eval-iteration.yaml` | Sub-recipe: one topic (pipeline + parallel competitors + evaluate) |
| Create | `tests/test_quality_eval_recipe.py` | Tests for main orchestrator recipe structure |
| Create | `recipes/quality-eval.yaml` | Main recipe: load topics, iterate, aggregate, report |

---

## Design Notes

**Model routing for competitors.** The recipe includes `provider_preferences` on the competitor step to route each competitor to its configured model provider. If the recipe engine does not support `provider_preferences` on agent steps, all 3 competitors will run on the default model. This still provides useful signal (3 independent research runs surface output variance) but loses multi-model triangulation. Verify after Task 3 by inspecting recipe execution logs.

**Pipeline output capture.** The `run-pipeline` step invokes `research-chain.yaml` as a sub-recipe, which saves its output to `docs/research-output/`. A subsequent bash step reads the most recently saved file. This works because topics run sequentially (not in parallel), so the latest file is always the one just created.

**Evaluator agent.** The evaluator is `agent: "self"` (same pattern as critic steps in `eval-harness.yaml`). It is NOT a new specialist agent.

---

### Task 1: Competitor Configuration

**Files:**
- Create: `tests/test_competitors_config.py`
- Create: `specs/evaluation/competitors.yaml`

**Step 1: Write the failing test**

Create `tests/test_competitors_config.py` with the following complete content:

```python
"""Validation tests for specs/evaluation/competitors.yaml schema.

Tests the competitor configuration used by the quality-eval recipe to run
competitive benchmarks against the specialists research pipeline.
"""
from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent


class TestCompetitorsConfig:
    """Validates specs/evaluation/competitors.yaml."""

    def _config_path(self) -> Path:
        return REPO_ROOT / "specs" / "evaluation" / "competitors.yaml"

    def setup_method(self) -> None:
        path = self._config_path()
        assert path.exists(), f"competitors.yaml not found at {path}"
        self.data = yaml.safe_load(path.read_text(encoding="utf-8"))

    def test_file_exists(self) -> None:
        """specs/evaluation/competitors.yaml must exist."""
        assert self._config_path().exists(), (
            f"competitors.yaml not found at {self._config_path()}"
        )

    def test_has_competitors_key(self) -> None:
        """Top-level 'competitors' key exists and is a list."""
        assert "competitors" in self.data, (
            "competitors.yaml must have a 'competitors' key"
        )
        assert isinstance(self.data["competitors"], list), (
            "'competitors' must be a list"
        )

    def test_minimum_competitor_count(self) -> None:
        """At least 3 competitors defined."""
        assert len(self.data["competitors"]) >= 3, (
            f"Expected at least 3 competitors, got {len(self.data['competitors'])}"
        )

    def test_competitor_required_fields(self) -> None:
        """Every competitor has: name, agent, provider, model."""
        required_fields = {"name", "agent", "provider", "model"}
        for comp in self.data["competitors"]:
            missing = required_fields - set(comp.keys())
            assert not missing, (
                f"Competitor '{comp.get('name', '<unknown>')}' missing fields: {missing}"
            )

    def test_competitor_names_unique(self) -> None:
        """No duplicate competitor names."""
        names = [c["name"] for c in self.data["competitors"]]
        assert len(names) == len(set(names)), (
            f"Duplicate competitor names: "
            f"{[n for n in names if names.count(n) > 1]}"
        )

    def test_competitor_agents_are_web_research(self) -> None:
        """All competitors use foundation:web-research agent."""
        for comp in self.data["competitors"]:
            assert comp["agent"] == "foundation:web-research", (
                f"Competitor '{comp['name']}' must use 'foundation:web-research', "
                f"got '{comp['agent']}'"
            )

    def test_competitor_providers_are_valid(self) -> None:
        """Competitor providers must be anthropic, google, or openai."""
        valid_providers = {"anthropic", "google", "openai"}
        for comp in self.data["competitors"]:
            assert comp["provider"] in valid_providers, (
                f"Competitor '{comp['name']}' has invalid provider "
                f"'{comp['provider']}'. Must be one of: {valid_providers}"
            )

    def test_all_three_providers_represented(self) -> None:
        """Must have at least one competitor per provider (triangulation)."""
        providers = {c["provider"] for c in self.data["competitors"]}
        required = {"anthropic", "google", "openai"}
        missing = required - providers
        assert not missing, (
            f"Missing provider coverage for triangulation: {missing}"
        )
```

**Step 2: Run test to verify it fails**

Run: `cd /Users/chrispark/Projects/specialists/canvas-specialists && python -m pytest tests/test_competitors_config.py -v`

Expected: FAIL — every test errors with `AssertionError: competitors.yaml not found` because the file does not exist yet.

**Step 3: Write minimal implementation**

Create `specs/evaluation/competitors.yaml` with the following complete content:

```yaml
# =============================================================================
# Competitor Configuration for Quality Evaluation Harness
# =============================================================================
#
# Defines competitor tools that the quality-eval recipe benchmarks against.
# Each competitor runs foundation:web-research with a different model provider.
# Same tools, same question, no specialist pipeline — the baseline for
# "what does a generic research agent produce?"
#
# Three providers give triangulation: if all three beat the pipeline on the
# same dimension, it's a real gap. If only one does, it's model-specific noise.
#
# Used by: recipes/quality-eval-iteration.yaml
# =============================================================================

competitors:
  - name: "anthropic-claude"
    agent: "foundation:web-research"
    provider: "anthropic"
    model: "claude-sonnet-4-5-*"
    description: >
      Generic research agent with Anthropic Claude. Best-in-class model
      for reasoning and instruction following.

  - name: "google-gemini"
    agent: "foundation:web-research"
    provider: "google"
    model: "gemini-2.5-pro"
    description: >
      Generic research agent with Google Gemini. Different model strengths,
      particularly strong on factual recall and multimodal understanding.

  - name: "openai-gpt4o"
    agent: "foundation:web-research"
    provider: "openai"
    model: "gpt-4o"
    description: >
      Generic research agent with OpenAI GPT-4o. Third perspective for
      triangulation across different model architectures.
```

**Step 4: Run test to verify it passes**

Run: `cd /Users/chrispark/Projects/specialists/canvas-specialists && python -m pytest tests/test_competitors_config.py -v`

Expected: All 8 tests PASS.

**Step 5: Commit**

```bash
cd /Users/chrispark/Projects/specialists/canvas-specialists && \
git add specs/evaluation/competitors.yaml tests/test_competitors_config.py && \
git commit -m "feat: add competitor configuration for quality eval harness"
```

---

### Task 2: Competitive Evaluation Topics

**Files:**
- Modify: `tests/test_eval_harness.py` (add 2 methods to `TestTestTopics` class)
- Modify: `specs/evaluation/test-topics.yaml` (append 3 new topics)

**Step 1: Write the failing test**

Open `tests/test_eval_harness.py`. Find the end of the `TestTestTopics` class — the last method is `test_expected_traits_are_lists` which ends around line 64. Add the following two methods **inside** the `TestTestTopics` class, **before** the `TestEvalHarnessRecipe` class begins:

```python
    def test_has_competitive_eval_topics(self) -> None:
        """Topics must include factual-deep-dive, strategy, and survey."""
        ids = [t["id"] for t in self.data["topics"]]
        required = {"factual-deep-dive", "strategy", "survey"}
        missing = required - set(ids)
        assert not missing, (
            f"Missing competitive eval topics: {missing}"
        )

    def test_competitive_eval_topics_have_profile(self) -> None:
        """Competitive eval topics must have profile: 'competitive-eval'."""
        comp_ids = {"factual-deep-dive", "strategy", "survey"}
        for topic in self.data["topics"]:
            if topic["id"] in comp_ids:
                assert topic.get("profile") == "competitive-eval", (
                    f"Topic '{topic['id']}' must have "
                    f"profile='competitive-eval', "
                    f"got '{topic.get('profile')}'"
                )
```

The exact edit: in `tests/test_eval_harness.py`, find this text:

```
            assert isinstance(topic["expected_traits"], list), (
                f"Topic '{topic.get('id')}' expected_traits must be a list, "
                f"got {type(topic['expected_traits']).__name__}"
            )


class TestEvalHarnessRecipe:
```

Replace it with:

```
            assert isinstance(topic["expected_traits"], list), (
                f"Topic '{topic.get('id')}' expected_traits must be a list, "
                f"got {type(topic['expected_traits']).__name__}"
            )

    def test_has_competitive_eval_topics(self) -> None:
        """Topics must include factual-deep-dive, strategy, and survey."""
        ids = [t["id"] for t in self.data["topics"]]
        required = {"factual-deep-dive", "strategy", "survey"}
        missing = required - set(ids)
        assert not missing, (
            f"Missing competitive eval topics: {missing}"
        )

    def test_competitive_eval_topics_have_profile(self) -> None:
        """Competitive eval topics must have profile: 'competitive-eval'."""
        comp_ids = {"factual-deep-dive", "strategy", "survey"}
        for topic in self.data["topics"]:
            if topic["id"] in comp_ids:
                assert topic.get("profile") == "competitive-eval", (
                    f"Topic '{topic['id']}' must have "
                    f"profile='competitive-eval', "
                    f"got '{topic.get('profile')}'"
                )


class TestEvalHarnessRecipe:
```

**Step 2: Run test to verify it fails**

Run: `cd /Users/chrispark/Projects/specialists/canvas-specialists && python -m pytest tests/test_eval_harness.py::TestTestTopics::test_has_competitive_eval_topics tests/test_eval_harness.py::TestTestTopics::test_competitive_eval_topics_have_profile -v`

Expected: FAIL — `test_has_competitive_eval_topics` fails with "Missing competitive eval topics: {'factual-deep-dive', 'strategy', 'survey'}" because the topics don't exist yet.

**Step 3: Write minimal implementation**

Open `specs/evaluation/test-topics.yaml`. Append the following 3 topics at the end of the `topics:` list (after the `comparison` topic that ends around line 72):

```yaml

  # =========================================================================
  # Competitive Evaluation Topics
  # =========================================================================
  # These topics are used by the quality-eval recipe to benchmark the
  # specialists pipeline against competitor research agents. Each has
  # profile: competitive-eval so the recipe can filter to just these.
  # =========================================================================

  - id: factual-deep-dive
    profile: competitive-eval
    query: "What is Jina AI and how does it compare to other embedding providers?"
    expected_traits:
      - high_confidence_findings
      - multiple_primary_sources
      - competitive_comparison
      - technical_depth
    purpose: >
      Competitive eval baseline — factual deep-dive with abundant sources.
      Tests source tiering, confidence calibration, and technical accuracy.
      High source availability means the pipeline should produce strong output.

  - id: strategy
    profile: competitive-eval
    query: "What are the best strategies for improving hybrid team productivity?"
    expected_traits:
      - evaluative_inferences
      - actionable_recommendations
      - multiple_perspectives
      - secondary_sources_dominant
    purpose: >
      Competitive eval — strategy request. Tests the data-analyzer chain's
      ability to produce genuine analytical lift and fact/inference separation.
      Stresses inference quality and actionable synthesis over raw sourcing.

  - id: survey
    profile: competitive-eval
    query: "What are the best places to retire abroad for US citizens?"
    expected_traits:
      - broad_coverage
      - comparison_matrix
      - multiple_entities
      - practical_details
    purpose: >
      Competitive eval — survey question. Tests breadth coverage and stresses
      the depth-optimized pipeline methodology on a topic that requires wide
      survey-style coverage rather than deep-dive analysis.
```

**Step 4: Run test to verify it passes**

Run: `cd /Users/chrispark/Projects/specialists/canvas-specialists && python -m pytest tests/test_eval_harness.py::TestTestTopics -v`

Expected: All 8 tests PASS (6 existing + 2 new). The existing tests still pass because: (a) topic count is now 8 ≥ 5, (b) all new topics have the required schema fields, (c) all new topic IDs are unique.

**Step 5: Commit**

```bash
cd /Users/chrispark/Projects/specialists/canvas-specialists && \
git add specs/evaluation/test-topics.yaml tests/test_eval_harness.py && \
git commit -m "feat: add 3 competitive eval topics to test topic bank"
```

---

### Task 3: Iteration Sub-Recipe

**Files:**
- Create: `tests/test_quality_eval_iteration_recipe.py`
- Create: `recipes/quality-eval-iteration.yaml`

**Step 1: Write the failing test**

Create `tests/test_quality_eval_iteration_recipe.py` with the following complete content:

```python
"""Validation tests for recipes/quality-eval-iteration.yaml structure.

Tests the sub-recipe that runs ONE topic through:
  1. Load competitors from config
  2. Run the specialists pipeline (research-chain)
  3. Capture pipeline output from disk
  4. Run 3 competitors in parallel
  5. Evaluate pipeline vs competitors — produce gap list
"""
from __future__ import annotations

from pathlib import Path

import yaml

RECIPE_PATH = Path(__file__).parent.parent / "recipes" / "quality-eval-iteration.yaml"


def load_recipe() -> dict:
    """Load and parse the recipe YAML."""
    assert RECIPE_PATH.exists(), f"Recipe not found: {RECIPE_PATH}"
    return yaml.safe_load(RECIPE_PATH.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# File existence and metadata
# ---------------------------------------------------------------------------


def test_recipe_file_exists() -> None:
    """recipes/quality-eval-iteration.yaml must exist."""
    assert RECIPE_PATH.exists(), (
        "recipes/quality-eval-iteration.yaml must exist"
    )


def test_recipe_name() -> None:
    """Recipe name must be 'quality-eval-iteration'."""
    recipe = load_recipe()
    assert recipe["name"] == "quality-eval-iteration", (
        f"Expected name='quality-eval-iteration', got {recipe.get('name')!r}"
    )


def test_recipe_has_required_fields() -> None:
    """Recipe has: name, description, version, steps, context."""
    recipe = load_recipe()
    required = {"name", "description", "version", "steps", "context"}
    missing = required - set(recipe.keys())
    assert not missing, f"Recipe missing required fields: {missing}"


def test_recipe_has_tags() -> None:
    """Recipe must have tags including 'evaluation' and 'competitive'."""
    recipe = load_recipe()
    tags = recipe.get("tags", [])
    for tag in ("evaluation", "competitive"):
        assert tag in tags, f"Tags must include '{tag}'"


# ---------------------------------------------------------------------------
# Context variables
# ---------------------------------------------------------------------------


def test_context_has_research_question() -> None:
    """Context must have 'research_question' (required, empty default)."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert "research_question" in context, (
        "Context must have 'research_question'"
    )


def test_context_has_topic_id() -> None:
    """Context must have 'topic_id' (required, empty default)."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert "topic_id" in context, "Context must have 'topic_id'"


# ---------------------------------------------------------------------------
# Steps — existence, uniqueness, outputs
# ---------------------------------------------------------------------------


def test_has_required_step_ids() -> None:
    """Step IDs must include the 5 core steps."""
    recipe = load_recipe()
    step_ids = [s["id"] for s in recipe["steps"]]
    required = {
        "load-competitors",
        "run-pipeline",
        "capture-pipeline-output",
        "run-competitors",
        "evaluate",
    }
    missing = required - set(step_ids)
    assert not missing, f"Recipe missing step IDs: {missing}"


def test_step_ids_unique() -> None:
    """No duplicate step IDs."""
    recipe = load_recipe()
    step_ids = [s["id"] for s in recipe["steps"]]
    assert len(step_ids) == len(set(step_ids)), (
        f"Duplicate step IDs: "
        f"{[s for s in step_ids if step_ids.count(s) > 1]}"
    )


def test_all_steps_have_output() -> None:
    """Every step declares an output variable."""
    recipe = load_recipe()
    for step in recipe["steps"]:
        assert "output" in step, (
            f"Step '{step.get('id', '<unknown>')}' is missing 'output'"
        )


# ---------------------------------------------------------------------------
# Step details — load-competitors
# ---------------------------------------------------------------------------


def test_load_competitors_is_bash() -> None:
    """load-competitors step must be type: bash."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "load-competitors")
    assert step.get("type") == "bash", (
        "load-competitors must be type: bash"
    )


def test_load_competitors_reads_yaml() -> None:
    """load-competitors command must read competitors.yaml."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "load-competitors")
    command = step.get("command", "")
    assert "competitors.yaml" in command, (
        "load-competitors must read from competitors.yaml"
    )


def test_load_competitors_has_parse_json() -> None:
    """load-competitors must have parse_json: true."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "load-competitors")
    assert step.get("parse_json") is True, (
        "load-competitors must have parse_json: true"
    )


# ---------------------------------------------------------------------------
# Step details — run-pipeline
# ---------------------------------------------------------------------------


def test_run_pipeline_is_recipe_type() -> None:
    """run-pipeline must invoke research-chain as a sub-recipe."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "run-pipeline")
    assert step.get("type") == "recipe", (
        "run-pipeline must be type: recipe"
    )
    assert "research-chain" in step.get("recipe", ""), (
        "run-pipeline must invoke research-chain.yaml"
    )


def test_run_pipeline_passes_research_question() -> None:
    """run-pipeline context must include research_question."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "run-pipeline")
    ctx = step.get("context", {})
    assert "research_question" in ctx, (
        "run-pipeline must pass research_question in context"
    )


# ---------------------------------------------------------------------------
# Step details — run-competitors
# ---------------------------------------------------------------------------


def test_run_competitors_has_foreach() -> None:
    """run-competitors must iterate over competitors with foreach."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "run-competitors")
    assert "foreach" in step, "run-competitors must have 'foreach'"


def test_run_competitors_has_parallel() -> None:
    """run-competitors must run in parallel."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "run-competitors")
    parallel = step.get("parallel")
    assert parallel is True or (isinstance(parallel, int) and parallel >= 3), (
        f"run-competitors must have parallel: true or parallel >= 3, got {parallel}"
    )


def test_run_competitors_has_collect() -> None:
    """run-competitors must collect results into a list."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "run-competitors")
    assert "collect" in step, "run-competitors must have 'collect'"
    assert step["collect"] == "competitor_results", (
        f"collect must be 'competitor_results', got '{step['collect']}'"
    )


def test_run_competitors_uses_web_research_agent() -> None:
    """run-competitors must use foundation:web-research agent."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "run-competitors")
    assert step.get("agent") == "foundation:web-research", (
        "run-competitors must use 'foundation:web-research' agent"
    )


def test_run_competitors_prompt_has_research_question() -> None:
    """run-competitors prompt must reference {{research_question}}."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "run-competitors")
    prompt = step.get("prompt", "")
    assert "{{research_question}}" in prompt, (
        "run-competitors prompt must reference {{research_question}}"
    )


# ---------------------------------------------------------------------------
# Step details — evaluate
# ---------------------------------------------------------------------------


def test_evaluate_references_pipeline_output() -> None:
    """evaluate prompt must reference {{pipeline_output}}."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "evaluate")
    prompt = step.get("prompt", "")
    assert "{{pipeline_output}}" in prompt, (
        "evaluate prompt must reference {{pipeline_output}}"
    )


def test_evaluate_references_competitor_results() -> None:
    """evaluate prompt must reference {{competitor_results}}."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "evaluate")
    prompt = step.get("prompt", "")
    assert "{{competitor_results}}" in prompt, (
        "evaluate prompt must reference {{competitor_results}}"
    )


def test_evaluate_references_topic_id() -> None:
    """evaluate prompt must reference {{topic_id}}."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "evaluate")
    prompt = step.get("prompt", "")
    assert "{{topic_id}}" in prompt, (
        "evaluate prompt must reference {{topic_id}}"
    )


# ---------------------------------------------------------------------------
# Step ordering
# ---------------------------------------------------------------------------


def test_load_competitors_before_run_competitors() -> None:
    """load-competitors must come before run-competitors."""
    recipe = load_recipe()
    step_ids = [s["id"] for s in recipe["steps"]]
    assert step_ids.index("load-competitors") < step_ids.index("run-competitors"), (
        "load-competitors must precede run-competitors"
    )


def test_pipeline_before_evaluate() -> None:
    """run-pipeline must come before evaluate."""
    recipe = load_recipe()
    step_ids = [s["id"] for s in recipe["steps"]]
    assert step_ids.index("run-pipeline") < step_ids.index("evaluate"), (
        "run-pipeline must precede evaluate"
    )


def test_competitors_before_evaluate() -> None:
    """run-competitors must come before evaluate."""
    recipe = load_recipe()
    step_ids = [s["id"] for s in recipe["steps"]]
    assert step_ids.index("run-competitors") < step_ids.index("evaluate"), (
        "run-competitors must precede evaluate"
    )


def test_capture_between_pipeline_and_evaluate() -> None:
    """capture-pipeline-output must be between run-pipeline and evaluate."""
    recipe = load_recipe()
    step_ids = [s["id"] for s in recipe["steps"]]
    pipe_idx = step_ids.index("run-pipeline")
    capture_idx = step_ids.index("capture-pipeline-output")
    eval_idx = step_ids.index("evaluate")
    assert pipe_idx < capture_idx < eval_idx, (
        "capture-pipeline-output must be between run-pipeline and evaluate"
    )
```

**Step 2: Run test to verify it fails**

Run: `cd /Users/chrispark/Projects/specialists/canvas-specialists && python -m pytest tests/test_quality_eval_iteration_recipe.py -v`

Expected: FAIL — `test_recipe_file_exists` fails with "recipes/quality-eval-iteration.yaml must exist". All other tests error in `load_recipe()` for the same reason.

**Step 3: Write minimal implementation**

Create `recipes/quality-eval-iteration.yaml` with the following complete content:

```yaml
# =============================================================================
# quality-eval-iteration: Competitive Evaluation for ONE Topic
# =============================================================================
#
# Runs the specialists research-chain pipeline on a single topic, runs 3
# competitor tools (foundation:web-research with different model providers)
# on the same topic in parallel, then compares all outputs head-to-head.
#
# Produces a structured gap list: dimensions where the pipeline loses to
# competitors, with severity, location (which specialist), and proposed fix.
#
# This is a sub-recipe — invoked by quality-eval.yaml for each topic.
# Not intended to be run standalone (though it can be for debugging).
#
# Usage (standalone debug):
#   recipe execute recipes/quality-eval-iteration.yaml \
#     --context '{"research_question": "What is Jina AI...", "topic_id": "factual-deep-dive"}'
#
# =============================================================================

name: "quality-eval-iteration"
description: "Competitive evaluation for one topic — pipeline + parallel competitors + head-to-head comparison"
version: "1.0.0"
tags: ["evaluation", "competitive", "quality", "iteration"]

context:
  research_question: ""    # Required: the topic query
  topic_id: ""             # Required: stable topic ID for tracking

steps:
  # ===========================================================================
  # LOAD COMPETITOR CONFIGURATION
  # ===========================================================================
  - id: "load-competitors"
    type: "bash"
    command: |
      python3 -c "
      import json, yaml
      with open('specs/evaluation/competitors.yaml') as f:
          data = yaml.safe_load(f)
      print(json.dumps(data['competitors']))
      "
    output: "competitors"
    parse_json: true
    timeout: 10

  # ===========================================================================
  # RUN SPECIALISTS PIPELINE (research-chain)
  # ===========================================================================
  - id: "run-pipeline"
    type: "recipe"
    recipe: "recipes/research-chain.yaml"
    context:
      research_question: "{{research_question}}"
    output: "pipeline_run_result"
    timeout: 3600
    on_error: "continue"

  # ===========================================================================
  # CAPTURE PIPELINE OUTPUT FROM DISK
  # ===========================================================================
  #
  # The research-chain saves its final document to docs/research-output/.
  # We read it back so the evaluator can compare content, not file paths.
  # This works because topics run sequentially — the latest file is always
  # the one we just created.
  #
  # ===========================================================================
  - id: "capture-pipeline-output"
    type: "bash"
    command: |
      latest=$(ls -t docs/research-output/*.md 2>/dev/null | head -1)
      if [ -z "$latest" ]; then
        echo "PIPELINE_ERROR: No output file found in docs/research-output/. The research-chain pipeline may have failed. Topic: {{topic_id}}"
      else
        echo "=== Pipeline output from: $latest ==="
        cat "$latest"
      fi
    output: "pipeline_output"
    timeout: 30

  # ===========================================================================
  # RUN COMPETITORS IN PARALLEL
  # ===========================================================================
  #
  # Each competitor runs foundation:web-research on the same question.
  # provider_preferences routes each run to the configured model provider
  # for multi-model triangulation.
  #
  # DESIGN NOTE: If the recipe engine does not support provider_preferences
  # on agent steps, all 3 competitors will use the default model. This still
  # provides useful signal (3 independent runs) but loses model triangulation.
  #
  # ===========================================================================
  - id: "run-competitors"
    foreach: "{{competitors}}"
    as: "competitor"
    parallel: 3
    collect: "competitor_results"
    agent: "foundation:web-research"
    prompt: |
      Research the following question thoroughly. Produce a comprehensive
      research report with:
      - Key findings with source attribution and URLs
      - Confidence levels for each claim (high / medium / low)
      - Analysis and insights beyond surface-level summarization
      - Explicit acknowledgment of gaps or areas of uncertainty

      Research question: {{research_question}}

      Be thorough. This output will be evaluated for depth, accuracy, source
      quality, and analytical insight.
    output: "single_competitor_result"
    timeout: 2700
    on_error: "continue"

  # ===========================================================================
  # EVALUATE: COMPARE PIPELINE vs COMPETITORS
  # ===========================================================================
  - id: "evaluate"
    agent: "self"
    prompt: |
      You are a COMPARATIVE EVALUATOR. Your job: compare a structured research
      pipeline's output against generic competitor research tools and identify
      where the pipeline falls short.

      TOPIC: {{research_question}}
      TOPIC ID: {{topic_id}}

      === SPECIALISTS PIPELINE OUTPUT ===
      {{pipeline_output}}

      === COMPETITOR OUTPUTS ===
      The following are outputs from 3 generic research agents (each using a
      different model provider) given the same research question with no
      specialist pipeline:
      {{competitor_results}}

      EVALUATION PROTOCOL:

      1. READ all outputs carefully. The pipeline output is from a structured
         specialist pipeline (researcher → formatter → data-analyzer →
         writer → writer-formatter). The competitor outputs are from generic
         research agents with the same web search tools but no pipeline.

      2. SCORE each output on these 6 dimensions (1-10 scale):
         - Source quality: Authoritative sources? Primary > secondary > tertiary.
         - Factual depth: Thorough coverage? Important aspects addressed?
         - Analytical insight: Genuine analysis beyond summarization?
           Patterns identified? Actionable conclusions?
         - Confidence calibration: Claims hedged appropriately? Uncertainty
           and evidence gaps acknowledged honestly?
         - Structure & readability: Well-organized? Easy to navigate? Logical flow?
         - Citation quality: Sources cited with verifiable URLs? Claims traceable?

      3. For each dimension, identify the BEST output (pipeline or which competitor).

      4. For dimensions where the pipeline LOSES to any competitor, describe
         the specific gap.

      Return your evaluation in this EXACT format:

      COMPETITIVE EVALUATION REPORT
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      Topic: {{topic_id}}
      Research question: {{research_question}}

      DIMENSION SCORES:
      - Source quality:          Pipeline=X/10  Comp1=X/10  Comp2=X/10  Comp3=X/10  Best=[name]
      - Factual depth:           Pipeline=X/10  Comp1=X/10  Comp2=X/10  Comp3=X/10  Best=[name]
      - Analytical insight:      Pipeline=X/10  Comp1=X/10  Comp2=X/10  Comp3=X/10  Best=[name]
      - Confidence calibration:  Pipeline=X/10  Comp1=X/10  Comp2=X/10  Comp3=X/10  Best=[name]
      - Structure & readability: Pipeline=X/10  Comp1=X/10  Comp2=X/10  Comp3=X/10  Best=[name]
      - Citation quality:        Pipeline=X/10  Comp1=X/10  Comp2=X/10  Comp3=X/10  Best=[name]

      PIPELINE AGGREGATE: [average]/10
      BEST COMPETITOR: [name] at [average]/10

      GAP LIST:
      For each dimension where the pipeline scored LOWER than the best competitor:
      - dimension: "[name]"
        pipeline_score: X
        best_competitor_score: X
        best_competitor_name: "[name]"
        gap_description: "[What the competitor did better — be specific]"
        severity: "[critical|major|minor]"
        location: "[researcher|data-analyzer|writer|formatter|pipeline-design]"
        proposed_fix: "[Specific, actionable fix suggestion]"

      PIPELINE WINS:
      For each dimension where the pipeline scored HIGHER than all competitors:
      - dimension: "[name]"
        margin: "+X over [best competitor name]"
        why: "[What the pipeline does well here]"

      SUMMARY:
      [2-3 sentences: pipeline's key strengths, key weaknesses, and the single
      most impactful improvement that would close the largest gap.]

      Rules:
      - Score honestly. A pipeline that loses on 5/6 dimensions is useful data.
      - Be specific in gap descriptions. "Competitor had better sources" is useless.
        "Competitor cited 3 primary academic papers; pipeline had 0 primary sources
        and relied on blog posts" is actionable.
      - Location must name a specific pipeline stage, not just "the pipeline".
      - If the pipeline output starts with PIPELINE_ERROR, score it 0/10 on all
        dimensions and note the failure in the summary.
    output: "topic_evaluation"
    timeout: 1800
```

**Step 4: Run test to verify it passes**

Run: `cd /Users/chrispark/Projects/specialists/canvas-specialists && python -m pytest tests/test_quality_eval_iteration_recipe.py -v`

Expected: All tests PASS.

**Step 5: Commit**

```bash
cd /Users/chrispark/Projects/specialists/canvas-specialists && \
git add recipes/quality-eval-iteration.yaml tests/test_quality_eval_iteration_recipe.py && \
git commit -m "feat: add quality-eval-iteration sub-recipe for competitive evaluation"
```

---

### Task 4: Main Orchestrator Recipe

**Files:**
- Create: `tests/test_quality_eval_recipe.py`
- Create: `recipes/quality-eval.yaml`

**Step 1: Write the failing test**

Create `tests/test_quality_eval_recipe.py` with the following complete content:

```python
"""Validation tests for recipes/quality-eval.yaml structure.

Tests the main orchestrator recipe that:
  1. Loads competitive eval topics from test-topics.yaml
  2. Runs quality-eval-iteration for each topic sequentially
  3. Aggregates cross-topic results (structural gaps vs topic noise)
  4. Saves the final gap report
"""
from __future__ import annotations

from pathlib import Path

import yaml

RECIPE_PATH = Path(__file__).parent.parent / "recipes" / "quality-eval.yaml"


def load_recipe() -> dict:
    """Load and parse the recipe YAML."""
    assert RECIPE_PATH.exists(), f"Recipe not found: {RECIPE_PATH}"
    return yaml.safe_load(RECIPE_PATH.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# File existence and metadata
# ---------------------------------------------------------------------------


def test_recipe_file_exists() -> None:
    """recipes/quality-eval.yaml must exist."""
    assert RECIPE_PATH.exists(), "recipes/quality-eval.yaml must exist"


def test_recipe_name() -> None:
    """Recipe name must be 'quality-eval'."""
    recipe = load_recipe()
    assert recipe["name"] == "quality-eval", (
        f"Expected name='quality-eval', got {recipe.get('name')!r}"
    )


def test_recipe_has_required_fields() -> None:
    """Recipe has: name, description, version, steps, context."""
    recipe = load_recipe()
    required = {"name", "description", "version", "steps", "context"}
    missing = required - set(recipe.keys())
    assert not missing, f"Recipe missing required fields: {missing}"


def test_recipe_has_tags() -> None:
    """Recipe tags must include 'evaluation' and 'competitive'."""
    recipe = load_recipe()
    tags = recipe.get("tags", [])
    for tag in ("evaluation", "competitive"):
        assert tag in tags, f"Tags must include '{tag}'"


# ---------------------------------------------------------------------------
# Context variables
# ---------------------------------------------------------------------------


def test_context_has_evaluation_mode() -> None:
    """Context must have 'evaluation_mode' defaulting to 'competitive'."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert "evaluation_mode" in context, (
        "Context must have 'evaluation_mode'"
    )
    assert context["evaluation_mode"] == "competitive", (
        f"evaluation_mode must default to 'competitive', "
        f"got {context['evaluation_mode']!r}"
    )


def test_context_has_target_score() -> None:
    """Context must have 'target_score'."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert "target_score" in context, "Context must have 'target_score'"


# ---------------------------------------------------------------------------
# Steps — existence, uniqueness, outputs
# ---------------------------------------------------------------------------


def test_has_required_step_ids() -> None:
    """Step IDs must include the 4 core steps."""
    recipe = load_recipe()
    step_ids = [s["id"] for s in recipe["steps"]]
    required = {
        "load-topics",
        "run-topic-iterations",
        "aggregate-results",
        "save-gap-report",
    }
    missing = required - set(step_ids)
    assert not missing, f"Recipe missing step IDs: {missing}"


def test_step_ids_unique() -> None:
    """No duplicate step IDs."""
    recipe = load_recipe()
    step_ids = [s["id"] for s in recipe["steps"]]
    assert len(step_ids) == len(set(step_ids)), (
        f"Duplicate step IDs: "
        f"{[s for s in step_ids if step_ids.count(s) > 1]}"
    )


def test_all_steps_have_output() -> None:
    """Every step declares an output variable."""
    recipe = load_recipe()
    for step in recipe["steps"]:
        assert "output" in step, (
            f"Step '{step.get('id', '<unknown>')}' is missing 'output'"
        )


# ---------------------------------------------------------------------------
# Step details — load-topics
# ---------------------------------------------------------------------------


def test_load_topics_is_bash() -> None:
    """load-topics must be type: bash."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "load-topics")
    assert step.get("type") == "bash", "load-topics must be type: bash"


def test_load_topics_reads_test_topics_yaml() -> None:
    """load-topics must read from test-topics.yaml."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "load-topics")
    command = step.get("command", "")
    assert "test-topics.yaml" in command, (
        "load-topics must read from test-topics.yaml"
    )


def test_load_topics_filters_competitive_eval() -> None:
    """load-topics must filter to competitive-eval profile topics."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "load-topics")
    command = step.get("command", "")
    assert "competitive-eval" in command, (
        "load-topics must filter to competitive-eval profile"
    )


def test_load_topics_has_parse_json() -> None:
    """load-topics must have parse_json: true."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "load-topics")
    assert step.get("parse_json") is True, (
        "load-topics must have parse_json: true"
    )


# ---------------------------------------------------------------------------
# Step details — run-topic-iterations
# ---------------------------------------------------------------------------


def test_run_topic_iterations_has_foreach() -> None:
    """run-topic-iterations must iterate over topics with foreach."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "run-topic-iterations")
    assert "foreach" in step, "run-topic-iterations must have 'foreach'"


def test_run_topic_iterations_collects_results() -> None:
    """run-topic-iterations must collect results."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "run-topic-iterations")
    assert "collect" in step, "run-topic-iterations must have 'collect'"
    assert step["collect"] == "topic_results", (
        f"collect must be 'topic_results', got '{step['collect']}'"
    )


def test_run_topic_iterations_invokes_iteration_recipe() -> None:
    """run-topic-iterations must invoke quality-eval-iteration.yaml."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "run-topic-iterations")
    assert step.get("type") == "recipe", (
        "run-topic-iterations must be type: recipe"
    )
    assert "quality-eval-iteration" in step.get("recipe", ""), (
        "run-topic-iterations must invoke quality-eval-iteration.yaml"
    )


def test_run_topic_iterations_passes_context() -> None:
    """run-topic-iterations must pass research_question and topic_id."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "run-topic-iterations")
    ctx = step.get("context", {})
    assert "research_question" in ctx, (
        "Must pass research_question to iteration sub-recipe"
    )
    assert "topic_id" in ctx, (
        "Must pass topic_id to iteration sub-recipe"
    )


# ---------------------------------------------------------------------------
# Step details — aggregate-results
# ---------------------------------------------------------------------------


def test_aggregate_references_topic_results() -> None:
    """aggregate-results prompt must reference {{topic_results}}."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "aggregate-results")
    prompt = step.get("prompt", "")
    assert "{{topic_results}}" in prompt, (
        "aggregate-results prompt must reference {{topic_results}}"
    )


def test_aggregate_references_evaluation_mode() -> None:
    """aggregate-results prompt must reference {{evaluation_mode}}."""
    recipe = load_recipe()
    step = next(s for s in recipe["steps"] if s["id"] == "aggregate-results")
    prompt = step.get("prompt", "")
    assert "{{evaluation_mode}}" in prompt, (
        "aggregate-results prompt must reference {{evaluation_mode}}"
    )


# ---------------------------------------------------------------------------
# Step ordering
# ---------------------------------------------------------------------------


def test_load_topics_before_iterations() -> None:
    """load-topics must come before run-topic-iterations."""
    recipe = load_recipe()
    step_ids = [s["id"] for s in recipe["steps"]]
    assert step_ids.index("load-topics") < step_ids.index("run-topic-iterations"), (
        "load-topics must precede run-topic-iterations"
    )


def test_iterations_before_aggregate() -> None:
    """run-topic-iterations must come before aggregate-results."""
    recipe = load_recipe()
    step_ids = [s["id"] for s in recipe["steps"]]
    assert step_ids.index("run-topic-iterations") < step_ids.index("aggregate-results"), (
        "run-topic-iterations must precede aggregate-results"
    )


def test_aggregate_before_save() -> None:
    """aggregate-results must come before save-gap-report."""
    recipe = load_recipe()
    step_ids = [s["id"] for s in recipe["steps"]]
    assert step_ids.index("aggregate-results") < step_ids.index("save-gap-report"), (
        "aggregate-results must precede save-gap-report"
    )
```

**Step 2: Run test to verify it fails**

Run: `cd /Users/chrispark/Projects/specialists/canvas-specialists && python -m pytest tests/test_quality_eval_recipe.py -v`

Expected: FAIL — `test_recipe_file_exists` fails with "recipes/quality-eval.yaml must exist". All other tests error in `load_recipe()`.

**Step 3: Write minimal implementation**

Create `recipes/quality-eval.yaml` with the following complete content:

```yaml
# =============================================================================
# quality-eval: Competitive Evaluation Harness
# =============================================================================
#
# Runs the specialists research pipeline against competitor tools across
# multiple test topics, identifies where the pipeline falls short, and
# produces a structured gap report.
#
# Architecture:
#   1. Load competitive eval topics from test-topics.yaml
#   2. For each topic, invoke quality-eval-iteration.yaml (sequentially)
#      — each iteration runs pipeline + 3 competitors + head-to-head eval
#   3. Aggregate all per-topic evaluations
#      — gaps in 2+/3 topics = structural (fix these)
#      — gaps in 1/3 topics = topic noise (investigate later)
#   4. Save the final gap report
#
# Estimated runtime: ~45 min (3 topics × ~15 min each)
#
# Usage:
#   recipe execute recipes/quality-eval.yaml
#
#   With custom target score:
#     recipe execute recipes/quality-eval.yaml \
#       --context '{"target_score": 8.5}'
#
# Phase 2 will add: while_condition loop, fix step, revert-on-regression.
# =============================================================================

name: "quality-eval"
description: "Competitive evaluation harness — benchmark specialists pipeline against competitor research tools across multiple topics"
version: "1.0.0"
tags: ["evaluation", "competitive", "quality", "harness", "benchmarking"]

context:
  evaluation_mode: "competitive"   # competitive (vs competitors) or rubric (vs criteria)
  target_score: 8.0                # target aggregate score (used by Phase 2 loop)

steps:
  # ===========================================================================
  # LOAD COMPETITIVE EVAL TOPICS
  # ===========================================================================
  #
  # Reads test-topics.yaml and filters to topics with profile: competitive-eval.
  # This keeps the quality-eval decoupled from the adversarial eval topics.
  #
  # ===========================================================================
  - id: "load-topics"
    type: "bash"
    command: |
      python3 -c "
      import json, yaml
      with open('specs/evaluation/test-topics.yaml') as f:
          data = yaml.safe_load(f)
      topics = [t for t in data['topics'] if t.get('profile') == 'competitive-eval']
      if not topics:
          print(json.dumps([]))
          import sys
          print('WARNING: No topics with profile=competitive-eval found', file=sys.stderr)
      else:
          print(json.dumps(topics))
      "
    output: "topics"
    parse_json: true
    timeout: 10

  # ===========================================================================
  # RUN EVALUATION FOR EACH TOPIC (sequentially)
  # ===========================================================================
  #
  # Each iteration runs:
  #   1. Specialists pipeline (research-chain) on the topic
  #   2. 3 competitors in parallel on the same topic
  #   3. Head-to-head evaluation producing a gap list
  #
  # Topics run sequentially (not in parallel) so that:
  #   - Pipeline output capture is unambiguous (latest file = current topic)
  #   - The evaluator can learn from earlier topics
  #   - Resource usage stays reasonable (~4 concurrent agent calls per topic)
  #
  # ===========================================================================
  - id: "run-topic-iterations"
    foreach: "{{topics}}"
    as: "topic"
    collect: "topic_results"
    type: "recipe"
    recipe: "recipes/quality-eval-iteration.yaml"
    context:
      research_question: "{{topic.query}}"
      topic_id: "{{topic.id}}"
    output: "single_topic_result"
    timeout: 5400
    on_error: "continue"
    max_iterations: 10

  # ===========================================================================
  # AGGREGATE RESULTS ACROSS TOPICS
  # ===========================================================================
  #
  # Triangulate: gaps appearing in 2+/3 topics are structural (high priority).
  # Gaps in 1/3 are topic noise (investigate but don't prioritize).
  #
  # ===========================================================================
  - id: "aggregate-results"
    agent: "self"
    prompt: |
      You are a CROSS-TOPIC AGGREGATOR. Your job: synthesize competitive
      evaluation results across multiple topics to identify structural gaps
      vs. topic noise.

      EVALUATION MODE: {{evaluation_mode}}
      TARGET SCORE: {{target_score}}

      PER-TOPIC EVALUATIONS:
      {{topic_results}}

      AGGREGATION PROTOCOL:

      1. EXTRACT all gap lists from all topic evaluations.

      2. TRIANGULATE:
         - A gap that appears in 2+ out of N topics is STRUCTURAL.
           These are systematic pipeline weaknesses. Fix these first.
         - A gap that appears in only 1 topic is TOPIC NOISE.
           Might be topic-specific difficulty, not a pipeline problem.

      3. RANK structural gaps by impact:
         - critical: Pipeline produces fundamentally wrong or missing output
         - major: Significant quality loss visible to any reader
         - minor: Polish issue, noticeable but not damaging

      4. For each structural gap, synthesize proposed fixes from all topics
         into a single actionable recommendation.

      5. COMPUTE aggregate scores:
         - Pipeline average = mean of pipeline aggregate scores across topics
         - Best competitor average = mean of best competitor scores across topics
         - Delta = Pipeline average - Best competitor average
         - Score vs target: Pipeline average vs {{target_score}}

      Return your report in this EXACT format:

      QUALITY EVALUATION GAP REPORT
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      Evaluation mode: {{evaluation_mode}}
      Topics evaluated: [count]

      OVERALL SCORES:
      | Topic | Pipeline | Best Competitor | Competitor Name | Delta |
      |-------|----------|----------------|-----------------|-------|
      | [id]  | X.X/10   | X.X/10         | [name]          | +/-X.X |
      ...

      Pipeline average: X.X/10
      Best competitor average: X.X/10
      Overall delta: +/-X.X
      Target score: {{target_score}}/10
      Gap to target: X.X

      STRUCTURAL GAPS (appear in 2+/N topics — fix these first):
      1. [Gap title]
         - Severity: [critical|major|minor]
         - Dimension: [which evaluation dimension]
         - Appears in topics: [list of topic IDs]
         - Location: [which specialist or pipeline stage]
         - Evidence: [1 sentence from each topic showing the gap]
         - Recommended fix: [Specific, actionable change]

      2. ...

      TOPIC NOISE (appear in 1/N topics — investigate later):
      1. [Gap title]
         - Topic: [topic ID]
         - Dimension: [which evaluation dimension]
         - Details: [brief description]

      PIPELINE STRENGTHS (dimensions where pipeline consistently wins):
      1. [Strength title]
         - Dimensions: [list]
         - Consistent across: [topic IDs]
         - Why: [brief explanation]

      RECOMMENDED ACTIONS (prioritized, most impactful first):
      1. [Action] — addresses structural gap #N, expected impact: +X.X points
      2. [Action] — addresses structural gap #N, expected impact: +X.X points
      3. ...

      SUMMARY:
      [3-5 sentences: pipeline quality relative to competitors, key structural
      gaps, what to fix first, and whether the target score is achievable with
      the identified fixes.]

      Rules:
      - If any topic evaluation contains PIPELINE_ERROR, note it and exclude
        that topic from aggregate scores (but still report the failure).
      - Structural gaps must have specific fix recommendations, not generic
        advice like "improve quality."
      - Recommended actions must be ordered by expected impact on the
        aggregate score.
    output: "gap_report"
    timeout: 1800

  # ===========================================================================
  # SAVE GAP REPORT
  # ===========================================================================
  - id: "save-gap-report"
    agent: "foundation:file-ops"
    prompt: |
      Save the following quality evaluation gap report to disk.

      File path: specs/evaluation/reports/quality-eval-report.md
      Create the specs/evaluation/reports/ directory if it does not exist.

      Content to save:

      # Quality Evaluation Gap Report

      **Evaluation mode:** {{evaluation_mode}}
      **Target score:** {{target_score}}/10

      ---

      {{gap_report}}

      ---

      *Generated by recipes/quality-eval.yaml v1.0.0*

      Report the full file path you saved to.
    output: "report_path"
    timeout: 300
```

**Step 4: Run test to verify it passes**

Run: `cd /Users/chrispark/Projects/specialists/canvas-specialists && python -m pytest tests/test_quality_eval_recipe.py -v`

Expected: All tests PASS.

**Step 5: Commit**

```bash
cd /Users/chrispark/Projects/specialists/canvas-specialists && \
git add recipes/quality-eval.yaml tests/test_quality_eval_recipe.py && \
git commit -m "feat: add quality-eval main orchestrator recipe for competitive benchmarking"
```

---

### Task 5: Full Regression Check

**Files:** None (verification only)

**Step 1: Run the complete test suite**

Run: `cd /Users/chrispark/Projects/specialists/canvas-specialists && python -m pytest tests/ -v`

Expected: ALL tests pass. Specifically verify:
- `tests/test_competitors_config.py` — 8 tests PASS
- `tests/test_eval_harness.py` — all existing tests PASS + 2 new tests PASS
- `tests/test_quality_eval_iteration_recipe.py` — all tests PASS
- `tests/test_quality_eval_recipe.py` — all tests PASS
- All other existing test files — no regressions

**Step 2: Verify file structure**

Run: `ls -la specs/evaluation/competitors.yaml recipes/quality-eval*.yaml`

Expected output shows all 3 new files exist:
```
specs/evaluation/competitors.yaml
recipes/quality-eval-iteration.yaml
recipes/quality-eval.yaml
```

**Step 3: Verify YAML validity**

Run: `python3 -c "import yaml; [yaml.safe_load(open(f)) for f in ['specs/evaluation/competitors.yaml', 'recipes/quality-eval-iteration.yaml', 'recipes/quality-eval.yaml']]; print('All YAML files valid')"`

Expected: `All YAML files valid`

**Step 4: Final commit (all Phase 1 work)**

If any fixes were needed during the regression check, commit them:

```bash
cd /Users/chrispark/Projects/specialists/canvas-specialists && \
git add -A && \
git status
```

If clean (nothing to commit), Phase 1 is complete. If there are uncommitted fixes:

```bash
git commit -m "fix: address regression issues from quality eval harness implementation"
```

---

## Verification Checklist

After all tasks complete, verify:

- [ ] `specs/evaluation/competitors.yaml` exists with 3 competitors (anthropic, google, openai)
- [ ] `specs/evaluation/test-topics.yaml` has 8 topics (5 original + 3 competitive eval)
- [ ] `recipes/quality-eval-iteration.yaml` exists with 5 steps (load-competitors, run-pipeline, capture-pipeline-output, run-competitors, evaluate)
- [ ] `recipes/quality-eval.yaml` exists with 4 steps (load-topics, run-topic-iterations, aggregate-results, save-gap-report)
- [ ] `python -m pytest tests/ -v` shows 0 failures
- [ ] 4 git commits (one per task 1-4)

## How to Run the Harness

After implementation, run the full competitive evaluation:

```bash
recipe execute recipes/quality-eval.yaml
```

This will:
1. Load the 3 competitive eval topics
2. For each topic (~15 min each):
   - Run the specialists research-chain pipeline
   - Run 3 competitors in parallel (foundation:web-research × 3 providers)
   - Compare outputs head-to-head
3. Aggregate results and identify structural gaps
4. Save gap report to `specs/evaluation/reports/quality-eval-report.md`

**Estimated runtime:** ~45 minutes (3 topics × ~15 min sequential)

## Phase 2 Preview

Phase 2 adds the autonomous fix loop on top of this harness:
- `while_condition` loop around the harness (iterate until target score)
- Diagnosis step that maps structural gaps to specific file changes
- Fix step that implements diagnosed changes
- Revert-on-regression after each fix (git revert if score drops)
- Convergence detection (stop if score stalls for 2 iterations)
- Run report with full history (starting score → ending score → what changed)
