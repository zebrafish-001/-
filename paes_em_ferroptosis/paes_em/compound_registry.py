"""Extensible plasticizer registry.

The bundled catalog (``config/plasticizers_catalog.csv``) seeds ~45
plasticizers across 14 chemical classes (phthalates, terephthalates,
DINCH-type cyclohexanoates, adipates, sebacates, citrates, trimellitates,
benzoates, phosphates, epoxidized oils, ...). The registry scales to
hundreds of compounds: append rows to the CSV (or point ``--catalog`` at
your own), and CIDs are resolved live against PubChem PUG REST by name,
with an on-disk cache so each name is fetched once. CAS numbers in the
catalog are convenience references — the PubChem name resolution is the
source of truth for structure identity; verify both for publication use.

Typical use::

    paes-em compounds                      # list catalog
    paes-em compounds --resolve            # resolve all CIDs via PubChem
    paes-em compounds --resolve --class phthalate,citrate

``resolved_compounds()`` then feeds stage 2 (network toxicology) and the
docking protocol generator with ``{name, abbrev, class, cid}`` records in
place of the 7-compound default list in ``pipeline.yaml``.
"""

from __future__ import annotations

import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

from .config import PKG_ROOT, RunContext

CATALOG = PKG_ROOT / "config" / "plasticizers_catalog.csv"
PUG = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}/cids/JSON"


def load_catalog(path: Path | None = None) -> list[dict]:
    with open(path or CATALOG, newline="", encoding="utf-8") as fh:
        return [row for row in csv.DictReader(fh) if row.get("name")]


def resolve_cid(name: str, timeout: float = 20.0) -> int | None:
    """Resolve one compound name to its best PubChem CID (None if absent)."""
    url = PUG.format(urllib.parse.quote(name))
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            data = json.load(resp)
        cids = data.get("IdentifierList", {}).get("CID", [])
        return int(cids[0]) if cids else None
    except Exception:
        return None


def resolved_compounds(
    ctx: RunContext,
    classes: list[str] | None = None,
    catalog_path: Path | None = None,
    delay: float = 0.25,
) -> list[dict]:
    """Catalog rows with CIDs, resolving and caching what is missing.

    The cache lives in ``data/processed/compound_cids.json`` so repeated
    runs (and offline runs after a first resolve) do not re-query PubChem.
    """
    rows = load_catalog(catalog_path)
    if classes:
        want = {c.strip().lower() for c in classes}
        rows = [r for r in rows if r["class"].lower() in want]

    cache_path = ctx.processed / "compound_cids.json"
    cache: dict[str, int | None] = (
        json.loads(cache_path.read_text()) if cache_path.exists() else {})

    out = []
    dirty = False
    for r in rows:
        name = r["name"]
        if name not in cache:
            cache[name] = resolve_cid(name)
            dirty = True
            time.sleep(delay)              # PubChem rate courtesy
        out.append({"abbrev": r["abbrev"], "name": name,
                    "class": r["class"], "cas": r.get("cas") or None,
                    "cid": cache[name]})
    if dirty:
        cache_path.write_text(json.dumps(cache, indent=2))
    return out


def cli(args, make_context) -> int:
    ctx = make_context(args.config, args.root)
    classes = args.cls.split(",") if args.cls else None
    if args.resolve:
        rows = resolved_compounds(ctx, classes)
        n_ok = sum(1 for r in rows if r["cid"])
        for r in rows:
            print(f"{r['abbrev']:7s} {r['class']:15s} "
                  f"CID={r['cid'] if r['cid'] else '-':<9} {r['name']}")
        print(f"\nresolved {n_ok}/{len(rows)} "
              f"(cache: {ctx.processed / 'compound_cids.json'})")
    else:
        rows = load_catalog()
        if classes:
            want = {c.lower() for c in classes}
            rows = [r for r in rows if r["class"].lower() in want]
        by_class: dict[str, int] = {}
        for r in rows:
            by_class[r["class"]] = by_class.get(r["class"], 0) + 1
        for r in rows:
            print(f"{r['abbrev']:7s} {r['class']:15s} {r['name']}")
        print(f"\n{len(rows)} compounds in {len(by_class)} classes; "
              "use --resolve for PubChem CIDs")
    return 0
