# SPIKE — Capital-region peer-municipality comparison (St. Albert, Strathcona County)

**Date:** 2026-07-17 (data pulled live this date)
**Status:** Spike complete. Feasibility CONFIRMED for a citywide-aggregate
comparison; no build started. Phase 2 / appendix-tier — not November scope.
**Scope of this doc:** data-source facts + feasibility verdict only. Lens
design (output form, copy, methodology) is NOT decided here.

---

## Verdict (the two questions the spike was run to answer)

1. **Is a lightweight citywide value-per-acre comparison feasible?** Yes — for
   both municipalities, today, with no new tooling beyond a second (ArcGIS)
   fetch path. But the two sources are NOT symmetric:
   - **St. Albert is the strong leg**: full multi-class roll, parcel
     **polygons**, assessed value **and actual tax levy** per parcel. It
     supports everything the Edmonton pipeline does — a real per-parcel
     revenue-per-acre calc, no mill-rate modeling needed.
   - **Strathcona is the weak leg**: residential-improved properties only,
     **point** geometry (all vintages checked), assessed value only (no levy,
     no class field). Lot area exists as an attribute (`parcelarea`), so a
     *residential lot-acre* value density is computable, but any "revenue"
     number requires applying the published mill rate as a modeled assumption,
     and non-residential is absent entirely.
2. **Geometry vintage (Strathcona)?** Centroids, not polygons — confirmed on
   2026 and 2024; the schema is identical across recent vintages. Ground-acre
   (Edmonton-grid-style) calcs are NOT possible for Strathcona; lot-acre calcs
   are (from the `parcelarea` attribute).

**Denominator constraint for any comparison:** Edmonton's headline grid metric
is *ground* acres; Strathcona can only do *lot* acres. A like-for-like
citywide comparison must use the lot-acre basis on all three sides (Edmonton
has deduped lot acres already) — or St. Albert + Edmonton only if ground-acre.

---

## Municipality 1: St. Albert — the key find

The on-prem server in the planning brief
(`gis.stalbert.ca/.../COSA_PUBd_LandscapePropInfo_3TM/MapServer/0`) is
**decommissioned** — it now blanket-301s to an ArcGIS Online web app. The
service moved to ArcGIS Online, org `fyyY0cNXvmUWvX1x` ("City of St. Albert"):

- **Current-year service:** `LandscapePropertyInfo2026`
  `https://services1.arcgis.com/fyyY0cNXvmUWvX1x/arcgis/rest/services/LandscapePropertyInfo2026/FeatureServer/0`
  — **29,366 records** (answers the brief's parcel-count question),
  `maxRecordCount: 2000` → 15 paginated calls (`resultOffset` +
  `orderByFields=OBJECTID`).
- **Prior year also up:** `LandscapeTaxAssessment2025_view` (28,883 records,
  same schema). Only these two years found in the org; no deep archive like
  Strathcona's.
- **Geometry:** `esriGeometryPolygon` — real parcel boundaries. Spatial ref
  **wkid 102187 / EPSG:3776** (NAD83 / Alberta 3TM ref. merid. 114°W), not the
  3780 in the brief — reproject to the project's EPSG:3400 on ingest.
- **Fields (all confirmed live):** `Roll_Number`, `Address`, `Neighbourhood`,
  `LanduseDistrict`, `Year_Built`, `Property_Class`, `Assessment_Class`
  (numeric code), `Assessment_Description` (human label), `LotSize_sqm`,
  `Assessment_Year`, **`Assessed_Value`**, **`CurrentTaxLevy`**, legal-plan
  and ATS fields, `Shape__Area`/`Shape__Length`.
- **Server-side statistics work** (`outStatistics` + `groupByFieldsForStatistics`)
  — citywide aggregates need no bulk download at all.

### Citywide anchors (2026 roll, pulled 2026-07-17 via server-side stats)

| | n | Assessed value | Tax levy (total bill) |
|---|---|---|---|
| All classes | 29,366 | $18.26 B | $197.3 M |
| Class 1 single family | 19,557 | $10.93 B | $121.2 M |
| Class 2 commercial (taxable) | 451 | $1.18 B | $20.7 M |
| Class 2 industrial (taxable) | 347 | $0.77 B | $13.5 M |

Exempt classes (schools, institutional, city reserves) carry assessed value
with `CurrentTaxLevy = 0` — a real zero, mirrors Edmonton's exempt handling.

### `CurrentTaxLevy` is the TOTAL bill (validated)

Effective rate = levy/value per class, computed from the data:
residential classes → **11.077–11.089 /$1000** (the published 2026 total
residential rate is 11.07666 — matches; single-family's extra 0.012 is
rounding + minimum-tax noise); commercial & industrial → **17.58685 /$1000**.
That settles the brief's open question #1: **St. Albert total non-residential
rate (municipal 13.39 + education + Heartland) ≈ 17.587 /$1000.** It also
means municipal-only comparisons must back the education share out (rate
arithmetic), same as Edmonton's levy decomposition.

---

## Municipality 2: Strathcona County

- **Annual snapshots 2012–2026** (14 services, one per tax year — 2016 absent),
  org `B7ZrK1Hv4P1dsm9R`, hub `opendata-strathconacounty.hub.arcgis.com`.
  2026 item id `211214c329394005a5a3c43a277b0d38`; 2026 layer:
  `https://services.arcgis.com/B7ZrK1Hv4P1dsm9R/arcgis/rest/services/2026%20Property%20Tax%20Assessment/FeatureServer/0`
  — **43,365 records**, `maxRecordCount: 1000` (44 paginated calls; full
  attribute pull takes ~1 min, done this spike).
- **Geometry: POINT in every vintage checked (2026, 2024).** The brief's
  polygon hope is dead; `parcelarea` + `measured_in` ("Acres" / "Sq. Mete" /
  "Units") carries lot size as an attribute instead.
- **Fields:** `roll`, `address`, `bldg` (building type), building attributes
  (garage/fireplace/basement), `assess_2025` (assessed value; field name
  embeds the valuation year), `latitude`/`longitude`, `parcelarea`,
  `measured_in`. **No assessment-class field, no levy.**
- **Residential-improved-only confirmed:** every `bldg` value is a dwelling
  type (2 Storey & Basement, Split Entry, Manufactured Home, …); no
  commercial/industrial descriptors; Refinery Row does not appear. The
  county's heavy-industrial base (the fiscally interesting part of Strathcona)
  is NOT in this dataset.

### ⚠️ Duplication hazard — the dataset's landmine

Multi-unit complexes repeat the **whole-building/complex assessed value on
every unit record.** E.g. 6101 Eton Blvd: 259 rows, each $70,717,000 (the
building total); 1040 Iris Evans Wy: 290 rows × $32.2 M. Some complexes do it
across *distinct addresses* (1339/1341/1343 Lakewood Rd… all $33,706,000,
identical 56.46-acre `parcelarea`). Meanwhile OTHER condo complexes (e.g.
Great Oaks) carry honest per-unit values — so dedup can't just collapse
same-address rows, and value-identity keys over-collapse legit twins.

Measured impact (2026 full pull):
- Naive sum of `assess_2025`: **$116.8 B** (absurd)
- Dedup on (base address, value, parcelarea): **$40.6 B** (still inflated —
  misses cross-address complexes)
- Strict dedup on (value, parcelarea, unit): **$21.3 B** — plausible vs the
  county's published residential base, but slightly UNDER-counts (collapses
  coincidentally identical units). **Truth is ~$21–22 B; a careful dedup rule
  is a build-time task.**

Strict-dedup split (assessed value per LOT acre, residential only):
- Urban lots (`Sq. Mete` ≈ Sherwood Park): 22,760 parcels, $13.3 B on
  3,667 lot acres → **~$3.6 M/lot-acre**
- Rural (`Acres`): 7,935 parcels, $6.9 B on 134,294 acres → **~$51 K/acre**
- Modeled municipal residential levy @ 4.5822/$1000 on $21.3 B ≈ **$97.5 M**
  (2026 rate bylaw 4-2026; a modeled assumption, must be disclosed as such).

### Mill rates
2026 rates are in the planning brief (municipal res 4.5822, non-res 10.9933;
totals 7.2770 / 15.0823). Historical table 2015–2026 is server-rendered at
`strathcona.ca/your-property-utilities/property-taxes/tax-payment/tax-rates/`
(plain scrape works — confirmed in the brief's pass, not re-fetched here).

---

## Cross-cutting

- **Fetch path:** both are ArcGIS REST (`resultOffset` pagination,
  `f=json`/`f=geojson`), unlike Edmonton's Socrata — one new loader idiom
  covers both peers. St. Albert additionally supports `outStatistics`
  server-side, so the aggregate-only output may need NO bulk download for SA.
- **Licensing (unresolved, check before committing any data):** Strathcona
  points to `opendata-strathconacounty.hub.arcgis.com/pages/licence` (custom);
  the St. Albert item has NO licenseInfo on the ArcGIS item — their open-data
  terms need locating before any pulled data is committed to the public repo.
  (Derived aggregate *statistics* are lower-risk than redistributing rows, but
  confirm.)
- **Comparability caveats for any output copy:** (a) Strathcona is
  residential-only + modeled levy; (b) mill-rate bundling differs (Strathcona
  Recreation Infrastructure line + Designated Industrial Requisition vs
  flatter structures); (c) valuation-date lag conventions look aligned
  (Strathcona 2026 roll = 2025-07-01 valuation; verify exactly at build time);
  (d) lot-acre vs ground-acre denominators (see Verdict).

## What was NOT done (deliberately)

No pipeline code, no data committed, no methodology chosen. The realistic
scope per the brief remains **(a) a citywide aggregate comparison**; the spike
adds that **St. Albert alone could support (b) a full parallel per-parcel
pipeline** if ever wanted — it is the only peer with polygons + class + levy.
Remaining open items: license terms (both), exact valuation-lag confirmation,
the Strathcona dedup rule, and the actual output design (Peter's call).

## Repro

```bash
# St. Albert schema + count
curl -s "https://services1.arcgis.com/fyyY0cNXvmUWvX1x/arcgis/rest/services/LandscapePropertyInfo2026/FeatureServer/0?f=json"
curl -s ".../FeatureServer/0/query?where=1%3D1&returnCountOnly=true&f=json"   # 29366
# St. Albert class aggregates (no bulk pull needed)
#   POST /query with groupByFieldsForStatistics=Assessment_Description,
#   outStatistics=[count OBJECTID, sum Assessed_Value, sum CurrentTaxLevy]
# Strathcona 2026 full attribute pull: paginate resultOffset 0..43000 step 1000,
#   outFields=roll,address,bldg,assess_2025,parcelarea,measured_in,latitude,longitude
```
