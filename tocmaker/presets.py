"""Journal / publisher presets for TOC graphic canvases.

All sizes are stored in millimetres; the renderers work in points (1 pt = 1/72 in).
If ``tocmaker/db/journal_specs.yaml`` exists, its entries are merged in (file wins
for size fields that are not null) so the research database and the code stay in sync.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

MM_PER_IN = 25.4
PT_PER_IN = 72.0


def mm_to_pt(mm: float) -> float:
    return mm / MM_PER_IN * PT_PER_IN


def pt_to_mm(pt: float) -> float:
    return pt / PT_PER_IN * MM_PER_IN


@dataclass
class Preset:
    key: str
    journal: str
    publisher: str
    width_mm: float
    height_mm: float
    min_dpi: int = 300
    min_font_pt: float = 6.0
    pref_font_pt: float = 8.0
    max_words: int = 25            # soft limit on words in the graphic
    fonts: List[str] = field(default_factory=lambda: ["Arial", "Helvetica", "Liberation Sans", "sans-serif"])
    reveal_results: bool = True    # ACS TOC: traditionally do NOT reveal results; Elsevier: show the key finding
    notes: str = ""

    @property
    def width_pt(self) -> float:
        return mm_to_pt(self.width_mm)

    @property
    def height_pt(self) -> float:
        return mm_to_pt(self.height_mm)

    @property
    def aspect(self) -> float:
        return self.width_mm / self.height_mm

    def px(self, dpi: Optional[int] = None):
        dpi = dpi or self.min_dpi
        return (round(self.width_mm / MM_PER_IN * dpi), round(self.height_mm / MM_PER_IN * dpi))

    def to_dict(self):
        d = asdict(self)
        d["width_pt"], d["height_pt"] = self.width_pt, self.height_pt
        d["px_at_min_dpi"] = list(self.px())
        return d


_IN = MM_PER_IN
PRESETS: Dict[str, Preset] = {
    # ACS: fit within 3.25 x 1.75 in (8.25 x 4.45 cm); sans-serif 8 pt, min 6 pt; TIFF 300 dpi.
    "acs": Preset("acs", "ACS journals (ES&T, ES&T Letters, Environment & Health, Chem Res Toxicol)", "ACS",
                  3.25 * _IN, 1.75 * _IN, 300, 6, 8, 20, reveal_results=False,
                  notes="Original artwork by a coauthor; no photos of people, no logos/trademarks/stamps/currency. "
                        "Classic ACS advice: hint at the finding, do not paste a results plot."),
    # Elsevier: min 1328 x 531 px at 300 dpi (500:200 window). = 112.4 x 44.96 mm
    "elsevier": Preset("elsevier", "Elsevier journals (Environ Int, JHM, STOTEN, EES, Chemosphere, Water Res, Environ Pollut)", "Elsevier",
                       1328 / 300 * _IN, 531 / 300 * _IN, 300, 6, 8, 30,
                       notes="Image only, no caption outside; fonts Times/Arial/Courier/Symbol; TIFF/EPS/PDF/Office preferred."),
    "keai": Preset("keai", "KeAi/Elsevier OA (Eco-Environment & Health, Environ Sci Ecotechnol)", "KeAi",
                   1328 / 300 * _IN, 531 / 300 * _IN, 300, 6, 8, 30),
    # Springer: 7:5 landscape, vector, little or no text (TOC size approx 80 x 57 mm — unconfirmed; use 7:5).
    "springer": Preset("springer", "Springer Nature journals with TOC graphics (ESPR, Arch Toxicol, Expo Health)", "Springer Nature",
                       84.0, 60.0, 300, 6, 8, 15, notes="7:5 ratio, landscape, vector preferred, minimal text."),
    # Wiley TOC image: ~ 80 mm wide x 35 mm high (unconfirmed; 2.3:1), plus a 50-80 word short abstract text.
    "wiley": Preset("wiley", "Wiley journals (Environ Toxicol Chem, Adv Sci)", "Wiley",
                    80.0, 35.0, 300, 6, 8, 20, notes="TOC image + separate 50-80 word TOC text (check journal)."),
    # RSC: 8 cm x 4 cm, plus 20-30 words of TOC text.
    "rsc": Preset("rsc", "RSC journals (ES: Processes & Impacts, ES: Nano, ES: Water Res Technol)", "RSC",
                  80.0, 40.0, 300, 6, 8, 20, notes="TOC entry: 8 x 4 cm graphic + 20-30 word text sentence."),
    # Cell Press: 1200 x 1200 px at 300 dpi (= 4 x 4 in); Arial/Avenir 12-16 pt; single panel; no data items.
    "cell": Preset("cell", "Cell Press (The Innovation, iScience, Cell Rep Sustain, One Earth)", "Cell Press",
                   4 * _IN, 4 * _IN, 300, 7, 10, 40, notes="Square; clear start/end, top-to-bottom; distinct from model figures; avoid red/green pairs."),
    # MDPI: minimum 1100 px wide x 560 px high (PNG/JPEG/TIFF); not identical to a paper figure; no collage.
    "mdpi": Preset("mdpi", "MDPI (Toxics, IJERPH)", "MDPI", 1100 / 300 * _IN, 560 / 300 * _IN, 300, 6, 8, 40,
                   notes="No stamps/currency/trademarks; must not be a sub-figure collage."),
    # ACS Chemical Research in Toxicology uses a larger box: 8.47 x 4.76 cm (3.33 x 1.88 in).
    "crt": Preset("crt", "Chemical Research in Toxicology (ACS, larger TOC box)", "ACS", 84.7, 47.6, 300, 6, 8, 20,
                  reveal_results=False, notes="No tables/spectra, no legend."),
    # Wiley Advanced Science: ToC figure 55 x 50 mm (portrait-ish) or 110 x 20 mm (strip); labels >= 10 pt; 50-60 word ToC text.
    "advsci": Preset("advsci", "Advanced Science / Wiley (55 x 50 mm ToC figure)", "Wiley", 55.0, 50.0, 300, 7, 10, 20,
                     notes="Alternative strip format 110 x 20 mm (preset 'advsci_strip'); ToC text 50-60 words, third person."),
    "advsci_strip": Preset("advsci_strip", "Advanced Science / Wiley (110 x 20 mm strip)", "Wiley", 110.0, 20.0, 300, 7, 10, 12),
    # Generic 16:9 slide-friendly "visual abstract" for talks / social media / Nature-style Fig. 1 schematic.
    "wide": Preset("wide", "Generic 16:9 visual abstract (talks, social media, Nature-style schematic Fig. 1)", "-",
                   160.0, 90.0, 300, 7, 10, 60),
}

ALIASES = {
    "est": "acs", "es&t": "acs", "acs_est": "acs", "environment_health": "acs",
    "environ_int": "elsevier", "ei": "elsevier", "jhm": "elsevier", "stoten": "elsevier", "ees": "elsevier",
    "chemosphere": "elsevier", "water_research": "elsevier", "environ_pollut": "elsevier", "environ_res": "elsevier",
    "eeh": "keai", "ese": "keai",
    "espr": "springer", "etc": "wiley", "espi": "rsc", "innovation": "cell", "iscience": "cell",
    "toxics": "mdpi", "ijerph": "mdpi", "slide": "wide", "nature": "wide", "chem_res_toxicol": "crt", "adv_sci": "advsci",
}


FROM_DB = set()


def _merge_db():
    """Merge sizes from db/journal_specs.yaml (if present) as additional presets keyed by journal slug."""
    path = os.path.join(os.path.dirname(__file__), "db", "journal_specs.yaml")
    if not os.path.exists(path):
        return
    try:
        import yaml  # type: ignore
        with open(path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
    except Exception:
        return
    entries = data.get("journals", data) if isinstance(data, dict) else data
    if isinstance(entries, dict):
        entries = list(entries.values())
    for e in entries or []:
        if not isinstance(e, dict):
            continue
        w, h = e.get("width_mm"), e.get("height_mm")
        if not (w and h):
            wp, hp, dpi = e.get("width_px"), e.get("height_px"), e.get("min_dpi") or 300
            if wp and hp:
                w, h = wp / dpi * _IN, hp / dpi * _IN
        if not (w and h):
            continue
        import re as _re
        slug = _re.sub(r"\(.*?\)", "", str(e.get("journal", ""))).lower()
        slug = _re.sub(r"[^0-9a-z]+", "_", slug).strip("_")
        if not slug or slug in PRESETS:
            continue
        PRESETS[slug] = Preset(
            slug, e.get("journal", slug), e.get("publisher", "?"), float(w), float(h),
            int(e.get("min_dpi") or 300), float(e.get("min_text_pt") or 6), float(e.get("max_text_pt") or 8),
            25, notes="; ".join(e.get("content_rules") or []) + (" " + str(e.get("notes") or "")),
        )
        FROM_DB.add(slug)


_merge_db()


def get_preset(key: str) -> Preset:
    k = (key or "acs").lower().strip()
    k = ALIASES.get(k, k)
    if k not in PRESETS:
        raise KeyError(f"Unknown journal preset '{key}'. Known: {', '.join(sorted(PRESETS))}")
    return PRESETS[k]


def list_presets(include_db: bool = False):
    return [p.to_dict() for p in PRESETS.values() if include_db or p.key not in FROM_DB]


def find_preset(name: str) -> Preset:
    """Fuzzy lookup: exact key/alias first, then substring match on journal names (db entries included)."""
    try:
        return get_preset(name)
    except KeyError:
        pass
    q = name.lower()
    toks = [t for t in __import__("re").split(r"[^0-9a-z&]+", q) if t]
    best, score = None, 0
    for p in PRESETS.values():
        jn = p.journal.lower()
        sc = sum(1 for t in toks if t in jn)
        if sc > score:
            best, score = p, sc
    if best is None or score == 0:
        raise KeyError(f"Unknown journal '{name}'. Run `toc presets --all`.")
    return best
