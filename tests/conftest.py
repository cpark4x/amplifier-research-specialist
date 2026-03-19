"""Shared test fixtures and path constants.

Centralizes agent file paths so a rename only requires updating this file.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
AGENTS_DIR = REPO_ROOT / "agents"

# Agent definition files
RESEARCHER = AGENTS_DIR / "researcher.md"
WRITER = AGENTS_DIR / "writer.md"
STORYTELLER = AGENTS_DIR / "storyteller.md"
PRIORITIZER = AGENTS_DIR / "prioritizer.md"
COMPETITIVE_ANALYSIS = AGENTS_DIR / "competitive-analysis.md"
DATA_ANALYZER = AGENTS_DIR / "data-analyzer.md"
RESEARCHER_FORMATTER = AGENTS_DIR / "researcher-formatter.md"
DATA_ANALYZER_FORMATTER = AGENTS_DIR / "data-analyzer-formatter.md"
WRITER_FORMATTER = AGENTS_DIR / "writer-formatter.md"
STORY_FORMATTER = AGENTS_DIR / "story-formatter.md"
PRIORITIZER_FORMATTER = AGENTS_DIR / "prioritizer-formatter.md"
PLANNER = AGENTS_DIR / "planner.md"

# Other key files
BEHAVIORS_YAML = REPO_ROOT / "behaviors" / "specialists.yaml"
COORDINATOR_ROUTING = REPO_ROOT / "context" / "coordinator-routing.md"
