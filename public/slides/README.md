# slides/ — per-slide modules

Sprint 1 scaffolding. Final shape per `SLIDE_MODULE_SPEC.md`.

## What goes where

```
slides/
  index.json              ← single source of truth for slide order + metadata
  _shared/
    chat-panel.{html,css,js}   ← shared chat UI imported by every slide
    loader.js                  ← fetches modules from briefing.modules table
  {act}-{slug}/
    manifest.json         ← id, slug, sequence, blocks, chat_context, skills
    slide.html            ← markup only
    slide.css             ← scoped styles
    slide.js              ← mount(container) / unmount()
```

## Data flow

```
slide.js mount()
   │
   ▼
loader.js → /proxy/skills/briefing/modules/{id}
                  │
                  ▼
       provider-roster-credentialing
       /briefing/routes.py
                  │
                  ▼
       briefing.modules (Postgres)
```

## Status

- [ ] Sprint 1 / commit 1: scaffolding (this file)
- [ ] Sprint 1 / commit 2: drop 21 dead appendix slides
- [ ] Sprint 1 / commit 3: migrate 6 keystone slides to module structure
- [ ] Sprint 1 / commit 4: shared chat panel + persistent "Ask" button
- [ ] Sprint 1 / commit 5: wire 2 production-grade DB skills
- [ ] Sprint 1 / commit 6: preview deploy
- [ ] Sprint 1 / commit 7: merge + production deploy
