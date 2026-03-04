# IaC Tool Selection — Decision Brief

**To:** CTO
**Re:** Infrastructure-as-Code Platform Selection
**Date:** March 2026

---

## Situation

Your team needs a primary IaC platform. Three candidates are in scope: Terraform, Pulumi, and Ansible. One recommendation emerges clearly given your cloud-native context.

---

## Bottom Line Up Front

**Choose Pulumi.** For a TypeScript-first cloud-native startup, it is the only tool that treats your engineers as the asset they are — letting them provision infrastructure in the languages they already own.

---

## Candidate Assessment

| | Pulumi | Terraform / OpenTofu | Ansible |
|---|---|---|---|
| **Language** | TypeScript, Python, Go, C# | HCL (proprietary DSL) | YAML |
| **Ramp time** | ~1 week (TypeScript teams) | 2–4 weeks | Days |
| **State management** | ✅ Full | ✅ Best-in-class | ❌ None |
| **Provider coverage** | 3,000+ (via bridge + native) | 3,000+ (industry standard) | N/A for cloud IaC |
| **License** | Commercial (SaaS optional) | BSL (OpenTofu = OSS fork) | Apache 2.0 |
| **Cost** | ~$50/user/mo (Teams tier) | Free (OSS) | Free |
| **Ceiling** | High — Automation API, platform eng | Medium — HCL limits at scale | Low — not built for cloud IaC |

---

## Key Risks & Mitigants

**Pulumi** — The `Output<T>` async type system creates a brief learning curve for new hires. Mitigant: invest one sprint in internal patterns and typed wrappers; this is a one-time cost.

**Terraform** — BSL license introduced August 2023 restricts commercial redistribution. If this is a concern, OpenTofu (the fully open-source fork) is a drop-in replacement with an active community. HCL's loops and conditionals become painful at scale; no credible unit-testing story.

**Ansible** — No state file. This is disqualifying for cloud provisioning. Ansible is appropriate only as a config-management complement to your primary IaC layer — never as a replacement.

---

## Decision Rules

| If… | Then… |
|---|---|
| Team is TypeScript or Python-native | **Pulumi** — highest velocity, lowest context-switching |
| Ops team has deep HCL expertise | **OpenTofu** — preserve institutional knowledge |
| Need widest public module library today | **OpenTofu** — Registry is the largest in the ecosystem |
| Managing VM configuration (not provisioning) | **Ansible alongside** your primary IaC tool |

---

## Recommendation

**Pulumi for cloud-native startups where TypeScript or Python is the primary engineering language.** You get real languages, real testing frameworks, built-in secrets encryption, and an Automation API purpose-built for platform engineering — without a DSL tax.

Only default to Terraform/OpenTofu if your ops team has deep HCL investment or you need immediate access to the broadest public module registry. Never rely on Ansible alone for cloud provisioning.

---

## Suggested Next Step

Authorize a two-week Pulumi proof-of-concept on one non-production workload. Instrument ramp time and module reuse rate. Decision should be fully evidenced before the Q2 infrastructure sprint begins.
