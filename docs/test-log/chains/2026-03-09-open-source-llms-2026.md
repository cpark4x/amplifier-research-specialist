---
specialist: all
chain: "researcher → formatter → data-analyzer → writer → save"
topic: open-source-llms-2026
date: 2026-03-09
quality_signal: mixed
action_items_promoted: false
---

# Research-Chain: State of Open Source LLMs in 2026 — 2026-03-09

**Context:** Full research-chain recipe (v1.2.0) run on the question "State of open source LLMs in 2026" with `quality_threshold: high`, `output_format: brief`, `voice: executive`. Checked whether the pipeline completes all five steps without timing out.

## What Worked

- **Steps 1–4 completed cleanly and in sequence.** Researcher → formatter → data-analyzer → writer all ran without errors or retries. Pipeline handled a broad, high-stakes research question with no step-level failures.
- **Research output was substantive.** 44 claims produced, covering MoE architecture convergence, benchmark parity narrative vs. production reality, infrastructure access barriers, EU licensing dynamics, and proprietary consolidation trends. Confidence distribution well-spread: 13 high · 13 medium · 2 low · 10 inference.
- **Writer produced a clean executive brief.** Well-structured with Summary → Key Points → Implications → What Requires Verification. Source attribution lines (`> *Sources: S1, S5…*`) present after every section. `CLAIMS TO VERIFY` block present and populated with 15 flagged claims.
- **Confidence calibration looked correct.** High confidence assigned to independently-corroborated findings (hardware specs, benchmark scores, EU AI Act text). Medium on single-survey claims (Menlo Ventures n=150). Low on self-reported benchmarks (Qwen3, Behemoth). Inference correctly labeled for derived conclusions. No obvious miscalibration.
- **Coverage gaps named correctly.** MIT CSAIL 15–22% production error figure flagged as unverifiable (no publication/DOI). Qwen3 SOTA claims flagged as self-reported. OpenAI open-weight model status flagged as unresolved. TCO gap in 86% cost savings claim explicitly surfaced. Writer correctly carried these into the `CLAIMS TO VERIFY` and verification section.
- **Session-analyst recovery worked.** After the save step failed, session-analyst extracted the full `final_document` from the recipe session without issue. Document was recoverable.

## What Didn't / Concerns

### Critical: Save step times out reliably at 120s

`foundation:file-ops` timed out on the initial run and on both resume attempts (3 failures total). The 120s ceiling in the recipe is not enough for the agent to spin up and complete the write. This is a hard blocker — the recipe never reaches a clean terminal state and requires manual recovery every run.

Manual workaround used: session-analyst to extract `final_document` from recipe session + direct `write_file` call. This works but is not acceptable as normal operating procedure.

### Low: Wrong context variable on first run

Orchestrator passed `question` instead of `research_question` as the context variable name. Recipe silently treated the question as blank and ran a null-result pipeline, wasting a full run. The recipe has no validation or error on missing required context. A null-result run produces a complete but empty artifact — correct pipeline behavior, but the failure mode is silent and expensive.

## Confidence Accuracy

Well-calibrated. The high/medium/low/inference distribution tracked appropriately with source quality:
- High on directly-verified factual claims (hardware minimums, independent benchmark scores, EU AI Act enactment)
- Medium on survey-backed claims with concentration risk (Menlo Ventures sole source for 5+ enterprise figures)
- Low on vendor self-reported benchmarks without independent corroboration
- Inference correctly used for derived conclusions and structural observations

No over-confidence on hard-to-verify claims observed. The MIT CSAIL finding was correctly held at medium with an explicit note that it lacks a verifiable publication — correct call.

## Coverage Assessment

Coverage: full per writer metadata. Gaps were correctly identified and named rather than papered over. The four verification-required items (TCO baseline, MIT CSAIL citation, Qwen3 independence, OpenAI status) represent genuine sourcing gaps, not over-caution. No verifiable public facts were flagged unnecessarily.

## Action Items

- [ ] **Bump save step timeout in research-chain.yaml** — increase from 120s to at least 300s. The 120s ceiling is consistently too tight for `foundation:file-ops` to complete. This is the remaining open piece of backlog #11. Check narrative-chain.yaml for the same issue.
- [ ] **Add required-field validation to research-chain recipe** — if `research_question` is blank, fail fast with a clear error rather than running a null-result pipeline. Saves a full multi-step run on orchestrator input error.
