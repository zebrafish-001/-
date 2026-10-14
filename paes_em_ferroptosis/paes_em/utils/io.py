"""Small IO helpers shared by all stages."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pandas as pd


def save_table(df: pd.DataFrame, path: Path, index: bool = True) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=index)
    return path


def save_json(obj, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def load_json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def rscript_available() -> bool:
    return shutil.which("Rscript") is not None


def run_rscript(script: Path, args: list[str], cwd: Path | None = None) -> bool:
    """Run an R hook script; return True on success, False when R is absent
    or the script fails (callers then fall back to the python-lite engine)."""
    if not rscript_available():
        return False
    try:
        subprocess.run(
            ["Rscript", str(script), *args],
            check=True, cwd=cwd, capture_output=True, text=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False
