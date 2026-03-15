# README Audit — All Public cpark4x Repos

**Date:** March 15, 2026
**Repos audited:** 26
**Method:** Four quality tests from the writing-readmes skill (substitution, "so what?", 30-second, explain-it-back)

---

## Tier 1: Strong (8+) — Leave Alone

| Repo | Score | Key Strength |
|---|---|---|
| **canvas-specialists** | 9 | Problem-first, two speeds, adversarial quality signal |
| **deckgen** | 9 | Command-forward, "15 seconds, one HTML file, zero dependencies" |
| **ridecast** | 8.5 | Strong consumer voice, "45-min commute and 12 tabs" |
| **amplifier-change-advisor** | 8.5 | "Should this change exist in this product?" + blast radius example |
| **amplifier-writing-readme** | 8.5 | Clean skill bundle README, problem-first |
| **finisher** | 8 | "Give it a goal. Watch it work. Get back results." |
| **amplifier-usage-insights** | 8 | "Do you actually know if you're getting better?" |
| **amplifier-session-capture** | 8 | "Every AI session is a learning opportunity" |
| **amplifier-health-provider-tool** | 8 | "This project failed. That's the point." — rare honesty |
| **outcomist** | 8 | "AI drives activity, not outcomes." — sharp contrarian |

---

## Tier 2: Surgical Edit Needed (6-7.5)

| Repo | Score | Key Issue | Specific Fix |
|---|---|---|---|
| **nouri** | 8 | Updated yesterday, holding | Leave alone |
| **amplifier-doc-driven-dev** | 7.5 | Fetch shows old opening — verify push landed | Check git status |
| **amplifier-builder-coach** | 7 | "Evaluates against a growth framework" — vague | Add one concrete example of coaching output |
| **visioncaster** | 7 | "Validate the problem before you build" — generic | Add what makes this different from just asking an LLM |
| **remember-twelve** | 7 | "Preserve your year in twelve moments" — substitution borderline | Add the specific mechanism — why "twelve" |
| **amplifier-bundle-ui-vision** | 6.5 | "AI-powered visual UI testing" — no problem statement | Add: "Visual regressions slip through CI. Screenshots catch what assertions miss." |
| **amplifier-bundle-session-guardian** | 6.5 | "Automatic session scope management" — no problem | Add: "Sessions fill up. Context degrades. You lose your work halfway through." |
| **murmur** | 6.5 | "A CLI speech-to-text tool" — no differentiation | Add: "Fully local. No cloud, no API keys, no data leaving your machine." |

---

## Tier 3: Rewrite or Intentionally Lightweight (1-5)

| Repo | Score | Status | Action |
|---|---|---|---|
| **amplifier-stories** | 5 | Internal tooling | Rewrite if external-facing; leave if internal |
| **amplifier-app-cli** | 5 | Reference implementation | Rewrite — 379 lines but opening is one generic line |
| **devcontainer-templates** | 5 | Dev tooling | Rewrite — emoji feature list, no problem |
| **ridecast-v1** | 5 | Superseded by ridecast2 | Skip — archive or redirect |
| **amplifier-module-tool-msgraph** | 4 | Spike/exploration | Skip — 9 lines is fine for a spike |
| **openai-images-mcp** | 4 | MCP server | Rewrite if maintained; skip if abandoned |
| **outcomist_collab** | 3 | Exploration | Skip — experimental project |
| **learn** | 2 | Personal sandbox | Skip — 11-line placeholder is appropriate |

---

## Score Distribution

```
9+    ██ 2
8-8.9 ████████ 8
7-7.9 ███ 3
6-6.9 ███ 3
5-5.9 ████ 4
1-4.9 ██████ 6
```

**10 repos at 8+ (38%)** — no action needed
**6 repos at 6-7.9 (23%)** — surgical edits, 1-2 lines each
**10 repos at 1-5.9 (38%)** — half are experiments (skip), half need rewrites

---

## Patterns Discovered

### 1. Amplifier bundle READMEs have a recurring gap
amplifier-bundle-ui-vision, amplifier-bundle-session-guardian, amplifier-bundle-session-capture — all describe the *capability* without the *problem*. "Automatic session scope management" tells you what it does. "Sessions fill up and you lose your work" tells you why you need it. Every bundle README needs the one-sentence problem before the capability.

### 2. Spike/experiment repos don't need the full treatment
learn, outcomist_collab, amplifier-module-tool-msgraph — these are explorations. A 4/10 README on a spike is appropriate. The skill should acknowledge this instead of treating every repo the same.

### 3. "Built by" compression worked everywhere
Every repo that had a multi-line Built By section was improved by compressing to one line. This pattern held across all 26 repos with zero exceptions.

### 4. Buried gold is universal
Every repo scored 6-7 had better material in docs/ or vision files than what was in the README. The "look for buried gold" pattern from the skill is the single most useful improvement technique.

---

## Top 5 Actions (Priority Order)

1. **Verify amplifier-doc-driven-dev push** — yesterday's rewrite may not have landed
2. **amplifier-builder-coach** — add one coaching output example (7 → 8.5)
3. **amplifier-bundle-ui-vision** — add visual regression problem statement (6.5 → 8)
4. **amplifier-bundle-session-guardian** — add session degradation problem (6.5 → 8)
5. **murmur** — add local/privacy differentiation (6.5 → 8)

---

## Skill Improvements to Make

1. Add "spike/experiment repos are intentionally lightweight — don't over-engineer them" to the skill
2. Add "Amplifier bundle" as a row in the weight-by-type table with: "Problem sentence before capability description. Show invocation pattern."
