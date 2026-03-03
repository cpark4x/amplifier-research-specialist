---
specialist: researcher → data-analyzer → writer
chain: "researcher → data-analyzer → writer"
topic: postgres-vs-mongodb
date: 2026-03-03
quality_signal: mixed
action_items_promoted: true
---

# Researcher → Data Analyzer → Writer — Format Compliance Chain Validation

**Topic:** What are the real-world tradeoffs between PostgreSQL and MongoDB for new SaaS
applications in 2025?
**Audience:** CTO
**Format:** Brief

---

## What Worked

- Researcher produced a substantively excellent response — detailed, well-sourced, covering
  9 dimensions, with clear decision framework and concrete recommendations.
- Chain was stopped at Step 2 per protocol — Researcher output was not passed to the Data
  Analyzer without manual intervention. Protocol followed correctly.

## What Didn't / Concerns

- **Researcher format compliance: FAIL.** Response began with `# PostgreSQL vs. MongoDB for
  SaaS in 2025: The Real Tradeoffs` — a markdown header. Required opening is `RESEARCH OUTPUT`
  (plain text, no preamble). Output was structured as narrative markdown with tables, headers,
  and prose sections — not the canonical RESEARCH OUTPUT block format with multi-line key-value
  FINDINGS.
- **Sprint 1 fix did not hold.** Four commits (a9cee89 → 6b60a1e → f18cb67 → 9e21501) added
  compliance notes and a preamble to Researcher Stage 7. The fix worked on the TypeScript topic
  in the Sprint 1 validation test but did not hold on a new topic (PostgreSQL vs MongoDB). This
  suggests the compliance note approach is insufficiently robust — the model's prose-writing
  instinct overrides the spec instruction on substantive topics.
- **Chain stopped at Step 2.** Data Analyzer and Writer were not invoked. Chain quality is
  `mixed` because Step 1 required manual intervention to proceed.

## Root Cause Pattern

Both the Researcher and Writer exhibit the same failure mode: the model produces high-quality
substantive output but ignores the structural output contract when the task is engaging enough
to activate its "write a great response" instinct. Compliance notes at the end of pipeline
stages are insufficient to override this. The fix requires structural changes — the output
format must be anchored earlier in the pipeline, not as a post-hoc compliance check.

## Confidence Accuracy

N/A — chain did not complete.

## Coverage Assessment

N/A — chain did not complete.

## Action Items

- [ ] **Researcher: move output format contract before Stage 1.** Add an "Output Structure"
  section before the pipeline (identical pattern to the Writer fix attempted) that anchors
  `RESEARCH OUTPUT` as the first line requirement before any pipeline stage executes.
  The compliance note after Stage 7 is too late — by then the model has already committed
  to a narrative structure.
- [ ] **Researcher: add a concrete filled-in example** of the required output (not just
  a template) so the model has a format anchor. The TypeScript example in the Stage 7
  format block is a good candidate.
- [ ] **Re-run Sprint 1 validation** after Researcher fix to confirm compliance holds on
  multiple topics, not just the original test topic.
- [ ] **Re-run Sprint 3 chain test** after both Researcher and Writer format compliance are
  confirmed stable across multiple topics.
- [ ] **Broader diagnosis needed:** Both Researcher and Writer have the same root cause.
  Consider a shared "compliance architecture" approach: structural blocks produced
  explicitly at named pipeline stages rather than as post-hoc checks.
