/*
  Slide-module loader.

  PILOT MODE: invoked from story.html when the URL contains
  ?preview-module=<slug>. Replaces the inline slide DOM for that slug
  with the loaded module. Lets us compare visual / behavior parity
  side-by-side without committing to the full migration.

  Usage:
    import { loadModule } from '/slides/_shared/loader.js';
    await loadModule('admin-s5');

  What it does:
    1. Fetch slide.html, slide.css, slide.js for the slug.
    2. Inject CSS into <head>.
    3. Find the existing <div data-id="{slug}"> in the deck and
       replace its outerHTML with slide.html.
    4. Dynamically import slide.js (ES module) and call mount(container).
    5. On unmount (slide deactivated), call slide.js's unmount().
*/

const _loadedSlugs = new Set();
const _modules    = new Map();          // slug → { mount, unmount }

export async function loadModule(slug) {
  if (_loadedSlugs.has(slug)) {
    console.warn(`[loader] ${slug} already loaded — skipping`);
    return;
  }

  const base = `/slides/${slug}`;

  // 1. Fetch the three module files in parallel
  const [htmlR, cssR] = await Promise.all([
    fetch(`${base}/slide.html`),
    fetch(`${base}/slide.css`),
  ]);

  if (!htmlR.ok || !cssR.ok) {
    console.error(`[loader] ${slug} fetch failed — html ${htmlR.status}, css ${cssR.status}`);
    return;
  }

  const html = await htmlR.text();
  const css  = await cssR.text();

  // 2. Inject scoped CSS (idempotent — keyed by slug)
  const styleId = `slide-css-${slug}`;
  if (!document.getElementById(styleId)) {
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = css;
    document.head.appendChild(style);
  }

  // 3. Replace the inline DOM for this slide
  const existing = document.querySelector(`[data-id="${slug}"]`);
  if (!existing) {
    console.error(`[loader] no inline slide with data-id="${slug}" found`);
    return;
  }
  existing.outerHTML = html;

  // 4. Dynamic-import slide.js
  let module;
  try {
    module = await import(`${base}/slide.js`);
  } catch (e) {
    console.error(`[loader] ${slug}/slide.js import failed:`, e);
    return;
  }
  if (typeof module.mount !== 'function') {
    console.error(`[loader] ${slug}/slide.js does not export mount()`);
    return;
  }
  _modules.set(slug, module);
  _loadedSlugs.add(slug);

  // 5. If the slide is currently visible, mount immediately. Otherwise
  //    attach a lazy mount that fires when the deck navigates to it.
  const container = document.querySelector(`[data-id="${slug}"]`);
  if (container && _isSlideActive(slug)) {
    await module.mount(container);
  } else {
    _attachNavHook(slug);
  }

  console.info(`[loader] ✓ ${slug} module loaded`);
}

function _isSlideActive(slug) {
  // Use the active progress dot to infer the current slide — works without
  // needing window.currentIdx exposed.
  const dots = document.querySelectorAll('#progress-dots .pdot');
  for (let i = 0; i < dots.length; i++) {
    if (dots[i].classList.contains('active')) {
      return window.SLIDES?.[i]?.id === slug;
    }
  }
  return false;
}

function _attachNavHook(slug) {
  // Patch goTo() so that when the deck navigates TO a registered slide, we
  // mount; and when it navigates AWAY from one, we unmount.
  if (window.__slideLoaderPatched) return;          // patch once
  if (typeof window.goTo !== 'function') return;

  const _origGoTo = window.goTo;
  let _previousIdx = 0; // tracked locally; updated from goTo's idx argument

  window.goTo = function patchedGoTo(idx) {
    const prevSlug = window.SLIDES?.[_previousIdx]?.id;
    const nextSlug = window.SLIDES?.[idx]?.id;

    // Unmount outgoing module
    if (prevSlug && _modules.has(prevSlug)) {
      try { _modules.get(prevSlug).unmount?.(); } catch (e) { console.warn('[loader] unmount failed', e); }
    }

    // Run original goTo (handles transform, breadcrumb, dot animations)
    _origGoTo.call(this, idx);

    // Mount incoming module after a small delay so the DOM has settled
    if (nextSlug && _modules.has(nextSlug)) {
      const container = document.querySelector(`[data-id="${nextSlug}"]`);
      if (container) {
        setTimeout(() => {
          try { _modules.get(nextSlug).mount(container); }
          catch (e) { console.warn('[loader] mount failed', e); }
        }, 80);
      }
    }

    _previousIdx = idx;
  };

  window.__slideLoaderPatched = true;
}
