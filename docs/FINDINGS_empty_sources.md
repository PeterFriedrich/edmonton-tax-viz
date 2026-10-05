# Findings — the empty-source class (queue item 18)

**Run:** 2026-10-05, S215, Opus 5.5. **Trigger:** the 2026-10-05 refresh. The
City reloaded `f2sy-bth7` with 0 rows, `download_data.py` passed it (local 0 ==
server `count(*)` 0), and only `load_transit` stopped the publish.
**Question:** for each of the 18 sources in `SOURCES`, does a 0-row table fail
loud, or does it publish?
**Instrument:**
- A scratch copy of the repo (`git archive HEAD`) with `data/raw` symlinked.
- Each source replaced in turn by what Socrata actually serves for a 0-row
  table: a header-only CSV (verified on `f2sy-bth7`), or
  `{"type":"FeatureCollection","features":[]}`.
- Then `main.py --skip-png` → `check_served_columns` → `check_value_anchors`
  → `check_temporal_years`, with baseline outputs restored before each run.
  Baseline: all green, 2 m 44 s.
- Predictions were written before any run.

## Verdict: 16 of 18 fail loud; **2 publish silently**, on the full build only

| Source | Result | How it fails | Diagnosis correct? |
|---|---|---|---|
| assessment | main exit 1 | `ValueError: attempt to get argmax of an empty sequence` (incidental) | ❌ crash, no message |
| boundaries | main exit 1 | `KeyError: 'name'` (incidental) | ❌ |
| zoning | main exit 1 | `KeyError: 'zoning'` (incidental) | ❌ |
| roads | main exit 1 | `KeyError: 'centerline_type'` (incidental) | ❌ |
| bike_routes | main exit 1 | "expected column 'classification' … columns: ['geometry']" | ❌ reads as schema drift |
| fire_events | main exit 1 | "does not parse as datetimes — wrong column resolved; fix DISPATCH_COLUMN_CANDIDATES" | ❌ **points at the wrong fix** |
| fire_stations | main exit 1 | "no stations with coordinates" | ~ |
| gtfs_calendar_dates | main exit 1 | "no active service dates — wrong/empty feed" | ✅ (live 2026-10-05) |
| gtfs_routes | main exit 1 | "ROUTE_MODE found no 'lrt' among []" | ~ reads as vocabulary drift |
| gtfs_stops / trips / stop_times | main exit 1 | "Citywide scheduled stop-events is not positive (0.0)" | ~ |
| lrt_routes | main exit 1 | "no features … wrong/empty file" | ✅ |
| permits | main exit 1 | "window year 2021 has ZERO permits … PERMIT_YEARS pin is wrong or the dataset drifted" | ~ |
| assessment_historical | main OK → **temporal guard exit 5** | "years: missing [2012 … 2023]" | ✅ |
| property_info | main OK → **served-columns exit 5, anchors exit 1** | caught after regen | ✅ |
| **schools_public** | **all green** | EPSB 0 of 0 points; school points **303 → 93**; `dist_school_m` median **900 → 1,486 m**, p90 2,008 → 2,958 m | — **silent** |
| **schools_catholic** | **all green** | same shape (ECSD dropped) | — **silent** |

**F1 — the school sources publish wrong distances on an empty table.**
`dist_school_m` feeds the Infill "Within 800 m of a school" highlight. That
control is full-build only (CONTROLS_MATRIX, Development → Infill 🔒). Losing
either board's table moves every grid cell's distance and passes every gate.
The log line *"EPSB 0 of 0"* is the only trace. **Class:** `guard-blind`;
**reach:** full.

**F2 — loud, but misdiagnosed.** 6 of the 16 loud failures surface as an
incidental `KeyError`, or as a message that names a schema or vocabulary
problem. Fire's message names a specific wrong fix, and RUNBOOK §2's
"Regenerate web GeoJSON" entry steers the operator toward extending exactly
that mapping. **Class:** `guard-noisy` (wrong diagnosis); **reach:** no.

**✅ Shipped 2026-10-05 (S216):** the 0-row check, without a per-source floor
(`verify_download`; tests `test_verify_fails_on_empty_geojson_even_when_server_agrees`,
`test_verify_fails_on_header_only_csv`). Run against the live empty `f2sy-bth7`,
it fails naming the dataset.

**Remedy for both (CI behaviour → Peter):** `download_data.py` fails a source
whose download is 0 rows (or under a per-source floor), naming the dataset id
and "upstream table is empty". That one check closes F1 at the download step,
gives F2's 16 sources the right diagnosis at the right step, and would have
named today's real cause. RUNBOOK §2 gains a "0 rows" line either way.

## Predictions vs observed
**Right:**
- calendar_dates, permits, historical, assessment, boundaries, and
  property_info (caught by guards) all failed loud as predicted.

**Wrong:**
- bike, fire_events, fire_stations and lrt_routes were predicted to publish a
  zero or blank lens. All four fail loud.
- Schools were marked "?". They are the two that publish silently.

## What this run got wrong
- **I predicted bike, fire and LRT would publish zeros**: four "Z"
  predictions, all wrong. The loaders are stricter than I assumed. The real
  silent path was in a source I had marked "?". Ranking risk by which lens
  *looks* important would have sent a fix to the wrong place.
- **Only the neighbourhood geojson was saved per run.** The schools diagnosis
  comes from the run log's own `dist_school_m` summary lines, not from a diff
  of the served grid file. The distance shift is the pipeline's report of
  itself, not an independent measurement.
- **Header-only is one empty shape.** A *partially* emptied table (e.g. a
  reload that lands at half size) was not tested. The count guard compares to
  the server, which would agree with a half-size table too.
