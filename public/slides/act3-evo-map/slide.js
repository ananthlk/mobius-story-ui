/* act3-evo-map — Tier A/B/C deep-dive map. Render via global buildEvoMap. */
const SLUG = 'act3-evo-map';
const _state = { data: null };

export async function mount(container) {
  unmount();
  _state.data = await _load();
  _render(container);
  setTimeout(() => {
    if (typeof window.buildEvoMap === 'function') { try { window.buildEvoMap(); } catch {} }
  }, 80);
}
export function unmount() { _state.data = null; }
async function _load() { try { const r = await fetch(`/slides/${SLUG}/data/static.json`); if (r.ok) return await r.json(); } catch {} return null; }
function _render(c) {
  const a = (_state.data?.narrative_anchors || []).reduce((m, x) => (m[x.id] = x, m), {});
  c.querySelectorAll('[data-anchor]').forEach(el => {
    const v = a[el.getAttribute('data-anchor')];
    if (v) el.textContent = v.value + (v.unit ? ' ' + v.unit : '');
  });
}
