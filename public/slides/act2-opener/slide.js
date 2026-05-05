/* act2-opener — anchor render only. */
const SLUG = 'act2-opener';
const _state = { data: null };

export async function mount(container) {
  unmount();
  _state.data = await _loadData();
  _renderAnchors(container);
}
export function unmount() { _state.data = null; }

async function _loadData() {
  try { const r = await fetch(`/slides/${SLUG}/data/static.json`); if (r.ok) return await r.json(); } catch {}
  return null;
}
function _renderAnchors(container) {
  const a = (_state.data?.narrative_anchors || []).reduce((m, x) => (m[x.id] = x, m), {});
  container.querySelectorAll('[data-anchor]').forEach(el => {
    const v = a[el.getAttribute('data-anchor')];
    if (v) el.textContent = _format(v);
  });
}
function _format(a) {
  const v = a.value, u = a.unit || '';
  if (u === 'days') return `${v} ${u}`;
  if (u === '%') return `${v}${u}`;
  if (u === 'calls/FTE/day') return `${v} ${u}`;
  return `${v}${u ? ' ' + u : ''}`;
}
