# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,848-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (323 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `THEMED` | 734–736 | Colours that depend on the backdrop, one value per theme (docs/UI.md → |
| `themed` | 737–741 | Throws on a missing or mis-sized light value: deck draws `undefined` |
| `tc` | 742–747 |  |
| `CENTER` | 748–752 |  |
| `HOME` | 753–753 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 754–767 |  |
| `WINDOWS` | 768–793 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 794–803 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 804–808 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 809–884 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 885–887 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 888–889 |  |
| `METRICS` | 890–1009 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `RATIO_DENOMS` | 1010–1043 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 1044–1044 |  |
| `ratioOf` | 1045–1045 |  |
| `ratioKept` | 1046–1067 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 1068–1080 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 1081–1108 |  |
| `dominantUse` | 1109–1150 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1151–1301 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1302–1397 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1398–1402 | the Lab: a container for unfinished lenses |
| `inLab` | 1403–1404 |  |
| `DEVIATION_TITLES` | 1405–1409 |  |
| `deviationTitle` | 1410–1415 |  |
| `deviationKind` | 1416–1418 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1419–1426 |  |
| `changeBlurb` | 1427–1444 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1445–1457 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1458–1470 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1471–1479 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1480–1488 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1489–1494 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1495–1502 |  |
| `infillAmenityBlurb` | 1503–1516 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1517–1528 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1529–1534 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1535–1596 |  |
| `setBlurb` | 1597–1611 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1612–1627 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1628–1645 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1646–1652 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1653–1666 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1667–1667 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1668–1682 |  |
| `fmtMB` | 1683–1693 |  |
| `showGridBusy` | 1694–1716 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1717–1733 |  |
| `loadGridData` | 1734–1787 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1788–1841 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1842–1866 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1867–1899 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1900–1900 |  |
| `gridFetches` | 1901–1927 |  |
| `RAMPS` | 1928–1980 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `THEME_RAMPS` | 1981–2015 | The ramps for a light backdrop, per theme (docs/UI.md → Light mode, phase |
| `activeRamp` | 2016–2029 | The ramp actually drawn: the palette choice under the current theme. |
| `rampSetAside` | 2030–2042 | The set-aside colour beside a RAMP-coloured surface. Only where the |
| `lotKey` | 2043–2043 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 2044–2050 |  |
| `AMENITY_BANDS` | 2051–2052 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 2053–2055 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 2056–2061 | Whether any band is actually filtering right now. |
| `amenityInBand` | 2062–2076 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 2077–2082 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 2083–2101 |  |
| `gridScale` | 2102–2122 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 2123–2129 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 2130–2141 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2142–2144 |  |
| `quantile` | 2145–2159 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2160–2194 |  |
| `moneyBlurb` | 2195–2206 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2207–2219 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2220–2273 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `GRID_INK` | 2274–2274 |  |
| `gridName` | 2275–2288 |  |
| `paintBackdrop` | 2289–2326 | The backdrop's three MapLibre layers, after a theme or ramp change. |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2327–2327 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2328–2352 |  |
| `failLoading` | 2353–2366 |  |
| `hideLoading` | 2367–2422 |  |
| `topRings` | 2423–2439 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2440–2465 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2466–2466 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2467–2479 |  |
| `svcT` | 2480–2488 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2489–2502 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2503–2503 |  |
| `fmtFire` | 2504–2505 |  |
| `fmtTransit` | 2506–2507 |  |
| `fmtBike` | 2508–2520 |  |
| `fmtRoadM` | 2521–2534 |  |
| `fmtResShare` | 2535–2537 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2538–2543 |  |
| `fmtRoadsCost` | 2544–2548 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2549–2550 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2551–2552 |  |
| `fmtBikeCost` | 2553–2564 |  |
| `servicePlaneLayer` | 2565–2597 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2598–2607 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2608–2613 |  |
| `DEV_IND_TOTAL` | 2614–2616 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2617–2622 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2623–2627 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2628–2633 |  |
| `devGridOfferable` | 2634–2635 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2636–2636 |  |
| `devCol` | 2637–2637 |  |
| `_devScale` | 2638–2638 |  |
| `devScale` | 2639–2645 |  |
| `devT` | 2646–2649 |  |
| `developmentPlaneLayer` | 2650–2666 |  |
| `fmtDev` | 2667–2682 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2683–2688 |  |
| `DEV_GRID_IND_N` | 2689–2689 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2690–2692 |  |
| `devGridScale` | 2693–2719 |  |
| `devGridLayer` | 2720–2768 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2769–2770 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2771–2778 |  |
| `_infillStats` | 2779–2779 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2780–2797 |  |
| `_infillRaw` | 2798–2800 |  |
| `infillScore` | 2801–2816 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2817–2818 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2819–2839 |  |
| `infillColorAt` | 2840–2844 |  |
| `infillPlaneLayer` | 2845–2866 |  |
| `fmtFar` | 2867–2877 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `amenityHighlightGridLayer` | 2878–2932 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2933–2940 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2941–2955 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2956–2976 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2977–2977 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2978–2992 |  |
| `chgT` | 2993–3002 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 3003–3033 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 3034–3122 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 3123–3130 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 3131–3131 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 3132–3139 |  |
| `deviationRate` | 3140–3183 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `exemptFrac` | 3184–3213 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3214–3220 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3221–3232 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3233–3236 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3237–3241 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3242–3252 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3253–3268 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3269–3300 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3301–3378 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `isBandLayer` | 3379–3383 |  |
| `bandHover` | 3384–3392 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3393–3495 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3496–3503 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3504–3505 |  |
| `glassInstBandLayers` | 3506–3546 |  |
| `ratioInstBandLayers` | 3547–3574 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3575–3587 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3588–3589 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3590–3591 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3592–3592 |  |
| `deviationStats` | 3593–3637 |  |
| `deviationOf` | 3638–3639 |  |
| `deviationT` | 3640–3650 |  |
| `fmtDeviation` | 3651–3672 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3673–3716 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3717–3803 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3804–3828 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `fireStationsLayer` | 3829–3849 |  |
| `ensureFireStations` | 3850–3866 |  |
| `transitStationsLayer` | 3867–3884 |  |
| `ensureTransitStations` | 3885–3901 |  |
| `lrtLinesLayer` | 3902–3918 |  |
| `ensureLrtLines` | 3919–3936 |  |
| `bikeLinesLayer` | 3937–3953 |  |
| `ensureBikeLines` | 3954–4040 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `referenceSplit` | 4041–4068 |  |
| `referenceUnderLayers` | 4069–4103 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 4104–4120 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 4121–4140 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 4141–4155 |  |
| `servicesBlurb` | 4156–4167 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 4168–4191 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4192–4202 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4203–4254 |  |
| `REF_TIERS` | 4255–4276 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4277–4285 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `placeAnchors` | 4286–4309 |  |
| `labelPool` | 4310–4317 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4318–4371 |  |
| `CHROME_IDS` | 4372–4376 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4377–4395 |  |
| `visibleLabels` | 4396–4450 |  |
| `labelLayer` | 4451–4505 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `withSelectedHood` | 4506–4546 |  |
| `_ratioScales` | 4547–4547 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4548–4563 |  |
| `ratioT` | 4564–4586 |  |
| `zMatrix` | 4587–4591 |  |
| `buildLayers` | 4592–4616 |  |
| `flattenDuringEase` | 4617–4641 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4642–4956 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4957–4986 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4987–4996 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4997–4999 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 5000–5031 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 5032–5038 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 5039–5046 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 5047–5051 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 5052–5062 |  |
| `revenueLens` | 5063–5064 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 5065–5097 |  |
| `SVC_COST_BASES` | 5098–5115 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 5116–5124 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 5125–5134 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 5135–5137 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 5138–5144 |  |
| `svcRank` | 5145–5149 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 5150–5156 |  |
| `svcDriverReading` | 5157–5177 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 5178–5178 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 5179–5182 |  |
| `servicePanelFor` | 5183–5187 |  |
| `ratioPanelFor` | 5188–5211 | Ratio carries the cost-as-a-share-of-tax panel that Services had until |
| `hoodPanelLens` | 5212–5216 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 5217–5234 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 5235–5266 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5267–5272 |  |
| `sparklineSvg` | 5273–5288 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5289–5348 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5349–5354 | Development history: new supply per year |
| `devHistKey` | 5355–5364 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5365–5369 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5370–5370 |  |
| `devHistVerb` | 5371–5376 |  |
| `devHistoryFor` | 5377–5415 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5416–5435 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5436–5455 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5456–5491 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5492–5494 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5495–5558 |  |
| `syncTemporalPos` | 5559–5585 |  |
| `openTemporal` | 5586–5623 |  |
| `renderRevenueMix` | 5624–5693 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderRatioCost` | 5694–5768 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `renderServiceCost` | 5769–5826 | The Services panel: what each cost IS for this hood, in dollars, and where |
| `fmtSvcRatio` | 5827–5830 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5831–5881 |  |
| `syncPinnedPanel` | 5882–5915 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5916–5931 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5932–5949 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5950–5997 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5998–6003 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 6004–6051 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 6052–6068 |  |
| `temporalClick` | 6069–6123 | Click a hood to pin its history; click the pinned one again to unpin. |

### neighbourhood search

| symbol | lines | what it does |
|---|---|---|
| `searchNorm` | 6124–6131 | neighbourhood search |
| `searchMatches` | 6132–6146 | Ranked: the name starts with the query, then a later WORD does (so |
| `renderSearchList` | 6147–6175 |  |
| `openSearch` | 6176–6188 |  |
| `closeSearch` | 6189–6207 |  |

### how-to-read guide

| symbol | lines | what it does |
|---|---|---|
| `openGuide` | 6208–6220 |  |
| `closeGuide` | 6221–6228 |  |
| `maybeAutoGuide` | 6229–6245 |  |
| `flyToHood` | 6246–6265 | Keep the current tilt and rotation, so the camera moves TO the hood |
| `pickSearch` | 6266–6284 | A pick reads exactly like tapping or clicking the hood (temporalClick |
| `primaryRow` | 6285–6353 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 6354–6731 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6732–6821 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6822–6822 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6823–6841 |  |
| `syncMetricButtons` | 6842–6865 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6866–6872 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6873–6886 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6887–6928 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6929–6971 |  |
| `toggleBudgetPanel` | 6972–6997 |  |
| `syncMillRates` | 6998–7030 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 7031–7051 |  |
| `applyColorAdjust` | 7052–7072 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 7073–7085 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 7086–7100 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 7101–7118 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 7119–7135 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 7136–7157 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 7158–7174 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 7175–7414 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 7415–7427 | Legend rows for the uses view: the categories actually on screen |
| `applyTheme` | 7428–7444 | Switch theme. Every tc() colour and the ramp (activeRamp) are re-read on |
| `syncThemeChrome` | 7445–7455 | The theme's wording and buttons outside the map. Also run once at boot, |
| `applyPalette` | 7456–7470 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 7471–7479 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 7480–7490 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 7491–7502 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7503–7515 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7516–7536 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7537–7584 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7585–7590 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7591–7612 |  |
| `applyMoneyDetail` | 7613–7637 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7638–7649 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7650–7657 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7658–7676 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7677–7687 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7688–7695 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7696–7712 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7713–7726 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7727–7737 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7738–7982 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7983–7992 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7993–8006 |  |
| `applySvcDriver` | 8007–8039 |  |

### shareable URL: the hash names the view on screen

| symbol | lines | what it does |
|---|---|---|
| `METRIC_FROM_URL` | 8040–8042 |  |
| `urlHash` | 8043–8083 |  |
| `shareLink` | 8084–8092 | Absolute on purpose: the full build carries <base href="../">, and a |
| `copyShareLink` | 8093–8104 | With no clipboard (an insecure origin, a denied permission) the link goes |
| `offered` | 8105–8111 | On screen, ignoring the Options fold: a folded panel on a phone hides |
| `applyUrlState` | 8112–8184 |  |
| `restoreFromHash` | 8185–8203 | Once, at the end of boot, after every build and data gate has run. The |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 8204–8848 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (1098 edges)

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
| the Lab: a container for unfinished lenses | 127 | 64% |
| tunables | 16 | 56% |
| Infill lens (SPEC_development.md Lens B) | 27 | 52% |
| uses view (use-mix, 2026-07-03) | 4 | 50% |
| deviation lens: revenue per developed acre against peer average | 4 | 50% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| base map (no basemap tiles for v1 — just a dark backdrop) | 5 | 40% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 10 | 40% |
| neighbourhood search | 11 | 36% |
| geographic reference layers (all views) | 97 | 35% |
| loading overlay | 57 | 33% |
| Development history: new supply per year | 112 | 29% |
| Money's revenue panel: where a hood's levy comes from | 35 | 29% |
| two tiers, answering two different questions | 30 | 27% |
| shareable URL: the hash names the view on screen | 24 | 21% |
| control appliers + the view/legend dispatchers | 232 | 20% |
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
| `#search` | 97 |
| `#search-btn` | 98 |
| `#search-box` | 101 |
| `#search-input` | 102 |
| `#search-close` | 106 |
| `#search-list` | 108 |
| `#guide-btn` | 116 |
| `#guide` | 118 |
| `#guide-close` | 119 |
| `#guide-ask` | 120 |
| `#guide-show` | 121 |
| `#guide-body` | 124 |
| `#temporal` | 143 |
| `#temporal-close` | 144 |
| `#temporal-name` | 145 |
| `#temporal-body` | 152 |
| `#temporal-chart` | 153 |
| `#temporal-read` | 154 |
| `#temporal-note` | 155 |
| `#temporal-hint` | 159 |
| `#millrates` | 175 |
| `#mill-head` | 176 |
| `#mill-rows` | 177 |
| `#mill-note` | 178 |
| `#budget` | 192 |
| `#budget-close` | 199 |
| `#budget-head` | 200 |
| `#budget-body` | 205 |
| `#budget-rows` | 206 |
| `#budget-other-hd` | 207 |
| `#budget-other` | 208 |
| `#budget-note` | 209 |
| `#peek` | 224 |
| `#peek-name` | 225 |
| `#peek-read` | 226 |
| `#peek-go` | 227 |
| `#controls` | 230 |
| `#toggle` | 243 |
| `#metric-row` | 244 |
| `#revcut` | 248 |
| `#moneymode` | 253 |
| `#views` | 259 |
| `#optpanel` | 273 |
| `#opt-fold` | 274 |
| `#opt-caret` | 274 |
| `#opt-body` | 275 |
| `#layers` | 276 |
| `#chgwindow-hd` | 277 |
| `#chgwindow` | 278 |
| `#labpick-hd` | 287 |
| `#labpick` | 288 |
| `#labcut-hd` | 289 |
| `#labcut` | 290 |
| `#moneydetail-hd` | 295 |
| `#moneydetail` | 296 |
| `#amenity-hd` | 321 |
| `#amenity` | 322 |
| `#amenity-lrt-row` | 323 |
| `#amenity-lrt-on` | 324 |
| `#amenity-school-row` | 326 |
| `#amenity-school-on` | 327 |
| `#uses-prisms-hd` | 330 |
| `#uses-prisms` | 331 |
| `#uses-prisms-on` | 333 |
| `#devmode-hd` | 336 |
| `#devmode` | 337 |
| `#devmetric-hd` | 341 |
| `#devmetric` | 342 |
| `#devwindow-hd` | 347 |
| `#devwindow` | 348 |
| `#devdetail-hd` | 353 |
| `#devdetail` | 354 |
| `#prism-hd` | 358 |
| `#prism-row` | 359 |
| `#prism-opacity` | 361 |
| `#prism-opacity-val` | 362 |
| `#services-hd` | 364 |
| `#services` | 365 |
| `#denom-hd` | 464 |
| `#denom` | 465 |
| `#ratio-denom-hd` | 469 |
| `#ratio-denom` | 470 |
| `#hoodmode` | 480 |
| `#hoodmode-btn` | 481 |
| `#coloradj` | 493 |
| `#coloradj-btn` | 494 |
| `#budget-pod` | 501 |
| `#budget-btn` | 502 |
| `#share` | 509 |
| `#share-btn` | 510 |
| `#a11y` | 513 |
| `#a11y-btn` | 514 |
| `#a11y-menu` | 515 |
| `#theme` | 517 |
| `#palette` | 522 |
| `#labels-on` | 529 |
| `#reference-on` | 537 |
| `#about` | 542 |
| `#about-btn` | 543 |
| `#about-menu` | 544 |
| `#about-src-roads` | 556 |
| `#about-src-services` | 557 |
| `#about-vintage` | 585 |
| `#about-build` | 589 |
| `#about-lot-acres` | 594 |
| `#about-modelled-roads` | 605 |
| `#about-modelled` | 627 |
| `#about-budget` | 637 |
| `#about-budget-lead` | 639 |
| `#about-budget-rows` | 640 |
| `#about-budget-note` | 641 |
| `#about-updated` | 653 |
| `#botleft` | 657 |
| `#compass` | 658 |
| `#rot-ccw` | 659 |
| `#tonorth` | 666 |
| `#needle` | 668 |
| `#rot-cw` | 673 |
| `#viewbtns` | 681 |
| `#recenter` | 683 |
| `#center2d` | 684 |
| `#legend` | 686 |
| `#legend-label` | 687 |
| `#legend-min` | 689 |
| `#legend-max` | 689 |
| `#legend-cats` | 691 |
| `#revmix` | 5643 |
| `#svccost` | 5737 |
