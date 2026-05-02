# Methodology — ch1-profile

Per-node values come from `story_fact_pack` skill (`/proxy/skills/story/fact-pack?scope={entity}`):

- **Market share** — sum of CMHC-flagged paid claims / total FL Medicaid BH paid claims (2019).
- **Beneficiaries** — unduplicated count of patients with ≥1 paid BH claim at a BHPF NPI in 2019.
- **Service mix ratio** — ratio of ongoing-service revenue to crisis+intake+ACT revenue.
- **New entrants** — count of orgs in the lookalike (specialty BH) classifier active in FL in 2019.
- **Rate position** — weighted-avg revenue-per-beneficiary vs FL-market median across the 81-code BH universe.
- **Panel commitment** — share of clinicians who continue billing Medicaid month-over-month vs market average.

LLM key-takeaway streams via `/proxy/skills/story/profile/summary/stream?entity={entity}`.

## Limitations
- 2019 baseline only; 2020+ comparison lives on `ch2-evolution` and `ch-finale`.
- Lookalike classifier is a Mobius-internal taxonomy; not all "new entrants" are captured.
