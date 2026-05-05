# The gap isn't effort — it's the platform

## The One Thing
> Eight RCM gates × four leading platforms. The platforms cover scattered gates well; none cover all eight, and none has shared network intelligence.

## Setup
After `admin-s1` showed BHPF spending more for worse outcomes, this slide locates the cause: vendor platforms aren't built for the BH-network shape.

## The Argument
- {{ANCHOR:n_gates}} RCM gates span the claim lifecycle (Patient Engagement → Eligibility → Payor → Credentialing → Authorization → Coding & Claims → Denial Mgmt → Claim Closure).
- {{ANCHOR:n_vendors}} vendors evaluated: Netsmart, Welligent, Qualifacts, Athena.
- Each vendor has gaps. None scores 4 (Best-in-Class) on all 8.
- Critical gap: none has a network-intelligence layer (the hub at the center).

Click any platform tab to see its scorecard; play to cycle through.

## The Data
Per-gate vendor scores live in `RCM8_GATES` (global in story.html). Each cell is `{1: Legacy, 2: Emerging, 3: Modern, 4: Best-in-Class}`.

## Expected Questions
- **Q:** Why these 8 gates?  **A:** Industry-standard RCM lifecycle, mapped to BH-specific needs (e.g. credentialing as its own gate, given the 90-day Medicaid blackout).
- **Q:** Where does the data come from?  **A:** G2, Capterra, SoftwareAdvice, vendor product pages — verified reviews only.

## What This Slide Does NOT Claim
- It does not endorse any specific vendor.
- It does not size the cost gap — that's `admin-s1c` (pricing) and `admin-s5` ($66M).

## Next Slide Setup
Audience sees the platform ceiling. Next: `admin-s2b-score` flattens the orbital into a comparable scorecard table.
