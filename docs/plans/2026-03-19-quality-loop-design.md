# Autonomous Quality Improvement Loop Design

## Goal

A reusable, recipe-driven loop that runs any agent pipeline against competitor tools on the same questions, identifies where the pipeline falls short, fixes the gaps, re-tests, and loops until a target score is reached.

## Background

Evaluating a pipeline on one topic against one competitor gives a data point. Data points are noisy — you can't tell whether a gap is structural or topic-specific. Running multiple topics against multiple competitors gives a distribution, which is trustworthy signal. The loop automates the full cycle: evaluate → diagnose → fix → re-evaluate, so the pipeline improves autonomously between human review sessions.

The first customer is the canvas-specialists research pipeline, but the design is portable to any Amplifier project.

## Approach

Recipe-driven quality loop using `while_condition` to iterate until convergence. The recipe is parameterized — any project provides its own pipeline config, competitor list, test topics, and evaluation mode.

Why a recipe (not a bundle or skill): Recipes are already reusable, resumable, and have approval gates built in. The recipe IS the portable pattern. Lighter than a standalone bundle and more autonomous than a skill.

## Loop Structure

Each iteration runs a **test matrix** (N topics × M competitors), not a single test. The same topics repeat across iterations so improvement is measured against topic variance, not masked by it.

### The Iteration Cycle

1. **Evaluate** — run the test matrix using the cheapest sufficient evaluation mode
2. **Aggregate** — synthesize across topics into a holistic scorecard. Gaps in 4/5 topics are structural. Gaps in 1/5 are topic noise. This is triangulation.
3. **Diagnose** — map each structural gap to a specific fix: which specialist file, which stage, what change
4. **Fix** — implement the diagnosed changes
5. **Loop** — back to step 1. Exit when: score ≥ target, convergence detected, or max iterations hit.

### Evaluation Mode Selection

The evaluator picks the cheapest mode that gives trustworthy signal, based on what changed since the last iteration:

| Mode | Cost | When Used |
|------|------|-----------|
| **Re-evaluate** | ~1 min | Re-score previous test logs against updated criteria. No pipeline run. Used when a fix is structural (e.g., added a self-check stage) and the old output clearly would or wouldn't have been caught. |
| **Partial re-run** | ~5 min | Re-run only the changed specialist(s) using cached upstream inputs. Used when a mid-pipeline specialist changed but the research itself didn't. |
| **Full re-run** | ~15 min/topic | Run the entire pipeline + competitors fresh. Used when the researcher itself changed or when it's time for a clean baseline. |

## Evaluation Modes

Two modes, configured per run:

**Competitive mode.** The pipeline runs alongside competitor tools on the same questions. The evaluator asks: "Where does this pipeline lose to the best available output, and why?" The score reflects performance relative to the best output across evaluation dimensions.

**Rubric mode.** No competitors — scores against quality criteria (e.g., "all claims must have source attribution," "hedging must match confidence tier"). Each criterion scores pass/fail/partial.

Both modes produce the same output contract: a **structured gap list** with:
- **Severity** — structural (appears across topics) vs. topic-noise (appears in one)
- **Location** — which specialist, which stage
- **Proposed fix** — what to change and why

The evaluator's scoring criteria evolve. If it notices a new failure pattern (e.g., "the researcher doesn't cover downsides"), it adds that as a dimension going forward. The scoring is not locked to a static rubric.

## Safety Mechanisms

Three mechanisms prevent the loop from going off the rails:

**Revert-on-regression.** After every fix, the loop re-evaluates. If the aggregate score dropped or stayed flat, the fix is reverted (`git revert`) before the next iteration. The loop never accumulates bad changes. Worst case: the loop ran for a while and made no progress — not that it made things worse.

**Max iterations cap.** Configurable per run (default: 5). The loop stops even if the target score isn't met.

**Convergence detection.** If the score doesn't improve for 2 consecutive iterations (after reverts), the loop stops and reports: current score, gaps it couldn't close, and why. This surfaces the hard problems that need human judgment.

The loop outputs a **run report**: starting score, ending score, what was fixed, what was reverted, and remaining gaps.

## Observability

Every round writes a structured log entry immediately after the round completes (append-only, not batched at end of run). This survives interruptions — if the loop crashes mid-run, you have logs for every completed round.

### Per-Round Log Entry

Each entry captures the full decision chain for that round:

| Field | Description |
|-------|-------------|
| `round` | Round number (1-indexed) |
| `gap` | The specific gap being addressed this round |
| `candidates` | All gaps considered as candidates (no cap — list every option) |
| `chosen_because` | Why this gap was selected over the others. Differentiates "stuck on one unfixable gap" from "cycling through gaps with no working fixes" |
| `target` | The specialist file being modified |
| `edit_plan` | What change is being made and why |
| `commit` | Git commit hash for this fix. Git commits are the snapshot mechanism — no `.bak` files, no cleanup debt |
| `score_before` | Aggregate score before the fix |
| `score_after` | Aggregate score after re-evaluation |
| `decision` | `kept` or `reverted` |
| `plateau_counter` | How many consecutive non-improving rounds (resets on improvement) |

### Example Log Entry

```yaml
round: 3
gap: "factual depth — insufficient claim count for broad surveys"
candidates: ["factual depth (4/5 topics)", "source diversity (2/5 topics)"]
chosen_because: "highest severity, structural across 4/5 topics"
target: "agents/researcher/researcher.md"
edit_plan: "Add breadth gate scaling claim budget to question scope"
commit: "a3f2c1b"
score_before: 7.33
score_after: 7.85
decision: kept
plateau_counter: 0
```

### Termination Summary

When the loop exits (for any reason), it writes a termination summary:

- Final aggregate score
- Total rounds completed
- Which exit condition fired (target reached, max iterations, convergence/plateau)
- Round-by-round score table showing the trajectory

## Recipe Inputs

The recipe is parameterized so any project can use it:

| Input | Description |
|-------|-------------|
| `pipeline` | How to run the thing being tested. A recipe path, agent delegation, or bash command. |
| `competitors` | List of competitor tools to benchmark against. Each entry specifies how to run that competitor (agent + model provider). Empty list = rubric mode. |
| `topics` | List of test inputs that stress different capabilities. |
| `evaluation_mode` | `competitive` or `rubric`. |
| `target_score` | Loop exits when aggregate score ≥ this value. |
| `max_iterations` | Safety cap (default: 5). |
| `test_logs_dir` | Where past test logs live. The evaluator can re-score these instead of re-running when a fix is structural. |

## Recommended Inputs: Canvas-Specialists

This is the first-customer configuration.

**Pipeline:** `research-chain` recipe (full 11-step deep chain: researcher → formatter → DA → DA-formatter → writer → writer-formatter → save)

**Competitors (3 — all runnable within Amplifier):**

| Competitor | Description |
|-----------|-------------|
| `foundation:web-research` + Anthropic (Claude) | Generic research agent, best-in-class model |
| `foundation:web-research` + Google (Gemini) | Generic research agent, different model strengths |
| `foundation:web-research` + OpenAI (Codex) | Generic research agent, third perspective |

Same tools, same question, no specialist pipeline. Three different models gives triangulation on the competitor side — if all three beat the pipeline on the same dimension, it's a real gap. If only one does, it might be model-specific noise.

**Topics (5):**

| Profile | Topic |
|---------|-------|
| Factual deep-dive | "What is Jina AI and how does it compare to other embedding providers?" |
| Strategy | "What are the best strategies for improving hybrid team productivity?" |
| Survey | "What are the best places to retire abroad for US citizens?" |
| Comparison | "Compare Cursor vs GitHub Copilot Workspace for AI-assisted development" |
| Technical analysis | "What are the security implications of WebAssembly outside the browser?" |

These topics stress different parts of the pipeline. Most have existing test logs from previous sessions, so re-evaluation mode can kick in on early iterations.

**Evaluation mode:** Competitive
**Target score:** Defined per-run. The loop reports "specialists scored 7, Anthropic scored 8.8" with specific reasons — then tries to close the gap.
**Max iterations:** 5

## Portability

The recipe is project-agnostic. All specialist-specific details are recipe inputs, not hardcoded.

For another project to adopt:

1. Define the pipeline (how to run their thing)
2. Define competitors (what to compare against, or nothing for rubric mode)
3. Define topics (test inputs that stress different capabilities)
4. Set evaluation mode and target score
5. Run the recipe

The recipe delegates to generic agents (evaluator, diagnostician, implementer) that read the project's own files to understand what to fix. No specialist-specific code is imported.

For dev-machine-bundle integration: a cron-like trigger could invoke the recipe periodically, and the run report accumulates into a quality history. The project improves while you sleep.

## Decisions

Resolved during design review. These were originally open questions.

### 1. Scoring Formula

Simple average of the 6 evaluation dimensions. No weighting. Revisit only if data shows certain dimensions consistently dominate or mislead the loop's fix priorities.

### 2. Competitor Timeout Handling

Skip the failed competitor's cell. Require a minimum of 2 out of 3 competitors to succeed for a topic to count in that iteration's scoring. Topics that don't meet the minimum are excluded from the iteration entirely and retried next round. This prevents a lucky timeout from inflating the pipeline's score while handling the practical reality that APIs fail.

### 3. Approval Gate for High-Risk Fixes

No gate. The loop runs fully autonomous. Revert-on-regression is the safety net — bad fixes get undone automatically before the next iteration. The run report provides full visibility after the fact: diagnosis reasoning, diffs, commit hashes, scores. If a run produces concerning diffs, adding a gate later is easy. For extra caution on a specific run, set `max_iterations: 1` for single-fix-then-review.

### 4. Persisting Scoring Criteria Evolution

Don't persist. Each run starts from the static rubric. The evaluator can notice new patterns within a run (across iterations), but those patterns don't carry to the next run. If a run reveals a genuinely new failure pattern, the run report surfaces it. A human decides whether to promote it to a permanent criterion. This keeps the rubric intentional and curated rather than auto-accumulated.

### 5. Dev-Machine-Bundle Integration

Not now. Run manually with `amplifier recipe execute`. The recipe is inherently schedulable — when the need arises, it's just `amplifier recipe execute` on a cron. Build the loop, run it 3–5 times manually, then decide if scheduling adds value. The run report format is the integration surface; any scheduling mechanism reads the same reports.
