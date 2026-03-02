# Writer Specialist

A domain expert agent for transforming structured source material into **polished, reader-appropriate prose**.

The Writer's job is precisely: take structured evidence and produce a finished document in the requested format. It does not research, invent, or interpret beyond the source material. It packages and articulates what already exists.

---

## Interface Contract

### Accepts

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `source_material` | string | Yes | — | Researcher output, analyst output, or raw notes to write from |
| `format` | `report \| brief \| proposal \| executive-summary \| email \| memo` | Yes | — | The document format to produce |
| `audience` | string | Yes | — | Who is reading this (shapes voice, detail level, and what to cut) |
| `voice` | `formal \| conversational \| executive` | No | inferred from format | Tone register for the document |
| `length` | string | No | — | Optional constraint (e.g., "500 words", "one page") |

### Returns

A document with a `WRITER METADATA` header followed by the document content.

Key fields in the metadata block:
- `Input type` — what kind of source material was provided
- `Output format` — the document format produced
- `Audience` — who the document is written for
- `Voice` — tone register used
- `Word count` — approximate length
- `Coverage` — `full` or `partial`
- `Coverage gaps` — what could not be written from the source material (`none` if full coverage)
- `Citations` — one entry per inline `[Sn]` marker: source text snippet (≤20 words) + document location where the marker appears; enables callers to verify any output claim against source material
- `Section attribution` — a `> *Sources: Sn (label)*` blockquote after every factual section in the document; enables trust verification at the point of reading without consulting the full CITATIONS index

### Can Do

- Write in 6 formats: report, brief, proposal, executive summary, email, memo
- Calibrate voice and detail level for a specified audience
- Audit source material coverage before writing (flags gaps before drafting)
- Preserve source confidence signals in prose ("confirmed by multiple sources" vs "reported by a single outlet")

### Cannot Do

- Research — that's the Researcher specialist
- Generate claims the source material does not contain
- Make recommendations unless specifically asked for and supported by the source
- Access external data sources — stateless, works only from what's passed in

---

## Design Notes

**Source fidelity above all.** Every claim in the output traces to the source material. If the source doesn't support a claim, the Writer names the gap — it does not silently write around it.

**Format is a contract.** A brief is not a report. An email is not a memo. Each format has conventions the reader expects. The Writer follows them precisely.

**Audience drives every decision.** Word choice, sentence length, level of detail — all determined by who is reading, not by what the source contains.

**Coverage gaps are first-class outputs.** If the source material cannot support the full document requested, the Writer stops and surfaces this before drafting. A partial honest document is more useful than a complete fabricated one.

---

## Typical Usage Chain

```
Researcher → [ResearchOutput] → Writer → [Finished Document]
```

Pass the full Researcher output as `source_material`. The Writer reads the RESEARCH BRIEF and FINDINGS sections to construct the document. No preprocessing needed.
