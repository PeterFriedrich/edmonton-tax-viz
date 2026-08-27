# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~6,803-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (262 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `CENTER` | 546–550 |  |
| `HOME` | 551–551 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 552–595 |  |
| `fmtMoney` | 596–597 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `METRICS` | 598–723 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `ARTERIAL_COLOR` | 724–740 |  |
| `RATIO_DENOMS` | 741–802 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 803–803 |  |
| `ratioOf` | 804–804 |  |
| `ratioKept` | 805–826 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 827–837 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 838–865 |  |
| `dominantUse` | 866–899 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 900–1054 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1055–1159 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1160–1164 | the Lab: a container for unfinished lenses |
| `inLab` | 1165–1166 |  |
| `DEVIATION_TITLES` | 1167–1171 |  |
| `deviationTitle` | 1172–1177 |  |
| `deviationKind` | 1178–1180 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1181–1186 |  |
| `changeBlurb` | 1187–1209 | Change-lens blurb follows the window picker, so the years named in the |
| `GLASS_BLURBS` | 1210–1231 | Glass blurb follows the spike denominator (the layers-panel toggle). It no |
| `glassInstBlurb` | 1232–1242 | The azure cells need a sentence for the same reason the Lab's outlined |
| `amenityWhichPhrase` | 1243–1248 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1249–1254 |  |
| `infillAmenityBlurb` | 1255–1268 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1269–1283 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `DEV_WINDOW_PHRASE` | 1284–1289 | Development blurb: the base choropleth prose, plus — when the 100 m |
| `devTitle` | 1290–1297 |  |
| `devChoroplethBlurb` | 1298–1299 | The choropleth blurb with the active window's phrase substituted for the |
| `devBlurb` | 1300–1348 |  |
| `withColourClause` | 1349–1363 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `ensureGridData` | 1364–1424 |  |
| `state` | 1425–1478 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `RAMPS` | 1479–1519 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `SET_ASIDE_COLOR` | 1520–1526 | Neutral off-ramp grey for set-aside neighbourhoods (>=90% never/not-yet |
| `GLASS_PLANE_COLOR` | 1527–1532 | Glass view's ground plane: one neutral dark slate for every hood — the |
| `lotKey` | 1533–1533 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 1534–1540 |  |
| `AMENITY_BANDS` | 1541–1542 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 1543–1545 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 1546–1551 | Whether any band is actually filtering right now. |
| `amenityInBand` | 1552–1566 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 1567–1572 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 1573–1584 |  |
| `gridScale` | 1585–1605 |  |
| `scaleT` | 1606–1612 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 1613–1624 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 1625–1627 |  |
| `quantile` | 1628–1642 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 1643–1675 |  |
| `moneyBlurb` | 1676–1680 | The money blurb under the active denominator (ground = the metric's own |
| `fillFor` | 1681–1693 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 1694–1743 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `topRings` | 1744–1760 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 1761–1786 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 1787–1787 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 1788–1800 |  |
| `svcT` | 1801–1805 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 1806–1807 |  |
| `fmtFire` | 1808–1808 |  |
| `fmtTransit` | 1809–1810 |  |
| `fmtBike` | 1811–1811 |  |
| `fmtWater` | 1812–1814 |  |
| `fmtSvcCost` | 1815–1819 |  |
| `fmtRoadsCost` | 1820–1821 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtTransitCost` | 1822–1823 |  |
| `fmtBikeCost` | 1824–1835 |  |
| `servicePlaneLayer` | 1836–1868 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 1869–1878 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 1879–1884 |  |
| `DEV_IND_TOTAL` | 1885–1887 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 1888–1893 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 1894–1898 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 1899–1904 |  |
| `devGridOfferable` | 1905–1906 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 1907–1907 |  |
| `devCol` | 1908–1908 |  |
| `_devScale` | 1909–1909 |  |
| `devScale` | 1910–1916 |  |
| `devT` | 1917–1920 |  |
| `developmentPlaneLayer` | 1921–1937 |  |
| `fmtDev` | 1938–1953 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 1954–1959 |  |
| `DEV_GRID_IND_N` | 1960–1960 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 1961–1963 |  |
| `devGridScale` | 1964–1990 |  |
| `devGridLayer` | 1991–2039 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2040–2041 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2042–2049 |  |
| `_infillStats` | 2050–2050 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2051–2068 |  |
| `_infillRaw` | 2069–2071 |  |
| `infillScore` | 2072–2087 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2088–2089 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2090–2107 |  |
| `INFILL_CENTER` | 2108–2108 | Dark-centred diverging ramp: t in [-1,1]. Negative arm (pressure) warms to |
| `INFILL_POS` | 2109–2109 |  |
| `INFILL_NEG` | 2110–2110 |  |
| `infillColorAt` | 2111–2115 |  |
| `infillPlaneLayer` | 2116–2130 |  |
| `fmtFar` | 2131–2140 |  |
| `AMENITY_HIGHLIGHT_COLOR` | 2141–2141 | Infill's amenity highlight grid (housing the paused infill-granularity |
| `amenityHighlightGridLayer` | 2142–2196 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2197–2202 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2203–2217 | Hardcoded, and deliberately NOT derived from temporal.json's last year: the |
| `changeFor` | 2218–2238 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2239–2239 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2240–2254 |  |
| `chgT` | 2255–2264 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2265–2295 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 2296–2384 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 2385–2392 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 2393–2393 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 2394–2401 |  |
| `deviationRate` | 2402–2444 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `UNCERTAIN_COLOR` | 2445–2445 | ⚠️ ACHROMATIC ON PURPOSE, and it is the wording rule made visual: a band |
| `exemptFrac` | 2446–2475 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 2476–2482 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 2483–2494 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 2495–2498 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 2499–2503 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 2504–2514 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 2515–2530 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 2531–2557 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `INST_OUTLINE_COLOR` | 2558–2610 | ⚠️ NOT the Lab's white, and the difference is measured, not stylistic. |
| `isBandLayer` | 2611–2615 |  |
| `bandHover` | 2616–2624 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 2625–2721 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 2722–2729 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 2730–2731 |  |
| `glassInstBandLayers` | 2732–2760 |  |
| `deviationRateExempt` | 2761–2773 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 2774–2775 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 2776–2777 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 2778–2778 |  |
| `deviationStats` | 2779–2823 |  |
| `deviationOf` | 2824–2825 |  |
| `deviationT` | 2826–2836 |  |
| `fmtDeviation` | 2837–2858 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 2859–2902 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 2903–2989 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 2990–3012 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `FIRE_STATION_COLOR` | 3013–3013 | Fire-station context dots (SPEC_services.md "Fire lens"): 31 points, |
| `fireStationsLayer` | 3014–3034 |  |
| `ensureFireStations` | 3035–3050 |  |
| `TRANSIT_STATION_COLOR` | 3051–3051 | Transit-station context dots (SPEC_services.md "Transit lens"): the |
| `transitStationsLayer` | 3052–3069 |  |
| `ensureTransitStations` | 3070–3085 |  |
| `TRANSIT_LINE_COLOR` | 3086–3086 | LRT track lines (SPEC_services.md "Transit lens"): the operating LRT |
| `lrtLinesLayer` | 3087–3103 |  |
| `ensureLrtLines` | 3104–3120 |  |
| `BIKE_LINE_COLOR` | 3121–3121 | The dedicated bike network (SPEC_services.md "Transportation lens"): a |
| `bikeLinesLayer` | 3122–3138 |  |
| `ensureBikeLines` | 3139–3196 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `RIVER_COLOR` | 3197–3197 | Barely-there greys against the #0a0a0f backdrop: enough to read as |
| `HIGHWAY_COLOR` | 3198–3201 |  |
| `BOUNDARY_COLOR` | 3202–3211 | Municipal outlines: dimmer than the highways and unfilled. They are the |
| `CITY_LIMIT_COLOR` | 3212–3212 | …with ONE exception, and it is the point of the tier split: Edmonton's own |
| `ZONE_LINE_COLOR` | 3213–3225 |  |
| `referenceSplit` | 3226–3253 |  |
| `referenceUnderLayers` | 3254–3288 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 3289–3305 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 3306–3325 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 3326–3338 |  |
| `servicesBlurb` | 3339–3356 | Services-view blurb: the colour-driving service's story, plus one line |
| `hoodHoverLayer` | 3357–3380 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 3381–3391 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 3392–3443 |  |
| `REF_TIERS` | 3444–3465 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 3466–3473 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `HOOD_COLOR` | 3474–3476 |  |
| `placeAnchors` | 3477–3500 |  |
| `labelPool` | 3501–3508 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 3509–3562 |  |
| `CHROME_IDS` | 3563–3566 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 3567–3585 |  |
| `visibleLabels` | 3586–3640 |  |
| `labelLayer` | 3641–3677 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `_ratioScales` | 3678–3678 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 3679–3694 |  |
| `ratioT` | 3695–3705 |  |
| `buildLayers` | 3706–3718 | Build the layer stack for the current view. Rebuilt on any toggle. |
| `buildViewLayers` | 3719–4021 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4022–4051 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4052–4055 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4056–4058 |  |
| `fmtBig` | 4059–4086 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 4087–4092 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 4093–4100 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 4101–4105 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 4106–4116 |  |
| `revenueLens` | 4117–4118 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 4119–4136 |  |
| `SVC_COST_BASES` | 4137–4149 | The Services panel: this hood's revenue per acre set against what the City |
| `serviceLens` | 4150–4150 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 4151–4153 |  |
| `servicePanelFor` | 4154–4167 |  |
| `hoodPanelLens` | 4168–4171 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 4172–4189 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 4190–4221 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 4222–4227 |  |
| `sparklineSvg` | 4228–4243 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 4244–4313 | The pinned chart: same geometry, plus the things only a 300px box can |
| `syncTemporalPos` | 4314–4340 |  |
| `openTemporal` | 4341–4369 |  |
| `renderRevenueMix` | 4370–4418 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderServiceCost` | 4419–4452 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `fmtSvcRatio` | 4453–4455 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 4456–4506 |  |
| `syncPinnedPanel` | 4507–4533 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 4534–4549 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 4550–4560 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 4561–4608 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 4609–4614 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 4615–4654 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 4655–4671 |  |
| `temporalClick` | 4672–4729 | Click a hood to pin its history; click the pinned one again to unpin. |
| `primaryRow` | 4730–4809 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 4810–5142 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 5143–5210 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 5211–5211 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 5212–5230 |  |
| `syncMetricButtons` | 5231–5254 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 5255–5261 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 5262–5275 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 5276–5317 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 5318–5360 |  |
| `toggleBudgetPanel` | 5361–5386 |  |
| `syncMillRates` | 5387–5417 | Paint the pod, gate it to the money view's revenue cuts, and place it. |
| `applyMetric` | 5418–5439 |  |
| `applyColorAdjust` | 5440–5461 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 5462–5474 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 5475–5490 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 5491–5508 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 5509–5525 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 5526–5541 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 5542–5558 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 5559–5798 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 5799–5809 | Legend rows for the uses view: the categories actually on screen |
| `applyPalette` | 5810–5823 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 5824–5832 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 5833–5843 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 5844–5855 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 5856–5869 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 5870–5890 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 5891–5938 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 5939–5944 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 5945–5962 |  |
| `applyMoneyDetail` | 5963–5972 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `applyMoneyMode` | 5973–5980 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 5981–5999 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 6000–6010 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 6011–6018 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 6019–6035 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 6036–6049 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 6050–6060 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 6061–6296 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 6297–6306 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 6307–6320 |  |
| `applySvcDriver` | 6321–6803 |  |

## Element ids (114) — the control surface

| id | line |
|---|---|
| `#map` | 18 |
| `#banner` | 20 |
| `#title` | 22 |
| `#title-h` | 23 |
| `#title-p` | 24 |
| `#temporal` | 35 |
| `#temporal-close` | 36 |
| `#temporal-name` | 37 |
| `#temporal-body` | 44 |
| `#temporal-chart` | 45 |
| `#temporal-read` | 46 |
| `#temporal-note` | 47 |
| `#temporal-hint` | 51 |
| `#millrates` | 67 |
| `#mill-head` | 68 |
| `#mill-rows` | 69 |
| `#mill-note` | 70 |
| `#budget` | 84 |
| `#budget-close` | 91 |
| `#budget-head` | 92 |
| `#budget-body` | 97 |
| `#budget-rows` | 98 |
| `#budget-other-hd` | 99 |
| `#budget-other` | 100 |
| `#budget-note` | 101 |
| `#peek` | 116 |
| `#peek-name` | 117 |
| `#peek-read` | 118 |
| `#peek-go` | 119 |
| `#controls` | 122 |
| `#toggle` | 135 |
| `#metric-row` | 136 |
| `#revcut` | 140 |
| `#moneymode` | 145 |
| `#views` | 151 |
| `#optpanel` | 165 |
| `#opt-fold` | 166 |
| `#opt-caret` | 166 |
| `#opt-body` | 167 |
| `#layers` | 168 |
| `#chgwindow-hd` | 169 |
| `#chgwindow` | 170 |
| `#labpick-hd` | 179 |
| `#labpick` | 180 |
| `#labcut-hd` | 181 |
| `#labcut` | 182 |
| `#moneydetail-hd` | 187 |
| `#moneydetail` | 188 |
| `#amenity-hd` | 202 |
| `#amenity` | 203 |
| `#amenity-lrt-row` | 204 |
| `#amenity-lrt-on` | 205 |
| `#amenity-school-row` | 207 |
| `#amenity-school-on` | 208 |
| `#uses-prisms-hd` | 211 |
| `#uses-prisms` | 212 |
| `#uses-prisms-on` | 214 |
| `#devmode-hd` | 217 |
| `#devmode` | 218 |
| `#devmetric-hd` | 222 |
| `#devmetric` | 223 |
| `#devwindow-hd` | 228 |
| `#devwindow` | 229 |
| `#devdetail-hd` | 234 |
| `#devdetail` | 235 |
| `#prism-hd` | 239 |
| `#prism-row` | 240 |
| `#prism-opacity` | 242 |
| `#prism-opacity-val` | 243 |
| `#services-hd` | 245 |
| `#services` | 246 |
| `#denom-hd` | 340 |
| `#denom` | 341 |
| `#ratio-denom-hd` | 345 |
| `#ratio-denom` | 346 |
| `#hoodmode` | 357 |
| `#hoodmode-btn` | 358 |
| `#coloradj` | 370 |
| `#coloradj-btn` | 371 |
| `#budget-pod` | 378 |
| `#budget-btn` | 379 |
| `#a11y` | 383 |
| `#a11y-btn` | 384 |
| `#a11y-menu` | 385 |
| `#palette` | 387 |
| `#labels-on` | 394 |
| `#reference-on` | 402 |
| `#about` | 407 |
| `#about-btn` | 408 |
| `#about-menu` | 409 |
| `#about-src-services` | 418 |
| `#about-vintage` | 446 |
| `#about-modelled` | 453 |
| `#about-budget` | 463 |
| `#about-budget-lead` | 465 |
| `#about-budget-rows` | 466 |
| `#about-budget-note` | 467 |
| `#about-updated` | 478 |
| `#botleft` | 482 |
| `#compass` | 483 |
| `#rot-ccw` | 484 |
| `#tonorth` | 491 |
| `#needle` | 493 |
| `#rot-cw` | 498 |
| `#viewbtns` | 506 |
| `#center2d` | 507 |
| `#recenter` | 508 |
| `#legend` | 510 |
| `#legend-label` | 511 |
| `#legend-min` | 513 |
| `#legend-max` | 513 |
| `#legend-cats` | 515 |
| `#revmix` | 4389 |
| `#svccost` | 4433 |
