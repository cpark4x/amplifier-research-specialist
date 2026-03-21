# Scenario 11: Raw Brainstorm — Minimal Input from Sparse Notes

## Parameters

- **audience**: Product Team
- **audience_type**: team
- **purpose**: propose
- **tone**: exploratory
- **output_format**: presentation
- **theme**: _(not specified)_
- **presentation_mode**: slide
- **include_speaker_notes**: true
- **include_appendix**: false

## Expected Behavior

The source material is deliberately minimal — rough whiteboard notes with no structure, no data, and incomplete thoughts. The model should build a coherent narrative using Ghost Deck methodology without fabricating specifics. Claims sourced from the notes should be presented as-is; anything the model infers or structures around them should be clearly signaled as speculative or "to be validated." This tests Input Flexibility, D3 (don't fabricate from thin input), and D1 (can you build assertion titles from sparse notes).

## Source Material

Raw notes from whiteboard session — not cleaned up. Treat as unstructured brainstorm input.

---

**Product idea: AI meeting summarizer + action tracker**

- Integrates directly with Google Calendar / Outlook — auto-joins meetings, records, transcribes
- Generates summary + extracts action items → pushes them into Jira / Asana / Linear automatically
- Users HATE taking notes during meetings. It splits attention. Everyone agrees this is a pain point
- Key differentiator: none of the competitors connect the loop back to task management. Otter.ai, Fireflies, Grain — they all stop at the transcript/summary. Nobody closes the loop into the actual workflow where tasks get tracked

Open questions / half-baked thoughts:
- Could reduce meeting follow-up time by ~60%? (gut feel, need to validate)
- Pricing: freemium to get adoption? or enterprise-only so we don't burn cash on free users... TBD
- MVP scope: start with Google Meet + Linear integration only? keep it narrow
- Worried about accuracy of action item extraction — if it gets it wrong, people stop trusting it fast
- Jamie mentioned something about "meeting fatigue" stats from Microsoft — look that up
