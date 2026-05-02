/* discussion — stagger-in animation for the 4 question cards. */
const _state = { animTimers: [] };
export function mount(container) {
  unmount();
  const cards = container.querySelectorAll('.disc-panel');
  cards.forEach(c => c.classList.remove('in'));
  setTimeout(() => {
    cards.forEach((c, i) => {
      const t = setTimeout(() => c.classList.add('in'), i * 140);
      _state.animTimers.push(t);
    });
  }, 80);
}
export function unmount() { _state.animTimers.forEach(t => clearTimeout(t)); _state.animTimers = []; }
