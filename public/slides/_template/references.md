# References — {{Slide title}}

External sources cited in `methodology.md`. Stable URLs only — if a link
rots, replace it; do not delete it. Format: markdown list grouped by
source type.

## Primary data sources

- **CMS DOGE — Medicaid claims**
  Florida fee-for-service claims, 2018–2024.
  Internal mart: `mobius-os-dev.landing_medicaid_npi_dev.org_kpis_v2`.
  Public docs: <https://data.cms.gov/medicaid> ({{specific dataset link}})

- **CMS HCPCS reference**
  Procedure code definitions and modifiers.
  <https://www.cms.gov/medicare/coding-billing/healthcare-common-procedure-system>

## Benchmarks

- **MGMA DataDive — 2024 edition**
  Median benchmarks for Days in AR, billing FTE, etc.
  <https://www.mgma.com/data/data-dive>

- **APQC Open Standards Benchmarking 2024**
  Cross-industry admin-spend benchmarks for $1B+ health systems.
  <https://www.apqc.org/benchmarking>

- **NSI National Healthcare Retention & RN Staffing Report 2024**
  Behavioral-health turnover benchmarks.
  <https://www.nsinursingsolutions.com/Documents/Library/NSI_National_Health_Care_Retention_Report.pdf>

## Surveys

- **BHPF CFO Benchmarking Survey 2025**
  N=34 BHPF member CFOs, fielded {{month/year}}, instrument linked
  internally at `{{path}}`.

## Vendor / external analysis

- **ADS / SimiTree — BH Denial Rate Benchmark 2026**
  Initial-claim denial rate average for behavioral-health practices.
  <{{vendor URL}}>

- **athenahealth network — 2024 benchmark report**
  Cross-specialty denial rate (5.7%).
  <{{publication URL}}>

## Methodology references

- **`mobius-skills/provider-roster-credentialing/migrations/027_bq_mart_sync.py`**
  How org_kpis_v2 is populated from raw claims.

- **`fl_bh_code_reference`** (BQ table)
  The 81-code universe defining "FL behavioral health".

---

## Adding a new reference

1. Add the citation to the appropriate section above.
2. Ensure `methodology.md` cites it by name where used.
3. Use a stable URL. If the source is internal (BQ table, repo path),
   use the table/path identifier exactly so chat can resolve it via
   `code_definition` or `bq_table_lookup`.
