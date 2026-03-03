# Principles

**Owner:** Chris Park  
**Last Updated:** 2026-03-03  

> Decisions made, why they were made, and what they rule out.
> Add a principle when a decision is made. Not before.
> Tag every principle as Universal or Specialist-Specific — principles designed for one
> specialist's job should not be extended to another specialist with a different job.

---

## Universal Principles

These apply to every specialist regardless of domain.

---

### Output schema is the contract

**Decision:** Every specialist's output format is a stable contract that downstream consumers depend on. Changing field names, removing sections, or altering the opening line is a breaking change that requires coordinating all downstream consumers in the same update.

**Why:** The Writer specialist parses researcher output. The Writer also parses AnalysisOutput. If either schema changes without coordination, the downstream specialist breaks silently — it may produce output without noticing a field is missing.

**What this rules out:** Casual restructuring of output formats. Schema changes require updating all consumers (Writer, orchestrators, human reviewers) in the same PR.

---

### Quality gates fail loud, not silent

**Decision:** When a quality gate cannot be satisfied — whether due to insufficient corroboration, thin evidence, or unresolvable contradiction — the output includes an explicit `QUALITY THRESHOLD RESULT: NOT MET` block naming what remains unresolved. It does not silently return lower-quality output as if nothing happened.

**Why:** The caller asked for a specific quality level. If they don't get it, they need to know — so they can decide whether to re-run, accept the gap, or escalate. Silent degradation is a trust violation: the output looks authoritative but isn't.

**What this rules out:** Silently omitting the threshold result when it isn't met. Returning medium-quality output when high was requested without disclosure.

---

## Researcher-Specific Principles

These principles govern the Researcher's job: gathering and reporting sourced evidence. They are not automatically valid for specialists with different jobs.

---

### Contradicted findings belong in FINDINGS, not EVIDENCE GAPS

**Decision:** When two sources conflict on a claim, the claim stays in `FINDINGS` with `Confidence: low` and a `Contradicted by:` field naming the conflicting source. It does NOT move to `EVIDENCE GAPS`.

**Why:** A contradiction is not a gap. A gap means "I couldn't find this." A contradiction means "I found two things that disagree." Mixing them makes the output harder to parse and hides signal — a contested claim is more informative than a missing one.

**What this rules out:** Moving disputed claims to `evidence_gaps` as a way to "clean up" findings. The Writer (and any other consumer) needs to see contradictions inline, not buried in a different section.

---

### Specialists use tools directly — never delegate research to other agents

**Decision:** Specialist agents use `web_search` and `web_fetch` tools directly. They do not delegate to general-purpose research agents (e.g., `foundation:web-research`).

**Why:** Delegating research to another agent bypasses the specialist's own pipeline — source tiering, corroboration, and the quality gate only work if the specialist directly handles the sources. When it delegates, it gets back a pre-processed summary with no way to verify how claims were sourced or how confident they should be.

**What this rules out:** Using the `delegate` tool as a shortcut to get research results faster. The specialist IS the quality layer — outsourcing the work removes the value.

---

## Data Analyzer-Specific Principles

These principles govern the Data Analyzer's job: drawing labeled inferences from sourced findings. They are derived from its specific authorization and obligations — not extended from Researcher principles.

---

### Contradiction handling has three paths, not one

**Decision:** When the Analyzer encounters contradicting findings, three paths are valid. The right path depends on what the contradiction reveals:

1. **Dead end** — Findings conflict directly, neither is clearly stronger, no synthesis is possible → Route both to `UNUSED FINDINGS` with `reason: contradicted`.

2. **Contested evidence is the finding** — Two credible independent sources reach opposite conclusions on the same question, and that disagreement is itself meaningful → Draw an `evaluative` inference: *"Evidence on X is genuinely contested, with [source A] finding Y and [source B] finding the opposite."* Confidence reflects source quality, not resolution of the conflict.

3. **One finding is more credible** — Sources differ in tier, methodology, or recency in a way that makes one more reliable → Use the stronger finding; route the weaker to `UNUSED FINDINGS` with `reason: contradicted` and a note on why.

**Why:** A contradiction silently routed to UNUSED loses signal the downstream Writer needs. The Writer cannot represent contested evidence accurately if the Analyzer has hidden that a contest exists. Path 2 preserves that signal as an explicitly labeled inference — which is exactly what the Analyzer is authorized to produce.

**What this rules out:** Automatically routing all contradictions to UNUSED without first asking whether the disagreement itself is informative. Also rules out routing contradictions to EVIDENCE GAPS — a contradiction is a found thing, not a missing thing.

---

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| v1.1 | 2026-03-03 | Chris Park | Restructured with Universal / Researcher-Specific / Analyzer-Specific sections; generalized "quality_threshold: maximum" principle to all quality gates; added Analyzer contradiction three-path principle |
| v1.0 | 2026-03-02 | Chris Park | Initial principles document |
