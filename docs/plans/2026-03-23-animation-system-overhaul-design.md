# Animation System & Visual Content Overhaul Design

## Goal

Overhaul the presentation-builder's animation system and visual content guidance to produce visually rich, animated HTML presentations — replacing the current restrictive system with a tier-based library where every slide gets animation matched to its visual complexity, and steering the model toward generating rich visual content instead of defaulting to text-heavy layouts.

## Background

The presentation-builder prompt (`agents/presentation-builder.md`, ~3,097 lines) currently defines a minimal animation system:

- **3 keyframes:** `fadeIn`, `fadeUp`, `scaleIn` (bounce/overshoot)
- **Constraint:** "2–4 animated slides per deck"
- **Constraint:** "3–8 second durations, slow and subtle"
- **4 embedded candidate examples** teaching animation patterns
- **`.active` class gating** mechanism for triggering animations on slide visibility

This system is too restrictive. It produces decks where most slides are static and the few animated ones use a bouncy `scaleIn` that feels cheap. The constraint language ("every animation must earn its place") discourages the model from animating at all, and the lack of visual content guidance means the model defaults to text-heavy slides that wouldn't benefit from animation anyway.

We prototyped 3 animation variants (Apple Subtle, Rich Choreography, Cinematic Data) across existing decks and a 14-slide visual showcase. User testing revealed the winning approach: a tier system where animation richness matches visual complexity, combined with explicit encouragement to generate rich visual content worth animating.

## Approach

Two problems are solved together because they're interdependent:

1. **Animation system overhaul** — The new tier system gives the model a rich library of ~20 animations organized by visual complexity, with clear decision rules for when to use each tier. Every slide gets at least basic entrance animation; richer content earns richer animation.

2. **Visual content steering** — New prompt guidance pushes the model toward SVG charts, diagrams, and web-inspired elements. The animation library only pays off if there's visual content worth animating.

The approach was validated through iterative prototyping — building concrete HTML examples across three variant philosophies, testing them on real deck content, and selecting the best elements from each.

## Architecture

### Animation Tier System

The core architecture is a 3-tier system replacing the flat 3-keyframe approach:

```
Tier 1 — Subtle Entrance (default, every slide)
    │
    ├── fadeIn (opacity, 350ms, ease-out)
    └── fadeUp (opacity + 12px translate, 350ms, ease-out, 80ms stagger)

Tier 2 — Content-Aware (data visualizations, charts, tables)
    │
    ├── growRight / growUp (bars growing from base)
    ├── drawLine (SVG stroke-dashoffset for lines, connections, paths)
    ├── revealDown (clip-path reveal for emphasis text)
    ├── nodeReveal (scale 0.7→1 for diagram nodes)
    ├── badgePop (scale 0.8→1 for badges/tags)
    └── rowReveal (table rows building sequentially)

Tier 3 — Cinematic & Web-Inspired (diagrams, special moments)
    │
    ├── Multi-phase builds + ambient
    │   ├── flowDash (continuous flowing dashes on connections)
    │   └── pulse (subtle opacity oscillation on active elements)
    │
    ├── Selective special effects
    │   ├── countUp (JS numeric interpolation — ONE per deck)
    │   ├── Color shift (red→green for before/after)
    │   └── Blur-to-focus (cards sharpening into view)
    │
    └── Web-inspired motion
        ├── Typewriter / word-swap
        ├── Code typing (syntax-highlighted)
        ├── Morphing number (digits roll + color transition)
        ├── Animated counter row (dashboard metrics)
        ├── Stacked reveal (sections expanding)
        ├── Gradient text sweep
        └── Network/connection animation
```

### What's Killed

**`scaleIn`** (the bounce/overshoot keyframe) is removed entirely — from the prompt, all examples, and the mini-deck. It is never generated.

### Model Decision Rule

The model assesses each slide's content and picks the tier:

- Is it mostly text/cards? → **Tier 1**
- Does it have a data visualization (chart, graph, table)? → **Tier 2**
- Does it have a multi-component diagram or is it a "special moment" slide? → **Tier 3**
- **Limit:** one `countUp` per deck, on THE most important number

### Timing Principles (All Tiers)

| Parameter | Value |
|-----------|-------|
| Entrance durations | 300–500ms |
| Data viz sequence durations | 600–1200ms |
| Easing | `ease-out` (decelerate on arrival) |
| Stagger between elements | 80–120ms |
| Bounce / elastic / overshoot | **Never** |

The feel: "Apple Keynote — you barely notice the animation, but the deck feels alive."

### Constraint Changes from Old to New

| Old Constraint | New Constraint |
|---------------|---------------|
| "2–4 animated slides per deck" | **Every slide gets animation** — tier determines richness |
| "Slow and subtle. 3–8 second durations" | **300–500ms for entrances, 600–1200ms for data viz sequences** |
| `scaleIn` bounce/overshoot as hero animation | **Killed entirely** — no bounce, no overshoot, ever |
| 3 prescribed keyframes | **Full library across 3 tiers** — model chooses per slide |
| "Every animation must earn its place" (restrictive) | **Every slide gets at least Tier 1** — model's job is to go UP tiers when content supports it |

### Web-Inspired Creative Latitude

For web-inspired animations (typewriter, code typing, morphing numbers, gradient sweeps, animated counters, etc.), the model gets explicit creative latitude. The prompt should convey:

> "These are HTML files viewed in a browser, not exported to PowerPoint. For web-inspired animations, think like a thoughtful startup building a landing page. Experiment. The format supports anything the browser supports. Keep it appropriate for a presentation context — these ought to fit loosely into a presentation style format — but don't constrain yourself to traditional slide conventions. Take creative liberty with the fact that these will be viewed in a browser."

## Visual Content Steering

### Principle

"Every deck should have at least 2–3 slides where the visual element IS the content, not an illustration of the content."

### Visual Content Hierarchy

The model should prefer higher tiers over lower:

| Preference | Content Type | Example |
|-----------|--------------|---------|
| **Strongly prefer** | SVG data visualization (charts, graphs) | Bar chart showing revenue, line graph showing trends |
| **Strongly prefer** | SVG diagrams (architecture, flow, dependency) | Microservices topology, CI/CD pipeline |
| **Prefer** | Interactive/web-inspired elements | Typewriter identity slide, code typing, morphing numbers |
| **Acceptable** | Styled card grids with data | Metric cards, comparison cards, status cards |
| **Avoid when possible** | Text-heavy layouts | Bullet point lists, long paragraphs, text-only slides |

### Decision Rule

Before generating any slide, the model should ask: "Could this information be shown visually?"

- Slide about performance improvement → morphing number, not a sentence
- Slide about system architecture → SVG diagram, not a description
- Slide comparing quantities → bar chart, not a table of numbers

### Minimum Visual Richness Target

At least **30–40%** of slides in any deck should contain SVG data visualizations or diagrams. For a 10-slide deck, that's 3–4 slides with actual visual content beyond styled cards.

## Candidate Examples Strategy

Replace the existing 4 embedded examples with 8 new ones demonstrating the full tier system. Sources are from the prototyping session, aligned to user-preferred variants:

| # | Example | Source | Teaches |
|---|---------|--------|---------|
| 1 | Bar chart with growing bars | Visual showcase slide 1, Variant B | Tier 2 — `growRight` + stagger |
| 2 | Line graph with drawing lines | Visual showcase slide 2, Variant B | Tier 2 — `drawLine` + data points |
| 3 | Architecture diagram with flow | Visual showcase slide 6, Variant C | Tier 3 — multi-phase + `flowDash` |
| 4 | Code security scan | Visual showcase slide 5, Variant B | Tier 2/3 — scan line + highlights |
| 5 | Before/After transformation | Existing Example 3 (updated, scaleIn removed) | Asymmetric animation as narrative |
| 6 | Typewriter / word-swap | Visual showcase slide 11 | Web-inspired — creative latitude |
| 7 | Morphing number with color shift | Visual showcase slide 13, Variant C | Web-inspired — digits roll + red→green |
| 8 | Section transition with gradient | Existing candidate 04 | Ambient — chapter break slides |

The prototype HTML files in `tests/presentation-builder/animation-prototypes/` serve as source material for extracting these candidate examples into the prompt.

## Prompt Changes Summary

### What Changes in `agents/presentation-builder.md`

| Area | Current State | New State |
|------|--------------|-----------|
| Animation as Storytelling section | 5 archetypes, 3 keyframes, "2–4 animated slides", "3–8s durations" | Tier system (3 tiers), full library (~20 animations), "every slide animated", "300–500ms entrances / 600–1200ms data viz", web-inspired creative latitude |
| Candidate examples | 4 embedded examples using scaleIn | 8 examples demonstrating all 3 tiers + web-inspired |
| Visual content guidance | _(new section)_ | Visual content hierarchy, 30–40% visual richness target, "could this be shown visually?" decision rule |
| Pre-flight checklist | References old animation constraints | Updated to reference tier system, no scaleIn, reduced-motion still required |
| scaleIn keyframe | Defined and used in examples + mini-deck | Removed from all locations |
| Constraint language | "2–4 animated slides per deck", "slow and subtle, 3–8 second durations" | "Every slide gets at least Tier 1 entrance animation", "300–500ms entrances, 600–1200ms data viz" |

### What Stays the Same

- **`.active` gating mechanism** — animations trigger on slide visibility
- **`prefers-reduced-motion` requirement** — hard accessibility gate
- **Navigation engine** — goTo, keyboard, progress bar
- **5-slide mini-deck structure** in the prompt (but its animations get updated to use the new system)

## Prototype Artifacts

The following prototype files were created during the design process and live in `tests/presentation-builder/animation-prototypes/`:

### Round 1 — Existing Deck Re-animation

Entrance animations applied to existing deck content:

- `01-qbr-variant-a-apple-subtle.html`
- `01-qbr-variant-b-rich-choreography.html`
- `01-qbr-variant-c-cinematic-data.html`
- `02-competitive-variant-a-apple-subtle.html`
- `02-competitive-variant-b-rich-choreography.html`
- `02-competitive-variant-c-cinematic-data.html`

### Round 2 — Visual Showcase

Rich visual elements built from scratch across a 14-slide deck:

- `visual-showcase-variant-a.html` (62KB) — clean fadeIn/fadeUp everywhere
- `visual-showcase-variant-b.html` (93KB) — content-aware: bars grow, lines draw, scan sweeps
- `visual-showcase-variant-c.html` (88KB) — full cinematic: multi-phase + countUp + flowDash + pulses

## Testing Strategy

- **Candidate example validation:** Each of the 8 new candidate examples will be extracted from the prototype HTML and verified to render correctly in isolation before embedding in the prompt.
- **End-to-end generation:** After prompt changes, generate decks across diverse topics and verify the model uses the tier system appropriately (Tier 1 on text slides, Tier 2 on charts, Tier 3 on diagrams).
- **Visual richness audit:** Check that generated decks hit the 30–40% visual content target.
- **Regression check:** Verify `.active` gating, `prefers-reduced-motion`, and navigation still work.
- **scaleIn elimination:** Grep generated output to confirm `scaleIn` never appears.
- **Eval rubric update:** The D5 animation dimension in the evaluation rubric needs updating to score against the tier system rather than the old constraints.

## Open Questions

1. **Invention beyond the library** — Should the model be allowed to invent NEW animation patterns beyond the defined set, or should it stick strictly to the library?
2. **Eval rubric alignment** — How do we evaluate animation quality in the rubric? The current D5 dimension scores animation and needs updating to match the tier system.
3. **Deck-level consistency** — Should we add guidance for animation consistency across a deck (e.g., "if you use `drawLine` on one diagram, use it on all diagrams in the same deck")?
