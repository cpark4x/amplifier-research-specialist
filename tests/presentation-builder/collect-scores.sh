#!/usr/bin/env bash
# =============================================================================
# Collect scores from evaluation files into scorecard.csv
# =============================================================================
#
# Scans all rounds and builds a single CSV for tracking progress over time.
# Re-running this regenerates the entire CSV from source evaluation files,
# so it's always consistent with what's on disk.
#
# Usage:
#   ./tests/presentation-builder/collect-scores.sh           # regenerate full CSV
#   ./tests/presentation-builder/collect-scores.sh --print   # also pretty-print
#   ./tests/presentation-builder/collect-scores.sh --check   # regression check (exit 1 if regressions)
#
# Output: tests/presentation-builder/rounds/scorecard.csv
#
# =============================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROUNDS_DIR="${SCRIPT_DIR}/rounds"
CSV="${ROUNDS_DIR}/scorecard.csv"
PRINT=false
CHECK=false
for arg in "$@"; do
  case "$arg" in
    --print) PRINT=true ;;
    --check) CHECK=true ;;
  esac
done

# Write CSV header
echo "round,date,scenario,overall_score,verdict,D1_narrative,D2_framework,D3_fidelity,D4_density,D5_rhythm,D6_audience,D7_completeness,D8_notes,D9_structure,D10_html,D11_insight,D12_infodesign" > "${CSV}"

# ---------------------------------------------------------------------------
# Score extraction: try structured ```scores block first, fall back to regex.
#
# The ```scores block is a fenced YAML block appended by the judge (v3.1+).
# It's machine-readable by design and avoids the fragility of regex parsing
# prose output. If the block isn't present (older evals), the regex fallback
# handles both v1-v2 inline format and v3 header-then-score format.
# ---------------------------------------------------------------------------

# Extract all scores from the ```scores block into shell variables.
# Sets: _overall, _verdict, _d1.._d12 (empty if block not found).
extract_scores_block() {
  local file="$1"
  _overall="" _verdict=""
  _d1="" _d2="" _d3="" _d4="" _d5="" _d6="" _d7="" _d8="" _d9="" _d10="" _d11="" _d12=""

  # Extract content between ```scores and ``` markers
  local block
  block=$(awk '/^```scores$/,/^```$/' "$file" 2>/dev/null | grep -v '^```')
  [ -z "$block" ] && return 1

  _overall=$(echo "$block" | grep '^overall_score:' | awk '{print $2}')
  _verdict=$(echo "$block" | grep '^verdict:' | awk '{print $2}')
  _d1=$(echo "$block" | grep 'D1_narrative:' | awk '{print $2}')
  _d2=$(echo "$block" | grep 'D2_framework:' | awk '{print $2}')
  _d3=$(echo "$block" | grep 'D3_fidelity:' | awk '{print $2}')
  _d4=$(echo "$block" | grep 'D4_density:' | awk '{print $2}')
  _d5=$(echo "$block" | grep 'D5_rhythm:' | awk '{print $2}')
  _d6=$(echo "$block" | grep 'D6_audience:' | awk '{print $2}')
  _d7=$(echo "$block" | grep 'D7_completeness:' | awk '{print $2}')
  _d8=$(echo "$block" | grep 'D8_notes:' | awk '{print $2}')
  _d9=$(echo "$block" | grep 'D9_structure:' | awk '{print $2}')
  _d10=$(echo "$block" | grep 'D10_html:' | awk '{print $2}')
  _d11=$(echo "$block" | grep 'D11_insight:' | awk '{print $2}')
  _d12=$(echo "$block" | grep 'D12_infodesign:' | awk '{print $2}')

  # Valid if we got at least overall and verdict
  [ -n "$_overall" ] && [ -n "$_verdict" ]
}

# Fallback: extract a single dimension score via regex (v1-v3 prose formats).
#   Old: "D1_narrative_coherence: 3/5 | ..." (v1-v2 evaluations)
#   New: "Score: 3/5" after "D1: NARRATIVE COHERENCE" header (v3 evaluations)
extract_dim() {
  local file="$1" dim="$2"
  # Try old format first (inline score)
  local score
  score=$(grep "^${dim}" "$file" 2>/dev/null | grep -oE '[0-9]+/5' | head -1 | cut -d'/' -f1)
  if [ -n "$score" ]; then
    echo "$score"
    return
  fi
  # Try new format (Score: N/5 on its own line after the dimension header)
  score=$(awk "/^${dim}/{found=1} found && /^Score:/{print; exit}" "$file" 2>/dev/null | grep -oE '[0-9]+/5' | head -1 | cut -d'/' -f1)
  echo "$score"
}

# Process each round
for round_dir in $(ls -d "${ROUNDS_DIR}"/round-* 2>/dev/null | sort -V); do
  round_name=$(basename "$round_dir")
  # Get round date from directory modification time
  round_date=$(stat -f '%Sm' -t '%Y-%m-%d' "$round_dir" 2>/dev/null || date -r "$round_dir" '+%Y-%m-%d' 2>/dev/null || echo "unknown")

  for eval_file in "${round_dir}"/*-evaluation.md; do
    [ -f "$eval_file" ] || continue

    scenario=$(basename "$eval_file" -output-evaluation.md)

    # Try structured ```scores block first (v3.1+), fall back to regex
    if extract_scores_block "$eval_file"; then
      overall="$_overall"
      verdict="$_verdict"
      d1="$_d1" d2="$_d2" d3="$_d3" d4="$_d4" d5="$_d5" d6="$_d6"
      d7="$_d7" d8="$_d8" d9="$_d9" d10="$_d10" d11="$_d11" d12="$_d12"
    else
      # Regex fallback for older evaluation formats
      overall=$(grep -m1 "^overall_score:" "$eval_file" 2>/dev/null | awk '{print $2}')
      verdict=$(grep -m1 "^verdict:" "$eval_file" 2>/dev/null | awk '{print $2}')

      d1=$(extract_dim "$eval_file" "D1_narrative\|D1: NARRATIVE")
      d2=$(extract_dim "$eval_file" "D2_framework\|D2: FRAMEWORK")
      d3=$(extract_dim "$eval_file" "D3_content\|D3: CONTENT")
      d4=$(extract_dim "$eval_file" "D4_density\|D4: DENSITY")
      d5=$(extract_dim "$eval_file" "D5_visual\|D5: VISUAL")
      d6=$(extract_dim "$eval_file" "D6_audience\|D6: AUDIENCE")
      d7=$(extract_dim "$eval_file" "D7_complete\|D7: COMPLETE")
      d8=$(extract_dim "$eval_file" "D8_speaker\|D8: SPEAKER")
      d9=$(extract_dim "$eval_file" "D9_structural\|D9: STRUCTURAL")
      d10=$(extract_dim "$eval_file" "D10_html\|D10: HTML")
      d11=$(extract_dim "$eval_file" "D11_insight\|D11: INSIGHT")
      d12=$(extract_dim "$eval_file" "D12_info\|D12: INFORMATION")
    fi

    # Skip files with no scores (pipeline errors)
    if [ -z "$overall" ] || [ "$overall" = "N/A" ]; then
      echo "${round_name},${round_date},${scenario},,ERROR,,,,,,,,,," >> "${CSV}"
      continue
    fi

    echo "${round_name},${round_date},${scenario},${overall},${verdict},${d1},${d2},${d3},${d4},${d5},${d6},${d7},${d8},${d9},${d10},${d11},${d12}" >> "${CSV}"
  done
done

rows=$(tail -n +2 "${CSV}" | wc -l | tr -d ' ')
echo "Wrote ${CSV} (${rows} rows)"

# Pretty-print if requested
if [ "$PRINT" = true ]; then
  echo ""
  echo "=== SCORECARD ==="
  echo ""

  # Print per-round summary
  prev_round=""
  while IFS=, read -r round date scenario score verdict d1 d2 d3 d4 d5 d6 d7 d8 d9 d10 d11 d12; do
    # Skip header
    [ "$round" = "round" ] && continue

    # Round header
    if [ "$round" != "$prev_round" ]; then
      if [ -n "$prev_round" ]; then
        echo "  ----------------------------------------"
      fi
      echo ""
      echo "  ${round} (${date})"
      echo "  ----------------------------------------"
      printf "  %-35s %5s  %-8s  D1 D2 D3 D4 D5 D6 D7 D8 D9 D10 D11 D12\n" "SCENARIO" "SCORE" "VERDICT"
      prev_round="$round"
    fi

    if [ "$verdict" = "ERROR" ]; then
      printf "  %-35s %5s  %-8s\n" "$scenario" "--" "ERROR"
    else
      printf "  %-35s %5s  %-8s  %-2s %-2s %-2s %-2s %-2s %-2s %-2s %-2s %-2s %-2s %-2s %-2s\n" \
        "$scenario" "$score" "$verdict" \
        "$d1" "$d2" "$d3" "$d4" "$d5" "$d6" "$d7" "$d8" "$d9" "$d10" "$d11" "$d12"
    fi
  done < "${CSV}"

  echo ""
  echo ""
  echo "=== DIMENSION AVERAGES BY ROUND ==="
  echo ""
  printf "  %-12s %5s  D1   D2   D3   D4   D5   D6   D7   D8   D9   D10  D11  D12\n" "ROUND" "AVG"

  for round_dir in $(ls -d "${ROUNDS_DIR}"/round-* 2>/dev/null | sort -V); do
    round_name=$(basename "$round_dir")

    # Calculate averages from CSV rows for this round
    # Columns 6-17 are D1-D12 (12 dimensions)
    awk -F, -v rnd="$round_name" '
      $1 == rnd && $5 != "ERROR" && $4 != "" {
        n++
        total += $4
        for (i=6; i<=17; i++) { if ($i != "") { dim[i] += $i; dc[i]++ } }
      }
      END {
        if (n > 0) {
          avg = total / n
          printf "  %-12s %5.1f ", rnd, avg
          for (i=6; i<=17; i++) {
            if (dc[i] > 0) printf " %-3.1f", dim[i]/dc[i]
            else printf " --  "
          }
          printf " (n=%d)\n", n
        }
      }
    ' "${CSV}"
  done

  echo ""
fi

# ---------------------------------------------------------------------------
# Regression check: compare the two most recent rounds and flag score drops.
#
# Thresholds:
#   REGRESSION — overall dropped > 0.3, or any dimension dropped > 0.5
#   NEW FAIL   — verdict went to FAIL, or any dimension hit 1
#   WARNING    — overall dropped any amount (but within regression threshold)
#
# Exit code: 1 if any REGRESSION or NEW FAIL found, 0 otherwise.
# ---------------------------------------------------------------------------
if [ "$CHECK" = true ]; then
  echo ""
  echo "=== REGRESSION CHECK ==="
  echo ""

  # Find the two most recent rounds with valid (non-ERROR) scores
  recent_rounds=$(awk -F, '
    NR > 1 && $5 != "ERROR" && $4 != "" { rounds[$1] = 1 }
    END { for (r in rounds) print r }
  ' "${CSV}" | sort -V | tail -2)

  n_rounds=$(echo "$recent_rounds" | wc -l | tr -d ' ')

  if [ "$n_rounds" -lt 2 ]; then
    echo "  Need at least 2 rounds with valid scores to compare. Found ${n_rounds}."
    echo ""
    exit 0
  fi

  prev_round=$(echo "$recent_rounds" | head -1)
  curr_round=$(echo "$recent_rounds" | tail -1)
  echo "  Comparing: ${curr_round} vs ${prev_round}"
  echo ""

  # Thresholds
  OVERALL_THRESH="0.3"
  DIM_THRESH="0.5"

  # Build comparison using awk. For each scenario present in both rounds,
  # compare overall and per-dimension scores.
  regression_found=false

  awk -F, -v prev="$prev_round" -v curr="$curr_round" \
            -v othresh="$OVERALL_THRESH" -v dthresh="$DIM_THRESH" '
    BEGIN {
      dim_names[6]="D1"; dim_names[7]="D2"; dim_names[8]="D3"; dim_names[9]="D4"
      dim_names[10]="D5"; dim_names[11]="D6"; dim_names[12]="D7"; dim_names[13]="D8"
      dim_names[14]="D9"; dim_names[15]="D10"; dim_names[16]="D11"; dim_names[17]="D12"
      regressions = 0
      warnings = 0
      ok = 0
    }
    NR > 1 && $5 != "ERROR" && $4 != "" {
      if ($1 == prev) {
        prev_overall[$3] = $4
        prev_verdict[$3] = $5
        for (i=6; i<=17; i++) prev_dim[$3, i] = $i
      }
      if ($1 == curr) {
        curr_overall[$3] = $4
        curr_verdict[$3] = $5
        for (i=6; i<=17; i++) curr_dim[$3, i] = $i
      }
    }
    END {
      # Process scenarios present in both rounds
      for (s in curr_overall) {
        if (!(s in prev_overall)) continue

        level = "OK"
        details = ""

        # Check for NEW FAIL
        if (curr_verdict[s] == "FAIL" && prev_verdict[s] != "FAIL") {
          level = "NEW FAIL"
          details = details "  verdict: " prev_verdict[s] " -> FAIL\n"
        }

        # Check per-dimension drops and dimension=1
        for (i=6; i<=17; i++) {
          p = prev_dim[s, i]
          c = curr_dim[s, i]
          if (p == "" || c == "" ) continue
          if (c+0 == 1 && p+0 > 1) {
            if (level != "NEW FAIL") level = "NEW FAIL"
            details = details "  " dim_names[i] ": " p " -> " c " (hit 1)\n"
          } else if (p - c > dthresh + 0) {
            if (level == "OK" || level == "WARNING") level = "REGRESSION"
            details = details "  " dim_names[i] ": " p " -> " c " (-" (p - c) ")\n"
          }
        }

        # Check overall drop
        odrop = prev_overall[s] - curr_overall[s]
        if (odrop > othresh + 0 && level == "OK") {
          level = "REGRESSION"
          details = details "  overall: " prev_overall[s] " -> " curr_overall[s] " (-" odrop ")\n"
        } else if (odrop > 0 && level == "OK") {
          level = "WARNING"
          details = details "  overall: " prev_overall[s] " -> " curr_overall[s] " (-" odrop ")\n"
        }

        # Print result
        if (level == "NEW FAIL" || level == "REGRESSION") {
          regressions++
          printf "  %-12s  %-35s\n", level, s
          printf details
        } else if (level == "WARNING") {
          warnings++
          printf "  %-12s  %-35s\n", level, s
          printf details
        } else {
          ok++
          printf "  %-12s  %-35s  %s -> %s\n", "OK", s, prev_overall[s], curr_overall[s]
        }
      }

      # Summary
      printf "\n  Result: %d regressions, %d warnings, %d ok\n\n", regressions, warnings, ok

      # Exit code: 1 if any regressions or new fails
      if (regressions > 0) exit 1
      exit 0
    }
  ' "${CSV}"

  exit $?
fi
