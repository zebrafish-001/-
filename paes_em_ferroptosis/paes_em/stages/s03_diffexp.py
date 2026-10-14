"""Stage 3 — differential expression on the training set (GSE51981).

Python reimplementation of limma's moderated t-test (eBayes shrinkage);
``R/limma_de.R`` provides the exact-limma hook for publication runs.
"""

from __future__ import annotations

import pandas as pd

from ..config import RunContext
from ..utils.io import save_json, save_table
from ..utils.stats import moderated_t
from .s01_intake import load_dataset


def run(ctx: RunContext) -> dict:
    de_cfg = ctx.cfg["diffexp"]
    acc = ctx.cfg["datasets"]["training"][0]["accession"]
    expr = pd.read_csv(ctx.processed / f"{acc}_expr.csv", index_col=0)
    groups = pd.read_csv(ctx.processed / f"{acc}_groups.csv",
                         index_col=0)["group"]

    table = moderated_t(expr, groups, case_label="EM")
    lfc, pth = de_cfg["logfc_threshold"], de_cfg["pvalue_threshold"]
    sig = table[(table["adj.P.Val"] < pth) & (table["logFC"].abs() > lfc)]
    save_table(table, ctx.results / "s03_de_full.csv")
    save_table(sig, ctx.results / "s03_degs.csv")
    save_json(sorted(sig.index), ctx.processed / "degs.json")

    out = {
        "dataset": acc,
        "n_tested": int(table.shape[0]),
        "n_degs": int(sig.shape[0]),
        "n_up": int((sig["logFC"] > 0).sum()),
        "n_down": int((sig["logFC"] < 0).sum()),
        "thresholds": {"abs_logFC": lfc, "adj_p": pth},
        "top10": sig.head(10).index.tolist(),
    }
    save_json(out, ctx.results / "s03_diffexp.json")
    return out
