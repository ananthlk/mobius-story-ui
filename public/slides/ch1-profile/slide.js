/* ch1-profile — radial node baseline. Trigger global layout + LLM hooks. */
export function mount(_container) {
  setTimeout(() => {
    if (typeof window.layoutRadial === 'function') { try { window.layoutRadial(); } catch {} }
    if (typeof window.populateProfileLLM === 'function') { try { window.populateProfileLLM(); } catch {} }
    if (window.STATE?.factPack && typeof window.renderProfile === 'function') {
      try { window.renderProfile(window.STATE.factPack); } catch {}
    }
  }, 60);
}
export function unmount() { /* global STATE persists across slides */ }
