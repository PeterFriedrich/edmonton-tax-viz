# CODEMAP — `web/index.html`

**Generated — do not hand-edit.** `python tools/codemap.py`

`web/index.html` is a single ~8,840-line file holding the whole front end. This is the lookup table for it: jump to a symbol's range instead of scanning. **Line numbers go stale on the next edit — regenerate rather than citing them.** Prose should still name symbols, not lines.

## Symbols (323 indexed)

Grouped by the file's own `// --- section ---` banners, in file order.

### tunables

| symbol | lines | what it does |
|---|---|---|
| `THEMED` | 733–733 | Colours that depend on the backdrop, one value per theme (docs/UI.md → |
| `themed` | 734–734 |  |
| `tc` | 735–740 |  |
| `CENTER` | 741–745 |  |
| `HOME` | 746–746 | The default framing — single source for the map constructor and the two |
| `HOME_2D` | 747–760 |  |
| `WINDOWS` | 761–786 | Every user-facing year range on the page derives from this block — lens |
| `CELLS` | 787–796 | Grid cell edges, in metres — the same pinning problem as WINDOWS, so the |
| `glassCellLabel` | 797–801 | Prose that describes the grid ON SCREEN, as opposed to naming a button. |
| `TOKENS` | 802–877 | Static tooltips carry {{key}} placeholders so the markup stays readable |
| `money0` | 878–880 | Per-metric display config. The clamp (colour saturation) sits at the same |
| `fmtMoney` | 881–882 |  |
| `METRICS` | 883–1002 |  |

### services lens views (SPEC_services.md display architecture)

| symbol | lines | what it does |
|---|---|---|
| `RATIO_DENOMS` | 1003–1036 | Ratio view: revenue_per_acre / <service per acre> — the acres cancel, |
| `ratioDenom` | 1037–1037 |  |
| `ratioOf` | 1038–1038 |  |
| `ratioKept` | 1039–1060 |  |

### uses view (use-mix, 2026-07-03)

| symbol | lines | what it does |
|---|---|---|
| `USE_CATEGORIES` | 1061–1073 | uses view (use-mix, 2026-07-03) |
| `USE_BY_KEY` | 1074–1101 |  |
| `dominantUse` | 1102–1143 | Largest composition share wins (ties: first in USE_CATEGORIES order). |

### services view (SPEC_services.md UI generalization, 2026-07-05)

| symbol | lines | what it does |
|---|---|---|
| `SERVICES` | 1144–1294 | services view (SPEC_services.md UI generalization, 2026-07-05) |
| `VIEWS` | 1295–1390 | Per-view chrome. money's title/blurb stay metric-driven (METRICS). |

### the Lab: a container for unfinished lenses

| symbol | lines | what it does |
|---|---|---|
| `LAB_EXPERIMENTS` | 1391–1395 | the Lab: a container for unfinished lenses |
| `inLab` | 1396–1397 |  |
| `DEVIATION_TITLES` | 1398–1402 |  |
| `deviationTitle` | 1403–1408 |  |
| `deviationKind` | 1409–1411 | "Peers", not "the Citywide Average", on the two split cuts: they are |
| `deviationPeers` | 1412–1419 |  |
| `changeBlurb` | 1420–1437 | Change-lens blurb (COPY_DECISIONS BC1, B8 shape). It follows the window |
| `glassLead` | 1438–1450 | Grid blurb (COPY_DECISIONS BG1, B8 shape). Names the metric (B6) and the |
| `glassInstBlurb` | 1451–1463 | The azure cells need a sentence for the same reason the Lab's outlined |
| `ratioInstBlurb` | 1464–1472 | Ratio's azure needs the same sentence as Glass's, for the same reason |
| `ratioBlurb` | 1473–1481 | Ratio blurb (COPY_DECISIONS BR1, B8 shape): the denominator's P1, a |
| `amenityWhichPhrase` | 1482–1487 | Phrase it as what KEEPS the highlight. The negative form does not |
| `glassBlurb` | 1488–1495 |  |
| `infillAmenityBlurb` | 1496–1509 | Infill's amenity overlay carries no colour of its own to defend — the |
| `usesBlurb` | 1510–1521 | Uses blurb: the base zoning caveat, plus the height sentence while the |
| `devTitle` | 1522–1527 | Development blurb, in the COPY_DECISIONS B8 shape (BD1): what the lens |
| `devBlurb` | 1528–1589 |  |
| `setBlurb` | 1590–1604 | Blurb markup (COPY_DECISIONS B8): a blank line starts a new paragraph and |
| `currentBlurb` | 1605–1620 | The active view's blurb. Read by applyView and by the camera's 2D/3D flip |
| `withColourClause` | 1621–1638 | The money/glass blurbs describe the colour transform in prose ("colour is |
| `GRID_URLS` | 1639–1645 | Glass view's spike layer: pipeline-binned 100 m cells (export_value_grid |
| `gridDetailButton` | 1646–1659 | The Detail button that selects a resolution, for the busy state in |
| `gridBytes` | 1660–1660 | Transfer size of a lazy grid, read from the network rather than written |
| `gridSize` | 1661–1675 |  |
| `fmtMB` | 1676–1686 |  |
| `showGridBusy` | 1687–1709 | The in-button sweep says WHICH control is busy; this says THAT the app is |
| `hideGridBusy` | 1710–1726 |  |
| `loadGridData` | 1727–1780 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `ensureGridData` | 1781–1834 | Infill reads the grid too (amenity bands), but it is not in Money's Detail |
| `warmGrid` | 1835–1859 | Speculative warm of a resolution the reader has not committed to. Silent |
| `state` | 1860–1892 | Active metric defaults to revenue (matches the static HTML chrome above). |
| `gridStore` | 1893–1893 |  |
| `gridFetches` | 1894–1920 |  |
| `RAMPS` | 1921–1973 | Three neutral, luminance-sequential ramps to compare: dark = low, bright = |
| `THEME_RAMPS` | 1974–2008 | The ramps for a light backdrop, per theme (docs/UI.md → Light mode, phase |
| `activeRamp` | 2009–2022 | The ramp actually drawn: the palette choice under the current theme. |
| `rampSetAside` | 2023–2035 | The set-aside colour beside a RAMP-coloured surface. Only where the |
| `lotKey` | 2036–2036 | The metric's lot-acre column name (value_per_acre -> value_per_lot_acre). |
| `gridColKey` | 2037–2043 |  |
| `AMENITY_BANDS` | 2044–2045 | Amenity bands (SPEC_development.md "Amenity distance"). ⚠️ CONVENTIONS, |
| `amenityOfferable` | 2046–2048 | Whether a row can be offered at all: the column has to be in the file. |
| `amenityActive` | 2049–2054 | Whether any band is actually filtering right now. |
| `amenityInBand` | 2055–2069 | A cell is in band when it clears EVERY active band. ⚠️ A null distance |
| `gridCellsFor` | 2070–2075 | The cells actually drawn for a column, cached so the layer's data |
| `moneyColKey` | 2076–2094 |  |
| `gridScale` | 2095–2115 | Glass grid scale anchors, per metric + denominator, computed once from |
| `scaleT` | 2116–2122 | Colour transform of the clamped ratio, per metric (FINDINGS §6.1 / §6.3): |
| `rampColorAt` | 2123–2134 | Interpolate the active ramp at t in [0,1]. |
| `colorFor` | 2135–2137 |  |
| `quantile` | 2138–2152 | Linear-interpolated quantile of a pre-sorted array. |
| `moneyScale` | 2153–2187 |  |
| `moneyBlurb` | 2188–2199 | The money blurb (COPY_DECISIONS BM1, B8 shape): the metric's own P1 under |
| `fillFor` | 2200–2212 | Per-feature fill: set-aside hoods grey, everything else the ramp colour at |
| `legendGradient` | 2213–2266 | Legend gradient for the CURRENT ramp under the CURRENT view's transform: |

### base map (no basemap tiles for v1 — just a dark backdrop)

| symbol | lines | what it does |
|---|---|---|
| `GRID_INK` | 2267–2267 |  |
| `gridName` | 2268–2281 |  |
| `paintBackdrop` | 2282–2320 | The backdrop's three MapLibre layers, after a theme or ramp change. |

### loading overlay

| symbol | lines | what it does |
|---|---|---|
| `framePainted` | 2321–2321 | Resolve-only. A failure calls failLoading() directly rather than |
| `basemapReady` | 2322–2348 |  |
| `failLoading` | 2349–2362 |  |
| `hideLoading` | 2363–2418 |  |
| `topRings` | 2419–2435 | Build the roof ring of each prism: the polygon's exterior ring lifted to |
| `roadLayers` | 2436–2461 | The roads ground layer (services + ratio views). When roads drive the |
| `_svcScales` | 2462–2462 | Per-column service scale anchors, computed once from the data (tracks |
| `svcScale` | 2463–2475 |  |
| `svcT` | 2476–2484 | Clamped ramp position for a plane-service value under its transform. |
| `fmtStorm` | 2485–2498 | All seven dollar readouts below floor through `money0` — a nonzero cost |
| `under2dp` | 2499–2499 |  |
| `fmtFire` | 2500–2501 |  |
| `fmtTransit` | 2502–2503 |  |
| `fmtBike` | 2504–2516 |  |
| `fmtRoadM` | 2517–2530 |  |
| `fmtResShare` | 2531–2533 | ⚠️ "0% of revenue is residential" reads as NOBODY LIVES HERE, and on the |
| `fmtWater` | 2534–2539 |  |
| `fmtRoadsCost` | 2540–2544 | Stage 2 operating-cost readouts. Each says "operating" in the readout |
| `fmtRoadsLife` | 2545–2546 | Same rule one step more important: this is the SAME METRES as |
| `fmtTransitCost` | 2547–2548 |  |
| `fmtBikeCost` | 2549–2560 |  |
| `servicePlaneLayer` | 2561–2593 | The shared service ground plane (services view): flat hoods coloured |
| `DEV_COLS` | 2594–2603 | Development & Infill lens A (SPEC_development.md): a flat hood plane |
| `DEV_TOTAL_COLS` | 2604–2609 |  |
| `DEV_IND_TOTAL` | 2610–2612 | Industrial permit COUNT total per window, for the tooltip (no units total). |
| `devIndustrial` | 2613–2618 | Industrial is a hood-level choropleth, and (since 2026-08-18) also has |
| `devIndCellsPresent` | 2619–2623 | Industrial detail cells exist only if the window actually has geocoded |
| `devGridActive` | 2624–2629 |  |
| `devGridOfferable` | 2630–2631 | Whether the Detail toggle + Spikes picker should be OFFERED (independent of |
| `DEV_WINDOW_LABEL` | 2632–2632 |  |
| `devCol` | 2633–2633 |  |
| `_devScale` | 2634–2634 |  |
| `devScale` | 2635–2641 |  |
| `devT` | 2642–2645 |  |
| `developmentPlaneLayer` | 2646–2662 |  |
| `fmtDev` | 2663–2678 |  |

### Development 100 m detail grid (layers-panel toggle, 2026-07-15)

| symbol | lines | what it does |
|---|---|---|
| `DEV_GRID_COLS` | 2679–2684 |  |
| `DEV_GRID_IND_N` | 2685–2685 | Industrial's companion permit-count column, per window. |
| `devGridColKey` | 2686–2688 |  |
| `devGridScale` | 2689–2715 |  |
| `devGridLayer` | 2716–2764 |  |

### Infill lens (SPEC_development.md Lens B)

| symbol | lines | what it does |
|---|---|---|
| `infillIncluded` | 2765–2766 | Infill lens (SPEC_development.md Lens B) |
| `meanStd` | 2767–2774 |  |
| `_infillStats` | 2775–2775 | Cached per activity column (far stats are constant, activity stats and the |
| `infillStats` | 2776–2793 |  |
| `_infillRaw` | 2794–2796 |  |
| `infillScore` | 2797–2812 | Signed score for a hood (null when excluded), and its clamped t in [-1,1]. |
| `infillOppSuppressed` | 2813–2814 | Asymmetric residential gate (SPEC_development.md Lens B): the OPPORTUNITY |
| `infillT` | 2815–2835 |  |
| `infillColorAt` | 2836–2840 |  |
| `infillPlaneLayer` | 2841–2862 |  |
| `fmtFar` | 2863–2873 | ⚠️ NO FLOOR, DECIDED — do not "fix" this. DECISIONS.md 2026-09-20 closed |
| `amenityHighlightGridLayer` | 2874–2928 |  |

### change lens: how each hood's share of the assessment base moved

| symbol | lines | what it does |
|---|---|---|
| `CHG_WINDOWS` | 2929–2936 | change lens: how each hood's share of the assessment base moved |
| `CHG_WINDOW_LABEL` | 2937–2951 | Pinned in WINDOWS, and still deliberately NOT derived from temporal.json's |
| `changeFor` | 2952–2972 | Endpoint pair + elapsed years for one hood over the active window, or |
| `_chgStats` | 2973–2973 | Per-arm p95 clamps, cached per window. Per-arm for the same structural |
| `chgStats` | 2974–2988 |  |
| `chgT` | 2989–2998 | Clamped t in [-1,1]; null = off the scale (no baseline, or no history). |
| `fmtChg` | 2999–3029 | Two decimals: the median hood's rate is well under 1%/yr, and one decimal |
| `changePrismLayer` | 3030–3118 |  |

### deviation lens: revenue per developed acre against peer average

| symbol | lines | what it does |
|---|---|---|
| `DEVIATION_POP` | 3119–3126 | deviation lens: revenue per developed acre against peer average |
| `devAcreFrac` | 3127–3127 | Guard sf >= 1: two hoods are 100% set-aside, and both are already |
| `inDeviationPop` | 3128–3135 |  |
| `deviationRate` | 3136–3179 | The hood's own rate on the developed base. The boundary acreage cancels |

### the institutional uncertainty band

| symbol | lines | what it does |
|---|---|---|
| `exemptFrac` | 3180–3209 |  |

### two tiers, answering two different questions

| symbol | lines | what it does |
|---|---|---|
| `deviationBandRaw` | 3210–3216 | Ordered so `deviationStats` can run without touching `isUncertain` — it |
| `instShiftDeviation` | 3217–3228 | Distance between the two worlds on the LEVIED world's ramp — the one |
| `isUncertain` | 3229–3232 | ⚠️ This selection contains every band that CROSSES ZERO on today's data |
| `instCaveatOnly` | 3233–3237 | Caveat without the range: ≥25% institutional, but the two worlds draw the |
| `deviationBandedCount` | 3238–3248 | Counted out here rather than inside deviationStats, which the shift now |
| `instShiftMoney` | 3249–3264 | The same question on the Money ramp. ⚠️ FIXED TRANSFORM, deliberately NOT |
| `instBandedMoney` | 3265–3296 | Money's outlined hoods: the caveat tier, narrowed to the ones whose two |
| `instBandedRatio` | 3297–3374 | Ratio's band (Peter, 2026-09-12: the lens "doesn't line up color wise |
| `isBandLayer` | 3375–3379 |  |
| `bandHover` | 3380–3388 | ⚠️ Clones the LIVE layers instead of calling buildLayers(). A rebuild would |
| `instBandLayers` | 3389–3491 |  |

### the same doubt, at 100 m

| symbol | lines | what it does |
|---|---|---|
| `glassInstCells` | 3492–3499 | ⚠️ THE RAMP FILL SURVIVES HERE, WHICH MONEY'S BAND DELIBERATELY DOES NOT |
| `glassInstCount` | 3500–3501 |  |
| `glassInstBandLayers` | 3502–3542 |  |
| `ratioInstBandLayers` | 3543–3570 | Ratio's pair. ⚠️ SHAPED ON GLASS, NOT ON MONEY, because Ratio is a |
| `deviationRateExempt` | 3571–3583 | The rate with institutional revenue removed — the other coherent world. |
| `deviationBand` | 3584–3585 | Both endpoints as deviations, each against ITS OWN scenario average. |
| `deviationBandSpan` | 3586–3587 | Ordered for display, so a printed range never reads high-to-low. |
| `_devStats` | 3588–3588 |  |
| `deviationStats` | 3589–3633 |  |
| `deviationOf` | 3634–3635 |  |
| `deviationT` | 3636–3646 |  |
| `fmtDeviation` | 3647–3668 | Signed money, minus sign carried OUTSIDE the dollar sign ("−$4,120", not |
| `deviationLayer` | 3669–3712 | ⚠️ EXTRUDED, AND THE DEFICIT HALF EXTRUDES DOWNWARD. deck.gl 9.0.38 |
| `deviationBandLayers` | 3713–3799 | The two endpoints of every banded hood, as bare OUTLINES — one layer per |
| `deviationBlurb` | 3800–3824 | ⚠️ KEEP THIS SHORT. Development's and Infill's blurbs are 442px and 479px |
| `fireStationsLayer` | 3825–3845 |  |
| `ensureFireStations` | 3846–3862 |  |
| `transitStationsLayer` | 3863–3880 |  |
| `ensureTransitStations` | 3881–3897 |  |
| `lrtLinesLayer` | 3898–3914 |  |
| `ensureLrtLines` | 3915–3932 |  |
| `bikeLinesLayer` | 3933–3949 |  |
| `ensureBikeLines` | 3950–4036 |  |

### geographic reference layers (all views)

| symbol | lines | what it does |
|---|---|---|
| `referenceSplit` | 4037–4064 |  |
| `referenceUnderLayers` | 4065–4099 | Bottom of the stack: the water, under everything the map draws. |
| `boundaryLayer` | 4100–4116 | One constant-styled outline layer. Returns [] for an empty collection so |
| `referenceOverLayers` | 4117–4136 | Top of the stack: the highways, over the data they help locate. |
| `ensureReference` | 4137–4151 |  |
| `servicesBlurb` | 4152–4163 | Services-view blurb (COPY_DECISIONS BS1, B8 shape): the colour-driving |
| `hoodHoverLayer` | 4164–4187 | Flat invisible hood layer for the services/ratio views: keeps the hood |
| `_measureEm` | 4188–4198 | True rendered width of a name, in ems (multiply by the label size for |
| `labelAnchors` | 4199–4250 |  |
| `REF_TIERS` | 4251–4272 | Per-tier text style. `base` feeds placeSize(), which scales it with the |
| `placeSize` | 4273–4281 | `base` is the tier's full size (REF_TIERS), defaulted to PLACE_SIZE so the |
| `placeAnchors` | 4282–4305 |  |
| `labelPool` | 4306–4313 | The pool the declutterer sweeps: each class gated by its OWN toggle, so |
| `labelZ` | 4314–4367 |  |
| `CHROME_IDS` | 4368–4372 | The HTML chrome the labels have to dodge. The sweep declutters labels |
| `chromeBoxes` | 4373–4391 |  |
| `visibleLabels` | 4392–4446 |  |
| `labelLayer` | 4447–4501 | The labels layer (all views, toggled from the lens panel). Billboarded |
| `withSelectedHood` | 4502–4542 |  |
| `_ratioScales` | 4543–4543 | Ratio-view scale anchors, computed once per DENOMINATOR from its kept |
| `ratioScale` | 4544–4559 |  |
| `ratioT` | 4560–4582 |  |
| `zMatrix` | 4583–4587 |  |
| `buildLayers` | 4588–4612 |  |
| `flattenDuringEase` | 4613–4637 | Center 2D lowers the heights over the LAST QUARTER OF THE TILT instead |
| `buildViewLayers` | 4638–4952 |  |

### money view (default): the classic metric prisms

| symbol | lines | what it does |
|---|---|---|
| `esc` | 4953–4982 | Entity-escape untrusted data-derived strings before they go into the |

### temporal lens (SPEC_temporal.md phase 3)

| symbol | lines | what it does |
|---|---|---|
| `TEMPORAL_SERIES` | 4983–4992 | temporal lens (SPEC_temporal.md phase 3) |
| `fmtPct` | 4993–4995 | Two decimals, so the floor is "<0.01%" where `fmtMix`'s one decimal |
| `fmtBig` | 4996–5027 | Assessment totals run $10M-$10B across hoods, so the unit has to follow |

### Money's revenue panel: where a hood's levy comes from

| symbol | lines | what it does |
|---|---|---|
| `fmtMix` | 5028–5034 | Sub-0.1% shares print as "<0.1%", never a rounded "0.0%" — a category that |
| `fmtLevy` | 5035–5042 | ⚠️ NOT fmtBig, which is calibrated for ASSESSMENT totals ($10M-$10B) and |
| `revenueMix` | 5043–5047 | Every non-zero category, largest first. Nothing is dropped as noise here: |
| `hoodProps` | 5048–5058 |  |
| `revenueLens` | 5059–5060 | Where the panel shows the breakdown instead of the history. Two tests, |
| `revenuePanelFor` | 5061–5093 |  |
| `SVC_COST_BASES` | 5094–5111 | The Services panel: this hood's revenue per acre set against what the City |
| `SVC_FAMILY` | 5112–5120 | A layer and its cost twin measure the same subject two ways, so the panel |
| `NO_SVC_COST` | 5121–5130 | Why the family has no cost, in the service's own terms. ⚠️ Each states a |
| `SVC_OPS_NOTE` | 5131–5133 | ⚠️ Exposed by scoping the panel to one family: the operating group's note |
| `SVC_FAMILY_COST` | 5134–5140 |  |
| `svcRank` | 5141–5145 | 1 = highest. Ranked over the hoods that HAVE the column, not over all 406, |
| `ordSuffix` | 5146–5152 |  |
| `svcDriverReading` | 5153–5173 | What the colour-driving service measures for this hood, as a number and as |
| `serviceLens` | 5174–5174 | Lens test and per-hood test kept separate, the same split revenueLens / |
| `svcCostRows` | 5175–5178 |  |
| `servicePanelFor` | 5179–5183 |  |
| `ratioPanelFor` | 5184–5207 | Ratio carries the cost-as-a-share-of-tax panel that Services had until |
| `hoodPanelLens` | 5208–5212 | Whether the pinned-hood PANEL applies to the current view. Services now has |
| `temporalFor` | 5213–5230 | Decoded series for one hood, or null when the lens can't speak for it |
| `temporalGeom` | 5231–5262 | Point coordinates plus the run boundaries, shared by both renderers so the |
| `runPath` | 5263–5268 |  |
| `sparklineSvg` | 5269–5284 | The hover teaser: line + a dot on the latest point. No axes, no band |
| `temporalChartSvg` | 5285–5344 | The pinned chart: same geometry, plus the things only a 300px box can |

### Development history: new supply per year

| symbol | lines | what it does |
|---|---|---|
| `DEVH_SERIES` | 5345–5350 | Development history: new supply per year |
| `devHistKey` | 5351–5360 | Which series the panel and teaser read, following the Development |
| `DEVH_NOUN` | 5361–5365 | Singular, plural, and the VERB each series takes. The verb is per-series |
| `devHistNoun` | 5366–5366 |  |
| `devHistVerb` | 5367–5372 |  |
| `devHistoryFor` | 5373–5411 | One hood's series for the ACTIVE sub-metric, or null when the lens cannot |
| `devHistGeom` | 5412–5431 | Column geometry. Zero-based by construction: every bar starts at the |
| `devHistSparkSvg` | 5432–5451 | The hover teaser. No axes and no labels at 28px — the muted row beneath it |
| `devHistChartSvg` | 5452–5487 | The pinned chart: same columns plus what a 300px box can hold — a peak |
| `devHistoryPanelFor` | 5488–5490 | Where the panel shows new supply over time instead of the history or the |
| `renderDevHistory` | 5491–5554 |  |
| `syncTemporalPos` | 5555–5581 |  |
| `openTemporal` | 5582–5619 |  |
| `renderRevenueMix` | 5620–5689 | Where the hood's levy comes from, by the zoning of each property. The |
| `renderRatioCost` | 5690–5764 | Revenue is the reference and every bar is a fraction OF IT, rather than the |
| `renderServiceCost` | 5765–5822 | The Services panel: what each cost IS for this hood, in dollars, and where |
| `fmtSvcRatio` | 5823–5826 | Under 10% the ratio rounds to "0%" for three of the four services, which |
| `renderHistory` | 5827–5877 |  |
| `syncPinnedPanel` | 5878–5911 | The panel's CONTENT is lens-dependent now, so a metric or view switch |
| `closeTemporal` | 5912–5927 | Un-pin. In PANEL mode the panel stays up showing its prompt, because the |
| `syncHoodModePod` | 5928–5945 | The readout-mode pod is offered only where BOTH destinations exist: the |
| `applyHoodMode` | 5946–5993 | Where a hood's detail appears. Leaving panel mode takes the panel with it; |
| `noHover` | 5994–5999 | A finger cannot hover, so touch needs a stage the mouse gets for free. |
| `openPeek` | 6000–6047 | The touch-only preview: the view's headline number for one hood, and an |
| `closePeek` | 6048–6064 |  |
| `temporalClick` | 6065–6119 | Click a hood to pin its history; click the pinned one again to unpin. |

### neighbourhood search

| symbol | lines | what it does |
|---|---|---|
| `searchNorm` | 6120–6127 | neighbourhood search |
| `searchMatches` | 6128–6142 | Ranked: the name starts with the query, then a later WORD does (so |
| `renderSearchList` | 6143–6171 |  |
| `openSearch` | 6172–6184 |  |
| `closeSearch` | 6185–6203 |  |

### how-to-read guide

| symbol | lines | what it does |
|---|---|---|
| `openGuide` | 6204–6216 |  |
| `closeGuide` | 6217–6224 |  |
| `maybeAutoGuide` | 6225–6241 |  |
| `flyToHood` | 6242–6261 | Keep the current tilt and rotation, so the camera moves TO the hood |
| `pickSearch` | 6262–6280 | A pick reads exactly like tapping or clicking the hood (temporalClick |
| `primaryRow` | 6281–6349 | Panel mode's one-line hover: the view's HEADLINE number and nothing else, |
| `viewTooltip` | 6350–6727 | Tooltip content is per-view (closure over `state`) and, inside money, |
| `tooltipFor` | 6728–6817 | The sparkline rides on every tooltip WHOSE PANEL IS THE HISTORY PANEL |
| `REV_CUTS` | 6818–6818 | Switch metric: rebuild layers and update the title/legend/toggle chrome. |
| `isRevenue` | 6819–6837 |  |
| `syncMetricButtons` | 6838–6861 | Paint the metric row and whichever row 2 belongs to it — the cuts under |
| `MILL_CUT_CLASSES` | 6862–6868 | Which classes each revenue cut is actually billed at |
| `MILL_LABELS` | 6869–6882 | Abbreviated so all three rates fit ONE line at the title's width. Every |
| `renderBudgetContext` | 6883–6924 | The Data & Methods pod's citywide budget-scale section (2026-08-03). |

### the citywide budget panel (EXPERIMENTAL, full build only)

| symbol | lines | what it does |
|---|---|---|
| `renderBudgetPanel` | 6925–6967 |  |
| `toggleBudgetPanel` | 6968–6993 |  |
| `syncMillRates` | 6994–7026 | Paint the pod, gate it to the money view's revenue cuts, and place it. |

### control appliers + the view/legend dispatchers

| symbol | lines | what it does |
|---|---|---|
| `applyMetric` | 7027–7047 |  |
| `applyColorAdjust` | 7048–7068 | Colour Adjustment (sqrt scaling) — a runtime toggle for the money/glass |
| `syncColorAdjust` | 7069–7081 | Sync the Colour Adjustment button to the toggle, and HIDE it in views |
| `applyDenom` | 7082–7096 | Switch the denominator (ground vs lot acres). Shown in the Glass and |
| `applyRatioDenom` | 7097–7114 | Switch the Ratio view's denominator (per road metre vs per fire event). |
| `applyDevMetric` | 7115–7131 | Development sub-metric picker (dwelling units \| permits \| industrial). |
| `syncDevChrome` | 7132–7153 | Shared development-view chrome refresh after a metric/window switch: the |
| `applyDevWindow` | 7154–7170 | Development-view window toggle (5yr base <-> 3yr recent <-> since 2009). |
| `refreshLegend` | 7171–7410 | Sync the whole legend to the current view. roads: the network's linear |
| `usesLegendCats` | 7411–7423 | Legend rows for the uses view: the categories actually on screen |
| `applyTheme` | 7424–7438 | Switch theme. Every tc() colour and the ramp (activeRamp) are re-read on |
| `syncThemeChrome` | 7439–7449 | The theme's wording and buttons outside the map. Also run once at boot, |
| `applyPalette` | 7450–7464 | Switch colour ramp: rebuild layers, restyle the background + legend gradient. |
| `applyLabels` | 7465–7473 | Toggle the neighbourhood-name labels (accessibility-menu checkbox). |
| `applyReference` | 7474–7484 | Toggle the orientation set: river, ring road, and the regional place |
| `applyUsesPrisms` | 7485–7496 | Toggle the Uses view's residential prisms (height = share of zoned |
| `applyAmenity` | 7497–7509 | Toggle one amenity band. Infill only — the rows are hidden elsewhere and |
| `syncAmenityControls` | 7510–7530 | Show the amenity section in Infill only (2026-08-26 — Glass reads the |
| `syncDevControls` | 7531–7578 | Sync the Development pickers' visibility to the current mode. The |
| `syncPrismRow` | 7579–7584 | The age spikes ride on the Glass grid file — kick its (shared, single) |
| `applyDevDetail` | 7585–7606 |  |
| `applyMoneyDetail` | 7607–7631 | Money's render toggle: Neighbourhood prisms (view "money") vs the |
| `syncMoneyDetail` | 7632–7643 | The Detail row's active button. Three buttons over two views, so the grid |
| `applyMoneyMode` | 7644–7651 | Money's Current/Change lens toggle. Change is a full-only render-mode of |
| `applyChgWindow` | 7652–7670 | Switch the change lens's window. State-only when the lens isn't on screen, |
| `syncChangeControls` | 7671–7681 | Reveal the change window picker, and re-run the metric rows that host the |
| `applyDevMode` | 7682–7689 | Development's Housing/Infill lens toggle (full build only). Infill is a |
| `syncLabControls` | 7690–7706 | The Lab's controls: the experiment picker (only once there are two — see |
| `applyLabCut` | 7707–7720 | Switch the deviation experiment's revenue cut. Its average, per-arm |
| `setPrismOpacity` | 7721–7731 | Set the ratio view's ghost-prism opacity (0–100). UI-state only — the |
| `applyView` | 7732–7975 | Switch view (money \| services \| ratio \| uses \| glass). Road geometry |
| `syncServiceControls` | 7976–7985 | Services-view controls. `applyService` flips a service on/off; |
| `applyService` | 7986–7999 |  |
| `applySvcDriver` | 8000–8032 |  |

### shareable URL: the hash names the view on screen

| symbol | lines | what it does |
|---|---|---|
| `METRIC_FROM_URL` | 8033–8035 |  |
| `urlHash` | 8036–8076 |  |
| `shareLink` | 8077–8085 | Absolute on purpose: the full build carries <base href="../">, and a |
| `copyShareLink` | 8086–8097 | With no clipboard (an insecure origin, a denied permission) the link goes |
| `offered` | 8098–8104 | On screen, ignoring the Options fold: a folded panel on a phone hides |
| `applyUrlState` | 8105–8177 |  |
| `restoreFromHash` | 8178–8196 | Once, at the end of boot, after every build and data gate has run. The |

### boot

| symbol | lines | what it does |
|---|---|---|
| `boot` | 8197–8840 | Everything that needs the map surface: fetch the data, mount the deck.gl |

## Dependency graph (1095 edges)

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
| tunables | 15 | 53% |
| Infill lens (SPEC_development.md Lens B) | 27 | 52% |
| uses view (use-mix, 2026-07-03) | 4 | 50% |
| deviation lens: revenue per developed acre against peer average | 4 | 50% |
| change lens: how each hood's share of the assessment base moved | 16 | 44% |
| base map (no basemap tiles for v1 — just a dark backdrop) | 5 | 40% |
| Development 100 m detail grid (layers-panel toggle, 2026-07-15) | 10 | 40% |
| neighbourhood search | 11 | 36% |
| geographic reference layers (all views) | 97 | 35% |
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
| `#title-p` | 86 |
| `#search` | 96 |
| `#search-btn` | 97 |
| `#search-box` | 100 |
| `#search-input` | 101 |
| `#search-close` | 105 |
| `#search-list` | 107 |
| `#guide-btn` | 115 |
| `#guide` | 117 |
| `#guide-close` | 118 |
| `#guide-ask` | 119 |
| `#guide-show` | 120 |
| `#guide-body` | 123 |
| `#temporal` | 142 |
| `#temporal-close` | 143 |
| `#temporal-name` | 144 |
| `#temporal-body` | 151 |
| `#temporal-chart` | 152 |
| `#temporal-read` | 153 |
| `#temporal-note` | 154 |
| `#temporal-hint` | 158 |
| `#millrates` | 174 |
| `#mill-head` | 175 |
| `#mill-rows` | 176 |
| `#mill-note` | 177 |
| `#budget` | 191 |
| `#budget-close` | 198 |
| `#budget-head` | 199 |
| `#budget-body` | 204 |
| `#budget-rows` | 205 |
| `#budget-other-hd` | 206 |
| `#budget-other` | 207 |
| `#budget-note` | 208 |
| `#peek` | 223 |
| `#peek-name` | 224 |
| `#peek-read` | 225 |
| `#peek-go` | 226 |
| `#controls` | 229 |
| `#toggle` | 242 |
| `#metric-row` | 243 |
| `#revcut` | 247 |
| `#moneymode` | 252 |
| `#views` | 258 |
| `#optpanel` | 272 |
| `#opt-fold` | 273 |
| `#opt-caret` | 273 |
| `#opt-body` | 274 |
| `#layers` | 275 |
| `#chgwindow-hd` | 276 |
| `#chgwindow` | 277 |
| `#labpick-hd` | 286 |
| `#labpick` | 287 |
| `#labcut-hd` | 288 |
| `#labcut` | 289 |
| `#moneydetail-hd` | 294 |
| `#moneydetail` | 295 |
| `#amenity-hd` | 320 |
| `#amenity` | 321 |
| `#amenity-lrt-row` | 322 |
| `#amenity-lrt-on` | 323 |
| `#amenity-school-row` | 325 |
| `#amenity-school-on` | 326 |
| `#uses-prisms-hd` | 329 |
| `#uses-prisms` | 330 |
| `#uses-prisms-on` | 332 |
| `#devmode-hd` | 335 |
| `#devmode` | 336 |
| `#devmetric-hd` | 340 |
| `#devmetric` | 341 |
| `#devwindow-hd` | 346 |
| `#devwindow` | 347 |
| `#devdetail-hd` | 352 |
| `#devdetail` | 353 |
| `#prism-hd` | 357 |
| `#prism-row` | 358 |
| `#prism-opacity` | 360 |
| `#prism-opacity-val` | 361 |
| `#services-hd` | 363 |
| `#services` | 364 |
| `#denom-hd` | 463 |
| `#denom` | 464 |
| `#ratio-denom-hd` | 468 |
| `#ratio-denom` | 469 |
| `#hoodmode` | 479 |
| `#hoodmode-btn` | 480 |
| `#coloradj` | 492 |
| `#coloradj-btn` | 493 |
| `#budget-pod` | 500 |
| `#budget-btn` | 501 |
| `#share` | 508 |
| `#share-btn` | 509 |
| `#a11y` | 512 |
| `#a11y-btn` | 513 |
| `#a11y-menu` | 514 |
| `#theme` | 516 |
| `#palette` | 521 |
| `#labels-on` | 528 |
| `#reference-on` | 536 |
| `#about` | 541 |
| `#about-btn` | 542 |
| `#about-menu` | 543 |
| `#about-src-roads` | 555 |
| `#about-src-services` | 556 |
| `#about-vintage` | 584 |
| `#about-build` | 588 |
| `#about-lot-acres` | 593 |
| `#about-modelled-roads` | 604 |
| `#about-modelled` | 626 |
| `#about-budget` | 636 |
| `#about-budget-lead` | 638 |
| `#about-budget-rows` | 639 |
| `#about-budget-note` | 640 |
| `#about-updated` | 652 |
| `#botleft` | 656 |
| `#compass` | 657 |
| `#rot-ccw` | 658 |
| `#tonorth` | 665 |
| `#needle` | 667 |
| `#rot-cw` | 672 |
| `#viewbtns` | 680 |
| `#recenter` | 682 |
| `#center2d` | 683 |
| `#legend` | 685 |
| `#legend-label` | 686 |
| `#legend-min` | 688 |
| `#legend-max` | 688 |
| `#legend-cats` | 690 |
| `#revmix` | 5639 |
| `#svccost` | 5733 |
