"""Stage 5 — GO / KEGG functional enrichment of the PAEs∩EM∩FRGs genes.

Python ORA (hypergeometric + BH); ``R/enrich.R`` provides the
clusterProfiler hook with live org.Hs.eg.db / KEGG annotation.
Demo mode uses the bundled synthetic annotation sets; a real python-side
run expects ``annotation_gene_sets.json`` in ``data/raw`` mapping
``"DB::term" -> [genes]`` (e.g. exported from MSigDB GMTs).
"""

from __future__ import annotations

import pandas as pd

from ..config import RunContext
from ..utils.io import load_json, save_json, save_table
from ..utils.stats import hypergeom_ora


def run(ctx: RunContext) -> dict:
    cfg = ctx.cfg["enrichment"]
    inter = load_json(ctx.processed / "intersection_genes.json")
    acc = ctx.cfg["datasets"]["training"][0]["accession"]
    universe = set(
        pd.read_csv(ctx.processed / f"{acc}_expr.csv", index_col=0).index)
    gene_sets = {k: set(v) for k, v in
                 load_json(ctx.raw / "annotation_gene_sets.json").items()}

    res = hypergeom_ora(set(inter), universe, gene_sets,
                        p_threshold=cfg["pvalue_threshold"])
    save_table(res, ctx.results / "s05_enrichment.csv", index=False)

    by_db: dict[str, int] = {}
    for term in res.get("term", pd.Series(dtype=str)):
        db = term.split("::")[0]
        by_db[db] = by_db.get(db, 0) + 1
    out = {
        "n_query_genes": len(inter),
        "n_significant_terms": int(res.shape[0]),
        "terms_by_database": by_db,
        "top_terms": res.head(8)["term"].tolist() if not res.empty else [],
    }
    save_json(out, ctx.results / "s05_enrich.json")
    return out
