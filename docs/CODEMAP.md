# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,743-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (319 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `THEMED` | 707–707 | Colours that depend on the backdrop, one value per theme (docs/UI.md → |
| `themed` | 708–708 |  |
| `tc` | 709–714 |  |
| `CENTER` | 715–719 |  |
| `HOME` | 720–720 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 721–734 |  |
| `WINDOWS` | 735–760 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 761–770 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 771–775 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 776–851 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 852–854 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 855–856 |  |
| `METRICS` | 857–976 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `RATIO_DENOMS` | 977–1010 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 1011–1011 |  |
| `ratioOf` | 1012–1012 |  |
| `ratioKept` | 1013–1034 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 1035–1047 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 1048–1075 |  |
| `dominantUse` | 1076–1117 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1118–1268 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1269–1364 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1365–1369 | the Lab: a container for unfinished lenses |
| `inLab` | 1370–1371 |  |
| `DEVIATION_TITLES` | 1372–1376 |  |
| `deviationTitle` | 1377–1382 |  |
| `deviationKind` | 1383–1385 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1386–1393 |  |
| `changeBlurb` | 1394–1411 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1412–1424 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1425–1437 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1438–1446 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1447–1455 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1456–1461 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1462–1469 |  |
| `infillAmenityBlurb` | 1470–1483 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1484–1495 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1496–1501 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1502–1560 |  |
| `setBlurb` | 1561–1573 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1574–1589 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1590–1607 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1608–1614 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1615–1628 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1629–1629 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1630–1644 |  |
| `fmtMB` | 1645–1655 |  |
| `showGridBusy` | 1656–1678 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1679–1695 |  |
| `loadGridData` | 1696–1749 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1750–1803 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1804–1828 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1829–1860 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1861–1861 |  |
| `gridFetches` | 1862–1888 |  |
| `RAMPS` | 1889–1941 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `THEME_RAMPS` | 1942–1976 | The ramps for a light backdrop, per theme (docs/UI.md → Light mode, phase |
| `activeRamp` | 1977–1990 | The ramp actually drawn: the palette choice under the current theme. |
| `rampSetAside` | 1991–2003 | The set-aside colour beside a RAMP-coloured surface. Only where the |
| `lotKey` | 2004–2004 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 2005–2011 |  |
| `AMENITY_BANDS` | 2012–2013 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 2014–2016 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 2017–2022 | Whether any band is actually filtering right now. |
| `amenityInBand` | 2023–2037 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 2038–2043 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 2044–2062 |  |
| `gridScale` | 2063–2083 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 2084–2090 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 2091–2102 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2103–2105 |  |
| `quantile` | 2106–2120 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2121–2155 |  |
| `moneyBlurb` | 2156–2167 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2168–2180 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2181–2259 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2260–2260 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2261–2287 |  |
| `failLoading` | 2288–2301 |  |
| `hideLoading` | 2302–2357 |  |
| `topRings` | 2358–2374 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2375–2400 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2401–2401 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2402–2414 |  |
| `svcT` | 2415–2423 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2424–2437 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2438–2438 |  |
| `fmtFire` | 2439–2440 |  |
| `fmtTransit` | 2441–2442 |  |
| `fmtBike` | 2443–2455 |  |
| `fmtRoadM` | 2456–2469 |  |
| `fmtResShare` | 2470–2472 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2473–2478 |  |
| `fmtRoadsCost` | 2479–2483 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2484–2485 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2486–2487 |  |
| `fmtBikeCost` | 2488–2499 |  |
| `servicePlaneLayer` | 2500–2532 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2533–2542 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2543–2548 |  |
| `DEV_IND_TOTAL` | 2549–2551 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2552–2557 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2558–2562 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2563–2568 |  |
| `devGridOfferable` | 2569–2570 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2571–2571 |  |
| `devCol` | 2572–2572 |  |
| `_devScale` | 2573–2573 |  |
| `devScale` | 2574–2580 |  |
| `devT` | 2581–2584 |  |
| `developmentPlaneLayer` | 2585–2601 |  |
| `fmtDev` | 2602–2617 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2618–2623 |  |
| `DEV_GRID_IND_N` | 2624–2624 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2625–2627 |  |
| `devGridScale` | 2628–2654 |  |
| `devGridLayer` | 2655–2703 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2704–2705 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2706–2713 |  |
| `_infillStats` | 2714–2714 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2715–2732 |  |
| `_infillRaw` | 2733–2735 |  |
| `infillScore` | 2736–2751 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2752–2753 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2754–2774 |  |
| `infillColorAt` | 2775–2779 |  |
| `infillPlaneLayer` | 2780–2801 |  |
| `fmtFar` | 2802–2812 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `amenityHighlightGridLayer` | 2813–2867 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2868–2875 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2876–2890 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2891–2911 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2912–2912 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2913–2927 |  |
| `chgT` | 2928–2937 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2938–2968 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2969–3057 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 3058–3065 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 3066–3066 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 3067–3074 |  |
| `deviationRate` | 3075–3118 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `exemptFrac` | 3119–3148 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3149–3155 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3156–3167 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3168–3171 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3172–3176 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3177–3187 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3188–3203 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3204–3235 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3236–3313 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `isBandLayer` | 3314–3318 |  |
| `bandHover` | 3319–3327 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3328–3430 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3431–3438 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3439–3440 |  |
| `glassInstBandLayers` | 3441–3481 |  |
| `ratioInstBandLayers` | 3482–3509 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3510–3522 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3523–3524 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3525–3526 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3527–3527 |  |
| `deviationStats` | 3528–3572 |  |
| `deviationOf` | 3573–3574 |  |
| `deviationT` | 3575–3585 |  |
| `fmtDeviation` | 3586–3607 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3608–3651 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3652–3738 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3739–3763 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `fireStationsLayer` | 3764–3784 |  |
| `ensureFireStations` | 3785–3801 |  |
| `transitStationsLayer` | 3802–3819 |  |
| `ensureTransitStations` | 3820–3836 |  |
| `lrtLinesLayer` | 3837–3853 |  |
| `ensureLrtLines` | 3854–3871 |  |
| `bikeLinesLayer` | 3872–3888 |  |
| `ensureBikeLines` | 3889–3975 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `referenceSplit` | 3976–4003 |  |
| `referenceUnderLayers` | 4004–4038 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 4039–4055 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 4056–4075 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 4076–4089 |  |
| `servicesBlurb` | 4090–4101 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 4102–4125 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4126–4136 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4137–4188 |  |
| `REF_TIERS` | 4189–4210 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4211–4219 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `placeAnchors` | 4220–4243 |  |
| `labelPool` | 4244–4251 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4252–4305 |  |
| `CHROME_IDS` | 4306–4310 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4311–4329 |  |
| `visibleLabels` | 4330–4384 |  |
| `labelLayer` | 4385–4439 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `withSelectedHood` | 4440–4480 |  |
| `_ratioScales` | 4481–4481 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4482–4497 |  |
| `ratioT` | 4498–4520 |  |
| `zMatrix` | 4521–4525 |  |
| `buildLayers` | 4526–4550 |  |
| `flattenDuringEase` | 4551–4575 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4576–4890 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4891–4920 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4921–4930 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4931–4933 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4934–4965 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4966–4972 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4973–4980 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4981–4985 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4986–4996 |  |
| `revenueLens` | 4997–4998 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4999–5031 |  |
| `SVC_COST_BASES` | 5032–5049 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 5050–5058 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 5059–5068 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 5069–5071 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 5072–5078 |  |
| `svcRank` | 5079–5083 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 5084–5090 |  |
| `svcDriverReading` | 5091–5111 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 5112–5112 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 5113–5116 |  |
| `servicePanelFor` | 5117–5121 |  |
| `ratioPanelFor` | 5122–5145 | Ratio carries the cost-as-a-share-of-tax panel that Services had until |
| `hoodPanelLens` | 5146–5150 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 5151–5168 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 5169–5200 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5201–5206 |  |
| `sparklineSvg` | 5207–5222 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5223–5282 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5283–5288 | Development history: new supply per year |
| `devHistKey` | 5289–5298 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5299–5303 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5304–5304 |  |
| `devHistVerb` | 5305–5310 |  |
| `devHistoryFor` | 5311–5349 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5350–5369 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5370–5389 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5390–5425 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5426–5428 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5429–5492 |  |
| `syncTemporalPos` | 5493–5519 |  |
| `openTemporal` | 5520–5557 |  |
| `renderRevenueMix` | 5558–5627 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderRatioCost` | 5628–5702 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `renderServiceCost` | 5703–5760 | The Services panel: what each cost IS for this hood, in dollars, and where |
| `fmtSvcRatio` | 5761–5764 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5765–5815 |  |
| `syncPinnedPanel` | 5816–5849 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5850–5865 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5866–5883 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5884–5931 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5932–5937 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5938–5985 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5986–6002 |  |
| `temporalClick` | 6003–6057 | Click a hood to pin its history; click the pinned one again to unpin. |

### neighbourhood search

| symbol | lines | what it does |
|---|---|---|
| `searchNorm` | 6058–6065 | neighbourhood search |
| `searchMatches` | 6066–6080 | Ranked: the name starts with the query, then a later WORD does (so |
| `renderSearchList` | 6081–6109 |  |
| `openSearch` | 6110–6122 |  |
| `closeSearch` | 6123–6141 |  |

### how-to-read guide

| symbol | lines | what it does |
|---|---|---|
| `openGuide` | 6142–6154 |  |
| `closeGuide` | 6155–6162 |  |
| `maybeAutoGuide` | 6163–6179 |  |
| `flyToHood` | 6180–6199 | Keep the current tilt and rotation, so the camera moves TO the hood |
| `pickSearch` | 6200–6218 | A pick reads exactly like tapping or clicking the hood (temporalClick |
| `primaryRow` | 6219–6287 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 6288–6665 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6666–6755 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6756–6756 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6757–6775 |  |
| `syncMetricButtons` | 6776–6799 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6800–6806 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6807–6820 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6821–6862 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6863–6905 |  |
| `toggleBudgetPanel` | 6906–6931 |  |
| `syncMillRates` | 6932–6964 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6965–6985 |  |
| `applyColorAdjust` | 6986–7006 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 7007–7019 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 7020–7034 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 7035–7052 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 7053–7069 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 7070–7091 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 7092–7108 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 7109–7348 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 7349–7361 | Legend rows for the uses view: the categories actually on screen |
| `applyTheme` | 7362–7371 | Switch theme. Every tc() colour and the ramp (activeRamp) are re-read on |
| `applyPalette` | 7372–7386 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 7387–7395 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 7396–7406 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 7407–7418 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7419–7431 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7432–7452 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7453–7500 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7501–7506 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7507–7528 |  |
| `applyMoneyDetail` | 7529–7553 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7554–7565 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7566–7573 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7574–7592 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7593–7603 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7604–7611 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7612–7628 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7629–7642 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7643–7653 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7654–7897 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7898–7907 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7908–7921 |  |
| `applySvcDriver` | 7922–7954 |  |

### shareable URL: the hash names the view on screen

| symbol | lines | what it does |
|---|---|---|
| `METRIC_FROM_URL` | 7955–7957 |  |
| `urlHash` | 7958–7998 |  |
| `shareLink` | 7999–8007 | Absolute on purpose: the full build carries <base href="../">, and a |
| `copyShareLink` | 8008–8019 | With no clipboard (an insecure origin, a denied permission) the link goes |
| `offered` | 8020–8026 | On screen, ignoring the Options fold: a folded panel on a phone hides |
| `applyUrlState` | 8027–8099 |  |
| `restoreFromHash` | 8100–8118 | Once, at the end of boot, after every build and data gate has run. The |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 8119–8743 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (1081 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 127 | the Lab: a container for unfinished lenses |
| `buildLayers` | 42 | geographic reference layers (all views) |
| `tc` | 27 | tunables |
| `themed` | 17 | tunables |
| `METRICS` | 17 | tunables |
| `applyView` | 17 | control appliers + the view/legend dispatchers |
| `SERVICES` | 16 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `refreshLegend` | 16 | control appliers + the view/legend dispatchers |
| `setBlurb` | 15 | the Lab: a container for unfinished lenses |
| `CELLS` | 11 | tunables |
| `quantile` | 10 | the Lab: a container for unfinished lenses |
| `ratioDenom` | 9 | services lens views (SPEC_services.md display architecture) |
| `ratioScale` | 9 | geographic reference layers (all views) |
| `deviationStats` | 9 | the same doubt, at 100 m |
| `esc` | 9 | money view (default): the classic metric prisms |

**Section self-containment** — share of each section's outgoing edges that stay inside it. Low means a module cut on this banner would mostly import its neighbours.

| section | edges | self-contained |
|---|---|---|
| the Lab: a container for unfinished lenses | 126 | 63% |
| tunables | 15 | 53% |
| Infill lens (SPEC_development.md Lens B) | 27 | 52% |
| uses view (use-mix, 2026-07-03) | 4 | 50% |
| deviation lens: revenue per developed acre against peer average | 4 | 50% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 10 | 40% |
| neighbourhood search | 11 | 36% |
| geographic reference layers (all views) | 96 | 34% |
| loading overlay | 56 | 34% |
| Development history: new supply per year | 112 | 29% |
| Money's revenue panel: where a hood's levy comes from | 35 | 29% |
| two tiers, answering two different questions | 30 | 27% |
| shareable URL: the hash names the view on screen | 24 | 21% |
| control appliers + the view/legend dispatchers | 226 | 20% |
| services lens views (SPEC_services.md display architecture) | 5 | 20% |
| the same doubt, at 100 m | 66 | 18% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| how-to-read guide | 113 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 18 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 4 | 0% |
| boot | 69 | 0% |

## Element ids (143) — the control surface

| id | line |
|---|---|
| `#map` | 18 |
| `#loading` | 22 |
| `#loading-box` | 23 |
| `#loading-title` | 34 |
| `#loading-blurb` | 35 |
| `#loading-spinner` | 36 |
| `#loading-text` | 37 |
| `#loading-retry` | 38 |
| `#banner` | 42 |
| `#gridbusy` | 53 |
| `#gridbusy-spinner` | 54 |
| `#gridbusy-text` | 56 |
| `#gridbusy-size` | 57 |
| `#title` | 61 |
| `#title-h` | 62 |
| `#title-p` | 65 |
| `#search` | 75 |
| `#search-btn` | 76 |
| `#search-box` | 79 |
| `#search-input` | 80 |
| `#search-close` | 84 |
| `#search-list` | 86 |
| `#guide-btn` | 94 |
| `#guide` | 96 |
| `#guide-close` | 97 |
| `#guide-ask` | 98 |
| `#guide-show` | 99 |
| `#guide-body` | 102 |
| `#temporal` | 121 |
| `#temporal-close` | 122 |
| `#temporal-name` | 123 |
| `#temporal-body` | 130 |
| `#temporal-chart` | 131 |
| `#temporal-read` | 132 |
| `#temporal-note` | 133 |
| `#temporal-hint` | 137 |
| `#millrates` | 153 |
| `#mill-head` | 154 |
| `#mill-rows` | 155 |
| `#mill-note` | 156 |
| `#budget` | 170 |
| `#budget-close` | 177 |
| `#budget-head` | 178 |
| `#budget-body` | 183 |
| `#budget-rows` | 184 |
| `#budget-other-hd` | 185 |
| `#budget-other` | 186 |
| `#budget-note` | 187 |
| `#peek` | 202 |
| `#peek-name` | 203 |
| `#peek-read` | 204 |
| `#peek-go` | 205 |
| `#controls` | 208 |
| `#toggle` | 221 |
| `#metric-row` | 222 |
| `#revcut` | 226 |
| `#moneymode` | 231 |
| `#views` | 237 |
| `#optpanel` | 251 |
| `#opt-fold` | 252 |
| `#opt-caret` | 252 |
| `#opt-body` | 253 |
| `#layers` | 254 |
| `#chgwindow-hd` | 255 |
| `#chgwindow` | 256 |
| `#labpick-hd` | 265 |
| `#labpick` | 266 |
| `#labcut-hd` | 267 |
| `#labcut` | 268 |
| `#moneydetail-hd` | 273 |
| `#moneydetail` | 274 |
| `#amenity-hd` | 299 |
| `#amenity` | 300 |
| `#amenity-lrt-row` | 301 |
| `#amenity-lrt-on` | 302 |
| `#amenity-school-row` | 304 |
| `#amenity-school-on` | 305 |
| `#uses-prisms-hd` | 308 |
| `#uses-prisms` | 309 |
| `#uses-prisms-on` | 311 |
| `#devmode-hd` | 314 |
| `#devmode` | 315 |
| `#devmetric-hd` | 319 |
| `#devmetric` | 320 |
| `#devwindow-hd` | 325 |
| `#devwindow` | 326 |
| `#devdetail-hd` | 331 |
| `#devdetail` | 332 |
| `#prism-hd` | 336 |
| `#prism-row` | 337 |
| `#prism-opacity` | 339 |
| `#prism-opacity-val` | 340 |
| `#services-hd` | 342 |
| `#services` | 343 |
| `#denom-hd` | 442 |
| `#denom` | 443 |
| `#ratio-denom-hd` | 447 |
| `#ratio-denom` | 448 |
| `#hoodmode` | 458 |
| `#hoodmode-btn` | 459 |
| `#coloradj` | 471 |
| `#coloradj-btn` | 472 |
| `#budget-pod` | 479 |
| `#budget-btn` | 480 |
| `#share` | 487 |
| `#share-btn` | 488 |
| `#a11y` | 491 |
| `#a11y-btn` | 492 |
| `#a11y-menu` | 493 |
| `#palette` | 495 |
| `#labels-on` | 502 |
| `#reference-on` | 510 |
| `#about` | 515 |
| `#about-btn` | 516 |
| `#about-menu` | 517 |
| `#about-src-roads` | 529 |
| `#about-src-services` | 530 |
| `#about-vintage` | 558 |
| `#about-build` | 562 |
| `#about-lot-acres` | 567 |
| `#about-modelled-roads` | 578 |
| `#about-modelled` | 600 |
| `#about-budget` | 610 |
| `#about-budget-lead` | 612 |
| `#about-budget-rows` | 613 |
| `#about-budget-note` | 614 |
| `#about-updated` | 626 |
| `#botleft` | 630 |
| `#compass` | 631 |
| `#rot-ccw` | 632 |
| `#tonorth` | 639 |
| `#needle` | 641 |
| `#rot-cw` | 646 |
| `#viewbtns` | 654 |
| `#recenter` | 656 |
| `#center2d` | 657 |
| `#legend` | 659 |
| `#legend-label` | 660 |
| `#legend-min` | 662 |
| `#legend-max` | 662 |
| `#legend-cats` | 664 |
| `#revmix` | 5577 |
| `#svccost` | 5671 |
