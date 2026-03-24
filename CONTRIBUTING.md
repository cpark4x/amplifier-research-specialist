# Contributing to canvas-specialists

Canvas Specialists is a library of best-in-class, single-domain AI specialist agents for knowledge worker and consumer scenarios. Contributions are welcome — whether you're adding a new specialist, improving an existing one, or fixing documentation.

---

## Prerequisites

- [Amplifier](https://github.com/microsoft/amplifier) installed and configured
- An API key for a supported LLM provider (Anthropic, OpenAI, Azure, etc.)
- Basic familiarity with Amplifier bundle structure (see [bundle.md](bundle.md))

---

## What Can I Contribute?

### New specialists

The main contribution type. Each specialist gets its own file under `agents/`, its own pipeline, and its own interface contract. The backlog at [docs/BACKLOG.md](docs/BACKLOG.md) shows what's planned — pick one or propose a new one.

**Full guide:** [docs/adding-a-specialist.md](docs/adding-a-specialist.md)

### Improvements to existing specialists

- **Pipeline improvements** — new or refined stages in a specialist's `index.md`
- **New input parameters** — must be optional with sensible defaults; don't break existing callers
- **Output schema changes** — coordinate with maintainers first; breaking changes require a schema version bump and updating all callers

### Documentation and examples

- Fix errors or gaps in specialist READMEs
- Add worked examples to [docs/examples/](docs/examples/)
- Improve the contributor guide or vision docs

---

## Development Workflow

1. **Fork and branch** — branch from `main`; use `specialist/[name]` for new specialists, `fix/[description]` for fixes
2. **Build** — follow [docs/adding-a-specialist.md](docs/adding-a-specialist.md) step by step, including the three-step registry process
3. **Test locally** — see the Testing section in the guide; include a sample invocation result in your PR
4. **Open a PR** — describe what you built, what it accepts and returns, and include evidence it works

---

## PR Guidelines

- **One specialist per PR** — keeps review focused
- **Include a sample invocation** — paste a real input and the output it produced
- **No breaking interface changes without coordination** — if you need to change an existing output schema, flag it in the PR and bump the version in `shared/interface/types.md`
- **Short, focused `index.md`** — longer instructions don't make better specialists; every sentence should constrain behavior

---

## Questions?

Open an issue or check [docs/BACKLOG.md](docs/BACKLOG.md) to see what's in flight.
