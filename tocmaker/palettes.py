"""Colour systems for TOC graphics.

Each palette maps semantic *roles* to colours so that a figure reads as one system:
exposure (source / stressor), organism (model or population), mechanism (biology),
outcome (health effect), method (analysis). ``ink`` is text / outline, ``paper`` the
background, ``muted`` a light panel tint. None of these is tab10 / d3 default.
"""
from __future__ import annotations

from typing import Dict

ROLES = ("exposure", "organism", "mechanism", "outcome", "method", "neutral")

PALETTES: Dict[str, Dict[str, str]] = {
    # Muted print palette: warm exposure, cool organism, teal mechanism, plum outcome.
    "envtox": {
        "ink": "#1F2937", "ink2": "#4B5563", "paper": "#FFFFFF", "muted": "#F2F5F8", "line": "#9AA5B1",
        "exposure": "#C8553D", "organism": "#4F8FC0", "mechanism": "#2E8B82",
        "outcome": "#7B4B94", "method": "#5F6B7A", "neutral": "#8A94A6",
    },
    # Cooler, more restrained: good for ACS where results are hinted, not shouted.
    "calm": {
        "ink": "#263238", "ink2": "#4F5B62", "paper": "#FFFFFF", "muted": "#EEF3F7", "line": "#90A4AE",
        "exposure": "#D98E4A", "organism": "#3C7FB1", "mechanism": "#4C9A8A",
        "outcome": "#5C6BC0", "method": "#607D8B", "neutral": "#90A4AE",
    },
    # Alert: exposure red, outcome dark red — for hazard-heavy stories (JHM, Environ Pollut).
    "alert": {
        "ink": "#1E1E24", "ink2": "#4A4A52", "paper": "#FFFFFF", "muted": "#F6F1EE", "line": "#A39E9A",
        "exposure": "#B23A48", "organism": "#2F6690", "mechanism": "#C98A1B",
        "outcome": "#8C1C13", "method": "#5D5F71", "neutral": "#9A9A9A",
    },
    # Monochrome blue ink (safe for 1-colour reproduction, very "clean" look).
    "mono": {
        "ink": "#17324D", "ink2": "#3D5A75", "paper": "#FFFFFF", "muted": "#EDF2F7", "line": "#8FA3B8",
        "exposure": "#17324D", "organism": "#17324D", "mechanism": "#17324D",
        "outcome": "#17324D", "method": "#17324D", "neutral": "#8FA3B8",
    },
}


def get_palette(name: str = "envtox") -> Dict[str, str]:
    if name not in PALETTES:
        raise KeyError(f"Unknown palette '{name}'. Known: {', '.join(PALETTES)}")
    return dict(PALETTES[name])


def tint(hex_colour: str, factor: float = 0.85) -> str:
    """Mix a colour toward white; factor 0 = original, 1 = white."""
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = (round(c + (255 - c) * factor) for c in (r, g, b))
    return f"#{r:02X}{g:02X}{b:02X}"


def shade(hex_colour: str, factor: float = 0.25) -> str:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = (round(c * (1 - factor)) for c in (r, g, b))
    return f"#{r:02X}{g:02X}{b:02X}"


def luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    def lin(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(int(h[i:i + 2], 16)) for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(c1: str, c2: str) -> float:
    l1, l2 = luminance(c1), luminance(c2)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)
