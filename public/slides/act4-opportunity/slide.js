/* act4-opportunity — bar fill animation on entry. */
const _state = { animTimers: [] };
export function mount(container) {
  unmount();
  setTimeout(() => {
    container.querySelectorAll('.bar-fill').forEach(el => {
      const w = el.style.width;
      el.style.width = '0';
      requestAnimationFrame(() => { el.style.transition='width .6s ease'; el.style.width = w; });
    });
  }, 80);
}
export function unmount() { _state.animTimers.forEach(t => clearTimeout(t)); _state.animTimers = []; }
