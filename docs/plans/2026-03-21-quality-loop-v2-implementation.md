# Quality Loop v2 (Simplified) Implementation Plan

> **Execution:** Use the subagent-driven-development workflow to implement this plan.

**Goal:** Reduce quality loop iteration time from ~3 hours to ~90 minutes by caching competitor baselines, running only 3 topics per iteration, and caching the gap report for instant diagnosis.

**Architecture:** The existing single-recipe `quality-loop.yaml` gains two pre-loop steps (`initial-eval` runs the full competitive evaluation once, `cache-competitors` saves competitor outputs to disk) and one new loop-body step (`select-topics` picks 2 worst + 1 regression check). The loop-body `evaluate` step passes cached competitor paths and selected topic IDs to `quality-eval.yaml`, which filters accordingly. Competitor re-runs are eliminated; topic count drops from 5 to 3.

**Tech Stack:** Amplifier recipe YAML, bash steps with `parse_json: true`, pytest structural tests, `python3` for all parsing (no `grep -oP` — macOS BSD grep incompatible).

**Design doc:** `docs/plans/2026-03-21-quality-loop-v2-design.md`

**Deferred to v2.1 (NOT in this plan):**
- Partial pipeline re-runs (re-run from point of change)
- Per-stage output caching (research_output, formatted_analysis, etc.)
- Specialist-to-position mapping and content hash tracking
- Splitting into separate baseline/loop recipe files

---

## Recipe Structure: Before vs After

**Before (v1) — top-level steps:**
```
steps:
  1. improvement-loop (while_condition, 5 substeps)
  2. termination-summary
```

**After (v2) — top-level steps:**
```
steps:
  1. initial-eval          ← NEW (runs full quality-eval.yaml once)
  2. cache-competitors     ← NEW (saves competitor outputs to cache dir)
  3. improvement-loop      (while_condition, 6 substeps — select-topics added)
  4. termination-summary
```

**Before (v1) — loop body steps:**
```
  evaluate → aggregate-diagnose → fix → check → log-round
```

**After (v2) — loop body steps:**
```
  select-topics → evaluate → aggregate-diagnose → fix → check → log-round
  ↑ NEW           ↑ MODIFIED (passes cache_dir + selected_topic_ids)
```

---

### Task 1: Add Cache Directory to `.gitignore`

**Why:** Cache files (competitor outputs, scores) are generated per-run and must never be committed. This must be done first so no subsequent task accidentally stages cache files.

**Files:**
- Modify: `.gitignore`

**Step 1: Add the cache directory exclusion**

Add this block to the end of `.gitignore`:

```gitignore

# Quality loop evaluation cache (per-run, disposable)
specs/evaluation/cache/
```

Place it after the existing `# OS` section (after line 20). Keep the blank line before the comment for readability.

**Step 2: Verify the pattern works**

Run:
```bash
mkdir -p specs/evaluation/cache/test_run/competitors
touch specs/evaluation/cache/test_run/competitors/test.md
git status --short specs/evaluation/cache/
```
Expected: No output (the directory is ignored).

**Step 3: Clean up and commit**

Run:
```bash
rm -rf specs/evaluation/cache/test_run
git add .gitignore && git commit -m "chore: add specs/evaluation/cache/ to .gitignore for quality loop v2"
```

---

### Task 2: Write Failing Tests for v2 Recipe Structure

**Why:** TDD red phase. We write all the tests that the v2 recipe must satisfy BEFORE modifying the recipe. These tests will fail now (good — that's TDD). We also update existing tests whose assertions will change (version number, step ordering, required step IDs).

**Files:**
- Modify: `tests/test_quality_loop_recipe.py`

**Step 1: Update the version test**

The recipe version bumps from `1.0.0` to `2.0.0`. Find and update the existing `test_recipe_version` function.

Find this (around line 54):
```python
def test_recipe_version() -> None:
    """Recipe version must be '1.0.0'."""
    recipe = load_recipe()
    assert recipe["version"] == "1.0.0", (
        f"Expected version='1.0.0', got {recipe.get('version')!r}"
    )
```

Replace with:
```python
def test_recipe_version() -> None:
    """Recipe version must be '2.0.0'."""
    recipe = load_recipe()
    assert recipe["version"] == "2.0.0", (
        f"Expected version='2.0.0', got {recipe.get('version')!r}"
    )
```

**Step 2: Add context test for `topics_per_iteration`**

Add this test right after `test_context_has_evaluation_mode` (after line 125):

```python


def test_context_has_topics_per_iteration() -> None:
    """Context must have 'topics_per_iteration' defaulting to 3."""
    recipe = load_recipe()
    context = recipe.get("context", {})
    assert "topics_per_iteration" in context, (
        "Context must have 'topics_per_iteration'"
    )
    assert context["topics_per_iteration"] == 3, (
        f"topics_per_iteration must default to 3, got {context['topics_per_iteration']!r}"
    )
```

**Step 3: Add helper function for top-level steps**

Add this helper right after the `test_context_has_topics_per_iteration` test, before the `# While-loop structure` section (before the line `# ---------------------------------------------------------------------------` that precedes `def test_has_while_condition`):

```python


# ---------------------------------------------------------------------------
# Top-level step helpers
# ---------------------------------------------------------------------------


def _get_top_level_step(recipe: dict, step_id: str) -> dict:
    """Get a top-level step by ID."""
    for step in recipe.get("steps", []):
        if step.get("id") == step_id:
            return step
    raise AssertionError(f"Top-level step '{step_id}' not found")


def _top_level_step_index(recipe: dict, step_id: str) -> int:
    """Get the index of a top-level step by ID."""
    step_ids = [s.get("id") for s in recipe.get("steps", [])]
    assert step_id in step_ids, (
        f"Step '{step_id}' not found in top-level steps, got: {step_ids}"
    )
    return step_ids.index(step_id)
```

**Step 4: Add tests for `initial-eval` top-level step**

Add these tests right after the new helper functions:

```python


# ---------------------------------------------------------------------------
# initial-eval step (top-level, before loop)
# ---------------------------------------------------------------------------


def test_has_initial_eval_step() -> None:
    """Recipe must have an 'initial-eval' top-level step."""
    recipe = load_recipe()
    step_ids = [s.get("id") for s in recipe.get("steps", [])]
    assert "initial-eval" in step_ids, (
        f"Recipe must have 'initial-eval' top-level step, got: {step_ids}"
    )


def test_initial_eval_invokes_quality_eval() -> None:
    """initial-eval must invoke quality-eval.yaml as a sub-recipe."""
    recipe = load_recipe()
    step = _get_top_level_step(recipe, "initial-eval")
    assert step.get("type") == "recipe", (
        f"initial-eval must be type='recipe', got {step.get('type')!r}"
    )
    recipe_ref = step.get("recipe", "")
    assert "quality-eval" in recipe_ref, (
        f"initial-eval must reference 'quality-eval', got {recipe_ref!r}"
    )


def test_initial_eval_passes_context() -> None:
    """initial-eval must pass evaluation_mode and target_score in context."""
    recipe = load_recipe()
    step = _get_top_level_step(recipe, "initial-eval")
    ctx = step.get("context", {})
    assert "evaluation_mode" in ctx, (
        "initial-eval context must include 'evaluation_mode'"
    )
    assert "target_score" in ctx, (
        "initial-eval context must include 'target_score'"
    )


def test_initial_eval_has_output() -> None:
    """initial-eval must declare an output variable."""
    recipe = load_recipe()
    step = _get_top_level_step(recipe, "initial-eval")
    assert "output" in step, "initial-eval must have an 'output' declaration"


def test_initial_eval_before_improvement_loop() -> None:
    """initial-eval must come before improvement-loop."""
    recipe = load_recipe()
    assert _top_level_step_index(recipe, "initial-eval") < _top_level_step_index(
        recipe, "improvement-loop"
    )
```

**Step 5: Add tests for `cache-competitors` top-level step**

Add these tests right after the initial-eval tests:

```python


# ---------------------------------------------------------------------------
# cache-competitors step (top-level, between initial-eval and loop)
# ---------------------------------------------------------------------------


def test_has_cache_competitors_step() -> None:
    """Recipe must have a 'cache-competitors' top-level step."""
    recipe = load_recipe()
    step_ids = [s.get("id") for s in recipe.get("steps", [])]
    assert "cache-competitors" in step_ids, (
        f"Recipe must have 'cache-competitors' top-level step, got: {step_ids}"
    )


def test_cache_competitors_is_bash() -> None:
    """cache-competitors must be type: bash."""
    recipe = load_recipe()
    step = _get_top_level_step(recipe, "cache-competitors")
    assert step.get("type") == "bash", (
        f"cache-competitors must be type='bash', got {step.get('type')!r}"
    )


def test_cache_competitors_writes_to_cache_dir() -> None:
    """cache-competitors command must reference specs/evaluation/cache/."""
    recipe = load_recipe()
    step = _get_top_level_step(recipe, "cache-competitors")
    command = step.get("command", "")
    assert "specs/evaluation/cache" in command, (
        "cache-competitors must write to 'specs/evaluation/cache/'"
    )


def test_cache_competitors_has_output() -> None:
    """cache-competitors must declare an output variable."""
    recipe = load_recipe()
    step = _get_top_level_step(recipe, "cache-competitors")
    assert "output" in step, "cache-competitors must have an 'output' declaration"


def test_cache_competitors_after_initial_eval() -> None:
    """cache-competitors must come after initial-eval."""
    recipe = load_recipe()
    assert _top_level_step_index(recipe, "initial-eval") < _top_level_step_index(
        recipe, "cache-competitors"
    )


def test_cache_competitors_before_improvement_loop() -> None:
    """cache-competitors must come before improvement-loop."""
    recipe = load_recipe()
    assert _top_level_step_index(recipe, "cache-competitors") < _top_level_step_index(
        recipe, "improvement-loop"
    )
```

**Step 6: Add tests for `select-topics` loop body step**

Add these tests right after the cache-competitors tests, before the existing `# Loop body steps` section:

```python


# ---------------------------------------------------------------------------
# select-topics step (inside loop body, before evaluate)
# ---------------------------------------------------------------------------


def test_loop_has_select_topics_step() -> None:
    """Loop body must include a 'select-topics' step."""
    recipe = load_recipe()
    step_ids = [s["id"] for s in _get_loop_steps(recipe)]
    assert "select-topics" in step_ids, (
        f"Loop body must include 'select-topics', got: {step_ids}"
    )


def test_select_topics_is_bash() -> None:
    """select-topics must be type: bash."""
    recipe = load_recipe()
    step = _get_loop_step(recipe, "select-topics")
    assert step.get("type") == "bash", (
        f"select-topics must be type='bash', got {step.get('type')!r}"
    )


def test_select_topics_has_parse_json() -> None:
    """select-topics must have parse_json: true."""
    recipe = load_recipe()
    step = _get_loop_step(recipe, "select-topics")
    assert step.get("parse_json") is True, (
        f"select-topics must have parse_json=true, got {step.get('parse_json')!r}"
    )


def test_select_topics_before_evaluate() -> None:
    """select-topics must come before evaluate in the loop body."""
    recipe = load_recipe()
    assert _loop_step_index(recipe, "select-topics") < _loop_step_index(
        recipe, "evaluate"
    )
```

**Step 7: Update the required loop step IDs test**

Find the existing `test_loop_has_required_step_ids` (around line 195):

```python
def test_loop_has_required_step_ids() -> None:
    """Loop body must include: evaluate, aggregate-diagnose, fix, check, log-round."""
    recipe = load_recipe()
    step_ids = [s["id"] for s in _get_loop_steps(recipe)]
    required = {"evaluate", "aggregate-diagnose", "fix", "check", "log-round"}
    missing = required - set(step_ids)
    assert not missing, f"Loop body missing required step IDs: {missing}"
```

Replace with:

```python
def test_loop_has_required_step_ids() -> None:
    """Loop body must include: select-topics, evaluate, aggregate-diagnose, fix, check, log-round."""
    recipe = load_recipe()
    step_ids = [s["id"] for s in _get_loop_steps(recipe)]
    required = {"select-topics", "evaluate", "aggregate-diagnose", "fix", "check", "log-round"}
    missing = required - set(step_ids)
    assert not missing, f"Loop body missing required step IDs: {missing}"
```

**Step 8: Add test for evaluate step referencing cache**

Add this test right after the existing `test_evaluate_passes_context` test (after line 279):

```python


def test_evaluate_passes_cache_context() -> None:
    """evaluate must pass cache_dir and selected_topic_ids in context."""
    recipe = load_recipe()
    step = _get_loop_step(recipe, "evaluate")
    ctx = step.get("context", {})
    assert "cache_dir" in ctx, "evaluate context must include 'cache_dir'"
    assert "selected_topic_ids" in ctx, (
        "evaluate context must include 'selected_topic_ids'"
    )
```

**Step 9: Add test for log-round cache fields**

Add this test right after the existing `test_log_round_does_not_use_grep_oP` test (after line 462):

```python


def test_log_round_includes_cache_fields() -> None:
    """log-round command must include cache-related fields."""
    recipe = load_recipe()
    step = _get_loop_step(recipe, "log-round")
    command = step.get("command", "")
    assert "topics_rerun" in command, (
        "log-round must include 'topics_rerun' field"
    )
    assert "competitors_cached" in command, (
        "log-round must include 'competitors_cached' field"
    )
```

**Step 10: Run tests to verify they fail**

Run:
```bash
cd /Users/chrispark/Projects/specialists/amplifier-research-specialist
python -m pytest tests/test_quality_loop_recipe.py -v 2>&1 | tail -30
```
Expected: Multiple failures. The new tests for `initial-eval`, `cache-competitors`, `select-topics`, `topics_per_iteration`, version `2.0.0`, and cache context should all FAIL. The existing tests that haven't been changed should still PASS (except `test_recipe_version` which now expects `2.0.0`).

Count the failures — there should be approximately 18-20 failing tests.

**Step 11: Commit the failing tests**

Run:
```bash
git add tests/test_quality_loop_recipe.py && git commit -m "test: add failing tests for quality-loop v2 structure (TDD red phase)"
```

---

### Task 3: Add `initial-eval` Step and Bump Version

**Why:** The first optimization — run the full competitive evaluation ONCE before the loop starts, instead of inside every iteration. This step is identical to the current in-loop `evaluate` step but placed before the `while_condition` so it runs exactly once. We also bump the version and add `topics_per_iteration` to context.

**Files:**
- Modify: `recipes/quality-loop.yaml`

**Step 1: Bump version and add `topics_per_iteration` to context**

In `recipes/quality-loop.yaml`, change line 3:

```yaml
version: "1.0.0"
```

to:

```yaml
version: "2.0.0"
```

And change the context block (lines 6-11) from:

```yaml
context:
  target_score: 8.0
  current_score: 0
  plateau_counter: 0
  converged: "false"
  evaluation_mode: "competitive"
```

to:

```yaml
context:
  target_score: 8.0
  current_score: 0
  plateau_counter: 0
  converged: "false"
  evaluation_mode: "competitive"
  topics_per_iteration: 3
```

**Step 2: Add `initial-eval` step before the improvement loop**

Insert this new step AFTER the `steps:` key and the section comment (after line 13), but BEFORE the `improvement-loop` step. The new content to insert between the `steps:` line and the existing `# QUALITY IMPROVEMENT LOOP` comment:

```yaml
  # ===========================================================================
  # PHASE A: INITIAL FULL EVALUATION (runs once)
  # ===========================================================================
  - id: "initial-eval"
    type: "recipe"
    recipe: "./quality-eval.yaml"
    context:
      evaluation_mode: "{{evaluation_mode}}"
      target_score: "{{target_score}}"
    output: "initial_eval_result"
    timeout: 21600
    on_error: "continue"

```

This is the same invocation pattern as the existing in-loop `evaluate` step (type: recipe, same recipe path, same context variables) but with a different output name (`initial_eval_result` instead of `eval_result`) so both can be referenced independently.

**Step 3: Run the relevant passing tests**

Run:
```bash
python -m pytest tests/test_quality_loop_recipe.py::test_recipe_version tests/test_quality_loop_recipe.py::test_context_has_topics_per_iteration tests/test_quality_loop_recipe.py::test_has_initial_eval_step tests/test_quality_loop_recipe.py::test_initial_eval_invokes_quality_eval tests/test_quality_loop_recipe.py::test_initial_eval_passes_context tests/test_quality_loop_recipe.py::test_initial_eval_has_output tests/test_quality_loop_recipe.py::test_initial_eval_before_improvement_loop -v
```
Expected: All 7 PASS.

**Step 4: Verify no existing tests broke**

Run:
```bash
python -m pytest tests/test_quality_loop_recipe.py -v 2>&1 | grep -E "PASSED|FAILED" | grep "FAILED"
```
Expected: Only the tests for features not yet implemented should fail (`cache-competitors`, `select-topics`, `evaluate_passes_cache_context`, `log_round_includes_cache_fields`). All previously-passing tests should still pass.

**Step 5: Commit**

Run:
```bash
git add recipes/quality-loop.yaml && git commit -m "feat: add initial-eval pre-loop step, bump to v2.0.0, add topics_per_iteration context"
```

---

### Task 4: Add `cache-competitors` Step

**Why:** After the initial full evaluation, we save the competitor results to a cache directory. Subsequent loop iterations reference this cache instead of re-running competitors (~25 min saved per iteration). The cache uses a timestamped `run_id` so multiple runs don't collide.

**Files:**
- Modify: `recipes/quality-loop.yaml`

**Step 1: Add the `cache-competitors` step**

Insert this step AFTER the `initial-eval` step and BEFORE the `# QUALITY IMPROVEMENT LOOP` comment block:

```yaml
  # ===========================================================================
  # PHASE A: CACHE COMPETITOR BASELINES
  # ===========================================================================
  - id: "cache-competitors"
    type: "bash"
    command: |
      RUN_ID=$(date +%Y%m%d_%H%M%S)
      CACHE_DIR="specs/evaluation/cache/${RUN_ID}"
      mkdir -p "${CACHE_DIR}/competitors"
      mkdir -p "${CACHE_DIR}/scores"

      # Save the full initial evaluation result for reference
      cat <<'__EVAL__' > "${CACHE_DIR}/initial_eval_result.txt"
      {{initial_eval_result}}
      __EVAL__

      # Write metadata
      cat <<EOF > "${CACHE_DIR}/metadata.json"
      {
        "run_id": "${RUN_ID}",
        "cache_dir": "${CACHE_DIR}",
        "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
        "competitors_cached": true,
        "topics_per_iteration": {{topics_per_iteration}}
      }
      EOF

      # Output cache info for subsequent steps
      cat <<EOF
      {
        "run_id": "${RUN_ID}",
        "cache_dir": "${CACHE_DIR}",
        "competitors_cached": true
      }
      EOF
    parse_json: true
    output: "cache_info"
    timeout: 60

```

**Step 2: Run the cache-competitors tests**

Run:
```bash
python -m pytest tests/test_quality_loop_recipe.py::test_has_cache_competitors_step tests/test_quality_loop_recipe.py::test_cache_competitors_is_bash tests/test_quality_loop_recipe.py::test_cache_competitors_writes_to_cache_dir tests/test_quality_loop_recipe.py::test_cache_competitors_has_output tests/test_quality_loop_recipe.py::test_cache_competitors_after_initial_eval tests/test_quality_loop_recipe.py::test_cache_competitors_before_improvement_loop -v
```
Expected: All 6 PASS.

**Step 3: Verify no regressions**

Run:
```bash
python -m pytest tests/test_quality_loop_recipe.py -v 2>&1 | grep "FAILED"
```
Expected: Only `select-topics`, `evaluate_passes_cache_context`, and `log_round_includes_cache_fields` tests still failing.

**Step 4: Commit**

Run:
```bash
git add recipes/quality-loop.yaml && git commit -m "feat: add cache-competitors step to save competitor baselines after initial eval"
```

---

### Task 5: Add `select-topics` Step Inside the Loop Body

**Why:** Instead of evaluating all 5 topics each iteration, we select only 3: the 2 worst-scoring topics (highest improvement potential) plus 1 well-scoring topic (regression check). This cuts per-iteration pipeline time from ~90 min to ~54 min.

**Files:**
- Modify: `recipes/quality-loop.yaml`

**Step 1: Add `select-topics` as the first step inside the loop body**

Find the loop body steps section inside the `improvement-loop` step. The loop body currently starts with the `evaluate` step:

```yaml
    steps:
      # --- Evaluate: invoke the competitive eval sub-recipe ---
      - id: "evaluate"
```

Insert the `select-topics` step BEFORE the `evaluate` step, so it becomes the first step in the loop body:

```yaml
    steps:
      # --- Select Topics: pick 2 worst + 1 regression check ---
      - id: "select-topics"
        type: "bash"
        command: |
          cat <<'__EVAL_DATA__' > /tmp/quality-loop-eval-data.txt
          {{initial_eval_result}}
          {{eval_result}}
          __EVAL_DATA__

          # Extract per-topic pipeline scores and select topics for this iteration
          python3 <<'__PYTHON__'
          import json, re

          with open("/tmp/quality-loop-eval-data.txt") as f:
              text = f.read()

          # Parse topic IDs and their scores from evaluation output
          # Look for patterns like "topic_id: X" with "pipeline_score: Y" or score tables
          topic_ids = ["factual-deep-dive", "strategy", "survey", "competitive-comparison", "technical-analysis"]
          scores = {}

          for tid in topic_ids:
              # Search for score patterns near each topic ID
              pattern = rf'{tid}.*?(?:pipeline[_ ]score|score)[:\s]*(\d+\.?\d*)'
              m = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
              if m:
                  scores[tid] = float(m.group(1))
              else:
                  # Default to 5.0 (neutral) if score not found
                  scores[tid] = 5.0

          # Sort by score ascending (worst first)
          sorted_topics = sorted(scores.items(), key=lambda x: x[1])

          # Select 2 worst + 1 best (regression check)
          topics_per_iteration = {{topics_per_iteration}}
          worst = [t[0] for t in sorted_topics[:2]]
          best = [t[0] for t in sorted_topics if t[0] not in worst][-1:]
          selected = worst + best

          # Ensure we have exactly topics_per_iteration topics
          selected = selected[:topics_per_iteration]

          result = {
              "selected_topic_ids": selected,
              "topic_scores": {t: s for t, s in sorted_topics},
              "selection_reason": f"2 worst: {worst}, 1 regression check: {best}"
          }
          print(json.dumps(result))
          __PYTHON__
        parse_json: true
        output: "selected_topics"
        timeout: 30

```

**Step 2: Run the select-topics tests**

Run:
```bash
python -m pytest tests/test_quality_loop_recipe.py::test_loop_has_select_topics_step tests/test_quality_loop_recipe.py::test_select_topics_is_bash tests/test_quality_loop_recipe.py::test_select_topics_has_parse_json tests/test_quality_loop_recipe.py::test_select_topics_before_evaluate tests/test_quality_loop_recipe.py::test_loop_has_required_step_ids -v
```
Expected: All 5 PASS.

**Step 3: Verify no regressions**

Run:
```bash
python -m pytest tests/test_quality_loop_recipe.py -v 2>&1 | grep "FAILED"
```
Expected: Only `evaluate_passes_cache_context` and `log_round_includes_cache_fields` still failing.

**Step 4: Commit**

Run:
```bash
git add recipes/quality-loop.yaml && git commit -m "feat: add select-topics step — picks 2 worst + 1 regression check topic per iteration"
```

---

### Task 6: Modify `evaluate` Step to Pass Cache and Topic Context

**Why:** The loop-body `evaluate` step currently calls `quality-eval.yaml` with no awareness of the cache or topic selection. We add `cache_dir` and `selected_topic_ids` to its context so `quality-eval.yaml` can filter topics and skip competitor re-runs. We also make a minimal change to `quality-eval.yaml` to accept the new context variables.

**Files:**
- Modify: `recipes/quality-loop.yaml` (evaluate step context)
- Modify: `recipes/quality-eval.yaml` (load-topics step to filter by selected_topic_ids)

**Step 1: Update the evaluate step's context in `quality-loop.yaml`**

Find the existing `evaluate` step inside the loop body (it's now the second step, after `select-topics`):

```yaml
      - id: "evaluate"
        type: "recipe"
        recipe: "./quality-eval.yaml"
        context:
          evaluation_mode: "{{evaluation_mode}}"
          target_score: "{{target_score}}"
        output: "eval_result"
        timeout: 21600
        on_error: "continue"
```

Replace the `context:` block to add cache and topic selection:

```yaml
      - id: "evaluate"
        type: "recipe"
        recipe: "./quality-eval.yaml"
        context:
          evaluation_mode: "{{evaluation_mode}}"
          target_score: "{{target_score}}"
          cache_dir: "{{cache_info.cache_dir}}"
          selected_topic_ids: "{{selected_topics.selected_topic_ids}}"
        output: "eval_result"
        timeout: 21600
        on_error: "continue"
```

**Step 2: Update `quality-eval.yaml` to accept `selected_topic_ids`**

In `recipes/quality-eval.yaml`, add the new context variables to the context block. Change lines 7-8 from:

```yaml
context:
  evaluation_mode: "competitive"   # competitive (vs competitors) or rubric (vs criteria)
  target_score: 8.0                # target aggregate score (used by Phase 2 loop)
```

to:

```yaml
context:
  evaluation_mode: "competitive"   # competitive (vs competitors) or rubric (vs criteria)
  target_score: 8.0                # target aggregate score (used by Phase 2 loop)
  cache_dir: ""                    # optional: path to cache dir for competitor baselines
  selected_topic_ids: ""           # optional: JSON list of topic IDs to evaluate (empty = all)
```

**Step 3: Update `quality-eval.yaml` load-topics step to filter**

Find the `load-topics` step in `recipes/quality-eval.yaml` (around lines 14-26):

```yaml
  - id: "load-topics"
    type: "bash"
    command: |
      uv run --with pyyaml python -c "
      import json, yaml
      with open('specs/evaluation/test-topics.yaml') as f:
          data = yaml.safe_load(f)
      topics = [t for t in data.get('topics', []) if t.get('profile') == 'competitive-eval']
      print(json.dumps(topics))
      "
    output: "topics"
    parse_json: true
    timeout: 10
```

Replace the command with a version that filters by `selected_topic_ids` when provided:

```yaml
  - id: "load-topics"
    type: "bash"
    command: |
      uv run --with pyyaml python -c "
      import json, yaml

      with open('specs/evaluation/test-topics.yaml') as f:
          data = yaml.safe_load(f)
      topics = [t for t in data.get('topics', []) if t.get('profile') == 'competitive-eval']

      # Filter to selected topics if provided (quality-loop v2 optimization)
      selected_raw = '{{selected_topic_ids}}'
      if selected_raw and selected_raw != '{{' + 'selected_topic_ids}}':
          try:
              selected = json.loads(selected_raw) if selected_raw.startswith('[') else []
              if selected:
                  topics = [t for t in topics if t['id'] in selected]
          except (json.JSONDecodeError, TypeError):
              pass  # Use all topics if parsing fails

      print(json.dumps(topics))
      "
    output: "topics"
    parse_json: true
    timeout: 10
```

The key trick: `'{{selected_topic_ids}}'` will be the literal string `{{selected_topic_ids}}` when the variable is empty/unset (Amplifier leaves unresolved variables as-is), so the check `selected_raw != '{{' + 'selected_topic_ids}}'` detects this. When called from the quality-loop with actual topic IDs, it will be a JSON array like `["factual-deep-dive", "strategy", "survey"]`.

**Step 4: Run the cache context test**

Run:
```bash
python -m pytest tests/test_quality_loop_recipe.py::test_evaluate_passes_cache_context -v
```
Expected: PASS.

**Step 5: Verify no regressions across both test files**

Run:
```bash
python -m pytest tests/test_quality_loop_recipe.py tests/test_quality_eval_recipe.py -v 2>&1 | grep "FAILED"
```
Expected: Only `test_log_round_includes_cache_fields` still failing in the quality-loop tests. All quality-eval tests should pass (the load-topics change is backward-compatible).

**Step 6: Commit**

Run:
```bash
git add recipes/quality-loop.yaml recipes/quality-eval.yaml && git commit -m "feat: pass cache_dir and selected_topic_ids to quality-eval, add topic filtering"
```

---

### Task 7: Update Observability — `log-round` and `termination-summary`

**Why:** The log-round step needs cache-related fields so we can verify the v2 optimizations are working. The termination summary should report cache usage. This is the last piece — after this, all tests pass.

**Files:**
- Modify: `recipes/quality-loop.yaml` (log-round step and termination-summary step)

**Step 1: Update the `log-round` step to include cache fields**

Find the `log-round` step inside the loop body (it starts with `# --- Log Round:`). Find the heredoc that writes the YAML log entry — the section that starts with `cat >> specs/evaluation/reports/quality-loop-log.yaml <<ENTRY` and ends with `ENTRY`.

Replace the entire heredoc block (from the `cat >>` line through the `ENTRY` delimiter) with this version that adds cache fields:

```bash
          cat >> specs/evaluation/reports/quality-loop-log.yaml <<ENTRY
          ---
          round: {{_loop_iteration}}
          gap: "${gap_name}"
          candidates: "see diagnosis output for full list"
          chosen_because: "${chosen_because}"
          target: "${target_file}"
          edit_plan: "${edit_plan}"
          commit: "{{check_result.fix_commit}}"
          score_before: {{check_result.score_before}}
          score_after: {{check_result.score_after}}
          decision: "{{check_result.decision}}"
          plateau_counter: {{check_result.plateau_counter}}
          topics_rerun: "{{selected_topics.selected_topic_ids}}"
          competitors_cached: true
          cache_dir: "{{cache_info.cache_dir}}"
          ENTRY
```

The three new fields are `topics_rerun`, `competitors_cached`, and `cache_dir`.

**Step 2: Update the `termination-summary` step to report cache info**

Find the `termination-summary` step (the last top-level step). In its command, find the line:

```bash
      echo "Converged:         {{converged}}"
```

Add these lines immediately after it:

```bash
      echo ""
      echo "Cache dir:         {{cache_info.cache_dir}}"
      echo "Competitors cached: {{cache_info.competitors_cached}}"
      echo "Topics/iteration:  {{topics_per_iteration}}"
```

**Step 3: Run the remaining failing test**

Run:
```bash
python -m pytest tests/test_quality_loop_recipe.py::test_log_round_includes_cache_fields -v
```
Expected: PASS.

**Step 4: Run the FULL test suite — everything must pass**

Run:
```bash
python -m pytest tests/test_quality_loop_recipe.py -v
```
Expected: ALL tests PASS. Zero failures. This is the moment of truth — all v2 structural tests plus all surviving v1 tests should be green.

Count the total: should be approximately 62-64 tests (44 original - 1 updated version test + ~18-20 new tests).

**Step 5: Run the broader test suite to check for collateral damage**

Run:
```bash
python -m pytest tests/test_quality_eval_recipe.py tests/test_quality_eval_iteration_recipe.py -v 2>&1 | tail -5
```
Expected: All tests pass. The `quality-eval.yaml` change is backward-compatible.

**Step 6: Commit**

Run:
```bash
git add recipes/quality-loop.yaml && git commit -m "feat: add cache fields to log-round and termination-summary observability"
```

---

## Post-Implementation Verification

After all 7 tasks are complete, run these final checks:

**1. Full test suite:**
```bash
python -m pytest tests/ -v 2>&1 | tail -10
```
Expected: All tests pass across the entire project.

**2. Recipe YAML validity:**
```bash
python3 -c "
import yaml
for f in ['recipes/quality-loop.yaml', 'recipes/quality-eval.yaml']:
    with open(f) as fh:
        data = yaml.safe_load(fh)
    print(f'{f}: OK ({len(data.get(\"steps\", []))} top-level steps)')
"
```
Expected:
```
recipes/quality-loop.yaml: OK (4 top-level steps)
recipes/quality-eval.yaml: OK (4 top-level steps)
```

**3. Verify recipe structure visually:**
```bash
python3 -c "
import yaml
with open('recipes/quality-loop.yaml') as f:
    recipe = yaml.safe_load(f)
print(f'Version: {recipe[\"version\"]}')
print(f'Context keys: {list(recipe[\"context\"].keys())}')
print(f'Top-level steps: {[s.get(\"id\", \"while-loop\") for s in recipe[\"steps\"]]}')
loop = [s for s in recipe['steps'] if 'while_condition' in s][0]
print(f'Loop body steps: {[s[\"id\"] for s in loop[\"steps\"]]}')
"
```
Expected:
```
Version: 2.0.0
Context keys: ['target_score', 'current_score', 'plateau_counter', 'converged', 'evaluation_mode', 'topics_per_iteration']
Top-level steps: ['initial-eval', 'cache-competitors', 'improvement-loop', 'termination-summary']
Loop body steps: ['select-topics', 'evaluate', 'aggregate-diagnose', 'fix', 'check', 'log-round']
```

**4. Verify .gitignore works:**
```bash
grep "specs/evaluation/cache" .gitignore
```
Expected: `specs/evaluation/cache/`

**5. Final commit log:**
```bash
git log --oneline -7
```
Expected: 7 clean commits, one per task, with descriptive messages.
