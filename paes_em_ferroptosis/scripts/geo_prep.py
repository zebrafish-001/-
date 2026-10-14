#!/usr/bin/env python
"""Parse GEO series matrices into pipeline-ready expr/pheno CSVs.

Usage: python scripts/geo_prep.py <raw_dir> <out_dir>

Handles the three atherosclerosis datasets (platform-specific probe→symbol
mapping and group parsing), collapsing multiple probes per gene by the
probe with the highest mean expression.
"""

from __future__ import annotations

import gzip
import io
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd


def read_series_matrix(path: Path):
    """Return (expr_df probes x samples, characteristics dict, titles)."""
    opener = gzip.open if path.suffix == ".gz" else open
    chars, titles, geo_acc = [], [], []
    table_lines = []
    in_table = False
    with opener(path, "rt", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("!series_matrix_table_begin"):
                in_table = True
                continue
            if line.startswith("!series_matrix_table_end"):
                in_table = False
                continue
            if in_table:
                table_lines.append(line)
            elif line.startswith("!Sample_characteristics_ch1"):
                chars.append([v.strip('"') for v in
                              line.rstrip("\n").split("\t")[1:]])
            elif line.startswith("!Sample_title"):
                titles = [v.strip('"') for v in
                          line.rstrip("\n").split("\t")[1:]]
            elif line.startswith("!Sample_geo_accession"):
                geo_acc = [v.strip('"') for v in
                           line.rstrip("\n").split("\t")[1:]]
    expr = pd.read_csv(io.StringIO("".join(table_lines)), sep="\t",
                       index_col=0)
    expr.columns = geo_acc if geo_acc else expr.columns
    return expr, chars, titles


def gpl570_map(path: Path) -> pd.Series:
    rows = []
    with gzip.open(path, "rt", errors="replace") as fh:
        in_t = False
        header = None
        for line in fh:
            if line.startswith(("!Annotation_table_begin", "!platform_table_begin")):
                in_t = True
                continue
            if line.startswith(("!Annotation_table_end", "!platform_table_end")):
                break
            if in_t:
                parts = line.rstrip("\n").split("\t")
                if header is None:
                    header = parts
                    i_id = header.index("ID")
                    i_sym = header.index("Gene symbol")
                    continue
                if len(parts) > max(i_id, i_sym):
                    rows.append((parts[i_id], parts[i_sym]))
    s = pd.Series(dict(rows))
    return s[s.str.len() > 0]


def full_table_map(path: Path, id_col: str, sym_col: str | None,
                   gene_assignment: bool = False) -> pd.Series:
    """Parse an acc.cgi full platform table into probe->symbol."""
    rows = []
    with open(path, errors="replace") as fh:
        in_t = False
        header = None
        for line in fh:
            if line.startswith("!platform_table_begin"):
                in_t = True
                continue
            if line.startswith("!platform_table_end"):
                break
            if not in_t:
                continue
            parts = line.rstrip("\n").split("\t")
            if header is None:
                header = parts
                i_id = header.index(id_col)
                i_sym = header.index(sym_col) if sym_col else None
                i_ga = (header.index("gene_assignment")
                        if gene_assignment else None)
                continue
            pid = parts[i_id] if len(parts) > i_id else ""
            sym = ""
            if gene_assignment and len(parts) > i_ga:
                ga = parts[i_ga]
                m = ga.split(" // ")
                if len(m) >= 2 and m[1] and m[1] != "---":
                    sym = m[1].strip()
            elif i_sym is not None and len(parts) > i_sym:
                sym = parts[i_sym].strip()
            if pid and sym and sym != "---":
                rows.append((pid, sym))
    return pd.Series(dict(rows))


def collapse(expr: pd.DataFrame, mapping: pd.Series) -> pd.DataFrame:
    expr = expr.loc[expr.index.astype(str).isin(mapping.index)]
    sym = mapping.loc[expr.index.astype(str)].to_numpy()
    expr = expr.copy()
    expr["__sym"] = sym
    # keep per gene the probe with the highest mean expression
    mean = expr.drop(columns="__sym").mean(axis=1)
    expr["__mean"] = mean.to_numpy()
    expr = expr.sort_values("__mean", ascending=False)
    expr = expr[~expr["__sym"].duplicated()]
    out = expr.drop(columns="__mean").set_index("__sym")
    out.index.name = "gene"
    return out.sort_index()


def groups_for(acc: str, chars: list[list[str]]) -> list[str]:
    def find_row(prefix):
        for row in chars:
            if row and row[0].lower().startswith(prefix):
                return row
        raise KeyError(prefix)

    if acc == "GSE100927":
        row = find_row("tissue:")
        return ["EM" if "atheroscler" in v.lower() else "Control"
                for v in row]
    if acc == "GSE28829":
        row = find_row("phenotype:")
        return ["EM" if "advanced" in v.lower() else "Control" for v in row]
    if acc == "GSE43292":
        row = find_row("tissue:")
        return ["EM" if "atheroma" in v.lower() else "Control" for v in row]
    raise ValueError(acc)


def main(raw: Path, out: Path):
    out.mkdir(parents=True, exist_ok=True)
    maps = {
        "GPL570": lambda: gpl570_map(raw / "GPL570.annot.gz"),
        "GPL17077": lambda: full_table_map(raw / "GPL17077.full.txt",
                                           "ID", "GENE_SYMBOL"),
        "GPL6244": lambda: full_table_map(raw / "GPL6244.full.txt",
                                          "ID", None, gene_assignment=True),
    }
    plat_of = {"GSE100927": "GPL17077", "GSE28829": "GPL570",
               "GSE43292": "GPL6244"}
    map_cache = {}
    for acc, plat in plat_of.items():
        expr, chars, _ = read_series_matrix(
            raw / f"{acc}_series_matrix.txt.gz")
        if plat not in map_cache:
            map_cache[plat] = maps[plat]()
        expr.index = expr.index.astype(str)
        g = collapse(expr.apply(pd.to_numeric, errors="coerce").dropna(),
                     map_cache[plat])
        grp = groups_for(acc, chars)
        # heuristically log2 if raw scale
        if g.to_numpy().max() > 50:
            g = pd.DataFrame(np.log2(g.clip(lower=0).to_numpy() + 1.0),
                             index=g.index, columns=g.columns)
        g.to_csv(out / f"{acc}_expr.csv")
        pd.DataFrame({"sample": g.columns, "group": grp}).to_csv(
            out / f"{acc}_pheno.csv", index=False)
        n_em = sum(1 for x in grp if x == "EM")
        print(f"{acc}: {g.shape[0]} genes x {g.shape[1]} samples | "
              f"case={n_em} control={len(grp) - n_em}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
