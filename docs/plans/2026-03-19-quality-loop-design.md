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

## Open Questions

- Exact scoring formula for competitive mode (percentage of dimensions won, weighted scoring, or something else)
- How to handle competitor runs that fail or timeout (skip that cell, or penalize?)
- Whether the fix step should have an optional approval gate for high-risk changes
- How to persist scoring criteria evolution across runs (so the evaluator doesn't forget what it learned)
- Integration pattern with dev-machine-bundle for continuous improvement
