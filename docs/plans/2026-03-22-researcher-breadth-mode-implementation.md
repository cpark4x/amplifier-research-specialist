# Researcher Breadth Mode (#46) Implementation Plan

> **Execution:** Use the subagent-driven-development workflow to implement this plan.

**Goal:** Add `research_mode: breadth` to the researcher so survey-type questions automatically use lighter corroboration (numeric claims only), letting the researcher cover 15–20 entities instead of 10–13.

**Architecture:** Two surgical insertions into `agents/researcher.md`. Stage 1 (Planner) gets a new Step D that auto-selects breadth mode for Survey/Ranking questions. Stage 5 (Corroborator) gets a preamble that skips corroboration for qualitative claims in breadth mode. No new files, no new pipeline stages — just two text blocks added to an existing markdown agent file.

**Tech Stack:** Markdown agent specification, pytest structural tests (text assertions against the `.md` file — no LLM calls)

**Design doc:** `docs/plans/2026-03-22-researcher-breadth-mode-design.md`

---

## Codebase Orientation

Before you touch anything, read this section so you know what you're working with.

**The file you're modifying:** `agents/researcher.md` (332 lines). It's a markdown agent spec with YAML frontmatter. The pipeline has 7 stages. You care about two:

- **Stage 1: Planner** (line 53). Has three sub-steps:
  - Step A — question-type classifier (line 67) — already detects "Survey / Ranking"
  - Step B — coverage dimensions per question type (line 77)
  - Step C — coverage gate (line 118) — ends at line 122
  - Then Stage 2 starts at line 124
- **Stage 5: Corroborator** (line 215). Currently says "For every Low or Medium confidence claim:" followed by 4 numbered steps (lines 219-222) and a closing sentence (line 224). Stage 6 starts at line 226.

**Test pattern to follow:** `tests/test_researcher_iterative_deepening.py`. Uses `SPEC_FILE`, `@lru_cache`, `_content()`, and individual `def test_*()` functions with `assert "text" in c` style assertions.

**File length threshold:** `tests/test_task7_researcher_verification.py` has a hard-fail at 350 lines and a target band of 280–350. Adding ~20 lines to the researcher file (currently 332) will push it to ~352, so you'll need to raise both thresholds.

---

## Task 1: Write structural tests (TDD red phase)

**Files:**
- Create: `tests/test_researcher_breadth_mode.py`

**Step 1: Create the test file**

Create `tests/test_researcher_breadth_mode.py` with the following exact content:

```python
"""
Structural tests for researcher breadth mode (#46).
Validates that the researcher agent file contains mode selection
in Stage 1 and breadth-aware corroboration logic in Stage 5.

Fixes #46: researcher breadth mode for survey questions.
"""

from functools import lru_cache
from pathlib import Path

SPEC_FILE = Path(__file__).parent.parent / "agents" / "researcher.md"


@lru_cache(maxsize=None)
def _content() -> str:
    assert SPEC_FILE.exists(), f"File not found: {SPEC_FILE}"
    return SPEC_FILE.read_text(encoding="utf-8")


# ─── Stage 1: Mode selection ────────────────────────────────────────


def test_breadth_mode_selection_exists() -> None:
    """Stage 1 must contain research_mode or breadth mode selection language."""
    c = _content()
    has_mode_selection = (
        "research_mode" in c
        or "breadth mode" in c.lower()
        or "research mode" in c.lower()
    )
    assert has_mode_selection, (
        "Stage 1 must contain 'research_mode' or 'breadth mode' selection language"
    )


def test_breadth_mode_after_question_type_classifier() -> None:
    """Mode selection must come after the question-type classifier (Step A) in Stage 1."""
    c = _content()
    assert c.index("Step A") < c.index("research_mode"), (
        "Mode selection (research_mode) must come after Step A (question-type classifier)"
    )


def test_breadth_mode_survey_trigger() -> None:
    """Mode selection must mention Survey/Ranking as the trigger for breadth mode."""
    c = _content()
    has_survey_trigger = (
        "Survey" in c and "breadth" in c.lower()
    )
    assert has_survey_trigger, (
        "Mode selection must mention 'Survey' as trigger for breadth mode"
    )


def test_breadth_mode_depth_override() -> None:
    """Mode selection must mention that caller can override with research_mode: depth."""
    c = _content()
    has_override = (
        "research_mode: depth" in c
        or "research_mode` was provided" in c
        or "override" in c.lower()
    )
    assert has_override, (
        "Mode selection must mention caller override with 'research_mode: depth'"
    )


# ─── Stage 5: Breadth mode corroboration ─────────────────────────────


def test_breadth_mode_corroboration_exists() -> None:
    """Stage 5 must contain breadth mode corroboration logic."""
    c = _content()
    # Find the Stage 5 section and check it mentions breadth
    stage5_start = c.index("Stage 5: Corroborator")
    stage6_start = c.index("Stage 6: Quality Gate")
    stage5_section = c[stage5_start:stage6_start]
    assert "breadth" in stage5_section.lower(), (
        "Stage 5 (Corroborator) must contain breadth mode corroboration logic"
    )


def test_breadth_mode_numeric_corroboration() -> None:
    """Stage 5 must state that numeric/financial claims get full corroboration in breadth mode."""
    c = _content()
    stage5_start = c.index("Stage 5: Corroborator")
    stage6_start = c.index("Stage 6: Quality Gate")
    stage5_section = c[stage5_start:stage6_start].lower()
    has_numeric = (
        "numeric" in stage5_section
        or "financial" in stage5_section
    )
    assert has_numeric, (
        "Stage 5 must mention numeric/financial claims get full corroboration in breadth mode"
    )


def test_breadth_mode_qualitative_skip() -> None:
    """Stage 5 must state that qualitative claims skip corroboration in breadth mode."""
    c = _content()
    stage5_start = c.index("Stage 5: Corroborator")
    stage6_start = c.index("Stage 6: Quality Gate")
    stage5_section = c[stage5_start:stage6_start].lower()
    has_qualitative = (
        "qualitative" in stage5_section
        and ("skip" in stage5_section or "accept" in stage5_section)
    )
    assert has_qualitative, (
        "Stage 5 must mention qualitative claims skip corroboration or are accepted at medium confidence"
    )


def test_breadth_mode_flag() -> None:
    """Stage 5 must mention 'breadth-mode' as a flag for single-source claims."""
    c = _content()
    stage5_start = c.index("Stage 5: Corroborator")
    stage6_start = c.index("Stage 6: Quality Gate")
    stage5_section = c[stage5_start:stage6_start]
    assert "breadth-mode" in stage5_section, (
        "Stage 5 must flag single-source qualitative claims as 'breadth-mode'"
    )
```

**Step 2: Run tests to verify they all fail**

Run:
```
pytest tests/test_researcher_breadth_mode.py -v
```

Expected: **All 8 tests FAIL.** The breadth mode text doesn't exist in `agents/researcher.md` yet. You should see 8 `FAILED` lines. If any test passes, something is wrong — stop and investigate.

**Step 3: Commit the failing tests**

```
git add tests/test_researcher_breadth_mode.py && git commit -m "test: add structural tests for researcher breadth mode (red phase, #46)"
```

---

## Task 2: Add mode selection to Stage 1 (Planner)

**Files:**
- Modify: `agents/researcher.md` (insert after line 122, before line 124)

**Step 1: Insert Step D after Step C in Stage 1**

In `agents/researcher.md`, find this exact text (the end of Step C, lines 118–124):

```
**Step C — Coverage gate:**

Before proceeding to Stage 2, verify your sub-question list covers at least 80% of the required dimensions for the detected question type. If coverage falls short, add sub-questions until the threshold is met.

For **Survey / Ranking** and **Head-to-Head Comparison** question types, expand the sub-question budget to **5–10** (from the default 3–7) to ensure sufficient breadth.

### Stage 2: Source Discoverer
```

Replace it with this (same Step C content, plus new Step D, then Stage 2):

```
**Step C — Coverage gate:**

Before proceeding to Stage 2, verify your sub-question list covers at least 80% of the required dimensions for the detected question type. If coverage falls short, add sub-questions until the threshold is met.

For **Survey / Ranking** and **Head-to-Head Comparison** question types, expand the sub-question budget to **5–10** (from the default 3–7) to ensure sufficient breadth.

**Step D — Research mode selection:**

- If question type is **Survey / Ranking** AND no explicit `research_mode` was provided by the caller → set `research_mode: breadth`
- If the caller explicitly passed `research_mode: depth` → use depth regardless of question type
- All other question types default to `research_mode: depth` (current behavior)
- If the question-type classifier failed to classify → default to `research_mode: depth` (safe fallback)

`research_mode` governs corroboration behavior in Stage 5. In `breadth` mode, the Corroborator applies lighter corroboration to qualitative claims, freeing search budget for broader entity coverage.

### Stage 2: Source Discoverer
```

**Step 2: Run the Stage 1 tests to verify they pass**

Run:
```
pytest tests/test_researcher_breadth_mode.py::test_breadth_mode_selection_exists tests/test_researcher_breadth_mode.py::test_breadth_mode_after_question_type_classifier tests/test_researcher_breadth_mode.py::test_breadth_mode_survey_trigger tests/test_researcher_breadth_mode.py::test_breadth_mode_depth_override -v
```

Expected: **All 4 tests PASS.** The Stage 5 tests (the other 4) should still fail — that's correct, we haven't added Stage 5 content yet.

**Step 3: Run the full existing test suite to check for regressions**

Run:
```
pytest tests/test_task7_researcher_verification.py tests/test_researcher_iterative_deepening.py -v
```

Expected: `test_task7_researcher_verification.py::TestFileLength::test_not_too_long` and `test_task7_researcher_verification.py::TestFileLength::test_approximate_target` **may fail** because the file is now ~340 lines (Step D added ~8 lines) — still under 350 so they should pass. All other tests should pass. If the file length tests fail, don't fix them yet — Task 3 handles that.

**Step 4: Commit**

```
git add agents/researcher.md && git commit -m "feat: add research mode selection (Step D) to researcher Stage 1 (#46)"
```

---

## Task 3: Add breadth mode corroboration logic to Stage 5 (Corroborator)

**Files:**
- Modify: `agents/researcher.md` (insert into Stage 5, between the heading and the existing steps)
- Modify: `tests/test_task7_researcher_verification.py` (raise file length thresholds)

**Step 1: Insert breadth mode preamble into Stage 5**

In `agents/researcher.md`, find this exact text (Stage 5, lines 215–224):

```
### Stage 5: Corroborator

For every Low or Medium confidence claim:

1. Search for a second independent source that confirms or contradicts it
2. If confirmed by a second source: upgrade confidence, increment `corroboration_count`
3. If contradicted: flag the contradiction, keep Low confidence, note both sources
4. If no second source found after a targeted search: mark as "single-source, unverified" — do not upgrade

Never upgrade confidence without evidence. A claim only becomes High confidence when a primary source or 2+ independent secondary sources confirm it.
```

Replace it with:

```
### Stage 5: Corroborator

**Breadth mode exception (when `research_mode: breadth`):**

Before running the standard corroboration loop below, classify each Low or Medium confidence claim as **numeric/financial** or **qualitative**:

- **Numeric/financial claims** — dollar amounts, percentages, statistics, dates, rankings, index scores → proceed to full corroboration below (same as depth mode)
- **Qualitative claims** — descriptions, lifestyle observations, cultural assessments, general characterizations, subjective evaluations → accept at medium confidence from a single credible source, skip corroboration. Flag as `single-source, medium confidence, breadth-mode`
- If a claim cannot be clearly classified as numeric vs qualitative → treat it as numeric and corroborate (err on the side of accuracy)

In `research_mode: depth` (the default), skip the classification above and corroborate all claims as usual.

**Standard corroboration (all modes for numeric claims, depth mode for all claims):**

For every Low or Medium confidence claim:

1. Search for a second independent source that confirms or contradicts it
2. If confirmed by a second source: upgrade confidence, increment `corroboration_count`
3. If contradicted: flag the contradiction, keep Low confidence, note both sources
4. If no second source found after a targeted search: mark as "single-source, unverified" — do not upgrade

Never upgrade confidence without evidence. A claim only becomes High confidence when a primary source or 2+ independent secondary sources confirm it.
```

**Step 2: Run the full breadth mode test suite**

Run:
```
pytest tests/test_researcher_breadth_mode.py -v
```

Expected: **All 8 tests PASS.**

**Step 3: Update file length thresholds**

The researcher file is now ~352 lines. The thresholds in `tests/test_task7_researcher_verification.py` need to be raised.

In `tests/test_task7_researcher_verification.py`, make these three changes:

1. Find `assert line_count < 350` (line 119) and replace with `assert line_count < 370`
2. Find the comment on line 118 `"""File must be under 350 lines (grew from ~237 to ~322 after quality loop additions)."""` and replace with `"""File must be under 370 lines (grew from ~237 to ~352 after quality loop + breadth mode additions)."""`
3. Find `assert 280 <= line_count <= 350` (line 138) and replace with `assert 280 <= line_count <= 370`
4. Find the docstring on lines 132-136 and update the target band description — change `280–350` to `280–370` and update the explanation:
   - Old: `"""File should be approximately 280–350 lines after quality loop additions.`
   - New: `"""File should be approximately 280–370 lines after quality loop + breadth mode additions.`
5. Find the assertion message on line 139-141 — change `280–350` to `280–370`:
   - Old: `f"File is {line_count} lines — outside the 280–350 target band. "` and `f"Expected approximately 280–350 after quality loop additions."`
   - New: `f"File is {line_count} lines — outside the 280–370 target band. "` and `f"Expected approximately 280–370 after quality loop + breadth mode additions."`
6. Find the class docstring `"""File should be ~280–350 lines. Hard fail if >350 or <200."""` and replace with `"""File should be ~280–370 lines. Hard fail if >370 or <200."""`

**Step 4: Run the full test suite**

Run:
```
pytest tests/test_researcher_breadth_mode.py tests/test_task7_researcher_verification.py tests/test_researcher_iterative_deepening.py -v
```

Expected: **All tests PASS** — 8 breadth mode tests + all verification tests + all iterative deepening tests.

**Step 5: Commit**

```
git add agents/researcher.md tests/test_task7_researcher_verification.py && git commit -m "feat: add breadth mode corroboration logic to researcher Stage 5 (#46)"
```

---

## Done Checklist

After all 3 tasks, verify:

- [ ] `pytest tests/test_researcher_breadth_mode.py -v` — 8/8 pass
- [ ] `pytest tests/test_task7_researcher_verification.py -v` — all pass
- [ ] `pytest tests/test_researcher_iterative_deepening.py -v` — all pass
- [ ] `git log --oneline -3` shows 3 commits for this feature
- [ ] `agents/researcher.md` has Step D in Stage 1 mentioning `research_mode: breadth`
- [ ] `agents/researcher.md` has breadth mode exception in Stage 5 mentioning `breadth-mode` flag