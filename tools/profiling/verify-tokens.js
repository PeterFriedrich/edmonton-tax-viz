// Guard: no {{token}} placeholder reaches the rendered page.
//
// tests/test_window_labels.py checks the placeholders STATICALLY — that every
// token names a real WINDOWS/CELLS key and none sits somewhere the substitution
// pass never selects. It cannot check that the pass actually FIRED, because it
// never runs the DOM.
//
// That gap was live, not hypothetical: `data-tok` is a valueless attribute, so
// `el.dataset.tok` is "" — falsy — and a truthiness test skipped every button
// while passing every static check. The buttons shipped reading
// "{{cellGlass}} grid" (2026-09-01, caught before merge).
const { chromium } = require('playwright');

(async () => {
  const url = process.argv[2] || 'http://localhost:8000/index.html';
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2500);

  let fail = 0;
  const check = (name, ok, detail = '') => {
    console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? `  ${detail}` : ''}`);
    if (!ok) fail++;
  };

  const r = await page.evaluate(() => {
    // innerHTML includes comment nodes, and one comment documents the {{key}}
    // mechanism itself — walk visible text and attributes instead.
    // Script and style text nodes live in the body too, and the substitution
    // pass's own source comments contain literal {{key}} examples.
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: n => /^(SCRIPT|STYLE)$/.test(n.parentNode.nodeName)
        ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT,
    });
    const text = [];
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      if (/\{\{\w+\}\}/.test(n.nodeValue)) text.push(n.nodeValue.trim().slice(0, 80));
    }
    const titles = [...document.querySelectorAll('[title]')]
      .map(e => e.title).filter(t => /\{\{\w+\}\}/.test(t)).map(t => t.slice(0, 80));
    const tokEls = [...document.querySelectorAll('[data-tok]')]
      .map(e => e.textContent.trim());
    return { text, titles, tokEls };
  });

  check('no raw {{token}} in visible text', r.text.length === 0, r.text.join(' | '));
  check('no raw {{token}} in any title attribute', r.titles.length === 0, r.titles.join(' | '));
  check('every [data-tok] element has substituted text',
    r.tokEls.length > 0 && r.tokEls.every(t => !/\{\{/.test(t)),
    `${r.tokEls.length} element(s): ${r.tokEls.join(' | ')}`);
  check('no page errors', errors.length === 0, errors.join(' | '));

  console.log(fail ? `\n${fail} CHECK(S) FAILED` : '\nALL CHECKS PASSED');
  await browser.close();
  process.exit(fail ? 1 : 0);
})();
