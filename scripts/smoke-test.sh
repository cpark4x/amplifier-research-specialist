#!/usr/bin/env bash
# =============================================================================
# Smoke Test — End-to-end research pipeline validation
# =============================================================================
#
# Runs the research-chain recipe on a simple topic and verifies the output
# contains the expected structural markers from each pipeline stage.
#
# Usage:
#   ./scripts/smoke-test.sh                    # default topic
#   ./scripts/smoke-test.sh "Custom question"  # custom topic
#
# Requirements:
#   - amplifier CLI installed and on PATH
#   - API key configured (ANTHROPIC_API_KEY or in ~/.amplifier/keys.env)
#   - Run from the repo root (or anywhere — script finds its own root)
#
# Cost: One full pipeline run (~5-15 minutes, standard API costs)
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="$REPO_ROOT/docs/research-output"
TOPIC="${1:-What is markdown and why is it widely used}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}  PASS${NC} $1"; }
fail() { echo -e "${RED}  FAIL${NC} $1"; FAILURES=$((FAILURES + 1)); }
warn() { echo -e "${YELLOW}  WARN${NC} $1"; }

FAILURES=0

echo "============================================="
echo "  Smoke Test — Research Pipeline"
echo "============================================="
echo ""
echo "Topic: $TOPIC"
echo "Time:  $(date)"
echo ""

# --- Pre-flight ---
if ! command -v amplifier &>/dev/null; then
  echo -e "${RED}ERROR: amplifier CLI not found on PATH${NC}"
  exit 1
fi

# Snapshot existing output files so we can find the new one
BEFORE=$(ls "$OUTPUT_DIR"/*.md 2>/dev/null | sort || true)

# --- Run the pipeline ---
echo "Running research-chain recipe..."
echo "(This takes 5-15 minutes)"
echo ""

cd "$REPO_ROOT"
amplifier tool invoke recipes \
  operation=execute \
  recipe_path="specialists:recipes/research-chain.yaml" \
  context="{\"research_question\": \"$TOPIC\"}" \
  2>&1 | tail -5

echo ""

# --- Find the new output file ---
AFTER=$(ls "$OUTPUT_DIR"/*.md 2>/dev/null | sort || true)
NEW_FILE=$(comm -13 <(echo "$BEFORE") <(echo "$AFTER") | head -1)

if [ -z "$NEW_FILE" ]; then
  echo -e "${RED}FAIL: No new output file found in $OUTPUT_DIR${NC}"
  exit 1
fi

echo "Output: $NEW_FILE"
echo ""
echo "--- Structural Checks ---"

# --- Check file size ---
BYTES=$(wc -c < "$NEW_FILE")
if [ "$BYTES" -gt 500 ]; then
  pass "File size: ${BYTES} bytes (>500)"
else
  fail "File size: ${BYTES} bytes (<500 — likely truncated)"
fi

# --- Check structural markers from each pipeline stage ---
check_marker() {
  local marker="$1"
  local label="$2"
  if grep -qi "$marker" "$NEW_FILE"; then
    pass "$label"
  else
    fail "$label — marker '$marker' not found"
  fi
}

check_marker "Parsed:"              "Writer formatter produced Parsed: line"
check_marker "confidence"           "Confidence assessments present"
check_marker "source"               "Source references present"
check_marker "S[0-9]"              "S-numbered claims present"

echo ""
if [ "$FAILURES" -eq 0 ]; then
  echo -e "${GREEN}SMOKE TEST PASSED${NC} — Pipeline produced valid output."
else
  echo -e "${RED}SMOKE TEST FAILED${NC} — $FAILURES check(s) failed."
  exit 1
fi