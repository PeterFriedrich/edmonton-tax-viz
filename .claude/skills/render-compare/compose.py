"""Pair <before-label>_<size>_<theme>.png with <after-label>_... side by side.

.venv/bin/python compose.py <dir> <before-label> <after-label> [caption...]
Writes <dir>/compare_<size>_<theme>.png, one per pair, and fails on a shot
with no partner rather than skipping it. Prints how many pixels changed by
more than 40 levels and where: two renders of one tree differ by <= 7 such
pixels (SwiftShader anti-aliasing, measured 2026-10-14), so a pair at that
level shows no change and a reader should not be sent to find one.
"""
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

# The box has no DejaVuSans.ttf, and truetype() on a bad path is not the
# failure: load_default() is. Never fall back to the ~10px bitmap.
FONT = "/usr/share/fonts/dejavu/DejaVuSansMono.ttf"
GAP, LINE, MAX_W = 24, 30, 2600


def main() -> None:
    d, before, after = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    caption = " ".join(sys.argv[4:])
    font = ImageFont.truetype(FONT, 22)
    pre = {p.name[len(before) + 1:]: p for p in d.glob(f"{before}_*.png")}
    post = {p.name[len(after) + 1:]: p for p in d.glob(f"{after}_*.png")}
    if pre.keys() != post.keys():
        sys.exit(f"unpaired shots: {sorted(pre.keys() ^ post.keys())}")
    if not pre:
        sys.exit(f"no {before}_*.png in {d}")
    for key in sorted(pre):
        a, b = Image.open(pre[key]).convert("RGB"), Image.open(post[key]).convert("RGB")
        head = LINE * (3 if caption else 2) + 8
        w, h = a.width + GAP + b.width, max(a.height, b.height) + head
        out = Image.new("RGB", (w, h), (128, 128, 128))
        out.paste(a, (0, head))
        out.paste(b, (a.width + GAP, head))
        draw = ImageDraw.Draw(out)
        size = key.removesuffix(".png").replace("_", " ")
        # One short line per panel: a 360 px shot fits ~24 mono characters.
        for x, label in ((8, before), (a.width + GAP + 8, after)):
            draw.text((x, 4), label, fill=(0, 0, 0), font=font)
            draw.text((x, 4 + LINE), size, fill=(0, 0, 0), font=font)
        if caption:
            draw.text((8, 4 + 2 * LINE), caption, fill=(0, 0, 0), font=font)
        changed = 0
        if a.size == b.size:
            diff = ImageChops.difference(a, b).convert("L").point(lambda v: 255 if v > 40 else 0)
            changed = diff.histogram()[255]
            where = diff.getbbox()
        else:
            where = "sizes differ"
        if w > MAX_W:
            out = out.resize((MAX_W, round(h * MAX_W / w)), Image.LANCZOS)
        dest = d / f"compare_{key}"
        out.save(dest)
        print(f"{dest}  changed px: {changed}  box: {where}")


if __name__ == "__main__":
    main()
