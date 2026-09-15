"""Compose the README side-by-side from the two panels shot-readme-sxs.js writes.

Stage 2 of 2 — run `shot-readme-sxs.js` first:

    node tools/profiling/shot-readme-sxs.js http://localhost:8947/index.html <dir>
    .venv/bin/python tools/profiling/compose-readme-sxs.py <dir> docs/assets/hood-vs-50m-grid.png

Kept separate from the capture because they need different runtimes (Playwright
is node, Pillow is python), and because re-composing after a caption tweak should
not mean re-rendering two WebGL scenes.

⚠️ The panels are NOT cropped. The "Beta build — work in progress" badge and the
MapLibre attribution both sit in the bottom strip, and a crop that tidies the
frame silently removes a disclosure and an attribution.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

# ⚠️ This box has three font families and DejaVuSans.ttf is NOT among them —
# only the Mono cut and Cantarell (docs/MOBILE_USABILITY.md notes the same gap
# for CSS). A missing path makes ImageFont fall back to a ~10px bitmap default
# and the captions render illegibly at export size, which is a silent failure
# that survived three renders. Fail loudly instead.
BOLD = "/usr/share/fonts/dejavu/DejaVuSansMono-Bold.ttf"
REG = "/usr/share/fonts/dejavu/DejaVuSansMono.ttf"

GAP, PAD, CAP = 24, 24, 250
BG = (10, 10, 15)          # matches the app's own ground
GOLD = (252, 210, 120)     # the app's accent
MUTED = (176, 176, 198)
RULE = (46, 46, 60)

CAPTIONS = [
    ("Neighbourhood", "363 neighbourhoods - the primary unit"),
    ("50 m grid", "the same revenue, binned to squares"),
]

EXPORT_WIDTHS = (1800, 1200)


def main(indir, outpath):
    for p in (BOLD, REG):
        if not os.path.exists(p):
            raise SystemExit("missing font: " + p)

    panels = [
        Image.open(os.path.join(indir, "panel-a-hood.png")).convert("RGB"),
        Image.open(os.path.join(indir, "panel-b-grid50.png")).convert("RGB"),
    ]
    if panels[0].size != panels[1].size:
        raise SystemExit("panels differ in size: %s vs %s" % (panels[0].size, panels[1].size))

    w, h = panels[0].size
    out = Image.new("RGB", (PAD * 2 + w * 2 + GAP, PAD + h + CAP), BG)
    for i, im in enumerate(panels):
        out.paste(im, (PAD + i * (w + GAP), PAD))

    d = ImageDraw.Draw(out)
    f_title = ImageFont.truetype(BOLD, 96)
    f_sub = ImageFont.truetype(REG, 62)
    for i, (title, sub) in enumerate(CAPTIONS):
        x, y = PAD + i * (w + GAP), PAD + h + 46
        d.text((x, y), title, font=f_title, fill=GOLD)
        d.text((x, y + 122), sub, font=f_sub, fill=MUTED)

    # Hairline, so the pair reads as two frames rather than one wide render.
    xm = PAD + w + GAP // 2
    d.line([(xm, PAD), (xm, PAD + h)], fill=RULE, width=2)

    root, ext = os.path.splitext(outpath)
    for width in EXPORT_WIDTHS:
        sm = out.resize((width, round(out.height * width / out.width)), Image.LANCZOS)
        path = outpath if width == EXPORT_WIDTHS[0] else "%s-%d%s" % (root, width, ext)
        sm.save(path, optimize=True)
        print("wrote %s  %dx%d  %d kB" % (path, sm.width, sm.height,
                                          os.path.getsize(path) // 1024))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2])
