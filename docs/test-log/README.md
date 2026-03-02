# Specialist Test Log

Records of real specialist invocations with quality assessments and improvement insights.

---

## Structure

```
test-log/
├── researcher/    # Researcher-only tests
├── writer/        # Writer-only tests
└── chains/        # Multi-specialist chains (researcher → writer, etc.)
```

File naming: `YYYY-MM-DD-short-description.md`

---

## When to Log

Log any test where you want to capture what worked, what didn't, and what it implies for improvement. Doesn't need to be exhaustive — a few sentences per section is enough.

---

## Template

```markdown
# [Short description]

**Date:** YYYY-MM-DD  
**Specialists:** [researcher | writer | researcher → writer | etc.]  
**Query:** [Exact query or close paraphrase]  

---

## What Worked

- [Observation]

## What Didn't / Concerns

- [Observation]

## Confidence Accuracy

Were the confidence ratings appropriate given what you know about the topic?

- High claims: [accurate / over-confident / under-confident]
- Medium claims: [accurate / over-confident / under-confident]

## Coverage Assessment

Was `Coverage: partial` accurate? Did it flag the right gaps?

- [Observation]

## Action Items

- [ ] [Backlog item, epic open question, or "none"]
```

---

## How Insights Get Actioned

| Finding | Where it goes |
|---------|---------------|
| Consistent quality gap in a specialist | BACKLOG.md as a new item |
| Edge case in a specific specialist | Open question in the relevant epic |
| Pattern across multiple tests | Note in `adding-a-specialist.md` design principles |
| Confidence systematically wrong | Issue in the relevant specialist's `index.md` |
