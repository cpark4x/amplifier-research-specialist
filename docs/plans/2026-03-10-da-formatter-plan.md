# data-analyzer-formatter Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build the `data-analyzer-formatter` specialist — a format normalization stage that receives DA output in any format plus the original research, and produces a canonical `ANALYSIS OUTPUT` block every time.

**Architecture:** 2-input formatter following the established pattern (story-formatter, writer-formatter, prioritizer-formatter). Stage 0 opens with `ANALYSIS OUTPUT` immediately. Three input-format cases: canonical (pass-through with validation), partial (fill gaps), narrative (extract inferences, mark traces_to as uncertain). Never re-analyzes, never draws new inferences.

**Design doc:** `docs/plans/2026-03-10-da-formatter-design.md`

**Files touched:** 4 files across specialists/, behaviors/, context/, and recipes/

---

## Task 1: Build `specialists/data-analyzer-formatter/index.md`

**Files:**
- Create: `specialists/data-analyzer-formatter/index.md`

**Reference before writing:**
- Read `specialists/story-formatter/index.md` — closest structural match (2-input, Stage 0 opens with block header)
- Read `specialists/prioritizer-formatter/index.md` — most recently written, clearest template
- Read `specialists/data-analyzer/index.md` — understand the ANALYSIS OUTPUT block structure you must produce

**Step 1: Write the formatter file**

The file must contain, in order:

1. **Frontmatter** (`meta:` block):
   ```yaml
   ---
   meta:
     name: data-analyzer-formatter
     description: |
       Essential pipeline stage — always runs after the data-analyzer. Receives
       DA output in any format (canonical ANALYSIS OUTPUT block, partial block,
       narrative prose/essay) plus the original research input, and produces a
       canonical ANALYSIS OUTPUT block. Never re-analyzes — only extracts,
       validates, and reformats.

       The data-analyzer focuses on inference quality. This specialist focuses on
       ensuring that analytical output arrives in the exact structured format
       downstream agents and parsers depend on. These are two different cognitive tasks.

       Input: (1) DA output in any format, (2) original research input (RESEARCH OUTPUT
              or Format B narrative)
       Output: canonical ANALYSIS OUTPUT block, always
   ---
   ```

2. **Role statement** — "You are the format normalization stage of the analysis pipeline. Every DA output passes through you before reaching any downstream step." You do not analyze. You do not draw inferences. You extract, validate, reformat.

3. **Core Principle** — "Extract, don't generate. Normalize everything." No pass-through mode.

4. **Stage 0 — Open your response:**
   Write `ANALYSIS OUTPUT` as the **literal first line** of your response. Nothing before it.

5. **Stage 1 — Parse inputs:**
   - Detect DA output format:
     - `canonical` — starts with `ANALYSIS OUTPUT` on the very first line AND contains all required sections (FINDINGS, INFERENCES, UNUSED FINDINGS, EVIDENCE GAPS, QUALITY THRESHOLD RESULT)
     - `partial` — contains `ANALYSIS OUTPUT` header but one or more required sections are missing
     - `narrative` — essay, prose, `## Section` headers, no canonical structure (also covers: stage narration only, with no block)
   - Strip stage narration prefix: if DA response starts with `**Stage` or `Stage 1:` or similar, find first occurrence of `ANALYSIS OUTPUT` and discard everything before it. If no `ANALYSIS OUTPUT` found, treat as `narrative`.
   - From **original research input**: re-extract F1-Fn findings as the authoritative list (same Format A / B / C detection logic as the DA's own Stage 1)
   - Emit parse summary as the line immediately after the `ANALYSIS OUTPUT` header:
     ```
     Parsed: [n] findings | da-format=[canonical|partial|narrative] | [n] inferences detected
     ```

6. **Stage 2 — Extract inferences:**

   **For `canonical` input:**
   - Pull inferences directly from the DA's INFERENCES section
   - Validate each `traces_to` — ensure referenced IDs exist in the F1-Fn list from original research
   - If a referenced ID doesn't exist: flag it as `traces_to: [ID-not-found]`
   - Normalize inference type to valid values: `pattern|causal|evaluative|predictive` only

   **For `partial` input:**
   - Same as canonical for sections that are present
   - For missing FINDINGS section: use F1-Fn from original research
   - For missing INFERENCES section: mark as empty — do not invent inferences
   - For missing UNUSED FINDINGS: compute from F1-Fn not referenced in any `traces_to`

   **For `narrative` input:**
   - Read the DA prose for evaluative/conclusion statements (look for: "X is positioned to...", "The evidence suggests...", "This indicates...", "X outperforms Y because...", "The pattern shows...")
   - Extract each as an inference entry:
     ```
     inference: [statement extracted from DA prose] | type: [pattern|causal|evaluative|predictive] | confidence: [high|medium|low] | traces_to: [narrative-mapped: uncertain]
     ```
   - Infer type: judgment/comparison → `evaluative`; trend/convergence → `pattern`; mechanism/driver → `causal`; forward-looking → `predictive`
   - Infer confidence from DA language: "clearly", "strongly" → `high`; "suggests", "indicates" → `medium`; "may", "could", "possibly" → `low`
   - If no inferential statements found in the narrative: produce `INFERENCES: none` — do not invent

7. **Stage 3 — Produce canonical ANALYSIS OUTPUT block:**

   Continue directly after the parse summary line. Produce the complete block:

   ```
   Specialist: data-analyzer
   Version: 1.0

   ANALYSIS BRIEF
   ━━━━━━━━━━━━━━━━━━━━━━━━━━
   Question: [from original research or DA narrative — infer from topic if not explicit]
   Focus: [from DA output, or "full research" if not stated]
   Findings received: [count of F1-Fn from original research]
   Inferences drawn: [count of inferences from Stage 2]
   Quality score: [high if all inferences high confidence | medium if any medium and none low | low if any low or no inferences drawn]
     Derivation: [one sentence explaining the score]

   FINDINGS
   F1: claim: [exact text] | source: [URL or unattributed] | tier: [primary|secondary|tertiary] | confidence: [high|medium|low]
   F2: ...
   [one line per finding — from original research, not from DA output]

   INFERENCES
   inference: [claim] | type: [pattern|causal|evaluative|predictive] | confidence: [high|medium|low] | traces_to: [F3, F7 — or narrative-mapped: uncertain]
   [one line per inference — or "none" if none extracted]

   UNUSED FINDINGS
   F5: reason: [contradicted|insufficient_evidence|out_of_scope|narrative-untraced] — [one sentence]
   [one line per unused finding — or "none" if all findings traced]
   Note: for narrative input, any finding not semantically referenced by extracted inferences → reason: narrative-untraced

   EVIDENCE GAPS
   gap: [what couldn't be found] | reason: [why]
   [from DA if present; from original research if not; "none" if neither source names gaps]

   QUALITY THRESHOLD RESULT: [MET | NOT MET]
   MET if: at least one inference extracted AND all findings accounted for (in INFERENCES or UNUSED FINDINGS)
   NOT MET if: DA output so incoherent that no recognizable inferences could be extracted
   ```

8. **"What You Do Not Do" section:**
   - Re-analyze findings
   - Draw new inferences not present in DA output
   - Upgrade or downgrade inference confidence beyond what DA language supports
   - Invent finding IDs not in original research
   - Produce anything other than ANALYSIS OUTPUT block
   - Wrap output in code fences
   - Add explanatory text outside the block
   - Begin your response with anything other than `ANALYSIS OUTPUT`

**Step 2: Spot-check the file structure**

Verify the file contains, in order:
- `---` frontmatter with `meta.name: data-analyzer-formatter`
- Role statement paragraph
- Core Principle section
- Stage 0 through Stage 3
- "What You Do Not Do" section

**Step 3: Commit**

```bash
git add specialists/data-analyzer-formatter/index.md
git commit -m "feat: build data-analyzer-formatter specialist (#34) — fifth formatter, handles canonical/partial/narrative DA output"
```

---

## Task 2: Register in `behaviors/specialists.yaml`

**Files:**
- Modify: `behaviors/specialists.yaml`

**Step 1: Read the current file**

```bash
cat behaviors/specialists.yaml
```

Look at how the other formatters are registered (researcher-formatter, story-formatter, writer-formatter, prioritizer-formatter). Copy that pattern exactly.

**Step 2: Add entry**

Add `data-analyzer-formatter` following the same structure as the other formatter entries. Place it adjacent to the `data-analyzer` entry (logically paired).

**Step 3: Commit**

```bash
git add behaviors/specialists.yaml
git commit -m "feat: register data-analyzer-formatter in behaviors/specialists.yaml"
```

---

## Task 3: Update `context/specialists-instructions.md`

**Files:**
- Modify: `context/specialists-instructions.md`

**Step 1: Read the current file**

```bash
cat context/specialists-instructions.md
```

You're looking for 4 things to add:
1. Rule 8 (the mandatory gate, matching Rules 5-7)
2. Description for `data-analyzer-formatter` in the Available Specialists section
3. Entry in the Typical Chain section
4. Agent ID (`specialists:data-analyzer-formatter`) in the Use these exact agent IDs line

**Step 2: Add Rule 8**

After Rule 7 (prioritizer-formatter mandatory gate), add:

```
**Rule 8 — Data-Analyzer-Formatter Is Always In The Path**: The data-analyzer and
data-analyzer-formatter are a matched pair by design — the data-analyzer produces
labeled inferences from research evidence, the data-analyzer-formatter canonicalizes
it into the structured ANALYSIS OUTPUT block downstream agents and parsers depend on.
When the data-analyzer's output feeds ANY downstream step or the user, **always**
route through `specialists:data-analyzer-formatter` first. This is the
designed architecture, not optional.

**Mandatory gate — before delivering data-analyzer output to the user or any downstream
agent:** Stop and answer: "Did I route through data-analyzer-formatter?" If the answer
is no — run data-analyzer-formatter now before proceeding.
```

**Step 3: Add description to Available Specialists section**

Following the `data-analyzer` entry, add:

```
- **data-analyzer-formatter** — Essential pipeline stage. Receives data-analyzer output
  in any format (canonical ANALYSIS OUTPUT block, partial block, narrative prose/essay)
  plus the original research input and produces a canonical ANALYSIS OUTPUT block.
  Classifies which findings are traced, untraced, or narrative-mapped. Never re-analyzes,
  never draws inferences — only extracts, validates, and reformats. Always runs after
  the data-analyzer — this is the designed architecture, not optional.
```

**Step 4: Add to Typical Chain entries**

In the Typical Chain section, add a chain entry showing the full analysis pipeline:

```
For full analysis chain (facts and inferences explicitly separated):
1. `specialists:researcher` → gathers and validates evidence
2. `specialists:researcher-formatter` → normalizes to canonical format (Rule 5)
3. `specialists:data-analyzer` → draws labeled inferences from evidence
4. `specialists:data-analyzer-formatter` → normalizes to canonical ANALYSIS OUTPUT (Rule 8)
5. `specialists:writer` → transforms analysis into requested document
6. `specialists:writer-formatter` → normalizes to canonical Writer output block (Rule 6)
```

**Step 5: Add agent ID**

In the "Use these exact agent IDs" line (or equivalent list), add: `specialists:data-analyzer-formatter`

**Step 6: Commit**

```bash
git add context/specialists-instructions.md
git commit -m "feat: add Rule 8 + data-analyzer-formatter description to specialists-instructions"
```

---

## Task 4: Update `recipes/research-chain.yaml`

**Files:**
- Modify: `recipes/research-chain.yaml`

**Step 1: Read the current recipe**

```bash
cat recipes/research-chain.yaml
```

Find the step that invokes the data-analyzer. You need to:
1. Confirm what context variables hold the DA output and original research
2. Insert a new `data-analyzer-formatter` step immediately after the DA step
3. Pass both inputs: DA output (from previous step) + original research (from earlier in the chain)

**Step 2: Add the da-formatter step**

Insert a new step after the data-analyzer step. The step should:
- Use agent `specialists:data-analyzer-formatter`
- Receive DA output from the previous step's output variable
- Receive original research from the formatter step earlier in the chain (the research-chain already has a researcher-formatter step — its output is the original research)
- Store output in a new context variable (e.g., `analyzed_output` or `da_formatted_output`)

Update any subsequent steps that previously consumed DA output directly to consume the new da-formatter output variable instead.

**Step 3: Validate the recipe YAML**

```bash
# If there's a validation tool:
amplifier tool invoke recipes operation=validate recipe_path=recipes/research-chain.yaml
```

If no validation tool available, visually inspect that:
- All step output variables match subsequent step input references
- The new step is correctly positioned
- YAML indentation is consistent

**Step 4: Commit**

```bash
git add recipes/research-chain.yaml
git commit -m "feat: add data-analyzer-formatter step to research-chain recipe (#34)"
```

---

## Task 5: Spot Test

**Goal:** Verify the formatter produces canonical ANALYSIS OUTPUT from a narrative DA response.

**Step 1: Prepare the test inputs**

You need two inputs:
1. A narrative DA response (the failure mode) — use this as the DA output:
   ```
   **Stage 1: Parse**
   Analyzing the research on Mistral AI...

   ## Competitive Position
   🟢 Mistral AI occupies a unique position in the open-source LLM market.
   The company's hybrid deployment strategy (cloud API + on-premise) differentiates
   it from pure-play API providers.

   ## Key Strengths
   🟡 Technical performance is competitive with GPT-3.5 class models at lower cost.
   European regulatory positioning gives enterprise customers a GDPR-compliant alternative.

   ## Strategic Risk
   🔴 Mistral faces commoditization pressure as open-source weights proliferate.

   | Factor | Assessment |
   |--------|-----------|
   | Technical moat | Medium |
   | Market position | Strong in EU |
   | Revenue model | Unproven at scale |
   ```

2. A simple RESEARCH OUTPUT as the original research — any short canonical RESEARCH OUTPUT block with 3-5 findings about Mistral AI.

**Step 2: Invoke the formatter in a session**

Delegate to `specialists:data-analyzer-formatter` with both inputs. Observe:
- Does output start with `ANALYSIS OUTPUT`?
- Is the parse summary line present and correctly identifies `da-format=narrative`?
- Are FINDINGS re-extracted from the original research (not from the DA narrative)?
- Are inferences extracted from the DA prose with `type: evaluative` and `traces_to: [narrative-mapped: uncertain]`?
- Are all FINDINGS accounted for in INFERENCES or UNUSED FINDINGS?
- Is `QUALITY THRESHOLD RESULT: MET` or `NOT MET` present?
- Are there no code fences around the block?

**Step 3: Log results**

Create `docs/test-log/data-analyzer/2026-03-10-da-formatter-spot-test.md` with:
- Test inputs summary
- Pass/fail per check above
- Any issues found and action items

**Step 4: Commit the test log**

```bash
git add docs/test-log/data-analyzer/2026-03-10-da-formatter-spot-test.md
git commit -m "docs: da-formatter spot test — [PASS|FAIL] + findings"
```

---

## Task 6: Update BACKLOG.md and SCORECARD.md

**Files:**
- Modify: `docs/BACKLOG.md`
- Modify: `docs/SCORECARD.md`

**Step 1: Close #34 in BACKLOG.md**

In the Near-term Priority 3 table, strike through item #34 and add a completion note:

```
| ~~34~~ | ~~Data Analyzer: da-formatter specialist (architectural fix)~~ | 08 | Chris | S | H | **Shipped 2026-03-10.** `specialists/data-analyzer-formatter/index.md` built — fifth application of formatter pattern. Handles canonical/partial/narrative DA output. Registered in `behaviors/specialists.yaml`. Rule 8 added to `specialists-instructions.md`. Step added to `research-chain` recipe. *(test log 2026-03-10-da-formatter-spot-test)* |
```

Also add to Recently Completed table.

Update the Change History entry.

**Step 2: Update SCORECARD.md**

Based on what was built:
- **Format Fidelity**: DA now has architectural formatter catch → move from 9/10 to **10/10**
- **Chain Reliability**: DA input-framing sensitivity resolved → move from 8/10 to **9/10**
- **Research Trustworthiness**: DA formatter closes the last open gap in the analysis chain → assess whether end-to-end chain is now validated; if spot test passed, consider moving from 3/10 to **4/10** (partial credit — da-formatter built, but full chain end-to-end not yet validated)
- **Overall**: Recalculate equal-weight average

Update the Score History table with a new row for today.

**Step 3: Commit**

```bash
git add docs/BACKLOG.md docs/SCORECARD.md
git commit -m "docs: close #34 (da-formatter), update scorecard"
```

---

## Task 7: Final Commit and Cleanup

**Step 1: Verify all files committed**

```bash
git status
```

Expected: clean working tree. If any untracked or modified files remain, review and commit or discard.

**Step 2: Review the full changeset**

```bash
git log --oneline -6
```

You should see 5-6 commits from this work:
1. `feat: build data-analyzer-formatter specialist (#34)`
2. `feat: register data-analyzer-formatter in behaviors/specialists.yaml`
3. `feat: add Rule 8 + data-analyzer-formatter description to specialists-instructions`
4. `feat: add data-analyzer-formatter step to research-chain recipe (#34)`
5. `docs: da-formatter spot test — PASS + findings`
6. `docs: close #34 (da-formatter), update scorecard`

**Step 3: Confirm no regression**

Check that the `behaviors/specialists.yaml` still references all 5 formatters and that the `context/specialists-instructions.md` rules section is complete (Rules 5-8 all present).

---

## Success Criteria

- [ ] `specialists/data-analyzer-formatter/index.md` exists and follows the 4-stage pipeline
- [ ] Stage 0 opens with literal `ANALYSIS OUTPUT` — no preamble
- [ ] Three input cases documented (canonical / partial / narrative)
- [ ] Option A implemented: `traces_to: [narrative-mapped: uncertain]` for narrative case — never invented IDs
- [ ] Stage narration strip logic present
- [ ] Registered in `behaviors/specialists.yaml`
- [ ] Rule 8 present in `context/specialists-instructions.md`
- [ ] `research-chain.yaml` includes da-formatter step between DA and Writer
- [ ] Spot test passes: narrative DA input → canonical ANALYSIS OUTPUT
- [ ] Backlog #34 closed, scorecard updated
- [ ] Clean git history with 5-6 focused commits
