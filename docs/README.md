# specialists Documentation

A library of best-in-class, single-domain AI specialist agents for knowledge worker and consumer scenarios. Specialists are deep, single-domain agents (researcher, writer, storyteller, etc.) that orchestrators delegate to when quality and trustworthiness matter. Built as a composable bundle that can be included in any Amplifier project.

---

## Quick Links

| Document | Purpose |
|----------|---------|
| [BACKLOG](BACKLOG.md) | Strategic planning view — epics, priorities, status |
| [VISION](01-vision/VISION.md) | Problems, positioning, philosophy |
| [PRINCIPLES](01-vision/PRINCIPLES.md) | Decision framework |
| [SUCCESS-METRICS](01-vision/SUCCESS-METRICS.md) | How we measure success |
| [Epics](02-requirements/epics/) | What we're building |
| [User Stories](02-requirements/user-stories/) | Implemented capabilities |
| [Adding a Specialist](adding-a-specialist.md) | Guide for new specialist authors |

---

## Epic Status

| # | Epic | Status | Description |
|---|------|--------|-------------|
| 01 | [Research Specialist](02-requirements/epics/01-research-specialist.md) | Complete | Structured, source-tiered research output with confidence scoring, evidence gaps, and a typed `ResearchOutput` contract |
| 02 | [Writer Specialist](02-requirements/epics/02-writer-specialist.md) | Complete | Transforms source material into polished prose with inline citations, coverage audit, and machine-readable metadata |
| 03 | Storyteller | Complete | Cognitive mode translation — transforms research/analysis into compelling narratives with NARRATIVE SELECTION editorial record |
| 04 | [Competitive Analysis](02-requirements/epics/04-competitive-analysis.md) | Complete | Structured competitive intelligence with comparison matrices, positioning gaps, and win conditions — head-to-head and landscape modes |
| 05 | Design | Planned | Translates briefs and research into structured design direction |
| 06 | Demo Generator | Planned | Reverse-engineers a persuasive arc from a product; sequences wow moments, generates script |
| 07 | Presentation Builder | Planned | Slide-by-slide deck outlines with speaker notes from any specialist output |
| 08 | Data Analyzer | Complete | Labeled inferences from research evidence with explicit fact/inference separation and full traceability |
| 09 | Planner | Complete | Transforms goals and context into structured plans with milestones, dependencies, timelines, and risk flags |
| 10 | Prioritizer | Complete | Ranks items using prioritization frameworks (impact/effort, MoSCoW, RICE) with per-item rationale |
| 11 | Platform Integrations | Planned | LangChain/LangGraph wrappers, rendering integrations |

**Status:** 7 complete · 4 planned

---

## Documentation Structure

```
docs/
  BACKLOG.md            # Strategic planning view (canonical)
  01-vision/              # Strategic direction
    VISION.md             # Problems, solution, philosophy
    PRINCIPLES.md         # Decision framework
    SUCCESS-METRICS.md    # How we measure success
  02-requirements/        # What we're building
    epics/                # High-level feature areas
    user-stories/         # Implemented capabilities (filed at implementation time)
  plans/                  # Implementation plans (historical)
  templates/              # Document templates for new docs
  adding-a-specialist.md  # Guide for contributing new specialists
```

---

## Contributing

- **Vision changes**: Rare, require broad alignment — the output schema is the contract
- **New epics**: Scope in planning before creating; one epic per specialist domain
- **User stories**: Created only when implementing a feature, not speculatively
- **Principles**: Evolve as we learn what the specialist pattern actually demands
