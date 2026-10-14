"""Publication-style figures computed from pipeline results.

Renders the classic figure set of a network-toxicology / multi-omics paper
from the persisted stage outputs in ``data/results``:

1. three-set Venn of PAEs / disease / ferroptosis targets
2. volcano plot of the training-set differential expression
3. machine-learning algorithm benchmark (10-fold CV AUC)
4. immune infiltration dumbbell (EM vs Control) + key-gene correlation
5. key-gene expression across single-cell types (EMT axis highlighted)
6. docking affinity chart with the -5.0 kcal/mol threshold

Design notes (dataviz method): color is assigned by job — categorical
slots in fixed order for identity, a blue/red diverging pair + neutral
gray for polarity, a single blue ramp for magnitude; one axis per chart;
thin marks; selective direct labels; recessive grid; text in ink tokens,
never series hues. The palette below is the validated reference instance
(categorical trio and diverging pair pass the CVD/normal-vision gates on
the light surface; the aqua slot's sub-3:1 contrast is relieved by direct
region labels on the only figure that uses it).
"""

from __future__ import annotations

import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Circle

from .config import RunContext
from .utils.io import load_json

# validated reference palette (light mode)
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#e8e7e3"
NEUTRAL = "#c3c2b7"
CAT = ["#2a78d6", "#eb6834", "#1baf7a"]      # categorical slots 1-3
DIV_NEG, DIV_POS = "#2a78d6", "#e34948"      # diverging blue <-> red
SEQ = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab"]  # ordinal blue steps


def _style(ax, xgrid=False, ygrid=True):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=9)
    if ygrid:
        ax.grid(axis="y", color=GRID, linewidth=0.8)
    if xgrid:
        ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def _fig(w=6.4, h=4.4):
    fig, ax = plt.subplots(figsize=(w, h), facecolor=SURFACE)
    return fig, ax


def _save(fig, ctx, name):
    path = ctx.results / name
    fig.savefig(path, dpi=180, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)
    return name


# ------------------------------------------------------------- 1. venn ----
def venn_targets(ctx: RunContext) -> str:
    paes = set(load_json(ctx.raw / "paes_targets.json"))
    em = set(load_json(ctx.raw / "em_targets.json"))
    frg = set(load_json(ctx.raw / "frgs_ferrdb.json"))
    only = [len(paes - em - frg), len(em - paes - frg), len(frg - paes - em)]
    pair = [len((paes & em) - frg), len((paes & frg) - em),
            len((em & frg) - paes)]
    tri = len(paes & em & frg)

    fig, ax = _fig(6.0, 5.4)
    centers = [(-0.55, 0.32), (0.55, 0.32), (0.0, -0.63)]
    names = [f"PAEs targets\nn={len(paes)}", f"EM targets\nn={len(em)}",
             f"Ferroptosis genes\nn={len(frg)}"]
    for (cx, cy), color, label, la in zip(
            centers, CAT, names, [(-1.35, 1.25), (1.35, 1.25), (0, -1.95)]):
        ax.add_patch(Circle((cx, cy), 1.05, facecolor=color, alpha=0.18,
                            edgecolor=color, linewidth=2))
        ax.text(*la, label, ha="center", va="center", fontsize=10,
                color=INK, fontweight="bold")
    # region counts (direct labels — the relief for low-contrast fills)
    for (x, y), v in zip(
            [(-0.95, 0.5), (0.95, 0.5), (0.0, -1.05),       # exclusive
             (0.0, 0.62), (-0.62, -0.28), (0.62, -0.28),    # pairwise
             (0.0, 0.0)], only + pair + [tri]):              # triple
        ax.text(x, y, str(v), ha="center", va="center",
                fontsize=12 if v == tri else 10, color=INK,
                fontweight="bold" if v == tri else "normal")
    inter = sorted(paes & em & frg)
    ax.text(0, -2.35, "Intersection: " + ", ".join(inter[:8])
            + (" …" if len(inter) > 8 else ""),
            ha="center", fontsize=9, color=INK2)
    ax.set_xlim(-2.3, 2.3)
    ax.set_ylim(-2.6, 1.75)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Exposure / disease / ferroptosis target intersection",
                 fontsize=12, color=INK, pad=10)
    return _save(fig, ctx, "fig1_venn_targets.png")


# ---------------------------------------------------------- 2. volcano ----
def volcano(ctx: RunContext) -> str:
    de = pd.read_csv(ctx.results / "s03_de_full.csv", index_col=0)
    cfg = ctx.cfg["diffexp"]
    lfc, pth = cfg["logfc_threshold"], cfg["pvalue_threshold"]
    x = de["logFC"]
    y = -np.log10(de["adj.P.Val"].clip(lower=1e-300))
    up = (de["adj.P.Val"] < pth) & (x > lfc)
    dn = (de["adj.P.Val"] < pth) & (x < -lfc)

    fig, ax = _fig(6.4, 5.0)
    _style(ax, xgrid=False, ygrid=True)
    ax.scatter(x[~(up | dn)], y[~(up | dn)], s=10, c=NEUTRAL, lw=0, alpha=0.7)
    ax.scatter(x[up], y[up], s=14, c=DIV_POS, lw=0, alpha=0.9,
               label=f"Up in EM ({int(up.sum())})")
    ax.scatter(x[dn], y[dn], s=14, c=DIV_NEG, lw=0, alpha=0.9,
               label=f"Down in EM ({int(dn.sum())})")
    ax.axvline(lfc, color=GRID, ls="--", lw=1)
    ax.axvline(-lfc, color=GRID, ls="--", lw=1)
    ax.axhline(-np.log10(pth), color=GRID, ls="--", lw=1)
    hub = load_json(ctx.processed / "hub_genes.json") or []
    marks = [g for g in ["ARF6", "GPX4", "ACSL4", "SLC7A11", "PTGS2"]
             if g in de.index][:5]
    for g in dict.fromkeys((hub[:1] + marks)):
        ax.annotate(g, (x[g], y[g]), xytext=(6, 5),
                    textcoords="offset points", fontsize=9, color=INK,
                    fontweight="bold" if g in hub else "normal")
    ax.set_xlabel("log2 fold change (EM vs Control)", color=INK2, fontsize=10)
    ax.set_ylabel("-log10 adjusted P", color=INK2, fontsize=10)
    ax.legend(frameon=False, fontsize=9, labelcolor=INK2)
    ax.set_title("Differential expression — training set", fontsize=12,
                 color=INK, pad=10)
    return _save(fig, ctx, "fig2_volcano.png")


# --------------------------------------------------- 3. ML benchmark ----
def ml_benchmark(ctx: RunContext) -> str:
    bench = pd.read_csv(ctx.results / "s06_algorithm_benchmark.csv")
    s6 = load_json(ctx.results / "s06_ml.json")
    finals = set(ctx.cfg["machine_learning"]["final_selectors"])
    bench = bench.sort_values("cv_auc")

    fig, ax = _fig(6.4, 4.8)
    _style(ax, xgrid=True, ygrid=False)
    colors = [SEQ[3] if a in finals else SEQ[1] for a in bench["algorithm"]]
    bars = ax.barh(bench["algorithm"], bench["cv_auc"], height=0.62,
                   color=colors)
    for b, v in zip(bars, bench["cv_auc"]):
        ax.text(v - 0.012, b.get_y() + b.get_height() / 2, f"{v:.2f}",
                ha="right", va="center", fontsize=8, color=SURFACE)
    ax.set_xlim(0.5, 1.0)
    ax.set_xlabel("10-fold CV AUC (training set)", color=INK2, fontsize=10)
    ax.set_title(
        f"Algorithm benchmark — final selectors (dark) agree on "
        f"{s6.get('key_gene', '?')}", fontsize=11, color=INK, pad=10)
    for lbl in ax.get_yticklabels():
        if lbl.get_text() in finals:
            lbl.set_fontweight("bold")
    return _save(fig, ctx, "fig3_ml_benchmark.png")


# ------------------------------------------- 4. immune infiltration ----
def immune(ctx: RunContext) -> str:
    tests = pd.read_csv(ctx.results / "s07_immune_tests.csv")
    key = load_json(ctx.results / "s07_immune.json").get("key_gene", "gene")
    top = tests.nsmallest(8, "wilcoxon_p").iloc[::-1]

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(9.6, 4.6), facecolor=SURFACE,
        gridspec_kw={"width_ratios": [1.35, 1]})
    _style(ax1, xgrid=True, ygrid=False)
    ypos = np.arange(len(top))
    for y0, a, b in zip(ypos, top["median_Control"], top["median_EM"]):
        ax1.plot([a, b], [y0, y0], color=GRID, lw=1.6, zorder=1)
    ax1.scatter(top["median_Control"], ypos, s=52, color=CAT[1], zorder=2,
                label="Control")
    ax1.scatter(top["median_EM"], ypos, s=52, color=CAT[0], zorder=2,
                label="EM")
    ax1.set_yticks(ypos)
    labels = [f"{ct} *" if p < 0.05 else ct
              for ct, p in zip(top["cell_type"], top["wilcoxon_p_adj"])]
    ax1.set_yticklabels(labels, fontsize=9)
    ax1.set_xlabel("ssGSEA score (median)", color=INK2, fontsize=10)
    ax1.legend(frameon=False, fontsize=9, labelcolor=INK2, loc="lower right")
    ax1.set_title("Immune cell infiltration (top 8, * adj P<0.05)",
                  fontsize=11, color=INK, pad=8)

    if "rho_key_gene" in tests:
        cor = tests.dropna(subset=["rho_key_gene"]).copy()
        cor = cor.reindex(cor["rho_key_gene"].abs().sort_values().index).tail(10)
        _style(ax2, xgrid=True, ygrid=False)
        y2 = np.arange(len(cor))
        colors = [DIV_POS if r > 0 else DIV_NEG for r in cor["rho_key_gene"]]
        ax2.hlines(y2, 0, cor["rho_key_gene"], color=colors, lw=2)
        ax2.scatter(cor["rho_key_gene"], y2, s=40, c=colors, zorder=2)
        ax2.axvline(0, color=GRID, lw=1)
        ax2.set_yticks(y2)
        ax2.set_yticklabels(
            [f"{ct} *" if p < 0.05 else ct
             for ct, p in zip(cor["cell_type"], cor["rho_p"])], fontsize=9)
        ax2.set_xlabel(f"Spearman rho with {key}", color=INK2, fontsize=10)
        ax2.set_title(f"{key} vs immune scores (* P<0.05)", fontsize=11,
                      color=INK, pad=8)
    fig.tight_layout()
    return _save(fig, ctx, "fig4_immune.png")


# ----------------------------------------- 5. single-cell key gene ----
def singlecell(ctx: RunContext) -> str:
    s8 = load_json(ctx.results / "s08_singlecell.json")
    key = s8.get("key_gene", "gene")
    means = s8.get("key_gene_mean_by_type", {})
    if not means:
        return ""
    axis_types = {"Lumenal", "Ciliated", "Fibroblasts"}
    items = sorted(means.items(), key=lambda kv: kv[1])

    fig, ax = _fig(6.4, 4.4)
    _style(ax, xgrid=True, ygrid=False)
    names = [k for k, _ in items]
    vals = [v for _, v in items]
    colors = [SEQ[3] if n in axis_types else SEQ[1] for n in names]
    bars = ax.barh(names, vals, height=0.62, color=colors)
    for b, v, n in zip(bars, vals, names):
        if n in axis_types:
            ax.text(v + 0.06, b.get_y() + b.get_height() / 2, f"{v:.2f}",
                    va="center", fontsize=8.5, color=INK)
    for lbl in ax.get_yticklabels():
        if lbl.get_text() in axis_types:
            lbl.set_fontweight("bold")
    rho = s8.get("key_gene_rho_pseudotime")
    p_axis = s8.get("key_gene_axis_enrichment_p")
    ax.set_xlabel(f"mean {key} (log-normalized)", color=INK2, fontsize=10)
    ax.set_title(
        f"{key} across cell types — EMT axis (bold) enriched, "
        f"P={p_axis:.1e}" if p_axis is not None else f"{key} by cell type",
        fontsize=11, color=INK, pad=10)
    return _save(fig, ctx, "fig5_singlecell.png")


# ------------------------------------------------------- 6. docking ----
def docking(ctx: RunContext) -> str:
    df = pd.read_csv(ctx.results / "s11_docking_affinities.csv")
    df = df.dropna(subset=["best_affinity"]).sort_values(
        "best_affinity", ascending=False)
    thr = ctx.cfg["docking"]["affinity_threshold_kcal_mol"]
    pdb = ctx.cfg["docking"]["receptor_pdb"]

    fig, ax = _fig(6.4, 4.2)
    _style(ax, xgrid=True, ygrid=False)
    bars = ax.barh(df["compound"], df["best_affinity"].abs(), height=0.62,
                   color=SEQ[2])
    for b, v in zip(bars, df["best_affinity"]):
        ax.text(abs(v) - 0.08, b.get_y() + b.get_height() / 2, f"{v:.1f}",
                ha="right", va="center", fontsize=8.5, color=SURFACE)
    ax.axvline(abs(thr), color=INK2, ls="--", lw=1.2)
    ax.text(abs(thr) + 0.04, len(df) - 0.4,
            f"strong-affinity threshold ({thr} kcal/mol)", fontsize=8.5,
            color=INK2)
    ax.set_xlabel("|binding energy| kcal/mol (AutoDock Vina, best pose)",
                  color=INK2, fontsize=10)
    ax.set_title(f"PAEs docking against {pdb}", fontsize=12, color=INK,
                 pad=10)
    return _save(fig, ctx, "fig6_docking.png")


RENDERERS = [venn_targets, volcano, ml_benchmark, immune, singlecell, docking]


def render_all(ctx: RunContext) -> list[str]:
    out = []
    for fn in RENDERERS:
        try:
            name = fn(ctx)
            if name:
                out.append(name)
        except FileNotFoundError as exc:
            print(f"[figures] skip {fn.__name__}: missing input {exc}")
    (ctx.results / "figures_manifest.json").write_text(
        json.dumps(out, indent=2))
    return out
