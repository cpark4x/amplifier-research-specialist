"""Validation tests for eval harness recipe components.

Tests three artifacts:
1. specs/evaluation/test-topics.yaml  — topic schema
2. recipes/eval-harness.yaml          — recipe structure
3. specs/evaluation/scoring-rubric.md — rubric content coverage
"""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent


class TestTestTopics:
    """Validates specs/evaluation/test-topics.yaml schema."""

    def setup_method(self) -> None:
        path = REPO_ROOT / "specs" / "evaluation" / "test-topics.yaml"
        self.data = yaml.safe_load(path.read_text(encoding="utf-8"))

    def test_has_topics_key(self) -> None:
        """'topics' key exists and is a list."""
        assert "topics" in self.data, "test-topics.yaml must have a 'topics' key"
        assert isinstance(self.data["topics"], list), "'topics' must be a list"

    def test_minimum_topic_count(self) -> None:
        """At least 5 topics defined."""
        assert len(self.data["topics"]) >= 5, (
            f"Expected at least 5 topics, got {len(self.data['topics'])}"
        )

    def test_topic_schema(self) -> None:
        """Every topic has required fields: id, query, expected_traits, purpose."""
        required_fields = {"id", "query", "expected_traits", "purpose"}
        for topic in self.data["topics"]:
            missing = required_fields - set(topic.keys())
            assert not missing, (
                f"Topic {topic.get('id', '<unknown>')} missing fields: {missing}"
            )

    def test_topic_ids_unique(self) -> None:
        """No duplicate topic IDs."""
        ids = [t["id"] for t in self.data["topics"]]
        assert len(ids) == len(set(ids)), (
            f"Duplicate topic IDs found: {[i for i in ids if ids.count(i) > 1]}"
        )

    def test_topic_queries_non_empty(self) -> None:
        """Every query is non-empty after strip()."""
        for topic in self.data["topics"]:
            assert topic["query"].strip(), (
                f"Topic '{topic.get('id')}' has an empty query"
            )

    def test_expected_traits_are_lists(self) -> None:
        """expected_traits is a list for every topic."""
        for topic in self.data["topics"]:
            assert isinstance(topic["expected_traits"], list), (
                f"Topic '{topic.get('id')}' expected_traits must be a list, "
                f"got {type(topic['expected_traits']).__name__}"
            )

    def test_has_competitive_eval_topics(self) -> None:
        """Topics must include factual-deep-dive, strategy, and survey."""
        ids = [t["id"] for t in self.data["topics"]]
        required = {"factual-deep-dive", "strategy", "survey"}
        missing = required - set(ids)
        assert not missing, f"Missing competitive eval topics: {missing}"

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
    """Validates recipes/eval-harness.yaml structure."""

    def setup_method(self) -> None:
        path = REPO_ROOT / "recipes" / "eval-harness.yaml"
        self.data = yaml.safe_load(path.read_text(encoding="utf-8"))
        # Collect all step IDs for convenience
        self.step_ids = [s["id"] for s in self.data.get("steps", [])]

    def test_has_required_recipe_fields(self) -> None:
        """Recipe has: name, description, version, steps, context."""
        required = {"name", "description", "version", "steps", "context"}
        missing = required - set(self.data.keys())
        assert not missing, f"Recipe missing required fields: {missing}"

    def test_context_has_required_inputs(self) -> None:
        """context has research_question and topic_id."""
        context = self.data["context"]
        for key in ("research_question", "topic_id"):
            assert key in context, f"context missing required input: '{key}'"

    def test_has_pipeline_steps(self) -> None:
        """Step IDs include: research, validate-research, analyze, write."""
        required = {"research", "validate-research", "analyze", "write"}
        missing = required - set(self.step_ids)
        assert not missing, f"Recipe missing pipeline steps: {missing}"

    def test_has_critic_steps(self) -> None:
        """Step IDs include: fact-check, challenge-inferences, audit-consistency."""
        required = {"fact-check", "challenge-inferences", "audit-consistency"}
        missing = required - set(self.step_ids)
        assert not missing, f"Recipe missing critic steps: {missing}"

    def test_has_scoring_step(self) -> None:
        """Step IDs include: compute-scores."""
        assert "compute-scores" in self.step_ids, "Recipe missing 'compute-scores' step"

    def test_has_save_steps(self) -> None:
        """Step IDs include: save-scores and save-report."""
        for step_id in ("save-scores", "save-report"):
            assert step_id in self.step_ids, f"Recipe missing '{step_id}' step"

    def test_critic_steps_after_pipeline_steps(self) -> None:
        """Critic steps come after pipeline steps by index."""
        pipeline_steps = {"research", "validate-research", "analyze", "write"}
        critic_steps = {"fact-check", "challenge-inferences", "audit-consistency"}

        pipeline_indices = [
            i for i, sid in enumerate(self.step_ids) if sid in pipeline_steps
        ]
        critic_indices = [
            i for i, sid in enumerate(self.step_ids) if sid in critic_steps
        ]

        assert pipeline_indices, "No pipeline steps found"
        assert critic_indices, "No critic steps found"

        max_pipeline = max(pipeline_indices)
        min_critic = min(critic_indices)
        assert min_critic > max_pipeline, (
            f"Critics must come after pipeline steps. "
            f"Max pipeline index: {max_pipeline}, min critic index: {min_critic}"
        )

    def test_step_ids_unique(self) -> None:
        """No duplicate step IDs."""
        assert len(self.step_ids) == len(set(self.step_ids)), (
            f"Duplicate step IDs found: "
            f"{[s for s in self.step_ids if self.step_ids.count(s) > 1]}"
        )

    def test_all_steps_have_output(self) -> None:
        """Every step declares an output variable."""
        for step in self.data.get("steps", []):
            assert "output" in step, (
                f"Step '{step.get('id', '<unknown>')}' is missing 'output' declaration"
            )


class TestScoringRubric:
    """Validates specs/evaluation/scoring-rubric.md."""

    def _rubric_path(self) -> Path:
        return REPO_ROOT / "specs" / "evaluation" / "scoring-rubric.md"

    def test_rubric_exists(self) -> None:
        """specs/evaluation/scoring-rubric.md exists."""
        assert self._rubric_path().exists(), (
            f"scoring-rubric.md not found at {self._rubric_path()}"
        )

    def test_rubric_covers_all_critics(self) -> None:
        """Content contains 'Fact-Checker', 'Inference Challenger', 'Consistency Auditor'."""
        content = self._rubric_path().read_text(encoding="utf-8")
        for label in ("Fact-Checker", "Inference Challenger", "Consistency Auditor"):
            assert label in content, f"scoring-rubric.md must mention critic: '{label}'"

    def test_rubric_documents_composite_formula(self) -> None:
        """Content contains composite formula weights: '0.40', '0.35', '0.25'."""
        content = self._rubric_path().read_text(encoding="utf-8")
        for weight in ("0.40", "0.35", "0.25"):
            assert weight in content, (
                f"scoring-rubric.md must document composite weight: '{weight}'"
            )
