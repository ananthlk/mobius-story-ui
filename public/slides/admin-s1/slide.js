/* admin-s1 — diagnosis: anchor render + FTE-vs-PCP bar chart. */

const SLUG = 'admin-s1';
const ADM_A = '#BA7517';
const ADM_G = '#1D9E75';
const ADM_GR = '#A09D98';

const _state = { data: null, charts: [] };

export async function mount(container) {
  unmount();
  _state.data = await _loadData();
  _renderAnchors(container);
  _renderFteChart(container);
}

export function unmount() {
  _state.charts.forEach(c => { try { c.destroy(); } catch {} });
  _state.charts = [];
}

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
  return `${v}${u ? ' ' + u : ''}`;
}

function _renderFteChart(container) {
  if (typeof Chart === 'undefined') return;
  const canvas = container.querySelector('[data-canvas="fte-bhpf-vs-pcp"]');
  if (!canvas) return;
  const cuts = _state.data?.blocks?.fte_vs_pcp?.cuts || {};
  const bhpf = cuts['bhpf__mid'] || {};
  const pcp = cuts['pcp__benchmark'] || {};
  const labels = ['Finance', 'IT', 'Billing/RCM', 'HR'];
  const keys = ['finance', 'it', 'billing', 'hr'];
  const chart = new Chart(canvas, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        { label: 'BHPF', data: keys.map(k => bhpf[k] || 0), backgroundColor: ADM_A, borderRadius: 4 },
        { label: 'PCP benchmark', data: keys.map(k => pcp[k] || 0), backgroundColor: ADM_G, borderRadius: 4 },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { color: ADM_GR, font: { size: 11 } } },
        y: { ticks: { color: ADM_GR, font: { size: 10 } }, grid: { color: 'rgba(0,0,0,.05)' } },
      },
    },
  });
  _state.charts.push(chart);
}
