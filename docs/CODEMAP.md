# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~7,462-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (284 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 645–649 |  |
| `HOME` | 650–650 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 651–664 |  |
| `WINDOWS` | 665–683 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 684–693 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 694–698 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 699–766 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `fmtMoney` | 767–768 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 769–894 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 895–911 |  |
| `RATIO_DENOMS` | 912–973 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 974–974 |  |
| `ratioOf` | 975–975 |  |
| `ratioKept` | 976–997 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 998–1008 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 1009–1036 |  |
| `dominantUse` | 1037–1078 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1079–1264 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1265–1369 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1370–1374 | the Lab: a container for unfinished lenses |
| `inLab` | 1375–1376 |  |
| `DEVIATION_TITLES` | 1377–1381 |  |
| `deviationTitle` | 1382–1387 |  |
| `deviationKind` | 1388–1390 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1391–1396 |  |
| `changeBlurb` | 1397–1421 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1422–1443 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1444–1454 | The azure cells need a sentence for the same reason the Lab's outlined |
| `amenityWhichPhrase` | 1455–1460 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1461–1466 |  |
| `infillAmenityBlurb` | 1467–1480 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1481–1495 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1496–1501 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1502–1509 |  |
| `devChoroplethBlurb` | 1510–1511 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1512–1560 |  |
| `withColourClause` | 1561–1578 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1579–1585 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1586–1599 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1600–1600 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1601–1615 |  |
| `fmtMB` | 1616–1626 |  |
| `showGridBusy` | 1627–1649 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1650–1666 |  |
| `loadGridData` | 1667–1720 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1721–1774 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1775–1799 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1800–1831 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1832–1832 |  |
| `gridFetches` | 1833–1856 |  |
| `RAMPS` | 1857–1897 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1898–1904 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1905–1910 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1911–1911 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1912–1918 |  |
| `AMENITY_BANDS` | 1919–1920 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1921–1923 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1924–1929 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1930–1944 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1945–1950 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1951–1969 |  |
| `gridScale` | 1970–1990 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1991–1997 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1998–2009 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2010–2012 |  |
| `quantile` | 2013–2027 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2028–2060 |  |
| `moneyBlurb` | 2061–2065 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 2066–2078 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2079–2157 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2158–2158 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2159–2185 |  |
| `failLoading` | 2186–2199 |  |
| `hideLoading` | 2200–2254 |  |
| `topRings` | 2255–2271 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2272–2297 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2298–2298 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2299–2311 |  |
| `svcT` | 2312–2316 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2317–2318 |  |
| `fmtFire` | 2319–2319 |  |
| `fmtTransit` | 2320–2321 |  |
| `fmtBike` | 2322–2322 |  |
| `fmtWater` | 2323–2325 |  |
| `fmtSvcCost` | 2326–2330 |  |
| `fmtRoadsCost` | 2331–2335 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2336–2337 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2338–2339 |  |
| `fmtBikeCost` | 2340–2351 |  |
| `servicePlaneLayer` | 2352–2384 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2385–2394 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2395–2400 |  |
| `DEV_IND_TOTAL` | 2401–2403 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2404–2409 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2410–2414 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2415–2420 |  |
| `devGridOfferable` | 2421–2422 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2423–2423 |  |
| `devCol` | 2424–2424 |  |
| `_devScale` | 2425–2425 |  |
| `devScale` | 2426–2432 |  |
| `devT` | 2433–2436 |  |
| `developmentPlaneLayer` | 2437–2453 |  |
| `fmtDev` | 2454–2469 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2470–2475 |  |
| `DEV_GRID_IND_N` | 2476–2476 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2477–2479 |  |
| `devGridScale` | 2480–2506 |  |
| `devGridLayer` | 2507–2555 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2556–2557 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2558–2565 |  |
| `_infillStats` | 2566–2566 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2567–2584 |  |
| `_infillRaw` | 2585–2587 |  |
| `infillScore` | 2588–2603 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2604–2605 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2606–2623 |  |
| `INFILL_CENTER` | 2624–2624 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2625–2625 |  |
| `INFILL_NEG` | 2626–2626 |  |
| `infillColorAt` | 2627–2631 |  |
| `infillPlaneLayer` | 2632–2646 |  |
| `fmtFar` | 2647–2656 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2657–2657 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2658–2712 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2713–2720 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2721–2735 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2736–2756 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2757–2757 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2758–2772 |  |
| `chgT` | 2773–2782 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2783–2813 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2814–2902 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2903–2910 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2911–2911 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2912–2919 |  |
| `deviationRate` | 2920–2962 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2963–2963 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2964–2993 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2994–3000 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3001–3012 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3013–3016 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3017–3021 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3022–3032 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3033–3048 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3049–3075 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 3076–3128 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3129–3133 |  |
| `bandHover` | 3134–3142 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3143–3239 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3240–3247 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3248–3249 |  |
| `glassInstBandLayers` | 3250–3278 |  |
| `deviationRateExempt` | 3279–3291 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3292–3293 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3294–3295 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3296–3296 |  |
| `deviationStats` | 3297–3341 |  |
| `deviationOf` | 3342–3343 |  |
| `deviationT` | 3344–3354 |  |
| `fmtDeviation` | 3355–3376 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3377–3420 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3421–3507 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3508–3530 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3531–3531 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3532–3552 |  |
| `ensureFireStations` | 3553–3568 |  |
| `TRANSIT_STATION_COLOR` | 3569–3569 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3570–3587 |  |
| `ensureTransitStations` | 3588–3603 |  |
| `TRANSIT_LINE_COLOR` | 3604–3604 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3605–3621 |  |
| `ensureLrtLines` | 3622–3638 |  |
| `BIKE_LINE_COLOR` | 3639–3639 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3640–3656 |  |
| `ensureBikeLines` | 3657–3714 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3715–3715 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3716–3719 |  |
| `BOUNDARY_COLOR` | 3720–3729 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3730–3730 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3731–3743 |  |
| `referenceSplit` | 3744–3771 |  |
| `referenceUnderLayers` | 3772–3806 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3807–3823 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3824–3843 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3844–3856 |  |
| `servicesBlurb` | 3857–3874 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3875–3898 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3899–3909 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3910–3961 |  |
| `REF_TIERS` | 3962–3983 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3984–3991 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3992–3994 |  |
| `placeAnchors` | 3995–4018 |  |
| `labelPool` | 4019–4026 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4027–4080 |  |
| `CHROME_IDS` | 4081–4085 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4086–4104 |  |
| `visibleLabels` | 4105–4159 |  |
| `labelLayer` | 4160–4196 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4197–4197 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4198–4213 |  |
| `ratioT` | 4214–4224 |  |
| `buildLayers` | 4225–4237 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 4238–4540 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4541–4570 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4571–4574 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4575–4577 |  |
| `fmtBig` | 4578–4605 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4606–4611 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4612–4619 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4620–4624 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4625–4635 |  |
| `revenueLens` | 4636–4637 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4638–4662 |  |
| `SVC_COST_BASES` | 4663–4677 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4678–4678 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4679–4682 |  |
| `servicePanelFor` | 4683–4696 |  |
| `hoodPanelLens` | 4697–4700 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4701–4718 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4719–4750 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4751–4756 |  |
| `sparklineSvg` | 4757–4772 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4773–4842 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4843–4869 |  |
| `openTemporal` | 4870–4898 |  |
| `renderRevenueMix` | 4899–4947 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4948–4994 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4995–4997 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4998–5048 |  |
| `syncPinnedPanel` | 5049–5075 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5076–5091 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5092–5102 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5103–5150 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5151–5156 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5157–5196 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5197–5213 |  |
| `temporalClick` | 5214–5271 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5272–5352 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5353–5690 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5691–5758 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5759–5759 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5760–5778 |  |
| `syncMetricButtons` | 5779–5802 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5803–5809 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5810–5823 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5824–5865 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5866–5908 |  |
| `toggleBudgetPanel` | 5909–5934 |  |
| `syncMillRates` | 5935–5967 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 5968–5989 |  |
| `applyColorAdjust` | 5990–6011 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 6012–6024 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 6025–6040 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6041–6058 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6059–6075 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6076–6091 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6092–6108 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6109–6356 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6357–6367 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6368–6381 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6382–6390 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6391–6401 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6402–6413 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6414–6427 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6428–6448 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6449–6496 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 6497–6502 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 6503–6524 |  |
| `applyMoneyDetail` | 6525–6549 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 6550–6561 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 6562–6569 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 6570–6588 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 6589–6599 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 6600–6607 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 6608–6624 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 6625–6638 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 6639–6649 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 6650–6893 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6894–6903 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6904–6917 |  |
| `applySvcDriver` | 6918–6931 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 6932–7462 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (869 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 111 | the Lab: a container for unfinished lenses |
| `buildLayers` | 35 | geographic reference layers (all views) |
| `METRICS` | 16 | tunables |
| `refreshLegend` | 14 | control appliers + the view/legend dispatchers |
| `applyView` | 13 | control appliers + the view/legend dispatchers |
| `SERVICES` | 12 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `CELLS` | 10 | tunables |
| `quantile` | 10 | the Lab: a container for unfinished lenses |
| `deviationStats` | 9 | the same doubt, at 100 m |
| `ratioDenom` | 8 | services lens views (SPEC_services.md display architecture) |
| `ratioScale` | 8 | geographic reference layers (all views) |
| `devIndustrial` | 8 | loading overlay |
| `devCol` | 8 | loading overlay |
| `labelPool` | 8 | geographic reference layers (all views) |
| `esc` | 8 | money view (default): the classic metric prisms |

**Section self-containment** — share of each section's outgoing edges that stay inside it. Low means a module cut on this banner would mostly import its neighbours.

| section | edges | self-contained |
|---|---|---|
| services lens views (SPEC_services.md display architecture) | 1 | 100% |
| uses view (use-mix, 2026-07-03) | 3 | 67% |
| deviation lens: revenue per developed acre against peer average | 3 | 67% |
| the Lab: a container for unfinished lenses | 107 | 65% |
| Infill lens (SPEC_development.md Lens B) | 26 | 65% |
| tunables | 10 | 60% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 9 | 44% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| geographic reference layers (all views) | 86 | 42% |
| loading overlay | 49 | 39% |
| Money's revenue panel: where a hood's levy comes from | 186 | 38% |
| two tiers, answering two different questions | 27 | 33% |
| the same doubt, at 100 m | 53 | 30% |
| control appliers + the view/legend dispatchers | 206 | 21% |
| the citywide budget panel (EXPERIMENTAL, full build only) | 12 | 8% |
| services view (SPEC_services.md UI generalization, 2026-07-05) | 16 | 0% |
| the institutional uncertainty band | 2 | 0% |
| temporal lens (SPEC_temporal.md phase 3) | 1 | 0% |
| boot | 56 | 0% |

## Element ids (128) — the control surface

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
| `#title-p` | 63 |
| `#temporal` | 74 |
| `#temporal-close` | 75 |
| `#temporal-name` | 76 |
| `#temporal-body` | 83 |
| `#temporal-chart` | 84 |
| `#temporal-read` | 85 |
| `#temporal-note` | 86 |
| `#temporal-hint` | 90 |
| `#millrates` | 106 |
| `#mill-head` | 107 |
| `#mill-rows` | 108 |
| `#mill-note` | 109 |
| `#budget` | 123 |
| `#budget-close` | 130 |
| `#budget-head` | 131 |
| `#budget-body` | 136 |
| `#budget-rows` | 137 |
| `#budget-other-hd` | 138 |
| `#budget-other` | 139 |
| `#budget-note` | 140 |
| `#peek` | 155 |
| `#peek-name` | 156 |
| `#peek-read` | 157 |
| `#peek-go` | 158 |
| `#controls` | 161 |
| `#toggle` | 174 |
| `#metric-row` | 175 |
| `#revcut` | 179 |
| `#moneymode` | 184 |
| `#views` | 190 |
| `#optpanel` | 204 |
| `#opt-fold` | 205 |
| `#opt-caret` | 205 |
| `#opt-body` | 206 |
| `#layers` | 207 |
| `#chgwindow-hd` | 208 |
| `#chgwindow` | 209 |
| `#labpick-hd` | 218 |
| `#labpick` | 219 |
| `#labcut-hd` | 220 |
| `#labcut` | 221 |
| `#moneydetail-hd` | 226 |
| `#moneydetail` | 227 |
| `#amenity-hd` | 252 |
| `#amenity` | 253 |
| `#amenity-lrt-row` | 254 |
| `#amenity-lrt-on` | 255 |
| `#amenity-school-row` | 257 |
| `#amenity-school-on` | 258 |
| `#uses-prisms-hd` | 261 |
| `#uses-prisms` | 262 |
| `#uses-prisms-on` | 264 |
| `#devmode-hd` | 267 |
| `#devmode` | 268 |
| `#devmetric-hd` | 272 |
| `#devmetric` | 273 |
| `#devwindow-hd` | 278 |
| `#devwindow` | 279 |
| `#devdetail-hd` | 284 |
| `#devdetail` | 285 |
| `#prism-hd` | 289 |
| `#prism-row` | 290 |
| `#prism-opacity` | 292 |
| `#prism-opacity-val` | 293 |
| `#services-hd` | 295 |
| `#services` | 296 |
| `#denom-hd` | 403 |
| `#denom` | 404 |
| `#ratio-denom-hd` | 408 |
| `#ratio-denom` | 409 |
| `#hoodmode` | 420 |
| `#hoodmode-btn` | 421 |
| `#coloradj` | 433 |
| `#coloradj-btn` | 434 |
| `#budget-pod` | 441 |
| `#budget-btn` | 442 |
| `#a11y` | 446 |
| `#a11y-btn` | 447 |
| `#a11y-menu` | 448 |
| `#palette` | 450 |
| `#labels-on` | 457 |
| `#reference-on` | 465 |
| `#about` | 470 |
| `#about-btn` | 471 |
| `#about-menu` | 472 |
| `#about-src-roads` | 484 |
| `#about-src-services` | 485 |
| `#about-vintage` | 513 |
| `#about-build` | 517 |
| `#about-modelled-roads` | 531 |
| `#about-modelled` | 545 |
| `#about-budget` | 555 |
| `#about-budget-lead` | 557 |
| `#about-budget-rows` | 558 |
| `#about-budget-note` | 559 |
| `#about-updated` | 570 |
| `#botleft` | 574 |
| `#compass` | 575 |
| `#rot-ccw` | 576 |
| `#tonorth` | 583 |
| `#needle` | 585 |
| `#rot-cw` | 590 |
| `#viewbtns` | 598 |
| `#center2d` | 599 |
| `#recenter` | 600 |
| `#legend` | 602 |
| `#legend-label` | 603 |
| `#legend-min` | 605 |
| `#legend-max` | 605 |
| `#legend-cats` | 607 |
| `#revmix` | 4918 |
| `#svccost` | 4967 |
