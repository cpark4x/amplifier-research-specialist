# Session Startup — Amplifier Research Specialist

> **For AI agents:** Read this at the start of every session, before any other work.

---

## Step 1 — Load the Vision

Read `docs/01-vision/VISION.md`.

This is the authoritative source for WHY this project exists and HOW to make decisions when a design choice is hard. The file itself says: *"Read this before touching any code."*

The core promise: output a user can **stake their reputation on** — defensible, auditable, honest about its limits. Every finding traces to a source. Every inference traces to a finding. Every gap is named.

**This changes how you frame everything else. Don't skip it.**

---

## Step 2 — Load Current Priorities

Read `docs/BACKLOG.md`.

Focus on **"Immediate Next (This Sprint)"** — these are the highest-priority items for today. Scan the near-term section to know what's queued behind them.

---

## Step 3 — Load Latest Quality Signal

Find and read the most recently modified file in `docs/test-log/`.

Test log findings are the freshest evidence of what's working and what's broken. They often contain observations not yet promoted to the backlog — the log is upstream of the backlog, not a copy of it.

---

## What You Should Know After Startup

| Question | Source |
|---|---|
| What does this project exist to do? | Vision |
| What are we working on today? | Backlog — sprint items |
| What quality gaps are active right now? | Latest test log |
| What shipped recently? | Recent commits (injected by session hooks) |

---

## Why This Order Matters

Vision before backlog: the vision tells you *why* a priority matters, not just *what* it is.

Without the vision, a broken feature looks like polish work. With it, the same fix is a broken V1 promise — that framing changes how you scope and approach the work.
