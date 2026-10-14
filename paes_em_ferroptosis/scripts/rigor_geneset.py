"""Gene-set differential-expression 'defense' across all 3 cohorts, using
the FULL FerrDb set (983), with TWO backgrounds:

* expression-matched background (honest): for each ferroptosis gene,
  draw a non-FRG gene from the same expression decile; compare the
  moderated-t statistics (Mann-Whitney) and the DEG proportion (Fisher).
* whole-transcriptome background (confounded): same test vs all non-FRG
  genes -> looks significant only because ferroptosis genes are highly
  expressed and high-expression genes are more often DE.

Reporting both exposes the confounder. Done per cohort to show the
3-cohort consistency the single-cohort result lacks.

Writes athero/results/rigor_geneset_defense.json.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact, mannwhitneyu

import sys
sys.path.insert(0, "paes_em")
from utils.stats import moderated_t  # noqa: E402

PROC = Path("athero/processed")
RES = Path("athero/results")
SEED = 20260302
FRG = set(json.loads((Path("athero/raw/frgs_ferrdb.json")).read_text()))
COHORTS = ["GSE100927", "GSE28829", "GSE43292"]
LFC, PADJ = 0.5, 0.05


def matched_background(expr_mean, frg_genes, nonfrg, rng, n_bins=10):
    """One expression-decile-matched non-FRG gene per FRG gene."""
    ranks = expr_mean.rank(pct=True)
    bins = np.minimum((ranks * n_bins).astype(int), n_bins - 1)
    nonfrg_by_bin = {b: [] for b in range(n_bins)}
    for g in nonfrg:
        nonfrg_by_bin[bins[g]].append(g)
    picked = []
    used = set()
    for g in frg_genes:
        b = bins[g]
        pool = [x for x in nonfrg_by_bin[b] if x not in used]
        if not pool:
            continue
        c = rng.choice(pool)
        used.add(c)
        picked.append(c)
    return picked


def cohort_test(acc, rng):
    expr = pd.read_csv(PROC / f"{acc}_expr.csv", index_col=0)
    grp = pd.read_csv(PROC / f"{acc}_groups.csv", index_col=0)["group"]
    de = moderated_t(expr, grp, "EM")
    de = de.loc[expr.index]
    is_deg = ((de["adj.P.Val"] < PADJ) & (de["logFC"].abs() > LFC))
    t = de["t"]
    expr_mean = expr.mean(axis=1)

    frg_in = [g for g in expr.index if g in FRG]
    nonfrg = [g for g in expr.index if g not in FRG]
    matched = matched_background(expr_mean, frg_in, nonfrg, rng)

    def pack(bg, label):
        mt = mannwhitneyu(t[frg_in], t[bg], alternative="two-sided")
        # Fisher on DEG proportion
        a = int(is_deg[frg_in].sum()); b = len(frg_in) - a
        c = int(is_deg[bg].sum()); d = len(bg) - c
        orr, pf = fisher_exact([[a, b], [c, d]])
        return {
            "background": label, "n_frg": len(frg_in), "n_bg": len(bg),
            "median_t_frg": round(float(t[frg_in].median()), 3),
            "median_t_bg": round(float(t[bg].median()), 3),
            "mwu_p": float(f"{mt.pvalue:.3g}"),
            "deg_prop_frg": round(a / len(frg_in), 3),
            "deg_prop_bg": round(c / len(bg), 3),
            "deg_odds_ratio": round(float(orr), 3),
            "deg_fisher_p": float(f"{pf:.3g}"),
        }

    return {"matched": pack(matched, "expression-matched"),
            "whole_transcriptome": pack(nonfrg, "whole-transcriptome")}


def main():
    rng = np.random.default_rng(SEED)
    out = {"full_ferrdb_n": len(FRG), "lfc": LFC, "padj": PADJ,
           "note": "the matched-background test is the valid one; the "
                   "whole-transcriptome test is confounded by the fact that "
                   "ferroptosis genes are highly expressed and highly "
                   "expressed genes are more often DE. Report both.",
           "cohorts": {}}
    for acc in COHORTS:
        out["cohorts"][acc] = cohort_test(acc, rng)
        m = out["cohorts"][acc]["matched"]
        w = out["cohorts"][acc]["whole_transcriptome"]
        print(f"{acc}: matched MWU p={m['mwu_p']} "
              f"(median t {m['median_t_frg']} vs {m['median_t_bg']}), "
              f"Fisher OR={m['deg_odds_ratio']} p={m['deg_fisher_p']} | "
              f"transcriptome MWU p={w['mwu_p']}")
    # consistency: matched background n.s. in all cohorts?
    matched_ps = [out["cohorts"][a]["matched"]["mwu_p"] for a in COHORTS]
    out["matched_nonsignificant_in_all_cohorts"] = all(
        p >= 0.05 for p in matched_ps)
    (RES / "rigor_geneset_defense.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False))
    print("matched n.s. in all cohorts:",
          out["matched_nonsignificant_in_all_cohorts"])


if __name__ == "__main__":
    main()
