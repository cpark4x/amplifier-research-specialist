# Scenario 07: Startup Pitch — AI Code Review Platform (Series A)

## Parameters

- **audience**: Venture capital partners evaluating a Series A investment
- **audience_type**: external
- **purpose**: persuade
- **tone**: conversational
- **output_format**: html
- **theme**: dark-keynote
- **presentation_mode**: slides
- **include_speaker_notes**: true
- **include_appendix**: true

## Expected Framework

5-Element Narrative (change -> winners/losers -> promised land -> magic gifts -> proof)

## Source Material

These are raw notes from the founder preparing for a Series A pitch. No specialist pipeline was used — this is direct input from the user.

---

We built Codex AI — an AI code review tool. Launched 8 months ago.

The problem: code reviews are the biggest bottleneck in engineering teams. Average PR waits 24 hours for review. Senior devs spend 30% of their time reviewing other people's code instead of building. I've talked to probably 60 engineering leaders in the last year and every single one says the same thing — they know reviews are slow, they know it hurts velocity, but they don't know how to fix it without hiring more seniors, and there aren't enough seniors to hire.

What we do: AI reviews PRs in under 2 minutes. Catches bugs, style issues, security vulnerabilities, performance anti-patterns. Not replacing human review — augmenting it. The human reviewer gets a pre-annotated PR with the AI's findings so they can focus on architecture and design decisions instead of nitpicking variable names and missing null checks. We call it "the boring parts, automated."

How it works technically (keep this brief, VCs don't need the deep dive): we fine-tuned models on 2.3 million code reviews from open source repos. We index the customer's entire codebase so reviews are context-aware — it knows your patterns, your abstractions, your style. It's not just generic linting. It understands intent.

Traction (these numbers are as of last week):
- 340 teams using it, up from 40 eight months ago
- $85k MRR, growing ~18% month over month
- Been over 15% MoM growth every month for the last 6 months
- 94% of users say it saves them at least 3 hours per week per developer
- NPS is 72
- Monthly retention: 96%
- Net revenue retention: 138% (teams expand to more repos/seats)

Biggest customer is a Fortune 500 fintech company (can't name them yet, NDA). They have 200 developers using it and they expanded from a 20-person pilot in 8 weeks. Their VP of Engineering told me it "changed how their team thinks about code quality."

We have 3 other customers over $5k MRR and a pipeline of 12 companies in active trials right now. Average trial-to-paid conversion is 67%.

Market: Developer tools market is huge, $45B+. Code review specifically is underserved — most tools are linting/static analysis, not actual review intelligence. We think the TAM for AI code review is $3-5B based on number of professional developers (28M worldwide) times willingness to pay ($10-25/developer/month based on our pricing experiments).

Competition: GitHub Copilot does code generation, not review — they're complementary, not competitive. Actually, 78% of our users also use Copilot. CodeRabbit is the closest competitor but they're focused on open source and their reviews are surface-level — they don't index the codebase for context. Snyk is security-only, not full-spectrum review. Linear and the other dev tools are workflow, not code intelligence. We're the only ones doing full-spectrum, context-aware review intelligence.

Team: 3 cofounders, 11 people total.
- CTO (Jamie Chen) was tech lead at GitHub on Copilot for 4 years. She led the team that built the original Copilot suggestion engine. She knows code intelligence at scale better than almost anyone.
- CEO (me, Marcus Webb) ran product at Stripe for developer tools for 3 years. Before that, engineering manager at Datadog. I know the developer tools buyer and the enterprise sales motion.
- Chief Scientist (Dr. Priya Sharma) has a PhD from Stanford in program analysis, 12 published papers on code understanding and automated program repair. She's the technical moat.
- Rest of the team: 4 ML engineers, 2 backend, 1 design, 1 DevRel

The moat: our fine-tuned models get better with every review. Customers who've been on the platform for 6+ months see 23% better accuracy than new customers because the model has learned their patterns. Switching costs increase over time — this is a flywheel, not a feature.

Raising $8M Series A. Using it for:
- Hiring 6 more ML engineers to accelerate model quality ($3.2M over 18 months)
- Building enterprise sales team — 2 AEs, 1 SE, 1 sales leader ($1.8M)
- SOC 2 Type II certification — we have 3 enterprise deals worth ~$180k combined ARR waiting on this ($400K for audit + engineering work)
- Infrastructure scaling — we're on AWS and our inference costs are $0.12 per review right now, need to get that under $0.05 ($600K)
- Runway buffer for 18 months to Series B ($2M)

Unit economics:
- Current blended CAC: $1,800 per team (mostly product-led, very little paid acquisition so far)
- Average contract value: $3,600/year (30 seats × $10/seat/month)
- LTV assuming 96% retention and 138% NRR: ~$24,000
- LTV:CAC ratio: 13:1
- Payback period: 6 months
- Gross margin: 71% (inference costs are the main COGS)

Some things I want to make sure we emphasize:
- The "before/after" of a code review with and without Codex — make this visceral
- Retention and NRR numbers — these are best-in-class for our stage
- The speed metric: 2 minutes AI review vs 24 hour average human review wait time
- Jamie's background on Copilot — this is a huge credibility signal for VCs
- The flywheel: more reviews → better model → higher accuracy → more value → more usage