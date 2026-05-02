# Slide module template

Copy this directory to `slides/{act}-{slug}/` to start a new slide. Every
file here is a working skeleton with placeholders — fill in, don't add new
files unless you have a real reason.

## Quick start

```bash
cp -r slides/_template slides/admin-s5
# rename .{slug}- CSS classes from .tpl- to .{slug}- in slide.html and slide.css
# fill in the 9 files (README.md skip — that's this file)
# add the slide to slides/index.json
```

## Why these files

| File | Source of truth for | Read by |
|---|---|---|
| `manifest.json` | Identity, blocks, skills, chat_context | Loader, chat backend |
| `slide.html` | Markup only — no inline JS, no CSS, no hardcoded numbers | Loader inserts into deck |
| `slide.css` | Scoped styles (`.{slug}-*` namespace) | Loader injects |
| `slide.js` | `mount(container)` / `unmount()` — chart builders, listeners | Loader on slide entry/exit |
| `narrative.md` | Audience-facing copy. The "what we say" | Authoring + chat |
| `methodology.md` | How every number was derived (sources, joins, scope) | Chat (when asked "where does X come from?") |
| `references.md` | Citations, external sources, follow-up reading | Chat (when asked for the receipt) |
| `system_prompt.md` | Chat instructions when this slide is active | Chat backend (loaded on slide enter) |
| `data/static.json` | Baked numbers per the JSONB contract | Slide.js render + chat fallback |
| `data/schema.json` | Field-level definitions (units, sources, types) | Chat (when asked what a field means) |

## Hard conventions (do not break)

1. **CSS namespace**: every class declared in `slide.css` starts with `.{slug}-`.
   Shared act-level styles go in a separate file (e.g. `slides/_shared/admin.css`),
   prefixed `.adm-` for the admin act.
2. **No inline JS in slide.html**. All behavior lives in `slide.js`. The deck
   strips inline `<script>` defensively; even if it didn't, mixing breaks the
   `mount`/`unmount` lifecycle.
3. **No hardcoded numbers in slide.html**. Numbers come from `data/static.json`
   (cold-start) or the briefing API (`/proxy/skills/briefing/modules/{id}`).
   Hardcoding orphans the chat's provenance graph.
4. **Every quoted number in `narrative.md` references an anchor id** declared
   in `data/static.json > narrative_anchors`. Anchor format:
   `{{ANCHOR:annual_excess}}` in markdown, resolved by the renderer.
5. **`mount()` is idempotent**. Re-entering a slide must not double-bind
   listeners or duplicate chart instances. Use `unmount()` to tear down.
6. **`chat_context: false`** for pure transition / title slides. Don't ship
   a `system_prompt.md` for those; the loader falls back to the deck-level
   default.

## When to break a convention

Almost never. If you do, leave a one-line `// CONVENTION-EXCEPTION:` comment
on the offending line with the reason. A reviewer should be able to spot it
in five seconds.

## Generating a new slide from a request

See `PROMPT.md` for the structured fill-in flow when authoring a new slide
from a plain-English brief (e.g. "I want a slide on patient leakage with a
funnel chart, audience is BHPF CFOs, key claim is each 1pp of conversion is
$3.8M").

## Lifecycle: from request → live slide

1. **Request** — plain-English brief.
2. **Apply `PROMPT.md`** — produces drafts of every file in this template.
3. **Review** — narrative, methodology, system_prompt for tone & accuracy.
4. **Drop in** — `slides/{act}-{slug}/`, register in `slides/index.json`.
5. **Seed** — push module row into `briefing.modules` (Postgres).
6. **Smoke test** — open slide in deck, click "Ask," verify chat tools
   resolve, verify data renders from cold-start static.json AND from API.
7. **Ship** — preview deploy first; production after review.
