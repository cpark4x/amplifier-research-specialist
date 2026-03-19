# Presentation Builder Redesign — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rewrite the presentation-builder agent so the model owns the entire HTML output (CSS, JS, navigation) with no post-processor, guided by outcome-based contracts, narrative/visual craft heuristics, and literal example slides.

**Architecture:** The agent prompt (`agents/presentation-builder.md`) is fully rewritten to teach the model judgment through examples and heuristics rather than prescriptive structural rules. The `generate-decks` recipe is simplified to remove HTML extraction and post-processor invocation. The post-processor (`fix-navigation.py`) is deleted entirely. The eval harness (scenarios, rubric, screenshot pipeline, judge) is unchanged.

**Tech Stack:** Markdown (agent prompt), YAML (recipe configuration), HTML/CSS/JS (example slides embedded in prompt as literal code), Bash (recipe steps)

---

## Task 1: Rewrite the Agent Prompt

This is the core of the redesign. The entire `agents/presentation-builder.md` file is rewritten from scratch. The current file is 339 lines; the new file will be significantly longer due to embedded example slides.

**Files:**
- Rewrite: `agents/presentation-builder.md`
- Reference (read-only): `docs/plans/2026-03-19-presentation-builder-redesign.md` (the design doc that specifies everything)
- Reference (read-only): `tests/presentation-builder/candidate-examples/01-hero-stat.html`
- Reference (read-only): `tests/presentation-builder/candidate-examples/03-animated-process.html`
- Reference (read-only): `tests/presentation-builder/candidate-examples/07-before-after.html`
- Reference (read-only): `tests/presentation-builder/candidate-examples/08-architecture-svg.html`

### Step 1: Read all reference files

Read the design doc (`docs/plans/2026-03-19-presentation-builder-redesign.md`) and all four example slide files. Read the current prompt to understand what to preserve vs. replace. The design philosophy is: **teach judgment, not rules.** The model should understand *why* good slides work, not follow a structural contract.

### Step 2: Write the new prompt

Replace the entire contents of `agents/presentation-builder.md`. The new file must have the exact structure laid out below. Each section includes precise content specifications, sources ("from design doc", "preserve from current prompt", "write new"), and quality bar descriptions.

---

#### Section 1: YAML Frontmatter

Keep the `---` delimited YAML frontmatter block. The frontmatter contains `meta.name`, `meta.description`, and an `<example>` block used by the orchestrator for routing.

**Changes from current frontmatter:**

1. Update `meta.description` to remove any implication of post-processing. New description should say the agent "transforms any input into self-contained HTML slide decks" and that "the output opens directly in a browser — no post-processing, no external dependencies." Keep the "Authoritative on" and "MUST be used for" subsections, updating as needed.

2. Update the `<commentary>` inside the `<example>` block. Current text says "returns a self-contained HTML deck" which is fine, but verify it doesn't mention post-processing.

3. Remove any reference to "structured source material" as the only input type — the new prompt accepts **any** input.

---

#### Section 2: Identity and Role

**Heading:** `# Presentation Builder`

Preserve the energy of the current opening ("world-class presentation designer", "presentations people remember", "the kind where the audience puts their phone down"). This voice is good — keep it.

**Add these new concepts** (weave into the opening, don't list mechanically):

- The model owns the **entire** output: HTML, CSS, JavaScript, navigation — everything.
- The output is the **final artifact**. It opens in a browser directly from disk. No post-processor, no formatter agent, no HTML extraction step.
- CSS/HTML-only visual design (no images) is a **strength**, not a limitation. Mention: metric cards, bar charts, donut charts, gradient typography, glassmorphism cards, inline SVG diagrams, CSS animations.

**Remove from current version:**
- Any mention of a post-processor handling navigation, speaker notes CSS, or print support.
- The line "You do not source images" can stay but the framing should emphasize capability not limitation.

---

#### Section 3: Outcome-Based Contract

**Heading:** `## Outcome-Based Contract`

This replaces the old "HTML Structure Contract" section. Instead of prescribing specific HTML elements, class names, and structural rules, define **what the output must achieve**.

Write a brief intro: "Instead of prescribing HTML structure, here is what your output must achieve. How you get there is your choice."

**Five requirements** (from design doc, section "Outcome-Based Contract"):

1. **Self-contained single HTML file** — works when opened from disk (`file://`), no external dependencies. No Google Fonts, no CDN links, no `@import url(...)`. System font stack only.
2. **Keyboard navigable** (Left/Right arrow keys at minimum; Home/End for first/last slide recommended) and **touch navigable** (swipe gesture with ~50px threshold).
3. **Accessible** — `@media (prefers-reduced-motion: reduce)` query that disables animations, semantic HTML where appropriate, keyboard-focusable interactive elements.
4. **First slide visible on load** — no blank screen, no loading state, the first slide renders immediately.
5. **Raw HTML output** — response starts with `<` (e.g., `<!DOCTYPE html>`), ends with `>` (e.g., `</html>`). No markdown fences, no prose preamble, no "Here is your presentation" text. This is critical because the output is saved directly as an `.html` file.

Close with: "How you achieve these outcomes is entirely your choice — class names, transition styles, navigation patterns, CSS approach, JS implementation. There is no structural contract to follow."

---

#### Section 4: Narrative Craft

**Heading:** `## Narrative Craft`

This section contains the storytelling methodology. It has six subsections.

##### 4a: Ghost Deck / Newspaper Test

**Heading:** `### Ghost Deck: Titles First, Always`

Preserve the current prompt's content almost verbatim — it's already excellent. Key points that must be present:

- Before writing any slide body content, write every slide title in sequence.
- Read just the titles. This is the **Newspaper Test** — if someone reading only the titles gets the full argument, you have a coherent deck.
- If any title could be a table-of-contents entry, it's a label — rewrite it as a claim.
- Slide titles must be **assertions, not labels**.
- "This is the single technique that separates a memorable deck from a forgettable one. Do not skip it."

##### 4b: Assertion Title Examples

**Heading:** `### Assertion Title Examples`

Include the full 8-row transformation table from the design doc (section "Assertion title examples"). Format as a markdown table:

```
| Label Title (never use) | Assertion Title (always use) |
|---|---|
| Market Overview | The mid-market segment is underserved and growing 23% YoY |
| Implementation Timeline | We can ship Phase 1 in 6 weeks with the existing team |
| Risk Assessment | Three risks could delay launch; all have mitigations |
| Methodology | Zero Trust works because it eliminates implicit trust at every layer |
| Team Structure | Cross-functional pods ship 40% faster than siloed teams |
| Q3 Results | Q3 exceeded targets on 4 of 5 OKRs despite the August outage |
| Competitive Landscape | Three competitors are converging on our core market — and two are already undercutting on price |
| Next Steps | Two decisions this week determine whether we ship in Q2 or slip to Q3 |
```

Add a note: these cover the hard cases — methodology slides, process slides, team structure slides — where the temptation to use a label is strongest.

##### 4c: Audience Calibration

**Heading:** `### Audience Calibration`

Preserve from current prompt (lines 63-73). Four audience types with slide count ranges:

- **Executives** — lead with the conclusion, keep it tight (6-10 slides), frame around decisions and impact
- **Teams** — include the journey and methodology, more detail welcome (10-15 slides)
- **External/clients** — their world first, your capabilities second, prove with evidence (8-12 slides)
- **Teaching/training** — progressive disclosure, build concepts step by step (12-20 slides)

##### 4d: Storytelling Frameworks

**Heading:** `### Storytelling Frameworks`

Preserve from current prompt (lines 77-91). These are the narrative arc patterns the model selects from. Keep all five:

- **Answer-first** (executives): recommendation upfront, then proof. Every slide stands alone because executives will interrupt.
- **Tension-resolution** (persuasion): problem → urgency → solution → proof.
- **Progressive discovery** (teaching): question → findings → implications.
- **Status report** (updates): objectives → progress with metrics → blockers → plan. Don't force a narrative onto a routine update.
- **Retrospective** (reflection): what happened → what worked → what didn't → what changes. Every action item has an owner.

##### 4e: Content Integrity

**Heading:** `### Content Integrity`

Preserve from current prompt (lines 107-124). This section is non-negotiable and mechanical — keep the firm tone. Key rules:

- **Never invent numbers.** If a number does not appear in the source material, it does not appear in the deck. When illustrating with a worked example, use source numbers or write `[X]`.
- **Preserve every qualifier.** "~23,400" stays "~23,400." "$1.84M estimated" stays "$1.84M estimated." Dropping a qualifier is fabrication.
- **Feature lists must come from source material.** Do not add features, capabilities, or pricing tiers not in the input.
- **Impact claims need baselines** — "30% faster" must say "than what?"
- **Recommendations must include trade-offs** — no free lunches.

##### 4f: Emotional Arc (NEW)

**Heading:** `### Emotional Arc`

This is new content from the design doc (section "Emotional arc"). Write this section from these specifications:

- Design 2-3 **"peak moment" slides** per deck first, then build everything else around them.
- Four archetypes for peak moments:
  - **The gap slide** — the problem felt viscerally. The audience should feel the cost of inaction.
  - **The reveal slide** — the solution clicks. The "aha" moment.
  - **The proof slide** — skeptics nod. Evidence that overcomes the audience's default objection.
  - **The close slide** — the thesis restated as a call to action, not "Questions?" Not "Thank You." A specific ask.
- The design question: "Which 2 slides will the audience remember tomorrow?" If you can't answer that, restructure.

##### 4g: Speaker Notes

**Heading:** `### Speaker Notes`

This subsection defines the speaker notes format and includes exemplars.

**Format** (preserve from current prompt, lines 261-272): Include speaker notes on content slides. Structure each note with four named fields:

- **key_point** — the 2-3 sentences of depth the presenter carries verbally. The core message the slide must land.
- **if_challenged** — "If [likely objection]: [your response]" — at least one per content slide with a specific rebuttal, not a generic deflection. This is what separates a prepared presenter from a nervous one.
- **transition** — one sentence connecting to the next slide's assertion. Reference the next slide's content specifically, not generically.
- **confidence** — source tier and corroboration level when relevant ("single secondary source — worth verifying", "three primary sources corroborate").

**HTML format:** Speaker notes go inside each slide as `<div class="speaker-notes">`. The model is responsible for styling them (hidden by default, toggled with the S key via the navigation JavaScript the model writes).

**Exemplars** (NEW — write from scratch): Include 2-3 complete exemplars demonstrating the four-field structure with specific, prepared responses. These must feel like real presenter preparation, not templates.

Write one exemplar for each of these slide types:

1. **A data/metrics slide** (e.g., a hero stat showing cost reduction). The `if_challenged` should name a specific likely objection ("Is this blended across all channels?") and give a concrete rebuttal with supporting data.

2. **An argument/claim slide** (e.g., a slide claiming a particular architecture is better). The `if_challenged` should anticipate the technical skeptic ("What about ordering guarantees?") and reference specific evidence (an ADR, a test result).

3. **A recommendation/next-steps slide** (e.g., a slide asking for two decisions this week). The `if_challenged` should address timeline pushback ("Can this wait until next quarter?") with concrete consequences of delay.

**Quality bar for exemplars** — here is what "good" looks like (from example slide `01-hero-stat.html`'s speaker notes):

```
key_point: The 47% reduction is a direct result of removing manual SDR
qualification — automated scoring handles top-of-funnel, humans engage only
at SQL threshold. This is not optimization; it's a structural change.

if_challenged: "This is blended CAC — what about channel breakdown?"
Outbound-only improvement is 61%; inbound is 33%. Both significant and
directionally consistent.

transition: These gains compound — faster cycles mean more cycles per
quarter. Let's look at what that means for total pipeline capacity heading
into Q3.

confidence: High — 6-month cohort with full attribution through CRM.
Finance reviewed and approved the $1.2M annualized figure using
fully-loaded cost basis.
```

Note: the exemplars in the prompt should use **different content** from the example slides — do not copy the example slides' speaker notes as the exemplars. Write original content for different hypothetical topics to show range.

---

#### Section 5: Visual Craft

**Heading:** `## Visual Craft`

This is the **new visual layer** from the design doc (section "Visual Craft"). The intro should say: "These are heuristics to calibrate your judgment, not rules to enforce mechanically."

##### 5a: Visual Hierarchy

**Heading:** `### Visual Hierarchy`

From design doc:
- Every slide has **one visual anchor**: the element that proves the title's assertion.
- Make it 3x larger, bolder, or more colorful than anything else on the slide.
- On a **data slide**, the anchor is the hero number. On an **argument slide**, it's the key evidence. On a **section break**, it's the statement itself.

##### 5b: Composition

**Heading:** `### Composition`

From design doc:
- Asymmetric layouts (60/40) are more interesting than symmetric (50/50).
- The eye follows **Z-pattern** on text slides, **F-pattern** on data slides.
- Put the most important element at the start of the eye path.

##### 5c: Visual Rhythm

**Heading:** `### Visual Rhythm`

From design doc + current prompt (merge both):
- Tag each slide as **heavy** (data grids, comparisons, dense evidence), **medium** (assertion + supporting points), or **light** (section divider, big quote, single stat, full-bleed statement).
- Enforce: **no two consecutive heavy slides**. At least one light slide per three.
- Dense slides earn their density by having a clear visual anchor that organizes the information.
- Spacious slides earn their space by making one element impossible to miss.
- Light slides are **peak moments**, not pauses — hero stats, full-bleed statements, dramatic contrasts. "These are the slides the audience will screenshot."
- **Density limit** (from current prompt): No single slide should contain more than 5 distinct content items (metric cards, list items, timeline steps, comparison cards). If the source material requires more, split across two slides. Two clean slides always beat one dense slide.

##### 5d: Animation as Storytelling

**Heading:** `### Animation as Storytelling`

From design doc + current prompt (merge both):

Concept: CSS animations and inline SVG reinforce the point, not decorate. Static slides are forgettable; purposeful animation makes a slide feel alive.

Examples of animation as content (from design doc):
- A **scanning line** sweeping over a code block says "we're analyzing this."
- A **bar chart that draws itself** says "watch the gap."
- A **metric that counts up** says "this number matters."
- **Flowing dots** on a pipeline slide show how data moves.
- **Pulsing elements** on a monitoring slide convey liveness.

Implementation guidance (from design doc):
- Use `@keyframes` for continuous effects (scanning, pulsing, flowing)
- Use CSS transitions with stagger delays for entrance effects
- Trigger animations on `.active` class so they play when the slide appears, not on page load

Constraints (from current prompt):
- **Max 1 animated element per slide.** Two competing animations both lose.
- **2-4 animated slides per deck.** Concentrate on the slides that carry the most weight.
- **Slow and subtle.** 3-8 second durations, ease-in-out. Fast animations feel cheap.

##### 5e: Palette Derived from Content

**Heading:** `### Palette`

From design doc — this **replaces** the named theme system (`clean-light`, `dark-keynote`, `warm-minimal`) from the current prompt. Do NOT include named themes.

New approach:
- No named themes. Instead, derive the palette from the content's emotional register.
- Ask: Is this content **optimistic or cautionary**? **Forward-looking or retrospective**? **Urgent or reflective**?
- No two decks about different topics should look the same.

Preserve the practical guidance from the current prompt about default tone:
- Default to **light backgrounds** unless the content strongly calls for dark (technical deep-dives, developer audiences, dramatic reveals). Light decks project better and read better in most environments.

Remove the named theme bullet list from the current prompt (Corporate → blue, Technical → dark, etc.). Replace with: the palette should feel **inevitable** for the subject matter. The audience shouldn't notice the design — it should feel like the only possible way this content could look.

##### 5f: Data Visualization Selection

**Heading:** `### Data Visualization`

From design doc:
- **Change over time**: horizontal bar with animated fill
- **Part of whole**: donut chart
- **Comparison**: grouped bars
- **One impressive number**: hero stat (giant number with annotation)
- Every chart gets a **one-line annotation** telling the audience what to conclude. A chart without an annotation is a chart the audience will misread.

---

#### Section 6: Input Flexibility

**Heading:** `## Input Flexibility`

From design doc (section "Input Flexibility"). This is new — the current prompt assumes structured specialist output. The new prompt must handle anything:

- **Structured specialist output** (researcher, analyst, competitive analysis, writer) — claims are pre-identified, use them directly.
- **Raw notes, meeting transcripts, brainstorms** — identify the 3-5 key claims yourself, then apply Ghost Deck.
- **A brief description or topic** — build the narrative from your knowledge.
- **A mix of the above.**

Close with: "You are the last mile and handle whatever shows up at your door."

---

#### Section 7: Example Slides

**Heading:** `## Example Slides`

This section contains 4 literal HTML examples embedded in the prompt. These demonstrate principles in action — they are not templates to copy.

**Intro text:** Write 2-3 sentences explaining that these examples show different archetypes and visual approaches. Each demonstrates specific principles from the sections above. The model should study *why* each works, then apply those principles to create something original for every new deck.

**For each example, include:**

1. A subheading: `### Example N: [Archetype Name]`
2. A "Demonstrates:" line listing the key principles shown (use the table from design doc section "Example Slides")
3. The trimmed HTML in a fenced `html` code block

**How to trim each example file:**

Each file in `tests/presentation-builder/candidate-examples/` is a complete HTML document. For the prompt, trim as follows:

1. **Remove** these boilerplate lines from the top of each file:
   - `<!DOCTYPE html>`
   - `<html lang="en">`
   - `<head>`
   - `<meta charset="UTF-8">` (or `<meta charset="UTF-8" />`)
   - `<meta name="viewport" content="width=device-width, initial-scale=1.0">` (or with `/>`)
   - `<title>...</title>`
2. **Remove** the `</head>` line
3. **Remove** the `<body>` opening tag (keep all content that was inside body)
4. **Remove** the `</body>` and `</html>` closing tags
5. **Keep everything else**: the `<style>` block (with its opening and closing tags), all slide content divs, speaker notes divs, and any `<script>` blocks.

The result for each example starts with `<style>` and ends with the last content element's closing tag.

**The four examples:**

**Example 1: Hero Stat (Data Slide)**
- Source file: `tests/presentation-builder/candidate-examples/01-hero-stat.html`
- Demonstrates: Visual anchor (giant animated number), stagger entrance with delays, breathing room, warm teal/amber palette, `prefers-reduced-motion` respect
- This is a single-slide example showing a "light" slide type — a hero stat with supporting metric cards. Note the animation stagger: eyebrow (0.05s) → kicker (0.2s) → hero number (0.25s) → annotation (0.85s) → cards (1.05s, 1.25s, 1.45s). Each element enters after the audience has absorbed the previous one.

**Example 2: Animated Process (Narrative with Animation)**
- Source file: `tests/presentation-builder/candidate-examples/03-animated-process.html`
- Demonstrates: Animation as content (scanning line sweeps over code, vulnerability cards appear as scan finds them), asymmetric 60/40 layout (code panel 60%, results panel 40%), phased reveal with JavaScript orchestration, dark code-editor aesthetic
- **This example includes a `<script>` tag.** This is correct — the model now owns JavaScript. Note how the script orchestrates a multi-phase animation cycle: scan line travels → vulnerability cards appear staggered → secure badge reveals → cycle resets. Also note the `prefers-reduced-motion` check that shows the end-state statically instead of animating.

**Example 3: Before/After (Contrast / Transformation Slide)**
- Source file: `tests/presentation-builder/candidate-examples/07-before-after.html`
- Demonstrates: Before/after split with contrasting palettes (muted blue-gray vs. warm green-amber), static gradient divider as metaphor (color transitions from "before" to "after" top-to-bottom), directional storytelling with staggered entrance on the "after" side only, transformation arrow overlay
- Note: the "before" metrics are static and slightly desaturated (opacity: 0.82), while the "after" metrics animate in — this visual asymmetry reinforces the narrative of transformation.

**Example 4: Architecture Diagram (System Diagram with SVG)**
- Source file: `tests/presentation-builder/candidate-examples/08-architecture-svg.html`
- Demonstrates: Inline SVG with animated data flow, three-phase entrance sequence (nodes scale in 0.1-1.1s → connection lines draw in 1.5-2.0s → data flow dashes animate 2.4s+), pub/sub topology made visual (teal = publish, blue = subscribe), hub ripple pulse effect, annotation bar that fades in last
- This is the most complex example. The phased entrance builds understanding: first you see the services, then the connections, then the live data flowing through them. The animation serves the explanation.

**Closing note after all examples:** "These examples demonstrate principles in action — they are not templates to copy. Every deck you create should look different from these examples and from every other deck you've created. Apply the same principles to create something original for the content at hand."

---

#### Section 8: Pre-Flight Self-Check

**Heading:** `## Pre-Flight Self-Check`

From design doc (section "Pre-Flight Self-Check"). Open with the firm tone from the current prompt: "STOP. Before returning your HTML, verify every item below."

**Seven items:**

1. **Every title is an assertion, not a label.** Read every slide title. If any could be a table-of-contents entry, rewrite it as a claim.
2. **Every slide has one clear visual anchor.** The element that proves the title's assertion should be 3x more prominent than anything else.
3. **Visual rhythm.** Check your heavy/medium/light sequence. No two consecutive heavy slides. Light slides are visually striking, not bare.
4. **All animations reinforce the slide's point.** No decorative motion. If you can't explain what the animation communicates, remove it.
5. **Self-contained.** No `@import`, no Google Fonts, no CDN links, no external dependencies of any kind.
6. **Accessibility.** `@media (prefers-reduced-motion: reduce)` is present and disables all animations. Keyboard navigation works.
7. **Content integrity.** No fabricated numbers. Every qualifier from the source material is preserved.

---

#### Section 9: Metadata

**Heading:** `## Metadata`

Preserve from current prompt (lines 274-294). Embed at the end of `<body>` as HTML comments:

```html
<!-- PRESENTATION METADATA
Specialist: presentation-builder
Input type: [type]
Audience: [audience]
Purpose: [purpose]
Framework: [framework chosen]
Slide count: [n]
-->

<!-- CONTENT MAP
C1: "[claim]" | used in: slide [n]
C2: "[claim]" | used in: slide [n]
...
UNUSED: C7 — [reason]
-->
```

---

#### Section 10: Routing Signal

**Heading:** `## Routing Signal (for orchestrator use only)`

Preserve from current prompt (lines 298-304). No changes needed — this is orchestrator-facing metadata.

---

#### Section 11: What You Do Not Do

**Heading:** `## What You Do Not Do`

Update from current prompt (lines 309-318):

**Keep these items:**
- Source or embed images — CSS/SVG-only visual design
- Research new facts — that's the Researcher's job
- Draw new inferences — that's the Data Analyzer's job
- Write prose documents — that's the Writer's job
- Fabricate claims not in the source material
- Import external fonts, CSS, or JavaScript
- Wrap your output in markdown — return raw HTML only

**Remove this item** (model now owns JS):
- ~~"Produce navigation JavaScript — the post-processor handles slide navigation"~~

**Add this item:**
- Copy example slides verbatim — they demonstrate principles, not templates

---

### Step 3: Verify the prompt

Open the completed `agents/presentation-builder.md` and verify every item on this checklist:

- [ ] YAML frontmatter is present and syntactically valid (open/close `---` delimiters)
- [ ] **Zero** references to "post-processor", "post-processing", "fix-navigation", or "fix_navigation" anywhere in the file
- [ ] **Zero** references to named themes: `clean-light`, `dark-keynote`, `warm-minimal`
- [ ] **Zero** instructions saying "No `<script>` tag" or "Do not write JavaScript" — the model owns JS now
- [ ] **Zero** instructions saying "No slide visibility CSS" or "No `display: none`" — the model owns all CSS now
- [ ] **Zero** references to `slides-container` as a **required** class name (it may appear in examples, but must not be mandated)
- [ ] All 4 example slides are present, properly trimmed (start with `<style>`, no DOCTYPE/html/head/meta/title boilerplate)
- [ ] Example 03 (animated process) retains its `<script>` block — do not strip it
- [ ] All 8 assertion title transformation examples are present in the table
- [ ] All 4 emotional arc archetypes are present (gap, reveal, proof, close)
- [ ] 2-3 speaker notes exemplars are present, each with all 4 fields (key_point, if_challenged, transition, confidence)
- [ ] Speaker notes exemplars use **original content** — not copied from the example slides
- [ ] 7 pre-flight self-check items are present
- [ ] 5 outcome-based contract requirements are present
- [ ] `prefers-reduced-motion` is mentioned (in outcome contract and/or pre-flight check)
- [ ] Keyboard navigation (arrow keys) and touch navigation (swipe) are mentioned in the outcome contract
- [ ] The file starts with `---` (YAML frontmatter) and the identity section uses `# Presentation Builder` as the top heading

### Step 4: Commit

```bash
git add agents/presentation-builder.md
git commit -m "feat: rewrite presentation-builder prompt — model owns everything

Outcome-based contract replaces structural HTML contract.
Narrative craft enhanced with emotional arc, 8 assertion title examples.
Visual craft layer added (hierarchy, composition, rhythm, animation, palette).
4 literal example slides embedded (hero-stat, animated-process, before-after, architecture-svg).
Speaker notes exemplars written from scratch.
Post-processor references removed — model owns HTML, CSS, JS, and navigation."
```

---

## Task 2: Simplify the Generate-Decks Recipe

**Files:**
- Modify: `tests/presentation-builder/generate-decks.yaml`

### Step 1: Read the current recipe

Read `tests/presentation-builder/generate-decks.yaml`. The current recipe has 3 steps:
1. `read-scenario` — reads scenario file (bash)
2. `generate-presentation` — delegates to presentation-builder agent
3. `save-output` — extracts HTML from agent output using Python regex, then runs `fix-navigation.py` post-processor

After this task, step 1 is unchanged, step 2 has a simplified prompt, and step 3 replaces the complex HTML extraction + post-processor call with a trivial string trim + save.

### Step 2: Update step 2 prompt (generate-presentation)

In the `generate-presentation` step, replace the `prompt` field. Changes:

1. **Remove instruction #5** entirely: `"Do NOT include a \`<script>\` tag — slide navigation is injected by a post-processor after generation."` — this is the key architectural change. The model now writes its own navigation JS.

2. **Keep instructions #1-4** with minor updates:
   - Instruction #4 stays (raw HTML output, first char `<`, last char `>`)
   - Remove any reference to post-processing from instruction text

The updated prompt should be:

```yaml
    prompt: |
      Generate a presentation from the following test scenario.

      The scenario file below contains:
      - A **Parameters** section listing audience, audience_type, purpose, tone,
        output_format, theme, presentation_mode, include_speaker_notes,
        include_appendix, and other configuration.
      - A **Source Material** section containing the structured input to build from.

      Instructions:
      1. Extract and follow ALL parameters exactly as specified.
      2. Build the complete presentation from the Source Material section.
      3. Do NOT fabricate any claims, statistics, or data points not present
         in the source material.
      4. Do NOT write to files — return the full content as your response.
         Return ONLY raw HTML. The first character of your response MUST be
         `<` (e.g., `<!DOCTYPE html>`) and the last MUST be `>` (e.g.,
         `</html>`). No prose, no explanation, no markdown fences, no
         "Here is the presentation" preamble. Raw HTML only.

      === SCENARIO FILE ===
      {{scenario_content}}
      === END SCENARIO FILE ===
```

Note: instruction #5 from the current version is simply gone — not replaced, not reworded, just removed.

### Step 3: Simplify step 3 (save-output)

Replace the entire `save-output` step command. The current version (lines 103-176) has:
- An inline Python script (~30 lines) that uses regex to find `<!DOCTYPE html>` or `<html>` and extract HTML between those markers
- A call to `tests/presentation-builder/fix-navigation.py`
- Raw file cleanup

Replace with a simplified version that does trivial string trimming only:

```yaml
  # —— Step 3: Save the generated deck to the output directory ————————————
  - id: "save-output"
    type: "bash"
    command: |
      set -euo pipefail
      mkdir -p "{{output_dir}}"

      # Derive output filename from scenario path
      scenario_basename=$(basename "{{scenario_path}}" .md)
      output_path="{{output_dir}}/${scenario_basename}-output.html"

      # Write raw agent output to temp file
      raw_path="${output_path}.raw"
      cat > "${raw_path}" <<'_CANVAS_DECK_EOF_7f3a9c'
      {{deck_output}}
      _CANVAS_DECK_EOF_7f3a9c

      # Trivial trim: strip any prose before the first < and after the last >.
      # The model should return clean HTML, but occasionally wraps output in
      # markdown fences or a prose preamble. This is string trimming, not HTML
      # surgery — no regex parsing, no structural assumptions.
      python3 -c "
      import sys
      with open('${raw_path}', 'r') as f:
          content = f.read()

      start = content.find('<')
      end = content.rfind('>') + 1
      if start < 0 or end <= start:
          print('ERROR: No HTML tags found in agent output', file=sys.stderr)
          sys.exit(1)

      html = content[start:end]
      if len(html) < 1000:
          print(f'ERROR: HTML too small ({len(html)} bytes)', file=sys.stderr)
          sys.exit(1)

      with open('${output_path}', 'w') as f:
          f.write(html)
      print(f'Saved {len(html)} bytes of HTML')
      "

      # Clean up raw file
      rm -f "${raw_path}"

      # Verify write succeeded
      if [ -s "${output_path}" ]; then
        byte_count=$(wc -c < "${output_path}")
        echo "Saved: ${output_path} (${byte_count} bytes)"
      else
        echo "ERROR: Write failed or produced empty output" >&2
        exit 1
      fi
    output: "save_result"
    timeout: 30
```

**What changed vs. the current step 3:**
- The inline Python is simpler: `content.find('<')` / `content.rfind('>')` instead of regex-based `<!DOCTYPE html>` / `<html>` searching
- The entire `fix-navigation.py` invocation block is removed (current lines 167-175)
- Comments updated to reflect the new architecture

### Step 4: Update the recipe header comment

Add a new changelog entry at the top of the changelog section (after the `# CHANGELOG` header, before the existing `v1.0.0` entry):

```yaml
# v2.0.0 (2026-03-19):
#   - Redesign: model owns full HTML output, no post-processor
#     * Step 2: Removed "no <script> tag" instruction — model owns navigation JS
#     * Step 3: Replaced HTML extraction regex + post-processor with trivial trim
#     * Removed fix-navigation.py dependency entirely
#
```

### Step 5: Verify the recipe

Open the modified file and check:

- [ ] No references to `fix-navigation.py` or `FIX_SCRIPT` anywhere
- [ ] No references to "post-processor" or "post-process" anywhere
- [ ] No "No `<script>` tag" instruction in the step 2 prompt
- [ ] Step 3 does NOT call any Python script other than the inline trivial trim
- [ ] YAML indentation is correct (use 2-space indent consistently)
- [ ] The heredoc delimiter `_CANVAS_DECK_EOF_7f3a9c` is preserved (it's unique enough to avoid collisions with deck content)

### Step 6: Commit

```bash
git add tests/presentation-builder/generate-decks.yaml
git commit -m "feat: simplify generate-decks recipe — remove post-processor

Step 2: removed 'no script tag' instruction (model owns navigation JS).
Step 3: replaced HTML extraction regex + post-processor with trivial trim.
Pipeline is now: read scenario -> generate complete HTML -> save to file."
```

---

## Task 3: Update Specialist Instructions

**Files:**
- Modify: `context/specialists-instructions.md`

### Step 1: Read the current file

Read `context/specialists-instructions.md`. Identify all references to the post-processor and named themes. The key locations are:

1. **Lines 146-159**: The `presentation-builder` description in the "Available Specialists" list — contains a full paragraph about the post-processor being "the mechanical equivalent of the formatter pattern."
2. **Lines 249-251**: Theme passing instruction — references named themes (`clean-light`, `dark-keynote`, `warm-minimal`).

### Step 2: Replace the presentation-builder description

Find this text block (lines 146-159):

```
- **presentation-builder** — Transforms structured source material into polished
  HTML slide decks. Accepts writer output, analysis output, research output,
  competitive analysis output, or raw notes and produces a self-contained HTML
  presentation with narrative arc, assertion-evidence slides, speaker notes, and
  keyboard navigation (arrow keys). Principles-based design grounded in cognitive
  science and visual hierarchy — audience calibration, ghost deck methodology, and
  visual rhythm. Produces decks that open directly in a browser.
  **Post-processor, not an LLM formatter** — after presentation-builder returns,
  `tests/presentation-builder/fix-navigation.py` always runs to inject slide
  navigation, slide engine CSS, speaker notes CSS, and print support
  deterministically. This is the mechanical equivalent of the formatter pattern:
  the model handles creative work, the script handles plumbing. No LLM formatter
  exists because navigation injection requires no judgment — a deterministic script
  is 100% reliable, costs zero tokens, and runs in milliseconds.
```

Replace with:

```
- **presentation-builder** — Transforms source material into self-contained HTML
  slide decks. The output is a complete, working presentation — no post-processing
  required. Accepts writer output, analysis output, research output, competitive
  analysis output, raw notes, or any other input and produces a single HTML file
  with narrative arc, assertion-evidence slides, CSS/SVG visual design, keyboard
  and touch navigation, speaker notes, and print support. Principles-based design
  grounded in visual hierarchy, narrative craft, and audience calibration. Opens
  directly in a browser from disk.
```

### Step 3: Update the theme passing instruction

Find this text (lines 249-251):

```
When delegating, pass `theme` (`clean-light`, `dark-keynote`, or `warm-minimal`) only when
the user explicitly requests one. Otherwise, omit it and let the presentation builder choose
based on content tone. The output is always a self-contained HTML file.
```

Replace with:

```
The output is always a self-contained HTML file. Do not pass theme names — the
presentation builder derives its visual palette from the content's emotional register.
```

### Step 4: Verify the file

Search the entire file for any remaining references:

- [ ] `grep -n "fix-navigation" context/specialists-instructions.md` returns zero matches
- [ ] `grep -n "post-processor" context/specialists-instructions.md` returns zero matches
- [ ] `grep -n "post-process" context/specialists-instructions.md` returns only the new "no post-processing required" phrase
- [ ] `grep -n "clean-light\|dark-keynote\|warm-minimal" context/specialists-instructions.md` returns zero matches
- [ ] The presentation chain variants (lines 288-294) are **unchanged** — deck only, deck + written document, analytical deck, competitive deck. These describe input routing, not post-processing.
- [ ] The "When to delegate to presentation-builder" section (lines 224-248) is **unchanged** except for the theme line.

### Step 5: Commit

```bash
git add context/specialists-instructions.md
git commit -m "docs: remove post-processor references from specialist instructions

Updated presentation-builder description: self-contained output, no post-processing.
Removed named theme instruction — palette derived from content."
```

---

## Task 4: Delete fix-navigation.py

**Files:**
- Delete: `tests/presentation-builder/fix-navigation.py`

### Step 1: Verify no remaining references

After completing Tasks 1-3, search the entire codebase for any remaining references to the post-processor:

```bash
grep -rn "fix-navigation\|fix_navigation" \
  --include="*.md" --include="*.yaml" --include="*.yml" \
  --include="*.py" --include="*.sh" --include="*.json" \
  .
```

This **must** return zero results. If any references remain, go back and fix them in the appropriate file before proceeding. Do not delete the file while references to it still exist.

### Step 2: Delete the file

```bash
git rm tests/presentation-builder/fix-navigation.py
```

### Step 3: Verify deletion

```bash
ls tests/presentation-builder/fix-navigation.py
# Should return: No such file or directory

git status
# Should show: deleted: tests/presentation-builder/fix-navigation.py
```

### Step 4: Commit

```bash
git commit -m "feat: delete fix-navigation.py post-processor (435 lines)

No longer needed — the presentation-builder model now owns the complete
HTML output including navigation JS, slide engine CSS, speaker notes CSS,
and print support."
```

---

## Task 5: End-to-End Verification

This task verifies the full pipeline works without the post-processor. No files are modified — this is a smoke test.

**Prerequisites:** Tasks 1-4 must be complete and committed.

### Step 1: Run the recipe against one scenario

Execute the simplified `generate-decks` recipe against scenario 01 (QBR Status Update):

```bash
amplifier tool invoke recipes operation=execute \
  recipe_path=tests/presentation-builder/generate-decks.yaml \
  context='{"scenario_path": "tests/presentation-builder/scenarios/01-qbr-status-update.md"}'
```

**Expected runtime:** 3-8 minutes. The recipe will:
1. Read the scenario file
2. Delegate to the presentation-builder agent (this is the slow step — LLM generation)
3. Save the output with trivial string trimming

**Expected outcome:** The recipe completes without errors and reports a saved file path.

### Step 2: Verify the output file exists

```bash
ls -la tests/presentation-builder/outputs/01-qbr-status-update-output.html
wc -c tests/presentation-builder/outputs/01-qbr-status-update-output.html
```

**Expected:** File exists with substantial content (> 10,000 bytes, typically 15-40KB for a full deck).

### Step 3: Verify the HTML is self-contained

Run these checks against the output file:

```bash
OUTPUT="tests/presentation-builder/outputs/01-qbr-status-update-output.html"

# 1. Starts with HTML
head -1 "$OUTPUT"
# Expected: <!DOCTYPE html> or <html

# 2. Contains <script> tag (model-generated navigation JS)
grep -c "<script" "$OUTPUT"
# Expected: >= 1

# 3. Contains keyboard navigation (arrow keys)
grep -ci "ArrowRight\|ArrowLeft\|keydown\|keyboard" "$OUTPUT"
# Expected: >= 1

# 4. Contains prefers-reduced-motion
grep -c "prefers-reduced-motion" "$OUTPUT"
# Expected: >= 1

# 5. No external dependencies
grep -c "@import" "$OUTPUT"
# Expected: 0

grep -ci "fonts.googleapis\|cdnjs\|unpkg\|jsdelivr" "$OUTPUT"
# Expected: 0

# 6. Contains speaker notes
grep -c "speaker-notes" "$OUTPUT"
# Expected: >= 1
```

**If any check fails:** This indicates the agent prompt needs refinement. Common issues:

| Check that failed | Likely cause | Fix |
|---|---|---|
| No `<script>` tag | The prompt doesn't clearly instruct the model to write navigation JS | Add explicit guidance in the outcome contract about writing keyboard/touch navigation JS |
| No arrow key handling | The model wrote JS but used a different navigation approach (e.g., scroll-based) | The outcome contract should be more explicit about arrow key requirement |
| No `prefers-reduced-motion` | The model forgot accessibility | The pre-flight check should catch this; verify it's present and prominent in the prompt |
| External `@import` found | The model used Google Fonts | The outcome contract and pre-flight check both forbid this; verify both are present |
| No speaker notes | The model omitted them | Verify the speaker notes section in the prompt is clear about including them on every content slide |

### Step 4: Open in browser and manually verify

```bash
open tests/presentation-builder/outputs/01-qbr-status-update-output.html
```

Manually check:

1. **First slide is visible** — no blank screen, no loading spinner, content renders immediately
2. **Arrow key navigation works** — Right arrow advances, Left arrow goes back
3. **Touch/click navigation works** — clicking right half advances, left half goes back (if the model implemented click navigation)
4. **Visual quality** — the deck looks polished, not broken. Slides have visual variety, not monotonous repetition.
5. **Speaker notes toggle** — pressing S shows/hides speaker notes (if the model implemented S-key toggle)
6. **No console errors** — open browser DevTools console, verify no JavaScript errors

### Step 5: Record results

No code changes to commit. If verification passes, the redesign is complete and ready for full eval harness runs across all 6 scenarios.

If verification fails, iterate on the agent prompt (Task 1) to address the specific failure. The recipe (Task 2), specialist instructions (Task 3), and file deletion (Task 4) should not need further changes.

---

## Summary

| Task | File(s) | Type | Key Change |
|---|---|---|---|
| 1 | `agents/presentation-builder.md` | Full rewrite | Model owns everything; outcome contract; narrative + visual craft; 4 example slides; speaker notes exemplars |
| 2 | `tests/presentation-builder/generate-decks.yaml` | Simplify | Remove HTML extraction + post-processor; trivial string trim only |
| 3 | `context/specialists-instructions.md` | Update | Remove post-processor paragraph; remove named themes |
| 4 | `tests/presentation-builder/fix-navigation.py` | Delete | 435-line post-processor no longer needed |
| 5 | (none) | Verify | Run recipe against one scenario; verify self-contained HTML output |

**Total files changed:** 3 modified, 1 deleted, 0 created.

**What is NOT changing in this plan:**
- The eval harness (scenarios, rubric, screenshot pipeline, judge)
- The eval rubric (being refined separately by the user)
- The test scenarios in `tests/presentation-builder/scenarios/`
- The candidate example files in `tests/presentation-builder/candidate-examples/` (read-only reference)
