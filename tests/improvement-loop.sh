#!/usr/bin/env bash
# =============================================================================
# Presentation Builder Self-Improvement Loop (with Convergence)
# =============================================================================
#
# Runs iterative test-improve cycles for one or both builders with convergence:
#
#   For each iteration, for each builder:
#     1. Run tests -> collect scores
#     2. Check convergence:
#        - Score declined >0.2 -> REVERT prompt, re-run tests
#        - Plateau (3 rounds within 0.1) -> stop that builder
#        - Prompt grew >20% -> REVERT (bloat guard)
#     3. Improve prompt based on evaluation evidence
#     4. Repeat
#
# Each builder converges independently — one may stop while the other continues.
#
# Usage:
#   ./tests/improvement-loop.sh                       # both builders, 5 iterations
#   ./tests/improvement-loop.sh --iterations 3        # custom count
#   ./tests/improvement-loop.sh --builder pb          # only presentation-builder
#   ./tests/improvement-loop.sh --builder pb2         # only presentation-builder-two
#   ./tests/improvement-loop.sh --skip-first-run      # use existing round 1 results
#
# =============================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Builder configs
PB_TEST_DIR="${SCRIPT_DIR}/presentation-builder"
PB_PROMPT="agents/presentation-builder.md"
PB_RUN="${PB_TEST_DIR}/run-all.sh"
PB_COLLECT="${PB_TEST_DIR}/collect-scores.sh"
PB_BACKUP="${PB_TEST_DIR}/rounds/.prompt-backup.md"

PB2_TEST_DIR="${SCRIPT_DIR}/presentation-builder-two"
PB2_PROMPT="specialists/presentation-builder-two/index.md"
PB2_RUN="${PB2_TEST_DIR}/run-all.sh"
PB2_COLLECT="${PB2_TEST_DIR}/collect-scores.sh"
PB2_BACKUP="${PB2_TEST_DIR}/rounds/.prompt-backup.md"

IMPROVE_RECIPE="${SCRIPT_DIR}/analyze-and-improve.yaml"

# Flags
ITERATIONS=5
BUILDER="both"
SKIP_FIRST=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --iterations) ITERATIONS="$2"; shift 2 ;;
    --builder) BUILDER="$2"; shift 2 ;;
    --skip-first-run) SKIP_FIRST=true; shift ;;
    *) echo "Unknown flag: $1" >&2; exit 1 ;;
  esac
done

run_pb=false; run_pb2=false
case "$BUILDER" in
  pb|presentation-builder) run_pb=true ;;
  pb2|presentation-builder-two) run_pb2=true ;;
  both) run_pb=true; run_pb2=true ;;
  *) echo "Unknown builder: $BUILDER" >&2; exit 1 ;;
esac

# Per-builder convergence state
pb_prev_avg=""; pb_prev_prev_avg=""; pb_converged=false
pb2_prev_avg=""; pb2_prev_prev_avg=""; pb2_converged=false

# ─── Helper functions ────────────────────────────────────────────────────

get_latest_avg() {
  local test_dir="$1"
  local rounds_dir="${test_dir}/rounds"
  local latest=$(ls -d "${rounds_dir}"/round-* 2>/dev/null | sort -V | tail -1)
  [ -z "$latest" ] && echo "" && return

  local total=0 count=0
  for eval_file in "${latest}"/*-evaluation.md; do
    [ -f "$eval_file" ] || continue
    local score=$(grep -m1 "^overall_score:" "$eval_file" 2>/dev/null | awk '{print $2}')
    if [ -n "$score" ] && [ "$score" != "N/A" ]; then
      total=$(echo "$total + $score" | bc)
      count=$((count + 1))
    fi
  done

  [ "$count" -eq 0 ] && echo "" && return
  echo "scale=2; $total / $count" | bc
}

# Returns: 0=ok, 2=declined(reverted), 3=plateau(stop)
check_convergence() {
  local current="$1" prev="$2" prev_prev="$3" name="$4" prompt="$5" backup="$6"

  [ -z "$prev" ] && return 0

  local diff=$(echo "scale=2; $current - $prev" | bc)
  echo "    Score change: ${prev} -> ${current} (${diff})"

  # Decline guard
  local declined=$(echo "$diff < -0.2" | bc)
  if [ "$declined" -eq 1 ]; then
    echo "    CONVERGENCE: Score declined. Reverting ${name} prompt."
    [ -f "$backup" ] && cp "$backup" "$prompt"
    return 2
  fi

  # Plateau detection
  if [ -n "$prev_prev" ]; then
    local prev_diff=$(echo "scale=2; $prev - $prev_prev" | bc)
    local flat1=$(echo "${diff#-} < 0.1" | bc)
    local flat2=$(echo "${prev_diff#-} < 0.1" | bc)
    if [ "$flat1" -eq 1 ] && [ "$flat2" -eq 1 ]; then
      echo "    CONVERGENCE: ${name} has plateaued (3 rounds within 0.1). Stopping."
      return 3
    fi
  fi

  return 0
}

improve_one_builder() {
  local name="$1" test_dir="$2" prompt="$3" backup="$4"

  echo "    Backing up prompt..."
  mkdir -p "$(dirname "$backup")"
  cp "$prompt" "$backup"

  echo "    Running improvement agent..."
  amplifier tool invoke recipes \
    operation=execute \
    recipe_path="${IMPROVE_RECIPE}" \
    context="{\"builder_name\": \"${name}\", \"test_dir\": \"${test_dir}\", \"prompt_path\": \"${prompt}\"}" \
    2>&1 | tail -5

  # Bloat guard
  local new_lines=$(wc -l < "$prompt")
  local old_lines=$(wc -l < "$backup")
  local growth=$(echo "scale=0; ($new_lines - $old_lines) * 100 / $old_lines" | bc)

  if [ "$growth" -gt 20 ]; then
    echo "    BLOAT GUARD: Prompt grew ${growth}% (${old_lines} -> ${new_lines} lines). Reverting."
    cp "$backup" "$prompt"
    return 1
  fi

  echo "    Prompt updated (${old_lines} -> ${new_lines} lines, ${growth}% change)"
  return 0
}

run_tests_parallel() {
  local iteration="$1"
  echo ""
  echo "  ┌─────────────────────────────────────┐"
  echo "  │  PHASE 1: RUNNING TESTS             │"
  echo "  └─────────────────────────────────────┘"
  echo ""

  local pids=() names=()

  if [ "$run_pb" = true ] && [ "$pb_converged" = false ]; then
    echo "  Starting: presentation-builder"
    "${PB_RUN}" > "${PB_TEST_DIR}/rounds/iteration-${iteration}.log" 2>&1 &
    pids+=($!); names+=("presentation-builder")
  fi
  if [ "$run_pb2" = true ] && [ "$pb2_converged" = false ]; then
    echo "  Starting: presentation-builder-two"
    "${PB2_RUN}" > "${PB2_TEST_DIR}/rounds/iteration-${iteration}.log" 2>&1 &
    pids+=($!); names+=("presentation-builder-two")
  fi

  [ ${#pids[@]} -eq 0 ] && echo "  All builders converged. Nothing to run." && return

  echo "  Waiting for ${#pids[@]} test suite(s)..."
  echo ""

  for i in "${!pids[@]}"; do
    if wait "${pids[$i]}"; then
      echo "  DONE: ${names[$i]}"
    else
      echo "  FAIL: ${names[$i]} (check logs)"
    fi
  done
}

show_scores() {
  echo ""
  echo "  ┌─────────────────────────────────────┐"
  echo "  │  PHASE 2: SCOREBOARD                │"
  echo "  └─────────────────────────────────────┘"
  echo ""

  if [ "$run_pb" = true ]; then
    echo "  ── presentation-builder ──"
    "${PB_COLLECT}" --print 2>/dev/null || echo "  (no scores)"
    echo ""
  fi
  if [ "$run_pb2" = true ]; then
    echo "  ── presentation-builder-two ──"
    "${PB2_COLLECT}" --print 2>/dev/null || echo "  (no scores)"
    echo ""
  fi
}

# ─── Main loop ───────────────────────────────────────────────────────────

echo ""
echo "╔═════════════════════════════════════════════════════════╗"
echo "║  IMPROVEMENT LOOP (with convergence)                   ║"
echo "║  Iterations: ${ITERATIONS}  |  Builders: ${BUILDER}                    ║"
echo "║                                                        ║"
echo "║  Guards: decline >0.2 reverts, bloat >20% reverts,     ║"
echo "║          plateau (3 rounds < 0.1 change) stops         ║"
echo "╚═════════════════════════════════════════════════════════╝"

for iteration in $(seq 1 "$ITERATIONS"); do
  # Check if all builders have converged
  if [ "$pb_converged" = true ] || [ "$run_pb" = false ]; then
    if [ "$pb2_converged" = true ] || [ "$run_pb2" = false ]; then
      echo ""
      echo "  All active builders have converged. Stopping early."
      break
    fi
  fi

  echo ""
  echo "══════════════════════════════════════════════════════════"
  echo "  ITERATION ${iteration} of ${ITERATIONS}"
  echo "══════════════════════════════════════════════════════════"

  # Phase 1: Run tests
  if [ "$iteration" -eq 1 ] && [ "$SKIP_FIRST" = true ]; then
    echo ""
    echo "  Skipping first run (--skip-first-run)"
  else
    run_tests_parallel "$iteration"
  fi

  # Phase 2: Show scores
  show_scores

  # Phase 3: Convergence check + improve (skip on last iteration)
  if [ "$iteration" -lt "$ITERATIONS" ]; then
    echo ""
    echo "  ┌─────────────────────────────────────┐"
    echo "  │  PHASE 3: CONVERGE + IMPROVE        │"
    echo "  └─────────────────────────────────────┘"

    # --- presentation-builder ---
    if [ "$run_pb" = true ] && [ "$pb_converged" = false ]; then
      echo ""
      echo "  ── presentation-builder ──"
      local pb_avg=$(get_latest_avg "$PB_TEST_DIR")
      if [ -n "$pb_avg" ]; then
        echo "    Average: ${pb_avg}"
        check_convergence "$pb_avg" "$pb_prev_avg" "$pb_prev_prev_avg" \
          "presentation-builder" "$PB_PROMPT" "$PB_BACKUP"
        conv=$?
        if [ $conv -eq 2 ]; then
          echo "    Re-running tests with reverted prompt..."
          "${PB_RUN}" > "${PB_TEST_DIR}/rounds/revert-run.log" 2>&1
          pb_avg=$(get_latest_avg "$PB_TEST_DIR")
        elif [ $conv -eq 3 ]; then
          pb_converged=true
        fi
        pb_prev_prev_avg="$pb_prev_avg"
        pb_prev_avg="$pb_avg"

        if [ "$pb_converged" = false ]; then
          improve_one_builder "presentation-builder" "$PB_TEST_DIR" "$PB_PROMPT" "$PB_BACKUP"
        fi
      else
        echo "    No valid scores — skipping"
      fi
    fi

    # --- presentation-builder-two ---
    if [ "$run_pb2" = true ] && [ "$pb2_converged" = false ]; then
      echo ""
      echo "  ── presentation-builder-two ──"
      local pb2_avg=$(get_latest_avg "$PB2_TEST_DIR")
      if [ -n "$pb2_avg" ]; then
        echo "    Average: ${pb2_avg}"
        check_convergence "$pb2_avg" "$pb2_prev_avg" "$pb2_prev_prev_avg" \
          "presentation-builder-two" "$PB2_PROMPT" "$PB2_BACKUP"
        conv=$?
        if [ $conv -eq 2 ]; then
          echo "    Re-running tests with reverted prompt..."
          "${PB2_RUN}" > "${PB2_TEST_DIR}/rounds/revert-run.log" 2>&1
          pb2_avg=$(get_latest_avg "$PB2_TEST_DIR")
        elif [ $conv -eq 3 ]; then
          pb2_converged=true
        fi
        pb2_prev_prev_avg="$pb2_prev_avg"
        pb2_prev_avg="$pb2_avg"

        if [ "$pb2_converged" = false ]; then
          improve_one_builder "presentation-builder-two" "$PB2_TEST_DIR" "$PB2_PROMPT" "$PB2_BACKUP"
        fi
      else
        echo "    No valid scores — skipping"
      fi
    fi
  else
    echo ""
    echo "  ┌─────────────────────────────────────┐"
    echo "  │  FINAL ITERATION — VALIDATION ONLY  │"
    echo "  └─────────────────────────────────────┘"
  fi

  echo ""
  echo "  Iteration ${iteration} complete."
  [ "$run_pb" = true ] && echo "    pb:  avg=${pb_prev_avg:-n/a} converged=${pb_converged}"
  [ "$run_pb2" = true ] && echo "    pb2: avg=${pb2_prev_avg:-n/a} converged=${pb2_converged}"
done

# ─── Final summary ───────────────────────────────────────────────────────

echo ""
echo "╔═════════════════════════════════════════════════════════╗"
echo "║  LOOP COMPLETE                                         ║"
echo "╚═════════════════════════════════════════════════════════╝"
echo ""

show_scores

if [ "$run_pb" = true ]; then
  echo "  PB-1 prompt: $(wc -l < "$PB_PROMPT") lines | converged: ${pb_converged}"
fi
if [ "$run_pb2" = true ]; then
  echo "  PB-2 prompt: $(wc -l < "$PB2_PROMPT") lines | converged: ${pb2_converged}"
fi
echo ""
echo "  Scorecard CSVs:"
[ "$run_pb" = true ] && echo "    ${PB_TEST_DIR}/rounds/scorecard.csv"
[ "$run_pb2" = true ] && echo "    ${PB2_TEST_DIR}/rounds/scorecard.csv"
echo ""
echo "  Improvement logs in each round's directory."
