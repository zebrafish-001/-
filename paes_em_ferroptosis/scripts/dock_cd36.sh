#!/usr/bin/env bash
# Real docking: 12 plasticizers vs human CD36 ectodomain (PDB 5LGD chain A).
# Box centered on the hydrophobic lipid-transport tunnel (residues 146-164
# + 289-301). Requires vina + obabel (micromamba env "dock").
set -euo pipefail
DOCK_BIN="${DOCK_BIN:?set DOCK_BIN to the dock env bin dir}"
WORK="$(readlink -f "${1:?workdir}")"; LOGDIR="$(readlink -f "${2:?log output dir}")"
mkdir -p "$WORK" "$LOGDIR"
cd "$WORK"

# ---- receptor ----
if [ ! -f receptor.pdbqt ]; then
  curl -sS --max-time 120 -o 5LGD.pdb "https://files.rcsb.org/download/5LGD.pdb"
  # chain A protein atoms only (drop PfEMP1 chain B, waters, glycans)
  awk '$1=="ATOM" && substr($0,22,1)=="A"' 5LGD.pdb > receptor_A.pdb
  "$DOCK_BIN/obabel" receptor_A.pdb -O receptor.pdbqt -xr -p 7.4 \
      --partialcharge gasteiger 2>/dev/null
fi

# ---- box center: centroid of CA atoms of tunnel residues ----
read CX CY CZ <<< "$(awk '$1=="ATOM" && substr($0,14,2)=="CA" {
  r=substr($0,23,4)+0;
  if ((r>=146 && r<=164) || (r>=289 && r<=301)) {
    n++; x+=substr($0,31,8); y+=substr($0,39,8); z+=substr($0,47,8)}
} END {printf "%.2f %.2f %.2f", x/n, y/n, z/n}' receptor_A.pdb)"
echo "box center: $CX $CY $CZ"

# ---- ligands + docking ----
declare -A CID=( [DEHP]=8343 [DBP]=3026 [BBP]=2347 [DEP]=6781 [DMP]=8554
  [DIBP]=6782 [DINP]=590836 [DEHT]=22932 [DINCH]=11524680 [DEHA]=7641
  [ATBC]=6505 [TOTM]=18725 )
for name in "${!CID[@]}"; do
  cid=${CID[$name]}
  if [ ! -f "$name.pdbqt" ]; then
    if ! curl -sS --max-time 120 -o "$name.sdf" \
      "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/$cid/record/SDF?record_type=3d" \
      || grep -q "PUGREST" "$name.sdf"; then
      curl -sS --max-time 120 -o "$name.sdf" \
        "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/$cid/record/SDF"
      "$DOCK_BIN/obabel" "$name.sdf" -O "$name.3d.sdf" --gen3d 2>/dev/null
      mv "$name.3d.sdf" "$name.sdf"
    fi
    "$DOCK_BIN/obabel" "$name.sdf" -O "$name.pdbqt" -p 7.4 \
        --partialcharge gasteiger 2>/dev/null
  fi
  if grep -q "^   1 " "$LOGDIR/${name}_5LGD.log" 2>/dev/null; then
    echo "skip $name (done)"; continue; fi
  echo "== docking $name (CID $cid)"
  "$DOCK_BIN/vina" --receptor receptor.pdbqt --ligand "$name.pdbqt" \
    --center_x "$CX" --center_y "$CY" --center_z "$CZ" \
    --size_x 26 --size_y 26 --size_z 26 \
    --exhaustiveness 8 --seed 20260302 --cpu 4 \
    --out "${name}_out.pdbqt" > "$LOGDIR/${name}_5LGD.log" 2>&1 \
    || echo "VINA FAIL $name"
  grep -m1 "^   1" "$LOGDIR/${name}_5LGD.log" || true
done
echo DONE
