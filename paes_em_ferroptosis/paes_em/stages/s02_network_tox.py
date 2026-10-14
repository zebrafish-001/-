"""Stage 2 — network toxicology target collection and intersection.

Demo mode reads bundled synthetic target lists. Real mode expects three
JSON lists of HGNC symbols (UniProt-normalized) in ``data/raw``:

* ``paes_targets.json`` — union of compound targets from ChEMBL / CTD /
  PharmMapper / SwissTargetPrediction for the 7 configured PAEs
  (PubChem CIDs in config give the structures to query with).
* ``em_targets.json``   — disease targets from GeneCards / TTD / DrugBank /
  OMIM for "endometriosis".
* ``frgs_ferrdb.json``  — FerrDb ferroptosis genes (driver+suppressor+marker,
  deduplicated; 471 in the paper).

The stage computes the three-way intersection that seeds all later stages.
"""

from __future__ import annotations

from ..config import RunContext
from ..utils.io import load_json, save_json


def run(ctx: RunContext) -> dict:
    paes = set(load_json(ctx.raw / "paes_targets.json"))
    em = set(load_json(ctx.raw / "em_targets.json"))
    frgs = set(load_json(ctx.raw / "frgs_ferrdb.json"))

    inter = sorted(paes & em & frgs)
    pairwise = {
        "paes_em": len(paes & em),
        "paes_frgs": len(paes & frgs),
        "em_frgs": len(em & frgs),
    }
    out = {
        "n_paes_targets": len(paes),
        "n_em_targets": len(em),
        "n_frgs": len(frgs),
        "pairwise_overlap": pairwise,
        "intersection_size": len(inter),
        "intersection_genes": inter,
    }
    save_json(out, ctx.results / "s02_network_tox.json")
    save_json(inter, ctx.processed / "intersection_genes.json")
    return out
