"""Extract the Purpose statement + uses section from cached DC provision pages.

ANALYSIS_BACKLOG.md item 3, step 2. Reads the raw HTML cached by
scripts/scrape_dc_provisions.py, pulls each provision's Purpose statement and
(where present) its permitted/listed-uses excerpt, and writes a compact table
for classification. The Purpose statement is the highest-signal field — e.g.
"facilitate the development of a Community Commercial Centre … commercial,
office … uses" classifies cleanly as commercial.

    python tools/extract_dc_uses.py    # -> data/dc_provisions_text.csv
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

CACHE = Path("data/raw/dc_provisions")
MANIFEST = CACHE / "_manifest.csv"
OUT = Path("data/dc_provisions_text.csv")

# Purpose runs from the "Purpose" heading to the "Area of Application" section
# that consistently follows it (present on 873/918 cached pages). This is the
# high-signal field — DC purpose statements consistently name the intended use
# ("convenience commercial uses", "mixed use development", "Community Commercial
# Centre"). The pages' "Uses" region is the standard 5.x regulation TOC, not a
# site-specific land-use list, so it is not extracted.
#
# Capture from the "Purpose" heading up to the first *real* next section, over a
# bounded window so the match can never fail (an anchored fallback that required
# a trailing "Appendix"/"$" silently dropped old-format DC1 pages). Three page
# formats occur:
#   - modern:      "1. Purpose 1.1. To … 2. Area of Application …"
#   - old DC1:     "Purpose <use text> 2. Uses …"        (no Area of Application)
#   - old DC1(loc):"Purpose <location> 2. Rationale <use text> …"
# So the window must NOT stop at internal sub-numbering ("1.1.", which truncated
# 62 provisions to a bare "1."), and must NOT stop at "Rationale" — for the
# location-style pages the Rationale is where the land-use signal lives, so we
# keep it in. It stops at the first heading that follows the use-bearing intro.
PURPOSE_START_RE = re.compile(r"\bPurpose\b\s*", re.I)
WINDOW = 900   # chars after the Purpose heading to search for a stop
STOP_RE = re.compile(
    r"\b\d+\.?\s*Area of Application\b|\bArea of Application\b"
    r"|\b\d+\.\s*Uses\b|\b\d+\.\s*Development Regulations\b"
    r"|\b\d+\.\s*General Regulations\b|\bAppendix\b",
    re.I)
# Leading section numbering to strip off the captured purpose ("1.1. To …").
LEAD_NUM_RE = re.compile(r"^(?:\d+(?:\.\d+)*\.?\s*)+")


def clean(html: str) -> str:
    m = re.search(r"<main[^>]*>(.*?)</main>", html, re.S | re.I)
    region = m.group(1) if m else html
    region = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", region, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", region)
    return re.sub(r"\s+", " ", text).strip()


def extract(text: str) -> str:
    sm = PURPOSE_START_RE.search(text)
    if not sm:
        return ""
    window = text[sm.end(): sm.end() + WINDOW]
    stop = STOP_RE.search(window)
    purpose = window[: stop.start()] if stop else window[:600]
    purpose = purpose.replace("\xa0", " ").replace("&nbsp;", " ")
    purpose = re.sub(r"\s+", " ", purpose).strip().lstrip(":").strip()
    purpose = LEAD_NUM_RE.sub("", purpose).strip()   # drop leading "1.1. " numbering
    return purpose[:600]


def main() -> None:
    if not MANIFEST.exists():
        raise SystemExit(f"no manifest at {MANIFEST} — run scripts/scrape_dc_provisions.py first")
    rows = list(csv.DictReader(open(MANIFEST)))
    out_rows, empty = [], 0
    for r in rows:
        path = CACHE / f"{r['slug']}.html"
        if r["status"] == "FAILED" or not path.exists():
            continue
        text = clean(path.read_text(errors="replace"))
        purpose = extract(text)
        if not purpose:
            empty += 1
        out_rows.append(dict(slug=r["slug"], agreement_no=r["agreement_no"],
                             url=r["url"], purpose=purpose))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["slug", "agreement_no", "url", "purpose"])
        w.writeheader()
        w.writerows(out_rows)
    print(f"extracted {len(out_rows)} provisions -> {OUT}  ({empty} with no Purpose statement)")


if __name__ == "__main__":
    main()
