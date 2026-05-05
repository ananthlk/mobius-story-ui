/* ch2-left-behind — hooks into story.html global render fns. */
export function mount(_container) {
  setTimeout(() => {
  if (typeof window.renderLeftBehindCascade === 'function') { try { window.renderLeftBehindCascade(); } catch {} }
  }, 60);
}
export function unmount() {}
