"""Paper-style figure suite computed from pipeline results.

Mirrors the computational figures of Wang et al. 2026 (J Hazard Mater
507:141670), figure-for-figure where the python-lite pipeline has the
numbers (wet-lab IHC/IF photographs and 3D docking poses excepted — the
latter come from the real Vina/PyMOL run via the generated protocol):

* fig01 workflow           — 12-stage pipeline diagram            (их Fig 1)
* fig02 targets & DE       — 2-set Venn, volcano, WGCNA module–trait
                             heatmap, 3-set Venn                  (Fig 2A-F)
* fig03 intersection genes — correlation dot-heatmap, GO dotplot,
                             KEGG bars                            (Fig 2H-J)
* fig04 ML benchmark       — algorithm x dataset AUC heatmap,
                             3-selector Venn                      (Fig 3A,E)
* fig05 ML models          — Lasso paths + CV curve, RF OOB error +
                             importance, XGBoost importance       (Fig 3B-D)
* fig06 immune             — infiltration dumbbell + key-gene
                             correlation lollipops                (Fig S2 / 2)
* fig07 single cell        — embedding, key-gene map, marker dotplot,
                             proportions by group, violin         (Fig 4-5)
* fig08 stemness & traj.   — stemness by subtype, key-gene vs
                             stemness, pseudotime trajectory, EMT
                             marker trends, key-gene vs CDH2/SNAI1 (Fig 5,7)
* fig09 spatial            — dominant-type map, gene feature maps,
                             lesion boxplot                       (Fig 8)
* fig10 virtual knockout   — perturbation lollipop + ORA dotplot  (Fig 9A)
* fig11 docking            — binding-energy chart                 (Fig 9I)

Design system: validated reference palette; color by job (categorical
identity in fixed slot order, sequential blue for magnitude, blue/red
diverging for polarity); one axis per panel; direct labels where fills
run light; text in ink tokens.
"""

from __future__ import annotations

import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyArrow, FancyBboxPatch
from scipy import stats as sps

from .config import RunContext
from .utils.io import load_json

# ----------------------------------------------------------------- theme --
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#e8e7e3"
NEUTRAL = "#c3c2b7"
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
       "#e87ba4", "#008300", "#6250d6", "#e34948"]   # fixed slot order
DIV_NEG, DIV_POS = "#2a78d6", "#e34948"
SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5",
       "#2a78d6", "#1c5cab", "#104281"]              # sequential blue ramp
SEQ_CMAP = matplotlib.colors.LinearSegmentedColormap.from_list(
    "seqblue", SEQ)
DIV_CMAP = matplotlib.colors.LinearSegmentedColormap.from_list(
    "divbr", [DIV_NEG, "#f0efec", DIV_POS])


def _style(ax, xgrid=False, ygrid=True):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=8.5)
    if ygrid:
        ax.grid(axis="y", color=GRID, linewidth=0.8)
    if xgrid:
        ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def _panel(ax, letter):
    ax.text(-0.02, 1.06, letter, transform=ax.transAxes, fontsize=14,
            fontweight="bold", color=INK, va="bottom", ha="right")


def _save(fig, ctx, name):
    fig.savefig(ctx.results / name, dpi=170, bbox_inches="tight",
                facecolor=SURFACE)
    plt.close(fig)
    return name


def _bare(ax):
    ax.set_facecolor(SURFACE)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def _venn2(ax, a: set, b: set, labels, colors=(CAT[0], CAT[1])):
    for (cx, c, lab, la) in [(-0.55, colors[0], labels[0], (-1.15, 1.25)),
                             (0.55, colors[1], labels[1], (1.15, 1.25))]:
        ax.add_patch(Circle((cx, 0), 1.0, facecolor=c, alpha=0.18,
                            edgecolor=c, linewidth=2))
        ax.text(*la, lab, ha="center", fontsize=9, color=INK,
                fontweight="bold")
    for x, v in [(-1.0, len(a - b)), (1.0, len(b - a)), (0, len(a & b))]:
        ax.text(x, 0, str(v), ha="center", va="center", fontsize=11,
                color=INK, fontweight="bold" if x == 0 else "normal")
    ax.set_xlim(-1.9, 1.9)
    ax.set_ylim(-1.35, 1.6)
    ax.set_aspect("equal")
    ax.axis("off")


def _venn3(ax, sets, labels, colors=CAT[:3], show_center_genes=False):
    a, b, c = sets
    centers = [(-0.55, 0.32), (0.55, 0.32), (0.0, -0.63)]
    lab_pos = [(-1.35, 1.3), (1.35, 1.3), (0, -1.95)]
    for (cx, cy), col, lab, la in zip(centers, colors, labels, lab_pos):
        ax.add_patch(Circle((cx, cy), 1.05, facecolor=col, alpha=0.18,
                            edgecolor=col, linewidth=2))
        ax.text(*la, lab, ha="center", va="center", fontsize=9,
                color=INK, fontweight="bold")
    vals = [len(a - b - c), len(b - a - c), len(c - a - b),
            len((a & b) - c), len((a & c) - b), len((b & c) - a),
            len(a & b & c)]
    pos = [(-0.95, 0.5), (0.95, 0.5), (0.0, -1.05),
           (0.0, 0.62), (-0.62, -0.28), (0.62, -0.28), (0.0, 0.0)]
    for (x, y), v in zip(pos, vals):
        ax.text(x, y, str(v), ha="center", va="center",
                fontsize=11 if (x, y) == (0.0, 0.0) else 9, color=INK,
                fontweight="bold" if (x, y) == (0.0, 0.0) else "normal")
    if show_center_genes:
        inter = sorted(a & b & c)
        ax.text(0, -2.35, ", ".join(inter[:6])
                + (" …" if len(inter) > 6 else ""),
                ha="center", fontsize=8, color=INK2)
    ax.set_xlim(-2.3, 2.3)
    ax.set_ylim(-2.55, 1.8)
    ax.set_aspect("equal")
    ax.axis("off")


# =================================================== fig01: workflow ======
def workflow(ctx: RunContext) -> str:
    rows = [
        ("Data layer", ["GEO bulk RNA-seq\nGSE51981 / 7305 / 7846",
                        "Compound targets\nPubChem·ChEMBL·CTD",
                        "Disease targets\nGeneCards·TTD·OMIM",
                        "FerrDb FRGs\n+ scRNA / spatial"]),
        ("Discovery", ["Network toxicology\ntarget intersection",
                       "limma DE +\nWGCNA modules",
                       "GO / KEGG\nenrichment",
                       "12-algorithm ML\n→ key FRG"]),
        ("Mechanism", ["ssGSEA immune\ninfiltration",
                       "scRNA-seq: stemness\n+ pseudotime (EMT)",
                       "Spatial transcriptome\ndeconvolution",
                       "Virtual knockout\n(GRN perturbation)"]),
        ("Validation", ["Molecular docking\nPAEs vs key protein",
                        "Clinical IHC / IF\n(wet lab)",
                        "Report:\nPAEs→Ferroptosis→EMT→EM", ""]),
    ]
    fig, ax = plt.subplots(figsize=(10.5, 6.2), facecolor=SURFACE)
    _bare(ax)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 6.2)
    band_cols = [CAT[0], CAT[2], CAT[1], CAT[6]]
    for ri, (band, boxes) in enumerate(rows):
        y = 5.3 - ri * 1.5
        ax.text(0.15, y + 0.35, band, fontsize=10, fontweight="bold",
                color=band_cols[ri], rotation=0, va="center")
        for bi, text in enumerate(boxes):
            if not text:
                continue
            x = 1.7 + bi * 2.2
            ax.add_patch(FancyBboxPatch(
                (x, y - 0.1), 1.95, 0.95,
                boxstyle="round,pad=0.06,rounding_size=0.12",
                facecolor=band_cols[ri], alpha=0.10,
                edgecolor=band_cols[ri], linewidth=1.3))
            ax.text(x + 0.975, y + 0.375, text, ha="center", va="center",
                    fontsize=8.2, color=INK)
        if ri < 3:
            ax.add_patch(FancyArrow(5.25, y - 0.18, 0, -0.26, width=0.012,
                                    head_width=0.12, head_length=0.1,
                                    color=INK2))
    ax.set_title("PAEs → Ferroptosis → EMT → Endometriosis analysis "
                 "pipeline", fontsize=13, color=INK, pad=12)
    return _save(fig, ctx, "fig01_workflow.png")


# ====================================== fig02: targets + DE + WGCNA ======
def targets_de(ctx: RunContext) -> str:
    paes = set(load_json(ctx.raw / "paes_targets.json"))
    em = set(load_json(ctx.raw / "em_targets.json"))
    frg = set(load_json(ctx.raw / "frgs_ferrdb.json"))
    de = pd.read_csv(ctx.results / "s03_de_full.csv", index_col=0)
    mt = pd.read_csv(ctx.results / "s04_module_trait.csv")
    cfg = ctx.cfg["diffexp"]
    lfc, pth = cfg["logfc_threshold"], cfg["pvalue_threshold"]

    fig, axs = plt.subplot_mosaic(
        [["A", "B"], ["C", "D"]], figsize=(11, 9), facecolor=SURFACE)

    # A: 2-set Venn exposure vs disease targets
    _venn2(axs["A"], paes, em, [f"PAEs targets\nn={len(paes)}",
                                f"EM targets\nn={len(em)}"])
    axs["A"].set_title("Exposure ∩ disease targets", fontsize=11,
                       color=INK, pad=6)
    _panel(axs["A"], "A")

    # B: volcano
    ax = axs["B"]
    _style(ax)
    x = de["logFC"]
    y = -np.log10(de["adj.P.Val"].clip(lower=1e-300))
    up = (de["adj.P.Val"] < pth) & (x > lfc)
    dn = (de["adj.P.Val"] < pth) & (x < -lfc)
    ax.scatter(x[~(up | dn)], y[~(up | dn)], s=9, c=NEUTRAL, lw=0, alpha=0.7)
    ax.scatter(x[up], y[up], s=13, c=DIV_POS, lw=0, alpha=0.9,
               label=f"Up ({int(up.sum())})")
    ax.scatter(x[dn], y[dn], s=13, c=DIV_NEG, lw=0, alpha=0.9,
               label=f"Down ({int(dn.sum())})")
    for v in (lfc, -lfc):
        ax.axvline(v, color=GRID, ls="--", lw=1)
    ax.axhline(-np.log10(pth), color=GRID, ls="--", lw=1)
    hub = load_json(ctx.processed / "hub_genes.json") or []
    offsets = [(6, 5), (6, -13), (-38, 7), (8, 14)]
    for i, g in enumerate(dict.fromkeys(
            hub[:1] + ["GPX4", "ACSL4", "SLC7A11"])):
        if g in de.index:
            ax.annotate(g, (x[g], y[g]), xytext=offsets[i % len(offsets)],
                        textcoords="offset points", fontsize=8.5, color=INK,
                        fontweight="bold" if g in hub else "normal")
    ax.set_xlabel("log2 fold change (EM vs Control)", color=INK2, fontsize=9)
    ax.set_ylabel("-log10 adjusted P", color=INK2, fontsize=9)
    ax.legend(frameon=False, fontsize=8.5, labelcolor=INK2)
    ax.set_title("Differential expression (training set)", fontsize=11,
                 color=INK, pad=6)
    _panel(ax, "B")

    # C: WGCNA module-trait heatmap
    ax = axs["C"]
    ax.set_facecolor(SURFACE)
    mods = mt.sort_values("trait_cor", ascending=False)
    mat = np.column_stack([mods["trait_cor"], -mods["trait_cor"]])
    im = ax.imshow(mat, cmap=DIV_CMAP, vmin=-1, vmax=1, aspect="auto")
    ax.set_xticks([0, 1], ["EM", "Control"], fontsize=9, color=INK2)
    ax.set_yticks(range(len(mods)),
                  [f"M{int(m)} (n={int(n)})" for m, n in
                   zip(mods["module"], mods["n_genes"])],
                  fontsize=9, color=INK2)
    for i in range(len(mods)):
        for j in range(2):
            r = mat[i, j]
            p = mods["trait_p"].iloc[i]
            ax.text(j, i, f"{r:.2f}\n({p:.1e})", ha="center", va="center",
                    fontsize=8, color=INK if abs(r) < 0.6 else SURFACE)
    fig.colorbar(im, ax=ax, shrink=0.75, label="module–trait correlation")
    ax.set_title("WGCNA module–trait relationships", fontsize=11,
                 color=INK, pad=6)
    for s in ax.spines.values():
        s.set_visible(False)
    _panel(ax, "C")

    # D: 3-set Venn
    _venn3(axs["D"], (paes, em, frg),
           [f"PAEs\nn={len(paes)}", f"EM\nn={len(em)}",
            f"FRGs\nn={len(frg)}"], show_center_genes=True)
    axs["D"].set_title("PAEs ∩ EM ∩ ferroptosis genes", fontsize=11,
                       color=INK, pad=6)
    _panel(axs["D"], "D")
    fig.tight_layout()
    return _save(fig, ctx, "fig02_targets_de.png")


# ================================= fig03: intersection-gene analyses =====
def intersection_genes(ctx: RunContext) -> str:
    inter = load_json(ctx.processed / "intersection_genes.json")
    acc = ctx.cfg["datasets"]["training"][0]["accession"]
    expr = pd.read_csv(ctx.processed / f"{acc}_expr.csv", index_col=0)
    enr = pd.read_csv(ctx.results / "s05_enrichment.csv")

    fig, axs = plt.subplot_mosaic([["A", "B"], ["A", "C"]],
                                  figsize=(11.5, 7.5), facecolor=SURFACE,
                                  gridspec_kw={"width_ratios": [1, 1.25]})

    # A: correlation dot-heatmap among intersection genes
    ax = axs["A"]
    genes = [g for g in inter if g in expr.index]
    sub = expr.loc[genes].T
    n = len(genes)
    rho = np.ones((n, n))
    pmat = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            r, p = sps.spearmanr(sub.iloc[:, i], sub.iloc[:, j])
            rho[i, j] = rho[j, i] = r
            pmat[i, j] = pmat[j, i] = p
    ax.set_facecolor(SURFACE)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            r = rho[i, j]
            ax.scatter(j, n - 1 - i, s=60 + 540 * abs(r),
                       c=[DIV_CMAP((r + 1) / 2)], lw=0)
            if pmat[i, j] < 0.05:
                ax.text(j, n - 1 - i, "*", ha="center", va="center",
                        fontsize=9, color=SURFACE)
    ax.set_xticks(range(n), genes, rotation=45, ha="right", fontsize=9)
    ax.set_yticks(range(n), genes[::-1], fontsize=9)
    ax.set_xlim(-0.6, n - 0.4)
    ax.set_ylim(-0.6, n - 0.4)
    for s in ax.spines.values():
        s.set_color(GRID)
    ax.set_title("Intersection-gene co-expression\n(Spearman, * P<0.05)",
                 fontsize=11, color=INK, pad=6)
    sm = plt.cm.ScalarMappable(cmap=DIV_CMAP,
                               norm=plt.Normalize(-1, 1))
    fig.colorbar(sm, ax=ax, shrink=0.6, label="rho")
    _panel(ax, "A")

    # B: GO dotplot
    go = enr[enr["term"].str.startswith("GO")].nsmallest(10, "pvalue")
    ax = axs["B"]
    _style(ax, xgrid=True, ygrid=False)
    terms = [t.split("::", 1)[1][:42] for t in go["term"]][::-1]
    gr = go["gene_ratio"].to_numpy()[::-1]
    cnt = go["overlap"].to_numpy()[::-1]
    logp = -np.log10(go["pvalue"].to_numpy())[::-1]
    sc = ax.scatter(logp, range(len(go)), s=40 + 60 * cnt,
                    c=gr, cmap=SEQ_CMAP, lw=0,
                    vmin=0, vmax=max(gr.max(), 0.5))
    ax.set_yticks(range(len(go)), terms, fontsize=8.5)
    ax.set_ylim(-0.6, len(go) - 0.4)
    ax.set_xlabel("-log10 P (size = gene count)", color=INK2, fontsize=9)
    fig.colorbar(sc, ax=ax, shrink=0.8, label="gene ratio")
    ax.set_title("GO enrichment", fontsize=11, color=INK, pad=6)
    _panel(ax, "B")

    # C: KEGG bars
    kegg = enr[enr["term"].str.startswith("KEGG")].nsmallest(8, "pvalue")
    ax = axs["C"]
    _style(ax, xgrid=True, ygrid=False)
    if not kegg.empty:
        terms = [t.split("::", 1)[1][:42] for t in kegg["term"]][::-1]
        logp = -np.log10(kegg["pvalue"].to_numpy())[::-1]
        bars = ax.barh(range(len(kegg)), logp, height=0.5, color=SEQ[4])
        ax.set_yticks(range(len(kegg)), terms, fontsize=8.5)
        ax.set_ylim(-0.8, len(kegg) - 0.2)
        for b, k in zip(bars, kegg["overlap"].to_numpy()[::-1]):
            ax.text(b.get_width() - 0.05, b.get_y() + b.get_height() / 2,
                    f"n={k}", ha="right", va="center", fontsize=8,
                    color=SURFACE)
        ax.set_xlabel("-log10 P", color=INK2, fontsize=9)
    ax.set_title("KEGG enrichment", fontsize=11, color=INK, pad=6)
    _panel(ax, "C")
    fig.tight_layout()
    return _save(fig, ctx, "fig03_intersection_genes.png")


# ========================================== fig04: ML benchmark ==========
def ml_benchmark(ctx: RunContext) -> str:
    bench = pd.read_csv(ctx.results / "s06_algorithm_benchmark.csv")
    s6 = load_json(ctx.results / "s06_ml.json")
    finals = ctx.cfg["machine_learning"]["final_selectors"]
    auc_cols = [c for c in bench.columns if c != "algorithm"]
    bench["mean"] = bench[auc_cols].mean(axis=1)
    bench = bench.sort_values("mean", ascending=True)

    fig, axs = plt.subplot_mosaic([["A", "B"]], figsize=(11.5, 5),
                                  facecolor=SURFACE,
                                  gridspec_kw={"width_ratios": [1.35, 1]})
    # A: heatmap of AUC across datasets + mean bar
    ax = axs["A"]
    ax.set_facecolor(SURFACE)
    cols = auc_cols + ["mean"]
    labels = [c.replace("auc_", "").replace("cv_auc", "train CV")
              for c in cols]
    mat = bench[cols].to_numpy(float)
    im = ax.imshow(mat, cmap=SEQ_CMAP, vmin=0.5, vmax=1.0, aspect="auto")
    ax.set_xticks(range(len(cols)), labels, fontsize=9, color=INK2)
    ax.set_yticks(range(len(bench)), bench["algorithm"], fontsize=9,
                  color=INK2)
    for lbl in ax.get_yticklabels():
        if lbl.get_text() in finals:
            lbl.set_fontweight("bold")
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            ax.text(j, i, f"{mat[i, j]:.2f}", ha="center", va="center",
                    fontsize=8, color=SURFACE if mat[i, j] > 0.78 else INK)
    fig.colorbar(im, ax=ax, shrink=0.8, label="AUC")
    ax.set_title("Algorithm benchmark across datasets (10-fold CV + "
                 "external validation)", fontsize=11, color=INK, pad=8)
    for s in ax.spines.values():
        s.set_visible(False)
    _panel(ax, "A")

    # B: 3-selector Venn
    ranks = s6.get("selector_rankings", {})
    sets = [set(ranks.get(f, [])) for f in finals]
    _venn3(axs["B"], tuple(sets),
           [f"{f}\n(top {len(s)})" for f, s in zip(finals, sets)],
           colors=[CAT[0], CAT[1], CAT[2]], show_center_genes=True)
    key = s6.get("key_gene")
    axs["B"].set_title(f"Selector consensus → key gene: {key}",
                       fontsize=11, color=INK, pad=6)
    _panel(axs["B"], "B")
    fig.tight_layout()
    return _save(fig, ctx, "fig04_ml_benchmark.png")


# ============================================= fig05: ML models ==========
def ml_models(ctx: RunContext) -> str:
    from sklearn.ensemble import GradientBoostingClassifier, \
        RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import log_loss
    from sklearn.model_selection import StratifiedKFold
    from sklearn.preprocessing import StandardScaler

    s6 = load_json(ctx.results / "s06_ml.json")
    feats = s6.get("candidate_genes") or s6.get("hub_genes", [])
    acc = ctx.cfg["datasets"]["training"][0]["accession"]
    expr = pd.read_csv(ctx.processed / f"{acc}_expr.csv", index_col=0)
    groups = pd.read_csv(ctx.processed / f"{acc}_groups.csv",
                         index_col=0)["group"]
    feats = [f for f in feats if f in expr.index]
    x = StandardScaler().fit_transform(expr.loc[feats].T.to_numpy())
    y = (groups == "EM").astype(int).to_numpy()
    seed = ctx.seed
    key = s6.get("key_gene")

    fig, axs = plt.subplot_mosaic([["A", "B", "C"], ["D", "D", "E"]],
                                  figsize=(12.5, 8), facecolor=SURFACE)

    # A: Lasso coefficient paths over log(C)
    cs = np.logspace(-2.2, 1.2, 30)
    paths = []
    for c in cs:
        m = LogisticRegression(solver="liblinear", l1_ratio=1.0, C=c,
                               random_state=seed).fit(x, y)
        paths.append(m.coef_.ravel())
    paths = np.array(paths)
    ax = axs["A"]
    _style(ax)
    for fi, f in enumerate(feats):
        is_key = f == key
        ax.plot(np.log10(cs), paths[:, fi],
                color=SEQ[5] if is_key else NEUTRAL,
                lw=2.2 if is_key else 1.2, zorder=3 if is_key else 2)
        if is_key:
            ax.annotate(f, (np.log10(cs)[-1], paths[-1, fi]),
                        xytext=(-4, 6), textcoords="offset points",
                        fontsize=9, color=INK, fontweight="bold",
                        ha="right")
    ax.set_xlabel("log10 C (inverse regularization)", color=INK2, fontsize=9)
    ax.set_ylabel("Lasso coefficient", color=INK2, fontsize=9)
    ax.set_title("Lasso coefficient paths", fontsize=11, color=INK, pad=6)
    _panel(ax, "A")

    # B: Lasso CV deviance curve
    cv = StratifiedKFold(5, shuffle=True, random_state=seed)
    mean_dev, sd_dev = [], []
    for c in cs:
        devs = []
        for tr, te in cv.split(x, y):
            m = LogisticRegression(solver="liblinear", l1_ratio=1.0, C=c,
                                   random_state=seed).fit(x[tr], y[tr])
            devs.append(2 * log_loss(y[te], m.predict_proba(x[te])[:, 1]))
        mean_dev.append(np.mean(devs))
        sd_dev.append(np.std(devs) / np.sqrt(len(devs)))
    ax = axs["B"]
    _style(ax)
    ax.errorbar(np.log10(cs), mean_dev, yerr=sd_dev, fmt="o-", ms=3.5,
                color=SEQ[4], ecolor=NEUTRAL, lw=1.4, capsize=2)
    best = np.log10(cs)[int(np.argmin(mean_dev))]
    ax.axvline(best, color=GRID, ls="--", lw=1.2)
    ax.text(best, max(mean_dev), " min deviance", fontsize=8, color=INK2)
    ax.set_xlabel("log10 C", color=INK2, fontsize=9)
    ax.set_ylabel("CV binomial deviance", color=INK2, fontsize=9)
    ax.set_title("Lasso cross-validation", fontsize=11, color=INK, pad=6)
    _panel(ax, "B")

    # C: RF OOB error vs number of trees
    ax = axs["C"]
    _style(ax)
    errs, ns = [], range(10, 301, 10)
    rf = RandomForestClassifier(warm_start=True, oob_score=True,
                                random_state=seed)
    for n in ns:
        rf.set_params(n_estimators=n)
        rf.fit(x, y)
        errs.append(1 - rf.oob_score_)
    ax.plot(list(ns), errs, color=SEQ[4], lw=1.6)
    ax.set_xlabel("number of trees", color=INK2, fontsize=9)
    ax.set_ylabel("OOB error", color=INK2, fontsize=9)
    ax.set_title("Random forest error", fontsize=11, color=INK, pad=6)
    _panel(ax, "C")

    # D: RF importance lollipop
    ax = axs["D"]
    _style(ax, xgrid=True, ygrid=False)
    imp = pd.Series(rf.feature_importances_, index=feats).sort_values()
    ypos = np.arange(len(imp))
    cols = [SEQ[5] if g == key else SEQ[2] for g in imp.index]
    ax.hlines(ypos, 0, imp.to_numpy(), color=cols, lw=2)
    ax.scatter(imp.to_numpy(), ypos, s=42, c=cols, zorder=2)
    ax.set_yticks(ypos, imp.index, fontsize=9)
    for lbl in ax.get_yticklabels():
        if lbl.get_text() == key:
            lbl.set_fontweight("bold")
    ax.set_xlabel("RF importance (impurity decrease)", color=INK2,
                  fontsize=9)
    ax.set_title("Random forest feature importance", fontsize=11,
                 color=INK, pad=6)
    _panel(ax, "D")

    # E: XGBoost(-fallback) importance
    try:
        from xgboost import XGBClassifier
        xgb = XGBClassifier(n_estimators=300, eval_metric="logloss",
                            random_state=seed).fit(x, y)
        label = "XGBoost gain importance"
    except ImportError:
        xgb = GradientBoostingClassifier(n_estimators=300,
                                         random_state=seed).fit(x, y)
        label = "Gradient-boosting importance (XGBoost fallback)"
    ax = axs["E"]
    _style(ax, xgrid=True, ygrid=False)
    imp = pd.Series(xgb.feature_importances_, index=feats).sort_values()
    cols = [SEQ[5] if g == key else SEQ[2] for g in imp.index]
    bars = ax.barh(imp.index, imp.to_numpy(), height=0.6, color=cols)
    ax.tick_params(axis="y", labelsize=9)
    for lbl in ax.get_yticklabels():
        if lbl.get_text() == key:
            lbl.set_fontweight("bold")
    ax.set_xlabel(label, color=INK2, fontsize=9)
    ax.set_title("Boosted-tree importance", fontsize=11, color=INK, pad=6)
    _panel(ax, "E")
    fig.tight_layout()
    return _save(fig, ctx, "fig05_ml_models.png")


# ================================================ fig06: immune ==========
def immune(ctx: RunContext) -> str:
    tests = pd.read_csv(ctx.results / "s07_immune_tests.csv")
    key = load_json(ctx.results / "s07_immune.json").get("key_gene", "gene")
    top = tests.nsmallest(8, "wilcoxon_p").iloc[::-1]

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(10, 4.6), facecolor=SURFACE,
        gridspec_kw={"width_ratios": [1.35, 1]})
    _style(ax1, xgrid=True, ygrid=False)
    ypos = np.arange(len(top))
    for y0, a, b in zip(ypos, top["median_Control"], top["median_EM"]):
        ax1.plot([a, b], [y0, y0], color=GRID, lw=1.6, zorder=1)
    ax1.scatter(top["median_Control"], ypos, s=50, color=CAT[1], zorder=2,
                label="Control")
    ax1.scatter(top["median_EM"], ypos, s=50, color=CAT[0], zorder=2,
                label="EM")
    ax1.set_yticks(ypos)
    ax1.set_yticklabels(
        [f"{ct} *" if p < 0.05 else ct
         for ct, p in zip(top["cell_type"], top["wilcoxon_p_adj"])],
        fontsize=9)
    ax1.set_xlabel("ssGSEA score (median)", color=INK2, fontsize=9)
    ax1.legend(frameon=False, fontsize=9, labelcolor=INK2,
               loc="lower right")
    ax1.set_title("Immune infiltration (top 8, * adj P<0.05)",
                  fontsize=11, color=INK, pad=8)
    _panel(ax1, "A")

    if "rho_key_gene" in tests:
        cor = tests.dropna(subset=["rho_key_gene"]).copy()
        cor = cor.reindex(
            cor["rho_key_gene"].abs().sort_values().index).tail(10)
        _style(ax2, xgrid=True, ygrid=False)
        y2 = np.arange(len(cor))
        colors = [DIV_POS if r > 0 else DIV_NEG
                  for r in cor["rho_key_gene"]]
        ax2.hlines(y2, 0, cor["rho_key_gene"], color=colors, lw=2)
        ax2.scatter(cor["rho_key_gene"], y2, s=38, c=colors, zorder=2)
        ax2.axvline(0, color=GRID, lw=1)
        ax2.set_yticks(y2)
        ax2.set_yticklabels(
            [f"{ct} *" if p < 0.05 else ct
             for ct, p in zip(cor["cell_type"], cor["rho_p"])], fontsize=9)
        ax2.set_xlabel(f"Spearman rho with {key}", color=INK2, fontsize=9)
        ax2.set_title(f"{key} vs immune scores (* P<0.05)", fontsize=11,
                      color=INK, pad=8)
        _panel(ax2, "B")
    fig.tight_layout()
    return _save(fig, ctx, "fig06_immune.png")


# =========================================== fig07: single cell ==========
def singlecell(ctx: RunContext) -> str:
    from sklearn.decomposition import PCA

    counts = pd.read_csv(ctx.raw / "sc_counts.csv", index_col=0)
    meta = pd.read_csv(ctx.results / "s08_cell_meta.csv")
    s8 = load_json(ctx.results / "s08_singlecell.json")
    key = s8.get("key_gene", "gene")
    markers = load_json(ctx.raw / "sc_marker_truth.json")
    counts = counts[meta["cell"]]
    norm = np.log1p(counts / counts.sum(axis=0).replace(0, 1) * 1e4)
    emb = PCA(n_components=2, random_state=ctx.seed).fit_transform(
        norm.T.to_numpy())
    types = sorted(meta["annotated"].unique())
    tcol = {t: CAT[i % len(CAT)] for i, t in enumerate(types)}

    fig, axs = plt.subplot_mosaic(
        [["A", "B", "C"], ["D", "E", "C"]], figsize=(13, 8),
        facecolor=SURFACE, gridspec_kw={"width_ratios": [1, 1, 1.15]})

    # A: embedding colored by annotated type, centroid direct labels
    ax = axs["A"]
    _style(ax, False, False)
    for t in types:
        m = (meta["annotated"] == t).to_numpy()
        ax.scatter(emb[m, 0], emb[m, 1], s=7, c=tcol[t], lw=0, alpha=0.75)
    for t in types:
        m = (meta["annotated"] == t).to_numpy()
        cx, cy = emb[m, 0].mean(), emb[m, 1].mean()
        ax.text(cx, cy, t, fontsize=8.5, color=INK, fontweight="bold",
                ha="center",
                bbox=dict(boxstyle="round,pad=0.15", fc=SURFACE,
                          ec=GRID, alpha=0.85))
    ax.set_xlabel("PC1", color=INK2, fontsize=9)
    ax.set_ylabel("PC2", color=INK2, fontsize=9)
    ax.set_title("Cell-type embedding", fontsize=11, color=INK, pad=6)
    _panel(ax, "A")

    # B: key gene on embedding (sequential)
    ax = axs["B"]
    _style(ax, False, False)
    kg = norm.loc[key].to_numpy()
    order = np.argsort(kg)
    sc = ax.scatter(emb[order, 0], emb[order, 1], s=7, c=kg[order],
                    cmap=SEQ_CMAP, lw=0)
    fig.colorbar(sc, ax=ax, shrink=0.75, label=f"{key} (log-norm)")
    ax.set_xlabel("PC1", color=INK2, fontsize=9)
    ax.set_ylabel("PC2", color=INK2, fontsize=9)
    ax.set_title(f"{key} expression", fontsize=11, color=INK, pad=6)
    _panel(ax, "B")

    # C: marker dotplot (top-2 truth markers per type)
    ax = axs["C"]
    ax.set_facecolor(SURFACE)
    mk = []
    for t in types:
        mk += [m for m in markers.get(t, [])[:2] if m in norm.index]
    mk = list(dict.fromkeys(mk))
    mean_mat = np.zeros((len(types), len(mk)))
    pct_mat = np.zeros_like(mean_mat)
    for ti, t in enumerate(types):
        cells = meta[meta["annotated"] == t]["cell"]
        sub = norm.loc[mk, cells]
        mean_mat[ti] = sub.mean(axis=1)
        pct_mat[ti] = (sub > 0).mean(axis=1)
    mz = (mean_mat - mean_mat.mean(0)) / (mean_mat.std(0) + 1e-9)
    for ti in range(len(types)):
        for mi in range(len(mk)):
            ax.scatter(mi, len(types) - 1 - ti,
                       s=10 + 140 * pct_mat[ti, mi],
                       c=[SEQ_CMAP((np.clip(mz[ti, mi], -2, 2) + 2) / 4)],
                       lw=0)
    ax.set_xticks(range(len(mk)), mk, rotation=60, ha="right", fontsize=8)
    ax.set_yticks(range(len(types)), types[::-1], fontsize=9)
    ax.set_xlim(-0.6, len(mk) - 0.4)
    for s in ax.spines.values():
        s.set_color(GRID)
    ax.set_title("Marker dotplot (size=pct expressed,\ncolor=scaled mean)",
                 fontsize=10.5, color=INK, pad=6)
    _panel(ax, "C")

    # D: cell-type proportions by group (stacked)
    ax = axs["D"]
    _style(ax, False, True)
    if "group" in meta:
        prop = (meta.groupby("group")["annotated"]
                .value_counts(normalize=True).unstack(fill_value=0))
        bottoms = np.zeros(len(prop))
        for t in types:
            vals = prop.get(t, pd.Series(0, index=prop.index)).to_numpy()
            ax.bar(prop.index, vals, bottom=bottoms, width=0.55,
                   color=tcol[t], label=t, edgecolor=SURFACE,
                   linewidth=1.5)
            bottoms += vals
        ax.set_ylabel("proportion", color=INK2, fontsize=9)
        ax.legend(frameon=False, fontsize=7.5, labelcolor=INK2,
                  loc="center left", bbox_to_anchor=(1.0, 0.5))
    ax.set_title("Cell composition by condition", fontsize=11, color=INK,
                 pad=6)
    _panel(ax, "D")

    # E: key-gene violin by type
    ax = axs["E"]
    _style(ax, False, True)
    axis_types = set(ctx.cfg["single_cell"].get("axis_types", ["Lumenal", "Ciliated", "Fibroblasts"]))
    data = [norm.loc[key, meta[meta["annotated"] == t]["cell"]].to_numpy()
            for t in types]
    vp = ax.violinplot(data, showmedians=True, widths=0.8)
    for body, t in zip(vp["bodies"], types):
        body.set_facecolor(SEQ[5] if t in axis_types else SEQ[2])
        body.set_alpha(0.75)
        body.set_edgecolor(INK2)
    for part in ("cmins", "cmaxes", "cbars", "cmedians"):
        vp[part].set_color(INK2)
        vp[part].set_linewidth(1)
    ax.set_xticks(range(1, len(types) + 1), types, rotation=40,
                  ha="right", fontsize=8.5)
    for lbl in ax.get_xticklabels():
        if lbl.get_text() in axis_types:
            lbl.set_fontweight("bold")
    ax.set_ylabel(f"{key} (log-norm)", color=INK2, fontsize=9)
    ax.set_title(f"{key} by cell type (EMT axis bold)", fontsize=11,
                 color=INK, pad=6)
    _panel(ax, "E")
    fig.tight_layout()
    return _save(fig, ctx, "fig07_singlecell.png")


# =================================== fig08: stemness + trajectory ========
def stemness_trajectory(ctx: RunContext) -> str:
    from sklearn.decomposition import PCA

    counts = pd.read_csv(ctx.raw / "sc_counts.csv", index_col=0)
    meta = pd.read_csv(ctx.results / "s08_cell_meta.csv")
    pt = pd.read_csv(ctx.results / "s08_pseudotime.csv", index_col=0)[
        "pseudotime"]
    s8 = load_json(ctx.results / "s08_singlecell.json")
    key = s8.get("key_gene", "gene")
    counts = counts[meta["cell"]]
    norm = np.log1p(counts / counts.sum(axis=0).replace(0, 1) * 1e4)
    axis_types = list(ctx.cfg["single_cell"].get("axis_types", ["Lumenal", "Ciliated", "Fibroblasts"]))
    meta_i = meta.set_index("cell")
    axis_cells = pt.index
    emb = PCA(n_components=2, random_state=ctx.seed).fit_transform(
        norm[axis_cells].T.to_numpy())

    fig, axs = plt.subplot_mosaic(
        [["A", "B", "C"], ["D", "E", "F"]], figsize=(13, 8),
        facecolor=SURFACE)

    # A: stemness by subtype (box)
    ax = axs["A"]
    _style(ax)
    types = sorted(meta["annotated"].unique())
    data = [meta[meta["annotated"] == t]["stemness"].to_numpy()
            for t in types]
    bp = ax.boxplot(data, patch_artist=True, widths=0.55,
                    medianprops=dict(color=INK2))
    for patch, t in zip(bp["boxes"], types):
        patch.set_facecolor(SEQ[5] if t in axis_types else SEQ[2])
        patch.set_alpha(0.8)
        patch.set_edgecolor(INK2)
    for el in ("whiskers", "caps"):
        for line in bp[el]:
            line.set_color(INK2)
    ax.set_xticks(range(1, len(types) + 1), types, rotation=40,
                  ha="right", fontsize=8.5)
    for lbl in ax.get_xticklabels():
        if lbl.get_text() in axis_types:
            lbl.set_fontweight("bold")
    ax.set_ylabel("stemness (CytoTRACE-style)", color=INK2, fontsize=9)
    ax.set_title("Differentiation potential by subtype", fontsize=11,
                 color=INK, pad=6)
    _panel(ax, "A")

    # B: key gene vs stemness (epithelial subtypes), fit line
    ax = axs["B"]
    _style(ax)
    epi_cells = meta[meta["annotated"].isin(["Lumenal", "Ciliated"])]["cell"]
    xg = norm.loc[key, epi_cells].to_numpy()
    yg = meta_i.loc[epi_cells, "stemness"].to_numpy()
    rho, pv = sps.spearmanr(xg, yg)
    ax.scatter(xg, yg, s=12, c=SEQ[3], lw=0, alpha=0.7)
    coef = np.polyfit(xg, yg, 1)
    xs = np.linspace(xg.min(), xg.max(), 50)
    ax.plot(xs, np.polyval(coef, xs), color=INK2, lw=1.6)
    ax.text(0.04, 0.93, f"R={rho:.2f}, P={pv:.1e}",
            transform=ax.transAxes, fontsize=9, color=INK)
    ax.set_xlabel(f"{key} (log-norm)", color=INK2, fontsize=9)
    ax.set_ylabel("stemness", color=INK2, fontsize=9)
    ax.set_title(f"{key} vs epithelial stemness", fontsize=11, color=INK,
                 pad=6)
    _panel(ax, "B")

    # C: trajectory embedding colored by pseudotime
    ax = axs["C"]
    _style(ax, False, False)
    sc = ax.scatter(emb[:, 0], emb[:, 1], s=9,
                    c=pt.loc[axis_cells].to_numpy(), cmap=SEQ_CMAP, lw=0)
    fig.colorbar(sc, ax=ax, shrink=0.75, label="pseudotime")
    ax.set_xlabel("component 1", color=INK2, fontsize=9)
    ax.set_ylabel("component 2", color=INK2, fontsize=9)
    ax.set_title("EMT trajectory (pseudotime)", fontsize=11, color=INK,
                 pad=6)
    _panel(ax, "C")

    # D: trajectory colored by subtype, centroid labels
    ax = axs["D"]
    _style(ax, False, False)
    for i, t in enumerate(axis_types):
        m = (meta_i.loc[axis_cells, "annotated"] == t).to_numpy()
        ax.scatter(emb[m, 0], emb[m, 1], s=9, c=CAT[i], lw=0, alpha=0.8)
        ax.text(emb[m, 0].mean(), emb[m, 1].mean(), t, fontsize=8.5,
                color=INK, fontweight="bold", ha="center",
                bbox=dict(boxstyle="round,pad=0.15", fc=SURFACE, ec=GRID,
                          alpha=0.85))
    ax.set_xlabel("component 1", color=INK2, fontsize=9)
    ax.set_ylabel("component 2", color=INK2, fontsize=9)
    ax.set_title(" + ".join(axis_types[:-1]) + " → " + axis_types[-1], fontsize=11,
                 color=INK, pad=6)
    _panel(ax, "D")

    # E: EMT marker trends along pseudotime
    ax = axs["E"]
    _style(ax)
    order = np.argsort(pt.loc[axis_cells].to_numpy())
    tvals = pt.loc[axis_cells].to_numpy()[order]
    for gi, g in enumerate([m for m in ("CDH1", "VIM", "SNAI1")
                            if m in norm.index]):
        vals = norm.loc[g, axis_cells].to_numpy()[order]
        smooth = pd.Series(vals).rolling(40, center=True,
                                         min_periods=10).mean()
        ax.plot(tvals, smooth, color=CAT[gi], lw=2, label=g)
    ax.legend(frameon=False, fontsize=8.5, labelcolor=INK2)
    ax.set_xlabel("pseudotime", color=INK2, fontsize=9)
    ax.set_ylabel("expression (smoothed)", color=INK2, fontsize=9)
    ax.set_title("EMT markers along pseudotime", fontsize=11, color=INK,
                 pad=6)
    _panel(ax, "E")

    # F: key gene vs CDH2 / SNAI1 in fibroblasts
    ax = axs["F"]
    _style(ax)
    fib_cells = meta[meta["annotated"] == "Fibroblasts"]["cell"]
    xg = norm.loc[key, fib_cells].to_numpy()
    txt = []
    for gi, g in enumerate([m for m in ("CDH2", "SNAI1")
                            if m in norm.index]):
        yg = norm.loc[g, fib_cells].to_numpy()
        rho, pv = sps.spearmanr(xg, yg)
        jitter = (np.random.default_rng(gi).uniform(-0.04, 0.04, xg.size))
        ax.scatter(xg + jitter, yg, s=11, c=CAT[gi], lw=0, alpha=0.6,
                   label=g)
        coef = np.polyfit(xg, yg, 1)
        xs = np.linspace(xg.min(), xg.max(), 50)
        ax.plot(xs, np.polyval(coef, xs), color=CAT[gi], lw=1.8)
        txt.append(f"{g}: R={rho:.2f}, P={pv:.1e}")
    ax.text(0.04, 0.95, "\n".join(txt), transform=ax.transAxes,
            fontsize=8.5, color=INK, va="top")
    ax.legend(frameon=False, fontsize=8.5, labelcolor=INK2,
              loc="lower right")
    ax.set_xlabel(f"{key} (log-norm)", color=INK2, fontsize=9)
    ax.set_ylabel("EMT marker expression", color=INK2, fontsize=9)
    ax.set_title(f"{key} vs EMT markers in fibroblasts", fontsize=11,
                 color=INK, pad=6)
    _panel(ax, "F")
    fig.tight_layout()
    return _save(fig, ctx, "fig08_stemness_trajectory.png")


# ================================================ fig09: spatial =========
def spatial(ctx: RunContext) -> str:
    if not (ctx.raw / "spatial_counts.csv").exists():
        return ""
    counts = pd.read_csv(ctx.raw / "spatial_counts.csv", index_col=0)
    coords = pd.read_csv(ctx.raw / "spatial_coords.csv")
    comp = pd.read_csv(ctx.results / "s09_deconvolution_proxy.csv",
                       index_col=0)
    s9 = load_json(ctx.results / "s09_spatial.json")
    key = s9.get("key_gene", "gene")
    norm = np.log1p(counts / counts.sum(axis=0).replace(0, 1) * 1e4)

    panelgenes = [g for g in (key, "VIM", "CDH1") if g in norm.index]
    mosaic = [["A"] + [f"G{i}" for i in range(len(panelgenes))] + ["E"]]
    fig, axs = plt.subplot_mosaic(
        mosaic, figsize=(3.2 * (len(panelgenes) + 2), 3.6),
        facecolor=SURFACE)

    # A: dominant cell type per spot
    ax = axs["A"]
    _style(ax, False, False)
    dom = comp.idxmax(axis=1).loc[coords["spot"]]
    types = sorted(dom.unique())
    for i, t in enumerate(types):
        m = (dom == t).to_numpy()
        ax.scatter(coords["x"][m], coords["y"][m], s=10,
                   c=CAT[i % len(CAT)], lw=0, alpha=0.85)
    # direct labels at densest region of each type (top 3 types only)
    for t in pd.Series(dom).value_counts().head(3).index:
        m = (dom == t).to_numpy()
        ax.text(coords["x"][m].median(), coords["y"][m].median(), t,
                fontsize=8, color=INK, fontweight="bold", ha="center",
                bbox=dict(boxstyle="round,pad=0.12", fc=SURFACE, ec=GRID,
                          alpha=0.85))
    ax.set_title("Dominant cell type (deconvolution)", fontsize=10,
                 color=INK, pad=6)
    ax.set_xticks([])
    ax.set_yticks([])
    _panel(ax, "A")

    # G*: spatial feature maps
    letters = "BCD"
    for i, g in enumerate(panelgenes):
        ax = axs[f"G{i}"]
        _style(ax, False, False)
        vals = norm.loc[g, coords["spot"]].to_numpy()
        sc = ax.scatter(coords["x"], coords["y"], c=vals, s=10,
                        cmap=SEQ_CMAP, lw=0)
        fig.colorbar(sc, ax=ax, shrink=0.8)
        ax.set_title(g, fontsize=10, color=INK, pad=6,
                     fontweight="bold" if g == key else "normal")
        ax.set_xticks([])
        ax.set_yticks([])
        _panel(ax, letters[i])

    # E: lesion vs non-lesion key gene box
    ax = axs["E"]
    _style(ax)
    lesion = coords.set_index("spot")["lesion"]
    kg = norm.loc[key]
    a = kg[lesion[lesion].index].to_numpy()
    b = kg[lesion[~lesion].index].to_numpy()
    bp = ax.boxplot([b, a], patch_artist=True, widths=0.5,
                    tick_labels=["non-lesion", "lesion"],
                    medianprops=dict(color=INK2))
    for patch, c in zip(bp["boxes"], [SEQ[2], SEQ[5]]):
        patch.set_facecolor(c)
        patch.set_alpha(0.85)
        patch.set_edgecolor(INK2)
    for el in ("whiskers", "caps"):
        for line in bp[el]:
            line.set_color(INK2)
    p = s9.get("lesion_enrichment_p")
    ax.set_ylabel(f"{key} (log-norm)", color=INK2, fontsize=9)
    ax.set_title(f"Lesion enrichment\nP={p:.1e}" if p else "Lesion",
                 fontsize=10, color=INK, pad=6)
    _panel(ax, "E")
    fig.tight_layout()
    return _save(fig, ctx, "fig09_spatial.png")


# ======================================== fig10: virtual knockout ========
def knockout(ctx: RunContext) -> str:
    pert = pd.read_csv(ctx.results / "s10_perturbation.csv")
    ora = pd.read_csv(ctx.results / "s10_perturbed_enrichment.csv")
    s10 = load_json(ctx.results / "s10_knockout.json")
    ko = s10.get("knockout_gene", "gene")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8),
                                   facecolor=SURFACE,
                                   gridspec_kw={"width_ratios": [1, 1.15]})
    # A: top-20 perturbed genes lollipop, FRGs highlighted
    top = pert.head(20).iloc[::-1]
    _style(ax1, xgrid=True, ygrid=False)
    ypos = np.arange(len(top))
    cols = [SEQ[5] if f else NEUTRAL for f in top["is_FRG"]]
    ax1.hlines(ypos, 0, top["perturbation"], color=cols, lw=2)
    ax1.scatter(top["perturbation"], ypos, s=40, c=cols, zorder=2)
    ax1.set_yticks(ypos)
    ax1.set_yticklabels(top["gene"], fontsize=8.5)
    for lbl, f in zip(ax1.get_yticklabels(), top["is_FRG"]):
        if f:
            lbl.set_fontweight("bold")
    ax1.set_xlabel("network perturbation score", color=INK2, fontsize=9)
    p = s10.get("frg_enrichment_p")
    ax1.set_title(f"Top genes perturbed by {ko} knockout\n"
                  f"(FRGs bold; FRG enrichment P={p:.1e})",
                  fontsize=10.5, color=INK, pad=6)
    legend = [Line2D([], [], color=SEQ[5], lw=2, label="ferroptosis gene"),
              Line2D([], [], color=NEUTRAL, lw=2, label="other")]
    ax1.legend(handles=legend, frameon=False, fontsize=8,
               labelcolor=INK2, loc="lower right")
    _panel(ax1, "A")

    # B: ORA dotplot of perturbed genes
    _style(ax2, xgrid=True, ygrid=False)
    if not ora.empty:
        top_t = ora.nsmallest(10, "pvalue").iloc[::-1]
        terms = [t.split("::", 1)[-1][:46] for t in top_t["term"]]
        logp = -np.log10(top_t["pvalue"].to_numpy())
        sc = ax2.scatter(top_t["gene_ratio"], range(len(top_t)),
                         s=40 + 55 * top_t["overlap"], c=logp,
                         cmap=SEQ_CMAP, lw=0)
        ax2.set_yticks(range(len(top_t)), terms, fontsize=8.5)
        ax2.set_xlabel("gene ratio", color=INK2, fontsize=9)
        fig.colorbar(sc, ax=ax2, shrink=0.8, label="-log10 P")
    ax2.set_title("Enrichment of perturbed genes", fontsize=10.5,
                  color=INK, pad=6)
    _panel(ax2, "B")
    fig.tight_layout()
    return _save(fig, ctx, "fig10_knockout.png")


# ================================================ fig11: docking =========
def docking(ctx: RunContext) -> str:
    df = pd.read_csv(ctx.results / "s11_docking_affinities.csv")
    df = df.dropna(subset=["best_affinity"]).sort_values(
        "best_affinity", ascending=False)
    thr = ctx.cfg["docking"]["affinity_threshold_kcal_mol"]
    pdb = ctx.cfg["docking"]["receptor_pdb"]

    fig, ax = plt.subplots(figsize=(6.4, 4.2), facecolor=SURFACE)
    _style(ax, xgrid=True, ygrid=False)
    bars = ax.barh(df["compound"], df["best_affinity"].abs(), height=0.62,
                   color=SEQ[4])
    for b, v in zip(bars, df["best_affinity"]):
        ax.text(abs(v) - 0.08, b.get_y() + b.get_height() / 2, f"{v:.1f}",
                ha="right", va="center", fontsize=8.5, color=SURFACE)
    ax.axvline(abs(thr), color=INK2, ls="--", lw=1.2)
    ax.text(abs(thr) + 0.04, len(df) - 0.4,
            f"strong-affinity threshold ({thr} kcal/mol)", fontsize=8.5,
            color=INK2)
    ax.set_xlabel("|binding energy| kcal/mol (AutoDock Vina, best pose)",
                  color=INK2, fontsize=9.5)
    ax.set_title(f"PAEs docking against {pdb}\n(3D poses: run "
                 "s11_docking_protocol.sh + PyMOL)", fontsize=11,
                 color=INK, pad=8)
    return _save(fig, ctx, "fig11_docking.png")


def _has(ctx, *names):
    return all((ctx.results / n).exists() for n in names)


def render_all(ctx: RunContext) -> list[str]:
    # pick single-cell / trajectory renderer by what the stage produced:
    # real scanpy exports take precedence over the synthetic-demo path
    sc_fig = (singlecell_real if _has(ctx, "s08_cells_viz.csv",
                                      "s08_marker_dotplot.csv")
              else singlecell)
    traj_fig = (stemness_trajectory_real
                if _has(ctx, "s08_cells_viz.csv", "s08_axis_cells.csv")
                else stemness_trajectory)
    renderers = [workflow, targets_de, intersection_genes, ml_benchmark,
                 ml_models, immune, sc_fig, traj_fig, spatial, knockout,
                 docking]
    out = []
    for fn in renderers:
        try:
            name = fn(ctx)
            if name:
                out.append(name)
        except FileNotFoundError as exc:
            print(f"[figures] skip {fn.__name__}: missing input {exc}")
        except Exception as exc:
            print(f"[figures] skip {fn.__name__}: {type(exc).__name__}: {exc}")
    (ctx.results / "figures_manifest.json").write_text(
        json.dumps(out, indent=2))
    return out


# ================= real-data single-cell figures (precomputed) ===========
def singlecell_real(ctx: RunContext) -> str:
    """fig07 from scanpy exports (s08_cells_viz.csv + s08_marker_dotplot.csv)."""
    viz = pd.read_csv(ctx.results / "s08_cells_viz.csv")
    dot = pd.read_csv(ctx.results / "s08_marker_dotplot.csv")
    s8 = load_json(ctx.results / "s08_singlecell.json")
    key = s8.get("key_gene", "gene")
    axis_types = set(ctx.cfg["single_cell"].get("axis_types", []))
    types = sorted(viz["annotated"].unique())
    tcol = {t: CAT[i % len(CAT)] for i, t in enumerate(types)}
    # subsample for scatter legibility
    rng = np.random.default_rng(0)
    idx = (rng.choice(len(viz), 8000, replace=False)
           if len(viz) > 8000 else np.arange(len(viz)))
    v = viz.iloc[idx]

    fig, axs = plt.subplot_mosaic(
        [["A", "B", "C"], ["D", "E", "C"]], figsize=(13, 8),
        facecolor=SURFACE, gridspec_kw={"width_ratios": [1, 1, 1.15]})

    ax = axs["A"]
    _style(ax, False, False)
    for t in types:
        m = (v["annotated"] == t).to_numpy()
        ax.scatter(v["pc1"][m], v["pc2"][m], s=4, c=tcol[t], lw=0, alpha=0.6)
    for t in types:
        m = (viz["annotated"] == t).to_numpy()
        ax.text(viz["pc1"][m].median(), viz["pc2"][m].median(), t,
                fontsize=8, color=INK, fontweight="bold", ha="center",
                bbox=dict(boxstyle="round,pad=0.12", fc=SURFACE, ec=GRID,
                          alpha=0.85))
    ax.set_xlabel("PC1", color=INK2, fontsize=9)
    ax.set_ylabel("PC2", color=INK2, fontsize=9)
    ax.set_title(f"Cell-type embedding (n={len(viz):,})", fontsize=11,
                 color=INK, pad=6)
    _panel(ax, "A")

    ax = axs["B"]
    _style(ax, False, False)
    if "key_gene_expr" in v:
        kg = v["key_gene_expr"].to_numpy()
        order = np.argsort(kg)
        sc = ax.scatter(v["pc1"].to_numpy()[order], v["pc2"].to_numpy()[order],
                        s=4, c=kg[order], cmap=SEQ_CMAP, lw=0)
        fig.colorbar(sc, ax=ax, shrink=0.75, label=f"{key} (log-norm)")
    ax.set_xlabel("PC1", color=INK2, fontsize=9)
    ax.set_ylabel("PC2", color=INK2, fontsize=9)
    ax.set_title(f"{key} expression", fontsize=11, color=INK, pad=6)
    _panel(ax, "B")

    ax = axs["C"]
    ax.set_facecolor(SURFACE)
    mk = list(dict.fromkeys(dot["marker"]))
    cts = sorted(dot["cell_type"].unique())
    piv_mean = dot.pivot(index="cell_type", columns="marker", values="mean")
    piv_pct = dot.pivot(index="cell_type", columns="marker", values="pct")
    mz = (piv_mean - piv_mean.mean()) / (piv_mean.std() + 1e-9)
    for ti, ct in enumerate(cts):
        for mi, m in enumerate(mk):
            ax.scatter(mi, len(cts) - 1 - ti,
                       s=10 + 150 * float(piv_pct.loc[ct, m]),
                       c=[SEQ_CMAP((np.clip(mz.loc[ct, m], -2, 2) + 2) / 4)],
                       lw=0)
    ax.set_xticks(range(len(mk)), mk, rotation=60, ha="right", fontsize=7.5)
    ax.set_yticks(range(len(cts)), cts[::-1], fontsize=8.5)
    ax.set_xlim(-0.6, len(mk) - 0.4)
    for sp in ax.spines.values():
        sp.set_color(GRID)
    ax.set_title("Marker dotplot (size=pct, color=scaled mean)",
                 fontsize=10.5, color=INK, pad=6)
    _panel(ax, "C")

    ax = axs["D"]
    _style(ax, False, True)
    prop = (viz.groupby("group")["annotated"]
            .value_counts(normalize=True).unstack(fill_value=0))
    bottoms = np.zeros(len(prop))
    for t in types:
        vals = prop.get(t, pd.Series(0, index=prop.index)).to_numpy()
        ax.bar(prop.index, vals, bottom=bottoms, width=0.55, color=tcol[t],
               label=t, edgecolor=SURFACE, linewidth=1.5)
        bottoms += vals
    ax.set_ylabel("proportion", color=INK2, fontsize=9)
    ax.legend(frameon=False, fontsize=7, labelcolor=INK2,
              loc="center left", bbox_to_anchor=(1.0, 0.5))
    ax.set_title("Composition by group (DIS/HEA)", fontsize=11, color=INK,
                 pad=6)
    _panel(ax, "D")

    ax = axs["E"]
    _style(ax, False, True)
    if "key_gene_expr" in viz:
        data = [viz.loc[viz["annotated"] == t, "key_gene_expr"].to_numpy()
                for t in types]
        vp = ax.violinplot(data, showmedians=True, widths=0.8)
        for body, t in zip(vp["bodies"], types):
            body.set_facecolor(SEQ[5] if t in axis_types else SEQ[2])
            body.set_alpha(0.75)
            body.set_edgecolor(INK2)
        for part in ("cmins", "cmaxes", "cbars", "cmedians"):
            vp[part].set_color(INK2)
            vp[part].set_linewidth(1)
        ax.set_xticks(range(1, len(types) + 1), types, rotation=40,
                      ha="right", fontsize=8)
        for lbl in ax.get_xticklabels():
            if lbl.get_text() in axis_types:
                lbl.set_fontweight("bold")
    ax.set_ylabel(f"{key} (log-norm)", color=INK2, fontsize=9)
    ax.set_title(f"{key} by cell type (axis bold)", fontsize=11, color=INK,
                 pad=6)
    _panel(ax, "E")
    fig.tight_layout()
    return _save(fig, ctx, "fig07_singlecell.png")


def stemness_trajectory_real(ctx: RunContext) -> str:
    """fig08 from scanpy exports (s08_cells_viz + s08_axis_cells)."""
    viz = pd.read_csv(ctx.results / "s08_cells_viz.csv")
    ax_df = pd.read_csv(ctx.results / "s08_axis_cells.csv")
    s8 = load_json(ctx.results / "s08_singlecell.json")
    key = s8.get("key_gene", "gene")
    axis_types = list(ctx.cfg["single_cell"].get("axis_types", []))
    origin = set(ctx.cfg["single_cell"].get("axis_origin", axis_types[:-1]))
    types = sorted(viz["annotated"].unique())

    fig, axs = plt.subplot_mosaic(
        [["A", "B", "C"], ["D", "E", "F"]], figsize=(13, 8),
        facecolor=SURFACE)

    ax = axs["A"]
    _style(ax)
    data = [viz.loc[viz["annotated"] == t, "stemness"].to_numpy()
            for t in types]
    bp = ax.boxplot(data, patch_artist=True, widths=0.55,
                    medianprops=dict(color=INK2), showfliers=False)
    for patch, t in zip(bp["boxes"], types):
        patch.set_facecolor(SEQ[5] if t in axis_types else SEQ[2])
        patch.set_alpha(0.8)
        patch.set_edgecolor(INK2)
    for el in ("whiskers", "caps"):
        for line in bp[el]:
            line.set_color(INK2)
    ax.set_xticks(range(1, len(types) + 1), types, rotation=40, ha="right",
                  fontsize=8)
    for lbl in ax.get_xticklabels():
        if lbl.get_text() in axis_types:
            lbl.set_fontweight("bold")
    ax.set_ylabel("stemness (CytoTRACE-style)", color=INK2, fontsize=9)
    ax.set_title("Differentiation potential by subtype", fontsize=11,
                 color=INK, pad=6)
    _panel(ax, "A")

    ax = axs["B"]
    _style(ax)
    if "key_gene_expr" in viz:
        xg = viz["key_gene_expr"].to_numpy()
        yg = viz["stemness"].to_numpy()
        rho, pv = sps.spearmanr(xg, yg)
        rng = np.random.default_rng(0)
        idx = rng.choice(len(xg), min(6000, len(xg)), replace=False)
        ax.scatter(xg[idx], yg[idx], s=5, c=SEQ[3], lw=0, alpha=0.4)
        coef = np.polyfit(xg, yg, 1)
        xs = np.linspace(xg.min(), xg.max(), 50)
        ax.plot(xs, np.polyval(coef, xs), color=INK2, lw=1.6)
        ax.text(0.04, 0.93, f"R={rho:.2f}, P={pv:.1e}",
                transform=ax.transAxes, fontsize=9, color=INK)
    ax.set_xlabel(f"{key} (log-norm)", color=INK2, fontsize=9)
    ax.set_ylabel("stemness", color=INK2, fontsize=9)
    ax.set_title(f"{key} vs stemness", fontsize=11, color=INK, pad=6)
    _panel(ax, "B")

    ax = axs["C"]
    _style(ax, False, False)
    sc = ax.scatter(ax_df["pc1"], ax_df["pc2"], s=7,
                    c=ax_df["pseudotime"], cmap=SEQ_CMAP, lw=0)
    fig.colorbar(sc, ax=ax, shrink=0.75, label="pseudotime")
    ax.set_xlabel("component 1", color=INK2, fontsize=9)
    ax.set_ylabel("component 2", color=INK2, fontsize=9)
    ax.set_title("Phenotype-switch trajectory", fontsize=11, color=INK, pad=6)
    _panel(ax, "C")

    ax = axs["D"]
    _style(ax, False, False)
    for i, t in enumerate(axis_types):
        m = (ax_df["annotated"] == t).to_numpy()
        ax.scatter(ax_df["pc1"][m], ax_df["pc2"][m], s=7, c=CAT[i], lw=0,
                   alpha=0.7)
        if m.sum():
            ax.text(ax_df["pc1"][m].median(), ax_df["pc2"][m].median(), t,
                    fontsize=8, color=INK, fontweight="bold", ha="center",
                    bbox=dict(boxstyle="round,pad=0.12", fc=SURFACE, ec=GRID,
                              alpha=0.85))
    ax.set_xlabel("component 1", color=INK2, fontsize=9)
    ax.set_ylabel("component 2", color=INK2, fontsize=9)
    ax.set_title(" + ".join(axis_types[:-1]) + " → " + axis_types[-1],
                 fontsize=11, color=INK, pad=6)
    _panel(ax, "D")

    ax = axs["E"]
    _style(ax)
    order = np.argsort(ax_df["pseudotime"].to_numpy())
    tvals = ax_df["pseudotime"].to_numpy()[order]
    switch = [g for g in ("MYH11", "ACTA2", "TAGLN", "FN1", "LUM", "COL1A1")
              if g in ax_df.columns][:4]
    for gi, g in enumerate(switch):
        vals = ax_df[g].to_numpy()[order]
        sm = pd.Series(vals).rolling(max(20, len(vals) // 25),
                                     center=True, min_periods=5).mean()
        ax.plot(tvals, sm, color=CAT[gi], lw=2, label=g)
    ax.legend(frameon=False, fontsize=8, labelcolor=INK2)
    ax.set_xlabel("pseudotime", color=INK2, fontsize=9)
    ax.set_ylabel("expression (smoothed)", color=INK2, fontsize=9)
    ax.set_title("Phenotype markers along pseudotime", fontsize=11,
                 color=INK, pad=6)
    _panel(ax, "E")

    ax = axs["F"]
    _style(ax)
    if key in ax_df.columns:
        xg = ax_df[key].to_numpy()
        txt = []
        for gi, g in enumerate([m for m in ("FN1", "LUM", "COL1A1")
                                if m in ax_df.columns][:2]):
            yg = ax_df[g].to_numpy()
            rho, pv = sps.spearmanr(xg, yg)
            ax.scatter(xg, yg, s=7, c=CAT[gi], lw=0, alpha=0.4, label=g)
            coef = np.polyfit(xg, yg, 1)
            xs = np.linspace(xg.min(), xg.max(), 50)
            ax.plot(xs, np.polyval(coef, xs), color=CAT[gi], lw=1.8)
            txt.append(f"{g}: R={rho:.2f}, P={pv:.1e}")
        ax.text(0.04, 0.95, "\n".join(txt), transform=ax.transAxes,
                fontsize=8, color=INK, va="top")
        ax.legend(frameon=False, fontsize=8, labelcolor=INK2,
                  loc="lower right")
    ax.set_xlabel(f"{key} (log-norm)", color=INK2, fontsize=9)
    ax.set_ylabel("mesenchymal marker", color=INK2, fontsize=9)
    ax.set_title(f"{key} vs switching markers", fontsize=11, color=INK, pad=6)
    _panel(ax, "F")
    fig.tight_layout()
    return _save(fig, ctx, "fig08_stemness_trajectory.png")
