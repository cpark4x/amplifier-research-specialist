# Epic 02: Writer Specialist

**Status:** Complete
**Specialist:** `specialists:writer`
**Depends on:** Epic 01 (Researcher) — Writer consumes Researcher output

---

## What This Enables

Orchestrators can delegate writing tasks to a specialist that:
- Takes researcher output and produces a polished document in the requested format
- Audits coverage before writing — flags what the source material cannot support
- Never adds claims beyond what the source contains
- Produces a machine-readable WRITER METADATA block for downstream consumption

## Formats Supported

Report, brief, proposal, executive summary, email, memo

## Typical Usage

```
specialists:researcher → structured evidence (RESEARCH BRIEF + FINDINGS)
        ↓
specialists:writer → polished document (WRITER METADATA + content)
```

## Output Contract

Every Writer response starts with a WRITER METADATA block:
- Input type, output format, audience, voice, word count
- Coverage: full | partial
- Coverage gaps: explicit list of what couldn't be written from source material

## What It Does Not Do

- Generate claims not in the source material
- Silently work around coverage gaps
- Research on its own
