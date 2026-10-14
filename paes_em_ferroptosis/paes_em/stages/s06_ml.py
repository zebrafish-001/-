"""Stage 6 — machine-learning screening of the key gene.

The paper screens 12 algorithm families (82 combinations) with 10-fold CV
and keeps RF + Lasso + XGBoost to pick the hub gene (ARF6). Here:

1. candidate features = (PAEs∩EM∩FRGs) ∪ significant-WGCNA-module genes,
   restricted to the training DEG table's tested genes;
2. every configured algorithm is scored by 10-fold CV AUC on the training
   set (the "82 combinations" grid collapses to its algorithm axis —
   extend ``_grid()`` for full hyper-parameter sweeps);
3. the three final selectors each rank features (RF impurity importance,
   |Lasso coef| > 0, XGBoost gain — gradient boosting fallback when the
   xgboost package is absent);
4. hub gene(s) = intersection of the three top-k rankings, validated by
   single-gene AUC on both validation datasets.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn import (discriminant_analysis, ensemble, linear_model,
                     naive_bayes, neighbors, neural_network, svm)
from sklearn.feature_selection import RFE
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler

from ..config import RunContext
from ..utils.io import load_json, save_json, save_table
from .s01_intake import load_dataset


def _algorithms(seed: int) -> dict:
    algs = {
        "lasso": linear_model.LogisticRegression(
            solver="liblinear", l1_ratio=1.0, C=0.5, random_state=seed),
        "elastic_net": linear_model.LogisticRegression(
            solver="saga", l1_ratio=0.5, C=0.5,
            max_iter=5000, random_state=seed),
        "ridge": linear_model.LogisticRegression(C=1.0, max_iter=5000,
                                                 random_state=seed),
        "random_forest": ensemble.RandomForestClassifier(
            n_estimators=300, random_state=seed),
        "extra_trees": ensemble.ExtraTreesClassifier(
            n_estimators=300, random_state=seed),
        "gbm": ensemble.GradientBoostingClassifier(random_state=seed),
        "svm_rfe": svm.SVC(kernel="linear", random_state=seed),
        "knn": neighbors.KNeighborsClassifier(),
        "naive_bayes": naive_bayes.GaussianNB(),
        "lda": discriminant_analysis.LinearDiscriminantAnalysis(),
        "mlp": neural_network.MLPClassifier(
            hidden_layer_sizes=(32,), max_iter=2000, random_state=seed),
    }
    try:
        from xgboost import XGBClassifier
        algs["xgboost"] = XGBClassifier(
            n_estimators=300, eval_metric="logloss", random_state=seed)
    except ImportError:  # gradient boosting stands in for XGBoost
        algs["xgboost"] = ensemble.GradientBoostingClassifier(
            n_estimators=300, random_state=seed)
    return algs


def _rank_features(name, model, x, y, feats, k) -> list[str]:
    if name == "lasso":
        model.fit(x, y)
        coef = np.abs(model.coef_).ravel()
        nz = [f for f, c in zip(feats, coef) if c > 1e-8]
        return sorted(nz, key=lambda f: -coef[feats.index(f)])[:k]
    if name == "svm_rfe":
        rfe = RFE(model, n_features_to_select=min(k, len(feats))).fit(x, y)
        return [f for f, s in zip(feats, rfe.support_) if s]
    model.fit(x, y)
    imp = getattr(model, "feature_importances_", None)
    if imp is None:
        imp = np.abs(getattr(model, "coef_", np.zeros((1, len(feats))))).ravel()
    order = np.argsort(-imp)[:k]
    return [feats[i] for i in order]


def run(ctx: RunContext) -> dict:
    cfg = ctx.cfg["machine_learning"]
    acc = ctx.cfg["datasets"]["training"][0]["accession"]
    expr = pd.read_csv(ctx.processed / f"{acc}_expr.csv", index_col=0)
    groups = pd.read_csv(ctx.processed / f"{acc}_groups.csv",
                         index_col=0)["group"]

    inter = set(load_json(ctx.processed / "intersection_genes.json"))
    wgcna = set(load_json(ctx.processed / "wgcna_key_genes.json")) \
        if (ctx.processed / "wgcna_key_genes.json").exists() else set()
    degs = set(load_json(ctx.processed / "degs.json")) \
        if (ctx.processed / "degs.json").exists() else set()
    cands = sorted((inter | (inter & wgcna)) & set(expr.index))
    cands = sorted(set(cands) & degs) or cands   # prefer DE-supported genes
    if not cands:
        raise RuntimeError("no candidate genes — run stages 2-4 first")

    feats = list(cands)
    x = StandardScaler().fit_transform(expr.loc[feats].T.to_numpy())
    y = (groups == "EM").astype(int).to_numpy()
    cv = StratifiedKFold(cfg["cv_folds"], shuffle=True, random_state=ctx.seed)

    # ---- benchmark all 12 algorithms by CV AUC -------------------------
    vsets = {}
    for d in ctx.cfg["datasets"]["validation"]:
        vacc = d["accession"]
        vexpr = pd.read_csv(ctx.processed / f"{vacc}_expr.csv", index_col=0)
        vgroups = pd.read_csv(ctx.processed / f"{vacc}_groups.csv",
                              index_col=0)["group"]
        vsets[vacc] = (vexpr, (vgroups == "EM").astype(int).to_numpy())

    scaler = StandardScaler().fit(expr.loc[feats].T.to_numpy())
    bench = []
    algs = _algorithms(ctx.seed)
    for name in cfg["algorithms"]:
        model = algs[name]
        auc = cross_val_score(model, x, y, cv=cv, scoring="roc_auc").mean()
        row = {"algorithm": name, "cv_auc": round(float(auc), 4)}
        model.fit(x, y)
        for vacc, (vexpr, vy) in vsets.items():
            common = [g for g in feats if g in vexpr.index]
            if len(common) < len(feats):
                row[f"auc_{vacc}"] = None
                continue
            vx = scaler.transform(vexpr.loc[feats].T.to_numpy())
            if hasattr(model, "predict_proba"):
                score = model.predict_proba(vx)[:, 1]
            else:
                score = model.decision_function(vx)
            row[f"auc_{vacc}"] = round(float(roc_auc_score(vy, score)), 4)
        bench.append(row)
    bench_df = pd.DataFrame(bench).sort_values("cv_auc", ascending=False)
    save_table(bench_df, ctx.results / "s06_algorithm_benchmark.csv",
               index=False)

    # ---- final selectors -> consensus hub gene -------------------------
    k = min(cfg["n_top_features"], len(feats))
    rankings = {
        name: _rank_features(name, algs[name], x, y, feats, k)
        for name in cfg["final_selectors"]
    }
    consensus = set(feats)
    for sel in rankings.values():
        consensus &= set(sel)
    # order consensus genes by mean rank across selectors
    def mean_rank(g):
        return np.mean([r.index(g) for r in rankings.values()])
    hub_genes = sorted(consensus, key=mean_rank)

    # ---- validate hub genes on validation datasets ---------------------
    validation = {}
    for d in ctx.cfg["datasets"]["validation"]:
        vacc = d["accession"]
        vexpr = pd.read_csv(ctx.processed / f"{vacc}_expr.csv", index_col=0)
        vgroups = pd.read_csv(ctx.processed / f"{vacc}_groups.csv",
                              index_col=0)["group"]
        vy = (vgroups == "EM").astype(int).to_numpy()
        validation[vacc] = {
            g: round(float(roc_auc_score(vy, vexpr.loc[g].to_numpy())), 4)
            for g in hub_genes[:5] if g in vexpr.index
        }

    out = {
        "n_candidates": len(feats),
        "candidate_genes": feats,
        "benchmark_top3": bench_df.head(3).to_dict("records"),
        "selector_rankings": {k_: v[:10] for k_, v in rankings.items()},
        "hub_genes": hub_genes,
        "key_gene": hub_genes[0] if hub_genes else None,
        "validation_auc": validation,
    }
    save_json(out, ctx.results / "s06_ml.json")
    save_json(hub_genes, ctx.processed / "hub_genes.json")
    return out
