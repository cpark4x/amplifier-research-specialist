# Database Selection Brief

**Decision: Primary Database for SaaS — 2025**
*For: CTO / Founding Engineer*

---

## Decision

**Use PostgreSQL.** Pair it with Redis for caching and sessions. Do not use MongoDB unless you have a documented, domain-specific reason.

---

## Rationale

**PostgreSQL is purpose-built for SaaS data topology.** The canonical SaaS schema — organizations, users, subscriptions, audit logs — is relational. PostgreSQL handles it natively with full ACID compliance, JOINs, Row-Level Security for multi-tenancy, and `jsonb` for any document flexibility you need.

**MongoDB's primary advantage is gone.** The argument for MongoDB was document-native flexibility. PostgreSQL's `jsonb` column type closes that gap. Most SaaS data is fundamentally relational — MongoDB creates friction against your own schema rather than enabling it.

**The operational gap has closed.** In 2025, Supabase ($25/mo) and Neon ($19/mo) make managed PostgreSQL trivial to operate. MongoDB Atlas starts at $57/mo with faster platform lock-in and a materially smaller talent pool.

**Redis is additive, not competitive.** Redis is a data structure server. It is the right tool for session storage, rate limiting, caching, and queues. It is not a primary database. Upstash makes it nearly free to start.

---

## Cost Comparison at Startup Scale

| Database | Monthly Cost |
|---|---|
| PostgreSQL (Supabase/Neon) | $19–25 |
| MongoDB Atlas (M10) | $57+ |
| Redis (Upstash) | $0–5 |

MongoDB runs **2–3× more expensive** before you've written a line of product code.

---

## Scaling Path

| Stage | Stack |
|---|---|
| 0 → early growth | Supabase or Neon + Upstash Redis |
| Growth → scale | Aurora PostgreSQL + ElastiCache |
| Edge cases only | MongoDB for document-native domains (product catalogs, CMS) with heterogeneous attributes |

PostgreSQL scales further than most SaaS teams will ever need. Aurora and Citus handle serious load. MongoDB's native sharding is real — but shard key selection is irreversible. A wrong choice is a migration.

---

## Recommendation

| Component | Choice | Rationale |
|---|---|---|
| **Primary database** | PostgreSQL | Best data model fit, lowest cost, largest talent pool, ACID, RLS |
| **Caching / sessions** | Redis | Right tool for the job |
| **MongoDB** | Do not use by default | Only justified with explicit document-native domain requirements |

---

**Bottom line:** Start on Supabase or Neon. Move to Aurora when revenue justifies it. Add Redis from day one via Upstash. The stack is boring, proven, and correct — which is exactly what you want when you're shipping product.
