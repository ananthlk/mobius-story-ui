#!/usr/bin/env python3
"""
Build script: insert Act 1 openers/close + Act 2 admin slides into story.html.
Run from /Users/ananth/Mobius/mobius-story-ui/
"""
import re, sys, os

SRC = '/Users/ananth/Mobius/mobius-story-ui/public/story.html'

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

print(f"Loaded {len(html):,} bytes")
assert len(html) > 270000, "File too small — restore from git first"

# ─────────────────────────────────────────────────────────────────────────────
# 1. Add Chart.js CDN before </head>
# ─────────────────────────────────────────────────────────────────────────────
CDN = '<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>'
if CDN not in html:
    html = html.replace('</head>', CDN + '\n</head>', 1)
    print("✓ Chart.js CDN added")
else:
    print("  Chart.js CDN already present")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Add CSS before </style>
# ─────────────────────────────────────────────────────────────────────────────
ADM_CSS = """
/* ═══════════════ ACT OPENERS / CLOSERS ═══════════════ */
.ly-opener{display:flex;flex-direction:column;justify-content:center;align-items:flex-start;
  background:var(--dark);color:#fff;height:100%;padding:3rem 4rem;gap:1.5rem}
.ly-opener .op-eyebrow{font-size:.7rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;
  color:#6B7280}
.ly-opener .op-title{font-size:clamp(1.8rem,3.5vw,2.8rem);font-weight:700;line-height:1.1;
  letter-spacing:-.02em;color:#fff}
.ly-opener .op-qs{display:flex;flex-direction:column;gap:.875rem;margin-top:.75rem}
.ly-opener .op-q{font-size:1rem;color:#D1D5DB;line-height:1.65;padding-left:1.25rem;
  border-left:2px solid #374151}
.ly-opener .op-q strong{color:#fff}
.ly-summary{display:flex;flex-direction:column;justify-content:center;background:var(--dark);
  color:#fff;height:100%;padding:3rem 4rem;gap:1.75rem}
.ly-summary .su-eyebrow{font-size:.7rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;
  color:#6B7280}
.ly-summary .su-title{font-size:clamp(1.6rem,3vw,2.4rem);font-weight:700;line-height:1.1;color:#fff}
.ly-summary .su-truths{display:grid;grid-template-columns:repeat(3,1fr);gap:1.25rem;margin-top:.5rem}
.ly-summary .su-truth{background:#1F2937;border-radius:12px;padding:1.25rem;
  border:1px solid #374151;display:flex;flex-direction:column;gap:.5rem}
.ly-summary .su-truth .st-num{font-size:.65rem;font-weight:700;letter-spacing:.1em;
  text-transform:uppercase;color:#6B7280}
.ly-summary .su-truth .st-head{font-size:.95rem;font-weight:700;color:#F9FAFB;line-height:1.25}
.ly-summary .su-truth .st-body{font-size:.8rem;color:#9CA3AF;line-height:1.6;flex:1}
.ly-summary .su-truth .st-stat{font-size:1.5rem;font-weight:700;color:var(--teal,#1D9E75)}
.ly-summary .su-verdict{background:#111827;border-radius:10px;padding:1rem 1.25rem;
  font-size:.88rem;color:#D1D5DB;line-height:1.7;border-left:3px solid var(--teal,#1D9E75)}
.ly-summary .su-verdict strong{color:#fff}
.ly-act{display:flex;flex-direction:column;justify-content:center;align-items:center;
  background:var(--dark);color:#fff;height:100%;gap:.75rem;text-align:center}
.ly-act .act-eyebrow{font-size:.65rem;font-weight:600;letter-spacing:.15em;text-transform:uppercase;
  color:#4B5563}
.ly-act .act-num{font-size:clamp(3rem,8vw,6rem);font-weight:700;letter-spacing:-.04em;color:#1F2937;
  line-height:1}
.ly-act .act-name{font-size:clamp(1.1rem,2.5vw,1.6rem);font-weight:600;color:#fff;letter-spacing:-.01em}
.ly-act .act-sub{font-size:.85rem;color:#6B7280;max-width:44ch;line-height:1.6;margin-top:.25rem}

/* ═══════════════ ADMIN SLIDES (adm-* namespace) ═══════════════ */
.adm-slide{display:flex;flex-direction:column;height:100%;padding:2rem 2.5rem 1.5rem;
  background:var(--bg,#F7F6F2);color:#1A1917;overflow:hidden}
.adm-slide.dark{background:#111827;color:#fff}
.adm-eyebrow{font-size:.65rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;
  color:#A09D98;margin-bottom:.375rem}
.adm-slide.dark .adm-eyebrow{color:#4B5563}
.adm-title{font-size:clamp(1.4rem,2.5vw,2rem);font-weight:700;line-height:1.15;
  letter-spacing:-.02em;margin-bottom:.375rem}
.adm-slide.dark .adm-title{color:#fff}
.adm-lead{font-size:.85rem;color:#6B6860;line-height:1.65;max-width:72ch;margin-bottom:.875rem}
.adm-slide.dark .adm-lead{color:#9CA3AF}
/* tabs */
.adm-tabs{display:flex;gap:.375rem;flex-wrap:wrap;margin-bottom:.875rem}
.adm-tab{padding:.28rem .75rem;border:1px solid rgba(0,0,0,.12);border-radius:20px;font-size:.75rem;
  font-weight:500;cursor:pointer;background:transparent;color:#6B6860;font-family:inherit;transition:all .14s}
.adm-tab:hover{color:#1A1917;border-color:rgba(0,0,0,.28)}
.adm-tab.on{background:#1A1917;color:#fff;border-color:#1A1917}
.adm-slide.dark .adm-tab{border-color:rgba(255,255,255,.15);color:#9CA3AF}
.adm-slide.dark .adm-tab.on{background:#fff;color:#1A1917}
.tpanel{display:none}.tpanel.on{display:contents}
/* layout */
.adm-row2{display:grid;grid-template-columns:1fr 240px;gap:1.125rem;flex:1;align-items:start;min-height:0}
.adm-cbox{background:#fff;border-radius:10px;padding:1rem 1.125rem;border:1px solid rgba(0,0,0,.07)}
.adm-slide.dark .adm-cbox{background:#1F2937;border-color:rgba(255,255,255,.08)}
.adm-cw{position:relative;width:100%;height:240px}
/* cards */
.adm-cards{display:flex;flex-direction:column;gap:.5rem}
.adm-card{background:#fff;border-radius:8px;padding:.625rem .8rem;border:1px solid rgba(0,0,0,.07)}
.adm-slide.dark .adm-card{background:#1F2937;border-color:rgba(255,255,255,.08)}
.adm-cl{font-size:.62rem;font-weight:600;text-transform:uppercase;letter-spacing:.07em;color:#A09D98;margin-bottom:.1rem}
.adm-cv{font-size:1.2rem;font-weight:700;line-height:1.1}
.adm-cs{font-size:.7rem;color:#6B6860;margin-top:.1rem;line-height:1.4}
.adm-slide.dark .adm-cs{color:#9CA3AF}
.adm-pill{display:inline-block;padding:2px 6px;border-radius:8px;font-size:.62rem;font-weight:600;margin-top:.2rem}
.adm-pr{background:#FCEBEB;color:#501313}
.adm-pg{background:#E1F5EE;color:#04342C}
.adm-pa{background:#FAEEDA;color:#412402}
/* verdict */
.adm-verdict{border-radius:8px;padding:.7rem .9rem;font-size:.78rem;font-weight:500;line-height:1.65;
  margin-top:auto;background:#1A1917;color:#D1D5DB}
.adm-slide.dark .adm-verdict{background:#0F172A;border:1px solid #374151}
.adm-verdict strong{color:#fff}
/* comparison table */
.adm-cmp{display:grid;grid-template-columns:1fr 1fr;gap:.875rem;flex:1;min-height:0}
.adm-col{border-radius:10px;overflow:hidden;border:1px solid rgba(0,0,0,.08)}
.adm-col-head{padding:.5rem .875rem;font-size:.75rem;font-weight:600}
.adm-ch-g{background:#E1F5EE;color:#04342C}
.adm-ch-r{background:#FCEBEB;color:#501313}
.adm-col-body{background:#fff;padding:.5rem .875rem}
.adm-crow{display:flex;justify-content:space-between;align-items:center;
  padding:.325rem 0;border-bottom:1px solid rgba(0,0,0,.06);font-size:.77rem}
.adm-crow:last-child{border-bottom:none}
.adm-crl{color:#6B6860}
.adm-crv{font-weight:600}
.adm-crv-g{color:#0F6E56}.adm-crv-r{color:#A32D2D}.adm-crv-n{color:#1A1917}
/* integer math */
.adm-int-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.75rem;margin-bottom:.875rem}
.adm-ic{border-radius:10px;overflow:hidden;border:1px solid rgba(0,0,0,.08)}
.adm-ic-head{padding:.5rem .75rem;font-size:.73rem;font-weight:600}
.adm-ic-bad{background:#FCEBEB;color:#501313}
.adm-ic-mid{background:#FAEEDA;color:#412402}
.adm-ic-good{background:#E1F5EE;color:#04342C}
.adm-ic-body{background:#fff;padding:.625rem .75rem}
.adm-ic-stat{margin-bottom:.5rem}
.adm-ic-l{font-size:.62rem;font-weight:600;text-transform:uppercase;letter-spacing:.06em;
  color:#A09D98;margin-bottom:.1rem}
.adm-ic-v{font-size:1.2rem;font-weight:700;line-height:1.1}
.adm-ic-s{font-size:.68rem;color:#6B6860;margin-top:.1rem;line-height:1.35}
.adm-ic-note{margin-top:.4rem;padding:.4rem .55rem;border-radius:5px;font-size:.7rem;
  font-weight:500;line-height:1.5}
.adm-in-r{background:#FCEBEB;color:#501313}
.adm-in-a{background:#FAEEDA;color:#412402}
.adm-in-g{background:#E1F5EE;color:#04342C}
/* legend */
.adm-legend{display:flex;gap:.75rem;flex-wrap:wrap;margin-bottom:.5rem}
.adm-li{display:flex;align-items:center;gap:.3rem;font-size:.7rem;color:#6B6860}
.adm-ld{width:9px;height:9px;border-radius:2px;flex-shrink:0}
/* source */
.adm-src{font-size:.6rem;color:#A09D98;margin-top:.625rem;line-height:1.6;font-style:italic}
/* curve slide */
.adm-curve-wrap{display:grid;grid-template-columns:1fr 310px;gap:1.25rem;flex:1;
  align-items:start;min-height:0}
.adm-curve-left{display:flex;flex-direction:column;gap:.625rem;min-height:0}
#admCurveSvg{width:100%;border-radius:8px;background:#faf9f5;border:1px solid rgba(0,0,0,.07)}
.adm-curve-legend{display:flex;flex-wrap:wrap;gap:.3rem .75rem;align-items:center;
  font-size:.68rem;color:#6b6860}
.adm-leg-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;display:inline-block}
.adm-curve-panel{background:#fff;border:1px solid rgba(0,0,0,.08);border-radius:10px;
  min-height:300px;overflow:hidden;display:flex;flex-direction:column}
.adm-cp-idle{flex:1;display:flex;align-items:center;justify-content:center}
.adm-cp-hint{text-align:center;font-size:.78rem;color:#a09d98;line-height:1.7}
.adm-cp-detail{flex:1;display:flex;flex-direction:column;padding:1rem 1rem .625rem;gap:.5rem}
.adm-cp-badge{display:inline-block;font-size:.6rem;font-weight:600;letter-spacing:.1em;
  text-transform:uppercase;padding:.18rem .55rem;border-radius:20px;width:fit-content;
  background:#FAEEDA;color:#412402;border:1px solid #BA7517}
.adm-cp-title{font-size:.9rem;font-weight:600;letter-spacing:-.01em;line-height:1.25}
.adm-cp-sub{font-size:.72rem;color:#6b6860;line-height:1.5}
.adm-cpb-row{display:grid;grid-template-columns:1fr auto auto;gap:.2rem .6rem;
  align-items:center;font-size:.72rem;padding:.3rem .45rem;border-radius:6px;background:#faf9f5;margin-bottom:.2rem}
.adm-cpb-label{color:#1a1917;font-weight:500}
.adm-cpb-val{font-size:.68rem}
.adm-cpb-pill{font-size:.58rem;font-weight:600;padding:.12rem .4rem;border-radius:20px;white-space:nowrap}
.adm-pill-r{background:#FCEBEB;color:#501313;border:1px solid #E24B4A}
.adm-pill-a{background:#FAEEDA;color:#412402;border:1px solid #BA7517}
.adm-pill-g{background:#E1F5EE;color:#04342C;border:1px solid #1D9E75}
.adm-cp-compare{font-size:.7rem;color:#6b6860;line-height:1.55;padding:.45rem .6rem;
  background:#f0ede8;border-radius:7px;border-left:3px solid #BA7517}
"""

# Insert CSS before last </style>
style_close = html.rfind('</style>')
assert style_close != -1
html = html[:style_close] + ADM_CSS + '\n' + html[style_close:]
print("✓ Admin CSS added")

# ─────────────────────────────────────────────────────────────────────────────
# 3. Build new slide HTML blocks
# ─────────────────────────────────────────────────────────────────────────────

NEW_SLIDES = """
      <!-- ── Act 1 Opener ───────────────────────────────────── -->
      <div class="slide" data-id="act1-opener" style="height:100%;overflow:hidden">
        <div class="ly-opener">
          <div class="op-eyebrow">Act I — The Administrative Crisis</div>
          <div class="op-title">Three questions<br>that keep CFOs up at night.</div>
          <div class="op-qs">
            <div class="op-q"><strong>Why do we spend as much on admin as a primary care practice</strong> — but get outcomes three times worse?</div>
            <div class="op-q"><strong>Where exactly does the money go</strong> — and which departments are generating the most drag?</div>
            <div class="op-q"><strong>If we already tried technology, why didn't it work</strong> — and what would it take to actually close the gap?</div>
          </div>
        </div>
      </div>

      <!-- ── Act 1 Close ────────────────────────────────────── -->
      <div class="slide" data-id="act1-close" style="height:100%;overflow:hidden">
        <div class="ly-summary">
          <div class="su-eyebrow">Act I — Verdict</div>
          <div class="su-title">Three forces trap BHPF in the curve.</div>
          <div class="su-truths">
            <div class="su-truth">
              <div class="st-num">Force A</div>
              <div class="st-head">Scale without consolidation</div>
              <div class="st-body">34 independent orgs each running Finance, IT, Billing, HR — 819 FTE where 474 would suffice at $1.1B scale.</div>
              <div class="st-stat">345 excess FTE</div>
            </div>
            <div class="su-truth">
              <div class="st-num">Force B</div>
              <div class="st-head">Platform priced for hospitals</div>
              <div class="st-body">EHR contracts, billing platforms, AI modules — all priced for the $500M–$1.5B sweet spot. BHPF pays proportionally more for systems that do less.</div>
              <div class="st-stat">11.7% vs 9% benchmark</div>
            </div>
            <div class="su-truth">
              <div class="st-num">Force C</div>
              <div class="st-head">Outcomes gap that compounds</div>
              <div class="st-body">44 AR days vs 28. 18% denial rate vs 5.7%. Same billers, different tools — the gap widens every year the platform doesn't change.</div>
              <div class="st-stat">~$12–14M/yr leakage</div>
            </div>
          </div>
          <div class="su-verdict"><strong>The diagnosis is structural, not behavioral.</strong> No CFO can hire their way out of this — the tools have to change first. Act II shows what that change actually looks like.</div>
        </div>
      </div>

      <!-- ── Act 2 Section Break ────────────────────────────── -->
      <div class="slide" data-id="act-infra-break" style="height:100%;overflow:hidden">
        <div class="ly-act">
          <div class="act-eyebrow">BHPF Admin Story</div>
          <div class="act-num">II</div>
          <div class="act-name">The Administrative Infrastructure</div>
          <div class="act-sub">What it costs. What it should cost. What consolidation unlocks.</div>
        </div>
      </div>

      <!-- ── Act 2 Opener ───────────────────────────────────── -->
      <div class="slide" data-id="act2-opener" style="height:100%;overflow:hidden">
        <div class="ly-opener">
          <div class="op-eyebrow">Act II — Administrative Infrastructure</div>
          <div class="op-title">The $43M question<br>hiding in plain sight.</div>
          <div class="op-qs">
            <div class="op-q"><strong>Can we close the benchmark gap</strong> — from 11.7% to 9% admin ratio — without cutting a single clinical role?</div>
            <div class="op-q"><strong>What happens to AI savings when you're fragmented</strong> — and why does consolidation multiply the math by 40×?</div>
            <div class="op-q"><strong>Where does $43M per year come from</strong> — and how much of it is recoverable in the next 24 months?</div>
          </div>
        </div>
      </div>

      <!-- ── Admin S0: Orientation ──────────────────────────── -->
      <div class="slide" data-id="admin-s0" style="height:100%;overflow:hidden">
        <div class="adm-slide">
          <div class="adm-eyebrow">00 — orientation</div>
          <div class="adm-title">Where does the admin dollar go?</div>
          <div class="adm-lead">Across 34 BHPF members, $1.1B in combined revenue supports 819 admin FTE — split across four departments. The breakdown reveals where duplication is concentrated.</div>
          <div class="adm-row2" style="flex:1;min-height:0">
            <div class="adm-cbox" style="height:100%;display:flex;flex-direction:column">
              <div class="adm-legend" id="admLg0"></div>
              <div class="adm-cw" style="flex:1;height:auto"><canvas id="admC0a" role="img" aria-label="Admin FTE breakdown by department"></canvas></div>
            </div>
            <div class="adm-cards">
              <div class="adm-card">
                <div class="adm-cl">Total admin FTE</div>
                <div class="adm-cv">819</div>
                <div class="adm-cs">34 BHPF orgs · Finance, IT, Billing, HR</div>
              </div>
              <div class="adm-card">
                <div class="adm-cl">Admin % of revenue</div>
                <div class="adm-cv">11.7%</div>
                <div class="adm-cs">vs 9% benchmark for $1B+ health systems</div>
                <span class="adm-pill adm-pr">+2.7pp above benchmark</span>
              </div>
              <div class="adm-card">
                <div class="adm-cl">Largest drag</div>
                <div class="adm-cv">Billing/RCM</div>
                <div class="adm-cs">Highest duplication ratio · 18% denial rate vs 5.7% benchmark</div>
                <span class="adm-pill adm-pr">3× benchmark denials</span>
              </div>
              <div class="adm-card">
                <div class="adm-cl">Benchmark at this scale</div>
                <div class="adm-cv">474 FTE</div>
                <div class="adm-cs">APQC median for $1B+ systems · 345 FTE gap</div>
                <span class="adm-pill adm-pg">−$29M/yr scale alone</span>
              </div>
            </div>
          </div>
          <div class="adm-src">BHPF CFO Benchmarking Survey 2025 (n=34) · APQC Open Standards Benchmarking 2024</div>
        </div>
      </div>

      <!-- ── Admin S1: Diagnosis ────────────────────────────── -->
      <div class="slide" data-id="admin-s1" style="height:100%;overflow:hidden">
        <div class="adm-slide">
          <div class="adm-eyebrow">01 — the diagnosis</div>
          <div class="adm-title">Under-invested.<br>Worst outcomes for your scale.</div>
          <div class="adm-lead">A $15M BHPF member and a $15M PCP practice spend the same on admin. But their outcomes are in different universes. Same investment — completely different results.</div>
          <div class="adm-tabs" id="admT1">
            <button class="adm-tab on" data-v="staff">Staffing — looks the same</button>
            <button class="adm-tab" data-v="outcomes">Outcomes — completely different</button>
          </div>
          <div class="adm-row2" style="flex:1;min-height:0">
            <div class="adm-cbox" style="height:100%;display:flex;flex-direction:column">
              <div class="adm-legend" id="admLg1"></div>
              <div class="adm-cw" style="flex:1;height:auto"><canvas id="admC1" role="img" aria-label="Staffing and outcomes comparison"></canvas></div>
            </div>
            <div class="adm-cards" id="admKp1"></div>
          </div>
          <div class="adm-verdict" id="admVd1"></div>
          <div class="adm-src">BHPF CFO Benchmarking Survey 2025 (n=34) · MGMA DataDive Cost &amp; Revenue 2024 · athenahealth network data Mar 2024 · ADS/SimiTree BH denial benchmark 2026</div>
        </div>
      </div>

      <!-- ── Admin S1c: U-Curve ─────────────────────────────── -->
      <div class="slide" data-id="admin-s1c" style="height:100%;overflow:hidden">
        <div class="adm-slide">
          <div class="adm-eyebrow">01c — the curve</div>
          <div class="adm-title">Healthcare pricing is calibrated<br>for the $500M–$1.5B sweet spot.</div>
          <div class="adm-lead">EHR contracts, billing platforms, AI modules — every vendor prices for hospital scale. Below $100M you pay proportionally more per revenue dollar for a product built for someone ten times your size.</div>
          <div class="adm-curve-wrap" style="flex:1;min-height:0">
            <div class="adm-curve-left">
              <svg id="admCurveSvg" viewBox="0 0 640 330" xmlns="http://www.w3.org/2000/svg" style="max-height:300px"></svg>
              <div class="adm-curve-legend">
                <span class="adm-leg-dot" style="background:#BA7517"></span><span>BHPF tiers (CFO Survey 2025)</span>
                <span class="adm-leg-dot" style="background:#1D9E75"></span><span>PCP benchmark (MGMA 2024)</span>
                <span class="adm-leg-dot" style="background:#888"></span><span>Hospital A&amp;G (Handlon 2025)</span>
              </div>
            </div>
            <div class="adm-curve-panel" id="admCurvePanelEl">
              <div class="adm-cp-idle" id="admCpIdleEl">
                <div class="adm-cp-hint">← Click any BHPF dot<br>to see the breakdown</div>
              </div>
              <div class="adm-cp-detail" id="admCpDetailEl" style="display:none">
                <div class="adm-cp-badge" id="admCpBadgeEl"></div>
                <div class="adm-cp-title" id="admCpTitleEl"></div>
                <div class="adm-cp-sub" id="admCpSubEl"></div>
                <div id="admCpBucketsEl"></div>
                <div class="adm-cp-compare" id="admCpCompareEl"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ── Admin S2: Tool Gap ─────────────────────────────── -->
      <div class="slide" data-id="admin-s2" style="height:100%;overflow:hidden">
        <div class="adm-slide">
          <div class="adm-eyebrow">02 — the tool gap</div>
          <div class="adm-title">The gap isn't effort.<br>It's the platform.</div>
          <div class="adm-lead">Vendor contracts are structured for hospital scale. BHPF members pay enterprise prices for tools that deliver sub-enterprise outcomes — and there's no shared intelligence to close the gap.</div>
          <div class="adm-cmp" style="flex:1;min-height:0">
            <div class="adm-col">
              <div class="adm-col-head adm-ch-r">What BHPF members have today</div>
              <div class="adm-col-body">
                <div class="adm-crow"><span class="adm-crl">EHR / PM system</span><span class="adm-crv adm-crv-r">Fragmented — 8+ platforms across 34 orgs</span></div>
                <div class="adm-crow"><span class="adm-crl">Billing platform</span><span class="adm-crv adm-crv-r">Stand-alone per org · no shared payer intel</span></div>
                <div class="adm-crow"><span class="adm-crl">AR days</span><span class="adm-crv adm-crv-r">44 days avg · cash trapped $4–6M</span></div>
                <div class="adm-crow"><span class="adm-crl">Denial rate</span><span class="adm-crv adm-crv-r">16–20% · 3× industry benchmark</span></div>
                <div class="adm-crow"><span class="adm-crl">Calls / FTE / day</span><span class="adm-crv adm-crv-r">30 · vs 80 on modern platform</span></div>
                <div class="adm-crow"><span class="adm-crl">Clean claim rate</span><span class="adm-crv adm-crv-r">75% · 23pp below benchmark</span></div>
                <div class="adm-crow"><span class="adm-crl">AI modules available</span><span class="adm-crv adm-crv-r">Minimal · no shared training data</span></div>
                <div class="adm-crow"><span class="adm-crl">Vendor contract leverage</span><span class="adm-crv adm-crv-r">None · priced as 34 small orgs</span></div>
              </div>
            </div>
            <div class="adm-col">
              <div class="adm-col-head adm-ch-g">What shared infrastructure delivers</div>
              <div class="adm-col-body">
                <div class="adm-crow"><span class="adm-crl">EHR / PM system</span><span class="adm-crv adm-crv-g">Single platform · shared config &amp; training</span></div>
                <div class="adm-crow"><span class="adm-crl">Billing platform</span><span class="adm-crv adm-crv-g">Collective payer intelligence · network learns</span></div>
                <div class="adm-crow"><span class="adm-crl">AR days</span><span class="adm-crv adm-crv-g">28 days target · $4–6M working cap freed</span></div>
                <div class="adm-crow"><span class="adm-crl">Denial rate</span><span class="adm-crv adm-crv-g">6% · at athena network benchmark</span></div>
                <div class="adm-crow"><span class="adm-crl">Calls / FTE / day</span><span class="adm-crv adm-crv-g">80 · 2.7× productivity improvement</span></div>
                <div class="adm-crow"><span class="adm-crl">Clean claim rate</span><span class="adm-crv adm-crv-g">98% · top-decile performance</span></div>
                <div class="adm-crow"><span class="adm-crl">AI modules available</span><span class="adm-crv adm-crv-g">Full suite · trained on $1.1B claim history</span></div>
                <div class="adm-crow"><span class="adm-crl">Vendor contract leverage</span><span class="adm-crv adm-crv-g">$1.1B negotiating position · 30–40% savings</span></div>
              </div>
            </div>
          </div>
          <div class="adm-verdict">The platform gap is a <strong>structural moat</strong> — not a skills gap, not a hiring problem. Closing it requires moving to shared infrastructure at sufficient scale to access enterprise-tier pricing.</div>
          <div class="adm-src">BHPF CFO Benchmarking Survey 2025 · athenahealth network data Mar 2024 · Dialog Health call centre benchmark 2024 · ADS/SimiTree BH denial benchmark 2026</div>
        </div>
      </div>

      <!-- ── Admin S3: AI Trap ──────────────────────────────── -->
      <div class="slide" data-id="admin-s3" style="height:100%;overflow:hidden">
        <div class="adm-slide">
          <div class="adm-eyebrow">03 — the AI trap</div>
          <div class="adm-title">AI alone fails.<br>Scale makes it work.</div>
          <div class="adm-lead">Apply 35% AI productivity to a fragmented org and you get ~2.3 extractable FTE. Apply the same AI to a consolidated $1.1B entity and you unlock 167 FTE. Same percentage — 40× the impact.</div>
          <div class="adm-int-grid">
            <div class="adm-ic">
              <div class="adm-ic-head adm-ic-bad">BHPF &lt;$15M tier · n=13</div>
              <div class="adm-ic-body">
                <div class="adm-ic-stat"><div class="adm-ic-l">Admin FTE (avg)</div><div class="adm-ic-v">~20 FTE</div><div class="adm-ic-s">Finance 5 · IT 6 · Billing 6.5 · HR 3</div></div>
                <div class="adm-ic-stat"><div class="adm-ic-l">35% AI applied</div><div class="adm-ic-v">~7 FTE saved</div><div class="adm-ic-s">Only 2.3 extractable — rest absorbed by complexity</div></div>
                <div class="adm-ic-note adm-in-r">~$200K/yr · stranded across 13 orgs · not a business case</div>
              </div>
            </div>
            <div class="adm-ic">
              <div class="adm-ic-head adm-ic-mid">BHPF $15–30M tier · n=8</div>
              <div class="adm-ic-body">
                <div class="adm-ic-stat"><div class="adm-ic-l">Admin FTE (avg)</div><div class="adm-ic-v">~28 FTE</div><div class="adm-ic-s">Finance 7 · IT 8 · Billing 9 · HR 4</div></div>
                <div class="adm-ic-stat"><div class="adm-ic-l">35% AI applied</div><div class="adm-ic-v">~10 FTE saved</div><div class="adm-ic-s">Only 3–4 extractable — highest ratio but smallest base</div></div>
                <div class="adm-ic-note adm-in-a">~$300K/yr · still not sufficient to fund transformation</div>
              </div>
            </div>
            <div class="adm-ic">
              <div class="adm-ic-head adm-ic-good">Consolidated $1.1B entity</div>
              <div class="adm-ic-body">
                <div class="adm-ic-stat"><div class="adm-ic-l">APQC benchmark FTE</div><div class="adm-ic-v">474 FTE</div><div class="adm-ic-s">Finance 116 · IT 132 · Billing 116 · HR 110</div></div>
                <div class="adm-ic-stat"><div class="adm-ic-l">35% AI applied</div><div class="adm-ic-v">167 FTE saved</div><div class="adm-ic-s">All restructurable — critical mass for redeployment</div></div>
                <div class="adm-ic-note adm-in-g">~$14M/yr · plus $29M fragmentation savings = $43M total</div>
              </div>
            </div>
          </div>
          <div class="adm-verdict"><strong>The math is multiplicative, not additive.</strong> AI on a fragmented base produces rounding errors. AI on a consolidated base produces a business case. The sequence matters: consolidate first, then automate.</div>
          <div class="adm-src">BHPF CFO Benchmarking Survey 2025 · APQC Open Standards Benchmarking 2024 · McKinsey Global Institute AI productivity benchmarks 2024</div>
        </div>
      </div>

      <!-- ── Admin S4: Scale Unlock (dark) ─────────────────── -->
      <div class="slide" data-id="admin-s4" style="height:100%;overflow:hidden">
        <div class="adm-slide dark">
          <div class="adm-eyebrow">04 — scale unlock</div>
          <div class="adm-title" style="color:#fff">The fragmentation tax.<br>345 FTE that exist only because of duplication.</div>
          <div class="adm-lead">At $1.1B combined revenue, APQC benchmarks for $1B+ health systems apply. Run the math: 819 current FTE vs 474 benchmark = 345 excess FTE = ~$29M/yr — before AI, before renegotiated contracts.</div>
          <div class="adm-tabs" id="admT4">
            <button class="adm-tab on" data-v="frag">Fragmentation tax — headcount</button>
            <button class="adm-tab" data-v="outcomes">Outcomes at scale</button>
          </div>
          <div class="adm-row2" style="flex:1;min-height:0">
            <div class="adm-cbox" style="height:100%;display:flex;flex-direction:column">
              <div class="adm-legend" id="admLg4"></div>
              <div class="adm-cw" style="flex:1;height:auto"><canvas id="admC4" role="img" aria-label="Scale unlock chart"></canvas></div>
            </div>
            <div class="adm-cards" id="admKp4"></div>
          </div>
          <div class="adm-verdict" id="admVd4">345 FTE exist because 34 organisations each run their own supervisors, credentialing pipelines, and denial playbooks. Consolidation eliminates this without touching a single clinical role.</div>
          <div class="adm-src">BHPF CFO Benchmarking Survey 2025 (n=34) · APQC Open Standards Benchmarking 2024 · $85K loaded FTE cost assumption</div>
        </div>
      </div>

      <!-- ── Admin S5: Payoff ───────────────────────────────── -->
      <div class="slide" data-id="admin-s5" style="height:100%;overflow:hidden">
        <div class="adm-slide">
          <div class="adm-eyebrow">05 — the payoff</div>
          <div class="adm-title">$43M/yr.<br>The math of consolidation.</div>
          <div class="adm-lead">Fragmentation savings ($29M) + AI on consolidated base ($14M) = $43M/yr. But the bigger prize is outcome recovery: bringing denial rate from 18% to 6% on $1.1B revenue adds $8–12M in collections.</div>
          <div class="adm-tabs" id="admT5">
            <button class="adm-tab on" data-v="calc">The calculation</button>
            <button class="adm-tab" data-v="outcomes">Outcome recovery</button>
          </div>
          <div id="admS5body" style="flex:1;min-height:0;overflow:auto"></div>
          <div class="adm-src">BHPF CFO Benchmarking Survey 2025 · APQC 2024 · athenahealth network data 2024</div>
        </div>
      </div>

      <!-- ── Act 2 Master Close ─────────────────────────────── -->
      <div class="slide" data-id="act2-master" style="height:100%;overflow:hidden">
        <div class="ly-summary">
          <div class="su-eyebrow">Act II — Verdict</div>
          <div class="su-title">The $43M is real. The sequence is everything.</div>
          <div class="su-truths">
            <div class="su-truth">
              <div class="st-num">Truth 1</div>
              <div class="st-head">Consolidation is the precondition</div>
              <div class="st-body">AI on fragmented orgs produces ~$200K per org. AI on a consolidated $1.1B entity produces $14M. Scale must come first.</div>
              <div class="st-stat">40× multiplier</div>
            </div>
            <div class="su-truth">
              <div class="st-num">Truth 2</div>
              <div class="st-head">The headcount math is conservative</div>
              <div class="st-body">$29M in fragmentation savings + $14M AI savings = $43M/yr. No heroics required — this is pure duplication elimination at benchmark rates.</div>
              <div class="st-stat">$43M/yr</div>
            </div>
            <div class="su-truth">
              <div class="st-num">Truth 3</div>
              <div class="st-head">Revenue recovery dwarfs cost savings</div>
              <div class="st-body">Reducing denial rate from 18% to 6% on $1.1B revenue recovers $8–12M in collections. At 3.4% net margin, this doubles the bottom line.</div>
              <div class="st-stat">+$8–12M/yr</div>
            </div>
          </div>
          <div class="su-verdict"><strong>The real prize isn't the headcount savings.</strong> Recovering 3pp of denial leakage on $1.1B revenue adds ~$33M to collections. The admin savings fund the transformation. The outcome recovery is the mission.</div>
        </div>
      </div>
"""

# Find insertion point: after the ch2-left-behind slide's closing </div>
# The slide closes at line 1141: "      </div>\n\n      <!-- ── Appendix"
MARKER = '\n\n      <!-- ── Appendix slides: 2019–2024 static snapshots ──────── -->'
pos = html.find(MARKER)
assert pos != -1, f"Insertion marker not found"
html = html[:pos] + NEW_SLIDES + html[pos:]
print("✓ New slides inserted")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Update SLIDES array — insert after ch2-left-behind entry
# ─────────────────────────────────────────────────────────────────────────────
OLD_SLIDES_ENTRY = "  {id: 'ch2-left-behind',   title: 'Chapter 1 — The verdict · Left behind'},\n  {id: 'app-2019',"
NEW_SLIDES_ENTRIES = """  {id: 'ch2-left-behind',   title: 'Chapter 1 — The verdict · Left behind'},
  {id: 'act1-opener',       title: 'Act I — Opener · Three questions'},
  {id: 'act1-close',        title: 'Act I — Verdict · Three forces'},
  {id: 'act-infra-break',   title: 'Act II — Administrative Infrastructure'},
  {id: 'act2-opener',       title: 'Act II — Opener · The $43M question'},
  {id: 'admin-s0',          title: 'Admin — Orientation · Where the dollar goes'},
  {id: 'admin-s1',          title: 'Admin — Diagnosis · Under-invested'},
  {id: 'admin-s1c',         title: 'Admin — The U-Curve · Pricing trap'},
  {id: 'admin-s2',          title: 'Admin — Tool Gap · Platform failure'},
  {id: 'admin-s3',          title: 'Admin — AI Trap · Scale makes it work'},
  {id: 'admin-s4',          title: 'Admin — Scale Unlock · Fragmentation tax'},
  {id: 'admin-s5',          title: 'Admin — The Payoff · $43M math'},
  {id: 'act2-master',       title: 'Act II — Verdict · $43M is real'},
  {id: 'app-2019',"""

html = html.replace(OLD_SLIDES_ENTRY, NEW_SLIDES_ENTRIES, 1)
assert "'act1-opener'" in html
print("✓ SLIDES array updated")

# Verify count
slide_count = html.count("{id: '")
print(f"  SLIDES entries: {slide_count}")

# ─────────────────────────────────────────────────────────────────────────────
# 5. Rebuild nav dots
# ─────────────────────────────────────────────────────────────────────────────
# SLIDES order (0-indexed), now 44 total:
DOTS_INFO = [
    ('cover',           'Cover',                        False),
    ('exec-summary',    'Executive Summary',             False),
    ('methodology',     'How to read this',              False),
    ('capabilities',    'Platform capabilities',         False),
    ('act1-break',      'Act I — The evidence',          True),
    ('ch1-backbone',    'The backbone',                  False),
    ('ch1-profile',     'Pre-COVID baseline',            False),
    ('ch-forces',       'Four forces',                   False),
    ('ch2-evolution',   'Market evolution',              False),
    ('ch-finale',       'Winners &amp; Losers',          False),
    ('ch2-left-behind', 'Left behind',                   False),
    ('act1-opener',     'Act I — Questions',             True),
    ('act1-close',      'Act I — Verdict',               False),
    ('act-infra-break', 'Act II — Admin Infrastructure', True),
    ('act2-opener',     'Act II — Questions',            True),
    ('admin-s0',        'Admin — Orientation',           False),
    ('admin-s1',        'Admin — Diagnosis',             False),
    ('admin-s1c',       'Admin — U-Curve',               False),
    ('admin-s2',        'Admin — Tool Gap',              False),
    ('admin-s3',        'Admin — AI Trap',               False),
    ('admin-s4',        'Admin — Scale Unlock',          False),
    ('admin-s5',        'Admin — Payoff',                False),
    ('act2-master',     'Act II — Verdict',              False),
    ('app-2019',        'Appendix — 2019',               False),
    ('app-2020',        'Appendix — 2020',               False),
    ('app-2021',        'Appendix — 2021',               False),
    ('app-2022',        'Appendix — 2022',               False),
    ('app-2023',        'Appendix — 2023',               False),
    ('app-2024',        'Appendix — 2024',               False),
    ('ch1b-what-changed','What changed',                 False),
    ('ch2-juxtaposition','Juxtaposition',                False),
    ('ch2-implication', 'What it costs',                 False),
    ('ch3-four-problems','Four problems',                False),
    ('ch4-tech-failed', 'Tech didn\'t fix it',           False),
    ('ch5-money',       'Where the money goes',          False),
    ('act2-break',      'Act II — The choice',           True),
    ('ch6-three-futures','Three futures',                False),
    ('act3-break',      'Act III — Path forward',        True),
    ('ch7a-individual', 'Individualized plan',           False),
    ('ch7b-shared',     'Shared services',               False),
    ('ch7c-ai',         'AI roadmap',                    False),
    ('act4-break',      'Act IV — Structure',            True),
    ('ch8-structure',   'Three-entity model',            False),
    ('ch9-scaling',     'The scaling act',               False),
]

btn_lines = []
for i, (sid, title, is_break) in enumerate(DOTS_INFO):
    active = ' active' if i == 0 else ''
    if is_break:
        btn_lines.append(f'      <button class="pdot{active} act-break-dot" onclick="goTo({i})" title="{title}" style="background:rgba(255,255,255,.08)"></button>')
    else:
        btn_lines.append(f'      <button class="pdot{active}" onclick="goTo({i})" title="{title}"></button>')

new_dots_block = '\n'.join(btn_lines)

# Find and replace the progress-dots div content
DOTS_START = '    <div class="progress-dots" id="progress-dots">\n'
DOTS_END   = '\n    </div>\n    <div class="bb-hint">↗ drill-in</div>'

ds = html.find(DOTS_START)
assert ds != -1, "progress-dots start not found"
de = html.find(DOTS_END, ds)
assert de != -1, "progress-dots end not found"

# Replace content between start and end markers
html = html[:ds] + DOTS_START + new_dots_block + html[de:]
print(f"✓ Nav dots rebuilt ({len(DOTS_INFO)} slides)")

# ─────────────────────────────────────────────────────────────────────────────
# 6. Add admin JS before </script> (last one)
# ─────────────────────────────────────────────────────────────────────────────
ADMIN_JS = """
// ═══════════════════════════════════════════════════════════
// ADMIN SLIDES JS (namespaced adm*)
// ═══════════════════════════════════════════════════════════
(function(){
const ADM_A='#BA7517',ADM_G='#1D9E75',ADM_R='#E24B4A',ADM_GR='#A09D98';
let admCharts={};
const admKill=id=>{try{admCharts[id]&&admCharts[id].destroy()}catch(e){}};

function admMkLegend(id,items){
  const el=document.getElementById(id);if(!el)return;
  el.innerHTML=items.map(i=>`<div class="adm-li"><div class="adm-ld" style="background:${i.c}"></div>${i.l}</div>`).join('');
}
function admMkCards(id,cards){
  const el=document.getElementById(id);if(!el)return;
  el.innerHTML=cards.map((c,i)=>`
    <div class="adm-card">
      <div class="adm-cl">${c.l}</div>
      <div class="adm-cv" style="${c.cs||''}">${c.v}</div>
      <div class="adm-cs">${c.s}</div>
      ${c.pill?`<span class="adm-pill ${c.pc}">${c.pill}</span>`:''}
    </div>`).join('');
}

// S0 chart
const ADM_S0={
  labels:['Finance','IT','Billing/RCM','HR'],
  ds:[{label:'Current BHPF (819 total FTE)',data:[211,216,216,176],bg:ADM_A},
      {label:'APQC benchmark at $1.1B',data:[116,132,116,110],bg:ADM_G}],
  ymax:260,yl:'FTE count'
};
function buildAdmC0(){
  admKill('admC0a');
  admMkLegend('admLg0',ADM_S0.ds.map(ds=>({c:ds.bg,l:ds.label})));
  admCharts['admC0a']=new Chart(document.getElementById('admC0a'),{
    type:'bar',
    data:{labels:ADM_S0.labels,datasets:ADM_S0.ds.map(ds=>({label:ds.label,data:ds.data,
      backgroundColor:ds.bg,borderRadius:4}))},
    options:{responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false}},
      scales:{x:{grid:{display:false},ticks:{color:ADM_GR,font:{size:11}}},
        y:{title:{display:true,text:ADM_S0.yl,color:ADM_GR,font:{size:11}},
          ticks:{color:ADM_GR,font:{size:11}},grid:{color:'rgba(0,0,0,.05)'},max:ADM_S0.ymax}}}
  });
}

// S1
const ADM_S1={
  staff:{
    labels:['Finance','IT','Billing/RCM','HR'],
    ds:[{label:'BHPF $15–30M tier',data:[2.0,2.4,2.7,1.0],bg:ADM_A},
        {label:'PCP practice $15–20M (MGMA 2024)',data:[2.2,1.8,2.5,1.1],bg:ADM_G}],
    ymax:4,yl:'% of total staff',
    cards:[{l:'BHPF billing staff',v:'2.7%',s:'of total staff',pill:'near PCP benchmark',pc:'adm-pg'},
           {l:'PCP billing staff',v:'2.5%',s:'MGMA 2024 · $15–20M practices',pill:'',pc:''},
           {l:'Admin investment',v:'Similar',s:'Both orgs look identical on staffing benchmarks',pill:'not the problem',pc:'adm-pg'}],
    verdict:'Staffing benchmarks out. The investment is comparable. So why are the outcomes so different?'
  },
  outcomes:{
    labels:['AR days','Calls/FTE/day','Denial rate %','Patients/biller÷100'],
    ds:[{label:'BHPF',data:[44,30,18,9],bg:ADM_R},
        {label:'Industry benchmark',data:[28,80,5.7,28],bg:ADM_G}],
    ymax:90,yl:'value (mixed)',
    cards:[{l:'AR days',v:'44 days',s:'vs 26–34 · cash trapped 10+ extra days',pill:'−$4–6M working cap',pc:'adm-pr'},
           {l:'Denial rate',v:'16–20%',s:'vs 5.7% on athena · 3× the write-offs',pill:'3× benchmark',pc:'adm-pr'},
           {l:'Root cause',v:'The tools',s:'Same billers, different platform, completely different output',pill:'tech failure',pc:'adm-pr'}],
    verdict:'Same investment. Completely different outcomes. The only explanation is the tool — not the people, not the effort, not the leadership.'
  }
};
function buildAdmC1(v){
  admKill('admC1');
  const d=ADM_S1[v];
  admMkLegend('admLg1',d.ds.map(ds=>({c:ds.bg,l:ds.label})));
  admCharts['admC1']=new Chart(document.getElementById('admC1'),{
    type:'bar',
    data:{labels:d.labels,datasets:d.ds.map(ds=>({label:ds.label,data:ds.data,
      backgroundColor:ds.bg,borderRadius:4}))},
    options:{responsive:true,maintainAspectRatio:false,animation:{duration:500},
      plugins:{legend:{display:false}},
      scales:{x:{grid:{display:false},ticks:{color:ADM_GR,font:{size:11}}},
        y:{title:{display:true,text:d.yl,color:ADM_GR,font:{size:11}},
          ticks:{color:ADM_GR,font:{size:11}},grid:{color:'rgba(0,0,0,.05)'},max:d.ymax}}}
  });
  admMkCards('admKp1',d.cards);
  document.getElementById('admVd1').textContent=d.verdict;
}

// S4
const ADM_S4={
  frag:{
    labels:['Finance','IT','Billing','HR'],
    ds:[{label:'APQC benchmark at $1.1B',data:[116,132,116,110],bg:ADM_G},
        {label:'Fragmentation tax (duplication)',data:[95,84,100,66],bg:ADM_A}],
    ymax:260,yl:'Back-office FTE',
    legend:[{c:ADM_G,l:'Benchmark at $1.1B (APQC)'},{c:ADM_A,l:'Fragmentation tax — duplication'}],
    cards:[{l:'Current total FTE',v:'819',s:'34 orgs · Finance, IT, Billing, HR',pill:'',pc:''},
           {l:'At $1.1B benchmark',v:'474 FTE',s:'APQC median — all four functions',pill:'−345 excess',pc:'adm-pa'},
           {l:'Scale saving',v:'~$29M/yr',s:'No AI required · pure duplication eliminated',pill:'before AI',pc:'adm-pg'}],
    verdict:'345 FTE exist because 34 organisations each run their own supervisors, credentialing pipelines, and denial playbooks.'
  },
  outcomes:{
    labels:['AR days','Denial rate %','Calls/FTE/day','Clean claim %'],
    ds:[{label:'BHPF today',data:[44,18,30,75],bg:ADM_R},
        {label:'With shared platform',data:[28,6,80,98],bg:ADM_G}],
    ymax:110,yl:'value',
    legend:[{c:ADM_R,l:'BHPF today'},{c:ADM_G,l:'With shared platform at scale'}],
    cards:[{l:'AR days',v:'44 → 28',s:'$4–6M working capital recovered',pill:'immediate',pc:'adm-pg'},
           {l:'Denial rate',v:'18% → 6%',s:'Shared payer intelligence · network learns',pill:'−$8M/yr est.',pc:'adm-pg'},
           {l:'Net margin',v:'+3–5pp',s:'At 3.4% margin today — this doubles the bottom line',pill:'the real prize',pc:'adm-pg'}],
    verdict:'The outcome improvement from the right platform at scale is worth more than the headcount savings.'
  }
};
function buildAdmC4(v){
  admKill('admC4');
  const d=ADM_S4[v];
  admMkLegend('admLg4',d.legend);
  admCharts['admC4']=new Chart(document.getElementById('admC4'),{
    type:'bar',
    data:{labels:d.labels,datasets:d.ds.map(ds=>({label:ds.label,data:ds.data,
      backgroundColor:ds.bg,borderRadius:v==='frag'?{topLeft:4,topRight:4,bottomLeft:0,bottomRight:0}:4}))},
    options:{responsive:true,maintainAspectRatio:false,animation:{duration:500},
      plugins:{legend:{display:false}},
      scales:{x:{stacked:v==='frag',grid:{display:false},ticks:{color:'#9CA3AF',font:{size:11}}},
        y:{stacked:v==='frag',
          title:{display:true,text:d.yl,color:'#6B7280',font:{size:11}},
          ticks:{color:'#9CA3AF',font:{size:11}},grid:{color:'rgba(255,255,255,.06)'},max:d.ymax}}}
  });
  admMkCards('admKp4',d.cards);
  document.getElementById('admVd4').textContent=d.verdict;
}

// S5
function buildAdmS5calc(){
  const el=document.getElementById('admS5body');if(!el)return;
  el.innerHTML=`<div style="display:grid;grid-template-columns:1fr 1fr;gap:.875rem;margin-bottom:.75rem">
    <div style="background:#FCEBEB;border-radius:10px;padding:1rem;border:1px solid #F09595">
      <div style="font-size:.75rem;font-weight:600;color:#501313;margin-bottom:.625rem">Individual org — AI alone today</div>
      <div style="font-size:.78rem;color:#6B6860;display:flex;flex-direction:column;gap:.35rem">
        <div style="display:flex;justify-content:space-between;padding:.25rem 0;border-bottom:1px solid rgba(0,0,0,.06)"><span style="font-weight:600;color:#1A1917">Finance</span><span>5 FTE → <b style="color:#1D9E75">1.8 saved</b> → <b style="color:#E24B4A">0.5 extractable</b></span></div>
        <div style="display:flex;justify-content:space-between;padding:.25rem 0;border-bottom:1px solid rgba(0,0,0,.06)"><span style="font-weight:600;color:#1A1917">IT</span><span>6 FTE → <b style="color:#1D9E75">2.1 saved</b> → <b style="color:#E24B4A">0.5 extractable</b></span></div>
        <div style="display:flex;justify-content:space-between;padding:.25rem 0;border-bottom:1px solid rgba(0,0,0,.06)"><span style="font-weight:600;color:#1A1917">Billing</span><span>6.5 FTE → <b style="color:#1D9E75">2.3 saved</b> → <b style="color:#E24B4A">1.0 extractable</b></span></div>
        <div style="display:flex;justify-content:space-between;padding:.25rem 0"><span style="font-weight:600;color:#1A1917">HR</span><span>3 FTE → <b style="color:#1D9E75">1.1 saved</b> → <b style="color:#E24B4A">0.3 extractable</b></span></div>
      </div>
      <div style="margin-top:.625rem;background:rgba(226,75,74,.12);border-radius:5px;padding:.4rem .55rem;font-size:.72rem;font-weight:600;color:#501313">
        Total extractable: ~2.3 FTE ≈ ~$200K/yr<br><span style="font-weight:400">Multiply by 34: still stranded everywhere</span>
      </div>
    </div>
    <div style="background:#E1F5EE;border-radius:10px;padding:1rem;border:1px solid #5DCAA5">
      <div style="font-size:.75rem;font-weight:600;color:#04342C;margin-bottom:.625rem">Consolidated $1.1B — same 35% AI</div>
      <div style="font-size:.78rem;color:#6B6860;display:flex;flex-direction:column;gap:.35rem">
        <div style="display:flex;justify-content:space-between;padding:.25rem 0;border-bottom:1px solid rgba(0,0,0,.06)"><span style="font-weight:600;color:#1A1917">Finance</span><span>116 FTE → <b style="color:#1D9E75">−41 FTE</b> → <b style="color:#085041">~$3.5M</b></span></div>
        <div style="display:flex;justify-content:space-between;padding:.25rem 0;border-bottom:1px solid rgba(0,0,0,.06)"><span style="font-weight:600;color:#1A1917">IT</span><span>132 FTE → <b style="color:#1D9E75">−46 FTE</b> → <b style="color:#085041">~$3.9M</b></span></div>
        <div style="display:flex;justify-content:space-between;padding:.25rem 0;border-bottom:1px solid rgba(0,0,0,.06)"><span style="font-weight:600;color:#1A1917">Billing</span><span>116 FTE → <b style="color:#1D9E75">−41 FTE</b> → <b style="color:#085041">~$3.5M</b></span></div>
        <div style="display:flex;justify-content:space-between;padding:.25rem 0"><span style="font-weight:600;color:#1A1917">HR</span><span>110 FTE → <b style="color:#1D9E75">−39 FTE</b> → <b style="color:#085041">~$3.3M</b></span></div>
      </div>
      <div style="margin-top:.625rem;background:rgba(29,158,117,.15);border-radius:5px;padding:.4rem .55rem;font-size:.72rem;font-weight:600;color:#04342C">
        Total: 167 FTE ≈ ~$14M/yr — fully extractable<br><span style="font-weight:400">100 billers × 35% = 35 real restructurable roles</span>
      </div>
    </div>
  </div>
  <div style="background:#111827;border-radius:8px;padding:.875rem 1.125rem;font-size:.82rem;color:#D1D5DB;line-height:1.65;border-left:3px solid #1D9E75">
    <strong style="color:#fff">Fragmentation savings ($29M) + AI on consolidated base ($14M) = $43M/yr.</strong> The math only works because consolidation creates the critical mass that makes AI extractable.
  </div>`;
}
function buildAdmS5outcomes(){
  const el=document.getElementById('admS5body');if(!el)return;
  el.innerHTML=`<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.875rem;margin-bottom:.875rem">
    <div style="background:#fff;border-radius:9px;padding:.875rem;border:1px solid rgba(0,0,0,.08)">
      <div style="font-size:.62rem;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:#A09D98;margin-bottom:.3rem">Admin cost</div>
      <div style="font-size:1.4rem;font-weight:700;color:#1D9E75">11.7% → ~9%</div>
      <div style="font-size:.72rem;color:#6B6860;margin-top:.2rem;line-height:1.4">Scale alone moves you from fragmented position to sweet spot on the curve</div>
    </div>
    <div style="background:#fff;border-radius:9px;padding:.875rem;border:1px solid rgba(0,0,0,.08)">
      <div style="font-size:.62rem;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:#A09D98;margin-bottom:.3rem">With AI on top</div>
      <div style="font-size:1.4rem;font-weight:700;color:#1D9E75">~9% → ~7.5%</div>
      <div style="font-size:.72rem;color:#6B6860;margin-top:.2rem;line-height:1.4">AI on 474 FTE · 166 extractable · comparable to leading health systems</div>
    </div>
    <div style="background:#E1F5EE;border-radius:9px;padding:.875rem;border:1px solid #5DCAA5">
      <div style="font-size:.62rem;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:#04342C;margin-bottom:.3rem">Revenue recovery</div>
      <div style="font-size:1.4rem;font-weight:700;color:#1D9E75">+$8–12M/yr</div>
      <div style="font-size:.72rem;color:#085041;margin-top:.2rem;line-height:1.4">Denial rate 18% → 6% · at $1.1B revenue · worth more than all headcount savings combined</div>
    </div>
  </div>
  <div style="background:#E1F5EE;border-radius:9px;padding:.875rem 1.125rem;border:1px solid #5DCAA5;font-size:.82rem;font-weight:500;color:#04342C;line-height:1.65">
    <strong>The real prize isn't the headcount savings.</strong> At 3.4% net margin, recovering 3pp of denial leakage on $1.1B revenue adds ~$33M to collections. The admin savings fund the transformation. The outcome recovery is the mission.
  </div>`;
}

// Tab listeners
function admInitTabs(){
  const t1=document.getElementById('admT1');
  if(t1) t1.addEventListener('click',e=>{
    const b=e.target.closest('.adm-tab');if(!b)return;
    t1.querySelectorAll('.adm-tab').forEach(t=>t.classList.remove('on'));
    b.classList.add('on'); buildAdmC1(b.dataset.v);
  });
  const t4=document.getElementById('admT4');
  if(t4) t4.addEventListener('click',e=>{
    const b=e.target.closest('.adm-tab');if(!b)return;
    t4.querySelectorAll('.adm-tab').forEach(t=>t.classList.remove('on'));
    b.classList.add('on'); buildAdmC4(b.dataset.v);
  });
  const t5=document.getElementById('admT5');
  if(t5) t5.addEventListener('click',e=>{
    const b=e.target.closest('.adm-tab');if(!b)return;
    t5.querySelectorAll('.adm-tab').forEach(t=>t.classList.remove('on'));
    b.classList.add('on');
    if(b.dataset.v==='calc') buildAdmS5calc(); else buildAdmS5outcomes();
  });
}

// goTo hook: initialize charts on slide entry
const _admGoTo=window.goTo;
window.goTo=function(idx){
  _admGoTo(idx);
  const id=typeof SLIDES!=='undefined'&&SLIDES[idx]?SLIDES[idx].id:'';
  if(id==='admin-s0') setTimeout(buildAdmC0,50);
  else if(id==='admin-s1') setTimeout(()=>buildAdmC1('staff'),50);
  else if(id==='admin-s4') setTimeout(()=>buildAdmC4('frag'),50);
  else if(id==='admin-s5') setTimeout(buildAdmS5calc,50);
};

// U-Curve (admin-s1c)
(function(){
const BHPF_DOTS=[
  {id:'b1',label:'BHPF < $15M',rev:10,admin:10.8,color:'#BA7517',n:13,
   buckets:[{label:'Finance & accounting',val:'~2.1% of staff',benchmark:'1.05% (APQC $1B+)',pill:'adm-pill-r',delta:'+100% vs benchmark'},
            {label:'IT',val:'~2.3% of staff',benchmark:'1.2% (APQC $1B+)',pill:'adm-pill-r',delta:'+92% vs benchmark'},
            {label:'Billing / RCM',val:'~2.0% of staff',benchmark:'1.05% (APQC $1B+)',pill:'adm-pill-r',delta:'+90% vs benchmark'},
            {label:'HR & payroll',val:'~1.6% of staff',benchmark:'1.0% (APQC $1B+)',pill:'adm-pill-a',delta:'+60% vs benchmark'}],
   compare:'A $10M CMHC pays twice the overhead per revenue dollar vs a $1B system — for software that does less.'},
  {id:'b2',label:'BHPF $15–30M',rev:22,admin:11.5,color:'#BA7517',n:8,
   buckets:[{label:'Finance & accounting',val:'~1.9% of staff',benchmark:'1.05% (APQC $1B+)',pill:'adm-pill-r',delta:'+81% vs benchmark'},
            {label:'IT',val:'~2.1% of staff',benchmark:'1.2% (APQC $1B+)',pill:'adm-pill-r',delta:'+75% vs benchmark'},
            {label:'Billing / RCM',val:'~2.0% of staff',benchmark:'1.05% (APQC $1B+)',pill:'adm-pill-r',delta:'+90% vs benchmark'},
            {label:'HR & payroll',val:'~1.5% of staff',benchmark:'1.0% (APQC $1B+)',pill:'adm-pill-a',delta:'+50% vs benchmark'}],
   compare:'The $15–30M tier is the paradox tier: slightly more revenue but proportionally MORE admin cost.'},
  {id:'b3',label:'BHPF $30M+',rev:60,admin:12.6,color:'#BA7517',n:13,
   buckets:[{label:'Finance & accounting',val:'~2.2% of staff',benchmark:'1.05% (APQC $1B+)',pill:'adm-pill-r',delta:'+110% vs benchmark'},
            {label:'IT',val:'~2.1% of staff',benchmark:'1.2% (APQC $1B+)',pill:'adm-pill-r',delta:'+75% vs benchmark'},
            {label:'Billing / RCM',val:'~2.3% of staff',benchmark:'1.05% (APQC $1B+)',pill:'adm-pill-r',delta:'+119% vs benchmark'},
            {label:'HR & payroll',val:'~1.5% of staff',benchmark:'1.0% (APQC $1B+)',pill:'adm-pill-a',delta:'+50% vs benchmark'}],
   compare:'The $30M+ tier has the highest admin ratio — 12.6%. More revenue has not bought better systems.'},
  {id:'b4',label:'BHPF $1.1B consolidated',rev:1100,admin:11.7,color:'#BA7517',outline:true,n:34,
   buckets:[{label:'Finance & accounting',val:'~1.9% of staff',benchmark:'1.05% (APQC $1B+)',pill:'adm-pill-r',delta:'+81% vs benchmark'},
            {label:'IT',val:'~2.0% of staff',benchmark:'1.2% (APQC $1B+)',pill:'adm-pill-r',delta:'+67% vs benchmark'},
            {label:'Billing / RCM',val:'~2.0% of staff',benchmark:'1.05% (APQC $1B+)',pill:'adm-pill-r',delta:'+90% vs benchmark'},
            {label:'HR & payroll',val:'~1.4% of staff',benchmark:'1.0% (APQC $1B+)',pill:'adm-pill-a',delta:'+40% vs benchmark'}],
   compare:'At $1.1B scale, shared platforms, AI, and vendor leverage could close the gap.'}
];
const REF=[{label:'PCP $15–20M',rev:17.5,admin:16,color:'#1D9E75'},{label:'Hospital A&G',rev:80,admin:4.8,color:'#888'}];
const SW=640,SH=330,PAD={t:24,r:20,b:46,l:52};
const W=SW-PAD.l-PAD.r,H=SH-PAD.t-PAD.b;
function xS(v){return PAD.l+Math.log10(v/5)/Math.log10(5000/5)*W;}
function yS(v){return PAD.t+H-(v/22)*H;}
function curveY(r){const lx=Math.log10(r),sw=Math.log10(700),d=lx-sw;return Math.max(6.5,18+(-2.2)*d+4.5*Math.abs(d)*0.5-1.2*d*d+0.4*d*d*d);}
function admBuildCurve(){
  const svg=document.getElementById('admCurveSvg');if(!svg)return;
  svg.innerHTML='';const ns='http://www.w3.org/2000/svg';
  function el(tag,attrs,p){const e=document.createElementNS(ns,tag);for(const[k,v]of Object.entries(attrs))e.setAttribute(k,v);if(p)p.appendChild(e);return e;}
  [5,8,10,12,15,18,20].forEach(y=>{const cy=yS(y);el('line',{x1:PAD.l,y1:cy,x2:PAD.l+W,y2:cy,stroke:'rgba(0,0,0,.06)','stroke-width':1},svg);el('text',{x:PAD.l-5,y:cy+4,'text-anchor':'end','font-size':'9','font-family':'monospace',fill:'#a09d98'},svg).textContent=y+'%';});
  [10,30,100,300,1000,3000].forEach(x=>{const cx=xS(x);el('line',{x1:cx,y1:PAD.t,x2:cx,y2:PAD.t+H,stroke:'rgba(0,0,0,.05)','stroke-width':1},svg);el('text',{x:cx,y:PAD.t+H+12,'text-anchor':'middle','font-size':'8','font-family':'monospace',fill:'#a09d98'},svg).textContent=x>=1000?'$'+(x/1000)+'B':'$'+x+'M';});
  el('line',{x1:PAD.l,y1:PAD.t,x2:PAD.l,y2:PAD.t+H,stroke:'rgba(0,0,0,.15)','stroke-width':1},svg);
  el('line',{x1:PAD.l,y1:PAD.t+H,x2:PAD.l+W,y2:PAD.t+H,stroke:'rgba(0,0,0,.15)','stroke-width':1},svg);
  const x1b=xS(500),x2b=xS(1500);
  el('rect',{x:x1b,y:PAD.t,width:x2b-x1b,height:H,fill:'rgba(29,158,117,.08)'},svg);
  el('text',{x:(x1b+x2b)/2,y:PAD.t+10,'text-anchor':'middle','font-size':'8','font-family':'monospace',fill:'#1D9E75','font-weight':'600'},svg).textContent='SWEET SPOT';
  const pts=[];for(let r=5;r<=4500;r*=1.05)pts.push([xS(r).toFixed(1),yS(curveY(r)).toFixed(1)]);
  el('path',{d:'M'+pts.map(p=>p.join(',')).join(' L'),fill:'none',stroke:'#ccc','stroke-width':'2','stroke-dasharray':'5 4'},svg);
  REF.forEach(rd=>{const cx=xS(rd.rev),cy=yS(rd.admin);el('circle',{cx,cy,r:5,fill:rd.color,opacity:.85},svg);el('text',{x:cx+8,y:cy+3,'font-size':'8','font-family':'monospace',fill:rd.color},svg).textContent=rd.label;});
  BHPF_DOTS.forEach((d,i)=>{
    const cx=xS(d.rev),cy=yS(d.admin);
    const g=el('g',{cursor:'pointer'},svg);
    g.addEventListener('click',()=>admShowPanel(i));
    if(d.outline){el('circle',{cx,cy,r:8,fill:'none',stroke:'#BA7517','stroke-width':2,'stroke-dasharray':'3 2'},g);el('circle',{cx,cy,r:4,fill:'#BA7517'},g);}
    else{el('circle',{cx,cy,r:7,fill:'#BA7517'},g);}
    const lx=d.rev<30?cx+11:(d.rev>500?cx-10:cx+11),ly=d.rev>500?cy-14:cy-10;
    el('text',{x:lx,y:ly,'font-size':'8.5','font-family':'monospace',fill:'#BA7517','font-weight':'600'},svg).textContent=d.label;
    el('text',{x:lx,y:ly+10,'font-size':'7.5','font-family':'monospace',fill:'#a09d98'},svg).textContent=d.admin+'% · n='+d.n;
  });
}
function admShowPanel(i){
  const d=BHPF_DOTS[i];
  document.getElementById('admCpIdleEl').style.display='none';
  document.getElementById('admCpDetailEl').style.display='flex';
  document.getElementById('admCpBadgeEl').textContent=d.label;
  document.getElementById('admCpTitleEl').textContent=d.admin+'% admin ratio · n='+d.n+' · CFO Survey 2025';
  document.getElementById('admCpSubEl').textContent=d.compare;
  document.getElementById('admCpBucketsEl').innerHTML=d.buckets.map(b=>`<div class="adm-cpb-row"><span class="adm-cpb-label">${b.label}</span><span class="adm-cpb-val">${b.val}</span><span class="adm-cpb-pill ${b.pill}">${b.delta}</span></div>`).join('');
  document.getElementById('admCpCompareEl').textContent='APQC $1B+ benchmarks — Finance 1.05%, IT 1.2%, Billing 1.05%, HR 1.0%';
}
// Build curve when its slide is visited
const origGoTo2=window.goTo;
window.goTo=function(idx){
  origGoTo2(idx);
  if(typeof SLIDES!=='undefined'&&SLIDES[idx]&&SLIDES[idx].id==='admin-s1c') setTimeout(admBuildCurve,80);
};
// Also build on DOMContentLoaded if we start on that slide
if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',()=>{if(document.getElementById('admCurveSvg')){}});}
})();

// Initialize on DOM ready
if(document.readyState==='loading'){
  document.addEventListener('DOMContentLoaded',()=>{admInitTabs();buildAdmS5calc();});
}else{
  admInitTabs();buildAdmS5calc();
}
})();
"""

# Insert before the last </script>
last_script = html.rfind('</script>')
assert last_script != -1
html = html[:last_script] + ADMIN_JS + '\n' + html[last_script:]
print("✓ Admin JS added")

# ─────────────────────────────────────────────────────────────────────────────
# Write output
# ─────────────────────────────────────────────────────────────────────────────
with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✅ Done — {len(html):,} bytes written to {SRC}")
print(f"   Slide count in SLIDES array: {html.count('{id:')}")
