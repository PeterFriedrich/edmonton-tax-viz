"""The light-mode ramps (docs/UI.md → Light mode, phase 2; DECISIONS 2026-10-08).

Measured on the published distribution, not on the stops: what a reader sees
is where the hoods land on the ramp, and they cluster. The colours are read out
of web/index.html, so a retuned stop is checked without being listed here.
"""
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
HOODS = json.loads((ROOT / "web" / "data" / "neighbourhood_value_per_acre.geojson")
                   .read_text(encoding="utf-8"))["features"]


def _block(start):
    body = HTML[HTML.index(start):]
    return body[:body.index("\n    };")]


def _ramps(block, indent):
    out = {}
    for m in re.finditer(rf"\n{indent}(\w+): \{{(.*?)\n{indent}\}},", block, re.S):
        stops = [(float(t), tuple(int(v) for v in c.split(",")))
                 for t, c in re.findall(r"\[\s*([\d.]+),\s*\[([\d, ]+)\]\]", m.group(2))]
        bg = re.search(r'bg: "#(\w{6})"', m.group(2)).group(1)
        out[m.group(1)] = (stops, tuple(int(bg[i:i + 2], 16) for i in (0, 2, 4)))
    return out


DARK = _ramps(_block("const RAMPS = {"), " " * 6)
LIGHT = _ramps(_block("const THEME_RAMPS = {"), " " * 8)


def _at(stops, t):
    # web/index.html rampColorAt: linear sRGB between stops, rounded.
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        if t <= t1:
            f = (t - t0) / (t1 - t0)
            return tuple(round(c0[k] + f * (c1[k] - c0[k])) for k in range(3))
    return stops[-1][1]


def _lin(u):
    u /= 255
    return ((u + 0.055) / 1.055) ** 2.4 if u > 0.04045 else u / 12.92


def _lum(c):
    r, g, b = map(_lin, c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _contrast(a, b):
    hi, lo = sorted((_lum(a), _lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def _lstar(c):
    y = _lum(c)
    return 116 * y ** (1 / 3) - 16 if y > 216 / 24389 else 24389 / 27 * y


def _landing_ts():
    # The landing view: revenue_per_acre, sqrt colour, METRICS' literal clamp.
    cfg = HTML[HTML.index("      revenue_per_acre: {"):]
    clamp = float(re.search(r"colorClamp: ([\d_]+)", cfg).group(1).replace("_", ""))
    vals = [f["properties"]["revenue_per_acre"] for f in HOODS
            if f["properties"].get("revenue_per_acre") is not None
            and not f["properties"]["is_set_aside"]]
    assert len(vals) > 300
    return [math.sqrt(min(1, max(0, v / clamp))) for v in vals]


def _under_3(ramp, ts):
    stops, bg = ramp
    return sum(_contrast(_at(stops, t), bg) < 3 for t in ts) / len(ts)


def test_light_offers_default_and_cividis_only():
    # glow is dropped in light: its point is a near-white peak against black.
    assert set(LIGHT) == {"current", "cividis"}


def test_light_ramps_run_light_to_dark():
    # Light = low, dark = high: every stop darker than the one before.
    for name, (stops, _) in LIGHT.items():
        ls = [_lstar(c) for _, c in stops]
        assert all(b < a for a, b in zip(ls, ls[1:])), (name, ls)


def test_light_default_never_reaches_near_black():
    # Near-black is the context linework's colour in light mode, so the data
    # stops at purple (Peter, S218). cividis may reach its navy end.
    stops, _ = LIGHT["current"]
    darkest = min(_lstar(c) for _, c in stops)
    assert darkest >= 20, darkest


def test_light_ramps_contrast_no_worse_than_the_dark_default():
    # WCAG 1.4.11 asks 3:1 of a graphical object against what it sits on. On
    # the landing view no light ramp may leave more hoods under 3:1 against its
    # backdrop than the dark default leaves against its own (14.5% at S218).
    ts = _landing_ts()
    floor = _under_3(DARK["current"], ts)
    for name, ramp in LIGHT.items():
        share = _under_3(ramp, ts)
        assert share <= floor, f"{name}: {share:.1%} under 3:1, dark default {floor:.1%}"
