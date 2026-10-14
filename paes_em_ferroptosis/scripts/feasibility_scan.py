"""Rapid feasibility scan for (exposure x disease x mechanism) triples.

For each candidate, computes the intersection-specificity permutation — the
one control that held up for the plasticizer study (p=0.001, 4.76x) — using
CTD exposure targets, OpenTargets disease targets, and a mechanism gene set.
Candidates are ranked by enrichment fold over a size-matched random null,
so promiscuous ('pan-tox') chemicals with huge target sets are penalized
automatically.

Primary metric: enrichment fold + empirical p of the 3-way intersection.
Secondary: intersection size, exposure target-set size (specificity).

Writes scan/feasibility_scan.csv + .json.
"""

from __future__ import annotations

import gzip
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

CTD = Path("athero/raw/CTD_chem_gene_ixns.tsv.gz")
GSDIR = Path("scan/genesets")
OUT = Path("scan")
SYM = re.compile(r"^[A-Z0-9][A-Za-z0-9-]{1,14}$")
SEED = 20260302
N_PERM = 1000

# candidate triples: (exposure label, CTD chemical name, disease label,
#                     OpenTargets search term, mechanism geneset)
CANDIDATES = [
    ("Paraquat", "Paraquat", "Parkinson disease", "Parkinson disease", "ferroptosis"),
    ("Paraquat", "Paraquat", "Parkinson disease", "Parkinson disease", "oxidative_stress"),
    ("Rotenone", "Rotenone", "Parkinson disease", "Parkinson disease", "ferroptosis"),
    ("Rotenone", "Rotenone", "Parkinson disease", "Parkinson disease", "mito_dysfunction"),
    ("Cadmium", "Cadmium", "chronic kidney disease", "chronic kidney disease", "ferroptosis"),
    ("Cadmium", "Cadmium", "osteoporosis", "osteoporosis", "ferroptosis"),
    ("Arsenic", "Arsenic", "hepatocellular carcinoma", "hepatocellular carcinoma", "ferroptosis"),
    ("Arsenic", "Arsenic", "urinary bladder cancer", "bladder carcinoma", "oxidative_stress"),
    ("Benzene", "Benzene", "acute myeloid leukemia", "acute myeloid leukemia", "apoptosis"),
    ("PFOA", "Perfluorooctanoic acid", "non-alcoholic fatty liver disease", "non-alcoholic fatty liver disease", "ferroptosis"),
    ("Chlorpyrifos", "Chlorpyrifos", "Parkinson disease", "Parkinson disease", "oxidative_stress"),
    ("Bisphenol A", "bisphenol A", "polycystic ovary syndrome", "polycystic ovary syndrome", "oxidative_stress"),
    # baseline for calibration
    ("DEHP(baseline)", "Diethylhexyl Phthalate", "atherosclerosis", "atherosclerosis", "ferroptosis"),
]


def ctd_universe_and_targets():
    """Return (universe set, {chemical_lower: set(genes)}) for needed chems."""
    needed = {c[1].lower() for c in CANDIDATES}
    universe = set()
    targets = {c: set() for c in needed}
    with gzip.open(CTD, "rt", errors="replace") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            p = line.rstrip("\n").split("\t")
            if len(p) < 7 or p[6] != "Homo sapiens":
                continue
            sym = p[3]
            if not SYM.match(sym):
                continue
            universe.add(sym)
            chem = p[0].lower()
            if chem in targets:
                targets[chem].add(sym)
    return universe, targets


def opentargets(term, min_score=0.1, cache={}):
    if term in cache:
        return cache[term]
    # resolve id
    q = {"query": "query($q:String!){search(queryString:$q,entityNames:[\"disease\"],page:{index:0,size:1}){hits{id name}}}",
         "variables": {"q": term}}
    hits = _gql(q)["data"]["search"]["hits"]
    if not hits:
        cache[term] = (None, set())
        return cache[term]
    did = hits[0]["id"]
    genes = {}
    idx = 0
    while True:
        q = {"query": "query($id:String!,$i:Int!){disease(efoId:$id){associatedTargets(page:{index:$i,size:500}){count rows{score target{approvedSymbol}}}}}",
             "variables": {"id": did, "i": idx}}
        at = _gql(q)["data"]["disease"]["associatedTargets"]
        for r in at["rows"]:
            genes[r["target"]["approvedSymbol"]] = r["score"]
        idx += 1
        if idx * 500 >= at["count"] or idx > 6:
            break
        time.sleep(0.2)
    g = {x for x, s in genes.items() if s >= min_score and SYM.match(x)}
    cache[term] = (did, g)
    return cache[term]


def _gql(q, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(
                "https://api.platform.opentargets.org/api/v4/graphql",
                data=json.dumps(q).encode(),
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(2 ** i)


def main():
    OUT.mkdir(exist_ok=True)
    print("loading CTD ...")
    universe, ctd = ctd_universe_and_targets()
    uni = np.array(sorted(universe))
    rng = np.random.default_rng(SEED)
    genesets = {p.stem: set(json.loads(p.read_text()))
                for p in GSDIR.glob("*.json")}

    rows = []
    for exp, chem, dis, oterm, mech in CANDIDATES:
        exp_t = ctd[chem.lower()] & universe
        did, dis_t = opentargets(oterm)
        dis_t &= universe
        mech_g = genesets[mech] & universe
        bg = dis_t & mech_g
        obs = len(exp_t & bg)
        n = len(exp_t)
        if n == 0 or not bg:
            rows.append({"exposure": exp, "disease": dis, "mechanism": mech,
                         "n_exposure": n, "n_disease": len(dis_t),
                         "n_mech": len(mech_g), "intersection": obs,
                         "fold": None, "perm_p": None})
            continue
        null = np.array([len(set(rng.choice(uni, n, replace=False)) & bg)
                         for _ in range(N_PERM)])
        fold = obs / max(null.mean(), 1e-9)
        p = (np.sum(null >= obs) + 1) / (N_PERM + 1)
        rows.append({
            "exposure": exp, "disease": dis, "mechanism": mech,
            "n_exposure": n, "n_disease": len(dis_t), "n_mech": len(mech_g),
            "intersection": obs, "null_mean": round(float(null.mean()), 2),
            "fold": round(float(fold), 2), "perm_p": round(float(p), 4),
        })
        print(f"{exp:14s} x {dis:28s} x {mech:16s} "
              f"n_exp={n:5d} inter={obs:3d} fold={fold:4.1f} p={p:.4f}")
    df = pd.DataFrame(rows)
    df = df.sort_values("fold", ascending=False, na_position="last")
    df.to_csv(OUT / "feasibility_scan.csv", index=False)
    (OUT / "feasibility_scan.json").write_text(
        df.to_json(orient="records", indent=1))
    print("\nTop by enrichment fold:")
    print(df.head(6).to_string(index=False))


if __name__ == "__main__":
    main()
