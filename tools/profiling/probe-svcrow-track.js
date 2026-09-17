// SERVICES HOOD PANEL: measure the BAR TRACK at phone widths, not the row.
//
// TODO.md ("The Services panel grouping was never checked on a phone") names
// this measurement and never took it. Its warning is the whole point: the row
// is a 3-column flex (`.svcrow` in styles.css — 82px label / flex:1 track /
// 40px percentage, gap 7px), so at narrow widths the TRACK collapses toward
// zero while the row still fits. A width probe that only asks "does it
// overflow" passes on a panel whose bars have stopped saying anything. The
// existing ✅ table in that item measures overflow and clearance only.
//
// Shape of the check, per the standing lessons:
//   - A 1400px CONTROL runs first. A probe that reported thin tracks at every
//     width would be indistinguishable from a broken probe; the control is what
//     makes a narrow reading mean something.
//   - Preconditions are ASSERTED, never assumed: services view, the driver
//     actually reached, the panel actually open, and at least one `.svcrow`
//     present. No row is recorded from a state the setup failed to reach
//     (the S158 lesson).
//   - The arithmetic is cross-checked against the CSS: label + track + pct +
//     2 gaps must reconstruct the row width. If that identity fails, the
//     numbers are measuring something other than this layout.
//
//   node probe-svcrow-track.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

// Roads is the worst case: the only family shown on TWO bases, so it renders
// the most bars. The other cost drivers are measured too — a narrower track
// under a different driver would be the more interesting result.
const DRIVERS = ['roadslife', 'roadscost', 'transitcost', 'bikecost'];
const WIDTHS = [1400, 390, 360, 320];

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  let fail = 0;
  const check = (name, cond, extra) => {
    console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
    if (!cond) fail++;
  };

  const rows = [];
  for (const width of WIDTHS) {
    const phone = width < 640;
    const page = await browser.newPage({
      viewport: { width, height: phone ? 844 : 900 },
      hasTouch: phone, isMobile: phone,
      deviceScaleFactor: phone ? 3 : 1,
    });
    page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
    await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(4000);

    for (const drv of DRIVERS) {
      const r = await page.evaluate(async (k) => {
        await applyView('services');
        applyService(k, true);
        Object.keys(SERVICES).forEach(s => { if (s !== k) applyService(s, false); });
        if (state.svcDriver !== k) applySvcDriver(k);
        closeTemporal();
        openTemporal('DOWNTOWN');
        const el = document.getElementById('temporal');
        const rs = [...el.querySelectorAll('.svcrow')];
        const m = rs.map(row => {
          const span = row.querySelector('span');
          const track = row.querySelector('i');
          const fill = row.querySelector('i b');
          const em = row.querySelector('em');
          const w = e => e ? e.getBoundingClientRect().width : null;
          return {
            label: span ? span.textContent.trim() : null,
            row: w(row), lab: w(span), track: w(track), pct: w(em),
            fillPx: w(fill), fillPct: fill ? fill.style.width : null,
          };
        });
        return {
          driver: state.svcDriver,
          checked: Object.keys(SERVICES).filter(s => state.services[s]),
          open: el.classList.contains('open'),
          panelW: el.getBoundingClientRect().width,
          rows: m,
        };
      }, drv);

      // Preconditions. A row recorded from a state the setup did not reach is
      // worse than no row at all.
      const ok = r.driver === drv && r.open && r.rows.length > 0
        && r.checked.length === 1 && r.checked[0] === drv;
      check(`${width}px ${drv}: state reached (driver, single check, panel open, bars present)`,
        ok, `driver=${r.driver} open=${r.open} bars=${r.rows.length} checked=[${r.checked.join(',')}]`);
      if (!ok) continue;

      for (const m of r.rows) {
        // The layout identity, from styles.css: 82 + track + 40 + 7 + 7.
        const recon = m.lab + m.track + m.pct + 14;
        const drift = Math.abs(recon - m.row);
        check(`${width}px ${drv} "${m.label}": row reconstructs from its 3 columns`,
          drift < 1.5, `row=${m.row.toFixed(1)} vs ${recon.toFixed(1)} (drift ${drift.toFixed(2)})`);
        rows.push({ width, drv, ...m });
      }
    }
    await page.close();
  }
  await browser.close();

  console.log('\n--- TRACK WIDTH (the measurement the item asks for) ---');
  console.log('width  driver       label                     row    label  TRACK   pct   fill%');
  for (const m of rows) {
    console.log(
      `${String(m.width).padStart(5)}  ${m.drv.padEnd(11)}  ${String(m.label).padEnd(24)}` +
      `${m.row.toFixed(0).padStart(5)}${m.lab.toFixed(0).padStart(7)}` +
      `${m.track.toFixed(1).padStart(8)}${m.pct.toFixed(0).padStart(6)}` +
      `${String(m.fillPct).padStart(8)}`);
  }

  const byW = {};
  for (const m of rows) byW[m.width] = Math.min(byW[m.width] ?? Infinity, m.track);
  console.log('\n--- narrowest track per viewport ---');
  const ctrl = byW[1400];
  for (const w of WIDTHS) {
    if (byW[w] == null) { console.log(`${w}px: NO ROWS MEASURED`); continue; }
    const pctOfCtrl = ctrl ? (byW[w] / ctrl * 100).toFixed(0) + '% of control' : '';
    // 1 percentage point of the metric = track/100 px. Below ~1px per point the
    // bar cannot separate adjacent values at the precision the label prints.
    console.log(`${w}px: ${byW[w].toFixed(1)}px  (${pctOfCtrl}; ` +
      `1 metric point = ${(byW[w] / 100).toFixed(2)}px)`);
  }
  console.log(`\n${fail} FAIL`);
  process.exit(fail ? 1 : 0);
})();
