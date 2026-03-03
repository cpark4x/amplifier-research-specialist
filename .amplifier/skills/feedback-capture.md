# feedback-capture

Structured protocol for capturing test log feedback after specialist runs and routing findings to the right destinations in the repo.

## When to Use

**Auto-nudge (light):** After a specialist chain completes, offer once:
> "Want to log this run? I can capture what worked, any concerns, and route action items to the backlog."

If declined, do not ask again in the session. If the user says yes — or requests feedback capture at any time — follow this protocol in full.

**On demand:** Any time the user asks to "capture feedback", "log this run", "write a test log entry", or similar.

## Capture Flow

Work through these sections conversationally, one at a time. Infer what you can from session context; confirm with the user before writing.

### 1. Collect Metadata (infer + confirm)

- **specialist** — entry-point specialist tested (`researcher`, `writer`, or `competitive-analysis`)
- **chain** — full chain if multi-step (e.g. `"researcher → writer"`), `null` if single specialist
- **topic** — slug identifying the subject (e.g. `notion-vs-obsidian`)
- **date** — today's date (YYYY-MM-DD)

### 2. What Worked?

Prompt: *"What worked well in this run? Consider: output quality, accuracy, schema usefulness, any synthesis that surprised you."*

### 3. What Didn't / Concerns?

Prompt: *"Any concerns or gaps? Consider: missing behaviors, wrong calls, confidence miscalibration, anything you'd flag for improvement."*

### 4. Confidence Accuracy

Prompt: *"Were confidence ratings calibrated correctly? Over-confident on hard-to-verify claims? Under-confident on solid ones?"*

### 5. Coverage Assessment

Prompt: *"Did coverage flags fire at the right time? Were gaps named correctly, or were they missed?"*

**Heuristic — no `Coverage: partial` flag was raised:**
Scan the output for specific numerical claims (benchmarks, percentages, dollar figures, counts) and highly specific assertions (named internal features, roadmap details, attributed quotes). If any appear without a traceable primary source, the flag should have fired — note as a miss.

**Heuristic — `Coverage: partial` was raised:**
Check whether the flagged gaps are genuine (things the specialist actually couldn't source) vs. over-cautious (things that are well-documented and should have been findable). A flag on a verifiable public fact is a calibration issue in the opposite direction.

### 6. Action Items

Prompt: *"What should change? Capture as `- [ ]` checkboxes, one per distinct finding."*

### 7. Quality Signal

Prompt: *"Overall signal for this run — pass, mixed, or fail?"*
- **pass** — output met the quality bar
- **mixed** — partial concerns, some things to address
- **fail** — significant quality issues

## Writing the File

**File location:**
- Single specialist: `docs/test-log/{specialist}/{date}-{topic}.md`
- Chain: `docs/test-log/chains/{date}-{topic}.md`

**Required front matter:**

```yaml
---
specialist: {specialist}
chain: "{chain}"        # omit this line entirely if null
topic: {topic}
date: {date}
quality_signal: {pass|mixed|fail}
action_items_promoted: false
---
```

Follow with the full log body using the standard 5-section structure:
`## What Worked` / `## What Didn't / Concerns` / `## Confidence Accuracy` / `## Coverage Assessment` / `## Action Items`

## Triage: Routing Action Items

After writing the file, route each `- [ ]` action item using this table:

| Finding type | Destination |
|---|---|
| Consistent quality gap | New item in `docs/BACKLOG.md` |
| Edge case in one specialist | Open question in `docs/02-requirements/epics/0{N}-{specialist}.md` |
| Pattern across multiple runs | Note in `docs/adding-a-specialist.md` |
| Confidence systematically off | Issue in `specialists/{specialist}/index.md` |

After routing, update `action_items_promoted` in the front matter:
- `true` — all action items promoted
- `partial` — some promoted, some deferred
- `false` — no items needed routing (rare)

## Commit

Commit the test log file and all updated destination files together:

```
git commit -m "docs: add test log entry for {chain or specialist} ({topic})"
```
