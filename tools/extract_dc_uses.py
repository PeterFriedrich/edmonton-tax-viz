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

# Purpose runs from the "Purpose" heading to the next numbered top-level section
# (typically "2. Area of Application" / "Area of Application"). This is the
# high-signal field — DC purpose statements consistently name the intended use
# ("convenience commercial uses", "mixed use development", "Community Commercial
# Centre"). The pages' "Uses" region is the standard 5.x regulation TOC, not a
# site-specific land-use list, so it is not extracted.
PURPOSE_RE = re.compile(
    r"\bPurpose\b\s*(.*?)(?:\b\d+\.?\s*Area of Application\b|\bArea of Application\b|\b\d+\.\s+[A-Z])",
    re.S)


def clean(html: str) -> str:
    m = re.search(r"<main[^>]*>(.*?)</main>", html, re.S | re.I)
    region = m.group(1) if m else html
    region = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", region, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", region)
    return re.sub(r"\s+", " ", text).strip()


def extract(text: str) -> str:
    pm = PURPOSE_RE.search(text)
    if not pm:
        return ""
    purpose = pm.group(1).strip().lstrip(":").strip()
    purpose = purpose.replace("\xa0", " ").replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", purpose)[:600]


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
