"""TOC spec: the YAML the user (or the skill) writes, validated into dataclasses.

Minimal example::

    journal: acs
    palette: envtox
    template: flow
    title: Prenatal PFAS exposure and birth weight          # optional
    panels:
      - role: exposure
        label: Prenatal PFAS exposure
        sublabel: maternal serum, 1st trimester
        icons: [pregnant-woman, chemical-flask-hazard]
      - role: mechanism
        label: Placental inflammation
        icons: [placenta-umbilical, inflammation-cell]
      - role: outcome
        label: Lower birth weight
        icons: [fetus]
        badge: "−48 g per ln-unit"
    arrows:
      - {from: 0, to: 1, label: ""}
      - {from: 1, to: 2, style: dashed}
    footer: "n = 1,203 mother–infant pairs"                 # optional
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union

from .palettes import ROLES

TEMPLATES = ("flow", "split", "hub", "two_row", "cohort", "cycle")


@dataclass
class IconRef:
    id: str
    scale: float = 1.0        # relative size among icons in the same panel
    flip: bool = False
    tint: str = "auto"        # auto | none | mono | duo
    opacity: float = 1.0

    @classmethod
    def parse(cls, v: Union[str, Dict[str, Any]]) -> "IconRef":
        if isinstance(v, str):
            if ":" in v and not v.lower().endswith(".svg") and "/" not in v.split(":")[-1]:
                base, _, sc = v.rpartition(":")
                try:
                    return cls(base, float(sc))
                except ValueError:
                    return cls(v)
            return cls(v)
        return cls(str(v["id"]), float(v.get("scale", 1.0)), bool(v.get("flip", False)),
                   str(v.get("tint", "auto")), float(v.get("opacity", 1.0)))


@dataclass
class Panel:
    label: str = ""
    role: str = "neutral"
    sublabel: str = ""
    icons: List[IconRef] = field(default_factory=list)
    badge: str = ""
    box: bool = True              # draw the tinted rounded background
    weight: float = 1.0           # relative width in flow layouts
    icon_layout: str = "row"      # row | overlap | stack
    items: List[str] = field(default_factory=list)   # bullet-like short items (outcome lists)

    @classmethod
    def parse(cls, d: Dict[str, Any]) -> "Panel":
        role = str(d.get("role", "neutral")).lower()
        if role not in ROLES:
            raise ValueError(f"panel role '{role}' must be one of {ROLES}")
        return cls(
            label=str(d.get("label", "") or ""),
            role=role,
            sublabel=str(d.get("sublabel", "") or ""),
            icons=[IconRef.parse(i) for i in (d.get("icons") or [])],
            badge=str(d.get("badge", "") or ""),
            box=bool(d.get("box", True)),
            weight=float(d.get("weight", 1.0)),
            icon_layout=str(d.get("icon_layout", "row")),
            items=[str(x) for x in (d.get("items") or [])],
        )


@dataclass
class Arrow:
    src: int
    dst: int
    label: str = ""
    style: str = "solid"      # solid | dashed | inhibit | none
    color: str = ""           # role name or hex; default palette line colour

    @classmethod
    def parse(cls, d: Union[Dict[str, Any], List[Any]]) -> "Arrow":
        if isinstance(d, (list, tuple)):
            return cls(int(d[0]), int(d[1]), *(str(x) for x in d[2:3]))
        return cls(int(d.get("from", 0)), int(d.get("to", 1)), str(d.get("label", "") or ""),
                   str(d.get("style", "solid")), str(d.get("color", "") or ""))


@dataclass
class TocSpec:
    journal: str = "acs"
    palette: str = "envtox"
    template: str = "flow"
    title: str = ""
    footer: str = ""
    panels: List[Panel] = field(default_factory=list)
    arrows: List[Arrow] = field(default_factory=list)
    # template-specific groups (indices into panels)
    left: List[int] = field(default_factory=list)
    center: Optional[int] = None
    right: List[int] = field(default_factory=list)
    rows: List[List[int]] = field(default_factory=list)
    converge: Optional[int] = None
    hub_direction: str = "in"       # hub: arrows in | out | none
    font_pt: Optional[float] = None
    language: str = "en"
    options: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TocSpec":
        template = str(d.get("template", "flow")).lower()
        if template not in TEMPLATES:
            raise ValueError(f"template '{template}' must be one of {TEMPLATES}")
        panels = [Panel.parse(p) for p in (d.get("panels") or [])]
        arrows = [Arrow.parse(a) for a in (d.get("arrows") or [])]
        spec = cls(
            journal=str(d.get("journal", "acs")), palette=str(d.get("palette", "envtox")), template=template,
            title=str(d.get("title", "") or ""), footer=str(d.get("footer", "") or ""), panels=panels, arrows=arrows,
            left=[int(i) for i in (d.get("left") or [])], center=d.get("center"),
            right=[int(i) for i in (d.get("right") or [])],
            rows=[[int(i) for i in r] for r in (d.get("rows") or [])], converge=d.get("converge"),
            hub_direction=str(d.get("hub_direction", "in")), font_pt=d.get("font_pt"),
            language=str(d.get("language", "en")), options=dict(d.get("options") or {}),
        )
        spec.validate()
        return spec

    @classmethod
    def load(cls, path: str) -> "TocSpec":
        import yaml  # type: ignore
        with open(path, "r", encoding="utf-8") as fh:
            return cls.from_dict(yaml.safe_load(fh) or {})

    def validate(self):
        n = len(self.panels)
        if n == 0:
            raise ValueError("spec needs at least one panel")
        for a in self.arrows:
            if not (0 <= a.src < n and 0 <= a.dst < n):
                raise ValueError(f"arrow {a.src}->{a.dst} out of range (panels: {n})")
        if self.template == "split":
            if self.center is None or not self.left:
                # default: first = left..., middle = center, rest = right
                if n < 2:
                    raise ValueError("split template needs >= 2 panels")
                if self.center is None:
                    self.center = n // 2 if n >= 3 else 1
                if not self.left:
                    self.left = list(range(0, self.center))
                if not self.right:
                    self.right = [i for i in range(self.center + 1, n)]
        if self.template == "hub" and self.center is None:
            self.center = 0
        if self.template == "two_row" and not self.rows:
            if self.converge is None and n >= 3:
                self.converge = n - 1
            body = [i for i in range(n) if i != self.converge]
            half = (len(body) + 1) // 2
            self.rows = [body[:half], body[half:]]
