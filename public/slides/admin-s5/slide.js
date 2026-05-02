/*
  admin-s5 — Act II conclusion module.

  Pilot-mode: data loads from /slides/admin-s5/data/static.json.
  When briefing.modules table is live, swap the live fetch URL.
*/

const SLUG = 'admin-s5';

const _state = {
  data: null,
  animTimers: [],
};

export async function mount(container) {
  unmount();

  _state.data = await _loadData();
  if (!_state.data) {
    console.warn(`[${SLUG}] no data — anchors will show em dashes`);
  }

  _renderAnchors(container);
  _animateIn(container);
}

export function unmount() {
  _state.animTimers.forEach(t => clearTimeout(t));
  _state.animTimers = [];
}

async function _loadData() {
  // Live briefing API (not yet deployed — fails fast, falls through)
  try {
    const r = await fetch(`/proxy/skills/briefing/modules/${SLUG}`);
    if (r.ok) return await r.json();
  } catch (_) { /* fall through */ }

  // Cold-start fallback: shipped static.json
  try {
    const r = await fetch(`/slides/${SLUG}/data/static.json`);
    if (r.ok) return await r.json();
  } catch (e) {
    console.warn(`[${SLUG}] static.json fallback failed:`, e.message);
  }

  return null;
}

function _renderAnchors(container) {
  const anchors = _state.data?.narrative_anchors || [];
  const byId = Object.fromEntries(anchors.map(a => [a.id, a]));

  container.querySelectorAll('[data-anchor]').forEach(el => {
    const id = el.getAttribute('data-anchor');
    const a = byId[id];
    el.textContent = a ? _formatAnchor(a) : '—';
  });
}

function _formatAnchor(a) {
  const v = a.value;
  const u = a.unit || '';
  if (u === 'M' || u === 'B' || u === 'K') return `$${v}${u}`;
  if (u === 'pp' || u === '%')              return `${v}${u}`;
  if (u === 'FTE')                          return `${v} FTE`;
  if (u === 'count')                        return String(v);
  return `${v}${u ? ' ' + u : ''}`;
}

function _animateIn(container) {
  const panels = container.querySelectorAll('.admin-s5-panel');
  panels.forEach(p => p.classList.remove('in'));
  panels.forEach((p, i) => {
    const t = setTimeout(() => p.classList.add('in'), 80 + i * 140);
    _state.animTimers.push(t);
  });
}
