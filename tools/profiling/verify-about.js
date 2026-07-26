// Verify the Sources & attribution pod (P1.2 — the live map had no link to the
// repo, the data sources or the methodology).
//
// The load-bearing claims:
//   1. The pod is a short, always-visible entry point ("Data & Methods") that
//      does NOT overlap the bottom-left legend cluster at phone widths — the
//      long credit label it used to carry was 294px wide and sat straight on
//      top of the legend (Peter, 2026-07-25). The attribution itself now lives
//      one tap in, alongside the licence.
//   2. The vintages come from status.json, not a hardcoded literal that goes
//      stale each January (docs/RUNBOOK.md year-roll).
//   3. The caveat the project must not bury: revenue and the utility layers are
//      MODELLED, not billed.
//   4. Methods + repo links are real, absolute and target=_blank.
//   5. The two bottom-right popovers never sit open at once (they'd overlap).
//   6. It survives a missing/broken status.json — the credit still reads.
//   node verify-about.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

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

  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(4000);

  const probe = () => page.evaluate(() => {
    const vis = id => { const e = document.getElementById(id); return !!e && e.offsetParent !== null; };
    const menu = document.getElementById('about-menu');
    const links = [...menu.querySelectorAll('a')].map(a => ({
      href: a.getAttribute('href'), target: a.getAttribute('target'),
      rel: a.getAttribute('rel'), text: a.textContent.trim(),
    }));
    const r = document.getElementById('about').getBoundingClientRect();
    const mr = menu.getBoundingClientRect();
    return {
      btnShown: vis('about-btn'),
      btnText: document.getElementById('about-btn').textContent.replace(/\s+/g, ' ').trim(),
      menuOpen: document.getElementById('about').classList.contains('open'),
      a11yOpen: document.getElementById('a11y').classList.contains('open'),
      menuText: menu.textContent.replace(/\s+/g, ' ').trim(),
      vintage: document.getElementById('about-vintage').textContent,
      updated: document.getElementById('about-updated').textContent,
      links,
      podRight: Math.round(r.right), menuRight: Math.round(mr.right),
      menuLeft: Math.round(mr.left), menuTop: Math.round(mr.top),
    };
  });

  // --- 1. the entry point reads before any click --------------------------
  let p = await probe();
  check('pod is visible on load', p.btnShown);
  check('button label is the short form', p.btnText === 'Data & Methods',
        JSON.stringify(p.btnText));
  check('label carries no year (it would go stale)', !/\d{4}/.test(p.btnText));
  check('menu starts closed', !p.menuOpen);

  // --- 2. vintages come from status.json ----------------------------------
  const status = await page.evaluate(async () => {
    const r = await fetch('./data/status.json', { cache: 'no-store' });
    return r.ok ? r.json() : null;
  });
  check('status.json reachable', !!status);

  await page.click('#about-btn');
  await page.waitForTimeout(400);
  p = await probe();
  check('clicking opens the panel', p.menuOpen);
  if (status) {
    check('vintage line carries assessment year', p.vintage.includes(String(status.data_year)), p.vintage);
    check('vintage line carries rate year',       p.vintage.includes(String(status.rate_year)), p.vintage);
    check('vintage line carries zoning year',     p.vintage.includes(String(status.zoning_year)), p.vintage);
    check('rebuilt line carries generated date',  p.updated.includes(status.generated), p.updated);
    // The whole point: no year may be a literal in the SOURCE. Read the served
    // file, not the DOM — the DOM legitimately shows the years, JS just put them
    // there, so regexing outerHTML would always "fail" and prove nothing.
    // Scope to the pod's OWN markup: the rest of the file is full of prose years
    // ("the 2024 Zoning Bylaw", "2021–2025") that a whole-file regex flags as
    // false positives.
    const src = await (await page.request.get(url)).text();
    const block = src.slice(src.indexOf('<div id="about"'), src.indexOf('<div id="botleft"'));
    check('found the pod markup to inspect', block.length > 200 && block.length < 4000,
          `${block.length} chars`);
    // Strip HTML comments first. The rule being enforced is "no year a READER
    // can see is a literal" — a comment renders nothing, so a year in one
    // (the licence's "v1.0, July 2022", a dated DECISIONS.md pointer) can never
    // go stale on screen. Leaving them in scope would only pressure the next
    // person to delete the explanation to get the suite green.
    const stray = block.replace(/<!--[\s\S]*?-->/g, ' ').match(/\b(19|20)\d\d\b/g);
    check('no year literal in the pod markup', !stray,
          stray ? `found: ${[...new Set(stray)].join(', ')}` : '');
  }

  // --- 3. the attribution + caveats are present ---------------------------
  // The credit moved off the button, so the panel is now the ONLY place it
  // lives — it has to be there.
  check('panel credits the City of Edmonton', /City of Edmonton/.test(p.menuText));
  check('licence is named', /Open Government Licence/i.test(p.menuText));
  // The OGL – City of Edmonton (v1.0, July 2022) prescribes this EXACT sentence
  // where the Information Provider specifies no attribution statement of its
  // own. Asserted verbatim, whitespace-normalised, because a reworded version
  // is not compliance — read the licence before touching this string.
  check('OGL prescribed attribution statement, VERBATIM',
        p.menuText.replace(/\s+/g, ' ')
         .includes('Contains information licensed under the Open Government Licence – City of Edmonton.'));
  // "...and, where possible, provide a link to this licence." Plainly possible
  // here, so its absence would be the one unambiguous gap.
  check('links to the licence itself',
        p.links.some(l => /data\.edmonton\.ca\/stories\/s\/.*msh8-if28/.test(l.href)),
        p.links.map(l => l.href).join(' | '));
  // The licence grants no right to imply official status or endorsement.
  check('disclaims affiliation/endorsement',
        /not affiliated with, nor endorsed by, the City/i.test(p.menuText));
  check('caveats heading reads "Important caveats"',
        /Important caveats/i.test(p.menuText));
  check('says revenue is modelled, not billed',
        /modelled, not billed|modeled, not billed/i.test(p.menuText));
  check('flags the utility layers as modelled',
        /stormwater and water\/sewer/i.test(p.menuText) && /not utility records/i.test(p.menuText));
  check('disclaims full cost of city services',
        /never the full cost/i.test(p.menuText));

  // --- 4. links ------------------------------------------------------------
  const methods = p.links.find(l => /METHODS\.md$/.test(l.href || ''));
  const repo = p.links.find(l => /edmonton-tax-viz\/?$/.test(l.href || ''));
  check('methods link present', !!methods, methods && methods.href);
  check('repo link present', !!repo, repo && repo.href);
  check('all links absolute https', p.links.every(l => /^https:\/\//.test(l.href)));
  check('all links open in a new tab with noopener',
        p.links.every(l => l.target === '_blank' && /noopener/.test(l.rel || '')));
  // A 404 methods link is worse than no link — actually fetch them. Must go
  // through page.request (Playwright's own client), NOT in-page fetch(): github
  // sends no CORS header, so an in-page fetch reports "blocked" for a perfectly
  // good URL and tells us nothing about whether it resolves.
  // 429/403 is github throttling this box, not a verdict on the URL — report it
  // as inconclusive rather than failing the suite on someone else's rate limit.
  for (const l of p.links) {
    let st;
    try { st = (await page.request.get(l.href, { timeout: 20000 })).status(); }
    catch (e) { st = 'error:' + e.message.slice(0, 40); }
    if (st === 429 || st === 403) {
      console.log(`SKIP  link resolves: ${l.text.slice(0, 28)}  rate-limited (${st}), not checked`);
    } else {
      check(`link resolves: ${l.text.slice(0, 28)}`, st === 200, `status=${st} ${l.href}`);
    }
  }

  // --- 5. the two popovers are mutually exclusive --------------------------
  await page.click('#a11y-btn');
  await page.waitForTimeout(300);
  p = await probe();
  check('opening Display closes Sources', p.a11yOpen && !p.menuOpen);
  await page.click('#about-btn');
  await page.waitForTimeout(300);
  p = await probe();
  check('opening Sources closes Display', p.menuOpen && !p.a11yOpen);
  await page.click('#map', { position: { x: 700, y: 400 } });
  await page.waitForTimeout(300);
  p = await probe();
  check('clicking the map closes it', !p.menuOpen && !p.a11yOpen);

  // --- 5b. the button must not sit on the bottom-left cluster --------------
  // This is the reported bug: the old 294px credit label ran from x=73 to x=367
  // at 390px while #legend reached x=304, so the button was painted straight on
  // top of the legend text. Geometry, at the two common phone widths plus
  // desktop — a screenshot is not the oracle here, boxes are.
  for (const vp of [{ width: 390, height: 844 }, { width: 360, height: 800 },
                    { width: 1440, height: 900 }]) {
    const pg = await browser.newPage({ viewport: vp });
    await pg.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
    await pg.waitForTimeout(4000);
    const g = await pg.evaluate(() => {
      const box = id => { const b = document.getElementById(id).getBoundingClientRect();
                          return { l: b.left, r: b.right, t: b.top, b: b.bottom }; };
      const hit = (a, b) => a.l < b.r && b.l < a.r && a.t < b.b && b.t < a.b;
      const btn = box('about-btn'), bl = box('botleft'), a11y = box('a11y');
      return { btnW: Math.round(btn.r - btn.l), btnL: Math.round(btn.l),
               blR: Math.round(bl.r), onBotleft: hit(btn, bl), onA11y: hit(btn, a11y) };
    });
    check(`${vp.width}px: button clear of the bottom-left cluster`, !g.onBotleft,
          `button ${g.btnL}..${g.btnL + g.btnW}, cluster ends ${g.blR}`);
    check(`${vp.width}px: button clear of the Display pod`, !g.onA11y);
    await pg.close();
  }

  // --- 6. phone: the panel must not overflow the viewport ------------------
  const phone = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await phone.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await phone.waitForTimeout(4000);
  await phone.click('#about-btn');
  await phone.waitForTimeout(400);
  const ph = await phone.evaluate(() => {
    const m = document.getElementById('about-menu').getBoundingClientRect();
    const b = document.getElementById('about-btn').getBoundingClientRect();
    return { left: Math.round(m.left), right: Math.round(m.right), top: Math.round(m.top),
             btnLeft: Math.round(b.left), btnRight: Math.round(b.right), w: window.innerWidth };
  });
  check('390px: panel starts on screen', ph.left >= 0, `left=${ph.left}`);
  check('390px: panel ends on screen', ph.right <= ph.w, `right=${ph.right} vw=${ph.w}`);
  check('390px: panel top is on screen', ph.top >= 0, `top=${ph.top}`);
  check('390px: credit button fits', ph.btnLeft >= 0 && ph.btnRight <= ph.w,
        `${ph.btnLeft}..${ph.btnRight} vw=${ph.w}`);
  // Paint order: on a phone the panel is tall enough to reach the bottom-left
  // cluster, and everything on the map shares z-index 1 — so #botleft used to
  // draw its compass/Center buttons straight THROUGH the panel text. Sample the
  // overlap region and demand the panel is what's actually on top.
  const overlap = await phone.evaluate(() => {
    const m = document.getElementById('about-menu').getBoundingClientRect();
    const bl = document.getElementById('botleft').getBoundingClientRect();
    const x = Math.round(Math.max(m.left, bl.left) + 4);
    const y = Math.round(Math.max(m.top, bl.top) + 4);
    if (x > Math.min(m.right, bl.right) || y > Math.min(m.bottom, bl.bottom))
      return { overlaps: false };
    const el = document.elementFromPoint(x, y);
    return { overlaps: true, x, y,
             inPanel: !!(el && el.closest('#about')),
             hit: el ? (el.id || el.tagName.toLowerCase()) : null };
  });
  if (!overlap.overlaps) {
    console.log('SKIP  390px: panel and #botleft do not overlap — nothing to stack');
  } else {
    check('390px: panel paints above the bottom-left chrome', overlap.inPanel,
          `at (${overlap.x},${overlap.y}) topmost=${overlap.hit}`);
  }
  await phone.close();

  // --- 7. a broken status.json must not break the credit -------------------
  const blind = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await blind.route('**/status.json*', r => r.abort());
  await blind.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await blind.waitForTimeout(4000);
  const b = await blind.evaluate(() => ({
    btn: document.getElementById('about-btn').textContent.replace(/\s+/g, ' ').trim(),
    vintage: document.getElementById('about-vintage').textContent,
    shown: document.getElementById('about-btn').offsetParent !== null,
  }));
  check('no status.json: pod still reachable', b.shown && b.btn === 'Data & Methods', b.btn);
  check('no status.json: vintage line stays empty', b.vintage === '', JSON.stringify(b.vintage));
  await blind.close();

  await browser.close();
  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  process.exit(fail ? 1 : 0);
})();
