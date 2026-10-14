#!/usr/bin/env python
"""Collect real target/gene sets for the plasticizer–atherosclerosis study.

Outputs into <raw_dir>:
  frgs_ferrdb.json          ferroptosis genes (FerrDb driver+suppressor+marker)
  paes_targets.json         union of compound targets (ChEMBL + CTD, human)
  em_targets.json           disease targets (OpenTargets MONDO_0005311 + KEGG
                            hsa05417)  [key name kept for pipeline compat]
  annotation_gene_sets.json Enrichr GO BP/MF/CC + KEGG 2021 GMTs
  immune_signatures_28.json Charoentong Table S6 (28 cell types)
  target_provenance.json    per-source counts + parameters

Usage: python scripts/collect_targets.py <raw_dir>
"""

from __future__ import annotations

import gzip
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

import openpyxl

COMPOUNDS = {  # abbrev -> (CTD/match names lowercase fragments, CAS)
    "DEHP": (["diethylhexyl phthalate"], "117-81-7"),
    "DBP": (["dibutyl phthalate"], "84-74-2"),
    "BBP": (["benzyl butyl phthalate", "butylbenzyl phthalate"], "85-68-7"),
    "DEP": (["diethyl phthalate"], "84-66-2"),
    "DMP": (["dimethyl phthalate"], "131-11-3"),
    "DIBP": (["diisobutyl phthalate"], "84-69-5"),
    "DINP": (["diisononyl phthalate"], "28553-12-0"),
    "DEHT": (["dioctyl terephthalate", "diethylhexyl terephthalate"],
             "6422-86-2"),
    "DINCH": (["cyclohexane-1,2-dicarboxylic acid diisononyl",
               "diisononyl cyclohexane"], "166412-78-8"),
    "DEHA": (["diethylhexyl adipate", "dioctyl adipate"], "103-23-1"),
    "ATBC": (["acetyl tributyl citrate", "acetyltributyl citrate",
              "tributyl acetylcitrate"], "77-90-7"),
    "TOTM": (["triethylhexyl trimellitate", "trioctyl trimellitate",
              "tris(2-ethylhexyl) trimellitate"], "3319-31-1"),
}
CHEMBL_IDS = {
    "DEHP": "CHEMBL1242017", "DBP": "CHEMBL272485", "BBP": "CHEMBL1450327",
    "DEP": "CHEMBL388558", "DMP": "CHEMBL323348", "DIBP": "CHEMBL1370662",
    "DINP": "CHEMBL1905899", "DEHT": "CHEMBL1871770",
    "DINCH": "CHEMBL3182578", "DEHA": "CHEMBL1414950",
    "ATBC": "CHEMBL1904556", "TOTM": "CHEMBL1425782",
}
SYMBOL_RE = re.compile(r"^[A-Z0-9][A-Z0-9-]{1,14}$")


def get_json(url, data=None, headers=None, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(
                url, data=data,
                headers={"User-Agent": "paes-pipeline/0.1",
                         **(headers or {})})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception:
            if i == retries - 1:
                raise
            time.sleep(2 ** i)


# ------------------------------------------------------------- FerrDb ----
def ferrdb(raw: Path) -> list[str]:
    genes = set()
    for t in ("driver", "suppressor", "marker"):
        d = json.loads((raw / f"ferrdb_v3_{t}.json").read_text())
        for row in d.values():
            s = (row.get("Symbol") or "").strip()
            if SYMBOL_RE.match(s):
                genes.add(s)
    return sorted(genes)


# ------------------------------------------------------------- ChEMBL ----
def chembl_targets() -> tuple[set[str], dict]:
    genes, per = set(), {}
    tcache: dict[str, list[str]] = {}
    for ab, chid in CHEMBL_IDS.items():
        tids = set()
        offset = 0
        while True:
            d = get_json("https://www.ebi.ac.uk/chembl/api/data/activity.json"
                         f"?molecule_chembl_id={chid}&limit=100&offset={offset}")
            for a in d["activities"]:
                if a.get("target_chembl_id"):
                    tids.add(a["target_chembl_id"])
            if not d["page_meta"]["next"]:
                break
            offset += 100
        syms = set()
        for tid in tids:
            if tid not in tcache:
                t = get_json("https://www.ebi.ac.uk/chembl/api/data/"
                             f"target/{tid}.json")
                out = []
                if t.get("organism") == "Homo sapiens":
                    for comp in t.get("target_components", []):
                        for syn in comp.get("target_component_synonyms", []):
                            if syn.get("syn_type") == "GENE_SYMBOL":
                                out.append(syn["component_synonym"])
                tcache[tid] = out
                time.sleep(0.15)
            syms.update(tcache[tid])
        syms = {s for s in syms if SYMBOL_RE.match(s)}
        per[ab] = sorted(syms)
        genes |= syms
        print(f"  ChEMBL {ab}: {len(tids)} targets -> {len(syms)} "
              "human genes")
    return genes, per


# ---------------------------------------------------------------- CTD ----
def ctd_targets(raw: Path) -> tuple[set[str], dict]:
    cas_of = {cas: ab for ab, (_, cas) in COMPOUNDS.items()}
    name_frags = [(frag, ab) for ab, (frags, _) in COMPOUNDS.items()
                  for frag in frags]
    genes, per = set(), {ab: set() for ab in COMPOUNDS}
    with gzip.open(raw / "CTD_chem_gene_ixns.tsv.gz", "rt",
                   errors="replace") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            p = line.rstrip("\n").split("\t")
            if len(p) < 7 or p[6] != "Homo sapiens":
                continue
            name, cas, sym = p[0].lower(), p[2], p[3]
            ab = cas_of.get(cas)
            if ab is None:
                for frag, ab2 in name_frags:
                    if frag in name:
                        ab = ab2
                        break
            if ab and SYMBOL_RE.match(sym):
                per[ab].add(sym)
                genes.add(sym)
    for ab in per:
        per[ab] = sorted(per[ab])
        print(f"  CTD {ab}: {len(per[ab])} human genes")
    return genes, per


# ------------------------------------------------- disease targets -------
def opentargets(mondo="MONDO_0005311", min_score=0.1) -> dict[str, float]:
    out = {}
    index = 0
    while True:
        q = {"query": """
            query($id: String!, $index: Int!) {
              disease(efoId: $id) {
                associatedTargets(page: {index: $index, size: 500}) {
                  count rows { score target { approvedSymbol } }
                }}}""",
             "variables": {"id": mondo, "index": index}}
        d = get_json("https://api.platform.opentargets.org/api/v4/graphql",
                     data=json.dumps(q).encode(),
                     headers={"Content-Type": "application/json"})
        at = d["data"]["disease"]["associatedTargets"]
        for row in at["rows"]:
            out[row["target"]["approvedSymbol"]] = row["score"]
        index += 1
        if index * 500 >= at["count"]:
            break
        time.sleep(0.3)
    return {g: s for g, s in out.items() if s >= min_score}


def kegg_pathway_genes(pid="hsa05417") -> list[str]:
    req = urllib.request.Request(f"https://rest.kegg.jp/get/{pid}")
    with urllib.request.urlopen(req, timeout=60) as r:
        txt = r.read().decode()
    genes, in_gene = [], False
    for line in txt.splitlines():
        if line.startswith("GENE"):
            in_gene = True
            line = line[4:]
        elif in_gene and not line.startswith(" "):
            break
        if in_gene:
            m = re.search(r"\d+\s+([A-Z0-9-]+);", line)
            if m:
                genes.append(m.group(1))
    return sorted(set(genes))


# ----------------------------------------------------- annotation sets ---
def enrichr_gmts(raw: Path) -> dict[str, list[str]]:
    sets = {}
    prefix = {"GO_Biological_Process_2023": "GO_BP",
              "GO_Molecular_Function_2023": "GO_MF",
              "GO_Cellular_Component_2023": "GO_CC",
              "KEGG_2021_Human": "KEGG"}
    for lib, pre in prefix.items():
        for line in (raw / f"{lib}.gmt").read_text().splitlines():
            parts = line.rstrip().split("\t")
            if len(parts) < 3:
                continue
            term = re.sub(r"\s*\(GO:\d+\)$", "", parts[0])
            sets[f"{pre}::{term}"] = sorted(
                {g.strip() for g in parts[2:] if g.strip()})
    return sets


# -------------------------------------------------- immune signatures ----
def charoentong(raw: Path) -> dict[str, list[str]]:
    wb = openpyxl.load_workbook(raw / "charoentong_mmc3.xlsx",
                                read_only=True)
    ws = wb["Sheet1"]
    sigs: dict[str, set[str]] = {}
    header_seen = False
    for row in ws.iter_rows(values_only=True):
        if not header_seen:
            if row and row[0] == "Metagene":
                header_seen = True
            continue
        if not row or not row[0] or not row[1]:
            continue
        gene, ct = str(row[0]).strip(), str(row[1]).strip()
        if SYMBOL_RE.match(gene):
            sigs.setdefault(ct, set()).add(gene)
    return {k: sorted(v) for k, v in sigs.items()}


def main(raw: Path):
    prov = {}

    frgs = ferrdb(raw)
    (raw / "frgs_ferrdb.json").write_text(json.dumps(frgs, indent=1))
    prov["frgs"] = {"source": "FerrDb (driver+suppressor+marker)",
                    "n": len(frgs)}
    print(f"FRGs: {len(frgs)}")

    print("ChEMBL targets ...")
    ch_genes, ch_per = chembl_targets()
    print("CTD targets ...")
    ctd_genes, ctd_per = ctd_targets(raw)
    paes = sorted(ch_genes | ctd_genes)
    (raw / "paes_targets.json").write_text(json.dumps(paes, indent=1))
    (raw / "paes_targets_by_compound.json").write_text(json.dumps(
        {ab: sorted(set(ch_per.get(ab, [])) | set(ctd_per.get(ab, [])))
         for ab in COMPOUNDS}, indent=1))
    prov["paes_targets"] = {"chembl": len(ch_genes), "ctd": len(ctd_genes),
                            "union": len(paes),
                            "n_compounds": len(COMPOUNDS)}
    print(f"PAEs targets union: {len(paes)} "
          f"(ChEMBL {len(ch_genes)}, CTD {len(ctd_genes)})")

    print("OpenTargets disease targets ...")
    ot = opentargets()
    kegg = kegg_pathway_genes()
    disease = sorted(set(ot) | set(kegg))
    (raw / "em_targets.json").write_text(json.dumps(disease, indent=1))
    prov["disease_targets"] = {
        "opentargets_MONDO_0005311_score>=0.1": len(ot),
        "kegg_hsa05417": len(kegg), "union": len(disease)}
    print(f"Disease targets: {len(disease)} "
          f"(OpenTargets {len(ot)}, KEGG {len(kegg)})")

    sets = enrichr_gmts(raw)
    (raw / "annotation_gene_sets.json").write_text(json.dumps(sets))
    prov["annotation_sets"] = {"n_terms": len(sets)}
    print(f"Annotation terms: {len(sets)}")

    sigs = charoentong(raw)
    (raw / "immune_signatures_28.json").write_text(json.dumps(sigs, indent=1))
    prov["immune_signatures"] = {"n_cell_types": len(sigs),
                                 "source": "Charoentong 2017 Table S6"}
    print(f"Immune signatures: {len(sigs)} cell types")

    (raw / "target_provenance.json").write_text(json.dumps(prov, indent=2))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
