/*
  Slide module — mount/unmount lifecycle.

  The deck loader calls mount(container) when this slide becomes active
  and unmount() when navigating away. Both must be idempotent.

  CONVENTIONS:
  - Module-private state lives on `_state` below. Reset on every mount.
  - Fetch data with the cache-first pattern (see _loadData).
  - Use stagger-in animation by toggling .{slug}-*.in classes on the
    blocks you want to animate. Pattern matches slide.css.
  - Drill-in clicks call the deck-level drillIn() — don't invent your
    own panel.

  Replace `tpl` with the actual slug (e.g. `admin-s5`) when copying.
*/

// Module-private state. Reset by unmount() and mount().
const _state = {
  data: null,
  charts: [],
  listeners: [],
  animTimers: [],
};

/**
 * mount(container) — called by the deck when this slide becomes active.
 *
 * Order:
 *   1. Load data (cache-first)
 *   2. Render anchors (numbers from data into [data-anchor] elements)
 *   3. Build any charts
 *   4. Wire interaction listeners
 *   5. Trigger stagger-in animation
 */
export async function mount(container) {
  unmount(); // belt + suspenders for re-entry

  _state.data = await _loadData();
  if (!_state.data) {
    console.warn('[tpl] no data — rendering with placeholders');
  }

  _renderAnchors(container);
  _buildCharts(container);
  _wireInteraction(container);
  _animateIn(container);
}

/**
 * unmount() — called when navigating away. Tear down everything mount() built.
 */
export function unmount() {
  // Destroy any chart instances (Chart.js, D3, etc.)
  _state.charts.forEach(c => { try { c.destroy?.(); } catch {} });
  _state.charts = [];

  // Detach listeners
  _state.listeners.forEach(({ el, ev, fn }) => {
    try { el.removeEventListener(ev, fn); } catch {}
  });
  _state.listeners = [];

  // Cancel stagger-in timers
  _state.animTimers.forEach(t => clearTimeout(t));
  _state.animTimers = [];
}

// ── Data loading ─────────────────────────────────────────────

async function _loadData() {
  // 1. Try the live briefing API (single source of truth in production).
  try {
    const moduleId = '{{slug}}';
    const r = await fetch(`/proxy/skills/briefing/modules/${moduleId}`);
    if (r.ok) return await r.json();
  } catch (e) {
    console.warn('[tpl] live briefing fetch failed:', e.message);
  }

  // 2. Fall back to the baked static.json shipped with this slide.
  try {
    const r = await fetch(`/slides/{{slug}}/data/static.json`);
    if (r.ok) return await r.json();
  } catch (e) {
    console.warn('[tpl] static.json fallback failed:', e.message);
  }

  return null;
}

// ── Rendering ────────────────────────────────────────────────

function _renderAnchors(container) {
  const anchors = _state.data?.narrative_anchors || [];
  const byId = Object.fromEntries(anchors.map(a => [a.id, a]));

  container.querySelectorAll('[data-anchor]').forEach(el => {
    const id = el.getAttribute('data-anchor');
    const a = byId[id];
    if (!a) {
      el.textContent = '—';
      return;
    }
    el.textContent = _formatAnchor(a);
  });
}

function _formatAnchor(a) {
  // Render as `${value}${unit}` with sensible defaults.
  const v = a.value;
  const u = a.unit || '';
  if (u === 'M' || u === 'B' || u === 'K') return `$${v}${u}`;
  if (u === 'pp' || u === '%')              return `${v}${u}`;
  if (u === 'FTE')                          return `${v} FTE`;
  return `${v}${u ? ' ' + u : ''}`;
}

function _buildCharts(container) {
  // Build any Chart.js / D3 / SVG instances here. Stash on _state.charts.
  // Example:
  //   const chart = new Chart(canvas, config);
  //   _state.charts.push(chart);
}

// ── Interaction ──────────────────────────────────────────────

function _wireInteraction(container) {
  // Drill-in clicks are wired declaratively in slide.html via
  // onclick="drillIn(...)" — no need to bind here.

  // Bind any module-specific listeners and stash them so unmount() can
  // detach. Example:
  //
  //   const tab = container.querySelector('.{{slug}}-tab');
  //   const onClick = () => _switchTab('foo');
  //   tab.addEventListener('click', onClick);
  //   _state.listeners.push({ el: tab, ev: 'click', fn: onClick });
}

// ── Animation ────────────────────────────────────────────────

function _animateIn(container) {
  const blocks = container.querySelectorAll('.tpl-block');
  // Reset (in case of re-entry — animation must replay)
  blocks.forEach(b => b.classList.remove('in'));

  // Stagger 140ms per block — matches admin-s5 / discussion pattern.
  blocks.forEach((b, i) => {
    const t = setTimeout(() => b.classList.add('in'), 80 + i * 140);
    _state.animTimers.push(t);
  });
}
