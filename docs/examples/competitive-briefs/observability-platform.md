# Observability Platform Decision Brief

**For: VP Engineering / Head of Platform Engineering**
**Decision deadline: Prior to next contract renewal or infrastructure scale event**

---

## Bottom Line Up Front

Three credible options. One clear winner per scenario. The decision hinges on three variables: security requirements, power-user headcount, and existing toolchain.

---

## The Stakes

At 100 hosts with full observability, platform cost ranges from **$51K to $115K/year** — a $64K spread for equivalent coverage. Vendor choice is also a 3–5 year architectural commitment. Choose wrong on pricing model and a single autoscaling event or cardinality spike can double your bill with no warning.

---

## Candidate Summary

| | Datadog | New Relic | Grafana Cloud |
|---|---|---|---|
| **Annual cost (100-host scenario)** | $115K | $71K | $51K |
| **Pricing model** | Per-host + 50+ SKUs | Per-GB + per-user | Per-unit + per-seat |
| **Alerting intelligence** | Strong (Watchdog) | Best-in-class (Applied Intelligence) | Solid, no ML |
| **Security signals** | Full stack (CSPM, SIEM, ASM) | None | None |
| **Lock-in risk** | High | Medium | Low (OTel-native) |

---

## The Decision

**Answer these three questions in order.**

**1. Do you need integrated security observability (CSPM, SIEM, runtime threat detection)?**
→ **Datadog.** No other platform competes here. The cost premium buys a unified security + observability layer. If this is a requirement, stop here.

**2. How many full-platform (power) users do you have or expect within 24 months?**
→ **Fewer than 20:** New Relic wins on value. Per-GB ingestion economics outperform at this seat count, and Pixie's zero-instrumentation Kubernetes coverage reduces onboarding friction significantly.
→ **20–30:** Model both. New Relic's per-user cliff means adding one team can reset pricing for everyone.
→ **More than 30:** Grafana Cloud wins on seat economics — $8–20/user versus $349/user (New Relic) makes the math unambiguous at scale.

**3. Is your team already running Prometheus / PromQL?**
→ **Yes:** Grafana Cloud. Zero migration friction, OTel-native, 56% cheaper than Datadog for equivalent coverage.

---

## Critical Risks — Know Before You Sign

**Datadog:** Custom metrics are a cost time bomb. High-cardinality tags (e.g., per-request IDs, feature flags) can multiply custom metrics spend **100×** without a hard limit. Require contractual cost caps or cardinality guardrails before signing.

**New Relic:** Francisco Partners/TPG acquired the company in 2023. Private equity ownership introduces product velocity risk on multi-year commitments. Appropriate for 1-year deals; pressure-test roadmap commitments for anything longer.

**Grafana Cloud:** No security story whatsoever. If compliance or threat detection is in scope — now or within 18 months — budget a separate SIEM purchase ($50–150K/year). Factor this into total cost of ownership before declaring Grafana the cheapest option.

---

## Recommended Path by Archetype

| Your situation | Recommended platform |
|---|---|
| Security-regulated environment (fintech, healthcare, defense) | **Datadog** |
| High-growth startup, small platform team, K8s-heavy | **New Relic** |
| Large engineering org, OSS-aligned, Prometheus today | **Grafana Cloud** |
| Cost-sensitive, no security requirement, 30+ users | **Grafana Cloud** |

---

## What to Do This Week

1. **Run the user count model.** New Relic's user cliff is the most common mis-buy. Map current and 12-month projected full-platform users before evaluating pricing.
2. **Audit custom metrics exposure (Datadog evaluations only).** Ask your team to inventory high-cardinality tag usage before accepting any Datadog quote.
3. **Require a 30-day POC with production traffic.** Alert quality and ingestion costs only reveal themselves under real load. All three vendors offer this.

---

*Weighted scores (cost-adjusted): New Relic 7.5 · Grafana Cloud 7.0 · Datadog 6.0*
