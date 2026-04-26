# Slide Module Specification
> Working contract for the monolith-to-modules refactor.  
> All new slides should be authored with this structure in mind, even while they live in `story.html`.

---

## 1. Module Identity

Every slide is a self-contained module. Its identity is declared once and referenced everywhere:

```json
// manifest.json
{
  "id": "admin-diagnosis",
  "slug": "admin-s1",
  "title": "Under-invested. Worst outcomes for your scale.",
  "act": "admin",
  "sequence": 1,
  "chapter": "The Diagnosis",
  "tags": ["admin", "benchmarking", "FTE", "denial-rate", "AR-days"],

  // ── Data blocks ────────────────────────────────────────────────────────────
  // Each block is an independently addressable unit of content on the slide.
  // live   = fetched from a skill endpoint at render time (reflects latest data)
  // static = baked into data/*.json at build/survey time (does not change in session)
  // hybrid = static baseline + live org-specific overlay
  "blocks": [
    {
      "id": "fte-comparison-chart",
      "label": "Avg FTE per org — BHPF vs PCP",
      "data_mode": "hybrid",
      "static_source": "cfo_survey_2025",        // BHPF bars — from survey JSON
      "live_source": null,                        // no live override for this block
      "endpoint": null,
      "chat_context": false                       // chart speaks for itself; no chat needed
    },
    {
      "id": "finance-ar-days",
      "label": "Finance · Days in AR",
      "data_mode": "live",
      "static_source": null,
      "live_source": "cfo_survey_2025",
      "endpoint": "/analytics/cfo-admin-benchmarks?tier=all",
      "chat_context": true,                       // chat can drill into this metric
      "chat_tools": ["get_cfo_admin_benchmarks"],
      "chat_scope": "What is BHPF's AR days figure, how does it compare by org size tier, and what drives the gap vs the MGMA benchmark?"
    },
    {
      "id": "billing-denial-rate",
      "label": "Billing / RCM · Denial Rate",
      "data_mode": "static",
      "static_source": "ads_simitree_2026",       // external benchmark, won't change
      "live_source": null,
      "endpoint": null,
      "chat_context": true,
      "chat_tools": [],                            // no tool — chat answers from RAG
      "chat_scope": "What is the BHPF denial rate, what is the benchmark, and what causes the gap?"
    },
    {
      "id": "it-calls-per-fte",
      "label": "IT / IS · Calls per FTE/day",
      "data_mode": "live",
      "static_source": null,
      "live_source": "cfo_survey_2025",
      "endpoint": "/analytics/cfo-admin-benchmarks?tier=all",
      "chat_context": false                        // derived metric; low expected question volume
    },
    {
      "id": "hr-turnover",
      "label": "HR + Payroll · Turnover Rate",
      "data_mode": "static",
      "static_source": "nsi_workforce_2024",
      "live_source": null,
      "endpoint": null,
      "chat_context": true,
      "chat_tools": [],
      "chat_scope": "What is BH sector turnover rate, what does it cost per role, and how does shared HR address it?"
    }
  ],

  // ── Slide-level chat ────────────────────────────────────────────────────────
  // chat_context: true means loading system_prompt.md when this slide is active.
  // Set false for transition/title slides with no drillable data.
  "chat_context": true,
  "rag_corpus": ["bhpf_cfo_survey_2025.pdf", "mgma_databook_2024.pdf", "ads_simitree_bh_denial_2026.pdf"]
}
```

### Data mode definitions

| Mode | Meaning | Rendered how |
|------|---------|--------------|
| `live` | Fetched from skill endpoint at slide mount time | JS `fetch()` on `goTo()` |
| `static` | Baked into `data/*.json` at survey/build time | Loaded once, cached in memory |
| `hybrid` | Static baseline + live org-specific overlay | Static loads first; live patch applied after |

### Chat context rules

| `chat_context` | Meaning |
|----------------|---------|
| Block: `false` | Block's numbers are self-explanatory; chat gets no extra context for it |
| Block: `true` | Block registers a `chat_scope` — the specific question domain chat is prepared to answer |
| Slide: `false` | No `system_prompt.md` loaded; chat falls back to global context |
| Slide: `true` | `system_prompt.md` injected when slide becomes active |

**Not every block needs chat context.** A chart that just illustrates a point visually (FTE comparison bars) doesn't need chat support. A metric card with a specific number that someone might challenge (18% denial rate) does.

---

## 2. Directory Structure (target state)

```
slides/
└── {act}-{slug}/
    ├── manifest.json        # identity, blocks (data_mode + chat_context per block)
    ├── slide.html           # markup only — no inline JS, no CSS
    ├── slide.css            # scoped styles (.{slug}-* namespace)
    ├── slide.js             # mount() / unmount() — chart builders, data loaders
    ├── narrative.md         # talking points, argument, data table, expected Qs
    ├── system_prompt.md     # present only if slide chat_context: true
    ├── data/
    │   ├── static.json      # baked survey/benchmark data (data_mode: static | hybrid)
    │   └── schema.json      # describes fields, units, sources for each data point
    ├── api/
    │   └── routes.py        # present only if any block has data_mode: live | hybrid
    └── rag_docs/
        └── *.pdf / *.md     # present only if rag_corpus is non-empty
```

> `system_prompt.md`, `api/`, and `rag_docs/` are **optional** — only created when the manifest requires them. A title or transition slide may have only `manifest.json`, `slide.html`, `slide.css`, and `narrative.md`.

---

## 3. Narrative Template

Every slide must have a `narrative.md`. This is the source of truth for what the slide says and why.

```markdown
# {Slide Title}

## The One Thing
> One sentence. What should the audience remember 24 hours later?

## Setup
What the audience needs to believe before this slide lands.

## The Argument
What this slide proves, and how. Be specific — reference the actual numbers shown.

## The Data
| Metric | Value | Source | Notes |
|--------|-------|--------|-------|
| BHPF denial rate | 18% | ADS/SimiTree BH 2026 | avg across 34 members |
| Benchmark denial rate | 5.7% | athenahealth network Mar 2024 | |

## Expected Questions
- Q: How was this measured?
- Q: Is this comparable to our org specifically?
- Q: What's the fix?

## What This Slide Does NOT Claim
(explicit caveats — important for credibility)

## Next Slide Setup
What belief this slide leaves the audience with, that the next slide builds on.
```

---

## 4. System Prompt Template

Every slide has a `system_prompt.md`. When the user is on this slide, chat loads this context.

```markdown
# Chat Context: {Slide Title}

## Slide Summary
One paragraph describing what this slide shows and argues.

## Data Available
List every number on the slide with its source and definition.
- **BHPF denial rate (18%)** — average across 34 BHPF member orgs, from ADS/SimiTree BH Denial Benchmark 2026. Defined as initial claim denial rate before appeals.
- **Benchmark denial rate (5.7%)** — athenahealth network average, March 2024.

## Tools to Call
| Question type | Tool | Parameters |
|---------------|------|------------|
| Tier-specific admin data | `get_cfo_admin_benchmarks` | `tier: sm | mid | lg | all` |
| Org-specific comparison | `get_org_benchmark` | `org_name, metric` |

## What Chat Can Answer
- Definition and source of any number on this slide
- Tier breakdowns (small/mid/large org) for CFO survey data
- How a specific org compares

## What Chat Cannot Answer (escalate)
- Individual org denial rates (not in survey)
- Claims-level denial data (requires BQ query)
- Benchmark data for states other than FL

## Tone
Analytical, direct. This is a diagnosis slide — reinforce the problem, don't soften it.
```

---

## 5. API Template

Every slide's endpoints follow a consistent pattern:

```python
# api/routes.py
"""
{act}-{slug} — {Slide Title}

Endpoints:
  GET  /{slug}/data          — primary data payload for this slide
  GET  /{slug}/context       — narrative + system_prompt for chat
"""
from __future__ import annotations
import json
from pathlib import Path
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/{slug}", tags=["{act}"])
DATA_DIR = Path(__file__).parent.parent / "data"


@router.get("/data")
def get_slide_data(tier: str = "all") -> dict:
    """Primary data for the slide. Tier: all | sm | mid | lg."""
    try:
        with open(DATA_DIR / "{slug}.json") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Slide data not found")


@router.get("/context")
def get_slide_context() -> dict:
    """Returns narrative + system_prompt for chat context injection."""
    narrative = (Path(__file__).parent.parent / "narrative.md").read_text()
    system_prompt = (Path(__file__).parent.parent / "system_prompt.md").read_text()
    return {"narrative": narrative, "system_prompt": system_prompt}
```

---

## 6. CSS Namespace Convention

All slide styles are scoped to a `{slug}-*` prefix to avoid collisions:

```css
/* admin-s1 scope */
.adm-s1-card { ... }
.adm-s1-value { ... }

/* Shared admin namespace (all admin slides) */
.adm-title { ... }
.adm-lead { ... }
.adm-eyebrow { ... }
```

Shared namespace styles (`adm-*`) live in a shared `admin.css`. Slide-specific styles are in `slide.css`.

---

## 7. JS Module Convention

Slide JS exposes exactly two functions:

```javascript
// slide.js
// mount(container) — called by the deck when this slide becomes active
// unmount()        — called when navigating away (destroy charts, cancel fetches)

export function mount(container) {
  // 1. load data (fetch or use cache)
  // 2. build charts
  // 3. wire listeners
}

export function unmount() {
  // destroy Chart.js instances
  // cancel any pending fetches
}
```

The deck's `goTo(idx)` calls `unmount()` on the outgoing slide and `mount(container)` on the incoming one.

---

## 8. Chat Integration Convention

When the user navigates to a slide, the deck posts to chat:

```javascript
// deck.js
async function goTo(idx) {
  const slide = SLIDES[idx];
  outgoing?.unmount();
  incoming.mount(container);

  // notify chat of active slide context
  await fetch('/chat/slide-context', {
    method: 'POST',
    body: JSON.stringify({ slide_id: slide.id })
  });
}
```

Chat uses `slide_id` to load the matching `system_prompt.md` and `manifest.json` and inject them as context for the session.

---

## 9. Checklist — "Is This Slide Done?"

**Every slide**
- [ ] `manifest.json` exists with correct `id`, `slug`, `act`, `sequence`
- [ ] Every block has `data_mode` declared (`live` / `static` / `hybrid`)
- [ ] Every block has `chat_context` declared (`true` / `false`)
- [ ] Markup is clean — no inline data constants, no hardcoded numbers in HTML
- [ ] All numbers on the slide have a row in `narrative.md > Data`
- [ ] `narrative.md` has Expected Questions filled in
- [ ] `narrative.md` has "What This Slide Does NOT Claim" filled in

**If any block is `data_mode: live` or `hybrid`**
- [ ] API endpoint exists, returns data, and is documented in `manifest.json`
- [ ] `data/schema.json` describes every field returned (units, source, definition)
- [ ] Slide falls back gracefully if the endpoint is unreachable (static values remain visible)

**If any block has `chat_context: true`**
- [ ] `chat_scope` is filled in for that block in `manifest.json`
- [ ] `system_prompt.md` covers that block's metric (source, definition, expected questions)
- [ ] Chat can answer: *"Where does [X] come from?"* for every `chat_context: true` block
- [ ] Chat can answer: *"How does [org] compare on [X]?"* if a comparison endpoint exists

**If slide `chat_context: false`** (title / transition slides)
- [ ] Confirm no numbers on the slide that an audience member would challenge
- [ ] No `system_prompt.md` needed — confirm and leave absent

---

## 10. Monolith → Module Migration Plan

When the story is locked, migrate each slide in one pass:

1. Extract HTML → `slide.html`
2. Extract CSS → `slide.css` (rename classes to scoped namespace)
3. Extract JS → `slide.js` (wrap in `mount/unmount`)
4. Write `narrative.md` from the slide's `adm-lead` text + known context
5. Write `system_prompt.md` from `narrative.md > Data` table
6. Move `data/*.json` to slide's `data/` directory
7. Move API endpoints to slide's `api/routes.py`
8. Write `manifest.json`
9. Run checklist

**Estimated effort per slide:** 1–2 hours once the pattern is established.  
**Total for 43-slide deck:** ~3–4 days (parallelisable by act).

---

*Last updated: 2026-04-24*  
*Owner: story-ui*
