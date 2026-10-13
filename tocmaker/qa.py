"""QA gates for a rendered TOC: size, type floor, word budget, overflow, contrast, licences."""
from __future__ import annotations

import os
import re
from typing import Any, Dict, List

from .layout import Layout, Scene
from .palettes import contrast_ratio
from .presets import Preset
from .spec import TocSpec


def run_qa(spec: TocSpec, scene: Scene, layout: Layout, preset: Preset, svg: str, png_path: str = "") -> Dict[str, Any]:
    issues: List[Dict[str, str]] = []

    def add(level: str, code: str, msg: str):
        issues.append(dict(level=level, code=code, message=msg))

    # canvas size
    m = re.search(r'width="([0-9.]+)mm" height="([0-9.]+)mm"', svg)
    if m:
        w, h = float(m.group(1)), float(m.group(2))
        if abs(w - preset.width_mm) > 0.05 or abs(h - preset.height_mm) > 0.05:
            add("error", "size", f"canvas {w:.1f}x{h:.1f} mm differs from preset {preset.width_mm:.1f}x{preset.height_mm:.1f} mm")
    # fonts
    sizes = [e["size"] for e in scene if e["type"] in ("text", "badge")]
    if sizes and min(sizes) < preset.min_font_pt - 1e-6:
        add("error", "font_floor", f"smallest text {min(sizes):.1f} pt < journal floor {preset.min_font_pt} pt")
    # words
    words = 0
    for e in scene:
        if e["type"] == "text":
            words += sum(len(l.split()) for l in e["lines"])
        elif e["type"] == "badge":
            words += len(e["text"].split())
    if words > preset.max_words:
        add("warn", "word_budget", f"{words} words in graphic; {preset.journal.split(' (')[0]} guidance suggests <= {preset.max_words}")
    # layout warnings (overflow, missing icons)
    for wmsg in layout.warnings:
        add("error" if ("overflow" in wmsg or "wider" in wmsg) else "warn", "layout", wmsg)
    # contrast of label text on panel tint
    panel_fill = {e["panel"]: e["fill"] for e in scene if e["type"] == "rect" and "panel" in e}
    for e in scene:
        if e["type"] == "text" and e.get("panel") in panel_fill:
            cr = contrast_ratio(e["color"], panel_fill[e["panel"]])
            if cr < 3.0:
                add("warn", "contrast", f"text '{e['lines'][0][:30]}' contrast {cr:.1f}:1 on panel tint (< 3:1)")
    for e in scene:
        if e["type"] == "badge" and contrast_ratio(e["color"], e["fill"]) < 3.0:
            add("warn", "contrast", f"badge '{e['text']}' low contrast")
    # ACS: results in TOC
    if not preset.reveal_results:
        for e in scene:
            if e["type"] == "badge" and re.search(r"\d", e["text"]):
                add("info", "acs_results", f"ACS TOC graphics traditionally hint rather than state results; badge '{e['text']}' shows a number")
    # licences / attribution
    lic_notes = set()
    for e in scene:
        if e["type"] == "icon":
            ic = e["icon"]
            lic = ic.license.lower()
            if lic.startswith("cc-by-sa"):
                add("warn", "license", f"icon {ic.id} is {ic.license}: share-alike is awkward for a journal figure; prefer CC0/MIT")
            elif lic.startswith("cc-by"):
                lic_notes.add(f"{ic.id} ({ic.license}, {ic.author or 'author unknown'}) — needs attribution in the manuscript (e.g. Acknowledgements/SI)")
            elif lic in ("unknown", "varies"):
                add("warn", "license", f"icon {ic.id}: licence unknown — check before submission")
    for n in sorted(lic_notes):
        add("info", "attribution", n)
    # raster check
    if "<image" in svg:
        add("warn", "raster", "SVG embeds raster <image> elements; journals prefer pure vector")
    n_icons = sum(1 for e in scene if e["type"] == "icon")
    if n_icons > 8:
        add("warn", "clutter", f"{n_icons} icons — a TOC should carry one message; consider trimming")
    px = None
    if png_path and os.path.exists(png_path):
        try:
            from PIL import Image
            px = Image.open(png_path).size
        except Exception:
            pass
    status = "fail" if any(i["level"] == "error" for i in issues) else ("warn" if any(i["level"] == "warn" for i in issues) else "pass")
    return dict(status=status, journal=preset.journal, size_mm=[round(preset.width_mm, 2), round(preset.height_mm, 2)],
                png_px=list(px) if px else None, words=words, min_font_pt=min(sizes) if sizes else None,
                n_icons=n_icons, issues=issues)


def format_report(report: Dict[str, Any]) -> str:
    lines = [f"QA: {report['status'].upper()}  | {report['journal']} | {report['size_mm'][0]} x {report['size_mm'][1]} mm"
             f" | words {report['words']} | min font {report['min_font_pt']} pt | icons {report['n_icons']}"
             + (f" | png {report['png_px'][0]}x{report['png_px'][1]} px" if report.get("png_px") else "")]
    for i in report["issues"]:
        lines.append(f"  [{i['level']}] {i['code']}: {i['message']}")
    return "\n".join(lines)
