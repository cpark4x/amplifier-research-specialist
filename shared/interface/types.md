# Shared Interface Types

These types are the stable contracts that all specialists follow. They do not change when specialist implementations evolve. Orchestrators and downstream specialists depend on them.

---

## ResearchOutput

The canonical output of the Researcher specialist.

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

## Schema Version

`v1.0` — established 2026-02-26. Changes require version bump and coordinated update to all callers.
