# Quality Loop v2 Design

## Goal

Reduce quality loop iteration time from ~3 hours (v1) to ~30-90 minutes by splitting initial evaluation from the improvement loop, caching upstream outputs, and re-running only from the point of change.

## Background

The v1 loop ran for 12+ hours overnight, producing 3 good fixes:

- **Round 1** (ad1d3d8, 12:28 AM): source-quality-diversity fix to researcher
- **Round 2** (4586a95, 3:14 AM): factual-depth-coverage-framework fix to researcher
- **Round 3** (9477d81, 6:06 AM): citation-quality-verification fix to writer-formatter

The fixes were correct — the loop diagnosed real gaps and targeted the right files. But each iteration took ~3 hours because it re-ran the full competitive evaluation (5 topics × full pipeline + 3 competitors) every time, even though only one specialist file changed per iteration. 95% of runtime was evaluation, 5% was improvement.

Three bugs were also found and fixed separately during the v1 run:

- `provider_preferences` dict vs list (competitors returning null)
- `grep -oP` incompatible with macOS BSD grep (score extraction zeros)
- `ls` + stale-check output capture failure (topic output serialized as `[1]`)

## Approach

Split the monolithic evaluate-then-improve loop into two phases: an expensive one-time baseline evaluation, and a fast iterative improvement loop that caches upstream outputs and only re-runs the pipeline from the point of change. Competitor baselines are computed once and reused across all iterations.

## Architecture

### Two-Phase Design

**Phase A: Baseline Evaluation (runs once per loop invocation)**

- Runs the full competitive eval: N topics × full pipeline + 3 competitors
- Caches all outputs in a structured directory
- Produces the initial gap report with scores
- This is the expensive step (~3 hours for 5 topics). Runs once.

**Phase B: Improvement Loop (fast iterations)**

- Diagnose top gap from last evaluation
- Fix the target file (one commit)
- Smart re-evaluate: identify which specialist was changed, re-run the pipeline from that specialist forward using cached upstream outputs, only on affected topics. Competitor baselines reused from Phase A.
- Score, compare, revert if no improvement
- ~15-90 min per iteration depending on where the fix is in the pipeline

**Recipe inputs add one new parameter:**

- `topics_per_iteration: 3` (default) — how many topics to re-run during the loop. The initial evaluation still runs all topics.

### Pipeline Dependency Chain

```
researcher → researcher-formatter → data-analyzer → DA-formatter → writer → writer-formatter
```

A fix to the researcher invalidates everything downstream. A fix to the writer invalidates only writer + writer-formatter. The cache knows which specialist was changed (from the diagnosis) and replays from that point.

**Important constraint:** Cache invalidation follows the pipeline chain, not just the file that was edited. If the diagnosis says "fix the researcher," we re-run researcher → formatter → DA → DA-formatter → writer → writer-formatter. No skipping intermediate stages — the data-analyzer's output depends on the research content, not just its own instructions.

## Components

### Cache Directory Structure

The cache lives at `specs/evaluation/cache/{run_id}/` where `run_id` is a timestamp. This keeps multiple runs separate and makes debugging easy.

```
specs/evaluation/cache/{run_id}/
├── competitors/
│   ├── {topic_id}/
│   │   ├── anthropic-claude.md
│   │   ├── google-gemini.md
│   │   └── openai-gpt4o.md
├── pipeline/
│   ├── {topic_id}/
│   │   ├── research_output.md        # researcher output
│   │   ├── formatted_research.md     # researcher-formatter output
│   │   ├── analysis_output.md        # data-analyzer output
│   │   ├── formatted_analysis.md     # DA-formatter output
│   │   ├── final_document.md         # writer output
│   │   └── formatted_document.md     # writer-formatter output
├── scores/
│   ├── {topic_id}.json               # per-topic scores (6 dimensions)
│   └── aggregate.json                # cross-topic aggregate + gap list
└── metadata.json                     # run config, timestamps, topic list, content hashes
```

### Cache Rules

- Competitor files are written once during Phase A and never invalidated within a run
- Pipeline files are invalidated from the changed specialist forward (downstream cascade)
- Scores are invalidated whenever any pipeline file they depend on is invalidated
- `metadata.json` tracks which specialist file (and its content hash) produced each pipeline cache entry. When a fix changes a specialist file, the cache identifies stale entries by comparing the current file hash vs the hash that produced the cached output. Simple, deterministic, no guessing.
- The cache is disposable — `.gitignore`'d. A new `run_id` is created each time you invoke the loop. Old caches can be deleted without consequence.

### Smart Re-evaluation Logic

When the fix step changes a specialist file, the re-evaluation step figures out what to re-run.

**Mapping from specialist file to pipeline position:**

| File changed | Re-run from | Estimated time (×3 topics) |
|---|---|---|
| `agents/researcher.md` | researcher (position 1) — everything | ~90 min |
| `agents/researcher-formatter.md` | researcher-formatter (position 2) | ~60 min |
| `agents/data-analyzer.md` | data-analyzer (position 3) | ~45 min |
| `agents/data-analyzer-formatter.md` | DA-formatter (position 4) | ~30 min |
| `agents/writer.md` | writer (position 5) | ~15 min |
| `agents/writer-formatter.md` | writer-formatter (position 6) | ~6 min |

**How it works:**

1. The diagnosis output includes `target_file` — which specialist file was changed
2. The re-evaluate step maps that file to a pipeline position
3. For each affected topic, it loads cached outputs for all stages before that position
4. It runs the pipeline from that position forward, producing new outputs
5. It re-scores using the new pipeline outputs + cached competitor baselines
6. New outputs replace the stale cache entries

### Topic Selection Strategy

Re-run on **the 2 worst-scoring topics for the diagnosed gap** plus **1 topic that scored well** (regression check). This keeps iteration time predictable (~30-90 min) regardless of how many topics flagged the gap. The 2 worst give maximum improvement signal. The 1 good topic catches regressions — if a researcher fix improves factual depth but degrades analytical insight on a topic that was scoring 9, you want to know.

### Recipe Split

The recipe splits into two files:

- **`quality-loop-baseline.yaml`** — Phase A. Runs the full competitive eval, populates the cache, produces the initial gap report.
- **`quality-loop.yaml`** — Phase B. The improvement loop with caching. Diagnose → fix → partial-evaluate → check → log.

## Data Flow

```
Phase A (once):
  All topics × full pipeline → cache/pipeline/{topic_id}/*.md
  All topics × 3 competitors → cache/competitors/{topic_id}/*.md
  Score all → cache/scores/{topic_id}.json + aggregate.json
  Write metadata.json with content hashes

Phase B (per iteration):
  1. Read aggregate.json → diagnose top gap → target_file
  2. Fix target_file → git commit
  3. Map target_file → pipeline position
  4. Select 3 topics (2 worst + 1 regression)
  5. For each topic:
     a. Load cached outputs for stages before pipeline position
     b. Run pipeline from position forward → new outputs
     c. Replace stale cache entries
  6. Re-score affected topics using new outputs + cached competitors
  7. Update aggregate.json
  8. Compare scores → keep fix or git revert
  9. Log round to observability log
```

## Error Handling

- **Revert-on-regression:** If scores don't improve after a fix, `git revert` the commit. Unchanged from v1.
- **Convergence detection:** Plateau counter >= 2 triggers early exit. Unchanged from v1.
- **Cache corruption:** The cache is disposable. If anything looks wrong, delete the `run_id` directory and re-run Phase A. No repair logic needed.
- **Max iterations:** `max_while_iterations: 5` hard cap. Unchanged from v1.
- **Single-file, single-commit constraint:** Each fix touches one file in one commit, keeping reverts clean and cache invalidation deterministic.

## Observability

The v1 observability design (per-round append-only log) carries forward with two additions:

### Cache Hit/Miss Logging

Each round's log entry adds:

- `cache_hits` — list of cached outputs that were reused (e.g., `"research_output/strategy"`)
- `cache_misses` — list of outputs that were re-generated
- `rerun_from` — which pipeline position the re-run started from (e.g., `"data-analyzer"`)
- `topics_rerun` — which 3 topics were selected

### Timing Per Phase

Each log entry adds:

- `phase_a_duration_minutes` — only on round 1
- `rerun_duration_minutes` — how long the partial re-run took
- `diagnose_duration_minutes`
- `fix_duration_minutes`

This gives the data to verify whether the v2 optimizations are delivering the expected speedup.

## What Changes vs What Stays

### Changes from v1

- Recipe splits into two files: `quality-loop-baseline.yaml` (Phase A) and `quality-loop.yaml` (Phase B)
- New cache directory at `specs/evaluation/cache/{run_id}/` (`.gitignore`'d)
- The evaluate step inside the loop becomes a partial-evaluate step that re-runs only from point of change on affected topics
- The check step reads cached scores to compare
- New `topics_per_iteration` parameter (default 3)
- Log entries gain cache hit/miss fields and timing data

### Unchanged from v1

- `while_condition` / `break_when` / `max_while_iterations: 5` — loop mechanics
- Revert-on-regression via `git revert` — safety net
- Convergence detection (plateau counter >= 2)
- Aggregate-diagnose step — same prompt, same triangulation logic
- Fix step — same single-file, single-commit constraint
- Append-only observability log — same format, extended with cache fields
- Termination summary — same exit conditions, same report format
- Scoring: simple average of 6 dimensions, no weighting

### Not Building (YAGNI)

- **Re-score-only mode** — dropped. Partial re-run is fast enough without speculative evaluation.
- **Dynamic topic selection during iterations** — fixed strategy: 2 worst + 1 regression check.
- **Multi-file fixes per iteration** — still one file per round, keeps reverts clean.
- **Scoring criteria evolution** — still static rubric per run.

## Expected Performance

| Scenario | v1 time | v2 time | Speedup |
|---|---|---|---|
| Initial evaluation (5 topics) | ~3 hrs | ~3 hrs (same — runs once) | 1x |
| Researcher fix iteration | ~3 hrs | ~90 min | 2x |
| Writer fix iteration | ~3 hrs | ~15 min | 12x |
| Writer-formatter fix iteration | ~3 hrs | ~6 min | 30x |
| Full convergence run (3 iterations) | ~9 hrs | ~3 hrs initial + ~2 hrs iterations = ~5 hrs | 1.8x |
| Full convergence run (5 iterations) | ~15 hrs | ~3 hrs + ~3.5 hrs = ~6.5 hrs | 2.3x |

The biggest wins are on downstream specialist fixes (writer, writer-formatter) which go from 3 hours to minutes. Researcher fixes are still the slowest because the entire pipeline must re-run, but even those drop from 3 hours to 90 minutes by running only 3 topics instead of 5.

## Open Questions

None — all sections reviewed and approved during design brainstorm.
