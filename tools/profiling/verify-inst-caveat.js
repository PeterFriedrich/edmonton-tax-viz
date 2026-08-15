// One-off verify for the institutional caveat on the MONEY tooltip (2026-08-15).
// The Lab bands a >=25%-institutional hood into a range and asserts no value;
// the default map keeps the solid prism and says it in words instead. Checks:
// the caveat fires on all three revenue cuts and NOT under Value (exemption
// changes whether a levy is collected, not what a parcel is assessed at); the
// hood set matches the Lab's threshold constant exactly; a low-institutional
// hood stays clean; the copy names ZONING (the row above it is a class share)
// and never asserts a direction.
//   node verify-inst-caveat.js <url>
const { chromium } = require('playwright');
const [url] = process.argv.slice(2);

// The wording rule from DECISIONS.md 2026-08-08, same list verify-deviation.js
// greps for: nothing may read as revenue the City fails to collect.
const BANNED = /\b(lost|uncollected|foregone|should be|really|actually)\b/i;

(async () => {
  const browser = await chromium.launch({
    args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
           '--ignore-gpu-blocklist', '--enable-webgl'],
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  page.on('pageerror', e => console.log('PAGE EXCEPTION:', e.message));
  page.on('console', m => { if (m.type() === 'error') console.log('PAGE ERROR:', m.text()); });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(4000);

  let fail = 0;
  const check = (name, cond, extra) => {
    console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${extra ? '  ' + extra : ''}`);
    if (!cond) fail++;
  };

  const tip = (hood, metric) => page.evaluate(([hood, metric]) => {
    if (state.metric !== metric) applyMetric(metric);
    const f = state.data.features.find(x => x.properties.neighbourhood_name === hood);
    return f ? viewTooltip({ object: f }).html : null;
  }, [hood, metric]);

  const CAVEAT = /of revenue is on institutionally-zoned land/;
  const EXEMPT = /the City does not publish which of it is tax-exempt/;

  // --- fires on Total, and prints the hood's own share ----------------------
  const ua = await tip('UNIVERSITY OF ALBERTA', 'revenue_per_acre');
  console.log('U of A / Total :', ua.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim());
  check('caveat fires on Total revenue', CAVEAT.test(ua) && EXEMPT.test(ua));
  check('share is the hood\'s own rev_frac_inst', /90% of revenue/.test(ua));
  check('headline value still printed (prism stays solid)', /\$171,670 \/ acre/.test(ua));

  // --- the two subset cuts carry it too ------------------------------------
  for (const m of ['res_revenue_per_acre', 'nonres_revenue_per_acre']) {
    const h = await tip('UNIVERSITY OF ALBERTA', m);
    check(`caveat fires on ${m}`, CAVEAT.test(h) && EXEMPT.test(h));
  }

  // --- and NOT under Value -------------------------------------------------
  const uaVal = await tip('UNIVERSITY OF ALBERTA', 'value_per_acre');
  check('NO caveat under Value (assessment is not uncertain)',
        !CAVEAT.test(uaVal) && !EXEMPT.test(uaVal));

  // --- a low-institutional hood stays clean --------------------------------
  const dt = await tip('DOWNTOWN', 'revenue_per_acre');
  check('DOWNTOWN (5% inst) has no caveat', !CAVEAT.test(dt) && !EXEMPT.test(dt));

  // --- the hood set is the Lab's, by construction --------------------------
  // Not a re-derived list: both surfaces must read INST_UNCERTAIN_MIN, so a
  // future change to the threshold moves them together or this fails.
  const sets = await page.evaluate(() => {
    if (state.metric !== 'revenue_per_acre') applyMetric('revenue_per_acre');
    const props = state.data.features.map(f => f.properties);
    const live = props.filter(p => !p.is_set_aside && p.revenue_per_acre);
    return {
      min: INST_UNCERTAIN_MIN,
      flagged: live.filter(p => instFrac(p) >= INST_UNCERTAIN_MIN)
                   .map(p => p.neighbourhood_name).sort(),
      tipped: live.filter(p => /institutionally-zoned/.test(viewTooltip({ object: { properties: p } }).html))
                  .map(p => p.neighbourhood_name).sort(),
    };
  });
  check('threshold is the Lab constant, not a copy', sets.min === 0.25, `min=${sets.min}`);
  check('tooltip set == threshold set',
        JSON.stringify(sets.flagged) === JSON.stringify(sets.tipped),
        `${sets.tipped.length} hoods`);
  check('15 hoods carry the caveat', sets.tipped.length === 15, sets.tipped.join(', '));

  // --- wording -------------------------------------------------------------
  check('copy says "zoned" (class share vs zoning share)', /institutionally-zoned/.test(ua));
  check('copy asserts no direction', !BANNED.test(ua.replace(/<[^>]+>/g, ' ')));
  check('does not claim the City fails to collect', !/fails? to collect|owed|should have/i.test(ua));

  console.log(fail ? `\n${fail} FAILED` : '\nall passed');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();
