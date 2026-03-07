---
specialist: dev-machine
chain: "spec-writing → machine-session → verify → iterate"
topic: dev-machine-ridecast2-full-session
date: 2026-03-06
quality_signal: pass
action_items_promoted: false
---

# Dev Machine — Ridecast2 Full Session Retrospective — 2026-03-06

**Context:** First full dev machine session on ridecast2 — an iOS content-to-audio app. 22 features shipped across 8 machine sessions. Phases covered: Phase 1 (foundation fixes), Phase 2 (quality + UI), Phase 0 (iOS infrastructure: auth, storage, payments, deployment). Test count grew from 58 → 151 (93 tests added by machine). Zero human-written test or feature code.

**Session type:** Dev machine workflow retrospective (not a specialist chain). Captured here as a reference for future dev machine sessions on any project.

---

## What Worked

**Spec quality improvement was directly measurable across phases.**
- Phase 1 (light test specs): 2 sessions for 5 features, some mock guessing
- Phase 2 (explicit mock patterns): 1 session for 4 features, cleaner commits
- Phase 0 (full code examples + mock patterns): 2 sessions for 6 complex infrastructure features

The single most valuable spec improvement: showing `vi.mock("./dependency", () => ({ ... }))` explicitly rather than saying "add a test." Machine matched mock patterns exactly when provided. Without them, machine guesses and sometimes guesses wrong.

**The depends_on field correctly sequenced infrastructure specs.**
Phase 0 had real dependency chains: `multi-user-schema` depended on `clerk-auth`; `stripe-subscription` depended on both. STATE.yaml `depends_on` field correctly batched independent specs first (session 7: Google TTS + Clerk + Blob Storage), then dependent ones (session 8: multi-user schema + Stripe + deployment). No explicit ordering instructions needed.

**Small specs beat large ones consistently.**
Every time a spec touched ≤4 files it shipped cleanly. The one large spec from Phase 1 (`pipeline-error-resilience.md`, 10 files) produced a shakier commit than all Phase 2 specs. Rule confirmed: ≤5 files per spec.

**The machine added 93 tests across the session — all unprompted.**
The human wrote zero test code. TDD in specs means the machine writes tests as part of implementing. This is the compound value: not just "features shipped" but "features shipped with coverage."

**Visual pass caught issues tests couldn't.**
After Phase 2, a browser visual audit found: no scrubber drag handle (confirmed in code — `h-1` bar with no thumb), no mini-player skip controls (confirmed — only play/pause), and 370px dead space on Upload. All three were invisible to the test suite. The visual pass should be a standard step after every batch of UI-touching machine sessions.

---

## What Didn't / Concerns

**Machine was not set up from day one — cost ~30 minutes mid-session.**
The dev machine bundle has `/admissions` → `/machine-design` → `/generate-machine` modes specifically to produce `build.yaml`, `iteration.yaml`, `working-session-instructions.md`, and the correct STATE.yaml format at project start. These were created manually mid-session instead. The fix: run `/machine-design` at project inception, not after 8 hours.

**Infrastructure specs produce a code-complete but not service-deployed result.**
Phase 0 (Clerk auth, Stripe, Azure) wrote all the code and tests pass. But no Clerk app exists, no Stripe product exists, no Azure Container App exists. The machine cannot provision cloud resources. Infrastructure specs need an explicit "requires human setup" annotation and a clear distinction in the workflow between "code complete" and "deployed." The `docs/deployment.md` is the right pattern — the machine generates the runbook, the human executes it.

**"test-mode" error noise in test output.**
Phase 0 tests produced 4 `Processing failed: Error: test-mode — no real API calls` console errors. Tests still passed (151/158) but the noise is a loose end. Likely from mocks that throw on unmocked calls — good practice, but the specific call sites weren't fully mocked in the spec. Should be cleaned up.

**STATE.yaml format mismatch required retrofitting.**
The project was created before the dev machine was set up. STATE.yaml was in a custom format (spec list) instead of the machine's expected format (features dict with statuses). Had to add `phase`, `phase_name`, `epoch`, `next_action`, `completed_features`, and `features: {}` dict mid-session. Starting with the correct format saves 20 minutes.

**The machine made an unprompted README rewrite.**
One commit was `docs: rewrite README for public portfolio` — not in any spec. The README content was good, but unprompted autonomous scope expansion is worth noting. The machine should stay within spec scope. Add to working-session-instructions: "Do not modify files that are not listed in your current spec's Files to Modify table."

---

## Confidence Accuracy

N/A — this is a workflow retrospective, not a research/analysis chain. The pattern observations are based on direct measurement (test counts, session counts, commit quality) not inference.

---

## Coverage Assessment

Covers 8 machine sessions across 4 phases. Deepest coverage on Phase 1 (most iterations) and Phase 0 (most novel). Phase 2 was the smoothest phase — specs were well-calibrated and sessions ran clean. Phase 0 raised new questions about infrastructure verification that don't apply to feature code.

---

## Action Items

- [ ] **Always run `/machine-design` at project start** — produces build.yaml, iteration.yaml, working-session-instructions.md, and correct STATE.yaml format. Never retrofit mid-session. Route to: `docs/BACKLOG.md`
- [ ] **Add "requires human setup" flag to infrastructure specs** — spec field: `requires_human_setup: true` with a "Manual Setup Steps" section listing what the human must do after machine ships. Route to: `docs/02-requirements/epics/`
- [ ] **Add visual pass to standard post-machine workflow** — after any batch of UI-touching machine sessions, run `browser-tester:visual-documenter` before writing next specs. Tests can't catch missing scrubber handles. Route to: `docs/BACKLOG.md`
- [ ] **Document the ≤5 files per spec rule formally** — add to `working-session-instructions.md` template: "Each spec should touch ≤5 files. If your spec requires more, split it." Route to: `docs/02-requirements/epics/`
- [ ] **Add scope guard to working-session-instructions template** — "Do not modify files not listed in your spec's Files to Modify table." Prevents unprompted README rewrites and scope creep. Route to: `docs/02-requirements/epics/`
- [ ] **Spec quality checklist** — formalize the spec quality bar as a checklist: (1) current code quoted, (2) explicit vi.mock() patterns, (3) ≤5 files, (4) success criteria with runnable commands, (5) scope section. Route to: `docs/BACKLOG.md`
