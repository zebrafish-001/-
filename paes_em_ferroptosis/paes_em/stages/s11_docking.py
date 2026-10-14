"""Stage 11 — molecular docking of the PAEs against the key-gene protein.

Paper setup: AutoDock Vina, receptor ARF6 (PDB 2A5D), binding energy
< -5.0 kcal/mol taken as strong affinity, PyMOL for visualization.

This stage has two modes:
* **run** — when the ``vina`` binary and prepared PDBQT files are present
  (``data/raw/docking/receptor.pdbqt`` + ``<ligand>.pdbqt``), it executes
  Vina per configured compound (grid parameters in config).
* **parse** — otherwise it parses existing Vina log files from
  ``data/raw/vina_logs/<NAME>_<PDB>.log`` (demo mode ships synthetic
  logs), extracts the best binding energy per compound, and applies the
  affinity threshold.

``prepare_instructions()`` writes a step-by-step shell protocol
(PDB fetch → receptor/ligand prep via OpenBabel/MGLTools → Vina → PyMOL)
so a wet-lab-adjacent user can reproduce the real docking.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pandas as pd

from ..config import RunContext
from ..utils.io import save_json, save_table

_BEST_RE = re.compile(r"^\s*1\s+(-?\d+\.\d+)")


def parse_vina_log(path: Path) -> float | None:
    for line in path.read_text().splitlines():
        m = _BEST_RE.match(line)
        if m:
            return float(m.group(1))
    return None


def prepare_instructions(ctx: RunContext) -> Path:
    cfg = ctx.cfg["docking"]
    pdb = cfg["receptor_pdb"]
    compounds = ctx.cfg["network_toxicology"]["compounds"]
    lines = [
        "#!/usr/bin/env bash",
        f"# Docking protocol: PAEs vs {pdb} (AutoDock Vina)",
        "set -euo pipefail",
        f"wget -O receptor.pdb https://files.rcsb.org/download/{pdb}.pdb",
        "# strip waters/ligands, add polar H, assign charges:",
        "obabel receptor.pdb -O receptor.pdbqt -xr -p 7.4 --partialcharge gasteiger",
    ]
    for c in compounds:
        lines += [
            f"wget -O {c['name']}.sdf "
            f"'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/"
            f"{c['cid']}/record/SDF?record_type=3d'",
            f"obabel {c['name']}.sdf -O {c['name']}.pdbqt -p 7.4 "
            f"--partialcharge gasteiger",
            f"vina --receptor receptor.pdbqt --ligand {c['name']}.pdbqt "
            f"--center_x 0 --center_y 0 --center_z 0 "   # set to pocket center
            f"--size_x 25 --size_y 25 --size_z 25 "
            f"--exhaustiveness {cfg['exhaustiveness']} "
            f"--out {c['name']}_{pdb}_out.pdbqt | tee {c['name']}_{pdb}.log",
        ]
    lines.append("# visualize best poses in PyMOL: load receptor.pdb + *_out.pdbqt")
    proto = ctx.results / "s11_docking_protocol.sh"
    proto.write_text("\n".join(lines))
    return proto


def run(ctx: RunContext) -> dict:
    cfg = ctx.cfg["docking"]
    pdb = cfg["receptor_pdb"]
    thr = cfg["affinity_threshold_kcal_mol"]
    compounds = [c["name"] for c in ctx.cfg["network_toxicology"]["compounds"]]
    prepare_instructions(ctx)

    log_dir = ctx.raw / "vina_logs"
    vina = shutil.which("vina")
    dock_dir = ctx.raw / "docking"
    mode = "parse"
    if vina and (dock_dir / "receptor.pdbqt").exists() and not ctx.demo:
        mode = "run"
        log_dir.mkdir(exist_ok=True)
        for name in compounds:
            lig = dock_dir / f"{name}.pdbqt"
            if not lig.exists():
                continue
            log = log_dir / f"{name}_{pdb}.log"
            with open(log, "w") as fh:
                subprocess.run(
                    [vina, "--receptor", str(dock_dir / "receptor.pdbqt"),
                     "--ligand", str(lig),
                     "--exhaustiveness", str(cfg["exhaustiveness"]),
                     "--out", str(dock_dir / f"{name}_out.pdbqt")],
                    stdout=fh, check=False)

    rows = []
    for name in compounds:
        log = log_dir / f"{name}_{pdb}.log"
        if not log.exists():
            rows.append({"compound": name, "best_affinity": None,
                         "strong_binder": None})
            continue
        e = parse_vina_log(log)
        rows.append({"compound": name, "best_affinity": e,
                     "strong_binder": (e is not None and e < thr)})
    df = pd.DataFrame(rows)
    save_table(df, ctx.results / "s11_docking_affinities.csv", index=False)

    done = df.dropna(subset=["best_affinity"])
    out = {
        "mode": mode,
        "receptor_pdb": pdb,
        "threshold_kcal_mol": thr,
        "n_docked": int(done.shape[0]),
        "n_strong_binders": int(done["strong_binder"].sum()),
        "affinities": {r["compound"]: r["best_affinity"]
                       for r in rows if r["best_affinity"] is not None},
        "protocol": "s11_docking_protocol.sh",
    }
    save_json(out, ctx.results / "s11_docking.json")
    return out
