"""Statistics helpers: BH adjustment, moderated t-test (limma-style),
hypergeometric ORA, and ssGSEA scoring — pure numpy/scipy implementations
so the pipeline runs without R. R hooks (limma / clusterProfiler / GSVA)
can replace these for publication-grade runs.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import special as spsp
from scipy import stats as sps


def bh_adjust(pvals: np.ndarray) -> np.ndarray:
    """Benjamini–Hochberg FDR adjustment."""
    p = np.asarray(pvals, dtype=float)
    n = p.size
    order = np.argsort(p)
    ranked = p[order] * n / (np.arange(n) + 1)
    # enforce monotonicity from the largest p downwards
    ranked = np.minimum.accumulate(ranked[::-1])[::-1]
    out = np.empty(n)
    out[order] = np.clip(ranked, 0, 1)
    return out


def moderated_t(
    expr: pd.DataFrame, groups: pd.Series, case_label: str
) -> pd.DataFrame:
    """limma-style moderated t-test (empirical-Bayes variance shrinkage).

    Implements the Smyth (2004) eBayes moderation for a two-group design:
    gene-wise residual variances are shrunk towards a pooled prior estimated
    by fitting a scaled inverse chi-square to the variance distribution.

    Parameters
    ----------
    expr : genes x samples log2 expression matrix.
    groups : per-sample labels aligned to ``expr.columns``.
    case_label : label treated as case; the remaining samples are control.

    Returns a DataFrame indexed by gene with columns
    ``logFC, AveExpr, t, P.Value, adj.P.Val``.
    """
    groups = groups.loc[expr.columns]
    case = expr.loc[:, (groups == case_label).values].to_numpy(float)
    ctrl = expr.loc[:, (groups != case_label).values].to_numpy(float)
    n1, n2 = case.shape[1], ctrl.shape[1]
    if min(n1, n2) < 2:
        raise ValueError("need >=2 samples per group for moderated t-test")

    m1, m2 = case.mean(axis=1), ctrl.mean(axis=1)
    logfc = m1 - m2
    df_resid = n1 + n2 - 2
    s2 = (case.var(1, ddof=1) * (n1 - 1) + ctrl.var(1, ddof=1) * (n2 - 1)) / df_resid
    s2 = np.maximum(s2, 1e-12)

    # --- empirical Bayes: fit scaled inv-chisq prior to log(s2) ---
    z = np.log(s2)
    e = z - spsp.digamma(df_resid / 2) + np.log(df_resid / 2)
    e_mean = e.mean()
    e_var = max(e.var(ddof=1) - spsp.polygamma(1, df_resid / 2), 1e-8)

    # solve trigamma(d0/2) = e_var for d0 by bisection
    def trigamma_inv(y: float) -> float:
        lo, hi = 1e-3, 1e4
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if spsp.polygamma(1, mid) > y:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    d0 = 2.0 * trigamma_inv(e_var)
    s0_2 = np.exp(e_mean + spsp.digamma(d0 / 2) - np.log(d0 / 2))

    s2_post = (d0 * s0_2 + df_resid * s2) / (d0 + df_resid)
    se = np.sqrt(s2_post * (1 / n1 + 1 / n2))
    tstat = logfc / se
    df_total = df_resid + d0
    pval = 2 * sps.t.sf(np.abs(tstat), df_total)

    out = pd.DataFrame(
        {
            "logFC": logfc,
            "AveExpr": expr.mean(axis=1).to_numpy(),
            "t": tstat,
            "P.Value": pval,
            "adj.P.Val": bh_adjust(pval),
        },
        index=expr.index,
    )
    return out.sort_values("P.Value")


def hypergeom_ora(
    hits: set[str], universe: set[str], gene_sets: dict[str, set[str]],
    p_threshold: float = 0.05,
) -> pd.DataFrame:
    """Over-representation analysis via hypergeometric test + BH."""
    hits = set(hits) & set(universe)
    rows = []
    for name, members in gene_sets.items():
        members = set(members) & set(universe)
        if not members:
            continue
        overlap = hits & members
        k, K, n, N = len(overlap), len(members), len(hits), len(universe)
        if k == 0:
            continue
        p = sps.hypergeom.sf(k - 1, N, K, n)
        rows.append(
            {
                "term": name,
                "overlap": k,
                "set_size": K,
                "gene_ratio": k / max(n, 1),
                "pvalue": p,
                "genes": ";".join(sorted(overlap)),
            }
        )
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df["p.adjust"] = bh_adjust(df["pvalue"].to_numpy())
    df = df.sort_values("pvalue").reset_index(drop=True)
    return df[df["pvalue"] < p_threshold].reset_index(drop=True)


def ssgsea_scores(
    expr: pd.DataFrame, signatures: dict[str, set[str]], alpha: float = 0.25
) -> pd.DataFrame:
    """Single-sample GSEA (Barbie et al. 2009) — signatures x samples scores.

    Scores are normalized by the range across the full score matrix,
    matching the common GSVA `ssgsea.norm=TRUE` behaviour.
    """
    genes = expr.index.to_numpy()
    n = len(genes)
    # rank genes per sample (descending expression -> rank n..1)
    ranks = expr.rank(axis=0, method="average").to_numpy()
    scores = np.zeros((len(signatures), expr.shape[1]))
    sig_names = list(signatures)
    for si, name in enumerate(sig_names):
        members = np.isin(genes, list(signatures[name]))
        if members.sum() == 0:
            continue
        for j in range(expr.shape[1]):
            order = np.argsort(-ranks[:, j])          # descending rank order
            in_set = members[order]
            r = ranks[order, j]
            w = np.abs(r) ** alpha
            p_hit = np.cumsum(np.where(in_set, w, 0.0))
            denom_hit = p_hit[-1] if p_hit[-1] > 0 else 1.0
            p_hit /= denom_hit
            p_miss = np.cumsum(~in_set) / max(n - in_set.sum(), 1)
            scores[si, j] = np.sum(p_hit - p_miss)
    df = pd.DataFrame(scores, index=sig_names, columns=expr.columns)
    rng = df.to_numpy().max() - df.to_numpy().min()
    return df / rng if rng > 0 else df
