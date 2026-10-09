# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,840-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (323 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `THEMED` | 733–735 | Colours that depend on the backdrop, one value per theme (docs/UI.md → |
| `themed` | 736–740 | Throws on a missing or mis-sized light value: deck draws `undefined` |
| `tc` | 741–746 |  |
| `CENTER` | 747–751 |  |
| `HOME` | 752–752 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 753–766 |  |
| `WINDOWS` | 767–792 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 793–802 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 803–807 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 808–883 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 884–886 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 887–888 |  |
| `METRICS` | 889–1008 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `RATIO_DENOMS` | 1009–1042 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 1043–1043 |  |
| `ratioOf` | 1044–1044 |  |
| `ratioKept` | 1045–1066 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 1067–1079 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 1080–1107 |  |
| `dominantUse` | 1108–1149 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1150–1300 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1301–1396 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1397–1401 | the Lab: a container for unfinished lenses |
| `inLab` | 1402–1403 |  |
| `DEVIATION_TITLES` | 1404–1408 |  |
| `deviationTitle` | 1409–1414 |  |
| `deviationKind` | 1415–1417 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1418–1425 |  |
| `changeBlurb` | 1426–1443 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1444–1456 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1457–1469 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1470–1478 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1479–1487 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1488–1493 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1494–1501 |  |
| `infillAmenityBlurb` | 1502–1515 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1516–1527 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1528–1533 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1534–1595 |  |
| `setBlurb` | 1596–1610 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1611–1626 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1627–1644 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1645–1651 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1652–1665 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1666–1666 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1667–1681 |  |
| `fmtMB` | 1682–1692 |  |
| `showGridBusy` | 1693–1715 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1716–1732 |  |
| `loadGridData` | 1733–1786 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1787–1840 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1841–1865 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1866–1898 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1899–1899 |  |
| `gridFetches` | 1900–1926 |  |
| `RAMPS` | 1927–1979 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `THEME_RAMPS` | 1980–2014 | The ramps for a light backdrop, per theme (docs/UI.md → Light mode, phase |
| `activeRamp` | 2015–2028 | The ramp actually drawn: the palette choice under the current theme. |
| `rampSetAside` | 2029–2041 | The set-aside colour beside a RAMP-coloured surface. Only where the |
| `lotKey` | 2042–2042 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 2043–2049 |  |
| `AMENITY_BANDS` | 2050–2051 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 2052–2054 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 2055–2060 | Whether any band is actually filtering right now. |
| `amenityInBand` | 2061–2075 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 2076–2081 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 2082–2100 |  |
| `gridScale` | 2101–2121 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 2122–2128 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 2129–2140 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2141–2143 |  |
| `quantile` | 2144–2158 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2159–2193 |  |
| `moneyBlurb` | 2194–2205 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2206–2218 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2219–2272 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `GRID_INK` | 2273–2273 |  |
| `gridName` | 2274–2287 |  |
| `paintBackdrop` | 2288–2326 | The backdrop's three MapLibre layers, after a theme or ramp change. |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2327–2327 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2328–2354 |  |
| `failLoading` | 2355–2368 |  |
| `hideLoading` | 2369–2424 |  |
| `topRings` | 2425–2441 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2442–2467 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2468–2468 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2469–2481 |  |
| `svcT` | 2482–2490 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2491–2504 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2505–2505 |  |
| `fmtFire` | 2506–2507 |  |
| `fmtTransit` | 2508–2509 |  |
| `fmtBike` | 2510–2522 |  |
| `fmtRoadM` | 2523–2536 |  |
| `fmtResShare` | 2537–2539 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2540–2545 |  |
| `fmtRoadsCost` | 2546–2550 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2551–2552 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2553–2554 |  |
| `fmtBikeCost` | 2555–2566 |  |
| `servicePlaneLayer` | 2567–2599 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2600–2609 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2610–2615 |  |
| `DEV_IND_TOTAL` | 2616–2618 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2619–2624 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2625–2629 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2630–2635 |  |
| `devGridOfferable` | 2636–2637 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2638–2638 |  |
| `devCol` | 2639–2639 |  |
| `_devScale` | 2640–2640 |  |
| `devScale` | 2641–2647 |  |
| `devT` | 2648–2651 |  |
| `developmentPlaneLayer` | 2652–2668 |  |
| `fmtDev` | 2669–2684 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2685–2690 |  |
| `DEV_GRID_IND_N` | 2691–2691 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2692–2694 |  |
| `devGridScale` | 2695–2721 |  |
| `devGridLayer` | 2722–2770 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2771–2772 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2773–2780 |  |
| `_infillStats` | 2781–2781 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2782–2799 |  |
| `_infillRaw` | 2800–2802 |  |
| `infillScore` | 2803–2818 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2819–2820 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2821–2841 |  |
| `infillColorAt` | 2842–2846 |  |
| `infillPlaneLayer` | 2847–2868 |  |
| `fmtFar` | 2869–2879 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `amenityHighlightGridLayer` | 2880–2934 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2935–2942 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2943–2957 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2958–2978 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2979–2979 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2980–2994 |  |
| `chgT` | 2995–3004 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 3005–3035 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 3036–3124 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 3125–3132 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 3133–3133 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 3134–3141 |  |
| `deviationRate` | 3142–3185 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `exemptFrac` | 3186–3215 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3216–3222 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3223–3234 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3235–3238 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3239–3243 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3244–3254 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3255–3270 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3271–3302 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3303–3380 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `isBandLayer` | 3381–3385 |  |
| `bandHover` | 3386–3394 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3395–3497 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3498–3505 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3506–3507 |  |
| `glassInstBandLayers` | 3508–3548 |  |
| `ratioInstBandLayers` | 3549–3576 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3577–3589 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3590–3591 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3592–3593 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3594–3594 |  |
| `deviationStats` | 3595–3639 |  |
| `deviationOf` | 3640–3641 |  |
| `deviationT` | 3642–3652 |  |
| `fmtDeviation` | 3653–3674 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3675–3718 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3719–3805 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3806–3830 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `fireStationsLayer` | 3831–3851 |  |
| `ensureFireStations` | 3852–3868 |  |
| `transitStationsLayer` | 3869–3886 |  |
| `ensureTransitStations` | 3887–3903 |  |
| `lrtLinesLayer` | 3904–3920 |  |
| `ensureLrtLines` | 3921–3938 |  |
| `bikeLinesLayer` | 3939–3955 |  |
| `ensureBikeLines` | 3956–4042 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `referenceSplit` | 4043–4070 |  |
| `referenceUnderLayers` | 4071–4105 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 4106–4122 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 4123–4142 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 4143–4157 |  |
| `servicesBlurb` | 4158–4169 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 4170–4193 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4194–4204 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4205–4256 |  |
| `REF_TIERS` | 4257–4278 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4279–4287 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `placeAnchors` | 4288–4311 |  |
| `labelPool` | 4312–4319 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4320–4373 |  |
| `CHROME_IDS` | 4374–4378 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4379–4397 |  |
| `visibleLabels` | 4398–4452 |  |
| `labelLayer` | 4453–4507 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `withSelectedHood` | 4508–4548 |  |
| `_ratioScales` | 4549–4549 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4550–4565 |  |
| `ratioT` | 4566–4588 |  |
| `zMatrix` | 4589–4593 |  |
| `buildLayers` | 4594–4618 |  |
| `flattenDuringEase` | 4619–4643 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4644–4958 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4959–4988 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4989–4998 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4999–5001 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 5002–5033 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 5034–5040 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 5041–5048 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 5049–5053 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 5054–5064 |  |
| `revenueLens` | 5065–5066 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 5067–5099 |  |
| `SVC_COST_BASES` | 5100–5117 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 5118–5126 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 5127–5136 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 5137–5139 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 5140–5146 |  |
| `svcRank` | 5147–5151 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 5152–5158 |  |
| `svcDriverReading` | 5159–5179 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 5180–5180 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 5181–5184 |  |
| `servicePanelFor` | 5185–5189 |  |
| `ratioPanelFor` | 5190–5213 | Ratio carries the cost-as-a-share-of-tax panel that Services had until |
| `hoodPanelLens` | 5214–5218 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 5219–5236 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 5237–5268 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5269–5274 |  |
| `sparklineSvg` | 5275–5290 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5291–5350 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5351–5356 | Development history: new supply per year |
| `devHistKey` | 5357–5366 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5367–5371 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5372–5372 |  |
| `devHistVerb` | 5373–5378 |  |
| `devHistoryFor` | 5379–5417 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5418–5437 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5438–5457 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5458–5493 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5494–5496 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5497–5560 |  |
| `syncTemporalPos` | 5561–5587 |  |
| `openTemporal` | 5588–5625 |  |
| `renderRevenueMix` | 5626–5695 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderRatioCost` | 5696–5770 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `renderServiceCost` | 5771–5828 | The Services panel: what each cost IS for this hood, in dollars, and where |
| `fmtSvcRatio` | 5829–5832 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5833–5883 |  |
| `syncPinnedPanel` | 5884–5917 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5918–5933 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5934–5951 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5952–5999 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 6000–6005 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 6006–6053 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 6054–6070 |  |
| `temporalClick` | 6071–6125 | Click a hood to pin its history; click the pinned one again to unpin. |

### neighbourhood search

| symbol | lines | what it does |
|---|---|---|
| `searchNorm` | 6126–6133 | neighbourhood search |
| `searchMatches` | 6134–6148 | Ranked: the name starts with the query, then a later WORD does (so |
| `renderSearchList` | 6149–6177 |  |
| `openSearch` | 6178–6190 |  |
| `closeSearch` | 6191–6209 |  |

### how-to-read guide

| symbol | lines | what it does |
|---|---|---|
| `openGuide` | 6210–6222 |  |
| `closeGuide` | 6223–6230 |  |
| `maybeAutoGuide` | 6231–6247 |  |
| `flyToHood` | 6248–6267 | Keep the current tilt and rotation, so the camera moves TO the hood |
| `pickSearch` | 6268–6286 | A pick reads exactly like tapping or clicking the hood (temporalClick |
| `primaryRow` | 6287–6355 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 6356–6733 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6734–6823 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6824–6824 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6825–6843 |  |
| `syncMetricButtons` | 6844–6867 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6868–6874 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6875–6888 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6889–6930 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6931–6973 |  |
| `toggleBudgetPanel` | 6974–6999 |  |
| `syncMillRates` | 7000–7032 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 7033–7053 |  |
| `applyColorAdjust` | 7054–7074 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 7075–7087 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 7088–7102 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 7103–7120 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 7121–7137 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 7138–7159 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 7160–7176 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 7177–7416 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 7417–7429 | Legend rows for the uses view: the categories actually on screen |
| `applyTheme` | 7430–7444 | Switch theme. Every tc() colour and the ramp (activeRamp) are re-read on |
| `syncThemeChrome` | 7445–7455 | The theme's wording and buttons outside the map. Also run once at boot, |
| `applyPalette` | 7456–7470 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 7471–7479 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 7480–7490 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 7491–7502 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7503–7515 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7516–7536 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7537–7584 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7585–7590 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7591–7612 |  |
| `applyMoneyDetail` | 7613–7637 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7638–7649 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7650–7657 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7658–7676 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7677–7687 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7688–7695 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7696–7712 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7713–7726 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7727–7737 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7738–7981 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7982–7991 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7992–8005 |  |
| `applySvcDriver` | 8006–8038 |  |

### shareable URL: the hash names the view on screen

| symbol | lines | what it does |
|---|---|---|
| `METRIC_FROM_URL` | 8039–8041 |  |
| `urlHash` | 8042–8082 |  |
| `shareLink` | 8083–8091 | Absolute on purpose: the full build carries <base href="../">, and a |
| `copyShareLink` | 8092–8103 | With no clipboard (an insecure origin, a denied permission) the link goes |
| `offered` | 8104–8110 | On screen, ignoring the Options fold: a folded panel on a phone hides |
| `applyUrlState` | 8111–8183 |  |
| `restoreFromHash` | 8184–8202 | Once, at the end of boot, after every build and data gate has run. The |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 8203–8840 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (1096 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 129 | the Lab: a container for unfinished lenses |
| `buildLayers` | 42 | geographic reference layers (all views) |
| `tc` | 27 | tunables |
| `themed` | 17 | tunables |
| `METRICS` | 17 | tunables |
| `applyView` | 17 | control appliers + the view/legend dispatchers |
| `SERVICES` | 16 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `refreshLegend` | 16 | control appliers + the view/legend dispatchers |
| `setBlurb` | 16 | the Lab: a container for unfinished lenses |
| `CELLS` | 11 | tunables |
| `quantile` | 10 | the Lab: a container for unfinished lenses |
| `ratioDenom` | 9 | services lens views (SPEC_services.md display architecture) |
| `ratioScale` | 9 | geographic reference layers (all views) |
| `deviationStats` | 9 | the same doubt, at 100 m |
| `esc` | 9 | money view (default): the classic metric prisms |

**Section self-containment** — share of each section's outgoing edges that stay inside it. Low means a module cut on this banner would mostly import its neighbours.

| section | edges | self-contained |
|---|---|---|
| the Lab: a container for unfinished lenses | 127 | 64% |
| tunables | 16 | 56% |
| Infill lens (SPEC_development.md Lens B) | 27 | 52% |
| uses view (use-mix, 2026-07-03) | 4 | 50% |
| deviation lens: revenue per developed acre against peer average | 4 | 50% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| base map (no basemap tiles for v1 — just a dark backdrop) | 5 | 40% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 10 | 40% |
| neighbourhood search | 11 | 36% |
| geographic reference layers (all views) | 97 | 35% |
| loading overlay | 56 | 34% |
| Development history: new supply per year | 112 | 29% |
| Money's revenue panel: where a hood's levy comes from | 35 | 29% |
| two tiers, answering two different questions | 30 | 27% |
| shareable URL: the hash names the view on screen | 24 | 21% |
| control appliers + the view/legend dispatchers | 231 | 20% |
| services lens views (SPEC_services.md display architecture) | 5 | 20% |
| the same doubt, at 100 m | 66 | 18% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| how-to-read guide | 113 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 18 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 4 | 0% |
| boot | 71 | 0% |

## Element ids (144) — the control surface

| id | line |
|---|---|
| `#map` | 39 |
| `#loading` | 43 |
| `#loading-box` | 44 |
| `#loading-title` | 55 |
| `#loading-blurb` | 56 |
| `#loading-spinner` | 57 |
| `#loading-text` | 58 |
| `#loading-retry` | 59 |
| `#banner` | 63 |
| `#gridbusy` | 74 |
| `#gridbusy-spinner` | 75 |
| `#gridbusy-text` | 77 |
| `#gridbusy-size` | 78 |
| `#title` | 82 |
| `#title-h` | 83 |
| `#title-p` | 86 |
| `#search` | 96 |
| `#search-btn` | 97 |
| `#search-box` | 100 |
| `#search-input` | 101 |
| `#search-close` | 105 |
| `#search-list` | 107 |
| `#guide-btn` | 115 |
| `#guide` | 117 |
| `#guide-close` | 118 |
| `#guide-ask` | 119 |
| `#guide-show` | 120 |
| `#guide-body` | 123 |
| `#temporal` | 142 |
| `#temporal-close` | 143 |
| `#temporal-name` | 144 |
| `#temporal-body` | 151 |
| `#temporal-chart` | 152 |
| `#temporal-read` | 153 |
| `#temporal-note` | 154 |
| `#temporal-hint` | 158 |
| `#millrates` | 174 |
| `#mill-head` | 175 |
| `#mill-rows` | 176 |
| `#mill-note` | 177 |
| `#budget` | 191 |
| `#budget-close` | 198 |
| `#budget-head` | 199 |
| `#budget-body` | 204 |
| `#budget-rows` | 205 |
| `#budget-other-hd` | 206 |
| `#budget-other` | 207 |
| `#budget-note` | 208 |
| `#peek` | 223 |
| `#peek-name` | 224 |
| `#peek-read` | 225 |
| `#peek-go` | 226 |
| `#controls` | 229 |
| `#toggle` | 242 |
| `#metric-row` | 243 |
| `#revcut` | 247 |
| `#moneymode` | 252 |
| `#views` | 258 |
| `#optpanel` | 272 |
| `#opt-fold` | 273 |
| `#opt-caret` | 273 |
| `#opt-body` | 274 |
| `#layers` | 275 |
| `#chgwindow-hd` | 276 |
| `#chgwindow` | 277 |
| `#labpick-hd` | 286 |
| `#labpick` | 287 |
| `#labcut-hd` | 288 |
| `#labcut` | 289 |
| `#moneydetail-hd` | 294 |
| `#moneydetail` | 295 |
| `#amenity-hd` | 320 |
| `#amenity` | 321 |
| `#amenity-lrt-row` | 322 |
| `#amenity-lrt-on` | 323 |
| `#amenity-school-row` | 325 |
| `#amenity-school-on` | 326 |
| `#uses-prisms-hd` | 329 |
| `#uses-prisms` | 330 |
| `#uses-prisms-on` | 332 |
| `#devmode-hd` | 335 |
| `#devmode` | 336 |
| `#devmetric-hd` | 340 |
| `#devmetric` | 341 |
| `#devwindow-hd` | 346 |
| `#devwindow` | 347 |
| `#devdetail-hd` | 352 |
| `#devdetail` | 353 |
| `#prism-hd` | 357 |
| `#prism-row` | 358 |
| `#prism-opacity` | 360 |
| `#prism-opacity-val` | 361 |
| `#services-hd` | 363 |
| `#services` | 364 |
| `#denom-hd` | 463 |
| `#denom` | 464 |
| `#ratio-denom-hd` | 468 |
| `#ratio-denom` | 469 |
| `#hoodmode` | 479 |
| `#hoodmode-btn` | 480 |
| `#coloradj` | 492 |
| `#coloradj-btn` | 493 |
| `#budget-pod` | 500 |
| `#budget-btn` | 501 |
| `#share` | 508 |
| `#share-btn` | 509 |
| `#a11y` | 512 |
| `#a11y-btn` | 513 |
| `#a11y-menu` | 514 |
| `#theme` | 516 |
| `#palette` | 521 |
| `#labels-on` | 528 |
| `#reference-on` | 536 |
| `#about` | 541 |
| `#about-btn` | 542 |
| `#about-menu` | 543 |
| `#about-src-roads` | 555 |
| `#about-src-services` | 556 |
| `#about-vintage` | 584 |
| `#about-build` | 588 |
| `#about-lot-acres` | 593 |
| `#about-modelled-roads` | 604 |
| `#about-modelled` | 626 |
| `#about-budget` | 636 |
| `#about-budget-lead` | 638 |
| `#about-budget-rows` | 639 |
| `#about-budget-note` | 640 |
| `#about-updated` | 652 |
| `#botleft` | 656 |
| `#compass` | 657 |
| `#rot-ccw` | 658 |
| `#tonorth` | 665 |
| `#needle` | 667 |
| `#rot-cw` | 672 |
| `#viewbtns` | 680 |
| `#recenter` | 682 |
| `#center2d` | 683 |
| `#legend` | 685 |
| `#legend-label` | 686 |
| `#legend-min` | 688 |
| `#legend-max` | 688 |
| `#legend-cats` | 690 |
| `#revmix` | 5645 |
| `#svccost` | 5739 |
