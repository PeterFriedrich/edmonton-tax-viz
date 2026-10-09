"""The backdrop grid must stay faint, and must not read as set-aside land.

Peter asked for a square grid that is "light either way" (2026-10-09). A first
prototype at ΔE2000 ~4.7 read too strong in light mode, and light lines read
stronger than dark ones at the same ΔE, so light carries the lower alpha. The
values are read out of web/index.html, so a retuned alpha or a new ramp
backdrop is checked without being listed.
"""
import re

import pytest

from test_set_aside_colour import HTML, _const, de2000

# Visible at all, and no stronger than the prototype that read too strong.
MIN_DE, MAX_DE = 1.5, 4.5
# Same floor test_set_aside_colour uses for adjacent map patches.
SET_ASIDE_FLOOR = 10.0


def _ink(theme):
    m = re.search(r"const GRID_INK = \{ dark: \[([^\]]+)\], light: \[([^\]]+)\] \}", HTML)
    assert m, "GRID_INK"
    *rgb, a = (float(v) for v in m.group(1 if theme == "dark" else 2).split(","))
    return rgb, a


def _backdrops(theme):
    # Dark ramps' bg live in RAMPS; light's in THEME_RAMPS.light.
    start = "const RAMPS = {" if theme == "dark" else "const THEME_RAMPS = {"
    body = HTML[HTML.index(start):]
    body = body[:body.index("\n    };")]
    hexes = set(re.findall(r'bg: "#([0-9a-f]{6})"', body))
    assert hexes, theme
    return [tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) for h in hexes]


def _line(bg, theme):
    rgb, a = _ink(theme)
    return tuple(round(b * (1 - a) + i * a) for b, i in zip(bg, rgb))


@pytest.mark.parametrize("theme", ["dark", "light"])
def test_grid_is_faint_on_every_backdrop(theme):
    for bg in _backdrops(theme):
        de = de2000(bg, _line(bg, theme))
        assert MIN_DE <= de <= MAX_DE, (theme, bg, round(de, 2))


def test_light_grid_is_fainter_than_dark():
    dark = min(de2000(bg, _line(bg, "dark")) for bg in _backdrops("dark"))
    light = max(de2000(bg, _line(bg, "light")) for bg in _backdrops("light"))
    assert light < dark, (round(light, 2), round(dark, 2))


@pytest.mark.parametrize("theme", ["dark", "light"])
def test_grid_line_is_not_set_aside_grey(theme):
    aside = _const("SET_ASIDE_COLOR", theme)
    for bg in _backdrops(theme):
        assert de2000(_line(bg, theme), aside) >= SET_ASIDE_FLOOR, (theme, bg)
