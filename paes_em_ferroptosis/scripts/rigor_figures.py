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


def figS4():
    """3-cohort ferroptosis gene-set DE defense, both backgrounds."""
    import json as _j
    d = _j.loads((RES / "rigor_geneset_defense.json").read_text())
    cohorts = list(d["cohorts"])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6), facecolor=SURFACE)

    # A: matched-background Fisher DEG-proportion (robust defense)
    _style(ax1, yg=True)
    x = np.arange(len(cohorts))
    w = 0.35
    frg = [d["cohorts"][c]["matched"]["deg_prop_frg"] for c in cohorts]
    bg = [d["cohorts"][c]["matched"]["deg_prop_bg"] for c in cohorts]
    ax1.bar(x - w/2, frg, w, color=RED, label="ferroptosis (983)")
    ax1.bar(x + w/2, bg, w, color=NEUTRAL, label="expr-matched background")
    for i, c in enumerate(cohorts):
        p = d["cohorts"][c]["matched"]["deg_fisher_p"]
        ax1.text(i, max(frg[i], bg[i]) + 0.02, f"OR={d['cohorts'][c]['matched']['deg_odds_ratio']}\np={p}",
                 ha="center", fontsize=7.5, color=INK2)
    ax1.set_xticks(x, cohorts, fontsize=9)
    ax1.set_ylabel("DEG proportion", color=INK2, fontsize=9)
    ax1.set_ylim(0, 1)
    ax1.legend(frameon=False, fontsize=8, labelcolor=INK2)
    ax1.set_title("A  DEG-proportion defense holds 3/3\n"
                  "(FRG not enriched vs matched background)", fontsize=10.5,
                  color=INK, pad=6)

    # B: matched vs whole-transcriptome MWU p (confounding)
    _style(ax2, yg=True)
    mp = [-np.log10(d["cohorts"][c]["matched"]["mwu_p"]) for c in cohorts]
    wp = [-np.log10(d["cohorts"][c]["whole_transcriptome"]["mwu_p"])
          for c in cohorts]
    ax2.bar(x - w/2, mp, w, color=BLUE, label="matched background (valid)")
    ax2.bar(x + w/2, wp, w, color="#eda100",
            label="whole transcriptome (confounded)")
    ax2.axhline(-np.log10(0.05), color=INK2, ls="--", lw=1)
    ax2.text(len(cohorts) - 0.5, -np.log10(0.05) + 0.1, "p=0.05",
             fontsize=7.5, color=INK2, ha="right")
    ax2.set_xticks(x, cohorts, fontsize=9)
    ax2.set_ylabel("-log10 MWU p (t-statistic)", color=INK2, fontsize=9)
    ax2.legend(frameon=False, fontsize=8, labelcolor=INK2)
    ax2.set_title("B  Whole-transcriptome background inflates\nsignificance "
                  "(expression confounding)", fontsize=10.5, color=INK, pad=6)
    fig.suptitle("Fig S4  Ferroptosis gene-set is not DE-enriched beyond "
                 "expression-matched background (full FerrDb 983, 3 cohorts)",
                 fontsize=11.5, color=INK, y=1.03)
    fig.tight_layout()
    return _save(fig, "figS4_geneset_defense.png")


def figS5():
    """Docking rigor: multi-site dispersion + control discrimination."""
    import json as _j
    d = _j.loads((RES / "rigor_docking_sites.json").read_text())
    c = d["controls"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6), facecolor=SURFACE)

    # A: pairwise centroid distances
    _style(ax1, yg=True)
    import numpy as _np
    from pathlib import Path as _P
    import itertools as _it
    def cen(p):
        xs = []; inm = False
        for line in open(p):
            if line.startswith("MODEL"):
                inm = line.split()[1] == "1"
            elif line.startswith("ENDMDL") and inm:
                break
            elif inm and line.startswith(("ATOM", "HETATM")):
                xs.append([float(line[30:38]), float(line[38:46]),
                           float(line[46:54])])
        return _np.mean(xs, 0) if xs else None
    dock = _P("athero/raw/docking")
    cents = {p.name.replace("_out.pdbqt", ""): cen(p)
             for p in sorted(dock.glob("*_out.pdbqt"))
             if "POS" not in p.name and "NEG" not in p.name}
    cents = {k: v for k, v in cents.items() if v is not None}
    dists = [ _np.linalg.norm(cents[a] - cents[b])
              for a, b in _it.combinations(cents, 2)]
    ax1.hist(dists, bins=18, color=NEUTRAL, edgecolor=SURFACE)
    ax1.axvline(8, color=RED, ls="--", lw=1.2, label="8 Å (same-site cutoff)")
    ax1.axvline(d["median_pair_dist_A"], color=BLUE, lw=1.5,
                label=f"median {d['median_pair_dist_A']} Å")
    ax1.set_xlabel("pairwise best-pose centroid distance (Å)", color=INK2,
                   fontsize=9)
    ax1.set_ylabel("compound pairs", color=INK2, fontsize=9)
    ax1.legend(frameon=False, fontsize=8, labelcolor=INK2)
    ax1.set_title(f"A  Compounds bind different sites\n"
                  f"({d['pairs_over_8A']}/{d['n_pairs']} pairs >8 Å; "
                  f"scores not comparable)", fontsize=10.5, color=INK, pad=6)

    # B: control discrimination
    _style(ax2, yg=True)
    items = [("linoleic\n(POS)", c["positive_ligands"]["linoleic_acid"], BLUE),
             ("oleic\n(POS)", c["positive_ligands"]["oleic_acid"], BLUE),
             ("glucose\n(decoy)", c["negative_decoy"]["glucose"], RED)]
    xs = range(len(items))
    ax2.bar(xs, [abs(v) for _, v, _ in items],
            color=[col for _, _, col in items], width=0.6)
    lo, hi = abs(d["controls"]["plasticizer_range"][1]), abs(
        d["controls"]["plasticizer_range"][0])
    ax2.axhspan(lo, hi, color="#eda100", alpha=0.18)
    ax2.text(2.4, (lo + hi) / 2, "plasticizer\nrange", fontsize=7.5,
             color="#a06a00", ha="center", va="center")
    for i, (_, v, _c) in enumerate(items):
        ax2.text(i, abs(v) + 0.05, f"{v}", ha="center", fontsize=8.5,
                 color=INK)
    ax2.set_xticks(list(xs), [n for n, _, _ in items], fontsize=8.5)
    ax2.set_ylabel("|binding energy| kcal/mol", color=INK2, fontsize=9)
    ax2.set_title("B  Decoy scores like real ligands\n"
                  "(box cannot discriminate binders)", fontsize=10.5,
                  color=INK, pad=6)
    fig.suptitle("Fig S5  Docking cannot support specific binding: multi-site "
                 "poses + decoy passes", fontsize=11.5, color=INK, y=1.03)
    fig.tight_layout()
    return _save(fig, "figS5_docking_rigor.png")


def figS6():
    """Formal permutation null distributions."""
    import json as _j
    it = _j.loads((RES / "rigor_intersection_permutation.json").read_text())
    ml = _j.loads((RES / "rigor_ml.json").read_text())
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4), facecolor=SURFACE)

    _style(ax1)
    nv = np.array(it["null_values"])
    ax1.hist(nv, bins=range(0, int(nv.max()) + 22, 1), color=NEUTRAL,
             edgecolor=SURFACE)
    ax1.axvline(it["observed_intersection_size"], color=RED, lw=2,
                label=f"observed {it['observed_intersection_size']}")
    ax1.set_xlabel("intersection size under random CTD gene sets", color=INK2,
                   fontsize=9)
    ax1.set_ylabel("permutations", color=INK2, fontsize=9)
    ax1.legend(frameon=False, fontsize=8, labelcolor=INK2)
    ax1.set_title(f"A  Intersection specificity\n(n=1000, P={it['empirical_p_size']}, "
                  f"{it['enrichment_fold']}× over null)", fontsize=10.5,
                  color=INK, pad=6)

    _style(ax2)
    perm = ml["external_auc_permutation"]
    nv2 = np.array(perm.get("null_values", []))
    ax2.hist(nv2, bins=25, color=NEUTRAL, edgecolor=SURFACE)
    ax2.axvline(perm["real_mean_external_auc"], color=RED, lw=2,
                label=f"observed {perm['real_mean_external_auc']}")
    ax2.axvline(perm["null_95pct"], color=INK2, ls="--", lw=1,
                label=f"null 95% {perm['null_95pct']}")
    ax2.set_xlabel("mean external AUC under label permutation", color=INK2,
                   fontsize=9)
    ax2.set_ylabel("permutations", color=INK2, fontsize=9)
    ax2.legend(frameon=False, fontsize=8, labelcolor=INK2)
    ax2.set_title(f"B  ML external generalization\n(n={perm['n_permutations']}, "
                  f"P={perm['empirical_p']})", fontsize=10.5, color=INK, pad=6)
    fig.suptitle("Fig S6  Formal permutation null distributions", fontsize=11.5,
                 color=INK, y=1.03)
    fig.tight_layout()
    return _save(fig, "figS6_permutation_nulls.png")
