"""Deterministic synthetic data for demo mode and tests.

Generates a miniature but structurally faithful version of every input the
real pipeline consumes, with a planted ground truth: ``ARF6`` sits in the
PAEs ∩ EM ∩ FRGs intersection, is up-regulated in EM, separates the groups
for the ML stage, correlates with immune scores, and is enriched in the
fibroblast / epithelial axis of the synthetic single-cell data.

Real runs replace these files in ``data/raw`` with downloads from
GEO / PubChem / ChEMBL / CTD / FerrDb etc. (see README for sources).
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .config import RunContext
from .utils.io import save_json, save_table

N_GENES = 600
CELL_TYPES = [
    "Lumenal", "Ciliated", "Fibroblasts", "SmoothMuscle",
    "Endothelial", "Tcell", "Macrophage",
]
IMMUNE_TYPES = [f"immune_ct_{i:02d}" for i in range(1, 29)]  # 28 signatures


def _gene_pool(rng: np.random.Generator) -> list[str]:
    genes = [f"G{i:04d}" for i in range(N_GENES)]
    # plant real symbols used by the ground truth
    for i, sym in enumerate(
        ["ARF6", "GPX4", "ACSL4", "SLC7A11", "TFRC", "FTH1", "NCOA4",
         "PTGS2", "HMOX1", "NFE2L2", "CDH1", "CDH2", "VIM", "SNAI1"]
    ):
        genes[i] = sym
    return genes


def generate_all(ctx: RunContext) -> dict:
    rng = np.random.default_rng(ctx.seed)
    genes = _gene_pool(rng)
    raw = ctx.raw

    manifest = {}
    manifest["bulk"] = _bulk_datasets(rng, genes, raw)
    manifest["targets"] = _target_lists(rng, genes, raw)
    manifest["gene_sets"] = _annotation_sets(rng, genes, raw)
    manifest["immune"] = _immune_signatures(rng, genes, raw)
    manifest["single_cell"] = _single_cell(rng, genes, raw)
    manifest["spatial"] = _spatial(rng, genes, raw)
    manifest["docking"] = _vina_logs(rng, raw, ctx)
    save_json(manifest, raw / "synthetic_manifest.json")
    return manifest


# ---------------------------------------------------------------- bulk ----
def _bulk_datasets(rng, genes, raw) -> dict:
    out = {}
    ferro = ["ARF6", "GPX4", "ACSL4", "SLC7A11", "TFRC", "FTH1", "NCOA4",
             "PTGS2", "HMOX1", "NFE2L2"]
    for acc, (n_case, n_ctrl) in {
        "GSE51981": (24, 18), "GSE7305": (10, 10), "GSE7846": (5, 5)
    }.items():
        n = n_case + n_ctrl
        base = rng.normal(7, 1.2, size=(len(genes), 1))
        expr = base + rng.normal(0, 0.8, size=(len(genes), n))
        labels = np.array(["EM"] * n_case + ["Control"] * n_ctrl)
        # plant DE signal in ferroptosis genes + a correlated module
        for gi, g in enumerate(genes):
            if g in ferro:
                expr[gi, :n_case] += 1.4 + rng.normal(0, 0.15)
            elif gi % 13 == 0:                     # module co-varying with trait
                expr[gi, :n_case] += 0.9
            elif gi % 29 == 0:                     # down-regulated genes
                expr[gi, :n_case] -= 1.0
        cols = [f"{acc}_S{j:02d}" for j in range(n)]
        df = pd.DataFrame(expr, index=genes, columns=cols)
        save_table(df, raw / f"{acc}_expr.csv")
        save_table(
            pd.DataFrame({"sample": cols, "group": labels}),
            raw / f"{acc}_pheno.csv", index=False,
        )
        out[acc] = {"n_case": n_case, "n_ctrl": n_ctrl}
    return out


# ------------------------------------------------------------- targets ----
def _target_lists(rng, genes, raw) -> dict:
    ferro = ["ARF6", "GPX4", "ACSL4", "SLC7A11", "TFRC", "FTH1", "NCOA4",
             "PTGS2", "HMOX1", "NFE2L2"]
    frgs = ferro + list(rng.choice([g for g in genes if g not in ferro], 90,
                                   replace=False))
    paes = ["ARF6", "GPX4", "ACSL4", "PTGS2", "HMOX1"] + list(
        rng.choice([g for g in genes if g not in ferro], 150, replace=False))
    em = ["ARF6", "SLC7A11", "TFRC", "PTGS2", "CDH1", "CDH2", "VIM",
          "SNAI1"] + list(rng.choice([g for g in genes if g not in ferro],
                                     180, replace=False))
    save_json(sorted(set(frgs)), raw / "frgs_ferrdb.json")
    save_json(sorted(set(paes)), raw / "paes_targets.json")
    save_json(sorted(set(em)), raw / "em_targets.json")
    return {"frgs": len(set(frgs)), "paes": len(set(paes)), "em": len(set(em))}


# ------------------------------------------------------- annotation DB ----
def _annotation_sets(rng, genes, raw) -> dict:
    sets = {}
    themes = (
        [("GO_BP", "response to oxidative stress"),
         ("GO_BP", "iron ion homeostasis"),
         ("GO_BP", "epithelial to mesenchymal transition"),
         ("GO_CC", "membrane raft"),
         ("GO_MF", "GTPase activity"),
         ("KEGG", "Ferroptosis"),
         ("KEGG", "Chemical carcinogenesis"),
         ("KEGG", "Regulation of actin cytoskeleton")]
    )
    ferro = ["ARF6", "GPX4", "ACSL4", "SLC7A11", "TFRC", "FTH1", "NCOA4",
             "PTGS2", "HMOX1", "NFE2L2"]
    for i, (db, name) in enumerate(themes):
        members = list(rng.choice(genes, 30, replace=False))
        if i < 3 or db == "KEGG" and name == "Ferroptosis":
            members = ferro + members          # make ferroptosis-themed terms hit
        sets[f"{db}::{name}"] = sorted(set(members))
    # background noise terms
    for j in range(20):
        sets[f"GO_BP::noise term {j}"] = sorted(
            rng.choice(genes, 25, replace=False).tolist())
    save_json(sets, raw / "annotation_gene_sets.json")
    return {"n_terms": len(sets)}


# ------------------------------------------------------------- immune ----
def _immune_signatures(rng, genes, raw) -> dict:
    sigs = {}
    for ct in IMMUNE_TYPES:
        sigs[ct] = sorted(rng.choice(genes, 15, replace=False).tolist())
    # couple two signatures to the planted DE genes so ARF6 correlation exists
    sigs["immune_ct_01"] = sorted(set(sigs["immune_ct_01"][:10] +
                                      ["GPX4", "ACSL4", "PTGS2", "HMOX1"]))
    save_json(sigs, raw / "immune_signatures_28.json")
    return {"n_signatures": len(sigs)}


# --------------------------------------------------------- single cell ----
def _single_cell(rng, genes, raw) -> dict:
    n_per = 80
    rows, meta = [], []
    markers = {ct: list(rng.choice(genes, 12, replace=False))
               for ct in CELL_TYPES}
    ferro = ["ARF6", "GPX4", "ACSL4", "SLC7A11", "TFRC", "FTH1", "NCOA4",
             "PTGS2", "HMOX1", "NFE2L2"]
    ferro_idx = [genes.index(g) for g in ferro]
    for ct in CELL_TYPES:
        lam = np.full(len(genes), 0.3)
        lam[[genes.index(m) for m in markers[ct]]] = 3.0
        if ct in ("Fibroblasts", "Lumenal", "Ciliated"):
            lam[genes.index("ARF6")] = 4.0       # ARF6-high axis of the paper
            lam[genes.index("VIM" if ct == "Fibroblasts" else "CDH1")] = 3.5
        lam_mat = np.tile(lam, (n_per, 1))
        if ct == "Fibroblasts":
            # shared latent activity couples ARF6 with ferroptosis genes,
            # giving the virtual-KO GRN its ARF6->FRG edges
            activity = rng.gamma(2.0, 0.5, size=n_per)
            lam_mat[:, ferro_idx] = np.outer(
                activity, np.maximum(lam[ferro_idx], 2.0))
        counts = rng.poisson(lam_mat)
        rows.append(counts)
        meta += [{"cell": f"{ct}_{i}", "cell_type": ct} for i in range(n_per)]
    mat = np.vstack(rows)
    cells = [m["cell"] for m in meta]
    save_table(pd.DataFrame(mat.T, index=genes, columns=cells),
               raw / "sc_counts.csv")
    save_table(pd.DataFrame(meta), raw / "sc_meta.csv", index=False)
    save_json(markers, raw / "sc_marker_truth.json")
    return {"n_cells": len(cells), "n_cell_types": len(CELL_TYPES)}


# -------------------------------------------------------------- spatial ----
def _spatial(rng, genes, raw) -> dict:
    n_spots = 400
    xy = rng.uniform(0, 100, size=(n_spots, 2))
    # lesion region: circle where fibro/epithelial mix and ARF6 high
    lesion = ((xy[:, 0] - 60) ** 2 + (xy[:, 1] - 55) ** 2) < 500
    lam = np.full((n_spots, len(genes)), 0.4)
    lam[lesion, genes.index("ARF6")] = 5.0
    lam[lesion, genes.index("VIM")] = 4.0
    counts = rng.poisson(lam)
    spots = [f"spot_{i:04d}" for i in range(n_spots)]
    save_table(pd.DataFrame(counts.T, index=genes, columns=spots),
               raw / "spatial_counts.csv")
    save_table(pd.DataFrame({"spot": spots, "x": xy[:, 0], "y": xy[:, 1],
                             "lesion": lesion}),
               raw / "spatial_coords.csv", index=False)
    return {"n_spots": n_spots}


# -------------------------------------------------------------- docking ----
def _vina_logs(rng, raw, ctx) -> dict:
    """Write AutoDock-Vina-style log files for each configured PAE so the
    docking stage's parser/filter runs in demo mode (no Vina needed)."""
    vdir = raw / "vina_logs"
    vdir.mkdir(exist_ok=True)
    compounds = [c["name"] for c in
                 ctx.cfg["network_toxicology"]["compounds"]]
    energies = {}
    for i, name in enumerate(compounds):
        best = round(float(-5.2 - rng.uniform(0, 2.3)), 1)
        energies[name] = best
        lines = ["mode |   affinity | dist from best mode",
                 "     | (kcal/mol) | rmsd l.b.| rmsd u.b.",
                 "-----+------------+----------+----------"]
        for m in range(1, 6):
            aff = best + 0.3 * (m - 1)
            lines.append(f"   {m}       {aff:6.1f}      0.000      0.000")
        (vdir / f"{name}_2A5D.log").write_text("\n".join(lines))
    return {"receptor": "2A5D", "compounds": energies}
