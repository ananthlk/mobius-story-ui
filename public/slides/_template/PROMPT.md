# Slide generation prompt

This file is a structured prompt for turning a plain-English slide brief into
a complete slide module. Use it as the input to an LLM, or as a checklist
when hand-authoring.

The output is the **other ten files in this directory**, filled in.

---

## Inputs you must collect first

Before generating, get crisp answers to these. Vague input → vague slide.

| Field | Question to ask | Required? |
|---|---|---|
| `slug` | URL-safe id, lowercase + hyphens. Lives forever — choose carefully. | yes |
| `act` | Which act does this belong to: `intro`, `I`, `II`, `III`, `IV`, `V`, `discussion`, `appendix`? | yes |
| `audience` | Who reads this? (e.g. "BHPF CFOs", "MCO benchmarking analysts") | yes |
| `the_one_thing` | One sentence the audience should remember 24 hours later. | yes |
| `key_claim` | The argument the slide makes, in two sentences. | yes |
| `headline_numbers` | List of the numbers that appear on the slide, with units. | yes |
| `data_sources` | Where each number came from (table name, file, survey, citation). | yes |
| `methodology_summary` | How the numbers were derived — joins, scope filters, exclusions. | yes |
| `visual_concept` | Chart type, layout, interaction. (e.g. "4-panel grid with stagger animation; click each panel to drill in") | yes |
| `expected_questions` | 3–5 questions an audience member will ask about this slide. | yes |
| `out_of_scope` | What this slide does NOT address — chat will refuse / redirect. | yes |
| `skills_needed` | Which DB tools should chat be able to call here? (e.g. `medicaid_rate_lookup`, `org_peer_compare`) | yes |
| `cross_slide_links` | Other slide ids whose context is relevant if user drills sideways. | optional |

If any required field is empty or hand-wavy, **stop and ask**. Do not generate
filler content.

---

## Fill order

Generate files in this exact order. Later files reference earlier ones, so
order matters.

### 1. `data/static.json`

Build the JSONB shape first — every other file depends on its anchors.

Required structure:

```json
{
  "blocks": {
    "{block_id}": {
      "label": "Human-readable label",
      "cuts": {
        "{scope}__{filter}": { /* metric values */ }
      }
    }
  },
  "narrative_anchors": [
    { "id": "anchor_id", "value": <num>, "unit": "<str>", "source_cut": "blocks.{block}.cuts.{scope}" }
  ]
}
```

Rule: every number you'll quote in `narrative.md` MUST appear as an anchor
here. If it doesn't have provenance, don't quote it.

### 2. `data/schema.json`

Document each block and field — units, type, source. This is what chat
returns when asked "what does this field mean?". Match block_ids to
`static.json`.

### 3. `methodology.md`

How were the numbers in `static.json` derived? One section per block. Cite
tables, joins, scope filters. This is the page chat reads when asked "where
does X come from?".

### 4. `references.md`

Every external source cited in `methodology.md` gets a row here. Format:
markdown link list. Stable URLs only.

### 5. `narrative.md`

Use the structure provided in the template. Quote numbers using
`{{ANCHOR:anchor_id}}` — never bare numerals.

### 6. `system_prompt.md`

The chat brief when this slide is active. Three sections:

- **Slide summary** — one paragraph the model can hold in context.
- **Tools to call** — which `skills_needed` tool fits which question.
- **What chat cannot answer** — pointer to escalate (other slide, manual
  follow-up, refuse).

Keep under 1500 chars; this loads on every chat turn while the slide is
active.

### 7. `manifest.json`

Identity + structural metadata. Reads from the other files — leave any
field with a clear template comment if upstream data isn't ready yet.

### 8. `slide.html`

Markup. No JS, no inline styles for content (only layout where unavoidable).
Replace `.tpl-*` class prefixes with `.{slug}-*`. Use semantic structure:
eyebrow, title, lead, content blocks, footer strip.

### 9. `slide.css`

Scoped styles. Match the visual_concept. Reuse design tokens
(`var(--ink)`, `var(--mono)`, `var(--serif)`, `var(--coral)`, etc.) from
`mobius-tokens.css`.

### 10. `slide.js`

`mount(container)` and `unmount()`. Standard pattern in the template:

- Fetch data (cache-first, fallback to `data/static.json`).
- Render.
- Wire interaction (drill-in clicks, animation triggers).
- Stash any chart instances on a module-private state object so
  `unmount()` can tear them down.

---

## Quality checklist before declaring "done"

- [ ] Every number in `narrative.md` resolves to an anchor in `static.json`.
- [ ] Every block in `static.json` has a row in `schema.json`.
- [ ] Every claim in `narrative.md` has a corresponding line in
      `methodology.md`.
- [ ] Every source cited in `methodology.md` has a link in `references.md`.
- [ ] `system_prompt.md` covers every `expected_question` from the brief.
- [ ] `manifest.json > skills_available` matches `skills_needed`.
- [ ] CSS classes are namespaced `.{slug}-*` (no leaks into global).
- [ ] `slide.js` has a working `unmount()` (chart destroy, listener detach).
- [ ] `chat_context: true` only if `system_prompt.md` exists and is non-empty.
- [ ] Slide renders correctly when `data/static.json` is the only data
      source (cold-start safety) AND when API returns the same shape from
      `briefing.modules`.

If any box is unchecked, the slide is not done. Fix or downgrade scope
before merging.

---

## Anti-patterns to refuse

If the brief asks for any of these, push back:

- "Use this number — I'll find the source later." → No. No anchor, no claim.
- "Just hard-code the numbers in the HTML, we'll wire data later." → No.
  Always populate `static.json` first; the HTML reads from it. This is the
  whole provenance contract.
- "Add another tool that does X." → If X isn't in the global skills
  registry, don't invent one inline. Add to the registry first
  (`mobius-os-backend/app/pipeline/tool_manifest.py`), then reference here.
- "Make it look like the old version of slide Y." → Read slide Y's
  `slide.css` and reuse its tokens, don't fork. If the visual is shared,
  promote it to `slides/_shared/{act}.css`.

---

## Example: minimum viable brief

```
slug:                  rate-gap
act:                   I
audience:              BHPF CFOs and clinical leadership
the_one_thing:         32 of 41 shared HCPCS codes are paid below market —
                       costing the network ~$7.8M annually.
key_claim:             CMHCs and new entrants share 41 outpatient codes;
                       on 32 of those, CMHCs are reimbursed less per claim
                       than non-CMHC peers. The gap is structural —
                       same code, same patient population, lower rate.
headline_numbers:      $7.8M annual gap; 32 of 41 codes underpaid;
                       weighted-avg rate ratio 0.88
data_sources:          BQ table org_kpis_v2 (rates), bq_mart_rate_codes
                       (HCPCS join), CMS DOGE 2024 claims
methodology_summary:   For each of the 41 shared HCPCS codes, compute
                       weighted-avg paid-per-claim for CMHCs and for
                       non-CMHCs (FL, 2024). Annual gap = sum over
                       underpaid codes of (cmhc_rpc – non_cmhc_rpc) ×
                       cmhc_volume. Excludes professional fee codes.
visual_concept:        Two-column layout: left, big stat ($7.8M); right,
                       sortable table of 41 codes with paid/peer/gap
                       columns. Click row → drill-in panel with rate
                       trend chart.
expected_questions:    Q1: How is "shared code" defined?
                       Q2: What's the rate ratio per code?
                       Q3: Which codes are MOST underpaid?
                       Q4: How does this compare across states?
                       Q5: What's the projected gap if rates go to parity?
out_of_scope:          Professional-fee codes; out-of-state benchmarks
                       beyond what's in the static cuts; rate-setting
                       policy recommendations.
skills_needed:         medicaid_rate_lookup, code_definition,
                       hcpcs_state_benchmarks
cross_slide_links:     act4-opportunity (rate gap is one of the 4 buckets),
                       methodology (general scope filters)
```

A brief this complete should produce a near-final draft on the first pass.
