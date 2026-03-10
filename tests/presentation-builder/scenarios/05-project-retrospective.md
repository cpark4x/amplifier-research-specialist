# Scenario 05: Project Retrospective — Mobile App Rewrite Post-Mortem

## Parameters

- **audience**: Product and engineering team that worked on the project
- **audience_type**: team
- **purpose**: reflect
- **tone**: conversational
- **output_format**: html
- **theme**: warm-minimal
- **presentation_mode**: slides
- **include_speaker_notes**: true
- **include_appendix**: true

## Expected Framework

Retrospective (what happened -> worked -> didn't -> change)

## Source Material

These are raw notes from the project lead, tech lead, and PM compiled from 1:1 interviews and the project tracker. This is raw-notes input.

---

Project: Rewrite of mobile banking app from React Native to native Swift/Kotlin
Duration: 9 months (originally estimated at 6 months)
Team: 12 engineers (4 iOS, 4 Android, 2 backend, 1 QA, 1 designer)
Outcome: Successfully launched, but 3 months over timeline and 40% over budget

## What Happened — Timeline

Month 1-2: Discovery and architecture. Decided to rewrite rather than incrementally migrate after assessing that 60% of React Native bridge code was unmaintainable. Architecture decision: native per-platform with a shared Kotlin Multiplatform (KMP) business logic layer. This decision was controversial — the iOS team preferred pure Swift, the Android team championed KMP. We went with KMP as a compromise.

Month 3-4: Core foundation work. Built authentication, networking, and data persistence layers. This went smoothly. The KMP layer worked well for networking and data models. We hit our first major issue here: the design system components took 3x longer than estimated because we were building everything from scratch instead of using a component library. Design team delivered specs in Figma but the handoff process was messy — lots of back-and-forth on platform-specific adaptations.

Month 5-6: Feature parity sprint. Attempted to reach feature parity with the existing React Native app. This is where the timeline slipped. We had 47 features to reimplement and had estimated 2 weeks per feature on average. Reality: simple features took 1 week, complex features (bill pay, account transfers, mobile deposit) took 4-6 weeks each. The backend team discovered that 8 APIs needed modification to support the new architecture, which hadn't been scoped.

Month 7: The crisis point. We were 6 weeks behind schedule with 12 features remaining. Management considered cutting scope. We made the hard decision to defer 4 lower-priority features (budget tracking, spending insights, card controls, travel notifications) and ship with 43 of 47 features. The PM worked with stakeholders to get buy-in by presenting a post-launch feature roadmap.

Month 8-9: Stabilization, beta testing, and launch. Beta program with 2,000 users revealed 340 bugs. 78 were P1/P2 severity. The most critical was a data sync issue where account balances showed stale data after transfers — took 2 weeks to root cause to a caching layer race condition in the KMP shared code. Launch happened in Month 9 with all P1 bugs resolved and 12 P2 bugs remaining on a known-issues list.

## What Worked Well

Shared KMP business logic layer: Despite initial resistance, KMP saved an estimated 30% of business logic development time. Both platforms shared networking, caching, data validation, and business rules. When we found and fixed a bug in the KMP layer, it was fixed on both platforms simultaneously. The team now considers this the best architectural decision of the project.

Beta testing program: The 2,000-user beta with staged rollout (500 → 1000 → 2000) caught critical issues before general availability. The stale balance bug would have been catastrophic if it reached production. We used TestFlight and Google Play internal testing tracks effectively.

Weekly architecture reviews: Every Thursday, the tech leads from iOS, Android, and backend met for a 1-hour architecture review. This caught integration issues early and kept the platforms aligned. When the Android team wanted to use Jetpack Compose and the iOS team was using UIKit, the architecture review identified the inconsistency in navigation patterns before it became a problem.

Dedicated QA from day one: Having a QA engineer embedded from Month 1 meant we had a test automation framework ready before features were built. By launch, we had 1,200 automated tests covering 78% of critical user journeys.

Stakeholder communication: Bi-weekly demos to leadership starting in Month 2 built trust and made the scope reduction conversation in Month 7 much easier. They had seen the progress and quality, so they trusted the team's assessment.

## What Didn't Work

Initial estimation: We underestimated by 50%. Root causes: (1) we estimated feature parity as if features were independent, but many had hidden dependencies on shared infrastructure that didn't exist yet, (2) we didn't account for the design system build-out time, (3) backend API modifications were not in scope.

Design handoff process: Figma-to-native translation was a constant source of friction. Designers created specs for a single platform and expected both platforms to "adapt." In practice, iOS and Android have different navigation patterns (tab bar vs bottom navigation), different interaction patterns (swipe behaviors, haptic feedback), and different typography systems. The design team wasn't staffed to create platform-specific specs.

KMP debugging experience: While KMP was great for code sharing, debugging shared code was painful. Xcode's debugger couldn't step into KMP code, and the error messages from the Kotlin/Native compiler were opaque. The team lost an estimated 2 weeks total to KMP-specific debugging challenges.

Feature flag infrastructure: We built a feature flag system too late (Month 6). If we had it from Month 1, we could have shipped incrementally behind flags, launched earlier with a subset of features, and avoided the all-or-nothing pressure of the Month 7 crisis.

No performance budget: We didn't set performance targets until Month 8, at which point we discovered the app cold start was 4.2 seconds (industry benchmark: under 2 seconds). Fixing this required refactoring the dependency injection and lazy-loading several modules. This work should have been ongoing, not a last-minute scramble.

Testing the deferred features: The 4 deferred features had partial implementations in the codebase that needed to be carefully isolated behind feature flags. This dead code created confusion and two bugs in unrelated features due to accidental execution paths reaching deferred code.

## By the Numbers

- Total engineering hours: 14,400 (12 engineers × 9 months × average 40 hrs/week, adjusted for PTO)
- Original estimate: 8,640 hours (12 × 6 × 40 × 0.9 PTO adjustment)
- Hours over budget: 5,760 (67% over hours estimate)
- Features shipped: 43 of 47 planned (91%)
- Bugs found in beta: 340 (78 P1/P2)
- Bugs at launch: 12 P2 remaining on known-issues list
- Test coverage: 78% of critical user journeys automated
- App store rating: 4.6 stars after first month (up from 3.2 with old React Native app)
- Crash-free rate: 99.7% (up from 97.8%)
- App cold start time at launch: 2.8 seconds (down from 4.2 after optimization, target was 2.0)
- User adoption: 89% of active users migrated within 30 days
- Customer support tickets: down 34% compared to pre-launch baseline

## Proposed Changes for Next Time

1. Build the design system first as a standalone workstream with platform-specific variants before feature work begins
2. Feature flags from day one — every feature behind a flag, enabling incremental launch
3. Performance budgets set at architecture time, measured in CI, with automated regression detection
4. Staff designers for platform-specific work or invest in design tokens that translate automatically
5. KMP investment in tooling: custom Xcode debugging plugin, better error reporting, shared logging framework
6. Estimate in ranges (optimistic/likely/pessimistic) and plan for the "likely" scenario with contingency for pessimistic
7. Backend API changes must be scoped in discovery — create an API contract review as a gate before feature work begins
8. Dead code policy: deferred features get their own branches, never partial implementations in main
