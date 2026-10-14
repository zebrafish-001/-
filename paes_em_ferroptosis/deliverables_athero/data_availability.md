# 数据与方法可用性 (真实数据)

## 转录组 (GEO)
- 训练集 GSE100927 (GPL17077): 69 动脉粥样硬化动脉 vs 35 对照, 30558 基因
- 验证集 GSE28829 (GPL570): 16 晚期 vs 13 早期颈动脉斑块
- 验证集 GSE43292 (GPL6244): 32 斑块 vs 32 配对正常内膜
- 单细胞 GSE159677: 3 患者 x (钙化核心+邻近), 49562 细胞过滤后

## 靶点与基因集
- 增塑剂靶点: ChEMBL 43 + CTD 2596 = 2624 (12 化合物)
- 疾病靶点: OpenTargets MONDO_0005311 (625) + KEGG hsa05417 (216) = 820
- 铁死亡基因: FerrDb ferroptosis preview (to 2023-12-31), Confidence=Validated, driver+suppressor+marker, HGNC-validated = 983
- 注释集: Enrichr GO/KEGG 7348 条目
- 免疫签名: Charoentong 2017 Table S6 28 细胞型

## 分子对接 (AutoDock Vina, 受体 CD36 5LGD A 链)
- DINCH: -7.25 kcal/mol
- BBP: -7.072 kcal/mol
- DINP: -7.065 kcal/mol
- DIBP: -6.375 kcal/mol
- DEHT: -6.322 kcal/mol
- DEHP: -6.232 kcal/mol
- TOTM: -6.215 kcal/mol
- DBP: -6.096 kcal/mol
- DEHA: -6.071 kcal/mol
- DMP: -5.884 kcal/mol
- DEP: -5.862 kcal/mol
- ATBC: -5.506 kcal/mol