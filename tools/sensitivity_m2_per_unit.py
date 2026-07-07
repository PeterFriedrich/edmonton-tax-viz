"""Sensitivity of the water lens to M2_GROSS_PER_UNIT.

The multi-res (OTHER RESIDENTIAL) unit count is estimated from gross floor
area at ``load_water.M2_GROSS_PER_UNIT`` (m² per dwelling). The modeled
household total runs ~20% over census; this sweep quantifies how much of
that — and of the citywide $ — moves with the assumption.

Household connections are UNAFFECTED (one per roll point); only multi-res
buildings' unit counts and their meter-size band shift. Run:

    .venv/bin/python tools/sensitivity_m2_per_unit.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import load_water  # noqa: E402

ASSESSMENT_CSV = ROOT / "data/raw/Property_Assessment_Data__Current_Calendar_Year_.csv"
PROPERTY_INFO_CSV = ROOT / "data/raw/Property_Info__Current_Calendar_Year_.csv"
RATES_JSON = ROOT / "data/water_rates.json"
YEAR = 2026

# Sweep: the 90 m²/unit baseline plus a bracketing range. Smaller m²/unit
# => MORE modeled units per building => higher household count + higher $.
SWEEP = [70.0, 80.0, 90.0, 100.0, 110.0, 120.0]

# The validation (FINDINGS_utility_validation §2.1) puts the baseline
# modeled household total (~551,831) at ~20% over the census dwelling stock,
# implying a census anchor near this figure. Used only as context, not a
# derived result — it is a fixed offset that does not move across the sweep.
CENSUS_DWELLINGS_APPROX = round(551_831 / 1.20)


def run_one(m2: float) -> dict:
    load_water.M2_GROSS_PER_UNIT = m2
    out = load_water.load_water(ASSESSMENT_CSV, PROPERTY_INFO_CSV, RATES_JSON, YEAR)
    total = out["water_charge_annual"].sum()
    fixed = out["water_fixed_annual"].sum()
    return {"m2": m2, "total": total, "fixed": fixed}


def main() -> None:
    baseline = load_water.M2_GROSS_PER_UNIT
    # Instrument to capture modeled-household + connection counts, which the
    # returned per-hood frame doesn't expose. Re-derive from the log by
    # rerunning the connection build directly is overkill; instead patch the
    # module logger call is fragile — simplest: recompute households here by
    # monkeypatching is unnecessary because the info log already prints them.
    # We capture via the logger record.
    import logging

    captured = []

    class _Grab(logging.Handler):
        def emit(self, record):
            msg = record.getMessage()
            if "connections /" in msg and "modeled households" in msg:
                captured.append(msg)

    h = _Grab()
    logging.getLogger("load_water").addHandler(h)
    logging.getLogger("load_water").setLevel(logging.INFO)

    rows = []
    for m2 in SWEEP:
        captured.clear()
        r = run_one(m2)
        # Parse "%d connections / %d modeled households" out of the info line.
        line = captured[-1] if captured else ""
        conns = hh = None
        if line:
            import re
            m = re.search(r"([\d,]+) connections / ([\d,]+) modeled households", line)
            if m:
                conns = int(m.group(1).replace(",", ""))
                hh = int(m.group(2).replace(",", ""))
        r.update(connections=conns, households=hh)
        rows.append(r)

    load_water.M2_GROSS_PER_UNIT = baseline
    logging.getLogger("load_water").removeHandler(h)

    base = next(r for r in rows if r["m2"] == 90.0)
    print()
    print(f"{'m²/unit':>8} {'connections':>12} {'households':>12} "
          f"{'vs census':>10} {'citywide $/yr':>15} {'Δ vs 90':>10}")
    print("-" * 72)
    for r in rows:
        vs_census = r["households"] / CENSUS_DWELLINGS_APPROX
        d_total = (r["total"] - base["total"]) / base["total"] * 100
        mark = "  <- baseline" if r["m2"] == 90.0 else ""
        print(f"{r['m2']:>8.0f} {r['connections']:>12,} {r['households']:>12,} "
              f"{vs_census:>9.2f}x ${r['total']/1e6:>13.1f}M {d_total:>+9.1f}%{mark}")
    print()
    print(f"Census anchor (approx, {CENSUS_DWELLINGS_APPROX:,} = 551,831 / 1.20 "
          f"per FINDINGS §2.1)")
    print(f"Baseline (90): {base['households']:,} households, "
          f"${base['total']/1e6:.1f}M/yr total, ${base['fixed']/1e6:.1f}M fixed")


if __name__ == "__main__":
    main()
