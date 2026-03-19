# Presentation Builder Redesign — Model Owns Everything

## Problem Statement

The current presentation-builder uses a two-stage pipeline: an LLM agent generates creative HTML, then a deterministic Python post-processor (`fix-navigation.py`, 435 lines) injects navigation JS, slide engine CSS, speaker notes CSS, and print support. This architecture has failed:

- 5 of the last 7 commits are fixes for cascading breakage between model output and post-processor assumptions.
- The model writes `display:none`/`display:flex` visibility CSS that fights the injected `opacity`/`visibility` engine — all slides go blank.
- The model nests slides inside extra wrapper divs — breaks CSS child combinators — blank pages.
- The post-processor's regexes disagree with each other — running it twice corrupts class names (`slide-wrapper-wrapper-wrapper`).
- The post-processor grew from a simple nav injector into a 435-line HTML repair tool through 4+ rounds of "model violated the contract, add a fix."

The root cause is split authorship. The CSS comes from the model but the JS comes from the post-processor, and they fight each other. Evidence from the `amplifier-stories` repository (9 self-contained presentations, zero post-processing, all working correctly) proves that models produce better decks when they own the full output.


## Design Decision

**Single-pass, model owns everything, no post-processing.**

The agent receives any kind of input and produces a complete, self-contained HTML file. The HTML is the final artifact — it opens in a browser directly from disk. No post-processor, no formatter agent, no HTML extraction step.


## Architecture

```
Any input (specialist output, raw notes, brief description, anything)
  → presentation-builder agent
  → self-contained HTML file (final artifact)
```

### What Gets Removed

- `tests/presentation-builder/fix-navigation.py` — deleted entirely
- HTML extraction Python snippet in `generate-decks.yaml` step 3
- All references to post-processing in `context/specialists-instructions.md`
- The "no `<script>` tag" instruction in the agent prompt
- The structural HTML contract (slides-container wrapper, specific class names)

### What Stays

- The eval harness (scenarios, rubric, screenshot pipeline, judge) — unchanged
- The `generate-decks` recipe — simplified to 2 steps (read, generate+save)
- All proven prompting techniques (ghost deck, visual rhythm, density discipline, content integrity, audience calibration, speaker notes)

### What Changes

- `agents/presentation-builder.md` — full rewrite
- `tests/presentation-builder/generate-decks.yaml` — simplified recipe
- `context/specialists-instructions.md` — remove post-processor references


## Outcome-Based Contract

Instead of prescribing HTML structure, we define what the output must achieve:

1. **Self-contained single HTML file** — works from disk, no external dependencies (no Google Fonts, no CDN links).
2. **Keyboard navigable** (arrow keys, Home/End) and **touch navigable** (swipe with 50px threshold).
3. **Accessible** — `prefers-reduced-motion` media query, keyboard-navigable elements.
4. **First slide visible on load.**
5. **Output starts with `<`, ends with `>`** — raw HTML, no markdown fences or prose.

How the model achieves these outcomes is entirely its choice — transition styles, navigation patterns, CSS approach, JS implementation.


## Prompt Philosophy: Teach Judgment, Not Rules

The prompt has two halves that work together.

### Narrative Craft (existing strength, enhanced)

**Ghost Deck / Newspaper Test.** Write all titles first. Read just the titles. If someone reading only the titles gets the full argument, proceed. If any title could be a table-of-contents entry, it's a label — rewrite it as a claim. Strengthened with 8 before/after transformation examples covering hard cases (methodology slides, process slides, team structure slides).

**Assertion title examples** — expanded table of transformations:

| Label Title | Assertion Title |
|---|---|
| Market Overview | The mid-market segment is underserved and growing 23% YoY |
| Implementation Timeline | We can ship Phase 1 in 6 weeks with the existing team |
| Risk Assessment | Three risks could delay launch; all have mitigations |
| Methodology | Zero Trust works because it eliminates implicit trust at every layer |
| Team Structure | Cross-functional pods ship 40% faster than siloed teams |
| Q3 Results | Q3 exceeded targets on 4 of 5 OKRs despite the August outage |
| Competitive Landscape | Three competitors are converging on our core market — and two are already undercutting on price |
| Next Steps | Two decisions this week determine whether we ship in Q2 or slip to Q3 |

**Audience calibration** — kept (executives 6-10 slides, teams 10-15, external 8-12, teaching 12-20).

**Content integrity** — kept (never invent numbers, preserve qualifiers, impact claims need baselines).

**Emotional arc** — new. Design 2-3 "peak moment" slides per deck first, build everything else around them. Four archetypes:

- **The gap slide** — problem felt viscerally
- **The reveal slide** — solution clicks
- **The proof slide** — skeptics nod
- **The close slide** — thesis restated as call to action, not "Questions?"

Ask: which 2 slides will the audience remember tomorrow?

**Speaker notes** — 4-field structure kept (`key_point`, `if_challenged`, `transition`, `confidence`) with 2-3 complete exemplars showing specific, prepared responses rather than generic deflections (to be written during prompt implementation — not included in this plan).

### Visual Craft (new layer)

These are heuristics to calibrate judgment, not rules to enforce.

**Visual hierarchy.** Every slide has one visual anchor: the element that proves the title's assertion. Make it 3x larger, bolder, or more colorful than anything else. On a data slide the anchor is the hero number. On an argument slide it's the key evidence. On a section break it's the statement itself.

**Composition.** Asymmetric layouts (60/40) are more interesting than symmetric (50/50). The eye follows Z-pattern on text slides, F-pattern on data slides. Put the most important element at the start of the eye path.

**Visual rhythm.** Heavy/medium/light taxonomy kept. Dense slides earn their density by having a clear visual anchor that organizes the information. Spacious slides earn their space by making one element impossible to miss. The audience should feel the shift between the two. Light slides are peak moments, not pauses — hero stats, full-bleed statements, dramatic contrasts. These are the slides the audience will screenshot.

**Animation as storytelling.** CSS animations and inline SVG reinforce the point, not decorate. A scanning line on a code review slide explains what code review does. Flowing dots on a pipeline slide show how data moves. Pulsing elements on a monitoring slide convey liveness. Implementation guidance:

- Use `@keyframes` for continuous effects (scanning, pulsing, flowing)
- Use CSS transitions with stagger delays for entrance effects
- Trigger animations on `.active` so they play when the slide appears, not on page load

**Palette derived from content.** No named themes (`clean-light`, `dark-keynote`, `warm-minimal`). Instead: Is this content optimistic or cautionary? Forward-looking or retrospective? Urgent or reflective? The emotional register determines the palette. No two decks about different topics should look the same.

**Data visualization selection.** Choose the right chart for the story:

- Change over time: horizontal bar with animated fill
- Part of whole: donut
- Comparison: grouped bars
- One impressive number: hero stat

Every chart gets a one-line annotation telling the audience what to conclude.


## Example Slides

Four selected example slides are included as literal HTML in the prompt. These demonstrate principles in action — they are not templates to copy. Each shows a different archetype and a different visual approach.

| # | File | Archetype | Key Principles Demonstrated |
|---|------|-----------|-----------------------------|
| 01 | `01-hero-stat.html` | Data / hero stat | Visual anchor (giant animated number), stagger entrance, breathing room, warm teal/amber palette |
| 03 | `03-animated-process.html` | Narrative with animation | Animation as content (scanning line over code), asymmetric 60/40 layout, phased reveal, dark code-editor aesthetic |
| 07 | `07-before-after.html` | Contrast / transformation | Before/after split, muted vs. vibrant, static gradient divider as metaphor, directional storytelling |
| 08 | `08-architecture-svg.html` | System diagram with SVG | Inline SVG with animated data flow, phased entrance sequence (nodes, connections, flow), pub/sub topology made visual |

Example slides are located at `tests/presentation-builder/candidate-examples/`.


## Input Flexibility

The presentation builder works with any input. No structured specialist format is required.

- **Structured specialist output** (researcher, analyst, competitive analysis, writer) — claims are pre-identified, use them directly.
- **Raw notes, meeting transcripts, brainstorms** — identify the 3-5 key claims yourself, then apply Ghost Deck.
- **A brief description or topic** — build the narrative from your knowledge.
- **A mix of the above.**

The presentation builder is the last mile and handles whatever shows up at its door. This matters especially for the standalone version outside the specialist pipeline.


## Pre-Flight Self-Check

Before returning output, verify:

1. Every title is an assertion, not a label (if any title could be a TOC entry, rewrite it).
2. Every slide has one clear visual anchor.
3. Visual rhythm: no two consecutive heavy slides, light slides are visually striking not bare.
4. All animations reinforce the slide's point (no decorative motion).
5. Self-contained: no external dependencies, no `@import`, no CDN links.
6. Accessibility: `prefers-reduced-motion` present, keyboard navigation works.
7. Content integrity: no fabricated numbers, qualifiers preserved.


## Recipe Changes

`tests/presentation-builder/generate-decks.yaml` simplifies from 3 steps to 2:

1. **read-scenario** — reads input material (unchanged).
2. **generate-presentation** — agent produces complete HTML, saved directly to file. If the model wraps output in markdown fences or prose, a trivial strip (remove everything before first `<` and after last `>`) is applied — but this is string trimming, not HTML surgery.


## Specialist Instructions Changes

`context/specialists-instructions.md` updates:

- Remove all references to `fix-navigation.py` and post-processing.
- Update presentation-builder description: "Transforms source material into self-contained HTML slide decks. The output is a complete, working presentation — no post-processing required."
- Chain variants stay (deck only, analytical deck, competitive deck) — these describe input routing, not post-processing.


## Future Option: Content-Only Review Pass

Not included in initial implementation. If eval data shows specific weaknesses that a review pass would catch, we add a scoped second pass where the model can revise slide titles, reorder slides, tighten copy, and fix narrative flow — but the HTML structure, CSS, and JS are locked. The second pass works within the existing scaffolding, not on top of it.

Decision to add this will be driven by eval scores after the redesign ships.


## Eval Rubric

The eval rubric is being refined separately. The current 10-dimension rubric and 6 test scenarios remain as infrastructure. The rubric refinement is independent of this design and will proceed in parallel.
