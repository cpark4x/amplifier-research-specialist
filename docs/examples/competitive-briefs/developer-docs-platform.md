# Documentation Platform Decision Brief

**For:** VP Engineering / Head of Developer Relations
**Decision:** Select a documentation platform for 2025–2026
**Urgency:** Moderate-High — Confluence EOL migration cycle creates competitive window

---

## The One-Sentence Market Read

Docs-as-code has won, AI-readability is the next table stake, and Atlassian's forced cloud migration has put the largest install base in years into active re-evaluation.

---

## What's Actually at Stake

Documentation is no longer a writing problem — it's an infrastructure problem. Platforms that auto-generate `llms.txt` and MCP servers turn your docs into AI-agent-consumable infrastructure. Platforms that don't will require retrofit work within 18 months. Choose accordingly.

---

## Decision Matrix

| If your situation is… | Choose | Why |
|---|---|---|
| API-first product, engineers own the docs | **Mintlify** | AI-native, best-in-class UX, auto-generates llms.txt + MCP, interactive API playground, docs PRs via AI agent. Category leader with a16z backing and 10x ARR growth. |
| OSS project or engineering team, cost-sensitive | **Docusaurus** | Free, MIT licensed, MDX/React, actively maintained by Meta. Full control, no vendor risk. Requires JS expertise; budget the setup time. |
| Mixed engineering + non-technical contributors | **GitBook** | Lowest onboarding friction across both audiences, Git sync available, clean output. Monitor for pricing changes and sync reliability before committing. |
| API product with a developer success mandate | **ReadMe** | The only platform with per-developer journey analytics — where individual users hit walls in your API. Expensive ($99+/month) but irreplaceable if that data drives retention. |
| Jira-dependent enterprise, high switching cost | **Confluence** | Only if Jira lock-in is non-negotiable. Expect add-on costs of 30–100% above base, forced cloud migration by March 2029, zero developer-native capabilities. Enter eyes open. |

**Do not choose Notion for technical documentation.** No versioned docs, no API reference support, AI features cost an additional $10/user/month. It is a team wiki, not a developer docs platform.

---

## Risks Worth Naming

- **Mintlify pricing** ($250/month Pro) is steep pre-Series B. Confirm contract flexibility if you're early-stage.
- **GitBook** has a documented history of pricing instability. Lock in terms before building on it.
- **Docusaurus** has no vendor — which is the risk as much as the feature. Maintenance depends on Meta's continued investment and your own JS capacity.
- **The mid-market gap is real.** No platform cleanly serves $50–$500/month teams that need AI features + Git-native workflow + polished design.

---

## Bottom Line

**For most developer-tool or API product teams: Mintlify is the default answer in 2026.** The AI-readability infrastructure alone justifies the evaluation. If budget or control requirements rule it out, Docusaurus is the defensible fallback. Everything else is a compromise optimized for a specific constraint — know which constraint you're optimizing for before you sign.
