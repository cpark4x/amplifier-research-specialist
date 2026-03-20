---
bundle:
  name: specialists
  version: 1.0.0
  description: Domain expert specialist agents — independent of any UI

includes:
  - bundle: git+https://github.com/microsoft/amplifier-foundation@1d26e9be0ca7c1e9939a5531f2d4d5485c72fea3
  - bundle: specialists:behaviors/specialists
  - bundle: git+https://github.com/cpark4x/amplifier-doc-driven-dev@dda74c522c7fb7bd092f440fdd5ca656b61a1423
---

# Specialists

@specialists:context/session-startup.md
@specialists:context/coordinator-routing.md
