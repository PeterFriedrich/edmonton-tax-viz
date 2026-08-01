"""Write ``web/data/status.json`` — the site's status manifest + heartbeat.

See docs/SPEC_deployment.md. This runs at the end of every refresh (after
``main.py`` regenerates the web GeoJSON) and does three jobs:

  1. **Provenance** — records which years the map is showing (assessment,
     mill-rate, zoning) so the frontend/visitor can see the vintage.
  2. **Heartbeat** — bumps ``last_checked`` every run. That commit is repo
     activity, which keeps the scheduled Action from being auto-disabled after
     60 days of inactivity (annual data can sit unchanged for months).
  3. **Banner** — an optional maintenance notice the frontend renders above the
     map (e.g. during the year-mismatch holding window). Preserved across runs
     unless explicitly set/cleared here, so a manual notice isn't wiped by the
     next heartbeat.

Two timestamps, deliberately distinct:
  - ``last_checked`` — bumped every run (the heartbeat).
  - ``generated``    — bumped ONLY when the GeoJSON content actually changed,
     detected via a content hash so it's independent of git commit ordering.

Usage:
    python scripts/generate_status.py                      # heartbeat + provenance
    python scripts/generate_status.py --banner "Showing 2025 data — ..."
    python scripts/generate_status.py --clear-banner
"""

import argparse
import datetime as dt
import hashlib
import json
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.apply_tax_rates import load_mill_rates  # noqa: E402

GEOJSON = ROOT / "web/data/neighbourhood_value_per_acre.geojson"
STATUS = ROOT / "web/data/status.json"
MILL_RATES = ROOT / "data/mill_rates.json"

# The rate classes the map's three revenue cuts are billed at, in display order:
# Total spans all three, Residential is the two housing classes, Non-residential
# is the third (apply_tax_rates.RESIDENTIAL_RATE_LABELS / NONRES_RATE_LABELS).
# Farmland is deliberately absent — no revenue cut isolates it, and its 2025 rate
# is an assumption; it is reported via ``assumed`` instead.
DISPLAY_RATE_CLASSES = ["Residential", "Other Residential", "Non Residential"]

# Vintages the manifest reports. Assessment + rate year are pinned to the local
# snapshot (single source of truth: main.py ASSESSMENT_YEAR); zoning is the 2024
# Zoning Bylaw (see DATA.md). Overridable via CLI so the runner can pass the
# aligned year once auto-year-detection lands (SPEC_deployment "Year alignment").
DATA_YEAR = 2025
RATE_YEAR = 2025
ZONING_YEAR = 2024

_SENTINEL = object()  # distinguishes "flag not passed" from "--banner '' "


def content_hash(path: Path) -> str:
    """SHA-256 of the file's bytes — the change detector for ``generated``."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def load_prior(path: Path) -> dict:
    """Return the existing manifest, or {} if absent/unreadable."""
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not read prior %s (%s) — treating as fresh", path.name, exc)
        return {}


def municipal_rates(rates_path: Path, year: int) -> dict | None:
    """Return the mill rates the revenue map is billed at, for the frontend pod.

    Publishes the MUNICIPAL rate only — every dollar on the site is the municipal
    levy, and the education levy is provincial (mill_rates.json notes). ``assumed``
    names the classes whose rate that year was inferred rather than published, so
    the caveat the UI prints is data-driven and stops appearing on its own the
    year the source publishes a real row. Returns None if the file is unreadable:
    a manifest without rates just means the pod never shows.
    """
    try:
        rates = load_mill_rates(rates_path, year)
        published = json.loads(Path(rates_path).read_text())["rates"][str(year)]
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        logger.warning("No municipal rates for %s (%s) — omitting from manifest", year, exc)
        return None

    missing = [c for c in DISPLAY_RATE_CLASSES if c not in rates]
    if missing:
        raise KeyError(f"{year} mill rates missing display class(es) {missing} in {rates_path}")

    return {
        "unit": "per $1,000 assessed",
        "classes": [{"name": c, "rate": rates[c]} for c in DISPLAY_RATE_CLASSES],
        "assumed": sorted(c for c, vals in published.items() if "_assumed" in vals),
    }


def build_status(
    *,
    geojson: Path,
    prior: dict,
    today: str,
    data_year: int,
    rate_year: int,
    zoning_year: int,
    rates_path: Path = MILL_RATES,
    banner=_SENTINEL,
) -> dict:
    """Compute the new manifest from the prior one + the current GeoJSON."""
    new_hash = content_hash(geojson)
    changed = prior.get("_geojson_sha256") != new_hash

    # generated: keep the prior date unless the data content actually changed
    # (or there was no prior — first run counts as "generated today").
    generated = today if (changed or "generated" not in prior) else prior["generated"]

    if banner is _SENTINEL:
        banner_value = prior.get("banner")  # preserve whatever was there
    else:
        banner_value = banner

    return {
        "data_year": data_year,
        "rate_year": rate_year,
        "zoning_year": zoning_year,
        "generated": generated,
        "last_checked": today,
        "banner": banner_value,
        "municipal_rates": municipal_rates(rates_path, rate_year),
        "_geojson_sha256": new_hash,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--geojson", type=Path, default=GEOJSON)
    p.add_argument("--status", type=Path, default=STATUS)
    p.add_argument("--data-year", type=int, default=DATA_YEAR)
    p.add_argument("--rate-year", type=int, default=RATE_YEAR)
    p.add_argument("--zoning-year", type=int, default=ZONING_YEAR)
    g = p.add_mutually_exclusive_group()
    g.add_argument("--banner", help="set the maintenance banner text")
    g.add_argument("--clear-banner", action="store_true", help="clear the banner (set null)")
    p.add_argument("--log-level", default="INFO")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    logging.basicConfig(
        stream=sys.stdout,
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(levelname)s: %(message)s",
    )
    if not args.geojson.exists():
        raise SystemExit(f"GeoJSON not found: {args.geojson} — run main.py first")

    if args.clear_banner:
        banner = None
    elif args.banner is not None:
        banner = args.banner
    else:
        banner = _SENTINEL

    today = dt.date.today().isoformat()
    status = build_status(
        geojson=args.geojson,
        prior=load_prior(args.status),
        today=today,
        data_year=args.data_year,
        rate_year=args.rate_year,
        zoning_year=args.zoning_year,
        banner=banner,
    )
    args.status.parent.mkdir(parents=True, exist_ok=True)
    args.status.write_text(json.dumps(status, indent=2, ensure_ascii=False) + "\n")
    logger.info(
        "Wrote %s (generated=%s last_checked=%s banner=%r)",
        args.status.name, status["generated"], status["last_checked"], status["banner"],
    )


if __name__ == "__main__":
    main()
