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
#
# Output: tests/presentation-builder/rounds/scorecard.csv
#
# =============================================================================

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROUNDS_DIR="${SCRIPT_DIR}/rounds"
CSV="${ROUNDS_DIR}/scorecard.csv"
PRINT=false
[[ "${1:-}" == "--print" ]] && PRINT=true

# Write CSV header
echo "round,date,scenario,overall_score,verdict,D1_narrative,D2_framework,D3_fidelity,D4_density,D5_rhythm,D6_audience,D7_completeness,D8_notes,D9_structure,D10_html,D11_insight,D12_infodesign" > "${CSV}"

# Extract score from either format:
#   Old: "D1_narrative_coherence: 3/5 | ..." (v1-v2 evaluations)
#   New: "Score: 3/5" after "D1: NARRATIVE COHERENCE" header (v3+ evaluations)
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
    overall=$(grep -m1 "^overall_score:" "$eval_file" 2>/dev/null | awk '{print $2}')
    verdict=$(grep -m1 "^verdict:" "$eval_file" 2>/dev/null | awk '{print $2}')

    # Skip files with no scores (pipeline errors)
    if [ -z "$overall" ] || [ "$overall" = "N/A" ]; then
      echo "${round_name},${round_date},${scenario},,ERROR,,,,,,,,,," >> "${CSV}"
      continue
    fi

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
