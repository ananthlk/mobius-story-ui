# The BHPF admin profile

## The One Thing

> BHPF runs at {{ANCHOR:admin_pct_avg}} admin spend vs {{ANCHOR:admin_pct_benchmark}} benchmark — a {{ANCHOR:admin_pp_gap}} gap that, on $1.1B combined revenue, sets up the $66M opportunity Acts II–V build on.

## Setup

After the four CFO questions in `act2-opener`, this slide grounds the rest of Act II: it shows BHPF's actual admin profile by tier so members can locate themselves on the chart before the diagnosis slides land.

## The Argument

The CFO Survey 2025 captured admin spend and FTE for all {{ANCHOR:n_members}} members. Three findings:

1. **The aggregate.** Admin is {{ANCHOR:admin_pct_avg}} of revenue across the network — {{ANCHOR:admin_pp_gap}} above the APQC $1B+ benchmark of {{ANCHOR:admin_pct_benchmark}}.

2. **The shape.** {{ANCHOR:total_fte_avg}} avg admin FTE per org, distributed across Finance, IT/IS, Billing/RCM, and HR. Tab between tiers (`<$15M`, `$15–30M`, `$30M+`) to see how the shape changes by org size.

3. **The trend.** From 2016 to 2025, average FTE per org *grew* in every department — admin scale pressure has been compounding, not improving.

## The Data

| Metric | Anchor | Value | Source |
|---|---|---|---|
| Admin %-of-revenue (network avg) | `admin_pct_avg` | 11.7% | CFO Survey 2025, n=34 |
| APQC $1B+ benchmark | `admin_pct_benchmark` | 9.0% | APQC Open Standards 2024 |
| Gap | `admin_pp_gap` | 2.7pp | derived |
| Avg admin FTE per org | `total_fte_avg` | 345 FTE | CFO Survey 2025 |
| Network sample size | `n_members` | 34 | BHPF directory |

Per-tier numbers (admin %, FTE, sample size) and per-department FTE breakdowns are returned by the `cfo_admin_benchmarks` skill at render time. Tab clicks re-call the skill.

## Expected Questions

- **Q:** Which tier am I in?
  **A:** `<$15M` = small (n=13), `$15–30M` = mid (n=8), `$30M+` = large (n=13). Click any tier tab to see those org-size benchmarks.

- **Q:** How does my dept compare to the network average?
  **A:** Click into the FTE-by-dept chart for a per-tier breakdown. Chat can pull `cfo_admin_benchmarks` for any specific tier.

- **Q:** Why are larger orgs spending a higher %?
  **A:** Counter to the conventional "scale dilutes admin" assumption — see `methodology.md` § admin_pct_revenue. Probable drivers: more clinical service lines, more compliance overhead.

- **Q:** Why is FTE growing 2016→2025?
  **A:** Compliance burden, EHR maintenance, payor-mix complexity. See `methodology.md` § fte_2016_vs_2025.

## What This Slide Does NOT Claim

- It does not claim BHPF members are mismanaged — the framing is structural overhead, not effort.
- It does not size the savings opportunity — that's the diagnosis slide (`admin-s1`) and the conclusion slide (`admin-s5`).
- It does not include clinical FTE — only the four admin departments are surveyed.
- It does not provide member-level data — the survey is anonymized to network and tier aggregates.

## Next Slide Setup

The audience now sees their tier on the chart and where the network sits relative to the benchmark. The next slide (`admin-s1`) takes that profile and shows that the *outcomes* (AR days, denial rate, calls/FTE, turnover) are systematically worse — over-invested AND under-performing.
