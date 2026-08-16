// Verify the experimental citywide budget panel (/full/ only).
//
// Usage: node verify-budget-panel.js [http://localhost:8791/index.html]
// ⚠️ BARE URL, no query string — the standing rule for these scripts.
//
// What it asserts, and why each one is here rather than eyeballed:
//   - the panel is FULL-BUILD ONLY (the public root must not offer it);
//   - it opens on its own button and, unlike the bottom-right pods, does NOT
//     close on a stray map click — it is a readout, not a menu;
//   - it does not collide with #millrates, which borrows the same left-column
//     slot, nor survive #temporal opening over it;
//   - the rendered dollars reconcile with the manifest, and the percentages
//     are computed from them (the manifest publishes no share);
//   - the list is ranked descending;
//   - it is capped to the viewport and scrolls, rather than running off the
//     bottom silently — the failure mode #about-menu and #temporal both hit.

const { chromium } = require("playwright");

const URL = process.argv[2] || "http://localhost:8791/index.html";

let failures = 0, checks = 0;
function check(name, cond, detail = "") {
  checks++;
  if (cond) { console.log(`  ok   ${name}`); }
  else { failures++; console.log(`  FAIL ${name}${detail ? " — " + detail : ""}`); }
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto(URL, { waitUntil: "networkidle" });
  await page.waitForTimeout(1500);

  const manifest = await page.evaluate(() =>
    fetch("./data/budget_ranked.json").then(r => r.json()));

  console.log("\n-- manifest --");
  check("services and other are both populated",
    manifest.services.length > 0 && manifest.other.length > 0,
    `${manifest.services.length}/${manifest.other.length}`);
  check("blocks reconcile with the published total",
    Math.abs(manifest.services_total + manifest.other_total - manifest.total) < 0.01);
  check("no share/percentage is published (computed in the UI only)",
    manifest.services.every(r => Object.keys(r).length === 2));
  check("services are ranked descending",
    manifest.services.every((r, i, a) => i === 0 || a[i - 1].budget >= r.budget));
  check("other is ranked descending",
    manifest.other.every((r, i, a) => i === 0 || a[i - 1].budget >= r.budget));
  check("source vintage is published",
    !!manifest.source && !!manifest.source.rows_updated_at,
    JSON.stringify(manifest.source));

  console.log("\n-- open/close --");
  check("panel starts closed", !(await page.locator("#budget").isVisible()));
  check("opener is visible in the full build",
    await page.locator("#budget-pod").isVisible());

  await page.locator("#budget-btn").click();
  await page.waitForTimeout(600);
  check("opens on its own button", await page.locator("#budget").isVisible());

  // ⚠️ A readout, not a menu: the two bottom-right pods close on click-outside
  // and this deliberately must not, or reading it while using the map is
  // impossible.
  await page.mouse.click(720, 500);
  await page.waitForTimeout(400);
  check("survives a map click (does not close like #about/#a11y)",
    await page.locator("#budget").isVisible());

  console.log("\n-- rendered content --");
  const rows = await page.locator("#budget-rows .revrow").count();
  const otherRows = await page.locator("#budget-other .revrow").count();
  check("every service branch rendered", rows === manifest.services.length,
    `${rows} vs ${manifest.services.length}`);
  check("every other branch rendered", otherRows === manifest.other.length,
    `${otherRows} vs ${manifest.other.length}`);

  const first = await page.locator("#budget-rows .revrow").first().innerText();
  check("top service row is the largest branch",
    first.includes(manifest.services[0].branch), first);

  // The percentages must be derived from the dollars in the manifest. Recompute
  // the top row's share independently and compare against what is on screen.
  const expectedPct = (manifest.services[0].budget / manifest.total) * 100;
  const shown = parseFloat((first.match(/([\d.]+)%/) || [])[1]);
  check("share is computed from the published dollars",
    Math.abs(shown - expectedPct) < 0.06, `shown ${shown} vs ${expectedPct.toFixed(2)}`);

  const noteText = await page.locator("#budget-note").innerText();
  check("note states the operating-only basis", /operating only/i.test(noteText));
  check("note states figures are citywide, not per-neighbourhood",
    /citywide/i.test(noteText) && /not neighbourhood/i.test(noteText));
  check("note carries the source vintage",
    noteText.includes(manifest.source.rows_updated_at), noteText.slice(-90));

  console.log("\n-- layout --");
  const box = await page.locator("#budget").boundingBox();
  check("panel fits inside the viewport vertically",
    box.y + box.height <= 900, JSON.stringify(box));
  const scrolls = await page.locator("#budget-body").evaluate(
    el => el.scrollHeight > el.clientHeight + 1);
  check("tall list scrolls rather than overflowing", scrolls);
  // The head must NOT be inside the scroller: every percentage on screen is a
  // share of the total printed there.
  const headPinned = await page.evaluate(() => {
    const body = document.getElementById("budget-body");
    const head = document.getElementById("budget-head");
    const before = head.getBoundingClientRect().top;
    body.scrollTop = body.scrollHeight;
    return Math.abs(head.getBoundingClientRect().top - before) < 1;
  });
  check("the total stays pinned while the list scrolls", headPinned);
  check("close button hidden on desktop (opener is adjacent and lit)",
    !(await page.locator("#budget-close").isVisible()));
  check("does not overlap the control column (x < 958)",
    box.x + box.width < 958, `right edge ${box.x + box.width}`);

  // ⚠️ THE CHECK THAT ACTUALLY CAUGHT SOMETHING. "Fits the viewport" passed
  // while the list ran 117px through the compass, legend and set-aside swatch:
  // both boxes are anchored to the viewport bottom, so the collision is
  // identical at every height and invisible to a viewport-only assertion.
  // Repeated at three heights because that is what proved it was structural.
  for (const h of [900, 800, 720]) {
    const t = await browser.newPage({ viewport: { width: 1440, height: h } });
    await t.goto(URL, { waitUntil: "networkidle" });
    // ⚠️ Wait for the ELEMENT, not a fixed delay. A bare waitForTimeout raced
    // the layout on a loaded machine and boundingBox() came back null, which
    // reads as a crash rather than a failure.
    await t.locator("#botleft").waitFor({ state: "visible", timeout: 15000 });
    await t.locator("#budget-btn").click();
    await t.locator("#budget").waitFor({ state: "visible", timeout: 15000 });
    const bud = await t.locator("#budget").boundingBox();
    const bl = await t.locator("#botleft").boundingBox();
    check(`clears #botleft at ${h}px tall`, bud.y + bud.height <= bl.y,
      `budget bottom ${(bud.y + bud.height).toFixed(0)} vs botleft top ${bl.y.toFixed(0)}`);
    await t.close();
  }

  // #millrates borrows the same slot; both visible would overlap outright.
  const millsVisible = await page.locator("#millrates").isVisible();
  check("#millrates yields the shared left-column slot", !millsVisible);

  console.log("\n-- public build must not offer it --");
  const pub = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await pub.goto(URL + "?build=public", { waitUntil: "networkidle" });
  await pub.waitForTimeout(1200);
  check("opener hidden in the public build",
    !(await pub.locator("#budget-pod").isVisible()));

  console.log("\n-- phone: the bottom-sheet form --");
  for (const w of [390, 360, 320]) {
    const phone = await browser.newPage({
      viewport: { width: w, height: 844 }, hasTouch: true, isMobile: true });
    await phone.goto(URL, { waitUntil: "networkidle" });
    await phone.waitForTimeout(1400);

    check(`${w}: opener is reachable`, await phone.locator("#budget-pod").isVisible());
    await phone.locator("#budget-btn").click();
    await phone.waitForTimeout(600);
    check(`${w}: sheet opens`, await phone.locator("#budget").isVisible());

    const s = await phone.locator("#budget").boundingBox();
    // A SHEET, not the desktop pod: anchored to the bottom, full width.
    check(`${w}: anchored to the bottom edge`, Math.abs((s.y + s.height) - (844 - 8)) < 2,
      `bottom ${(s.y + s.height).toFixed(0)}`);
    check(`${w}: spans the width without overflowing`,
      s.x >= 7 && s.x + s.width <= w - 7, `x=${s.x} w=${s.width}`);
    // ⚠️ The map is the subject; a sheet that eats it is a different product.
    check(`${w}: leaves the map more than half the screen`, s.height <= 844 * 0.55,
      `${s.height.toFixed(0)}px of 844`);

    // #controls owns 58-197 at this seam — the fact that made #temporal a
    // sheet. The sheet must not climb back into it.
    const ctrl = await phone.locator("#controls").boundingBox();
    check(`${w}: clears the control column`, s.y > ctrl.y + ctrl.height,
      `sheet top ${s.y.toFixed(0)} vs controls bottom ${(ctrl.y + ctrl.height).toFixed(0)}`);

    // ⚠️ THE MILL-RATES FAILURE MODE, applied here. There the phone one-liner
    // wrapped and broke "between a class and its number"; the fix was one row
    // each. These rows already stack, so what must hold is narrower: a long
    // BRANCH NAME may wrap, but the "$630M · 15.6%" value must never split.
    const wrapped = await phone.evaluate(() => {
      const out = [];
      document.querySelectorAll("#budget-rows .revrow, #budget-other .revrow")
        .forEach(r => {
          const b = r.querySelector("b");
          const lh = parseFloat(getComputedStyle(b).lineHeight) || 16;
          if (b.getBoundingClientRect().height > lh * 1.5) out.push(b.textContent);
        });
      return out;
    });
    check(`${w}: no value splits across lines`, wrapped.length === 0,
      wrapped.join(" | "));

    check(`${w}: close button is present and tappable`,
      await phone.locator("#budget-close").isVisible());
    const cb = await phone.locator("#budget-close").boundingBox();
    check(`${w}: close meets a ~44px touch target`, cb.width >= 34 && cb.height >= 34,
      `${cb.width}x${cb.height}`);

    // Real tap, not .click() — the standing caveat is that verify scripts
    // bypass pointer-events, and this sheet is new chrome over other chrome.
    await phone.locator("#budget-close").tap();
    await phone.waitForTimeout(500);
    check(`${w}: a real TAP on close dismisses it`,
      !(await phone.locator("#budget").isVisible()));

    await phone.close();
  }

  // #temporal is a bottom sheet too; two sheets at once would overlap outright.
  const both = await browser.newPage({
    viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
  await both.goto(URL, { waitUntil: "networkidle" });
  await both.waitForTimeout(1400);
  await both.locator("#budget-btn").click();
  await both.waitForTimeout(400);
  await both.evaluate(() => document.getElementById("temporal").classList.add("open"));
  await both.waitForTimeout(300);
  check("budget yields to an open #temporal (both are sheets on a phone)",
    !(await both.locator("#budget").isVisible()));
  await both.close();

  await browser.close();
  console.log(`\n${checks - failures}/${checks} checks passed`);
  process.exit(failures ? 1 : 0);
})();
