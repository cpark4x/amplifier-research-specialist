# 03-05: Model-Agnostic CLI

**Epic:** [03. Storyteller](../../epics/03-storyteller.md)
**Status:** ✅ Implemented

---

## Capability

A developer can invoke Storyteller from the Amplifier CLI with any supported LLM provider (Anthropic, OpenAI, Gemini) and receive identical StoryOutput regardless of provider — no provider-specific features required.

---

## Done Looks Like

1. `amplifier run specialists:storyteller --provider anthropic < analysis.txt` produces StoryOutput with all required sections
2. Same command with `--provider openai` produces equivalent output
3. Same command with `--provider gemini` produces equivalent output
4. No provider-specific features used — pure text in, text out

---

## Why This Matters

**The Problem:** Specialists that depend on provider-specific features (function calling, structured output APIs, vision) cannot be swapped between providers — they create hidden lock-in and break when a preferred provider is unavailable.

**This Fix:** Storyteller uses only plain text prompting and text output. No structured output APIs, no tool use, no vision. Any provider that accepts text and returns text works identically.

**The Result:** Developers can switch providers for cost, latency, or availability reasons without changing how Storyteller is invoked or what it returns.

---

## Dependencies

**Requires:** 03-01 (transform analysis to narrative), Amplifier CLI

**Enables:** Provider-flexible deployments and cost optimization across LLM vendors

---

**Created:** 2026-03-04 by Chris Park

**Epic:** [03. Storyteller](../../epics/03-storyteller.md)
