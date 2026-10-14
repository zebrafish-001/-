"""Pipeline stages, numbered in paper order. Each module exposes
``run(ctx) -> dict`` returning a JSON-serializable summary that is also
persisted to ``data/results/<stage>.json``."""

from . import (  # noqa: F401
    s01_intake, s02_network_tox, s03_diffexp, s04_wgcna, s05_enrich,
    s06_ml, s07_immune, s08_singlecell, s09_spatial, s10_knockout,
    s11_docking, s12_report,
)

ORDER = [
    ("intake", s01_intake),
    ("network_tox", s02_network_tox),
    ("diffexp", s03_diffexp),
    ("wgcna", s04_wgcna),
    ("enrich", s05_enrich),
    ("ml", s06_ml),
    ("immune", s07_immune),
    ("singlecell", s08_singlecell),
    ("spatial", s09_spatial),
    ("knockout", s10_knockout),
    ("docking", s11_docking),
    ("report", s12_report),
]
