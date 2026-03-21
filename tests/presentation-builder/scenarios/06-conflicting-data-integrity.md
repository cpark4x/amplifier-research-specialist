# Scenario 06: Conflicting Data Integrity — Contradictory Source Material

## Parameters

- **audience**: Senior Leadership Team
- **audience_type**: executive
- **purpose**: decide
- **tone**: analytical
- **output_format**: presentation
- **theme**: _(not specified)_
- **presentation_mode**: slide
- **include_speaker_notes**: true
- **include_appendix**: false
- **framework**: SCQA → Pyramid

## Expected Behavior

The source material contains deliberately contradictory data points across multiple dimensions (market size, growth rates, CAC, competitor share, revenue projections). A well-behaved presentation builder should **acknowledge discrepancies explicitly** — using ranges, qualifiers, or callout slides — rather than silently selecting one number and presenting it as fact. This tests D3 (Content Fidelity) under ambiguity: the model must not resolve contradictions by picking a side without disclosure.

## Source Material

The following is a compiled research package from multiple internal and external sources. It has not been reconciled or deduplicated. Treat as raw researcher output.

---

### Internal Strategy Group — APAC Market Sizing (Draft, February 2026)

The Asia-Pacific region represents a growing opportunity for enterprise workflow automation. Based on our bottom-up analysis of 14 national markets (Australia, Japan, South Korea, India, Singapore, Indonesia, Thailand, Vietnam, Philippines, Malaysia, Taiwan, Hong Kong, New Zealand, and Bangladesh), we estimate a total addressable market (TAM) of **$2.1 billion** for 2026. This figure is derived from enterprise IT spending data published by national statistics bureaus, filtered to the workflow automation and process orchestration segments, and adjusted for purchasing power parity.

The serviceable addressable market (SAM) is approximately $680 million, reflecting our current product capabilities and language support (English, Japanese, Korean). We project a **12% compound annual growth rate (CAGR)** for the broader APAC workflow automation segment through 2030, driven primarily by digital transformation initiatives in Japan and Australia, which together account for 58% of the regional TAM.

Customer acquisition in APAC has historically been more expensive than in North America due to fragmented channel partnerships and longer enterprise sales cycles. Our pilot program in Australia (Q3–Q4 2025) yielded a **customer acquisition cost (CAC) of $340 per account**, roughly 1.7x our North American average of $200. The pilot engaged 23 mid-market prospects through a combination of direct outreach and partner referrals, closing 8 accounts with an average contract value (ACV) of $42,000.

Competitive intensity in the region varies by sub-market. In Japan and Australia, **Competitor X (WorkflowPro)** holds an estimated **34% market share** based on publicly reported revenue and our channel intelligence. Competitor Y (AutomateSuite) holds approximately 19%, with the remainder fragmented across regional vendors and in-house solutions.

### Gartner Excerpt — Workflow Automation Market Forecast (Published January 2026)

The global workflow automation market is projected to reach $18.7 billion by 2028. The Asia-Pacific segment is the fastest-growing region, with an estimated TAM of **$4.8 billion in 2026** and a projected **23% CAGR** through 2030. This top-down estimate includes adjacent categories such as intelligent document processing (IDP), robotic process automation (RPA) applied to workflow contexts, and low-code/no-code orchestration platforms.

Growth is fueled by rapid cloud adoption in Southeast Asia and India, where enterprise SaaS penetration remains below 30% but is accelerating. Japan and South Korea continue to represent the largest absolute spend, but India and Indonesia are expected to surpass Australia in total segment spend by 2028.

Note: Gartner's market definition includes RPA-adjacent workflow tools, which our internal analysis excludes. The definitional difference likely accounts for a significant portion of the TAM discrepancy, though the exact delta has not been quantified.

### Finance Team — International Expansion Unit Economics (Q4 2025 Review)

Summary of unit economics across international expansion markets for FY2025:

| Region | Accounts Acquired | Avg CAC | Avg ACV | LTV:CAC | Payback (months) |
|---|---|---|---|---|---|
| EMEA | 112 | $285 | $51,000 | 4.2:1 | 9.1 |
| APAC (pilot) | 8 | $340 | $42,000 | 3.1:1 | 11.4 |
| LATAM | 14 | $195 | $28,000 | 3.8:1 | 8.7 |

The APAC pilot is early-stage with a small sample size. CAC is expected to improve with scale, though the magnitude of improvement is uncertain.

### BD Team — International Market Benchmarking Memo (March 2026)

Our international expansion to date shows strong unit economics. Across all active international markets (EMEA, APAC, LATAM), the **average customer acquisition cost is $180**, reflecting efficiency gains from centralized demand generation and shared SDR infrastructure. APAC-specific figures are directionally consistent with the global average; early elevated costs in the pilot phase have moderated as channel partnerships in Australia and Singapore have matured.

We recommend using the $180 blended CAC for planning purposes when modeling APAC expansion scenarios, as it better reflects steady-state operations than pilot-phase figures.

### Competitive Intelligence Update — Q1 2026

The competitive landscape in APAC workflow automation is evolving rapidly. Several developments worth noting:

- **AutomateSuite** raised a $120M Series D in December 2025, with stated plans to triple their APAC go-to-market team by end of 2026.
- **Competitor X (WorkflowPro)** continues to grow but has faced headwinds. Recent customer interviews and win/loss analysis suggest their **estimated market share in APAC is 18–22%**, lower than previously believed. Earlier estimates may have overstated their position due to double-counting of partner-resold licenses. Their strength remains concentrated in Japan; outside Japan, their share drops to approximately 10–12%.
- Regional players (notably KaizenFlow in Japan and SmartOps in India) are gaining traction in the mid-market segment.

### Revenue Planning — APAC Expansion Scenario Model (Draft)

Below is our base-case revenue projection for APAC, assuming market entry in Q3 2026:

| Year | New Accounts | ACV | New ARR | Cumulative ARR |
|---|---|---|---|---|
| 2026 (H2) | 15 | $45,000 | $675K | $675K |
| 2027 | 60 | $48,000 | $2.88M | $3.56M |
| 2028 | 140 | $52,000 | $7.28M | $10.84M |
| 2029 | 280 | $55,000 | $15.4M | $26.24M |
| 2030 | 450 | $58,000 | $26.1M | $52.34M |

This model assumes a **35% year-over-year growth** in new account acquisition after the initial ramp, and a 3–5% annual ACV uplift from pricing and upsell. Note: the account acquisition growth rate in this model implies a faster market penetration trajectory than either the 12% or 23% market CAGR figures would suggest, based on our assumed starting market share of <1%. The finance team has flagged this discrepancy but the growth assumptions reflect management's view of our competitive differentiation and go-to-market investment.

Net revenue retention is assumed at 115%, consistent with our North American cohort performance, though this has not been validated for APAC customers.

---

CITATIONS
S1: "TAM of $2.1 billion for 2026" → Internal Strategy Group bottom-up analysis | confidence: medium (0.74)
S2: "TAM of $4.8 billion in 2026" → Gartner Workflow Automation Market Forecast, Jan 2026 | confidence: medium (0.79)
S3: "12% CAGR through 2030" → Internal Strategy Group | confidence: medium (0.72)
S4: "23% CAGR through 2030" → Gartner (includes adjacent categories) | confidence: medium (0.76)
S5: "CAC of $340 per account" → APAC pilot program data, n=8 | confidence: low (0.61) — small sample
S6: "average customer acquisition cost is $180" → BD Team blended international average | confidence: medium (0.70) — blended across regions
S7: "Competitor X holds an estimated 34% market share" → Internal channel intelligence, pre-Q1 2026 | confidence: medium (0.65)
S8: "estimated market share in APAC is 18–22%" → Updated win/loss analysis, Q1 2026 | confidence: medium (0.71) — corrects earlier overcount
S9: "35% year-over-year growth in new account acquisition" → Management assumption, not derived from market CAGR | confidence: low (0.55) — flagged internally
S10: "Net revenue retention assumed at 115%" → North American cohort proxy, unvalidated for APAC | confidence: low (0.50)
