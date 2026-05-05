/* admin-s1c — pricing-trap ROI curve. Render via global buildAdmCurve()
   which reads admCurveSvg + _ADM_CURVE_DATA from story.html.

   Click handlers (admCurveClick) are global onclick attrs on the SVG circles.
*/
export function mount(_container) {
  setTimeout(() => {
    if (typeof window.buildAdmCurve === 'function') {
      try { window.buildAdmCurve(); } catch (e) { console.warn('[admin-s1c] buildAdmCurve failed', e); }
    }
  }, 60);
}
export function unmount() { /* no-op */ }
