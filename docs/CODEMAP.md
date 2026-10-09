# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,799-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (320 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `THEMED` | 728–728 | Colours that depend on the backdrop, one value per theme (docs/UI.md → |
| `themed` | 729–729 |  |
| `tc` | 730–735 |  |
| `CENTER` | 736–740 |  |
| `HOME` | 741–741 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 742–755 |  |
| `WINDOWS` | 756–781 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 782–791 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 792–796 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 797–872 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 873–875 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 876–877 |  |
| `METRICS` | 878–997 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `RATIO_DENOMS` | 998–1031 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 1032–1032 |  |
| `ratioOf` | 1033–1033 |  |
| `ratioKept` | 1034–1055 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 1056–1068 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 1069–1096 |  |
| `dominantUse` | 1097–1138 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1139–1289 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1290–1385 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1386–1390 | the Lab: a container for unfinished lenses |
| `inLab` | 1391–1392 |  |
| `DEVIATION_TITLES` | 1393–1397 |  |
| `deviationTitle` | 1398–1403 |  |
| `deviationKind` | 1404–1406 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1407–1414 |  |
| `changeBlurb` | 1415–1432 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1433–1445 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1446–1458 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1459–1467 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1468–1476 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1477–1482 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1483–1490 |  |
| `infillAmenityBlurb` | 1491–1504 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1505–1516 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1517–1522 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1523–1584 |  |
| `setBlurb` | 1585–1599 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1600–1615 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1616–1633 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1634–1640 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1641–1654 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1655–1655 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1656–1670 |  |
| `fmtMB` | 1671–1681 |  |
| `showGridBusy` | 1682–1704 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1705–1721 |  |
| `loadGridData` | 1722–1775 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1776–1829 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1830–1854 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1855–1887 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1888–1888 |  |
| `gridFetches` | 1889–1915 |  |
| `RAMPS` | 1916–1968 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `THEME_RAMPS` | 1969–2003 | The ramps for a light backdrop, per theme (docs/UI.md → Light mode, phase |
| `activeRamp` | 2004–2017 | The ramp actually drawn: the palette choice under the current theme. |
| `rampSetAside` | 2018–2030 | The set-aside colour beside a RAMP-coloured surface. Only where the |
| `lotKey` | 2031–2031 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 2032–2038 |  |
| `AMENITY_BANDS` | 2039–2040 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 2041–2043 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 2044–2049 | Whether any band is actually filtering right now. |
| `amenityInBand` | 2050–2064 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 2065–2070 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 2071–2089 |  |
| `gridScale` | 2090–2110 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 2111–2117 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 2118–2129 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2130–2132 |  |
| `quantile` | 2133–2147 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2148–2182 |  |
| `moneyBlurb` | 2183–2194 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2195–2207 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2208–2286 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2287–2287 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2288–2314 |  |
| `failLoading` | 2315–2328 |  |
| `hideLoading` | 2329–2384 |  |
| `topRings` | 2385–2401 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2402–2427 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2428–2428 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2429–2441 |  |
| `svcT` | 2442–2450 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2451–2464 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2465–2465 |  |
| `fmtFire` | 2466–2467 |  |
| `fmtTransit` | 2468–2469 |  |
| `fmtBike` | 2470–2482 |  |
| `fmtRoadM` | 2483–2496 |  |
| `fmtResShare` | 2497–2499 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2500–2505 |  |
| `fmtRoadsCost` | 2506–2510 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2511–2512 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2513–2514 |  |
| `fmtBikeCost` | 2515–2526 |  |
| `servicePlaneLayer` | 2527–2559 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2560–2569 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2570–2575 |  |
| `DEV_IND_TOTAL` | 2576–2578 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2579–2584 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2585–2589 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2590–2595 |  |
| `devGridOfferable` | 2596–2597 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2598–2598 |  |
| `devCol` | 2599–2599 |  |
| `_devScale` | 2600–2600 |  |
| `devScale` | 2601–2607 |  |
| `devT` | 2608–2611 |  |
| `developmentPlaneLayer` | 2612–2628 |  |
| `fmtDev` | 2629–2644 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2645–2650 |  |
| `DEV_GRID_IND_N` | 2651–2651 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2652–2654 |  |
| `devGridScale` | 2655–2681 |  |
| `devGridLayer` | 2682–2730 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2731–2732 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2733–2740 |  |
| `_infillStats` | 2741–2741 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2742–2759 |  |
| `_infillRaw` | 2760–2762 |  |
| `infillScore` | 2763–2778 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2779–2780 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2781–2801 |  |
| `infillColorAt` | 2802–2806 |  |
| `infillPlaneLayer` | 2807–2828 |  |
| `fmtFar` | 2829–2839 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `amenityHighlightGridLayer` | 2840–2894 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2895–2902 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2903–2917 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2918–2938 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2939–2939 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2940–2954 |  |
| `chgT` | 2955–2964 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2965–2995 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2996–3084 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 3085–3092 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 3093–3093 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 3094–3101 |  |
| `deviationRate` | 3102–3145 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `exemptFrac` | 3146–3175 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3176–3182 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3183–3194 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3195–3198 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3199–3203 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3204–3214 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3215–3230 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3231–3262 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3263–3340 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `isBandLayer` | 3341–3345 |  |
| `bandHover` | 3346–3354 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3355–3457 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3458–3465 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3466–3467 |  |
| `glassInstBandLayers` | 3468–3508 |  |
| `ratioInstBandLayers` | 3509–3536 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3537–3549 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3550–3551 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3552–3553 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3554–3554 |  |
| `deviationStats` | 3555–3599 |  |
| `deviationOf` | 3600–3601 |  |
| `deviationT` | 3602–3612 |  |
| `fmtDeviation` | 3613–3634 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3635–3678 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3679–3765 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3766–3790 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `fireStationsLayer` | 3791–3811 |  |
| `ensureFireStations` | 3812–3828 |  |
| `transitStationsLayer` | 3829–3846 |  |
| `ensureTransitStations` | 3847–3863 |  |
| `lrtLinesLayer` | 3864–3880 |  |
| `ensureLrtLines` | 3881–3898 |  |
| `bikeLinesLayer` | 3899–3915 |  |
| `ensureBikeLines` | 3916–4002 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `referenceSplit` | 4003–4030 |  |
| `referenceUnderLayers` | 4031–4065 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 4066–4082 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 4083–4102 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 4103–4116 |  |
| `servicesBlurb` | 4117–4128 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 4129–4152 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4153–4163 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4164–4215 |  |
| `REF_TIERS` | 4216–4237 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4238–4246 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `placeAnchors` | 4247–4270 |  |
| `labelPool` | 4271–4278 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4279–4332 |  |
| `CHROME_IDS` | 4333–4337 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4338–4356 |  |
| `visibleLabels` | 4357–4411 |  |
| `labelLayer` | 4412–4466 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `withSelectedHood` | 4467–4507 |  |
| `_ratioScales` | 4508–4508 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4509–4524 |  |
| `ratioT` | 4525–4547 |  |
| `zMatrix` | 4548–4552 |  |
| `buildLayers` | 4553–4577 |  |
| `flattenDuringEase` | 4578–4602 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4603–4917 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4918–4947 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4948–4957 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4958–4960 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4961–4992 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4993–4999 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 5000–5007 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 5008–5012 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 5013–5023 |  |
| `revenueLens` | 5024–5025 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 5026–5058 |  |
| `SVC_COST_BASES` | 5059–5076 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 5077–5085 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 5086–5095 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 5096–5098 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 5099–5105 |  |
| `svcRank` | 5106–5110 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 5111–5117 |  |
| `svcDriverReading` | 5118–5138 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 5139–5139 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 5140–5143 |  |
| `servicePanelFor` | 5144–5148 |  |
| `ratioPanelFor` | 5149–5172 | Ratio carries the cost-as-a-share-of-tax panel that Services had until |
| `hoodPanelLens` | 5173–5177 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 5178–5195 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 5196–5227 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5228–5233 |  |
| `sparklineSvg` | 5234–5249 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5250–5309 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5310–5315 | Development history: new supply per year |
| `devHistKey` | 5316–5325 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5326–5330 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5331–5331 |  |
| `devHistVerb` | 5332–5337 |  |
| `devHistoryFor` | 5338–5376 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5377–5396 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5397–5416 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5417–5452 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5453–5455 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5456–5519 |  |
| `syncTemporalPos` | 5520–5546 |  |
| `openTemporal` | 5547–5584 |  |
| `renderRevenueMix` | 5585–5654 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderRatioCost` | 5655–5729 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `renderServiceCost` | 5730–5787 | The Services panel: what each cost IS for this hood, in dollars, and where |
| `fmtSvcRatio` | 5788–5791 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5792–5842 |  |
| `syncPinnedPanel` | 5843–5876 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5877–5892 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5893–5910 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5911–5958 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5959–5964 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5965–6012 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 6013–6029 |  |
| `temporalClick` | 6030–6084 | Click a hood to pin its history; click the pinned one again to unpin. |

### neighbourhood search

| symbol | lines | what it does |
|---|---|---|
| `searchNorm` | 6085–6092 | neighbourhood search |
| `searchMatches` | 6093–6107 | Ranked: the name starts with the query, then a later WORD does (so |
| `renderSearchList` | 6108–6136 |  |
| `openSearch` | 6137–6149 |  |
| `closeSearch` | 6150–6168 |  |

### how-to-read guide

| symbol | lines | what it does |
|---|---|---|
| `openGuide` | 6169–6181 |  |
| `closeGuide` | 6182–6189 |  |
| `maybeAutoGuide` | 6190–6206 |  |
| `flyToHood` | 6207–6226 | Keep the current tilt and rotation, so the camera moves TO the hood |
| `pickSearch` | 6227–6245 | A pick reads exactly like tapping or clicking the hood (temporalClick |
| `primaryRow` | 6246–6314 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 6315–6692 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6693–6782 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6783–6783 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6784–6802 |  |
| `syncMetricButtons` | 6803–6826 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6827–6833 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6834–6847 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6848–6889 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6890–6932 |  |
| `toggleBudgetPanel` | 6933–6958 |  |
| `syncMillRates` | 6959–6991 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6992–7012 |  |
| `applyColorAdjust` | 7013–7033 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 7034–7046 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 7047–7061 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 7062–7079 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 7080–7096 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 7097–7118 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 7119–7135 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 7136–7375 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 7376–7388 | Legend rows for the uses view: the categories actually on screen |
| `applyTheme` | 7389–7403 | Switch theme. Every tc() colour and the ramp (activeRamp) are re-read on |
| `syncThemeChrome` | 7404–7414 | The theme's wording and buttons outside the map. Also run once at boot, |
| `applyPalette` | 7415–7429 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 7430–7438 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 7439–7449 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 7450–7461 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7462–7474 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7475–7495 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7496–7543 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7544–7549 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7550–7571 |  |
| `applyMoneyDetail` | 7572–7596 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7597–7608 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7609–7616 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7617–7635 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7636–7646 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7647–7654 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7655–7671 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7672–7685 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7686–7696 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7697–7940 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7941–7950 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7951–7964 |  |
| `applySvcDriver` | 7965–7997 |  |

### shareable URL: the hash names the view on screen

| symbol | lines | what it does |
|---|---|---|
| `METRIC_FROM_URL` | 7998–8000 |  |
| `urlHash` | 8001–8041 |  |
| `shareLink` | 8042–8050 | Absolute on purpose: the full build carries <base href="../">, and a |
| `copyShareLink` | 8051–8062 | With no clipboard (an insecure origin, a denied permission) the link goes |
| `offered` | 8063–8069 | On screen, ignoring the Options fold: a folded panel on a phone hides |
| `applyUrlState` | 8070–8142 |  |
| `restoreFromHash` | 8143–8161 | Once, at the end of boot, after every build and data gate has run. The |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 8162–8799 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (1090 edges)

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
| the Lab: a container for unfinished lenses | 128 | 63% |
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
| `#map` | 34 |
| `#loading` | 38 |
| `#loading-box` | 39 |
| `#loading-title` | 50 |
| `#loading-blurb` | 51 |
| `#loading-spinner` | 52 |
| `#loading-text` | 53 |
| `#loading-retry` | 54 |
| `#banner` | 58 |
| `#gridbusy` | 69 |
| `#gridbusy-spinner` | 70 |
| `#gridbusy-text` | 72 |
| `#gridbusy-size` | 73 |
| `#title` | 77 |
| `#title-h` | 78 |
| `#title-p` | 81 |
| `#search` | 91 |
| `#search-btn` | 92 |
| `#search-box` | 95 |
| `#search-input` | 96 |
| `#search-close` | 100 |
| `#search-list` | 102 |
| `#guide-btn` | 110 |
| `#guide` | 112 |
| `#guide-close` | 113 |
| `#guide-ask` | 114 |
| `#guide-show` | 115 |
| `#guide-body` | 118 |
| `#temporal` | 137 |
| `#temporal-close` | 138 |
| `#temporal-name` | 139 |
| `#temporal-body` | 146 |
| `#temporal-chart` | 147 |
| `#temporal-read` | 148 |
| `#temporal-note` | 149 |
| `#temporal-hint` | 153 |
| `#millrates` | 169 |
| `#mill-head` | 170 |
| `#mill-rows` | 171 |
| `#mill-note` | 172 |
| `#budget` | 186 |
| `#budget-close` | 193 |
| `#budget-head` | 194 |
| `#budget-body` | 199 |
| `#budget-rows` | 200 |
| `#budget-other-hd` | 201 |
| `#budget-other` | 202 |
| `#budget-note` | 203 |
| `#peek` | 218 |
| `#peek-name` | 219 |
| `#peek-read` | 220 |
| `#peek-go` | 221 |
| `#controls` | 224 |
| `#toggle` | 237 |
| `#metric-row` | 238 |
| `#revcut` | 242 |
| `#moneymode` | 247 |
| `#views` | 253 |
| `#optpanel` | 267 |
| `#opt-fold` | 268 |
| `#opt-caret` | 268 |
| `#opt-body` | 269 |
| `#layers` | 270 |
| `#chgwindow-hd` | 271 |
| `#chgwindow` | 272 |
| `#labpick-hd` | 281 |
| `#labpick` | 282 |
| `#labcut-hd` | 283 |
| `#labcut` | 284 |
| `#moneydetail-hd` | 289 |
| `#moneydetail` | 290 |
| `#amenity-hd` | 315 |
| `#amenity` | 316 |
| `#amenity-lrt-row` | 317 |
| `#amenity-lrt-on` | 318 |
| `#amenity-school-row` | 320 |
| `#amenity-school-on` | 321 |
| `#uses-prisms-hd` | 324 |
| `#uses-prisms` | 325 |
| `#uses-prisms-on` | 327 |
| `#devmode-hd` | 330 |
| `#devmode` | 331 |
| `#devmetric-hd` | 335 |
| `#devmetric` | 336 |
| `#devwindow-hd` | 341 |
| `#devwindow` | 342 |
| `#devdetail-hd` | 347 |
| `#devdetail` | 348 |
| `#prism-hd` | 352 |
| `#prism-row` | 353 |
| `#prism-opacity` | 355 |
| `#prism-opacity-val` | 356 |
| `#services-hd` | 358 |
| `#services` | 359 |
| `#denom-hd` | 458 |
| `#denom` | 459 |
| `#ratio-denom-hd` | 463 |
| `#ratio-denom` | 464 |
| `#hoodmode` | 474 |
| `#hoodmode-btn` | 475 |
| `#coloradj` | 487 |
| `#coloradj-btn` | 488 |
| `#budget-pod` | 495 |
| `#budget-btn` | 496 |
| `#share` | 503 |
| `#share-btn` | 504 |
| `#a11y` | 507 |
| `#a11y-btn` | 508 |
| `#a11y-menu` | 509 |
| `#theme` | 511 |
| `#palette` | 516 |
| `#labels-on` | 523 |
| `#reference-on` | 531 |
| `#about` | 536 |
| `#about-btn` | 537 |
| `#about-menu` | 538 |
| `#about-src-roads` | 550 |
| `#about-src-services` | 551 |
| `#about-vintage` | 579 |
| `#about-build` | 583 |
| `#about-lot-acres` | 588 |
| `#about-modelled-roads` | 599 |
| `#about-modelled` | 621 |
| `#about-budget` | 631 |
| `#about-budget-lead` | 633 |
| `#about-budget-rows` | 634 |
| `#about-budget-note` | 635 |
| `#about-updated` | 647 |
| `#botleft` | 651 |
| `#compass` | 652 |
| `#rot-ccw` | 653 |
| `#tonorth` | 660 |
| `#needle` | 662 |
| `#rot-cw` | 667 |
| `#viewbtns` | 675 |
| `#recenter` | 677 |
| `#center2d` | 678 |
| `#legend` | 680 |
| `#legend-label` | 681 |
| `#legend-min` | 683 |
| `#legend-max` | 683 |
| `#legend-cats` | 685 |
| `#revmix` | 5604 |
| `#svccost` | 5698 |
