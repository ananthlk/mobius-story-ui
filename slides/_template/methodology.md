# Methodology — {{Slide title}}

How every number on this slide was derived. One section per block in
`data/static.json`. This file is what chat reads when asked "where does
{{X}} come from?".

---

## {{block_id_1}} — {{Block label}}

**Source tables / files:**
- `{{schema.table}}` (BQ project `{{project}}`)
- `{{file.json}}` (static fact pack)

**Scope filters:**
- State: FL only
- Year: 2024 (annual aggregate; partial Nov–Dec for v2 marts)
- Org universe: {{e.g. all_cmhc, bhpf members, fl_bh_specialty}}
- Code universe: {{e.g. 81 FL BH HCPCS codes per fl_bh_code_reference}}

**Joins:**
- {{Describe each join, with the join key.}}

**Computation:**
1. {{Step-by-step computation. Include filter logic, aggregation, rate
   formulas. A reviewer should be able to reproduce this in SQL/Python
   from this section alone.}}
2. {{...}}

**Anchors derived from this block:**
- `{{anchor_id_1}}` — {{which cell of static.json.blocks.{block_id_1}.cuts maps to this anchor}}

**Known limitations:**
- {{Things this number does NOT account for. E.g. "excludes professional
  fee codes", "does not adjust for service mix differences", etc.}}

**Last refreshed:** {{date}}, source job `{{job_name}}`.

---

## {{block_id_2}} — {{Block label}}

(Repeat the structure above for each block.)

---

## Cross-cutting notes

- **Currency**: all dollars in nominal USD, not inflation-adjusted unless
  explicitly noted.
- **Time grain**: annual rollups unless the block explicitly says monthly.
- **Beneficiary counts**: unduplicated within (year, org), summed across
  orgs for network totals.
