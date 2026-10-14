"""paes_em — PAEs → Ferroptosis → EMT → Endometriosis analysis pipeline.

A reproducible reimplementation scaffold of the computational workflow in
Wang et al., J Hazard Mater 2026;507:141670
(doi:10.1016/j.jhazmat.2026.141670): network toxicology + bulk RNA-seq
(limma-style DE, WGCNA, enrichment, 12-algorithm ML screening, ssGSEA
immune infiltration) + scRNA-seq / spatial transcriptomics + virtual
knockout + molecular docking, generalized so the exposure, disease and
context gene set are configurable.
"""

__version__ = "0.1.0"
