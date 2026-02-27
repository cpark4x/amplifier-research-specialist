# specialists Documentation

A library of domain expert specialist agents for Amplifier — independent of any UI. Specialists are deep, single-domain agents (researcher, writer, etc.) that orchestrators delegate to when quality and trustworthiness matter. Built as a composable bundle that can be included in any Amplifier project.

---

## Quick Links

| Document | Purpose |
|----------|---------|
| [VISION](01-vision/VISION.md) | Problems, positioning, roadmap |
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

**Status Legend:** `Planning` · `In Progress` · `Complete`

---

## Documentation Structure

```
docs/
  01-vision/              # Strategic direction
    VISION.md             # Problems, solution, roadmap
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
