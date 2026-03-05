# Canvas-Specialists: World-Class Roadmap

**Created:** March 5, 2026  
**Owner:** Chris Park  
**Status:** In Effect  

---

## Why This Exists

This roadmap captures a 4-phase progression toward a world-class specialist library. It's grounded in three architectural principles:

1. **Mechanism over Policy** – Build composable, predictable specialist behavior first. Governance emerges naturally from reliable mechanisms, not top-down rules.
2. **Bounded Defaults** – Each specialist ships with sensible out-of-box behavior. Configuration happens at the edges, not in the core.
3. **Regeneration** – Build feedback loops into the product. Test logs, usage metrics, and quality gates inform continuous refinement without breaking existing patterns.

The roadmap is reviewed and re-scored after Phase 1 ships. Each phase should take ~1-2 months.

---

## Phase 1: NOW — Solidify Core Foundations (Targeted: Shipped in Early April 2026)

### Goal
Stabilize 4 shipped specialists + 1 in-progress specialist. Lock contracts, establish bounded defaults, and build the feedback system that powers regeneration cycles.

### Prioritized Tasks

- [ ] **Storyteller specialist to shipped status**
  - Finish narrative-chain recipe (compound tones, structured NARRATIVE SELECTION)
  - Validate 5-stage pipeline across 5+ end-to-end tests
  - Add to USING-SPECIALISTS.md with real examples
  
- [ ] **Specialist output contract enforcement** (Quality Gate v1.1)
  - All 5 specialists serialize output to canonical schema (ResearchOutput, WriterOutput, CompetitiveAnalysisOutput, AnalysisOutput, StoryOutput)
  - All outputs pass strict JSON schema validation
  - Non-conforming outputs fail fast with clear error messages
  
- [ ] **Bounded defaults for each specialist**
  - Researcher: source-tier defaults (primary > secondary > analyst/circulated)
  - Writer: word-budget enforcement per format (brief ~600w, report ~1500w, exec summary ~400w)
  - Competitive Analysis: landscape mode as default, head-to-head via `mode: detailed`
  - Data Analyzer: quality threshold defaults (`confidence_minimum: 0.75`)
  - Storyteller: tone defaults (neutral, adaptive per input)
  
- [ ] **Test-log feedback system** (Phase 0 infrastructure → Phase 1 enforcement)
  - Test logs automatically mined for signals (word-budget gaps, audience drift, claim specificity issues)
  - Signals routed to epic definitions + specialist instructions for next phase
  - At least 2 sprints of test logs captured and analyzed
  
- [ ] **Async chain reliability**
  - Increase `research-chain` step timeouts + bound output sizes
  - Increase `narrative-chain` step timeouts + move save to foundation:file-ops
  - Benchmark parallel execution costs (N researchers in parallel → queue lag)
  - Document throttling guidance for orchestrators
  
- [ ] **Documentation: USING-SPECIALISTS.md v1.1**
  - Add Storyteller to the invocation guide
  - Include test-log feedback loop (how users contribute, how it informs improvements)
  - Real examples for each specialist at current quality level

### Acceptance Criteria

- [ ] All 5 specialists in BACKLOG "4 complete" status
- [ ] Zero tolerance for non-conforming specialist output in test runs
- [ ] USING-SPECIALISTS.md covers all 5 specialists with working examples
- [ ] Test-log mining produces at least 3 actionable signals for Phase 2
- [ ] `research-chain` + `narrative-chain` complete 10 consecutive end-to-end runs without timeout

### How to Verify

```bash
# Run all 5 specialist end-to-end tests
amplifier recipes run research-chain --test
amplifier recipes run competitive-analysis-brief --test
amplifier recipes run narrative-chain --test
amplifier recipes run analysis-synthesis --test
amplifier recipes run combined-research-analysis --test

# Validate schema conformance
python scripts/validate-specialist-output.py docs/examples/**/*.json

# Mine test logs for improvement signals
python scripts/mine-test-logs.py docs/test-log/ --since 2026-02-26

# Check recipe reliability
bash scripts/benchmark-chains.sh --runs 10 --parallel false
```

---

## Phase 2: NEXT — Expand Specialist Coverage & Refine Quality (Targeted: May–June 2026)

### Goal
Ship 3 additional specialists (Design, Planner, Prioritizer). Apply Phase 1 feedback to refine existing specialists. Establish inter-specialist composition patterns.

### Prioritized Tasks

- [ ] **Design specialist (Epic 05)**
  - 4-stage pipeline: parse brief → extract principles → define visual language → generate component guidance
  - DesignOutput schema (principles, visual language, constraints, reasoning)
  - Integration with Writer output as upstream
  
- [ ] **Planner specialist (Epic 09)**
  - 5-stage pipeline: parse goals → identify dependencies → timeline + milestones → risk flagging → output plan
  - PlannerOutput schema (phases, dependencies, timeline, risks, success metrics)
  - Integration with Competitive Analysis + Research as upstream
  
- [ ] **Prioritizer specialist (Epic 10)**
  - 4-stage pipeline: parse items + context → apply framework (impact/effort, RICE, MoSCoW) → rank → justify
  - PrioritizerOutput schema (ranked items, scores per dimension, rationale)
  - Framework selection defaults (impact/effort as default, others via config)
  
- [ ] **Refine Writer specialist based on Phase 1 feedback**
  - Word-budget enforcement: brief/report/summary contracts enforced, not advisory
  - Audience calibration: `audience: myself` → first-person, actionable; `audience: executive` → formal, decision-ready
  - Specificity enforcement: pull subject-specific findings through to conclusions
  
- [ ] **Refine Researcher specialist based on Phase 1 feedback**
  - Conservative confidence scoring: analyst estimates rated vs. audited primary data
  - Source-tier guidance update: when analyst estimates appear, call out confidence limits
  
- [ ] **Recipe composition patterns**
  - Document common chains: research → analyze → write, research → design, research → plan
  - New recipes: `research-design-chain`, `research-plan-chain`, `research-analyze-prioritize-chain`
  - Establish step-naming convention for reusable orchestration
  
- [ ] **Demonstration: end-to-end user journey**
  - Single conversational flow: "Help me launch a product" → research + competitive analysis + design + plan + prioritization
  - Captured with narrated execution (transparent which specialists ran in what order)

### Acceptance Criteria

- [ ] Design, Planner, Prioritizer specialists shipped + in BACKLOG "complete"
- [ ] Writer + Researcher ship Phase 1 refinements (word budget, audience, confidence) with no regression
- [ ] At least 3 new documented recipe patterns working end-to-end
- [ ] End-to-end user journey demo runs cleanly without manual hand-offs
- [ ] Phase 1 test-log signals all addressed or explicitly deferred

### How to Verify

```bash
# Run new specialists
amplifier recipes run design-from-brief --test
amplifier recipes run plan-from-competitive-analysis --test
amplifier recipes run prioritize-roadmap-items --test

# Run composite chains
amplifier recipes run research-design-chain --test
amplifier recipes run research-plan-chain --test

# Run end-to-end user journey
amplifier --conversational "Help me launch a product for [domain]" --log-execution

# Validate no regression in existing specialists
bash scripts/benchmark-chains.sh --baseline phase-1-performance
```

---

## Phase 3: LATER — Cross-Domain Orchestration & Advanced Regeneration (Targeted: July–August 2026)

### Goal
Enable ecosystem-level synthesis (cross-specialist consensus), advanced feedback loops, and sophisticated orchestration patterns. Move toward "platform" status.

### Prioritized Tasks

- [ ] **Ecosystem Comparison Recipe** (Big Idea from BACKLOG)
  - Accept research question + list of ecosystems
  - Fan out: one Researcher per ecosystem (parallel)
  - Synthesis Writer: leads with cross-ecosystem consensus, surfaces differentiated signals
  - Output: comparative brief with confidence tiers based on signal replication
  
- [ ] **Cross-specialist consensus synthesis**
  - When 2+ specialists produce independent analyses of the same subject, surface consensus signals
  - Example: Competitive Analysis + Researcher both flag the same market shift → confidence boost
  - Build into Quality Gate v2.0
  
- [ ] **Advanced feedback loops**
  - User feedback (thumbs up/down on sections) mined into specialist instruction refinements
  - Performance metrics (latency, token usage, cost) tracked per specialist + recipe variant
  - A/B testing framework for specialist prompt variants
  
- [ ] **Demo Generator specialist (Epic 06) [stretch goal]**
  - Reverse-engineer persuasive arc from a product/research
  - Output: wow moments, sequence for impact, script and talking points
  - Integration with Presentation Builder (below)
  
- [ ] **Presentation Builder specialist (Epic 07) [stretch goal]**
  - Accept research output + design direction
  - Generate slide deck (markdown + structure for pandoc → PPTX conversion)
  - Closes research → write → present chain
  
- [ ] **Platform integration layer**
  - LangChain / LangGraph wrapper package for the specialist library
  - Thin wrapper for orchestration, focuses on ecosystem presence not proprietary value

### Acceptance Criteria

- [ ] `ecosystem-comparison-chain` recipe delivers trustworthy cross-ecosystem synthesis
- [ ] Consensus signals integrated into Quality Gate with worked examples
- [ ] Advanced feedback loop infrastructure in place (user feedback → instruction updates)
- [ ] Demo Generator specialist (if shipping) has 90%+ task success rate
- [ ] Platform integration package published + documented

### How to Verify

```bash
# Run ecosystem comparison
amplifier recipes run ecosystem-comparison-chain \
  --research-question "AI coding tools landscape" \
  --ecosystems '["Microsoft Copilot", "Anthropic Claude Code", "OpenAI"]'

# Validate consensus signals
python scripts/check-consensus-signals.py docs/examples/ecosystem-comparisons/ --min-threshold 2

# Test advanced feedback loop
amplifier feedback submit --specialist writer --section "bottom-line" --feedback "thumbs-down: too generic"
amplifier inspect specialist instructions --specialist writer --feedback-applied-since 2026-06-01

# Demo Generator (if available)
amplifier recipes run demo-generation-chain --test
```

---

## Phase 4: CI/Polish — Production Readiness & Continuous Regeneration (Targeted: September onwards)

### Goal
Harden the product for sustained production use. Establish continuous improvement loops that allow regeneration without breaking existing workflows.

### Prioritized Tasks

- [ ] **Performance optimization**
  - Profile all specialists for latency hotspots
  - Implement caching for stable research outputs (source research has long shelf life)
  - Benchmark token efficiency improvements (prompt trimming, context window optimization)
  
- [ ] **Reliability & observability**
  - Structured logging across all specialists (execution traces, decision points, confidence scores)
  - Health checks for upstream dependencies (search APIs, knowledge bases)
  - Graceful degradation (fallback behaviors when sources fail)
  
- [ ] **Backwards compatibility & deprecation policy**
  - Version all specialist outputs (ResearchOutput v1.1, WriterOutput v1.2, etc.)
  - Document migration paths for schema changes
  - Sunset timeline for deprecated specialist versions (minimum 2 releases forward notice)
  
- [ ] **Continuous regeneration infrastructure**
  - Automated test-log mining on a cadence (weekly signal roll-up)
  - Quarterly specialist "health reports" (accuracy, latency, token efficiency, user satisfaction)
  - Automated A/B testing for prompt variants → A/B testing results feed back into instruction updates
  
- [ ] **Rendering & export parity**
  - All specialist outputs render to PDF, DOCX, HTML, Markdown with consistent styling
  - pandoc integration for slide deck generation (Presentation Builder output → PPTX)
  - Custom CSS for branded output templates
  
- [ ] **Documentation & community**
  - Specialist architecture guide for contributors
  - Integration cookbook for common orchestration patterns
  - Community feedback channel for specialist improvement signals

### Acceptance Criteria

- [ ] All specialists complete in <10s latency at p95, <50K tokens for typical use cases
- [ ] Zero unhandled exceptions in production test runs (100 runs minimum)
- [ ] Deprecation policy documented + first batch of policy changes communicated (if needed)
- [ ] Continuous regeneration pipeline runs weekly with no manual intervention
- [ ] All outputs support PDF, DOCX, HTML rendering without data loss

### How to Verify

```bash
# Performance benchmarking
bash scripts/benchmark-all-specialists.sh --samples 50 --profile true

# Reliability testing
bash scripts/stress-test-specialists.sh --runs 100 --parallel true --error-recovery enabled

# Schema versioning
amplifier inspect specialist-schemas --all-versions
amplifier migrate specialist-output --from ResearchOutput@v1.0 --to ResearchOutput@v1.1 docs/examples/old-research/

# Continuous regeneration
python scripts/weekly-signal-rollup.py --output docs/reports/signals-$(date +%Y-%W).md

# Rendering tests
amplifier render --input docs/examples/research-output.json --output test-render.pdf
amplifier render --input docs/examples/research-output.json --output test-render.docx
amplifier render --input docs/examples/competitive-brief.json --output test-render.html
```

---

## How to Use This Roadmap

### After Each Phase Completes

1. **Gather feedback**: Review test logs, user feedback, performance metrics from the completed phase
2. **Re-score**: Assess which tasks from the next phase have changed in priority or scope
3. **Adjust**: Update the next phase's task list based on learnings. It's OK if 20% of the roadmap moves.
4. **Communicate**: Publish updated roadmap with change notes (see format below)

### Updating This Document

**Format for changes:**
```markdown
| Phase | Item | Previous | New | Reason |
|-------|------|----------|-----|--------|
| 2 | Refine Writer | High | Medium | Phase 1 testing showed audience calibration less impactful than expected |
```

### When to Deviate

- **New specialized requests** (e.g., "we need a Fact-Checker specialist"): Add to Phase 3 planning section, don't re-prioritize active phase
- **Critical bugs**: Fix immediately, log in BACKLOG, backfill roadmap with the fix
- **Major architectural insights**: Pause, discuss, update all 4 phases if needed

### Relationship to BACKLOG.md

- This roadmap is the **strategic direction** (where we're heading)
- BACKLOG.md is the **tactical execution** (what's being worked on right now)
- When Phase 1 completes, the items move from this roadmap into BACKLOG's "Immediate Next" for Phase 2 + actual sprint planning

---

**Next Review Date:** After Phase 1 ships (estimated April 15, 2026)  
**Questions or feedback?** Update this file and re-commit with clear change notes.
