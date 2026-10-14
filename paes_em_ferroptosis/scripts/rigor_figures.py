"""Supplementary rigor figures (S1-S3) visualizing the statistical
corrections: pan-target dominance, ML CV-vs-external + permutation,
pseudoreplication / composition evidence. Uses the project palette.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RES = Path("athero/results")
SURFACE, INK, INK2, GRID, NEUTRAL = "#fcfcfb", "#0b0b0b", "#52514e", "#e8e7e3", "#c3c2b7"
BLUE, RED, HL = "#2a78d6", "#e34948", "#1c5cab"


def _style(ax, xg=False, yg=True):
    ax.set_facecolor(SURFACE)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=8.5)
    if yg:
        ax.grid(axis="y", color=GRID, lw=0.8)
    if xg:
        ax.grid(axis="x", color=GRID, lw=0.8)
    ax.set_axisbelow(True)


def _save(fig, name):
    fig.savefig(RES / name, dpi=180, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    return name


def figS1():
    full = pd.read_csv(RES / "rigor_gene_term_hits.csv")
    hub = json.loads((RES / "rigor_enrichment_hubfilter.json").read_text())
    top = full.head(15)
    tab = top if "CD36" in set(top["gene"]) else pd.concat(
        [top, full[full.gene == "CD36"]])
    fig, ax = plt.subplots(figsize=(7, 5.2), facecolor=SURFACE)
    _style(ax, xg=True, yg=False)
    t = tab.iloc[::-1]
    cols = [RED if g == "CD36" else (HL if p > 25 else NEUTRAL)
            for g, p in zip(t["gene"], t["pct_terms"])]
    ax.barh(range(len(t)), t["pct_terms"], color=cols, height=0.7)
    ax.set_yticks(range(len(t)), t["gene"], fontsize=8.5)
    for lbl in ax.get_yticklabels():
        if lbl.get_text() == "CD36":
            lbl.set_fontweight("bold")
    ax.axvline(25, color=INK2, ls="--", lw=1)
    ax.text(25.5, 0.5, "pan-target cutoff 25%", fontsize=8, color=INK2)
    ax.set_xlabel(f"% of {hub['n_sig_kegg_terms']} enriched KEGG terms the gene appears in",
                  color=INK2, fontsize=9)
    ax.set_title(f"Fig S1  Enrichment breadth is driven by signalling hubs;\n"
                 f"CD36 is pathway-specific ({hub['cd36_pct_terms']}%, red)",
                 fontsize=11, color=INK, pad=8)
    return _save(fig, "figS1_pantarget.png")


def figS2():
    ml = json.loads((RES / "rigor_ml.json").read_text())
    bench = pd.read_csv(RES / "s06_algorithm_benchmark.csv")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6), facecolor=SURFACE)

    # A: internal CV vs external AUC per algorithm (uncorrelated)
    _style(ax1)
    cv = bench["cv_auc"].to_numpy()
    ext = bench[["auc_GSE28829", "auc_GSE43292"]].mean(axis=1).to_numpy()
    ax1.scatter(cv, ext, s=45, color=BLUE, lw=0)
    for x, y, n in zip(cv, ext, bench["algorithm"]):
        ax1.annotate(n, (x, y), fontsize=6.5, color=INK2,
                     xytext=(3, 2), textcoords="offset points")
    from scipy.stats import spearmanr
    rho, p = spearmanr(cv, ext)
    ax1.set_xlabel("internal 10-fold CV AUC (leaked)", color=INK2, fontsize=9)
    ax1.set_ylabel("mean external-validation AUC", color=INK2, fontsize=9)
    ax1.set_title(f"A  CV AUC does not predict generalization\n"
                  f"(Spearman rho={rho:.2f}, P={p:.2f})", fontsize=10.5,
                  color=INK, pad=6)

    # B: permutation null for external AUC
    _style(ax2)
    perm = ml["external_auc_permutation"]
    null = np.array(perm.get("null_values", []))
    ax2.hist(null, bins=25, color=NEUTRAL, edgecolor=SURFACE)
    ax2.axvline(perm["real_mean_external_auc"], color=RED, lw=2,
                label=f"observed {perm['real_mean_external_auc']}")
    ax2.axvline(perm["null_95pct"], color=INK2, ls="--", lw=1,
                label=f"null 95% {perm['null_95pct']}")
    ax2.set_xlabel("mean external AUC under label permutation", color=INK2,
                   fontsize=9)
    ax2.set_ylabel("permutations", color=INK2, fontsize=9)
    ax2.legend(frameon=False, fontsize=8, labelcolor=INK2)
    ax2.set_title(f"B  External signal is real but modest\n"
                  f"(permutation P={perm['empirical_p']}, n={perm['n_permutations']})",
                  fontsize=10.5, color=INK, pad=6)
    fig.tight_layout()
    return _save(fig, "figS2_ml_honest.png")


def figS3():
    r = json.loads((RES / "rigor_singlecell.json").read_text())
    pp = pd.read_csv(RES / "rigor_per_patient.csv")
    fig, axs = plt.subplot_mosaic([["A", "B"], ["C", "D"]],
                                  figsize=(11, 8), facecolor=SURFACE)
    pats = ["P1", "P2", "P3"]

    def paired_panel(ax, metric, title, letter):
        _style(ax)
        for i, p in enumerate(pats):
            h = pp[(pp.patient == p) & (pp.cond == "HEA")][metric].iloc[0]
            d = pp[(pp.patient == p) & (pp.cond == "DIS")][metric].iloc[0]
            col = BLUE if d > h else RED
            ax.plot([0, 1], [h, d], "-o", color=col, ms=6, lw=1.6)
            ax.annotate(p, (1, d), fontsize=8, color=INK2,
                        xytext=(5, 0), textcoords="offset points")
        ax.set_xticks([0, 1], ["adjacent\n(HEA)", "core\n(DIS)"], fontsize=9)
        ax.set_xlim(-0.3, 1.4)
        ax.set_title(title, fontsize=10.5, color=INK, pad=6)
        _panel(ax, letter)

    paired_panel(axs["A"], "macro_prop",
                 f"A  Macrophage proportion (3/3 ↑, robust)", "A")
    paired_panel(axs["B"], "foam_prop",
                 f"B  Foam-like proportion (3/3 ↑, robust)", "B")
    paired_panel(axs["C"], "cd36_in_macro",
                 f"C  CD36 within macrophages (2/3, NOT robust)", "C")

    # D: composition decomposition bars
    ax = axs["D"]
    _style(ax, yg=True)
    comp = r["composition_decomposition"]
    labels = ["whole-tissue\nCD36", "within-macro\nCD36", "macrophage\nfraction"]
    vals = [comp["whole_tissue_fold_DIS_over_HEA"],
            comp["within_macrophage_fold_DIS_over_HEA"],
            comp["macrophage_prop_fold_DIS_over_HEA"]]
    cols = [RED, BLUE, "#eda100"]
    ax.bar(labels, vals, color=cols, width=0.6)
    ax.axhline(1, color=INK2, lw=1)
    for i, v in enumerate(vals):
        ax.text(i, v + 0.03, f"{v}×", ha="center", fontsize=9, color=INK)
    ax.set_ylabel("DIS / HEA fold", color=INK2, fontsize=9)
    ax.set_title("D  CD36 'increase' is a composition effect", fontsize=10.5,
                 color=INK, pad=6)
    _panel(ax, "D")
    fig.suptitle("Fig S3  Pseudoreplication & composition controls (n=3 "
                 "patients; cell-level P-values not used)", fontsize=12,
                 color=INK, y=1.02)
    fig.tight_layout()
    return _save(fig, "figS3_pseudoreplication.png")


def _panel(ax, letter):
    ax.text(-0.02, 1.05, letter, transform=ax.transAxes, fontsize=13,
            fontweight="bold", color=INK, va="bottom", ha="right")


if __name__ == "__main__":
    for fn in (figS1, figS2, figS3):
        print("rendered", fn())
