/* ch-finale — hooks into story.html global render fns. */
export function mount(_container) {
  setTimeout(() => {
  if (window.STATE?.factPack && !window.STATE.yearsSeries && typeof window.renderEvoSlide === 'function') {
    try { window.renderEvoSlide(window.STATE.factPack); } catch {}
  }
  if (typeof window.renderFinaleHeatMap === 'function') { try { window.renderFinaleHeatMap(); } catch {} }
  }, 60);
}
export function unmount() {}
