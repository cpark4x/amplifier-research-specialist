# Presentation Builder

Transforms structured source material into visually stunning HTML slide decks for knowledge work — research readouts, competitive analysis, strategy decks, team updates, and executive briefings.

Principles-based design grounded in cognitive science and visual hierarchy. The specialist understands storytelling, audience calibration, and visual design — and has creative freedom to apply them.

## Accepts

| Field | Type | Required | Default |
|---|---|---|---|
| `source_material` | string | Yes | — |
| `audience` | string | Yes | — |
| `purpose` | string | No | inferred |
| `output_format` | `html` | No | `html` |
| `theme` | string | No | inferred from content |

## Returns

Self-contained HTML slide deck with embedded CSS, JavaScript navigation, speaker notes, and metadata.

## Can Do

- Accept any structured input (research, competitive analysis, writer output, raw notes)
- Select narrative structure appropriate to audience and purpose
- Render CSS data visualizations (charts, metrics, comparisons)
- Produce responsive, navigable HTML presentations
- Calibrate density and framing by audience type

## Cannot Do

- Source or embed images
- Research new facts
- Draw new inferences
- Write prose documents
- Generate claims not in source material
