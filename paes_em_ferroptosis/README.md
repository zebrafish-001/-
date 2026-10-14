# paes-em-ferroptosis — 邻苯二甲酸酯 → 铁死亡 → EMT → 子宫内膜异位症 分析流程

可复现的多组学分析流水线，方法学参照：

> Wang H, Wu F, Li Y, Chen H, Wang X, Sun Z, Gu N, Zhu Y.
> *Mechanism study of phthalate exposure promoting endometriosis: Based on
> the ferroptosis perspective.* **J Hazard Mater**. 2026;507:141670.
> doi: [10.1016/j.jhazmat.2026.141670](https://doi.org/10.1016/j.jhazmat.2026.141670) (PMID 41791190)

流程把论文的"网络毒理学 + bulk 转录组 + 机器学习 + 免疫浸润 + 单细胞 +
空间转录组 + 虚拟敲除 + 分子对接"工作流拆成 12 个可独立运行的阶段，
暴露物 / 疾病 / 背景基因集全部由 `config/pipeline.yaml` 配置，
因此同一套代码可迁移到其他"环境暴露物 X 疾病 X 机制基因集"课题。

## 快速开始（合成数据演示）

```bash
python -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/paes-em run-all --demo        # 全流程, 约 30 秒
.venv/bin/python -m pytest -q           # 端到端 + 单元测试
```

演示模式生成带"已知答案"的合成数据（ARF6 被种植为交集基因、DEG、
ML 共识关键基因、EMT 轴高表达基因），跑通后在
`data/results/report.md` / `report.html` 得到按论文叙事组织的报告。

## 12 个阶段

| # | 阶段 | 论文方法 | 本流程实现 |
|---|------|----------|-----------|
| 1 | intake | GEO 表达谱读入 QC | CSV 读入, log2 启发式转换 |
| 2 | network_tox | PubChem/ChEMBL/CTD/PharmMapper/SwissTarget + GeneCards/TTD/DrugBank/OMIM + FerrDb, UniProt 标准化 | 三方靶点 JSON 交集 |
| 3 | diffexp | limma | Python 版 moderated t (eBayes 方差收缩); `R/limma_de.R` 为精确 limma 钩子 |
| 4 | wgcna | WGCNA | `R/wgcna.R` 钩子; python-lite: soft-power 选择 + TOM + 层次聚类模块 + 模块-表型相关 |
| 5 | enrich | clusterProfiler GO/KEGG | 超几何 ORA + BH; R 钩子可换 clusterProfiler |
| 6 | ml | 12 算法 82 组合 10 折 CV, RF+Lasso+XGBoost 共识 → ARF6 | sklearn 12 算法基准 + 三选择器共识 + 验证集单基因 AUC |
| 7 | immune | ssGSEA 28 免疫细胞 + Wilcoxon + 相关 | 纯 Python ssGSEA (Barbie 2009) |
| 8 | singlecell | Seurat + CytoTRACE + Monocle2 | `R/singlecell.R` 钩子; lite: PCA/k-means 注释 + 干性代理 + PCA 伪时间 |
| 9 | spatial | SCTransform + RCTD + SpatialFeaturePlot | `R/rctd.R` 钩子; lite: marker 软反卷积 + 病灶富集检验 + matplotlib 空间图 |
| 10 | knockout | scTenifoldKnk 成纤维细胞虚拟敲除 | `R/sctenifoldknk.R` 钩子; lite: 相关 GRN + 敲除扰动传播 + FRG 富集 |
| 11 | docking | AutoDock Vina, ARF6 (PDB 2A5D), <-5.0 kcal/mol | 有 vina 即真跑; 否则解析 Vina 日志; 自动生成完整对接协议脚本 |
| 12 | report | — | 汇总所有阶段 → Markdown/HTML 报告 (+ 湿实验 IHC/IF 验证设计说明) |

单独跑某几步：

```bash
paes-em run --stages intake,network_tox,diffexp,ml
paes-em stages      # 列出全部阶段
```

## 真实数据获取

把下列文件放入 `data/raw/` 后去掉 `--demo` 运行：

1. **转录组** `GSE51981/GSE7305/GSE7846`：用 GEOparse / GEOquery 下载，
   导出为 `<ACC>_expr.csv`（基因 x 样本）与 `<ACC>_pheno.csv`
   （`sample,group`，group ∈ {EM, Control}）。
2. **靶点列表**（UniProt 标准化后的 HGNC symbol JSON 数组）：
   - `paes_targets.json` — 7 种 PAEs（配置里含 PubChem CID）在
     ChEMBL / CTD / PharmMapper / SwissTargetPrediction 的靶点并集；
   - `em_targets.json` — GeneCards / TTD / DrugBank / OMIM 的 EM 靶点；
   - `frgs_ferrdb.json` — FerrDb driver+suppressor+marker 去重（论文 471 个）。
3. **注释基因集** `annotation_gene_sets.json`：`"库::条目" -> [genes]`，
   可由 MSigDB GMT 转换（GO/KEGG）。
4. **免疫签名** `immune_signatures_28.json`：Charoentong 等 28 细胞型签名。
5. **单细胞 / 空间**：`sc_counts.csv`、`sc_meta.csv`、`spatial_counts.csv`、
   `spatial_coords.csv`（真实跑建议直接走 R 钩子用 Seurat 对象）。
6. **对接**：装好 AutoDock Vina 后按 `data/results/s11_docking_protocol.sh`
   准备受体 (PDB 2A5D) 与配体并运行；或把现成 Vina 日志放
   `data/raw/vina_logs/<化合物>_2A5D.log`。

## Python-lite 与 R 钩子

每个重计算阶段都有两档引擎：**python-lite**（零 R 依赖，原理同源，
适合联调与演示）与 **R 钩子**（`R/*.R`，调用 limma / WGCNA / Seurat /
CytoTRACE / Monocle2 / spacexr(RCTD) / scTenifoldKnk 原包，发表级结果用
这一档）。检测到 `Rscript` 且非 demo 模式时自动优先走 R 钩子，失败即
回退 lite 并在结果 JSON 标明 `engine`。

## 已知限制

- lite 引擎是方法学近似（如 CytoTRACE 代理、相关网络版虚拟敲除），
  结论级分析请用 R 钩子跑原包。
- 真实 GEO/数据库下载、探针-基因映射、批次校正需用户按上节准备。
- 第 11 阶段的湿实验（IHC/IF, 伦理批准）超出计算流程范围，报告中仅
  给出设计说明。
