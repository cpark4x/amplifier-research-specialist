# Decision Brief: Project Management Tool Selection

**For:** VP Engineering / Head of Product
**Team size:** 20–100 engineers
**Decision:** Linear vs. Jira vs. Shortcut

---

## Bottom Line Up Front

**Choose Linear.** For product-led software teams under 80 engineers, it delivers the best return on the only metric that matters at your scale: whether your team actually uses it.

---

## The Core Trade-off

Every team at your size faces the same trap — buying configurability you'll never fully deploy, at the cost of adoption you can't recover.

Jira is the category leader in flexibility. It is also the category leader in friction. Slow loads, JQL queries, notification fatigue, and months of configuration overhead create a system that EMs customize and ICs ignore. **A Jira instance nobody updates is a liability, not an asset.**

Linear inverts this. It's opinionated by design — sub-100ms UI, keyboard-first navigation, automatic status updates from GitHub/GitLab merge events. Developers use it without being asked to. That behavioral change compounds.

---

## Scoring Summary

| | Linear | Shortcut | Jira |
|---|---|---|---|
| **Weighted Score** | **7.1** | 6.8 | 6.3 |
| Developer Experience | ★★★★★ | ★★★★ | ★★ |
| Workflow Flexibility | ★★★ | ★★★★ | ★★★★★ |
| Reporting Depth | ★★★ | ★★ | ★★★★★ |
| **Monthly Cost (50 users)** | **~$400** | Mid | **~$1,100** |

---

## Financial Signal

Linear Business vs. Jira Premium + Confluence at 50 users: **$700/month delta** — $8,400/year that funds roughly half an engineering sprint. The reporting depth Jira provides at that premium is primarily consumed by EMs and Directors; individual contributors rarely touch it.

---

## Decision Rules

**Go with Linear if:**
- Your team is under 80 engineers
- Engineering velocity is your primary operating metric
- You want shipping momentum, not process compliance infrastructure

**Go with Jira if:**
- You're crossing 80+ engineers with cross-team dependency complexity
- You have compliance or audit requirements tied to workflow state
- You're already deep in the Atlassian ecosystem (Confluence, Bitbucket)

**Consider Shortcut if:**
- You have a significant non-technical stakeholder presence that needs softer onboarding
- Budget is constrained and you need 80% of Linear's UX at a lower commitment

---

## Recommendation

Linear. Lock in strong adoption habits while your team is still small enough for culture to move fast. If you scale past 80 engineers with cross-org coordination needs, you'll have the leverage to negotiate an enterprise transition — and the operational maturity to use Jira well.

> *At 20–100 people, adoption beats configurability. Every time.*
