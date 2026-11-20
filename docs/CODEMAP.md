# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~9,063-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (330 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `THEMED` | 759–761 | Colours that depend on the backdrop, one value per theme (docs/UI.md → |
| `themed` | 762–766 | Throws on a missing or mis-sized light value: deck draws `undefined` |
| `tc` | 767–772 |  |
| `CENTER` | 773–777 |  |
| `HOME` | 778–778 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 779–792 |  |
| `WINDOWS` | 793–818 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 819–828 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 829–833 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 834–909 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 910–912 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 913–914 |  |
| `METRICS` | 915–1036 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `RATIO_DENOMS` | 1037–1070 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 1071–1071 |  |
| `ratioOf` | 1072–1072 |  |
| `ratioKept` | 1073–1094 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 1095–1107 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 1108–1135 |  |
| `dominantUse` | 1136–1177 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1178–1328 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1329–1424 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1425–1429 | the Lab: a container for unfinished lenses |
| `inLab` | 1430–1431 |  |
| `DEVIATION_TITLES` | 1432–1436 |  |
| `deviationTitle` | 1437–1442 |  |
| `deviationKind` | 1443–1443 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1444–1451 |  |
| `changeBlurb` | 1452–1469 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1470–1482 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1483–1499 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1500–1508 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1509–1517 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1518–1523 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1524–1530 |  |
| `infillAmenityBlurb` | 1531–1544 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1545–1556 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1557–1562 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1563–1624 |  |
| `setBlurb` | 1625–1639 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1640–1655 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1656–1673 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1674–1680 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1681–1694 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1695–1695 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1696–1710 |  |
| `fmtMB` | 1711–1721 |  |
| `showGridBusy` | 1722–1744 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1745–1761 |  |
| `loadGridData` | 1762–1818 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1819–1872 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1873–1897 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1898–1930 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1931–1931 |  |
| `gridFetches` | 1932–1958 |  |
| `RAMPS` | 1959–2011 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `THEME_RAMPS` | 2012–2046 | The ramps for a light backdrop, per theme (docs/UI.md → Light mode, phase |
| `activeRamp` | 2047–2060 | The ramp actually drawn: the palette choice under the current theme. |
| `rampSetAside` | 2061–2073 | The set-aside colour beside a RAMP-coloured surface. Only where the |
| `lotKey` | 2074–2074 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 2075–2081 |  |
| `AMENITY_BANDS` | 2082–2083 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 2084–2086 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 2087–2092 | Whether any band is actually filtering right now. |
| `amenityInBand` | 2093–2107 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 2108–2113 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 2114–2132 |  |
| `gridScale` | 2133–2153 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 2154–2160 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 2161–2172 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2173–2175 |  |
| `quantile` | 2176–2190 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2191–2225 |  |
| `moneyBlurb` | 2226–2237 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2238–2250 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2251–2304 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `GRID_INK` | 2305–2305 |  |
| `gridName` | 2306–2319 |  |
| `paintBackdrop` | 2320–2357 | The backdrop's three MapLibre layers, after a theme or ramp change. |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2358–2358 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2359–2383 |  |
| `failLoading` | 2384–2397 |  |
| `hideLoading` | 2398–2453 |  |
| `topRings` | 2454–2470 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2471–2496 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2497–2497 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2498–2510 |  |
| `svcT` | 2511–2519 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2520–2533 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2534–2534 |  |
| `fmtFire` | 2535–2536 |  |
| `fmtTransit` | 2537–2538 |  |
| `fmtBike` | 2539–2551 |  |
| `fmtRoadM` | 2552–2565 |  |
| `fmtResShare` | 2566–2568 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2569–2574 |  |
| `fmtRoadsCost` | 2575–2579 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2580–2581 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2582–2583 |  |
| `fmtBikeCost` | 2584–2595 |  |
| `servicePlaneLayer` | 2596–2628 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2629–2638 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2639–2644 |  |
| `DEV_IND_TOTAL` | 2645–2647 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2648–2653 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2654–2658 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2659–2664 |  |
| `devGridOfferable` | 2665–2666 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2667–2667 |  |
| `devCol` | 2668–2668 |  |
| `_devScale` | 2669–2669 |  |
| `devScale` | 2670–2676 |  |
| `devT` | 2677–2680 |  |
| `developmentPlaneLayer` | 2681–2697 |  |
| `fmtDev` | 2698–2713 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2714–2719 |  |
| `DEV_GRID_IND_N` | 2720–2720 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2721–2723 |  |
| `devGridScale` | 2724–2750 |  |
| `devGridLayer` | 2751–2799 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2800–2801 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2802–2809 |  |
| `_infillStats` | 2810–2810 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2811–2828 |  |
| `_infillRaw` | 2829–2831 |  |
| `infillScore` | 2832–2847 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2848–2849 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2850–2870 |  |
| `infillColorAt` | 2871–2875 |  |
| `infillPlaneLayer` | 2876–2897 |  |
| `fmtFar` | 2898–2908 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `amenityHighlightGridLayer` | 2909–2963 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2964–2971 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2972–2986 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2987–3007 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 3008–3008 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 3009–3023 |  |
| `chgT` | 3024–3033 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 3034–3064 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 3065–3153 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 3154–3161 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 3162–3162 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 3163–3170 |  |
| `deviationRate` | 3171–3223 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `EXEMPT_COL` | 3224–3228 | ⚠️ THE SHARE OF THE CUT BEING DRAWN, not of the total levy |
| `exemptFrac` | 3229–3231 |  |
| `exemptCutWord` | 3232–3263 | COPY_DECISIONS F6 (option A): the caveat names the cut its share is of. |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3264–3270 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3271–3282 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3283–3286 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3287–3291 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3292–3302 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3303–3318 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3319–3350 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3351–3428 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `isBandLayer` | 3429–3433 |  |
| `bandHover` | 3434–3442 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3443–3546 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `GRID_EXEMPT_COL` | 3547–3551 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `gridExemptCol` | 3552–3553 |  |
| `glassInstCells` | 3554–3561 |  |
| `glassInstCount` | 3562–3563 |  |
| `glassInstBandLayers` | 3564–3604 |  |
| `ratioInstBandLayers` | 3605–3632 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3633–3645 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3646–3647 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3648–3649 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3650–3650 |  |
| `deviationStats` | 3651–3695 |  |
| `deviationOf` | 3696–3697 |  |
| `deviationT` | 3698–3708 |  |
| `fmtDeviation` | 3709–3730 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3731–3774 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3775–3861 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3862–3886 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `fireStationsLayer` | 3887–3907 |  |
| `ensureFireStations` | 3908–3924 |  |
| `transitStationsLayer` | 3925–3942 |  |
| `ensureTransitStations` | 3943–3959 |  |
| `lrtLinesLayer` | 3960–3976 |  |
| `ensureLrtLines` | 3977–3994 |  |
| `bikeLinesLayer` | 3995–4011 |  |
| `ensureBikeLines` | 4012–4098 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `referenceSplit` | 4099–4126 |  |
| `referenceUnderLayers` | 4127–4161 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 4162–4178 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 4179–4198 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 4199–4213 |  |
| `servicesBlurb` | 4214–4225 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 4226–4262 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4263–4273 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4274–4325 |  |
| `REF_TIERS` | 4326–4347 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4348–4359 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `placeAnchors` | 4360–4384 |  |
| `labelPool` | 4385–4392 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4393–4446 |  |
| `CHROME_IDS` | 4447–4451 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4452–4470 |  |
| `visibleLabels` | 4471–4540 |  |
| `labelLayer` | 4541–4596 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `withSelectedHood` | 4597–4637 |  |
| `_ratioScales` | 4638–4638 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4639–4654 |  |
| `ratioT` | 4655–4677 |  |
| `zMatrix` | 4678–4682 |  |
| `buildLayers` | 4683–4707 |  |
| `flattenDuringEase` | 4708–4732 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4733–5047 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 5048–5077 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 5078–5087 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 5088–5090 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 5091–5122 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 5123–5129 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 5130–5137 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 5138–5142 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 5143–5153 |  |
| `revenueLens` | 5154–5155 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 5156–5188 |  |
| `SVC_COST_BASES` | 5189–5206 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 5207–5215 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 5216–5225 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 5226–5228 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 5229–5235 |  |
| `svcRank` | 5236–5240 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 5241–5247 |  |
| `svcDriverReading` | 5248–5268 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 5269–5269 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 5270–5273 |  |
| `servicePanelFor` | 5274–5278 |  |
| `ratioPanelFor` | 5279–5302 | Ratio carries the cost-as-a-share-of-tax panel that Services had until |
| `hoodPanelLens` | 5303–5307 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 5308–5325 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 5326–5357 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5358–5363 |  |
| `sparklineSvg` | 5364–5379 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5380–5439 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5440–5445 | Development history: new supply per year |
| `devHistKey` | 5446–5455 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5456–5460 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5461–5461 |  |
| `devHistVerb` | 5462–5467 |  |
| `devHistoryFor` | 5468–5506 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5507–5526 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5527–5546 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5547–5582 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5583–5585 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5586–5649 |  |
| `syncTemporalPos` | 5650–5704 |  |
| `syncControlsTop` | 5705–5722 |  |
| `openTemporal` | 5723–5760 |  |
| `renderRevenueMix` | 5761–5835 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderRatioCost` | 5836–5920 |  |
| `renderServiceCost` | 5921–5978 | The Services panel: what each cost IS for this hood, in dollars, and where |
| `fmtSvcRatio` | 5979–5982 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5983–6033 |  |
| `syncPinnedPanel` | 6034–6067 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 6068–6083 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 6084–6101 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 6102–6149 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 6150–6155 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 6156–6203 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 6204–6220 |  |
| `temporalClick` | 6221–6275 | Click a hood to pin its history; click the pinned one again to unpin. |

### neighbourhood search

| symbol | lines | what it does |
|---|---|---|
| `searchNorm` | 6276–6283 | neighbourhood search |
| `searchMatches` | 6284–6298 | Ranked: the name starts with the query, then a later WORD does (so |
| `renderSearchList` | 6299–6327 |  |
| `openSearch` | 6328–6340 |  |
| `closeSearch` | 6341–6359 |  |

### how-to-read guide

| symbol | lines | what it does |
|---|---|---|
| `openGuide` | 6360–6372 |  |
| `closeGuide` | 6373–6380 |  |
| `maybeAutoGuide` | 6381–6397 |  |
| `flyToHood` | 6398–6417 | Keep the current tilt and rotation, so the camera moves TO the hood |
| `pickSearch` | 6418–6436 | A pick reads exactly like tapping or clicking the hood (temporalClick |
| `primaryRow` | 6437–6505 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 6506–6885 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6886–6975 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6976–6976 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6977–6995 |  |
| `syncMetricButtons` | 6996–7019 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 7020–7026 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 7027–7040 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 7041–7073 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |
| `SPLIT_CLASS_LABELS` | 7074–7078 | The Data & Methods pod's citywide tax split (2026-11-17). Two cuts of one |
| `renderCitywideLevy` | 7079–7128 |  |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 7129–7171 |  |
| `toggleBudgetPanel` | 7172–7197 |  |
| `syncMillRates` | 7198–7231 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 7232–7252 |  |
| `applyColorAdjust` | 7253–7273 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 7274–7286 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 7287–7301 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 7302–7319 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 7320–7336 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 7337–7358 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 7359–7375 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 7376–7615 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 7616–7632 | Legend rows for the uses view: the categories actually on screen |
| `applyTheme` | 7633–7655 |  |
| `syncThemeChrome` | 7656–7666 | The theme's wording and buttons outside the map. Also run once at boot, |
| `applyPalette` | 7667–7682 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 7683–7691 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 7692–7702 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 7703–7714 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7715–7727 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7728–7748 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7749–7796 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7797–7802 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7803–7824 |  |
| `applyMoneyDetail` | 7825–7849 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7850–7861 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7862–7869 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7870–7888 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7889–7899 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7900–7907 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7908–7924 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7925–7938 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7939–7949 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7950–8194 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 8195–8204 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 8205–8218 |  |
| `applySvcDriver` | 8219–8251 |  |

### shareable URL: the hash names the view on screen

| symbol | lines | what it does |
|---|---|---|
| `METRIC_FROM_URL` | 8252–8254 |  |
| `urlHash` | 8255–8295 |  |
| `shareLink` | 8296–8304 | Absolute on purpose: the full build carries <base href="../">, and a |
| `copyShareLink` | 8305–8316 | With no clipboard (an insecure origin, a denied permission) the link goes |
| `offered` | 8317–8323 | On screen, ignoring the Options fold: a folded panel on a phone hides |
| `applyUrlState` | 8324–8396 |  |
| `restoreFromHash` | 8397–8415 | Once, at the end of boot, after every build and data gate has run. The |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 8416–9063 | Everything that needs the map surface: fetch the data, mount the deck.gl |

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
| `#about-lot-acres` | 608 |
| `#about-modelled-roads` | 619 |
| `#about-modelled` | 641 |
| `#about-budget` | 651 |
| `#about-budget-lead` | 653 |
| `#about-budget-rows` | 654 |
| `#about-budget-note` | 655 |
| `#about-split` | 660 |
| `#about-split-lead` | 662 |
| `#about-split-class` | 663 |
| `#about-split-zone` | 665 |
| `#about-split-note` | 666 |
| `#about-updated` | 678 |
| `#botleft` | 682 |
| `#compass` | 683 |
| `#rot-ccw` | 684 |
| `#tonorth` | 691 |
| `#needle` | 693 |
| `#rot-cw` | 698 |
| `#viewbtns` | 706 |
| `#recenter` | 708 |
| `#center2d` | 709 |
| `#legend` | 711 |
| `#legend-label` | 712 |
| `#legend-min` | 714 |
| `#legend-max` | 714 |
| `#legend-cats` | 716 |
| `#revmix` | 5780 |
| `#svccost` | 5886 |
