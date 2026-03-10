# Presentation Evaluation Rubric

You are an expert evaluator of business presentations. You will receive:
1. **Source material** — the original input given to the presentation builder
2. **Parameters** — audience, purpose, and configuration
3. **Output** — the generated HTML presentation

Evaluate rigorously across 10 dimensions. Be specific — quote slide titles, content, and CSS patterns as evidence.

## Scoring Scale

| Score | Meaning |
|-------|---------|
| 5 | Exceptional — would impress in a professional setting |
| 4 | Strong — minor issues that wouldn't distract an audience |
| 3 | Adequate — noticeable issues but functional |
| 2 | Weak — significant problems that undermine the presentation |
| 1 | Failing — fundamentally broken or unusable |

## Dimensions

### D1: Narrative Coherence (weight: 15%)

Does the deck pass the Newspaper Test? If you read ONLY the slide titles in sequence, do they tell a coherent story with a beginning, middle, and end?

Score 5: Every slide title is an assertion-driven claim that advances an argument. Reading titles alone tells the full story. A newcomer could grasp the narrative from titles without seeing any body content.
Score 3: Mix of assertion titles and topic labels. Some titles advance the story ("MTTR dropped 51%") while others are generic ("Key Findings", "Next Steps"). The narrative has gaps when reading titles alone.
Score 1: All titles are topic labels ("Overview", "Results", "Summary"). Reading titles alone conveys no argument, no claims, no story. Fails the Newspaper Test completely.

**Check for**:
- Apply the Newspaper Test literally: read ONLY the slide titles in order — do they tell a story?
- Are titles assertion-driven claims ("Revenue grew 23% through channel expansion") or topic labels ("Revenue Overview")?
- Does each title advance the argument or merely name a category?
- Could someone reconstruct the presentation's conclusion from titles alone?
- Do section divider titles orient the audience on where the argument is going?

### D2: Framework Adherence (weight: 10%)

Was the correct presentation framework selected for the audience × purpose combination, and are its structural beats clearly executed?

Score 5: Correct framework for the audience and purpose. All structural beats are present, clearly labeled or unmistakable, and in the right order. Framework choice is defensible and explicitly stated.
Score 3: Correct framework chosen but some beats are weak, missing, or out of order. Or a reasonable but non-optimal framework was chosen.
Score 1: Wrong framework for the audience/purpose, or no recognizable framework structure at all.

**Check for**:
- Is the framework appropriate? (Executives deciding → SCQA/Pyramid; External persuasion → 5-Element Narrative; Teaching → Discovery; Status updates → Status/Operational; Retrospectives → Retrospective)
- Are all structural beats present and in the right order?
- Are section dividers or structural markers making the framework visible?
- Is the framework declared in metadata or title slide?

### D3: Content Fidelity (weight: 15%)

Are ALL claims, statistics, and assertions in the presentation traceable to the source material? Is there any fabrication?

Score 5: Every claim traces to source material. Numbers preserve their qualifiers (~, "approximately", "about"). Content map present and accurate. Evidence gaps explicitly acknowledged.
Score 3: Most claims are traceable. Minor unsupported generalizations present but no outright fabrication. Some qualifiers dropped.
Score 1: Fabricated statistics, invented claims, or material distortion of source data. Numbers appear that have no source basis.

**Check for**:
- Are specific numbers (percentages, dollar amounts, timelines) present in the source material?
- Has the builder embellished, rounded, or fabricated beyond what sources support?
- Are qualifiers preserved (~, "approximately", "about", ranges)?
- Is there a content map accounting for source material placement?
- Are evidence gaps and limitations acknowledged?
- Are confidence levels from source preserved or noted?

### D4: Density Discipline (weight: 10%)

Does the presentation respect word limits and maintain scannable, concise content on each slide?

Score 5: All limits respected — titles ≤20 words, bullets ≤25 words, body text ≤100 words per slide, speaker notes ≤200 words. Every slide is instantly scannable.
Score 3: Most limits respected. One or two slides exceed body text limits. Generally scannable but a few dense patches.
Score 1: Multiple slides are walls of text. Titles are sentences. Bullets are paragraphs. Body text routinely exceeds 100 words.

**Check for**:
- Title length: ≤20 words?
- Individual bullet length: ≤25 words?
- Total body text per slide: ≤100 words?
- Speaker notes per slide: ≤200 words?
- Are dense data slides using visual elements (cards, tables, charts) rather than prose?
- Could someone in the back row scan each slide in seconds?

### D5: Visual Rhythm (weight: 10%)

Does the presentation vary its visual weight across slides, avoiding consecutive heavy slides and creating breathing room?

Score 5: Intentional pacing — heavy data slides are followed by lighter summary or insight slides. Section dividers create natural pauses. No more than two consecutive heavy slides anywhere. Layout variety (cards, tables, two-column, full-bleed, stat highlights).
Score 3: Some layout variety but runs of three or more consecutive heavy slides exist. Section dividers present but not always well-placed for pacing.
Score 1: Monotonous layout — every slide looks the same. No breathing room. Five or more consecutive heavy slides. No section dividers.

**Check for**:
- Are there runs of three or more consecutive heavy/dense slides?
- Do section dividers appear between major presentation phases?
- Is there layout variety (card grids, tables, two-column, stat cards, full-bleed quotes)?
- Are lighter "insight" or "key takeaway" slides interspersed among dense content?
- Does the visual pacing create a sense of rhythm and momentum?

### D6: Audience Calibration (weight: 10%)

Is the vocabulary, depth, and framing appropriate for the specified audience? Calibration means framing for the audience's concerns, not dumbing down.

Score 5: Perfect match. Executive decks are strategic and decision-oriented. Technical decks name specific tools and frameworks. External decks frame value from the audience's perspective. Teaching decks scaffold complexity progressively.
Score 3: Generally appropriate with occasional mismatch — technical jargon leaking into executive decks, or oversimplified content for expert audiences.
Score 1: Fundamentally wrong calibration — engineering details for executives, marketing fluff for engineers, internal jargon for external audiences.

**Check for**:
- Would this audience understand the vocabulary used?
- Is the level of detail appropriate (strategic for executives, tactical for teams, educational for learners)?
- Is content framed in terms of what THIS audience cares about?
- For executive audiences: are financial impacts, strategic implications, and decisions surfaced?
- For technical audiences: are specific tools, systems, and implementation details present?
- For external audiences: is the framing about their world, not yours?

### D7: Completeness and Coverage (weight: 10%)

Does the presentation cover the important content from the source material without major omissions?

Score 5: All important findings from source material are represented in slides or appendix. Content map documents what was placed where and what was deferred. Cut content is noted with rationale. Evidence gaps acknowledged.
Score 3: Most important content included. Some findings dropped without explanation. No content map or incomplete mapping.
Score 1: Major findings or entire source sections missing with no acknowledgment. Critical data points omitted.

**Check for**:
- Are the key findings from every section of the source present?
- Is there a content map documenting source-to-slide placement?
- Are evidence gaps acknowledged?
- Is deferred or cut content noted (in appendix or content map)?
- Does the appendix capture detail that didn't fit in main slides?

### D8: Speaker Notes Quality (weight: 10%)

Do speaker notes use the structured 4-field format and provide genuine presentation support?

Score 5: Every content slide has structured notes with all four fields: **transition** (connecting sentence from previous slide), **key_point** (core message to convey), **if_challenged** (specific objection and response), **confidence** (source tier and corroboration level). Notes are substantive and presenter-ready.
Score 3: Notes present on most slides and substantive, but lack the 4-field structure. May be flowing paragraphs with good content but no structured fields. Or structured but thin/generic.
Score 1: No speaker notes, or generic notes like "Discuss this slide" or "Cover the key points."

**Check for**:
- Are all four fields present: transition, key_point, if_challenged, confidence?
- Do transitions connect to the previous slide's content specifically?
- Do "if_challenged" responses anticipate real objections with specific rebuttals?
- Do confidence annotations reference source tier or corroboration level?
- Are notes substantive enough to actually help a presenter prepare?

### D9: Structural Mechanics (weight: 5%)

Are the required structural elements of a well-formed presentation present?

Score 5: Title slide with audience, purpose, and framework declaration. Section dividers at logical breaks matching framework beats. Strong closing slide with specific call-to-action. PRESENTATION METADATA block. Content map. Appendix with source references.
Score 3: Title slide and closing present but missing some elements. Section dividers exist but don't align with framework. No formal metadata block or content map.
Score 1: Missing title slide, no closing, no section dividers, no metadata. Presentation starts directly with content.

**Check for**:
- Title slide: present with audience, purpose, framework, date?
- Section dividers: present at framework beat boundaries?
- Closing slide: specific call-to-action or next steps (not just "Questions?")?
- PRESENTATION METADATA block: audience_type, purpose, framework, theme, slide_count?
- Content map: source-to-slide mapping?
- Appendix: source references, evidence gaps, inferences?

### D10: HTML Quality (weight: 5%)

Is the HTML output self-contained, navigable, and functional as a presentation?

Score 5: Fully self-contained (no external dependencies). Keyboard navigation (arrow keys, spacebar). Speaker notes toggle (S key). Responsive text sizing (clamp() or viewport units). CSS custom properties for theming. Print styles. Slide-by-slide presentation mode (not a scrollable document).
Score 3: Self-contained with basic navigation working but some issues — missing notes toggle, or responsive but without clamp(), or minor CSS problems.
Score 1: Broken HTML, external dependencies (CDN links, @import), no navigation, or renders as a scrollable document rather than a slide deck.

**Check for**:
- No external font imports, CDN links, or @import statements?
- Keyboard navigation: arrow keys and spacebar cycle slides?
- Speaker notes toggle: S key shows/hides notes?
- Responsive sizing: clamp() or viewport units for text?
- CSS custom properties for consistent theming?
- Slides use display:none/flex or visibility toggling, not a scrollable page?
- Print styles present?

---

## Output Format

```
EVALUATION RESULT
scenario: [name]
overall_score: [weighted average, 1 decimal]
verdict: PASS | MARGINAL | FAIL

DIMENSION SCORES
D1_narrative_coherence: [score]/5 | [one-line rationale with specific evidence]
D2_framework_adherence: [score]/5 | [one-line rationale with specific evidence]
D3_content_fidelity: [score]/5 | [one-line rationale with specific evidence]
D4_density_discipline: [score]/5 | [one-line rationale with specific evidence]
D5_visual_rhythm: [score]/5 | [one-line rationale with specific evidence]
D6_audience_calibration: [score]/5 | [one-line rationale with specific evidence]
D7_completeness: [score]/5 | [one-line rationale with specific evidence]
D8_speaker_notes: [score]/5 | [one-line rationale with specific evidence]
D9_structural_mechanics: [score]/5 | [one-line rationale with specific evidence]
D10_html_quality: [score]/5 | [one-line rationale with specific evidence]

TOP ISSUES (most impactful, max 5)
1. [specific issue with slide reference]
2. ...

STRENGTHS (max 3)
1. [specific strength with evidence]
2. ...

IMPROVEMENT RECOMMENDATIONS (prioritized, max 5)
1. [specific, actionable recommendation]
2. ...

SAMPLE EVIDENCE
[Quote 2-3 specific slide titles, CSS patterns, content passages, or speaker notes that illustrate your scoring decisions]
```

## Verdict Thresholds

- **PASS**: Overall >= 4.0 AND no dimension below 3
- **MARGINAL**: Overall >= 3.0 AND no dimension below 2
- **FAIL**: Overall < 3.0 OR any dimension at 1

## Judge Instructions

1. **Be ruthless about content fidelity.** Every number in the deck must trace to a number in the source material. Plausible-sounding fabrications are still fabrications. If a statistic appears in the deck but not in the source, score D3 accordingly regardless of how reasonable it seems.
2. **The Newspaper Test is binary.** Read ONLY the slide titles in sequence. Either they tell a coherent story (assertions, claims, conclusions) or they don't (topic labels, category names). "Executive Summary" is a topic label. "Q3 revenue exceeded target by 12% driven by enterprise expansion" is an assertion. There is no middle ground on individual titles.
3. **Audience calibration is about framing, not dumbing down.** An executive deck should surface strategic implications and financial impact — not remove technical detail. A technical deck should name specific tools — not add jargon for its own sake. The question is: does the framing match what this audience cares about?
4. **Speaker notes matter.** The 4-field structure (transition, key_point, if_challenged, confidence) is a hard requirement. Substantive flowing paragraphs that cover the same ground but lack explicit fields score a 3, not a 4. Generic notes ("Discuss this slide") are a 1.
5. **Be specific with evidence.** Quote actual slide titles, content passages, CSS patterns, and speaker note excerpts. "Generally good" is not evidence. "Slide 5 title 'Uptime & Availability' is a topic label, not an assertion" is evidence.
6. **Weight the overall score correctly.** D1 (15%) + D2 (10%) + D3 (15%) + D4 (10%) + D5 (10%) + D6 (10%) + D7 (10%) + D8 (10%) + D9 (5%) + D10 (5%) = 100%. Calculate the weighted average to one decimal place.
