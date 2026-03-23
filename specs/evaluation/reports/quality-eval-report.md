The report is complete and rendered to `quality-evaluation-gap-report.docx`. Here's the executive summary:

---

## Key Findings

**Pipeline average: 7.60** | **Target: 9.0** | **Gap: −1.40**

### Two Structural Gaps (recurring across topics)

| Gap | Severity | Topics Affected | Pipeline Avg | Competitor Avg | Δ |
|-----|----------|:-:|:-:|:-:|:-:|
| **Citation Quality** | CRITICAL | 3/5 | 5.80 | 8.40 | −2.60 |
| **Factual Depth** | MAJOR | 4/5 | 7.20 | 8.80 | −1.60 |

**Citation Quality** is the #1 problem: in 3 topics the pipeline produced zero URLs in the final document despite claiming 29–43 sourced findings. The pipeline *can* do this correctly (strategy scored 9, technical-analysis scored 8) — the failure is intermittent, likely in the writer → writer-formatter handoff during format escalation.

**Factual Depth** is the most consistent deficit: 4/5 evaluators independently identified the same pattern — strong depth on 5–7 themes but missing 3–5 additional themes that competitors found through wider search strategies. The researcher anchors on an initial source cluster and doesn't perform a breadth sweep.

### Three Pipeline Strengths (consistent advantages)

| Dimension | Pipeline Avg | Competitor Avg | Δ |
|-----------|:-:|:-:|:-:|
| **Analytical Insight** | 8.40 | 8.00 | +0.40 |
| **Confidence Calibration** | 8.60 | 8.00 | +0.60 |
| **Structure & Readability** | 8.40 | 7.80 | +0.60 |

The pipeline's system-level causal synthesis, epistemic discipline, and thesis-driven structure are its clearest competitive advantages — it never loses on structure and wins on insight in 3/5 topics.

### First Action

**Fix URL propagation through the writer stage.** It's the highest-severity gap, the largest per-dimension deficit, and a solvable engineering fix. Closing it would raise the pipeline average from 7.60 to ~8.12, eliminating 37% of the gap to target.
