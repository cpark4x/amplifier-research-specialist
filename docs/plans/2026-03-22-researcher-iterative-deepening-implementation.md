# Researcher Iterative Deepening Implementation Plan

> **Execution:** Use the subagent-driven-development workflow to implement this plan.

**Goal:** Add a "depth check" to the researcher's Quality Gate (Stage 6) so thin sub-questions automatically get a targeted second-pass search.
**Architecture:** Single file change to `agents/researcher.md` — a new item 6 in the Quality Gate's numbered list, inserted between the existing item 5 (factual breadth gate) and the PASS/FAIL lines. No new stages, files, or output format changes.
**Tech Stack:** Markdown (agent spec), pytest (structural tests)
**Design doc:** `docs/plans/2026-03-22-researcher-iterative-deepening-design.md`

---

### Task 1: Write structural tests (TDD red phase)

**Files:**
- Create: `tests/test_researcher_iterative_deepening.py`

**Step 1: Create the test file**

Create `tests/test_researcher_iterative_deepening.py` with this exact content:

```python
"""
Structural tests for the researcher iterative deepening depth check (#49).
Validates that the Quality Gate in agents/researcher.md contains the depth check
with correct triggers and targeted deepening strategies.
"""

from functools import lru_cache
from pathlib import Path

SPEC_FILE = Path(__file__).parent.parent / "agents" / "researcher.md"


@lru_cache(maxsize=None)
def _content() -> str:
    assert SPEC_FILE.exists(), f"File not found: {SPEC_FILE}"
    return SPEC_FILE.read_text(encoding="utf-8")


def test_depth_check_exists() -> None:
    """The Quality Gate must mention the depth check for thin sub-questions."""
    c = _content()
    assert "thin" in c.lower() and "sub-question" in c.lower(), (
        "Quality Gate must mention 'thin sub-question' concept"
    )


def test_depth_check_after_breadth_gate() -> None:
    """The depth check must come after the factual breadth gate (item 5)."""
    c = _content()
    assert c.index("Factual breadth gate") < c.index("Depth check"), (
        "Depth check must appear after the Factual breadth gate in the file"
    )


def test_depth_check_before_pass_line() -> None:
    """The depth check must come before the PASS/FAIL lines."""
    c = _content()
    assert c.index("Depth check") < c.index("**PASS:**"), (
        "Depth check must appear before the PASS line"
    )


def test_depth_check_source_count_trigger() -> None:
    """The depth check must mention the source count trigger (fewer than 3)."""
    c = _content()
    assert "fewer than 3" in c or "< 3" in c, (
        "Depth check must specify 'fewer than 3' as a thin trigger"
    )


def test_depth_check_tier_trigger() -> None:
    """The depth check must mention the source tier trigger (no primary/academic)."""
    c = _content()
    # Extract the Quality Gate section
    qg = c[c.index("Stage 6: Quality Gate"):]
    assert "no" in qg.lower() and ("primary" in qg.lower() or "academic" in qg.lower()), (
        "Depth check must mention absence of primary or academic sources as a trigger"
    )


def test_depth_check_academic_search() -> None:
    """The deepening strategies must include academic sources."""
    c = _content()
    qg = c[c.index("Stage 6: Quality Gate"):]
    has_academic = (
        "arxiv" in qg.lower()
        or "google scholar" in qg.lower()
        or "conference proceedings" in qg.lower()
    )
    assert has_academic, (
        "Depth check must mention arxiv, Google Scholar, or conference proceedings"
    )


def test_depth_check_official_search() -> None:
    """The deepening strategies must include official/primary sources."""
    c = _content()
    qg = c[c.index("Stage 6: Quality Gate"):]
    has_official = (
        "official docs" in qg.lower()
        or "gov sites" in qg.lower()
        or "vendor pages" in qg.lower()
    )
    assert has_official, (
        "Depth check must mention official docs, gov sites, or vendor pages"
    )


def test_depth_check_practitioner_search() -> None:
    """The deepening strategies must include practitioner sources."""
    c = _content()
    qg = c[c.index("Stage 6: Quality Gate"):]
    has_practitioner = (
        "engineering blogs" in qg.lower()
        or "case studies" in qg.lower()
        or "conference talks" in qg.lower()
    )
    assert has_practitioner, (
        "Depth check must mention engineering blogs, case studies, or conference talks"
    )
```

**Step 2: Run tests to verify they fail**

Run:
```bash
pytest tests/test_researcher_iterative_deepening.py -v
```

Expected: All 7 tests FAIL. The depth check content does not exist in `agents/researcher.md` yet. You should see failures like `AssertionError: Depth check must appear after the Factual breadth gate` and `ValueError` (from `.index()` not finding "Depth check").

**Step 3: Commit the failing tests**

```bash
git add tests/test_researcher_iterative_deepening.py && git commit -m "test: add structural tests for researcher depth check (#49) — red phase"
```

---

### Task 2: Add depth check to Quality Gate (Stage 6)

**Files:**
- Modify: `agents/researcher.md` (lines 239–241 — insert between item 5 and the PASS line)

**Step 1: Read the file to confirm the insertion point**

Read `agents/researcher.md`. Find the end of item 5 (the factual breadth gate) and the `**PASS:**` line. The new content goes between them.

Currently, the file has this around lines 239–241:

```
5. **Factual breadth gate.** For the detected question type, verify your findings cover at least **80% of the required dimensions** listed in Step B of the Planner. If any required dimension has zero findings, run 1–2 targeted searches specifically for that dimension before proceeding. This is the single most common failure mode: the pipeline produces strong analysis on a narrow evidence base while missing entire topic categories that the audience needs.

**PASS:** All checks clear — proceed to Synthesizer
```

**Step 2: Insert the depth check as item 6**

Insert the following block between item 5 and the `**PASS:**` line (replacing the blank line between them):

```markdown

6. **Depth check for thin sub-questions.** For each sub-question from the Planner (Stage 1), evaluate evidence depth. A sub-question is "thin" if either trigger fires:
   - **Source count trigger:** The sub-question has fewer than 3 distinct findings addressing it.
   - **Source tier trigger:** The sub-question has no findings from primary or academic sources (all coverage is tertiary/blog-level).

   For each thin sub-question, run one targeted deepening pass that fills whatever source type is missing:
   - **No academic sources →** search arxiv, Google Scholar, conference proceedings for the sub-question topic.
   - **No official/primary sources →** search official docs, gov sites, vendor pages, specification documents.
   - **No practitioner depth →** search engineering blogs, case studies, conference talks for specific metrics and named examples.

   Max 1 deepening pass per Quality Gate cycle. New findings from the deepening pass go through the normal extract → corroborate flow before the Quality Gate re-evaluates.

```

After this edit, the file should read (around the insertion area):

```
5. **Factual breadth gate.** ...

6. **Depth check for thin sub-questions.** ...

**PASS:** All checks clear — proceed to Synthesizer
```

**Step 3: Run the structural tests to verify they pass**

Run:
```bash
pytest tests/test_researcher_iterative_deepening.py -v
```

Expected: All 7 tests PASS.

**Step 4: Commit**

```bash
git add agents/researcher.md && git commit -m "feat: add depth check for thin sub-questions to Quality Gate (#49)"
```

---

### Task 3: Update file length thresholds and run full suite

**Files:**
- Modify: `tests/test_task7_researcher_verification.py` (lines 115–141 — the `TestFileLength` class)

**Step 1: Check the new line count**

Run:
```bash
wc -l agents/researcher.md
```

Expected: approximately 336–340 lines (was 322, added ~14–18 lines). This is within the current `< 350` hard limit and `280–350` band, but barely. Update the thresholds to give headroom for future edits.

**Step 2: Update the thresholds**

In `tests/test_task7_researcher_verification.py`, make these three changes inside the `TestFileLength` class:

**Change 1** — `test_not_too_long` (line 119): Change `350` to `370`.

Find:
```python
    def test_not_too_long(self, line_count: int) -> None:
        """File must be under 350 lines (grew from ~237 to ~322 after quality loop additions)."""
        assert line_count < 350, (
            f"File is {line_count} lines — above 350. "
            f"Check whether unexpected content was added."
        )
```

Replace with:
```python
    def test_not_too_long(self, line_count: int) -> None:
        """File must be under 370 lines (grew from ~322 to ~337 after depth check addition)."""
        assert line_count < 370, (
            f"File is {line_count} lines — above 370. "
            f"Check whether unexpected content was added."
        )
```

**Change 2** — `TestFileLength` class docstring (line 115): Change `350` to `370`.

Find:
```python
class TestFileLength:
    """File should be ~280–350 lines. Hard fail if >350 or <200."""
```

Replace with:
```python
class TestFileLength:
    """File should be ~300–370 lines. Hard fail if >370 or <200."""
```

**Change 3** — `test_approximate_target` (lines 131–141): Change the band from `280–350` to `300–370`.

Find:
```python
    def test_approximate_target(self, line_count: int) -> None:
        """File should be approximately 280–350 lines after quality loop additions.

        The file legitimately grew from ~237 to ~322 lines because it gained
        coverage checklists and diversity gates.  We use a wider band (280–350)
        to allow minor variation while still catching major drift.
        """
        assert 280 <= line_count <= 350, (
            f"File is {line_count} lines — outside the 280–350 target band. "
            f"Expected approximately 280–350 after quality loop additions."
        )
```

Replace with:
```python
    def test_approximate_target(self, line_count: int) -> None:
        """File should be approximately 300–370 lines after depth check addition.

        The file legitimately grew from ~322 to ~337 lines because it gained
        the depth check for thin sub-questions (#49).  We use a wider band
        (300–370) to allow minor variation while still catching major drift.
        """
        assert 300 <= line_count <= 370, (
            f"File is {line_count} lines — outside the 300–370 target band. "
            f"Expected approximately 300–370 after depth check addition."
        )
```

**Step 3: Run the full test suite**

Run:
```bash
pytest tests/test_task7_researcher_verification.py tests/test_researcher_iterative_deepening.py -v
```

Expected: ALL tests pass — both the new depth check tests and the existing researcher verification tests (including the updated length thresholds).

**Step 4: Run the complete test suite for regressions**

Run:
```bash
pytest tests/ -v
```

Expected: No regressions. All existing tests pass.

**Step 5: Commit**

```bash
git add tests/test_task7_researcher_verification.py && git commit -m "test: update researcher file length thresholds for depth check (#49)"
```

---

## Summary

| Task | Action | File |
|------|--------|------|
| 1 | Create | `tests/test_researcher_iterative_deepening.py` (7 structural tests) |
| 2 | Modify | `agents/researcher.md` (add item 6 to Quality Gate) |
| 3 | Modify | `tests/test_task7_researcher_verification.py` (update length thresholds) |

Total commits: 3
Total files changed: 3 (1 created, 2 modified)
