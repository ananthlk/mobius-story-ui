/* exec-summary — EXEC_LINES content + animation are global in story.html.
   Trigger the same hook the inline goTo runs. */
export function mount(_container) {
  if (typeof window._resetExecLines === 'function') { try { window._resetExecLines(); } catch {} }
  setTimeout(() => {
    if (typeof window._animateExecLines === 'function') { try { window._animateExecLines(); } catch {} }
  }, 150);
}
export function unmount() {}
