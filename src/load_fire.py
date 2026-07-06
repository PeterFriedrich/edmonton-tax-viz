"""Fire-response demand per neighbourhood (services lens, third service).

Counts dispatched emergency events per neighbourhood per year from the
fire-response dataset (``7hsn-idqi``) and averages them over a pinned window
of full calendar years. Design + the four locked decisions:
docs/SPEC_services.md "Fire lens"; dataset facts DATA.md §7–8.

**Demand metric only.** The data carries dispatch and close timestamps but
NO on-scene-arrival timestamp, so a response-time or coverage-adequacy
metric is not buildable from open data (confirmed Session 12) — never
present this as one. The dispatch-priority ``response_code`` letters are
undecoded; never filter on them.

Locked filter (Peter, 2026-07-05): ALL emergency responses minus
operational noise — the explicit ``NOISE_GROUPS`` below plus null groups,
each exclusion counted. The ~57% MEDICAL share of kept events is a display
caveat, NOT a filter; the kept mix is logged every load so drift is
visible. Unrecognized new groups stay IN (they are presumably real
dispatches) and are logged loudly.

Column-name caveat: the build session (2026-07-06) could not reach
data.edmonton.ca, so the dispatch-datetime header could not be pinned.
``DISPATCH_COLUMN_CANDIDATES`` enumerates the plausible snake_case API
names; resolution HARD-ERRORS listing the file's actual headers if none
match. ``event_type_group`` and ``neighbourhood_name`` were confirmed in
the Session-12 probe.
"""

import json
import logging
from pathlib import Path

import pandas as pd

from load_assessment import NAME_CORRECTIONS

logger = logging.getLogger(__name__)

# Operational noise excluded from the demand metric (locked decision 2 —
# SPEC_services.md "Fire lens"; counts as of the Session-12 probe:
# TRAINING/MAINTENANCE 18k, plus COMMUNITY EVENT and PRE-INCIDENT PLANNING).
# Matched against the stripped, uppercased event_type_group.
NOISE_GROUPS = {"TRAINING/MAINTENANCE", "COMMUNITY EVENT", "PRE-INCIDENT PLANNING"}

# Emergency groups seen in the Session-12 probe — used ONLY to spot new
# vocabulary (unknown groups are still kept; they get a loud log line).
KNOWN_GROUPS = {
    "MEDICAL", "ALARMS", "MOTOR VEHICLE INCIDENT", "MVI", "OUTSIDE FIRE",
    "CITIZEN ASSIST", "FIRE", "HAZMAT", "RESCUE", "VEHICLE FIRE",
}

# Plausible snake_case API names for the dispatch datetime — the one keyed
# column the Session-12 probe didn't record. Resolution is exact-match
# against this explicit list (no fuzzy matching); a miss hard-errors with
# the file's real headers so the fix is a one-line addition here.
DISPATCH_COLUMN_CANDIDATES = (
    "dispatch_datetime",
    "dispatched_datetime",
    "dispatch_date_time",
    "dispatch_time",
    "dispatch_date",
    "event_dispatch_datetime",
    "date_dispatched",
)

# Station-file column candidates (b4y7-zhnz: station number + address +
# lat/long only). Same explicit-candidates rule as the dispatch column.
STATION_LAT_CANDIDATES = ("latitude", "lat")
STATION_LON_CANDIDATES = ("longitude", "long", "lon")
STATION_LABEL_CANDIDATES = ("station_number", "station", "station_name", "name")


def _resolve_column(columns, candidates: tuple[str, ...], what: str, required: bool = True) -> str | None:
    """Exact-match one of ``candidates`` in ``columns`` (case-insensitive).

    Hard-errors with the file's actual headers on a required miss — the fix
    is adding the real name to the candidate list, never guessing silently.
    """
    by_lower = {str(c).strip().lower(): c for c in columns}
    for cand in candidates:
        if cand in by_lower:
            return by_lower[cand]
    if required:
        raise ValueError(
            f"could not resolve the {what} column — none of {list(candidates)} "
            f"present. File headers: {list(columns)}. Add the real name to the "
            f"candidate list in src/load_fire.py."
        )
    return None


def _resolve_dispatch_column(columns) -> str:
    """The dispatch-datetime header: exact candidate first, then a single
    unambiguous 'dispatch' substring match (logged loudly — pin it in the
    candidate list), else a hard error with the real headers."""
    exact = _resolve_column(columns, DISPATCH_COLUMN_CANDIDATES, "dispatch datetime", required=False)
    if exact is not None:
        return exact
    matches = [c for c in columns if "dispatch" in str(c).lower()]
    if len(matches) == 1:
        logger.warning(
            "dispatch datetime column resolved by substring match: %r — add it "
            "to DISPATCH_COLUMN_CANDIDATES in src/load_fire.py to pin it",
            matches[0],
        )
        return matches[0]
    raise ValueError(
        f"could not resolve the dispatch datetime column — no exact candidate "
        f"({list(DISPATCH_COLUMN_CANDIDATES)}) and {len(matches)} substring "
        f"matches ({matches}). File headers: {list(columns)}. Add the real "
        f"name to the candidate list in src/load_fire.py."
    )


def load_fire_events(
    events_csv: str | Path,
    years: tuple[int, ...],
) -> pd.DataFrame:
    """Mean annual dispatched emergency events per neighbourhood.

    ``years`` is the pinned window of FULL calendar years (main.py
    FIRE_YEARS). Returns a DataFrame:
        neighbourhood_name    str    normalized + NAME_CORRECTIONS applied
        fire_events_per_year  float  kept events in window / len(years)

    A hood absent from the result had zero kept events in the window —
    join_and_calculate fills the true 0 (roads semantics).
    """
    if not years:
        raise ValueError("years window is empty")
    years = tuple(sorted(years))

    header = pd.read_csv(events_csv, nrows=0)
    dispatch_col = _resolve_dispatch_column(header.columns)
    for needed in ("event_type_group", "neighbourhood_name"):
        if needed not in header.columns:
            raise ValueError(
                f"expected column {needed!r} not in {events_csv} — headers: "
                f"{list(header.columns)}"
            )

    df = pd.read_csv(
        events_csv,
        usecols=[dispatch_col, "event_type_group", "neighbourhood_name"],
        low_memory=False,
    )
    n_total = len(df)

    # --- year window ---------------------------------------------------------
    when = pd.to_datetime(df[dispatch_col], errors="coerce", format="mixed")
    unparsed = when.isna()
    if unparsed.all():
        raise ValueError(
            f"column {dispatch_col!r} in {events_csv} does not parse as "
            f"datetimes at all — wrong column resolved; fix "
            f"DISPATCH_COLUMN_CANDIDATES in src/load_fire.py"
        )
    if unparsed.any():
        logger.warning(
            "%d of %d rows have unparseable %s values — excluded",
            int(unparsed.sum()), n_total, dispatch_col,
        )
    df = df.loc[~unparsed]
    df["year"] = when.loc[~unparsed].dt.year.astype(int)

    per_year_all = df["year"].value_counts()
    for y in years:
        if per_year_all.get(y, 0) == 0:
            raise ValueError(
                f"window year {y} has ZERO events in {events_csv} — the FIRE_YEARS "
                f"pin is wrong or the dataset drifted (years present: "
                f"{sorted(per_year_all.index)[:5]}…{sorted(per_year_all.index)[-3:]})"
            )
    df = df[df["year"].isin(years)]
    logger.info(
        "Fire events in window %s: %d of %d rows (%s)",
        years, len(df), n_total,
        ", ".join(f"{y}: {int((df['year'] == y).sum()):,}" for y in years),
    )

    # --- event filter (locked decision 2) -------------------------------------
    group = df["event_type_group"].astype("string").str.strip().str.upper()

    null_group = group.isna() | (group == "")
    if null_group.any():
        logger.warning(
            "%d in-window rows have a null event_type_group — excluded (operational noise)",
            int(null_group.sum()),
        )

    noise = group.isin(NOISE_GROUPS)
    if noise.any():
        counts = group[noise].value_counts()
        logger.info(
            "Excluding %d operational-noise events:\n  %s",
            int(noise.sum()),
            "\n  ".join(f"{g}: {n:,}" for g, n in counts.items()),
        )

    kept = df.loc[~null_group & ~noise].copy()
    kept_groups = group.loc[kept.index]

    unknown = set(kept_groups.unique()) - KNOWN_GROUPS
    if unknown:
        logger.warning(
            "event_type_group values not seen in the Session-12 probe — KEPT "
            "(presumed real dispatches), review + add to KNOWN_GROUPS: %s",
            sorted(unknown),
        )

    mix = kept_groups.value_counts()
    medical_share = mix.get("MEDICAL", 0) / len(kept) if len(kept) else 0.0
    logger.info(
        "Kept %d emergency events (MEDICAL %.0f%% — display caveat, not a "
        "filter). Mix:\n  %s",
        len(kept), 100 * medical_share,
        "\n  ".join(f"{g}: {n:,}" for g, n in mix.items()),
    )
    if not len(kept):
        raise ValueError("no kept events in the window after filtering — inputs are wrong")

    # --- hood normalization + aggregation -------------------------------------
    hood = (
        kept["neighbourhood_name"].astype("string").str.strip().str.upper()
        .replace(NAME_CORRECTIONS)
    )
    no_hood = hood.isna() | (hood == "")
    if no_hood.any():
        logger.warning(
            "%d kept events have no neighbourhood_name — excluded (no spatial "
            "fallback by design; ~99%% of rows come pre-joined)",
            int(no_hood.sum()),
        )
    kept = kept.loc[~no_hood]
    kept["neighbourhood_name"] = hood.loc[kept.index]

    out = (
        kept.groupby("neighbourhood_name", as_index=False)
        .size()
        .rename(columns={"size": "fire_events_per_year"})
    )
    out["fire_events_per_year"] = out["fire_events_per_year"] / len(years)

    logger.info(
        "Fire demand: %d hoods, %.0f kept events/yr citywide (window mean)",
        len(out), out["fire_events_per_year"].sum(),
    )
    return out


def export_fire_stations_web(stations_csv: str | Path, out_path: str | Path) -> int:
    """Write the fire-station context dots for the web map.

    Reads the 31-row stations CSV (b4y7-zhnz) and writes a tiny committed
    JSON — ``{"stations": [[lon, lat, label], ...]}`` — lazy-loaded by the
    Services view. Returns the station count written. Null-coordinate rows
    are dropped + reported, never silently.
    """
    df = pd.read_csv(stations_csv)
    lat_col = _resolve_column(df.columns, STATION_LAT_CANDIDATES, "station latitude")
    lon_col = _resolve_column(df.columns, STATION_LON_CANDIDATES, "station longitude")
    label_col = _resolve_column(df.columns, STATION_LABEL_CANDIDATES, "station label", required=False)
    if label_col is None:
        logger.warning(
            "no station label column among %s — dots will be unlabelled. Headers: %s",
            list(STATION_LABEL_CANDIDATES), list(df.columns),
        )

    lat = pd.to_numeric(df[lat_col], errors="coerce")
    lon = pd.to_numeric(df[lon_col], errors="coerce")
    bad = lat.isna() | lon.isna()
    if bad.any():
        logger.warning("%d station row(s) have null coordinates — dropped", int(bad.sum()))

    stations = [
        [round(float(x), 5), round(float(y), 5),
         "" if label_col is None else str(df[label_col].iloc[i])]
        for i, (x, y) in enumerate(zip(lon, lat))
        if not bad.iloc[i]
    ]
    if not stations:
        raise ValueError(f"no stations with coordinates in {stations_csv}")

    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"stations": stations}, f, separators=(",", ":"))
    logger.info("Wrote %d fire stations to %s", len(stations), out_path)
    return len(stations)
