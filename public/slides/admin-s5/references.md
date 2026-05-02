# References — admin-s5

## Primary data sources

- **CMS DOGE — Medicaid claims**
  Florida fee-for-service claims, 2018–2024.
  Internal mart: `mobius-os-dev.landing_medicaid_npi_dev.org_kpis_v2`.

- **BHPF CFO Benchmarking Survey 2025**
  N=34 BHPF member CFOs, fielded Q1 2025. Self-reported admin FTE
  by department (Finance, IT/IS, Billing/RCM, HR+Payroll), admin %
  of revenue, AR days, denial rate. Internal instrument at
  `Financial Benchmarking specs/cfo_admin_benchmarks_2025.json`.
  Mart: `landing_medicaid_npi_dev.cfo_admin_benchmarks`.

## Benchmarks

- **APQC Open Standards Benchmarking 2024**
  Cross-industry admin spend benchmarks for $1B+ health systems.
  Source for the 9.0% admin %-of-revenue benchmark and FTE-per-revenue
  ratios used in `methodology.md` § admin_overhead.
  <https://www.apqc.org/benchmarking>

- **MGMA DataDive 2024**
  Median Days in AR (28 days) and other RCM benchmarks referenced
  earlier in Act II.
  <https://www.mgma.com/data/data-dive>

- **ADS / SimiTree — BH Denial Rate Benchmark 2026**
  5.7% denial-rate benchmark referenced in Act II diagnosis slides
  (admin-overview, admin-s1).

## Vendor pitch decks

- Netsmart, Welligent, Qualifacts, Athena product decks reviewed
  Q1 2026. Used for the 2:1 ROI math validation-size figure
  ($500M system) and fixed-cost calculation. Internal vendor-eval
  notes: `Financial Benchmarking specs/platform_intelligence_evidence.json`.

- **Waystar 10-Q (FY 2024)**
  Used for sales+integration fixed-cost decomposition (~$150K per deal).
  <https://investors.waystar.com/sec-filings>

## Methodology references

- **`mobius-skills/provider-roster-credentialing/migrations/027_bq_mart_sync.py`**
  How `org_kpis_v2` is populated from raw claims.

- **`fl_bh_code_reference`** (BQ table)
  The 81-code universe defining "FL behavioral health" — used as the
  scope filter for revenue rollups.

## Cross-slide context

- **`admin-overview`** — the BHPF admin profile that produces the 11.7% / 9.0% gap quoted here.
- **`admin-s1`** — over-investment evidence (FTE per dept vs APQC).
- **`admin-s1c`** — pricing-trap chart (the ROI-curve visualization of the vendor pricing claim in Conclusion 02).
- **`admin-s4`** — AI Center of Excellence detail (where the $37M scale + $29M AI breakdown is built up).
- **`act4-opportunity`** — admin overspend as one of the four buckets summing to $144M–$217M.
- **`act5-approach`** — Phase 1–3 capture sequencing.
