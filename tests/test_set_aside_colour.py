"""The set-aside colour must stay perceptibly distinct from every colour a real
hood can take beside it (FINDINGS_colour_claims.md claim 2).

Cividis passed through a neutral grey ΔE2000 1.9 from SET_ASIDE_COLOR, so four
real hoods rendered as set-aside land on the public build. A comment asserted
the distinctness; nothing measured it. These tests read the colours out of
web/index.html, so a new ramp or a retuned stop is checked without being listed.
"""
import math
import re
from pathlib import Path

import pytest

HTML = (Path(__file__).resolve().parents[1] / "web" / "index.html").read_text(encoding="utf-8")
# ~2.3 is a just-noticeable difference; adjacent map patches need well above it.
FLOOR = 10.0


def _rgb(text):
    return tuple(int(v) for v in re.findall(r"\d+", text)[:3])


def _const(name):
    m = re.search(rf"const {name} = \[([^\]]+)\]", HTML)
    assert m, name
    return _rgb(m.group(1))


def _ramps():
    body = HTML[HTML.index("const RAMPS = {"):]
    body = body[:body.index("\n    };")]
    ramps = {}
    for m in re.finditer(r"\n      (\w+): \{(.*?)\n      \},", body, re.S):
        stops = [(float(t), _rgb(c)) for t, c in
                 re.findall(r"\[\s*([\d.]+),\s*\[([^\]]+)\]\]", m.group(2))]
        aside = re.search(r"setAside: \[([^\]]+)\]", m.group(2))
        ramps[m.group(1)] = (stops, _rgb(aside.group(1)) if aside else None)
    return ramps


def _sample(stops, n=400):
    out = []
    for i in range(n + 1):
        t = i / n
        for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
            if t <= t1:
                f = (t - t0) / (t1 - t0)
                out.append(tuple(round(c0[k] + f * (c1[k] - c0[k])) for k in range(3)))
                break
    return out


def _lab(c):
    def lin(u):
        u /= 255
        return ((u + 0.055) / 1.055) ** 2.4 if u > 0.04045 else u / 12.92
    r, g, b = map(lin, c)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    return 116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))


def de2000(c1, c2):
    return _de2000_lab(_lab(c1), _lab(c2))


def _de2000_lab(lab1, lab2):
    """CIEDE2000 (Sharma, Wu & Dalal 2005)."""
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    cb = (math.hypot(a1, b1) + math.hypot(a2, b2)) / 2
    g = 0.5 * (1 - math.sqrt(cb ** 7 / (cb ** 7 + 25 ** 7)))
    a1p, a2p = (1 + g) * a1, (1 + g) * a2
    c1p, c2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1 = math.degrees(math.atan2(b1, a1p)) % 360
    h2 = math.degrees(math.atan2(b2, a2p)) % 360
    dh = 0.0
    if c1p * c2p:
        dh = h2 - h1
        dh = dh - 360 if dh > 180 else dh + 360 if dh < -180 else dh
    dH = 2 * math.sqrt(c1p * c2p) * math.sin(math.radians(dh / 2))
    lb, cbp = (L1 + L2) / 2, (c1p + c2p) / 2
    if not c1p * c2p:
        hb = h1 + h2
    elif abs(h1 - h2) <= 180:
        hb = (h1 + h2) / 2
    else:
        hb = (h1 + h2 + 360) / 2 if h1 + h2 < 360 else (h1 + h2 - 360) / 2
    t = (1 - 0.17 * math.cos(math.radians(hb - 30)) + 0.24 * math.cos(math.radians(2 * hb))
         + 0.32 * math.cos(math.radians(3 * hb + 6)) - 0.20 * math.cos(math.radians(4 * hb - 63)))
    dth = 30 * math.exp(-(((hb - 275) / 25) ** 2))
    rc = 2 * math.sqrt(cbp ** 7 / (cbp ** 7 + 25 ** 7))
    sl = 1 + 0.015 * (lb - 50) ** 2 / math.sqrt(20 + (lb - 50) ** 2)
    sc, sh = 1 + 0.045 * cbp, 1 + 0.015 * cbp * t
    rt = -math.sin(math.radians(2 * dth)) * rc
    dl, dc = L2 - L1, c2p - c1p
    return math.sqrt((dl / sl) ** 2 + (dc / sc) ** 2 + (dH / sh) ** 2 + rt * (dc / sc) * (dH / sh))


@pytest.mark.parametrize("lab1, lab2, expected", [
    # Sharma, Wu & Dalal (2005) Table 1, pairs 1, 7 and 17.
    ((50.0, 2.6772, -79.7751), (50.0, 0.0, -82.7485), 2.0425),
    ((50.0, 0.0, 0.0), (50.0, -1.0, 2.0), 2.3669),
    ((50.0, 2.5, 0.0), (73.0, 25.0, -18.0), 27.1492),
])
def test_de2000_matches_published_reference_pairs(lab1, lab2, expected):
    assert _de2000_lab(lab1, lab2) == pytest.approx(expected, abs=1e-4)


RAMPS = _ramps()


def test_every_ramp_was_parsed():
    assert set(RAMPS) >= {"current", "glow", "cividis"}
    assert all(len(stops) >= 2 for stops, _ in RAMPS.values())


@pytest.mark.parametrize("name", sorted(RAMPS))
def test_set_aside_is_distinct_from_its_ramp(name):
    stops, own = RAMPS[name]
    aside = own or _const("SET_ASIDE_COLOR")
    worst = min(_sample(stops), key=lambda c: de2000(aside, c))
    assert de2000(aside, worst) >= FLOOR, (name, aside, worst, round(de2000(aside, worst), 1))


def test_shared_set_aside_is_distinct_from_glass_plane_and_diverging_ramp():
    """Surfaces that keep SET_ASIDE_COLOR whatever the ramp: the Glass ground
    plane and the Infill/Change/Deviation diverging ramp (rampSetAside's comment)."""
    aside = _const("SET_ASIDE_COLOR")
    assert de2000(aside, _const("GLASS_PLANE_COLOR")) >= FLOOR
    centre = _const("INFILL_CENTER")
    for end in (_const("INFILL_POS"), _const("INFILL_NEG")):
        arm = _sample([(0.0, centre), (1.0, end)])
        assert min(de2000(aside, c) for c in arm) >= FLOOR
