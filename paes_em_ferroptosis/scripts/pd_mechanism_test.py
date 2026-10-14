"""Mechanism-reality test for Paraquat -> Parkinson's disease.

The intersection-specificity scan ranked Paraquat x PD x {oxidative_stress,
ferroptosis} top. But specificity of the target overlap is necessary, not
sufficient — the atherosclerosis story died because the mechanism gene set
showed NO differential-expression enrichment in disease tissue. This script
runs that decisive test in two PD substantia-nigra cohorts:

  GSE7621 (GPL570, SN, Control vs PD) and GSE20292 (GPL96, SN).

For each mechanism gene set (ferroptosis, oxidative_stress), it tests
whether the set is DE-enriched vs an expression-matched background
(Mann-Whitney on moderated-t; Fisher on DEG proportion). A mechanism that
is REAL in the disease passes here; one that is a network-toxicology
artifact does not.
"""

from __future__ import annotations

import gzip
import io
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import fisher_exact, mannwhitneyu

sys.path.insert(0, "paes_em")
from utils.stats import moderated_t  # noqa: E402

PD = Path("scan/pd_geo")
GSDIR = Path("scan/genesets")
LFC, PADJ = 0.5, 0.05
MECHS = ["ferroptosis", "oxidative_stress"]


def annot_map(path, id_col="ID", sym_col="Gene symbol"):
    rows = {}
    with gzip.open(path, "rt", errors="replace") as fh:
        in_t, header = False, None
        for line in fh:
            if line.startswith(("!platform_table_begin",
                                "!Annotation_table_begin")):
                in_t = True
                continue
            if line.startswith(("!platform_table_end",
                                "!Annotation_table_end")):
                break
            if not in_t:
                continue
            p = line.rstrip("\n").split("\t")
            if header is None:
                header = p
                i_id, i_sym = header.index(id_col), header.index(sym_col)
                continue
            if len(p) > max(i_id, i_sym) and p[i_sym]:
                rows[p[i_id]] = p[i_sym]
    s = pd.Series(rows)
    return s[s.str.len() > 0]


def read_matrix(path):
    lines, in_t, chars, titles = [], False, [], []
    with gzip.open(path, "rt", errors="replace") as fh:
        for line in fh:
            if line.startswith("!series_matrix_table_begin"):
                in_t = True
                continue
            if line.startswith("!series_matrix_table_end"):
                break
            if in_t:
                lines.append(line)
            elif line.startswith("!Sample_characteristics_ch1"):
                chars.append([v.strip('"') for v in
                              line.rstrip().split("\t")[1:]])
            elif line.startswith("!Sample_title"):
                titles = [v.strip('"') for v in line.rstrip().split("\t")[1:]]
    expr = pd.read_csv(io.StringIO("".join(lines)), sep="\t", index_col=0)
    return expr, chars, titles


def collapse(expr, mapping):
    expr = expr.loc[expr.index.astype(str).isin(mapping.index)]
    expr = expr.copy()
    expr["__s"] = mapping.loc[expr.index.astype(str)].to_numpy()
    expr["__m"] = expr.drop(columns="__s").mean(axis=1).to_numpy()
    expr = expr.sort_values("__m", ascending=False)
    expr = expr[~expr["__s"].duplicated()].set_index("__s").drop(columns="__m")
    expr.index.name = "gene"
    return expr


def groups_7621(chars, titles):
    # characteristics row holds "Old Control"/"Parkinson..."
    for row in chars:
        if row and ("control" in row[0].lower() or "parkinson" in row[0].lower()):
            return ["PD" if "parkinson" in v.lower() else "Control"
                    for v in row]
    return ["PD" if "parkinson" in t.lower() else "Control" for t in titles]


def groups_20292(chars):
    for row in chars:
        if row and row[0].lower().startswith("disease state"):
            return ["PD" if "parkinson" in v.lower() else "Control"
                    for v in row]
    raise ValueError("no disease state row")


def matched_bg(expr_mean, mech, nonmech, rng, nb=10):
    ranks = expr_mean.rank(pct=True)
    bins = np.minimum((ranks * nb).astype(int), nb - 1)
    by = {b: [] for b in range(nb)}
    for g in nonmech:
        by[bins[g]].append(g)
    used, picked = set(), []
    for g in mech:
        pool = [x for x in by[bins[g]] if x not in used]
        if pool:
            c = rng.choice(pool)
            used.add(c)
            picked.append(c)
    return picked


def test_cohort(acc, expr, grp, genesets, rng):
    de = moderated_t(expr, grp, "PD").loc[expr.index]
    is_deg = (de["adj.P.Val"] < PADJ) & (de["logFC"].abs() > LFC)
    t = de["t"]
    em = expr.mean(axis=1)
    out = {"n_samples": expr.shape[1],
           "groups": grp.value_counts().to_dict(),
           "n_degs": int(is_deg.sum())}
    for mech in MECHS:
        gset = [g for g in expr.index if g in genesets[mech]]
        nonm = [g for g in expr.index if g not in genesets[mech]]
        bg = matched_bg(em, gset, nonm, rng)
        mwu = mannwhitneyu(t[gset], t[bg], alternative="two-sided")
        a = int(is_deg[gset].sum()); b = len(gset) - a
        c = int(is_deg[bg].sum()); d = len(bg) - c
        orr, pf = fisher_exact([[a, b], [c, d]])
        out[mech] = {
            "n_in_set": len(gset),
            "median_t_set": round(float(t[gset].median()), 3),
            "median_t_bg": round(float(t[bg].median()), 3),
            "mwu_p": float(f"{mwu.pvalue:.3g}"),
            "deg_prop_set": round(a / len(gset), 3),
            "deg_prop_bg": round(c / len(bg), 3),
            "deg_or": round(float(orr), 3),
            "deg_fisher_p": float(f"{pf:.3g}"),
        }
    return out


def main():
    rng = np.random.default_rng(20260302)
    genesets = {m: set(json.loads((GSDIR / f"{m}.json").read_text()))
                for m in MECHS}
    m570 = annot_map(PD / "GPL570.annot.gz")
    m96 = annot_map(PD / "GPL96.annot.gz")

    res = {}
    # GSE7621
    expr, chars, titles = read_matrix(PD / "GSE7621_series_matrix.txt.gz")
    g = collapse(expr.apply(pd.to_numeric, errors="coerce").dropna(), m570)
    if g.to_numpy().max() > 50:
        g = pd.DataFrame(np.log2(g.clip(lower=0).to_numpy() + 1),
                         index=g.index, columns=g.columns)
    grp = pd.Series(groups_7621(chars, titles), index=g.columns)
    res["GSE7621"] = test_cohort("GSE7621", g, grp, genesets, rng)

    # GSE20292
    expr, chars, titles = read_matrix(PD / "GSE20292_series_matrix.txt.gz")
    g = collapse(expr.apply(pd.to_numeric, errors="coerce").dropna(), m96)
    if g.to_numpy().max() > 50:
        g = pd.DataFrame(np.log2(g.clip(lower=0).to_numpy() + 1),
                         index=g.index, columns=g.columns)
    grp = pd.Series(groups_20292(chars), index=g.columns)
    res["GSE20292"] = test_cohort("GSE20292", g, grp, genesets, rng)

    Path("scan/pd_mechanism_test.json").write_text(
        json.dumps(res, indent=2, ensure_ascii=False))
    for acc, r in res.items():
        print(f"\n{acc}: {r['groups']}, DEGs={r['n_degs']}")
        for m in MECHS:
            x = r[m]
            print(f"  {m:16s} median t set {x['median_t_set']} vs bg "
                  f"{x['median_t_bg']}, MWU p={x['mwu_p']}; "
                  f"DEG OR={x['deg_or']} Fisher p={x['deg_fisher_p']}")


if __name__ == "__main__":
    main()
