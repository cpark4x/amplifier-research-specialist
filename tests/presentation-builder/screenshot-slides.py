#!/usr/bin/env python3
"""
screenshot-slides.py -- Capture per-slide screenshots from an HTML presentation.

Uses agent-browser CLI to open the presentation in a headless browser and
capture a PNG screenshot of each slide. Works by replacing document.body with
each slide's content in turn, which avoids CSS cascade issues that can cause
slides to render with zero dimensions in headless mode.

Requirements:
    - agent-browser CLI installed: npm install -g agent-browser
    - Chromium downloaded: agent-browser install

Usage:
    python3 screenshot-slides.py <html_path> <output_dir>

Output:
    <output_dir>/slide-01.png
    <output_dir>/slide-02.png
    ...

Prints a machine-readable summary line at the end:
    SCREENSHOTS: <count> slides captured in <output_dir>
"""

import os
import re
import subprocess
import sys
import time

# Seconds to wait for initial page render
RENDER_WAIT = 2
# Seconds to wait after replacing body content before screenshotting
SWAP_WAIT = 0.5
# Seconds to wait after a navigation action before checking state
NAV_WAIT = 0.3

# JavaScript: detect slides using \bslide\b word boundary match
# (excludes slides-container and slide-wrapper to find actual slide elements)
# Stores each slide's outerHTML in window.__slides for later retrieval.
INIT_JS = r"""
(() => {
    const re = /\bslide\b(?!-)/;
    const slides = [...document.querySelectorAll('div, section')].filter(el =>
        re.test(el.className)
        && !el.className.includes('slides-container')
        && !el.className.includes('slide-wrapper'));
    window.__slides = slides.map(s => s.outerHTML);
    window.__originalBody = document.body.innerHTML;
    return slides.length;
})()
""".strip()

# JavaScript template: replace body with slide N, forced to fill viewport.
# {idx} is replaced by the 0-based slide index at call time.
SHOW_SLIDE_JS = """
(() => {{
    const html = window.__slides[{idx}];
    if (!html) return 'MISSING';
    document.body.innerHTML = html;
    const s = document.body.firstElementChild;
    s.style.cssText = 'display:flex !important; flex-direction:column !important; '
        + 'width:100vw !important; height:100vh !important; '
        + 'opacity:1 !important; visibility:visible !important; '
        + 'overflow:hidden !important; box-sizing:border-box !important;';
    return 'OK';
}})()
""".strip()


# JavaScript: test keyboard navigation by simulating ArrowRight then ArrowLeft.
# Returns a JSON object with test results. Runs BEFORE screenshot capture
# (which replaces body content) so the deck's actual navigation JS is exercised.
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


def test_navigation(slide_count):
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
    import json

    try:
        # Find JSON object in output
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

    # -- Open presentation --
    print(f"Opening: {file_url}")
    ab("open", file_url)
    time.sleep(RENDER_WAIT)

    # -- Detect and cache slides --
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

    print(f"Found {slide_count} slides")

    # -- Test navigation functionality --
    # Run BEFORE screenshot capture (which replaces body content).
    # The deck's actual JS event handlers are exercised here.
    time.sleep(NAV_WAIT)
    nav = test_navigation(slide_count)
    print(
        f"\nNAV_TEST: has_script={nav['has_script']} "
        f"nav_works={nav['nav_works']} "
        f"notes_toggle={nav['notes_toggle']}"
    )
    for detail in nav.get("details", []):
        print(f"  {detail}")
    print()

    # -- Screenshot each slide --
    # For each slide: replace body content with that slide's outerHTML,
    # force it to fill the viewport, then screenshot.
    screenshots = []
    for i in range(slide_count):
        js = SHOW_SLIDE_JS.format(idx=i)
        out, ok = ab("eval", js)
        if not ok or "OK" not in (out or ""):
            print(
                f"  WARNING: slide {i + 1} swap failed ({out!r}), skipping",
                file=sys.stderr,
            )
            continue

        time.sleep(SWAP_WAIT)
        path = os.path.join(output_dir, f"slide-{i + 1:02d}.png")
        ab("screenshot", path)
        screenshots.append(path)
        print(f"  [{i + 1}/{slide_count}] {os.path.basename(path)}")

    # -- Cleanup --
    ab("close")
    print(f"\nSCREENSHOTS: {len(screenshots)} slides captured in {output_dir}")
    print(
        f"NAV_RESULT: has_script={nav['has_script']} "
        f"nav_works={nav['nav_works']} "
        f"notes_toggle={nav['notes_toggle']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
