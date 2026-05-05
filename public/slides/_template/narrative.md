# {{Slide title}}

## The One Thing

> One sentence. What should the audience remember 24 hours later?

## Setup

What the audience needs to believe before this slide lands. One paragraph.

## The Argument

What this slide proves, and how. Be specific — quote the actual numbers
shown using anchor refs:

> {{ANCHOR:headline_anchor}} of the gap is structural — same code, same
> patient, lower rate.

Anchor refs resolve at render time from `data/static.json > narrative_anchors`.
Never write a bare numeral here.

## The Data

| Metric | Anchor | Value | Source |
|---|---|---|---|
| {{Metric name}} | `{{anchor_id}}` | {{value}} | {{citation}} |

Every row corresponds to one anchor in `data/static.json`. If you add a row
here, add the anchor there. If you delete a row here, delete the anchor too.

## Expected Questions

- **Q:** How was {{X}} measured?
  **A:** See `methodology.md` § {{section}}.

- **Q:** Is this comparable to my org specifically?
  **A:** {{Yes/no/depends — and how chat would route the answer}}

- **Q:** What's the fix?
  **A:** {{Pointer to the next-act slide that covers this}}

## What This Slide Does NOT Claim

Explicit caveats. Important for credibility — and important for chat,
which uses this section to refuse out-of-scope questions.

- {{Claim chat will refuse to make}}
- {{Claim chat will defer to a different slide for}}
- {{Claim that requires a tool not in skills_available}}

## Next Slide Setup

What belief this slide leaves the audience with, that the next slide
builds on. One sentence.
