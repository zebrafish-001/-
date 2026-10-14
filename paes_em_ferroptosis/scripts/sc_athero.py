#!/usr/bin/env python
"""Real scRNA-seq processing for GSE159677 (carotid plaque, 3 patients x
calcified core [DIS] + proximal adjacent [HEA]).

Scanpy workflow: load 6 CellRanger matrices -> QC (min_genes, mito%) ->
normalize/log -> HVG -> PCA -> harmony-free concat (sample as covariate
noted) -> neighbors -> Leiden -> marker-based annotation of 7 major cell
types -> SMC phenotype-switching axis (Contractile SMC -> Modulated
SMC/Fibromyocyte, the EMT analog in atherosclerosis) -> CytoTRACE-style
stemness -> diffusion-free PCA pseudotime -> per-type hub-gene stats.

Writes (into <results>):
  s08_cell_meta.csv      cell, sample, group(DIS/HEA), leiden, annotated,
                         stemness
  s08_pseudotime.csv     SMC-axis cells with pseudotime
  s08_singlecell.json    summary incl. hub-gene statistics
And (into <raw>): sc_counts_subset.csv (genes x cells, subsampled for the
virtual-knockout stage), sc_meta.csv, sc_marker_truth.json (markers used).

Usage: sc_athero.py <sc_dir> <raw_dir> <results_dir> <hub_gene>
"""

from __future__ import annotations

import json
import re
import sys
import tarfile
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import scanpy as sc
from scipy.stats import mannwhitneyu, spearmanr

MARKERS = {
    "Endothelial": ["PECAM1", "VWF", "CLDN5", "ESAM"],
    "SMC_contractile": ["MYH11", "CNN1", "ACTA2", "TAGLN", "MYL9"],
    "Fibromyocyte": ["FN1", "LUM", "DCN", "TNFRSF11B", "COL1A1", "COL1A2"],
    "Macrophage": ["CD68", "LYZ", "CD14", "AIF1", "C1QA"],
    "Tcell": ["CD3E", "CD3D", "TRAC", "IL7R"],
    "NK": ["NKG7", "GNLY", "KLRD1"],
    "Bcell": ["CD79A", "MS4A1", "IGHM"],
}
AXIS = ["SMC_contractile", "Fibromyocyte"]   # phenotype-switching axis


def load_sample(tgz: Path) -> sc.AnnData:
    with tempfile.TemporaryDirectory() as td:
        with tarfile.open(tgz) as tf:
            tf.extractall(td, filter="data")
        mat_dir = next(Path(td).rglob("filtered_feature_bc_matrix"))
        ad = sc.read_10x_mtx(mat_dir, var_names="gene_symbols",
                             make_unique=True)
    gsm = tgz.name.split("_")[0]
    group = "DIS" if "DIS" in tgz.name else "HEA"
    ad.obs["sample"] = gsm
    ad.obs["group"] = group
    ad.obs_names = [f"{gsm}_{bc}" for bc in ad.obs_names]
    return ad


def main(sc_dir: Path, raw: Path, results: Path, hub: str):
    results.mkdir(parents=True, exist_ok=True)
    adatas = [load_sample(p) for p in sorted(sc_dir.glob("*.tar.gz"))]
    ad = sc.concat(adatas, join="inner")
    ad.var_names_make_unique()
    print("loaded:", ad.shape)

    # ---- QC ----
    ad.var["mt"] = ad.var_names.str.startswith("MT-")
    sc.pp.calculate_qc_metrics(ad, qc_vars=["mt"], inplace=True,
                               percent_top=None, log1p=False)
    ad = ad[(ad.obs.n_genes_by_counts >= 200) &
            (ad.obs.n_genes_by_counts <= 6000) &
            (ad.obs.pct_counts_mt < 20)].copy()
    sc.pp.filter_genes(ad, min_cells=10)
    print("post-QC:", ad.shape)

    ad.layers["counts"] = ad.X.copy()
    sc.pp.normalize_total(ad, target_sum=1e4)
    sc.pp.log1p(ad)
    ad.raw = ad
    sc.pp.highly_variable_genes(ad, n_top_genes=2000, batch_key="sample")
    hv = ad[:, ad.var.highly_variable].copy()
    sc.pp.scale(hv, max_value=10)
    sc.tl.pca(hv, n_comps=30)
    ad.obsm["X_pca"] = hv.obsm["X_pca"]
    sc.pp.neighbors(ad, n_neighbors=15)
    sc.tl.leiden(ad, resolution=0.5, flavor="igraph", n_iterations=2,
                 directed=False)
    print("clusters:", ad.obs.leiden.value_counts().to_dict())

    # ---- annotate clusters by mean marker z-scores ----
    expr = ad.raw.to_adata()
    scores = {}
    for ct, ms in MARKERS.items():
        ms_in = [m for m in ms if m in expr.var_names]
        sc.tl.score_genes(ad, ms_in, score_name=f"score_{ct}")
    ann = {}
    for cl in ad.obs.leiden.cat.categories:
        mask = ad.obs.leiden == cl
        best = max(MARKERS, key=lambda ct:
                   ad.obs.loc[mask, f"score_{ct}"].mean())
        ann[cl] = best
    ad.obs["annotated"] = ad.obs.leiden.map(ann).astype(str)
    print("annotation:", ad.obs.annotated.value_counts().to_dict())

    # ---- stemness (CytoTRACE-style proxy) ----
    counts = ad.layers["counts"]
    n_detected = np.asarray((counts > 0).sum(axis=1)).ravel().astype(float)
    X = ad.X.tocsr() if hasattr(ad.X, "tocsr") else ad.X
    nc = n_detected - n_detected.mean()
    # sparse per-gene correlation with detected-gene counts
    num = np.asarray(X.T.dot(nc)).ravel()           # centering nc kills mu term
    mu = np.asarray(X.mean(axis=0)).ravel()
    ex2 = np.asarray(X.power(2).mean(axis=0)).ravel()
    sd_g = np.sqrt(np.maximum(ex2 - mu ** 2, 1e-12)) * np.sqrt(X.shape[0])
    gcor = num / (sd_g * np.linalg.norm(nc) + 1e-12)
    top = np.argsort(-np.abs(gcor))[:200]
    stem = np.asarray(X[:, top].mean(axis=1)).ravel()
    stem = (stem - stem.min()) / (stem.max() - stem.min() + 1e-12)
    ad.obs["stemness"] = stem

    # ---- SMC phenotype-switching pseudotime ----
    axis_mask = ad.obs.annotated.isin(AXIS).to_numpy()
    sub = ad[axis_mask].copy()
    pt = sub.obsm["X_pca"][:, 0].astype(float)
    con = (sub.obs.annotated == "SMC_contractile").to_numpy()
    if pt[con].mean() > pt[~con].mean():
        pt = -pt
    pt = (pt - pt.min()) / (pt.max() - pt.min() + 1e-12)
    sub.obs["pseudotime"] = pt
    sub.obs[["pseudotime"]].to_csv(results / "s08_pseudotime.csv")

    # ---- hub-gene statistics ----
    def gvec(adata, g):
        if g not in adata.raw.var_names:
            return None
        v = adata.raw[:, g].X
        return np.asarray(v.todense()).ravel() if hasattr(v, "todense") \
            else np.asarray(v).ravel()

    kg = gvec(ad, hub)
    out = {"engine": "scanpy", "n_cells": int(ad.n_obs),
           "n_genes": int(ad.n_vars),
           "n_clusters": int(ad.obs.leiden.nunique()),
           "cell_type_counts": ad.obs.annotated.value_counts().to_dict(),
           "key_gene": hub}
    if kg is not None:
        by_type = {ct: float(kg[(ad.obs.annotated == ct).to_numpy()].mean())
                   for ct in sorted(set(ad.obs.annotated))}
        out["key_gene_mean_by_type"] = by_type
        rho_s, p_s = spearmanr(kg, ad.obs["stemness"])
        out["key_gene_rho_stemness"] = float(rho_s)
        kg_axis = gvec(sub, hub)
        rho_pt, p_pt = spearmanr(kg_axis, pt)
        out["key_gene_rho_pseudotime"] = float(rho_pt)
        out["key_gene_rho_pseudotime_p"] = float(p_pt)
        on = kg[axis_mask]
        off = kg[~axis_mask]
        out["key_gene_axis_enrichment_p"] = float(
            mannwhitneyu(on, off, alternative="greater")[1])
        dis = kg[(ad.obs.group == "DIS").to_numpy()]
        hea = kg[(ad.obs.group == "HEA").to_numpy()]
        out["key_gene_DIS_vs_HEA_p"] = float(
            mannwhitneyu(dis, hea, alternative="greater")[1])
        out["key_gene_mean_DIS"] = float(dis.mean())
        out["key_gene_mean_HEA"] = float(hea.mean())

    # ---- figure-ready exports ----
    viz = pd.DataFrame({
        "cell": ad.obs_names,
        "pc1": ad.obsm["X_pca"][:, 0], "pc2": ad.obsm["X_pca"][:, 1],
        "annotated": ad.obs.annotated.to_numpy(),
        "group": ad.obs.group.to_numpy(),
        "stemness": ad.obs.stemness.to_numpy(),
    })
    if kg is not None:
        viz["key_gene_expr"] = kg
    viz.to_csv(results / "s08_cells_viz.csv", index=False)

    # marker dotplot data (top-2 markers per type)
    rows = []
    for ct, ms in MARKERS.items():
        for m in ms[:2]:
            v = gvec(ad, m)
            if v is None:
                continue
            for ct2 in sorted(set(ad.obs.annotated)):
                mask = (ad.obs.annotated == ct2).to_numpy()
                rows.append({"marker": m, "cell_type": ct2,
                             "mean": float(v[mask].mean()),
                             "pct": float((v[mask] > 0).mean())})
    pd.DataFrame(rows).to_csv(results / "s08_marker_dotplot.csv",
                              index=False)

    # axis cells: embedding + pseudotime + switching markers
    axis_genes = [g for g in ("MYH11", "ACTA2", "TAGLN", "FN1", "LUM",
                              "COL1A1", hub) if g in sub.raw.var_names]
    ax_df = pd.DataFrame({
        "cell": sub.obs_names,
        "pc1": sub.obsm["X_pca"][:, 0], "pc2": sub.obsm["X_pca"][:, 1],
        "annotated": sub.obs.annotated.to_numpy(),
        "pseudotime": pt,
    })
    for g in axis_genes:
        ax_df[g] = gvec(sub, g)
    ax_df.to_csv(results / "s08_axis_cells.csv", index=False)

    meta = ad.obs[["sample", "group", "leiden", "annotated",
                   "stemness"]].copy()
    meta.index.name = "cell"
    meta.reset_index().to_csv(results / "s08_cell_meta.csv", index=False)
    (results / "s08_singlecell.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False))
    json.dump(MARKERS, open(raw / "sc_marker_truth.json", "w"), indent=1)

    # ---- export subset for the virtual-knockout stage ----
    # target cell type: the modulated SMC/fibromyocyte population
    tgt = "Fibromyocyte"
    cells = ad.obs_names[(ad.obs.annotated == tgt).to_numpy()]
    rng = np.random.default_rng(0)
    if len(cells) > 1500:
        cells = rng.choice(cells, 1500, replace=False)
    subx = ad.raw.to_adata()[cells]
    expr_mean = np.asarray(subx.X.mean(axis=0)).ravel()
    keep_genes = subx.var_names[np.argsort(-expr_mean)[:3000]]
    frgs = set(json.load(open(raw / "frgs_ferrdb.json")))
    keep_genes = sorted(set(keep_genes) | (frgs & set(subx.var_names))
                        | ({hub} & set(subx.var_names)))
    dense = subx[:, keep_genes].X
    dense = np.asarray(dense.todense()) if hasattr(dense, "todense") \
        else np.asarray(dense)
    df = pd.DataFrame(dense.T, index=keep_genes, columns=cells)
    df.to_csv(raw / "sc_counts.csv")
    pd.DataFrame({"cell": cells, "cell_type": tgt}).to_csv(
        raw / "sc_meta.csv", index=False)
    print(json.dumps(out, indent=1, ensure_ascii=False)[:600])


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]),
         sys.argv[4])
