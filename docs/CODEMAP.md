# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,127-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (313 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 650–654 |  |
| `HOME` | 655–655 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 656–669 |  |
| `WINDOWS` | 670–695 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 696–705 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 706–710 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 711–786 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 787–789 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 790–791 |  |
| `METRICS` | 792–894 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 895–911 |  |
| `RATIO_DENOMS` | 912–945 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 946–946 |  |
| `ratioOf` | 947–947 |  |
| `ratioKept` | 948–969 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 970–980 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 981–1008 |  |
| `dominantUse` | 1009–1050 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1051–1201 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1202–1297 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1298–1302 | the Lab: a container for unfinished lenses |
| `inLab` | 1303–1304 |  |
| `DEVIATION_TITLES` | 1305–1309 |  |
| `deviationTitle` | 1310–1315 |  |
| `deviationKind` | 1316–1318 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1319–1326 |  |
| `changeBlurb` | 1327–1344 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1345–1357 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1358–1370 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1371–1379 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1380–1388 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1389–1394 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1395–1402 |  |
| `infillAmenityBlurb` | 1403–1416 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1417–1428 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1429–1434 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1435–1493 |  |
| `setBlurb` | 1494–1506 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1507–1522 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1523–1540 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1541–1547 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1548–1561 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1562–1562 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1563–1577 |  |
| `fmtMB` | 1578–1588 |  |
| `showGridBusy` | 1589–1611 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1612–1628 |  |
| `loadGridData` | 1629–1682 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1683–1736 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1737–1761 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1762–1793 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1794–1794 |  |
| `gridFetches` | 1795–1819 |  |
| `RAMPS` | 1820–1860 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1861–1867 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1868–1873 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1874–1874 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1875–1881 |  |
| `AMENITY_BANDS` | 1882–1883 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1884–1886 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1887–1892 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1893–1907 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1908–1913 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1914–1932 |  |
| `gridScale` | 1933–1953 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1954–1960 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1961–1972 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1973–1975 |  |
| `quantile` | 1976–1990 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1991–2025 |  |
| `moneyBlurb` | 2026–2037 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2038–2050 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2051–2129 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2130–2130 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2131–2157 |  |
| `failLoading` | 2158–2171 |  |
| `hideLoading` | 2172–2226 |  |
| `topRings` | 2227–2243 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2244–2269 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2270–2270 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2271–2283 |  |
| `svcT` | 2284–2292 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2293–2306 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2307–2307 |  |
| `fmtFire` | 2308–2309 |  |
| `fmtTransit` | 2310–2311 |  |
| `fmtBike` | 2312–2324 |  |
| `fmtRoadM` | 2325–2338 |  |
| `fmtResShare` | 2339–2341 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2342–2347 |  |
| `fmtRoadsCost` | 2348–2352 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2353–2354 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2355–2356 |  |
| `fmtBikeCost` | 2357–2368 |  |
| `servicePlaneLayer` | 2369–2401 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2402–2411 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2412–2417 |  |
| `DEV_IND_TOTAL` | 2418–2420 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2421–2426 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2427–2431 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2432–2437 |  |
| `devGridOfferable` | 2438–2439 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2440–2440 |  |
| `devCol` | 2441–2441 |  |
| `_devScale` | 2442–2442 |  |
| `devScale` | 2443–2449 |  |
| `devT` | 2450–2453 |  |
| `developmentPlaneLayer` | 2454–2470 |  |
| `fmtDev` | 2471–2486 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2487–2492 |  |
| `DEV_GRID_IND_N` | 2493–2493 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2494–2496 |  |
| `devGridScale` | 2497–2523 |  |
| `devGridLayer` | 2524–2572 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2573–2574 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2575–2582 |  |
| `_infillStats` | 2583–2583 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2584–2601 |  |
| `_infillRaw` | 2602–2604 |  |
| `infillScore` | 2605–2620 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2621–2622 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2623–2640 |  |
| `INFILL_CENTER` | 2641–2641 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2642–2642 |  |
| `INFILL_NEG` | 2643–2643 |  |
| `infillColorAt` | 2644–2648 |  |
| `infillPlaneLayer` | 2649–2670 |  |
| `fmtFar` | 2671–2680 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `AMENITY_HIGHLIGHT_COLOR` | 2681–2681 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2682–2736 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2737–2744 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2745–2759 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2760–2780 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2781–2781 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2782–2796 |  |
| `chgT` | 2797–2806 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2807–2837 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2838–2926 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2927–2934 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2935–2935 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2936–2943 |  |
| `deviationRate` | 2944–2986 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2987–2987 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2988–3017 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3018–3024 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3025–3036 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3037–3040 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3041–3045 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3046–3056 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3057–3072 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3073–3104 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3105–3129 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `INST_OUTLINE_COLOR` | 3130–3182 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3183–3187 |  |
| `bandHover` | 3188–3196 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3197–3299 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3300–3307 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3308–3309 |  |
| `glassInstBandLayers` | 3310–3350 |  |
| `ratioInstBandLayers` | 3351–3378 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3379–3391 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3392–3393 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3394–3395 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3396–3396 |  |
| `deviationStats` | 3397–3441 |  |
| `deviationOf` | 3442–3443 |  |
| `deviationT` | 3444–3454 |  |
| `fmtDeviation` | 3455–3476 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3477–3520 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3521–3607 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3608–3630 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3631–3631 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3632–3652 |  |
| `ensureFireStations` | 3653–3668 |  |
| `TRANSIT_STATION_COLOR` | 3669–3669 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3670–3687 |  |
| `ensureTransitStations` | 3688–3703 |  |
| `TRANSIT_LINE_COLOR` | 3704–3704 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3705–3721 |  |
| `ensureLrtLines` | 3722–3738 |  |
| `BIKE_LINE_COLOR` | 3739–3739 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3740–3756 |  |
| `ensureBikeLines` | 3757–3814 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3815–3815 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3816–3819 |  |
| `BOUNDARY_COLOR` | 3820–3829 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3830–3830 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3831–3843 |  |
| `referenceSplit` | 3844–3871 |  |
| `referenceUnderLayers` | 3872–3906 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3907–3923 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3924–3943 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3944–3957 |  |
| `servicesBlurb` | 3958–3969 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 3970–3993 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3994–4004 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4005–4056 |  |
| `REF_TIERS` | 4057–4078 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4079–4086 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 4087–4089 |  |
| `placeAnchors` | 4090–4113 |  |
| `labelPool` | 4114–4121 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4122–4175 |  |
| `CHROME_IDS` | 4176–4180 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4181–4199 |  |
| `visibleLabels` | 4200–4254 |  |
| `labelLayer` | 4255–4291 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4292–4292 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4293–4308 |  |
| `ratioT` | 4309–4331 |  |
| `zMatrix` | 4332–4336 |  |
| `buildLayers` | 4337–4360 |  |
| `flattenDuringEase` | 4361–4385 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4386–4695 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4696–4725 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4726–4735 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4736–4738 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4739–4770 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4771–4777 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4778–4785 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4786–4790 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4791–4801 |  |
| `revenueLens` | 4802–4803 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4804–4836 |  |
| `SVC_COST_BASES` | 4837–4854 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 4855–4863 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 4864–4873 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 4874–4876 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 4877–4883 |  |
| `svcRank` | 4884–4888 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 4889–4895 |  |
| `svcDriverReading` | 4896–4916 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 4917–4917 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4918–4921 |  |
| `servicePanelFor` | 4922–4926 |  |
| `ratioPanelFor` | 4927–4950 | Ratio carries the cost-as-a-share-of-tax panel that Services had until |
| `hoodPanelLens` | 4951–4955 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4956–4973 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4974–5005 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5006–5011 |  |
| `sparklineSvg` | 5012–5027 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5028–5087 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5088–5093 | Development history: new supply per year |
| `devHistKey` | 5094–5103 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5104–5108 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5109–5109 |  |
| `devHistVerb` | 5110–5115 |  |
| `devHistoryFor` | 5116–5151 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5152–5171 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5172–5191 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5192–5227 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5228–5230 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5231–5294 |  |
| `syncTemporalPos` | 5295–5321 |  |
| `openTemporal` | 5322–5358 |  |
| `renderRevenueMix` | 5359–5428 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderRatioCost` | 5429–5503 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `renderServiceCost` | 5504–5561 | The Services panel: what each cost IS for this hood, in dollars, and where |
| `fmtSvcRatio` | 5562–5565 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5566–5616 |  |
| `syncPinnedPanel` | 5617–5650 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5651–5666 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5667–5684 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5685–5732 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5733–5738 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5739–5786 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5787–5803 |  |
| `temporalClick` | 5804–5861 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5862–5930 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5931–6308 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6309–6398 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6399–6399 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6400–6418 |  |
| `syncMetricButtons` | 6419–6442 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6443–6449 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6450–6463 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6464–6505 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6506–6548 |  |
| `toggleBudgetPanel` | 6549–6574 |  |
| `syncMillRates` | 6575–6607 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 6608–6628 |  |
| `applyColorAdjust` | 6629–6649 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6650–6662 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6663–6677 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6678–6695 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6696–6712 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6713–6734 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6735–6751 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6752–6991 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6992–7002 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 7003–7016 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 7017–7025 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 7026–7036 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 7037–7048 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7049–7061 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7062–7082 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7083–7130 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7131–7136 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7137–7158 |  |
| `applyMoneyDetail` | 7159–7183 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7184–7195 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7196–7203 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7204–7222 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7223–7233 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7234–7241 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7242–7258 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7259–7272 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7273–7283 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7284–7527 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7528–7537 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7538–7551 |  |
| `applySvcDriver` | 7552–7565 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 7566–8127 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (992 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 120 | the Lab: a container for unfinished lenses |
| `buildLayers` | 37 | geographic reference layers (all views) |
| `METRICS` | 17 | tunables |
| `applyView` | 15 | control appliers + the view/legend dispatchers |
| `setBlurb` | 15 | the Lab: a container for unfinished lenses |
| `SERVICES` | 14 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `refreshLegend` | 14 | control appliers + the view/legend dispatchers |
| `CELLS` | 10 | tunables |
| `quantile` | 10 | the Lab: a container for unfinished lenses |
| `ratioDenom` | 9 | services lens views (SPEC_services.md display architecture) |
| `ratioScale` | 9 | geographic reference layers (all views) |
| `deviationStats` | 9 | the same doubt, at 100 m |
| `esc` | 9 | money view (default): the classic metric prisms |
| `devIndustrial` | 8 | loading overlay |
| `devCol` | 8 | loading overlay |

**Section self-containment** — share of each section's outgoing edges that stay inside it. Low means a module cut on this banner would mostly import its neighbours.

| section | edges | self-contained |
|---|---|---|
| uses view (use-mix, 2026-07-03) | 3 | 67% |
| Infill lens (SPEC_development.md Lens B) | 27 | 67% |
| deviation lens: revenue per developed acre against peer average | 3 | 67% |
| the Lab: a container for unfinished lenses | 119 | 64% |
| tunables | 13 | 46% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 9 | 44% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| geographic reference layers (all views) | 92 | 43% |
| loading overlay | 55 | 35% |
| two tiers, answering two different questions | 29 | 31% |
| Money's revenue panel: where a hood's levy comes from | 35 | 29% |
| the same doubt, at 100 m | 61 | 26% |
| Development history: new supply per year | 214 | 23% |
| services lens views (SPEC_services.md display architecture) | 5 | 20% |
| control appliers + the view/legend dispatchers | 216 | 20% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 18 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 4 | 0% |
| boot | 59 | 0% |

## Element ids (129) — the control surface

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
| `#temporal` | 75 |
| `#temporal-close` | 76 |
| `#temporal-name` | 77 |
| `#temporal-body` | 84 |
| `#temporal-chart` | 85 |
| `#temporal-read` | 86 |
| `#temporal-note` | 87 |
| `#temporal-hint` | 91 |
| `#millrates` | 107 |
| `#mill-head` | 108 |
| `#mill-rows` | 109 |
| `#mill-note` | 110 |
| `#budget` | 124 |
| `#budget-close` | 131 |
| `#budget-head` | 132 |
| `#budget-body` | 137 |
| `#budget-rows` | 138 |
| `#budget-other-hd` | 139 |
| `#budget-other` | 140 |
| `#budget-note` | 141 |
| `#peek` | 156 |
| `#peek-name` | 157 |
| `#peek-read` | 158 |
| `#peek-go` | 159 |
| `#controls` | 162 |
| `#toggle` | 175 |
| `#metric-row` | 176 |
| `#revcut` | 180 |
| `#moneymode` | 185 |
| `#views` | 191 |
| `#optpanel` | 205 |
| `#opt-fold` | 206 |
| `#opt-caret` | 206 |
| `#opt-body` | 207 |
| `#layers` | 208 |
| `#chgwindow-hd` | 209 |
| `#chgwindow` | 210 |
| `#labpick-hd` | 219 |
| `#labpick` | 220 |
| `#labcut-hd` | 221 |
| `#labcut` | 222 |
| `#moneydetail-hd` | 227 |
| `#moneydetail` | 228 |
| `#amenity-hd` | 253 |
| `#amenity` | 254 |
| `#amenity-lrt-row` | 255 |
| `#amenity-lrt-on` | 256 |
| `#amenity-school-row` | 258 |
| `#amenity-school-on` | 259 |
| `#uses-prisms-hd` | 262 |
| `#uses-prisms` | 263 |
| `#uses-prisms-on` | 265 |
| `#devmode-hd` | 268 |
| `#devmode` | 269 |
| `#devmetric-hd` | 273 |
| `#devmetric` | 274 |
| `#devwindow-hd` | 279 |
| `#devwindow` | 280 |
| `#devdetail-hd` | 285 |
| `#devdetail` | 286 |
| `#prism-hd` | 290 |
| `#prism-row` | 291 |
| `#prism-opacity` | 293 |
| `#prism-opacity-val` | 294 |
| `#services-hd` | 296 |
| `#services` | 297 |
| `#denom-hd` | 396 |
| `#denom` | 397 |
| `#ratio-denom-hd` | 401 |
| `#ratio-denom` | 402 |
| `#hoodmode` | 412 |
| `#hoodmode-btn` | 413 |
| `#coloradj` | 425 |
| `#coloradj-btn` | 426 |
| `#budget-pod` | 433 |
| `#budget-btn` | 434 |
| `#a11y` | 438 |
| `#a11y-btn` | 439 |
| `#a11y-menu` | 440 |
| `#palette` | 442 |
| `#labels-on` | 449 |
| `#reference-on` | 457 |
| `#about` | 462 |
| `#about-btn` | 463 |
| `#about-menu` | 464 |
| `#about-src-roads` | 476 |
| `#about-src-services` | 477 |
| `#about-vintage` | 505 |
| `#about-build` | 509 |
| `#about-lot-acres` | 514 |
| `#about-modelled-roads` | 525 |
| `#about-modelled` | 547 |
| `#about-budget` | 557 |
| `#about-budget-lead` | 559 |
| `#about-budget-rows` | 560 |
| `#about-budget-note` | 561 |
| `#about-updated` | 573 |
| `#botleft` | 577 |
| `#compass` | 578 |
| `#rot-ccw` | 579 |
| `#tonorth` | 586 |
| `#needle` | 588 |
| `#rot-cw` | 593 |
| `#viewbtns` | 601 |
| `#recenter` | 603 |
| `#center2d` | 604 |
| `#legend` | 606 |
| `#legend-label` | 607 |
| `#legend-min` | 609 |
| `#legend-max` | 609 |
| `#legend-cats` | 611 |
| `#revmix` | 5378 |
| `#svccost` | 5472 |
