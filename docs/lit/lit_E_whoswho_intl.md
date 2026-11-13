# WHO'S-WHO: Predictive / Computational Environmental Toxicology Outside Mainland China
### Compiled 2026-11-13 for a Chinese environmental-toxicology lab (high-information larval/adult zebrafish behavioural phenotyping + transcriptomics; LC-MS/MS + non-target HRMS available) aiming above the current ES&T prediction norm.

**Verification standard used.** Every paper in the tables below was retrieved from PubMed (title / journal / year / DOI as indexed). Where a claim could not be confirmed from a primary indexed record it is explicitly marked **[unverified]**. Affiliations were checked by web search where they were likely to have changed. Nothing in this file is reconstructed from memory.

**Known gaps / caveats (read before using):**
- api.openalex.org is blocked in this container, and pubs.acs.org refuses automated fetch, so citation counts and some ACS front-matter (volume/page) could not be independently confirmed. DOIs and years are from PubMed and are reliable; volume/page numbers are given only where PubMed returned them.
- PubMed author-initial searches are ambiguous for common names (Shah I, Bender A, Hartung T, Song Y, Xia J, Martin JW). Where ambiguity could not be resolved, only papers whose author list/affiliation I could see are listed.
- A separate agent covers mainland China. Chinese-affiliated papers appear here only where they are co-authored with a listed non-Chinese group, or where they define the current methodological bar.

---

## TIER 1 — Groups that set the standard the field now follows

### 1. US EPA Center for Computational Toxicology and Exposure (CCTE), Research Triangle Park, NC
**PIs:** Russell S. Thomas (Director, confirmed on EPA's CCTE page), Katie Paul Friedman, Richard Judson, Imran Shah, Grace Patlewicz, John Wambaugh, Antony J. Williams, Christopher Grulke, Joshua Harrill, Logan Everett, Jon Sobus, Kristin Isaacs, Stephanie Padilla.
**Signature contribution:** The whole industrial stack — ToxCast/Tox21 screening data, the `tcpl`/`invitrodb` curve-fitting and hit-calling standard, high-throughput transcriptomics (HTTr) and transcriptomic points of departure (tPODs), high-throughput toxicokinetics (`httk`), Generalised Read-Across (GenRA), DSSTox/CompTox Chemicals Dashboard, and INTERPRET NTA for non-target analysis. In practice they define the *units* an ES&T prediction paper has to be expressed in (AC50, POD, administered equivalent dose, bioactivity:exposure ratio).

| Paper | Year | Journal | DOI |
|---|---|---|---|
| The ToxCast pipeline: updates to curve-fitting approaches and database structure (Feshuk M, Kolaczkowski L, Dunham K, Davidson-Fritz SE, Carstens KE, Brown J, Judson RS, Paul Friedman K) — Front Toxicol 5:1275980 | 2023 | Frontiers in Toxicology | 10.3389/ftox.2023.1275980 |
| Exploring the effects of experimental parameters and data modeling approaches on in vitro transcriptomic point-of-departure estimates (Harrill JA, Everett LJ, Haggard DE, Bundy JL, Willis CM, Shah I, Paul Friedman K, Basili D, Middleton A, Judson RS) — Toxicology 501:153694 | 2023 | Toxicology | 10.1016/j.tox.2023.153694 |
| Signature analysis of high-throughput transcriptomics screening data for mechanistic inference and chemical grouping (Harrill JA, Everett LJ, Haggard DE, Word LJ, Bundy JL, … Judson R) | 2024 | Toxicological Sciences | 10.1093/toxsci/kfae108 |
| Integration of new approach methods for the assessment of data-poor chemicals (Paul Friedman K, Thomas RS, Wambaugh JF, Harrill JA, Judson RS, Shafer TJ, Williams AJ, …) | 2025 | Toxicological Sciences | 10.1093/toxsci/kfaf019 |
| Integrating Transcriptomic and Targeted New Approach Methodologies into a Tiered Framework for Chemical Bioactivity Screening (Rogers JD, Bundy JL, Harrill JA, Judson RJ, Paul-Friedman K, Everett LJ) | 2025 | Environmental Health Perspectives | 10.1289/EHP16024 |
| Characterizing Accuracy of Model Predictions for Chemical Concentration in High Throughput Screening Assays (Scherer MN, Feshuk M, Armitage JM, Arnot JA, …) | 2026 | Environmental Science & Technology | 10.1021/acs.est.5c10195 |
| Collaborative evaluation of in silico predictions for high throughput toxicokinetics (Wambaugh JF, Sipes NS, Padilla Mercado G, Arnot JA, Bertato L, Brown TN, Chirico N, Cook C, …) | 2025 | Toxicology in Vitro | 10.1016/j.tiv.2025.106150 |
| Prioritizing Chemical Candidates from Non-targeted Analysis Using Metadata, Spectral Similarity, and Hazard Scoring within INTERPRET NTA (Chao A, Minucci JM, Ferland TM, Carr ET, Janesch G, … Williams AJ) | 2025 | Analytical Chemistry | 10.1021/acs.analchem.5c02223 |
| Toward Metabolic Similarity in Read-Across: A Case Study Using Graph Convolutional Networks to Predict Genotoxicity Outcomes from Simulated Metabolic Networks (Hagan B, Groff L, Patlewicz G, Shah I) | 2025 | Chemical Research in Toxicology | 10.1021/acs.chemrestox.5c00120 |
| Building a compendium of expert driven read-across cases to facilitate an analysis of the contribution that different similarity contexts play in read-across performance (Patlewicz G, Charest N, Ross A, Bledsoe HC, Vidal J, … Shah I) | 2025 | Computational Toxicology | 10.1016/j.comtox.2025.100366 |
| The effect of noise on the predictive limit of QSAR models (Kolmar SS, Grulke CM) | 2021 | Journal of Cheminformatics | 10.1186/s13321-021-00571-7 |
| Sourcing data on chemical properties and hazard data from the US-EPA CompTox Chemicals Dashboard: A practical guide for human risk assessment (Williams AJ, Lambert JC, Thayer K, Dorne JLCM) | 2021 | Environment International | 10.1016/j.envint.2021.106566 |

**Experimental pairing:** In-house ToxCast/Tox21 battery (hundreds of targeted assays), HTTr (TempO-Seq in MCF7/HepaRG/U-2 OS), microelectrode-array (MEA) neurotoxicity, zebrafish DNT behaviour (Padilla), high-content imaging (Nyffeler/Harrill), in vitro TK (Wetmore). They do their own wet work at scale — this is not a dry-lab-only group.
**Public assets:** invitroDB (v4.x) + `tcpl`/`tcplfit2` R packages; `httk` R package (CRAN); CompTox Chemicals Dashboard + DSSTox (comptox.epa.gov/dashboard); GenRA (web + API); ToxRefDB; OPERA models (jointly with NICEATM); INTERPRET NTA; HTTr signature catalogues; Abstract Sifter (F1000Res 2026, 10.12688/f1000research.160617.2).
**Computational ceiling / collaboration:** Ceiling is deliberately *conservative* — they favour interpretable, auditable, regulatory-defensible models (XGBoost/random forest, nearest-neighbour read-across, Hill/exponential curve fits) over deep learning. Their genuinely novel 2025–26 computational work is in graph-convolutional metabolic read-across (Shah/Patlewicz) and tPOD statistics. A mid-size lab should treat CCTE as **infrastructure to build on, not a competitor**: their data and code are fully open, licensing-free, and their staff routinely co-author with external labs. Caveat: US federal science has been under resource pressure; do not design a project that depends on a new EPA data generation commitment.

---

### 2. Helmholtz Centre for Environmental Research (UFZ), Leipzig / Tübingen — Beate I. Escher
**PIs:** Beate I. Escher (Cell Toxicology, UFZ + Univ. Tübingen); Luise Henneberger, Maria König, Georg Braun (group members); linked UFZ departments: Martin Krauss & Werner Brack (Exposure Science; Brack now also Goethe Univ. Frankfurt), Stefan Scholz & Wibke Busch & Tamara Tal (Ecotoxicology / Bioanalytical Ecotoxicology), Jana Schor (bioinformatics), Qiuguo Fu (Analytical chemistry).
**Signature contribution:** Quantitative mixture toxicology. Iceberg modelling (what fraction of a measured bioassay effect is explained by quantified chemicals — usually <1–5%), bioanalytical equivalent concentrations (BEQ), effect-based trigger values (EBTs), mass-balance / free-concentration models for in vitro assays, and baseline-toxicity QSARs as the reference against which specificity is judged. **This is the group whose numeric framework an ES&T mixture/effect paper is graded against.**

| Paper | Year | Journal | DOI |
|---|---|---|---|
| Characterizing the marine mammal exposome by iceberg modeling, linking chemical analysis and in vitro bioassays (Reiter EB, Escher BI, Rojo-Nieto E, Nolte H, Siebert U, … Jahnke A) | 2023 | Environ Sci Process Impacts | 10.1039/d3em00033h |
| Application of Effect-Based Methods to Water Quality Monitoring: Answering Frequently Asked Questions by Water Quality Managers, Regulators, and Policy Makers (Neale PA, Escher BI, de Baat ML, Dechesne M, Dingemans MML, … Leusch FDL) | 2023 | Environmental Science & Technology | 10.1021/acs.est.2c06365 |
| Following the Mixtures of Organic Micropollutants with In Vitro Bioassays in a Large Lowland River from Source to Sea (Hommel E, König M, Braun G, Krauss M, Kamjunke N, Brack W, … Escher BI) — ACS Environ Au 5(4):363–375 | 2025 | ACS Environmental Au | 10.1021/acsenvironau.4c00059 |
| Role of Suspended Particulate Matter for the Transport and Risks of Organic Micropollutant Mixtures in Rivers (Niu L, Gärtner AAE, König M, Krauss M, Spahr S, … Escher BI) | 2025 | Environmental Science & Technology | 10.1021/acs.est.4c13378 |
| Beyond Estrogenicity: A Comparative Assessment of Bisphenol A and Its Alternatives in In Vitro Assays Questions Safety of Replacements (Srebny V, Henneberger L, König M, Huchthausen J, Braasch J, … Escher BI) | 2025 | Environmental Science & Technology | 10.1021/acs.est.5c07018 |
| DYNAMEX: A Time-Resolved Model for Predicting Distribution of Chemicals in In Vitro Cell Assays (Fischer FC, Geyer L, Rodriguez M, Henneberger L, Escher BI) | 2026 | Environmental Science & Technology | 10.1021/acs.est.6c06087 |
| Predicting the immunotoxic potential of chemical mixtures based on their endocrine activity profiles via computational modeling and in vitro bioassays (Braun G, Hilscherová K, van Brummelen S, Pieters R, Smutná M, … Escher BI) | 2026 | Environment International | 10.1016/j.envint.2026.110413 |
| In Vitro Bioassay Evidence for Chemical Mixture Propagation from the Environment to Humans (Escher B, Scholze M, Margalef M, König M, Valente MJ, … Vinggaard AM) | 2026 | Environmental Science & Technology | 10.1021/acs.est.6c00908 |
| Mapping disease-linked AOPs to inform bioassay selection for chemical hazard assessment (Stevens S, Muncke J, Escher BI) | 2026 | Environment International | 10.1016/j.envint.2026.110465 |
| The Role of ES&T in Advancing Environmental Toxicology and Chemical Risk Assessment: Past, Present, and Future (Escher BI, Hermens JLM, Sumpter JP, Ankley GT) | 2026 | Environmental Science & Technology | 10.1021/acs.est.6c03315 |

**UFZ zebrafish/data-driven sub-group (directly relevant to the lab's experimental strength):**

| Paper | Year | Journal | DOI |
|---|---|---|---|
| Leveraging Zebrafish Embryo Phenotypic Observations to Advance Data-Driven Analyses in Toxicology (Michaelis P, Klüver N, Aulhorn S, Bohring H, Bumberger J, … Busch W) | 2025 | Environmental Science & Technology | 10.1021/acs.est.4c11757 |
| Uptake and Biotransformation Govern the Toxicity of Reactive Acrylamides in a Zebrafish Embryo Model: Implications for NAM-Based Hazard Assessment (Grasse N, Scholz S, Reemtsma T, Fu Q) | 2026 | Environmental Science & Technology | 10.1021/acs.est.5c10178 |
| The zebrafish visual and acoustic motor response (VAMR) assay has the potential to add value to the developmental neurotoxicity in vitro battery (Spath J, Raab J, Schor J, Scholz S, Gutsfeld S, … Tal T) | 2026 | NeuroToxicology | 10.1016/j.neuro.2026.103414 |
| Dynamics in zebrafish development define transcriptomic specificity after angiogenesis inhibitor exposure (Nöth J, Michaelis P, Schüler L, Scholz S, Krüger J, … Busch W) | 2025 | Archives of Toxicology | 10.1007/s00204-024-03944-7 |
| High-Throughput Effect-Directed Analysis of Androgenic Compounds in Hospital Wastewater: Identifying Effect Drivers through Non-Target Screening Supported by Toxicity Prediction (Alvarez-Mora I, Muratuly A, Johann S, Arturi K, Jünger F, … Muz M) | 2025 | Environmental Science & Technology | 10.1021/acs.est.4c09942 |
| Comparative toxicity of plant protection products, their active substances and mixtures in zebrafish embryos and HepaRG cells (Nissen B, Stagkos-Georgiadis A, Krauss M, Bloch D, Busch W) | 2026 | Archives of Toxicology | 10.1007/s00204-025-04290-y |

**Experimental pairing:** In-house CALUX/AREc32/ER-GeneBLAzer bioassay battery with measured free concentrations and mass-balance correction; large-volume passive sampling and solid-phase extraction; UFZ zebrafish embryo high-content phenotyping (FET+behaviour), LC-HRMS target/non-target (Krauss).
**Public assets:** Published BEQ / EBT value sets and baseline-toxicity QSAR parameters in SI of the papers above; UFZ zebrafish phenotype ontology and datasets described in the ES&T 2025 Michaelis paper (data at UFZ/Zenodo — **asset location [unverified]**); PrecisionTox 200-chemical library (jointly, see Tier 2 #8).
**Computational ceiling / collaboration:** Escher's computational layer is *physico-chemically rigorous rather than ML-heavy* — mass-balance, mixture-concentration-addition, Hill-fit statistics, QSAR for baseline toxicity. She does not build deep models, and does not need to. Ceiling: excellent at making numbers comparable and defensible; weaker at high-dimensional representation learning. **This is probably the single most productive collaboration for a Chinese lab doing mixtures/non-target** because her framework converts your HRMS + bioassay data into reviewer-proof quantities, and she co-authors widely with Asian groups (see the Korean Hanyang/Hong Seongjin EDA papers and the Kwon Jung-Hwan collaboration in her 2026 output). Highly collaborative.

---

### 3. Eawag (Swiss Federal Institute of Aquatic Science and Technology), Dübendorf
**PIs:** Kathrin Fenner (Environmental Chemistry; also Univ. Zürich) — biotransformation and persistence prediction; Juliane Hollender — non-target HRMS; **Katarzyna (Kasia) Arturi** — ML-based hazard prediction from HRMS; Kristin Schirmer (+ Ksenia Groh, Marion Revel) — fish cell lines and the "fish invitrome"; Jörg Wicker (Univ. Auckland, enviPath co-lead); Jasmin Hafner, Kunyang Zhang (now with Philippe Schwaller, EPFL).
**Signature contribution:** The most genuinely *modern* machine-learning layer in environmental chemistry outside industry. Three distinct strands: (a) biotransformation pathway and half-life prediction (enviPath, probabilistic ML for soil half-lives, contrastive learning for enzyme–reaction association); (b) **MLinvitroTox** — predicting ToxCast/Tox21 endpoint activity directly from MS2-derived structural fingerprints, so an unidentified HRMS feature can be hazard-ranked without a confirmed structure; (c) mechanism-guided transfer learning with interpretable attention in GNNs.

| Paper | Year | Journal | DOI |
|---|---|---|---|
| Machine Learning-Based Hazard-Driven Prioritization of Features in Nontarget Screening of Environmental High-Resolution Mass Spectrometry Data (Arturi K, Hollender J) | 2023 | Environmental Science & Technology | 10.1021/acs.est.3c00304 |
| MLinvitroTox reloaded for high-throughput hazard-based prioritization of high-resolution mass spectrometry data (Arturi K, Harris EJ, Gasser L, Escher BI, Braun G, … Hollender J) | 2025 | Journal of Cheminformatics | 10.1186/s13321-025-00950-4 |
| Predicting Toxicity toward Nitrifiers by Attention-Enhanced Graph Neural Networks and Transfer Learning from Baseline Toxicity (Zhang K, Schwaller P, Fenner K) — ES&T 59(9):4518–4529 | 2025 | Environmental Science & Technology | 10.1021/acs.est.4c12247 |
| Predicting Micropollutant Removal in Wastewater Treatment Based on Molecular Structure: Benchmark Data and Models (Cordero Solano JA, Hafner J, McLachlan MS, Singer H, Fenner K) | 2025 | Environmental Science & Technology | 10.1021/acs.est.5c09314 |
| Confidently Uncertain: Probabilistic Machine Learning to Predict Soil Biotransformation Half-Lives (Salz M, Cordero Solano JA, Fenner K, Hafner J) | 2026 | Environmental Science & Technology | 10.1021/acs.est.6c03516 |
| Advancements in biotransformation pathway prediction: enhancements, datasets, and novel functionalities in enviPath (Hafner J, Lorsbach T, Schmidt S, Brydon L, Dost K, … Wicker J) | 2024 | Journal of Cheminformatics | 10.1186/s13321-024-00881-6 |
| Enzyme association for environmental biotransformation reactions through contrastive learning of reaction center-specific fingerprints (Zhang K, Marti TD, Probst SI, Robinson SL, Fenner K) | 2026 | Bioinformatics | 10.1093/bioinformatics/btag142 |
| Persistence Assessment of Chemicals: Trajectories toward New Approach Methodologies (P-NAMs) (Fenner K, Zahn D, Jöhncke U, Sigmund G, Mayer P, … Reemtsma T) | 2026 | Environmental Science & Technology | 10.1021/acs.est.6c00444 |
| FAIR and Effective Communication of Data on Chemical Contaminant Biotransformation in the Environment (Rich SL, Hafner J, Salz M, Qanbarzadeh M, Geng F, … Fenner K) | 2025 | Environ Sci Technol Lett | 10.1021/acs.estlett.5c00753 |
| Development of the fish invitrome for animal-free environmental risk assessment of chemicals (Revel M, Groh K, Bertoli J, Degeratu MO, Fischer M, … Schirmer K) | 2025 | Environmental Toxicology and Chemistry | 10.1093/etojnl/vgaf028 |
| A High-Content Imaging Pipeline to Investigate Subcytotoxic Effects in RTgill-W1 Cells (Tome M, Jozef B, Mosimann SL, Kosnik M, Schirmer K, Županič A) | 2026 | Environmental Science & Technology | 10.1021/acs.est.5c18316 |
| Suspect and Nontarget Screening of Organic Micropollutants in Swiss Sewage Sludge: A Nationwide Survey (Lara-Martín PA, Schinkel L, Eberhard Y, Giger W, Berg M, … Hollender J) | 2025 | Environmental Science & Technology | 10.1021/acs.est.4c13217 |
| Non-targeted Analysis of the Environment: A Special Issue in ES&T and ES&T Letters (Hollender J, Martin JW, Covaci A, Chen D, Letcher RJ, … Newton SR) | 2025 | Environmental Science & Technology | 10.1021/acs.est.5c16761 |

**Experimental pairing:** Activated-sludge and soil biotransformation incubations with LC-HRMS time-series; nationwide/pan-European sampling campaigns; RTgill-W1 / PLHC-1 / zebrafish-cell (PAC2) in vitro assays with high-content imaging; Eawag runs its own full-scale WWTP pilot infrastructure.
**Public assets:**
- **MLinvitroTox** — Python package on PyPI (`pip install mlinvitrotox`, v0.3.x); data package archived at Eawag OpenData, DOI 10.25678/0007QS. Works with SIRIUS fingerprints (≤ v5.8.6 at last check; v6 support listed as WIP).
- **enviPath** (envipath.org) — biotransformation pathway database + prediction API, with BBD and Eawag soil/sludge packages.
- **Eawag MassBank / MassBank EU** (co-maintained; see Schymanski entry).
- Benchmark micropollutant-removal dataset and models (SI of the 2025 ES&T benchmark paper).
**Computational ceiling / collaboration:** **The highest genuine computational ceiling of any wet-lab-anchored environmental group outside China.** They publish interpretable GNNs, probabilistic/uncertainty-aware models, contrastive representation learning, and proper benchmark datasets — in ES&T. Fenner's group collaborates with EPFL's Schwaller lab (one of the strongest chemistry-ML groups anywhere). For a mid-size lab this is the best *technical* partner and the hardest to out-compete on method; the right move is to supply what they lack — large, well-controlled in vivo phenotype data — rather than compete on model architecture.

---

### 4. UCSF — Michael J. Keiser & David Kokel (+ Matthew N. McCarroll)
**Institution:** University of California, San Francisco (Keiser: Depts of Pharmaceutical Chemistry / Bioengineering & Therapeutic Sciences; Kokel: UCSF — current affiliation **[unverified by direct search this session; all 2024–25 papers carry UCSF addresses]**).
**Signature contribution:** The current gold standard for *computational larval-zebrafish behavioural phenotyping*. Deep metric learning over high-dimensional behavioural profiles, with explicit prospective validation and — crucially — an explicit published account of shortcut learning: their first screen's models exploited plate artefacts, forcing a complete re-run with well-wise randomisation.

| Paper | Year | Journal | DOI |
|---|---|---|---|
| Deep phenotypic profiling of neuroactive drugs in larval zebrafish (Gendelev L, Taylor J, Myers-Turnbull D, Chen S, McCarroll MN, Arkin MR, Kokel D, Keiser MJ) — Nat Commun 15(1):9955 | 2024 | Nature Communications | 10.1038/s41467-024-54375-y |
| A Multimodal, In Vivo Approach for Assessing Structurally and Phenotypically Related Neuroactive Molecules (McCarroll MN, Sisko E, Gong JH, Teng J, Taylor J, … Sello JK) | 2024 | ACS Chemical Neuroscience | 10.1021/acschemneuro.4c00426 |
| Behavioral Profiling in Zebrafish Identifies Insecticide-Related Compounds (Watson G, Taylor J, Lambert WT, Beavers K, Kirk D, … McCarroll MN) | 2025 | J Agricultural and Food Chemistry | 10.1021/acs.jafc.4c09342 |

**Experimental pairing:** 650-compound CNS library in high replicate; prospective radioligand binding validation of predicted targets (58% hit rate reported); orthogonal druglike compound set for generalisation testing.
**Public assets:** Code and processed behavioural profiles released with the Nat Commun paper (GitHub/Zenodo per the paper's data-availability statement); the `sauronlab` analysis stack from the Keiser lab (**exact repository URL [unverified]**).
**Computational ceiling / collaboration:** Very high — deep metric learning, embedding-space analysis, calibrated negative controls, honest artefact reporting. **The 2025 JAFC paper shows they have already begun applying this to insecticides**, i.e. they are entering environmental chemical space. This is both the clearest *benchmark* for your lab and the clearest *collaboration* target: your group has the chemical/exposure relevance and the transcriptomic axis they lack; they have the representation-learning method and the experimental-design discipline. Realistic entry point: replicate their randomisation + negative-control design in your own screen, cite the shortcut-learning analysis, and approach them with environmental chemicals + a transcriptomic readout.

---

### 5. US EPA Great Lakes Toxicology & Ecology Division, Duluth — Daniel L. Villeneuve & Carlie A. LaLone
**Signature contribution:** The adverse outcome pathway (AOP) framework's operational core, plus **SeqAPASS** — sequence- (now structure-) based cross-species extrapolation, which is the field's accepted answer to "does this human/mammalian assay result transfer to fish?" Villeneuve's recent work is the reference for *ecological* transcriptomic PODs in fish and invertebrates.

| Paper | Year | Journal | DOI |
|---|---|---|---|
| Comparison of transcriptomic points of departure with apical endpoints in developing zebrafish exposed to PFOS, PFOA, or PFHxS (Shankar P, Hazemi M, Mattingly K, See MJ, Bell ME, … Villeneuve DL) | 2025 | Toxicological Sciences | 10.1093/toxsci/kfaf047 |
| An evaluation of transcriptomic points of departure and gene expression profiles for larval fathead minnows (Pimephales promelas) exposed to 22 chemicals with known modes of action (Baettig CG, Cavallin JE, Bush K, Kasparek A, Schumann P, … Villeneuve DL) | 2025 | Aquatic Toxicology | 10.1016/j.aquatox.2025.107650 |
| Comparison of whole transcriptome and targeted RNA sequencing for ecological high-throughput transcriptomics (Villeneuve DL, Nash M, Biales A, Bush K, Evensen G, … Flynn K) | 2025 | Regul Toxicol Pharmacol | 10.1016/j.yrtph.2025.105898 |
| Transcriptomic points of departure from the aquatic insect Chironomus dilutus for 22 PFAS and their use in chemical hazard screening (Flynn KM, Bush K, Cavallin J, Kasparek A, Schumann P, … Villeneuve DL) | 2026 | Environmental Toxicology and Chemistry | 10.1093/etojnl/vgag244 |
| An automated computational data pipeline to rapidly acquire, score, and rank toxicological data for ecological hazard assessment (Schaupp CM, Byrne G, Chan M, Haggard DE, Hazemi M, … Villeneuve DL) | 2024 | Integr Environ Assess Manag | 10.1002/ieam.4945 |
| Accelerating AOP Development in the AOP-Wiki with AI: A Practical Road Map for the Community (Song Y, Kumar V, Tanabe S, Villeneuve DL, Wittwehr C) | 2026 | Environmental Science & Technology | 10.1021/acs.est.6c05148 |
| Cross-Species Molecular Docking Method to Support Predictions of Species Susceptibility to Chemical Effects (Schumann PG, Chang D, Mayasich S, Vliet S, Brown T, … LaLone CA) | 2024 | Computational Toxicology | 10.1016/j.comtox.2024.100319 |
| Using molecular dynamics simulation to enhance conservation analysis for cross species extrapolation of the PFOA-transthyretin interaction (Buglewicz DJ, Staub R, Chang DT, Evoli S, Schumann PG, … LaLone CA) | 2025 | Environmental Toxicology and Chemistry | 10.1093/etojnl/vgaf160 |
| Zebrafish cell lines and high-throughput transcriptomics: advancing in vitro and bioinformatics methods for supporting environmental risk assessment (Schumann PG, Bundy J, Haggard DE, Everett L, Harrill JA, … LaLone CA) | 2025 | Toxicological Sciences | 10.1093/toxsci/kfaf127 |
| Best Practices for the Development and Application of Bioinformatics Approaches for Species Extrapolation in Chemical Safety Assessment (LaLone CA, Schumann P, Rivetti C, Ewald J, Edwards S, … Basu N) | 2026 | Integr Environ Assess Manag | 10.1093/inteam/vjag058 |

**Experimental pairing:** Fathead minnow and zebrafish in vivo exposures with matched apical endpoints; Chironomus dilutus; caged-fish field studies (with Escher/Jahnke); their own RNA-seq and TempO-Seq capacity.
**Public assets:** **SeqAPASS** (seqapass.epa.gov; original tool paper LaLone et al., Toxicol Sci 2016, 10.1093/toxsci/kfw119; sequence-to-structure extension ETC 2023, 10.1002/etc.5537); AOP-Wiki (OECD/EU-JRC co-hosted); ECOTOX Knowledgebase; the automated ecological hazard data pipeline (IEAM 2024).
**Computational ceiling / collaboration:** Moderate-to-good and clearly rising — they have moved from pure sequence alignment to molecular docking and MD simulation for cross-species inference, and from whole-transcriptome to targeted-panel tPOD statistics. Ceiling: they are not building new ML architectures; their edge is biological framing and standardisation. **For your lab, SeqAPASS is the obvious free tool to make any "does this mammalian target matter in zebrafish?" claim defensible**, and the Villeneuve tPOD papers are the correct benchmark for the transcriptomics half of your work.

---

### 6. NIEHS / NICEATM / DTT (Research Triangle Park) — Nicole C. Kleinstreuer
**PIs:** Nicole C. Kleinstreuer (Director, NICEATM — confirmed by ALTEX leadership announcement), Kamel Mansouri (OPERA), Helena T. Hogberg, Agnes Karmaus, Xiaoqing Chang, Kristen Ryan, David M. Reif (ToxPi). Warren Casey has moved out of the NICEATM directorship (most recent sourcing puts him at NIH ORIVA / ICCVAM Executive Director — **[partly unverified]**).
**Signature contribution:** Validation science. They are the people who decide whether an in silico or in vitro method is *fit for regulatory purpose*: defined approaches (DAs), performance benchmarking against reference data, and curated reference datasets. Plus OPERA — the open, applicability-domain-aware physchem/ADME/ecotox QSAR suite that most environmental papers use for predicted properties.

| Paper | Year | Journal | DOI |
|---|---|---|---|
| Evaluation of in silico model predictions for mammalian acute oral toxicity and regulatory application in pesticide hazard and risk assessment (Bishop PL, Mansouri K, Eckel WP, Lowit MB, Allen D, … Kleinstreuer NC) | 2024 | Regul Toxicol Pharmacol | 10.1016/j.yrtph.2024.105614 |
| The skin allergy risk assessment-integrated chemical environment (SARA-ICE) defined approach to derive points of departure for skin sensitization (Reinke EN, Reynolds J, Gilmour N, Reynolds G, Strickland J, … Kleinstreuer NC) | 2024 | Current Research in Toxicology | 10.1016/j.crtox.2024.100205 |
| Integrated Approach for Testing and Assessment for Developmental Neurotoxicity (DNT) to Prioritize Aromatic Organophosphorus Flame Retardants (Kreutz A, Oyetade OB, Chang X, Hsieh JH, Behl M, … Hogberg HT) | 2024 | Toxics | 10.3390/toxics12060437 |
| Defined approaches to predict GHS and EPA classifications for ocular irritation potential of agrochemical formulations (Daniel AB, van der Zalm AJ, Raabe HA, Clippinger AJ, Choksi NY, … Kleinstreuer NC) | 2025 | Cutaneous and Ocular Toxicology | 10.1080/15569527.2025.2499552 |
| Perspectives on variability of in vivo toxicology studies: considerations for next-generation toxicology (Karmaus AL, Kreutz AL, Oyetade O, Friedman KP, Paparella M, … Kleinstreuer NC) | 2026 | Frontiers in Toxicology | 10.3389/ftox.2026.1778353 |
| Application of in vitro to in vivo extrapolation (IVIVE) to inform chemical health guidance value derivation (Chang X, Allen DG, Kleinstreuer NC, Mumtaz MM) | 2026 | Toxicological Sciences | 10.1093/toxsci/kfag017 |
| Enhancing toxicological interpretation and reporting of in vitro high-throughput screening data (Hill BN, Karmaus AL, Hull V, Unnikrishnan A, Kleinstreuer NC, … Hogberg HT) | 2026 | Frontiers in Toxicology | 10.3389/ftox.2026.1886801 |
| Extending the high-throughput toxicokinetics R package to include brain and adipose compartments (Unnikrishnan A, Kreutz A, Chang X, Sluka JP, Li D, Linakis MW, Wambaugh JF, Kleinstreuer N) | 2026 | Frontiers in Pharmacology | 10.3389/fphar.2026.1895108 |

**Experimental pairing:** They mostly do not generate primary data; they commission and curate (Tox21 10K via NCATS, DNT in vitro battery, zebrafish multi-lab studies). Their "validation" is the experiment.
**Public assets:** **OPERA** (open-source QSAR suite — logP, water solubility, BCF, fish LC50, pKa, AOP-relevant endpoints, with applicability-domain and confidence metrics; GitHub + CompTox Dashboard integration); **Integrated Chemical Environment (ICE)** (ice.ntp.niehs.nih.gov — curated reference data, IVIVE workflows, DA implementations); Tox21 10K screening data; **ToxPi** software + ToxPi*GIS toolkit (Reif group; JESEE 2022, 10.1038/s41370-022-00433-w; weight optimisation, Comput Toxicol 2023, 10.1016/j.comtox.2023.100294).
**Computational ceiling / collaboration:** Ceiling is intentionally low-variance — consensus QSAR, DA decision trees, IVIVE. The value is not novelty, it is **the ability to say "validated"**. If your target is ES&T rather than a regulatory journal, use ICE/OPERA as inputs and benchmarks; a formal collaboration is slow (US federal process) but their tools are unrestricted.

---

## TIER 2 — Strong, methodologically distinctive, realistic partners

### 7. Broad Institute / Uppsala / Cambridge — Cell Painting & image-based profiling for toxicology
**PIs:** Anne E. Carpenter & Shantanu Singh (Broad Institute Imaging Platform); Ola Spjuth (Uppsala); Andreas Bender (Univ. Cambridge, Yusuf Hamied Dept of Chemistry; co-author on the OASIS consortium and on Seal's models); Srijit Seal; **Jessica D. Ewald** (ex-McGill ecotoxicogenomics, now first-authoring Broad Cell Painting work — a direct bridge between ecotox and the Broad stack).
**Signature contribution:** High-content morphological profiling (Cell Painting) as a general-purpose, chemical-agnostic bioactivity readout, plus the most honest benchmarking culture in the profiling field.

| Paper | Year | Journal | DOI |
|---|---|---|---|
| Counting cells can accurately predict small-molecule bioactivity benchmarks (Seal S, Dee W, Shah A, Cerisier N, Zhang A, … Carpenter AE) | 2026 | Nature Communications | 10.1038/s41467-026-68725-5 |
| Cell Painting for cytotoxicity and mode-of-action analysis in primary human hepatocytes (Ewald JD, Titterton KL, Bäuerle A, Beatson A, Boiko DA, … Singh S) | 2026 | Cell Systems | 10.1016/j.cels.2026.101566 |
| Morphological map of under- and overexpression of genes in human cells (Chandrasekaran SN, Alix E, Arevalo J, Borowa A, Byrne PJ, … Carpenter AE) | 2025 | Nature Methods | 10.1038/s41592-025-02753-9 |
| High-content morphological profiling by Cell Painting in 3D spheroids (Ringers C, Holmberg D, Larsson A, Jung B, Jarvius M, … Spjuth O) | 2026 | Nature Communications | 10.1038/s41467-026-78596-5 |
| The OASIS Consortium: integrating multi-omics technologies to transform chemical safety assessment (Rouquié D, Bender A, Cheah J, Crute CE, Dalmas D, … Carpenter AE) | 2025 | Toxicological Sciences | 10.1093/toxsci/kfaf128 |
| PKSmart: an open-source computational model to predict intravenous pharmacokinetics of small molecules (Seal S, Trapotsi MA, Mahale M, Subramanian V, Greene N, … Bender A) | 2025 | Journal of Cheminformatics | 10.1186/s13321-025-01066-5 |
| Progress and new challenges in image-based profiling (Serrano E, Peters J, Wagner J, Graham RE, Chen Z, … Way GP) | 2026 | Molecular Systems Biology | 10.1038/s44320-026-00197-7 |

**Experimental pairing:** Industrial-scale imaging (JUMP-Cell Painting: >100k perturbations), primary human hepatocytes, 3D spheroids, CRISPR/ORF genetic perturbation maps.
**Public assets:** **JUMP-Cell Painting datasets** (cellpainting-gallery on AWS Open Data, ~hundreds of TB of images + profiles); **CellProfiler** and **pycytominer**; the Cell Painting Gallery; PKSmart (open source). This is the largest free phenotypic-profiling resource in existence.
**Computational ceiling / collaboration:** Very high, and **the "Counting cells…" Nat Commun 2026 paper is the single most useful paper for your reviewers' sake**: it demonstrates that a trivial baseline (cell count) matches sophisticated models on standard bioactivity benchmarks — i.e. it is the canonical "your benchmark is too easy" citation. Any prediction paper you write should pre-empt it by including a trivial baseline. Collaboration: Carpenter/Singh are extremely open (their data is public by default) but are not environmental toxicologists; Bender is the natural bridge, and Ewald is the natural bridge on the ecotox side.

### 8. University of Birmingham — Mark R. Viant & John K. Colbourne (PrecisionTox)
**Signature contribution:** Omics-based chemical grouping and read-across with regulatory intent; metabolomics benchmark-dose/POD methodology; and **"phylotoxicology"** — the hypothesis that toxicity mechanisms are evolutionarily conserved, tested across Drosophila, Daphnia, C. elegans, zebrafish and Xenopus embryos in the EU PrecisionTox consortium (Colbourne coordinates; Birmingham leads).

| Paper | Year | Journal | DOI |
|---|---|---|---|
| The PrecisionTox chemical library: creation of a chemical collection to discover evolutionary conserved biomolecular signatures of toxicity (Martínez R, González-Sánchez JC, Sampani SI, Scholz S, Escher BI, Henneberger L, Huchthausen J, Whelan M, Dickmeis T, Weiss C, Colbourne JK, Freedman JH) — Toxicol Sci 208(2):317–329 | 2025 | Toxicological Sciences | 10.1093/toxsci/kfaf126 |
| Alternative Vertebrate and Invertebrate Model Organisms Show Similar Sensitivity as Rodents to a Diverse Set of Chemicals (Hayot G, Lloyd GR, Diwan GD, Keith N, Smoot SR, … Dickmeis T) | 2025 | Environmental Science & Technology | 10.1021/acs.est.5c10177 |
| Utilizing Omics Data for Chemical Grouping (Viant MR, Barnett RE, Campos B, Colbourne JK, Barnard M, … Hodges G) | 2024 | Environmental Toxicology and Chemistry | 10.1002/etc.5959 |
| Multi-omics bioactivity profile-based chemical grouping and read-across: a case study with Daphnia magna and azo dyes (Gruszczynska H, Barnett RE, Lloyd GR, Weber RJM, Lawson TN, … Viant MR) | 2024 | Archives of Toxicology | 10.1007/s00204-024-03759-6 |
| Substantiating chemical groups for read-across using molecular response profiles (Barnett RE, Lawson TN, Rivetti C, Barata C, Cronin MTD, … Viant MR) | 2025 | Regul Toxicol Pharmacol | 10.1016/j.yrtph.2025.105894 |
| Experimental and computational approaches for deep metabolome annotation with application to the ecotoxicological model organism Daphnia magna (Lawson TN, Jones MR, Chetwynd AJ, Sostare E, Weidt S, … Viant MR) | 2026 | GigaScience | 10.1093/gigascience/giag055 |
| Demonstrating the reliability of in vivo metabolomics-based chemical grouping: Part 2 — Consistency of group-specific metabolic effects (Lloyd GR, Sands C, Kende A, Haake V, Amstalden E, … Viant MR) | 2026 | Archives of Toxicology | 10.1007/s00204-026-04570-1 |

**Experimental pairing:** LC-MS/DI-MS metabolomics at scale with proper QC; five-species embryo/larval exposures; Daphnia and zebrafish in-house.
**Public assets:** The **PrecisionTox 200-chemical library** definition and property/baseline-toxicity annotations (SI of Toxicol Sci 2025); Daphnia magna deep metabolome annotation resource (GigaScience 2026); `struct`/`pmp` R packages for metabolomics QC and statistics (Lloyd/Weber, Birmingham — **package names [verified by author overlap; repository URLs unverified]**); PrecisionTox data releases via precisiontox.org.
**Computational ceiling / collaboration:** Good but not cutting-edge ML: their strength is *statistical rigour in omics* (reproducibility across labs, group-level consistency testing, BMD modelling), not representation learning. The phylotoxicology dataset is however exactly the kind of multi-species resource your zebrafish+transcriptomics lab could extend. PrecisionTox is an EU-funded consortium running to 2026, so a formal join is unlikely now; data reuse and bilateral collaboration with Viant or Colbourne is realistic.

### 9. University of Luxembourg (LCSB) — Emma L. Schymanski
**Signature contribution:** The open cheminformatics backbone of non-target analysis — identification-confidence reporting, FAIR chemical data, open spectral libraries, and cheminformatics-driven prioritisation of transformation products. She is why your HRMS annotations have to carry a confidence level.

| Paper | Year | Journal | DOI |
|---|---|---|---|
| MassBank: an open and FAIR mass spectral data resource (Neumann S, Meier R, Wenk M, Elapavalore A, Nishioka T, … Schymanski EL) | 2026 | Nucleic Acids Research | 10.1093/nar/gkaf1193 |
| Identification of persistent substructures in transformation products with zebrafish embryos using cheminformatics and a suspect screening approach (Chirsir P, Cordero-Maldonado ML, Carlier MP, Hamers T, Schymanski EL) | 2026 | Environ Sci Process Impacts | 10.1039/d5em00825e |
| Reporting Chemical Data in the Environmental Sciences (Baskaran S, Chirsir P, Joudan S, Wolf R, Bolton EE, … Schymanski EL) | 2025 | ACS Environmental Au | 10.1021/acsenvironau.5c00034 |
| Frontiers Shaping the Next Generation of Transformation Product Prediction and Toxicological Assessment (Löffler P, Schymanski EL, Henschel H, Lai FY) | 2025 | Environmental Science & Technology | 10.1021/acs.est.5c06790 |
| Shinyscreen: mass spectrometry data inspection and quality checking utility (Kondić T, Elapavalore A, Krier J, Lai A, Taha HM, … Schymanski EL) | 2025 | Journal of Cheminformatics | 10.1186/s13321-025-01044-x |
| pyMSscreen: an interactive interface for automated quality control and prescreening in mass spectrometry workflows (Elapavalore A, Chirsir P, Palm EH, Jakubec M, Schymanski EL) | 2026 | Journal of Cheminformatics | 10.1186/s13321-026-01260-z |
| Embrace Open, Collaborative, Discovery-Based Exposomics (Schymanski EL, Raptopoulou F, Gkanali V, Vermeulen R) | 2026 | Environmental Science & Technology | 10.1021/acs.est.6c02651 |
| Comprehensive Mass Spectrometry Workflows to Systematically Elucidate Transformation Processes of Organic Micropollutants (Helmus R, Bagdonaite I, de Voogt P, van Bommel MR, Schymanski EL, … Ter Laak TL) | 2025 | Environmental Science & Technology | 10.1021/acs.est.4c09121 |

**Experimental pairing:** Collaborative — she pairs with wet labs (note the 2026 zebrafish-embryo transformation-product paper is with Timo Hamers at VU Amsterdam).
**Public assets:** **MassBank / MassBank-EU** (massbank.eu, open spectra, FAIR, DOI-citable); **PubChemLite for Exposomics** (Zenodo-versioned, exposomics-tailored PubChem subset); `patRoon` ecosystem interoperability (Helmus, Amsterdam); Shinyscreen and pyMSscreen; the Environmental Cheminformatics group's GitLab.
**Computational ceiling / collaboration:** High in cheminformatics/data engineering, deliberately modest in predictive ML (she builds the substrate others model on). **Extremely collaborative and explicitly pro-open-science** — a very low-friction partner, and essentially mandatory to cite if you publish non-target work in ES&T.

### 10. VU Amsterdam / Utrecht — Timo Hamers, Marja Lamoree, Juliette Legler, Remco H.S. Westerink
**Signature contribution:** Effect-directed analysis (EDA) with mechanistically specific endpoints — above all transthyretin (TTR) competitive binding for thyroid-hormone-displacing activity (Hamers) — and in vitro neurotoxicity by microelectrode array with proper exposure-duration design (Westerink, Utrecht).

| Paper | Year | Journal | DOI |
|---|---|---|---|
| Effect-Directed Analysis Based on Transthyretin Binding Activity of Per- and Polyfluoroalkyl Substances in a Contaminated Sediment Extract (Langberg HA, Choyke S, Hale SE, Koekkoek J, Cenijn PH, … Hamers T) | 2023 | Environmental Toxicology and Chemistry | 10.1002/etc.5777 |
| The contribution of PFAS to thyroid hormone-displacing activity in Dutch waters: A comparison between two in vitro bioassays with chemical analysis (de Schepper JKH, van Oorschot Y, Jaspers RJ, Hamers T, Lamoree MH, … Houtman CJ) | 2023 | Environment International | 10.1016/j.envint.2023.108256 |
| Characterization of thyroid hormone transport in a human choroid plexus papilloma cell line (HIBCPP) as an in vitro blood-cerebrospinal fluid barrier model (Wagenaars F, Cenijn P, van Boxel J, Koekkoek J, Schroten H, … Hamers T) | 2024 | Molecular and Cellular Endocrinology | 10.1016/j.mce.2024.112449 |
| Competitive binding of newly synthesized hydroxylated and carbonylated metabolites of chlorinated paraffins to transthyretin (Ji Y, van Mourik LM, Hamers T, Cenijn P, Gorovoy A, … Leonards PEG) | 2026 | Environmental Research | 10.1016/j.envres.2026.125623 |
| Exposure to organophosphate flame retardants and phthalates alters neuronal activity and network development (van Melis LVJ, Zimnik KN, Persad AR, Bak T, van Rossum MJH, … Westerink RHS) | 2025 | Toxicology | 10.1016/j.tox.2025.154168 |
| Acute, prolonged, and chronic exposure to organochlorine insecticides evoke differential effects on in vitro neuronal activity and network development (van Melis LVJ, Bak T, Peerdeman AM, van Kleef RGDM, Wopken JP, … Westerink RHS) | 2025 | NeuroToxicology | 10.1016/j.neuro.2025.103308 |
| Exposure matters: The impact of exposure characteristics on in vitro neurotoxicity of pesticides and implications for regulatory testing (Meerman JJ, Sinnige TL, Klerx W, Tuominen A, Legler J, … Westerink RHS) | 2026 | Toxicology | 10.1016/j.tox.2026.154526 |
| Evaluating bioassays to study the occurrence and fate of antibiotics in the water cycle (de Schepper JKH, de Boer T, Cenijn P, Hamers T, Nguyen MT, … Houtman CJ) | 2026 | Environmental Toxicology and Chemistry | 10.1093/etojnl/vgag207 |

**Experimental pairing:** TTR-binding and other receptor/transport assays; rat cortical and hiPSC MEA networks; EDA fractionation coupled to LC-HRMS.
**Public assets:** Assay protocols published in detail; no large public model or dataset release. (**No model weights or pipelines located — treat as a method/assay partner, not a data source.**)
**Computational ceiling / collaboration:** **Low computational ceiling — this is a wet-lab/assay group.** Their value to you is a mechanistically defensible, non-nuclear-receptor endpoint (thyroid-hormone displacement) and MEA expertise. Highly collaborative, European-funding-driven, and used to hosting visitors. Hamers has already co-published with Schymanski (zebrafish + cheminformatics) — a natural triangle for your lab.

### 11. Oregon State University — Robyn L. Tanguay (+ Lisa Truong, Manuel Garcia-Jaramillo) with Sciome LLC
**Signature contribution:** The largest-throughput zebrafish developmental toxicity and behaviour screening platform in environmental toxicology, now paired with deep-learning image analysis and foundation models.

| Paper | Year | Journal | DOI |
|---|---|---|---|
| A self-supervised foundation model for large-scale zebrafish image analysis (Oktay AB, Tandon A, Howard BE, Green AJ, Truong L, … Shah RR) | 2026 | SLAS Technology | 10.1016/j.slast.2026.100471 |
| FINS: An interactive platform for automated zebrafish image analysis and morphological screening (Oktay AB, McAfee E, Green AJ, Howard BE, Truong L, … Tandon A) | 2026 | SLAS Technology | 10.1016/j.slast.2026.100426 |
| Zebrafish behavioral assessment as a first-tier whole-organism NAM for developmental neurotoxicity: A multi-laboratory evaluation (Truong L, Hsieh JH, Ellis L, Jaka O, Muriana A, … Ryan K) | 2026 | NeuroToxicology | 10.1016/j.neuro.2026.103504 |
| Addressing community concerns about unregulated organic contaminants in surface water: Integrating suspect and non-targeted chemical analyses with zebrafish toxicity testing and computational hazard comparisons (Fender CL, Morshead M, Schindler J, Williamson M, Brown K, … Garcia-Jaramillo M) | 2026 | Environmental Pollution | 10.1016/j.envpol.2026.128103 |
| A mixture parameterized biologically based dosimetry model to predict body burdens of polycyclic aromatic hydrocarbons in developmental zebrafish toxicity assays (Rude CI, Smith JN, Scott RP, Schultz KJ, Anderson KA, … Tanguay RL) | 2025 | Toxicological Sciences | 10.1093/toxsci/kfaf039 |
| Enhanced high-throughput embryonic photomotor response assays in zebrafish using a multi-camera array microscope (Jamison J, Doman TJJ, Antenucci Z, Efromson J, Johnson C, … Tanguay RL) | 2025 | SLAS Technology | 10.1016/j.slast.2025.100310 |
| ToxPoint: The indispensable role of zebrafish as a new approach methodology (NAM) in toxicology (Tanguay RL) | 2025 | Toxicological Sciences | 10.1093/toxsci/kfaf121 |

**Experimental pairing:** Tens of thousands of embryos; 22-endpoint morphology + photomotor/embryonic behaviour; internal-dose measurement and dosimetry modelling; passive samplers and non-target chemistry in the same workflow.
**Public assets:** **FINS** zebrafish image-analysis platform and the self-supervised zebrafish foundation model (released via Sciome; **repository/weights location [unverified]**); OSU's zebrafish screening datasets (largely published in SI rather than as a single portal).
**Computational ceiling / collaboration:** Historically modest (ANOVA/LOEL per endpoint), but the 2026 Sciome collaboration marks a real step up — a self-supervised image foundation model is a genuinely current method. **The 2026 Environmental Pollution paper is almost exactly your lab's intended design** (non-target HRMS + zebrafish + computational hazard comparison), so read it as both a template and a competitor. Tanguay collaborates very widely and the multi-lab DNT evaluation shows the group is set up for inter-laboratory work — a strong candidate for a ring trial with your behavioural platform.

### 12. McGill / Univ. of Saskatchewan / Environment and Climate Change Canada — Niladri Basu, Jianguo Xia, Jessica Head, Markus Hecker, Doug Crump, Jason O'Brien
**Signature contribution:** **EcoToxChip** — a cross-species targeted qPCR/RNA-seq toxicogenomics platform for ecologically relevant species — plus the **Analyst software suite** (ExpressAnalyst, MetaboAnalyst), which is the de facto free web infrastructure for omics analysis in non-model organisms.

| Paper | Year | Journal | DOI |
|---|---|---|---|
| ExpressAnalyst: A unified platform for RNA-sequencing analysis in non-model species (Liu P, Ewald J, Pang Z, Legrand E, Jeon YS, … Xia J) | 2023 | Nature Communications | 10.1038/s41467-023-38785-y |
| Web-based multi-omics integration using the Analyst software suite (Ewald JD, Zhou G, Lu Y, Kolic J, Ellis C, … Xia J) | 2024 | Nature Protocols | 10.1038/s41596-023-00950-4 |
| Using MetaboAnalyst 6.0 for exposomics data analysis — from LC-MS2 spectra processing to dose-response modeling and causal inference (Pang Z, Lu Y, Zhou G, Ou H, Viau C, … Xia J) | 2026 | Nature Protocols | 10.1038/s41596-026-01415-0 |
| Comparing transcriptomic responses to chemicals across six species using the EcoToxChip RNASeq database (Mittal K, Ewald J, Crump D, Head J, Hecker M, … Basu N) | 2025 | Environmental Toxicology and Chemistry | 10.1002/etc.5803 |
| TPD-seq: A high throughput RNA-seq method to derive transcriptomic points of departure from cell lines (Mittal K, Xu K, Rulli SJ, Zhou G, Xia J, … Basu N) | 2024 | Toxicology in Vitro | 10.1016/j.tiv.2024.106001 |
| The DIKW of transcriptomics in ecotoxicology: extracting information, knowledge, and wisdom from big data (Head JA, Ewald JD, Basu N) | 2025 | Environmental Toxicology and Chemistry | 10.1002/etc.5954 |
| EcoToxChip reveals immune and metabolic pathway disruption in fish chronically exposed to stormwater-impacted environments (Taridashti F, Marjan P, Hecker M, Munkittrick KR) | 2026 | Aquatic Toxicology | 10.1016/j.aquatox.2026.107748 |
| Effects of legacy and emerging antimicrobial compounds to early-life stages of rainbow trout (Amekor M, Kohlman E, Roberts C, Alcaraz AJ, Jain N, … Hogan N) | 2025 | Aquatic Toxicology | 10.1016/j.aquatox.2025.107487 |

**Experimental pairing:** Multi-species in vivo and cell-line exposures (fathead minnow, rainbow trout, Japanese quail, frog, zebrafish); field-caught fish; their own qPCR array manufacturing (with Qiagen).
**Public assets:** **ExpressAnalyst** (expressanalyst.ca — RNA-seq for non-model species including zebrafish, with built-in BMD/tPOD modules); **MetaboAnalyst 6.0** (metaboanalyst.ca); **EcoToxChip** platform and the EcoToxChip RNA-Seq cross-species database (ecotoxchip.ca; data described in ETC 2025); `FastBMD`.
**Computational ceiling / collaboration:** Xia's group has real software-engineering capacity and is one of the most widely used free tool providers in the field; the ecotox side (Basu/Head/Hecker/Crump) is strong biologically with a moderate computational ceiling. **For your lab, ExpressAnalyst + FastBMD are the lowest-friction way to produce defensible transcriptomic PODs in zebrafish without building a pipeline.** All three Canadian groups are collaborative and have histories of hosting international students.

### 13. ARC / NIVA Norway — Knut Erik Tollefsen & You Song (quantitative AOP)
**Signature contribution:** Quantitative AOP (qAOP) modelling — turning AOPs into dose–response-linked predictive models for ecological endpoints, and AI-assisted AOP construction.

| Paper | Year | Journal | DOI |
|---|---|---|---|
| Accelerating AOP Development in the AOP-Wiki with AI: A Practical Road Map for the Community (Song Y, Kumar V, Tanabe S, Villeneuve DL, Wittwehr C) | 2026 | Environmental Science & Technology | 10.1021/acs.est.6c05148 |
| Advancing component-based mixture risk assessment using new approach methodologies: An environmental case study (Noventa S, Moe SJ, Tollefsen KE, Song Y, Manfra L, … Lillicrap A) | 2026 | Ecotoxicology and Environmental Safety | 10.1016/j.ecoenv.2026.120876 |
| Computational characterisation of ecological hazard and risk of environmental mixtures (Noventa S, Moe SJ, Tollefsen KE, Zobl W, … Lillicrap A) | 2025 | EFSA Journal | 10.2903/j.efsa.2025.e231111 |
| Inhibitory binding to plastoquinone B site on D1 protein of photosystem II leading to decreased population growth rate via disruption of cellular energy metabolism (Xie L, Tollefsen KE) | 2026 | Frontiers in Plant Science | 10.3389/fpls.2026.1910560 |

**Experimental pairing:** Algal and daphnid population experiments; radioecology; zebrafish and salmon exposures.
**Public assets:** AOP-Wiki contributions; Bayesian network qAOP models published with case studies (**model files [unverified]**).
**Computational ceiling / collaboration:** Moderate — Bayesian networks and ODE-based dose–response-to-population models rather than ML. But **qAOP is an under-occupied niche where a mid-size lab with good in vivo data can publish above the ES&T norm fairly quickly**, because the bottleneck is quantitative key-event-relationship data, which is exactly what high-information zebrafish phenotyping produces.

### 14. JKU Linz / ELLIS — Günter Klambauer (with Sepp Hochreiter)
**Signature contribution:** The machine-learning methodology that toxicity prediction should be held to. The original DeepTox/Tox21-challenge lineage, and now **a reproducible leaderboard for the Tox21 challenge** — i.e. they built the benchmark that exposes inflated performance claims. Also few-shot/low-data bioactivity prediction (MHNfs), which matters because environmental endpoints are always data-poor.

| Paper | Year | Journal | DOI |
|---|---|---|---|
| Measuring AI Progress in Drug Discovery: A Reproducible Leaderboard for the Tox21 Challenge (Ebner A, Bartmann C, Topf S, Klambauer G, Schimunek J, … Luukkonen S) | 2026 | Journal of Chemical Information and Modeling | 10.1021/acs.jcim.6c01148 |
| MHNfs: Prompting In-Context Bioactivity Predictions for Low-Data Drug Discovery (Schimunek J, Luukkonen S, Klambauer G) | 2025 | Journal of Chemical Information and Modeling | 10.1021/acs.jcim.4c02373 |
| VN-EGNN: E(3)- and SE(3)-Equivariant Graph Neural Networks with Virtual Nodes Enhance Protein Binding Site Identification (Sestak F, Schneckenreiter L, Brandstetter J, Hochreiter S, Mayr A, … Klambauer G) | 2025 | Journal of Cheminformatics | 10.1186/s13321-025-01127-9 |
| HyperPCM: Robust Task-Conditioned Modeling of Drug-Target Interactions (Svensson E, Hoedt PJ, Hochreiter S, Klambauer G) | 2024 | Journal of Chemical Information and Modeling | 10.1021/acs.jcim.3c01417 |

**Experimental pairing:** None — pure ML group.
**Public assets:** The Tox21 reproducible leaderboard (code + splits); MHNfs implementation; `clamp`/MHNfs model weights on GitHub (**exact URLs [unverified]**).
**Computational ceiling / collaboration:** The highest ML ceiling on this list. **If you want your prediction paper to survive a methods-oriented reviewer, adopt their evaluation discipline** (scaffold/time splits, published leaderboard baselines, no test-set leakage). They have no toxicological data of their own and are receptive to collaborations that bring real data; the asymmetry works in your favour.

### 15. Johns Hopkins — Carsten Prasse (reactivity-directed analysis) | and, separately, Thomas Hartung (CAAT)
**Prasse (Dept of Environmental Health & Engineering):** chemically motivated prioritisation — capture the *reactive electrophiles* in a sample rather than everything, then rank by hazard. This is a genuinely different and under-used idea that pairs well with non-target HRMS.

| Paper | Year | Journal | DOI |
|---|---|---|---|
| Combining Nontargeted Analysis with Computer-Based Hazard Comparison Approaches to Support Prioritization of Unregulated Organic Contaminants in Biosolids (Newmeyer MN, Lyu Q, Sobus JR, Williams AJ, Nachman KE, … Prasse C) | 2024 | Environmental Science & Technology | 10.1021/acs.est.4c02934 |
| Solid-Phase Reactivity-Directed Extraction (SPREx): An Alternative Approach for Simultaneous Extraction, Identification, and Prioritization of Toxic Electrophiles Produced in Water Treatment Applications (Grace DN, Newmeyer MN, Prasse C) | 2024 | ACS Environmental Au | 10.1021/acsenvironau.4c00025 |
| Nontargeted Identification and Prioritization of Organic Contaminants in Biosolid-Amended Soils across the United States (Hamdan N, Qian J, Prasek S, Pepper I, Prasse C) | 2026 | Environmental Science & Technology | 10.1021/acs.est.6c13101 |

**Hartung (Center for Alternatives to Animal Testing):** agenda-setting rather than method-building. His 2025–26 output is overwhelmingly perspectives, editorials and roadmaps in Frontiers journals and ALTEX (e.g. "AI snake oil? A risk/benefit analysis for toxicology", Front Artif Intell 2026, 10.3389/frai.2026.1779276; "Mechanistic read-across comes of age: a comparative appraisal of EFSA 2025 guidance, ECHA's RAAF, and good read-across practice", Front Toxicol 2025, 10.3389/ftox.2025.1690491; "Navigating the AI Frontier in Toxicology: Trends, Trust, and Transformation", Curr Environ Health Rep 2025, 10.1007/s40572-025-00514-6). **Blunt assessment: coasting on volume.** The read-across appraisal is genuinely useful as a framing citation; most of the rest is positioning. Cite him for framing, do not benchmark against him. Historical note: his probabilistic read-across and brain-organoid work was substantive; the current cadence is not.

### 16. Griffith University, Australia — Frederic D.L. Leusch & Peta A. Neale
**Signature contribution:** With Escher, the co-authors of the effect-based-trigger-value framework; the people who translate bioassay batteries into actionable water-quality decisions, and who document how little of the observed effect is explained by quantified chemicals.

| Paper | Year | Journal | DOI |
|---|---|---|---|
| Effect-Based Trigger Values Are Essential for the Uptake of Effect-Based Methods in Water Safety Planning (Neale PA, Escher BI, de Baat ML, Enault J, Leusch FDL) | 2023 | Environmental Toxicology and Chemistry | 10.1002/etc.5544 |
| A bioanalytical and chemical approach for wastewater discharge: Beyond detected chemicals for water quality assessment (Lewis P, Neale PA, Tan H, Leeder J, O'Malley E, … Saaristo M) | 2025 | Environmental Pollution | 10.1016/j.envpol.2025.126807 |
| Whole effluent toxicity testing using in vitro effect-based methods: Comparison with conventional methods (Johnson M, Akrami K, Crosbie ND, Goonan P, Griffith M, … Finlayson K) | 2025 | Science of the Total Environment | 10.1016/j.scitotenv.2025.179877 |
| Occurrence of chemical contaminants in environmental matrices using non-targeted analysis and effect-based method: A systematic quantitative literature review (Radke MJ, Cresswell SL, Leusch FDL) | 2025 | Science of the Total Environment | 10.1016/j.scitotenv.2025.180763 |
| First assessment of wastewater effluent and contaminated surface waters using the invertebrate cell line (C6/36) (Johnson MJ, van de Merwe JP, Leusch FDL, Finlayson KA) | 2026 | Aquatic Toxicology | 10.1016/j.aquatox.2026.107969 |
| Aryl hydrocarbon receptor activity in water: Looking beyond dioxin-like toxicity (Neale PA, Leusch FDL, Escher BI) | 2026 | Environmental Toxicology and Chemistry | 10.1093/etojnl/vgag187 |

**Experimental pairing:** Large bioassay batteries on real effluents and surface waters; sea-turtle and invertebrate cell lines.
**Public assets:** Published EBT value compilations (SI); the NTA-EDA systematic review database (STOTEN 2025) is a ready-made map of what has and has not been done.
**Computational ceiling / collaboration:** Low computational ceiling (iceberg/mixture arithmetic only), but the **systematic review is a gift for positioning a new paper** — it names the under-studied matrices (groundwater, drinking water, reclaimed water, dust, air, snow) and the recognised failure to identify polar transformation products.

### 17. Stockholm University / ETH Zürich — Jonathan W. Martin, Ian T. Cousins, Michael S. McLachlan, Martin Scheringer
**Signature contribution:** Exposure-side framing and the PFAS/persistence agenda. Martin runs Sweden's national exposomics facility and co-edited the ES&T non-target special issue; Cousins and Scheringer define the persistence-and-planetary-boundary argument that now shapes regulatory framing; McLachlan supplies the measured WWTP removal data behind Fenner's prediction benchmark.

| Paper | Year | Journal | DOI |
|---|---|---|---|
| Is Persistence a Hazard? (Scheringer M, Cousins IT) — ES&T 60(13):9718–9720 | 2026 | Environmental Science & Technology | 10.1021/acs.est.6c00770 |
| Fluoropolymers across Their Life Cycle: Why "Emissions Reduction" Is Not "Safe" (Figuière R, Cousins IT, Lohmann R, Miller AJ, Rensmo A, Scheringer M, Trier X, Wang Z, Sigmund G) — ES&T 60(42):29717–29720 | 2026 | Environmental Science & Technology | 10.1021/acs.est.6c12936 |
| Global Disparities in the Regulation of PFASs: The Risk of Shifting the PFAS Pollution Burden to Developing Countries (Sharma BM, Cousins IT, Arp HPH, Scheringer M) — ES&T 60(11):8266–8278 | 2026 | Environmental Science & Technology | 10.1021/acs.est.5c14777 |
| Planetary Boundary for Novel Entities: Time for a Reboot (Jahnke A, Bai Y, Brack W, Carney Almroth B, Diamond ML, … Caesar L; incl. Escher BI) | 2026 | Environmental Science & Technology | 10.1021/acs.est.6c03044 |
| Non-targeted Analysis of the Environment: A Special Issue in ES&T and ES&T Letters (Hollender J, Martin JW, Covaci A, Chen D, Letcher RJ, … Newton SR) | 2025 | Environmental Science & Technology | 10.1021/acs.est.5c16761 |
| Predicting Micropollutant Removal in Wastewater Treatment Based on Molecular Structure: Benchmark Data and Models (Cordero Solano JA, Hafner J, McLachlan MS, Singer H, Fenner K) | 2025 | Environmental Science & Technology | 10.1021/acs.est.5c09314 |

**Public assets:** SciLifeLab National Facility for Exposomics (Martin — service access, Stockholm); the WWTP micropollutant-removal benchmark dataset (with Eawag).
**Computational ceiling / collaboration:** Scheringer's multimedia fate modelling is mature and well-validated; the group's recent high-profile output is *argumentative* rather than methodological. **Honest assessment: Cousins and Scheringer are now primarily agenda-setters publishing ES&T Perspectives/Viewpoints, not prediction methodologists.** Do not benchmark a prediction paper against them; do cite them to justify why a chemical class matters. Martin's exposomics facility is a real, accessible analytical resource.

### 18. ARC Arnot Research & Consulting / Univ. of Toronto — Jon A. Arnot (with Trevor N. Brown, Alessandro Sangion, Li Li, Univ. of Nevada Reno)
**Signature contribution:** Bioaccumulation and exposure modelling with **explicit, quantified uncertainty and applicability domains** — the part of QSAR practice most environmental papers skip.

| Paper | Year | Journal | DOI |
|---|---|---|---|
| Identifying uncertainty in physical-chemical property estimation with IFSQSAR (Brown TN, Sangion A, Arnot JA) | 2024 | Journal of Cheminformatics | 10.1186/s13321-024-00853-w |
| Chemical Space Covered by Applicability Domains of Quantitative Structure-Property Relationships and Semiempirical Relationships in Chemical Assessments (Zhang Z, Sangion A, Wang S, Gouin T, Brown T, … Li L) | 2024 | Environmental Science & Technology | 10.1021/acs.est.3c05643 |
| Integrating Monitoring and Biomonitoring Data with Mechanistic Models to Better Estimate and Characterize Aggregate Human Exposures to Semivolatile Organic Chemicals (Hughes L, Cops J, Geerts L, De Brouwere K, Sangion A, … Arnot JA) | 2025 | Environmental Science & Technology | 10.1021/acs.est.5c08964 |
| Collaborative evaluation of in silico predictions for high throughput toxicokinetics (Wambaugh JF, Sipes NS, … Arnot JA, Bertato L, Brown TN, …) | 2025 | Toxicology in Vitro | 10.1016/j.tiv.2025.106150 |

**Public assets:** **IFSQSAR** (open-source Python package, uncertainty-aware physchem QSARs); RAIDAR / EAS-E Suite exposure models (arnotresearch.com — partly commercial).
**Computational ceiling / collaboration:** Narrow but deep. The **ES&T 2024 applicability-domain paper is the citation a reviewer reaches for when a prediction paper has no AD analysis** — read it before you submit. Arnot is a small consultancy-style operation; collaboration is possible but transactional.

### 19. Baylor University — Bryan W. Brooks ("precision ecotoxicology")
**Signature contribution:** The conceptual framing of read-across from pharmacology to ecology — using drug-target conservation and therapeutic plasma concentrations to predict which pharmaceuticals and PPCPs matter to which species and life stages.

| Paper | Year | Journal | DOI |
|---|---|---|---|
| Towards Precision Ecotoxicology: Leveraging Evolutionary Conservation of Pharmaceutical and Personal Care Product Targets to Understand Adverse Outcomes Across Species and Life Stages (Brooks BW, van den Berg S, Dreier DA, LaLone CA, Owen SF, … Zhang X) | 2023 | Environmental Toxicology and Chemistry | 10.1002/etc.5754 |
| Comparative glucocorticoid receptor agonism: In silico, in vitro, and in vivo and identification of potential biomarkers for synthetic glucocorticoid exposure (Cole AR, Blackwell BR, Cavallin JE, Collins JE, Kittelson AR, … Brooks BW) | 2025 | Environmental Toxicology and Chemistry | 10.1093/etojnl/vgae041 |

**Computational ceiling / collaboration:** Low-to-moderate (read-across reasoning, not model building). Brooks is an excellent framing co-author and a very well-connected editor-level figure; he already co-publishes with LaLone and with Chinese groups (Zhang Xiaowei). **Realistic, low-cost collaboration; will not raise your computational ceiling.**

### 20. UNC Chapel Hill — Alexander Tropsha & Eugene N. Muratov
**Signature contribution:** QSAR validation doctrine (the "best practices" lineage) and open NAM web tools for acute/topical toxicity. **Important caveat: the group's centre of gravity has moved to antiviral and oncology drug discovery.**

| Paper | Year | Journal | DOI |
|---|---|---|---|
| External Validation of STopTox — Novel Alternative Method (NAM) for Acute Systemic and Topical Toxicity (Tieghi RS, Melo-Filho CC, Martin HJ, Moreira-Filho JT, LaPratt T, … Muratov EN) | 2025 | Environmental Health Perspectives | 10.1289/EHP16647 |
| One size does not fit all: revising traditional paradigms for assessing accuracy of QSAR models used for virtual screening (Wellnitz J, Jain S, Hochuli JE, Maxfield T, Muratov EN, … Zakharov AV) | 2025 | Journal of Cheminformatics | 10.1186/s13321-025-00948-y |
| Pharmacokinetics Profiler (PhaKinPro): Model Development, Validation, and Implementation as a Web Tool for Triaging Compounds with Undesired Pharmacokinetics Profiles (Rath M, Wellnitz J, Martin HJ, Melo-Filho C, Hochuli JE, … Tropsha A) | 2024 | Journal of Medicinal Chemistry | 10.1021/acs.jmedchem.3c02446 |

**Public assets:** **STopTox** (stoptox.mml.unc.edu) and **PhaKinPro** web tools, free.
**Computational ceiling / collaboration:** High in general cheminformatics; **in environmental toxicology specifically, they are now largely absent — the STopTox external validation is the main 2021–2026 env-relevant output.** Cite the 2025 J Cheminform paper on accuracy paradigms (it is a sharp, useful methodological corrective). Do not treat Tropsha as an environmental-tox benchmark.

### 21. Tulane University — Hao Zhu (**affiliation corrected**)
Hao Zhu has moved: Rutgers Camden → Rowan → **Tulane University, Professor of Biomedical Informatics and Genomics** (Tulane faculty page; 2025 SOT/AACT Distinguished Chinese Toxicologist Award listing him at Tulane). Older sources listing Rutgers or Rowan are stale.
**Signature contribution:** Public-data-driven predictive toxicology — automated model building over large curated chemical/biological datasets, chemical-biological read-across, big-data QSAR.
**Verified 2021–2026 papers:** **Not located in this session.** Author-initial searches for "Zhu H" are too ambiguous to verify safely, and I will not list papers I could not confirm. Treat his recent record as **[unverified]** and check his Tulane/Google Scholar page directly before citing.
**Assessment:** Historically a significant figure in chemical-biological read-across and a natural China-facing contact; current output and computational ceiling not verified here. Likely a receptive and culturally well-placed collaborator.

### 22. Wageningen University — Nynke I. Kramer (PBK modelling for IVIVE)
| Paper | Year | Journal | DOI |
|---|---|---|---|
| Development of a Generic Physiologically Based Kinetic Model for the Prediction of Internal Exposure to Organophosphate Pesticides (Moerenhout TMJA, Chen J, Bouwmeester H, Rietjens IMCM, Kramer NI) | 2024 | Environmental Science & Technology | 10.1021/acs.est.4c06534 |
| A population physiologically based kinetic and toxicodynamic model for acute diazinon exposure (Chen J, Chen B, Wesseling S, Bouwmeester H, Rietjens IMCM, … Kramer NI) | 2025 | Ecotoxicology and Environmental Safety | 10.1016/j.ecoenv.2025.118083 |
| Investigating the effect of glutathione-mediated metabolism of organophosphate pesticides on rat and human toxicokinetics using physiologically based kinetic modeling (Moerenhout TMJA, Bakker W, Bouwmeester H, Kramer NI) | 2026 | Food and Chemical Toxicology | 10.1016/j.fct.2026.116450 |

**Assessment:** Narrow, high-quality generic-PBK modelling. Relevant if you need internal-dose estimates to convert zebrafish water concentrations into tissue concentrations. Moderate ceiling; very approachable.

### 23. UCL — Jason Rihel (zebrafish behavioural fingerprinting)
| Paper | Year | Journal | DOI |
|---|---|---|---|
| Behavioural pharmacology predicts disrupted signalling pathways and candidate therapeutics from zebrafish mutants of Alzheimer's disease risk genes (Kroll F, Donnelly J, Özcan GG, Mackay E, Rihel J) | 2025 | eLife | 10.7554/eLife.96839 |
| Sleep pressure modulates single-neuron synapse number in zebrafish (Suppermpool A, Lyons DG, Broom E, Rihel J) | 2024 | Nature | 10.1038/s41586-024-07367-3 |
| Modeling diseases of aging in larval zebrafish, a paradoxical yet powerful strategy (Özcan GG, Rihel J) | 2026 | Genetics | 10.1093/genetics/iyag027 |

**Assessment:** The intellectual origin of behavioural-fingerprint-based pharmacological inference in zebrafish, and still producing high-quality work — but **not environmental toxicology**, and the computational layer is correlation/clustering of behavioural fingerprints rather than modern representation learning. Public assets: Kroll's open behavioural-analysis tooling (**package name/URL [unverified]**). Best used as a *method* reference and a potential methods-transfer host, not an environmental-tox partner.

### 24. OCHEM / Helmholtz Munich — Igor V. Tetko; Université Paris Cité — Olivier Taboureau
**Not verified in this session.** Author-name ambiguity prevented safe identification of 2021–2026 papers for either PI. OCHEM (ochem.eu) remains a real public modelling platform with QSAR model hosting and consensus prediction; Taboureau's group works on systems-toxicology network modelling. **Both should be treated as [unverified] here and checked directly.** Neither is currently setting the ES&T methodological bar.

---

## ANSWER 1 — The 5–8 most valuable collaborators/benchmarks for a lab with high-information zebrafish behaviour + transcriptomics + LC-MS/MS and non-target HRMS

Ranked by expected value to *this* lab, not by fame.

1. **Eawag — Katarzyna Arturi & Juliane Hollender (+ Kathrin Fenner).** The only group that has solved the exact problem you will hit: turning thousands of unidentified HRMS features into hazard-ranked candidates without confirmed structures (MLinvitroTox). Fenner adds state-of-the-art interpretable GNNs published *in ES&T*. Your zebrafish phenotype data is the validation layer they do not have. **Highest value, both as partner and as the bar.**
2. **UCSF — Michael Keiser & David Kokel.** The benchmark for computational zebrafish behavioural phenotyping, and already moving into insecticides. Their shortcut-learning disclosure is the experimental-design standard your screen must meet. Collaboration is plausible because you have environmental relevance and a transcriptomic axis they lack.
3. **UFZ Leipzig — Beate Escher (for the chemistry/effect quantification) + Wibke Busch, Stefan Scholz and Tamara Tal (for zebrafish phenotype data science).** One institute gives you both the mixture-quantification framework that makes HRMS+bioassay numbers reviewer-proof and a zebrafish data-driven group publishing in ES&T on exactly your readout. Escher's group has a strong track record of co-publishing with East Asian labs.
4. **US EPA CCTE (Paul Friedman / Harrill / Everett for tPODs; Williams / Sobus / Chao for INTERPRET NTA).** Not so much a collaborator as the standard your transcriptomic POD statistics and your NTA prioritisation will be measured against. Adopt their tPOD methodology explicitly (Harrill et al. 2023 shows method choice moves tPODs by orders of magnitude — a reviewer will ask).
5. **US EPA Duluth — Daniel Villeneuve & Carlie LaLone.** The reference for *ecological* tPODs in fish (their PFOS/PFOA/PFHxS zebrafish tPOD-vs-apical comparison is the direct precedent for your transcriptomics), and SeqAPASS is the free tool that makes cross-species claims defensible.
6. **Oregon State — Robyn Tanguay & Lisa Truong (+ Sciome).** The closest competitor-template: their 2026 Environmental Pollution paper is non-target HRMS + zebrafish + computational hazard comparison. Their multi-lab DNT behavioural evaluation also makes them the natural partner for an inter-laboratory validation of your behavioural platform — a very publishable joint output.
7. **McGill — Jianguo Xia (ExpressAnalyst/MetaboAnalyst) and Niladri Basu / Jessica Head (EcoToxChip).** The cheapest route to defensible, reproducible transcriptomic PODs in zebrafish, plus a cross-species transcriptomic comparison database to anchor your results.
8. **JKU Linz — Günter Klambauer.** Only if your ambition includes a genuine ML-methods contribution. He supplies evaluation rigour and few-shot methods for data-poor endpoints; you supply data. Their Tox21 leaderboard is what a methods reviewer will compare you to.

**Deliberately not on this list, and why:** Hartung (volume over method), Cousins/Scheringer (agenda-setting, not prediction), Tropsha (left environmental tox), Rihel (not environmental), Hamers/Westerink/Leusch (excellent assays, negligible computational ceiling — collaborate for endpoints, not for modelling).

---

## ANSWER 2 — Reusable public assets to build on rather than compete with

| Asset | What it is | Owner | Where it lives |
|---|---|---|---|
| **invitroDB (v4.x) + `tcpl` / `tcplfit2`** | ~10⁶ concentration–response series, the standard curve-fit and hit-call implementation | EPA CCTE | CompTox Dashboard download + CRAN (`tcpl`, `tcplfit2`); method paper 10.3389/ftox.2023.1275980 |
| **CompTox Chemicals Dashboard + DSSTox** | ~1.2M curated structures, identifiers, predicted + measured properties, hazard links; the chemical-space substrate for enumerated-space prediction | EPA CCTE (Williams, Grulke, Richard) | comptox.epa.gov/dashboard; guide 10.1016/j.envint.2021.106566 |
| **`httk` R package** | High-throughput toxicokinetics / IVIVE, now with brain and adipose compartments | EPA CCTE + NICEATM | CRAN; 10.3389/fphar.2026.1895108 |
| **OPERA** | Open QSAR suite (logP, solubility, BCF, fish LC50, pKa…) with applicability domain + prediction confidence | NICEATM (Mansouri) | GitHub + Dashboard integration; evaluation 10.1016/j.yrtph.2024.105614 |
| **Integrated Chemical Environment (ICE)** | Curated reference datasets, IVIVE workflows, defined-approach implementations | NICEATM | ice.ntp.niehs.nih.gov |
| **SeqAPASS** | Cross-species susceptibility prediction from protein sequence → structure | EPA Duluth (LaLone) | seqapass.epa.gov; 10.1093/toxsci/kfw119, 10.1002/etc.5537 |
| **MLinvitroTox** | 490 XGBoost classifiers mapping MS2-derived fingerprints → ToxCast/Tox21 endpoint activity; hazard-ranks unidentified HRMS features | Eawag (Arturi, Hollender) | PyPI `mlinvitrotox`; data DOI 10.25678/0007QS; 10.1186/s13321-025-00950-4 |
| **enviPath** | Biotransformation pathway DB + prediction (BBD, soil, sludge packages) with API | Eawag/Auckland (Fenner, Wicker) | envipath.org; 10.1186/s13321-024-00881-6 |
| **WWTP micropollutant-removal benchmark** | Benchmark dataset + baseline models for structure-based removal prediction | Eawag + Stockholm (Fenner, McLachlan) | SI of 10.1021/acs.est.5c09314 |
| **MassBank / MassBank-EU + PubChemLite for Exposomics** | Open FAIR mass spectral library; exposomics-tailored PubChem subset | Luxembourg LCSB (Schymanski) + consortium | massbank.eu; Zenodo (PubChemLite); 10.1093/nar/gkaf1193 |
| **Shinyscreen / pyMSscreen** | HRMS data inspection and automated QC/prescreening | Luxembourg LCSB | 10.1186/s13321-025-01044-x, 10.1186/s13321-026-01260-z |
| **ExpressAnalyst + MetaboAnalyst 6.0 + FastBMD** | RNA-seq and metabolomics analysis for non-model species, with BMD/tPOD modules | McGill (Xia, Ewald) | expressanalyst.ca, metaboanalyst.ca; 10.1038/s41467-023-38785-y, 10.1038/s41596-026-01415-0 |
| **EcoToxChip + EcoToxChip RNA-Seq database** | Cross-species targeted toxicogenomics arrays and a six-species transcriptomic response database | McGill/Saskatchewan/ECCC | ecotoxchip.ca; 10.1002/etc.5803 |
| **JUMP-Cell Painting gallery + CellProfiler + pycytominer** | >100k-perturbation morphological profiles and the full analysis stack | Broad (Carpenter, Singh) | cellpainting-gallery (AWS Open Data); 10.1038/s41592-025-02753-9 |
| **Tox21 reproducible leaderboard** | Fixed splits + baselines for toxicity-prediction benchmarking | JKU Linz (Klambauer) | 10.1021/acs.jcim.6c01148 |
| **IFSQSAR** | Uncertainty-aware physchem property QSARs | ARC (Brown, Arnot) | open-source Python; 10.1186/s13321-024-00853-w |
| **AOP-Wiki + ECOTOX Knowledgebase** | AOP knowledge base; curated ecotoxicity effect data | OECD/JRC; EPA | aopwiki.org; cfpub.epa.gov/ecotox |
| **ToxPi + ToxPi\*GIS** | Transparent weighted-score prioritisation with uncertainty and geospatial linkage | NIEHS/NC State (Reif) | toxpi.org; 10.1038/s41370-022-00433-w |
| **FINS + zebrafish image foundation model** | Automated zebrafish morphology scoring; self-supervised image model | Oregon State + Sciome | 10.1016/j.slast.2026.100426, 10.1016/j.slast.2026.100471 (**hosting location unverified**) |
| **PrecisionTox 200-chemical library** | Diversity-designed reference chemical set with baseline-toxicity and ADME annotations, across five species | Birmingham-led EU consortium | SI of 10.1093/toxsci/kfaf126; precisiontox.org |

**Practical note for your lab:** the single highest-leverage combination is **MLinvitroTox (hazard-rank your HRMS features) → zebrafish behavioural + transcriptomic confirmation of the top-ranked features → ExpressAnalyst/FastBMD tPODs → Escher-style iceberg/BEQ accounting of how much of the observed effect you explained → SeqAPASS for any cross-species target claim.** Every component is free, and the assembly is publishable because nobody has closed that loop with high-information in vivo phenotyping.

---

## ANSWER 3 — Whose work is the methodological bar an ES&T prediction paper is judged against?

A reviewer saying "this has been done better" in 2026 is most likely to cite, in rough order of likelihood:

1. **Kathrin Fenner's group (Eawag) — Zhang, Schwaller & Fenner, ES&T 2025, 10.1021/acs.est.4c12247.** This is the current in-journal standard for a *good* ES&T ML paper: mechanism-guided transfer learning instead of brute force, attention-based substructure attribution, Shapley-value quantification of substructure contributions, and recovery of known structural alerts as validation. If your model is a generic GNN on a small dataset with no mechanistic pretraining and no interpretability check, this is the paper that sinks you. Companion standards from the same group: probabilistic/uncertainty-aware prediction (ES&T 2026, 10.1021/acs.est.6c03516) and publishing an actual benchmark dataset (ES&T 2025, 10.1021/acs.est.5c09314).
2. **Arturi & Hollender (Eawag) — ES&T 2023, 10.1021/acs.est.3c00304 and J Cheminform 2025, 10.1186/s13321-025-00950-4.** The bar for any claim of "prioritising hazard from non-target HRMS". If you prioritise features by intensity, by a crude toxicity proxy, or by a model you built on identified structures only, a reviewer will ask why you did not use or beat MLinvitroTox.
3. **Keiser & Kokel (UCSF) — Nat Commun 2024, 15:9955, 10.1038/s41467-024-54375-y.** The bar for high-dimensional in vivo phenotype → chemical/target inference, and specifically for *experimental* rigour in ML-coupled screens: well-wise randomisation, high replication, prospective orthogonal validation, and an explicit shortcut-learning audit. Any zebrafish behaviour + ML paper now gets compared to this.
4. **Seal & Carpenter — Nat Commun 2026, 10.1038/s41467-026-68725-5 ("Counting cells can accurately predict small-molecule bioactivity benchmarks").** The canonical "your baseline is too weak / your benchmark is gameable" citation. Pre-empt it: report a trivial baseline (e.g. a single summary feature, or a physicochemical-descriptor-only model) alongside your deep model.
5. **EPA CCTE — Harrill et al., Toxicology 2023, 10.1016/j.tox.2023.153694 (tPOD method sensitivity) and Feshuk et al., Front Toxicol 2023, 10.3389/ftox.2023.1275980 (tcpl/invitroDB).** The bar for *dose–response and POD statistics*. Harrill shows tPODs vary by orders of magnitude with computational choice; if you report a single tPOD without a sensitivity analysis across methods, expect to be asked why.
6. **Escher (UFZ) — iceberg modelling and BEQ/EBT framework (10.1039/d3em00033h; 10.1021/acs.est.2c06365; and the Elbe study 10.1021/acsenvironau.4c00059 showing quantified chemicals explain 0.002–1.2% of observed effect).** The bar for *effect accounting*. A paper claiming to have identified "the" drivers of an observed effect without an explained-fraction calculation is now straightforwardly criticisable.
7. **Klambauer (JKU Linz) — J Chem Inf Model 2026, 10.1021/acs.jcim.6c01148.** The bar for *evaluation protocol*. Reproducible leaderboard, fixed splits, no leakage. Increasingly cited by ML-literate reviewers of environmental journals.
8. **Arnot/Li — ES&T 2024, 10.1021/acs.est.3c05643 (applicability-domain chemical-space coverage) and Brown et al. J Cheminform 2024, 10.1186/s13321-024-00853-w (IFSQSAR uncertainty).** The bar for *applicability domain and uncertainty reporting*, a near-universal reviewer complaint.
9. **LaLone (EPA Duluth) — SeqAPASS lineage plus the docking/MD extensions (10.1016/j.comtox.2024.100319; 10.1093/etojnl/vgaf160).** The bar for *cross-species extrapolation claims*. "It binds the human receptor, therefore it affects fish" is no longer acceptable without conservation analysis.

**Blunt summary of who is ahead versus who is coasting:**

- **Genuinely methodologically ahead:** Fenner/Arturi/Hollender (Eawag) — interpretable, uncertainty-aware, benchmark-publishing ML inside environmental chemistry; Keiser/Kokel (UCSF) — deep metric learning with honest artefact reporting; Klambauer (JKU) — evaluation rigour; Carpenter/Singh/Seal (Broad/Cambridge) — benchmark skepticism and the largest open phenotypic resource.
- **Indispensable but deliberately conservative:** EPA CCTE and NIEHS/NICEATM. Their ceiling is set by regulatory defensibility, not by ambition. Use them; do not expect novelty from them.
- **Strong framework, modest computation:** Escher (UFZ), Villeneuve/LaLone (EPA Duluth), Viant/Colbourne (Birmingham), Basu/Xia (McGill), Tollefsen/Song (NIVA), Arnot.
- **Excellent wet-lab, negligible computational layer:** Hamers, Westerink, Lamoree, Legler (NL); Leusch/Neale (Griffith); Hecker/Crump/Munkittrick (Canada); Schirmer (Eawag, though now partnering with Županič for computation).
- **Coasting on volume / position rather than method:** **Thomas Hartung** — his 2025–26 record is dominated by Frontiers and ALTEX opinion pieces on AI in toxicology; cite for framing, never as a benchmark. **Ian Cousins and Martin Scheringer** — now mainly ES&T Perspectives and Viewpoints on persistence and PFAS policy; important for justifying relevance, irrelevant as prediction methodology. **Alexander Tropsha** — still a major cheminformatics figure, but has effectively left environmental toxicology for antiviral/oncology AI; one env-relevant output (STopTox external validation) in the whole 2021–2026 window.
- **Rising and worth watching:** Katarzyna Arturi (Eawag) — her name on a paper is now a quality signal in HRMS prioritisation; Jessica Ewald (ex-McGill → Broad) — uniquely positioned between ecotoxicogenomics and Cell Painting; Peter Schumann (EPA Duluth) — driving the docking/MD extension of SeqAPASS; Wibke Busch and Tamara Tal (UFZ) — zebrafish phenotype data science in ES&T; Anže Županič (NIB Slovenia) — the computational half of Schirmer's new high-content fish-cell pipeline.
