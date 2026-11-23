# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~9,065-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (330 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `THEMED` | 761–763 | Colours that depend on the backdrop, one value per theme (docs/UI.md → |
| `themed` | 764–768 | Throws on a missing or mis-sized light value: deck draws `undefined` |
| `tc` | 769–774 |  |
| `CENTER` | 775–779 |  |
| `HOME` | 780–780 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 781–794 |  |
| `WINDOWS` | 795–820 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 821–830 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 831–835 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 836–911 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 912–914 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 915–916 |  |
| `METRICS` | 917–1038 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `RATIO_DENOMS` | 1039–1072 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 1073–1073 |  |
| `ratioOf` | 1074–1074 |  |
| `ratioKept` | 1075–1096 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 1097–1109 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 1110–1137 |  |
| `dominantUse` | 1138–1179 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1180–1330 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1331–1426 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1427–1431 | the Lab: a container for unfinished lenses |
| `inLab` | 1432–1433 |  |
| `DEVIATION_TITLES` | 1434–1438 |  |
| `deviationTitle` | 1439–1444 |  |
| `deviationKind` | 1445–1445 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1446–1453 |  |
| `changeBlurb` | 1454–1471 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1472–1484 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1485–1501 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1502–1510 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1511–1519 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1520–1525 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1526–1532 |  |
| `infillAmenityBlurb` | 1533–1546 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1547–1558 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1559–1564 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1565–1626 |  |
| `setBlurb` | 1627–1641 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1642–1657 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1658–1675 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1676–1682 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1683–1696 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1697–1697 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1698–1712 |  |
| `fmtMB` | 1713–1723 |  |
| `showGridBusy` | 1724–1746 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1747–1763 |  |
| `loadGridData` | 1764–1820 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1821–1874 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1875–1899 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1900–1932 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1933–1933 |  |
| `gridFetches` | 1934–1960 |  |
| `RAMPS` | 1961–2013 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `THEME_RAMPS` | 2014–2048 | The ramps for a light backdrop, per theme (docs/UI.md → Light mode, phase |
| `activeRamp` | 2049–2062 | The ramp actually drawn: the palette choice under the current theme. |
| `rampSetAside` | 2063–2075 | The set-aside colour beside a RAMP-coloured surface. Only where the |
| `lotKey` | 2076–2076 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 2077–2083 |  |
| `AMENITY_BANDS` | 2084–2085 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 2086–2088 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 2089–2094 | Whether any band is actually filtering right now. |
| `amenityInBand` | 2095–2109 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 2110–2115 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 2116–2134 |  |
| `gridScale` | 2135–2155 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 2156–2162 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 2163–2174 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2175–2177 |  |
| `quantile` | 2178–2192 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2193–2227 |  |
| `moneyBlurb` | 2228–2239 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2240–2252 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2253–2306 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `GRID_INK` | 2307–2307 |  |
| `gridName` | 2308–2321 |  |
| `paintBackdrop` | 2322–2359 | The backdrop's three MapLibre layers, after a theme or ramp change. |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2360–2360 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2361–2385 |  |
| `failLoading` | 2386–2399 |  |
| `hideLoading` | 2400–2455 |  |
| `topRings` | 2456–2472 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2473–2498 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2499–2499 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2500–2512 |  |
| `svcT` | 2513–2521 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2522–2535 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2536–2536 |  |
| `fmtFire` | 2537–2538 |  |
| `fmtTransit` | 2539–2540 |  |
| `fmtBike` | 2541–2553 |  |
| `fmtRoadM` | 2554–2567 |  |
| `fmtResShare` | 2568–2570 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2571–2576 |  |
| `fmtRoadsCost` | 2577–2581 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2582–2583 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2584–2585 |  |
| `fmtBikeCost` | 2586–2597 |  |
| `servicePlaneLayer` | 2598–2630 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2631–2640 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2641–2646 |  |
| `DEV_IND_TOTAL` | 2647–2649 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2650–2655 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2656–2660 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2661–2666 |  |
| `devGridOfferable` | 2667–2668 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2669–2669 |  |
| `devCol` | 2670–2670 |  |
| `_devScale` | 2671–2671 |  |
| `devScale` | 2672–2678 |  |
| `devT` | 2679–2682 |  |
| `developmentPlaneLayer` | 2683–2699 |  |
| `fmtDev` | 2700–2715 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2716–2721 |  |
| `DEV_GRID_IND_N` | 2722–2722 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2723–2725 |  |
| `devGridScale` | 2726–2752 |  |
| `devGridLayer` | 2753–2801 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2802–2803 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2804–2811 |  |
| `_infillStats` | 2812–2812 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2813–2830 |  |
| `_infillRaw` | 2831–2833 |  |
| `infillScore` | 2834–2849 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2850–2851 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2852–2872 |  |
| `infillColorAt` | 2873–2877 |  |
| `infillPlaneLayer` | 2878–2899 |  |
| `fmtFar` | 2900–2910 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `amenityHighlightGridLayer` | 2911–2965 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2966–2973 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2974–2988 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2989–3009 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 3010–3010 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 3011–3025 |  |
| `chgT` | 3026–3035 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 3036–3066 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 3067–3155 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 3156–3163 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 3164–3164 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 3165–3172 |  |
| `deviationRate` | 3173–3225 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `EXEMPT_COL` | 3226–3230 | ⚠️ THE SHARE OF THE CUT BEING DRAWN, not of the total levy |
| `exemptFrac` | 3231–3233 |  |
| `exemptCutWord` | 3234–3265 | COPY_DECISIONS F6 (option A): the caveat names the cut its share is of. |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3266–3272 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3273–3284 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3285–3288 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3289–3293 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3294–3304 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3305–3320 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3321–3352 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3353–3430 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `isBandLayer` | 3431–3435 |  |
| `bandHover` | 3436–3444 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3445–3548 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `GRID_EXEMPT_COL` | 3549–3553 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `gridExemptCol` | 3554–3555 |  |
| `glassInstCells` | 3556–3563 |  |
| `glassInstCount` | 3564–3565 |  |
| `glassInstBandLayers` | 3566–3606 |  |
| `ratioInstBandLayers` | 3607–3634 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3635–3647 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3648–3649 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3650–3651 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3652–3652 |  |
| `deviationStats` | 3653–3697 |  |
| `deviationOf` | 3698–3699 |  |
| `deviationT` | 3700–3710 |  |
| `fmtDeviation` | 3711–3732 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3733–3776 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3777–3863 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3864–3888 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `fireStationsLayer` | 3889–3909 |  |
| `ensureFireStations` | 3910–3926 |  |
| `transitStationsLayer` | 3927–3944 |  |
| `ensureTransitStations` | 3945–3961 |  |
| `lrtLinesLayer` | 3962–3978 |  |
| `ensureLrtLines` | 3979–3996 |  |
| `bikeLinesLayer` | 3997–4013 |  |
| `ensureBikeLines` | 4014–4100 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `referenceSplit` | 4101–4128 |  |
| `referenceUnderLayers` | 4129–4163 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 4164–4180 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 4181–4200 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 4201–4215 |  |
| `servicesBlurb` | 4216–4227 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 4228–4264 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4265–4275 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4276–4327 |  |
| `REF_TIERS` | 4328–4349 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4350–4361 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `placeAnchors` | 4362–4386 |  |
| `labelPool` | 4387–4394 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4395–4448 |  |
| `CHROME_IDS` | 4449–4453 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4454–4472 |  |
| `visibleLabels` | 4473–4542 |  |
| `labelLayer` | 4543–4598 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `withSelectedHood` | 4599–4639 |  |
| `_ratioScales` | 4640–4640 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4641–4656 |  |
| `ratioT` | 4657–4679 |  |
| `zMatrix` | 4680–4684 |  |
| `buildLayers` | 4685–4709 |  |
| `flattenDuringEase` | 4710–4734 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4735–5049 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 5050–5079 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 5080–5089 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 5090–5092 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 5093–5124 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 5125–5131 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 5132–5139 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 5140–5144 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 5145–5155 |  |
| `revenueLens` | 5156–5157 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 5158–5190 |  |
| `SVC_COST_BASES` | 5191–5208 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 5209–5217 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 5218–5227 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 5228–5230 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 5231–5237 |  |
| `svcRank` | 5238–5242 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 5243–5249 |  |
| `svcDriverReading` | 5250–5270 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 5271–5271 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 5272–5275 |  |
| `servicePanelFor` | 5276–5280 |  |
| `ratioPanelFor` | 5281–5304 | Ratio carries the cost-as-a-share-of-tax panel that Services had until |
| `hoodPanelLens` | 5305–5309 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 5310–5327 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 5328–5359 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5360–5365 |  |
| `sparklineSvg` | 5366–5381 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5382–5441 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5442–5447 | Development history: new supply per year |
| `devHistKey` | 5448–5457 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5458–5462 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5463–5463 |  |
| `devHistVerb` | 5464–5469 |  |
| `devHistoryFor` | 5470–5508 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5509–5528 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5529–5548 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5549–5584 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5585–5587 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5588–5651 |  |
| `syncTemporalPos` | 5652–5706 |  |
| `syncControlsTop` | 5707–5724 |  |
| `openTemporal` | 5725–5762 |  |
| `renderRevenueMix` | 5763–5837 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderRatioCost` | 5838–5922 |  |
| `renderServiceCost` | 5923–5980 | The Services panel: what each cost IS for this hood, in dollars, and where |
| `fmtSvcRatio` | 5981–5984 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5985–6035 |  |
| `syncPinnedPanel` | 6036–6069 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 6070–6085 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 6086–6103 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 6104–6151 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 6152–6157 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 6158–6205 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 6206–6222 |  |
| `temporalClick` | 6223–6277 | Click a hood to pin its history; click the pinned one again to unpin. |

### neighbourhood search

| symbol | lines | what it does |
|---|---|---|
| `searchNorm` | 6278–6285 | neighbourhood search |
| `searchMatches` | 6286–6300 | Ranked: the name starts with the query, then a later WORD does (so |
| `renderSearchList` | 6301–6329 |  |
| `openSearch` | 6330–6342 |  |
| `closeSearch` | 6343–6361 |  |

### how-to-read guide

| symbol | lines | what it does |
|---|---|---|
| `openGuide` | 6362–6374 |  |
| `closeGuide` | 6375–6382 |  |
| `maybeAutoGuide` | 6383–6399 |  |
| `flyToHood` | 6400–6419 | Keep the current tilt and rotation, so the camera moves TO the hood |
| `pickSearch` | 6420–6438 | A pick reads exactly like tapping or clicking the hood (temporalClick |
| `primaryRow` | 6439–6507 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 6508–6887 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6888–6977 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6978–6978 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6979–6997 |  |
| `syncMetricButtons` | 6998–7021 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 7022–7028 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 7029–7042 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 7043–7075 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |
| `SPLIT_CLASS_LABELS` | 7076–7080 | The Data & Methods pod's citywide tax split (2026-11-17). Two cuts of one |
| `renderCitywideLevy` | 7081–7130 |  |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 7131–7173 |  |
| `toggleBudgetPanel` | 7174–7199 |  |
| `syncMillRates` | 7200–7233 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 7234–7254 |  |
| `applyColorAdjust` | 7255–7275 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 7276–7288 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 7289–7303 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 7304–7321 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 7322–7338 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 7339–7360 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 7361–7377 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 7378–7617 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 7618–7634 | Legend rows for the uses view: the categories actually on screen |
| `applyTheme` | 7635–7657 |  |
| `syncThemeChrome` | 7658–7668 | The theme's wording and buttons outside the map. Also run once at boot, |
| `applyPalette` | 7669–7684 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 7685–7693 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 7694–7704 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 7705–7716 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7717–7729 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7730–7750 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7751–7798 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7799–7804 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7805–7826 |  |
| `applyMoneyDetail` | 7827–7851 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7852–7863 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7864–7871 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7872–7890 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7891–7901 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7902–7909 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7910–7926 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7927–7940 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7941–7951 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7952–8196 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 8197–8206 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 8207–8220 |  |
| `applySvcDriver` | 8221–8253 |  |

### shareable URL: the hash names the view on screen

| symbol | lines | what it does |
|---|---|---|
| `METRIC_FROM_URL` | 8254–8256 |  |
| `urlHash` | 8257–8297 |  |
| `shareLink` | 8298–8306 | Absolute on purpose: the full build carries <base href="../">, and a |
| `copyShareLink` | 8307–8318 | With no clipboard (an insecure origin, a denied permission) the link goes |
| `offered` | 8319–8325 | On screen, ignoring the Options fold: a folded panel on a phone hides |
| `applyUrlState` | 8326–8398 |  |
| `restoreFromHash` | 8399–8417 | Once, at the end of boot, after every build and data gate has run. The |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 8418–9065 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (1117 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 130 | the Lab: a container for unfinished lenses |
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
| `esc` | 10 | money view (default): the classic metric prisms |
| `ratioDenom` | 9 | services lens views (SPEC_services.md display architecture) |
| `ratioScale` | 9 | geographic reference layers (all views) |
| `deviationStats` | 9 | the same doubt, at 100 m |

**Section self-containment** — share of each section's outgoing edges that stay inside it. Low means a module cut on this banner would mostly import its neighbours.

| section | edges | self-contained |
|---|---|---|
| the Lab: a container for unfinished lenses | 127 | 63% |
| tunables | 16 | 56% |
| Infill lens (SPEC_development.md Lens B) | 27 | 52% |
| uses view (use-mix, 2026-07-03) | 4 | 50% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| base map (no basemap tiles for v1 — just a dark backdrop) | 5 | 40% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 10 | 40% |
| neighbourhood search | 11 | 36% |
| geographic reference layers (all views) | 100 | 35% |
| loading overlay | 57 | 33% |
| deviation lens: revenue per developed acre against peer average | 6 | 33% |
| Development history: new supply per year | 114 | 31% |
| Money's revenue panel: where a hood's levy comes from | 35 | 29% |
| two tiers, answering two different questions | 30 | 27% |
| the same doubt, at 100 m | 70 | 21% |
| shareable URL: the hash names the view on screen | 24 | 21% |
| control appliers + the view/legend dispatchers | 232 | 20% |
| services lens views (SPEC_services.md display architecture) | 5 | 20% |
| how-to-read guide | 117 | 9% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 13 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 18 | 0% |
| the institutional uncertainty band | 3 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 4 | 0% |
| boot | 73 | 0% |

## Element ids (149) — the control surface

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
| `#title-p` | 87 |
| `#search` | 98 |
| `#search-btn` | 99 |
| `#search-box` | 102 |
| `#search-input` | 103 |
| `#search-close` | 107 |
| `#search-list` | 109 |
| `#guide-btn` | 117 |
| `#guide` | 119 |
| `#guide-close` | 120 |
| `#guide-ask` | 121 |
| `#guide-show` | 122 |
| `#guide-body` | 125 |
| `#temporal` | 144 |
| `#temporal-close` | 145 |
| `#temporal-name` | 146 |
| `#temporal-body` | 153 |
| `#temporal-chart` | 154 |
| `#temporal-read` | 155 |
| `#temporal-note` | 156 |
| `#temporal-hint` | 160 |
| `#millrates` | 176 |
| `#mill-head` | 177 |
| `#mill-rows` | 178 |
| `#mill-note` | 179 |
| `#budget` | 193 |
| `#budget-close` | 200 |
| `#budget-head` | 201 |
| `#budget-body` | 206 |
| `#budget-rows` | 207 |
| `#budget-other-hd` | 208 |
| `#budget-other` | 209 |
| `#budget-note` | 210 |
| `#peek` | 225 |
| `#peek-name` | 226 |
| `#peek-read` | 227 |
| `#peek-go` | 228 |
| `#controls` | 231 |
| `#toggle` | 244 |
| `#metric-row` | 245 |
| `#revcut` | 249 |
| `#moneymode` | 254 |
| `#views` | 260 |
| `#optpanel` | 274 |
| `#opt-fold` | 275 |
| `#opt-caret` | 275 |
| `#opt-body` | 276 |
| `#layers` | 277 |
| `#chgwindow-hd` | 278 |
| `#chgwindow` | 279 |
| `#labpick-hd` | 288 |
| `#labpick` | 289 |
| `#labcut-hd` | 290 |
| `#labcut` | 291 |
| `#moneydetail-hd` | 296 |
| `#moneydetail` | 297 |
| `#amenity-hd` | 322 |
| `#amenity` | 323 |
| `#amenity-lrt-row` | 324 |
| `#amenity-lrt-on` | 325 |
| `#amenity-school-row` | 327 |
| `#amenity-school-on` | 328 |
| `#uses-prisms-hd` | 331 |
| `#uses-prisms` | 332 |
| `#uses-prisms-on` | 334 |
| `#devmode-hd` | 337 |
| `#devmode` | 338 |
| `#devmetric-hd` | 342 |
| `#devmetric` | 343 |
| `#devwindow-hd` | 348 |
| `#devwindow` | 349 |
| `#devdetail-hd` | 354 |
| `#devdetail` | 355 |
| `#prism-hd` | 359 |
| `#prism-row` | 360 |
| `#prism-opacity` | 362 |
| `#prism-opacity-val` | 363 |
| `#services-hd` | 365 |
| `#services` | 366 |
| `#denom-hd` | 465 |
| `#denom` | 466 |
| `#ratio-denom-hd` | 470 |
| `#ratio-denom` | 471 |
| `#hoodmode` | 481 |
| `#hoodmode-btn` | 482 |
| `#coloradj` | 494 |
| `#coloradj-btn` | 495 |
| `#budget-pod` | 502 |
| `#budget-btn` | 503 |
| `#share` | 510 |
| `#share-btn` | 511 |
| `#a11y` | 514 |
| `#a11y-btn` | 515 |
| `#a11y-menu` | 516 |
| `#theme` | 518 |
| `#palette` | 523 |
| `#labels-on` | 530 |
| `#reference-on` | 538 |
| `#about` | 543 |
| `#about-btn` | 544 |
| `#about-menu` | 545 |
| `#about-src-roads` | 557 |
| `#about-src-services` | 558 |
| `#about-vintage` | 591 |
| `#about-build` | 595 |
| `#about-lot-acres` | 610 |
| `#about-modelled-roads` | 621 |
| `#about-modelled` | 643 |
| `#about-budget` | 653 |
| `#about-budget-lead` | 655 |
| `#about-budget-rows` | 656 |
| `#about-budget-note` | 657 |
| `#about-split` | 662 |
| `#about-split-lead` | 664 |
| `#about-split-class` | 665 |
| `#about-split-zone` | 667 |
| `#about-split-note` | 668 |
| `#about-updated` | 680 |
| `#botleft` | 684 |
| `#compass` | 685 |
| `#rot-ccw` | 686 |
| `#tonorth` | 693 |
| `#needle` | 695 |
| `#rot-cw` | 700 |
| `#viewbtns` | 708 |
| `#recenter` | 710 |
| `#center2d` | 711 |
| `#legend` | 713 |
| `#legend-label` | 714 |
| `#legend-min` | 716 |
| `#legend-max` | 716 |
| `#legend-cats` | 718 |
| `#revmix` | 5782 |
| `#svccost` | 5888 |
