/* admin-s2b-score — flat scorecard. Renders the table via the global
   renderScoreTable() defined in story.html, which reads RCM8_GATES. */

export function mount(_container) {
  setTimeout(() => {
    if (typeof window.renderScoreTable === 'function') {
      try { window.renderScoreTable(); } catch (e) { console.warn('[admin-s2b-score] renderScoreTable failed', e); }
    }
  }, 60);
}
export function unmount() { /* no-op */ }
