# Design: Competitive Analysis Follow-ups

**Date:** 2026-03-02
**Status:** Approved
**Source:** Test log action items — `docs/test-log/chains/2026-03-02-notion-vs-obsidian-competitive-brief.md`

---

## What We're Building

Three small, independent improvements surfaced from the first live test of the
competitive-analysis → writer chain. All are additive — no breaking changes to
existing specialists or recipes.

---

## Item 1: Recipe — `competitive-analysis-brief`

**File:** `recipes/competitive-analysis-brief.yaml`

A 2-step recipe that encodes the competitive-analysis → writer chain as a single
invokable workflow. Callers no longer dispatch both agents manually.

**Pipeline:**
```
Step 1: competitive-analysis
  Agent:  specialists:specialists/competitive-analysis
  Input:  {{query}}, optional {{dimensions}}, optional {{subjects}}
  Output: competitive_analysis_output

Step 2: writer
  Agent:  specialists:specialists/writer
  Input:  {{competitive_analysis_output}}, {{format}} (default: report), {{audience}}
  Output: final_document
```

**Context variables:**
| Variable | Required | Default | Notes |
|---|---|---|---|
| `query` | Yes | — | The competitive question |
| `format` | No | `report` | One of: report, brief, executive-summary |
| `audience` | No | `general` | Passed to Writer for voice/tone calibration |

---

## Item 2: Recipe — `competitive-analysis-brief-researched`

**File:** `recipes/competitive-analysis-brief-researched.yaml`

A 3-step recipe that runs the Researcher specialist first, passing its structured
output to competitive-analysis. This gives the matrix entries higher-fidelity source
tiering and confidence scoring vs. the self-research path.

**Pipeline:**
```
Step 1: researcher
  Agent:  specialists:specialists/researcher
  Input:  {{query}}
  Output: research_output

Step 2: competitive-analysis
  Agent:  specialists:specialists/competitive-analysis
  Input:  {{query}}, research: {{research_output}}   ← skips Stage 2
  Output: competitive_analysis_output

Step 3: writer
  Agent:  specialists:specialists/writer
  Input:  {{competitive_analysis_output}}, {{format}}, {{audience}}
  Output: final_document
```

**Same context variables as Item 1.** The two recipes are parallel choices:
- `competitive-analysis-brief` → fast, self-contained
- `competitive-analysis-brief-researched` → rigorous, sourced

No changes to either specialist. The competitive-analysis specialist already skips
Stage 2 when `research` is provided (Stage 1 parse logic).

---

## Item 3: Writer "Claims to Verify" Block

**File:** `specialists/writer/index.md`

When the Writer receives `analyst-output` (e.g., from competitive-analysis), all
claims are marked `unrated`. Some of those claims contain specific numerical values
— measurements, counts, dollar amounts, percentages, version numbers, dates — that
are easy to present at face value but hard to verify later.

**Change:** Add a scan at the end of Stage 5 (Verify and Cite). After building
the CITATIONS block, check all `unrated` claims for specific values. Surface any
flagged claims in a new Block 4: `CLAIMS TO VERIFY`.

**Detection heuristic:** An `unrated` claim contains a "specific value" if it has:
- A number with a unit (`87ms`, `50-row`, `2,000ms`, `$10/mo`)
- A percentage (`40%`, `60%`)
- A count with magnitude (`200+`, `8,000+`, `1,000+`)
- A named statistic presented as fact (`"the #1 tool for..."`)

**New output block (Block 4 — after CITATIONS):**
```
CLAIMS TO VERIFY
Unrated claims containing specific values — verify before citing externally.
S3: "87ms load time" | type: specific measurement
S7: "50-row database cap" | type: specific number
S12: "8,000+ Zapier integrations" | type: specific count

(or: CLAIMS TO VERIFY: none)
```

**When it fires:** Only when `input type` is `analyst-output` or `raw-notes`
(i.e., when claims are `unrated`). When input is `researcher-output`, confidence
is already explicit — no flag needed.

**No changes to CITATIONS.** This is an additive block, not a replacement.

---

## What Is Not Changing

- `specialists/competitive-analysis/index.md` — no changes
- `specialists/researcher/index.md` — no changes
- `recipes/capture-feedback.yaml` — no changes
- Any existing tests or test log entries

---

## Success Criteria

1. `competitive-analysis-brief` recipe runs end-to-end with just `query` provided
2. `competitive-analysis-brief-researched` recipe runs end-to-end; competitive-analysis
   receives and uses the researcher output (Stage 2 skipped)
3. Writer produces `CLAIMS TO VERIFY` block when given competitive-analysis output
   containing specific numerical claims
4. Writer produces `CLAIMS TO VERIFY: none` when no specific values are present
5. No regressions to existing Writer output format (Blocks 1–3 unchanged)
