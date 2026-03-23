# Writer-Formatter Tier-Aware Hedging Implementation Plan (#40)

> **Execution:** Use the subagent-driven-development workflow to implement this plan.

**Goal:** Make the writer-formatter's Stage 3.5 (Confidence-Hedge Audit) check source tiers before inserting hedges — stop applying "reportedly" to peer-reviewed studies and institutional data.

**Architecture:** Single-file agent change to `agents/writer-formatter.md`. Stage 3.5 step 5 currently inserts hedge qualifiers uniformly regardless of source tier. We add a source-tier gate: primary/secondary source claims are protected from "reportedly" (the writer's Stage 4 already handles tier-appropriate hedging for these). Tertiary source claims and inference claims keep current behavior. This is a simplified tier gate — not a full language mapping.

**Tech Stack:** Markdown agent files, Python structural tests (pytest)

---

## Task 1: Write structural tests (TDD red phase)

**Context for the implementer:** We're writing tests first. These tests assert that the writer-formatter's Stage 3.5 section contains tier-aware hedging language. They will all FAIL right now because the current Stage 3.5 has no tier-awareness. That's the point — red phase of TDD.

**Files:**
- Create: `tests/test_writer_formatter_tier_hedging.py`

**Step 1: Create the test file**

Create `tests/test_writer_formatter_tier_hedging.py` with exactly this content:

```python
"""
Structural tests for writer-formatter tier-aware hedging (#40).
Validates that Stage 3.5 (Confidence-Hedge Audit) checks source tiers
before inserting hedges — protecting primary/secondary claims from
inappropriate "reportedly" insertion.

Fixes #40: writer-formatter applies "reportedly" uniformly regardless of source tier.
"""

from functools import lru_cache
from pathlib import Path

SPEC_FILE = Path(__file__).parent.parent / "agents" / "writer-formatter.md"


@lru_cache(maxsize=None)
def _content() -> str:
    assert SPEC_FILE.exists(), f"File not found: {SPEC_FILE}"
    return SPEC_FILE.read_text(encoding="utf-8")


def _stage_35_section() -> str:
    """Extract Stage 3.5 content (between 'Stage 3.5' and 'Stage 4')."""
    c = _content()
    start = c.index("Stage 3.5")
    end = c.index("Stage 4: Generate CLAIMS TO VERIFY")
    return c[start:end]


def test_tier_check_exists_in_stage_35() -> None:
    """Stage 3.5 must contain source-tier or tier-aware language."""
    section = _stage_35_section()
    has_tier_language = (
        "source tier" in section.lower()
        or "tier-aware" in section.lower()
        or "source-tier" in section.lower()
        or "primary" in section.lower() and "secondary" in section.lower()
    )
    assert has_tier_language, (
        "Stage 3.5 must contain source-tier check language — "
        "expected 'source tier', 'tier-aware', or 'primary'/'secondary'"
    )


def test_primary_secondary_protected() -> None:
    """Stage 3.5 must protect primary/secondary source claims from 'reportedly'."""
    section = _stage_35_section()
    has_protection = (
        "primary" in section.lower()
        and "secondary" in section.lower()
        and (
            "do not" in section.lower()
            or "skip" in section.lower()
            or "protect" in section.lower()
            or "leave" in section.lower()
        )
    )
    assert has_protection, (
        "Stage 3.5 must mention that primary/secondary source claims "
        "are protected from 'reportedly' or similar weak hedges"
    )


def test_tertiary_still_hedged() -> None:
    """Stage 3.5 must mention that tertiary source claims still get hedged."""
    section = _stage_35_section()
    has_tertiary = "tertiary" in section.lower()
    assert has_tertiary, (
        "Stage 3.5 must mention that tertiary source claims "
        "still receive hedge insertion as before"
    )


def test_tier_check_before_hedge_insertion() -> None:
    """The tier check must appear within Stage 3.5 — between 'Stage 3.5' and 'Stage 4'."""
    c = _content()
    stage35_start = c.index("Stage 3.5")
    stage4_start = c.index("Stage 4: Generate CLAIMS TO VERIFY")
    # Find tier language position — must be between Stage 3.5 and Stage 4
    tier_keywords = ["source tier", "primary", "tertiary"]
    found_in_stage_35 = False
    for keyword in tier_keywords:
        pos = c.lower().find(keyword, stage35_start)
        if pos != -1 and pos < stage4_start:
            found_in_stage_35 = True
            break
    assert found_in_stage_35, (
        "Tier check language must appear within Stage 3.5 section "
        "(between 'Stage 3.5' heading and 'Stage 4' heading)"
    )


def test_inference_unchanged() -> None:
    """Stage 3.5 must mention that inference claims are unchanged by the tier check."""
    section = _stage_35_section()
    has_inference = (
        "inference" in section.lower()
        and (
            "unchanged" in section.lower()
            or "regardless" in section.lower()
            or "still" in section.lower()
            or "current" in section.lower()
        )
    )
    assert has_inference, (
        "Stage 3.5 must mention that inference claims keep current "
        "behavior regardless of source tier"
    )
```

**Step 2: Run tests to verify they FAIL**

Run:
```bash
python -m pytest tests/test_writer_formatter_tier_hedging.py -v
```

Expected: All 5 tests FAIL. The current Stage 3.5 has no tier-awareness, so every assertion about tier language will fail. This is correct — red phase.

**Step 3: Commit the failing tests**

```bash
git add tests/test_writer_formatter_tier_hedging.py && git commit -m "test: add structural tests for writer-formatter tier-aware hedging (red phase, #40)"
```

---

## Task 2: Add tier-aware hedging logic to Stage 3.5

**Context for the implementer:** The writer-formatter's Stage 3.5 is at lines 147–167 of `agents/writer-formatter.md`. Step 5 (line 159) currently says "If **not** hedged, insert a minimal qualifier by confidence tier:" and then lists the same hedge for all sources. We need to add a source-tier check before the hedge insertion so that primary/secondary source claims are protected from "reportedly."

**Files:**
- Modify: `agents/writer-formatter.md` (lines 159–164)

**Step 1: Replace step 5 with tier-aware version**

In `agents/writer-formatter.md`, find this exact text (lines 159–164):

```
5. If **not** hedged, insert a minimal qualifier by confidence tier:
   - `medium` → Prepend `reportedly` before the specific value, or insert `(reported)`
     immediately after it.
   - `low` → Prepend `According to unconfirmed reports,` before the sentence.
   - `inference` → Ensure inferential framing — if absent, prepend `Evidence suggests`
     to the sentence.
```

Replace it with:

```
5. If **not** hedged, check the claim's **source tier** (from the S-number metadata
   in Stage 1) before inserting a qualifier:
   - **Primary/Secondary source** (academic, institutional, established press) with
     confidence `medium`: Do **not** insert `reportedly` or similar weak hedges.
     The writer's Stage 4 should have already applied tier-appropriate language
     ("research indicates," "a study found"). If it didn't, leave the prose as-is —
     over-hedging strong evidence is worse than under-hedging it.
   - **Tertiary source** (blogs, aggregators, vendor content) with confidence `medium`:
     Proceed with current hedge insertion — prepend `reportedly` before the specific
     value, or insert `(reported)` immediately after it.
   - `low` (any source tier) → Prepend `According to unconfirmed reports,` before the
     sentence.
   - `inference` (unchanged — current behavior regardless of source tier) → Ensure
     inferential framing — if absent, prepend `Evidence suggests` to the sentence.
   - If source tier is missing or ambiguous, fall back to current behavior (insert the
     hedge). Better to over-hedge an unknown claim than to leave a weak-source claim
     unhedged.
```

**Step 2: Run all 5 structural tests to verify they PASS**

Run:
```bash
python -m pytest tests/test_writer_formatter_tier_hedging.py -v
```

Expected: All 5 tests PASS. The new text contains "source tier", "primary", "secondary", "tertiary", "do not", and "inference" with "unchanged" / "regardless" — satisfying every assertion.

**Step 3: Commit**

```bash
git add agents/writer-formatter.md && git commit -m "feat: add tier-aware hedging to writer-formatter Stage 3.5 — protect primary/secondary claims from 'reportedly' (#40)"
```

---

## Task 3: Run full test suite and final commit

**Context for the implementer:** We need to make sure nothing else broke. The writer-formatter has existing tests in `tests/test_writer_formatter_degraded_mode.py` that check Stage 0.5 degraded mode behavior. Our change to Stage 3.5 should not affect those tests. Run the full suite to be sure.

**Files:**
- No new files — verification only

**Step 1: Run the full test suite**

Run:
```bash
python -m pytest tests/ -v
```

Expected: All tests pass. In particular:
- `tests/test_writer_formatter_tier_hedging.py` — all 5 PASS (our new tests)
- `tests/test_writer_formatter_degraded_mode.py` — all 7 PASS (existing tests, unaffected)

**Step 2: Verify the change is scoped correctly**

Run:
```bash
git diff HEAD~1 --stat
```

Expected: Only `agents/writer-formatter.md` changed. Approximately 8–14 lines added (replacing the 6 original lines of step 5 with ~14 tier-aware lines).

**Step 3: Tag the completion**

If everything passes, the feature is done. No further action needed — the two previous commits already captured the test and implementation.

---

## Summary

| Task | What | Files | Tests |
|------|------|-------|-------|
| 1 | Write structural tests (red phase) | Create `tests/test_writer_formatter_tier_hedging.py` | 5 tests, all FAIL |
| 2 | Add tier-aware hedging to Stage 3.5 | Modify `agents/writer-formatter.md` | 5 tests, all PASS |
| 3 | Run full test suite, verify no regressions | None | All tests PASS |

**Total commits:** 2 (test commit + implementation commit)
**Total files changed:** 2 (1 new test file + 1 modified agent file)
**Estimated time:** 10–15 minutes
