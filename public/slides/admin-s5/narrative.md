# What the admin evidence establishes

## The One Thing

> The {{ANCHOR:annual_overhead}} admin gap is structural, not a management failure — and the BHPF network already has the scale to recover it.

## Setup

Acts I–II have shown the admin profile slide-by-slide: BHPF runs at 11.7% admin vs 9.0% benchmark, AR days at 84 vs 28 benchmark, denial rate at 18% vs 5.7% benchmark. The audience has seen the metrics. This slide compresses what those metrics together actually establish — and what they don't.

## The Argument

Four conclusions, each backed by data already shown earlier in the act:

1. **Structural, not accidental.** {{ANCHOR:fte_excess}} excess FTE across {{ANCHOR:n_orgs}} orgs producing {{ANCHOR:annual_overhead}}/yr in pure overhead is the predictable output of running 34 separate back-offices at sub-scale, not a failure of any individual member's management.

2. **Vendor pricing is calibrated for someone else.** Vendor 2:1 ROI math is validated at {{ANCHOR:vendor_validation_size}} system size. At BHPF's {{ANCHOR:bhpf_avg_org_revenue}} average, the same fixed sales-and-integration costs consume {{ANCHOR:fixed_cost_low}}–{{ANCHOR:fixed_cost_high}} of every deal — leaving no room for vendor margin or member ROI.

3. **AI alone does not fix it.** Deploying AI on 34 separate orgs gives 34 slightly faster broken processes — no shared learning, no network intelligence, no scale economics.

4. **Scale is already present — the constraint is governance.** At {{ANCHOR:combined_revenue}} combined, BHPF already sits in the vendor sweet spot. The CoE consolidation captures ~{{ANCHOR:scale_dividend}} from scale alone; AI layered on top adds another ~{{ANCHOR:ai_dividend}} — {{ANCHOR:annual_overhead}} total. The decision is whether the network organizes to act as one.

## The Data

| Metric | Anchor | Value | Source |
|---|---|---|---|
| Excess admin FTE (network) | `fte_excess` | 345 | CFO Survey 2025 vs APQC $1B+ benchmark |
| Annual admin overhead | `annual_overhead` | $66M | derived: 2.7pp gap × $1.1B + AI dividend |
| Recoverable from scale | `scale_dividend` | $37M | derived: APQC $1B+ FTE benchmark applied to BHPF revenue |
| Recoverable from AI on top | `ai_dividend` | $29M | AI CoE estimate (denial engine, AR automation, intake routing) |
| Vendor ROI validation size | `vendor_validation_size` | $500M | vendor pitch decks reviewed in Act II |
| BHPF average org revenue | `bhpf_avg_org_revenue` | $32M | org_kpis_v2 (FL, 2024) |
| Fixed-cost share at $32M (low) | `fixed_cost_low` | 50% | Act II pricing-trap chart |
| Fixed-cost share at $32M (high) | `fixed_cost_high` | 68% | Act II pricing-trap chart |
| Combined network revenue | `combined_revenue` | $1.1B | org_kpis_v2 (FL, 2024, BHPF members) |
| Member org count | `n_orgs` | 34 | BHPF directory |

Every row corresponds to one anchor in `data/static.json > narrative_anchors`.

## Expected Questions

- **Q:** Why 11.7% vs 9.0% — is APQC the right benchmark for behavioral health?
  **A:** APQC $1B+ is the closest cross-industry benchmark for back-office spend at health-system scale. BH-specific data isn't published. See `methodology.md` § benchmark sourcing.

- **Q:** How is the $37M scale dividend separated from the $29M AI dividend?
  **A:** Scale dividend is the FTE reduction predicted by applying APQC FTE-per-revenue ratios to BHPF's $1.1B; AI dividend is the additional reduction from automation layered on the consolidated stack. See `methodology.md` § admin_overhead.

- **Q:** Doesn't AI work without consolidation?
  **A:** Tools work; a network intelligence layer doesn't. AI on 34 fragmented data stacks can't share learning across denials, intake patterns, or rate signals. The slide claims AI without consolidation = 34 slightly faster broken processes — see `narrative.md` § argument 3.

- **Q:** Where does the $66M get captured first?
  **A:** Act V — Phase 1 (months 0–12) targets ~$22M (governance, credentialing, unified rate work); Phase 2 (12–24) reaches ~$41M cumulative; Phase 3 (24–36) hits $69M+ run-rate. See cross-slide link `act5-approach`.

## What This Slide Does NOT Claim

- It does not claim AI is unnecessary — only that AI alone doesn't capture the gap. AI on top of consolidation captures ~$29M.
- It does not claim BHPF members are mismanaged — the explicit framing is "structural, not accidental."
- It does not size patient leakage, employee churn, or rate gap — those are buckets in Act IV. This slide is admin-only.
- It does not specify governance form (single entity vs federated) — that's Act III / Act V.

## Next Slide Setup

The audience now believes admin is a structural problem worth $66M, AI alone won't solve it, and the network already has the scale. The next act (Act III) shows the same dynamic on the revenue side — clinician churn, panel displacement, and rate compression — and brings the total opportunity into the four-bucket frame ($144M–$217M).
