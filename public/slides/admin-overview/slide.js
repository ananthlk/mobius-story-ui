/*
  admin-overview — Act II opener.

  Demonstrates "skill-driven slide" pattern:
  - Primary data path: cfo_admin_benchmarks skill (per-tier).
  - Cold-start fallback: data/static.json shipped with the module.
  - Tab interaction → re-call skill with new tier param.
*/

const SLUG = 'admin-overview';

const ADM_A = '#BA7517';
const ADM_GR = '#A09D98';

const _state = {
  data: null,
  charts: [],
  listeners: [],
  currentTier: 'all',
};

export async function mount(container) {
  unmount();
  _state.data = await _loadData();
  _renderTier(container, _state.currentTier);
  _wireTabs(container);
}

export function unmount() {
  _state.charts.forEach(c => { try { c.destroy?.(); } catch {} });
  _state.charts = [];
  _state.listeners.forEach(({ el, ev, fn }) => {
    try { el.removeEventListener(ev, fn); } catch {}
  });
  _state.listeners = [];
  _state.currentTier = 'all';
}

// ── Data ────────────────────────────────────────────────────

async function _loadData() {
  // Primary: live cfo_admin_benchmarks skill via the proxy
  try {
    const r = await fetch('/proxy/skills/analytics/cfo-admin-benchmarks?tier=all');
    if (r.ok) {
      const live = await r.json();
      // The skill returns the same shape as admin_benchmarks.json's "data".
      // Adapt to our static.json shape so the renderer stays uniform.
      return _adaptLiveSkillResponse(live);
    }
  } catch (_) { /* fall through */ }

  // Fallback: shipped static.json
  try {
    const r = await fetch(`/slides/${SLUG}/data/static.json`);
    if (r.ok) return await r.json();
  } catch (e) {
    console.warn(`[${SLUG}] static.json fallback failed:`, e.message);
  }
  return null;
}

function _adaptLiveSkillResponse(live) {
  // Live skill returns { all: {...}, sm: {...}, mid: {...}, lg: {...}, all_2016: {...} }
  // Map into the static.json shape so _renderTier doesn't care which path served it.
  const tiers = ['all', 'sm', 'mid', 'lg'];
  const out = {
    blocks: { admin_kpi: { cuts: {} }, fte_by_dept: { cuts: {} }, fte_2016_vs_2025: { cuts: {} } },
    narrative_anchors: [],
  };
  for (const t of tiers) {
    const s = live[t] || {};
    out.blocks.admin_kpi.cuts[`bhpf__${t}`] = {
      admin_pct_revenue_avg: s.admin_pct_revenue?.avg,
      total_fte_avg: s.total_fte?.avg,
      n: s.n,
    };
    const dept = s.staff_by_dept || {};
    out.blocks.fte_by_dept.cuts[`bhpf__${t}`] = {
      finance: dept.accounting_payroll?.avg_fte,
      it:      dept.it_is?.avg_fte,
      billing: dept.billing?.avg_fte,
      hr:      dept.hr?.avg_fte,
    };
  }
  const old = live.all_2016?.staff_by_dept || {};
  out.blocks.fte_2016_vs_2025.cuts['bhpf__2016'] = {
    finance: old.accounting_payroll?.avg_fte,
    it:      old.it_is?.avg_fte,
    billing: old.billing?.avg_fte,
    hr:      old.hr?.avg_fte,
  };
  out.blocks.fte_2016_vs_2025.cuts['bhpf__2025'] = out.blocks.fte_by_dept.cuts['bhpf__all'];
  return out;
}

// ── Render ──────────────────────────────────────────────────

function _renderTier(container, tier) {
  if (!_state.data) return;
  _renderKpiPanel(container, tier);
  _renderFteByDept(container, tier);
  _renderTrend(container);
}

function _renderKpiPanel(container, tier) {
  const cuts = _state.data.blocks?.admin_kpi?.cuts || {};
  const k = cuts[`bhpf__${tier}`] || {};
  const pct = k.admin_pct_revenue_avg != null ? (k.admin_pct_revenue_avg * 100).toFixed(1) + '%' : '—';
  const fte = k.total_fte_avg != null ? Math.round(k.total_fte_avg) + ' FTE avg' : '—';
  const n   = k.n != null ? k.n + ' orgs' : '—';

  const fteCuts = _state.data.blocks?.fte_by_dept?.cuts || {};
  const dept = fteCuts[`bhpf__${tier}`] || {};
  const labels = { finance: 'Finance', it: 'IT', billing: 'Billing/RCM', hr: 'HR' };
  const topKey = Object.keys(labels).reduce((a, b) => (dept[a] || 0) >= (dept[b] || 0) ? a : b, 'finance');

  const root = container.querySelector(`[data-block="admin_kpi"]`);
  if (!root) return;
  const big = root.querySelector('[data-anchor="admin_pct_avg"]');
  if (big) big.textContent = pct;
  _setField(root, 'total_fte', fte);
  _setField(root, 'n', n);
  _setField(root, 'top_dept', labels[topKey] || '—');
}

function _setField(root, name, val) {
  const el = root.querySelector(`[data-field="${name}"]`);
  if (el) el.textContent = val;
}

function _renderFteByDept(container, tier) {
  if (typeof Chart === 'undefined') return;
  const cuts = _state.data.blocks?.fte_by_dept?.cuts || {};
  const dept = cuts[`bhpf__${tier}`] || {};
  const canvas = container.querySelector('[data-canvas="fte-by-dept"]');
  if (!canvas) return;

  _killChart('fte-by-dept');
  const labels = ['Finance', 'IT', 'Billing/RCM', 'HR'];
  const vals = [dept.finance, dept.it, dept.billing, dept.hr].map(v => +(v || 0).toFixed(2));

  const chart = new Chart(canvas, {
    type: 'bar',
    data: { labels, datasets: [{ label: 'Avg FTE/org', data: vals, backgroundColor: ADM_A, borderRadius: 4 }] },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { color: ADM_GR, font: { size: 11 } } },
        y: { ticks: { color: ADM_GR, font: { size: 11 } }, grid: { color: 'rgba(0,0,0,.05)' } },
      },
    },
  });
  chart._slug = 'fte-by-dept';
  _state.charts.push(chart);
}

function _renderTrend(container) {
  if (typeof Chart === 'undefined') return;
  const cuts = _state.data.blocks?.fte_2016_vs_2025?.cuts || {};
  const old = cuts['bhpf__2016'] || {};
  const cur = cuts['bhpf__2025'] || {};
  const canvas = container.querySelector('[data-canvas="fte-2016-vs-2025"]');
  if (!canvas) return;

  _killChart('fte-2016-vs-2025');
  const labels = ['Finance', 'IT', 'Billing/RCM', 'HR'];
  const cur16 = [old.finance, old.it, old.billing, old.hr].map(v => +(v || 0).toFixed(2));
  const cur25 = [cur.finance, cur.it, cur.billing, cur.hr].map(v => +(v || 0).toFixed(2));

  const chart = new Chart(canvas, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        { label: '2016', data: cur16, backgroundColor: 'rgba(160,157,152,.45)', borderRadius: 4 },
        { label: '2025', data: cur25, backgroundColor: ADM_A, borderRadius: 4 },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: true, position: 'top', labels: { font: { size: 10 }, color: ADM_GR } } },
      scales: {
        x: { grid: { display: false }, ticks: { color: ADM_GR, font: { size: 11 } } },
        y: { ticks: { color: ADM_GR, font: { size: 11 } }, grid: { color: 'rgba(0,0,0,.05)' } },
      },
    },
  });
  chart._slug = 'fte-2016-vs-2025';
  _state.charts.push(chart);
}

function _killChart(slug) {
  const i = _state.charts.findIndex(c => c._slug === slug);
  if (i >= 0) {
    try { _state.charts[i].destroy(); } catch {}
    _state.charts.splice(i, 1);
  }
}

// ── Tabs ────────────────────────────────────────────────────

function _wireTabs(container) {
  const tabs = container.querySelector('[data-role="tier-tabs"]');
  if (!tabs) return;
  const onClick = (e) => {
    const b = e.target.closest('.admin-overview-tab');
    if (!b) return;
    const tier = b.dataset.tier;
    if (!tier || tier === _state.currentTier) return;
    tabs.querySelectorAll('.admin-overview-tab').forEach(t => t.classList.remove('on'));
    b.classList.add('on');
    _state.currentTier = tier;
    _renderTier(container, tier);
  };
  tabs.addEventListener('click', onClick);
  _state.listeners.push({ el: tabs, ev: 'click', fn: onClick });
}
