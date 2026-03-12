# PR #17 Review Discussion Agenda

## 1. Executive Summary

This PR introduces a new **presentation-builder** specialist that transforms research, analysis, and writer output into self-contained HTML slide decks, plus a comprehensive eval harness for quality iteration. The blast radius extends beyond the specialist itself — it changes routing behavior for *all* users by adding proactive presentation suggestions and silently defaulting executive audiences to slide decks over written documents. **The single most important conversation:** the specialist's navigation script — the thing that makes a deck a deck — fails to generate correctly ~60% of the time, and the post-processor that fixes it only runs inside the eval harness, not in interactive sessions.

---

## 2. PR Overview

| | |
|---|---|
| **Title** | feat: introduce presentation-builder specialist with eval harness |
| **Author** | singh2 (Gurkaran Singh) |
| **Branch** | `gurkaran/epic-07-presentation-builder` → `main` |
| **Files** | 18 changed (+2,506 / −3) |
| **Shape** | 1 specialist definition (index.md + README), routing instruction updates, 1 epic doc, 6 test scenarios, 2 recipe YAMLs, 2 shell scripts, 1 Python post-processor, 1 rubric |

The diff adds a new specialist to the chain that takes structured input and returns a single self-contained HTML file with CSS-only visuals, keyboard navigation, and speaker notes. It updates the coordinator's routing instructions with disambiguation rules and proactive triggers. A parallel eval harness generates decks from 6 scenarios, scores them against a 10-dimension rubric, and tracks quality over rounds.

**Contributor:** New contributor — 3 PRs total, 2 merged (a path fix and an epic assignment). This is their first substantive feature PR.

---

## 3. What This PR Actually Brings In

| Change | Described in PR body? | Surprise factor |
|---|---|---|
| New specialist with 376-line instruction set | ✅ Yes | None |
| Coordinator silently defaults executive audiences to decks over docs | ❌ Buried in routing rules | **High** — changes existing user experience |
| Three proactive suggestion triggers added to every session | ❌ Mentioned but not flagged as behavioral change | **High** — affects non-presentation sessions |
| `fix-navigation.py` patches 60% of outputs post-generation | ✅ Honestly disclosed | **Medium** — only runs in eval harness, not interactive use |
| Epic doc promises `PresentationOutput` type in `shared/interface/types.md` | ❌ Not mentioned | **Medium** — file doesn't exist |
| Eval harness scores patched output, not raw specialist output | ✅ Noted in comments | **Medium** — quality signal is confounded |
| No pytest integration or structural smoke tests | ❌ Not mentioned | **Low** |

---

## 4. The Conversation You Need To Have

---

**[B1] 60% of interactive users will receive broken presentations** · CPO

The PR honestly discloses that the model drops the `<script>` navigation tag ~60% of the time. `fix-navigation.py` exists to patch this — but it only runs inside the eval harness recipe. When a real user says "turn this research into a presentation," the specialist returns raw HTML with no post-processing. More often than not, they get a scrollable webpage, not a navigable deck. A presentation that doesn't respond to arrow keys isn't a presentation. This is the first-run experience for every user who tries the feature.

**Ask:** "Gurkaran — what's the plan for making navigation work in interactive sessions? Could `fix-navigation.py` run automatically as a post-processing step on every specialist invocation, not just inside the eval recipe? Or is there a prompt approach you've tested that gets reliability above 95%?"

**Resolution:** Either integrate `fix-navigation.py` as an automatic post-processor for all presentation-builder output, or demonstrate >95% navigation reliability in interactive sessions before merging.

---

**[B2] Bash template interpolation will silently corrupt HTML output** · CTO

Both recipe files use `printf '%s' '{{deck_output}}'` to write agent output to disk. When the recipe engine substitutes the HTML into this shell command, any single quote in the content — and HTML with inline JavaScript *always* contains single quotes (e.g., `d.className = 'nav-dot'` from the skeleton itself) — will terminate the shell string literal. This causes partial writes, syntax errors, or silently truncated files. The `{{evaluation_result}}` substitution in `evaluate-deck.yaml` has the same issue.

**Ask:** "Have you run `run-all.sh` end-to-end and confirmed the HTML files on disk are byte-identical to what the agent returned? If the recipe engine does its own escaping before shell expansion, this is fine — but the code as written doesn't show that. Can you confirm how the engine handles this?"

**Resolution:** Write output using the recipe engine's native file-write mechanism or a heredoc with a unique delimiter instead of single-quote-wrapped `printf`.

---

**[I1] Silent routing change defaults executive audiences away from Writer** · CPO

The new disambiguation rule says "Executive audience + no format signal → default to Presentation Builder." This changes what every executive-audience request produces — silently. A user who says "summarize this research for the VP" today gets a written document. After this PR, they get a slide deck. The disambiguation table is thoughtful, but "document-signal vs. slide-signal" is a judgment call the coordinator makes without telling the user. The "if genuinely ambiguous, ask the user" escape valve is good — but the executive-default rule means many genuinely ambiguous cases won't trigger it.

**Ask:** "Could the executive-default rule start as 'ask the user' instead of 'default to presentation-builder' for the initial release? That gives you real usage data on what executive-audience users actually want, without surprising anyone. Once you have the signal, you can confidently set the default."

**Resolution:** Change the executive-audience default from auto-routing to an explicit ask for the initial release.

---

**[I2] Proactive suggestion triggers change every session's UX** · CPO

The routing instructions now tell the coordinator to proactively offer deck-building after research chains for executive audiences, after competitive analysis when users mention meetings, and whenever users mention upcoming presentations. The third trigger is reasonable — the user expressed intent. The first two are speculative: they guess intent from audience type, not expressed need. Every "Want me to also build a slide deck?" that appears when the user didn't want one is friction. For a new, unvalidated specialist, starting conservative is safer.

**Ask:** "What if proactive suggestions launched only when the user explicitly mentions a presentation context — and not based on inferred audience type? You could expand the triggers after you see real usage patterns. Would that feel too restrictive?"

**Resolution:** Keep the "user mentions a presentation event" trigger. Remove the audience-inferred triggers for the initial release.

---

**[I3] Eval harness scores patched output, masking true specialist quality** · CTO

`generate-decks.yaml` runs `fix-navigation.py` on every deck *before* evaluation. The rubric then scores the patched HTML. D10 (HTML Quality) will consistently score 4–5, even though the specialist drops navigation 60% of the time. The cross-round scorecard tracks improvement, but the signal is confounded by the post-processor. The PR comments even note "the evaluation will score the PATCHED output, not the raw agent output" — but the scorecard consumer won't see that caveat.

**Ask:** "Would it make sense to run the rubric twice — once on raw output, once on patched — and track both in the scorecard? That way you can see specialist improvement over time (raw D10) while also knowing user-facing quality (patched D10). The CSV already has the column structure for it."

**Resolution:** Add a "raw score" evaluation pass, at minimum for D10, so specialist improvement is trackable independently of the post-processor.

---

**[I4] Epic document describes a different specialist than what was built** · CTO

The epic (`07-presentation-builder.md`) says "Returns `PresentationOutput` — defined in `shared/interface/types.md`" and describes structured machine-parseable blueprints for downstream renderers (PPTX, Google Slides, HTML). The actual implementation returns raw HTML with metadata in HTML comments. No `shared/interface/types.md` is created or modified. The "Blocks: Downstream renderer tool" section describes a dependency chain that doesn't exist. The epic's a contract for future contributors — it should match reality.

**Ask:** "The epic describes a multi-format blueprint approach, but you built — sensibly — an HTML-first specialist. Could you update the epic to reflect what you actually shipped, and move the structured `PresentationOutput` / multi-renderer concept to the Future section?"

**Resolution:** Update the epic to match the implementation.

---

**[A1] No integration with the project's test framework.** The eval harness is excellent for quality iteration but runs standalone. A minimal pytest test validating structural invariants (specialist registered in `specialists.yaml`, scenario files parse correctly) would catch regressions in CI cheaply.

**[A2] `collect-scores.sh` uses macOS-specific `stat` flags.** The `stat -f '%Sm' -t '%Y-%m-%d'` syntax fails on Linux. The fallback chain partially handles it, but round dates will show "unknown" in CI. Swap `stat`/`date` order to prefer the more portable `date -r` first.

**[A3] Root README not updated.** Users browsing the repo to discover available specialists won't find the presentation builder listed. Worth adding alongside the other specialists.

---

## 5. Open Questions

1. **What's the actual interactive reliability rate?** The "~60%" figure comes from the PR description — is that from the eval harness runs, from ad-hoc testing, or estimated? How many interactive sessions have been run end-to-end without the post-processor?

2. **Has the recipe engine's template substitution been tested with single-quote-heavy content?** If the engine escapes `{{variables}}` before shell expansion, [B2] is a non-issue. If it does literal string substitution, every run is broken. Only the author or someone who knows the recipe engine internals can confirm.

3. **What does the formatter-pair pattern look like for presentation-builder?** Every other downstream specialist has a matched formatter (writer/writer-formatter, story/story-formatter). Is a presentation-formatter planned, or does the HTML-comment metadata serve that role? The routing instructions add presentation-builder to the formatter gate but don't define a corresponding formatter.

4. **How should the specialist handle sources with low confidence scores?** The content integrity rules say "never fabricate" and "preserve qualifiers," but they don't address what to do when source confidence is medium or low. Should the specialist visually distinguish high-confidence claims from hedged ones in the deck?

5. **Is the 5-item-per-slide density limit the right number for all content types?** A comparison matrix (scenario 02) or a timeline (scenario 05) may naturally have 6–8 items. Is the split-across-two-slides rule tested against these scenarios, and does it produce better or worse decks?

---

## 6. Verdict: DISCUSS

The core tension is **ambition vs. reliability.** The specialist's design is genuinely impressive — ghost deck methodology, assertion-evidence structure, visual rhythm rules, content integrity constraints, and a 10-dimension eval harness with cross-round tracking. This is clearly the work of someone who studied what makes presentations good and built a system around those principles. But the primary output contract — "a navigable HTML slide deck" — fails more often than it succeeds in unassisted use, and the routing changes that introduce this specialist to users are more aggressive than a first release warrants. The path to merge is clear: make navigation reliable for interactive users (either via automatic post-processing or demonstrated prompt reliability), start the routing rules conservative (ask instead of assume for executive audiences), and align the epic doc with what was actually built. Do that, and this is a strong addition to the specialist chain.
