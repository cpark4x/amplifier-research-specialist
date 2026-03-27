# Phase 1: Cold-Start Reliability — Implementation Plan

> **Execution:** Use the subagent-driven-development workflow to implement this plan.

**Goal:** A fresh clone of amplifier-research-specialist loads all modules without errors and emits specialist narration on first run.
**Architecture:** Fix the hook-specialist-narration module (currently missing source files on disk — only stale `__pycache__/*.pyc` remain), remove the broken `tool-canvas-renderer` reference from the behavior YAML, and add a packaging health test that prevents regression.
**Tech Stack:** Python 3.11+ (uses `tomllib` from stdlib), pytest, Amplifier module system (hooks)

**Roadmap reference:** `docs/plans/2026-03-05-world-class-roadmap.md` — Phase 1

---

### Task 1: Write the cold-start module health test

**Files:**
- Create: `tests/test_module_health.py`

**Step 1: Write the test file**

Create `tests/test_module_health.py` with the following exact content:

```python
"""Cold-start module health tests.

Validates that every local Amplifier module under modules/ has proper packaging:
  - pyproject.toml exists
  - pyproject.toml declares an amplifier.modules entry point
  - The entry point's target package contains __init__.py
  - The __init__.py is syntactically valid Python

Also validates that behaviors/specialists.yaml local source: paths resolve
to existing directories on disk.
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
MODULES_DIR = REPO_ROOT / "modules"
BEHAVIOR_YAML = REPO_ROOT / "behaviors" / "specialists.yaml"


def _discover_modules() -> list[Path]:
    """Return all module directories under modules/."""
    return sorted(
        [d for d in MODULES_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")],
        key=lambda d: d.name,
    )


# ---------------------------------------------------------------------------
# Module packaging health
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("module_dir", _discover_modules(), ids=lambda d: d.name)
def test_module_has_pyproject_toml(module_dir: Path) -> None:
    """Every module directory must contain a pyproject.toml."""
    pyproject = module_dir / "pyproject.toml"
    assert pyproject.is_file(), f"{module_dir.name} is missing pyproject.toml"


@pytest.mark.parametrize("module_dir", _discover_modules(), ids=lambda d: d.name)
def test_module_has_amplifier_entry_point(module_dir: Path) -> None:
    """Every module's pyproject.toml must declare an amplifier.modules entry point."""
    pyproject = module_dir / "pyproject.toml"
    if not pyproject.is_file():
        pytest.skip("pyproject.toml missing (covered by test_module_has_pyproject_toml)")
    data = tomllib.loads(pyproject.read_text())
    entry_points = (
        data.get("project", {}).get("entry-points", {}).get("amplifier.modules", {})
    )
    assert entry_points, (
        f'{module_dir.name}: pyproject.toml has no [project.entry-points."amplifier.modules"] section'
    )


@pytest.mark.parametrize("module_dir", _discover_modules(), ids=lambda d: d.name)
def test_module_package_has_init_py(module_dir: Path) -> None:
    """Every entry point's target package must contain __init__.py."""
    pyproject = module_dir / "pyproject.toml"
    if not pyproject.is_file():
        pytest.skip("pyproject.toml missing")
    data = tomllib.loads(pyproject.read_text())
    entry_points = (
        data.get("project", {}).get("entry-points", {}).get("amplifier.modules", {})
    )
    if not entry_points:
        pytest.skip("No amplifier.modules entry point")
    for _name, target in entry_points.items():
        package = target.split(":")[0]
        init_py = module_dir / package / "__init__.py"
        assert init_py.is_file(), (
            f"{module_dir.name}: package '{package}/' is missing __init__.py"
        )


@pytest.mark.parametrize("module_dir", _discover_modules(), ids=lambda d: d.name)
def test_module_source_compiles(module_dir: Path) -> None:
    """Every module's __init__.py must be syntactically valid Python."""
    pyproject = module_dir / "pyproject.toml"
    if not pyproject.is_file():
        pytest.skip("pyproject.toml missing")
    data = tomllib.loads(pyproject.read_text())
    entry_points = (
        data.get("project", {}).get("entry-points", {}).get("amplifier.modules", {})
    )
    if not entry_points:
        pytest.skip("No amplifier.modules entry point")
    for _name, target in entry_points.items():
        package = target.split(":")[0]
        init_py = module_dir / package / "__init__.py"
        if not init_py.is_file():
            pytest.skip("__init__.py missing")
        compile(init_py.read_text(), str(init_py), "exec")


# ---------------------------------------------------------------------------
# Behavior YAML health
# ---------------------------------------------------------------------------


def test_behavior_yaml_local_sources_resolve() -> None:
    """Every local source: path in the behavior YAML must resolve to an existing directory."""
    assert BEHAVIOR_YAML.is_file(), f"Behavior YAML not found: {BEHAVIOR_YAML}"
    yaml_dir = BEHAVIOR_YAML.parent
    text = BEHAVIOR_YAML.read_text()

    # Extract source: values that are relative paths (start with . or ..)
    sources = re.findall(r"source:\s*(\.\S+)", text)
    assert sources, "Expected at least one local source: path in behavior YAML"

    broken = []
    for source in sources:
        resolved = (yaml_dir / source).resolve()
        if not resolved.is_dir():
            broken.append(f"  source: {source} -> {resolved}")

    assert not broken, (
        "Broken local source paths in behaviors/specialists.yaml:\n" + "\n".join(broken)
    )
```

**Step 2: Run the test to verify it fails**

Run:
```bash
python3 -m pytest tests/test_module_health.py -v
```

Expected: **2 FAILED, 3 SKIPPED, 4 PASSED** (9 tests total)

```
test_module_has_pyproject_toml[hook-specialist-narration]       FAILED   ← no pyproject.toml
test_module_has_pyproject_toml[tool-canvas-renderer]            PASSED
test_module_has_amplifier_entry_point[hook-specialist-narration] SKIPPED ← cascading skip
test_module_has_amplifier_entry_point[tool-canvas-renderer]     PASSED
test_module_package_has_init_py[hook-specialist-narration]      SKIPPED ← cascading skip
test_module_package_has_init_py[tool-canvas-renderer]           PASSED
test_module_source_compiles[hook-specialist-narration]          SKIPPED ← cascading skip
test_module_source_compiles[tool-canvas-renderer]               PASSED
test_behavior_yaml_local_sources_resolve                        FAILED   ← ./modules/... paths wrong
```

**Step 3: Commit the failing test**

Run:
```bash
git add tests/test_module_health.py && git commit -m "test: add cold-start module health test (red)"
```

---

### Task 2: Ship hook-specialist-narration as a real module

**Files:**
- Create: `modules/hook-specialist-narration/pyproject.toml`
- Create: `modules/hook-specialist-narration/amplifier_module_hook_specialist_narration/__init__.py`
- Modify: `tests/test_module_health.py` (add `@pytest.mark.xfail` on `test_behavior_yaml_local_sources_resolve`)

**Step 1: Create the pyproject.toml**

Create `modules/hook-specialist-narration/pyproject.toml` with the following exact content.
This follows the same packaging pattern as `modules/tool-canvas-renderer/pyproject.toml`:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "hook-specialist-narration"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "amplifier-core",
]

[project.entry-points."amplifier.modules"]
hook-specialist-narration = "amplifier_module_hook_specialist_narration:mount"
```

**Step 2: Create the hook implementation**

Create `modules/hook-specialist-narration/amplifier_module_hook_specialist_narration/__init__.py`
with the following exact content. This is the narration hook that was previously running
from stale bytecache only — now committed as real source:

```python
"""Specialist narration hook module.

Emits progress narration lines to the user when specialists are delegated to,
showing which specialist is running, handoff transitions, and final completion.

Hooks registered:
  tool:pre              — "🔍 Running <specialist>..." (or combined with prior completion)
  tool:post             — records completed specialist (deferred message)
  orchestrator:complete — "✏️ Done. Here's your <format>."

Suppression:
  If the delegate instruction starts with "[RAW]", no narration is emitted
  for that entire chain and state is cleared on orchestrator:complete.
"""

from __future__ import annotations

__amplifier_module_type__ = "hook"

import logging
from typing import Any

from amplifier_core import HookResult, ModuleCoordinator

logger = logging.getLogger(__name__)

# Maps the last specialist in a chain to the human-friendly output format name
# used in the FINAL narration line: "Done. Here's your <format>."
FORMAT_MAP: dict[str, str] = {
    "writer": "brief",
    "storyteller": "story",
    "data-analyzer": "analysis",
    "researcher": "research",
}

SPECIALIST_PREFIX = "specialists:"


def _extract_specialist(agent: str) -> str | None:
    """Extract the specialist short name from a delegate agent path.

    e.g. "specialists:writer" -> "writer"
    Returns None if the agent is not a specialists bundle specialist.
    """
    if agent.startswith(SPECIALIST_PREFIX):
        return agent[len(SPECIALIST_PREFIX):]
    return None


class SpecialistNarrationHook:
    """Emits narration lines for specialist delegation chains.

    State machine per-instance (one instance per coordinator session):
      _completed_specialist  — specialist that just finished (set in tool:post,
                               consumed in next tool:pre or orchestrator:complete)
      _last_specialist       — most recently started specialist (for format mapping)
      _suppressed            — True when a [RAW] instruction was seen; cleared on
                               orchestrator:complete
    """

    def __init__(self) -> None:
        self._completed_specialist: str | None = None
        self._last_specialist: str | None = None
        self._suppressed: bool = False

    def _get_specialist_from_data(self, data: dict[str, Any]) -> str | None:
        """Return specialist name if this is a specialist delegate call, else None."""
        tool_name = data.get("tool_name", "")
        if tool_name != "delegate":
            return None
        tool_input = data.get("tool_input")
        if not isinstance(tool_input, dict):
            return None
        agent = tool_input.get("agent", "")
        return _extract_specialist(agent)

    def on_tool_pre(self, event: str, data: dict[str, Any]) -> HookResult:
        """Emit narration before a specialist delegate call.

        Emits:
          "🔍 Running <specialist>..."
        or, when a previous specialist just completed and a different one starts:
          "✅ <prev> complete — passing to <current>...\\n🔍 Running <current>..."
        """
        current = self._get_specialist_from_data(data)
        if current is None:
            return HookResult("continue")

        # Check for [RAW] suppression
        tool_input = data.get("tool_input")
        if isinstance(tool_input, dict):
            instruction = str(tool_input.get("instruction", ""))
            if instruction.startswith("[RAW]"):
                self._suppressed = True

        if self._suppressed:
            self._completed_specialist = None
            self._last_specialist = current
            return HookResult("continue")

        # Build narration message
        if self._completed_specialist:
            msg = (
                f"✅ {self._completed_specialist} complete — passing to {current}...\n"
                f"🔍 Running {current}..."
            )
        else:
            msg = f"🔍 Running {current}..."

        self._completed_specialist = None
        self._last_specialist = current
        return HookResult("continue", msg)

    def on_tool_post(self, event: str, data: dict[str, Any]) -> HookResult:
        """Record which specialist just completed (deferred — no message yet).

        The "complete" message is deferred to the next tool:pre (where we know
        whether it's a handoff or the end of the chain) or to orchestrator:complete.
        """
        current = self._get_specialist_from_data(data)
        if current is None:
            return HookResult("continue")
        if not self._suppressed:
            self._completed_specialist = current
        return HookResult("continue")

    def on_orchestrator_complete(self, event: str, data: dict[str, Any]) -> HookResult:
        """Emit the final completion line when the specialist chain ends.

        Clears all instance state regardless of suppression so the next run starts fresh.
        """
        suppressed = self._suppressed
        completed = self._completed_specialist
        last = self._last_specialist

        # Clear state for next run
        self._suppressed = False
        self._completed_specialist = None
        self._last_specialist = None

        if suppressed:
            return HookResult("continue")

        parts = []
        if completed:
            parts.append(f"✅ {completed} complete — returning to coordinator...")

        fmt = FORMAT_MAP.get(last, "output") if last else "output"
        parts.append(f"✏️ Done. Here's your {fmt}.")

        return HookResult("continue", "\n".join(parts))


async def mount(coordinator: ModuleCoordinator, config: dict) -> None:
    """Mount the specialist narration hook.

    Registers three event handlers on the coordinator's hook registry:
      tool:pre, tool:post, orchestrator:complete
    """
    hook = SpecialistNarrationHook()
    coordinator.hooks.register(
        "tool:pre", hook.on_tool_pre, name="hook-specialist-narration-pre"
    )
    coordinator.hooks.register(
        "tool:post", hook.on_tool_post, name="hook-specialist-narration-post"
    )
    coordinator.hooks.register(
        "orchestrator:complete",
        hook.on_orchestrator_complete,
        name="hook-specialist-narration-complete",
    )
    logger.info("Mounted hook-specialist-narration")
```

**Step 3: Run health tests to verify module packaging passes**

Also mark `test_behavior_yaml_local_sources_resolve` as `@pytest.mark.xfail(strict=True)` in
`tests/test_module_health.py`. The YAML source paths (`./modules/...`) are still broken at this
point — that fix belongs to Task 3. The xfail marker keeps the suite green without hiding the
known failure, and `strict=True` ensures an unexpected pass (i.e. after Task 3 lands) will be
caught and the marker removed.

Run:
```bash
python3 -m pytest tests/test_module_health.py -v
```

Expected: **8 passed, 1 xfailed** (9 tests total)

> **Why not "1 FAILED" as originally planned?** The original plan expected a raw FAILED for the
> YAML test so Task 3 had a clear red state to fix. In practice the implementer elected to xfail
> the known-broken test immediately (keeping CI green on this branch) rather than leave an
> outstanding failure. The YAML path remains unfixed — Task 3 still applies the real fix and
> removes the xfail marker.

```
test_module_has_pyproject_toml[hook-specialist-narration]       PASSED  ← fixed
test_module_has_pyproject_toml[tool-canvas-renderer]            PASSED
test_module_has_amplifier_entry_point[hook-specialist-narration] PASSED ← fixed
test_module_has_amplifier_entry_point[tool-canvas-renderer]     PASSED
test_module_package_has_init_py[hook-specialist-narration]      PASSED  ← fixed
test_module_package_has_init_py[tool-canvas-renderer]           PASSED
test_module_source_compiles[hook-specialist-narration]          PASSED  ← fixed
test_module_source_compiles[tool-canvas-renderer]               PASSED
test_behavior_yaml_local_sources_resolve                        XFAIL  ← xfailed (yaml not fixed yet)
```

**Step 4: Commit**

Run:
```bash
git add modules/hook-specialist-narration/pyproject.toml \
      modules/hook-specialist-narration/amplifier_module_hook_specialist_narration/__init__.py \
      tests/test_module_health.py \
  && git commit -m "fix: add hook-specialist-narration packaging + xfail broken source paths"
```

---

### Task 3: Fix behaviors/specialists.yaml

**Files:**
- Modify: `behaviors/specialists.yaml`

**Step 1: Edit the file**

Make two changes to `behaviors/specialists.yaml`:

1. **Remove the `tool-canvas-renderer` entry** (lines 9–10). It references a module we are
   deferring to a later phase. Every run currently logs a "Failed to activate" warning because
   of it. Also update the `description` on line 4 to remove the "rendering" mention.

2. **Fix the hook source path** (line 27). Change `./modules/hook-specialist-narration` to
   `../modules/hook-specialist-narration`. Paths in `source:` resolve relative to the YAML
   file's own directory (`behaviors/`), so `./modules/...` resolves to `behaviors/modules/...`
   which does not exist. The `../` prefix correctly resolves to the repo-root `modules/` dir.

The file should look like this after editing:

```yaml
bundle:
  name: specialists-behavior
  version: 1.0.0
  description: Adds researcher and writer specialists with web capabilities

tools:
  - module: tool-web
    source: git+https://github.com/microsoft/amplifier-module-tool-web@main
  - module: tool-skills
    config:
      skills:
        - "@doc-driven-dev:skills"

agents:
  include:
    - specialists:researcher
    - specialists:writer
    - specialists:competitive-analysis
    - specialists:data-analyzer
    - specialists:researcher-formatter
    - specialists:storyteller

hooks:
  - module: hook-specialist-narration
    source: ../modules/hook-specialist-narration

spawn:
  exclude_tools: [write_file, edit_file, apply_patch]

context:
  include:
    - specialists:context/specialists-instructions.md
```

**Step 2: Run the full test suite**

Run the health tests first:
```bash
python3 -m pytest tests/test_module_health.py -v
```

Expected: **ALL 9 PASSED**.

Then run the entire existing test suite to make sure nothing else broke:
```bash
python3 -m pytest tests/ -v
```

Expected: All existing tests still pass (no regressions).

**Step 3: Commit**

Run:
```bash
git add behaviors/specialists.yaml && git commit -m "fix: remove tool-canvas-renderer, fix hook-specialist-narration source path"
```

---

### Task 4: Add "Verify Your Setup" section to USING-SPECIALISTS.md

**Files:**
- Modify: `docs/USING-SPECIALISTS.md`

**Step 1: Add the section**

Insert a new `## Verify Your Setup` section in `docs/USING-SPECIALISTS.md` between
the `---` separator on line 26 and `## The Specialists` on line 28.

Add this block after the `---` on line 26 (before `## The Specialists`):

```markdown

## Verify Your Setup

Before using specialists, confirm the system is healthy:

```bash
# Run the module health test — validates packaging and source files
python3 -m pytest tests/test_module_health.py -v
```

All tests should pass. If any fail, the error message tells you exactly what's missing.

To run a quick end-to-end smoke test with the full specialist chain:

```bash
amplifier run --bundle "file://$(pwd)" "Research the history of the paperclip. Keep it to 3 sources max."
```

You should see narration lines before the output:
- `🔍 Running researcher...`
- `✅ researcher complete — passing to writer...`
- `✏️ Done. Here's your brief.`

Followed by the writer's `Parsed:` output.

---
```

The resulting section order should be: *Why specialists...* → *Verify Your Setup* → *The Specialists*.

**Step 2: Commit**

Run:
```bash
git add docs/USING-SPECIALISTS.md && git commit -m "docs: add Verify Your Setup section to USING-SPECIALISTS.md"
```

---

## Phase 1 Acceptance Checklist

After all 4 tasks are complete, verify:

- [ ] `python3 -m pytest tests/test_module_health.py -v` — all 9 tests pass
- [ ] `python3 -m pytest tests/ -v` — entire existing test suite still passes
- [ ] `modules/hook-specialist-narration/pyproject.toml` exists and has `amplifier.modules` entry point
- [ ] `modules/hook-specialist-narration/amplifier_module_hook_specialist_narration/__init__.py` exists (real source, not just `__pycache__`)
- [ ] `behaviors/specialists.yaml` has **no** `tool-canvas-renderer` entry
- [ ] `behaviors/specialists.yaml` hook source path is `../modules/hook-specialist-narration` (not `./modules/...`)
- [ ] `docs/USING-SPECIALISTS.md` has a "Verify Your Setup" section
- [ ] `git log --oneline -4` shows 4 clean commits for this phase