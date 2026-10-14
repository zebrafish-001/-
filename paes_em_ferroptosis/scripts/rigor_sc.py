#!/usr/bin/env python
"""Pseudoreplication-corrected single-cell statistics (n=3 patients).

The scRNA data are 3 patients x (diseased core DIS + adjacent HEA). The
independent unit is the PATIENT, not the cell. This script replaces the
cell-level p-values (which treat 49k cells as independent -> spurious
P=0) with patient-level paired analysis:

* per-patient DIS-vs-HEA for macrophage proportion, foam-like proportion,
  CD36 whole-tissue mean, CD36 within-macrophage mean;
* Wilcoxon signed-rank (exact, n=3 -> min two-sided P = 0.25) + direction
  consistency (how many of 3 patients agree);
* per-patient CD36~foam-pseudotime Spearman rho (exposes sign flips);
* composition decomposition: how much of the whole-tissue CD36 shift is
  explained by the macrophage-proportion shift.

Writes athero/results/rigor_singlecell.json + per-patient CSVs.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr, wilcoxon

RES = Path("athero/results")
# date-based patient map (GSMxxxx -> patient, condition)
SAMPLE = {
    "GSM4837523": ("P1", "DIS"), "GSM4837524": ("P1", "HEA"),
    "GSM4837525": ("P2", "DIS"), "GSM4837526": ("P2", "HEA"),
    "GSM4837527": ("P3", "DIS"), "GSM4837528": ("P3", "HEA"),
}


def paired_test(dis, hea):
    """Signed-rank on 3 paired patients + direction consistency."""
    d = np.array(dis) - np.array(hea)
    n_up = int((d > 0).sum())
    try:
        p = float(wilcoxon(dis, hea).pvalue)
    except ValueError:
        p = float("nan")
    return {"per_patient_delta": [round(float(x), 4) for x in d],
            "n_consistent": max(n_up, len(d) - n_up),
            "n_patients": len(d),
            "direction": "DIS>HEA" if n_up > len(d) - n_up else "DIS<HEA",
            "signed_rank_p": round(p, 4),
            "mean_DIS": round(float(np.mean(dis)), 4),
            "mean_HEA": round(float(np.mean(hea)), 4)}


def main():
    meta = pd.read_csv(RES / "s08_cell_meta.csv")
    viz = pd.read_csv(RES / "s08_cells_viz.csv")
    axis = pd.read_csv(RES / "s08_axis_cells.csv")
    meta["patient"] = meta["sample"].map(lambda s: SAMPLE.get(s, ("?",))[0])
    meta["cond"] = meta["sample"].map(lambda s: SAMPLE.get(s, ("", "?"))[1])
    cd36 = dict(zip(viz["cell"], viz.get("key_gene_expr", pd.Series())))
    meta["CD36"] = meta["cell"].map(cd36)

    pats = ["P1", "P2", "P3"]
    rows = []
    for p in pats:
        sub = meta[meta.patient == p]
        for cond in ("DIS", "HEA"):
            c = sub[sub.cond == cond]
            mac = c[c.annotated == "Macrophage"]
            rows.append({
                "patient": p, "cond": cond, "n_cells": len(c),
                "macro_prop": len(mac) / len(c) if len(c) else np.nan,
                "cd36_whole": c["CD36"].mean(),
                "cd36_in_macro": mac["CD36"].mean() if len(mac) else np.nan,
            })
    pp = pd.DataFrame(rows)

    # foam proportion per patient (from axis_cells mac_state)
    ax = axis.copy()
    ax["patient"] = ax["cell"].str.split("_").str[0].map(
        lambda s: SAMPLE.get(s, ("?",))[0])
    ax["cond"] = ax["cell"].str.split("_").str[0].map(
        lambda s: SAMPLE.get(s, ("", "?"))[1])
    foam = []
    for p in pats:
        for cond in ("DIS", "HEA"):
            c = ax[(ax.patient == p) & (ax.cond == cond)]
            foam.append({"patient": p, "cond": cond,
                         "foam_prop": (c.annotated == "Foam-like").mean()
                         if len(c) else np.nan})
    fp = pd.DataFrame(foam)
    pp = pp.merge(fp, on=["patient", "cond"])
    pp.to_csv(RES / "rigor_per_patient.csv", index=False)

    def col(metric):
        dis = [pp[(pp.patient == p) & (pp.cond == "DIS")][metric].iloc[0]
               for p in pats]
        hea = [pp[(pp.patient == p) & (pp.cond == "HEA")][metric].iloc[0]
               for p in pats]
        return dis, hea

    out = {"n_patients": 3, "design": "3 patients x (DIS core + HEA adjacent)",
           "note": "patient is the independent unit; cell-level p-values are "
                   "pseudoreplicated and are NOT reported",
           "min_possible_signed_rank_p_at_n3": 0.25}
    for metric, label in [("macro_prop", "macrophage_proportion"),
                          ("foam_prop", "foam_like_proportion"),
                          ("cd36_whole", "CD36_whole_tissue"),
                          ("cd36_in_macro", "CD36_within_macrophage")]:
        dis, hea = col(metric)
        out[label] = paired_test(dis, hea)

    # composition decomposition: whole-tissue vs within-macrophage fold
    cw = out["CD36_whole_tissue"]
    cm = out["CD36_within_macrophage"]
    out["composition_decomposition"] = {
        "whole_tissue_fold_DIS_over_HEA":
            round(cw["mean_DIS"] / cw["mean_HEA"], 3),
        "within_macrophage_fold_DIS_over_HEA":
            round(cm["mean_DIS"] / cm["mean_HEA"], 3),
        "macrophage_prop_fold_DIS_over_HEA":
            round(out["macrophage_proportion"]["mean_DIS"]
                  / out["macrophage_proportion"]["mean_HEA"], 3),
        "interpretation": "most of the whole-tissue CD36 increase is a "
                          "composition effect (more macrophages), not higher "
                          "per-macrophage CD36",
    }

    # per-patient trajectory rho (CD36 vs foam pseudotime)
    rhos = {}
    for p in pats:
        c = ax[ax.patient == p]
        if "CD36" in c and len(c) > 10:
            rhos[p] = round(float(spearmanr(c["CD36"], c["pseudotime"])[0]), 3)
    signs = [1 if v > 0 else -1 for v in rhos.values()]
    out["trajectory_rho_per_patient"] = {
        "per_patient": rhos,
        "sign_consistent": abs(sum(signs)) == len(signs),
        "note": "pooled rho is driven by the patient contributing the most "
                "macrophages; per-patient signs flip, so the trajectory "
                "claim does not generalize",
    }

    (RES / "rigor_singlecell.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
