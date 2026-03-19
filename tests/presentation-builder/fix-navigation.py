#!/usr/bin/env python3
"""
Production post-processor for presentation-builder HTML output.

The presentation-builder specialist focuses on creative slide content and visual
design. This script handles all mechanical structure deterministically — analogous
to the formatter pattern used by other specialists, but implemented as a script
rather than an LLM because navigation injection requires no judgment.

This script always runs after presentation-builder in the pipeline. It:

1. Extracts clean HTML — strips prose preamble, markdown fences, trailing commentary
2. Ensures body has overflow: hidden
3. Wraps slides in a .slides-container if missing
4. Adds .active to the first slide if missing
5. Injects the slide engine CSS (position, opacity, transition) if missing
6. Injects speaker notes CSS if missing
7. Injects print support CSS if missing
8. Adds nav dots and slide counter elements if missing
9. Injects the keyboard/click/touch navigation script if missing

Usage:
    python fix-navigation.py <file.html>
    python fix-navigation.py <directory>   # processes all .html files
"""

import re
import sys
from pathlib import Path

NAVIGATION_SCRIPT = """
<script>
const slides = document.querySelectorAll('.slide');
let cur = 0;
const total = slides.length;
const dots = document.querySelector('.nav-dots');
const counter = document.querySelector('.slide-counter');
if (dots) {
  dots.innerHTML = '';
  slides.forEach((_, i) => {
    const d = document.createElement('div');
    d.className = 'nav-dot' + (i === 0 ? ' active' : '');
    d.style.cssText = 'width:8px;height:8px;border-radius:50%;background:rgba(128,128,128,0.4);cursor:pointer;transition:background 0.3s;';
    d.onclick = () => go(i);
    dots.appendChild(d);
  });
}
if (counter) counter.textContent = '1 / ' + total;

function go(n) {
  slides[cur].classList.remove('active');
  cur = (n + total) % total;
  slides[cur].classList.add('active');
  if (dots) dots.querySelectorAll('.nav-dot').forEach((d, i) => {
    d.classList.toggle('active', i === cur);
    d.style.background = i === cur ? 'var(--accent, rgba(128,128,128,0.9))' : 'rgba(128,128,128,0.4)';
  });
  if (counter) counter.textContent = (cur + 1) + ' / ' + total;
}
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); go(cur + 1); }
  if (e.key === 'ArrowLeft') { e.preventDefault(); go(cur - 1); }
  if (e.key === 's' || e.key === 'S') document.body.classList.toggle('show-notes');
});
document.addEventListener('click', e => {
  if (e.target.closest('.nav-dot, .speaker-notes, button, a, input, select')) return;
  e.clientX > innerWidth / 2 ? go(cur + 1) : go(cur - 1);
});
let tx;
document.addEventListener('touchstart', e => { tx = e.changedTouches[0].screenX; });
document.addEventListener('touchend', e => { const d = tx - e.changedTouches[0].screenX; if (Math.abs(d) > 50) d > 0 ? go(cur + 1) : go(cur - 1); });
</script>
""".strip()

NAV_DOTS_HTML = '<div class="nav-dots" style="position:fixed;bottom:20px;left:50%;transform:translateX(-50%);display:flex;gap:8px;z-index:10;"></div>'
COUNTER_HTML = '<div class="slide-counter" style="position:fixed;bottom:20px;right:30px;font-size:13px;opacity:0.5;z-index:10;"></div>'

SLIDE_ENGINE_CSS = """
/* --- injected slide engine --- */
body { overflow: hidden !important; }
.slides-container { position: relative; width: 100vw; height: 100vh; height: 100dvh; overflow: hidden; }
.slides-container > .slide,
.slides-container > section.slide {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  opacity: 0; visibility: hidden;
  transition: opacity 0.4s ease, visibility 0.4s;
  overflow-y: auto; box-sizing: border-box;
}
.slides-container > .slide.active,
.slides-container > section.slide.active { opacity: 1; visibility: visible; }
"""

SPEAKER_NOTES_CSS = """
/* --- injected speaker notes --- */
.speaker-notes { display: none; position: fixed; bottom: 0; left: 0; right: 0; max-height: 40vh; overflow-y: auto;
  padding: clamp(0.75rem, 2vw, 1.5rem); background: rgba(0,0,0,0.92); color: #e0e0e0;
  font-size: clamp(0.7rem, 1.5vw, 0.85rem); line-height: 1.5; z-index: 100; border-top: 2px solid var(--accent, #666); }
.show-notes .speaker-notes { display: block; }
"""

PRINT_CSS = """
/* --- injected print support --- */
@media print {
  body { overflow: visible; }
  .slides-container { position: static; height: auto; }
  .slide { position: static; opacity: 1 !important; visibility: visible !important; page-break-after: always; height: auto; min-height: 100vh; }
  .nav-dots, .slide-counter, .speaker-notes { display: none !important; }
}
"""


# Module-level compiled regex for detecting/renaming wrapper slides.
# Shared by fix_html (step 5) and the process_file quick-check so the two
# paths stay in sync automatically.
#
# Pattern notes:
#   \bslide\b(?!-)  — matches the standalone "slide" class token but never
#                     "slide-wrapper", "slide-title", etc.  Without (?!-),
#                     plain \bslide\b fires on "slide-" because '-' is a
#                     non-word character that satisfies the \b assertion.
#   "(?:\s[^>]*)?>  — tolerates extra attributes after the class attribute
#                     without accidentally consuming into the next tag.
_WRAPPER_RE = re.compile(
    r'(<(?:div|section)\s+[^>]*class=")'  # opening tag up to class="
    r'([^"]*\bslide\b(?!-)[^"]*)'  # standalone "slide" token in class list
    r'("(?:\s[^>]*)?>)'  # closing of the opening tag
    r"(.*?)"  # inner content (lazy — stops at first matching close)
    r"(</(?:div|section)>)",  # closing tag
    re.DOTALL,
)


def _has_nested_wrappers(html: str) -> bool:
    """Return True if any element with a standalone 'slide' class contains
    descendant elements that also carry a standalone 'slide' class.

    Uses the same regex and inner-content check as fix_html step 5 so the
    quick-check in process_file is always consistent with the fixer logic.
    """
    for match in _WRAPPER_RE.finditer(html):
        inner = match.group(4)
        # Require an actual HTML opening tag before the nested class= so that
        # sibling slide text / class names like "slide-title" on child elements
        # don't produce false positives.
        if re.search(r'<[^>]+class="[^"]*\bslide\b(?!-)', inner):
            return True
    return False


def extract_html(content: str) -> tuple[str, bool]:
    """Extract clean HTML from agent output that may include prose and markdown fences.
    Returns (html, was_extracted)."""
    # Find the start of HTML
    start = None
    for pattern in [r"<!DOCTYPE\s+html", r"<html"]:
        m = re.search(pattern, content, re.IGNORECASE)
        if m:
            start = m.start()
            break

    if start is None:
        return content, False

    # Find the end of HTML
    end = content.rfind("</html>")
    if end == -1:
        return content, False
    end += len("</html>")

    html = content[start:end].strip()
    if len(html) < 500:
        return content, False

    # Only consider it "extracted" if there is actual non-whitespace prose
    # before the HTML start or after the HTML end.  A bare trailing newline
    # (very common from editors) must NOT set was_extracted=True — that would
    # bypass the quick-check and force reprocessing on every run.
    was_extracted = (start > 0 and content[:start].strip() != "") or (
        content[end:].strip() != ""
    )
    return html, was_extracted


def fix_html(html: str) -> tuple[str, list[str]]:
    """Fix navigation in an HTML presentation. Returns (fixed_html, list_of_changes)."""
    changes = []

    # 1. Ensure body overflow: hidden
    if "overflow: hidden" not in html and "overflow:hidden" not in html:
        html = re.sub(
            r"(body\s*\{[^}]*)",
            r"\1 overflow: hidden;",
            html,
            count=1,
        )
        if "overflow: hidden" in html:
            changes.append("Added overflow:hidden to body")
        else:
            # body rule might not exist, inject into style block
            html = html.replace("</style>", "body { overflow: hidden; }\n</style>", 1)
            changes.append("Injected body { overflow: hidden } rule")

    # 2. Check for slides - support both <div class="slide"> and <section class="slide">
    # Use \bslide\b(?!-) so that "slides-container" (no boundary at e/s) and
    # "slide-wrapper" / "slide-title" (boundary at e/- but negative lookahead)
    # are never mistaken for content slides.
    slide_pattern = re.compile(
        r'<(div|section)\s+[^>]*class="[^"]*\bslide\b(?!-)[^"]*"', re.IGNORECASE
    )
    slides = list(slide_pattern.finditer(html))

    if not slides:
        return html, ["ERROR: No slide elements found"]

    # 3. Ensure first slide has .active class
    first_slide = slides[0]
    first_slide_text = first_slide.group(0)
    if "active" not in first_slide_text:
        # Use a token-aware substitution so that class="slide-something" is never
        # accidentally mutated into class="slide active-something".
        fixed = re.sub(
            r'(class="[^"]*)\bslide\b(?!-)',
            r"\1slide active",
            first_slide_text,
            count=1,
        )
        html = html[: first_slide.start()] + fixed + html[first_slide.end() :]
        changes.append("Added 'active' class to first slide")

    # 4. Wrap slides in .slides-container if missing
    if "slides-container" not in html:
        # Find the first and last slide elements, wrap them
        # Re-find slides after potential modification
        slides_found = list(slide_pattern.finditer(html))
        if slides_found:
            first_start = slides_found[0].start()
            # Find the closing tag of the last slide
            last_slide = slides_found[-1]
            tag_name = last_slide.group(1)  # div or section
            # Find the closing tag after the last slide's opening
            rest = html[last_slide.end() :]
            # Count nesting to find the matching close
            depth = 1
            pos = 0
            open_pattern = re.compile(rf"<{tag_name}\b", re.IGNORECASE)
            close_pattern = re.compile(rf"</{tag_name}>", re.IGNORECASE)
            while depth > 0 and pos < len(rest):
                next_open = open_pattern.search(rest, pos)
                next_close = close_pattern.search(rest, pos)
                if next_close is None:
                    break
                if next_open and next_open.start() < next_close.start():
                    depth += 1
                    pos = next_open.end()
                else:
                    depth -= 1
                    pos = next_close.end()
            last_end = last_slide.end() + pos

            html = (
                html[:first_start]
                + '<div class="slides-container">\n'
                + html[first_start:last_end]
                + "\n</div>"
                + html[last_end:]
            )
            changes.append("Wrapped slides in .slides-container")

    # 5. Flatten nested slide wrappers
    # The model sometimes wraps all slides in a container div that also has
    # class "slide" (e.g., <div class="slide actives-container">). This breaks
    # the child-combinator CSS (.slides-container > .slide) because the real
    # slides aren't direct children. Fix: remove "slide" from any element that
    # contains other .slide elements — it's a wrapper, not a content slide.
    # All correctness constraints are documented on the module-level _WRAPPER_RE.
    for match in list(_WRAPPER_RE.finditer(html)):
        inner_content = match.group(4)
        # Require a real HTML opening tag before the nested "slide" class so
        # that sibling slide text / inline mentions don't count as nesting.
        if re.search(r'<[^>]+class="[^"]*\bslide\b(?!-)', inner_content):
            # This element contains nested .slide elements — it's a wrapper
            old_class = match.group(2)
            # Replace only the exact bare "slide" token; never touch compound
            # tokens like "slide-wrapper" or "slide-title".
            new_class = " ".join(
                "slide-wrapper" if token == "slide" else token
                for token in old_class.split()
            )
            html = html[: match.start(2)] + new_class + html[match.end(2) :]
            changes.append(f"Renamed wrapper class '{old_class}' to '{new_class}'")
            break  # re-find after modification to avoid offset issues

    # 6. Inject slide engine CSS into style block
    # Check if slides already use position: absolute
    has_absolute = bool(re.search(r"\.slide\s*\{[^}]*position:\s*absolute", html))
    if not has_absolute:
        # Strip model's display:none/flex visibility pattern — conflicts with
        # the injected opacity/visibility engine. The model often writes its own
        # slide visibility system (display:none + .active{display:flex}) which
        # fights the injected engine (opacity:0 + .active{opacity:1}).
        # Remove display:none from .slide rules and display:flex from .slide.active.
        html = re.sub(
            r"(\.slide\s*\{[^}]*?)display\s*:\s*none\s*;?\s*",
            r"\1",
            html,
        )
        html = re.sub(
            r"(\.slide\.active\s*\{[^}]*?)display\s*:\s*flex\s*;?\s*",
            r"\1",
            html,
        )
        changes.append("Stripped model's display:none/flex visibility pattern")
        html = html.replace("</style>", SLIDE_ENGINE_CSS + "\n</style>", 1)
        changes.append("Injected slide engine CSS (position:absolute + opacity)")

    # 7. Inject speaker notes CSS if missing
    if ".speaker-notes" not in html:
        html = html.replace("</style>", SPEAKER_NOTES_CSS + "\n</style>", 1)
        changes.append("Injected speaker notes CSS")

    # 8. Inject print support CSS if missing
    if "@media print" not in html:
        html = html.replace("</style>", PRINT_CSS + "\n</style>", 1)
        changes.append("Injected print support CSS (@media print)")

    # 9. Add nav dots and counter if missing
    if "nav-dots" not in html:
        html = html.replace("</body>", NAV_DOTS_HTML + "\n</body>", 1)
        changes.append("Added nav-dots element")

    if "slide-counter" not in html:
        html = html.replace("</body>", COUNTER_HTML + "\n</body>", 1)
        changes.append("Added slide-counter element")

    # 10. Inject navigation script if missing
    has_script = bool(re.search(r"<script\b", html))
    has_arrow = "ArrowRight" in html
    if not has_script or not has_arrow:
        # Remove any existing broken script blocks (e.g., scroll-based nav)
        if has_script and not has_arrow:
            html = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.DOTALL)
            changes.append("Removed broken script block (no arrow key navigation)")

        html = html.replace("</body>", NAVIGATION_SCRIPT + "\n</body>", 1)
        changes.append("Injected navigation script (arrow keys, click, touch)")

    return html, changes


def process_file(path: Path) -> bool:
    """Process a single HTML file. Returns True if changes were made."""
    content = path.read_text(encoding="utf-8")
    changes = []

    # Step 0: Extract clean HTML if wrapped in prose/markdown
    html, was_extracted = extract_html(content)
    if was_extracted:
        changes.append(f"Extracted HTML ({len(html)} bytes from {len(content)} bytes)")

    # Quick check: does it already have all post-processor components?
    has_script = bool(re.search(r"<script\b", html))
    has_arrow = "ArrowRight" in html
    has_container = "slides-container" in html
    has_speaker_notes_css = ".speaker-notes" in html
    has_print_css = "@media print" in html

    # Also check for conflicting display:none visibility pattern from the model
    has_display_none_conflict = bool(
        re.search(r"\.slide\s*\{[^}]*display\s*:\s*none", html)
        or re.search(r"\.slide\{[^}]*display\s*:\s*none", html)
    )

    # Check for nested slide wrapper (a .slide element containing other .slide elements).
    # Uses the shared _has_nested_wrappers() helper so this check is always
    # identical to what fix_html step 5 would actually act on — eliminating the
    # class of bug where the quick-check forces a re-run but fix_html finds
    # nothing to fix (infinite churn on already-clean files).
    has_nested_wrapper = _has_nested_wrappers(html)

    if (
        has_script
        and has_arrow
        and has_container
        and has_speaker_notes_css
        and has_print_css
        and not was_extracted
        and not has_display_none_conflict
        and not has_nested_wrapper
    ):
        print(f"  OK: {path.name} (all post-processor components present)")
        return False

    fixed, nav_changes = fix_html(html)
    changes.extend(nav_changes)

    if changes:
        path.write_text(fixed, encoding="utf-8")
        print(f"  FIXED: {path.name}")
        for c in changes:
            print(f"    - {c}")
        return True
    else:
        print(f"  OK: {path.name} (no changes needed)")
        return False


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file.html | directory>")
        sys.exit(1)

    target = Path(sys.argv[1])

    if target.is_file():
        process_file(target)
    elif target.is_dir():
        files = sorted(target.glob("*-output.html"))
        if not files:
            files = sorted(target.glob("*.html"))
        if not files:
            print(f"No HTML files found in {target}")
            sys.exit(1)

        fixed_count = 0
        for f in files:
            if process_file(f):
                fixed_count += 1
        print(f"\nProcessed {len(files)} files, fixed {fixed_count}")
    else:
        print(f"Not found: {target}")
        sys.exit(1)


if __name__ == "__main__":
    main()
