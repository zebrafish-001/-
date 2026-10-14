# Plasticizers (7 PAEs + 5 alternatives) → 铁死亡 → Atherosclerosis (AS) 网络毒理学与多组学分析报告

- 流程: paes-em-ferroptosis v0.1 (真实数据)
- 生成时间: 2026-10-14
- 方法学参照: Wang et al., J Hazard Mater 2026;507:141670 (doi:10.1016/j.jhazmat.2026.141670)

## 1. 网络毒理学靶点交集
- 增塑剂靶点 2624 个; AS 靶点 820 个; 铁死亡基因 983 个
- 三重交集 **40** 个基因: AKT1, ANGPTL4, ATF4, BCL2, CD36, CDKN1A, CDKN2A, CKB, CXCL8, ERN1, ESR1, FEN1, GDF15, GSK3B, IL1B …

## 2. 差异表达 (limma 式 moderated t)
- 训练集 GSE100927: DEG 2587 个 (上调 1579 / 下调 1008)

## 3. WGCNA
- 引擎 python-lite, 软阈值 β=6, 检出模块 15 个, 表型显著模块基因 2500 个

## 4. 功能富集
- 显著条目 1551 个: KEGG::Lipid and atherosclerosis; KEGG::Hepatitis B; KEGG::Human cytomegalovirus infection; KEGG::Pathways in cancer; KEGG::AGE-RAGE signaling pathway in diabetic complications

## 5. 机器学习关键基因
- 12 算法 10 折交叉验证, 最优: random_forest (AUC 1.0), extra_trees (AUC 1.0), ridge (AUC 1.0)
- RF ∩ Lasso ∩ XGBoost 共识关键基因: **CD36**
- 验证集单基因 AUC: {"GSE28829": {"TNF": 0.4014, "CD36": 0.7067, "CDKN2A": 0.7115, "IL1B": 0.7067, "CKB": 0.1106}, "GSE43292": {"TNF": 0.7803, "CD36": 0.7988, "CDKN2A": 0.6602, "IL1B": 0.7178, "CKB": 0.4121}}

## 6. 免疫浸润 (ssGSEA, 28 细胞型)
- 组间差异细胞型 28 个; 与 CD36 显著相关 28 个

## 7. 单细胞分析
- 引擎 scanpy, 细胞 49562, 20 个细胞亚型
- CD36 在病变 vs 正常组: 0.28 vs 0.14 (P=0.00e+00)
- CD36 与干性相关 ρ=0.354; 沿 Resident-like → Foam-like 轨迹伪时间 ρ=0.445 (P=0.00e+00)

## 8. 空间转录组
- 本终点无可用的公共空间转录组原始计数数据, 该阶段跳过

## 9. 虚拟敲除 (Macrophage)
- 敲除 CD36, GRN 网络基因 3285 个; 高扰动基因: SPP1, SLAMF9, CD52, MARCO, FABP5, CSTB
- 铁死亡基因在高扰动集中富集 P=0.881 (不显著; lite GRN 的局限, 建议用 scTenifoldKnk R 包复核)
- 扰动基因富集通路: KEGG::Systemic lupus erythematosus; KEGG::Staphylococcus aureus infection; GO_CC::Collagen-Containing Extracellular Matrix

## 10. 分子对接
- 受体 5LGD, 阈值 -5.0 kcal/mol, 强结合 12/12
- 结合能: {"DEHP": -6.232, "DBP": -6.096, "BBP": -7.072, "DEP": -5.862, "DMP": -5.884, "DIBP": -6.375, "DINP": -7.065, "DEHT": -6.322, "DINCH": -7.25, "DEHA": -6.071, "ATBC": -5.506, "TOTM": -6.215}

## 11. 实验验证设计 (湿实验, 不由本流程执行)
- CEA plaque vs control artery specimens (>=5+5): IHC/IF of CD36,
- co-staining with CD68 (macrophage) and ACTA2 (SMC)
- Cell assays: ox-LDL macrophage/VSMC + DEHP/DBP gradient, +/- Fer-1;
- readouts: lipid ROS (C11-BODIPY), MDA/GSH, Fe2+, WB of GPX4/ACSL4/CD36
- Optional in vivo: high-fat zebrafish or ApoE-/- mice under plasticizer
- exposure; vascular lipid deposition + ferroptosis markers

## 结论轴
**Plasticizers (7 PAEs + 5 alternatives) 暴露 → 铁死亡相关基因 CD36 上调 → 免疫微环境扰动 → Resident-like → Foam-like 细胞状态转换 → Atherosclerosis (AS)**

## 图表
- fig01_workflow.png
- fig02_targets_de.png
- fig03_intersection_genes.png
- fig04_ml_benchmark.png
- fig05_ml_models.png
- fig06_immune.png
- fig07_singlecell.png
- fig08_stemness_trajectory.png
- fig10_knockout.png
- fig11_docking.png