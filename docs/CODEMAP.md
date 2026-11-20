# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~9,060-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

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
| `glassInstBlurb` | 1483–1495 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1496–1504 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1505–1513 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1514–1519 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1520–1527 |  |
| `infillAmenityBlurb` | 1528–1541 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1542–1553 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1554–1559 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1560–1621 |  |
| `setBlurb` | 1622–1636 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1637–1652 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1653–1670 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1671–1677 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1678–1691 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1692–1692 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1693–1707 |  |
| `fmtMB` | 1708–1718 |  |
| `showGridBusy` | 1719–1741 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1742–1758 |  |
| `loadGridData` | 1759–1815 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1816–1869 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1870–1894 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1895–1927 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1928–1928 |  |
| `gridFetches` | 1929–1955 |  |
| `RAMPS` | 1956–2008 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `THEME_RAMPS` | 2009–2043 | The ramps for a light backdrop, per theme (docs/UI.md → Light mode, phase |
| `activeRamp` | 2044–2057 | The ramp actually drawn: the palette choice under the current theme. |
| `rampSetAside` | 2058–2070 | The set-aside colour beside a RAMP-coloured surface. Only where the |
| `lotKey` | 2071–2071 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 2072–2078 |  |
| `AMENITY_BANDS` | 2079–2080 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 2081–2083 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 2084–2089 | Whether any band is actually filtering right now. |
| `amenityInBand` | 2090–2104 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 2105–2110 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 2111–2129 |  |
| `gridScale` | 2130–2150 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 2151–2157 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 2158–2169 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2170–2172 |  |
| `quantile` | 2173–2187 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2188–2222 |  |
| `moneyBlurb` | 2223–2234 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2235–2247 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2248–2301 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `GRID_INK` | 2302–2302 |  |
| `gridName` | 2303–2316 |  |
| `paintBackdrop` | 2317–2354 | The backdrop's three MapLibre layers, after a theme or ramp change. |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2355–2355 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2356–2380 |  |
| `failLoading` | 2381–2394 |  |
| `hideLoading` | 2395–2450 |  |
| `topRings` | 2451–2467 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2468–2493 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2494–2494 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2495–2507 |  |
| `svcT` | 2508–2516 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2517–2530 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2531–2531 |  |
| `fmtFire` | 2532–2533 |  |
| `fmtTransit` | 2534–2535 |  |
| `fmtBike` | 2536–2548 |  |
| `fmtRoadM` | 2549–2562 |  |
| `fmtResShare` | 2563–2565 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2566–2571 |  |
| `fmtRoadsCost` | 2572–2576 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2577–2578 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2579–2580 |  |
| `fmtBikeCost` | 2581–2592 |  |
| `servicePlaneLayer` | 2593–2625 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2626–2635 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2636–2641 |  |
| `DEV_IND_TOTAL` | 2642–2644 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2645–2650 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2651–2655 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2656–2661 |  |
| `devGridOfferable` | 2662–2663 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2664–2664 |  |
| `devCol` | 2665–2665 |  |
| `_devScale` | 2666–2666 |  |
| `devScale` | 2667–2673 |  |
| `devT` | 2674–2677 |  |
| `developmentPlaneLayer` | 2678–2694 |  |
| `fmtDev` | 2695–2710 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2711–2716 |  |
| `DEV_GRID_IND_N` | 2717–2717 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2718–2720 |  |
| `devGridScale` | 2721–2747 |  |
| `devGridLayer` | 2748–2796 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2797–2798 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2799–2806 |  |
| `_infillStats` | 2807–2807 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2808–2825 |  |
| `_infillRaw` | 2826–2828 |  |
| `infillScore` | 2829–2844 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2845–2846 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2847–2867 |  |
| `infillColorAt` | 2868–2872 |  |
| `infillPlaneLayer` | 2873–2894 |  |
| `fmtFar` | 2895–2905 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `amenityHighlightGridLayer` | 2906–2960 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2961–2968 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2969–2983 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2984–3004 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 3005–3005 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 3006–3020 |  |
| `chgT` | 3021–3030 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 3031–3061 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 3062–3150 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 3151–3158 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 3159–3159 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 3160–3167 |  |
| `deviationRate` | 3168–3220 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `EXEMPT_COL` | 3221–3225 | ⚠️ THE SHARE OF THE CUT BEING DRAWN, not of the total levy |
| `exemptFrac` | 3226–3228 |  |
| `exemptCutWord` | 3229–3260 | COPY_DECISIONS F6 (option A): the caveat names the cut its share is of. |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3261–3267 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3268–3279 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3280–3283 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3284–3288 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3289–3299 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3300–3315 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3316–3347 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3348–3425 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `isBandLayer` | 3426–3430 |  |
| `bandHover` | 3431–3439 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3440–3543 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `GRID_EXEMPT_COL` | 3544–3548 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `gridExemptCol` | 3549–3550 |  |
| `glassInstCells` | 3551–3558 |  |
| `glassInstCount` | 3559–3560 |  |
| `glassInstBandLayers` | 3561–3601 |  |
| `ratioInstBandLayers` | 3602–3629 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3630–3642 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3643–3644 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3645–3646 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3647–3647 |  |
| `deviationStats` | 3648–3692 |  |
| `deviationOf` | 3693–3694 |  |
| `deviationT` | 3695–3705 |  |
| `fmtDeviation` | 3706–3727 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3728–3771 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3772–3858 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3859–3883 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `fireStationsLayer` | 3884–3904 |  |
| `ensureFireStations` | 3905–3921 |  |
| `transitStationsLayer` | 3922–3939 |  |
| `ensureTransitStations` | 3940–3956 |  |
| `lrtLinesLayer` | 3957–3973 |  |
| `ensureLrtLines` | 3974–3991 |  |
| `bikeLinesLayer` | 3992–4008 |  |
| `ensureBikeLines` | 4009–4095 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `referenceSplit` | 4096–4123 |  |
| `referenceUnderLayers` | 4124–4158 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 4159–4175 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 4176–4195 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 4196–4210 |  |
| `servicesBlurb` | 4211–4222 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 4223–4259 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4260–4270 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4271–4322 |  |
| `REF_TIERS` | 4323–4344 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4345–4356 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `placeAnchors` | 4357–4381 |  |
| `labelPool` | 4382–4389 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4390–4443 |  |
| `CHROME_IDS` | 4444–4448 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4449–4467 |  |
| `visibleLabels` | 4468–4537 |  |
| `labelLayer` | 4538–4593 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `withSelectedHood` | 4594–4634 |  |
| `_ratioScales` | 4635–4635 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4636–4651 |  |
| `ratioT` | 4652–4674 |  |
| `zMatrix` | 4675–4679 |  |
| `buildLayers` | 4680–4704 |  |
| `flattenDuringEase` | 4705–4729 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4730–5044 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 5045–5074 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 5075–5084 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 5085–5087 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 5088–5119 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 5120–5126 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 5127–5134 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 5135–5139 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 5140–5150 |  |
| `revenueLens` | 5151–5152 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 5153–5185 |  |
| `SVC_COST_BASES` | 5186–5203 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 5204–5212 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 5213–5222 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 5223–5225 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 5226–5232 |  |
| `svcRank` | 5233–5237 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 5238–5244 |  |
| `svcDriverReading` | 5245–5265 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 5266–5266 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 5267–5270 |  |
| `servicePanelFor` | 5271–5275 |  |
| `ratioPanelFor` | 5276–5299 | Ratio carries the cost-as-a-share-of-tax panel that Services had until |
| `hoodPanelLens` | 5300–5304 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 5305–5322 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 5323–5354 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5355–5360 |  |
| `sparklineSvg` | 5361–5376 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5377–5436 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5437–5442 | Development history: new supply per year |
| `devHistKey` | 5443–5452 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5453–5457 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5458–5458 |  |
| `devHistVerb` | 5459–5464 |  |
| `devHistoryFor` | 5465–5503 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5504–5523 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5524–5543 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5544–5579 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5580–5582 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5583–5646 |  |
| `syncTemporalPos` | 5647–5701 |  |
| `syncControlsTop` | 5702–5719 |  |
| `openTemporal` | 5720–5757 |  |
| `renderRevenueMix` | 5758–5832 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderRatioCost` | 5833–5917 |  |
| `renderServiceCost` | 5918–5975 | The Services panel: what each cost IS for this hood, in dollars, and where |
| `fmtSvcRatio` | 5976–5979 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5980–6030 |  |
| `syncPinnedPanel` | 6031–6064 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 6065–6080 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 6081–6098 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 6099–6146 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 6147–6152 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 6153–6200 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 6201–6217 |  |
| `temporalClick` | 6218–6272 | Click a hood to pin its history; click the pinned one again to unpin. |

### neighbourhood search

| symbol | lines | what it does |
|---|---|---|
| `searchNorm` | 6273–6280 | neighbourhood search |
| `searchMatches` | 6281–6295 | Ranked: the name starts with the query, then a later WORD does (so |
| `renderSearchList` | 6296–6324 |  |
| `openSearch` | 6325–6337 |  |
| `closeSearch` | 6338–6356 |  |

### how-to-read guide

| symbol | lines | what it does |
|---|---|---|
| `openGuide` | 6357–6369 |  |
| `closeGuide` | 6370–6377 |  |
| `maybeAutoGuide` | 6378–6394 |  |
| `flyToHood` | 6395–6414 | Keep the current tilt and rotation, so the camera moves TO the hood |
| `pickSearch` | 6415–6433 | A pick reads exactly like tapping or clicking the hood (temporalClick |
| `primaryRow` | 6434–6502 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 6503–6882 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6883–6972 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6973–6973 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6974–6992 |  |
| `syncMetricButtons` | 6993–7016 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 7017–7023 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 7024–7037 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 7038–7070 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |
| `SPLIT_CLASS_LABELS` | 7071–7075 | The Data & Methods pod's citywide tax split (2026-11-17). Two cuts of one |
| `renderCitywideLevy` | 7076–7125 |  |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 7126–7168 |  |
| `toggleBudgetPanel` | 7169–7194 |  |
| `syncMillRates` | 7195–7228 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 7229–7249 |  |
| `applyColorAdjust` | 7250–7270 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 7271–7283 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 7284–7298 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 7299–7316 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 7317–7333 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 7334–7355 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 7356–7372 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 7373–7612 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 7613–7629 | Legend rows for the uses view: the categories actually on screen |
| `applyTheme` | 7630–7652 |  |
| `syncThemeChrome` | 7653–7663 | The theme's wording and buttons outside the map. Also run once at boot, |
| `applyPalette` | 7664–7679 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 7680–7688 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 7689–7699 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 7700–7711 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7712–7724 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7725–7745 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7746–7793 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7794–7799 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7800–7821 |  |
| `applyMoneyDetail` | 7822–7846 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7847–7858 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7859–7866 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7867–7885 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7886–7896 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7897–7904 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7905–7921 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7922–7935 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7936–7946 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7947–8191 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 8192–8201 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 8202–8215 |  |
| `applySvcDriver` | 8216–8248 |  |

### shareable URL: the hash names the view on screen

| symbol | lines | what it does |
|---|---|---|
| `METRIC_FROM_URL` | 8249–8251 |  |
| `urlHash` | 8252–8292 |  |
| `shareLink` | 8293–8301 | Absolute on purpose: the full build carries <base href="../">, and a |
| `copyShareLink` | 8302–8313 | With no clipboard (an insecure origin, a denied permission) the link goes |
| `offered` | 8314–8320 | On screen, ignoring the Options fold: a folded panel on a phone hides |
| `applyUrlState` | 8321–8393 |  |
| `restoreFromHash` | 8394–8412 | Once, at the end of boot, after every build and data gate has run. The |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 8413–9060 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (1116 edges)

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
| the Lab: a container for unfinished lenses | 126 | 63% |
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
| `#revmix` | 5777 |
| `#svccost` | 5883 |
