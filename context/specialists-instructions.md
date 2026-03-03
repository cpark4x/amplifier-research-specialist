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

- **competitive-analysis** — Transforms a question or existing research into structured
  competitive intelligence. Returns a machine-parseable `CompetitiveAnalysisOutput` with
  comparison matrices, positioning gaps, and win conditions. Handles head-to-head and
  landscape modes. Output is designed for downstream agents (Writer) to consume.

## When to Use Each

**Delegate to `specialists:researcher` when:**
- Researching a person, company, product, or event
- Finding documentation for libraries, APIs, or frameworks
- Any research where source credibility and confidence matter

**Delegate to `specialists:writer` when:**
- Source material exists and needs to become a document
- Turning researcher output into a report, brief, or email
- Any writing task where substance already exists but needs clear expression

**Delegate to `specialists:specialists/competitive-analysis` when:**
- Comparing two or more companies, products, or services head-to-head
- Mapping the competitive landscape for a subject ("who competes with X?")
- You need structured comparison data, not a narrative summary
- Source material from the Researcher needs to be structured into competitive intelligence

## Typical Chain

For most knowledge work tasks:
1. `specialists:researcher` → gathers and validates evidence
2. `specialists:writer` → transforms evidence into the requested document

For competitive intelligence tasks:
1. `specialists:researcher` → gathers evidence (optional — competitive-analysis can research itself)
2. `specialists:specialists/competitive-analysis` → structures evidence into competitive intelligence
3. `specialists:writer` → transforms competitive intelligence into a brief or report

## Feedback Capture

After a specialist chain completes, offer once to capture a test log entry:
> "Want to log this run? I can capture what worked, any concerns, and route action items to the backlog."

For the full procedure, load the `feedback-capture` skill.
