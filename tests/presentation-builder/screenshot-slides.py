#!/usr/bin/env python3
"""
screenshot-slides.py -- Capture per-slide screenshots from an HTML presentation.

Uses agent-browser CLI to open the presentation in a headless browser and
capture a PNG screenshot of each slide. Navigates the live deck by dispatching
ArrowRight keyboard events and screenshots after each transition settles.

Requirements:
    - agent-browser CLI installed: npm install -g agent-browser
    - Chromium downloaded: agent-browser install

Usage:
    python3 screenshot-slides.py <html_path> <output_dir>

Output:
    <output_dir>/slide-01.png
    <output_dir>/slide-02.png
    ...

Prints machine-readable summary lines at the end:
    SCREENSHOTS: <count> slides captured in <output_dir>
    NAV_RESULT: <json>
"""

import json
import os
import re
import subprocess
import sys
import time

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Seconds to wait for initial page render
RENDER_WAIT = 2
# Seconds to wait after dispatching ArrowRight for transition to settle
TRANSITION_WAIT = 1
# Seconds to wait after a navigation action before checking state (nav test)
NAV_WAIT = 0.3
# Maximum slides to capture (safety cap against circular navigation)
MAX_SLIDES = 50
# Consecutive unchanged attempts before declaring end-of-deck
END_THRESHOLD = 3

# ---------------------------------------------------------------------------
# JavaScript snippets
# ---------------------------------------------------------------------------

# Detect slides using \bslide\b word-boundary match (excludes slides-container
# and slide-wrapper to find actual slide elements). Stores count for reporting.
INIT_JS = r"""
(() => {
    const re = /\bslide\b(?!-)/;
    const slides = [...document.querySelectorAll('div, section')].filter(el =>
        re.test(el.className)
        && !el.className.includes('slides-container')
        && !el.className.includes('slide-wrapper'));
    window.__slide_count = slides.length;
    return slides.length;
})()
""".strip()

# Returns the 0-based index of the currently active slide, or -1 if none found.
# Uses the same \bslide\b filter as INIT_JS / NAV_TEST_JS for consistency.
# Primary detection: .active class. Fallback: computed opacity/visibility/display.
ACTIVE_SLIDE_JS = r"""
(function() {
    var re = /\bslide\b(?!-)/;
    var slides = [...document.querySelectorAll('div, section')].filter(function(el) {
        return re.test(el.className)
            && !el.className.includes('slides-container')
            && !el.className.includes('slide-wrapper');
    });
    // Primary: .active class
    for (var i = 0; i < slides.length; i++) {
        if (slides[i].classList.contains('active')) return i;
    }
    // Fallback: computed visibility (opacity:1, not hidden, not display:none)
    for (var i = 0; i < slides.length; i++) {
        var style = window.getComputedStyle(slides[i]);
        if (style.opacity === '1'
                && style.visibility !== 'hidden'
                && style.display !== 'none') return i;
    }
    return -1;
})()
""".strip()

# Dispatch ArrowRight keydown to advance the deck one slide.
ARROW_RIGHT_JS = (
    "document.dispatchEvent(new KeyboardEvent('keydown', "
    "{key: 'ArrowRight', code: 'ArrowRight', keyCode: 39, bubbles: true}));"
)

# JavaScript: test keyboard navigation by simulating ArrowRight then ArrowLeft.
# Returns a JSON object with test results. Runs BEFORE screenshot capture
# so the deck's actual navigation JS is exercised on the live DOM.
NAV_TEST_JS = r"""
(() => {
    const results = {has_script: false, nav_works: false, notes_toggle: false,
                     slide_count: 0, details: []};

    // Check if any <script> tag exists
    results.has_script = document.querySelectorAll('script').length > 0;
    if (!results.has_script) {
        results.details.push('No <script> tags found');
        return JSON.stringify(results);
    }

    // Find slides using the same pattern as INIT_JS
    const re = /\bslide\b(?!-)/;
    const slides = [...document.querySelectorAll('div, section')].filter(el =>
        re.test(el.className)
        && !el.className.includes('slides-container')
        && !el.className.includes('slide-wrapper'));
    results.slide_count = slides.length;

    if (slides.length < 2) {
        results.details.push('Need 2+ slides to test navigation');
        return JSON.stringify(results);
    }

    // Find which slide is currently visible (has .active or is visible)
    const getActive = () => {
        const active = slides.findIndex(s => s.classList.contains('active'));
        if (active >= 0) return active;
        return slides.findIndex(s => {
            const st = getComputedStyle(s);
            return st.opacity !== '0' && st.visibility !== 'hidden'
                   && st.display !== 'none';
        });
    };

    const before = getActive();

    // Simulate ArrowRight keydown
    document.dispatchEvent(new KeyboardEvent('keydown', {key: 'ArrowRight', bubbles: true}));

    // Check if slide changed (small delay handled by caller)
    setTimeout(() => {}, 50);
    const after = getActive();
    if (after !== before && after >= 0) {
        results.nav_works = true;
        results.details.push('ArrowRight: slide ' + before + ' -> ' + after);
    } else {
        results.details.push('ArrowRight: no slide change (before=' + before + ' after=' + after + ')');
    }

    // Simulate ArrowLeft to go back
    document.dispatchEvent(new KeyboardEvent('keydown', {key: 'ArrowLeft', bubbles: true}));

    // Test S-key for speaker notes toggle
    const notesBefore = document.querySelector('.speaker-notes, [class*="speaker-note"]');
    const notesVisBefore = notesBefore ? getComputedStyle(notesBefore).display : null;
    document.dispatchEvent(new KeyboardEvent('keydown', {key: 's', bubbles: true}));
    const notesAfter = notesBefore ? getComputedStyle(notesBefore).display : null;
    if (notesBefore && notesVisBefore !== notesAfter) {
        results.notes_toggle = true;
        results.details.push('S-key: notes toggled (' + notesVisBefore + ' -> ' + notesAfter + ')');
    } else if (!notesBefore) {
        results.details.push('S-key: no .speaker-notes element found');
    } else {
        results.details.push('S-key: no visibility change');
    }

    return JSON.stringify(results);
})()
""".strip()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def ab(*args, timeout=30):
    """Run an agent-browser CLI command. Returns (stdout, success)."""
    try:
        result = subprocess.run(
            ["agent-browser", *args],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.stdout.strip(), result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT: agent-browser {' '.join(args)}", file=sys.stderr)
        return "", False
    except FileNotFoundError:
        print(
            "ERROR: agent-browser not found. Install with: npm install -g agent-browser",
            file=sys.stderr,
        )
        sys.exit(1)


def parse_active_index(output: str) -> int:
    """Extract the integer active-slide index from agent-browser eval output.

    The JS returns a bare integer (-1, 0, 1, …); agent-browser echoes it as
    plain text, possibly with surrounding whitespace or a trailing newline.
    """
    m = re.search(r"-?\d+", output or "")
    return int(m.group()) if m else -1


def test_navigation(slide_count: int) -> dict:
    """Test keyboard navigation and speaker notes toggle. Returns dict with results."""
    if slide_count < 2:
        return {
            "has_script": False,
            "nav_works": False,
            "notes_toggle": False,
            "slide_count": slide_count,
            "details": ["Skipped: <2 slides"],
        }

    out, ok = ab("eval", NAV_TEST_JS)
    if not ok or not out:
        return {
            "has_script": False,
            "nav_works": False,
            "notes_toggle": False,
            "slide_count": slide_count,
            "details": [f"eval failed: {out!r}"],
        }

    # Parse JSON from agent-browser output (may have extra text around it)
    try:
        start = out.index("{")
        end = out.rindex("}") + 1
        return json.loads(out[start:end])
    except (ValueError, json.JSONDecodeError):
        return {
            "has_script": False,
            "nav_works": False,
            "notes_toggle": False,
            "slide_count": slide_count,
            "details": [f"JSON parse failed: {out!r}"],
        }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    if len(sys.argv) < 3:
        print("Usage: screenshot-slides.py <html_path> <output_dir>", file=sys.stderr)
        return 1

    html_path = os.path.abspath(sys.argv[1])
    output_dir = sys.argv[2]

    if not os.path.isfile(html_path):
        print(f"ERROR: File not found: {html_path}", file=sys.stderr)
        return 1

    os.makedirs(output_dir, exist_ok=True)
    file_url = f"file://{html_path}"

    print(f"SCREENSHOT_DIR: {output_dir}")

    # -- Open presentation --
    print(f"Opening: {file_url}")
    ab("open", file_url)
    time.sleep(RENDER_WAIT)

    # -- Count slides --
    count_out, ok = ab("eval", INIT_JS)
    if not ok or not count_out:
        print(
            f"ERROR: Could not detect slides (output: {count_out!r})", file=sys.stderr
        )
        ab("close")
        return 1

    match = re.search(r"(\d+)", count_out)
    if not match:
        print(
            f"ERROR: Could not parse slide count from: {count_out!r}", file=sys.stderr
        )
        ab("close")
        return 1

    slide_count = int(match.group(1))
    if slide_count == 0:
        print("ERROR: No slides found in presentation", file=sys.stderr)
        ab("close")
        return 1

    print(f"Found {slide_count} slides (expected)")

    # -- Test navigation functionality --
    # Run BEFORE the capture loop while the deck's JS event handlers are live.
    # NAV_TEST_JS dispatches ArrowRight then ArrowLeft, so we should land back
    # on slide 1 when it finishes. Give it a moment to settle.
    time.sleep(NAV_WAIT)
    nav = test_navigation(slide_count)
    nav_json = json.dumps(nav)

    if not nav["nav_works"]:
        print(
            "WARNING: Navigation test reports nav_works=false"
            " — attempting capture anyway (may be a false negative)"
        )
    for detail in nav.get("details", []):
        print(f"  {detail}")

    time.sleep(NAV_WAIT)  # Let any ArrowLeft from nav test finish animating

    # -- Capture loop: arrow-key navigation --
    #
    # Strategy:
    #   1. Screenshot the current (first) slide immediately.
    #   2. Dispatch ArrowRight, wait TRANSITION_WAIT seconds.
    #   3. Query which slide is now active.
    #   4a. If active index changed  → screenshot, repeat from 2.
    #   4b. If active index unchanged → increment stall counter.
    #        After END_THRESHOLD consecutive stalls → end of deck, stop.
    #   Safety cap: never exceed MAX_SLIDES total captures.

    screenshots: list[str] = []

    # Snapshot the active index before we touch anything
    out, _ = ab("eval", ACTIVE_SLIDE_JS)
    current_active = parse_active_index(out)

    # Screenshot slide 1 — already visible on load
    slide_num = 1
    fname = f"slide-{slide_num:02d}.png"
    path = os.path.join(output_dir, fname)
    ab("screenshot", path)
    screenshots.append(fname)
    print(f"Captured slide {slide_num}/{slide_count}: {fname}")

    consecutive_unchanged = 0

    while slide_num < MAX_SLIDES:
        # Advance the deck
        ab("eval", ARROW_RIGHT_JS)
        time.sleep(TRANSITION_WAIT)

        # Check whether the active slide index moved
        out, _ = ab("eval", ACTIVE_SLIDE_JS)
        new_active = parse_active_index(out)

        if new_active == current_active:
            # Slide did not change — stall detected
            consecutive_unchanged += 1
            if consecutive_unchanged >= END_THRESHOLD:
                print(
                    f"  Slide unchanged after {END_THRESHOLD} consecutive"
                    f" ArrowRight attempts — reached end of deck at slide {slide_num}"
                )
                break
            # Try once more without incrementing slide_num
            continue

        # Slide changed successfully
        consecutive_unchanged = 0
        current_active = new_active
        slide_num += 1
        fname = f"slide-{slide_num:02d}.png"
        path = os.path.join(output_dir, fname)
        ab("screenshot", path)
        screenshots.append(fname)
        print(f"Captured slide {slide_num}/{slide_count}: {fname}")

    if slide_num >= MAX_SLIDES:
        print(
            f"WARNING: Hit safety cap of {MAX_SLIDES} slides — stopping early",
            file=sys.stderr,
        )

    # -- Cleanup --
    ab("close")

    # Machine-readable summary lines (eval recipe parses these)
    print(f"FILES: {' '.join(screenshots)}")
    print(f"NAV_TEST: {nav_json}")
    print(f"SCREENSHOTS: {len(screenshots)} slides captured in {output_dir}")
    print(f"NAV_RESULT: {nav_json}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
