/* ch-forces — hooks into story.html global render fns. */
export function mount(_container) {
  setTimeout(() => {
  document.querySelectorAll('.force-card').forEach(c => c.classList.remove('visible'));
  setTimeout(() => {
    document.querySelectorAll('.force-card').forEach((c, i) => setTimeout(() => c.classList.add('visible'), i * 130));
  }, 80);
  }, 60);
}
export function unmount() {}
