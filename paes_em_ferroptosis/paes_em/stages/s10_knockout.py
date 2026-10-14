"""Stage 10 — virtual knockout of the key gene in fibroblasts.

Paper workflow: scTenifoldKnk builds a fibroblast gene regulatory network,
zeroes the key gene's outgoing edges, and ranks genes by the perturbation
of their network profile; perturbed ferroptosis genes are then enriched.

``R/sctenifoldknk.R`` is the exact-method hook. The python-lite engine
follows the same principle: a denoised correlation-based GRN on fibroblast
cells, knockout = zeroing the key gene's row/column, per-gene perturbation
score = distance between pre/post network profiles propagated one step,
then hypergeometric enrichment of FRGs among the top-perturbed genes and
ORA of those genes against the annotation sets.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import hypergeom

from ..config import RunContext, PKG_ROOT
from ..utils.io import load_json, run_rscript, save_json, save_table
from ..utils.stats import hypergeom_ora


def run(ctx: RunContext) -> dict:
    cfg = ctx.cfg["virtual_knockout"]
    if cfg.get("method") == "sctenifoldknk" and not ctx.demo:
        if run_rscript(PKG_ROOT / "R" / "sctenifoldknk.R",
                       [str(ctx.raw), str(ctx.results)]):
            return {"engine": "R/scTenifoldKnk", "see": "s10_* outputs"}

    counts = pd.read_csv(ctx.raw / "sc_counts.csv", index_col=0)
    meta = pd.read_csv(ctx.raw / "sc_meta.csv")
    frgs = set(load_json(ctx.raw / "frgs_ferrdb.json"))
    hub = load_json(ctx.processed / "hub_genes.json")
    key_gene = hub[0] if hub else "ARF6"
    target_ct = cfg["target_cell_type"]

    cells = meta[meta["cell_type"] == target_ct]["cell"]
    sub = counts[cells]
    sub = np.log1p(sub / sub.sum(axis=0).replace(0, 1) * 1e4)
    # keep expressed genes
    expressed = sub.index[(sub > 0).mean(axis=1) > 0.05]
    sub = sub.loc[expressed]
    if key_gene not in sub.index:
        raise RuntimeError(f"{key_gene} not expressed in {target_ct}")

    x = sub.to_numpy()
    cor = np.corrcoef(x)
    cor = np.nan_to_num(cor)
    # denoise: keep strong edges only (soft threshold)
    grn = np.where(np.abs(cor) > 0.1, cor, 0.0)
    np.fill_diagonal(grn, 0.0)

    gi = sub.index.get_loc(key_gene)
    grn_ko = grn.copy()
    grn_ko[gi, :] = 0.0
    grn_ko[:, gi] = 0.0

    # one-step propagation of each gene's regulatory profile
    pre = grn @ grn
    post = grn_ko @ grn_ko
    pert = np.linalg.norm(pre - post, axis=1)
    pert_df = pd.DataFrame(
        {"gene": sub.index, "perturbation": pert,
         "is_FRG": [g in frgs for g in sub.index]}
    ).sort_values("perturbation", ascending=False).reset_index(drop=True)
    pert_df = pert_df[pert_df["gene"] != key_gene]
    save_table(pert_df, ctx.results / "s10_perturbation.csv", index=False)

    top_n = max(25, int(0.05 * len(pert_df)))
    top = pert_df.head(top_n)
    k = int(top["is_FRG"].sum())
    K = int(pert_df["is_FRG"].sum())
    p_frg = float(hypergeom.sf(k - 1, len(pert_df), K, top_n))

    # ORA of top-perturbed genes
    gene_sets = {k_: set(v) for k_, v in
                 load_json(ctx.raw / "annotation_gene_sets.json").items()}
    ora = hypergeom_ora(set(top["gene"]), set(pert_df["gene"]), gene_sets)
    save_table(ora, ctx.results / "s10_perturbed_enrichment.csv", index=False)

    out = {
        "engine": "python-lite",
        "knockout_gene": key_gene,
        "cell_type": target_ct,
        "n_network_genes": int(len(pert_df)),
        "top_perturbed": top["gene"].head(10).tolist(),
        "frg_in_top": k,
        "frg_enrichment_p": p_frg,
        "top_terms": ora.head(5)["term"].tolist() if not ora.empty else [],
    }
    save_json(out, ctx.results / "s10_knockout.json")
    return out
