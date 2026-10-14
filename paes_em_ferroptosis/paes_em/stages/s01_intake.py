"""Stage 1 — data intake and QC.

Demo mode reads the bundled synthetic matrices. Real mode expects, for each
configured GEO accession, two files in ``data/raw``:

* ``<ACC>_expr.csv``  — genes x samples, log2-scale expression
* ``<ACC>_pheno.csv`` — columns ``sample, group`` with group in {EM, Control}

(obtainable via GEOquery / GEOparse; see README "真实数据获取").
"""

from __future__ import annotations

import pandas as pd

from ..config import RunContext
from ..utils.io import save_json, save_table


def load_dataset(ctx: RunContext, acc: str):
    expr = pd.read_csv(ctx.raw / f"{acc}_expr.csv", index_col=0)
    pheno = pd.read_csv(ctx.raw / f"{acc}_pheno.csv")
    pheno = pheno.set_index("sample").loc[expr.columns]
    return expr, pheno["group"]


def run(ctx: RunContext) -> dict:
    cfg = ctx.cfg["datasets"]
    accs = [d["accession"] for d in cfg["training"] + cfg["validation"]]
    summary = {"datasets": {}}
    for acc in accs:
        expr, groups = load_dataset(ctx, acc)
        if expr.isna().any().any():
            expr = expr.dropna()
        # heuristically log2-transform raw-intensity matrices
        if expr.to_numpy().max() > 50:
            import numpy as np
            expr = pd.DataFrame(
                np.log2(expr.clip(lower=0).to_numpy() + 1.0),
                index=expr.index, columns=expr.columns,
            )
        save_table(expr, ctx.processed / f"{acc}_expr.csv")
        save_table(groups.to_frame(), ctx.processed / f"{acc}_groups.csv")
        summary["datasets"][acc] = {
            "n_genes": int(expr.shape[0]),
            "n_samples": int(expr.shape[1]),
            "groups": groups.value_counts().to_dict(),
        }
    save_json(summary, ctx.results / "s01_intake.json")
    return summary
