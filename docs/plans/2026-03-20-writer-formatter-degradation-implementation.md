# Writer-Formatter Graceful Degradation Implementation Plan

> **Execution:** Use the subagent-driven-development workflow to implement this plan.

**Goal:** Make the writer-formatter pass through prose with a notice instead of halting when the source corpus is missing (fixes #44).

**Architecture:** Single-file agent change to `agents/writer-formatter.md` — add a Stage 0.5 detection step that checks for source corpus markers, and a Degraded Mode section that emits the writer's prose unchanged with a citation-unavailable notice. One prerequisite fix: add Rule 9 (Two-Path Doctrine from #45) to `context/coordinator-routing.md`, which was lost during the context refactor.

**Tech Stack:** Markdown agent files, Python structural tests (pytest)

---

## Task 1: Add Rule 9 (Two-Path Doctrine) to coordinator-routing.md

**Context for the implementer:** Commit `7a07b66` added Rule 9 to the old `context/specialists-instructions.md`. Then commit `8c614d1` refactored that file into `context/coordinator-routing.md` — but dropped Rule 9 in the process. The current `coordinator-routing.md` has Rules 1–8. We're restoring the missing Rule 9, not creating a new rule.

**Files:**
- Modify: `context/coordinator-routing.md` (insert after line 77)

**Step 1: Add Rule 9 after the formatter-invisibility paragraph**

In `context/coordinator-routing.md`, find this text (line 77):

```
The formatter is invisible to the user — do not mention it in narration unless the user asks about the pipeline. HANDOFF narration should say "✅ Research complete — normalizing format..." (not "passing to formatter").
```

Insert the following **after** that paragraph and its trailing blank line, **before** the `## Available Specialists` heading:

```markdown
**Rule 9 — Two-Path Doctrine**: Rules 5–8 assume both formatter inputs are available. This is always true in **recipe pipelines** (context variables pass handoffs between steps). In **ad-hoc coordinator mode**, re-sending ~15K token research output to formatters defeats delegation's token-conservation purpose. Apply these paths:

| Mode | Formatters | Why |
|------|-----------|-----|
| **Recipe pipeline** | Always run (Rules 5–8 in full) | Context variables handle dual inputs between steps. No token cost. |
| **Ad-hoc coordinator** | Run only for intermediate steps | Re-sending large payloads to formatters at the terminal step wastes tokens. |

**Ad-hoc coordinator rules:**
- **Researcher-formatter (Rule 5):** Always run. It's single-input (research output only) and lightweight.
- **Writer-formatter (Rule 6):** Skip when writer output goes directly to the user. The writer produces readable prose with inline `> *Sources:*` attributions — this is sufficient for human consumption. Run only when writer output feeds another specialist downstream.
- **DA-formatter (Rule 8):** Always run when DA output feeds the writer. The writer needs canonical ANALYSIS OUTPUT to function correctly.
- **Prioritizer-formatter (Rule 7):** Skip when output goes directly to the user. Run when output feeds the writer.

**The test:** "Does the next consumer need canonical structured format?" If yes → formatter runs. If the next consumer is a human reading prose → formatter is optional.

```

**Step 2: Verify the edit**

Run: `grep -n "Rule 9" context/coordinator-routing.md`

Expected output: a line showing `**Rule 9 — Two-Path Doctrine**:` with a line number between 78 and 80.

**Step 3: Commit**

```bash
git add context/coordinator-routing.md && git commit -m "fix: restore Rule 9 (Two-Path Doctrine) lost during context refactor (#45)"
```

---

## Task 2: Write structural tests for writer-formatter degraded mode

**Context for the implementer:** We're writing tests FIRST (TDD red phase). All 7 tests will fail because the degraded mode sections don't exist in `agents/writer-formatter.md` yet. That's the point — we'll make them pass in Tasks 3 and 4.

**Files:**
- Create: `tests/test_writer_formatter_degraded_mode.py`

**Step 1: Create the test file**

Create `tests/test_writer_formatter_degraded_mode.py` with this exact content:

```python
"""
Structural tests for writer-formatter degraded mode (graceful degradation).
Validates that the writer-formatter agent file contains degraded mode
detection, pass-through behavior, and citation-unavailable notice text.

Fixes #44: writer-formatter halts in ad-hoc mode when source corpus is missing.
"""

from functools import lru_cache
from pathlib import Path

SPEC_FILE = Path(__file__).parent.parent / "agents" / "writer-formatter.md"


@lru_cache(maxsize=None)
def _content() -> str:
    assert SPEC_FILE.exists(), f"File not found: {SPEC_FILE}"
    return SPEC_FILE.read_text(encoding="utf-8")


def test_degraded_mode_section_exists() -> None:
    """A 'Stage 0.5' or 'Degraded Mode' section heading must exist."""
    c = _content()
    assert "Stage 0.5" in c or "Degraded Mode" in c


def test_degraded_mode_detection_before_stage1() -> None:
    """The detection step must come before Stage 1 in the file."""
    c = _content()
    assert c.index("Stage 0.5") < c.index("Stage 1: Extract source claims")


def test_degraded_mode_checks_research_output_marker() -> None:
    """Stage 0.5 must mention RESEARCH OUTPUT as a detection marker."""
    c = _content()
    stage05_section = c.split("Stage 0.5")[1].split("Stage 1")[0]
    assert "RESEARCH OUTPUT" in stage05_section


def test_degraded_mode_checks_analysis_output_marker() -> None:
    """Stage 0.5 must mention ANALYSIS OUTPUT as a detection marker."""
    c = _content()
    stage05_section = c.split("Stage 0.5")[1].split("Stage 1")[0]
    assert "ANALYSIS OUTPUT" in stage05_section


def test_degraded_mode_notice_text() -> None:
    """The exact citation-unavailable notice must appear in the file."""
    assert "Citation block omitted" in _content()


def test_degraded_mode_pass_through() -> None:
    """Degraded mode must describe passing through the writer's prose unchanged."""
    c = _content()
    has_pass_through = (
        "pass-through" in c.lower()
        or "pass through" in c.lower()
        or "verbatim" in c.lower()
        or "unchanged" in c.lower()
    )
    assert has_pass_through, "Degraded mode must mention pass-through/verbatim/unchanged"


def test_full_mode_still_exists() -> None:
    """Stage 1 two-input contract language must still be present (full mode intact)."""
    c = _content()
    assert "You receive two inputs" in c
    assert "Writer output" in c
    assert "Original source material" in c
```

**Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_writer_formatter_degraded_mode.py -v`

Expected: 5 of 7 tests FAIL. The two that might pass are `test_degraded_mode_pass_through` (if the existing "no pass-through mode" text matches the loose check) and `test_full_mode_still_exists` (Stage 1 text already exists). The other 5 must fail — "Stage 0.5" and "Citation block omitted" don't exist yet.

**Step 3: Commit the red tests**

```bash
git add tests/test_writer_formatter_degraded_mode.py && git commit -m "test: add structural tests for writer-formatter degraded mode (red phase, #44)"
```

---

## Task 3: Add Stage 0.5 detection block to writer-formatter.md

**Context for the implementer:** Stage 0 (the `Parsed:` line) ends at line 57. Stage 1 (extract source claims) starts at line 59. We're inserting a new Stage 0.5 between them that checks whether the source corpus was provided.

**Files:**
- Modify: `agents/writer-formatter.md` (insert between lines 57–59, update line 38)

**Step 1: Update the Core Principle section**

In `agents/writer-formatter.md`, find this exact line (line 38):

```
There is no pass-through mode.
```

Replace it with:

```
In full mode (source corpus present), there is no pass-through — every structural block
is required. See **Degraded Mode** below for behavior when source corpus is absent.
```

**Step 2: Insert Stage 0.5 after Stage 0**

Find this exact text (lines 56–59):

```
That single line is your entire Stage 0. Nothing before it. Not "Here is the formatted
output." Not a heading. The `Parsed:` line.

### Stage 1: Extract source claims
```

Replace it with:

```
That single line is your entire Stage 0. Nothing before it. Not "Here is the formatted
output." Not a heading. The `Parsed:` line.

### Stage 0.5: Detect operating mode

Before proceeding to Stage 1, check whether the source corpus was provided in your
input. Look for any of these block headers:

- `RESEARCH OUTPUT`
- `ANALYSIS OUTPUT`
- `CompetitiveAnalysisOutput`

**If found → full mode.** Proceed with Stage 1 through Stage 5 as written below.

**If absent → degraded mode.** The source corpus is not available (this typically
happens in ad-hoc coordinator sessions where only the writer's prose was forwarded).
Skip Stages 1–5 entirely and follow the **Degraded Mode** instructions at the end of
this document.

### Stage 1: Extract source claims
```

**Step 3: Run tests to check progress**

Run: `python3 -m pytest tests/test_writer_formatter_degraded_mode.py -v`

Expected: 5 of 7 tests now PASS:
- `test_degraded_mode_section_exists` → PASS
- `test_degraded_mode_detection_before_stage1` → PASS
- `test_degraded_mode_checks_research_output_marker` → PASS
- `test_degraded_mode_checks_analysis_output_marker` → PASS
- `test_full_mode_still_exists` → PASS

Still failing (will be fixed in Task 4):
- `test_degraded_mode_notice_text` → FAIL ("Citation block omitted" not present yet)
- `test_degraded_mode_pass_through` → may PASS or FAIL depending on text matching

**Step 4: Commit**

```bash
git add agents/writer-formatter.md && git commit -m "feat: add Stage 0.5 source corpus detection to writer-formatter (#44)"
```

---

## Task 4: Add Degraded Mode section and update constraints

**Context for the implementer:** We're adding the Degraded Mode section that Stage 0.5 routes to when the source corpus is absent. It goes between the `## Output Format` section and `## What You Do Not Do`. We also need to update one line in "What You Do Not Do" that contradicts degraded mode.

**Files:**
- Modify: `agents/writer-formatter.md` (insert before "What You Do Not Do", update constraints)

**Step 1: Insert the Degraded Mode section**

In `agents/writer-formatter.md`, find this exact text (the separator and heading before "What You Do Not Do"):

```
---

## What You Do Not Do
```

Replace it with:

```
---

## Degraded Mode (source corpus absent)

When Stage 0.5 determines the source corpus is absent, skip Stages 1–5 entirely.

1. **Emit the `Parsed:` line** (Stage 0 always fires):
   ```
   Parsed: 0 claims | input=writer-only | format=[format] | audience=[audience]
   ```

2. **Pass through the writer's prose unchanged** — do not reformat, rewrite, restructure,
   strip preamble, or insert hedges. Emit the prose exactly as received.

3. **Append the citation notice** at the very end:
   ```
   ---
   [Citation block omitted — source corpus not available in this session.
   Run via research-chain recipe for full citations and source traceability.]
   ```

That's the entire degraded mode output: `Parsed:` line, verbatim prose, notice. Nothing else.

---

## What You Do Not Do
```

**Step 2: Update the constraints for degraded mode**

In the same file, find this line in the "What You Do Not Do" section:

```
- Skip any structural block — all five are required every time
```

Replace it with:

```
- Skip any structural block in full mode — all five are required every time
```

**Step 3: Run all tests to verify everything passes**

Run: `python3 -m pytest tests/test_writer_formatter_degraded_mode.py -v`

Expected: ALL 7 tests PASS.

**Step 4: Run the full test suite to check for regressions**

Run: `python3 -m pytest tests/ -v`

Expected: No regressions. All pre-existing tests still pass.

**Step 5: Commit**

```bash
git add agents/writer-formatter.md && git commit -m "feat: add degraded mode pass-through with citation notice to writer-formatter (#44)"
```

---

## Verification

After all 4 tasks are complete, confirm the implementation by running:

```bash
python3 -m pytest tests/test_writer_formatter_degraded_mode.py -v
```

All 7 tests must pass:
```
test_degraded_mode_section_exists          PASSED
test_degraded_mode_detection_before_stage1 PASSED
test_degraded_mode_checks_research_output_marker PASSED
test_degraded_mode_checks_analysis_output_marker PASSED
test_degraded_mode_notice_text             PASSED
test_degraded_mode_pass_through            PASSED
test_full_mode_still_exists                PASSED
```

Then verify the commit history shows 4 clean commits:
```bash
git log --oneline -4
```

Expected (newest first):
```
feat: add degraded mode pass-through with citation notice to writer-formatter (#44)
feat: add Stage 0.5 source corpus detection to writer-formatter (#44)
test: add structural tests for writer-formatter degraded mode (red phase, #44)
fix: restore Rule 9 (Two-Path Doctrine) lost during context refactor (#45)
```

**Live validation** (manual, not automated): Start an ad-hoc coordinator session and trigger the writer-formatter without source corpus. Expected result: prose + citation notice returned instead of the formatter halting.
