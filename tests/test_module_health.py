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
        pytest.skip(
            "pyproject.toml missing (covered by test_module_has_pyproject_toml)"
        )
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
