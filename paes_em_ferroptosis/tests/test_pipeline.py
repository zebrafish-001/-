"""End-to-end smoke test of the full pipeline on synthetic data, plus
unit checks of the statistical primitives."""

import numpy as np
import pandas as pd
import pytest

from paes_em import synthetic
from paes_em.config import make_context
from paes_em.stages import ORDER
from paes_em.utils.stats import bh_adjust, hypergeom_ora, moderated_t


@pytest.fixture(scope="module")
def ctx(tmp_path_factory):
    root = tmp_path_factory.mktemp("paesdemo")
    c = make_context(root=root, demo=True)
    synthetic.generate_all(c)
    return c


@pytest.fixture(scope="module")
def pipeline_results(ctx):
    summaries = {}
    for name, mod in ORDER:
        summaries[name] = mod.run(ctx)
    return summaries


def test_bh_adjust_monotone():
    p = np.array([0.001, 0.01, 0.02, 0.8])
    adj = bh_adjust(p)
    assert np.all(np.diff(adj[np.argsort(p)]) >= -1e-12)
    assert adj.max() <= 1.0


def test_moderated_t_detects_planted_signal():
    rng = np.random.default_rng(0)
    expr = pd.DataFrame(rng.normal(7, 1, (50, 20)),
                        index=[f"g{i}" for i in range(50)],
                        columns=[f"s{i}" for i in range(20)])
    expr.iloc[0, :10] += 2.0
    groups = pd.Series(["EM"] * 10 + ["Control"] * 10, index=expr.columns)
    res = moderated_t(expr, groups, "EM")
    assert res.index[0] == "g0"
    assert res.iloc[0]["adj.P.Val"] < 0.01


def test_hypergeom_ora_hits_enriched_set():
    universe = {f"g{i}" for i in range(100)}
    hits = {f"g{i}" for i in range(10)}
    sets = {"enriched": {f"g{i}" for i in range(12)},
            "random": {f"g{i}" for i in range(50, 80)}}
    res = hypergeom_ora(hits, universe, sets)
    assert res.iloc[0]["term"] == "enriched"


def test_full_pipeline(pipeline_results, ctx):
    s = pipeline_results
    # network toxicology intersection contains the planted key gene
    assert "ARF6" in s["network_tox"]["intersection_genes"]
    # DE finds the planted ferroptosis signal
    assert s["diffexp"]["n_degs"] > 0
    # ML consensus recovers ARF6 as (one of) the hub gene(s)
    assert "ARF6" in s["ml"]["hub_genes"]
    # validation AUC for the key gene is strong on both validation sets
    for acc, aucs in s["ml"]["validation_auc"].items():
        if "ARF6" in aucs:
            assert aucs["ARF6"] > 0.8, acc
    # single cell: ARF6 enriched on the EMT axis
    assert s["singlecell"]["key_gene_axis_enrichment_p"] < 0.05
    # spatial: lesion enrichment
    assert s["spatial"]["lesion_enrichment_p"] < 0.05
    # virtual KO: FRGs enriched among top perturbed genes
    assert s["knockout"]["frg_enrichment_p"] < 0.05
    # docking: all 7 compounds parsed, threshold applied
    assert s["docking"]["n_docked"] == 7
    assert s["docking"]["n_strong_binders"] >= 1
    # report rendered
    assert (ctx.results / "report.md").exists()
    assert (ctx.results / "report.html").exists()
