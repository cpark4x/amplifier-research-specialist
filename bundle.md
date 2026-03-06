---
bundle:
  name: specialists
  version: 1.0.0
  description: Domain expert specialist agents — independent of any UI

includes:
  - bundle: git+https://github.com/microsoft/amplifier-foundation@main
  - bundle: specialists:behaviors/specialists
  - bundle: git+https://github.com/cpark4x/amplifier-doc-driven-dev@main
---

# Specialists

@specialists:context/session-startup.md
@specialists:context/specialists-instructions.md
