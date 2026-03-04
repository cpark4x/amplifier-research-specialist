# Backend-as-a-Service: Platform Decision Brief

**Audience:** CTO / Engineering Lead
**Decision:** BaaS platform selection for new product
**Date:** Q1 2026

---

## Recommendation

**Default to Supabase. Qualify against Neon or Firebase only if your workload has a specific edge case.**

Supabase scored 18/20 across evaluation criteria — the highest by a significant margin. It delivers full PostgreSQL compatibility, a credible self-hosting path, and the broadest capability surface at predictable cost. For most new products, it eliminates the need to choose between developer experience and production readiness.

---

## The Short List

| Platform | Score | Starting Cost | Best For | Disqualifier |
|---|---|---|---|---|
| **Supabase** | 18/20 | $25/mo (Pro) | All-in-one greenfield | Free tier pauses after 7 days idle |
| **Neon** | 14/20 | $0–$19/mo | Postgres teams, CI branching, bursty traffic | No native real-time; cold starts on free tier |
| **Firebase** | 10/20 | Variable (no cap) | Mobile-first, sub-100ms sync | No SQL, no spend guardrails, no self-hosting |
| **PlanetScale** | 11/20 | $39/mo minimum | Hyperscale MySQL sharding | No free tier; HA storage billed 3× per replica |

---

## Decision Factors by Priority

**1. Data model**
If your team thinks in SQL and schemas, eliminate Firebase immediately. Supabase and Neon are both 100% native Postgres. PlanetScale is MySQL with a Postgres beta that is not production-ready.

**2. Real-time requirements**
Firebase is the only platform with purpose-built real-time sync: sub-100ms, offline-first, with conflict resolution. If you are building a collaborative or mobile-first product where sync latency and offline behavior are core UX requirements, Firebase is the correct choice — accept the NoSQL constraint and the billing exposure. Supabase offers real-time via WAL CDC (100–500ms, no delivery guarantees), which is sufficient for most use cases.

**3. Cost structure and risk**
- **Neon** is the only true pay-per-use platform with scale-to-zero. Idle compute costs nothing.
- **Supabase** Pro ($25/mo) is predictable and well-scoped for early-stage products.
- **Firebase** Blaze plan carries real billing risk — there is no automatic spend cap.
- **PlanetScale** HA deployments bill storage per replica × 3. Confirm your storage model before signing.

**4. Vendor lock-in exposure**
Supabase is Apache 2.0 and ships Docker Compose-ready. Firebase cannot be self-hosted and its data model creates high migration friction.

---

## Guidance by Scenario

| Scenario | Platform |
|---|---|
| New product, fastest time to production | **Supabase** |
| Mobile app with real-time collaboration or offline-first UX | **Firebase** |
| Postgres-native team, branching per PR, variable load | **Neon** |
| Known hyperscale MySQL workload with sharding requirements | **PlanetScale** |
| Regulatory, on-prem, or vendor-lock-in constraint | **Supabase** (self-hosted) |

---

## Risks to Flag Before Committing

- **Supabase** — Disable free-tier project auto-pause in production; it is on by default.
- **Firebase** — Set a billing budget alert on day one. The Blaze plan has no hard cutoff.
- **Neon** — Cold start latency (500ms–several seconds) on the free tier is disqualifying for latency-sensitive endpoints.
- **PlanetScale** — Model your storage cost at 3× to account for HA replica billing.

---

## Bottom Line

Supabase is the high-confidence default. It covers the broadest set of requirements, avoids lock-in, and carries no billing surprises. Deviate toward Neon if your team is Postgres-native and traffic is unpredictable. Deviate toward Firebase only if real-time sync is a first-class product requirement and you can accept the NoSQL data model.
