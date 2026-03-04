# ENTERPRISE AI PROVIDER STRATEGY
## Decision Brief — CTO Office

**Date:** March 2026 | **Classification:** Internal | **Decision Required:** Provider Architecture

---

## SITUATION

The enterprise AI market has consolidated around three credible providers — Google Gemini, OpenAI, and Anthropic — each with distinct capability profiles and material cost differentials. A single-provider dependency is both strategically and economically indefensible. A routing architecture is warranted.

---

## BOTTOM LINE UP FRONT

**Adopt a three-tier multi-provider architecture.** Route ~80% of token volume to Gemini Flash, escalate complex reasoning to GPT-5.2, and run agentic/code workloads on Claude. This configuration optimizes cost, capability, and compliance simultaneously.

---

## PROVIDER ASSESSMENT

| Dimension | Google Gemini | OpenAI | Anthropic |
|---|---|---|---|
| **Overall Score** | **8.63** ✓ | 7.75 | 7.38 |
| **Reliability** | Best (GCP, 15-min P1) | Solid | Weakest (128+ incidents) |
| **Cost @ 1B tokens/mo** | **~$1.1M** | ~$6.4M | ~$7.4M |
| **Compliance** | FedRAMP High ✓ | Missing ISO 27001/42001 | Auditable (Constitutional AI) |
| **Fine-tuning** | Available | Available | Effectively exited |
| **Standout Capability** | Multimodal, ARC-AGI-2 | Math/Science (AIME ~100%) | Code agents (SWE-bench 80.9%) |

---

## KEY RISKS

- **Anthropic reliability** is the primary operational concern — multi-hour outages are incompatible with production SLAs. Contain exposure; do not route high-volume or latency-sensitive workloads.
- **OpenAI integration churn** — rapid model release cadence creates ongoing engineering overhead. Abstract behind a provider interface layer.
- **Google vendor lock-in** — high volume concentration on Gemini Flash demands abstraction and fallback routing from day one.

---

## ROUTING ARCHITECTURE

```
Incoming Request
       │
       ▼
  [Volume / Cost workloads]  ──────▶  Gemini Flash         ~80% traffic
       │
  [Complex reasoning / math] ──────▶  GPT-5.2              ~15% traffic
       │
  [Agentic / code / HIPAA]  ────────▶  Claude Sonnet         ~5% traffic
```

**Estimated blended cost:** ~$1.5–2M/month at 1B tokens vs. $6–7M single-provider. **Projected savings: 70–80%.**

---

## COMPLIANCE ROUTING

| Regulatory Context | Mandated Provider |
|---|---|
| Federal / DoD | Google (sole FedRAMP High holder) |
| Healthcare / HIPAA | Anthropic (auditable architecture) |
| General enterprise | Gemini Flash primary |

---

## DECISIONS REQUIRED

1. **Approve multi-provider architecture** as the strategic default — single-provider is not recommended.
2. **Mandate provider abstraction layer** in platform engineering — enables routing, fallback, and cost governance without application re-engineering.
3. **Qualify Google as primary volume provider** — cost differential alone justifies 83–85% savings versus flagship equivalents.
4. **Cap Anthropic exposure** to workloads where safety auditability or code-agent performance are the decisive requirement — do not use as a reliability-sensitive primary path.

---

## WHAT THIS IS NOT

This is not a recommendation to pick a winner. The 2025–2026 provider landscape rewards *routing intelligence*, not vendor loyalty. The organizations that will win are those that treat AI providers as infrastructure — abstracted, interchangeable, and cost-optimized at the routing layer.

---

*Source: Competitive analysis across reliability, safety, cost, capability, and compliance dimensions. March 2026.*
