# Principles

**Owner:** Chris Park  
**Last Updated:** 2026-03-02  

> Decisions made, why they were made, and what they rule out.
> Add a principle when a decision is made. Not before.

---

## Contradicted findings belong in FINDINGS, not EVIDENCE GAPS

**Decision:** When two sources conflict on a claim, the claim stays in `FINDINGS` with `Confidence: low` and a `Contradicted by:` field naming the conflicting source. It does NOT move to `EVIDENCE GAPS`.

**Why:** A contradiction is not a gap. A gap means "I couldn't find this." A contradiction means "I found two things that disagree." Mixing them makes the output harder to parse and hides signal — a contested claim is more informative than a missing one.

**What this rules out:** Moving disputed claims to `evidence_gaps` as a way to "clean up" findings. The Writer (and any other consumer) needs to see contradictions inline, not buried in a different section.

---

## `quality_threshold: maximum` fails loud, not silent

**Decision:** When `quality_threshold: maximum` is requested and the Quality Gate cannot be fully satisfied after 3 corroboration cycles, the output includes an explicit `QUALITY THRESHOLD RESULT: NOT MET` block naming what remains unresolved. It does not silently return medium-quality output as if nothing happened.

**Why:** The caller asked for maximum quality. If they don't get it, they need to know — so they can decide whether to re-run, accept the gap, or escalate. Silent degradation is a trust violation: the output looks authoritative but isn't.

**What this rules out:** Adding more cycles beyond 3 as the solution (it just delays the same outcome). Silently omitting the threshold result when it isn't met.

---

## Specialists use tools directly — never delegate research to other agents

**Decision:** Specialist agents use `web_search` and `web_fetch` tools directly. They do not delegate to general-purpose research agents (e.g., `foundation:web-research`).

**Why:** Delegating research to another agent bypasses the specialist's own pipeline — source tiering, corroboration, and the quality gate only work if the specialist directly handles the sources. When it delegates, it gets back a pre-processed summary with no way to verify how claims were sourced or how confident they should be.

**What this rules out:** Using the `delegate` tool as a shortcut to get research results faster. The specialist IS the quality layer — outsourcing the work removes the value.

---

## Output schema is the contract

**Decision:** The researcher's output format (FINDINGS, EVIDENCE GAPS, QUALITY THRESHOLD RESULT, etc.) is a contract that downstream agents depend on. Changing field names or removing sections is a breaking change.

**Why:** The Writer specialist will parse researcher output. If the schema changes without coordination, the Writer breaks silently — it may produce output without noticing a field is missing.

**What this rules out:** Casual restructuring of the output format. Schema changes require updating all consumers (Writer, etc.) in the same PR.
