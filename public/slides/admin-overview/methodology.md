# Methodology — admin-overview

How every number on this slide was derived. One section per block in
`data/static.json`. Live data path: `cfo_admin_benchmarks` skill
(`/proxy/skills/analytics/cfo-admin-benchmarks?tier={tier}`).

---

## admin_kpi — Total admin spend KPI card

**Source tables / files:**
- `landing_medicaid_npi_dev.cfo_admin_benchmarks` (BHPF CFO Survey 2025)
- Survey instrument internal at `Financial Benchmarking specs/cfo_admin_benchmarks_2025.json`

**Scope filters:**
- Year: 2025 (CFO survey)
- Org universe: 34 BHPF members (`in_bhpf=TRUE`)
- Tier filter applied at query time: `all` | `sm` (<$15M) | `mid` ($15–30M) | `lg` ($30M+)
- Departments included: Finance (accounting+payroll), IT/IS, Billing/RCM, HR+Payroll. C-suite, UM excluded from FTE bars.

**Computation:**

1. **`admin_pct_revenue.avg`** = mean of self-reported (admin_budget / total_revenue) across orgs in the tier. Self-reported admin budget includes overhead, facilities, and depreciation — not just departmental headcount.

2. **`total_fte.avg`** = sum of department FTE per org, averaged across orgs in the tier.

3. **`n`** = count of survey respondents in the tier.

4. **`top_dept`** = the department (Finance / IT / Billing / HR) with the highest avg_fte for the tier.

**Anchors derived from this block:**
- `admin_pct_avg` → bhpf__all → 11.7%
- `total_fte_avg` → bhpf__all → 345
- `n_members` → bhpf__all → 34

**Known limitations:**
- Self-reported admin budgets vary in what's included (some orgs include facilities, some don't). Respondent variance is documented in the survey instrument.
- Tier boundaries fixed at $15M and $30M annual revenue — drawn from the survey design, not adjustable.
- Sample sizes per tier (sm=13, mid=8, lg=13) are small enough that medians may be more reliable than averages for the smaller tiers.

---

## fte_by_dept — Avg FTE per org by department

**Source tables / files:** same as `admin_kpi`.

**Computation:**
- For each tier × department, mean of self-reported FTE counts.
- Departments: Finance, IT/IS, Billing/RCM, HR+Payroll.

**Live skill mapping:**
- Live response key `staff_by_dept.{dept_key}.avg_fte` (e.g. `staff_by_dept.accounting_payroll.avg_fte`) maps to local `finance` / `it` / `billing` / `hr` field names. Mapping happens in `slide.js > _adaptLiveSkillResponse`.

**Known limitations:**
- "Billing/RCM" includes both internal billing FTE and outsourced-billing-equivalent FTE (orgs were asked to estimate FTE-equivalent for outsourced functions). Not all orgs answered consistently.

---

## fte_2016_vs_2025 — Trend block

**Source tables / files:**
- 2025: same survey as above.
- 2016: prior wave of the BHPF CFO survey, shipped in the static fact pack as `all_2016` and not refreshed by the live skill.

**Computation:**
- Department FTE 2025 vs 2016 deltas, network-level only (no per-tier 2016 data).
- Bars overlay 2016 (gray) vs 2025 (orange) for each of the four departments.

**Known limitations:**
- 2016 was a smaller survey (n unknown — internal records ambiguous). Treat the trend as directional, not statistical.
- Department definitions changed slightly between the 2016 and 2025 instruments. Documented in the trend block's data-validation note.

---

## Cross-cutting notes

- **Currency**: nominal USD, not inflation-adjusted. The 2016→2025 FTE growth therefore does NOT reflect wage inflation — only headcount.
- **Data freshness**: the `cfo_admin_benchmarks` skill returns the latest survey wave. Cold-start fallback (`data/static.json`) is a snapshot from 2026-05-02.
- **Cross-slide coupling**: `admin-s1` reads the same KPIs to render the AR-days, denial-rate, calls/FTE, and turnover diagnosis cards. `admin-s4` reads the same FTE breakdown to compute the AI CoE consolidation target. Single source of truth via the skill.
