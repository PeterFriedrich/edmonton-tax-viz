"""The light chrome tokens (docs/UI.md → Light mode, phase 4).

styles.css declares the light values twice — under the OS media query and under
[data-theme="light"] — because CSS cannot share one block between the two. The
failure modes are silent: the copies drift, a new :root token gets no light
value (so a dark colour shows in light), or a light ink is too faint to read.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / "web" / "styles.css").read_text(encoding="utf-8")
HTML = (ROOT / "web" / "index.html").read_text(encoding="utf-8")


def _decls(body):
    body = re.sub(r"/\*.*?\*/", "", body, flags=re.S)   # comments name tokens too
    return dict(re.findall(r"(--[\w-]+):\s*([^;]+);", body))


def _rule(selector):
    i = CSS.index(selector + " {")
    return CSS[i:CSS.index("}", i)]


ROOT_TOKENS = _decls(_rule("\n:root"))
MEDIA = _decls(_rule('@media (prefers-color-scheme: light) {\n  :root:not([data-theme="dark"])'))
LIGHT = _decls(_rule(':root[data-theme="light"]'))


def _rgba(v):
    if v.startswith("#"):
        return tuple(int(v[i:i + 2], 16) for i in (1, 3, 5)) + (1.0,)
    r, g, b, a = (float(x) for x in re.match(r"rgba\(([^)]*)\)", v).group(1).split(","))
    return (r, g, b, a)


def _over(fg, bg):
    a = fg[3]
    return tuple(fg[i] * a + bg[i] * (1 - a) for i in range(3)) + (1.0,)


def _lum(c):
    ch = [v / 255 for v in c[:3]]
    ch = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in ch]
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def _contrast(a, b):
    hi, lo = sorted((_lum(a), _lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def test_both_light_blocks_are_identical():
    assert MEDIA == LIGHT


def test_every_root_token_has_a_light_value():
    assert set(LIGHT) == set(ROOT_TOKENS)


def test_every_referenced_token_is_defined():
    used = set(re.findall(r"var\((--[\w-]+)\)", CSS + HTML))
    assert used - set(ROOT_TOKENS) == set()


def test_light_inks_are_legible():
    bg = _rgba(LIGHT["--bg"])
    surfaces = {
        "map": bg,
        "pod": _over(_rgba(LIGHT["--pod-bg"]), bg),
        "read": _over(_rgba(LIGHT["--read-bg"]), bg),
        "sheet": _over(_rgba(LIGHT["--sheet-bg"]), bg),
    }
    # Text: WCAG 1.4.3. --ink-off / --ink-disabled are dim on purpose.
    text = ["--ink", "--ink-2", "--ink-3", "--ink-2-bright", "--ink-toast", "--ink-tip",
            "--ink-revcut", "--ink-faint", "--ink-caret-mobile", "--accent-ink"]
    # Marks: WCAG 1.4.11 graphical objects.
    marks = ["--mark", "--mark-2", "--spinner"]
    low = []
    for name, s in surfaces.items():
        for t in text:
            if _contrast(_rgba(LIGHT[t]), s) < 4.5:
                low.append((t, name))
        for t in marks:
            if _contrast(_rgba(LIGHT[t]), s) < 3.0:
                low.append((t, name))
    banner = _over(_rgba(LIGHT["--banner-bg"]), bg)
    if _contrast(_rgba(LIGHT["--banner-ink"]), banner) < 4.5:
        low.append(("--banner-ink", "banner"))
    if _contrast(_rgba(LIGHT["--ink-on-accent"]), _rgba(LIGHT["--accent"])) < 4.5:
        low.append(("--ink-on-accent", "accent"))
    assert low == []


def test_light_ink_keeps_the_dark_order():
    # The ink steps are a hierarchy; a light value must not swap two of them.
    bg = _rgba(LIGHT["--bg"])
    dark_bg = _rgba(ROOT_TOKENS["--bg"])
    steps = ["--ink-tip", "--ink", "--ink-toast", "--ink-2-bright", "--ink-2", "--ink-off"]
    dark = [_contrast(_rgba(ROOT_TOKENS[t]), dark_bg) for t in steps]
    light = [_contrast(_rgba(LIGHT[t]), bg) for t in steps]
    assert dark == sorted(dark, reverse=True)
    assert light == sorted(light, reverse=True)
