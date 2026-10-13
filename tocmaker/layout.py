"""Layout engine: TocSpec + Preset -> scene (list of drawing primitives in points).

The scene is renderer-agnostic so the SVG and PPTX writers produce the same picture.
Primitive types: rect, text, icon, arrow, badge, line.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from . import icons as iconlib
from .palettes import get_palette, shade, tint
from .presets import Preset, get_preset
from .spec import Arrow, Panel, TocSpec
from .textmetrics import text_width, wrap

Scene = List[Dict[str, Any]]


@dataclass
class Box:
    x: float
    y: float
    w: float
    h: float

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.h / 2

    @property
    def right(self):
        return self.x + self.w

    @property
    def bottom(self):
        return self.y + self.h


class Layout:
    def __init__(self, spec: TocSpec, preset: Optional[Preset] = None):
        self.spec = spec
        self.preset = preset or get_preset(spec.journal)
        self.pal = get_palette(spec.palette)
        self.W, self.H = self.preset.width_pt, self.preset.height_pt
        self.font = float(spec.font_pt or self.preset.pref_font_pt)
        self.small = max(self.preset.min_font_pt, self.font - 1.5)
        self.margin = float(spec.options.get("margin_pt", 4.0))
        self.gap = float(spec.options.get("gap_pt", 10.0))   # space for arrows between panels
        self.scene: Scene = []
        self.boxes: Dict[int, Box] = {}
        self.anchors: Dict[int, Box] = {}   # icon-area boxes (arrow anchors)
        self.warnings: List[str] = []

    # ------------------------------------------------------------------ public
    def build(self) -> Scene:
        self.scene = []
        if self.spec.options.get("background", True):
            self.scene.append(dict(type="rect", x=0, y=0, w=self.W, h=self.H, rx=0, fill=self.pal["paper"], stroke=None))
        top = self.margin
        bottom = self.H - self.margin
        if self.spec.title:
            size = self.font + 1
            lines = wrap(self.spec.title, self.W - 2 * self.margin, size, "bold", 2)
            self._text(self.margin, top, self.W - 2 * self.margin, lines, size, "bold", self.pal["ink"], "center")
            top += len(lines) * size * 1.2 + 2
        if self.spec.footer:
            lines = wrap(self.spec.footer, self.W - 2 * self.margin, self.small, "regular", 1)
            fh = len(lines) * self.small * 1.2
            self._text(self.margin, bottom - fh, self.W - 2 * self.margin, lines, self.small, "regular", self.pal["neutral"], "center")
            bottom -= fh + 2
        area = Box(self.margin, top, self.W - 2 * self.margin, bottom - top)
        getattr(self, f"_layout_{self.spec.template}")(area)
        self._arrows()
        return self.scene

    # ------------------------------------------------------------------ templates
    def _row(self, idxs: List[int], area: Box, compact: bool = False):
        """Lay panels side by side; text blocks share one top line so icons align across the row."""
        panels = self.spec.panels
        n = len(idxs)
        weights = [panels[i].weight for i in idxs]
        avail = area.w - self.gap * (n - 1)
        widths = [avail * w / sum(weights) for w in weights]
        pad = 3.0 if not compact else 2.0
        block = max(self._block_height(panels[i], widths[k] - 2 * pad, compact) for k, i in enumerate(idxs))
        x = area.x
        for k, i in enumerate(idxs):
            self._panel(i, Box(x, area.y, widths[k], area.h), compact=compact, block_h=block)
            x += widths[k] + self.gap

    def _label_gap(self):
        """Widen the inter-panel gap when arrows carry labels so the label fits between panels."""
        labelled = [a.label for a in self.spec.arrows if a.label and a.style != "none"]
        if labelled:
            need = max(text_width(l, self.small, "regular") for l in labelled) + 4.0
            self.gap = max(self.gap, need)

    def _layout_flow(self, area: Box):
        n = len(self.spec.panels)
        if not self.spec.arrows:
            self.spec.arrows = [Arrow(i, i + 1) for i in range(n - 1)]
        self._label_gap()
        self._row(list(range(n)), area)

    def _layout_cohort(self, area: Box):
        # same as flow but the first panel is wider (population + badge) and arrows carry labels
        for p in self.spec.panels[:1]:
            p.weight = max(p.weight, 1.25)
        self._layout_flow(area)

    def _layout_split(self, area: Box):
        s = self.spec
        left, center, right = s.left, s.center, s.right
        col_gap = self.gap
        wl = area.w * (0.30 if left else 0)
        wr = area.w * (0.30 if right else 0)
        wc = area.w - wl - wr - col_gap * ((1 if left else 0) + (1 if right else 0))
        x = area.x
        if left:
            self._stack(left, Box(x, area.y, wl, area.h))
            x += wl + col_gap
        self._panel(center, Box(x, area.y, wc, area.h))
        x += wc + col_gap
        if right:
            self._stack(right, Box(x, area.y, wr, area.h))
        if not s.arrows:
            s.arrows = [Arrow(i, center) for i in left] + [Arrow(center, i) for i in right]

    def _stack(self, idxs: List[int], box: Box):
        n = len(idxs)
        vgap = 3.0
        h = (box.h - vgap * (n - 1)) / n
        for k, i in enumerate(idxs):
            self._panel(i, Box(box.x, box.y + k * (h + vgap), box.w, h), compact=n > 1)

    def _layout_hub(self, area: Box):
        s = self.spec
        c = s.center or 0
        sats = [i for i in range(len(s.panels)) if i != c]
        n = len(sats)
        cw, ch = min(area.w * 0.34, area.h * 0.9), area.h * 0.9
        cbox = Box(area.cx - cw / 2, area.cy - ch / 2, cw, ch)
        self._panel(c, cbox)
        # satellites: left column and right column, split evenly
        left = sats[: (n + 1) // 2]
        right = sats[(n + 1) // 2:]
        side_w = (area.w - cw) / 2 - self.gap
        if left:
            self._stack(left, Box(area.x, area.y, side_w, area.h))
        if right:
            self._stack(right, Box(cbox.right + self.gap, area.y, side_w, area.h))
        if not s.arrows and s.hub_direction != "none":
            s.arrows = [Arrow(i, c) if s.hub_direction == "in" else Arrow(c, i) for i in sats]

    def _layout_cycle(self, area: Box):
        s = self.spec
        n = len(s.panels)
        r_x, r_y = area.w * 0.36, area.h * 0.30
        pw, ph = area.w * 0.26, area.h * 0.40
        for k in range(n):
            ang = -math.pi / 2 + 2 * math.pi * k / n
            cx, cy = area.cx + r_x * math.cos(ang), area.cy + r_y * math.sin(ang)
            self._panel(k, Box(cx - pw / 2, cy - ph / 2, pw, ph), compact=True)
        if not s.arrows:
            s.arrows = [Arrow(k, (k + 1) % n) for k in range(n)]

    def _layout_two_row(self, area: Box):
        s = self.spec
        conv = s.converge
        rows = s.rows
        body_w = area.w * (0.72 if conv is not None else 1.0)
        rh = (area.h - 3.0 * (len(rows) - 1)) / len(rows)
        for r, idxs in enumerate(rows):
            y = area.y + r * (rh + 3.0)
            self._row(idxs, Box(area.x, y, body_w, rh), compact=True)
        if conv is not None:
            cw = area.w - body_w - self.gap
            self._panel(conv, Box(area.x + body_w + self.gap, area.y, cw, area.h))
        if not s.arrows:
            for idxs in rows:
                s.arrows += [Arrow(a, b) for a, b in zip(idxs, idxs[1:])]
                if conv is not None and idxs:
                    s.arrows.append(Arrow(idxs[-1], conv))

    # ------------------------------------------------------------------ panel composition
    def _fit_wrap(self, text: str, w: float, size: float, weight: str, max_lines: int):
        """Wrap, shrinking the type (down to the journal floor) when a word or line will not fit."""
        floor = self.preset.min_font_pt
        s = size
        while True:   # pass 1: shrink without breaking words
            lines = wrap(text, w, s, weight, max_lines, break_words=False)
            if all(text_width(l, s, weight) <= w for l in lines) and len(lines) <= max_lines:
                return lines, s
            if s - 0.5 < floor - 1e-6:
                break
            s -= 0.5
        s = max(floor, size - 1.0)   # pass 2: hyphenate long words at a modest size
        while True:
            lines = wrap(text, w, s, weight, max_lines, break_words=True)
            if all(text_width(l, s, weight) <= w for l in lines) and len(lines) <= max_lines:
                return lines, s
            if s - 0.5 < floor - 1e-6:
                return lines, s
            s -= 0.5

    def _text_block(self, p: Panel, w: float, compact: bool):
        size = self.font if not compact else max(self.preset.min_font_pt, self.font - 1)
        label_lines, size = self._fit_wrap(p.label, w, size, "bold", 3) if p.label else ([], size)
        lh = size * 1.18
        sub_lines, _ = self._fit_wrap(p.sublabel, w, self.small, "regular", 2) if p.sublabel else ([], 0)
        item_lines: List[str] = []
        for it in p.items:
            item_lines += wrap("• " + it, w, self.small, "regular", 1)
        text_h = len(label_lines) * lh + len(sub_lines) * self.small * 1.18 + len(item_lines) * self.small * 1.18
        badge_lines, bsize = self._badge_fit(p.badge, w) if p.badge else ([], size)
        badge_h = (bsize * 1.25 * len(badge_lines) + bsize * 0.45) if p.badge else 0.0
        block_h = text_h + badge_h + (1.5 if p.badge and text_h else 0)
        return size, lh, label_lines, sub_lines, item_lines, text_h, badge_h, block_h, badge_lines, bsize

    def _badge_fit(self, text: str, w: float):
        """Badge text: shrink to the floor, then wrap to two lines."""
        bsize = self.font
        floor = self.preset.min_font_pt
        inner = w - 2.0
        while text_width(text, bsize, "bold") + bsize * 0.9 > inner and bsize - 0.5 >= floor:
            bsize -= 0.5
        if text_width(text, bsize, "bold") + bsize * 0.9 <= inner:
            return [text], bsize
        bsize = max(floor, self.font - 1.0)
        lines = wrap(text, inner - bsize * 0.6, bsize, "bold", 2)
        return lines, bsize

    def _block_height(self, p: Panel, w: float, compact: bool) -> float:
        return self._text_block(p, w, compact)[-1]

    def _panel(self, idx: int, box: Box, compact: bool = False, block_h: Optional[float] = None):
        p = self.spec.panels[idx]
        pal = self.pal
        role_col = pal.get(p.role, pal["neutral"])
        self.boxes[idx] = box
        pad = 3.0 if not compact else 2.0
        if p.box:
            self.scene.append(dict(type="rect", x=box.x, y=box.y, w=box.w, h=box.h, rx=4.0,
                                   fill=tint(role_col, 0.88), stroke=None, role=p.role, panel=idx))
        inner = Box(box.x + pad, box.y + pad, box.w - 2 * pad, box.h - 2 * pad)
        # --- text block (bottom): label, sublabel, items, badge
        size, lh, label_lines, sub_lines, item_lines, text_h, badge_h, own_block, badge_lines, bsize = self._text_block(p, inner.w, compact)
        block_h = max(own_block, block_h or 0.0)
        # --- icon area (top)
        icon_area_h = max(0.0, inner.h - block_h - (2.0 if block_h else 0))
        if p.icons and icon_area_h < size * 1.5:
            self.warnings.append(f"panel {idx} '{p.label}': not enough room for icons (icon area {icon_area_h:.1f} pt)")
        icon_box = Box(inner.x, inner.y, inner.w, icon_area_h)
        self.anchors[idx] = icon_box if p.icons else inner
        self._icons(p, icon_box, role_col)
        # --- place text block below icons
        y = inner.y + icon_area_h + (2.0 if block_h else 0)
        if label_lines:
            self._text(inner.x, y, inner.w, label_lines, size, "bold", pal["ink"], "center", panel=idx)
            y += len(label_lines) * lh
        if sub_lines:
            self._text(inner.x, y, inner.w, sub_lines, self.small, "regular", pal.get("ink2", pal["ink"]), "center", panel=idx)
            y += len(sub_lines) * self.small * 1.18
        if item_lines:
            self._text(inner.x, y, inner.w, item_lines, self.small, "regular", pal["ink"], "left", panel=idx)
            y += len(item_lines) * self.small * 1.18
        if p.badge:
            y += 1.5 if text_h else 0
            widest = max(text_width(l, bsize, "bold") for l in badge_lines)
            if widest + bsize * 0.6 > inner.w + 0.5:
                self.warnings.append(f"panel {idx}: badge '{p.badge}' wider than its box even at {bsize} pt / 2 lines")
            bw = min(inner.w, widest + bsize * 1.2)
            self.scene.append(dict(type="badge", x=inner.cx - bw / 2, y=y, w=bw, h=badge_h, text=p.badge, lines=badge_lines,
                                   size=bsize, fill=role_col, color="#FFFFFF", panel=idx))
            y += badge_h
        if y > inner.bottom + 0.5:
            self.warnings.append(f"panel {idx} '{p.label}': text block overflows panel by {y - inner.bottom:.1f} pt")

    def _icons(self, p: Panel, box: Box, role_col: str):
        if not p.icons or box.h <= 0:
            return
        n = len(p.icons)
        scales = [max(0.2, ic.scale) for ic in p.icons]
        aspects = []
        for ic in p.icons:
            try:
                aspects.append(max(0.45, min(2.2, iconlib.aspect(iconlib.get(ic.id).path))))
            except KeyError:
                aspects.append(1.0)
        gap = 2.0
        if p.icon_layout == "overlap":
            gap = -box.h * 0.25
        if p.icon_layout == "stack":
            h_each = (box.h - gap * (n - 1)) / n
            y = box.y
            for ic, sc, a in zip(p.icons, scales, aspects):
                h = min(h_each, box.w / a) * sc
                w = h * a
                self._icon(ic, box.cx - w / 2, y + (h_each - h) / 2, w, h, role_col)
                y += h_each + gap
            return
        # row: start from full height, shrink uniformly until the widths fit
        unit = box.h
        widths = [unit * sc * a for sc, a in zip(scales, aspects)]
        total = sum(widths) + gap * (n - 1)
        if total > box.w:
            unit *= box.w / total
            widths = [unit * sc * a for sc, a in zip(scales, aspects)]
            total = sum(widths) + gap * (n - 1)
        x = box.cx - total / 2
        for ic, sc, a, w in zip(p.icons, scales, aspects, widths):
            h = unit * sc
            self._icon(ic, x, box.cy - h / 2, w, h, role_col)
            x += w + gap

    def _icon(self, ref, x, y, w, h, role_col):
        try:
            info = iconlib.get(ref.id)
        except KeyError as e:
            self.warnings.append(str(e))
            self.scene.append(dict(type="rect", x=x, y=y, w=w, h=h, rx=2, fill="#DDDDDD", stroke="#999999",
                                   stroke_width=0.5, placeholder=ref.id))
            return
        primary = self.pal["ink"]
        if info.monochrome and ref.tint in ("auto", "mono"):
            primary = shade(role_col, 0.12)
        self.scene.append(dict(type="icon", x=x, y=y, w=w, h=h, icon=info, primary=primary, accent=role_col,
                               tint=ref.tint, flip=ref.flip, opacity=ref.opacity))

    def _text(self, x, y, w, lines, size, weight, color, align, panel=None):
        if not lines:
            return
        for ln in lines:
            tw = text_width(ln, size, weight)
            if tw > w + 0.5:
                self.warnings.append(f"text '{ln}' ({tw:.1f} pt) wider than its box ({w:.1f} pt)")
        self.scene.append(dict(type="text", x=x, y=y, w=w, lines=list(lines), size=size, weight=weight, color=color,
                               align=align, line_height=size * 1.18, panel=panel))

    # ------------------------------------------------------------------ arrows
    def _arrows(self):
        pal = self.pal
        for a in self.spec.arrows:
            if a.style == "none":
                continue
            A, B = self.boxes.get(a.src), self.boxes.get(a.dst)
            if A is None or B is None:
                continue
            aa, bb = self.anchors.get(a.src, A), self.anchors.get(a.dst, B)
            color = pal.get(a.color, a.color) if a.color else pal["line"]
            if a.color in pal:
                color = pal[a.color]
            x1, y1, x2, y2 = self._edge_points(A, B, aa, bb)
            self.scene.append(dict(type="arrow", x1=x1, y1=y1, x2=x2, y2=y2, color=color, width=1.4,
                                   style=a.style, label=a.label, size=self.small))

    def _edge_points(self, A: Box, B: Box, aa: Box, bb: Box) -> Tuple[float, float, float, float]:
        pad = 1.5
        dx, dy = B.cx - A.cx, B.cy - A.cy
        if abs(dx) * A.h >= abs(dy) * A.w:   # mostly horizontal
            y = (aa.cy + bb.cy) / 2 if abs(aa.cy - bb.cy) < 0.3 * A.h else None
            if dx > 0:
                return (A.right + pad, y if y is not None else aa.cy, B.x - pad, y if y is not None else bb.cy)
            return (A.x - pad, y if y is not None else aa.cy, B.right + pad, y if y is not None else bb.cy)
        if dy > 0:
            return (A.cx, A.bottom + pad, B.cx, B.y - pad)
        return (A.cx, A.y - pad, B.cx, B.bottom + pad)


def build_scene(spec: TocSpec, preset: Optional[Preset] = None) -> Tuple[Scene, Layout]:
    lay = Layout(spec, preset)
    scene = lay.build()
    return scene, lay
