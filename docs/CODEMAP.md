# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~9,061-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

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
| `deviationKind` | 1443–1445 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1446–1453 |  |
| `changeBlurb` | 1454–1471 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1472–1484 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1485–1497 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1498–1506 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1507–1515 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1516–1521 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1522–1529 |  |
| `infillAmenityBlurb` | 1530–1543 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1544–1555 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1556–1561 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1562–1623 |  |
| `setBlurb` | 1624–1638 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1639–1654 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1655–1672 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1673–1679 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1680–1693 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1694–1694 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1695–1709 |  |
| `fmtMB` | 1710–1720 |  |
| `showGridBusy` | 1721–1743 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1744–1760 |  |
| `loadGridData` | 1761–1817 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1818–1871 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1872–1896 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1897–1929 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1930–1930 |  |
| `gridFetches` | 1931–1957 |  |
| `RAMPS` | 1958–2010 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `THEME_RAMPS` | 2011–2045 | The ramps for a light backdrop, per theme (docs/UI.md → Light mode, phase |
| `activeRamp` | 2046–2059 | The ramp actually drawn: the palette choice under the current theme. |
| `rampSetAside` | 2060–2072 | The set-aside colour beside a RAMP-coloured surface. Only where the |
| `lotKey` | 2073–2073 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 2074–2080 |  |
| `AMENITY_BANDS` | 2081–2082 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 2083–2085 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 2086–2091 | Whether any band is actually filtering right now. |
| `amenityInBand` | 2092–2106 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 2107–2112 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 2113–2131 |  |
| `gridScale` | 2132–2152 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 2153–2159 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 2160–2171 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2172–2174 |  |
| `quantile` | 2175–2189 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2190–2224 |  |
| `moneyBlurb` | 2225–2236 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2237–2249 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2250–2303 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `GRID_INK` | 2304–2304 |  |
| `gridName` | 2305–2318 |  |
| `paintBackdrop` | 2319–2356 | The backdrop's three MapLibre layers, after a theme or ramp change. |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2357–2357 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2358–2382 |  |
| `failLoading` | 2383–2396 |  |
| `hideLoading` | 2397–2452 |  |
| `topRings` | 2453–2469 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2470–2495 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2496–2496 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2497–2509 |  |
| `svcT` | 2510–2518 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2519–2532 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2533–2533 |  |
| `fmtFire` | 2534–2535 |  |
| `fmtTransit` | 2536–2537 |  |
| `fmtBike` | 2538–2550 |  |
| `fmtRoadM` | 2551–2564 |  |
| `fmtResShare` | 2565–2567 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2568–2573 |  |
| `fmtRoadsCost` | 2574–2578 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2579–2580 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2581–2582 |  |
| `fmtBikeCost` | 2583–2594 |  |
| `servicePlaneLayer` | 2595–2627 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2628–2637 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2638–2643 |  |
| `DEV_IND_TOTAL` | 2644–2646 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2647–2652 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2653–2657 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2658–2663 |  |
| `devGridOfferable` | 2664–2665 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2666–2666 |  |
| `devCol` | 2667–2667 |  |
| `_devScale` | 2668–2668 |  |
| `devScale` | 2669–2675 |  |
| `devT` | 2676–2679 |  |
| `developmentPlaneLayer` | 2680–2696 |  |
| `fmtDev` | 2697–2712 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2713–2718 |  |
| `DEV_GRID_IND_N` | 2719–2719 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2720–2722 |  |
| `devGridScale` | 2723–2749 |  |
| `devGridLayer` | 2750–2798 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2799–2800 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2801–2808 |  |
| `_infillStats` | 2809–2809 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2810–2827 |  |
| `_infillRaw` | 2828–2830 |  |
| `infillScore` | 2831–2846 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2847–2848 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2849–2869 |  |
| `infillColorAt` | 2870–2874 |  |
| `infillPlaneLayer` | 2875–2896 |  |
| `fmtFar` | 2897–2907 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `amenityHighlightGridLayer` | 2908–2962 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2963–2970 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2971–2985 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2986–3006 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 3007–3007 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 3008–3022 |  |
| `chgT` | 3023–3032 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 3033–3063 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 3064–3152 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 3153–3160 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 3161–3161 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 3162–3169 |  |
| `deviationRate` | 3170–3222 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `EXEMPT_COL` | 3223–3227 | ⚠️ THE SHARE OF THE CUT BEING DRAWN, not of the total levy |
| `exemptFrac` | 3228–3229 |  |
| `exemptCutWord` | 3230–3261 | COPY_DECISIONS F6 (option A): the caveat names the cut its share is of. |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3262–3268 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3269–3280 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3281–3284 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3285–3289 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3290–3300 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3301–3316 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3317–3348 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3349–3426 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `isBandLayer` | 3427–3431 |  |
| `bandHover` | 3432–3440 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3441–3544 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `GRID_EXEMPT_COL` | 3545–3549 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `gridExemptCol` | 3550–3551 |  |
| `glassInstCells` | 3552–3559 |  |
| `glassInstCount` | 3560–3561 |  |
| `glassInstBandLayers` | 3562–3602 |  |
| `ratioInstBandLayers` | 3603–3630 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3631–3643 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3644–3645 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3646–3647 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3648–3648 |  |
| `deviationStats` | 3649–3693 |  |
| `deviationOf` | 3694–3695 |  |
| `deviationT` | 3696–3706 |  |
| `fmtDeviation` | 3707–3728 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3729–3772 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3773–3859 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3860–3884 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `fireStationsLayer` | 3885–3905 |  |
| `ensureFireStations` | 3906–3922 |  |
| `transitStationsLayer` | 3923–3940 |  |
| `ensureTransitStations` | 3941–3957 |  |
| `lrtLinesLayer` | 3958–3974 |  |
| `ensureLrtLines` | 3975–3992 |  |
| `bikeLinesLayer` | 3993–4009 |  |
| `ensureBikeLines` | 4010–4096 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `referenceSplit` | 4097–4124 |  |
| `referenceUnderLayers` | 4125–4159 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 4160–4176 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 4177–4196 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 4197–4211 |  |
| `servicesBlurb` | 4212–4223 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 4224–4260 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4261–4271 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4272–4323 |  |
| `REF_TIERS` | 4324–4345 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4346–4357 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `placeAnchors` | 4358–4382 |  |
| `labelPool` | 4383–4390 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4391–4444 |  |
| `CHROME_IDS` | 4445–4449 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4450–4468 |  |
| `visibleLabels` | 4469–4538 |  |
| `labelLayer` | 4539–4594 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `withSelectedHood` | 4595–4635 |  |
| `_ratioScales` | 4636–4636 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4637–4652 |  |
| `ratioT` | 4653–4675 |  |
| `zMatrix` | 4676–4680 |  |
| `buildLayers` | 4681–4705 |  |
| `flattenDuringEase` | 4706–4730 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4731–5045 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 5046–5075 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 5076–5085 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 5086–5088 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 5089–5120 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 5121–5127 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 5128–5135 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 5136–5140 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 5141–5151 |  |
| `revenueLens` | 5152–5153 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 5154–5186 |  |
| `SVC_COST_BASES` | 5187–5204 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 5205–5213 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 5214–5223 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 5224–5226 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 5227–5233 |  |
| `svcRank` | 5234–5238 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 5239–5245 |  |
| `svcDriverReading` | 5246–5266 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 5267–5267 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 5268–5271 |  |
| `servicePanelFor` | 5272–5276 |  |
| `ratioPanelFor` | 5277–5300 | Ratio carries the cost-as-a-share-of-tax panel that Services had until |
| `hoodPanelLens` | 5301–5305 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 5306–5323 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 5324–5355 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5356–5361 |  |
| `sparklineSvg` | 5362–5377 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5378–5437 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5438–5443 | Development history: new supply per year |
| `devHistKey` | 5444–5453 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5454–5458 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5459–5459 |  |
| `devHistVerb` | 5460–5465 |  |
| `devHistoryFor` | 5466–5504 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5505–5524 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5525–5544 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5545–5580 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5581–5583 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5584–5647 |  |
| `syncTemporalPos` | 5648–5702 |  |
| `syncControlsTop` | 5703–5720 |  |
| `openTemporal` | 5721–5758 |  |
| `renderRevenueMix` | 5759–5833 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderRatioCost` | 5834–5918 |  |
| `renderServiceCost` | 5919–5976 | The Services panel: what each cost IS for this hood, in dollars, and where |
| `fmtSvcRatio` | 5977–5980 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5981–6031 |  |
| `syncPinnedPanel` | 6032–6065 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 6066–6081 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 6082–6099 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 6100–6147 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 6148–6153 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 6154–6201 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 6202–6218 |  |
| `temporalClick` | 6219–6273 | Click a hood to pin its history; click the pinned one again to unpin. |

### neighbourhood search

| symbol | lines | what it does |
|---|---|---|
| `searchNorm` | 6274–6281 | neighbourhood search |
| `searchMatches` | 6282–6296 | Ranked: the name starts with the query, then a later WORD does (so |
| `renderSearchList` | 6297–6325 |  |
| `openSearch` | 6326–6338 |  |
| `closeSearch` | 6339–6357 |  |

### how-to-read guide

| symbol | lines | what it does |
|---|---|---|
| `openGuide` | 6358–6370 |  |
| `closeGuide` | 6371–6378 |  |
| `maybeAutoGuide` | 6379–6395 |  |
| `flyToHood` | 6396–6415 | Keep the current tilt and rotation, so the camera moves TO the hood |
| `pickSearch` | 6416–6434 | A pick reads exactly like tapping or clicking the hood (temporalClick |
| `primaryRow` | 6435–6503 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 6504–6883 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6884–6973 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6974–6974 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6975–6993 |  |
| `syncMetricButtons` | 6994–7017 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 7018–7024 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 7025–7038 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 7039–7071 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |
| `SPLIT_CLASS_LABELS` | 7072–7076 | The Data & Methods pod's citywide tax split (2026-11-17). Two cuts of one |
| `renderCitywideLevy` | 7077–7126 |  |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 7127–7169 |  |
| `toggleBudgetPanel` | 7170–7195 |  |
| `syncMillRates` | 7196–7229 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 7230–7250 |  |
| `applyColorAdjust` | 7251–7271 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 7272–7284 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 7285–7299 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 7300–7317 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 7318–7334 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 7335–7356 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 7357–7373 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 7374–7613 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 7614–7630 | Legend rows for the uses view: the categories actually on screen |
| `applyTheme` | 7631–7653 |  |
| `syncThemeChrome` | 7654–7664 | The theme's wording and buttons outside the map. Also run once at boot, |
| `applyPalette` | 7665–7680 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 7681–7689 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 7690–7700 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 7701–7712 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7713–7725 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7726–7746 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7747–7794 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7795–7800 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7801–7822 |  |
| `applyMoneyDetail` | 7823–7847 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7848–7859 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7860–7867 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7868–7886 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7887–7897 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7898–7905 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7906–7922 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7923–7936 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7937–7947 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7948–8192 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 8193–8202 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 8203–8216 |  |
| `applySvcDriver` | 8217–8249 |  |

### shareable URL: the hash names the view on screen

| symbol | lines | what it does |
|---|---|---|
| `METRIC_FROM_URL` | 8250–8252 |  |
| `urlHash` | 8253–8293 |  |
| `shareLink` | 8294–8302 | Absolute on purpose: the full build carries <base href="../">, and a |
| `copyShareLink` | 8303–8314 | With no clipboard (an insecure origin, a denied permission) the link goes |
| `offered` | 8315–8321 | On screen, ignoring the Options fold: a folded panel on a phone hides |
| `applyUrlState` | 8322–8394 |  |
| `restoreFromHash` | 8395–8413 | Once, at the end of boot, after every build and data gate has run. The |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 8414–9061 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (1115 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 131 | the Lab: a container for unfinished lenses |
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
| the Lab: a container for unfinished lenses | 127 | 64% |
| tunables | 16 | 56% |
| Infill lens (SPEC_development.md Lens B) | 27 | 52% |
| uses view (use-mix, 2026-07-03) | 4 | 50% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| base map (no basemap tiles for v1 — just a dark backdrop) | 5 | 40% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 10 | 40% |
| deviation lens: revenue per developed acre against peer average | 5 | 40% |
| neighbourhood search | 11 | 36% |
| geographic reference layers (all views) | 100 | 35% |
| loading overlay | 57 | 33% |
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
| the institutional uncertainty band | 2 | 0% |
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
| `#revmix` | 5778 |
| `#svccost` | 5884 |
