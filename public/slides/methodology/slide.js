/* methodology — startMethParade animation lives in story.html. */
export function mount(_c) {
  setTimeout(() => { if (typeof window.startMethParade === 'function') { try { window.startMethParade(); } catch {} } }, 200);
}
export function unmount() {
  if (typeof window._methParadeClear === 'function') { try { window._methParadeClear(); } catch {} }
}
