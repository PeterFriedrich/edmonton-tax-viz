// SCOPING INSTRUMENT for the "published number with no check" audit.
//
// ⚠️ It reads the RENDERED page, not the source. A regex over `web/index.html`
// cannot tell a blurb from a code comment — the first attempt at this counted
// `colorClamp: 30_000, // hand-set from the ramp` as a reader-facing claim —
// and the blurbs are `+`-concatenated across lines, so a per-line match splits
// a number from its sentence. Driving the page is the only way to enumerate
// what a reader can actually see.
//
// Emits JSON: every numeric claim visible in blurb / panel note / legend text,
// per view and per service layer, with the surface it appeared on. It asserts
// NOTHING — ranking and coverage judgement belong to the audit run.
//
//   node audit-published-numbers.js <url> > claims.json
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

// Dollar amounts, percentages, distances, magnitudes. Bare small integers are
// excluded: "the two bases" and "31 fire stations" are prose, not a published
// figure a guard could anchor. Years are kept — a stale year IS a published
// number, and this project has shipped one (DECISIONS.md 2026-08-27).
const NUM = /\$[\d,]+(?:\.\d+)?(?:\s?(?:million|billion|M|B))?|\d[\d,]*(?:\.\d+)?\s?(?:million|billion|%|km|m\b|×|times)|\b(?:19|20)\d{2}\b/g;

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(4000);

  const surfaces = async (label) => page.evaluate((label) => {
    const txt = id => (document.getElementById(id) || {}).textContent || '';
    const leg = [...document.querySelectorAll('#legend *')]
      .map(e => e.children.length ? '' : e.textContent).join(' ');
    return {
      label,
      blurb: txt('title-p'),
      title: txt('title-h'),
      note: txt('temporal-note'),
      read: txt('temporal-read'),
      legend: leg.replace(/\s+/g, ' ').trim(),
      about: txt('about-menu').slice(0, 4000),
    };
  }, label);

  const out = [];
  const views = await page.evaluate(() => Object.keys(VIEWS));
  for (const v of views) {
    await page.evaluate(async (v) => { await applyView(v); }, v);
    await page.waitForTimeout(900);
    // A hood must be pinned for the panel note to exist at all.
    await page.evaluate(() => { try { openTemporal('DOWNTOWN'); } catch (e) {} });
    await page.waitForTimeout(500);
    out.push(await surfaces(`view:${v}`));
    if (v === 'services') {
      const keys = await page.evaluate(() => Object.keys(SERVICES));
      for (const k of keys) {
        await page.evaluate(async (k) => {
          applyService(k, true);
          Object.keys(SERVICES).forEach(s => { if (s !== k) applyService(s, false); });
          if (state.svcDriver !== k) applySvcDriver(k);
          closeTemporal(); openTemporal('DOWNTOWN');
        }, k);
        await page.waitForTimeout(700);
        out.push(await surfaces(`service:${k}`));
      }
    }
  }

  // Collapse to distinct claims, each with the surfaces it appears on.
  const claims = {};
  for (const s of out) {
    for (const [field, text] of Object.entries(s)) {
      if (field === 'label' || !text) continue;
      for (const m of String(text).match(NUM) || []) {
        const k = m.trim();
        (claims[k] ||= new Set()).add(`${s.label}/${field}`);
      }
    }
  }
  const rows = Object.entries(claims)
    .map(([value, where]) => ({ value, n: where.size, where: [...where].slice(0, 6) }))
    .sort((a, b) => b.n - a.n);
  console.log(JSON.stringify({ captured: out.length, distinct: rows.length, rows }, null, 1));
  await browser.close();
})().catch(e => { console.error('THREW:', e.message); process.exit(1); });
