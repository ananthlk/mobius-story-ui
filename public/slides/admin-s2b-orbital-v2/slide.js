/* admin-s2b-orbital-v2 — orbital + scorecard. Interactive logic still lives
   in story.html globals (rcm8Select, rcm8Play, RCM8_GATES). On mount we
   trigger the same default selection the inline goTo hook used. */

const _state = {};

export function mount(container) {
  setTimeout(() => {
    const tab = container.querySelector('.rcm-ptab[data-p="netsmart"]');
    if (typeof window.rcm8Select === 'function' && tab) {
      try { window.rcm8Select('netsmart', tab); } catch (e) { console.warn('[admin-s2b-orbital-v2] rcm8Select failed', e); }
    }
  }, 60);
}

export function unmount() { /* no-op — global handlers are stateless across slides */ }
