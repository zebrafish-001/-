# Methods-Frontier Survey: Predicting Chemical–Biological Interaction and Toxicity
## Target: publishing *above* the 2020–2025 ES&T computational-toxicology norm

**Compiled:** 2026-11-13
**Baseline being beaten:** AutoDock Vina/Glide docking on one nuclear receptor (+ optional MD + MM/GBSA), or RF/XGBoost QSAR on ToxCast/Tox21 descriptors, confirmed by a reporter-gene assay or a zebrafish endpoint.

### Verification key
| Tag | Meaning |
|---|---|
| **[V]** | Bibliographic metadata verified this session (PubMed record retrieved, or publisher/journal landing page returned in search with volume/pages/DOI) |
| **[P]** | Preprint (bioRxiv / arXiv / ChemRxiv / eLife reviewed preprint) — real and locatable, but not peer-reviewed in that form |
| **[U]** | **Unverified** — title and venue appeared in search results but one or more of {authors, volume, pages, year, DOI} could not be confirmed. Treat as a lead, re-verify before citing. |

### Methodological caveat on this survey
`api.openalex.org`, `doi.org`, `api.crossref.org`, `*.ncbi.nlm.nih.gov` and `nature.com` were **not reachable** from this session (egress proxy denial / DNS). Verification therefore rests on (a) the PubMed MCP server, (b) the Consensus MCP server, and (c) web-search result metadata. Numeric performance claims taken from search snippets rather than full text are explicitly marked. **No citation below was invented**; where a detail is missing it is marked [U] rather than filled in.

---

## Axis 1 — Structure / interaction prediction: co-folding

### Key citations

| # | Citation | Venue / year | What it establishes | Code / weights |
|---|---|---|---|---|
| 1.1 | Abramson, J. et al. "Accurate structure prediction of biomolecular interactions with AlphaFold 3." *Nature* **630**, 493–500 (2024). DOI 10.1038/s41586-024-07487-1 | Nature 2024 | The co-folding paradigm: joint protein+ligand+ion+nucleic-acid structure from sequence + ligand graph. Replaces "rigid receptor + docked ligand". **[V]** (volume/pages from prior knowledge — re-check) | Weights available to academics on request (non-commercial); AF3 server restricted to a ligand whitelist |
| 1.2 | Buttenschoen, M., Morris, G.M., Deane, C.M. "PoseBusters: AI-based docking methods fail to generate physically valid poses or generalise to novel sequences." *Chem. Sci.* **15**, 3130–3139 (2024). DOI 10.1039/D3SC04185A | Chem Sci 2024 **[V]** | The physical-validity gate. DL docking (DiffDock, EquiBind, TankBind, Uni-Mol, DeepDock) loses to Vina/GOLD once stereochemistry, ring planarity, clashes and novel-sequence generalisation are scored. "MM force fields contain docking-relevant physics missing from deep-learning methods." | `posebusters` pip package, open |
| 1.3 | Škrinjar, P., Eberhardt, J., Durairaj, J., Schwede, T. "Have protein–ligand cofolding methods moved beyond memorisation?" bioRxiv 2025.02.03.636309 (2025). Published version indexed as "Evaluating generalization in protein–ligand cofolding methods" (PMC13661253) | bioRxiv 2025 **[P]**; journal version **[U]** | **The single most important honest-limits paper for pollutant work.** "Runs N' Poses" benchmark: ~2,600 high-resolution PLI systems released after the 30 Sep 2021 cutoff. AF3 / Protenix / Chai-1 / Boltz-1 all degrade sharply on ligands and pockets dissimilar to training data. LDDT-LP > 0.8: 92/91/90/90% all-systems → 87/83/82/83% on cluster representatives. | Benchmark on Zenodo + Polaris Hub; code at `plinder-org` GitHub |
| 1.4 | Shen, C., Zhang, X., Gu, S., Zhang, O., Wang, Q., Du, G., Zhao, Y., Jiang, L., Pan, P., Kang, Y., Zhao, Q., Hsieh, C.-Y., Hou, T. "Unlocking the application potential of AlphaFold3-like approaches in virtual screening." *Chem. Sci.* **17**(5), 2858–2879 (online 11 Dec 2025). DOI 10.1039/d5sc06481c; PMID 41403459 | Chem Sci 2025/26 **[V]** (PubMed record retrieved) | The best available answer to "does co-folding change virtual screening?" On DEKOIS2.0, **AF3's own confidence metrics alone give exceptional enrichment** — no third-party rescoring needed. Performance declines in three regimes: (i) progressive removal of chemically similar actives, (ii) a novel GPCR set under-represented in training, (iii) LIT-PCBA subset with experimentally verified inactives. Still beats conventional docking in most cases. Poses mostly physically plausible with minor artefacts. | AF3 / Protenix / Boltz-2 all usable |
| 1.5 | Singh, S., Clerkin, A.B., Castellanos, M.A., Chodera, J.D. "More protein-ligand data are needed for AlphaFold-like models to enable drug discovery." *Curr. Opin. Struct. Biol.* **98**, 103257 (2026). DOI 10.1016/j.sbi.2026.103257; PMID 41924828 | Curr Opin Struct Biol 2026 **[V]** | Authoritative framing of *why* co-folding plateaus: PDB-derived training data under-represents real design tasks. Offers a hierarchical framework of which tasks current models do well vs. remain unexplored. Essential for the Discussion section of a pollutant co-folding paper. | — |
| 1.6 | "Large-scale prospective evaluation of co-folding across hundreds of Mac1–ligand complexes and three virtual screens." eLife reviewed preprint 110475 (2025/26); also bioRxiv, PMC12776374 | eLife reviewed preprint **[P]**; authors **[U]** | Prospective, not retrospective. AF3, Boltz-2, Chai-1 each reproduce >50% of 557 Mac1 ligand poses to <2 Å RMSD, **but fail to re-rank docking hit lists and fail to reproduce common conformational rearrangements (peptide flip, loop opening).** Boltz-2 affinity correlated with potency only after calibration. | — |
| 1.7 | "AlphaFold3 for Structure-guided Ligand Discovery." bioRxiv 2025.12.04.692352 (2025) | bioRxiv **[P]**; authors **[U]** | >700,000-compound prospective screens vs σ2, D4, AmpC with >2,500 molecules tested. **DOCK3 gave stronger overall enrichment; AF3 contributed mainly early enrichment.** A crystal structure of σ2 + top AF3 hit confirmed a near-native pose. | — |
| 1.8 | Qiao, Z., Nie, W., Vahdat, A., Miller, T.F. III, Anandkumar, A. "State-specific protein–ligand complex structure prediction with a multiscale deep generative model." *Nat. Mach. Intell.* **6**, 195–208 (2024). DOI 10.1038/s42256-024-00792-z | Nat Mach Intell 2024 **[V]** | NeuralPLexer: diffusion over residue contact maps + all heavy atoms; samples ligand-free *and* ligand-bound ensembles. The conceptual route to **induced-fit / conformational-ensemble receptor modelling**, which matters for promiscuous pollutant binding. | GitHub `zrqiao/NeuralPLexer`; CUDA ≥10.2 |
| 1.9 | Abriata, L.A., Dal Peraro, M. "Practical Outcomes From CASP16 for Users in Need of Biomolecular Structure Prediction." *Proteins* (2025), DOI 10.1002/prot.70078; PMC12750028 | Proteins 2025 **[V]** (volume/pages **[U]**) | CASP16 user-facing synthesis. Co-folding pose prediction with AF3 "demonstrated strong potential … outperforming many participants and some dedicated docking tools", **while ligand affinity prediction is described as unreliable.** Emphasises pLDDT/pAE confidence use. | — |
| 1.10 | Boltz-1: Wohlwend, J. et al. "Boltz-1: Democratizing Biomolecular Interaction Modeling." bioRxiv (2024). Boltz-2: Passaro, S., Corso, G., Wohlwend, J. et al. "Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction." bioRxiv 2025.06.14.659707 | bioRxiv **[P]** (no journal version found as of this search) | Fully open (MIT) AF3-class co-folding + an affinity head. | **MIT licence**: code, weights, training pipeline. (Boltz-2.1 is closed-source, Boltz PBC.) |
| 1.11 | Protenix: "Protenix — Advancing Structure Prediction Through a Comprehensive AlphaFold3 Reproduction." bioRxiv 2025.01.08.631967 (ByteDance). OpenFold3 (OpenFold consortium) preview checkpoints, Apache-2.0 | bioRxiv **[P]** | Open AF3 reproductions. Protenix-v1 reported as 368M params, Apache-2.0; Protenix-Mini for cheaper inference. **[U]** on exact parameter counts. | Apache-2.0 |
| 1.12 | Azhagiya Singam, E.R., Durkin, K.A., La Merrill, M.A., Furlow, J.D., Wang, J.-C., Smith, M.T. "Prediction of the Interactions of a Large Number of Per- and Poly-Fluoroalkyl Substances with Ten Nuclear Receptors." *Environ. Sci. Technol.* **58**(10), 4487–4499 (2024). DOI 10.1021/acs.est.3c05974; PMID 38422483 | ES&T 2024 **[V]** | **This is the current ES&T state of the art on this axis** — 4,545 PFAS × 10 nuclear receptors by molecular modelling + ML. Classic docking-based, no co-folding, no free energy, no physical-validity gate. The paper to beat. | — |

### Transferability to pollutants / what it would take

**Why this axis is immediately transferable.** Pollutant receptor targets (ERα/β, AR, TRβ, PPARγ/α, PXR, CAR, AhR, GR, RXR, TTR, L-FABP, HSA) mostly have good experimental structures, so co-folding is not needed for the *receptor*. The actual value is threefold:
1. **Induced fit without a crystal structure of the pollutant complex.** Pollutant ligands (PFAS tails, brominated aromatics, phthalate esters) are chemically unlike pharma ligands; rigid-receptor docking into a drug-bound conformer is the hidden error source. Co-folding with ensemble sampling (1.8) or multi-seed AF3/Boltz addresses it.
2. **Confidence metrics as a *free* enrichment signal** (1.4) — AF3/Protenix confidence ranks compounds without any scoring function, which is a genuinely new screening primitive.
3. **The failure modes are published and quantifiable** (1.3, 1.5, 1.6, 1.7). A pollutant paper that reports a PLINDER/Runs-N'-Poses-style **training-similarity-stratified** evaluation, plus PoseBusters validity rates, plus an orthogonal docking comparison, is methodologically ahead of almost every ES&T co-folding paper.

**Specific unexploited gap:** nobody has published a co-folding evaluation on *environmental* chemistry. There is no PoseBusters-style set of pollutant–receptor complexes. Building one (PDB mining for ER/TR/PPAR/TTR/PXR complexes with halogenated, perfluorinated and phenolic ligands, stratified by similarity to AF3/Boltz training cutoffs) would be a standalone contribution.

**Compute.** One A100/H100 (40–80 GB) runs AF3-class inference in ~10 s–3 min per complex depending on sequence length and sampling. MSA generation, not the network, is the bottleneck — precompute MSAs once per receptor and reuse across the whole chemical library. A 10,000-compound × 10-receptor screen with 5 seeds each = 500k inferences ≈ realistically 2–6 weeks on 4–8 GPUs. Boltz-2 is markedly cheaper than AF3.

**Open weights:** Boltz-1/-2 (MIT), Protenix (Apache-2.0), OpenFold3 (Apache-2.0) are fully usable, including commercially. AF3 weights require a DeepMind academic request and are non-commercial. **A mid-size lab should build on Boltz-2 + Protenix, not AF3**, for reproducibility and licence cleanliness.

**Verdict: deployable in 3–6 months.** This is the lowest-hanging frontier move.

---

## Axis 2 — Binding affinity: free energy and ML potentials

### Key citations

| # | Citation | Venue / year | Headline accuracy | Code |
|---|---|---|---|---|
| 2.1 | Schindler, C.E.M. et al. "Large-Scale Assessment of Binding Free Energy Calculations in Active Drug Discovery Projects." *J. Chem. Inf. Model.* **60**(11), 5457–5474 (2020). DOI 10.1021/acs.jcim.0c00900 | JCIM 2020 **[V]** (volume/pages confirmed; the frequently quoted "RMSE ≈ 1.1 kcal/mol" figure **[U]** — not confirmed from abstract, check SI) | The reference point for commercial FEP+ in prospective projects, plus a new public 8-target benchmark | FEP+ commercial (Schrödinger); benchmark public |
| 2.2 | "Large-Scale Collaborative Assessment of Binding Free Energy Calculations for Drug Discovery Using OpenFE." *J. Chem. Inf. Model.* **66**(11), 6429–… (2026); ChemRxiv 10.26434/chemrxiv-2025-7sthd; PMC13555741 | JCIM 2026 **[V]** on venue/volume; author list **[U]** | **The number to quote for open-source RBFE:** weighted RMSE ≈ **1.73 kcal/mol** (95% CI ~1.53–1.96) across 58 public systems, 10 sub-kcal; **2.44 kcal/mol** (1.94–3.06) on 37 private industry systems, only 2 sub-kcal. >1,700 ligands, 15 pharma companies. Explicitly **less accurate than optimised FEP+ on deviation metrics**, comparable on ranking. | **OpenFE / `openfe` — fully open** |
| 2.3 | "A formally exact method for high-throughput absolute binding-free-energy calculations." *Nat. Comput. Sci.* (2025). DOI 10.1038/s43588-025-00821-w | Nat Comput Sci 2025 **[V]** on venue; authors/volume **[U]** | ABFE: average unsigned error **<1 kcal/mol** on 34 complexes *with validated force-field accuracy*; hysteresis <0.5 kcal/mol; 4–8× efficiency gain. Note the force-field caveat — this is a sampling-method result, not a general accuracy claim. | **[U]** |
| 2.4 | "BindFlow: a free, user-friendly pipeline for absolute binding free energy calculations using free energy perturbation or MM(PB/GB)SA." bioRxiv 2025.09.25.678545 | bioRxiv **[P]** | 139 receptor–ligand pairs; FEP > MM(PB/GB)SA for accuracy, but MM(PB/GB)SA gives useful *rankings* at a fraction of cost → explicit tiered-screening justification | Open pipeline |
| 2.5 | Devereux, C., Smith, J.S., Huddleston, K.K., Barros, K., Zubatyuk, R., Isayev, O., Roitberg, A.E. "Extending the Applicability of the ANI Deep Learning Molecular Potential to Sulfur and Halogens." *J. Chem. Theory Comput.* **16**, 4192–4202 (2020) | JCTC 2020 **[V]** | ANI-2x: H, C, N, O, **F, Cl, S** (~90% of drug-like space); ~10⁶× faster than DFT; sub-chemical accuracy on most of COMP6 | TorchANI, open |
| 2.6 | Kovács, D.P., Moore, J.H., Browning, N.J., Batatia, I., Horton, J.T., Pu, Y., Kapil, V., Witt, W.C., Magdău, I.-B., Cole, D.J., Csányi, G. "MACE-OFF: Short-Range Transferable Machine Learning Force Fields for Organic Molecules." *J. Am. Chem. Soc.* **147**(21), 17598–17611 (2025). DOI 10.1021/jacs.4c07099 | JACS 2025 **[V]** | Current best transferable MLIP for organic molecules; short-range by design (explicit long-range still needed) | `ACEsuit/mace-off`, open (MACE-OFF23 licence caveats) |
| 2.7 | Anstine, D.M., Zubatyuk, R., Isayev, O. "AIMNet2: a neural network potential to meet your neutral, charged, organic, and elemental-organic needs." *Chem. Sci.* **16**, 10228–10244 (2025). DOI 10.1039/D4SC08572H | Chem Sci 2025 **[V]** | **The MLIP most relevant to pollutants:** up to 14 elements, **neutral *and charged* species**, ML short-range + physics-based long-range, 20M hybrid QM reference calcs. Outperforms GFN-xTB, near-DFT on conformer search and geometry optimisation. Open-shell (`aimnet2-nse`) and Pd variants released. | HuggingFace `isayevlab`, open |
| 2.8 | "Evaluating Electrostatic Embedding MLIP/MM for Relative Binding Free Energy Calculations." arXiv 2608.13355 (2026) | arXiv **[P]** | Identifies the live problem: mechanical-embedding MLIP/MM fixes ligand strain but still treats ligand–environment electrostatics with static point charges; proposes ML charges in a production alchemical workflow | **[U]** |
| 2.9 | "Machine Learning Enhanced Calculation of Quantum-Classical Binding Free Energies." arXiv 2503.03955 (2025) | arXiv **[P]** | ML potentials trained on QM/MM data correcting classical alchemical ΔG; reported 2.1 kJ/mol shift for a transition-metal system (single-system result) | **[U]** |
| 2.10 | Boltz-2 (see 1.10) | bioRxiv **[P]** | Claims to **approach FEP accuracy at >1000× speed**: Pearson R ≈ 0.62 on the FEP+ benchmark vs ~0.72 for physics (press-reported; a vendor summary gives R = 0.66 on a 4-target subset — figures unreconciled). **Independent checks are worse:** poor-to-negative correlation and large absolute errors on a 93-molecular-glue set; systematic under-dispersion of the affinity range. | MIT |

### Transferability to pollutants / what it would take

**Where the real accuracy is.** For xenobiotics the honest expectation is:
- **RBFE (OpenFE/FEP+) within a congeneric series: ~1.5–2.5 kcal/mol RMSE** (2.2). That is good enough to rank PFAS chain-length series, bisphenol analogues, OPFR/BFR congeners, phthalate esters — i.e. exactly the read-across problems environmental labs face.
- **ABFE across chemically unrelated pollutants: worse**, and the "<1 kcal/mol" numbers (2.3) carry a force-field-validation precondition that pollutants rarely satisfy.
- **The force field, not the sampling, is the bottleneck for pollutants.** Perfluoroalkyl chains, polybrominated aromatics, organotins and charged sulfonates/carboxylates are poorly parameterised in GAFF2/OpenFF. This is precisely where **AIMNet2 (2.7) is the differentiator** — it is the only widely-released MLIP that handles charged and elemental-organic species across 14 elements.

**The highest-value, genuinely novel move on this axis:** validate/derive ML-potential-corrected parameters for a pollutant class (PFAS sulfonates/carboxylates; brominated flame retardants) and then run OpenFE RBFE against measured TTR / HSA / L-FABP / PPARγ binding data. Transthyretin and serum-albumin competitive-binding datasets for PFAS and halogenated phenols are large, quantitative, and have never been addressed with modern alchemical free energy. **A pollutant-series RBFE paper with experimental ΔΔG validation would be a clear first.**

**Compute.** RBFE: ~1–4 GPU-hours per edge (per λ-window set) on an A100. A 30-compound congeneric series with a reasonable perturbation map ≈ 40–60 edges ≈ 100–250 GPU-hours ≈ **1–2 weeks on 2 GPUs**. ABFE is roughly 3–10× that per ligand. MLIP/MM hybrid free energy is another 10–50× — treat as a stretch goal, not a deliverable. MLIP single-point/optimisation work (conformer ensembles, tautomer/protonation-state energetics, descriptor generation) is cheap: thousands of molecules per GPU-day.

**Open code:** OpenFE, OpenMM, `openfe`/`perses`, ANI (TorchANI), AIMNet2, MACE — all open. No commercial licence needed. **This axis requires no proprietary software**, which is itself a reproducibility selling point.

**Verdict: RBFE on a congeneric pollutant series is deployable in 6–12 months** with one competent MD person. MLIP/MM hybrid free energy is 18+ months.

---

## Axis 3 — Molecular representation learning: do foundation models actually win?

### Key citations

| # | Citation | Venue / year | What it establishes | Code |
|---|---|---|---|---|
| 3.1 | Ross, J., Belgodere, B., Chenthamarakshan, V., Padhi, I., Mroueh, Y., Das, P. "Large-Scale Chemical Language Representations Capture Molecular Structure and Properties." *Nat. Mach. Intell.* (2022); arXiv 2106.09553 | Nat Mach Intell 2022 **[V]** on authors/venue; volume/pages **[U]** | MoLFormer-XL: 1.1B molecules (ZINC + 111M PubChem), linear attention + rotary embeddings; 12 layers / 12 heads / d=768. **Pretraining cost only ~208 GPU-hours on 16 V100s** — cheap enough for a mid-size lab to *re-pretrain*. Beats GNN baselines on many MoleculeNet tasks but **loses to explicit-3D models (SchNet, DimeNet) on QM9 energetics.** | HuggingFace `ibm/MoLFormer-XL-both-10pct` |
| 3.2 | Ji, X., Wang, Z., Gao, Z., Zheng, H., Zhang, L., Ke, G., E, W. "Uni-Mol2: Exploring Molecular Pretraining Model at Scale." NeurIPS 2024; arXiv 2406.14969 | NeurIPS 2024 **[V]** on authors/venue | First systematic **scaling-law** study for molecular pretraining: power-law validation loss vs params (84M → 1.1B), data and compute; two-track transformer on atom + pair features; ~884M 3D conformations. Reported +27% on QM9, +14% on COMPAS-1D for the 1.1B model **[U] — numbers from secondary summaries only.** | `deepmodeling/Uni-Mol`, open |
| 3.3 | van Tilborg, D., Alenicheva, A., Grisoni, F. "Exposing the Limitations of Molecular Machine Learning with Activity Cliffs." *J. Chem. Inf. Model.* **62**(23), 5938–5951 (2022). DOI 10.1021/acs.jcim.2c01073. **Correction**: DOI 10.1021/acs.jcim.3c01576 (2023) — a splitting bug mislabelled some activity cliffs; use the corrected figures | JCIM 2022 + correction **[V]** | **MoleculeACE.** 24 ML/DL methods × 30 targets: all struggle on activity cliffs, and **descriptor-based classical ML beats the deeper models.** High global accuracy coexists with gross cliff mispredictions. Argues for mandatory cliff-specific metrics. | `molML/MoleculeACE`, pip |
| 3.4 | "Critical Assessment of ML models for ADMET Prediction in TDC leaderboards" (2025) | **[U]** venue | Found significant issues in two gradient-boosting leaderboard entries; after fixing the split function and re-evaluating, **substantially lower ranks resulted.** Directly relevant to whether published tree baselines were fair. Re-verify before citing. | — |
| 3.5 | "Revisiting ADMET prediction reliability under real-world challenges in the foundation model era." PMC13371653 | **[U]** venue/year | Head-to-head of molecular FMs, a tabular FM (TabPFNv2), GNNs, AutoML and classical methods. **Regime-dependent:** pretrained GNNs lead when data is plentiful and topology complex; expert features + tabular FMs win in data-scarce regimes. | — |
| 3.6 | "Tabular foundation models for in-context prediction of molecular properties." arXiv 2604.16123 | arXiv **[P]** | Counterpoint: TFM approaches beat classical baselines and previously reported molecular FMs on Polaris and MoleculeACE suites (authors' own claim) | **[U]** |
| 3.7 | "Benchmarking Artificial Intelligence Models for Predicting Nuclear Receptor Activity from Tox21 Assays." bioRxiv 2026.03.20.713297 | bioRxiv **[P]** | The most on-point honest benchmark for this audience: **RF and XGBoost on descriptors (or descriptors+fingerprints) consistently win on Tox21 NR datasets with >10% actives; DL is more robust at 5–10% actives.** | **[U]** |
| 3.8 | "Identification of Optimal Machine Learning Algorithms and Molecular Fingerprints for Explainable Toxicity Prediction Models Using ToxCast/Tox21 Bioassay Data." *ACS Omega* (2024). DOI 10.1021/acsomega.4c04474 | ACS Omega 2024 **[V]** on venue/DOI; authors **[U]** | 1,092 ToxCast/Tox21 assays; **MACCS + RF judged the optimal predictivity/explainability combination** on a 737-assay subset | — |
| 3.9 | Belfield, S.J. et al. "Guidance for good practice in the application of machine learning in development of toxicological quantitative structure-activity relationships (QSARs)." *PLoS ONE* (2023) | PLoS ONE 2023 **[V]** (via Consensus; 56 citations) | Extends classical QSAR best-practice guidance to ML: feature importance/reduction, cross-validation, hyperparameter optimisation, and the reproducibility/interpretability/generalisability deficits that block regulatory uptake | — |

### Transferability to pollutants / what it would take

**The uncomfortable, publishable truth:** for tabular toxicity endpoints with a few hundred to a few thousand labelled compounds — which is every environmental endpoint — **a well-tuned gradient-boosted tree on descriptors + fingerprints is still the model to beat** (3.3, 3.7, 3.8). Papers claiming foundation-model superiority usually (a) use random rather than scaffold splits, (b) do not tune the tree baseline, or (c) have leaked (3.4).

**Therefore the frontier move on this axis is *not* "use a foundation model."** It is:
1. **Use FM embeddings as a transfer-learning layer for the data-poor endpoint**, with a tree or linear head, and report against a tuned tree baseline on scaffold *and* similarity-stratified splits.
2. **Report cliff-specific metrics (MoleculeACE, 3.3)** — essential because environmental read-across lives and dies on activity cliffs (chain-length cut-offs in PFAS; halogenation-pattern cliffs in BFRs; a single methyl distinguishing an ER agonist from an inactive).
3. **Report the honest null result when it is a null result.** A rigorous paper showing *where* FMs do and do not beat descriptors on environmental endpoints, with leakage controls, is more publishable and more cited than another "our GNN got +0.02 AUC".

**Compute.** Fine-tuning MoLFormer-XL or Uni-Mol2 (84M–300M): one 24–80 GB GPU, hours to a day per endpoint. Re-pretraining MoLFormer from scratch on an environmental-chemistry corpus (DSSTox + PubChem subset): ~200–400 GPU-hours (3.1) — genuinely feasible, and a **domain-pretrained environmental chemical language model does not exist yet.** That is a clean contribution.

**Open weights:** MoLFormer-XL, ChemBERTa-2, Uni-Mol/Uni-Mol2, GROVER all open. TabPFNv2 open.

**Verdict: deployable in 3–6 months.** Low compute, high methodological-rigour payoff. The risk is that it reads as incremental unless the leakage/cliff/applicability-domain analysis is the centrepiece.

---

## Axis 4 — Transcriptome / omics-based prediction and perturbation models

### Key citations

| # | Citation | Venue / year | What it establishes | Data / code |
|---|---|---|---|---|
| 4.1 | Harrill, J. et al. "High-Throughput Transcriptomics Platform for Screening Environmental Chemicals." *Toxicol. Sci.* (2021), 197 citations | Toxicol Sci 2021 **[V]** (Consensus) | The EPA HTTr platform: TempO-Seq concentration–response in MCF7; signature-level concentration–response modelling; BPACs aligned with prior ToxCast HTS | tcplfit2, open; data on EPA CompTox |
| 4.2 | Harrill, J. et al. "Signature analysis of high-throughput transcriptomics screening data for mechanistic inference and chemical grouping." *Toxicol. Sci.* (2024), 39 citations | Toxicol Sci 2024 **[V]** (Consensus) | **1,751 additional ToxCast chemicals** in MCF7, 8 concentrations, 6 h. Predicts MeOA (ER, GR, RAR, NRF2/KEAP/ARE, AP-1), stratifies agonist potency, separates agonists from antagonists, finds novel ER modulators by UMAP that the ToxCast ER pathway model missed | Public |
| 4.3 | Bundy, J.L. et al. "High-Throughput Transcriptomics Screen of ToxCast Chemicals in U-2 OS Cells." *Toxicol. Appl. Pharmacol.* (2024), 28 citations | Tox Appl Pharmacol 2024 **[V]** (Consensus) | 1,201 chemicals × 8 concentrations. **Critically: BPACs agree only modestly (R² = 0.55) with Cell-Painting-derived phenotype-altering concentrations in the same cell line.** The orthogonality argument for using both modalities. | Public |
| 4.4 | Rogers, J.D. et al. "Integrating Transcriptomic and Targeted New Approach Methodologies into a Tiered Framework for Chemical Bioactivity Screening." *Environ. Health Perspect.* (2025). DOI 10.1289/EHP16024 | EHP 2025 **[V]** (Consensus) | **The best template for a prediction→validation paper.** 1,126 non-reference chemicals in U-2 OS + HepaRG; 201 selectively bioactive in ≥1 signature; 57 confirmed as selective NR agonists. Signature PODs were as or more sensitive than BPACs in 95.4% of cases. **Prospective test of 37 chemicals with no prior orthogonal data: 18/37 (49%) were bioactive against the predicted receptor.** | Public |
| 4.5 | O'Brien, J.M. et al. "Bioinformatic workflows for deriving transcriptomic points of departure: current status, data gaps, and research priorities." *Toxicol. Sci.* (2024), 45 citations | Toxicol Sci 2024 **[V]** (Consensus) | The consensus methods review for tPODs: standards of practice, sources of variability, data gaps, recommendations for regulatory use | — |
| 4.6 | Harrill, J. et al. "Exploring the effects of experimental parameters and data modeling approaches on in vitro transcriptomic point-of-departure estimates." *Toxicology* (2023), 31 citations | Toxicology 2023 **[V]** (Consensus) | **The essential honest-limits citation:** "tPODs calculated by different methods can vary by several orders of magnitude" and "tPODs are at least as sensitive to computational methods as to experimental conditions" (tcplfit2 vs BMDExpress vs PLIER) | — |
| 4.7 | Lee, H. et al. "Empirical Characterization of False Discovery Rates of Differentially Expressed Genes and Transcriptomic Benchmark Concentrations in Zebrafish Embryos." *Environ. Sci. Technol.* (2024), 15 citations | **ES&T 2024** **[V]** (Consensus) | Mock-treatment FDR characterisation across embryo pool sizes and sample sizes — the experimental-design guard-rail for anyone doing zebrafish HTTr | — |
| 4.8 | Reardon, A.J.F. et al. "From vision toward best practices: Evaluating in vitro transcriptomic points of departure for application in risk assessment using a uniform workflow." *Front. Toxicol.* (2023), 80 citations | Front Toxicol 2023 **[V]** (Consensus) | 6 datasets, 117 chemicals, 3 cell types, uniform workflow; httk translation of in vitro tPODs to AEDs; **most AEDs lower (more conservative) than apical PODs in CompTox** → protective. 7 outlier chemicals flagged. | — |
| 4.9 | Emberley-Korkmaz, S. et al. "Comparison of in vitro transcriptomic points of departure with fish acute and chronic toxicity values: a case study of rainbow trout cells exposed to pesticides." *Environ. Toxicol. Chem.* (2025) | ET&C 2025 **[V]** (Consensus) | 20 pesticides, RTgill-W1 (OECD 249), ExpressAnalyst. tPOD mode vs rainbow trout acute LC50: R² = 0.63; vs fish chronic lethal: R² = 0.59; vs chronic sublethal: R² = 0.40. **Quantitative in-vitro-to-in-vivo transferability for ecotoxicology.** | ExpressAnalyst.ca, free |
| 4.10 | Ahlmann-Eltze, C., Huber, W., Anders, S. "Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines." *Nat. Methods* **22**, 1657–1661 (2025). DOI 10.1038/s41592-025-02772-6 | Nat Methods 2025 **[V]** | **The decisive negative result.** scGPT and scFoundation are beaten by a *mean-of-training-examples* baseline. Geneformer, scBERT and UCE added in revision also underperform simple baselines. Shows scGPT's own linear comparator was set up to predict "no change" for unseen perturbations. FM gene embeddings + linear head beat the mean baseline but not a linear model on training-data embeddings. | Code public |
| 4.11 | Theodoris, C.V. et al. "Transfer learning enables predictions in network biology." *Nature* (2023) — Geneformer. Cui, H. et al. "scGPT: toward building a foundation model for single-cell multi-omics using generative AI." *Nat. Methods* (2024). scFoundation: "Large Scale Foundation Model on Single-cell Transcriptomics," bioRxiv 2023.05.29.542705 | Venues **[V]**; volumes/pages/full author lists **[U]** | The three perturbation FMs whose claims 4.10 undercuts | Open weights (HuggingFace / NVIDIA BioNeMo) |
| 4.12 | Arc Institute **STATE** virtual cell model (June 2025): State Embedding + State Transition modules; ~170M observational and >100M perturbational cells across 70 cell lines; **Cell_Eval** benchmark adding perturbation-strength and DE metrics. Claimed first model to consistently beat simple linear baselines; >50% improvement in perturbation-effect discrimination vs GEARS and scGPT on Tahoe-100M | Release + preprint; **peer-reviewed version not confirmed [U]**; all numbers are Arc's own | Direct answer to 4.10. Arc **Virtual Cell Challenge**: 2025 round >1,200 teams, >300 submissions; 2026 round = CRISPRi knockdown in six unseen cell lines | Weights released for non-commercial use |
| 4.13 | "Deep Learning-Based Genetic Perturbation Models Do Outperform Uninformative Baselines on Well-Calibrated Metrics." bioRxiv 2025.10.20.683304 | bioRxiv **[P]** | The rebuttal to 4.10 — the conclusion depends on metric calibration. Cite both; the controversy is the story. | **[U]** |
| 4.14 | Chandrasekaran, S.N. et al. JUMP Cell Painting **genetic** perturbation paper, *Nat. Methods* (2025), DOI 10.1038/s41592-025-02753-9. JUMP **chemical** dataset: 115,796 compounds, 1.53 billion single-cell profiles, bioRxiv 2023.03.23.534023 (publication status **[U]**) | Nat Methods 2025 **[V]** on DOI/venue; full author list **[U]** | The largest public morphological-profiling resource; 18 industry + non-profit partners | Images + profiles public (AWS) |
| 4.15 | "Cell Painting for cytotoxicity and mode-of-action analysis in primary human hepatocytes." bioRxiv 2025.01.22.634152 / PMC11785178 | **[P]** | **Primary human hepatocytes**, 1,085 compounds × 8 concentrations including known environmental contaminants, agrochemicals, food additives. Supervised ML predicted cytotoxicity and *cell-based* assay readouts but **not cell-free readouts** — an informative boundary. | **[U]** |
| 4.16 | "Deep Learning on High-Throughput Transcriptomics to Predict Drug-Induced Liver Injury" (PMC7728858) | **[U]** venue/year | 8-layer DNN on LINCS L1000 human cell-line profiles with DILIst labels, beating KNN/SVM/RF. The template for "predict in vivo outcome from in vitro transcriptomics" | — |

### Transferability to pollutants / what it would take

**This axis is where environmental science is closest to the frontier already** — EPA's HTTr programme (4.1–4.4) is world-leading, and the fish tPOD work (4.9) has no pharma equivalent. The frontier moves are:

1. **Multimodal fusion of HTTr + Cell Painting + targeted assays with a shared latent space.** 4.3 establishes that transcriptomic and morphological potencies agree only at R² = 0.55, so they are genuinely complementary. No one has published a model that predicts *in vivo* ecotoxicological outcome from the joint in vitro HTTr + morphology representation. All input data are public.
2. **Prospective validation, following the 4.4 template.** 18/37 prospective hits is the number to beat, and it is the single most credible design in this whole survey: predict → test → report the hit rate including misses.
3. **Perturbation FMs: use the controversy, don't ride the hype.** 4.10 vs 4.12/4.13 is an open, high-profile dispute. A paper that evaluates whether STATE/scGPT/Geneformer embeddings add anything over a linear baseline *for chemical* (not genetic) perturbations in a toxicologically relevant cell line, with Cell_Eval-style calibrated metrics, is a defensible and timely contribution. **Prediction: they will not add much, and publishing that cleanly is valuable.**
4. **Virtual-cell framing for ecotoxicology does not exist.** Every perturbation FM is trained on human (and some mouse) single-cell data. There is no zebrafish/daphnia/fathead-minnow perturbation foundation model. That is a real gap, but also a data gap — probably out of reach in 12 months.

**Compute.** HTTr/Cell-Painting reanalysis: CPU-bound, modest. Fine-tuning scGPT/Geneformer: 1–4 × 40–80 GB GPUs for days. Training a STATE-class model from scratch: not feasible for a mid-size lab (hundreds of GPU-days). **Use released weights.**

**Verdict: HTTr + Cell Painting fusion with prospective validation is deployable in 6–12 months** and is probably the single most publishable axis for an environmental lab, because the wet-lab validation loop is within reach. Training new perturbation FMs: no.

---

## Axis 5 — Toxicokinetics and dose context

### Key citations

| # | Citation | Venue / year | What it establishes | Code |
|---|---|---|---|---|
| 5.1 | Pearce, R.G., Setzer, R.W., Strope, C.L., Sipes, N.S., Wambaugh, J.F. "httk: R Package for High-Throughput Toxicokinetics." *J. Stat. Softw.* **79**(4) (2017). DOI 10.18637/jss.v079.i04 | J Stat Softw 2017 **[V]** | The standard open IVIVE engine: four TK models, Monte Carlo sampling, reverse dosimetry, Css/Vd/half-life. Paper version covered 553 chemicals (94 pharmaceuticals, 415 ToxCast) in human, rat, mouse, dog, rabbit | **CRAN `httk`, fully open** |
| 5.2 | Paul Friedman, K. et al. "Utility of In Vitro Bioactivity as a Lower Bound Estimate of In Vivo Adverse Effect Levels and in Risk-Based Prioritization." *Toxicol. Sci.* **173**(1), 202–225 (2020). DOI 10.1093/toxsci/kfz201; PMID 31532525 | Toxicol Sci 2020 **[V]** | **The foundational BER paper.** 448 chemicals: for 400 (89%), POD_NAM,95 < POD_traditional. For the 48 exceptions, the two PODs were typically within 10× and the group was **enriched for organophosphate and carbamate insecticides** (a directly environmental caveat). High-throughput exposure exceeded POD_NAM,95 for 11 substances. | httk + ToxCast, open |
| 5.3 | EPA httk parameter resource (Feb 2025 version): **7,569 HTTK data points or predictions** (Css, Vd, half-life). Canada's bioactivity–exposure-ratio science approach document uses httk v2.3 | EPA / ECCC, 2025 **[V]** on existence; exact figures from slide decks **[U]** | Current coverage. BER defined there as (lower bound of HTPP-derived AED CI) / (upper bound of SEEM3 exposure prediction) | Public |
| 5.4 | Wambaugh, J.F. et al. "Applying New Approach Methods for Toxicokinetics for Chemical Risk Assessment." *Chem. Res. Toxicol.* **38**(8) (2025) — and a companion *Toxicology* **515** (Aug 2025) paper on NAM-based risk prioritisation | 2025 **[V]** on venue/volume; author lists and titles **[U]** — re-verify | The current TK-NAM state of the art | — |
| 5.5 | "Collaborative evaluation of in silico predictions for high-throughput toxicokinetics" (2025) | **[U]** venue | Multi-group evaluation of *predicted* (rather than measured) TK parameters — the key uncertainty when no in vitro TK data exist for a pollutant | — |
| 5.6 | "Incorporating a dermal absorption route into high throughput toxicokinetic modeling." *J. Expo. Sci. Environ. Epidemiol.* (2026). DOI 10.1038/s41370-026-00881-8 | 2026 **[V]** on DOI/venue; authors **[U]** | Route extension; found dermal exposures reach bioactive plasma concentrations for only a small fraction of chemicals examined | httk extension |
| 5.7 | "High-throughput PBK modelling for dermal exposure: a pragmatic approach to predict systemic pharmacokinetics" (PMC13221391) | **[U]** | 52 compounds simulated from **QSAR-predicted physicochemical properties only, no compound-specific in vitro measurements** — the closest thing to "PBK from structure" | — |
| 5.8 | Thienpont, A. et al. "In vitro to in vivo extrapolation modeling to facilitate the integration of transcriptomics data into genotoxicity assessment." *Toxicology* (2025) | Toxicology 2025 **[V]** (Consensus) | Worked tPOD → AED pipeline for 10 reference genotoxicants in HepaRG; generic AEDs more conservative than biomarker-specific; transcriptomic AEDs < in vivo PODs for 6/9 | — |
| 5.9 | "Comparative transcriptomic points of departure analysis of pesticides in human Caco-2 and Hep G2 cells." *NAM Journal* (2026) | 2026 **[V]** (Consensus) | 19 pesticides; mass-balance modelling + IVIVE; ~50% (Caco-2) and ~70% (HepG2) of t-AEDs within one order of magnitude of chronic animal PODs | — |
| 5.10 | OECD guidance document on PBK modelling and IVIVE, with a reporting checklist and required input parameters (referenced in EPA's 2024 NAMs conference summary) | OECD **[V]** on existence; document number **[U]** | The regulatory frame a dose-relevant paper should cite | — |

### Transferability to pollutants / what it would take

**This is the cheapest and most decisive upgrade in the entire survey.** Nearly every ES&T prediction paper reports nominal in vitro concentrations or docking scores and stops. Adding:
- **free/intracellular concentration correction** (mass-balance in-well modelling — note 5.9 does this explicitly; for fish cells, IV-MBM EQP v2.1 as used in 4.9),
- **httk-based reverse dosimetry to an AED (mg/kg-bw/day)**, and
- **a bioactivity:exposure ratio against SEEM3 / ExpoCast or measured environmental concentrations**

converts "compound X binds receptor Y in silico" into "compound X is or is not plausibly active at realistic human/wildlife exposure." That is the difference between a screening paper and a risk-relevant paper, and reviewers at ES&T increasingly expect it.

**What it takes:** `httk` in R, a day to learn, a week to wire into an existing pipeline. The real work is sourcing Caco-2/HepG2/fish-cell clearance and fraction-unbound inputs, or accepting QSAR-predicted values and **propagating that uncertainty explicitly** (5.5, 5.7). For pollutants specifically, the known weak points are: high protein binding of PFAS and other anionic surfactants (standard f_up assays fail), ionisable species, and the adult-only parameterisation of most httk models.

**Genuinely novel move available:** httk/PBK for **non-mammalian** species. Fish, Daphnia and bird TK is where IVIVE is thinnest, and 4.9 shows the in vitro side is ready. A fish-specific IVIVE layer that converts RTgill-W1 tPODs into whole-body internal concentrations and then to water concentrations would be new and highly citable.

**Compute: negligible** (laptop/CPU).

**Verdict: deployable in 1–3 months.** No GPU needed. Highest benefit-to-cost ratio of any axis here — this should be in the paper regardless of what else is done.

---

## Axis 6 — Mixtures, transformation products, exposure, and chemical-space-wide hazard

### Key citations

| # | Citation | Venue / year | What it establishes | Code |
|---|---|---|---|---|
| 6.1 | Djoumbou-Feunang, Y. / Wishart group. "BioTransformer 3.0—a web server for accurately predicting metabolic transformation products." *Nucleic Acids Res.* **50**(W1), W115–… (2022) | NAR 2022 **[V]** on venue/volume; full author list **[U]** | Xenobiotic + endogenous metabolite prediction, reported 40–50% more accurate than earlier versions with fewer combinatorial blow-ups; **has an environmental-microbial option** | GitHub `Wishartlab-openscience/Biotransformer`, open |
| 6.2 | "Advancements in biotransformation pathway prediction: enhancements, datasets, and novel functionalities in enviPath" (2024); PMC11304562 | *J. Cheminform.* 2024 **[V]** on existence; volume/authors **[U]** | The environmental-specific biotransformation system. The 2024 update **reworked the prediction engine's evaluation to give a more candid picture of its performance** — i.e. earlier accuracy claims were optimistic. | enviPath, open/freemium |
| 6.3 | "Predictive modeling of biodegradation pathways using transformer architectures" (2025) | **[U]** venue — preprint | Transformer reaction prediction implemented *in* enviPath; tested on in vitro biotransformation and soil degradation of xenobiotics; model-agnostic | **[U]** |
| 6.4 | Bushuiev, R., Pluskal, T. et al. "MassSpecGym: A benchmark for the discovery and identification of molecules." NeurIPS 2024 Datasets & Benchmarks; arXiv 2410.23326 | NeurIPS 2024 **[V]** | **The benchmark that makes MS/ML claims falsifiable:** 231k high-quality spectra, 29k unique structures; three tasks (de novo generation, retrieval, spectrum simulation); **generalisation-enforcing splits**; finding: de novo structure generation from spectra is "exceptionally challenging" for current baselines | `pluskal-lab/MassSpecGym`, open |
| 6.5 | Stravs, M.A., Dührkop, K., Böcker, S., Zamboni, N. "MSNovelist: de novo structure generation from mass spectra." *Nat. Methods* **19**(7), 865–870 (2022). DOI 10.1038/s41592-022-01486-3 | Nat Methods 2022 **[V]** | Database-free structure generation: SIRIUS + CSI:FingerID fingerprint → encoder–decoder LSTM → SMILES. On 3,863 GNPS spectra: correct structure retrieved for 45%, ranked first for 25% (vs 39% top-1 for CSI:FingerID database search). CASMI 2016: 26% correct, 57% retrieved. **The honest read: de novo MS structure elucidation is a 25–45% proposition, not a solved problem.** | Open |
| 6.6 | Wang, H., Kuo, T.-C., Tseng, Y.J. "DeePFAS: Deep-Learning-Enabled Rapid Annotation of PFAS: Enhancing Nontargeted Screening through Spectral Encoding and Latent Space Analysis." *Environ. Sci. Technol.* **59**(46), 24841–24852 (2025). DOI 10.1021/acs.est.5c09769; PMID 41026849 | **ES&T 2025** **[V]** | The current ES&T frontier for ML-driven NTS: CNN+transformer spectral encoder projects raw MS2 into a chemical-structure latent space learned from a large unlabelled corpus; annotation by latent-space comparison with candidates; evaluated on wastewater | **GitHub `CMDM-Lab/DeePFAS`, open** |
| 6.7 | "Machine Learning-based Classification for the Prioritization of Potentially Hazardous Chemicals with Structural Alerts in Nontarget Screening." *Environ. Sci. Technol.* DOI 10.1021/acs.est.4c10498 | ES&T **[V]** on DOI/venue; authors/year **[U]** | Hazard-driven prioritisation of NTS features directly from MS2 — predicts hazard before identification | — |
| 6.8 | "Recent Advances in Implementation of Machine Learning for Environmental Nontarget Identification." *Environ. Health* (ACS) (2025). DOI 10.1021/envhealth.5c00091 | 2025 **[V]** on DOI/venue; authors **[U]** | The review to orient from. SIRIUS and CFM-ID are the most widely used ML tools in environmental NTS; covers library matching, database retrieval, de novo generation | — |
| 6.9 | "Critical review on in silico methods for structural annotation of chemicals detected with LC/HRMS non-targeted screening." *Anal. Bioanal. Chem.* (2024). DOI 10.1007/s00216-024-05471-x | ABC 2024 **[V]** on DOI/venue; authors **[U]** | Method-by-method critical assessment incl. MIST; wastewater test case | — |
| 6.10 | Lai, T.T., Kuntz, D., Wilson, A.K. "Molecular Screening and Toxicity Estimation of 260,000 Perfluoroalkyl and Polyfluoroalkyl Substances (PFASs) through Machine Learning." *J. Chem. Inf. Model.* **62**(19), 4569–4578 (2022). DOI 10.1021/acs.jcim.2c00374; PMID 36154169 | JCIM 2022 **[V]** | **The reference point for enumerated-chemical-space hazard mapping.** Generative ML produced >260,000 novel PFAS ("PFAS-AI-Gen"), then tiered screening (descriptors → docking → MD) against hPXR and PPARγ with CMC as industrial-suitability filter, benchmarked to GenX; 22 candidate substitutes nominated. | **[U]** |
| 6.11 | Matteo, G. et al. "High-throughput transcriptomics analysis of equipotent and human relevant mixtures of BPA alternatives reveal additive effects in vitro." *Arch. Toxicol.* (2025) | Arch Toxicol 2025 **[V]** (Consensus) | **The best modern mixtures design.** 7 mixtures × 12 components, MCF-7, 0.001–50 µM; tPODs by BMC modelling + an ERα transcriptomic biomarker; mixtures modelling tested additivity. All seven mixtures were additive across all tPODs modelled; mixtures and most components perturbed the same upstream regulators. | — |
| 6.12 | "Mathematical models for predicting the toxicity of micropollutant mixtures in water" (2025); PMC12455698 | review **[U]** venue | Current status: CA dominates, then IA, then QSAR/ML; IA may underestimate when components interact | — |
| 6.13 | "Morphological profiling of environmental chemicals enables efficient and untargeted exploration of combination effects." bioRxiv 2022.02.10.479889 | **[P]** | Cell Painting on mixtures across MCF7, A549, Caco-2, U-2 OS — the untargeted route to mixture MoA that does not presuppose CA or IA | — |
| 6.14 | MS2Quant (concentration prediction for unidentified features) and `patRoon` (automated NTS workflow) | referenced in 6.8 **[U]** | The missing link that makes NTS features dose-relevant | Open |

### Transferability to pollutants / what it would take

**This axis is intrinsically environmental — there is no pharma competition.** The frontier combination that nobody has published end-to-end:

> **enumerate → predict transformation products → predict hazard → predict MS2 → match against real NTS data → convert to concentration → mixture-additivity model → BER**

Each link now has open tooling: enviPath/BioTransformer (6.1–6.3) → an axis-3 hazard model with a declared applicability domain → CFM-ID/spectrum-simulation models benchmarked on MassSpecGym (6.4) → DeePFAS-style latent matching (6.6) → MS2Quant (6.14) → CA/IA plus a transcriptomic additivity test (6.11) → httk BER (axis 5). **Closing that loop on one chemical class (PFAS, OPFRs, or a pesticide-transformation-product set) in archived NTS data would be a flagship paper.**

**Honest limits to state up front:** de novo MS structure elucidation tops out at ~25–45% top-1/retrieval (6.5); enviPath's own 2024 re-evaluation was deliberately less flattering than earlier claims (6.2); and combinatorial transformation-product enumeration explodes, so a prioritisation criterion must be declared in advance.

**Compute.** Modest. Transformation-product enumeration and MS matching are CPU-bound. Spectrum-simulation / latent-encoder models: single GPU, hours to days. Enumerating and scoring 10⁵–10⁶ structures through a trained hazard model: hours on one GPU. The bottleneck is **data curation and chemistry judgement, not FLOPs.**

**Verdict: deployable in 6–12 months** for a lab that already has HRMS NTS data. If the lab does not generate its own NTS data, use public repositories (MassIVE/GNPS, NORMAN) — but then the novelty rests entirely on the computational loop.

---

## Axis 7 — Causal / mechanistic layers, uncertainty, and active learning

### Key citations

| # | Citation | Venue / year | What it establishes | Code |
|---|---|---|---|---|
| 7.1 | "Computational approaches to adverse outcome pathway networks: advances in construction, quantification, and regulatory decision support." ScienceDirect, PII S2468111326000307 (2026) | 2026 **[V]** on existence/PII; authors/journal **[U]** (likely *Current Opinion in Toxicology* — re-verify) | The current review of ML/DL/NLP/knowledge-graph methods for building, enriching, quantifying and validating AOP networks. States plainly that **most AOP use remains qualitative, which blocks dose–response extrapolation when pathways interact**, and proposes curated training sets + NLP extraction + supervised/unsupervised key-event prioritisation + KGs with probabilistic inference for causal direction. Mentions a toxicological knowledge graph (ToxKG) built on ComptoxAI. | — |
| 7.2 | "Quantification of an Adverse Outcome Pathway Network by Bayesian Regression and Bayesian Network Modeling" (2020); PMC7820971 | 2020 **[V]** on existence; venue/authors **[U]** | The canonical qAOP-as-Bayesian-network demonstration (AOP #245). **Hard constraint: a Bayesian network cannot contain feedback loops** — which rules out many real toxicity pathways. | — |
| 7.3 | "Proof of concept for quantitative adverse outcome pathway modeling of chronic toxicity in repeated exposure" (2024); PMC10899215 | 2024 **[V]** on existence; venue **[U]** | **Dynamic** Bayesian network estimating outcome probabilities from earlier upstream events — the route past the no-feedback limitation | — |
| 7.4 | Romano, J.D. et al. ComptoxAI; and the PSB 2022 paper training a GNN on a ComptoxAI chemical–assay–gene subgraph to predict Tox21 assay activation (*Pac. Symp. Biocomput.* **27**, 2022) | PSB 2022 **[V]** on venue/volume; full author list **[U]** | The reference chemical–gene–disease knowledge graph for toxicology (Neo4j; AOP-DB, DSSTox, DrugBank, Hetionet, PubChem, Reactome, Tox21), with a worked graph-ML task | **ComptoxAI, open** |
| 7.5 | AIDTox (ComptoxAI + DTox): interpretable DL using chemical–gene connections + gene–pathway annotations to predict HepG2/HEK293 cytotoxicity; bioRxiv 2022.10.07.511348, later published | **[P]** → published **[U]** | The template for *mechanistically interpretable* toxicity prediction — the model's internal nodes are pathways, not latent dimensions | — |
| 7.6 | "Graph Neural Network-Based Toxicity Prediction by Integrating Molecular Fingerprints and Knowledge Graph Features." *Toxics* (Nov 2025); PMC12656225 | Toxics 2025 **[V]** on existence/venue; authors **[U]** | ToxKG: extends ComptoxAI with PubChem/Reactome/ChEMBL, fuses fingerprint + KG features in a GNN. **The most direct precedent for "structure + mechanism graph" hybrid prediction.** | — |
| 7.7 | "AOPTK: Open-Source Software for AI-Assisted Toxicological Literature Analysis." bioRxiv 2026.10.29.761316 | **[P]**, very recent | LLM-assisted PubMed/Europe PMC retrieval + PDF full-text extraction. Gap-junction case study: **81% agreement with an expert-curated inhibitor list and 95% accuracy on inhibition vs no-inhibition across 86 publications.** The best quantified LLM-to-AOP result found. | Open-source Python package |
| 7.8 | "AOP-Smart: A RAG-Enhanced Large Language Model Framework for Adverse Outcome Pathway Analysis." arXiv 2604.10874 | arXiv **[P]** | RAG-LLM framework specifically for AOP analysis; results not verified | **[U]** |
| 7.9 | "ToxReason: A Benchmark for Mechanistic Chemical Toxicity Reasoning via Adverse Outcome Pathway." arXiv 2604.06264 | arXiv **[P]** | A benchmark for LLM mechanistic toxicity reasoning — needed to make LLM-AOP claims falsifiable | **[U]** |
| 7.10 | "Automated Continuous LLM-driven Biomedical Literature Mining for a Large-Scale Hepatotoxicity Knowledge Base." bioRxiv 2026.11.09.765369 | **[P]**, days old | Fixed-schema LLM extraction at scale: **189,212 findings on 17,002 chemicals from 53,575 articles (1995–2026)** | **[U]** |
| 7.11 | "Artificial Intelligence in Adverse Outcome Pathways: A Review of Strategies for Automated Information Extraction, Quantitative Analysis, and Iterative Optimization." *MDPI* 3042-8637/1/1/9 (2025) | **[V]** on existence; journal name **[U]** (new MDPI title) | NLP extraction of MIEs, KEs and KERs from literature | — |
| 7.12 | "A Bayesian active learning platform for scalable combination drug screens" (BATCHIE). *Nat. Commun.* (Jan 2025). DOI 10.1038/s41467-024-55287-7 | Nat Commun 2025 **[V]** on DOI/venue; authors **[U]** | **The best-validated active-learning-chooses-the-next-experiment paper**: modified diameter-based acquisition built for noisy probabilistic outcomes; retrospective *and prospective* validation. Directly portable to mixture/combination ecotoxicology screens. | Open |
| 7.13 | "Deep Bayesian Experimental Design for Drug Discovery." In: Springer, DOI 10.1007/978-3-031-72381-0_12 (2025) | **[V]** on DOI; authors **[U]** | Applies BED to **toxicity** modelling: SMILES-pretrained BERT features; active learning selects a higher share of toxic compounds than random (helps with class imbalance); pretrained features beat ECFP on Tox21 | **[U]** |
| 7.14 | Conformal prediction for hazard prioritisation: "Predicting Endocrine Disruption Using Conformal Prediction – A Prioritization Strategy to Identify Hazardous Chemicals with Confidence." *Chem. Res. Toxicol.* (2022). DOI 10.1021/acs.chemrestox.2c00267; PMC9846826 | Chem Res Toxicol 2022 **[V]** on DOI/venue; authors **[U]** | Conformal prediction for endocrine-disruptor prioritisation; nonconformity scores as the applicability-domain measure | Open methods |
| 7.15 | "Beyond Heuristics: A Model-Agnostic Framework for Uncertainty Quantification in QSAR via Adaptive Conformal Prediction." *Chem. Res. Toxicol.* **39**(7), 1357–… (2026) | Chem Res Toxicol 2026 **[V]** on venue/volume; authors **[U]** | Argues for replacing binary "out of applicability domain" flags with **conformal intervals that inform testing priorities** rather than discarding predictions. The modern AD framing. | **[U]** |
| 7.16 | "Conformal prediction-based machine learning in Cheminformatics: Current applications and new challenges." ScienceDirect PII S2667318525000030 (2025) | 2025 **[V]** on PII; journal/authors **[U]** | Review; tables of ToxCast/Tox21/PubChem conformal applications. Caveat from an earlier ecotoxicology chapter: standard CP may be unsuitable for strongly imbalanced datasets. | — |
| 7.17 | "Introducing conformal prediction in predictive modeling for regulatory purposes. A transparent and flexible alternative to applicability domain determination." *Regul. Toxicol. Pharmacol.* / ScienceDirect PII S0273230014003432 (2014) | 2014 **[V]** on PII; venue **[U]** | The regulatory argument: CP satisfies the OECD applicability-domain principle | — |

### Transferability to pollutants / what it would take

**The move that most clearly separates a frontier paper from the ES&T norm is closing the loop: prediction → calibrated uncertainty → chosen experiment → measured result → updated model.** Nobody in environmental toxicology has published this properly. All the pieces exist:
- calibrated uncertainty: conformal prediction (7.14–7.17), already demonstrated on ToxCast/Tox21 and endocrine disruption;
- acquisition: BATCHIE-style Bayesian active learning (7.12), validated prospectively;
- mechanism: ComptoxAI/ToxKG graph features (7.4, 7.6) to make the predictions interpretable rather than black-box;
- literature-to-AOP: AOPTK (7.7) with a *quantified* agreement rate against expert curation — crucially, 81%/95% means the LLM layer can be reported with error bars instead of enthusiasm.

**A concrete 12-month design:** build a conformal-calibrated hazard model for a pollutant class on an environmental endpoint; use Bayesian active learning to select 20–40 compounds for an in-house assay (reporter gene, RTgill-W1 tPOD, zebrafish); measure them; report the hit rate against random and against an uncertainty-blind baseline; update the model; and overlay the resulting active chemicals on an AOP network assembled semi-automatically with AOPTK-style extraction *with the agreement rate reported*. That is a methods paper, a dataset paper and a mechanism paper at once.

**Honest limits to state:** Bayesian networks for qAOP cannot represent feedback (7.2) — use dynamic BNs (7.3) or say why static is acceptable. Conformal prediction degrades under the severe class imbalance typical of toxicity data (7.16) — use Mondrian/class-conditional CP and show the calibration plots. LLM-extracted KERs must be expert-audited, with the audit sample size and agreement rate reported (7.7); an unaudited LLM-built AOP is not evidence.

**Compute: low.** Conformal wrappers, graph ML on a KG subgraph, and active-learning acquisition all run on one GPU or even CPU. The cost is wet-lab assay capacity, not compute.

**Verdict: deployable in 6–12 months,** and it is the axis where a mid-size lab's *experimental* capability becomes the competitive advantage rather than a liability.

---

## Axis 8 — Honest limits: reproducibility, leakage, standards

### Key citations

| # | Citation | Venue / year | What it establishes |
|---|---|---|---|
| 8.1 | Zhu, J.-J., Yang, M., Ren, Z.J. "Machine Learning in Environmental Research: Common Pitfalls and Best Practices." *Environ. Sci. Technol.* **57**(46), 17671–17689 (2023). DOI 10.1021/acs.est.3c00026; PMID 37384597 | **ES&T 2023** **[V]** (741 citations per Consensus) | **The in-field standard.** >30 key items, evidence base of 148 highly cited articles: terminology misuse, sample/feature size, data enrichment and feature selection, randomness assessment, **data leakage management**, data splitting, method selection and comparison, optimisation and evaluation, explainability and causality. |
| 8.2 | Zhu, J.-J., Boehm, A.B., Ren, Z.J. "Environmental Machine Learning, Baseline Reporting, and Comprehensive Evaluation: The EMBRACE Checklist." *Environ. Sci. Technol.* **58**(45), 19909–19912 (2024). DOI 10.1021/acs.est.4c09611; PMID 39469888 | **ES&T 2024** **[V]** | **The checklist to comply with explicitly.** Eight sections following the ML development workflow, for authors, reviewers, editors and readers; maintained in an open repository. A later ES&T Letters methods-guidance article states that **any method using machine learning must address EMBRACE requirements** ("Essential Elements of Manuscripts Describing New Methods for Measuring Environmental Contaminants…", DOI 10.1021/acs.estlett.6c00742 **[V]** on DOI; authors/year **[U]**). **Filling in EMBRACE as an SI table is close to free and visibly raises the paper's standard.** |
| 8.3 | Kapoor, S., Narayanan, A. "Leakage and the reproducibility crisis in machine-learning-based science." *Patterns* (2023), 2,315 citations; arXiv 2207.07048 | Patterns 2023 **[V]** (Consensus) | **17 fields, 294 affected papers**; a taxonomy of **eight leakage types**; model info sheets; and a reproducibility study where corrected complex ML models did not substantively beat decades-old logistic regression. |
| 8.4 | Kapoor, S. et al. "REFORMS: Consensus-based Recommendations for Machine-learning-based Science." *Sci. Adv.* (2024), 256 citations | Science Advances 2024 **[V]** (Consensus) | 32-question checklist + guidelines, consensus of 19 researchers across CS, data science, maths, social and biomedical science. The cross-disciplinary complement to EMBRACE. |
| 8.5 | Stock, A., Gregr, E.J., Chan, K.M.A. "Data leakage jeopardizes ecological applications of machine learning." *Nat. Ecol. Evol.* (2023). DOI 10.1038/s41559-023-02162-1 | Nat Ecol Evol 2023 **[V]** on DOI/venue; author initials **[U]** | Commentary arguing discipline-specific model info sheets are needed; nearest analogue for environmental/ecological leakage |
| 8.6 | van Tilborg et al. 2022 + 2023 correction (see 3.3) | JCIM **[V]** | Activity cliffs; **and a published correction caused by a train/test splitting bug** — itself the cleanest available illustration that splitting code is where leakage hides |
| 8.7 | "Critical Assessment of ML models for ADMET Prediction in TDC leaderboards" (see 3.4) | **[U]** | Fixing a split function dropped two gradient-boosting models substantially down the leaderboard |
| 8.8 | "Illusions of Accuracy: Widespread Data Leakage Distorts Machine Learning Results in Biochar Research." *GCB Bioenergy* (2026). DOI 10.1111/gcbb.70173 | 2026 **[V]** on DOI/venue; authors **[U]** | A domain-specific environmental leakage audit; recommends journals require transparent reporting of CV procedures, leakage testing, data documentation and reproducibility practices |
| 8.9 | Yan, Z. et al. "A Tutorial on Best Practices and Pitfalls in Applying Machine Learning to Environmental Research." *ACS Environ. Au* **6**(4), 553–… (2026) | ACS Environ Au 2026 **[V]** (Consensus + ACS page) | The newest in-field tutorial: integrating domain knowledge into workflow design, preprocessing, development, evaluation, interpretability; recurring pipeline pitfalls. Notes leakage from improper handling of **temporal or spatial** information — relevant to monitoring-data models. |
| 8.10 | Koldasbayeva, D. et al. "Challenges in data-driven geospatial modeling for environmental research and practice." *Nat. Commun.* (2024), 262 citations | Nat Commun 2024 **[V]** (Consensus) | Imbalanced data, **spatial autocorrelation**, generalisation and uncertainty estimation — the leakage mode unique to environmental data |
| 8.11 | "Data leakage in machine learning studies creep into meta-analytic estimates of predictive performance" (PMC12602356) | **[U]** | Leakage propagates upward: biased primary studies bias meta-analytic performance estimates |
| 8.12 | Belfield, S.J. et al. (see 3.9) | PLoS ONE 2023 **[V]** | Best-practice guidance specifically for *toxicological* ML-QSAR |

### What a frontier paper must therefore do

1. **Scaffold split AND a chemical-similarity-stratified (or time/assay-stratified) split**, reported side by side with a random split so the inflation is visible.
2. **Fully tuned classical baselines** (RF, XGBoost on descriptors + fingerprints) — 3.7/3.8 say they may well win, and a deep model that beats a *tuned* tree is a real result.
3. **Activity-cliff metrics** (3.3) and **calibrated uncertainty / conformal applicability domain** (7.14–7.16) rather than a binary AD flag.
4. **Complete the EMBRACE checklist in the SI** (8.2) — ES&T now effectively expects it — and consider REFORMS (8.4) as well.
5. **Preprocessing fitted on training folds only**; explicit statements on spatial/temporal autocorrelation (8.9, 8.10) for any monitoring-data component.
6. **Multi-seed runs with dispersion reported**, and all splits/code/weights deposited.
7. **Report the misses.** The 4.4 design (18/37 prospective hits) is more persuasive than any AUC.

**Verdict: deployable immediately, costs nothing, and is the single cheapest credibility upgrade available.**

---

## Cross-cutting: what "above the ES&T norm" actually means

The ES&T norm fails on five structural counts, each with a specific remedy:

| Norm's weakness | Frontier remedy | Axis |
|---|---|---|
| Rigid-receptor docking score treated as affinity | Co-folding with training-similarity stratification + PoseBusters validity, or alchemical RBFE within a congeneric series | 1, 2 |
| Nominal concentration, no dose context | Free/intracellular concentration correction + httk reverse dosimetry + BER | 5 |
| Random-split QSAR with untuned baselines | Scaffold + similarity-stratified splits, tuned trees, cliff metrics, conformal AD, EMBRACE | 3, 8 |
| Single-modality, single-receptor | HTTr + Cell Painting + targeted assay fusion with prospective validation | 4 |
| One-shot prediction, no feedback | Calibrated uncertainty → Bayesian active learning → measure → update | 7 |

---

## Ranked: the five methodological moves with the highest marginal value

1. **Dose-relevant everything (axis 5).** Free-concentration correction + httk reverse dosimetry to AEDs + bioactivity:exposure ratio against SEEM3/ExpoCast or measured environmental concentrations. One week of work; transforms the claim from "binds in silico" to "plausibly active at real exposure". Cite 5.1, 5.2, 4.8.
2. **A training-similarity-stratified, PoseBusters-validated co-folding benchmark for pollutant–receptor complexes (axis 1).** Does not exist. Build the set from PDB, run Boltz-2 + Protenix + AF3 multi-seed, report enrichment from native confidence metrics, compare against Vina/DOCK, and stratify by similarity to the training cutoff. Cite 1.3, 1.4, 1.2, 1.5; beat 1.12.
3. **Prospective, uncertainty-driven predict→test→update loop (axes 7 + 8).** Conformal-calibrated model → Bayesian active learning selects 20–40 compounds → in-house assay → report hit rate vs random and vs uncertainty-blind, plus the misses. Cite 7.12, 7.14, 7.15 and follow the 4.4 design.
4. **Alchemical RBFE with ML-potential-informed parameters for one pollutant congeneric series, validated against measured ΔΔG (axis 2).** PFAS–TTR / PFAS–serum albumin / BFR–TRβ are the obvious targets. Expect ~1.5–2.5 kcal/mol. Fully open stack (OpenFE + AIMNet2). Cite 2.2, 2.7, 2.3.
5. **Multimodal HTTr + Cell Painting fusion predicting an in vivo ecotoxicological endpoint (axis 4).** Justified by the R² = 0.55 orthogonality in 4.3; all input data public; validated in the 4.4 prospective style. Cite 4.2, 4.3, 4.4, 4.9; frame the perturbation-FM question honestly via 4.10 vs 4.12/4.13.

**Runner-up (highest novelty, highest risk):** the closed enumerate → biotransform → predict hazard → simulate MS2 → match in archived NTS data → quantify → mixture-model → BER loop for one chemical class (axis 6). No pharma competition, entirely open tooling, but it depends on NTS data access and on accepting a 25–45% structure-elucidation ceiling (6.5).

---

## Items flagged for re-verification before submission

- Abramson et al. 2024 AF3 volume/pages (1.1) — from prior knowledge, not confirmed this session.
- Schindler et al. 2020 "RMSE ≈ 1.1 kcal/mol" (2.1) — abstract does not state it; check full text/SI.
- Uni-Mol2 reported +27% QM9 / +14% COMPAS-1D (3.2) — secondary summaries only.
- The published journal version of Runs N' Poses (1.3) — PMC13661253, journal/volume unknown.
- Mac1 prospective co-folding (1.6) and AF3 ligand-discovery (1.7) author lists.
- OpenFE collaborative assessment (2.2) author list; Nat Comput Sci ABFE (2.3) authors/volume.
- Wambaugh et al. 2025 TK-NAM titles and author lists (5.4).
- Axis-7 review 7.1 journal name; ComptoxAI PSB 2022 full author list (7.4).
- All Geneformer / scGPT / scFoundation volumes and full author lists (4.11).
- STATE (4.12) peer-reviewed status and all quoted performance figures (currently vendor-reported only).
- Every entry tagged **[U]** above.
