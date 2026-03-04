# CI/CD Platform Decision Brief

**To:** Engineering Manager
**Re:** CI/CD Platform Selection — 50-Person Team
**Date:** March 2026

---

## Bottom Line Up Front

**Adopt GitHub Actions.** It delivers the lowest total cost, fastest time-to-productivity, and strongest ecosystem fit for a GitHub-native team at your scale. No dedicated ops overhead. No procurement complexity.

---

## The Decision

| Platform | Score | Monthly Cost | Setup Burden | Verdict |
|---|---|---|---|---|
| **GitHub Actions** | 9.0 | ~$200 + compute | Hours | ✅ **Recommended** |
| CircleCI | 7.75 | ~$750 | Days | Conditional |
| Jenkins | 6.0 | "Free" + 0.5 FTE | Weeks | ❌ Do not pursue |

---

## Why GitHub Actions Wins

**Cost.** At $200/month base — plus optional self-hosted runners at near-zero marginal cost — GitHub Actions runs roughly **$6,600/year cheaper** than CircleCI. Jenkins' "free" price tag conceals 0.25–0.5 FTE in maintenance labor, which at market rates likely exceeds CircleCI's sticker price.

**Time to value.** 20,000+ pre-built marketplace actions. No separate service to procure, configure, or secure. Your team ships pipelines in hours, not sprint cycles.

**No new operational surface.** Jenkins at 50 engineers requires a dedicated DevOps resource to keep it healthy. That is a headcount decision disguised as a tooling decision. Reject it on those grounds alone.

---

## When to Choose Differently

| If your team... | Consider instead |
|---|---|
| Runs a large monorepo with complex test sharding, or does heavy macOS/iOS builds | **CircleCI** — superior native test splitting and Apple silicon support justify the premium |
| Operates in an air-gapped environment or has deep existing Jenkins automation | **Jenkins** — compliance requirements or sunk switching costs may override the calculus |
| Spans multiple VCS providers (GitLab, Bitbucket) | **CircleCI** — its VCS-agnostic model is a genuine architectural advantage |

---

## Risk Register

| Risk | Likelihood | Mitigation |
|---|---|---|
| GitHub compute costs spike at scale | Low–Medium | Migrate hot runners to self-hosted; cost remains controllable |
| GitHub platform outage blocks CI | Low | Acceptable; industry-standard risk shared by all SaaS CI tools |
| Workflow lock-in | Medium | Actions YAML is portable enough; not a blocking concern at this stage |

---

## Recommended Next Step

Run a **two-week pilot**: migrate one active service's pipeline to GitHub Actions. Measure setup time, build reliability, and developer friction. If the pilot clears baseline, proceed with full rollout.

**No further analysis required.** The data supports a decision now.
