# Weekly Sprint Plan — Mar 9–13, 2026

> **For Claude:** Use the writing-plans + subagent-driven-development skills to execute this plan task-by-task.

**Goal:** Close Epic 03 (Storyteller), sweep all S-effort quality debt, ship Prioritizer specialist (Epic 10)

**Strategy:** Fix the two OUTPUT CONTRACT blockers first (Day 1) because #30 blocks verification of two already-shipped items (#18, #19), and #29 is the same class of fix using the same proven technique. Then sweep all remaining S-effort quality items (Days 2–3) while they're fresh and the patterns are warm. Ship the Prioritizer specialist (Days 3–4) as the week's headline deliverable. Close with recipe timeout resilience and a full verification sweep (Day 5).

**Compression lever:** Items #30 and #29 share the same fix pattern (WRONG/RIGHT examples + structural mandate). Items #16 and #17 share a file. Items #14, #15, #13 are all Writer spec touches that batch naturally. The Prioritizer follows the exact pattern of every existing specialist — no design invention needed.

---

## Day-by-Day Schedule

### Day 1 (Mon Mar 9): OUTPUT CONTRACT Compliance Sweep

**Theme:** Unblock Epic 03 by fixing the two format compliance failures that broke test runs.

| Order | Item | Effort | What ships |
|-------|------|--------|------------|
| 1 | **#30** — Storyteller OUTPUT CONTRACT | S | Storyteller produces `STORY OUTPUT` header + `NARRATIVE SELECTION` block + `QUALITY THRESHOLD RESULT` line reliably |
| 2 | **Verify #18/#19** — Storyteller inference auditability + quality_threshold | — | Confirm these features work now that #30 is fixed |
| 3 | **#29** — Writer OUTPUT CONTRACT for informal registers | S | `audience: myself` runs still produce `Parsed:` line and all structural blocks |

**End of day:** Epic 03 Storyteller at 100%. Writer informal-register compliance restored.

---

### Day 2 (Tue Mar 10): Data Analyzer + Writer Quality Sweep

**Theme:** Clear all remaining S-effort quality debt across Data Analyzer and Writer.

| Order | Item | Effort | What ships |
|-------|------|--------|------------|
| 1 | **#16** — Data Analyzer Format B detection hardening | S | Narrative markdown inputs parse reliably without silent extraction failures |
| 2 | **#17** — Data Analyzer code-fence prevention | S | `ANALYSIS OUTPUT` block never wrapped in triple backticks |
| 3 | **#14** — Writer structural sections for analysis-based inputs | S | Clear spec on when WRITER METADATA / CITATIONS / CLAIMS TO VERIFY are required vs. relaxed |
| 4 | **#13** — Writer parse-line-first output ordering | S | Spec accurately documents the `Parsed:` line comes first, always |

**End of day:** Data Analyzer and Writer specs hardened. All S-effort backlog items closed.

---

### Day 3 (Wed Mar 11): Prioritizer Design + Scaffold

**Theme:** Design the Prioritizer specialist and ship the spec + types.

| Order | Item | Effort | What ships |
|-------|------|--------|------------|
| 1 | Prioritizer specialist design — pipeline, schema, output format | — | Design document with full contract |
| 2 | `PrioritizerOutput` added to `shared/interface/types.md` | S | Schema contract published |
| 3 | `specialists/prioritizer/index.md` — full spec | M | Complete specialist spec following existing patterns |
| 4 | Coordinator routing update in `context/specialists-instructions.md` | S | Prioritizer is routable |

**End of day:** Prioritizer specialist fully specified and integrated into the routing layer.

---

### Day 4 (Thu Mar 12): Prioritizer Validation + Writer Dedup

**Theme:** Validate the Prioritizer with a test run, close remaining Writer item.

| Order | Item | Effort | What ships |
|-------|------|--------|------------|
| 1 | Prioritizer test run — manual validation against spec | M | Confirmed working specialist |
| 2 | Iterate on spec based on test run findings | S | Spec refined |
| 3 | **#15** — Writer deduplication pass | S | Dedup check strengthened in Writer Stage 5 |

**End of day:** Prioritizer validated. Writer dedup shipped.

---

### Day 5 (Fri Mar 13): Recipe Resilience + Verification Sweep

**Theme:** Fix recipe timeouts, run full chain verification, close the week clean.

| Order | Item | Effort | What ships |
|-------|------|--------|------------|
| 1 | **#11** — Recipe timeout resilience | M | `research-chain.yaml` timeouts increased, save step de-LLM'd |
| 2 | Full chain verification — research-chain + narrative-chain | — | Confirmed end-to-end pipeline works |
| 3 | Backlog/scorecard/epic status updates | S | All tracking artifacts current |
| 4 | *(Stretch)* Prioritizer recipe — `prioritize-chain.yaml` | S | Automated prioritization pipeline |

**End of day:** All committed items shipped. Tracking current. Week closed.

---

## Sequencing Rationale

### Why #30 first (Monday morning)

**#30 is a force multiplier.** It blocks verification of two already-shipped items (#18 inference auditability, #19 quality_threshold parameter). Until #30 is fixed, we can't confirm whether Epic 03 is actually at 90% or has regressed. Fixing it first means we can verify #18/#19 the same morning and potentially close Epic 03 to 100% by Monday afternoon.

### Why #29 immediately after #30

**Same fix pattern, warm context.** Both #30 and #29 are OUTPUT CONTRACT violations where the model interpreted informal language in the spec as permission to skip structural requirements. The proven fix is identical: add WRONG/RIGHT examples showing the exact failure mode, add an explicit "structural blocks required regardless of..." mandate. Doing them back-to-back means the person implementing doesn't need to re-learn the pattern.

### Why Data Analyzer + Writer sweep on Day 2

**Batch similar work.** Items #16, #17, #14, #13 are all spec-hardening changes — adding detection rules, WRONG/RIGHT examples, or clarifying ambiguous language. They touch different files but use the same cognitive pattern. Batching them into one day avoids context-switching between "spec hardening" and "new feature design."

### Why Prioritizer on Days 3–4

**Needs a clean runway.** The Prioritizer is the week's only M-effort new feature. It follows the exact pattern of every existing specialist (pipeline stages + output schema + coordinator routing), so there's no design invention — but it still needs focused time for spec writing, type definition, and validation. Placing it mid-week means all blocking/urgent items are already done, and there's a buffer day (Friday) if it runs long.

### Why #11 on Friday

**Low risk, high independence.** Recipe timeout changes are purely mechanical (bump numbers, replace one step type). They don't block any other item. If Friday gets compressed, #11 is safe to defer — the workaround (re-running timed-out recipes) is annoying but functional.

---

## Task Details

### Task 1: Fix Storyteller OUTPUT CONTRACT Compliance (#30)

**Priority:** HIGH — blocks Epic 03 closure and verification of #18/#19

**Root cause analysis:**
The storyteller spec (`specialists/storyteller/index.md`) already has extensive format requirements:
- Lines 35–41: `⚠️ FORMAT REQUIREMENT — NON-NEGOTIABLE` with WRONG/RIGHT examples
- Lines 53–57: OUTPUT CONTRACT block
- Lines 93–135: Stage 0 template with exact format
- Lines 276–281: Format checklist in Stage 5
- Lines 297–304: Output Format section with `MANDATORY OUTPUT FORMAT` header

Despite all of this, the test run produced **no STORY OUTPUT header, no NARRATIVE SELECTION block, and no QUALITY THRESHOLD RESULT line.** The story prose started with "Here is the board narrative." — a complete structural collapse, not just a header formatting issue.

This tells us the existing instructions are being ignored wholesale. The fix needs to address **structural completeness**, not just the first-line format. The current spec focuses heavily on the first line (`STORY OUTPUT`) but doesn't have equally strong WRONG/RIGHT examples for the **entire structural block** being missing.

**Files:**
- Modify: `specialists/storyteller/index.md`

**The fix — three targeted changes:**

**Change 1: Add WRONG/RIGHT examples for structural completeness (after line 41)**

The current WRONG/RIGHT examples only cover the header format (`# STORY OUTPUT` vs `STORY OUTPUT`). Add examples showing the **complete structural failure mode** — where the model produces bare prose with no structural blocks at all:

```markdown
⚠️ **STRUCTURAL COMPLETENESS — NON-NEGOTIABLE:**
Your response MUST contain ALL of these structural elements. Missing ANY is a spec violation:
1. `STORY OUTPUT` header (first line, plain text)
2. Metadata lines (Input type, Audience, Tone, Framework, Quality threshold)
3. `NARRATIVE SELECTION` section with INCLUDED and OMITTED FINDINGS
4. Story prose (clean paragraphs)
5. `QUALITY THRESHOLD RESULT: MET` or `QUALITY THRESHOLD RESULT: NOT MET`

WRONG (total structural failure — story prose with no structural blocks):
```
Here is the board narrative.

The competitive landscape has shifted dramatically...
```

RIGHT (complete structural output):
```
STORY OUTPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Input type: competitive-analysis-output
Audience: board
...

NARRATIVE SELECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Dramatic question: ...
...

QUALITY THRESHOLD RESULT: MET
```
```

**Change 2: Add a pre-flight check to Stage 0 (before line 96)**

Add an explicit self-check instruction that fires before any thinking:

```markdown
**MANDATORY SELF-CHECK before proceeding:**
You are about to type. The very first characters you produce MUST be `STORY OUTPUT`.
- NOT "Here is..." — VIOLATION
- NOT a title or heading — VIOLATION
- NOT story prose — VIOLATION
If your first instinct is to write a narrative opening, STOP. Type `STORY OUTPUT` instead.
```

**Change 3: Add a post-hoc structural audit to Stage 5 Quality Gate (after line 281)**

After the existing format checklist item, add a structural completeness check:

```markdown
**Structural completeness audit (ZERO TOLERANCE):**
2. Structural blocks present — does your response contain ALL of:
   - `STORY OUTPUT` (first line)
   - `NARRATIVE SELECTION` (section header)
   - `INCLUDED FINDINGS` (subsection)
   - `OMITTED FINDINGS` (subsection)
   - `QUALITY THRESHOLD RESULT:` (final line)
   If ANY block is missing, fail this gate immediately and rewrite from Stage 0.
   A response that contains only story prose is a TOTAL FAILURE — it means
   you skipped every stage of this pipeline.
```

**Verification:**
1. Run a storyteller delegation: provide any AnalysisOutput and request a board narrative
2. Check output starts with literal `STORY OUTPUT` (no `#` prefix)
3. Check output contains `NARRATIVE SELECTION` section
4. Check output contains `INCLUDED FINDINGS` and `OMITTED FINDINGS`
5. Check output ends with `QUALITY THRESHOLD RESULT: MET` or `NOT MET`
6. If all 5 checks pass → #30 is fixed
7. Then verify #18 (inference auditability in NARRATIVE SELECTION) and #19 (quality_threshold parameter) using the same output

---

### Task 2: Fix Writer OUTPUT CONTRACT for Informal Registers (#29)

**Priority:** MEDIUM — prevents `audience: myself` runs from producing parseable output

**Root cause analysis:**
The writer spec (`specialists/writer/index.md`) has a register table at line 220 that says for `myself`/`me`:
> "First-person, direct ... informal prose, personal notes register — **structural blocks (Parsed:, CLAIMS TO VERIFY, WRITER METADATA, CITATIONS) still required**"

The bold note is already there. But in the test run, `audience: myself` produced no `Parsed:` line and no structural blocks at all. The problem is that the register table's "skip formality" language (`informal prose, personal notes register`) was interpreted as blanket permission to skip structural requirements.

The fix needs to be **louder** — a WRONG/RIGHT example specifically for the informal register case, positioned where the model encounters it during drafting.

**Files:**
- Modify: `specialists/writer/index.md`

**The fix — two targeted changes:**

**Change 1: Add WRONG/RIGHT example after the register table (after line 222)**

```markdown
⚠️ **REGISTER ≠ STRUCTURE. These are independent concerns.**
The register table controls VOICE (word choice, sentence style, person).
It does NOT control STRUCTURE (Parsed: line, S-numbered claims, CLAIMS TO VERIFY, WRITER METADATA, CITATIONS).
ALL structural blocks are ALWAYS required — for EVERY audience, including `myself`.

WRONG (informal register interpreted as "skip structure"):
```
Here are my notes on the research.

The key finding is that adoption rates are climbing...
```
No Parsed: line. No S-numbered claims. No WRITER METADATA. No CITATIONS. This is a spec violation.

RIGHT (informal register WITH full structure):
```
Parsed: 8 claims | input=researcher-output | format=brief | audience=myself

S1: Adoption rates increased 40% YoY | confidence: high
S2: Enterprise segment leads growth | confidence: medium
...

Here are my quick takeaways from this research.

The big story is adoption — up 40% year over year...

> *Sources: S1 (adoption rates), S2 (enterprise segment)*

CLAIMS TO VERIFY
S1: "40% YoY" | type: percentage

---

WRITER METADATA
Specialist: writer
...

CITATIONS
S1: "Adoption rates increased 40% YoY" → used in: takeaways | confidence: high (0.9)
...
```
Informal voice ✓ First-person ✓ All structural blocks present ✓
```

**Change 2: Strengthen the OUTPUT CONTRACT block (near line 36)**

The existing OUTPUT CONTRACT says:
> "Your entire response MUST begin with the `Parsed:` parse line."

Add after it:
```markdown
> This requirement applies to ALL audiences and ALL registers — including `myself`, `me`,
> and informal registers. The `Parsed:` line is a pipeline signal, not a formality.
> An informal register changes your VOICE, never your STRUCTURE.
```

**Verification:**
1. Run a writer delegation with `audience: myself` and any ResearchOutput as input
2. Check output starts with `Parsed:` line
3. Check output contains S-numbered claims
4. Check output contains `CLAIMS TO VERIFY` (or `CLAIMS TO VERIFY: none`)
5. Check output contains `WRITER METADATA` block
6. Check output contains `CITATIONS` block
7. Check prose uses first-person voice (not third-person presentation style)
8. If all checks pass → #29 is fixed

---

### Task 3: Prioritizer Specialist (Epic 10)

**Priority:** MEDIUM — new capability, week's headline deliverable

**Design rationale:**
The Prioritizer follows the exact specialist pattern established by Researcher, Writer, Data Analyzer, Storyteller, and Competitive Analysis. It takes a list of items + context, applies a prioritization framework, and returns a structured `PrioritizerOutput` with ranked, justified items.

**Files:**
- Create: `specialists/prioritizer/index.md` — full specialist spec
- Modify: `shared/interface/types.md` — add `PrioritizerOutput` schema
- Modify: `context/specialists-instructions.md` — add routing entry

#### Part A: PrioritizerOutput Schema (types.md)

Add to `shared/interface/types.md` after the StoryOutput section:

```typescript
interface PrioritizerOutput {
  // What was prioritized
  context: string                    // The situation or goal driving prioritization
  framework: 'moscow' | 'rice' | 'impact-effort' | 'weighted-scoring' | 'custom'
  framework_rationale: string        // Why this framework was selected
  items_received: number
  items_ranked: number

  // The ranked output — one entry per item, in priority order
  rankings: RankedItem[]

  // Items that couldn't be meaningfully ranked
  unrankable_items: UnrankableItem[]

  // Overall signal
  quality_threshold_met: boolean
}

interface RankedItem {
  rank: number                       // 1 = highest priority
  item: string                       // The item as received (not modified)
  priority: 'must' | 'should' | 'could' | 'wont'  // MoSCoW mapping (universal)
  score: number | null               // Framework-specific numeric score (null for MoSCoW)
  rationale: string                  // 2-3 sentences: why this rank, what evidence supports it
  framework_scores: FrameworkScore   // Framework-specific breakdown
  dependencies: string[]             // Other items this blocks or is blocked by
}

interface FrameworkScore {
  // RICE scores (null if framework != 'rice')
  reach?: number
  impact?: number
  confidence?: number
  effort?: number

  // Impact-Effort scores (null if framework != 'impact-effort')
  impact_score?: number              // 1-5
  effort_score?: number              // 1-5

  // Weighted scoring (null if framework != 'weighted-scoring')
  weights?: Record<string, number>
  dimension_scores?: Record<string, number>
}

interface UnrankableItem {
  item: string
  reason: 'insufficient_context' | 'out_of_scope' | 'duplicate' | 'not_actionable'
  detail: string                     // One sentence explaining why
}
```

#### Part B: Specialist Spec (specialists/prioritizer/index.md)

The full spec follows the same structure as every other specialist. Key design decisions:

**Pipeline (4 stages):**
1. **Stage 1: Parse** — Extract items, detect or select framework, identify context/constraints
2. **Stage 2: Score** — Apply framework scoring to each item independently
3. **Stage 3: Rank** — Order by score, resolve ties, identify dependencies
4. **Stage 4: Quality Gate** — Verify every item is accounted for (ranked or unrankable), check for obvious ranking errors (high-dependency items ranked after their dependents)

**Framework selection logic:**
- If caller specifies a framework → use it
- If items have numeric reach/impact data → default to RICE
- If items are features/tasks with effort estimates → default to impact-effort
- If items are requirements or backlog items → default to MoSCoW
- Otherwise → default to impact-effort (simplest general-purpose framework)

**Output format:**
```
PRIORITIZER OUTPUT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Context: [the situation or goal]
Framework: [moscow | rice | impact-effort | weighted-scoring | custom]
Framework rationale: [why this framework]
Items received: [n]
Items ranked: [n]

RANKINGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#1: [item text]
    Priority: must | Score: [n] | Dependencies: [items]
    Rationale: [2-3 sentences]

#2: [item text]
    Priority: should | Score: [n] | Dependencies: [items]
    Rationale: [2-3 sentences]

[one block per ranked item]

UNRANKABLE ITEMS
[item]: reason: [type] — [detail]
[or "none"]

QUALITY THRESHOLD RESULT: [MET | NOT MET]
```

**Core principles (from spec):**
- **Every item accounted for.** Either ranked or listed as unrankable with reason. Nothing silently dropped.
- **Rationale is the product.** The ranking itself is trivial — the value is in the justification. Each rationale must reference specific evidence from the items or context, not generic prioritization language.
- **Framework is a lens, not a cage.** The framework structures the scoring, but obvious practical considerations (dependencies, deadlines, blockers) override framework-only scores. Document any overrides.
- **Fails loud, not silent.** If items lack enough context for meaningful prioritization (no goals, no constraints, generic descriptions), emit `QUALITY THRESHOLD RESULT: NOT MET` with specifics on what's missing.

#### Part C: Coordinator Routing (context/specialists-instructions.md)

Add to the Available Specialists list:
```markdown
- **prioritizer** — Ranks and justifies a list of items using a prioritization framework
  (MoSCoW, RICE, impact/effort, weighted scoring, or caller-specified). Returns
  `PrioritizerOutput` with every item ranked with score, rationale, and dependencies,
  or listed as unrankable with reason. Use when the caller needs structured prioritization,
  not just a list.
```

Add to the "When to Use Each" section:
```markdown
**Delegate to `specialists:specialists/prioritizer` when:**
- The user has a list of items and needs them ranked by priority
- Backlog grooming, roadmap planning, feature triage
- Any situation where "what should we do first?" needs a structured, justified answer
- The user specifies a prioritization framework (MoSCoW, RICE, etc.)
```

Add the agent ID to the delegation list on line 32:
```
`specialists:specialists/prioritizer`
```

**Verification:**
1. Provide the Prioritizer with 8-10 backlog items and a context sentence
2. Check output starts with `PRIORITIZER OUTPUT`
3. Check every input item appears in RANKINGS or UNRANKABLE ITEMS
4. Check each ranked item has a rationale that references specific item/context details
5. Check framework was selected and rationalized
6. Check `QUALITY THRESHOLD RESULT` line is present
7. Run a second test with `framework: rice` explicitly specified — confirm it uses RICE

---

### Task 4: Recipe Timeout Resilience (#11)

**Priority:** MEDIUM — affects broad-topic research chains

**Root cause analysis:**
`research-chain.yaml` has these timeouts:
- research: 2700s (45 min)
- format-research: 600s (10 min)
- analyze: 900s (15 min)
- write: 900s (15 min) ← **this is the ceiling that causes timeouts**
- save: 120s (2 min) ← **uses LLM agent for a file-save operation**

The `narrative-chain.yaml` already addressed some of these (research bumped to 4500s, format to 1200s, save to 300s). But `research-chain.yaml` hasn't been updated.

Additionally, the save step in both recipes uses `foundation:file-ops` (an LLM agent) to perform what is essentially `mkdir -p && cat > file`. This is fragile under LLM back-pressure and adds unnecessary latency.

**Files:**
- Modify: `recipes/research-chain.yaml`
- Modify: `recipes/narrative-chain.yaml` (save step only)

**The fix — two changes:**

**Change 1: Bump research-chain.yaml timeouts to match narrative-chain.yaml**

```yaml
# research step: 2700 → 4500 (match narrative-chain)
# format-research step: 600 → 1200 (match narrative-chain)
# write step: 900 → 1800 (2× — this was the bottleneck)
# save step: 120 → 300 (match narrative-chain)
```

Also add scope constraints to the research step prompt (matching narrative-chain):
```yaml
prompt: |
  ...
  Scope constraints (required — enforce in Stage 1):
  - Decompose into no more than 5 sub-questions
  - Cap your source queue at 15 URLs total across all sub-questions
  - Run no more than 2 Quality Gate cycles before accepting remaining gaps
  - Target a maximum of 3,000 words and 30 sourced claims in your final output
```

**Change 2: Replace LLM-based save step with bash step in both recipes**

Replace the `foundation:file-ops` agent save step with a deterministic bash step:

```yaml
- id: "save"
  type: "bash"
  command: |
    # Derive filename from research question (first 5 words, kebab-case)
    slug=$(printf '%s' '{{research_question}}' | \
      tr '[:upper:]' '[:lower:]' | \
      sed 's/[^a-z0-9 ]//g' | \
      awk '{for(i=1;i<=5&&i<=NF;i++) printf "%s%s",$i,(i<5&&i<NF?"-":""); print ""}')
    # Ensure slug isn't empty
    [ -z "$slug" ] && slug="research-output"
    mkdir -p docs/research-output
    filepath="docs/research-output/${slug}.md"
    cat > "$filepath" <<'__SAVE_EOF__'
    {{final_document}}
    __SAVE_EOF__
    echo "Saved to: $filepath"
  output: "output_path"
  timeout: 30
```

This eliminates the LLM dependency from the save step entirely. The filename derivation is deterministic (first 5 words of the research question, kebab-cased). The timeout drops from 120–300s to 30s.

**Verification:**
1. Run `research-chain.yaml` with a broad topic (e.g., "What is the current state of AI regulation globally?")
2. Confirm the chain completes without timeout
3. Confirm the saved file exists at the expected path
4. Confirm the saved file content matches the writer output (no truncation)
5. Run `narrative-chain.yaml` with the same topic — same checks

---

### Task 5: Data Analyzer Format B Hardening (#16) + Code-Fence Prevention (#17)

**Priority:** MEDIUM — improves robustness for non-canonical inputs and outputs

**Root cause analysis for #16:**
The data-analyzer spec (`specialists/data-analyzer/index.md`) has Format B detection at lines 88–108 for "narrative markdown." The extraction rules say to scan for:
- Rows in markdown tables with source and confidence columns
- Bullet points with inline source attribution
- Named claims with Source/Tier/Confidence labels

The gap: when the input is **pure narrative** (no tables, no structured bullets, no explicit labels), the extraction rules have no fallback. The model may either (a) extract nothing and produce an empty FINDINGS section, or (b) hallucinate structure that isn't there.

**Root cause analysis for #17:**
The spec says at line 202–204: "Return this exact structure — no narrative prose, no code fence wrapping." But there's no WRONG/RIGHT example and no Quality Gate check for code fences. Models frequently wrap structured output in code fences as a "helpful" formatting gesture.

**Files:**
- Modify: `specialists/data-analyzer/index.md`

**The fix for #16 — add a Format B fallback clause (after line 108):**

```markdown
**Format B fallback — when narrative lacks explicit structure:**
If the input is narrative markdown with NO tables, NO explicit Source/Tier/Confidence
labels, and NO structured bullets:
1. Scan for discrete factual assertions (not opinions, not transitions)
2. For each assertion: extract the claim text as-is
3. Source: extract any inline URL or named publication; default to `unknown`
4. Tier: infer from source type if identifiable; default to `tertiary`
5. Confidence: default to `low` — unstructured narrative with no explicit confidence
   signal gets the lowest default
6. Emit parse summary noting `format=B (narrative fallback)` so downstream consumers
   know the extraction was best-effort

If fewer than 3 discrete claims can be extracted, emit:
`QUALITY THRESHOLD RESULT: NOT MET` with reason: "Input is narrative with insufficient
discrete claims for meaningful analysis. Consider running through the Researcher first."
```

**The fix for #17 — add WRONG/RIGHT examples and Quality Gate check:**

Add after line 204 (the "no code fence wrapping" instruction):

```markdown
WRONG (output wrapped in code fences):
```
```
ANALYSIS OUTPUT
Specialist: data-analyzer
...
```
```

RIGHT (plain text, no wrapping):
```
ANALYSIS OUTPUT
Specialist: data-analyzer
...
```

If your output begins with ``` (triple backtick) — STOP, delete the backticks, and emit
the block as plain text. Code fences break downstream parsers.
```

Add to Stage 3 Quality Gate (after line 198), a new check:

```markdown
5. **Format check:** Does your output begin with `ANALYSIS OUTPUT` as plain text (no
   code fences, no markdown headers)? If it begins with ``` — rewrite without fences.
```

**Verification for #16:**
1. Provide the Data Analyzer with a pure narrative markdown document (no tables, no labels)
2. Check that findings are extracted with `confidence: low` defaults
3. Check parse summary shows `format=B (narrative fallback)`
4. Check QUALITY THRESHOLD RESULT is present

**Verification for #17:**
1. Run any Data Analyzer delegation
2. Confirm output starts with `ANALYSIS OUTPUT` as plain text
3. Confirm no triple-backtick code fences anywhere in the output

---

### Task 6: Writer Structural Sections for Analysis Input (#14)

**Priority:** MEDIUM — clarifies ambiguous spec for analysis-based inputs

**Root cause:**
When the writer receives `analysis-output` as input, it's unclear whether WRITER METADATA, CITATIONS, and CLAIMS TO VERIFY are still required. The spec says they're always required (Output Structure section, lines 62–77), but the `analysis-output` handling in Stage 1 (lines 162–164) doesn't explicitly restate this.

**Files:**
- Modify: `specialists/writer/index.md`

**The fix — add explicit reinforcement in the analysis-output handling section:**

After line 164, add:
```markdown
   **Structural blocks for analysis-output:** All structural blocks (Parsed: line,
   S-numbered claims, CLAIMS TO VERIFY, WRITER METADATA, CITATIONS) are required.
   The analysis-output input type changes how you EXTRACT claims (from findings and
   inferences), not whether you PRODUCE structural blocks.
```

**Verification:**
1. Run writer with an AnalysisOutput as input
2. Confirm all structural blocks present

---

### Task 7: Writer Parse-Line Ordering Documentation (#13)

**Priority:** SMALL — documentation accuracy

**Root cause:**
The spec already mandates `Parsed:` as the first line (Stage 0, lines 120–134). But the Output Structure section (line 66) lists it as item 1, while the Output Format section (line 330) shows it in a code block. The documentation is technically correct but could be clearer about the **why** of parse-line-first ordering.

**Files:**
- Modify: `specialists/writer/index.md`

**The fix:** Minor clarification — add a one-line note to the Output Structure section:

```markdown
**Why Parsed: comes first:** The parse line is a machine-readable signal for pipeline
orchestration. It is emitted BEFORE analysis begins — not computed after the fact.
This is the only structural block that precedes the document content.
```

**Verification:** Read the spec and confirm the ordering is unambiguous.

---

### Task 8: Writer Deduplication Pass (#15)

**Priority:** MEDIUM — reduces redundancy in writer output

**Root cause:**
The writer spec already has a deduplication check in Stage 5 (lines 268–272). But it's item 6 in a 10-item checklist, making it easy to skip under cognitive load. The check says "scan for repeated claims" but doesn't specify HOW to detect duplicates.

**Files:**
- Modify: `specialists/writer/index.md`

**The fix — strengthen the dedup check with specific detection rules:**

Replace lines 268–272 with:
```markdown
6. **Deduplication check (3-pass scan):**
   Before writing the CITATIONS block, scan the document for repeated claims:
   **Pass 1 — Exact repeats:** Search for any S-numbered claim whose core assertion
   appears verbatim in more than one section. Remove all but the first occurrence.
   **Pass 2 — Semantic repeats:** Search for claims restated in different words
   (e.g., "revenue grew 40%" in the summary and "40% revenue increase" in findings).
   Consolidate into the stronger phrasing; remove the weaker.
   **Pass 3 — Attribution-line repeats:** Check that no Sn appears in attribution
   lines for sections where it wasn't actually used in the prose.
   After dedup, verify the document still covers all required points. If removing a
   duplicate leaves a section unsupported, keep the stronger instance.
```

**Verification:**
1. Run writer with a source that contains overlapping findings
2. Check no claim appears twice in different sections
3. Check attribution lines only reference claims actually used in that section

---

## Scope Assessment

### Committed (shipping this week — high confidence)

| Item | Day | Confidence |
|------|-----|------------|
| **#30** — Storyteller OUTPUT CONTRACT | Mon | 95% — proven fix pattern, same technique as Writer's earlier fix |
| **#18/#19 verification** — unblocked by #30 | Mon | 90% — just needs a test run |
| **#29** — Writer informal register | Mon | 95% — same fix pattern as #30 |
| **#16** — Data Analyzer Format B hardening | Tue | 95% — additive spec change, no breaking changes |
| **#17** — Data Analyzer code-fence prevention | Tue | 95% — WRONG/RIGHT example addition |
| **#14** — Writer structural sections | Tue | 95% — one-paragraph reinforcement |
| **#13** — Writer parse-line ordering | Tue | 95% — documentation clarification |
| **Prioritizer spec** — Epic 10 spec + types + routing | Wed | 90% — follows established pattern |
| **#15** — Writer dedup pass | Thu | 90% — strengthening existing check |

**Total committed: 9 items (7 backlog items + 2 verifications)**

### Stretch (shipping if pace is fast)

| Item | Day | Confidence |
|------|-----|------------|
| **#11** — Recipe timeout resilience | Fri | 70% — mechanical changes but needs testing |
| **Prioritizer test run + iteration** | Thu | 75% — depends on first-run quality |
| **Prioritizer recipe** (`prioritize-chain.yaml`) | Fri | 50% — nice-to-have, not blocking |
| **Full chain verification sweep** | Fri | 60% — depends on how clean the week was |

### What gets deferred if the week gets compressed

If days are lost to unexpected issues:
1. **First to defer:** Prioritizer recipe (not blocking, specialist works without it)
2. **Second to defer:** #11 recipe timeout (workaround exists — re-run timed-out recipes)
3. **Third to defer:** Full chain verification (can be next Monday morning)
4. **Never defer:** #30, #29, Prioritizer spec — these are the week's core commitments

---

## Epic Status After This Week

| Epic | Before | After | Notes |
|------|--------|-------|-------|
| 01 — Researcher | 95% | 95% | No changes (architectural reality accepted) |
| 02 — Writer | 80% | 95% | #29, #14, #15, #13 close most remaining gaps |
| 03 — Storyteller | 90% | **100%** | #30 fixes compliance, #18/#19 verified |
| 04 — Competitive Analysis | 100% | 100% | No changes |
| 08 — Data Analyzer | 100% | 100% | #16/#17 are hardening, not new capability |
| 10 — Prioritizer | 0% | **80%** | Spec + types + routing shipped; recipe is stretch |

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| #30 fix doesn't hold — model still ignores format instructions | Medium | High | The narrative-chain.yaml already has bash post-processing for header normalization. If prompt-level fix isn't enough, add a similar bash normalization step that injects missing structural blocks. |
| Prioritizer first run reveals design gaps | Medium | Medium | Day 4 is explicitly reserved for iteration. The spec follows a proven pattern, so gaps should be small. |
| Recipe timeout changes break working recipes | Low | Medium | Only changing timeout numbers and one step type. Test both recipes after changes. |
| Broad-topic research still times out even with bumped timeouts | Medium | Low | The scope constraints (5 sub-questions, 15 URLs, 3000 words) are the real fix. Timeouts are the safety net. |

---

## Execution Notes

**Commit strategy:** One commit per backlog item. Commit message format: `fix(specialist): #NN description` for fixes, `feat(specialist): description` for new features.

**Test strategy:** Each fix is verified by running the relevant specialist delegation and checking the output against the verification criteria listed in each task. No automated tests for prompt-based fixes (these are instruction changes, not code changes). Log all test runs to `docs/test-log/`.

**Backlog updates:** Update `docs/BACKLOG.md` after each item ships — move from "Open" to "Closed", update epic completion percentages. Final backlog update on Friday.