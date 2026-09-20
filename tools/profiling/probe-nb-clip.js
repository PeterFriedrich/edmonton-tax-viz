// Audit rendered evidence notebooks for content that is CLIPPED rather than
// scrollable at narrow widths.
//
// nbconvert's lab template uses `display: table` / `table-cell` with
// `overflow: hidden` in TWO places — `.jp-InputArea-editor` (code) and
// `.jp-OutputArea-child` (results). Either can swallow content with no scroller
// to reach it. The first version of this probe only checked the input side and
// missed clipped dataframe tables entirely, so it checks both now.
//
// It flags a CONTAINER whose content exceeds it while it cannot scroll —
// not any element wider than the viewport. An inline <span> that wraps across
// lines reports a union getBoundingClientRect() wider than its line box and is
// a false positive; that mistake cost a round trip.
//
//   node tools/profiling/probe-nb-clip.js <file-or-url> [...]

const { chromium } = require('playwright');

const WIDTHS = [390, 768, 1280];
const CONTAINERS = ['.jp-InputArea-editor', '.jp-OutputArea-child'];

(async () => {
  const targets = process.argv.slice(2);
  if (!targets.length) {
    console.error('usage: probe-nb-clip.js <file-or-url> [...]');
    process.exit(2);
  }
  const browser = await chromium.launch();
  let bad = 0;
  for (const width of WIDTHS) {
    const page = await browser.newPage({ viewport: { width, height: 900 } });
    for (const t of targets) {
      const url = /^https?:/.test(t) ? t : 'file://' + t;
      await page.goto(url, { waitUntil: 'load' });
      await page.waitForTimeout(500);
      const r = await page.evaluate((sels) => {
        const res = {};
        for (const sel of sels) {
          const els = [...document.querySelectorAll(sel)];
          // Whether content is reachable is tested by MOVING it, never by
          // reading overflow-x. The lab template sets `overflow-x: auto` on
          // .jp-RenderedHTMLCommon, which is `display: table-row` — where
          // overflow is inert. Trusting the computed style made this probe
          // report a clean page whose table was provably cut off.
          // BOTH halves are required, and each rules out a case that fooled an
          // earlier version of this probe:
          //   - computed auto/scroll rules out `overflow: hidden`, which a
          //     script CAN still scroll (scrollLeft moves) while a reader cannot
          //   - the move test rules out `overflow-x: auto` on a table-row box,
          //     where the declaration is inert
          const userScrollable = (k) => {
            if (!['auto', 'scroll'].includes(getComputedStyle(k).overflowX)) return false;
            const before = k.scrollLeft;
            k.scrollLeft = 99999;
            const moved = k.scrollLeft > 0;
            k.scrollLeft = before;
            return moved;
          };
          const clipped = els.filter((e) => {
            if (e.scrollWidth <= e.clientWidth + 2) return false;
            if (userScrollable(e)) return false;
            return ![...e.querySelectorAll('*')].some(
              (k) => k.scrollWidth > k.clientWidth + 2 && userScrollable(k)
            );
          });
          res[sel] = {
            total: els.length,
            clipped: clipped.length,
            worst: clipped.reduce((a, e) => Math.max(a, e.scrollWidth - e.clientWidth), 0),
          };
        }
        res.pageOverflow = document.documentElement.scrollWidth - window.innerWidth;
        return res;
      }, CONTAINERS);

      const name = t.split('/').pop();
      const parts = CONTAINERS.map((s) => {
        const v = r[s];
        if (v.clipped) bad++;
        return `${s.replace('.jp-', '')} ${v.clipped}/${v.total}` + (v.clipped ? ` (-${v.worst}px)` : '');
      });
      if (r.pageOverflow > 2) { bad++; parts.push(`PAGE +${r.pageOverflow}px`); }
      console.log(`${String(width).padStart(4)}px  ${name.padEnd(32)} ${parts.join('   ')}`);
    }
    await page.close();
  }
  await browser.close();
  console.log(bad ? `\nFAIL — ${bad} clipped container group(s)` : '\nOK — nothing clipped at any width');
  process.exit(bad ? 1 : 0);
})();
