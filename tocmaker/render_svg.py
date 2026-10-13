"""Scene -> SVG string. Canvas units are points; the root carries physical size in mm."""
from __future__ import annotations

from typing import Any, Dict, List
from xml.sax.saxutils import escape

from . import icons as iconlib
from .layout import Scene
from .presets import Preset, pt_to_mm

FONT_STACK = "Arial, Helvetica, 'Liberation Sans', sans-serif"


def _num(v: float) -> str:
    return f"{v:.2f}".rstrip("0").rstrip(".")


def render_svg(scene: Scene, preset: Preset, embed_fonts_note: bool = True) -> str:
    W, H = preset.width_pt, preset.height_pt
    out: List[str] = []
    out.append(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
               f'width="{pt_to_mm(W):.3f}mm" height="{pt_to_mm(H):.3f}mm" viewBox="0 0 {_num(W)} {_num(H)}" '
               f'font-family="{FONT_STACK}">')
    out.append("<defs>")
    colors = sorted({e["color"] for e in scene if e["type"] == "arrow"})
    for c in colors:
        cid = "arw_" + c.lstrip("#").lower()
        out.append(f'<marker id="{cid}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4.5" markerHeight="4.5" '
                   f'orient="auto-start-reverse" markerUnits="strokeWidth"><path d="M0,0.5 L9,5 L0,9.5 z" fill="{c}"/></marker>')
        out.append(f'<marker id="{cid}_inh" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" '
                   f'orient="auto" markerUnits="strokeWidth"><rect x="7" y="0" width="2.2" height="10" fill="{c}"/></marker>')
    out.append("</defs>")
    for e in scene:
        t = e["type"]
        if t == "rect":
            stroke = e.get("stroke")
            sattr = f' stroke="{stroke}" stroke-width="{_num(e.get("stroke_width", 0.5))}"' if stroke else ""
            extra = f' data-panel="{e["panel"]}" data-role="{e["role"]}"' if "panel" in e else ""
            out.append(f'<rect x="{_num(e["x"])}" y="{_num(e["y"])}" width="{_num(e["w"])}" height="{_num(e["h"])}" '
                       f'rx="{_num(e.get("rx", 0))}" fill="{e["fill"]}"{sattr}{extra}/>')
        elif t == "text":
            _text(out, e)
        elif t == "icon":
            out.append(iconlib.placed_svg(e["icon"], e["x"], e["y"], e["w"], e["h"], e["primary"], e["accent"],
                                          e.get("tint", "auto"), e.get("opacity", 1.0), e.get("flip", False)))
        elif t == "badge":
            r = e["h"] / 2
            out.append(f'<rect x="{_num(e["x"])}" y="{_num(e["y"])}" width="{_num(e["w"])}" height="{_num(e["h"])}" '
                       f'rx="{_num(r)}" fill="{e["fill"]}"/>')
            lines = e.get("lines") or [e["text"]]
            lh = e["size"] * 1.25
            y0 = e["y"] + e["h"] / 2 - lh * (len(lines) - 1) / 2
            for i, ln in enumerate(lines):
                out.append(f'<text x="{_num(e["x"] + e["w"] / 2)}" y="{_num(y0 + i * lh)}" font-size="{_num(e["size"])}" '
                           f'font-weight="bold" fill="{e["color"]}" text-anchor="middle" dominant-baseline="central">'
                           f'{escape(ln)}</text>')
        elif t == "arrow":
            _arrow(out, e)
        elif t == "line":
            out.append(f'<line x1="{_num(e["x1"])}" y1="{_num(e["y1"])}" x2="{_num(e["x2"])}" y2="{_num(e["y2"])}" '
                       f'stroke="{e["color"]}" stroke-width="{_num(e.get("width", 0.8))}"/>')
    out.append("</svg>")
    return "\n".join(out)


def _text(out: List[str], e: Dict[str, Any]):
    size, lh = e["size"], e["line_height"]
    weight = "bold" if e["weight"] == "bold" else "normal"
    align = e.get("align", "center")
    if align == "center":
        x, anchor = e["x"] + e["w"] / 2, "middle"
    elif align == "right":
        x, anchor = e["x"] + e["w"], "end"
    else:
        x, anchor = e["x"], "start"
    # first baseline: top + ascent (~0.8 em for Arial-like faces) + half the leading
    y0 = e["y"] + size * 0.8 + (lh - size) / 2
    out.append(f'<text x="{_num(x)}" y="{_num(y0)}" font-size="{_num(size)}" font-weight="{weight}" fill="{e["color"]}" '
               f'text-anchor="{anchor}">')
    for i, ln in enumerate(e["lines"]):
        dy = "0" if i == 0 else _num(lh)
        out.append(f'<tspan x="{_num(x)}" dy="{dy}">{escape(ln)}</tspan>')
    out.append("</text>")


def _arrow(out: List[str], e: Dict[str, Any]):
    c = e["color"]
    cid = "arw_" + c.lstrip("#").lower()
    dash = ' stroke-dasharray="3 2"' if e.get("style") == "dashed" else ""
    marker = f"url(#{cid}_inh)" if e.get("style") == "inhibit" else f"url(#{cid})"
    x1, y1, x2, y2 = e["x1"], e["y1"], e["x2"], e["y2"]
    out.append(f'<line x1="{_num(x1)}" y1="{_num(y1)}" x2="{_num(x2)}" y2="{_num(y2)}" stroke="{c}" '
               f'stroke-width="{_num(e.get("width", 1.4))}" stroke-linecap="round"{dash} marker-end="{marker}"/>')
    if e.get("label"):
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        horizontal = abs(x2 - x1) >= abs(y2 - y1)
        ty = my - 2.0 if horizontal else my
        tx = mx if horizontal else mx + 2.5
        anchor = "middle" if horizontal else "start"
        out.append(f'<text x="{_num(tx)}" y="{_num(ty)}" font-size="{_num(e["size"])}" fill="{c}" text-anchor="{anchor}" '
                   f'font-style="italic">{escape(e["label"])}</text>')
