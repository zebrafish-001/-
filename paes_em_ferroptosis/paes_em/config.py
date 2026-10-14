"""Pipeline configuration loading and run-context handling."""

from __future__ import annotations

import dataclasses
from pathlib import Path

import yaml

PKG_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = PKG_ROOT / "config" / "pipeline.yaml"


@dataclasses.dataclass
class RunContext:
    """Resolved paths + parsed config carried through all stages."""

    cfg: dict
    root: Path          # project root (where data/ lives)
    demo: bool = False  # True -> run on bundled synthetic data
    seed: int = 20260302

    @property
    def raw(self) -> Path:
        return self._dir("raw")

    @property
    def processed(self) -> Path:
        return self._dir("processed")

    @property
    def results(self) -> Path:
        return self._dir("results")

    def _dir(self, key: str) -> Path:
        p = self.root / self.cfg["paths"][key]
        p.mkdir(parents=True, exist_ok=True)
        return p


def load_config(path: str | Path | None = None) -> dict:
    with open(path or DEFAULT_CONFIG, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def make_context(config_path=None, root=None, demo=False, seed=None) -> RunContext:
    cfg = load_config(config_path)
    ctx = RunContext(cfg=cfg, root=Path(root) if root else PKG_ROOT, demo=demo)
    if seed is not None:
        ctx.seed = int(seed)
    return ctx
