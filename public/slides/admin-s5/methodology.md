# Methodology — admin-s5

How every number on this slide was derived. One section per block in
`data/static.json`.

---

## admin_overhead — Excess admin spend & FTE

**Source tables / files:**
- `landing_medicaid_npi_dev.cfo_admin_benchmarks` (BHPF CFO Survey 2025, n=34)
- `landing_medicaid_npi_dev.org_kpis_v2` (BHPF combined revenue base)
- APQC Open Standards Benchmarking 2024 (external benchmark)

**Scope filters:**
- Year: 2025 (CFO survey); 2024 (claims-derived revenue)
- Org universe: 34 BHPF members (`in_bhpf=TRUE`)
- Department universe: Finance, IT/IS, Billing/RCM, HR+Payroll

**Computation:**

1. **Admin %-of-revenue gap.**
   - BHPF: 11.7% (CFO survey, weighted by member revenue).
   - Benchmark: 9.0% (APQC $1B+ health systems).
   - Gap: 2.7pp.

2. **Annual overhead in dollars.**
   - Combined network revenue: $1.1B (sum of `total_revenue` across 34 members in `org_kpis_v2`).
   - Gross gap on revenue base: 2.7pp × $1.1B = ~$30M.
   - Add AI dividend (see step 4) → ~$66M total.
   - Anchor: `annual_overhead`.

3. **Excess FTE.**
   - APQC FTE-per-$M-revenue ratios applied to BHPF's $1.1B yields a target of ~474 admin FTE.
   - BHPF actual: 819 admin FTE (CFO survey: 223 Finance + 217 IT + 226 Billing + 153 HR).
   - Excess: 819 − 474 ≈ 345 FTE.
   - Anchor: `fte_excess`.

4. **Scale dividend separation.**
   - Step-1 gap (pure FTE consolidation, no AI) recovers ~$37M (the 345-FTE × loaded-cost calculation).
   - AI on top of consolidation: AI denial engine (denial rate 18% → <8% target), AR automation (84 days → 34 days target), intake routing (510 calls/day shared) recovers an additional ~$29M.
   - Anchors: `scale_dividend` ($37M), `ai_dividend` ($29M).

**Anchors derived from this block:**
- `fte_excess` → 345 FTE
- `annual_overhead` → $66M
- `scale_dividend` → $37M
- `ai_dividend` → $29M

**Known limitations:**
- APQC benchmark is cross-industry, not BH-specific. We do not have a BH-only $1B+ benchmark.
- $37M / $29M split is directional; the consolidation+AI capture is sequenced over 36 months in Act V — actual Y1 capture is $22M (Phase 1).
- CFO survey is self-reported; FTE counts not audited against payroll systems.

**Last refreshed:** 2026-04-30 (CFO Survey 2025 close).

---

## vendor_pricing — Vendor ROI calibration

**Source tables / files:**
- Vendor pitch decks reviewed Q1 2026 (Netsmart, Welligent, Qualifacts, Athena) — internal eval.
- `landing_medicaid_npi_dev.org_kpis_v2` for BHPF average org revenue.
- 10-Q margin analysis (Waystar) for fixed-cost decomposition.

**Scope filters:**
- Vendor segment: BH EHR / RCM platforms with explicit ROI calculators in their sales decks.

**Computation:**

1. **Validation size.** Standard vendor 2:1 ROI calculators are calibrated against deals at ~$500M system size — pulled from the customer-spotlight slides in vendor decks. Anchor: `vendor_validation_size`.

2. **BHPF average org revenue.** `SELECT AVG(total_revenue) FROM org_kpis_v2 WHERE year=2024 AND in_bhpf=TRUE` ≈ $32M. Anchor: `bhpf_avg_org_revenue`.

3. **Fixed-cost consumption at $32M.** Industry pricing: ~$150K fixed sales+integration cost regardless of org size. At $32M revenue with typical 1.5–2.5% deal value:
   - Deal value at $32M: $0.5M – $0.9M
   - Fixed cost as share: $150K / $0.5M = 30%; $150K / $0.22M (lower deal) = 68%
   - Range expressed as 50–68% to bracket typical deal sizing. Anchors: `fixed_cost_low`, `fixed_cost_high`.

**Known limitations:**
- The 50–68% range is illustrative, derived from cross-vendor deck math. Actual share varies by deal structure.
- Validation-size figure is from sales-deck framing, not audited.

---

## network_scale — BHPF combined footprint

**Source tables / files:**
- `landing_medicaid_npi_dev.org_kpis_v2` for revenue
- BHPF directory for org count

**Computation:**
- `SELECT SUM(total_revenue) FROM org_kpis_v2 WHERE year=2024 AND in_bhpf=TRUE` → $1.1B (rounded). Anchor: `combined_revenue`.
- Member count: 34, from BHPF directory at time of survey. Anchor: `n_orgs`.

---

## Cross-cutting notes

- **Currency**: nominal USD, not inflation-adjusted.
- **AI dividend timing**: $29M is run-rate at network scale post-CoE deployment, not Year 1. See Act V phasing for the time profile.
- **Governance scope**: this slide quantifies the gap; it does not specify the governance form needed to capture it. That is `act3-teeup` and `act5-approach`.
