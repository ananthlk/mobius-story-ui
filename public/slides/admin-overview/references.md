# References — admin-overview

## Primary data source

- **BHPF CFO Benchmarking Survey 2025**
  N=34 BHPF member CFOs, fielded Q1 2025. Self-reported admin FTE
  by department (Finance, IT/IS, Billing/RCM, HR+Payroll), admin %
  of revenue, AR days, denial rate, turnover.
  Instrument: `Financial Benchmarking specs/cfo_admin_benchmarks_2025.json`.
  Mart: `landing_medicaid_npi_dev.cfo_admin_benchmarks`.
  Live skill endpoint: `/proxy/skills/analytics/cfo-admin-benchmarks?tier={tier}`.

- **BHPF CFO Survey — 2016 wave**
  Prior survey instance, used for the 2016→2025 trend bars only.
  Internal: shipped in the static fact pack as `all_2016`.

## Benchmark

- **APQC Open Standards Benchmarking 2024**
  Cross-industry admin %-of-revenue benchmarks. Provides the 9.0%
  benchmark for $1B+ health systems referenced in the slide.
  <https://www.apqc.org/benchmarking>

## Skills referenced

- **`cfo_admin_benchmarks(tier)`** — returns per-tier KPIs
  (admin_pct_revenue, total_fte, staff_by_dept, n) plus the 2016
  baseline. This slide's primary live data source.

## Cross-slide context

- **`act2-opener`** — the four CFO questions this profile is meant to
  answer.
- **`admin-s1`** — diagnosis: same admin profile, but worse outcomes
  (AR days, denial rate, calls/FTE, turnover).
- **`admin-s4`** — the AI CoE consolidation that captures ~$66M of the
  network's admin spend ($37M scale + $29M AI).
- **`admin-s5`** — the four-conclusion summary that closes Act II.
- **`act4-opportunity`** — admin overspend as one of four buckets in
  the $144M–$217M total opportunity.

## Internal references

- **`mobius-skills/provider-roster-credentialing/sub_skills/analytics/routes.py`**
  — `api_cfo_admin_benchmarks` implementation; the canonical SQL.
