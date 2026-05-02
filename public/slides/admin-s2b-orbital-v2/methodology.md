# Methodology — admin-s2b-orbital-v2

Per-gate vendor scoring. Sources, scoring rubric, and gate definitions are
sourced from a separate Mobius Platform Intelligence rubric:

- **Rubric file**: `/data/platform_intelligence_rubric.json` (loaded by global `_piLoad()` in story.html).
- **Evidence file**: `/data/platform_intelligence_evidence.json` — per-gate review citations and verbatim quotes per vendor.
- **Scoring**: 1=Legacy, 2=Emerging, 3=Modern, 4=Best-in-Class. Anchored to specific behaviors per gate; documented in the rubric.
- **Gate set**: 8 gates spanning the RCM claim lifecycle; new in v2 vs v1: Credentialing as its own gate (was bundled with Eligibility before).

## Limitations
- Vendor reviews are aggregated; specific deployment outcomes vary by site.
- Scoring reflects published capabilities, not necessarily real-world configuration depth.
