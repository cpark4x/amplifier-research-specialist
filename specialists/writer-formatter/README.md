# Writer Formatter

Takes raw writer output in any format plus the original source material and produces
a canonical Writer output block with all required structural elements. Pipeline
equivalent of the researcher-formatter and story-formatter — the writer produces good
prose, this specialist ensures it arrives in structured format every time.

---

## Accepts

| Field | Type | Required | Description |
|---|---|---|---|
| writer_output | string | Yes | Raw output from the writer specialist, in any format (structured doc, informal prose, partially-formed output) |
| source_material | string | Yes | The original source material passed to the writer (RESEARCH OUTPUT, AnalysisOutput, or CompetitiveAnalysisOutput) |

---

## Returns

Canonical Writer output block with all required fields:

- `Parsed:` line (first line — pipeline signal)
- S-numbered claims list (extracted from source material)
- Document prose (cleaned from writer output)
- `CLAIMS TO VERIFY` block
- `---` separator
- `WRITER METADATA` block
- `CITATIONS` block (every S-number accounted for)

---

## Can Do

- Accept writer output in any format: structured document, informal prose, partial Writer output
- Extract S-numbered claims from any source material type (researcher-output, analysis-output, competitive-analysis-output)
- Infer format, audience, voice, and word count from writer prose
- Generate CLAIMS TO VERIFY by scanning prose for numerical/verifiable claims
- Map S-numbers to prose usage for CITATIONS block
- Clean intro preamble ("So, here's what I found...") from writer output

---

## Cannot Do

- Rewrite or improve writer prose — preserves it exactly
- Generate new claims not present in source material
- Research new facts
- Produce output without all five structural blocks

---

## Design Notes

Architecturally equivalent to researcher-formatter and story-formatter:

| | researcher-formatter | story-formatter | writer-formatter |
|---|---|---|---|
| Runs after | researcher | storyteller | writer |
| Receives | Raw research narrative | Raw story prose + findings | Raw writer prose + source material |
| Produces | Canonical RESEARCH OUTPUT | Canonical STORY OUTPUT | Canonical Writer output |
| Core task | Extract + normalize claims | Classify findings + wrap | Extract claims + wrap blocks |

Always runs after the writer: `write → format-writer → save`.

The writer produces audience-calibrated prose; the formatter ensures it arrives
with the structural blocks that downstream agents and parsers depend on.
