"""Reading / writing result folders."""
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional, Tuple

import cv2
import numpy as np
import pandas as pd

from .arenas import Arena
from .config import Config, load_config

EXT = {"csv": ".csv", "csv.gz": ".csv.gz", "parquet": ".parquet"}


def write_table(df: pd.DataFrame, base: Path, fmt: str = "csv") -> Path:
    path = Path(str(base) + EXT[fmt])
    if fmt == "parquet":
        try:
            df.to_parquet(path, index=False)
        except ImportError as e:  # pragma: no cover - depends on optional pyarrow
            raise ImportError("parquet output needs 'pip install pyarrow'") from e
    else:
        df.to_csv(path, index=False, float_format="%.5g")
    return path


def read_table(base: Path) -> pd.DataFrame:
    for fmt, ext in EXT.items():
        p = Path(str(base) + ext)
        if p.exists():
            return pd.read_parquet(p) if fmt == "parquet" else pd.read_csv(p)
    raise FileNotFoundError(f"no table {base}(.csv|.csv.gz|.parquet)")


def save_arenas(arenas: List[Arena], path: Path) -> None:
    path.write_text(json.dumps([a.to_dict() for a in arenas], indent=1), encoding="utf-8")


def load_arenas(path: Path) -> List[Arena]:
    return [Arena.from_dict(d) for d in json.loads(Path(path).read_text(encoding="utf-8"))]


def save_tracking(result, out_dir: Path, cfg: Config) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    write_table(result.raw, out_dir / "tracks_raw", cfg.output.tracks_format)
    result.frames.to_csv(out_dir / "frames.csv", index=False, float_format="%.5g")
    save_arenas(result.arenas, out_dir / "arenas.json")
    (out_dir / "video_info.json").write_text(json.dumps(result.info, indent=1), encoding="utf-8")
    cv2.imwrite(str(out_dir / "background.png"), result.background)
    cfg.save(out_dir / "config_used.yaml")


def load_tracking(out_dir: Path) -> Tuple[pd.DataFrame, pd.DataFrame, List[Arena], dict,
                                           Optional[np.ndarray], Config]:
    out_dir = Path(out_dir)
    raw = read_table(out_dir / "tracks_raw")
    raw["track_id"] = raw["track_id"].astype(str)
    raw["arena"] = raw["arena"].astype(str)
    frames = pd.read_csv(out_dir / "frames.csv") if (out_dir / "frames.csv").exists() else None
    arenas = load_arenas(out_dir / "arenas.json")
    info = json.loads((out_dir / "video_info.json").read_text(encoding="utf-8"))
    bg = cv2.imread(str(out_dir / "background.png"), cv2.IMREAD_GRAYSCALE)
    cfg = load_config(out_dir / "config_used.yaml")
    return raw, frames, arenas, info, bg, cfg


def save_analysis(res, out_dir: Path, cfg: Config) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    if cfg.output.save_tracks:
        write_table(res.tracks, out_dir / "tracks", cfg.output.tracks_format)
    for name in ("summary", "timebins", "phases", "events", "bouts"):
        df = getattr(res, name)
        p = out_dir / f"{name}.csv"
        if df is not None and len(df):
            df.to_csv(p, index=False, float_format="%.6g")
        elif p.exists():
            p.unlink()  # stale file from an earlier analysis
