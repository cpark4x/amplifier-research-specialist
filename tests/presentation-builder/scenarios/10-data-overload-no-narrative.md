# Scenario 10: Data Overload — Raw Metrics with No Narrative

## Parameters

- **audience**: VP of Engineering and department heads
- **audience_type**: executive
- **purpose**: inform
- **tone**: formal
- **output_format**: html
- **theme**: clean-light
- **presentation_mode**: slides
- **include_speaker_notes**: true
- **include_appendix**: true

## Expected Framework

Answer-first (executives)

## Source Material

This is a raw data dump from an engineering metrics dashboard export. There is no prose, no framing, and no analysis — just numbers. The builder must interpret the data, identify the story, and choose appropriate visual formats. This is raw-notes input.

---

## Platform Health Metrics — March 2026

### Availability

| Service | Uptime (Feb) | Uptime (Mar) | Target | SLA |
|---------|-------------|-------------|--------|-----|
| API Gateway | 99.97% | 99.91% | 99.95% | 99.9% |
| Auth Service | 99.99% | 99.98% | 99.95% | 99.9% |
| Payment Processing | 99.95% | 99.88% | 99.99% | 99.95% |
| Search | 99.92% | 99.96% | 99.9% | 99.9% |
| Notifications | 99.80% | 99.94% | 99.9% | 99.5% |
| Data Pipeline | 99.70% | 99.72% | 99.5% | 99.5% |
| CDN | 99.99% | 99.99% | 99.95% | 99.9% |

### Incident Summary

| Severity | Count (Feb) | Count (Mar) | MTTR Feb | MTTR Mar |
|----------|------------|------------|----------|----------|
| P1 | 2 | 4 | 34 min | 52 min |
| P2 | 7 | 5 | 2.1 hrs | 1.8 hrs |
| P3 | 23 | 19 | 8.4 hrs | 6.2 hrs |
| P4 | 41 | 38 | 24 hrs | 18 hrs |

### P1 Incidents (March Detail)

1. Mar 3 — Payment Processing: database connection pool exhaustion during flash sale. Duration: 47 min. Customer impact: ~2,300 failed transactions. Root cause: connection limit not scaled for promotional traffic.
2. Mar 11 — API Gateway: certificate rotation failure caused 12-minute full outage. All services affected. Root cause: automated rotation script had a race condition with the load balancer health check.
3. Mar 18 — Payment Processing: third-party fraud detection provider timeout caused cascading failures. Duration: 38 min. Workaround: circuit breaker activated, transactions processed without fraud check for 6 min before provider recovered.
4. Mar 24 — Auth Service: memory leak in session token validation after deploying v2.4.1. Duration: 23 min. Root cause: unbounded cache growth in new token introspection module. Rolled back to v2.4.0.

### Performance

| Endpoint | p50 (Feb) | p50 (Mar) | p99 (Feb) | p99 (Mar) | Target p99 |
|----------|----------|----------|----------|----------|-----------|
| /api/search | 45ms | 42ms | 320ms | 290ms | 500ms |
| /api/checkout | 180ms | 210ms | 890ms | 1,240ms | 1,000ms |
| /api/auth/login | 65ms | 68ms | 180ms | 195ms | 300ms |
| /api/products | 32ms | 30ms | 150ms | 145ms | 200ms |
| /api/orders | 78ms | 95ms | 340ms | 480ms | 500ms |
| /api/notifications | 25ms | 22ms | 90ms | 85ms | 150ms |

### Deployment Metrics

| Metric | Feb | Mar |
|--------|-----|-----|
| Deployments | 142 | 168 |
| Rollbacks | 3 | 7 |
| Rollback rate | 2.1% | 4.2% |
| Deploy-to-incident rate | 1.4% | 2.4% |
| Mean lead time (commit to prod) | 4.2 hrs | 3.8 hrs |
| Change failure rate | 3.5% | 5.4% |

### Infrastructure Cost

| Category | Feb | Mar | MoM Change |
|----------|-----|-----|-----------|
| Compute (EC2/EKS) | $184,200 | $198,400 | +7.7% |
| Storage (S3/EBS) | $42,100 | $43,800 | +4.0% |
| Database (RDS/DynamoDB) | $67,300 | $71,200 | +5.8% |
| Networking | $23,400 | $28,900 | +23.5% |
| ML/AI services | $31,200 | $45,600 | +46.2% |
| Monitoring | $12,800 | $12,800 | 0% |
| Total | $361,000 | $400,700 | +11.0% |

### Team Metrics

| Metric | Feb | Mar |
|--------|-----|-----|
| Headcount | 52 | 54 |
| Open reqs | 6 | 4 |
| Attrition (trailing 12mo) | 8.2% | 7.8% |
| Sprint velocity (avg pts) | 156 | 148 |
| Unplanned work % | 22% | 28% |
| On-call escalation count | 14 | 21 |
| Engineer satisfaction (survey) | 7.2/10 | 6.8/10 |

### Customer Impact

| Metric | Feb | Mar |
|--------|-----|-----|
| Support tickets (platform) | 342 | 418 |
| Tickets mentioning "slow" | 28 | 67 |
| Tickets mentioning "error" | 45 | 72 |
| NPS (platform component) | 42 | 38 |
| Churn risk accounts flagged | 3 | 5 |
