# Shared Interface Types

These types are the stable contracts that all specialists follow. They do not change when specialist implementations evolve. Orchestrators and downstream specialists depend on them.

---

## ResearchOutput

The canonical output of the research pipeline (Researcher → Formatter). The Researcher
produces evidence in whatever format is natural for the research task; the Formatter
normalizes it into this schema. Downstream consumers depend on formatter output, not
raw researcher output.

```typescript
interface ResearchOutput {
  // What was researched
  question: string
  query_type: 'person' | 'company' | 'technical' | 'market' | 'event'
  quality_threshold: 'medium' | 'high' | 'maximum'

  // The evidence — one entry per discrete claim
  findings: Finding[]

  // What couldn't be verified
  evidence_gaps: EvidenceGap[]

  // Overall trustworthiness signal
  quality_score: 'low' | 'medium' | 'high'

  // What to research next
  follow_up_questions: string[]

  // Full observability trail
  research_events: ResearchEvent[]
}

interface Finding {
  sub_question: string          // Which sub-question this addresses
  claim: string                 // The specific, discrete claim
  source_url: string            // Where it came from
  source_tier: 'primary' | 'secondary' | 'tertiary'
  confidence: 'high' | 'medium' | 'low'
  corroboration_count: number   // How many independent sources confirm this
  timestamp: string             // When the source was published (if known)
  is_direct_quote: boolean      // Exact quote vs. paraphrase
}

interface EvidenceGap {
  description: string           // What couldn't be found
  fallbacks_attempted: string[] // What was tried before giving up
  reason: string                // Why it's inaccessible (paywall, no index, etc.)
}

interface ResearchEvent {
  stage: string
  action: 'source_attempted' | 'claim_extracted' | 'corroboration_found' | 'gap_identified' | 'quality_gate_check'
  detail: string
  timestamp: string
}
```

---

## Source Tiers

| Tier | Definition | Examples |
|---|---|---|
| **Primary** | The subject speaks directly | Personal blog, official announcement, congressional testimony, direct quote |
| **Secondary** | Credible third-party reporting | AP, Reuters, CNBC, TechCrunch, Washington Post |
| **Tertiary** | Aggregation, summary, or single-source speculation | Wikipedia, summary blogs, unconfirmed reports |

---

## Confidence Levels

| Level | Meaning |
|---|---|
| **High** | Primary source or confirmed by 2+ independent secondary sources |
| **Medium** | Single secondary source or tertiary confirmed by one secondary |
| **Low** | Single tertiary source, unconfirmed, or journalist-mediated (not direct) |

---

## Confidence Mapping (Writer Output)

When the Writer produces CITATIONS, it maps Researcher confidence levels to numeric values.
These are **fixed categorical-to-numeric mappings**, not measured probabilities.

| Categorical | Numeric | Notes |
|-------------|---------|-------|
| `high`      | `0.9`   | Primary source or 2+ independent secondary sources |
| `medium`    | `0.6`   | Single secondary source |
| `low`       | `0.3`   | Single tertiary or unconfirmed source |
| `unrated`   | —       | Source has no Researcher confidence signal (raw notes, analyst output) |

The numeric values are intentionally spaced to reflect the categorical gap — they are not
interchangeable with a continuously-measured confidence score.

---

## CompetitiveAnalysisOutput

The canonical output of the Competitive Analysis specialist.

```typescript
interface CompetitiveAnalysisOutput {
  // What was analyzed
  query: string
  comparison_type: 'head-to-head' | 'landscape'
  subjects: string[]
  dimensions_analyzed: number

  // The comparison grid — one entry per subject+dimension
  comparison_matrix: ComparisonEntry[]

  // Summary profile per subject (facts only)
  profiles: SubjectProfile[]

  // Strategic inferences — clearly labeled, traceable to matrix
  win_conditions: WinCondition[]
  positioning_gaps: PositioningGap[]

  // What couldn't be verified
  evidence_gaps: EvidenceGap[]   // reuse from ResearchOutput

  // Overall trustworthiness signal
  quality_score: 'low' | 'medium' | 'high'
  quality_threshold_met: boolean
}

interface ComparisonEntry {
  subject: string
  dimension: string
  rating: 'strong' | 'moderate' | 'weak' | 'unknown'
  confidence: 'high' | 'medium' | 'low'
  evidence: string            // one-sentence fact with source
}

interface SubjectProfile {
  subject: string
  primary_advantage: string   // one phrase — what this subject has that others lack
  key_weakness: string        // one phrase — where this subject is consistently weaker
}

interface WinCondition {
  subject: string
  wins_when: string           // "When the buyer prioritizes X..."
  loses_when: string          // "When the buyer prioritizes X..."
}

interface PositioningGap {
  gap: string                 // "Subject A has no [capability]"
  benefits: string            // which competitor benefits from this gap
}
```

---

## AnalysisOutput

The canonical output of the Data Analyzer specialist.

```typescript
interface AnalysisOutput {
  // What was analyzed
  question: string
  focus_question: string | null   // null if not provided by caller
  quality_threshold: 'low' | 'medium' | 'high'   // Controls minimum inference confidence. Note: different vocab from ResearchOutput.quality_threshold ('medium'|'high'|'maximum') — ResearchOutput measures research rigor; this measures inference confidence floor.

  // Findings projected from ResearchOutput.Finding — subset of fields with Analyzer-assigned IDs (F1...Fn)
  findings: AnalysisFinding[]

  // The inference layer — new work by the Analyzer
  inferences: Inference[]

  // Findings that didn't yield inferences — every finding is accounted for
  unused_findings: UnusedFinding[]

  // Passed through from ResearchOutput — unchanged
  evidence_gaps: EvidenceGap[]   // reuse from ResearchOutput

  // Overall signal
  quality_score: 'low' | 'medium' | 'high'
  quality_threshold_met: boolean
}

interface AnalysisFinding {
  id: string                    // "F1", "F2", "F3"...
  claim: string                 // sourced from ResearchOutput.Finding.claim — not modified
  source_url: string
  source_tier: 'primary' | 'secondary' | 'tertiary'
  confidence: 'high' | 'medium' | 'low'
  is_direct_quote: boolean
}

interface Inference {
  claim: string                 // the conclusion — specific and falsifiable
  type: 'pattern' | 'causal' | 'evaluative' | 'predictive'
  confidence: 'high' | 'medium' | 'low'
  traces_to: string[]           // finding IDs: ["F3", "F7", "F12"]
}

interface UnusedFinding {
  finding_id: string            // "F5"
  reason: 'contradicted' | 'insufficient_evidence' | 'out_of_scope'
  detail: string                // one sentence explaining why
}
```

---

## WriterOutput

The canonical output of the Writer pipeline (Writer → Writer-Formatter). The Writer
produces audience-calibrated prose; the Writer-Formatter normalizes it into this schema.
Downstream consumers depend on formatter output, not raw writer output.

```typescript
interface WriterOutput {
  // Parse metadata — first line of output
  claims_count: number
  input_type: 'researcher-output' | 'analyst-output' | 'analysis-output' | 'story-output' | 'raw-notes'
  output_format: 'report' | 'brief' | 'proposal' | 'exec-summary' | 'email' | 'memo'
  audience: string

  // Source claims extracted from input material — numbered S1, S2...
  claims: WriterClaim[]

  // The document body — audience-calibrated prose with per-section source attribution
  document: string

  // Claims flagged for verification — specific numbers, percentages, named statistics
  claims_to_verify: ClaimToVerify[]

  // Production metadata
  metadata: WriterMetadata

  // Every source claim accounted for — used or not used
  citations: WriterCitation[]
}

interface WriterClaim {
  id: string                     // "S1", "S2", "S3"...
  claim: string                  // The discrete factual claim from source material
  confidence: 'high' | 'medium' | 'low' | 'unrated' | 'inference'
  source_url: string | null      // From upstream Finding's source field
  traces_to: string[] | null     // For inference claims only — e.g. ["F3", "F7"]
}

interface ClaimToVerify {
  claim_id: string               // "S4"
  quote: string                  // The specific value — "$37.5M Series A"
  type: 'specific_number' | 'percentage' | 'named_statistic' | 'specific_measurement'
}

interface WriterMetadata {
  specialist: 'writer'
  version: string
  input_type: string
  output_format: string
  audience: string
  voice: string
  word_count: number
  coverage: 'full' | 'partial'
  coverage_gaps: string[]        // empty array if full coverage
  confidence_distribution: {
    high: number
    medium: number
    low: number
    unrated: number
    inference: number
  }
}

interface WriterCitation {
  claim_id: string               // "S1"
  claim: string                  // Brief quote of the claim
  used_in: string | null         // Section name, or null if not used
  confidence: 'high' | 'medium' | 'low' | 'unrated' | 'inference'
  confidence_numeric: number | null  // 0.9 | 0.6 | 0.3 | null
  source_url: string | null      // Carried from upstream
  type: 'inference' | null       // Only present on inference claims
  traces_to: string[] | null     // Only present on inference claims
}
```

---

## StoryOutput

The canonical output of the Storyteller specialist.

```typescript
interface StoryOutput {
  // What was narrated
  input_type: string
  audience: string
  tone: 'dramatic' | 'trustworthy' | 'creative' | 'persuasive'
  framework: 'scqa' | 'three-act' | 'story-spine' | 'sparkline' | 'kishotenketsu'

  // Narrative structure decisions
  narrative_selection: NarrativeSelection

  // The finished story
  story: string

  // Overall signal
  quality_threshold_met: boolean
}

interface NarrativeSelection {
  dramatic_question: string
  protagonist: string
  framework: string
  framework_rationale: string
  included_findings: IncludedFinding[]
  omitted_findings: OmittedFinding[]
}

interface IncludedFinding {
  finding_id: string
  description: string
  role: string
}

interface OmittedFinding {
  finding_id: string
  description: string
  reason: string
}
```

---

## PrioritizerOutput

The canonical output of the Prioritizer specialist.

```typescript
interface PrioritizerOutput {
  // What was prioritized
  goal: string                        // The situation or goal driving prioritization
  framework: 'moscow' | 'impact-effort' | 'rice' | 'weighted-scoring'
  framework_rationale: string         // Why this framework was selected
  items_received: number
  items_ranked: number
  items_unrankable: number

  // The ranked output — one entry per item, in priority order
  rankings: RankedItem[]

  // Items that couldn't be meaningfully ranked
  unrankable_items: UnrankableItem[]

  // Overall signal
  quality_threshold_met: boolean
}

interface RankedItem {
  rank: number
  item: string                        // The item exactly as received — not reworded
  priority: 'must' | 'should' | 'could' | 'wont'   // MoSCoW mapping for all frameworks
  score: number | string | null       // Framework score (null for MoSCoW which is categorical)
  framework_scores: Record<string, number | string>  // Dimension breakdown (e.g. {impact: 4, effort: 2, score: 2.0})
  rationale: string                   // 2–3 sentences citing specific context
  dependencies: string[]              // Items this must follow or that follow it
}

interface UnrankableItem {
  item: string
  reason: 'insufficient_context' | 'out_of_scope' | 'duplicate' | 'not_actionable'
  detail: string                      // One sentence explaining why
}
```

---

## Schema Version

`v1.3` — updated 2026-03-13. Added WriterOutput interface (the most-consumed specialist now has a typed contract). Previous: v1.2 (2026-03-09).
