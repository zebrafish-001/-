"""Stage 7 — ssGSEA immune infiltration (28 cell types).

Scores every sample of the training set against the 28 immune-cell
signatures (Charoentong et al.; demo mode ships synthetic signatures as
``immune_signatures_28.json``), compares EM vs control per cell type with
a Wilcoxon rank-sum test, and correlates the key gene's expression with
each cell type's score (Spearman).
"""

from __future__ import annotations

import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr

from ..config import RunContext
from ..utils.io import load_json, save_json, save_table
from ..utils.stats import bh_adjust, ssgsea_scores


def run(ctx: RunContext) -> dict:
    acc = ctx.cfg["datasets"]["training"][0]["accession"]
    expr = pd.read_csv(ctx.processed / f"{acc}_expr.csv", index_col=0)
    groups = pd.read_csv(ctx.processed / f"{acc}_groups.csv",
                         index_col=0)["group"]
    sigs = {k: set(v) for k, v in
            load_json(ctx.raw / "immune_signatures_28.json").items()}
    hub = load_json(ctx.processed / "hub_genes.json")
    key_gene = hub[0] if hub else None

    scores = ssgsea_scores(expr, sigs)
    save_table(scores, ctx.results / "s07_ssgsea_scores.csv")

    em_cols = groups[groups == "EM"].index
    ct_cols = groups[groups != "EM"].index
    rows = []
    for ct in scores.index:
        a, b = scores.loc[ct, em_cols], scores.loc[ct, ct_cols]
        stat, p = mannwhitneyu(a, b, alternative="two-sided")
        row = {"cell_type": ct, "median_EM": float(a.median()),
               "median_Control": float(b.median()), "wilcoxon_p": float(p)}
        if key_gene and key_gene in expr.index:
            rho, rp = spearmanr(expr.loc[key_gene, scores.columns], scores.loc[ct])
            row.update({"rho_key_gene": float(rho), "rho_p": float(rp)})
        rows.append(row)
    df = pd.DataFrame(rows)
    df["wilcoxon_p_adj"] = bh_adjust(df["wilcoxon_p"].to_numpy())
    df = df.sort_values("wilcoxon_p")
    save_table(df, ctx.results / "s07_immune_tests.csv", index=False)

    sig_df = df[df["wilcoxon_p_adj"] < 0.05]
    corr_hits = df[(df.get("rho_p", 1) < 0.05)] if key_gene else df.iloc[:0]
    out = {
        "key_gene": key_gene,
        "n_cell_types": int(df.shape[0]),
        "n_diff_cell_types": int(sig_df.shape[0]),
        "n_key_gene_correlated": int(corr_hits.shape[0]),
        "top_diff": sig_df.head(5)["cell_type"].tolist(),
    }
    save_json(out, ctx.results / "s07_immune.json")
    return out
