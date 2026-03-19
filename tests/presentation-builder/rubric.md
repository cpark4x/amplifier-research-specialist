# Presentation Evaluation Rubric

You are an expert evaluator of business presentations. You will receive:
1. **Source material** — the original input given to the presentation builder
2. **Parameters** — audience, purpose, and configuration
3. **Output** — the generated HTML presentation

Evaluate rigorously across 12 dimensions. Be specific — quote slide titles, content, and CSS patterns as evidence.

## Scoring Scale

| Score | Meaning |
|-------|---------|
| 5 | Exceptional — would impress in a professional setting |
| 4 | Strong — minor issues that wouldn't distract an audience |
| 3 | Adequate — noticeable issues but functional |
| 2 | Weak — significant problems that undermine the presentation |
| 1 | Failing — fundamentally broken or unusable |

## Evaluation Method: Explanation Before Score

For EACH dimension, you MUST:
1. **Write your analysis FIRST** — examine specific evidence, quote slide titles and content, apply the dimension's checks literally
2. **Only AFTER completing your analysis**, commit to a score
3. **Do NOT write the score until the analysis paragraph is complete**

This ordering is mandatory. Writing the score first and then justifying it produces less accurate evaluations due to anchoring bias. The analysis must drive the score, not the reverse.

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

### D4: Density Discipline (weight: 8%)

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

### D5: Visual Rhythm (weight: 8%)

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

### D6: Audience Calibration (weight: 12%)

Is the vocabulary, depth, and framing appropriate for the specified audience? Calibration means framing for the audience's concerns, not dumbing down.

Score 5: Perfect match. Executive decks are strategic and decision-oriented. Technical decks name specific tools and frameworks. External decks frame value from the audience's perspective. Teaching decks scaffold complexity progressively. General/non-specialist audiences get accessible explanations without condescension.
Score 3: Generally appropriate with occasional mismatch — technical jargon leaking into executive decks, or oversimplified content for expert audiences.
Score 1: Fundamentally wrong calibration — engineering details for executives, marketing fluff for engineers, internal jargon for external audiences.

**Check for**:
- Would this audience understand the vocabulary used?
- Is the level of detail appropriate (strategic for executives, tactical for teams, educational for learners)?
- Is content framed in terms of what THIS audience cares about?
- For executive audiences: are financial impacts, strategic implications, and decisions surfaced?
- For technical audiences: are specific tools, systems, and implementation details present?
- For external audiences: is the framing about their world, not yours?
- For non-specialist audiences: are complex concepts made accessible without condescension?

### D7: Completeness and Coverage (weight: 8%)

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

### D8: Speaker Notes Quality (weight: 7%)

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

### D11: Insight Density (weight: 10%)

Does every data slide state its implication? Does the deck build to a clear, inevitable conclusion? This dimension measures whether the presentation drives understanding and action, not just displays information.

Score 5: Every data point and finding is paired with its "so what" — the implication is explicit, not left for the audience to infer. The deck builds toward a conclusion that feels inevitable given the evidence. There is a single, clear takeaway the audience would remember after leaving the room.
Score 3: Some slides state implications but others present data without interpretation. The overall argument is present but not every slide advances it. The conclusion exists but doesn't feel like a natural consequence of the evidence.
Score 1: Data is presented without interpretation. Slides show numbers, charts, or findings but never state what they mean. No clear takeaway. The audience would leave asking "so what?"

**Check for**:
- Does each data slide explicitly state what the data means, not just what it is?
- Are implications framed in terms of what the audience should do or think differently?
- Does the deck build toward a single, memorable conclusion?
- Could you state the "one big idea" of this presentation in one sentence?
- Is the conclusion a natural consequence of the evidence presented, or does it feel bolted on?
- Are "insight" or "implication" statements present on data-heavy slides?

### D12: Information Design (weight: 10%)

When the source material contains structured data, is it presented visually rather than as prose? This dimension measures whether the builder makes effective use of visual information display.

Score 5: Comparison data is in tables or matrices. Trends and changes use stat cards with directional indicators. Key numbers are given visual prominence (large type, callout boxes, stat highlights). Relationships are shown spatially. Dense data uses cards, grids, or visual groupings rather than bullet lists. The visual format accelerates comprehension.
Score 3: Some data is visualized effectively but other data that would benefit from tables or visual treatment is presented as prose or bullet points. Mixed execution.
Score 1: All data is presented as prose or bullet lists regardless of structure. Comparison data that belongs in a table is in paragraphs. Numbers that should be visually prominent are buried in body text. No use of visual data display.

**Check for**:
- When source has comparison data (A vs B vs C), is it in a table or matrix?
- Are key statistics given visual prominence (stat cards, large numbers, callout boxes)?
- Are trends shown with directional indicators (arrows, color coding, before/after)?
- Does the slide format match the data structure (lists for lists, grids for comparisons, timelines for sequences)?
- Would a different visual format make any slide's data more immediately comprehensible?
- Are there slides where prose is doing the job of a table or chart?

---

## Output Format

For each dimension, write your analysis FIRST, then score. Use this exact format:

```
EVALUATION RESULT
scenario: [name]
overall_score: [weighted average, 1 decimal]
verdict: PASS | MARGINAL | FAIL

DIMENSION SCORES

D1: NARRATIVE COHERENCE (15%)
Analysis: [2-4 sentences examining specific slide titles, applying the Newspaper Test literally. Quote actual titles. Identify which are assertions vs topic labels.]
Score: [n]/5

D2: FRAMEWORK ADHERENCE (10%)
Analysis: [2-4 sentences checking framework selection and beat execution. Name the framework used and whether it matches audience x purpose. Identify missing or weak beats.]
Score: [n]/5

D3: CONTENT FIDELITY (15%)
Analysis: [2-4 sentences tracing claims to source material. Identify any fabricated or unsupported numbers. Note preserved or dropped qualifiers. Check for content map.]
Score: [n]/5

D4: DENSITY DISCIPLINE (8%)
Analysis: [2-4 sentences checking word limits on specific slides. Quote any overlong titles or dense body text. Note visual analysis evidence for scanability.]
Score: [n]/5

D5: VISUAL RHYTHM (8%)
Analysis: [2-4 sentences examining slide pacing. Identify runs of consecutive heavy slides. Note layout variety. Reference visual analysis evidence.]
Score: [n]/5

D6: AUDIENCE CALIBRATION (12%)
Analysis: [2-4 sentences evaluating vocabulary, depth, and framing match. Quote specific passages that match or mismatch the target audience.]
Score: [n]/5

D7: COMPLETENESS (8%)
Analysis: [2-4 sentences checking source coverage. Identify any major omissions. Note content map presence and accuracy.]
Score: [n]/5

D8: SPEAKER NOTES (7%)
Analysis: [2-4 sentences checking note structure. Quote examples of good and bad notes. Check for 4-field format presence.]
Score: [n]/5

D9: STRUCTURAL MECHANICS (5%)
Analysis: [2-4 sentences checking required elements. Note title slide, dividers, closing, metadata block presence.]
Score: [n]/5

D10: HTML QUALITY (5%)
Analysis: [2-4 sentences checking technical implementation. Note navigation, responsiveness, self-containment. Reference visual analysis evidence.]
Score: [n]/5

D11: INSIGHT DENSITY (10%)
Analysis: [2-4 sentences examining whether data slides state their implications. Quote examples of "so what" statements or their absence. Assess whether the deck builds to a clear conclusion.]
Score: [n]/5

D12: INFORMATION DESIGN (10%)
Analysis: [2-4 sentences examining how structured data is displayed. Identify data presented as prose that should be visual. Note effective use of tables, stat cards, or visual groupings.]
Score: [n]/5

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

1. **Content fidelity is paramount.** Every number in the deck must trace to a number in the source material. Plausible-sounding fabrications are still fabrications. If a statistic appears in the deck but not in the source, score D3 accordingly regardless of how reasonable it seems.
2. **The Newspaper Test is binary.** Read ONLY the slide titles in sequence. Either they tell a coherent story (assertions, claims, conclusions) or they don't (topic labels, category names). "Executive Summary" is a topic label. "Q3 revenue exceeded target by 12% driven by enterprise expansion" is an assertion. There is no middle ground on individual titles.
3. **Audience calibration is about framing, not dumbing down.** An executive deck should surface strategic implications and financial impact — not remove technical detail. A technical deck should name specific tools — not add jargon for its own sake. A deck for non-specialists should make complex topics accessible without condescension. The question is: does the framing match what this audience cares about?
4. **Speaker notes matter.** The 4-field structure (transition, key_point, if_challenged, confidence) is a hard requirement. Substantive flowing paragraphs that cover the same ground but lack explicit fields score a 3, not a 4. Generic notes ("Discuss this slide") are a 1.
5. **Be specific with evidence.** Quote actual slide titles, content passages, CSS patterns, and speaker note excerpts. "Generally good" is not evidence. "Slide 5 title 'Uptime & Availability' is a topic label, not an assertion" is evidence.
6. **Use the visual analysis for visual dimensions.** For D4 (Density Discipline), D5 (Visual Rhythm), D10 (HTML Quality), and D12 (Information Design), incorporate the visual analysis findings. The visual analysis tells you what the slides ACTUALLY LOOK LIKE when rendered — use this over CSS inference. Reference specific visual observations in your rationale.
7. **Insight density is about interpretation, not repetition.** Showing a number is not insight. Stating what the number means for the audience is insight. "Revenue: $45.2B" is data. "A $45.2B market growing at 14.8% signals a window for entry before consolidation" is insight. Score D11 based on whether data slides include this interpretive layer.
8. **Information design rewards visual thinking.** When source material contains comparison data, the correct display is a table or matrix, not prose. When there are key statistics, they deserve visual prominence. Score D12 based on whether the builder chose the right visual format for the data structure.
9. **Write analysis BEFORE scoring.** For each dimension, complete your analytical observations before committing to a number. This is not optional — it is the evaluation method. Scores written before analysis are unreliable.
10. **Weight the overall score correctly.** D1 (15%) + D2 (10%) + D3 (15%) + D4 (8%) + D5 (8%) + D6 (12%) + D7 (8%) + D8 (7%) + D9 (5%) + D10 (5%) + D11 (10%) + D12 (10%) = 113%. **Normalize**: divide the weighted sum by 1.13 to produce the overall score on a 1-5 scale. Calculate to one decimal place.

**Weight normalization note**: The 12 dimensions sum to 113% rather than 100% by design — the two new dimensions (D11, D12) were added without proportionally shrinking all existing dimensions, since D4/D5/D7/D8 were already at appropriate absolute weights. The normalization divisor (1.13) ensures the overall score remains on the 1-5 scale. A future rubric revision may rebalance to exactly 100%.