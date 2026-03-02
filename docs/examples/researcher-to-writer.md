# Example: Researcher → Writer Chain

This walkthrough shows the full researcher → writer pipeline using a realistic knowledge work scenario: preparing an executive brief on remote work productivity challenges.

---

## The Task

**Goal:** Produce a 1-page executive brief for an HR leadership team on the key productivity challenges facing remote-first organizations in 2025.

**Why this chain?** Research first (to get sourced, confident evidence), then write (to transform that evidence into a format-faithful document without fabricating claims).

---

## Step 1: Call the Researcher

```python
research = delegate(
    agent="specialists:specialists/researcher",
    instruction="""
    Research the key productivity challenges facing remote-first organizations in 2025.
    Focus on: communication overhead, async coordination, focus/deep work, and onboarding.
    Return structured findings with source tiering and confidence levels.
    quality_threshold: high
    query_type: market
    """
)
```

### Sample ResearchOutput (abbreviated)

```
RESEARCH BRIEF
━━━━━━━━━━━━━━
Question: Key productivity challenges for remote-first orgs in 2025
Quality threshold: high | Quality score: 0.84

Key findings (high confidence):
• Meeting overload is the #1 reported challenge — avg 4.2hrs/day in meetings for remote knowledge workers [S1]
• Async coordination failures cost ~2hrs/day in context-switching for distributed teams [S2]
• New hire time-to-productivity is 40% longer in fully remote settings vs. hybrid [S3]

Evidence gaps:
• Industry-specific data (tech vs. finance vs. healthcare) — insufficient sources found
• Post-2024 longitudinal data on hybrid vs. fully remote productivity — paywall blocked

FINDINGS
━━━━━━━━
Finding 1:
  Claim: Remote knowledge workers average 4.2 hours per day in meetings
  Source: https://www.microsoft.com/en-us/worklab/work-trend-index-2024
  Source tier: Primary (direct research publication)
  Confidence: High
  Corroboration: 3 independent sources

Finding 2:
  Claim: Async coordination failures cause ~2 hours/day of context-switching overhead
  Source: https://hbr.org/2024/remote-work-coordination-costs
  Source tier: Secondary (credible third-party reporting)
  Confidence: Medium
  Corroboration: 1 independent source

Finding 3:
  Claim: New hire time-to-productivity is 40% longer in fully remote settings
  Source: https://www.gallup.com/workplace/remote-onboarding-2024
  Source tier: Primary (Gallup research)
  Confidence: High
  Corroboration: 2 independent sources

EVIDENCE GAPS
━━━━━━━━━━━━━
Gap 1: Industry-specific breakdown (tech/finance/healthcare)
  Fallbacks attempted: Google search, Archive.org, author summary search
  Reason: No primary research found with industry-level segmentation

QUALITY THRESHOLD RESULT: MET
```

---

## Step 2: Call the Writer

```python
document = delegate(
    agent="specialists:specialists/writer",
    instruction=f"""
    Write an executive brief for HR leadership.
    Format: executive-summary
    Audience: HR VPs and CHROs at mid-size tech companies
    Voice: professional, data-forward, actionable
    Length: 400-500 words

    Source material:
    {research.response}
    """
)
```

### Sample Writer Output

```
WRITER METADATA
━━━━━━━━━━━━━━━
Input type: ResearchOutput
Output format: executive-summary
Audience: HR VPs and CHROs, mid-size tech
Voice: professional, data-forward, actionable
Word count: 412
Coverage: partial
Coverage gaps:
  - Industry-specific data unavailable in source material
  - Post-2024 longitudinal comparisons not available

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REMOTE-FIRST PRODUCTIVITY: EXECUTIVE BRIEF

Remote-first organizations face three compounding productivity challenges that
HR leadership must address to maintain competitive workforce performance in 2025.

**The Meeting Trap**
Remote knowledge workers now average 4.2 hours per day in meetings — a figure
that has grown 40% since 2020 [S1]. Unlike in-person organizations where physical
proximity enables quick hallway conversations, remote teams default to scheduled
calls for every coordination need, regardless of urgency or complexity. The result
is a calendar-first culture that fragments deep work time and drives burnout.

**Async Coordination Overhead**
When meetings aren't the answer, distributed teams face a different problem: async
coordination failures. Context-switching between communication tools, waiting for
responses across time zones, and reconstructing decision history costs the average
remote knowledge worker approximately two hours per day [S2]. This overhead is
largely invisible in productivity reporting but shows up clearly in employee
satisfaction scores and throughput per contributor.

**The Onboarding Gap**
New hire time-to-productivity is 40% longer in fully remote settings compared to
hybrid environments [S3]. Without ambient learning — the informal conversations,
observed behaviors, and incidental context of shared spaces — new employees take
significantly longer to build the network and institutional knowledge needed to
work independently. This gap is especially acute in the first 90 days.

**Implications for HR Leadership**
These three challenges are structural, not behavioral. Meeting overload won't be
solved by asking managers to schedule fewer calls; it requires redesigning
coordination norms. Async overhead requires tooling and protocol investment, not
time management training. The onboarding gap requires a formal remote-first
onboarding program, not a longer version of the in-person playbook.

Note: Industry-specific data (tech vs. finance vs. healthcare) was not available
in the research. The figures above represent cross-industry averages and should
be validated against your sector benchmarks before use in strategic planning.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CITATIONS
━━━━━━━━━
[S1] "Remote knowledge workers average 4.2 hours per day in meetings"
     → Source: Microsoft Work Trend Index 2024 (Primary, High confidence)
     → Used in: The Meeting Trap, paragraph 1

[S2] "Context-switching costs ~2 hours per day for remote knowledge workers"
     → Source: Harvard Business Review, Remote Work Coordination Costs (Secondary, Medium confidence)
     → Used in: Async Coordination Overhead, paragraph 1

[S3] "New hire time-to-productivity is 40% longer in fully remote settings"
     → Source: Gallup Workplace Report 2024 (Primary, High confidence)
     → Used in: The Onboarding Gap, paragraph 1
```

---

## What to Notice

**Researcher output:**
- Every finding has a source URL, tier, and confidence level
- Evidence gaps are explicit — not hidden inside confident-sounding prose
- The RESEARCH BRIEF section gives a fast machine-parseable summary at the top

**Writer output:**
- Starts with `WRITER METADATA` — machine-readable block for downstream processing
- Coverage gaps are surfaced in metadata before the document, not buried in a footnote
- Every factual sentence has an inline `[Sn]` marker
- `CITATIONS` at the end maps every marker back to its source and location in the document
- The coverage gap (no industry-specific data) appears as a note in the document — the writer didn't fabricate the missing data

---

## Common Variations

**Research only (no writing needed):**
```python
delegate(agent="specialists:specialists/researcher", instruction="Research X")
```

**Write from existing notes (no researcher needed):**
```python
delegate(
    agent="specialists:specialists/writer",
    instruction="Write a report brief from these notes: [your notes here]"
)
```

**Different output formats:**
```
format: report          # Long-form, sectioned document
format: brief           # Short, high-signal summary
format: email           # Direct, actionable, recipient-focused
format: memo            # Internal, context-rich
format: proposal        # Structured argument with ask
format: executive-summary  # Leadership-facing, data-forward
```
