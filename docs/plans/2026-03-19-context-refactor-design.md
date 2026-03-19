# Specialists Bundle Context Refactor Design

## Goal

Refactor the specialists bundle's context architecture to bring the largest context file under the 4,000-token guideline, eliminate wasteful context injection into spawned specialists, and pin all external dependencies.

## Background

The bundle validation recipe identified three problems:

1. **Oversized context file** — `context/specialists-instructions.md` at 4,924 tokens exceeds the 4,000-token per-file guideline by 23% and consumes 92% of the coordinator's context budget.
2. **Wasteful specialist spawn context** — `behaviors/specialists.yaml` includes `context/specialists-instructions.md` via `context.include`, injecting ~4,924 tokens of coordinator routing logic into every spawned specialist that has no use for it.
3. **Unpinned dependencies** — Three external dependencies reference `@main`, creating exposure to unintentional breaking changes from upstream.

A secondary finding: `data-analyzer` (416 lines, the most analytically demanding agent) has no `model_role` override, while the simpler `planner` (87 lines) already has `model_role: reasoning`.

## Approach

**Strip specialist spawn context entirely.** Split the monolith into a coordinator-only file and remove the behavior's `context.include`. Spawned specialists operate solely from their own agent `.md` definitions, which are already self-contained at 87–416 lines each. Additionally pin all external deps and add `model_role: reasoning` to `data-analyzer`.

This was chosen over:

- **Option B (keep a lightweight catalog for specialists)** — No specialist has demonstrated a need for awareness of other specialists. Their output contracts and routing signals are defined in their own `.md` files. YAGNI.
- **Option C (per-specialist selective context)** — Over-engineering with ongoing maintenance burden to decide what each specialist should see.

## Architecture

### File Split

**Current state:** One monolith `context/specialists-instructions.md` (4,924 tokens) referenced from two places — `bundle.md` body (coordinator) and `behaviors/specialists.yaml` context.include (spawned specialists).

**New state:** One file, one audience.

**`context/coordinator-routing.md` (~2,750 tokens) — Coordinator only.** Contains everything the coordinator needs to orchestrate specialist chains:

- Conversational Chain Behavior header
- Rule 1 (chain completion default + routing heuristic table + depth check)
- Rule 2 (per-step narration templates — BEFORE/HANDOFF/FINAL)
- Agent ID list
- Rule 3 (escape hatch)
- Rule 4 (analysis signal)
- Rules 5–8 (formatter mandatory gates)
- Formatter narration suppression note
- Available Specialists (merged format — see below)
- Typical Chain patterns (5 chain recipes)
- Feedback Capture section

**`context/specialists-instructions.md` — DELETED.** Replaced entirely by `coordinator-routing.md`.

**`behaviors/specialists.yaml` context.include — REMOVED ENTIRELY.** Spawned specialists get zero additional context overhead.

### Merged Specialist Catalog

The current file has two parallel sections: "Available Specialists" (~1,300 tokens, 67 lines) and "When to Use Each" (~1,100 tokens, 63 lines). These describe the same 11 specialists from different angles, consuming 48% of the file budget and risking drift.

Merge into a single "Available Specialists" section using a compact per-specialist entry format:

```markdown
## Available Specialists

- **researcher** — Deep research with web search + fetch. Produces source-tiered
  evidence with confidence ratings and explicit evidence gaps. Optimizes for
  trustworthiness over speed. **Use when:** researching people, companies, products;
  finding documentation; any research where source credibility matters.

- **writer** — Transforms structured source material into polished prose. Takes
  researcher output, analyst output, or raw notes. Never generates unsupported
  claims. **Use when:** source material exists and needs to become a report,
  brief, email, or memo.
```

One description + one trigger per specialist. Single point of maintenance. Estimated savings: ~400–600 tokens.

### Wiring Changes

| File | Before | After |
|------|--------|-------|
| `bundle.md` body | `@specialists:context/session-startup.md` + `@specialists:context/specialists-instructions.md` | `@specialists:context/session-startup.md` + `@specialists:context/coordinator-routing.md` |
| `behaviors/specialists.yaml` context.include | `specialists:context/specialists-instructions.md` | *(section removed entirely)* |

### Dependency Pinning

Three external dependencies pinned from `@main` to current HEAD SHAs:

| Dependency | Location | Change |
|------------|----------|--------|
| `amplifier-foundation` | `bundle.md` includes | `@main` → `@{current SHA}` |
| `amplifier-doc-driven-dev` | `bundle.md` includes | `@main` → `@{current SHA}` |
| `amplifier-module-tool-web` | `behaviors/specialists.yaml` tools | `@main` → `@{current SHA}` |

SHAs over semver tags: these repos don't consistently publish semver tags. Pinning to SHA is deterministic and available today.

Upgrade path: bump SHA intentionally and re-run bundle validation recipe to verify nothing breaks.

### model_role Addition

Add `model_role: reasoning` to `agents/data-analyzer.md` frontmatter. It's the most analytically demanding agent (416 lines, labeled inference work, fact/inference separation, 5-item self-check) but currently has no model role override.

## Components

### Complete File Change List

| Action | File | Details |
|--------|------|---------|
| **Create** | `context/coordinator-routing.md` | All routing logic: Rules 1–8, merged specialist catalog, typical chains, feedback capture (~2,750 tokens) |
| **Delete** | `context/specialists-instructions.md` | Replaced by coordinator-routing.md |
| **Edit** | `bundle.md` body | Replace `@specialists:context/specialists-instructions.md` with `@specialists:context/coordinator-routing.md` |
| **Edit** | `behaviors/specialists.yaml` | Remove `context.include` section entirely |
| **Edit** | `agents/data-analyzer.md` | Add `model_role: reasoning` to frontmatter |
| **Edit** | `bundle.md` includes | Pin foundation and doc-driven-dev to current HEAD SHAs |
| **Edit** | `behaviors/specialists.yaml` tools | Pin tool-web to current HEAD SHA |

### What Doesn't Change

- All 12 agent `.md` files (except `data-analyzer.md` one-line frontmatter addition)
- `context/session-startup.md`
- All recipes, tests, specs, docs, modules, shared/

## Data Flow

**Coordinator session:**

```
bundle.md body → loads @specialists:context/session-startup.md (449 tokens)
              → loads @specialists:context/coordinator-routing.md (~2,750 tokens)
behaviors/specialists.yaml → contributes tools, agent list, spawn config (no context.include)
Total coordinator context: ~3,200 tokens
```

**Spawned specialist session:**

```
effective_bundle = parent.compose(agent)
  .context = parent context (empty — no context.include) + agent context (if any)
  .instruction = agent's own .md body (replaces bundle.md body)
Total additional context: 0 tokens
```

## Error Handling

- **coordinator-routing.md exceeds 4,000 tokens after writing** — Trim the merged specialist catalog entries, which are the most compressible section.
- **A specialist needs ecosystem awareness post-refactor** — Add a targeted `@mention` in that specific agent's `.md` file. Don't re-add a blanket catalog for all 12.
- **Unpinned dependency breaks before pinning is complete** — Pin that specific dep first as a hotfix.

## Testing Strategy

1. **Re-run bundle validation recipe** — Verify `coordinator-routing.md` is under 4,000 tokens and total coordinator context is under 8K.
2. **Verify spawned specialist context** — Run a quick specialist delegation (e.g., researcher) and confirm it doesn't receive coordinator routing content.
3. **Run existing test suite** — `pytest tests/` to catch any regressions.
4. **Smoke test a full chain** — Run the research-chain recipe end-to-end to verify narration, routing, and formatter gates still work correctly.

## Expected Outcome

| Metric | Before | After |
|--------|--------|-------|
| Coordinator context | 5,373 tokens | ~3,200 tokens |
| Per-specialist spawn context | ~4,924 tokens | 0 additional |
| Largest single file | 4,924 tokens (over guideline) | ~2,750 tokens (well under) |
| Files over 4K guideline | 1 | 0 |
| Unpinned deps | 3 | 0 |

## Open Questions

- Exact SHAs for dependency pinning will be determined at implementation time.
- Whether `session-startup.md` should be gated to dev-only sessions is deferred to a future refactor.
