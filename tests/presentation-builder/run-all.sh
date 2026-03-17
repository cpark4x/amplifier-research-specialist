#!/usr/bin/env bash
# =============================================================================
# Presentation Builder Evaluation Harness — Full Run (Parallel)
# =============================================================================
#
# Generates all 6 test decks and evaluates each against the rubric.
# All scenarios within a phase run in PARALLEL.
# Results are organized into numbered rounds for comparison over time.
#
# Usage:
#   ./tests/presentation-builder/run-all.sh                    # auto-increment round
#   ./tests/presentation-builder/run-all.sh --round 3          # explicit round number
#   ./tests/presentation-builder/run-all.sh --generate-only    # generate only
#   ./tests/presentation-builder/run-all.sh --evaluate-only    # evaluate only (decks must exist)
#
# Rounds are stored in: tests/presentation-builder/rounds/round-NN/
#
# =============================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCENARIOS_DIR="${SCRIPT_DIR}/scenarios"
ROUNDS_DIR="${SCRIPT_DIR}/rounds"
GENERATE_RECIPE="${SCRIPT_DIR}/generate-decks.yaml"
EVALUATE_RECIPE="${SCRIPT_DIR}/evaluate-deck.yaml"

# Parse flags
GENERATE=true
EVALUATE=true
ROUND=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --generate-only) EVALUATE=false; shift ;;
    --evaluate-only) GENERATE=false; shift ;;
    --round) ROUND="$2"; shift 2 ;;
    *) echo "Unknown flag: $1" >&2; exit 1 ;;
  esac
done

# Determine round number
if [ -z "$ROUND" ]; then
  # Auto-increment: find highest existing round and add 1
  latest=$(ls -d "${ROUNDS_DIR}"/round-* 2>/dev/null | sort -V | tail -1 | grep -oE '[0-9]+$' || echo "0")
  ROUND=$(printf "%02d" $((10#$latest + 1)))
else
  ROUND=$(printf "%02d" "$ROUND")
fi

OUTPUT_DIR="${ROUNDS_DIR}/round-${ROUND}"
LOG_DIR="${OUTPUT_DIR}/logs"
mkdir -p "${OUTPUT_DIR}" "${LOG_DIR}"

# Collect scenario files
scenarios=()
for f in "${SCENARIOS_DIR}"/*.md; do
  [ -f "$f" ] && scenarios+=("$f")
done

if [ ${#scenarios[@]} -eq 0 ]; then
  echo "ERROR: No scenario files found in ${SCENARIOS_DIR}" >&2
  exit 1
fi

echo "=== Round ${ROUND} ==="
echo "Found ${#scenarios[@]} scenarios — running in parallel"
echo "Output: ${OUTPUT_DIR}/"
echo ""

# --- Phase 1: Generate decks (all in parallel) ---
if [ "$GENERATE" = true ]; then
  echo "=== PHASE 1: GENERATING DECKS (parallel) ==="
  echo ""

  pids=()
  names=()
  for scenario in "${scenarios[@]}"; do
    name=$(basename "$scenario" .md)
    log="${LOG_DIR}/${name}-generate.log"
    echo "  Starting: ${name} (log: ${log})"

    amplifier tool invoke recipes \
      operation=execute \
      recipe_path="${GENERATE_RECIPE}" \
      context="{\"scenario_path\": \"${scenario}\", \"output_dir\": \"${OUTPUT_DIR}\"}" \
      > "${log}" 2>&1 &

    pids+=($!)
    names+=("${name}")
  done

  echo ""
  echo "  Waiting for ${#pids[@]} jobs..."
  echo ""

  # Wait for each and report
  failures=0
  for i in "${!pids[@]}"; do
    if wait "${pids[$i]}"; then
      echo "  DONE: ${names[$i]}"
    else
      echo "  FAIL: ${names[$i]} (see ${LOG_DIR}/${names[$i]}-generate.log)"
      failures=$((failures + 1))
    fi
  done

  echo ""
  echo "Generation complete. ${failures} failures out of ${#pids[@]}."
  echo ""
fi

# --- Phase 2: Evaluate decks (all in parallel) ---
if [ "$EVALUATE" = true ]; then
  echo "=== PHASE 2: EVALUATING DECKS (parallel) ==="
  echo ""

  pids=()
  names=()
  for scenario in "${scenarios[@]}"; do
    name=$(basename "$scenario" .md)
    deck_path="${OUTPUT_DIR}/${name}-output.html"
    if [ ! -f "$deck_path" ]; then
      echo "  SKIP: ${name} (no deck at ${deck_path})"
      continue
    fi
    log="${LOG_DIR}/${name}-evaluate.log"
    echo "  Starting: ${name} (log: ${log})"

    amplifier tool invoke recipes \
      operation=execute \
      recipe_path="${EVALUATE_RECIPE}" \
      context="{\"scenario_path\": \"${scenario}\", \"deck_path\": \"${deck_path}\", \"output_dir\": \"${OUTPUT_DIR}\"}" \
      > "${log}" 2>&1 &

    pids+=($!)
    names+=("${name}")
  done

  echo ""
  echo "  Waiting for ${#pids[@]} jobs..."
  echo ""

  failures=0
  for i in "${!pids[@]}"; do
    if wait "${pids[$i]}"; then
      echo "  DONE: ${names[$i]}"
    else
      echo "  FAIL: ${names[$i]} (see ${LOG_DIR}/${names[$i]}-evaluate.log)"
      failures=$((failures + 1))
    fi
  done

  echo ""
  echo "Evaluation complete. ${failures} failures out of ${#pids[@]}."
  echo ""
fi

# --- Summary ---
echo "=== ROUND ${ROUND} RESULTS ==="
echo ""
echo "Output directory: ${OUTPUT_DIR}/"
echo ""
ls -la "${OUTPUT_DIR}"/*.html "${OUTPUT_DIR}"/*.md 2>/dev/null || echo "(no output files yet)"
echo ""

# Extract verdicts from evaluation files if they exist
if ls "${OUTPUT_DIR}"/*-evaluation.md 1>/dev/null 2>&1; then
  echo "=== VERDICTS ==="
  printf "  %-40s %-8s %s\n" "SCENARIO" "SCORE" "VERDICT"
  printf "  %-40s %-8s %s\n" "--------" "-----" "-------"
  for eval_file in "${OUTPUT_DIR}"/*-evaluation.md; do
    name=$(basename "$eval_file" -output-evaluation.md)
    verdict=$(grep -m1 "^verdict:" "$eval_file" 2>/dev/null | awk '{print $2}' || echo "N/A")
    score=$(grep -m1 "^overall_score:" "$eval_file" 2>/dev/null | awk '{print $2}' || echo "N/A")
    printf "  %-40s %-8s %s\n" "$name" "$score" "$verdict"
  done
  echo ""
fi

# --- Collect scores into CSV and show cross-round progress ---
echo ""
"${SCRIPT_DIR}/collect-scores.sh" --print
