"""Raster -> vector: trace a finished TOC image (from any drawing tool) into SVG and into native,
editable PowerPoint shapes.

Pipeline
  1. vtracer (colour quantisation + curve fitting) -> SVG of filled paths, one path per colour region.
  2. svgelements flattens every path to a polygon (tolerance in px) so it can become a PPTX freeform.
  3. python-pptx FreeformBuilder draws each region as a native shape (fill = traced colour, no line);
     regions are ordered back-to-front as vtracer emitted them, grouped per colour layer.
  4. Optional second slide carries the SVG itself (svgBlip) so PowerPoint can also *Convert to Shape*.

Flat artwork (solid fills, hard edges, no gradients/photo textures) traces cleanly; painterly or
gradient-heavy AI renders produce thousands of blobs and are better left as a picture.
"""
from __future__ import annotations

import io
import os
import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

from .presets import MM_PER_IN, Preset


@dataclass
class TraceOptions:
    colormode: str = "color"       # color | binary
    hierarchical: str = "cutout"   # cutout (regions do not overlap: best for editing) | stacked
    mode: str = "spline"           # spline | polygon | none
    filter_speckle: int = 6        # px; drop regions smaller than this
    color_precision: int = 6       # bits per channel kept (fewer = fewer colours)
    layer_difference: int = 24     # colour distance between layers
    corner_threshold: int = 60
    length_threshold: float = 4.0
    max_iterations: int = 10
    splice_threshold: int = 45
    path_precision: int = 3
    max_shapes: int = 1500         # safety cap for the PPTX
    flatten_tol: float = 0.6       # px tolerance when flattening curves to polygons
    drop_background: bool = True   # drop a near-white region covering the whole canvas


def trace_svg(image_path: str, svg_out: str, opt: TraceOptions = TraceOptions()) -> str:
    import vtracer
    vtracer.convert_image_to_svg_py(
        image_path, svg_out, colormode=opt.colormode, hierarchical=opt.hierarchical, mode=opt.mode,
        filter_speckle=opt.filter_speckle, color_precision=opt.color_precision,
        layer_difference=opt.layer_difference, corner_threshold=opt.corner_threshold,
        length_threshold=opt.length_threshold, max_iterations=opt.max_iterations,
        splice_threshold=opt.splice_threshold, path_precision=opt.path_precision,
    )
    return svg_out


@dataclass
class Region:
    color: str                      # #RRGGBB
    opacity: float
    polys: List[List[Tuple[float, float]]]   # one or more closed rings (holes included as separate rings)
    bbox: Tuple[float, float, float, float]


def _flatten(path, tol: float) -> List[List[Tuple[float, float]]]:
    """Flatten an svgelements Path into closed polygons, one per subpath."""
    from svgelements import Close, Line, Move
    rings: List[List[Tuple[float, float]]] = []
    cur: List[Tuple[float, float]] = []
    for seg in path:
        if isinstance(seg, Move):
            if len(cur) >= 3:
                rings.append(cur)
            cur = [(seg.end.x, seg.end.y)]
        elif isinstance(seg, (Line, Close)):
            if seg.end is not None:
                cur.append((seg.end.x, seg.end.y))
        else:  # curves: sample by length
            try:
                L = seg.length(error=1e-3)
            except Exception:
                L = 10.0
            n = max(2, min(64, int(L / max(tol, 0.1) ** 0.5)))
            for k in range(1, n + 1):
                p = seg.point(k / n)
                cur.append((p.x, p.y))
    if len(cur) >= 3:
        rings.append(cur)
    # drop consecutive duplicates
    out = []
    for r in rings:
        rr = [r[0]]
        for p in r[1:]:
            if abs(p[0] - rr[-1][0]) > 1e-6 or abs(p[1] - rr[-1][1]) > 1e-6:
                rr.append(p)
        if len(rr) >= 3:
            out.append(rr)
    return out


def svg_regions(svg_path: str, opt: TraceOptions = TraceOptions()) -> Tuple[List[Region], float, float]:
    from svgelements import SVG, Path, Color
    svg = SVG.parse(svg_path, reify=True)
    W, H = float(svg.width or svg.viewbox.width), float(svg.height or svg.viewbox.height)
    regions: List[Region] = []
    for el in svg.elements():
        if not isinstance(el, Path):
            continue
        fill = el.fill
        if fill is None or fill.value is None:
            continue
        col = Color(fill)
        hexc = f"#{col.red:02X}{col.green:02X}{col.blue:02X}"
        opacity = float(col.alpha) / 255.0 if col.alpha is not None else 1.0
        rings = _flatten(el, opt.flatten_tol)
        if not rings:
            continue
        xs = [p[0] for r in rings for p in r]
        ys = [p[1] for r in rings for p in r]
        bbox = (min(xs), min(ys), max(xs), max(ys))
        regions.append(Region(hexc, opacity, rings, bbox))
    if opt.drop_background and regions:
        r0 = regions[0]
        full = (r0.bbox[2] - r0.bbox[0]) >= 0.98 * W and (r0.bbox[3] - r0.bbox[1]) >= 0.98 * H
        if full and _is_light(r0.color):
            regions = regions[1:]
    return regions, W, H


def _is_light(hexc: str) -> bool:
    h = hexc.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) > 235


def regions_to_pptx(regions: List[Region], W: float, H: float, out_path: str, width_mm: Optional[float] = None,
                    svg_path: Optional[str] = None, png_path: Optional[str] = None, max_shapes: int = 1500,
                    group_by_color: bool = True, boxes: Optional[List["TextBox"]] = None) -> dict:
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.util import Emu
    width_mm = width_mm or (W / 300.0 * MM_PER_IN)
    scale = width_mm / MM_PER_IN * 914400 / W       # EMU per px
    prs = Presentation()
    prs.slide_width = Emu(int(W * scale))
    prs.slide_height = Emu(int(H * scale))
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    n = 0
    skipped = 0
    by_color: dict = {}
    for reg in regions:
        if n >= max_shapes:
            skipped += 1
            continue
        # one freeform per region; every ring is a sub-path so holes (even-odd) survive, as in PowerPoint's own
        # "Merge Shapes > Subtract" output
        first = reg.polys[0]
        fb = slide.shapes.build_freeform(Emu(int(first[0][0] * scale)), Emu(int(first[0][1] * scale)), scale=1.0)
        fb.add_line_segments([(Emu(int(x * scale)), Emu(int(y * scale))) for x, y in first[1:]], close=True)
        for ring in reg.polys[1:]:
            fb.move_to(Emu(int(ring[0][0] * scale)), Emu(int(ring[0][1] * scale)))
            fb.add_line_segments([(Emu(int(x * scale)), Emu(int(y * scale))) for x, y in ring[1:]], close=True)
        shp = fb.convert_to_shape()
        shp.fill.solid()
        shp.fill.fore_color.rgb = RGBColor.from_string(reg.color.lstrip("#"))
        shp.line.fill.background()
        shp.shadow.inherit = False
        style = shp._element.find("{http://schemas.openxmlformats.org/presentationml/2006/main}style")
        if style is not None:   # theme style refs add outlines/shadows in some renderers
            shp._element.remove(style)
        shp.name = f"region {n} {reg.color}"
        if reg.opacity < 0.999:
            _alpha(shp, reg.opacity)
        by_color.setdefault(reg.color, []).append(shp)
        n += 1
    # one group for the whole artwork keeps the painter's order (grouping per colour would reorder layers)
    all_shapes = [shp for shapes in by_color.values() for shp in shapes]
    if group_by_color and len(all_shapes) > 1:
        try:
            all_shapes.sort(key=lambda sh: sh._element.getparent().index(sh._element))
            grp = slide.shapes.add_group_shape(all_shapes)
            grp.name = "traced artwork (ungroup to edit regions)"
        except Exception:
            pass
    if boxes:
        _text_pptx(slide, boxes, scale, width_mm, W)
    if svg_path and os.path.exists(svg_path):
        _svg_slide(prs, svg_path, png_path)
    prs.save(out_path)
    return dict(shapes=n, skipped=skipped, colors=len(by_color), width_mm=round(width_mm, 2),
                height_mm=round(width_mm * H / W, 2))


def _alpha(shape, opacity: float):
    from lxml import etree
    NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
    solid = shape.fill._xPr.find(f"{{{NS_A}}}solidFill")
    if solid is not None and len(solid):
        a = etree.SubElement(solid[0], f"{{{NS_A}}}alpha")
        a.set("val", str(int(opacity * 100000)))


def _svg_slide(prs, svg_path: str, png_path: Optional[str]):
    """Second slide: the traced SVG as a picture (PowerPoint 2016+ can Convert to Shape)."""
    from lxml import etree
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT
    from pptx.opc.package import Part
    from pptx.opc.packuri import PackURI
    import cairosvg
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    with open(svg_path, "rb") as fh:
        svg_bytes = fh.read()
    png = cairosvg.svg2png(bytestring=svg_bytes, output_width=1600)
    pic = slide.shapes.add_picture(io.BytesIO(png), 0, 0, prs.slide_width, prs.slide_height)
    pic.name = "traced SVG (right-click > Convert to Shape)"
    part = Part(PackURI("/ppt/media/traced.svg"), "image/svg+xml", prs.part.package, svg_bytes)
    rid = slide.part.relate_to(part, RT.IMAGE)
    NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
    NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    blip = pic._element.blipFill.blip
    ext_lst = etree.SubElement(blip, f"{{{NS_A}}}extLst")
    ext = etree.SubElement(ext_lst, f"{{{NS_A}}}ext")
    ext.set("uri", "{96DAC541-7B7A-43D3-8B79-37D633B846F1}")
    sb = etree.SubElement(ext, "{http://schemas.microsoft.com/office/drawing/2016/SVG/main}svgBlip")
    sb.set(f"{{{NS_R}}}embed", rid)


def regions_to_svg(regions: List[Region], W: float, H: float, out_path: str, width_mm: Optional[float] = None,
                   boxes: Optional[List["TextBox"]] = None) -> str:
    """Clean polygon SVG (what the PPTX contains), with physical size for journal upload."""
    width_mm = width_mm or (W / 300.0 * MM_PER_IN)
    height_mm = width_mm * H / W
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width_mm:.3f}mm" height="{height_mm:.3f}mm" viewBox="0 0 {W:.2f} {H:.2f}">']
    for reg in regions:
        d = " ".join("M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in ring) + " Z" for ring in reg.polys)
        op = f' fill-opacity="{reg.opacity:.3f}"' if reg.opacity < 0.999 else ""
        parts.append(f'<path d="{d}" fill="{reg.color}" fill-rule="evenodd"{op}/>')
    if boxes:
        parts.append(_text_svg(boxes, W, H))
    parts.append("</svg>")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts))
    return out_path


# ----------------------------------------------------------------------------- text layer (OCR)
@dataclass
class TextBox:
    x: float
    y: float
    w: float
    h: float
    text: str
    score: float
    color: str = "#1F2937"
    bold: bool = False


def _stroke_ratio(crop, lum) -> float:
    """Median stroke width / box height for the ink pixels (Arial regular ~0.09, bold ~0.15)."""
    try:
        import cv2
        import numpy as np
        ink = (lum < max(120, lum.min() + 60)).astype("uint8")
        if ink.sum() < 20:
            return 0.0
        dist = cv2.distanceTransform(ink, cv2.DIST_L2, 3)
        core = dist[(ink > 0) & (dist >= 1.0)]
        if len(core) == 0:
            return 0.0
        return float(2.0 * np.median(core)) / max(1.0, crop.shape[0])
    except Exception:
        return 0.0


_COMMON = set("""the of and in to a is for with on by at from as or an be this that are was were which were it its into
exposure exposures brain brains fish water behavior behaviour behavioral behavioural anxiety like memory impairment
accumulation environmental occurrence metabolic rerouting pathway pathways serotonin kynurenine tryptophan supplementation
attenuated deficits locomotion social exploratory neurobehavioral neurobehavioural ratio benzoate emamectin genes gene
enters rescues rescue males females male female increased decreased reduced higher lower low high dose doses chronic
larvae larval adult adults zebrafish mouse mice human cohort children prenatal placental birth weight hypertension
microplastics microplastic pfas cadmium lead mercury arsenic pesticide pesticides pollution pollutant pollutants
oxidative stress inflammation dysbiosis gut microbiome liver kidney lung heart thyroid hormone receptor dna rna
to-water hpf dpf hours days weeks months years control treatment treated""".split())


def load_vocab(path: Optional[str]) -> set:
    vocab = set(_COMMON)
    if path and os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            for w in re.findall(r"[A-Za-z][A-Za-z\-]{1,}", fh.read()):
                if len(w) >= 2:
                    vocab.add(w.lower())
    return vocab


def respace(token: str, vocab: set) -> str:
    """Re-insert spaces OCR dropped ('Brainaccumulation' -> 'Brain accumulation') using a dictionary DP.
    Only touches alphabetic runs of >= 9 chars that are not themselves in the vocabulary."""
    def split_run(run: str) -> str:
        if len(run) < 9 or run.lower() in vocab:
            return run
        n = len(run)
        best: List[Optional[Tuple[int, int]]] = [None] * (n + 1)   # (cost, prev) ; cost = number of words + penalty
        best[0] = (0, -1)
        for i in range(1, n + 1):
            for j in range(max(0, i - 24), i):
                if best[j] is None:
                    continue
                piece = run[j:i].lower()
                if piece in vocab and len(piece) >= 2:
                    cand = (best[j][0] + 1, j)
                    if best[i] is None or cand[0] < best[i][0]:
                        best[i] = cand
        if best[n] is None:
            return run
        parts, i = [], n
        while i > 0:
            j = best[i][1]
            parts.append(run[j:i])
            i = j
        return " ".join(reversed(parts))
    return re.sub(r"[A-Za-z]{9,}", lambda m: split_run(m.group(0)), token)


def detect_text(image_path: str, min_score: float = 0.6, vocab: Optional[set] = None) -> List[TextBox]:
    """Offline OCR (RapidOCR, PP-OCR models). Returns axis-aligned boxes in source pixels."""
    try:
        from rapidocr_onnxruntime import RapidOCR
    except ImportError:
        return []
    import numpy as np
    from PIL import Image
    im = Image.open(image_path).convert("RGB")
    arr = np.asarray(im)
    ocr = RapidOCR()
    res, _ = ocr(arr)
    out: List[TextBox] = []
    for box, text, score in (res or []):
        try:
            sc = float(score)
        except (TypeError, ValueError):
            sc = 1.0
        if sc < min_score or not str(text).strip():
            continue
        txt = str(text).strip()
        if vocab:
            txt = respace(txt, vocab)
        if sum(ch.isalnum() for ch in txt) < 2:      # a lone glyph is more often artwork than text
            continue
        xs = [p[0] for p in box]
        ys = [p[1] for p in box]
        x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
        w, h = x1 - x0, y1 - y0
        if h <= 0 or w / h < 1.2:                     # text lines are wide; tall boxes are shapes
            continue
        crop2 = arr[int(y0):int(y1) + 1, int(x0):int(x1) + 1]
        crop = crop2.reshape(-1, 3)
        lum = crop @ np.array([0.2126, 0.7152, 0.0722])
        ink = crop[lum < max(120, lum.min() + 60)] if len(crop) else crop
        col = "#1F2937"
        if len(ink):
            r, g, b = (int(v) for v in np.median(ink, axis=0))
            col = f"#{r:02X}{g:02X}{b:02X}"
        bold = _stroke_ratio(crop2, lum.reshape(crop2.shape[0], crop2.shape[1])) >= 0.125
        out.append(TextBox(x0, y0, w, h, txt, sc, col, bold))
    return out


def mask_text(image_path: str, boxes: List[TextBox], out_path: str, pad: int = 3) -> str:
    """Inpaint the text boxes so the tracer sees only the artwork."""
    import cv2
    import numpy as np
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    for b in boxes:
        x0, y0 = max(0, int(b.x) - pad), max(0, int(b.y) - pad)
        x1, y1 = min(img.shape[1] - 1, int(b.x + b.w) + pad), min(img.shape[0] - 1, int(b.y + b.h) + pad)
        mask[y0:y1 + 1, x0:x1 + 1] = 255
    if mask.any():
        img = cv2.inpaint(img, mask, 5, cv2.INPAINT_TELEA)
    cv2.imwrite(out_path, img)
    return out_path


def _text_svg(boxes: List[TextBox], W: float, H: float) -> str:
    from xml.sax.saxutils import escape
    parts = []
    for b in boxes:
        size = b.h * 0.78
        weight = ' font-weight="bold"' if b.bold else ""
        parts.append(f'<text x="{b.x:.1f}" y="{b.y + b.h * 0.8:.1f}" font-family="Arial, Helvetica, sans-serif" '
                     f'font-size="{size:.1f}"{weight} fill="{b.color}" textLength="{b.w:.1f}" lengthAdjust="spacingAndGlyphs">'
                     f'{escape(b.text)}</text>')
    return "\n".join(parts)


def _text_pptx(slide, boxes: List[TextBox], scale: float, width_mm: float, W: float):
    from pptx.dml.color import RGBColor
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.util import Emu, Pt
    pt_per_px = width_mm / W / MM_PER_IN * 72.0
    for b in boxes:
        tb = slide.shapes.add_textbox(Emu(int(b.x * scale)), Emu(int(b.y * scale)), Emu(int(b.w * scale * 1.15) + 20000),
                                      Emu(int(b.h * scale * 1.3)))
        tf = tb.text_frame
        tf.word_wrap = False
        for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
            setattr(tf, m, Emu(0))
        tf.vertical_anchor = MSO_ANCHOR.TOP
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run()
        r.text = b.text
        r.font.size = Pt(max(4.0, b.h * pt_per_px * 0.78))
        r.font.bold = b.bold
        r.font.name = "Arial"
        r.font.color.rgb = RGBColor.from_string(b.color.lstrip("#"))
        tb.name = "text: " + b.text[:30]


def vectorize(image_path: str, out_dir: str, name: str = "traced", preset: Optional[Preset] = None,
              width_mm: Optional[float] = None, opt: TraceOptions = TraceOptions(), preview: bool = False,
              text_mode: str = "ocr", vocab_path: Optional[str] = None) -> dict:
    """text_mode: 'ocr' = lift text into editable text objects (RapidOCR), 'trace' = keep text as shapes, 'none' = erase text."""
    from PIL import Image
    os.makedirs(out_dir, exist_ok=True)
    if image_path.lower().endswith(".svg"):
        # vector input (e.g. an AI tool that emits SVG with strokes/gradients): rasterise at high resolution
        # and trace — robust to strokes, gradients and text that a direct path import would lose.
        import cairosvg
        raster = os.path.join(out_dir, name + "_src.png")
        cairosvg.svg2png(url=image_path, write_to=raster, output_width=2400, background_color="white")
        image_path = raster
    im = Image.open(image_path)
    src = image_path
    if im.mode not in ("RGB", "RGBA") or not image_path.lower().endswith(".png"):
        src = os.path.join(out_dir, name + "_src.png")
        im.convert("RGB").save(src)
    boxes: List[TextBox] = []
    if text_mode in ("ocr", "none"):
        boxes = detect_text(src, vocab=load_vocab(vocab_path))
        if boxes:
            src = mask_text(src, boxes, os.path.join(out_dir, name + "_notext.png"))
        if text_mode == "none":
            boxes = []
    svg_raw = trace_svg(src, os.path.join(out_dir, name + "_vtracer.svg"), opt)
    regions, W, H = svg_regions(svg_raw, opt)
    if preset is not None:
        width_mm = preset.width_mm
    width_mm = width_mm or (W / 300.0 * MM_PER_IN)
    svg_clean = regions_to_svg(regions, W, H, os.path.join(out_dir, name + ".svg"), width_mm, boxes)
    pptx_path = os.path.join(out_dir, name + ".pptx")
    info = regions_to_pptx(regions, W, H, pptx_path, width_mm, svg_path=svg_raw, max_shapes=opt.max_shapes, boxes=boxes)
    info.update(regions=len(regions), text_boxes=[(b.text, round(b.score, 2)) for b in boxes], svg=svg_clean,
                svg_vtracer=svg_raw, pptx=pptx_path, source_px=[int(W), int(H)])
    if preset is not None:
        ratio = (W / H) / preset.aspect
        info["aspect_note"] = (f"image aspect {W / H:.2f} vs {preset.key} {preset.aspect:.2f} "
                               f"({'ok' if abs(ratio - 1) < 0.05 else 'will need letterboxing/cropping'})")
    if preview:
        from .export import pptx_preview
        pv = pptx_preview(pptx_path, os.path.join(out_dir, name + "_pptx_preview.png"), dpi=200)
        info["preview"] = pv
    return info


# ----------------------------------------------------------------------------- hybrid route (painterly art)
def hybrid(image_path: str, out_dir: str, name: str = "hybrid", preset: Optional[Preset] = None,
           width_mm: Optional[float] = None, line_layer: bool = True, preview: bool = False,
           line_threshold: int = 90, min_score: float = 0.6, vocab_path: Optional[str] = None) -> dict:
    """Keep painterly artwork as a picture layer; lift text (OCR) and dark line-art (chemical structures,
    arrows, boxes) into editable vector objects on top. Output: PPTX (picture + freeform lines + text boxes)
    and SVG (embedded PNG + paths + <text>)."""
    import base64
    import cv2
    import numpy as np
    from PIL import Image
    from pptx import Presentation
    from pptx.util import Emu
    os.makedirs(out_dir, exist_ok=True)
    im = Image.open(image_path).convert("RGB")
    src = os.path.join(out_dir, name + "_src.png")
    im.save(src)
    W, H = im.size
    boxes = detect_text(src, min_score=min_score, vocab=load_vocab(vocab_path))
    bg = mask_text(src, boxes, os.path.join(out_dir, name + "_background.png")) if boxes else src
    regions: List[Region] = []
    if line_layer:
        # dark, saturated-or-black strokes -> binary mask -> trace; the same pixels are softened in the background
        img = cv2.imread(bg)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ink = (gray < line_threshold).astype("uint8") * 255
        ink = cv2.morphologyEx(ink, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
        line_png = os.path.join(out_dir, name + "_lines.png")
        cv2.imwrite(line_png, 255 - ink)
        opt = TraceOptions(colormode="binary", filter_speckle=6, mode="spline", drop_background=True)
        svg_raw = trace_svg(line_png, os.path.join(out_dir, name + "_lines.svg"), opt)
        regions, _w, _h = svg_regions(svg_raw, opt)
        # colour each line region with the median colour of the original pixels under it
        orig = np.asarray(im)
        for r in regions:
            x0, y0, x1, y1 = (int(max(0, v)) for v in r.bbox)
            patch = orig[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3)
            g = cv2.cvtColor(img[y0:y1 + 1, x0:x1 + 1], cv2.COLOR_BGR2GRAY).reshape(-1)
            dark = patch[g < line_threshold] if len(g) else patch
            if len(dark):
                rr, gg, bb = (int(v) for v in np.median(dark, axis=0))
                r.color = f"#{rr:02X}{gg:02X}{bb:02X}"
    width_mm = (preset.width_mm if preset else None) or width_mm or (W / 300.0 * MM_PER_IN)
    height_mm = width_mm * H / W
    # ---- SVG
    with open(bg, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode("ascii")
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width_mm:.3f}mm" '
             f'height="{height_mm:.3f}mm" viewBox="0 0 {W} {H}">',
             f'<image id="artwork" x="0" y="0" width="{W}" height="{H}" xlink:href="data:image/png;base64,{b64}"/>',
             '<g id="line-art">']
    for reg in regions:
        d = " ".join("M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in ring) + " Z" for ring in reg.polys)
        parts.append(f'<path d="{d}" fill="{reg.color}" fill-rule="evenodd"/>')
    parts.append("</g><g id=\"text\">")
    parts.append(_text_svg(boxes, W, H))
    parts.append("</g></svg>")
    svg_path = os.path.join(out_dir, name + ".svg")
    with open(svg_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(parts))
    # ---- PPTX
    scale = width_mm / MM_PER_IN * 914400 / W
    prs = Presentation()
    prs.slide_width = Emu(int(W * scale))
    prs.slide_height = Emu(int(H * scale))
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    pic = slide.shapes.add_picture(bg, 0, 0, prs.slide_width, prs.slide_height)
    pic.name = "artwork (text removed)"
    pptx_path = os.path.join(out_dir, name + ".pptx")
    tmp_prs_path = pptx_path  # regions_to_pptx builds its own presentation; reuse its freeform code inline
    from pptx.dml.color import RGBColor
    n = 0
    shapes = []
    for reg in regions:
        first = reg.polys[0]
        fb = slide.shapes.build_freeform(Emu(int(first[0][0] * scale)), Emu(int(first[0][1] * scale)), scale=1.0)
        fb.add_line_segments([(Emu(int(x * scale)), Emu(int(y * scale))) for x, y in first[1:]], close=True)
        for ring in reg.polys[1:]:
            fb.move_to(Emu(int(ring[0][0] * scale)), Emu(int(ring[0][1] * scale)))
            fb.add_line_segments([(Emu(int(x * scale)), Emu(int(y * scale))) for x, y in ring[1:]], close=True)
        shp = fb.convert_to_shape()
        shp.fill.solid()
        shp.fill.fore_color.rgb = RGBColor.from_string(reg.color.lstrip("#"))
        shp.line.fill.background()
        shp.shadow.inherit = False
        style = shp._element.find("{http://schemas.openxmlformats.org/presentationml/2006/main}style")
        if style is not None:
            shp._element.remove(style)
        shp.name = f"line {n} {reg.color}"
        shapes.append(shp)
        n += 1
    if len(shapes) > 1:
        try:
            grp = slide.shapes.add_group_shape(shapes)
            grp.name = "line art (ungroup to edit)"
        except Exception:
            pass
    _text_pptx(slide, boxes, scale, width_mm, W)
    prs.save(pptx_path)
    info = dict(mode="hybrid", text_boxes=[(b.text, round(b.score, 2)) for b in boxes], line_regions=len(regions),
                svg=svg_path, pptx=pptx_path, background=bg, width_mm=round(width_mm, 2), height_mm=round(height_mm, 2))
    if preview:
        from .export import pptx_preview
        info["preview"] = pptx_preview(pptx_path, os.path.join(out_dir, name + "_pptx_preview.png"), dpi=200)
    return info
