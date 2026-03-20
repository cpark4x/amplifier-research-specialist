"""Validation tests for specs/evaluation/competitors.yaml.

Ensures the competitor configuration used by the quality-eval recipe
is well-formed and covers all required providers for triangulation.
"""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
COMPETITORS_PATH = REPO_ROOT / "specs" / "evaluation" / "competitors.yaml"
VALID_PROVIDERS = {"anthropic", "google", "openai"}


class TestCompetitorsConfig:
    """Validates specs/evaluation/competitors.yaml schema and content."""

    def setup_method(self) -> None:
        self.data = yaml.safe_load(COMPETITORS_PATH.read_text(encoding="utf-8"))

    def test_file_exists(self) -> None:
        """specs/evaluation/competitors.yaml exists."""
        assert COMPETITORS_PATH.exists(), (
            f"competitors.yaml not found at {COMPETITORS_PATH}"
        )

    def test_has_competitors_key(self) -> None:
        """Top-level 'competitors' key exists and is a list."""
        assert "competitors" in self.data, (
            "competitors.yaml must have a top-level 'competitors' key"
        )
        assert isinstance(self.data["competitors"], list), (
            "'competitors' must be a list"
        )

    def test_minimum_three_competitors(self) -> None:
        """At least 3 competitors defined."""
        competitors = self.data.get("competitors", [])
        assert len(competitors) >= 3, (
            f"Expected at least 3 competitors, got {len(competitors)}"
        )

    def test_required_fields_on_each_competitor(self) -> None:
        """Every competitor has required fields: name, agent, provider, model."""
        required_fields = {"name", "agent", "provider", "model"}
        for competitor in self.data.get("competitors", []):
            missing = required_fields - set(competitor.keys())
            assert not missing, (
                f"Competitor '{competitor.get('name', '<unknown>')}' "
                f"missing fields: {missing}"
            )

    def test_unique_names(self) -> None:
        """No duplicate competitor names."""
        names = [c["name"] for c in self.data.get("competitors", [])]
        assert len(names) == len(set(names)), (
            f"Duplicate competitor names found: "
            f"{[n for n in names if names.count(n) > 1]}"
        )

    def test_all_use_foundation_web_research_agent(self) -> None:
        """All competitors use the foundation:web-research agent."""
        for competitor in self.data.get("competitors", []):
            assert competitor.get("agent") == "foundation:web-research", (
                f"Competitor '{competitor.get('name')}' must use "
                f"'foundation:web-research', got '{competitor.get('agent')}'"
            )

    def test_valid_providers(self) -> None:
        """All providers are one of: anthropic, google, openai."""
        for competitor in self.data.get("competitors", []):
            provider = competitor.get("provider")
            assert provider in VALID_PROVIDERS, (
                f"Competitor '{competitor.get('name')}' has invalid provider "
                f"'{provider}'. Must be one of: {VALID_PROVIDERS}"
            )

    def test_all_three_providers_represented(self) -> None:
        """All three providers (anthropic, google, openai) are present for triangulation."""
        providers = {c.get("provider") for c in self.data.get("competitors", [])}
        missing = VALID_PROVIDERS - providers
        assert not missing, (
            f"Missing providers for triangulation: {missing}. "
            f"All three providers must be represented."
        )
