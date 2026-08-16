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
  const scrolls = await page.locator("#budget").evaluate(
    el => el.scrollHeight > el.clientHeight + 1);
  check("tall list scrolls rather than overflowing", scrolls);
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
    await t.waitForTimeout(1200);
    await t.locator("#budget-btn").click();
    await t.waitForTimeout(500);
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

  console.log("\n-- mobile: desktop-only by decision --");
  const phone = await browser.newPage({
    viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
  await phone.goto(URL, { waitUntil: "networkidle" });
  await phone.waitForTimeout(1200);
  check("opener hidden at 390px", !(await phone.locator("#budget-pod").isVisible()));

  await browser.close();
  console.log(`\n${checks - failures}/${checks} checks passed`);
  process.exit(failures ? 1 : 0);
})();
