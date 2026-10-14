"""Stage 4 — WGCNA (weighted gene co-expression network analysis).

Engine selection:
* ``auto``/``r``  — call ``R/wgcna.R`` (the real WGCNA package) if Rscript
  is on PATH; falls back to the python-lite engine otherwise.
* ``python``      — python-lite reimplementation: signed-hybrid adjacency
  ``|cor|^beta``, TOM similarity, average-linkage hierarchical module
  detection, module eigengenes (PC1), module–trait correlation.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.cluster import hierarchy
from scipy.stats import pearsonr

from ..config import RunContext, PKG_ROOT
from ..utils.io import run_rscript, save_json, save_table


def _pick_soft_power(cor_abs: np.ndarray, target_r2: float) -> int:
    """Smallest beta in 1..20 whose degree distribution is scale-free-ish."""
    for beta in range(1, 21):
        k = (cor_abs ** beta).sum(axis=0)
        k = k[k > 0]
        hist, edges = np.histogram(np.log10(k + 1e-9), bins=10)
        mask = hist > 0
        if mask.sum() < 3:
            continue
        centers = 0.5 * (edges[1:] + edges[:-1])
        r = np.corrcoef(centers[mask], np.log10(hist[mask]))[0, 1]
        if r ** 2 >= target_r2 and r < 0:
            return beta
    return 6  # WGCNA's customary default


def _tom(adj: np.ndarray) -> np.ndarray:
    """Topological overlap matrix from an adjacency matrix."""
    np.fill_diagonal(adj, 0.0)
    l_mat = adj @ adj
    k = adj.sum(axis=0)
    denom = np.minimum.outer(k, k) + 1 - adj
    tom = (l_mat + adj) / np.where(denom <= 0, 1, denom)
    np.fill_diagonal(tom, 1.0)
    return tom


def run(ctx: RunContext) -> dict:
    cfg = ctx.cfg["wgcna"]
    acc = ctx.cfg["datasets"]["training"][0]["accession"]
    engine = cfg.get("engine", "auto")

    if engine in ("auto", "r") and not ctx.demo:
        ok = run_rscript(PKG_ROOT / "R" / "wgcna.R",
                         [str(ctx.processed), str(ctx.results), acc])
        if ok:
            return {"engine": "R/WGCNA", "see": "s04_wgcna_r_output"}

    expr = pd.read_csv(ctx.processed / f"{acc}_expr.csv", index_col=0)
    groups = pd.read_csv(ctx.processed / f"{acc}_groups.csv",
                         index_col=0)["group"]
    trait = (groups == "EM").astype(float).to_numpy()

    # top-MAD genes
    mad = (expr.sub(expr.median(axis=1), axis=0)).abs().median(axis=1)
    keep = mad.sort_values(ascending=False).index[: cfg["top_mad_genes"]]
    x = expr.loc[keep]

    cor = np.corrcoef(x.to_numpy())
    cor_abs = np.abs(np.nan_to_num(cor))
    beta = cfg["soft_power"] or _pick_soft_power(
        cor_abs, cfg["scale_free_r2_target"])
    tom = _tom(cor_abs ** beta)

    # background filter: low-connectivity genes go straight to grey
    # (approximates WGCNA's dynamic tree cut, which prunes unassigned
    # genes; noise genes otherwise chain the dendrogram together)
    conn = tom.sum(axis=0) - 1
    connected = conn > np.quantile(conn, 0.5)
    sub_tom = tom[np.ix_(connected, connected)]
    sub_genes = keep[connected]

    dist = 1 - sub_tom
    # Ward linkage approximates WGCNA's dynamic tree cut far better than
    # average linkage on real TOMs (average linkage chains into one blob).
    link = hierarchy.linkage(dist[np.triu_indices_from(dist, 1)],
                             method="ward")
    min_size = min(cfg["min_module_size"], max(10, len(sub_genes) // 20))
    # deepest cut at which every cluster still clears the size floor
    best_labels = None
    for k in range(2, 16):
        labels = hierarchy.fcluster(link, t=k, criterion="maxclust")
        sizes = pd.Series(labels).value_counts()
        if sizes.min() < min_size:
            break
        best_labels = labels
    if best_labels is None:
        best_labels = hierarchy.fcluster(link, t=2, criterion="maxclust")
    modules = pd.Series(0, index=keep, name="module")
    modules.loc[sub_genes] = best_labels
    # relabel modules as 1..k ordered by size; 0 stays grey/background
    order = [m for m in modules.value_counts().index if m != 0]
    remap = {old: i + 1 for i, old in enumerate(order)}
    remap[0] = 0
    modules = modules.map(remap)
    big = modules.value_counts()
    keep_ids = big[(big >= min_size) & (big <= 0.5 * len(keep))].index
    modules[~modules.isin(keep_ids)] = 0  # grey / background

    # module eigengene = PC1; correlate with trait
    rows = []
    for m in sorted(set(modules) - {0}):
        sub = x.loc[modules[modules == m].index].to_numpy()
        sub = (sub - sub.mean(1, keepdims=True)) / (
            sub.std(1, keepdims=True) + 1e-9)
        u, s, vt = np.linalg.svd(sub, full_matrices=False)
        eig = vt[0]
        # orient eigengene so it correlates positively with mean expression
        mean_expr = sub.mean(axis=0)
        if np.corrcoef(eig, mean_expr)[0, 1] < 0:
            eig = -eig
        r, p = pearsonr(eig, trait)
        rows.append({"module": int(m), "n_genes": int((modules == m).sum()),
                     "trait_cor": float(r), "trait_p": float(p)})
    mt = pd.DataFrame(rows, columns=["module", "n_genes", "trait_cor",
                                     "trait_p"]).sort_values("trait_p")
    save_table(mt, ctx.results / "s04_module_trait.csv", index=False)
    save_table(modules.to_frame(), ctx.results / "s04_modules.csv")

    key_modules = mt[(mt["trait_p"] < 0.05)]["module"].tolist()
    key_genes = sorted(modules[modules.isin(key_modules)].index)
    save_json(key_genes, ctx.processed / "wgcna_key_genes.json")

    out = {
        "engine": "python-lite",
        "soft_power": int(beta),
        "n_modules": int(mt.shape[0]),
        "key_modules": key_modules,
        "n_key_genes": len(key_genes),
    }
    save_json(out, ctx.results / "s04_wgcna.json")
    return out
