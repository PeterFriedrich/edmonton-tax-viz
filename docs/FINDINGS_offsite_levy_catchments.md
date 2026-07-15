# FINDINGS — Off-Site Levy Fire-Hall Catchment Boundaries (Debt-Lens D0)

Investigation date: 2026-07-15 (laptop session; edmonton.ca reachable).
Ticket: TODO.md → "Growth Infrastructure Financing Panel (Debt Lens)" → **D0**.
Brief: `docs/fable_brief_debt_lens.md` (Component 1 spatial join key = the 12
fire-hall off-site levy catchments).

## 1. Source resolution (the D0 acquisition risk)

The 12 catchments were flagged (2026-07-14) as a data-acquisition risk: **not on
data.edmonton.ca** (Socrata: 0 hits) and **not on ArcGIS Hub** (every "off-site
levy" layer there is Calgary's). This session resolved where the boundaries
actually live:

- The **only** published catchment boundaries are a **raster map exhibit —
  Schedule A of Off-Site Levy Bylaw 19340** ("Fire Halls with Catchment
  Boundaries"), a JPEG embedded in the bylaw PDF. **No GIS vector layer exists
  anywhere.**
- The bylaw text itself calls the boundaries advisory: *"Catchment boundaries …
  the City may adjust and refine … over time"* and the map footnote *"subject to
  change based on new information."* So sub-parcel precision is not meaningful —
  an approximation is faithful to the source's own confidence.
- Source artifacts saved to `data/raw/offsite_levy/`:
  - `BL19340_offsite_levy_bylaw.pdf` — the bylaw (Schedule A map on p.7)
  - `ScheduleA_catchment_map.jpg` — extracted catchment map exhibit
  - `2026_approved_rates.pdf` — the approved rates table (cost/area/rate)

## 2. Approach chosen: neighbourhood-union approximation

Decision (Peter, 2026-07-15): approximate each catchment as a **union of existing
neighbourhoods** from `data/raw/neighbourhoods.geojson` (407 hoods), rather than
hand-tracing the raster. Rationale: Schedule A's catchment edges follow the
neighbourhood / quarter-section grid; the approach is reproducible from data we
own, aligns with the project's neighbourhood-unit aggregation, and matches the
bylaw's own "approximate/advisory" framing. Alternatives (trace the raster;
table-only) recorded in the D0 ticket.

## 3. Feasibility: partially viable — the grid is finer than catchments in
developed edges, but COARSER in the far greenfield

First-pass assignment (read off Schedule A against a labelled render of
`neighbourhoods.geojson` in the same projection/extent) was validated against the
brief's per-catchment hectare targets. Ratio = dissolved-hood-area ÷ brief target:

| Catchment | Target ha | Union ha | Ratio | Verdict |
|---|---|---|---|---|
| Wedgewood | 622 | 616 | 0.99 | ✅ clean |
| Big Lake | 1,214 | 1,321 | 1.09 | ✅ clean |
| Walker | 1,095 | 1,234 | 1.13 | ✅ clean |
| Riverview | 838 | 974 | 1.16 | ✅ clean (≈1 hood) |
| Horse Hill | 905 | 1,118 | 1.24 | ✅ borderline |
| Mistatim Industrial | 1,102 | 920 | 0.83 | ✅ borderline |
| Cumberland | 1,338 | 786 | 0.59 | ⚠️ fixable (too few hoods picked) |
| Southeast | 1,181 | 2,050 | 1.74 | ⚠️ fixable (wrong hoods picked) |
| Blatchford | 785 | 305 | 0.39 | ⚠️ catchment ≈2.6× the `BLATCHFORD AREA` hood → spills into neighbours |
| Northeast Horse Hill | 963 | 2,715 | 2.82 | ❌ rural hoods 2–3× the catchment |
| EETP | 1,268 | 5,334 | 4.21 | ❌ **shares one hood with Northeast EETP** |
| Northeast EETP | 2,040 | 5,334 | 2.61 | ❌ **shares one hood with EETP** |

Note: this table's assignments are a FIRST PASS for feasibility, not the final
join. The ✅ rows are close; the ⚠️ rows are my hood-pick errors (fixable with a
more careful read); the ❌ rows are **structural**.

### The structural limit
In Edmonton's far growth areas the neighbourhood units are single giant
"ANTHONY HENDAY …", "RURAL NORTH EAST …", and "EDMONTON …" polygons that are
**larger than, or shared across, catchments**:

- **`EDMONTON ENERGY AND TECHNOLOGY PARK` (5,334 ha) contains BOTH the EETP and
  Northeast EETP catchments.** Neighbourhood-union cannot separate them — the
  only hood in that corner spans both.
- **Northeast Horse Hill**: `RURAL NORTH EAST HORSE HILL` + `RURAL NORTH EAST
  SOUTH STURGEON` are 2–3× the catchment; the catchment is a sub-portion of a
  rural hood the union can't subdivide.

So the neighbourhood-union is faithful for the **developed-edge catchments** and
breaks down for the **far-greenfield catchments** where the grid is too coarse.

## 4. Options for the ❌/⚠️ catchments (open — Peter's call)

1. **Hybrid**: neighbourhood-union for the ~6–9 that resolve; hand-trace the 2–3
   structural ones (EETP pair; NE Horse Hill) from the Schedule A raster.
2. **Merge to the grid**: collapse catchments that share a hood into one unit
   (EETP + Northeast EETP → a single "EETP" catchment; likewise the Horse Hill
   pair). Honest, coarser, fewer catchments. Component 1 still shows the
   levy-only-fire-halls asymmetry, just at merged granularity for the far NE.
3. **Table-only for the exceptions**: map the resolvable catchments; list the
   structural ones as a per-catchment table (cost/area/rate from the brief) with
   no polygon.

Whatever is chosen, the join layer must be **labelled "approximated to
neighbourhood boundaries"** and the merged/traced exceptions footnoted — no
silent precision claims.
