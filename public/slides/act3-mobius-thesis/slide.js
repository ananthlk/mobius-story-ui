/* act3-mobius-thesis */
const SLUG='act3-mobius-thesis';
const _state={data:null};
export async function mount(c){unmount();_state.data=await _load();_render(c);}
export function unmount(){_state.data=null;}
async function _load(){try{const r=await fetch(`/slides/${SLUG}/data/static.json`);if(r.ok)return await r.json();}catch{}return null;}
function _render(c){const a=(_state.data?.narrative_anchors||[]).reduce((m,x)=>(m[x.id]=x,m),{});c.querySelectorAll('[data-anchor]').forEach(el=>{const v=a[el.getAttribute('data-anchor')];if(v)el.textContent=v.value+(v.unit?' '+v.unit:'');});}
