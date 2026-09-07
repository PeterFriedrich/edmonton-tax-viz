# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~7,419-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (283 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 636–640 |  |
| `HOME` | 641–641 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 642–655 |  |
| `WINDOWS` | 656–674 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 675–684 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 685–689 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 690–757 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `fmtMoney` | 758–759 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 760–885 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 886–902 |  |
| `RATIO_DENOMS` | 903–935 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 936–936 |  |
| `ratioOf` | 937–937 |  |
| `ratioKept` | 938–959 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 960–970 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 971–998 |  |
| `dominantUse` | 999–1040 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1041–1207 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1208–1312 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1313–1317 | the Lab: a container for unfinished lenses |
| `inLab` | 1318–1319 |  |
| `DEVIATION_TITLES` | 1320–1324 |  |
| `deviationTitle` | 1325–1330 |  |
| `deviationKind` | 1331–1333 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1334–1339 |  |
| `changeBlurb` | 1340–1364 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1365–1386 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1387–1397 | The azure cells need a sentence for the same reason the Lab's outlined |
| `amenityWhichPhrase` | 1398–1403 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1404–1409 |  |
| `infillAmenityBlurb` | 1410–1423 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1424–1438 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1439–1444 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1445–1452 |  |
| `devChoroplethBlurb` | 1453–1454 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1455–1503 |  |
| `withColourClause` | 1504–1521 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1522–1528 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1529–1542 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1543–1543 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1544–1558 |  |
| `fmtMB` | 1559–1569 |  |
| `showGridBusy` | 1570–1592 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1593–1609 |  |
| `loadGridData` | 1610–1663 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1664–1717 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1718–1742 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1743–1774 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1775–1775 |  |
| `gridFetches` | 1776–1799 |  |
| `RAMPS` | 1800–1840 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1841–1847 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1848–1853 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1854–1854 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1855–1861 |  |
| `AMENITY_BANDS` | 1862–1863 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1864–1866 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1867–1872 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1873–1887 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1888–1893 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1894–1912 |  |
| `gridScale` | 1913–1933 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 1934–1940 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1941–1952 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1953–1955 |  |
| `quantile` | 1956–1970 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1971–2003 |  |
| `moneyBlurb` | 2004–2008 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 2009–2021 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2022–2100 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2101–2101 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2102–2128 |  |
| `failLoading` | 2129–2142 |  |
| `hideLoading` | 2143–2197 |  |
| `topRings` | 2198–2214 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2215–2240 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2241–2241 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2242–2254 |  |
| `svcT` | 2255–2259 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2260–2261 |  |
| `fmtFire` | 2262–2262 |  |
| `fmtTransit` | 2263–2264 |  |
| `fmtBike` | 2265–2265 |  |
| `fmtWater` | 2266–2271 |  |
| `fmtRoadsCost` | 2272–2276 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2277–2278 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2279–2280 |  |
| `fmtBikeCost` | 2281–2292 |  |
| `servicePlaneLayer` | 2293–2325 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2326–2335 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2336–2341 |  |
| `DEV_IND_TOTAL` | 2342–2344 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2345–2350 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2351–2355 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2356–2361 |  |
| `devGridOfferable` | 2362–2363 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2364–2364 |  |
| `devCol` | 2365–2365 |  |
| `_devScale` | 2366–2366 |  |
| `devScale` | 2367–2373 |  |
| `devT` | 2374–2377 |  |
| `developmentPlaneLayer` | 2378–2394 |  |
| `fmtDev` | 2395–2410 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2411–2416 |  |
| `DEV_GRID_IND_N` | 2417–2417 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2418–2420 |  |
| `devGridScale` | 2421–2447 |  |
| `devGridLayer` | 2448–2496 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2497–2498 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2499–2506 |  |
| `_infillStats` | 2507–2507 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2508–2525 |  |
| `_infillRaw` | 2526–2528 |  |
| `infillScore` | 2529–2544 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2545–2546 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2547–2564 |  |
| `INFILL_CENTER` | 2565–2565 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2566–2566 |  |
| `INFILL_NEG` | 2567–2567 |  |
| `infillColorAt` | 2568–2572 |  |
| `infillPlaneLayer` | 2573–2587 |  |
| `fmtFar` | 2588–2597 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2598–2598 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2599–2653 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2654–2661 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2662–2676 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2677–2697 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2698–2698 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2699–2713 |  |
| `chgT` | 2714–2723 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2724–2754 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2755–2843 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2844–2851 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2852–2852 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2853–2860 |  |
| `deviationRate` | 2861–2903 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2904–2904 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2905–2934 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2935–2941 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2942–2953 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2954–2957 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2958–2962 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2963–2973 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2974–2989 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2990–3016 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 3017–3069 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 3070–3074 |  |
| `bandHover` | 3075–3083 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3084–3180 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3181–3188 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3189–3190 |  |
| `glassInstBandLayers` | 3191–3219 |  |
| `deviationRateExempt` | 3220–3232 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3233–3234 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3235–3236 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3237–3237 |  |
| `deviationStats` | 3238–3282 |  |
| `deviationOf` | 3283–3284 |  |
| `deviationT` | 3285–3295 |  |
| `fmtDeviation` | 3296–3317 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3318–3361 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3362–3448 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3449–3471 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3472–3472 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3473–3493 |  |
| `ensureFireStations` | 3494–3509 |  |
| `TRANSIT_STATION_COLOR` | 3510–3510 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3511–3528 |  |
| `ensureTransitStations` | 3529–3544 |  |
| `TRANSIT_LINE_COLOR` | 3545–3545 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3546–3562 |  |
| `ensureLrtLines` | 3563–3579 |  |
| `BIKE_LINE_COLOR` | 3580–3580 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3581–3597 |  |
| `ensureBikeLines` | 3598–3655 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3656–3656 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3657–3660 |  |
| `BOUNDARY_COLOR` | 3661–3670 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3671–3671 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3672–3684 |  |
| `referenceSplit` | 3685–3712 |  |
| `referenceUnderLayers` | 3713–3747 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3748–3764 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3765–3784 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3785–3797 |  |
| `servicesBlurb` | 3798–3815 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3816–3839 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3840–3850 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3851–3902 |  |
| `REF_TIERS` | 3903–3924 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3925–3932 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3933–3935 |  |
| `placeAnchors` | 3936–3959 |  |
| `labelPool` | 3960–3967 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3968–4021 |  |
| `CHROME_IDS` | 4022–4026 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4027–4045 |  |
| `visibleLabels` | 4046–4100 |  |
| `labelLayer` | 4101–4137 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 4138–4138 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4139–4154 |  |
| `ratioT` | 4155–4165 |  |
| `buildLayers` | 4166–4178 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 4179–4481 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4482–4511 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4512–4515 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4516–4518 |  |
| `fmtBig` | 4519–4546 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4547–4552 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4553–4560 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4561–4565 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4566–4576 |  |
| `revenueLens` | 4577–4578 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4579–4610 |  |
| `SVC_COST_BASES` | 4611–4623 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4624–4624 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4625–4628 |  |
| `servicePanelFor` | 4629–4649 |  |
| `hoodPanelLens` | 4650–4653 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4654–4671 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4672–4703 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4704–4709 |  |
| `sparklineSvg` | 4710–4725 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4726–4795 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4796–4822 |  |
| `openTemporal` | 4823–4851 |  |
| `renderRevenueMix` | 4852–4918 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4919–4963 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4964–4966 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4967–5017 |  |
| `syncPinnedPanel` | 5018–5044 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5045–5060 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5061–5071 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5072–5119 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5120–5125 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 5126–5165 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 5166–5182 |  |
| `temporalClick` | 5183–5240 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 5241–5320 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 5321–5656 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5657–5724 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5725–5725 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5726–5744 |  |
| `syncMetricButtons` | 5745–5768 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5769–5775 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5776–5789 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5790–5831 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5832–5874 |  |
| `toggleBudgetPanel` | 5875–5900 |  |
| `syncMillRates` | 5901–5933 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 5934–5955 |  |
| `applyColorAdjust` | 5956–5977 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5978–5990 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5991–6006 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 6007–6024 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 6025–6041 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 6042–6057 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 6058–6074 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 6075–6314 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 6315–6325 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 6326–6339 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 6340–6348 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 6349–6359 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 6360–6371 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 6372–6385 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 6386–6406 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 6407–6454 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 6455–6460 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 6461–6482 |  |
| `applyMoneyDetail` | 6483–6507 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 6508–6519 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 6520–6527 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 6528–6546 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 6547–6557 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 6558–6565 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 6566–6582 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 6583–6596 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 6597–6607 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 6608–6853 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6854–6863 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6864–6877 |  |
| `applySvcDriver` | 6878–6891 |  |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 6892–7419 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (869 edges)

⚠️ **A regex reference count, not a call graph** — a name in a comment or string counts, and a nested symbol is attributed to its enclosing range. Use it for *what is central* and *would this seam hold*, never as ground truth for a final module boundary.

**Most depended-on** — moving one of these touches everything below it.

| symbol | referenced by | section |
|---|---|---|
| `state` | 112 | the Lab: a container for unfinished lenses |
| `buildLayers` | 35 | geographic reference layers (all views) |
| `METRICS` | 16 | tunables |
| `refreshLegend` | 14 | control appliers + the view/legend dispatchers |
| `SERVICES` | 13 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `applyView` | 13 | control appliers + the view/legend dispatchers |
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
| `#denom-hd` | 395 |
| `#denom` | 396 |
| `#ratio-denom-hd` | 400 |
| `#ratio-denom` | 401 |
| `#hoodmode` | 411 |
| `#hoodmode-btn` | 412 |
| `#coloradj` | 424 |
| `#coloradj-btn` | 425 |
| `#budget-pod` | 432 |
| `#budget-btn` | 433 |
| `#a11y` | 437 |
| `#a11y-btn` | 438 |
| `#a11y-menu` | 439 |
| `#palette` | 441 |
| `#labels-on` | 448 |
| `#reference-on` | 456 |
| `#about` | 461 |
| `#about-btn` | 462 |
| `#about-menu` | 463 |
| `#about-src-roads` | 475 |
| `#about-src-services` | 476 |
| `#about-vintage` | 504 |
| `#about-build` | 508 |
| `#about-modelled-roads` | 522 |
| `#about-modelled` | 536 |
| `#about-budget` | 546 |
| `#about-budget-lead` | 548 |
| `#about-budget-rows` | 549 |
| `#about-budget-note` | 550 |
| `#about-updated` | 561 |
| `#botleft` | 565 |
| `#compass` | 566 |
| `#rot-ccw` | 567 |
| `#tonorth` | 574 |
| `#needle` | 576 |
| `#rot-cw` | 581 |
| `#viewbtns` | 589 |
| `#center2d` | 590 |
| `#recenter` | 591 |
| `#legend` | 593 |
| `#legend-label` | 594 |
| `#legend-min` | 596 |
| `#legend-max` | 596 |
| `#legend-cats` | 598 |
| `#revmix` | 4871 |
| `#svccost` | 4937 |
