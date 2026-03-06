#!/bin/bash
# Test: Stage 0 should not exist in researcher/index.md
# Acceptance criteria:
# 1. grep -c 'Stage 0' returns 0
# 2. Section flow goes directly from Research Pipeline intro to Stage 1: Planner

FILE="specialists/researcher/index.md"
PASS=0
FAIL=0

# Test 1: No "Stage 0" references
count=$(grep -c 'Stage 0' "$FILE")
if [ "$count" -eq 0 ]; then
    echo "PASS: No 'Stage 0' references found"
    ((PASS++))
else
    echo "FAIL: Found $count 'Stage 0' references (expected 0)"
    ((FAIL++))
fi

# Test 2: Stage 1 heading still exists
if grep -q '### Stage 1: Planner' "$FILE"; then
    echo "PASS: '### Stage 1: Planner' heading exists"
    ((PASS++))
else
    echo "FAIL: '### Stage 1: Planner' heading is missing"
    ((FAIL++))
fi

# Test 3: Research Pipeline intro flows directly to Stage 1
# The line "Do not skip stages." should be followed (after a blank line) by "### Stage 1: Planner"
# with NO Stage 0 heading in between
between=$(sed -n '/Do not skip stages\./,/### Stage 1: Planner/p' "$FILE" | grep -c '### Stage 0')
if [ "$between" -eq 0 ]; then
    echo "PASS: No Stage 0 between pipeline intro and Stage 1"
    ((PASS++))
else
    echo "FAIL: Stage 0 still exists between pipeline intro and Stage 1"
    ((FAIL++))
fi

# Test 4: The "Open your response" text should be gone
if grep -q 'Open your response' "$FILE"; then
    echo "FAIL: 'Open your response' text still present"
    ((FAIL++))
else
    echo "PASS: 'Open your response' text removed"
    ((PASS++))
fi

# Test 5: "Proceed to Stage 1" instruction should be gone
if grep -q 'Proceed to Stage 1' "$FILE"; then
    echo "FAIL: 'Proceed to Stage 1' text still present"
    ((FAIL++))
else
    echo "PASS: 'Proceed to Stage 1' text removed"
    ((PASS++))
fi

echo ""
echo "Results: $PASS passed, $FAIL failed"
if [ "$FAIL" -gt 0 ]; then
    exit 1
else
    exit 0
fi
