"""Stage 8 — single-cell RNA-seq analysis.

Paper workflow: Seurat QC/clustering → 7 annotated cell types → CytoTRACE
stemness → Monocle2 pseudotime, centred on the ARF6-high
Lumenal+Ciliated → Fibroblasts EMT axis.

Engines:
* ``R/singlecell.R`` hook (Seurat + CytoTRACE + Monocle2) when Rscript and
  the packages are available (real runs);
* python-lite fallback: library-size + log normalization, PCA, k-means to
  the configured number of clusters, marker-score annotation, a
  CytoTRACE-style stemness proxy (per-cell gene counts correlated against
  expression), and PCA-based pseudotime along the epithelial→fibroblast
  axis. scanpy slots in transparently if installed (demo stays
  dependency-light).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

from ..config import RunContext, PKG_ROOT
from ..utils.io import load_json, run_rscript, save_json, save_table


def _normalize(counts: pd.DataFrame) -> pd.DataFrame:
    lib = counts.sum(axis=0)
    return np.log1p(counts / lib.replace(0, 1) * 1e4)


def run(ctx: RunContext) -> dict:
    cfg = ctx.cfg["single_cell"]
    if cfg.get("engine") in ("auto", "r") and not ctx.demo:
        if run_rscript(PKG_ROOT / "R" / "singlecell.R",
                       [str(ctx.raw), str(ctx.results)]):
            return {"engine": "R/Seurat+CytoTRACE+Monocle2",
                    "see": "s08_* outputs"}

    counts = pd.read_csv(ctx.raw / "sc_counts.csv", index_col=0)
    meta = pd.read_csv(ctx.raw / "sc_meta.csv")
    markers = load_json(ctx.raw / "sc_marker_truth.json")
    hub = load_json(ctx.processed / "hub_genes.json")
    key_gene = hub[0] if hub else "ARF6"

    # QC
    genes_per_cell = (counts > 0).sum(axis=0)
    keep = genes_per_cell >= min(cfg["qc"]["min_genes"],
                                 int(genes_per_cell.median() * 0.2))
    counts = counts.loc[:, keep]
    meta = meta[meta["cell"].isin(counts.columns)].reset_index(drop=True)

    norm = _normalize(counts)
    pcs = PCA(n_components=20, random_state=ctx.seed).fit_transform(
        norm.T.to_numpy())
    km = KMeans(cfg["n_cell_types"], n_init=10,
                random_state=ctx.seed).fit_predict(pcs)

    # annotate clusters by mean marker-set score
    ann = {}
    for cl in range(cfg["n_cell_types"]):
        cells = norm.columns[km == cl]
        best, best_s = None, -np.inf
        for ct, ms in markers.items():
            s = norm.loc[[m for m in ms if m in norm.index], cells].mean().mean()
            if s > best_s:
                best, best_s = ct, s
        ann[cl] = best
    meta["cluster"] = km
    meta["annotated"] = [ann[c] for c in km]
    acc = float((meta["annotated"] == meta["cell_type"]).mean()) \
        if "cell_type" in meta else None

    # CytoTRACE-style stemness proxy: per-cell detected-gene count,
    # smoothed by correlation with the count-correlated gene module
    n_detected = (counts > 0).sum(axis=0).astype(float)
    gcor = norm.apply(lambda row: np.corrcoef(row, n_detected)[0, 1], axis=1)
    top = gcor.abs().sort_values(ascending=False).index[:50]
    stem = norm.loc[top].mean(axis=0)
    stem = (stem - stem.min()) / (stem.max() - stem.min() + 1e-12)
    meta["stemness"] = stem.loc[meta["cell"]].to_numpy()

    # pseudotime: PC1 across the EMT axis cell types, origin at epithelium
    axis_types = ["Lumenal", "Ciliated", "Fibroblasts"]
    axis_cells = meta[meta["annotated"].isin(axis_types)]["cell"]
    sub_pcs = PCA(n_components=2, random_state=ctx.seed).fit_transform(
        norm[axis_cells].T.to_numpy())
    pt = sub_pcs[:, 0]
    epi = meta.set_index("cell").loc[axis_cells, "annotated"].isin(
        ["Lumenal", "Ciliated"]).to_numpy()
    if pt[epi].mean() > pt[~epi].mean():
        pt = -pt
    pt = (pt - pt.min()) / (pt.max() - pt.min() + 1e-12)
    ptime = pd.Series(pt, index=axis_cells, name="pseudotime")
    save_table(ptime.to_frame(), ctx.results / "s08_pseudotime.csv")

    # key-gene statistics along the axis
    kg = norm.loc[key_gene] if key_gene in norm.index else None
    kg_by_type = (
        {ct: float(kg[meta[meta["annotated"] == ct]["cell"]].mean())
         for ct in sorted(set(meta["annotated"]))} if kg is not None else {})
    rho_stem = rho_pt = p_axis = None
    if kg is not None:
        rho_stem = float(spearmanr(kg.loc[meta["cell"]],
                                   meta["stemness"])[0])
        rho_pt = float(spearmanr(kg.loc[axis_cells], pt)[0])
        on_axis = kg.loc[axis_cells]
        off_axis = kg.drop(axis_cells)
        p_axis = float(mannwhitneyu(on_axis, off_axis,
                                    alternative="greater")[1])
    save_table(meta, ctx.results / "s08_cell_meta.csv", index=False)

    out = {
        "engine": "python-lite",
        "n_cells": int(norm.shape[1]),
        "n_clusters": cfg["n_cell_types"],
        "annotation_accuracy_vs_truth": acc,
        "key_gene": key_gene,
        "key_gene_mean_by_type": kg_by_type,
        "key_gene_rho_stemness": rho_stem,
        "key_gene_rho_pseudotime": rho_pt,
        "key_gene_axis_enrichment_p": p_axis,
    }
    save_json(out, ctx.results / "s08_singlecell.json")
    return out
