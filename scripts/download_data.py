"""Download the raw open-data inputs the pipeline needs, into ``data/raw/``.

This is the CI/runner's "fetch" step (see docs/SPEC_deployment.md): a fresh
GitHub Actions VM has none of the raw inputs, so it must pull them before
``main.py`` can regenerate the map. Run locally the same way to refresh a
snapshot.

Three inputs come from Edmonton's Socrata open-data portal:
  - assessment  q7d6-ambg  (Property Assessment Data, current year)  -> CSV
  - boundaries  65fr-66s6  (Neighbourhood Boundaries)                -> GeoJSON
  - zoning      fixa-tstc  (Zoning Bylaw Geographical Data)          -> GeoJSON

Mill rates (pwis-wc4c) are NOT fetched here — they live in the committed
``data/mill_rates.json`` (see DATA.md); refreshing them for a new year is a
manual, reviewed step because the year must align with the assessment roll.

Usage:
    python scripts/download_data.py                 # fetch all three inputs
    python scripts/download_data.py --only zoning   # fetch one (repeatable)
"""

import argparse
import logging
import sys
from pathlib import Path

import requests

logger = logging.getLogger(__name__)

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"

# Each input: the Socrata download URL + the local filename main.py expects.
# GeoJSON exports use the resource endpoint with an explicit $limit above the
# feature count (Socrata paginates at 1,000 by default and truncates silently).
SOURCES = {
    "assessment": {
        "url": "https://data.edmonton.ca/api/views/q7d6-ambg/rows.csv?accessType=DOWNLOAD",
        "dest": RAW / "Property_Assessment_Data__Current_Calendar_Year_.csv",
    },
    "boundaries": {
        "url": "https://data.edmonton.ca/resource/65fr-66s6.geojson?$limit=500",
        "dest": RAW / "neighbourhoods.geojson",
    },
    "zoning": {
        "url": "https://data.edmonton.ca/resource/fixa-tstc.geojson?$limit=20000",
        "dest": RAW / "zoning.geojson",
    },
}


def download(url: str, dest: Path, timeout: int = 300) -> int:
    """Stream ``url`` to ``dest``, returning bytes written. Raises on HTTP error."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Downloading %s -> %s", url, dest.name)
    written = 0
    with requests.get(url, stream=True, timeout=timeout) as r:
        r.raise_for_status()
        # Write to a temp sibling first so a mid-stream failure can't leave a
        # truncated file where main.py would read it as complete.
        tmp = dest.with_suffix(dest.suffix + ".part")
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 16):
                if chunk:
                    written += len(chunk)
                    f.write(chunk)
        tmp.replace(dest)
    logger.info("Wrote %s (%.1f MB)", dest.name, written / 1e6)
    return written


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument(
        "--only",
        action="append",
        choices=sorted(SOURCES),
        help="download only this input (repeatable); default is all three",
    )
    p.add_argument("--log-level", default="INFO")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    logging.basicConfig(
        stream=sys.stdout,
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(levelname)s: %(message)s",
    )
    wanted = args.only or list(SOURCES)
    failures = []
    for name in wanted:
        src = SOURCES[name]
        try:
            download(src["url"], src["dest"])
        except Exception as exc:  # noqa: BLE001 — report every input, don't stop at the first
            logger.error("FAILED to download %s: %s", name, exc)
            failures.append(name)
    if failures:
        raise SystemExit(f"Download failed for: {', '.join(failures)}")
    logger.info("All downloads complete (%d input(s)).", len(wanted))


if __name__ == "__main__":
    main()
