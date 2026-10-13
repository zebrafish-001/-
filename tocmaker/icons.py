"""Icon library: index, search and SVG normalisation.

Sources (searched in this order; all are vector SVG):
  * ``assets/icons/envtox``   — original icons drawn for this repo (CC0), two-token recolourable.
  * ``assets/icons/curated``  — vendored subset of Health Icons (MIT) and Bioicons (CC0 only), see ATTRIBUTION.md.
  * external directories listed in ``TOCMAKER_ICON_PATHS`` (os.pathsep separated), e.g. a full
    Bioicons or Health Icons checkout fetched with ``scripts/fetch_icon_sets.sh``.

Every icon is normalised to a nested ``<svg>`` element with a viewBox, so it scales cleanly
inside the TOC canvas; ids are prefixed per placement to avoid ``url(#id)`` collisions.
"""
from __future__ import annotations

import functools
import json
import os
import re
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple

from lxml import etree

SVG_NS = "http://www.w3.org/2000/svg"
ASSETS = os.path.join(os.path.dirname(__file__), "assets", "icons")
ENVTOX_PRIMARY = "#1F2937"
ENVTOX_ACCENT = "#4F8FC0"
_HEX = re.compile(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")


@dataclass
class IconInfo:
    id: str                     # e.g. "envtox/zebrafish-adult" or "bioicons/Animals/Mouse"
    path: str
    source: str
    license: str
    keywords: List[str] = field(default_factory=list)
    author: str = ""
    recolorable: bool = False   # two-token envtox convention
    monochrome: bool = False    # single-ink icon (Health Icons) — safe to tint

    def score(self, query_tokens: List[str]) -> float:
        name = self.id.lower()
        kw = " ".join(self.keywords).lower()
        s = 0.0
        base = os.path.basename(name)
        for t in query_tokens:
            if not t:
                continue
            if t == base or t == base.replace("-", " ").replace("_", " "):
                s += 10
            elif len(t) < 3 and not any("\u4e00" <= ch <= "\u9fff" for ch in t):
                continue   # 1-2 letter fragments match everything; ignore them
            elif t in base:
                s += 4
            elif t in kw:
                s += 2
            elif t in name:
                s += 1
        if s and self.source == "envtox":
            s += 1.5   # prefer the house style when it exists
        if s and self.license.lower() in ("cc0", "cc-0", "mit", "public domain"):
            s += 0.5
        return s


def _tokens(s: str) -> List[str]:
    s = s.lower().replace("_", " ").replace("-", " ").replace(".svg", "")
    return [t for t in re.split(r"[^0-9a-z\u4e00-\u9fff]+", s) if t]


def _keywords_from_file(path: str) -> List[str]:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            head = fh.read(2000)
        m = re.search(r"<!--\s*keywords:\s*(.*?)-->", head, re.S | re.I)
        if m:
            return [k.strip() for k in re.split(r"[,;，；]", m.group(1)) if k.strip()]
    except OSError:
        pass
    return []


def _scan_dir(root: str, source: str, default_license: str, recolorable: bool, monochrome: bool,
              attribution: Optional[Dict[str, Dict]] = None) -> List[IconInfo]:
    out: List[IconInfo] = []
    if not os.path.isdir(root):
        return out
    for dirpath, _dirs, files in os.walk(root):
        for fn in files:
            if not fn.lower().endswith(".svg") or fn.startswith("_"):
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            ident = f"{source}/{rel[:-4]}"
            lic, author = default_license, ""
            parts = rel.split("/")
            if source == "bioicons" and len(parts) >= 4:      # license/category/author/name.svg
                lic, author = parts[0], parts[2]
            kws = _tokens(rel) + _keywords_from_file(path)
            if attribution and rel in attribution:
                a = attribution[rel]
                lic, author = a.get("license", lic), a.get("author", author)
                kws += a.get("keywords", [])
            out.append(IconInfo(ident, path, source, lic, sorted(set(kws)), author, recolorable, monochrome))
    return out


@functools.lru_cache(maxsize=1)
def build_index() -> List[IconInfo]:
    icons: List[IconInfo] = []
    icons += _scan_dir(os.path.join(ASSETS, "envtox"), "envtox", "CC0", True, False)
    cur = os.path.join(ASSETS, "curated")
    attr_path = os.path.join(cur, "attribution.json")
    attribution = {}
    if os.path.exists(attr_path):
        with open(attr_path, "r", encoding="utf-8") as fh:
            attribution = json.load(fh)
    icons += _scan_dir(os.path.join(cur, "healthicons"), "healthicons", "MIT", False, True, attribution.get("healthicons"))
    icons += _scan_dir(os.path.join(cur, "bioicons"), "bioicons", "CC0", False, False, attribution.get("bioicons"))
    icons += _scan_dir(os.path.join(cur, "reactome"), "reactome", "CC-BY-4.0", False, False, attribution.get("reactome"))
    for ext in (os.environ.get("TOCMAKER_ICON_PATHS") or "").split(os.pathsep):
        ext = ext.strip()
        if not ext:
            continue
        base = os.path.basename(ext.rstrip("/\\")).lower()
        if "healthicons" in ext.lower():
            icons += _scan_dir(ext, "healthicons", "MIT", False, True)
        elif "reactome" in ext.lower():
            icons += _scan_dir(ext, "reactome", "CC-BY-4.0", False, False, _reactome_attribution(ext))
        elif "bioicons" in ext.lower():
            icons += _scan_dir(ext, "bioicons", "varies", False, False)
        else:
            icons += _scan_dir(ext, base or "ext", "unknown", False, False)
    return icons


def search(query: str, limit: int = 10, sources: Optional[Iterable[str]] = None,
           licenses: Optional[Iterable[str]] = None) -> List[IconInfo]:
    toks = _tokens(query)
    srcs = set(s.lower() for s in sources) if sources else None
    lics = set(l.lower() for l in licenses) if licenses else None
    scored: List[Tuple[float, IconInfo]] = []
    for ic in build_index():
        if srcs and ic.source.lower() not in srcs:
            continue
        if lics and ic.license.lower() not in lics:
            continue
        s = ic.score(toks)
        if s > 0:
            scored.append((s, ic))
    scored.sort(key=lambda x: (-x[0], x[1].id))
    return [ic for _s, ic in scored[:limit]]


def get(icon_id: str) -> IconInfo:
    """Exact id, or path to an SVG file, or a search query (best hit)."""
    if os.path.isfile(icon_id) and icon_id.lower().endswith(".svg"):
        return IconInfo(os.path.splitext(os.path.basename(icon_id))[0], icon_id, "file", "unknown")
    idx = {ic.id.lower(): ic for ic in build_index()}
    if icon_id.lower() in idx:
        return idx[icon_id.lower()]
    # allow "envtox/foo" without source prefix, or "foo.svg"
    short = icon_id.lower().replace(".svg", "")
    for ic in build_index():
        if ic.id.lower().endswith("/" + short):
            return ic
    hits = search(icon_id, limit=1)
    if not hits or hits[0].score(_tokens(icon_id)) < 4:   # require a file-name match, not a stray keyword
        raise KeyError(f"No icon matches '{icon_id}'. Try `toc icons search <keyword>`.")
    return hits[0]


# ---------------------------------------------------------------------------------------- SVG handling

_STRIP_TAGS = {"title", "desc", "metadata", "script"}


def _parse(path: str) -> etree._Element:
    parser = etree.XMLParser(remove_comments=True, remove_pis=True, huge_tree=True, recover=True)
    tree = etree.parse(path, parser)
    root = tree.getroot()
    if etree.QName(root).localname != "svg":
        raise ValueError(f"{path} is not an SVG")
    return root


def _viewbox(root: etree._Element) -> Tuple[float, float, float, float]:
    vb = root.get("viewBox")
    if vb:
        nums = [float(x) for x in re.split(r"[\s,]+", vb.strip()) if x]
        if len(nums) == 4 and nums[2] > 0 and nums[3] > 0:
            return tuple(nums)  # type: ignore
    w, h = root.get("width"), root.get("height")

    def num(v):
        m = re.match(r"\s*([0-9.]+)", v or "")
        return float(m.group(1)) if m else None
    wn, hn = num(w), num(h)
    if wn and hn:
        return (0.0, 0.0, wn, hn)
    return (0.0, 0.0, 100.0, 100.0)


_counter = [0]


@functools.lru_cache(maxsize=4096)
def aspect(path: str) -> float:
    """width / height of the icon's viewBox (1.0 for square)."""
    try:
        _x, _y, w, h = _viewbox(_parse(path))
        return max(0.2, min(5.0, w / h)) if h else 1.0
    except Exception:
        return 1.0


def placed_svg(info: IconInfo, x: float, y: float, w: float, h: float, primary: Optional[str] = None,
               accent: Optional[str] = None, tint_mode: str = "auto", opacity: float = 1.0,
               flip: bool = False) -> str:
    """Return a nested <svg> string placing the icon in the box (x, y, w, h) in canvas units.

    tint_mode: "auto" (recolour envtox tokens; tint monochrome icons to primary; leave others),
               "none" (keep original colours), "mono" (force every non-white colour to primary),
               "duo" (dark colours -> primary, light/saturated -> accent).
    """
    root = _parse(info.path)
    vx, vy, vw, vh = _viewbox(root)
    for el in list(root):
        if etree.QName(el).localname in _STRIP_TAGS:
            root.remove(el)
    for attr in ("width", "height", "x", "y", "id", "class", "style"):
        if attr in root.attrib:
            del root.attrib[attr]
    root.set("viewBox", f"{vx} {vy} {vw} {vh}")
    root.set("preserveAspectRatio", "xMidYMid meet")
    root.set("x", f"{x:.3f}")
    root.set("y", f"{y:.3f}")
    root.set("width", f"{w:.3f}")
    root.set("height", f"{h:.3f}")
    if opacity < 1:
        root.set("opacity", f"{opacity:.3f}")
    if flip:
        # mirror horizontally inside the icon's own coordinate system
        g = etree.SubElement(root, f"{{{SVG_NS}}}g")
        g.set("transform", f"translate({vx + vw + vx},0) scale(-1,1)")
        for el in list(root):
            if el is not g:
                root.remove(el)
                g.append(el)
    s = etree.tostring(root, encoding="unicode")
    s = _recolour(s, info, primary, accent, tint_mode)
    _counter[0] += 1
    s = _prefix_ids(s, f"ic{_counter[0]}_")
    return s


def _recolour(s: str, info: IconInfo, primary: Optional[str], accent: Optional[str], mode: str) -> str:
    primary = primary or ENVTOX_PRIMARY
    accent = accent or ENVTOX_ACCENT
    if mode == "none":
        return s
    if info.recolorable and mode in ("auto", "duo", "mono"):
        s = re.sub(ENVTOX_PRIMARY, primary, s, flags=re.I)
        s = re.sub(ENVTOX_ACCENT, primary if mode == "mono" else accent, s, flags=re.I)
        return s
    if mode == "auto" and not info.monochrome:
        return s
    from .palettes import luminance

    def repl(m):
        c = m.group(0)
        h = c.lstrip("#")
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        if h.upper() in ("FFFFFF",):
            return c
        if mode == "duo":
            return primary if luminance("#" + h) < 0.35 else accent
        return primary
    return _HEX.sub(repl, s)


def _prefix_ids(s: str, prefix: str) -> str:
    ids = set(re.findall(r'\bid="([^"]+)"', s))
    if not ids:
        return s
    for i in ids:
        s = s.replace(f'id="{i}"', f'id="{prefix}{i}"')
        s = s.replace(f"url(#{i})", f"url(#{prefix}{i})")
        s = s.replace(f'href="#{i}"', f'href="#{prefix}{i}"')
    return s


def icon_png(info: IconInfo, width_px: int, primary: Optional[str] = None, accent: Optional[str] = None,
             tint_mode: str = "auto", flip: bool = False) -> bytes:
    """Rasterise an icon (for PPTX fallback thumbnails and previews)."""
    import cairosvg
    a = aspect(info.path)
    h = 100.0 / a
    inner = placed_svg(info, 0, 0, 100, h, primary, accent, tint_mode, flip=flip)
    svg = f'<svg xmlns="{SVG_NS}" viewBox="0 0 100 {h:.3f}" width="100" height="{h:.3f}">{inner}</svg>'
    return cairosvg.svg2png(bytestring=svg.encode("utf-8"), output_width=width_px, output_height=max(1, round(width_px / a)))


def icon_svg_bytes(info: IconInfo, primary: Optional[str] = None, accent: Optional[str] = None,
                   tint_mode: str = "auto", flip: bool = False) -> bytes:
    """Standalone SVG document for one icon (used for PPTX svgBlip embedding)."""
    h = 100.0 / aspect(info.path)
    inner = placed_svg(info, 0, 0, 100, h, primary, accent, tint_mode, flip=flip)
    svg = (f'<svg xmlns="{SVG_NS}" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 100 {h:.3f}" '
           f'width="100" height="{h:.3f}">{inner}</svg>')
    return svg.encode("utf-8")


def _reactome_attribution(root: str) -> Dict[str, Dict]:
    """Build keyword metadata for a full reactome_illustrations checkout (icons/R-ICO-xxxx.xml next to the SVGs)."""
    out: Dict[str, Dict] = {}
    for dirpath, _d, files in os.walk(root):
        for fn in files:
            if not fn.endswith(".xml"):
                continue
            try:
                r = etree.parse(os.path.join(dirpath, fn)).getroot()
            except Exception:
                continue
            name = (r.findtext("name") or "").strip()
            cats = [c.text.strip().replace("_", " ") for c in r.iter("category") if c.text]
            syn = [x.text.strip() for x in r.iter("synonym") if x.text]
            rel = os.path.relpath(os.path.join(dirpath, fn[:-4] + ".svg"), root).replace(os.sep, "/")
            out[rel] = dict(license="CC-BY-4.0", author="Reactome", keywords=[name] + syn + cats)
    return out
