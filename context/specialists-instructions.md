# Specialists: Available Agents

This bundle provides domain expert specialist agents for deep, structured work.
Delegate to these agents when quality and trustworthiness matter more than speed.

## Available Specialists

- **researcher** — Deep research with web search + fetch. Returns structured evidence
  with source tiers (primary/secondary/tertiary), per-claim confidence levels, a
  RESEARCH BRIEF for fast machine parsing, and explicit evidence gaps. Optimizes
  for trustworthiness, not speed.

- **writer** — Transforms structured source material into polished prose. Takes
  researcher output, analyst output, or raw notes and produces documents in the
  requested format (report, brief, proposal, executive summary, email, memo).
  Never generates claims the source material doesn't support.

## When to Use Each

**Delegate to `specialists:researcher` when:**
- Researching a person, company, product, or event
- Finding documentation for libraries, APIs, or frameworks
- Any research where source credibility and confidence matter

**Delegate to `specialists:writer` when:**
- Source material exists and needs to become a document
- Turning researcher output into a report, brief, or email
- Any writing task where substance already exists but needs clear expression

## Typical Chain

For most knowledge work tasks:
1. `specialists:researcher` → gathers and validates evidence
2. `specialists:writer` → transforms evidence into the requested document
