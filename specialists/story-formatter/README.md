# Story Formatter

Takes raw storyteller output in any format and produces a canonical STORY OUTPUT block.
Pipeline equivalent of the researcher-formatter — the storyteller produces compelling prose,
this specialist ensures it arrives in structured format every time.

---

## Accepts

| Field | Type | Required | Description |
|---|---|---|---|
| storyteller_output | string | Yes | Raw output from the storyteller, in any format (prose, markdown document, partial STORY OUTPUT block) |
| original_input | string | Yes | The analysis, research, or document originally given to the storyteller — used to extract and classify findings |

---

## Returns

Canonical `StoryOutput` block (see `shared/interface/types.md`) with all required fields:

- `STORY OUTPUT` header (plain text, no markdown prefix)
- Metadata lines: input type, audience, tone, framework, quality threshold
- Parse summary line
- `NARRATIVE SELECTION` section: dramatic question, protagonist, framework rationale,
  `INCLUDED FINDINGS` with narrative roles, `OMITTED FINDINGS` with rationales
- Story prose (extracted and cleaned from storyteller output)
- `QUALITY THRESHOLD RESULT: MET` or `NOT MET`

---

## Can Do

- Accept storyteller output in any format: full markdown document, partial STORY OUTPUT block, plain prose
- Infer audience, tone, and framework from the prose content
- Classify which findings from the original input appear in the narrative
- Assign narrative roles to included findings (hook, complication, evidence, peak, resolution)
- Clean markdown formatting from prose (strip section headers, bold titles, citation markers)
- Infer dramatic question and protagonist from the narrative arc

---

## Cannot Do

- Generate new story prose — uses only what the storyteller produced
- Re-select findings based on its own editorial judgment
- Research new facts or add content not in the inputs
- Produce anything other than a STORY OUTPUT block

---

## Design Notes

This specialist is architecturally equivalent to the researcher-formatter:

| | researcher-formatter | story-formatter |
|---|---|---|
| Runs after | researcher | storyteller |
| Receives | Raw research narrative | Raw storyteller prose |
| Produces | Canonical RESEARCH OUTPUT block | Canonical STORY OUTPUT block |
| Core task | Extract claims, normalize confidence + tier labels | Extract prose, classify findings against narrative |

Always runs after the storyteller: `narrate → story-formatter → normalize-header → save`.

The storyteller produces narrative content; the formatter ensures it arrives in canonical
format. These are two different cognitive tasks — format compliance is not the storyteller's
job.
