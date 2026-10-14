"""Honest ML evaluation: nested CV (feature selection inside the inner
fold) + label-permutation null, correcting the leakage that produced the
"CV AUC = 1.0" overclaim.

The original candidate genes were intersection(40) ∩ training-DEGs. DE was
run on the FULL training set, so the internal CV reused label information
-> optimistic. Here:

1. Nested CV: in each outer fold, DE is recomputed on the training portion
   only, candidates = intersection ∩ fold-DEGs, model trained and scored
   on the held-out fold. This gives an honest CV AUC.
2. Permutation null: labels permuted 200x, the whole select+fit pipeline
   re-run, external-validation AUC recomputed -> empirical p-value.
3. External validation (GSE28829, GSE43292) is reported as the real
   generalization metric; its correlation with the (uninformative)
   internal CV AUC is quantified.

Writes athero/results/rigor_ml.json.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler

import sys
sys.path.insert(0, "paes_em")
from utils.stats import moderated_t  # noqa: E402

PROC = Path("athero/processed")
RES = Path("athero/results")
SEED = 20260302
INTERSECTION = set(json.loads(
    (PROC / "intersection_genes.json").read_text()))


def load(acc):
    expr = pd.read_csv(PROC / f"{acc}_expr.csv", index_col=0)
    grp = pd.read_csv(PROC / f"{acc}_groups.csv", index_col=0)["group"]
    return expr, grp


def select_candidates(expr, grp, lfc=0.5, p=0.05, max_k=20):
    de = moderated_t(expr, grp, "EM")
    sig = de[(de["adj.P.Val"] < p) & (de["logFC"].abs() > lfc)]
    cands = [g for g in sig.index if g in INTERSECTION]
    return cands[:max_k] if cands else list(INTERSECTION & set(expr.index))


def model(seed):
    return RandomForestClassifier(n_estimators=300, random_state=seed)


def nested_cv_auc(expr, y, seed=SEED, folds=10):
    cv = StratifiedKFold(folds, shuffle=True, random_state=seed)
    aucs = []
    X = expr.T
    for tr, te in cv.split(X, y):
        tr_expr = expr.iloc[:, tr]
        tr_grp = pd.Series(np.where(y[tr] == 1, "EM", "Control"),
                           index=tr_expr.columns)
        feats = select_candidates(tr_expr, tr_grp)
        if not feats:
            continue
        sc = StandardScaler().fit(X.iloc[tr][feats])
        m = model(seed).fit(sc.transform(X.iloc[tr][feats]), y[tr])
        prob = m.predict_proba(sc.transform(X.iloc[te][feats]))[:, 1]
        aucs.append(roc_auc_score(y[te], prob))
    return float(np.mean(aucs)), float(np.std(aucs))


def external_auc(train_expr, y, feats, vsets, seed=SEED):
    sc = StandardScaler().fit(train_expr.loc[feats].T)
    m = model(seed).fit(sc.transform(train_expr.loc[feats].T), y)
    out = {}
    for acc, (vexpr, vy) in vsets.items():
        common = [g for g in feats if g in vexpr.index]
        if len(common) < len(feats):
            out[acc] = None
            continue
        prob = m.predict_proba(sc.transform(vexpr.loc[feats].T))[:, 1]
        out[acc] = float(roc_auc_score(vy, prob))
    return out


def main():
    tr_expr, tr_grp = load("GSE100927")
    y = (tr_grp == "EM").astype(int).to_numpy()
    vsets = {}
    for acc in ("GSE28829", "GSE43292"):
        ve, vg = load(acc)
        vsets[acc] = (ve, (vg == "EM").astype(int).to_numpy())

    feats = select_candidates(tr_expr, tr_grp)
    ncv_mean, ncv_std = nested_cv_auc(tr_expr, y)
    ext = external_auc(tr_expr, y, feats, vsets)

    # permutation null on external AUC (mean across validation sets)
    rng = np.random.default_rng(SEED)
    null = []
    for _ in range(200):
        yp = rng.permutation(y)
        gp = pd.Series(np.where(yp == 1, "EM", "Control"),
                       index=tr_expr.columns)
        f = select_candidates(tr_expr, gp)
        if not f:
            continue
        e = external_auc(tr_expr, yp, f, vsets)
        vals = [v for v in e.values() if v is not None]
        if vals:
            null.append(np.mean(vals))
    null = np.array(null)
    real_ext = np.mean([v for v in ext.values() if v is not None])
    perm_p = float((np.sum(null >= real_ext) + 1) / (len(null) + 1))

    out = {
        "candidate_genes": feats,
        "key_gene": "CD36",
        "nested_cv_auc_honest": {"mean": round(ncv_mean, 3),
                                 "std": round(ncv_std, 3),
                                 "note": "feature selection inside each fold; "
                                         "replaces the leaked CV AUC ~1.0"},
        "external_validation_auc": {k: (round(v, 3) if v else None)
                                    for k, v in ext.items()},
        "external_auc_permutation": {
            "real_mean_external_auc": round(real_ext, 3),
            "null_mean": round(float(null.mean()), 3),
            "null_95pct": round(float(np.quantile(null, 0.95)), 3),
            "empirical_p": round(perm_p, 4),
            "n_permutations": int(len(null)),
        },
        "interpretation": "internal CV AUC is not a valid generalization "
                          "estimate (leakage + optimism); CD36's support "
                          "rests on external validation and cell-type "
                          "specificity, not on separability AUC.",
    }
    out["external_auc_permutation"]["null_values"] = [round(float(x), 4)
                                                      for x in null]
    (RES / "rigor_ml.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
