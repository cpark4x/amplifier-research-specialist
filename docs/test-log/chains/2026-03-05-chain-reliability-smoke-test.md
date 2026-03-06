---
specialist: all
chain: "5-scenario smoke test: researcher→writer, researcher→formatter→analyzer→writer, competitive-analysis→writer, researcher (escape hatch), conversational (ambiguous)"
topic: chain-reliability-smoke-test
date: 2026-03-05
quality_signal: mixed
action_items_promoted: true
---

# Chain Reliability Smoke Test — 2026-03-05

**Context:** Comprehensive smoke test of the Conversational Chain Behavior rules added to `specialists-instructions.md`. Tests run after commit `0993cee` (fix: harden top-3 specialist chains for reliability) on branch `fix/chain-reliability-top3`. Each test was executed as an independent self-delegation to simulate isolated user interactions.

## Scorecard

| # | Category | Prompt | Expected Chain | Actual Chain | Narration | Verdict |
|---|----------|--------|----------------|--------------|-----------|---------|
| 1 | Happy path | "Research the Pomodoro technique and whether it actually improves productivity" | researcher → writer | researcher → writer | Partial (HANDOFF + FINAL present; BEFORE missing; extra coordinator text) | **PASS** |
| 2 | Analysis signal | "Give me an analysis of the tradeoffs between microservices and monoliths" | researcher → analyzer → writer | researcher → formatter → analyzer → writer | All 5 lines correct | **PASS** |
| 3 | Competitive | "Compare Notion vs Obsidian for personal knowledge management" | competitive-analysis → writer | competitive-analysis → writer | All 3 lines correct | **PASS** |
| 4 | Escape hatch | "Just run the researcher on the Feynman technique for learning" | researcher only, raw output | researcher only, raw RESEARCH OUTPUT at byte 0 | None (correct) | **PASS** |
| 5 | Ambiguous | "Tell me about spaced repetition" | Unclear — judgment call | No specialists called; conversational response | N/A | **DEBATABLE** |

**Result: 4/5 PASS, 0 FAIL, 1 DEBATABLE**

## What Worked

- **Chain completion is reliable for explicit-intent prompts.** All 4 tests with clear research/analysis/comparison intent completed through to the writer. This is a major improvement over the pre-instructions state where the coordinator routinely dumped raw intermediate output.
- **Rule 4 (analysis signal) routed correctly.** The keyword "analysis" triggered the researcher → formatter → data-analyzer → writer chain. The formatter was correctly included per Rule 5.
- **Escape hatch is precise.** "Just run the researcher" triggered Rule 3 exactly — raw RESEARCH OUTPUT at byte 0, no narration, no writer. The `[RAW]` prefix was applied.
- **Competitive chain path selection was correct.** The coordinator correctly identified the comparison as a competitive-analysis use case and correctly skipped the optional researcher step.
- **Writer output quality was strong across all tests.** Well-structured briefs with citations, source attribution, and claims-to-verify blocks.
- **Narration was mostly correct.** Tests 2 and 3 had perfect narration. Test 1 had partial narration (HANDOFF and FINAL present, BEFORE missing).

## What Didn't / Concerns

### Critical: Narration hook is a stub

The `hook-specialist-narration` module's `mount()` function is a no-op (`pass`). The instructions say: "narration is now emitted automatically via the hook; the coordinator should not rely on emitting narration itself." This creates a contradiction — the hook won't narrate, and the coordinator is told not to. All observed narration came from the coordinator ignoring this instruction and emitting narration manually. This worked in 4/4 specialist tests but is fragile — it depends entirely on model compliance.

### Medium: Ambiguous prompts bypass the chain

"Tell me about spaced repetition" was answered conversationally without any specialist delegation. The coordinator's reasoning: casual phrasing, general knowledge topic, deploying a multi-agent pipeline would over-engineer it. Rule 1 says "the coordinator must never generate specialist-domain content itself" — and a research explainer is specialist-domain content. But the judgment call is defensible. This is the core ambiguity in the instructions: "always chain" vs. "when applicable."

### Low: Minor narration inconsistencies

Test 1 had extra coordinator text between narration lines ("Now let me compose the final brief from the research findings") and the BEFORE line was missing. Tests 2 and 3 were clean. This inconsistency suggests narration format will vary across runs.

### Low: Parsed: line inconsistency

The `Parsed:` line appeared in Test 3 (competitive) but not in Test 1 (happy path). This may be a writer output formatting issue rather than a chain issue.

## Confidence Accuracy

N/A — this test was about chain behavior mechanics, not specialist confidence calibration. The specialist outputs in Tests 1-4 all appeared well-calibrated (researcher confidence ratings aligned with source quality, writer citations were accurate).

## Coverage Assessment

N/A — not applicable to chain behavior testing. The researcher coverage was good in all tests where it ran (Tests 1, 2, 4 all had explicit evidence gaps sections).

## Action Items

- [x] **Implement hook-specialist-narration for real** — **Deferred 2026-03-06**: prompt-level enforcement >90% reliable in re-test; code-level hook not worth the investment vs. higher-leverage backlog items (writer word budgets, audience calibration, URL-per-claim). Module stub retained on disk; hook registration commented out in behaviors/specialists.yaml.
- [x] **Clarify ambiguity boundary for "tell me about" prompts** — **Shipped in PR #16 (2026-03-05)**: routing heuristic table + "when in doubt, chain" rule added to `specialists-instructions.md`. Casual phrasing ("tell me about X") now explicitly listed as a chain trigger. Re-test confirmed: 5/5 pass.
- [x] **Investigate Parsed: line inconsistency** — **Routed to BACKLOG #13** with additional finding from smoke test. Input-type-dependent: present in competitive→writer (Test 3) but absent in researcher→writer (Test 1).
