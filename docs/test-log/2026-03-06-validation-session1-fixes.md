# Test Log: Session 1 Fix Validation

**Date:** 2026-03-06
**Type:** Validation test — verifying backlog #5, #6, #27 fixes from Session 1
**Verdict:** 1 PASS, 1 PARTIAL, 1 NOT TESTED

---

## Test Design

Ran 4 parallel delegates to validate the three sprint items shipped in Session 1:

| Test | Target Fix | Method |
|---|---|---|
| Researcher x3 (Jina AI, Anthropic RSP, Rust borrow checker) | #5 — confidence tiers + URLs | Direct delegation to `specialists:researcher` |
| Writer x1 (canned Rust input, format=brief) | #6 — word budget enforcement | Direct delegation to `specialists:writer` with 5-claim input |

#27 (formatter gate) was not directly testable — the gate is in coordinator instructions and requires a live chat session, not a direct delegation test.

---

## Results

### #6 — Writer Word Budget: PASS

| Metric | Result | Budget |
|---|---|---|
| Format | brief | brief |
| Word count | **316** | 250–400 |
| Structure | Summary → Key Points → Implications → Next Steps | Matches brief template |
| Starts with `Parsed:` | Yes | Required |
| WRITER METADATA present | Yes | Required |
| CITATIONS present | Yes, all 5 S-numbers accounted for | Required |
| CLAIMS TO VERIFY | "none" (correct for researcher-output input) | Required |
| Confidence distribution | 5 high · 0 medium · 0 low · 0 unrated · 0 inference | No unrated |

**Verdict: PASS.** Word budget is enforced. Brief no longer reads like a report.

---

### #5 — Researcher Trustworthiness: PARTIAL

**What worked:**
- `unrated` is gone — zero instances across all 3 runs (was 142/142 in pre-fix Mar 6 test)
- URLs are present — all 3 outputs have real `https://` links to source material
- Source quality is high — Anthropic run had 14 sources across 3 tiers, Rust run had 12

**What didn't work:**
- **Confidence tiers are numeric, not categorical.** All 3 researchers used values like `0.97`, `0.93`, `0.80` instead of `high`, `medium`, `low`. The model dodged the categorical system entirely.
- **Output is narrative, not canonical RESEARCH OUTPUT format.** Zero of 3 runs produced the structured FINDINGS block format (Claim/Source/Tier/Confidence per entry). All produced narrative documents with inline confidence notes.
- **Opening anchor is wrong.** Zero of 3 runs started with plain `RESEARCH OUTPUT`. All started with `---` or `# RESEARCH OUTPUT:` (markdown heading).
- **Tier labels are abbreviated.** All 3 used "T1/T2/T3" instead of "primary/secondary/tertiary".

| Check | Jina AI | Anthropic RSP | Rust Borrow Checker |
|---|---|---|---|
| Starts with `RESEARCH OUTPUT` (plain text) | NO — `---` + `##` header | NO — `---` + `##` header | NO — `---` + `#` header |
| FINDINGS block format | NO — narrative sections | NO — narrative sections | NO — narrative sections |
| Confidence: high/medium/low | NO — numeric (0.88–0.97) | NO — numeric (0.90–0.97) | NO — numeric (0.80–0.99) |
| Tier: primary/secondary/tertiary | NO — "Tier 1/2/3" or "T1/T2/T3" | NO — "T1/T2/T3" | NO — "T1/T2/T3" |
| Source URLs present | YES — inline | YES — source registry | YES — source registry |
| `unrated` absent | YES | YES | YES |

**Root cause analysis:** The #5 fix addressed confidence tier *classification* (banning `unrated`) and *URL capture* — both improved. But the researcher has a deeper format compliance problem (#22 in backlog) that #5 didn't address. The model consistently produces narrative research documents instead of the structured RESEARCH OUTPUT block, regardless of the detailed Stage 7 format spec. This is not a single-field fix — the entire output structure diverges from spec.

**Relationship to existing backlog:**
- #22 (stabilize canonical output header) is now confirmed as a systemic format compliance issue, not just a header problem
- The `researcher-formatter` exists as an architectural mitigation — it normalizes whatever the researcher produces into canonical format. This test confirms the formatter remains necessary.

**Verdict: PARTIAL.** URLs fixed. `unrated` gone. Format compliance still fundamentally broken — the researcher ignores the structured output format across all query types.

---

### #27 — Coordinator Formatter Gate: NOT TESTED

The mandatory self-check ("Did I route through researcher-formatter?") was added to `context/specialists-instructions.md`. This gate only fires when the coordinator decides routing in a live chat session — it does not apply to recipe-driven chains (where the formatter step is hardcoded) or direct specialist delegation (where there is no coordinator).

**To properly test:** Run a live chat query like "tell me about Jina AI" in a session using the specialists bundle and observe whether the coordinator includes the formatter step before passing to writer/analyzer.

**Verdict: NOT TESTED.** Requires separate session.

---

## New Findings

### Finding: Researcher format compliance is systemically broken (promotes #22 to sprint priority)

The researcher's Stage 7 spec is detailed and correct. It specifies:
- Plain `RESEARCH OUTPUT` as the first characters of output
- Structured FINDINGS blocks with `Claim:` / `Source:` / `Tier:` / `Confidence:` per entry
- Categorical confidence labels (high/medium/low)
- Source tier labels (primary/secondary/tertiary)

In practice, across 3 independent runs on 3 different query types (company, policy, technical), the researcher produces:
- Markdown-formatted narrative documents
- Numeric confidence values
- Abbreviated tier labels
- Inline source references instead of structured FINDINGS blocks

This is not a regression from Session 1 — this is a pre-existing condition that the #5 fix did not address. The researcher has likely never consistently produced canonical format output, which is why the `researcher-formatter` was created as an architectural mitigation.

**Recommendation:** Promote #22 from near-term to Immediate Next. The fix likely requires more aggressive format enforcement in the researcher spec — possibly including explicit "wrong vs right" output examples, negative examples of narrative format, and a final self-check similar to what we added for the writer's word budget.

### Finding: Recipe timeout confirmed at writer step (#11)

The initial attempt to run the full `research-chain.yaml` recipe on "State of open source LLMs in 2026" timed out at the writer step (900s ceiling). This confirms #11 is a real blocker for broad topics, not hypothetical.

---

## Scorecard Impact

| Dimension | Before Test | After Test | Change |
|---|---|---|---|
| Research Trustworthiness | 5/10 *(spec)* | 3/10 *(validated)* | DOWN — format compliance failure means the spec improvement didn't land as expected |
| Chain Reliability | 5/10 *(spec)* | 4/10 *(partial)* | DOWN — recipe timeout confirmed; formatter gate untested |
| Format Fidelity | 5/10 *(spec)* | 5/10 *(validated for writer)* | HOLDS — writer brief budget confirmed at 316w |
| Specialist Coverage | 4/10 | 4/10 | No change |
| **Overall** | **4.8/10** | **4.0/10** | Honest correction — spec improvements that don't land in practice can't hold inflated scores |

---

## Action Items

1. Promote #22 to Immediate Next — researcher format compliance is the root blocker for Research Trustworthiness scoring above 5
2. Consider whether #5 needs a follow-up fix for numeric-vs-categorical confidence (the model dodges categorical by using numeric)
3. Test #27 in a live coordinator session
4. Address #11 (recipe timeout) — increase writer step timeout for broad topics
