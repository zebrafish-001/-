# ES&T Publishing Landscape for Computational Pollutant-Hazard Prediction (2022–2026)

Audit date: 2026-11-13. Prepared for a lab targeting ES&T with pollutant-prediction / computational-toxicology work.

## Provenance and verification status

- **Primary verified source: PubMed** (via MCP PubMed server). Every row tagged `[PM]` has title, journal, year and DOI taken directly from the PubMed record. Cite PubMed as the retrieval source.
- **Consensus** (MCP) supplied near-full body text for the EMBRACE Viewpoint; quotes marked `[CONSENSUS-TEXT]` are verbatim from that record.
- **WebSearch snippets** supplied verbatim quotes from publisher/journal pages for several editorials; these are marked `[SNIPPET-QUOTE]` — the wording was returned by the search tool reading the page, but **could not be re-verified against the publisher page directly** (see blocked hosts below). Treat as high-confidence but not double-checked.
- **BLOCKED HOSTS in this session** (DNS/policy refusal): `pubs.acs.org`, `researcher-resources.acs.org`, `par.nsf.gov`, `api.crossref.org`, `eutils.ncbi.nlm.nih.gov`, `api.openalex.org`. No ACS full text or ACS masthead page could be opened. Anything that would have required those pages is explicitly labelled UNVERIFIED below.
- **Nothing in this file is invented.** Where a detail could not be confirmed it says so.

---

## 1. Inventory of real recent papers: computational prediction × pollutant hazard

Tag key: **P** = pure prediction, no new experiments. **P+V** = prediction plus a confirmatory experiment generated in the same paper. **V-led** = experiment-led, computation as mechanism support.

Validation column: none / in vitro / cell / zebrafish / medaka / other-invert / rodent / field samples / human cohort.

### 1A. Environmental Science & Technology (ES&T)

| # | Title | Yr | Computational method | Pollutant class | Experimental validation | Tag | DOI |
|---|---|---|---|---|---|---|---|
| 1 | Why Can Cross-End Point Transfer Fail in Computational Toxicology? Diagnosing Decision-Structure Incompatibility across 13 End Points under Scaffold-Held-Out Evaluation | 2026 | Transfer learning, multitask, MAML, stacking; scaffold-disjoint CV, leakage control | broad chemical space, 13 tox endpoints | none | P | 10.1021/acs.est.6c08192 [PM] |
| 2 | Mechanistic Prediction and High-Throughput Risk Screening of Aquatic Contaminants Using Daphnia magna AOP Network | 2026 | Multidomain deep learning QSAR + applicability domain + AOP network | aquatic contaminants (broad) | none | P | 10.1021/acs.est.6c06646 [PM] |
| 3 | Tabular Foundation Models for Environmental Quantitative Structure-Activity Relationship: Robust Prediction with Imperfect Data | 2026 | TabPFN foundation models; zero/few-shot, generative augmentation | OH-radical/singlet-O2 kinetics + tox endpoints | none | P | 10.1021/acs.est.6c05983 [PM] |
| 4 | Filling Ecotoxicity Data Gaps for Plasticizers via an Integrated Framework: Toxicity Prediction, Prioritization, and Hazardous Concentration Derivation | 2026 | Species-specific QSAR, 6 species/3 trophic levels, HC5 derivation | plasticizers | none | P | 10.1021/acs.est.6c01604 [PM] |
| 5 | MechoA+: A Chemical Structure Profiler Raising the Bar for the Prediction of Mechanisms of Toxic Action for Chemical Safety Assessment | 2026 | Structure-based MIE/MoA classification scheme | broad industrial chemicals | none | P | 10.1021/acs.est.5c18657 [PM] |
| 6 | Machine Learning-Based Prediction for over 10,000 PFAS across Multiple Fish Species Enables Large-Scale Toxicological Analysis | 2026 | ML regression on mechanistic descriptors; NOEC prediction | PFAS (10,863) | none | P | 10.1021/acs.est.5c17531 [PM] |
| 7 | MarineTox Predictor: An Online Library Platform for Enhancing Low-Resourced Saltwater Ecotoxicity Prediction via Knowledge Sharing from Freshwater Ecotoxicity | 2026 | Multitask deep learning + cross-domain transfer; web server | broad, marine species | none | P | 10.1021/acs.est.5c15496 [PM] |
| 8 | EDC Profiler: A High-Throughput Screening Server for Identifying Endocrine Disrupting Chemicals toward Multiple Nuclear Receptors | 2026 | Interaction-aware ML across nuclear receptors; web server | EDCs | none | P | 10.1021/acs.est.5c18135 [PM] |
| 9 | BeeEcoTox: A Large Language Model-Empowered Graph-Learning Framework for Predicting Ecotoxicity of Agrochemicals to Bees | 2026 | LLM + multimodal graph learning | agrochemicals/pesticides | none | P | 10.1021/acs.est.5c18162 [PM] |
| 10 | Counted Fingerprint-Enhanced Graph Neural Network Models Enable Accurate Screening of hERG Blockers from Diverse Categories of Chemicals | 2026 | GNN + counted fingerprints | diverse chemicals (hERG) | none | P | 10.1021/acs.est.5c16775 [PM] |
| 11 | AI-Driven Species Sensitivity Distribution (AI-4-SSD) Framework for Predicting Aquatic Ecological Risks of Chemical Pollutants in Global Near-Coastal Environments | 2026 | AI-generated SSDs at global scale | >350,000 registered chemicals | none (uses occurrence data) | P | 10.1021/acs.est.6c00675 [PM] |
| 12 | A Stacking Ensemble Model for Koc Prediction and Environmental Mobility Assessment of Global Neutral Chemicals | 2026 | Stacking ensemble ML | neutral PMT chemicals | none | P | 10.1021/acs.est.5c16765 [PM] |
| 13 | Screening of Respiratory Toxicity of Environmental Compounds Based on Multimodal Feature Fusion Model | 2026 | Multimodal feature fusion DL | broad environmental compounds | none | P | 10.1021/acs.est.5c17401 [PM] |
| 14 | ParetoGen: Generative Machine Learning Models To Push the Pareto Optimal Frontier of Functionality-Hazard Trade-offs in PFAS Green Alternative Designs | 2026 | Generative ML, multi-objective Pareto optimisation | PFAS alternatives | none | P | 10.1021/acs.est.6c00350 [PM] |
| 15 | Leveraging Large Language Models for Contextual Prioritization of Contaminants of Emerging Concern in Chemical Mixtures | 2026 | Agent-based LLM workflow over NTA inventories | CECs in mixtures | none | P | 10.1021/acs.est.6c01342 [PM] |
| 16 | Integrated Machine-Learning Framework for Balanced Performance-Safety Design of Iron-Based Remediation Materials | 2026 | ML on 1,007-case literature dataset; performance+safety co-assessment | Fe-based remediation nanomaterials | none (literature-derived) | P | 10.1021/acs.est.6c02923 [PM] |
| 17 | Integrating Cascade Mechanistic Insights into Structure-Activity Relationships for Quantitative Mode-of-Action Analysis: A Novel Risk Assessment Framework for OPFRs | 2026 | Quantitative MoA (qMOA) framework, structure + cascade mechanism | organophosphate flame retardants | none | P | 10.1021/acs.est.6c01412 [PM] |
| 18 | Mechanism-Based Multitarget Modeling for Pathway-Level Prediction of PI3K/Akt Signaling Perturbation Induced by Liquid Crystal Monomers | 2026 | KEGG enrichment + 19-protein multitarget models | liquid crystal monomers | none | P | 10.1021/acs.est.6c00371 [PM] |
| 19 | Molecular Insights into Ocular Exposure Risk of Indoor Smoke Components on the Tear Film | 2026 | Atomistic MD of tear-film lipid layer | indoor smoke constituents / PAHs | none | P | 10.1021/acs.est.5c17707 [PM] |
| 20 | A Protein Interactome-Based Framework Reveals the General Toxicity of Chemicals | 2025 | Protein-interactome network modelling | broad chemicals | none | P | 10.1021/acs.est.5c08341 [PM] |
| 21 | Replacing Fish Early Life Stage Toxicity Test: Performance of Three QSAR Tools for Recently Submitted REACH Data | 2025 | Benchmarking of 3 regulatory QSAR tools vs REACH submissions | REACH-registered industrial chemicals | none (external regulatory data) | P | 10.1021/acs.est.5c08163 [PM] |
| 22 | Gene Target Prediction of Environmental Chemicals Using Coupled Matrix-Matrix Completion | 2024 | Coupled matrix-matrix completion | environmental chemicals (broad) | none | P | 10.1021/acs.est.4c00458 [PM] |
| 23 | Two-Stage Machine Learning-Based Approach to Predict Points of Departure for Human Noncancer and Developmental/Reproductive Effects | 2024 | Two-stage ML; POD prediction | chemicals in commerce | none | P | 10.1021/acs.est.4c00172 [PM] |
| 24 | A Data-Driven Computational Framework for Assessing the Risk of Placental Exposure to Environmental Chemicals | 2024 | Placental gene-network computational framework | environmental chemicals | none | P | 10.1021/acs.est.4c00475 [PM] |
| 25 | Data-Driven Quantitative Structure-Activity Relationship Modeling for Human Carcinogenicity by Chronic Oral Exposure | 2023 | Data-driven QSAR | carcinogens (oral) | none | P | 10.1021/acs.est.3c00648 [PM] |
| 26 | Potential for Machine Learning to Address Data Gaps in Human Toxicity and Ecotoxicity Characterization | 2023 | Systematic ML gap-filling assessment (LCIA context) | broad chemicals | none | P | 10.1021/acs.est.3c05300 [PM] |
| 27 | 6PPD-Quinone Promotes Metabolic Dysfunction-Associated Steatotic Liver Disease through Immune-Inflammatory Disruption | 2026 | Computational toxicology target prediction + human transcriptomics intersection | tire antioxidant TP (6PPD-Q) | cross-model (cell + in vivo) | P+V | 10.1021/acs.est.6c05547 [PM] |
| 28 | Mapping the Invisible Landscape of Pesticides and Adjuvants in Peri-Urban Agricultural Waterways of the Megacity Shanghai | 2026 | NTA + in silico hazard prioritisation | pesticides + adjuvants | field samples (193 sites) + in vivo tox | P+V | 10.1021/acs.est.6c02355 [PM] |
| 29 | Health Risk Assessment for Rare Earth Ions: From End Point Identification of Cytotoxicity to Mixed Toxicity Prediction | 2026 | Mixture-toxicity prediction models | rare earth ions (16) | 8 human cell lines, single+binary | P+V | 10.1021/acs.est.6c00777 [PM] |
| 30 | Combination of Chromatographic and Machine Learning-Driven Virtual Fractionation Identifies Aryl Hydrocarbon Receptor Agonists in Sediments | 2026 | ML-driven "virtual fractionation" | sediment organic mixtures / AhR agonists | field sediment + in vitro AhR bioassay | P+V | 10.1021/acs.est.6c02059 [PM] |
| 31 | Molecular Representation and Closed-Loop Validation for Toxicity Assessment of Organic Compounds in Ambient Air PM | 2026 | Interpretable ML on curated A549 cytotoxicity data; closed loop | PM-bound organics | in vitro A549 (closed-loop) | P+V | 10.1021/acs.est.5c17667 [PM] |
| 32 | Structure-Informed Comprehensive Screening and Risk Prioritization of Organophosphorus Compounds in Human Serum: Revealing the Hidden Burden and Emerging Risks | 2026 | Structure-informed screening + risk prioritisation | organophosphorus compounds | human serum samples | P+V | 10.1021/acs.est.5c18271 [PM] |
| 33 | Ecological and Structural Drivers Underlying Species-Specific Estrogen Receptor α Responses to Estrogenic Chemicals in Mammals | 2026 | NAMs: bioinformatics + in silico structure + ML | estrogenic chemicals | receptor assays (cross-species) | P+V | 10.1021/acs.est.6c04974 [PM] |
| 34 | Mechanistic Insights into PET-MPs-Aggravated Ischemic Stroke via Integrated Computational-Experimental Approaches | 2026 | Integrated computational-experimental | PET microplastics | rodent/cell | P+V | 10.1021/acs.est.6c00049 [PM] |
| 35 | AOP-Guided Toxicogenomic Mapping Profiles for Mechanism-Informed Toxicity Pattern Prediction in Zebrafish | 2026 | AOP-guided toxicogenomic mapping, pattern prediction | broad chemicals | zebrafish | P+V | 10.1021/acs.est.6c01532 [PM] |
| 36 | Network-Based Assessment of Environmental Neurotoxicants Using High-Throughput Transcriptomics in Zebrafish Embryos | 2026 | Network analysis on HT transcriptomics | neurotoxicants | zebrafish embryos | P+V | 10.1021/acs.est.5c11994 [PM] |
| 37 | Unveiling the Underexplored Neurotoxicity of 2,6-Dichloro-1,4-benzoquinone: Insights from Network Toxicology and In Vivo Models | 2026 | Network toxicology | DBP (halobenzoquinone) | in vivo models | P+V | 10.1021/acs.est.6c11071 [PM] |
| 38 | Mechanism-Driven Risk Assessment of 1,3,6-Tribromocarbazole: An Integrated Strategy Implicates ESR1-Associated Cardiovascular Toxicity | 2026 | Integrated in silico target strategy | polyhalogenated carbazoles | zebrafish/in vivo | P+V | 10.1021/acs.est.6c08481 [PM] |
| 39 | Diversity of Iodinated Water Disinfection Byproducts and Their Formation Dynamics Discovered Using Exposome-Scale Nontargeted Analysis and Machine Learning | 2026 | Exposome-scale NTA + ML | iodinated DBPs | real water, formation experiments | P+V | 10.1021/acs.est.6c03869 [PM] |
| 40 | Halogenated Nucleosides: Highly Toxic Biogenic Disinfection Byproducts Prevalent in Drinking Water | 2026 | 2 QSAR models for toxicity | halogenated nucleoside DBPs | nationwide survey (China) + toxicity assays | P+V | 10.1021/acs.est.6c07375 [PM] |
| 41 | Overlooked Effluent Toxicity: A Missing Link in China's Wastewater Discharge Standards | 2026 | Automated/DL quantification for WET throughput | whole wastewater effluent | C. elegans WET, large-scale effluents | P+V | 10.1021/acs.est.6c00944 [PM] |
| 42 | Uncovering the Global Burden and Future Trajectories of Nanomagnetite Particle Emissions from Biomass Power Plants | 2026 | Emission-inventory + trajectory modelling | nanomagnetite ultrafine particles | in vitro cytotoxicity | P+V | 10.1021/acs.est.6c02455 [PM] |
| 43 | Machine Learning-Based Hazard-Driven Prioritization of Features in Nontarget Screening of Environmental High-Resolution Mass Spectrometry Data | 2023 | ML hazard prioritisation of NTS features | unknown organic contaminants | real environmental samples | P+V | 10.1021/acs.est.3c00304 [PM] |
| 44 | Machine Learning Demonstrates Dominance of Physical Characteristics over Particle Composition in Coal Dust Toxicity | 2024 | ML feature-importance | coal/mine dust | in vitro toxicity data | P+V | 10.1021/acs.est.3c08732 [PM] |
| 45 | Environmental Hazard Screening of Heterocyclic Polyaromatic Hydrocarbons: Physicochemical Data and In Silico Models | 2022 | In silico hazard models + new physchem measurements | heterocyclic PAHs | new physicochemical measurements | P+V | 10.1021/acs.est.2c06915 [PM] |
| 46 | Perturbation of the Reproductive Endocrine System by Halogenated Nitrophenols via Thyroid Receptor Signaling: Implications for Developmental, Fertility, and Intergenerational Risks in Japanese Medaka | 2026 | Receptor-signalling in silico support | halogenated nitrophenol DBPs | medaka, multigenerational | V-led | 10.1021/acs.est.6c06184 [PM] |
| 47 | Potential Ecological Risks of the Novel Alternative Plasticizer Di(isononyl)cyclohexane-1,2-Dicarboxylate via Metabolic Toxification in Earthworms | 2026 | metabolic/biotransformation modelling support | DINCH plasticizer | earthworms + MS imaging | V-led | 10.1021/acs.est.6c02959 [PM] |
| 48 | Lipophilicity and Steric Constraints Govern V-Shaped Inhibition of Human and Rat Placental 3β-Hydroxysteroid Dehydrogenase by Dialkyldimethylammonium Disinfectants | 2026 | SAR + docking | quaternary ammonium disinfectants | enzyme assays (human + rat) | V-led | 10.1021/acs.est.6c02784 [PM] |
| 49 | Identifying Genotoxicity Forcing Agents from Individual Aliphatic and Aromatic Disinfection Byproducts in Drinking Water and Wastewater Effluents | 2026 | concentration-response attribution modelling | DBPs (12 groups) | genotoxicity assays, real waters | V-led | 10.1021/acs.est.6c04014 [PM] |
| 50 | Attribution of PM2.5-Induced Transcriptomic Perturbation to Toxic Components | 2026 | Interpretable chemotranscriptomic attribution | PM2.5 components | cells + field PM samples | V-led | 10.1021/acs.est.6c05482 [PM] |
| 51 | Reproductive Toxicity of the Fungicide Pyraclostrobin: Endocrine-Disrupting and Mechanistic Insights | 2026 | mechanistic/in silico support | strobilurin fungicide | zebrafish, 120 d chronic | V-led | 10.1021/acs.est.6c00003 [PM] |
| 52 | BHT and Its Metabolites Disrupt β2-Adrenergic Signaling: A Biotransformation-Dependent Cardiotoxicity Mechanism in Zebrafish | 2026 | receptor docking/mechanism support | synthetic antioxidant BHT | zebrafish | V-led | 10.1021/acs.est.6c04202 [PM] |
| 53 | Neurodevelopmental Toxicity of Tris(2,4-di-tert-Butylphenyl)phosphate: Mechanistic Insights from Laboratory Models and Implications for Human Health | 2026 | mechanism support | novel organophosphate ester | laboratory models (in vivo) | V-led | 10.1021/acs.est.6c07562 [PM] |
| 54 | Trifluoroacetic Acid Competitively Inhibits Lactate Dehydrogenase to Disrupt Endothelial Glycolysis and Impair Vascular Development | 2026 | enzyme-binding/in silico support | TFA (F-gas degradation product) | endothelial cells + in vivo vascular | V-led | 10.1021/acs.est.6c06569 [PM] |
| 55 | Three-Dimensional Burrowing Behavior of Earthworms for Ecotoxicological Studies | 2026 | Deep-learning trajectory reconstruction | soil contaminants | earthworms, transparent medium | V-led | 10.1021/acs.est.5c15144 [PM] |
| 56 | Deep Learning-Enabled Unbiased Precision Toxicity Assessment of Zebrafish Organ Development | 2025 | Deep learning organ-level phenotyping | broad pollutants | zebrafish | V-led | 10.1021/acs.est.5c10763 [PM] |
| 57 | Deep Learning-Enabled Morphometric Analysis for Toxicity Screening Using Zebrafish Larvae | 2023 | Deep-learning morphometrics | environmental pollutants | zebrafish larvae | V-led | 10.1021/acs.est.3c00593 [PM] |
| 58 | A Novel Framework of an Adverse Outcome Pathway Targeting the Eye Lens: Mechanistic Insights from DCOIT Exposure in Cataract Etiology | 2026 | AOP construction + in silico (pull-down informed) | marine antifoulant DCOIT | ex vivo + in vitro + in vivo | V-led | 10.1021/acs.est.6c00969 [PM] |
| 59 | Integrative Proteomic and In Silico Analysis of Perfluorooctanoic Acid Exposures in Primary Human Placental Cytotrophoblasts | 2026 | In silico analysis on proteomics | PFOA | primary human cytotrophoblasts | V-led | 10.1021/acs.est.5c12107 [PM] |
| 60 | Comprehensive Mapping of Ionic Liquid Degradation Pathways and Toxicity Risks in UV/NaClO Treatment via Integrated Molecular Networking and (In Silico) Toxicology | 2026 | molecular networking + in silico tox | ionic liquids + TPs | degradation experiments, real waters | V-led | 10.1021/acs.est.5c15866 [PM] |
| 61 | Unveiling Halogenated and Nitrogenous DBPs in Chloramination-Ozonation Process: DFT-Driven Formation Pathways from Tyrosine and Toxicity Assessment | 2026 | DFT formation pathways | halogenated/N-DBPs | cytotoxicity assays | V-led | 10.1021/acs.est.6c00147 [PM] |
| 62 | Isothiazolinone Disrupts Reproductive Endocrinology by Targeting the G-Protein-Coupled Receptor Signaling | 2024 | receptor target in silico support | isothiazolinones | in vivo long-term reproductive | V-led | 10.1021/acs.est.3c08577 [PM] |
| 63 | Thyroid Endocrine Disruption and Mechanism of the Marine Antifouling Pollutant DCOIT | 2024 | mechanism support | DCOIT | in vivo/in vitro thyroid | V-led | 10.1021/acs.est.4c07614 [PM] |
| 64 | 6PPD, Not 6PPD-Quinone, Induced Serious Zebrafish Eye Damage by Disrupting the Thyroid Signaling Pathway | 2024 | mechanism support | 6PPD / 6PPD-Q | zebrafish | V-led | 10.1021/acs.est.4c11264 [PM] |

### 1B. ES&T Letters

| # | Title | Yr | Method | Pollutant class | Validation | Tag | DOI |
|---|---|---|---|---|---|---|---|
| 65 | Bioactivity Classification of 2,649 Per- and Polyfluoroalkyl Substances (PFASs) via Quantitative Structure-Activity Relationships and Molecular Docking to Health-Relevant Proteins | 2026 | QSAR + docking to tox-relevant proteins | PFAS (2,649) | none | P | 10.1021/acs.estlett.6c00172 [PM] |
| 66 | Hazard Assessment of Antioxidants as Contaminants of Concern | 2026 | In silico NRB/P/B/T profiling of >500 compounds | synthetic + natural antioxidants | none | P | 10.1021/acs.estlett.5c01217 [PM] |
| 67 | Screening Environmentally Benign Ionic Liquids for CO2 Absorption Using Representation Uncertainty-Based Machine Learning | 2024 | Representation-uncertainty ML (extrapolation control) | ionic liquids (toxicity + viscosity) | none | P | 10.1021/acs.estlett.4c00524 [PM] |
| 68 | Systematic Handling of Environmental Fate Data for Model Development—Illustrated for the Case of Biodegradation Half-Life Data | 2023 | data curation protocol for model building | broad chemicals (persistence) | none | P | 10.1021/acs.estlett.3c00526 [PM] |
| 69 | ShinyTPs: Curating Transformation Products from Text Mining Results | 2023 | text mining + FAIR curation tool | transformation products | none | P | 10.1021/acs.estlett.3c00537 [PM] |
| 70 | FAIR and Effective Communication of Data on Chemical Contaminant Biotransformation in the Environment | 2025 | review/position on prediction of biotransformation + FAIR data | contaminants + TPs | none (position piece) | P | 10.1021/acs.estlett.5c00753 [PM] |

### 1C. Environment International

| # | Title | Yr | Method | Pollutant class | Validation | Tag | DOI |
|---|---|---|---|---|---|---|---|
| 71 | A practical decision-making approach for tiered in silico chemical hazard assessment based on the safe and sustainable by design framework | 2026 | tiered in silico hazard decision framework (SSbD) | industrial chemicals/alternatives | none | P | 10.1016/j.envint.2026.110527 [PM] |
| 72 | Adverse outcome pathway network-based approach for the evaluation of thyroid hormone system disruption for human health and environmental regulatory hazard assessment | 2026 | AOP network for regulatory THSD assessment | thyroid-disrupting chemicals | none | P | 10.1016/j.envint.2026.110451 [PM] |
| 73 | An integrated computational framework for hazard identification of emerging contaminants: a case study of 6PPD | 2026 | integrated computational hazard ID | 6PPD / emerging contaminants | none | P | 10.1016/j.envint.2026.110334 [PM] |
| 74 | Predicting the immunotoxic potential of chemical mixtures based on their endocrine activity profiles via computational modeling and in vitro bioassays | 2026 | computational mixture modelling | EDC mixtures | in vitro bioassays | P+V | 10.1016/j.envint.2026.110413 [PM] |
| 75 | Integrative computational toxicology and experimental validation unveils ESR1-mediated steroidogenic disruption in triphenyl phosphate-induced female reproductive toxicity | 2026 | network toxicology + docking | TPHP (OPFR) | in vivo/in vitro validation | P+V | 10.1016/j.envint.2026.110458 [PM] |
| 76 | An AI-based integrative framework with multi-omics and experimental validation reveals mechanisms of DABP-induced neurotoxicity | 2026 | network toxicology + ML target prioritisation + multi-omics | 4,4'-diaminobenzophenone | experimental validation | P+V | 10.1016/j.envint.2026.110269 [PM] |
| 77 | Photoinitiators and UV filters as triggers of oxidative stress damage: evidence from national monitoring to in vitro and in silico studies | 2026 | docking + in silico | photoinitiators, UV filters | 334 paired dust+urine samples, in vitro | P+V | 10.1016/j.envint.2026.110296 [PM] |
| 78 | Occurrence, mixture neurotoxicity risk, and prioritization of neonicotinoid and diamide insecticides in urban residential soils | 2026 | mixture risk + prioritisation modelling | neonicotinoids, diamides | 200 field soils (10 provinces) | P+V | 10.1016/j.envint.2026.110507 [PM] |
| 79 | Prenatal urinary phenanthrene metabolites associated with fetal growth restriction: a nested case-control study with integrated computational toxicology | 2026 | integrated computational toxicology | PAH metabolites | human cohort (nested case-control) | P+V | 10.1016/j.envint.2026.110486 [PM] |
| 80 | Machine learning prediction model combined with network toxicology analysis identifies potential cardiotoxic components and mechanisms among 741 pesticides | 2025 | ML + network toxicology | 741 pesticides | limited/none | P | 10.1016/j.envint.2025.109860 [PM] |
| 81 | Integrated network toxicology and transcriptomics reveal NF-κB signaling as a key mediator of TDCPP-induced inflammatory responses in human microglia | 2026 | network toxicology | TDCPP (OPFR) | human microglia in vitro | V-led | 10.1016/j.envint.2026.110373 [PM] |
| 82 | Integrative network toxicology and single-cell analysis implicates a potential TGFBR1-centered fibroblast remodeling axis in Benzo[a]pyrene-related atrial fibrillation | 2026 | network toxicology + scRNA-seq | BaP | human tissue single-cell data | V-led | 10.1016/j.envint.2026.110390 [PM] |
| 83 | Chemical structure drives developmental toxicity of alkyl-substituted naphthalenes in zebrafish | 2025 | structure-activity analysis | alkyl-naphthalenes | zebrafish | V-led | 10.1016/j.envint.2025.109837 [PM] |
| 84 | Early-life triphenyl phosphate (TPhP) exposure impairs the zebrafish dopaminergic system and elevates parkinsonian-like neurotoxicity risk | 2026 | mechanism support | TPhP | zebrafish | V-led | 10.1016/j.envint.2026.110320 [PM] |

### 1D. Journal of Hazardous Materials

| # | Title | Yr | Method | Pollutant class | Validation | Tag | DOI |
|---|---|---|---|---|---|---|---|
| 85 | Integrative QSAR and q-RASAR models for Danio rerio acute toxicity from short-term exposures: Mechanistic insights and data gap filling | 2025 | QSAR + q-RASAR | broad chemicals | none | P | 10.1016/j.jhazmat.2025.139710 [PM] |
| 86 | A priority control list for LCMs in freshwater food chain by deep learning | 2025 | deep learning prioritisation | liquid crystal monomers | none | P | 10.1016/j.jhazmat.2025.140362 [PM] |
| 87 | MLSE machine learning algorithm-assisted priority screening of aquatic toxicity risk of DBPs and the guidance of environmental regulations | 2025 | ML priority screening | DBPs | none | P | 10.1016/j.jhazmat.2025.140069 [PM] |
| 88 | Integrated prioritization of liquid crystal monomers based on environmental hazard and PPARγ-binding potential | 2026 | hazard + receptor-binding prioritisation | liquid crystal monomers | none | P | 10.1016/j.jhazmat.2026.144178 [PM] |
| 89 | Integrating RNA sequencing with deep learning-based metabolic toxicity prediction: A new perspective on screening prioritized liquid crystal monomers | 2025 | DL metabolic toxicity prediction + RNA-seq | liquid crystal monomers | RNA-seq / in vivo | P+V | 10.1016/j.jhazmat.2025.140465 [PM] |
| 90 | Proteome-wide reverse molecular docking reveals folate receptor as a mediator of PFAS-induced neurodevelopmental toxicity | 2026 | proteome-wide reverse docking | PFAS | in vivo/in vitro | P+V | 10.1016/j.jhazmat.2026.142012 [PM] |
| 91 | Bridging HRMS spectra and anti-Staphylococcus aureus activity by machine learning for prioritization of putative antibacterial contaminants in wastewater | 2026 | ML on HRMS spectra → bioactivity | antibacterial contaminants | wastewater samples + bioassay | P+V | 10.1016/j.jhazmat.2026.144125 [PM] |
| 92 | Cross-species concordance indicates ecological risks of liquid crystal monomers in freshwater and saltwater sediments of China | 2026 | cross-species concordance modelling | liquid crystal monomers | field sediments | P+V | 10.1016/j.jhazmat.2026.141880 [PM] |
| 93 | A multi-target adverse outcome pathway network for sub-chronic ketamine-induced cognitive impairment in adult zebrafish | 2026 | AOP network | ketamine (pharmaceutical contaminant) | adult zebrafish | V-led | 10.1016/j.jhazmat.2026.143858 [PM] |
| 94 | Structure-dependent visual toxic mechanisms of benzothiazoles in zebrafish larvae (Danio rerio) | 2026 | SAR/mechanism support | benzothiazoles | zebrafish larvae | V-led | 10.1016/j.jhazmat.2026.143464 [PM] |
| 95 | Triclosan induces cardiac malformations via an estrogen receptor-ERK-mitochondrial apoptotic signaling axis in zebrafish embryos | 2026 | receptor/pathway in silico support | triclosan | zebrafish embryos | V-led | 10.1016/j.jhazmat.2026.143189 [PM] |
| 96 | 6PPD-Q interaction with human apo-transferrin accompanies hepatic iron dysregulation and pro-ferroptotic responses: Evidence from in vitro and zebrafish studies | 2026 | protein-binding simulation | 6PPD-Q | in vitro + zebrafish | V-led | 10.1016/j.jhazmat.2026.143315 [PM] |
| 97 | Tire rubber-derived contaminant 6PPD-quinone induced male-biased reproductive toxicity in zebrafish (Danio rerio) | 2026 | mechanism support | 6PPD-Q | zebrafish | V-led | 10.1016/j.jhazmat.2026.144194 [PM] |
| 98 | Typical persistent organic pollutant exposure induces body axial curvature through binding to Kdm1a transcriptionally activating expression of urp2 in zebrafish | 2026 | target binding in silico | POPs | zebrafish | V-led | 10.1016/j.jhazmat.2026.141764 [PM] |

### 1E. Water Research

| # | Title | Yr | Method | Pollutant class | Validation | Tag | DOI |
|---|---|---|---|---|---|---|---|
| 99 | Establishment of predictive machine learning models for disinfection byproduct formation during chlorination or chlorine photolysis | 2026 | predictive ML (formation) | DBPs | none (lab data) | P | 10.1016/j.watres.2026.126344 [PM] |
| 100 | Toxicity-guided assessment of disinfection by-products via machine learning and network toxicology | 2026 | ML + network toxicology | DBPs | none | P | 10.1016/j.watres.2026.126658 [PM] |
| 101 | High-risk contaminants detected in wastewater effluent samples can be prioritized prior to structural assignment using machine learning tools | 2026 | ML prioritisation pre-identification | unknown contaminants | wastewater effluent samples | P+V | 10.1016/j.watres.2026.126581 [PM] |
| 102 | Decoding microplastic pollution in China freshwater: interpretable machine learning insights into composition-specific distribution and associated phthalate ester leaching risk | 2026 | interpretable ML | microplastics + phthalates | national field dataset | P+V | 10.1016/j.watres.2026.126663 [PM] |
| 103 | Model-driven high-throughput zebrafish embryo assay for evaluating whole effluent toxicity variation across 100 full-scale wastewater treatment plants | 2025 | model-driven HT assay design/analysis | whole effluent | zebrafish embryos + 100 real WWTPs | P+V | 10.1016/j.watres.2025.123675 [PM] |

### 1F. Environmental Health Perspectives

| # | Title | Yr | Method | Pollutant class | Validation | Tag | DOI |
|---|---|---|---|---|---|---|---|
| 104 | Expanded Tox21 Biological Assay Panel for the Prediction of (In Vivo) Toxicity and Cardiotoxicity | 2026 | ML on expanded Tox21 assay panel (DILI, cardiotox) | broad chemicals/drugs | none (uses existing HTS) | P | 10.1021/EHP.6c00052 [PM] |
| 105 | Systematic Evidence Map for the Per- and Polyfluoroalkyl Substances (PFAS) Universe | 2025 | systematic evidence mapping of PFAS data landscape | PFAS (thousands) | none | P | 10.1289/EHP16952 [PM] |
| 106 | Multibehavioral Phenotyping in Early-Life-Stage Zebrafish for Identifying Disruptors of Nonassociative Learning | 2026 | automated multibehavioural phenotyping/analysis | neuroactive chemicals | zebrafish (early life stage) | V-led | 10.1021/EHP.6c00394 [PM] |

> NOTE on EHP: PubMed records for 2026 EHP articles carry `10.1021/EHP.*` DOIs, consistent with EHP having moved to ACS-hosted DOIs; the 2025 record carries the legacy `10.1289/EHP*` prefix. The publishing transition itself was **not independently verified** (ACS/EHP pages blocked).

### Tag proportions

Counted from the table above (n = 106 rows).

| Group | P | P+V | V-led | n |
|---|---|---|---|---|
| ES&T (1A) | 26 | 19 | 19 | 64 |
| ES&T Letters (1B) | 6 | 0 | 0 | 6 |
| **ES&T family (1A+1B)** | **32 (46%)** | **19 (27%)** | **19 (27%)** | **70** |
| Environment International | 4 | 6 | 4 | 14 |
| J Hazard Mater | 4 | 4 | 6 | 14 |
| Water Research | 2 | 3 | 0 | 5 |
| EHP | 2 | 0 | 1 | 3 |
| **All journals** | **44 (42%)** | **32 (30%)** | **30 (28%)** | **106** |

**Caveats on these proportions.** This is a purposive, search-driven sample (PubMed queries combining ML/QSAR/in-silico terms with hazard/toxicity terms), not a random or exhaustive census. It over-samples ES&T 2026 because the query sorted by publication date. The ES&T Letters row is small and all-P, which is a real signal (Letters favours short, self-contained computational screens) but is based on only 6 rows. Use these as order-of-magnitude proportions, not precise rates.

### Are pure-prediction papers getting rarer or more common?

**More common in absolute terms, roughly flat-to-declining as a share.** Verified PubMed counts for `"Environmental science & technology"[Journal] AND (machine learning OR deep learning OR QSAR OR in silico) AND (toxicity OR hazard OR bioactivity)`:

| Year | Papers |
|---|---|
| 2023 | 36 |
| 2024 | 49 |
| 2025 | 53 |
| 2026 (to 13 Nov) | 56 |

So the computational-hazard literature in ES&T has grown ~55% in four years. Qualitatively, what changed is **not** the acceptability of pure prediction but its required form:

- 2023–2024 pure-prediction papers in ES&T were often single-endpoint QSAR/ML models (carcinogenicity QSAR, POD prediction, gene-target prediction).
- 2025–2026 pure-prediction papers that still get in are almost all one of: (a) **chemical-space scale** — 2,649 PFAS, 10,863 PFAS, >350,000 chemicals, >500 antioxidants; (b) **a deployed tool** — MarineTox Predictor, EDC Profiler, web servers; (c) **a regulatory deliverable** — HC5/SSD derivation, REACH QSAR benchmarking, points of departure, PMT mobility; or (d) **methodological self-criticism** — the scaffold-held-out transfer-failure diagnosis, TabPFN robustness under imperfect data.
- The "small curated dataset + off-the-shelf random forest + SHAP plot + no environmental anchor" paper has essentially vanished from ES&T and now lands in JHM/Chemosphere/EES.

---

## 2. What distinguishes prediction papers in ES&T vs JHM / Chemosphere / Ecotoxicol Environ Saf

ES&T's own editorials make the criterion explicit — it is **environmental relevance**, not model performance.

### 2.1 The stated criterion

Lowry G, Field J, Westerhoff P, Zimmerman J, Alvarez P, Boehm A, Crittenden J, Dachs J, Diamond M, Eckelman M, Gardea-Torresdey J, Giammar D, Hofstetter T, Hornbuckle K, Jiang G, Li X-D, Leusch F, Mihelcic J, Miller S, Pruden A, Raskin L, Richardson S, Scheringer M, Schlenk D, Strathmann T, Tao S, Waite TD, Wang P, Wang S. **"Why Was My Paper Rejected without Review?"** *Environ Sci Technol* 2020;54(19):11641–11644. DOI [10.1021/acs.est.0c05784](https://doi.org/10.1021/acs.est.0c05784). PMID 32936617. [PM — Editorial]

Verified from the record itself [CONSENSUS-TEXT]:

> "All papers have a minimum of two prescreen reviews before making a 'Reject Without Review' decision."

> "This 'prescreening' approach prior to peer review provides several benefits to our scientific community, including rapid and informed decisions for authors, and prioritizing only those papers that are considered to be of high quality, and possess both novelty and impactfulness to undergo the peer review process."

From search snippets of the same editorial [SNIPPET-QUOTE — not re-verified]: missing contextualisation of environmental relevance is a primary reason for rejection without review; authors are asked to frame broad environmental implications for both the environmental research and policy communities; and a 20–30 word synopsis is required for research and perspective articles to capture environmental relevance.

### 2.2 The field-specific bar for ecotoxicology (most relevant to this lab)

Schlenk D, Gago-Ferrero P, Leusch FDL, Shi H, Wang B, Zhang X, Mills M. **"Why Was My Manuscript Rejected without Review? Focus on Public Health and Environmental Exposures, Ecotoxicology, and Micro/Nanoplastics."** *Environ Sci Technol* 2025;59(9):4213–4214. DOI [10.1021/acs.est.5c02615](https://doi.org/10.1021/acs.est.5c02615). PMID 40065690. [PM — Editorial]

Verified from the record [CONSENSUS-TEXT]:

> "Selecting which papers move through the initial assessment made by our team of expert Executive and Associate Editors and onto external peer review is based on whether the manuscript contains the basic expectations of quality for a given research field."

> "General guidance for what ES&T is seeking in quality submissions was described in the editorial Why my Paper Was Rejected Without Review and includes fundamental expectations of appropriate scientific rigor, sound experimental setup and reporting, replicate samples, treatment groups and controls, analytical quality assurance/quality control (QA/QC), and other key considerations."

> "However, for a given research topic within the broad umbrella of environmental science and technology there are also quality expectations unique to that particular field. This editorial provides insights into the basic quality expectations for submissions in public health and environmental exposures, ecotoxicology, and micro/nanoplastics research."

> "The journal has a core commitment to remain a thought leader, publishing the latest advances of high novelty that significantly move the field forward in new directions and discoveries."

**This is the single most important document for this lab.** Its author list also identifies the handling editors for ecotoxicology/exposure (see §5).

### 2.3 The "environmental applicability" precedent from materials science

Wang P, Rosario-Ortiz F, Giammar D, He H, Lowry G, Waite D, Westerhoff P, Zimmerman J. **"The Intersection between Materials Science and Environmental Applicability: Defining the Scope of ES&T for Materials-Based Research."** *Environ Sci Technol* 2023;57(33):12135–12136. DOI [10.1021/acs.est.3c06152](https://doi.org/10.1021/acs.est.3c06152). PMID 37605609. [PM — Editorial]

[SNIPPET-QUOTE — not re-verified]: many materials-based submissions rejected without peer review lack this relevance, and the one constant across the journal is the need for authors to demonstrate the relevance of their work **under environmentally relevant conditions**.

This is the direct structural analogue for in-silico work: a new model is to ES&T what a new sorbent is — interesting only once it is demonstrated under environmentally relevant conditions.

### 2.4 The methods-paper bar (applies by analogy to new predictive methods)

Boehm AB, Hsu-Kim H, Arnold WA. **"Essential Elements of Manuscripts Describing New Methods for Measuring Environmental Contaminants at Environmental Science & Technology and Environmental Science & Technology Letters."** *Environ Sci Technol Lett* 2026;13(10):1267–. DOI [10.1021/acs.estlett.6c00742](https://doi.org/10.1021/acs.estlett.6c00742). Published online 13 Aug 2026. [Authors/volume from search snippets — ACS page blocked; treat pagination as PARTIALLY VERIFIED]

[SNIPPET-QUOTE — not re-verified]:

> "Papers describing new or redesigned methods must clearly articulate the scientific innovation of the new approach."

> "These performance criteria should be benchmarked against scientifically accepted methods."

> "Ideally papers submitted to ES&T and ES&T Letters should include a section showing application of the new method to characterize an affected environment with sufficient depth."

> "Authors should address practicality in their work by describing ease of use, costs, and resources (including reagents, instrumentation, and software)."

And from the ACS ES&T Letters author guidelines [SNIPPET-QUOTE — ACS page blocked, not re-verified]:

> "Manuscripts that do not include results from the application of the method either to real environmental samples or to samples that simulate environmental samples in a meaningful manner will be declined."

Mapped onto a prediction paper, the four demands are: (i) say what is genuinely new in the method; (ii) **benchmark against the accepted incumbent** (ECOSAR, TEST, OPERA, VEGA, read-across, a published QSAR); (iii) **apply it to a real environment in depth**, not just a held-out test split; (iv) make it usable.

### 2.5 The six concrete "environmental relevance" hooks, with which papers used them

Derived from the inventory above — these are the observable differentiators between the ES&T set and the JHM/Chemosphere/EES set:

1. **Real occurrence / monitoring data as the prediction substrate.** AI-4-SSD (near-coastal occurrence, #11); Structure-Informed screening of OPCs in human serum (#32); iodinated DBPs by exposome-scale NTA+ML (#39); halogenated nucleosides with a nationwide China survey (#40).
2. **Field samples in the same paper.** Shanghai peri-urban agricultural waterways, 193 sites (#28); AhR agonists in sediments via virtual fractionation (#30); PM2.5 attribution with urban roadside + coastal samples (#50); 100 full-scale WWTPs (#103).
3. **Exposure realism.** Environmentally relevant concentrations (pyraclostrobin 3–18 µg/L, 120 d, #51); human serum/placenta as matrix (#32, #59); bioaccessibility and dietary exposure framing; indoor-relevant conditions for the tear-film MD study (#19).
4. **Regulatory consequence.** HC5/hazardous-concentration derivation (#4); REACH QSAR tool benchmarking to replace the fish early-life-stage test (#21); points of departure (#23); PMT/mobility for drinking-water protection (#12); AOP networks framed for regulatory hazard assessment (#72); China wastewater discharge standards (#41); "guidance of environmental regulations" (#87 — note this one is in JHM, i.e. the claim alone is not sufficient).
5. **Chemical-space scale.** 2,649 PFAS (#65); 10,863 PFAS (#6); >350,000 chemicals (#11); >500 antioxidants (#66); 13 endpoints benchmarked (#1); global neutral organics (#12).
6. **A new class of chemicals.** Novel organophosphate esters (#53); halogenated nucleosides as a new DBP class (#40); liquid crystal monomers (#18); DINCH as a plasticizer substitute (#47); TFA from HFO-1234yf; rubber-dam leachates; 6PPD-Q transformation products.

### 2.6 What the JHM / Chemosphere / EES set looks like instead

From the same searches, the papers that cluster in JHM (and by extension Chemosphere/EES) have a recognisable signature:

- **Network toxicology + molecular docking + a public GEO/CTD dataset, no new chemistry and no occurrence data.** Environment International 2026 is now saturated with this genre: TDCPP/NF-κB microglia (#81), BaP/atrial fibrillation (#82), triclosan/breast cancer with Mendelian randomisation, paraquat/Parkinson's, PFOS/Kawasaki disease, plasticizer/heart-failure toxicogenomics, DABP neurotoxicity (#76). ES&T publishes very few of these, and when it does there is an added environmental anchor (#37, #38).
- **Single-compound zebrafish toxicity with docking as decoration** — spirotetramat, avermectin, etomidate, triclosan, PLA microplastics, medium-chain PFCAs (all JHM 2025–2026).
- **Prioritisation lists for one chemical family with no field or regulatory tie-in** — the liquid crystal monomer cluster (#86, #88, and the LCM chlorination TP paper) is the clearest example: four to five LCM prioritisation papers in JHM within ~18 months.
- **ML applied to an environmental matrix with no hazard endpoint** — groundwater fluoride mapping, PAH soil simulation, microplastic/heavy-metal meta-analysis (JHM 2026).

**Blunt summary of the divide:** JHM/Chemosphere/EES will publish a competent model of a hazard endpoint. ES&T will only publish it if the model changes what someone does about a real environmental problem — a monitoring programme, a regulatory threshold, a chemical substitution decision, or a newly recognised contaminant class.

---

## 3. ES&T-family editorials, perspectives, features and guidance on ML / AI / data science / in silico methods (2022–2026)

All citations below verified in PubMed unless marked otherwise.

### 3.1 The EMBRACE Checklist — the closest thing to a reporting requirement

Zhu J-J, Boehm AB, Ren ZJ. **"Environmental Machine Learning, Baseline Reporting, and Comprehensive Evaluation: The EMBRACE Checklist."** *Environ Sci Technol* 2024;58(45):19909–19912. DOI [10.1021/acs.est.4c09611](https://doi.org/10.1021/acs.est.4c09611). PMID 39469888. [PM — Viewpoint; no abstract in PubMed]

Note the author list: **Alexandria Boehm and Zhiyong Jason Ren are ES&T-family editors**, which is why this Viewpoint functions as quasi-editorial guidance.

Verbatim [CONSENSUS-TEXT — near-full body text retrieved via Consensus]:

> "Given the complexity of ML and the various assumptions and data manipulations often required, it is essential to follow best practices for reporting methods and results from ML applications."

> "In the review of closely examining 148 highly cited environmental ML papers, we found only 24%, 48%, 37%, and 26% of the studies clearly reported their methods for missing data management, feature selection, feature scaling, and hyperparameter optimization, respectively."

> "After publishing the review, we received numerous requests for easy-to-use guidelines to assistant authors, reviewers, and editors to better conceptualize, prepare, conduct, and evaluate ML research."

> "By using the checklist, researchers can ensure that they provide important methodological details, identify critical problems, implement robust and explainable models, and improve the overall quality and impact of their ML research."

> "We encourage researchers using ML methods for environmental applications to utilize the checklist to help report key details of their work."

[SNIPPET-QUOTE] Section structure: "The first section (Section I) guides clear reporting of study objectives. Section IV includes reporting of methods selected and general modeling arrangement." The checklist is described as one that "helps authors, reviewers, editors, and readers conduct, report, and assess ML research."

**Critical nuance — it is NOT mandatory.** The checklist says "we encourage", and a thesis found in the search observed that no journal currently requires its completion. Operationally: completing EMBRACE will not get a paper accepted, but failing its items gives a reviewer a ready-made rejection scaffold. Supporting Information plus a GitHub repository (`starfriend10/EMBRACE`) accompany it.

### 3.2 The companion critical review — the pitfalls list reviewers use

Zhu J-J, Yang M, Ren ZJ. **"Machine Learning in Environmental Research: Common Pitfalls and Best Practices."** *Environ Sci Technol* 2023;57(46):17671–17689. DOI [10.1021/acs.est.3c00026](https://doi.org/10.1021/acs.est.3c00026). PMID 37384597. [PM — Review]

Verbatim from the PubMed abstract:

> "However, due to the lack of familiarity and methodological rigor, inadequate ML studies may lead to spurious conclusions."

> "We identified more than 30 key items and provided evidence-based data analysis based on 148 highly cited research articles to exhibit the misconceptions of terminologies, proper sample size and feature size, data enrichment and feature selection, randomness assessment, data leakage management, data splitting, method selection and comparison, model optimization and evaluation, and model explainability and causality."

> "...we hope to help researchers adopt more rigorous data preprocessing and model development standards for more accurate, robust, and practicable model uses in environmental research and applications."

The named failure modes — **data leakage, data splitting, randomness assessment, model comparison, explainability and causality** — are precisely what the 2026 ES&T transfer-learning paper (#1) operationalises with scaffold-disjoint CV and "strict leakage control". Expect reviewers to ask for scaffold/cluster-based splits rather than random splits.

### 3.3 The ES&T Feature that set the framework

Zhong S, Zhang K, Bagheri M, Burken JG, Gu A, Li B, Ma X, Marrone BL, Ren ZJ, Schrier J, Shi W, Tan H, Wang T, Wang X, Wong BM, Xiao X, Yu X, Zhu J-J, Zhang H. **"Machine Learning: New Ideas and Tools in Environmental Science and Engineering."** *Environ Sci Technol* 2021;55(19):12741–12754. DOI [10.1021/acs.est.1c01339](https://doi.org/10.1021/acs.est.1c01339). PMID 34403250. [PM — Feature]

Verbatim from the abstract — the three-part standard:

> "Next, we introduce the essential knowledge required and current shortcomings in ML applications in ESE, with a focus on three important but often overlooked components when applying ML: correct model development, proper model interpretation, and sound applicability analysis."

"**Sound applicability analysis**" is the applicability-domain requirement. 2021, but it predates the 2022–2026 window only slightly and is the most-cited framing document; the 2026 papers that pass (e.g. #2, with "applicability domain assessment" in the abstract) do this explicitly.

### 3.4 Interpretable computational toxicology

Jia X, Wang T, Zhu H. **"Advancing Computational Toxicology by Interpretable Machine Learning."** *Environ Sci Technol* 2023;57(46):17690–17706. DOI [10.1021/acs.est.3c00653](https://doi.org/10.1021/acs.est.3c00653). PMC10666545. [Verified via PMC record + search; PubMed title search did not resolve]

Theme: ML/DL toxicity models are hard to interpret; the review covers feature data, interpretation methods, knowledge-base frameworks, and applications, with the goal of interpretable models that reveal mechanisms of human toxicity. Note it sits in the **same issue (57:46)** as the Common Pitfalls review and the Data Science editorial — that issue is the data-science special issue and is the single best orientation read.

### 3.5 Generative AI / LLMs

Wu Y, Xu M, Liu S. **"Generative Artificial Intelligence: A New Engine for Advancing Environmental Science and Engineering."** *Environ Sci Technol* 2024;58(40):17524–17528. DOI [10.1021/acs.est.4c07216](https://doi.org/10.1021/acs.est.4c07216). PMID 39342507. [PM — Viewpoint]

[SNIPPET-QUOTE] Current use is "mostly limited to generating training data and specialized chatbots"; prospective areas listed are "Design New Treatment Processes; Develop Environmental Models; Evaluate Environmental Policies". **The piece's specific positions on hallucination, validation and transparency could NOT be verified** (ACS full text blocked). Do not cite it for those claims without reading it.

ES&T is already publishing LLM-based work: Multimodal LLMs for life-cycle inventory extraction (10.1021/acs.est.6c12624), agent-based LLM prioritisation of CECs (#15), and BeeEcoTox's LLM-empowered graph learning (#9). So LLM methods are in scope.

### 3.6 Data-science special-issue editorials (the editors' own statement of what they want)

- Lowry GV, Boehm AB, Brooks BW, Gago-Ferrero P, Jiang G, Jones GD, Liu Q, Ren ZJ, Wang S, Zimmerman J. **"Data Science for Advancing Environmental Science, Engineering, and Technology: Upcoming Special and Virtual Issues in ES&T and ES&T Letters."** *Environ Sci Technol* 2022;56(14):9827–9828. DOI [10.1021/acs.est.2c03735](https://doi.org/10.1021/acs.est.2c03735). PMID 35713615. [PM — Editorial]
- Ren ZJ, Lowry GV, Arnold WA, Brooks BW, Gago-Ferrero P, Garcia JM, Leonard KC, Mills M, Serrano JF, Wang S, Zimmerman JB. **"Data Science for the Transformation of Environmental and Chemical Research and Development."** *Environ Sci Technol* 2022;57(46):17663–17664. DOI [10.1021/acs.est.2c07679](https://doi.org/10.1021/acs.est.2c07679). PMID 36283093. [PM — Editorial]
- Ren ZJ, Lowry GV, Boehm AB, Brooks BW, Gago-Ferrero P, Jiang G, Jones GD, Liu Q, Wang S, Zimmerman JB. **"Data Science for Advancing Environmental Science, Engineering, and Technology."** *Environ Sci Technol* 2023;57(46):17661–17662. DOI [10.1021/acs.est.3c08700](https://doi.org/10.1021/acs.est.3c08700). PMID 38104271. [PM — Editorial] (also appeared in *Environ Sci Technol Lett* 2023;10(11):963–964)

Key requirement sentences [SNIPPET-QUOTE — not re-verified against ACS]:

> "While machine learning (ML) and artificial intelligence (AI) approaches are not inherently mechanistic, they are complementary to traditional deterministic approaches."

> "The future of environmental research aided by ML and AI tools holds great promise, but the success hinges on rigorous and informed application of such tools."

And from the 2022 announcement editorial:

> "Researchers have to go beyond the 'black box' of simple agnostic applications of existing algorithms to determine the 'best one'."

That last sentence is the clearest single statement of what ES&T rejects: algorithm-shopping. The special issue reportedly contains over 90 articles.

### 3.7 Other relevant ES&T perspectives in window

- **"Perspectives on Advancing Multimodal Learning in Environmental Science and Engineering Studies."** *Environ Sci Technol* 2024. DOI [10.1021/acs.est.4c03088](https://doi.org/10.1021/acs.est.4c03088). PMID 39226136. [PM — Review/Perspective]
- **"Application of Machine Learning in Nanotoxicology: A Critical Review and Perspective."** *Environ Sci Technol* 2024. DOI [10.1021/acs.est.4c03328](https://doi.org/10.1021/acs.est.4c03328). PMID 39109992. [PM]
- **"Bringing Artificial Intelligence (AI) into Environmental Toxicology Studies: A Perspective of AI-Enabled Zebrafish High-Throughput Screening."** *Environ Sci Technol* 2024. DOI [10.1021/acs.est.4c00480](https://doi.org/10.1021/acs.est.4c00480). PMID 38691763. [PM — Review/Perspective] — **directly on this lab's intended niche.** Abstract notes that in zebrafish toxicology studies "the microscopic images and videos" are the data AI can exploit.
- **"Missing Genomic Resources for the Next Generation of Environmental Risk Assessment."** *Environ Sci Technol* 2024. DOI [10.1021/acs.est.3c08701](https://doi.org/10.1021/acs.est.3c08701). PMID 38245867. [PM]
- **"Exploiting Omic Data to Advance Predictive Ecotoxicology."** *Environ Sci Technol* 2026. DOI [10.1021/acs.est.6c01198](https://doi.org/10.1021/acs.est.6c01198). PMID 42689779. [PM — Review] — states the ambition directly: "Predicting species-specific chemical sensitivity using in silico approaches has the potential to transform environmental risk assessment, conservation, and biomonitoring, while reducing, and ultimately replacing, animal testing."
- **"Harnessing Machine Learning to Enhance UV-based Advanced Oxidation Processes for Sustainable Micropollutant Abatement."** *Environ Sci Technol* 2026. DOI [10.1021/acs.est.6c00957](https://doi.org/10.1021/acs.est.6c00957). PMID 42689806. [PM — Review]
- **"Future Directions in Protein Affinity Selection-Mass Spectrometry for High-Throughput Protein-Ligand Recognition."** *Environ Sci Technol* 2026. DOI [10.1021/acs.est.6c03677](https://doi.org/10.1021/acs.est.6c03677). PMID 42689815. [PM — Review] — frames the problem this lab is in: "The rapid proliferation of synthetic chemicals has far outpaced the ability of traditional toxicological methods, underscoring the urgent need for efficient strategies to identify bioactive contaminants."
- **"FAIR and Effective Communication of Data on Chemical Contaminant Biotransformation in the Environment."** *Environ Sci Technol Lett* 2025. DOI [10.1021/acs.estlett.5c00753](https://doi.org/10.1021/acs.estlett.5c00753). PMID 41246183. [PM — Review] — the FAIR-data position piece for prediction-relevant datasets.

### 3.8 ACS ES&T Water and ACS ES&T Air

- **ACS ES&T Water** ran a Special Issue "Applications of Artificial Intelligence, Machine Learning, and Data Analytics in Water Environments", guest-edited by **Jacqueline MacDonald Gibson (NC State)** and **Carla Ng (University of Pittsburgh)**; submissions closed 31 March 2023; listed scope explicitly included "QSAR development". An introductory editorial exists at DOI 10.1021/acsestwater.4c00140 — **author list and exact title UNVERIFIED** (ACS page blocked).
- **ACS ES&T Air** published an editorial introducing "Artificial Intelligence and Machine Learning in Atmospheric Chemistry", *ACS ES&T Air* 2024;1(5):330, with a cross-journal ES&T collection. **Authors UNVERIFIED.**
- An ACS **virtual issue** "AI/Machine Learning in Environmental Science and Technology" spans ES&T, ES&T Letters and ACS Sustainable Chemistry & Engineering, introduced by an editorial from the curating Topic Editors and Associate Editors. **Date and editor names UNVERIFIED.**

### 3.9 ACS-wide AI/LLM policy (applies to ES&T submissions)

[SNIPPET-QUOTE from ACS publisher pages — `researcher-resources.acs.org` was blocked for direct verification]:

> "Artificial intelligence (AI) tools do not qualify for authorship. Such tools can neither take responsibility for published content, nor can they assent to co-authorship."

> "Authors must disclose the use of generative AI tools to create or substantially modify text, permitted images and figures, or other submission content. More extensive use of generative AI must be described in the Methods section or another appropriate section of the manuscript."

> "The authors of the work are responsible for all submitted content and agree upon submission that generated content from AI tools is appropriate, both scientifically and based on the ACS Ethical Guidelines to Publication of Chemical Research."

> "Editors remain responsible for all editorial assessments and decisions and must not delegate editorial judgment or decision-making to a generative AI tool. Similarly, peer reviewers remain responsible for all comments and recommendations provided during peer review and must not use generative AI tools to generate, draft, or revise their peer review reports."

ACS ES&T Air states more strongly [SNIPPET-QUOTE]: "The use of generative Artificial Intelligence (AI) to generate an external peer review is viewed as an ethical violation as it contravenes the ACS policy of full confidentiality in the peer review process."

**A third-party blog (manusights.com) claims ES&T prohibits AI-generated figures representing original research data, and that desk rejections run 30–40%. Neither claim could be confirmed against ACS sources. Treat both as UNVERIFIED.**

### 3.10 What was NOT found

- **No ES&T editorial that mandates data or code deposition for ML papers.** EMBRACE is voluntary. By contrast, a 2026 editorial in *Environmental Geochemistry and Health* (DOI 10.1007/s10653-026-03324-3, a different publisher) reportedly requires full training/validation/test datasets plus analysis code at submission and rejects "available on reasonable request" statements, returning non-compliant submissions without peer review [SNIPPET-QUOTE]. ES&T has not gone this far — **yet**. Expect it to.
- No ES&T/ES&T Letters/ACS ES&T Water editorial specifically on NAMs or 21st-century toxicology was found in 2022–2026.

---

## 4. Prediction + zebrafish: crowded niches to avoid, and open ground

### 4.1 Scale of the crowding

PubMed: `zebrafish AND (machine learning OR deep learning OR QSAR OR molecular docking OR in silico OR network toxicology)` restricted to ES&T, ES&T Letters, Environment International, J Hazard Mater and Water Research, 2023–2026 → **118 papers**. This is a saturated space.

### 4.2 Already done — do not repeat

**(a) The zebrafish-image / phenotype deep-learning pipeline itself is taken, twice over, in ES&T.**
- "Deep Learning-Enabled Morphometric Analysis for Toxicity Screening Using Zebrafish Larvae", *ES&T* 2023, DOI 10.1021/acs.est.3c00593 [PM]
- "Deep Learning-Enabled Unbiased Precision Toxicity Assessment of Zebrafish Organ Development", *ES&T* 2025, DOI 10.1021/acs.est.5c10763 [PM]
- Plus the agenda-setting perspective: "Bringing AI into Environmental Toxicology Studies: A Perspective of AI-Enabled Zebrafish High-Throughput Screening", *ES&T* 2024, DOI 10.1021/acs.est.4c00480 [PM]
- And in EHP: "Multibehavioral Phenotyping in Early-Life-Stage Zebrafish for Identifying Disruptors of Nonassociative Learning", 2026, DOI 10.1021/EHP.6c00394 [PM]
→ A new "we built a CNN to score zebrafish malformations" paper will not land in ES&T.

**(b) AOP / network-toxicology + zebrafish confirmation in ES&T is now a filled template.**
- "AOP-Guided Toxicogenomic Mapping Profiles for Mechanism-Informed Toxicity Pattern Prediction in Zebrafish", *ES&T* 2026, DOI 10.1021/acs.est.6c01532 [PM]
- "Network-Based Assessment of Environmental Neurotoxicants Using High-Throughput Transcriptomics in Zebrafish Embryos", *ES&T* 2026, DOI 10.1021/acs.est.5c11994 [PM]
- "Mechanistic Prediction and High-Throughput Risk Screening of Aquatic Contaminants Using Daphnia magna AOP Network", *ES&T* 2026, DOI 10.1021/acs.est.6c06646 [PM] (same template, Daphnia)

**(c) Specific chemical classes where prediction + fish in vivo is saturated:**

| Chemical class | Status | Representative papers |
|---|---|---|
| **6PPD / 6PPD-quinone** | Extremely crowded | ES&T 2024 zebrafish eye/thyroid (4c11264); ES&T 2026 MASLD (6c05547); JHM 2026 male reproductive (144194); JHM 2026 apo-transferrin/ferroptosis (143315); Environ Int 2026 computational hazard ID (110334) |
| **Liquid crystal monomers** | Extremely crowded | ES&T 2026 PI3K/Akt multitarget (6c00371); JHM 2025 DL priority list (140362); JHM 2025 RNA-seq+DL (140465); JHM 2026 PPARγ prioritisation (144178); JHM 2026 cross-species sediments (141880); JHM 2025 chlorination TPs |
| **Organophosphate esters / flame retardants** | Crowded | ES&T 2026 qMOA OPFRs (6c01412); ES&T 2026 TDtBPP neurodevelopment (6c07562); Environ Int 2026 TPHP/ESR1 (110458); Environ Int 2026 TPhP dopaminergic (110320); Environ Int 2026 TDCPP/NF-κB (110373) |
| **DBPs (incl. halobenzoquinones, nitrophenols)** | Crowded | ES&T 2026 2,6-DCBQ network toxicology + in vivo (6c11071); ES&T 2026 halogenated nitrophenols/medaka (6c06184); ES&T 2026 halogenated nucleosides + QSAR (6c07375); JHM 2025 MLSE DBP screening (140069); Water Res 2026 ML + network toxicology DBPs (126658) |
| **PFAS + fish/neurodevelopment** | Crowded | ES&T 2026 10,863-PFAS NOEC (5c17531); ESTL 2026 2,649-PFAS QSAR+docking (6c00172); JHM 2026 reverse docking folate receptor (142012); JHM 2025 medium-chain PFCAs/AR |
| **Isothiazolinones / DCOIT** | Crowded | ES&T 2024 isothiazolinone GPCR (3c08577); ES&T 2024 DCOIT thyroid (4c07614); ES&T 2026 DCOIT eye-lens AOP (6c00969) |
| **Synthetic antioxidants (BHT, antioxidant TPs)** | Filling fast | ES&T 2026 BHT/β2-adrenergic zebrafish (6c04202); ESTL 2026 hazard assessment of >500 antioxidants (5c01217); ES&T 2026 novel OPEs from antioxidant transformation (6c12069) |
| **Triclosan, benzothiazoles, pesticides (single-compound zebrafish)** | Crowded in JHM, not ES&T-viable | JHM 2026 triclosan cardiac (143189); JHM 2026 benzothiazoles visual (143464); JHM 2026 spirotetramat; Environ Int 2025 741-pesticide cardiotoxicity ML |

### 4.3 Open niches (gaps visible in the corpus)

These are **inferred gaps from the searches performed** — absence of evidence in this sample, not proof of absence. Each should be novelty-checked before committing.

1. **Prospective, blinded, pre-registered prediction→zebrafish validation.** Every P+V paper found validated chemicals the model had already flagged, post hoc. Nothing found that pre-registers predictions, then tests them blind, and reports the hit rate including failures. The ES&T 2026 transfer-failure paper (#1) shows the journal now rewards honest negative methodological results. A "our model predicted 40 compounds, we tested 40 blind, here is the confusion matrix" paper would be genuinely new and directly answers the benchmarking demand in §2.4.
2. **Zebrafish validation anchored to real environmental mixtures rather than single compounds.** The field-anchored prediction papers (#28, #30, #41, #103) use C. elegans, in vitro AhR, or effluent-level zebrafish endpoints. A prediction model that prioritises constituents of a real field extract and then confirms the specific predicted constituents in zebrafish — effect-directed analysis closed by in silico prioritisation — appears unoccupied for most matrices.
3. **Cross-species extrapolation validated in zebrafish.** ES&T 2026 published cross-species ERα work in mammals (#33) and species-specific sensitivity ambitions (§3.7, "Exploiting Omic Data"), and ESTL published a marine/freshwater transfer model (#7). Using zebrafish as the experimental anchor for a genome-informed cross-species sensitivity prediction — predict which species' receptor variants are sensitive, then test the zebrafish ortholog — is an explicitly stated field ambition with no paper found delivering it.
4. **Chemical classes with occurrence data but no predictive-toxicology treatment.** From the ES&T 2026 occurrence literature: rubber-dam leachates (10.1021/acs.est.6c05884), brominated additives released from microplastics in soil (6c05830), fermented-food PFAS bioaccessibility (5c15723), TFA from HFO-1234yf refrigerant transition (estlett.6c00356), gas-phase atmospheric chemicals on XAD passive samplers (6c07599), and neutral adipose-partitioning PFAS (6c01695). Each has fresh occurrence data and no prediction+in vivo paper found.
5. **Behavioural / functional endpoints beyond morphology.** The DL work is on morphometrics and organ development. Prediction of behavioural or electrophysiological endpoints is thinner — ES&T 2026 did 3D earthworm burrowing with DL (#55) and EHP 2026 did zebrafish nonassociative learning (#106), but a predictive model targeting a behavioural endpoint and validated in zebrafish behaviour was not found.
6. **Negative/failure reporting and applicability-domain honesty for in-vivo-anchored models.** No paper found reports where its in silico prioritisation failed against the in vivo result. Given §3.2's emphasis on data leakage and §3.1's on rigour, this is a defensible ES&T contribution in itself.
7. **Mixture-toxicity prediction validated in a vertebrate.** Environment International has mixture work with in vitro validation (#74) and ES&T has mixture prediction for rare earth ions in cells (#29). Vertebrate-anchored mixture prediction at environmentally realistic ratios was not found.

---

## 5. Editors, associate editors and special issues

### 5.1 Editors (what is verifiable without the ACS masthead)

**The ACS masthead page could not be opened (`pubs.acs.org` blocked).** The following is inferred from verified authorship of ES&T editorials, where editorial authorship is itself strong evidence of an editorial role. **Roles are inferred, not confirmed from a masthead.**

From the 2025 ecotoxicology/exposure desk-rejection editorial (DOI 10.1021/acs.est.5c02615, PMID 40065690) — these are the people who prescreen ecotoxicology and exposure submissions:

| Name | Affiliation (from PubMed) | Inferred remit |
|---|---|---|
| **Daniel Schlenk** | Aquatic Ecotoxicology and Environmental Toxicology, University of California, Riverside | Ecotoxicology / environmental toxicology — **most likely handling editor for this lab's work** |
| **Frederic D. L. Leusch** | Griffith University, Gold Coast | Ecotoxicology, bioanalytical tools / effect-based methods |
| **Pablo Gago-Ferrero** | IDAEA-CSIC, Barcelona | Environmental analytical chemistry, NTA |
| **Xiaowei Zhang** | School of Ecology and Environmental Science, Yunnan University | Toxicogenomics / ecotoxicogenomics |
| **Bin Wang** | Peking University | Public health and environmental exposures |
| **Huahong Shi** | East China Normal University | Micro/nanoplastics |
| **Margaret Mills** | (ACS) | Managing editor |

From the data-science editorials (DOIs 10.1021/acs.est.2c03735, 2c07679, 3c08700) — the ES&T-family editors who own the data-science/ML remit:

**Zhiyong Jason Ren** (Princeton), **Gregory V. Lowry** (Carnegie Mellon), **Alexandria B. Boehm** (Stanford), **Bryan W. Brooks** (Baylor), **Gerrad D. Jones** (Oregon State), **Qian Liu**, **Shuxiao Wang** (Tsinghua), **Guibin Jiang** (RCEES), **Julie B. Zimmerman** (Yale), **William A. Arnold** (Minnesota), **Heileen Hsu-Kim** (Duke), **Kevin C. Leonard**, **Jeannette M. Garcia**, **Pablo Gago-Ferrero**.

Notes: Ren, Lowry, Boehm and Zimmerman recur across the ML/data-science editorials and the rejection-criteria editorial, so they set this policy. Boehm, Hsu-Kim and Arnold authored the 2026 methods-manuscript editorial. Guibin Jiang was publicly recognised by ES&T as a long-standing associate editor [SNIPPET-QUOTE, ES&T journal page]. **Jun-Jie Zhu** (Princeton) is the lead author on both the EMBRACE checklist and the Common Pitfalls review — not an editor as far as could be verified, but the de facto standards author for environmental ML; cite him.

**Not discoverable in this session:** a current ES&T masthead, which Associate Editor formally holds "computational toxicology" or "machine learning", and the ACS ES&T Water / ES&T Air editorial boards.

### 5.2 Special issues and calls for papers

**Verified:**
- **ES&T + ES&T Letters joint Special Issue, "Data Science for Advancing Environmental Science, Engineering, and Technology."** Announced 2022 (DOI 10.1021/acs.est.2c03735); submission deadline was **12 January 2023** [SNIPPET-QUOTE from the ACS Axial call]; introduced by editorials in *ES&T* 57(46):17661–17662 and *ES&T Lett* 10(11):963–964. Reportedly >90 articles. **Closed.** ES&T 57(46) is the key issue to read.
- **ACS ES&T Water Special Issue, "Applications of Artificial Intelligence, Machine Learning, and Data Analytics in Water Environments."** Guest editors Jacqueline MacDonald Gibson (NC State) and Carla Ng (Univ. Pittsburgh); deadline **31 March 2023**; scope included QSAR development. **Closed.**
- **ACS ES&T Air collection, "Artificial Intelligence and Machine Learning in Atmospheric Chemistry"** (editorial *ACS ES&T Air* 2024;1(5):330), cross-listed with ES&T.
- **ACS Virtual Issue "AI/Machine Learning in Environmental Science and Technology"** spanning ES&T, ES&T Letters, ACS Sustainable Chem & Eng.
- **Environment & Health** (ACS, journal code ehnea2) published "Artificial Intelligence and Machine Learning for Environmental Health Study", 2025;3(10):1115, with an associated virtual special issue. **Authors UNVERIFIED.**

**Searched for and NOT found:** any open (as of Nov 2026) call for papers on AI/ML, new approach methodologies (NAMs) or 21st-century toxicology in ES&T, ES&T Letters, ACS ES&T Water, Environment International or EHP. The only open ACS environmental-family call surfaced was "Critical Minerals and Sustainable Energy Innovation" (deadline 1 June 2027), which is off-topic. The AI-related open ACS call found was ACS Applied Bio Materials / ACS Pharmacology & Translational Science on AI in biomaterials (through 30 November 2026) — wrong journals.

Practical read: there is **no AI/NAMs special issue to aim at right now**. The data-science special issues all closed in 2023. Submit to the regular ES&T stream and let the environmental hook, not an AI framing, carry the paper.

---

## 6. Bottom line: what now gets a prediction paper rejected from ES&T

1. **No environmental anchor.** A model trained on a public toxicity database, validated on a random split, with no occurrence data, no field samples, no regulatory output and no new chemical class. Desk-rejected on environmental relevance (§3.1).
2. **Algorithm-shopping.** Comparing eight algorithms to find "the best one" is explicitly named as insufficient: "Researchers have to go beyond the 'black box' of simple agnostic applications of existing algorithms to determine the 'best one'."
3. **Random train/test splits and leakage.** §3.2 names data leakage and data splitting among >30 pitfalls; ES&T 2026 now publishes scaffold-disjoint, leakage-controlled benchmarks. A random split on a congeneric dataset reads as inflated.
4. **No applicability domain.** "Sound applicability analysis" has been a stated ES&T requirement since 2021 (§3.3), and the 2026 papers that pass state it explicitly.
5. **No benchmark against the accepted incumbent.** "These performance criteria should be benchmarked against scientifically accepted methods" (§2.4). A model that is not compared to ECOSAR/TEST/OPERA/read-across has no demonstrated value.
6. **Network toxicology + docking on public data.** This genre has moved to Environment International and JHM. In ES&T it needs occurrence data, field samples, or a new contaminant class attached (cf. #37, #38).
7. **A CNN for zebrafish phenotypes.** Done in ES&T 2023 and 2025 (§4.2a). Novelty exhausted.
8. **One more compound in a saturated class.** Another 6PPD-Q or liquid-crystal-monomer paper needs an exceptional hook (§4.2c).
9. **Weak experimental design in the validation arm.** The ecotoxicology editorial requires "replicate samples, treatment groups and controls, analytical quality assurance/quality control (QA/QC)" (§2.2). A thin zebrafish arm bolted onto a strong model fails on the experimental side — and n=1 exposures, no measured exposure concentrations, or no positive control will sink it.
10. **Missing synopsis / implications framing.** A 20–30 word synopsis capturing environmental relevance is required, and implications must be framed for research **and policy** communities (§3.1).

### Strategic recommendation

Lead with the environmental problem, not the model. The ES&T-viable shape of this lab's paper is: *a named, environmentally occurring chemical class with fresh occurrence or field data → a prediction method with a stated applicability domain, scaffold-aware validation and a benchmark against the incumbent → prospective, blind zebrafish confirmation reported with failures included → an explicit regulatory or substitution consequence.* Open niche 1 (prospective blinded validation) combined with open niche 4 (an occurrence-rich, prediction-poor class) is the highest-value, lowest-duplication combination visible in this corpus.
