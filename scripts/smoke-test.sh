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
#   ./scripts/smoke-test.sh --check            # just validate most recent output
#
# Requirements:
#   - amplifier CLI installed and on PATH
#   - API key configured (ANTHROPIC_API_KEY or in ~/.amplifier/keys.env)
#   - Run from the repo root (or anywhere — script finds its own root)
#
# Cost: One full pipeline run (~15-20 minutes, standard API costs)
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
OUTPUT_DIR="$REPO_ROOT/docs/research-output"
MAX_WAIT=1800  # 30 minutes max

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}  PASS${NC} $1"; }
fail() { echo -e "${RED}  FAIL${NC} $1"; FAILURES=$((FAILURES + 1)); }

FAILURES=0

# --- Validate a single output file ---
validate_output() {
  local file="$1"
  echo ""
  echo "Output: $file"
  echo ""
  echo "--- Structural Checks ---"

  # Check file size
  local bytes
  bytes=$(wc -c < "$file")
  if [ "$bytes" -gt 500 ]; then
    pass "File size: ${bytes} bytes (>500)"
  else
    fail "File size: ${bytes} bytes (<500 — likely truncated)"
  fi

  # Check structural markers from each pipeline stage
  check_marker() {
    local marker="$1"
    local label="$2"
    if grep -qi "$marker" "$file"; then
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
}

# --- --check mode: validate most recent output file ---
if [ "${1:-}" = "--check" ]; then
  echo "============================================="
  echo "  Smoke Test — Validate Latest Output"
  echo "============================================="
  LATEST=$(ls -t "$OUTPUT_DIR"/*.md 2>/dev/null | head -1)
  if [ -z "$LATEST" ]; then
    echo -e "${RED}ERROR: No output files in $OUTPUT_DIR${NC}"
    exit 1
  fi
  validate_output "$LATEST"
  exit 0
fi

# --- Full run mode ---
TOPIC="${1:-What is markdown and why is it widely used}"

echo "============================================="
echo "  Smoke Test — Research Pipeline"
echo "============================================="
echo ""
echo "Topic: $TOPIC"
echo "Time:  $(date)"
echo ""

# Pre-flight
if ! command -v amplifier &>/dev/null; then
  echo -e "${RED}ERROR: amplifier CLI not found on PATH${NC}"
  exit 1
fi

# Snapshot existing output files
BEFORE=$(ls "$OUTPUT_DIR"/*.md 2>/dev/null | sort || true)

# Run the pipeline in the background
echo "Starting research-chain recipe..."
echo "(Pipeline runs in background — polling for output file)"
echo ""

cd "$REPO_ROOT"
amplifier tool invoke recipes \
  operation=execute \
  recipe_path="$REPO_ROOT/recipes/research-chain.yaml" \
  context="{\"research_question\": \"$TOPIC\"}" \
  >/dev/null 2>&1 &
RECIPE_PID=$!

# Poll for new output file
ELAPSED=0
POLL_INTERVAL=30
NEW_FILE=""

while [ "$ELAPSED" -lt "$MAX_WAIT" ]; do
  sleep "$POLL_INTERVAL"
  ELAPSED=$((ELAPSED + POLL_INTERVAL))

  AFTER=$(ls "$OUTPUT_DIR"/*.md 2>/dev/null | sort || true)
  NEW_FILE=$(comm -13 <(echo "$BEFORE") <(echo "$AFTER") | head -1)

  if [ -n "$NEW_FILE" ]; then
    echo "Output file appeared after ${ELAPSED}s"
    # Give it a moment to finish writing
    sleep 5
    break
  fi

  MINS=$((ELAPSED / 60))
  SECS=$((ELAPSED % 60))
  echo "  Waiting... ${MINS}m${SECS}s elapsed"
done

# Clean up background process
kill "$RECIPE_PID" 2>/dev/null || true

if [ -z "$NEW_FILE" ]; then
  echo -e "${RED}FAIL: No new output file after ${MAX_WAIT}s${NC}"
  echo "Check recipe status: amplifier tool invoke recipes operation=list"
  exit 1
fi

validate_output "$NEW_FILE"
