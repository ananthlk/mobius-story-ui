/* capabilities — startDemoChat animation lives in story.html. */
export function mount(_c) {
  setTimeout(() => { if (typeof window.startDemoChat === 'function') { try { window.startDemoChat(); } catch {} } }, 300);
}
export function unmount() {
  if (typeof window._demoClear === 'function') { try { window._demoClear(); } catch {} }
}
