"""Readers for Noldus EthoVision XT exports (DanioVision).

Supported:

* ``Export -> Raw data`` files (.txt / .csv / .xlsx), one arena per file.
  Layout: first line "Number of header lines:", N; then "key", "value" rows;
  then the column-name row (starts with "Trial time"), a units row, and the
  samples.  Missing values are written as "-".  Delimiter and decimal mark
  depend on the Windows locale, both are auto-detected.

The reader is deliberately tolerant: it locates the column-name row by
content instead of trusting the header-line count.
"""
from __future__ import annotations

import csv
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

# EthoVision column name -> standard name. Matched on the part before "(".
_STD = {
    "trial time": "time_s",
    "recording time": "rec_time_s",
    "x center": "x",
    "y center": "y",
    "x nose": "x_nose",
    "y nose": "y_nose",
    "x tail": "x_tail",
    "y tail": "y_tail",
    "area": "area",
    "areachange": "area_change",
    "elongation": "elongation",
    "distance moved": "distance",
    "velocity": "velocity",
    "heading": "heading",
    "turn angle": "turn_angle",
    "angular velocity": "angular_velocity",
    "meander": "meander",
    "acceleration": "acceleration",
    "activity": "activity",
}


@dataclass
class EthoTrack:
    data: pd.DataFrame            # standardised columns, numeric, NaN for "-"
    meta: Dict[str, str]          # header key/value rows (Trial name, Arena name, ...)
    units: Dict[str, str]         # standard column -> unit string
    columns: Dict[str, str]       # standard column -> original EthoVision column
    path: Optional[Path] = None

    @property
    def trial(self) -> str:
        return self.meta.get("Trial name", "").strip()

    @property
    def arena(self) -> str:
        return self.meta.get("Arena name", "").strip()

    @property
    def subject(self) -> str:
        return self.meta.get("Subject name", "").strip()

    @property
    def sample_rate(self) -> float:
        t = self.data["time_s"].to_numpy(float)
        return 1.0 / float(np.nanmedian(np.diff(t))) if len(t) > 1 else float("nan")


def _sniff_delimiter(line: str) -> str:
    counts = {d: line.count(d) for d in (";", "\t", ",")}
    return max(counts, key=counts.get)


def _read_rows(path: Path) -> List[List[str]]:
    if path.suffix.lower() in (".xlsx", ".xls"):
        df = pd.read_excel(path, header=None, dtype=str)
        return [["" if (isinstance(v, float) and np.isnan(v)) or v is None else str(v)
                 for v in row] for row in df.itertuples(index=False)]
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    first = text.splitlines()[0] if text else ""
    delim = _sniff_delimiter(first)
    return list(csv.reader(text.splitlines(), delimiter=delim, quotechar='"'))


_NUM_RE = re.compile(r"^[-+]?(\d+([.,]\d*)?|[.,]\d+)([eE][-+]?\d+)?$")


def _to_float(col: pd.Series) -> pd.Series:
    s = col.astype(str).str.strip()
    s = s.where(~s.isin(["-", "", "nan", "NaN", "None"]), other=np.nan)
    sample = s.dropna().head(50)
    if len(sample) and sample.str.contains(",").mean() > 0.5 and not sample.str.contains(r"\.").any():
        s = s.str.replace(",", ".", regex=False)      # decimal comma locale
    return pd.to_numeric(s, errors="coerce")


def _standard_name(col: str) -> str:
    base = col.split("(")[0].strip().lower()
    if base in _STD:
        return _STD[base]
    m = re.match(r"^(movement|in zone|mobility|zone transition)\s*\((.*)\)\s*$", col.strip(), re.I)
    if m:
        kind, inner = m.group(1).lower().replace(" ", "_"), m.group(2)
        label = re.sub(r"[^0-9a-zA-Z一-鿿]+", "_", inner.split("/")[0]).strip("_").lower()
        return f"{kind}_{label}"
    return re.sub(r"[^0-9a-zA-Z一-鿿]+", "_", col.strip()).strip("_").lower()


def read_raw_export(path) -> EthoTrack:
    """Parse one EthoVision 'Raw data' export file into an EthoTrack."""
    path = Path(path)
    rows = _read_rows(path)
    hdr = next((i for i, r in enumerate(rows)
                if r and r[0].strip().strip('"').lower().startswith("trial time")), None)
    if hdr is None:
        raise ValueError(f"{path}: no 'Trial time' column row found - is this an EthoVision raw export?")
    meta = {}
    for r in rows[:hdr]:
        if len(r) >= 2 and r[0].strip():
            meta[r[0].strip().strip('"').rstrip(":")] = r[1].strip().strip('"')
    names = [c.strip().strip('"') for c in rows[hdr]]
    units_row = rows[hdr + 1] if hdr + 1 < len(rows) else []
    has_units = bool(units_row) and not any(_NUM_RE.match(c.strip().strip('"') or "x") for c in units_row[:2])
    units_raw = [c.strip().strip('"') for c in units_row] if has_units else [""] * len(names)
    data_rows = rows[hdr + 2 if has_units else hdr + 1:]
    data_rows = [r[:len(names)] + [""] * (len(names) - len(r)) for r in data_rows if any(c.strip() for c in r)]
    raw = pd.DataFrame(data_rows, columns=names)
    std_cols, units, columns = {}, {}, {}
    for i, name in enumerate(names):
        if not name:
            continue
        std = _standard_name(name)
        k, base = 2, std
        while std in std_cols:            # duplicate names -> suffix
            std = f"{base}_{k}"
            k += 1
        std_cols[std] = _to_float(raw[name])
        units[std] = units_raw[i] if i < len(units_raw) else ""
        columns[std] = name
    df = pd.DataFrame(std_cols)
    if "time_s" not in df:
        raise ValueError(f"{path}: 'Trial time' column missing")
    df = df.dropna(subset=["time_s"]).reset_index(drop=True)
    return EthoTrack(df, meta, units, columns, path)


def read_raw_exports(paths) -> List[EthoTrack]:
    return [read_raw_export(p) for p in paths]


def to_mm(track: EthoTrack, col: str) -> np.ndarray:
    """Column values converted to mm (or mm/s) from the unit recorded in the file."""
    v = track.data[col].to_numpy(float)
    u = track.units.get(col, "").lower()
    if u.startswith("cm"):
        return v * 10.0
    if u.startswith("mm"):
        return v
    if u.startswith("m") and not u.startswith("mm"):
        return v * 1000.0
    return v
