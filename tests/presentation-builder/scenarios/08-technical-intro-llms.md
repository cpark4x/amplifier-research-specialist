# Scenario 08: Technical Introduction — How LLMs Actually Work

## Parameters

- **audience**: Product managers, designers, and non-ML engineers at a company all-hands
- **audience_type**: teaching
- **purpose**: teach
- **tone**: conversational
- **output_format**: html
- **theme**: clean-light
- **presentation_mode**: slides
- **include_speaker_notes**: true
- **include_appendix**: true

## Expected Framework

Discovery (question -> methodology -> findings -> implications -> summary)

## Source Material

These are the speaker's preparation notes and outline. No specialist pipeline was used — this is a direct outline from someone preparing a talk for their team.

---

Presentation: "How LLMs Actually Work — A Non-Technical Guide for Product Teams"

For our next product all-hands. About 30 minutes. Want it to be approachable but not dumbed down — these are smart people who just don't have ML backgrounds. The goal is that after this talk, everyone on the product team can have an informed conversation about what LLMs can and can't do, and make better product decisions because of it.

Outline:

1. Start with something they already know — autocomplete on their phone. LLMs are essentially autocomplete at massive scale. That's actually not a simplification, that's literally what they are — next token prediction. Every time you see ChatGPT generating a response, it's predicting one token at a time, picking the most likely next token given everything that came before it. The magic is that this simple mechanism, scaled up, produces what looks like understanding.

2. What's a token? Not a word. "unhappiness" = "un" + "happiness" or maybe "un" + "hap" + "pi" + "ness" depending on the tokenizer. Average English text: ~1.3 tokens per word. This matters for two practical reasons: pricing is per-token (so you're paying for ~30% more tokens than words), and context windows are measured in tokens (so a "128K context window" is roughly 100K words, or about 200 pages of text).

3. The training process — three stages that I want people to understand conceptually:

   Pre-training: read most of the internet. Hundreds of billions of tokens. Think of it as "reading every book in the library." This is where the model's knowledge comes from — it's compressed patterns from all that text. This stage costs $10-100M+ in compute. Takes weeks to months on thousands of GPUs. This is why you can't just "retrain the model on our data" — the base model training is a massive capital expenditure that only a handful of companies can afford.

   Fine-tuning: teach it to be helpful. This is where RLHF (reinforcement learning from human feedback) comes in. Humans rank outputs — "this response is better than that one" — and the model learns to prefer the kinds of outputs humans rated highly. This is what makes it a "chat" model vs just a fancy autocomplete. Think of pre-training as "learning everything" and fine-tuning as "learning to be helpful about what you know."

   Post-training alignment: safety guardrails, instruction following, format compliance. This is why it responds to "write this as bullet points" or refuses to help with harmful requests. Relatively cheap compared to pre-training.

4. Key concepts the product team needs for their daily work:

   Context window: how much text the model can "see" at once. Think of it as the model's working memory. GPT-4 is 128K tokens (~100 pages). Claude is 200K tokens (~150 pages). This is why "just paste the whole codebase" sometimes works for smaller projects. But context has a cost — longer context = slower + more expensive. And there's research showing models pay less attention to stuff in the middle of long contexts ("lost in the middle" problem).

   Temperature: the randomness dial. 0 = deterministic (always picks the highest-probability token), 1 = creative (samples from the probability distribution more broadly). For our product, most features should be low temp (0.1-0.3) because we want consistent, reliable output. High temp (0.7-1.0) is for brainstorming or creative features where you want variety. Important: temperature doesn't make the model "smarter" — it just changes how it samples from what it already knows.

   Prompt engineering: it's not magic, it's UX for AI. The prompt IS the interface between our product and the model's capabilities. Show the before/after of a bad prompt vs a good prompt for the same task. Example: "Summarize this" vs "You are a technical writer. Summarize this document for a product manager audience. Focus on user-facing impact. Use bullet points. Limit to 5 key points." The difference in output quality is dramatic.

   System prompts vs user prompts: system prompt is "who are you and how should you behave" (set by us as developers), user prompt is "what should you do right now" (from the user). System prompts persist across the conversation. This is how we give the model its "personality" and constraints for each feature.

5. What LLMs can and can't do — the honest version:

   CAN do well: summarize, translate, extract structured data from unstructured text, classify, generate first drafts, explain complex topics, transform between formats (e.g., meeting notes → action items), brainstorm, roleplay/simulate perspectives

   CAN'T do reliably: math (especially multi-step — use a calculator tool), counting and precise enumeration, access real-time information (training data has a cutoff), cite sources accurately (it will generate plausible-looking but fake citations), maintain consistency across very long outputs, remember previous conversations (there's no persistent memory between API calls — each call starts fresh)

   The gray zone: reasoning about novel problems (sometimes impressive, sometimes completely wrong), following very complex multi-step instructions (works ~80% of the time, fails silently the other 20%), generating code (good for common patterns, dangerous for security-critical or subtle logic)

6. Hallucination — what it actually is and why it matters for us:

   Not "lying" — the model has no concept of truth. It's generating plausible text based on patterns. The same mechanism that makes it creative (recombining patterns in novel ways) also makes it fabricate (recombining patterns into things that seem real but aren't).

   This is the #1 risk for our product. If we put LLM output in front of users without verification, we WILL eventually show them something confidently wrong. This is why we need retrieval augmentation (RAG) — ground the model's outputs in real data from our system, then have the model work with that data rather than making things up.

   Practical rule: the more specific and factual the claim, the less you should trust raw LLM output. "This is a summary of the themes in the document" = usually reliable. "The meeting was on January 15th and the budget was $4.2M" = verify against source data.

7. Cost and latency — giving the team practical intuition:

   Cost tiers (approximate, mid-2025 pricing):
   - Frontier models (GPT-4, Claude Opus): ~$10-30 per million input tokens, $30-60 per million output tokens. Use for: complex analysis, nuanced writing, difficult reasoning.
   - Mid-tier (GPT-4o, Claude Sonnet): ~$2-5 per million tokens. Use for: most production features. Best cost-quality tradeoff.
   - Cheap/fast models (GPT-4o-mini, Claude Haiku): ~$0.15-0.60 per million tokens. Use for: classification, extraction, simple formatting, high-volume low-stakes tasks.
   - Open source (Llama, Mistral): hosting cost only, no per-token fee. We don't use these today but they're getting competitive fast.

   Latency: first-token latency is 200ms-2s depending on model. Full response depends on length — budget 1-5 seconds for typical product features. Streaming helps perceived latency a lot.

   For our product right now: most features use the mid-tier. The expensive frontier model is reserved for the two premium analysis features. We're spending about $12K/month on API costs and it scales linearly with usage.

8. Close with: what this means for how we build product.

   The model is a capability, not a feature. Nobody wants "AI-powered" anything — they want their problem solved. Our job is to figure out where this capability solves real user problems better than the alternatives.

   Three questions to ask when considering an LLM feature:
   - What would the user do without this? (If the answer is "nothing, it's fine," you don't need AI.)
   - What happens when it's wrong? (If the cost of error is high, you need human review or RAG.)
   - Is the output verifiable? (Users should be able to assess quality. "Summarize this" is verifiable. "Is this contract legally sound?" is not.)

Notes to self: I know some people on the team are anxious about AI replacing their jobs. I don't want to address it head-on because that makes it a bigger deal than it needs to be, but the framing throughout should implicitly show that these tools augment human work. The "prompt engineering is UX" point is good for this — it positions product and design skills as essential to making AI useful. The "what happens when it's wrong" question also helps — it shows that human judgment is the irreplaceable part.

Also: keep the slides light. This is a talk, not a textbook. The slides should support what I'm saying, not try to capture everything. Lots of visuals, minimal text. The speaker notes should have the depth.