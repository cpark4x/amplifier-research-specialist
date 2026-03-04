# Specialists: Available Agents

This bundle provides domain expert specialist agents for deep, structured work.
Delegate to these agents when quality and trustworthiness matter more than speed.

## Conversational Chain Behavior

**Rule 1 — Chain Completion Default**: Always complete through to the writer before responding. Default output format = `brief`. Never stop at an intermediate specialist and surface the raw structured block. The user gets a finished document.

**Rule 2 — Per-Step Narration**: Before each delegation announce what's running. After each delegation announce what completed:
- Before: '🔍 Running researcher...'
- After: '✅ Researcher complete — passing to writer...'
- Final: '✍️ Done. Here's your brief.'

**Rule 3 — Escape Hatch**: If the user explicitly says 'raw output', 'give me the raw research', 'just run the researcher', or 'don't write a document' — stop at that specialist and surface the structured block directly.

**Rule 4 — Analysis Signal**: If the user asks for 'analysis', 'insights', or 'full analysis' — chain through data-analyzer before writer: researcher → data-analyzer → writer.

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

- **data-analyzer** — Draws labeled inferences from ResearchOutput. Returns
  `AnalysisOutput` — findings projected from ResearchOutput plus explicit inferences
  that each trace to specific findings. Use between Researcher and Writer when you
  need facts and conclusions explicitly separated. Input must be canonical
  `ResearchOutput` from the Researcher — not raw notes or narrative summaries.

- **researcher-formatter** — Format conversion specialist. Receives raw research
  narrative in any format (canonical RESEARCH OUTPUT block or narrative markdown
  with inline citations) and produces a canonical RESEARCH OUTPUT block. Use after
  the researcher when guaranteed canonical format is required for machine parsing
  or downstream pipeline steps. Never researches, never analyzes — only extracts
  and reformats.

- **storyteller** — Transforms research, analysis, or existing documents into
  compelling narrative using cognitive mode translation. Returns StoryOutput with
  a clean story, NARRATIVE SELECTION editorial record, and framework/tone metadata.
  Selects load-bearing findings for the arc — the Writer covers everything, the
  Storyteller selects.

## When to Use Each

**Delegate to `specialists:researcher` when:**
- Researching a person, company, product, or event
- Finding documentation for libraries, APIs, or frameworks
- Any research where source credibility and confidence matter

**Delegate to `specialists:writer` when:**
- Source material exists and needs to become a document
- Turning researcher output into a report, brief, or email
- Any writing task where substance already exists but needs clear expression

**Delegate to `specialists:specialists/data-analyzer` when:**
- You have ResearchOutput and need conclusions drawn before writing
- You want facts and inferences explicitly separated and labeled
- The Writer needs more than raw findings — it needs "what the evidence means"
- Any Researcher → Analyzer → Writer chain

**Delegate to `specialists:specialists/competitive-analysis` when:**
- Comparing two or more companies, products, or services head-to-head
- Mapping the competitive landscape for a subject ("who competes with X?")
- You need structured comparison data, not a narrative summary
- Source material from the Researcher needs to be structured into competitive intelligence

**Delegate to `specialists:specialists/storyteller` when:**
- Source material (research, analysis, competitive brief, or existing document) needs to
  become a compelling narrative rather than a structured document
- The audience needs to be moved or persuaded, not just informed
- You want narrative output instead of document output at the end of a chain
- Any Researcher → Formatter → Analyzer → Storyteller chain

## Typical Chain

For most knowledge work tasks:
1. `specialists:researcher` → gathers and validates evidence
2. `specialists:writer` → transforms evidence into the requested document

For reliable machine-parseable research output:
1. `specialists:researcher` → gathers and validates evidence (any format)
2. `specialists:specialists/researcher-formatter` → normalizes to canonical RESEARCH OUTPUT block
3. Downstream agents receive guaranteed canonical format

For analytical tasks requiring explicit fact/inference separation:
1. `specialists:researcher` → gathers and validates evidence
2. `specialists:specialists/researcher-formatter` → normalizes format (optional but recommended)
3. `specialists:specialists/data-analyzer` → draws labeled inferences from the evidence
4. `specialists:writer` → transforms facts + labeled inferences into the requested document

For competitive intelligence tasks:
1. `specialists:researcher` → gathers evidence (optional — competitive-analysis can research itself)
2. `specialists:specialists/competitive-analysis` → structures evidence into competitive intelligence
3. `specialists:writer` → transforms competitive intelligence into a brief or report

For narrative output from a research chain:
1. `specialists:researcher` → gathers and validates evidence
2. `specialists:specialists/researcher-formatter` → normalizes to canonical RESEARCH OUTPUT block
3. `specialists:specialists/data-analyzer` → draws labeled inferences
4. `specialists:specialists/storyteller` → transforms analysis into compelling narrative

## Feedback Capture

After a specialist chain completes, offer once to capture a test log entry:
> "Want to log this run? I can capture what worked, any concerns, and route action items to the backlog."

For the full procedure, load the `feedback-capture` skill.
