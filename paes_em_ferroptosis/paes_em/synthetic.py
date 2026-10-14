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
        trait = np.array([1.0] * n_case + [0.0] * n_ctrl)
        # latent factors: trait-coupled up/down + three independent modules
        factors = {
            "up": trait + rng.normal(0, 0.35, n),
            "down": -trait + rng.normal(0, 0.35, n),
            "f1": rng.normal(0, 1, n),
            "f2": rng.normal(0, 1, n),
            "f3": rng.normal(0, 1, n),
        }
        module_of = {}
        for gi, g in enumerate(genes):
            if g in ferro:
                module_of[gi] = "up"               # ferroptosis genes trait-up
            elif gi % 13 == 0:
                module_of[gi] = "up"
            elif gi % 29 == 0:
                module_of[gi] = "down"
            elif gi % 7 == 1:
                module_of[gi] = "f1"
            elif gi % 7 == 2:
                module_of[gi] = "f2"
            elif gi % 7 == 3:
                module_of[gi] = "f3"
        for gi, fac in module_of.items():
            load = 0.9 + 0.3 * rng.random()
            expr[gi] += load * factors[fac]
            if fac == "up" and genes[gi] in ferro:
                expr[gi, :n_case] += 0.5           # extra DE margin
        # ARF6 carries the strongest, cleanest trait signal (ground truth)
        gi_key = genes.index("ARF6")
        expr[gi_key] = (base[gi_key] + 1.1 * factors["up"]
                        + rng.normal(0, 0.35, n))
        expr[gi_key, :n_case] += 1.6
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
    paes = ferro + list(
        rng.choice([g for g in genes if g not in ferro], 150, replace=False))
    em = ferro + ["CDH1", "CDH2", "VIM", "SNAI1"] + list(
        rng.choice([g for g in genes if g not in ferro], 180,
                   replace=False))
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
            if ct == "Fibroblasts":              # mesenchymal EMT markers
                lam[genes.index("VIM")] = 3.5
                lam[genes.index("CDH2")] = 3.0
                lam[genes.index("SNAI1")] = 2.5
            else:                                # epithelial marker
                lam[genes.index("CDH1")] = 3.5
        lam_mat = np.tile(lam, (n_per, 1))
        if ct == "Fibroblasts":
            # shared latent activity couples ARF6 with ferroptosis genes
            # AND the mesenchymal EMT markers, giving the virtual-KO GRN
            # its ARF6->FRG edges and the ARF6~CDH2/SNAI1 correlation
            activity = rng.gamma(2.0, 0.5, size=n_per)
            emt_idx = ferro_idx + [genes.index(g)
                                   for g in ("VIM", "CDH2", "SNAI1")]
            lam_mat[:, emt_idx] = np.outer(
                activity, np.maximum(lam[emt_idx], 2.0))
        if ct in ("Lumenal", "Ciliated"):
            # per-cell stemness factor scales ARF6 and a broad progenitor
            # program, so the CytoTRACE-style proxy correlates with ARF6
            stem = rng.gamma(3.0, 1.0 / 3.0, size=n_per)
            lam_mat[:, genes.index("ARF6")] = 4.0 * stem
            prog = slice(100, 380)
            lam_mat[:, prog] = lam_mat[:, prog] * (0.2 + 1.0 * stem[:, None])
        counts = rng.poisson(lam_mat)
        rows.append(counts)
        # condition labels: mesenchymal types enriched in EM (as in the paper)
        p_em = {"Fibroblasts": 0.68, "SmoothMuscle": 0.60,
                "Lumenal": 0.40, "Ciliated": 0.40}.get(ct, 0.5)
        grp = rng.choice(["EM", "Control"], size=n_per, p=[p_em, 1 - p_em])
        meta += [{"cell": f"{ct}_{i}", "cell_type": ct, "group": grp[i]}
                 for i in range(n_per)]
    mat = np.vstack(rows)
    cells = [m["cell"] for m in meta]
    save_table(pd.DataFrame(mat.T, index=genes, columns=cells),
               raw / "sc_counts.csv")
    save_table(pd.DataFrame(meta), raw / "sc_meta.csv", index=False)
    save_json(markers, raw / "sc_marker_truth.json")
    return {"n_cells": len(cells), "n_cell_types": len(CELL_TYPES)}


# -------------------------------------------------------------- spatial ----
def _spatial(rng, genes, raw) -> dict:
    import json as _json
    n_spots = 400
    xy = rng.uniform(0, 100, size=(n_spots, 2))
    markers = _json.loads((raw / "sc_marker_truth.json").read_text())
    midx = {ct: [genes.index(m) for m in ms] for ct, ms in markers.items()}
    # tissue zones: epithelial band (left), fibrotic lesion (circle),
    # stromal background elsewhere
    lesion = ((xy[:, 0] - 60) ** 2 + (xy[:, 1] - 55) ** 2) < 500
    epi_band = (xy[:, 0] < 30) & ~lesion
    stroma = ~lesion & ~epi_band
    lam = np.full((n_spots, len(genes)), 0.35)
    for zone, cts, boosts in [
        (lesion, ["Fibroblasts"],
         {"ARF6": 5.0, "VIM": 4.0, "CDH2": 2.5, "SNAI1": 2.0}),
        (epi_band, ["Lumenal", "Ciliated"], {"CDH1": 3.5, "ARF6": 1.8}),
        (stroma, ["Endothelial", "Tcell", "SmoothMuscle"], {}),
    ]:
        for ct in cts:
            lam[np.ix_(zone, midx[ct])] = 2.4
        for g, v in boosts.items():
            lam[zone, genes.index(g)] = v
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
