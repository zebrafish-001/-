"""Stage 9 — spatial transcriptomics.

Paper workflow: SCTransform normalization → RCTD deconvolution (using the
scRNA-seq reference) → SpatialFeaturePlot of ARF6.

``R/rctd.R`` is the hook for the real SCTransform+RCTD run; the
python-lite engine normalizes spots, scores them with a marker-based
soft deconvolution proxy, tests key-gene enrichment in lesion vs
non-lesion spots, and renders the spatial feature plot with matplotlib.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu

from ..config import RunContext, PKG_ROOT
from ..utils.io import load_json, run_rscript, save_json, save_table


def run(ctx: RunContext) -> dict:
    if ctx.cfg["spatial"].get("deconvolution") == "rctd" and not ctx.demo:
        if run_rscript(PKG_ROOT / "R" / "rctd.R",
                       [str(ctx.raw), str(ctx.results)]):
            return {"engine": "R/SCTransform+RCTD", "see": "s09_* outputs"}

    if not (ctx.raw / "spatial_counts.csv").exists():
        out = {"engine": "skipped",
               "reason": "no spatial dataset configured/available"}
        save_json(out, ctx.results / "s09_spatial.json")
        return out
    counts = pd.read_csv(ctx.raw / "spatial_counts.csv", index_col=0)
    coords = pd.read_csv(ctx.raw / "spatial_coords.csv")
    markers = load_json(ctx.raw / "sc_marker_truth.json")
    hub = load_json(ctx.processed / "hub_genes.json")
    key_gene = hub[0] if hub else "ARF6"

    lib = counts.sum(axis=0)
    norm = np.log1p(counts / lib.replace(0, 1) * 1e4)

    # marker-score soft deconvolution proxy (RCTD stand-in)
    comp = {}
    for ct, ms in markers.items():
        ms_in = [m for m in ms if m in norm.index]
        comp[ct] = norm.loc[ms_in].mean(axis=0)
    comp_df = pd.DataFrame(comp)
    comp_df = comp_df.div(comp_df.sum(axis=1).replace(0, 1), axis=0)
    save_table(comp_df, ctx.results / "s09_deconvolution_proxy.csv")

    kg = norm.loc[key_gene] if key_gene in norm.index else None
    p_lesion = None
    if kg is not None and "lesion" in coords:
        lesion_mask = coords.set_index("spot")["lesion"]
        a = kg[lesion_mask[lesion_mask].index]
        b = kg[lesion_mask[~lesion_mask].index]
        p_lesion = float(mannwhitneyu(a, b, alternative="greater")[1])

        # SpatialFeaturePlot equivalent
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6, 5))
        sc = ax.scatter(coords["x"], coords["y"], c=kg[coords["spot"]],
                        s=14, cmap="magma")
        fig.colorbar(sc, label=f"{key_gene} (log-normalized)")
        ax.set_title(f"Spatial expression of {key_gene}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        fig.tight_layout()
        fig.savefig(ctx.results / "s09_spatial_feature_plot.png", dpi=150)
        plt.close(fig)

    out = {
        "engine": "python-lite",
        "n_spots": int(norm.shape[1]),
        "key_gene": key_gene,
        "lesion_enrichment_p": p_lesion,
        "figure": "s09_spatial_feature_plot.png",
    }
    save_json(out, ctx.results / "s09_spatial.json")
    return out
