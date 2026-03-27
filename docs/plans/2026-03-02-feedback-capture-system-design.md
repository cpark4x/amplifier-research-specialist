# Feedback Capture System Design

## Goal

Build a structured, low-friction system for capturing test log entries after specialist runs, triaging action items to the right destinations, and closing the loop that is currently handled manually.

## Background

The amplifier-research-specialist project uses a test log (`docs/test-log/`) to record how specialist chains perform across different topics. A routing table already defines where different types of findings should land — quality gaps go to the backlog, edge cases go to specialist epics, cross-run patterns go to `adding-a-specialist.md`, and so on.

Today, this process is entirely ad-hoc. There is no consistent capture flow, no structured metadata on log entries, and no automated path from a test observation to a backlog item or epic note. Two log entries exist, but they have no front matter, making programmatic querying impossible. The routing table exists but is not wired to anything.

The feedback capture system closes this loop: it provides a skill with a clear capture protocol, a recipe that automates the full cycle, and structured front matter that makes the log machine-readable going forward.

## Approach

Three components work together:

1. **Structured front matter** on every test log entry (enables filtering and querying)
2. **A project-scoped skill** (`feedback-capture`) that carries the full capture and triage protocol
3. **A recipe** (`capture-feedback.yaml`) that automates the end-to-end cycle: collect → capture → assess → write → triage → commit

A context nudge in `specialists-instructions.md` keeps the trigger visible without adding noise — it offers the capture flow once after a chain completes, then defers to the skill if the user says yes.

This approach was chosen over recipe-only because the skill carries the protocol in a reusable form: it can be invoked outside the recipe, referenced by other agents, and extended without restructuring the workflow.

## Architecture

```
Specialist chain completes
        │
        ▼
Context nudge offers capture (once)
        │
   User says yes ──────────────────────────┐
        │                                  │
        ▼                                  ▼
  Recipe invoked                    Skill loaded manually
  (capture-feedback.yaml)           (feedback-capture skill)
        │
        ▼
  6-step automated loop
  ┌─────────────────────────────────────────────────┐
  │  1. collect-metadata  (infer + confirm)          │
  │  2. capture-body      (5 sections)               │
  │  3. assess-quality    (pass / mixed / fail)      │
  │  4. write-log         (file + front matter)      │
  │  5. triage-action-items (route per table)        │
  │  6. commit            (all touched files)        │
  └─────────────────────────────────────────────────┘
```

## Components

### Component 1: Front Matter Schema

Every test log entry carries YAML front matter at the top of the file:

```yaml
---
specialist: researcher          # entry-point specialist tested
chain: "researcher → writer"    # full chain if multi-step, null if single
topic: notion-vs-obsidian       # slug identifying the subject matter
date: 2026-03-02
quality_signal: mixed           # pass | mixed | fail
action_items_promoted: true     # true | false | partial
---
```

**Field definitions:**

| Field | Type | Notes |
|---|---|---|
| `specialist` | string | Entry-point specialist. For chains, the first leg. Enables "show all researcher tests" regardless of chain composition. |
| `chain` | string or null | Full chain composition string (e.g., `"researcher → writer"`). Null for single-specialist tests. |
| `topic` | string | Slug-style identifier for the subject matter tested. |
| `date` | ISO 8601 | Date the test was run. |
| `quality_signal` | enum | Top-level assessment: `pass`, `mixed`, or `fail`. |
| `action_items_promoted` | enum | Whether action items were promoted to the backlog: `true`, `false`, or `partial`. |

### Component 2: Skill — `feedback-capture`

Location: `.amplifier/skills/feedback-capture.md` (project-scoped)

The skill has three parts:

**Part A — Trigger guidance**

After a specialist chain completes, offer once lightly:
> "Want to capture a test log entry for this run?"

If declined, do not ask again. If yes, or if the user makes an explicit request, load and execute the full capture procedure.

**Part B — Capture flow (sequential)**

1. Infer metadata from session context (specialist, chain, topic) — confirm with user before proceeding
2. What worked?
3. What didn't / what are the concerns?
4. Confidence accuracy — were ratings calibrated correctly?
5. Coverage assessment — did coverage flags fire correctly?
6. Action items — one `- [ ]` per distinct finding
7. Quality signal — ask user: pass, mixed, or fail?

**Part C — Triage + commit**

Route each action item according to the existing routing table:

| Finding type | Destination |
|---|---|
| Consistent quality gap | New item in `BACKLOG.md` |
| Edge case in one specialist | Open question in that specialist's epic |
| Pattern across multiple runs | Note in `adding-a-specialist.md` |
| Confidence systematically off | Issue in specialist's `index.md` |

After routing, write the test log file with front matter to the correct subdirectory, update all routed destinations, and commit all touched files together in a single commit.

### Component 3: Context Nudge

Location: bottom of `context/specialists-instructions.md`

```markdown
## Feedback Capture

After a specialist chain completes, offer once to capture a test log entry:
> "Want to log this run? I can capture what worked, any concerns, and route action items to the backlog."

For the full procedure, load the `feedback-capture` skill.
```

This keeps the trigger visible to the agent without encoding the full protocol in the context file. The skill carries the protocol; the context file carries the reminder.

### Component 4: Recipe — `capture-feedback.yaml`

Location: `recipes/capture-feedback.yaml`

Six-step automated loop:

| Step | Agent | Purpose |
|---|---|---|
| `collect-metadata` | self | Infer and confirm specialist, chain, and topic from session context |
| `capture-body` | self | Walk through the 5 template sections conversationally |
| `assess-quality` | self | Confirm pass / mixed / fail with user |
| `write-log` | foundation:file-ops | Write test log file with front matter to correct subdirectory |
| `triage-action-items` | self | Route each action item per the routing table |
| `commit` | foundation:git-ops | Commit all touched files in a single commit |

**Invocation:**
```
recipes tool operation=execute recipe_path=specialists:recipes/capture-feedback.yaml
```

### Component 5: Migration

The two existing test log entries get front matter added as part of this implementation. With only two entries, this is the lowest-cost migration moment — the recipe will generate front matter for all future entries automatically, so no ongoing manual burden is introduced.

**`docs/test-log/chains/2026-03-02-microsoft-anthropic-competitive-brief.md`**
```yaml
---
specialist: researcher
chain: "researcher → writer"
topic: microsoft-anthropic-competitive-brief
date: 2026-03-02
quality_signal: mixed
action_items_promoted: false
---
```

**`docs/test-log/chains/2026-03-02-notion-vs-obsidian-competitive-brief.md`**
```yaml
---
specialist: competitive-analysis
chain: "competitive-analysis → writer"
topic: notion-vs-obsidian
date: 2026-03-02
quality_signal: mixed
action_items_promoted: true
---
```

## Data Flow

```
Session context
    │
    ▼
collect-metadata ──► confirmed: specialist, chain, topic, date
    │
    ▼
capture-body ──► confirmed: worked, concerns, confidence, coverage, action items
    │
    ▼
assess-quality ──► confirmed: quality_signal (pass | mixed | fail)
    │
    ├──► write-log ──► docs/test-log/{specialist|chains}/YYYY-MM-DD-{topic}.md
    │                      (with full front matter + body)
    │
    ├──► triage-action-items
    │        ├──► consistent gap ──► BACKLOG.md
    │        ├──► edge case ──► specialist epic open questions
    │        ├──► cross-run pattern ──► adding-a-specialist.md
    │        └──► confidence issue ──► specialist index.md
    │
    └──► commit ──► single commit covering all touched files
```

## Error Handling

- **Metadata ambiguity**: If specialist or chain cannot be inferred from session context, the `collect-metadata` step asks the user directly before proceeding. No step executes with unconfirmed metadata.
- **Declined capture**: If the user declines the nudge, the offer is not repeated in the same session. The user can invoke the skill or recipe explicitly at any time.
- **Missing routing destination**: If a routed file (e.g., a specialist epic) does not exist, the triage step flags the item and surfaces it for manual handling before committing. It does not silently drop the action item.
- **Partial promotion**: If some action items are routed and others are not (e.g., destination file missing), `action_items_promoted` is set to `partial` in the front matter.

## Testing Strategy

- **Front matter schema**: Validate that both migrated entries parse correctly after front matter is added.
- **Skill trigger**: Verify the context nudge fires once after a chain completes and does not repeat on decline.
- **Recipe steps**: Run the recipe against a synthetic test session to confirm each step produces the expected output before routing or committing.
- **Triage routing**: Confirm each finding type lands in the correct destination file by running the recipe with one action item of each type.
- **Commit scope**: Verify that a single commit covers the log file and all routed destinations — no partial commits.

## Files to Create / Edit

| File | Action |
|---|---|
| `docs/plans/2026-03-02-feedback-capture-system-design.md` | Create — this document |
| `.amplifier/skills/feedback-capture.md` | Create — capture + triage protocol |
| `context/specialists-instructions.md` | Edit — add nudge section at bottom |
| `recipes/capture-feedback.yaml` | Create — 6-step automated recipe |
| `docs/test-log/chains/2026-03-02-microsoft-anthropic-competitive-brief.md` | Edit — add front matter |
| `docs/test-log/chains/2026-03-02-notion-vs-obsidian-competitive-brief.md` | Edit — add front matter |

## Open Questions

None. All design decisions were resolved during the brainstorming session. See the decision table in the Approach section for the rationale behind each choice.
