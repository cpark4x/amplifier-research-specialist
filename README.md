# Specialists

A collection of domain expert agents — each with a focused persona, domain-specific tools, deep instructions, and a clean interface.

## Philosophy

> A specialist is like a consultant with a toolbox. A skill is a textbook. A specialist *does the work.*

Specialists are **stateless domain experts**. Each one:

- Has deep expertise in a specific domain
- Exposes a defined interface contract — what it accepts, what it returns, what it can do
- Has no knowledge of Canvas or any UI — callable from any product identically
- Does not manage its own memory — loads context from external memory, does work, produces structured output, optionally writes back

**The specialist never knows where it's being called from.** Canvas, a CLI, another agent — the interface contract is the boundary.

## How Specialists Are Invoked

Any orchestrator calls a specialist the same way:

1. Provide the structured input (task, context, memory)
2. Receive the structured output
3. Continue

The orchestrator picks the right specialist. The specialist does the work. Neither knows the internals of the other.

## Specialists

| Specialist | Domain | Status |
|---|---|---|
| [researcher](specialists/researcher/) | Structured web research with source tiering, quality gates, and confidence-rated evidence | v1 |

## Shared Interface

`shared/interface/types.md` defines the stable output contracts all specialists follow. Orchestrators and downstream specialists depend on these — they do not change when implementations evolve.

## Design Principles

**Outcome over speed.** The primary design constraint across all specialists is quality of output, not time-to-output. Speed is what you opt into. Quality is the default.

**The output schema is the center.** Each specialist's output schema is its stable contract. Implementations evolve freely. The schema does not change without a version bump and coordinated update to callers.

**Mechanism, not policy.** Specialists expose their behavior as configurable parameters. Defaults are tuned for quality. Callers opt into speed or alternative behavior.

**Composable stages.** Specialists run as sequences of discrete stages — each with one job and a clean output. Individual stages are improvable, debuggable, and swappable independently.

## Adding a Specialist

See [`docs/adding-a-specialist.md`](docs/adding-a-specialist.md).
