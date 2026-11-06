# Daniel L. Villeneuve（Dan Villeneuve）— US EPA Duluth 深蒸馏档案

> 档案编号：PLAN D24。建档日期 2026-11-06。证据纪律：下列论文均来自本次 PubMed（get_article_metadata）或 JRC/AOP-Wiki/data.gov 实际返回；未能核实处标 `⚠️待核实`。
> 同名排除：Claude Villeneuve（加拿大魁北克生物学家/学者，2024 年去世，与 AOP 无关）——非本人。PubMed 检索式 `Villeneuve DL[Author]` 2023–2026 命中 46 条，抽查作者单位均为 US EPA Duluth 或其合作团队；其他同姓缩写（如 D. Villeneuve 在非毒理领域）未发现混入，但未逐条核对全部 46 条的署名位次 ⚠️待核实。

## 1. 基本信息
- **单位**：US EPA，ORD / Center for Computational Toxicology and Exposure（CCTE）下属 Great Lakes Toxicology and Ecology Division（GLTED），Duluth, MN（早年为 Mid-Continent Ecology Division, MED）。2025–2026 发表论文中同团队成员（Flynn）署名已出现 "Office of Chemical Safety and Pollution Prevention（OCSPP）, Risk Assessment Support Division, Duluth"，提示 EPA 2025 年重组后部分人员归属变化；Villeneuve 本人现单位 ⚠️待核实。
- **头衔**：Research Toxicologist（EPA Science Matters 页面："research toxicologist at EPA's MED in Duluth"）。学历：Michigan State University 博士，Oregon State University 博士后，2004 年以 NRC postdoc 加入 EPA（EPA Science Matters 页面，epa.gov/node/74083）。
- **邮箱**：villeneuve.dan@epa.gov（2014 论文通讯信息核实）。
- **方向标签**：AOP 框架与 AOP-Wiki；生态高通量转录组学与 tPOD；黑头呆鱼（fathead minnow）内分泌/生殖毒理；NAM 驱动的生态危害筛查与优先级排序；五大湖污染物优先排序。
- **关联**：长期与 Gerald T. Ankley 同团队（见 PLAN 备注"⚭Ankley"，应理解为同源合作关系，非其他含义）。

## 2. 学术思想蒸馏
### 2.1 核心主张
1. **AOP 是"知识组织与外推"的工具，不是化学品专属模型**：AOP 不依赖具体化学品、模块化（KE/KER 可复用）、单条 AOP 为开发单元而 AOP 网络才是预测单元、AOP 是"活文档"（Toxicol Sci 2014，五原则，摘要原文可核）。
2. **机制数据须"翻译"为风险评估相关终点**：2010 年奠基文指出需把分子起始事件连到个体存活/发育/繁殖并外推到种群（ETC 2010 摘要）。
3. **KE 应是在特定生物层级的独立测量，以"功能等效"决定粒度；优先复用知识库既有 KE/KER**（Toxicol Sci 2014 II，最佳实践）。
4. **tPOD 作为筛查级保守起点**：转录组浓度-响应得到的 tPOD 通常低于鱼类顶端终点效应浓度，但不一定低于甲壳类/昆虫（Arch Environ Contam Toxicol 2024 摘要），因此应跨类群（鱼/溞/藻/摇蚊）组合使用，并用"实测浓度"计算。
5. **NAM + AOP + 机制模型可预测体内效应**：以体外芳香化酶抑制数据+AOP+计算模型，预测咪鲜胺类杀菌剂 imazalil 对黑头呆鱼生殖的影响，体内效能在预测的一个数量级内（ETC 2023）。
6. **AOP 开发需要社区基础设施与质量控制**：OECD 教练计划、AOP-Wiki "园艺"（去除冗余 KE）、并向 AI 辅助人机混合流程推进。

### 2.2 方法论签名
- 黑头呆鱼成鱼 21 d 繁殖试验（E2、Vtg、产卵量）+ 离体卵巢类固醇生成 + 机制计算模型（HPG 轴模型）指导暴露设计。
- 幼鱼/幼虫 24 h 暴露、96 孔板、TempO-Seq 靶向（"reduced transcriptome"，1832 基因）或全转录组，BMC 建模 → tPOD；多类群（FHM、Daphnia magna、Raphidocelis、Chironomus dilutus）。
- ToxCast/SeqAPASS 数据与 PFAS、农药、药物的筛查优先级排序；Cell Painting（RTgill-W1）+ 体外处置（IVD）模型。
- 逐步优先级框架（stepwise prioritization）与大型现场监测数据（五大湖支流，与 USGS 合作）。

### 2.3 研究范式演变
2000s 鱼类内分泌干扰与 HPG 轴生物标志物 → 2010 AOP 概念框架 → 2014 AOP 开发原则/最佳实践、AOP-KB → 2015–2020 具体通路（含 AOP 网络、芳香化酶/雄激素受体）与 SeqAPASS 物种外推 → 2019 起 EPA 生态 HTTr 计划（挑战赛选定测序平台）→ 2022–2025 tPOD 系列（FHM、溞、藻、斑马鱼、摇蚊）→ 2023–2026 五大湖污染物优先排序与 AOP 334 → 2025–2026 AOP 教练计划与"AI 加速 AOP"路线图。

## 3. 代表作精读（均经 PubMed 检索核实）
1. **Adverse outcome pathways: a conceptual framework to support ecotoxicology research and risk assessment** | Environ Toxicol Chem | 2010 | 10.1002/etc.34 —— 第一作者 Ankley，Villeneuve 为末位署名（13 位作者）。提出 AOP 概念：连接分子起始事件与风险评估相关层级的不良结局；以 5 个案例（含 AhR、ER 与 Vtg 等）说明其可聚焦测试设计、跨化学品外推和混合物预测。AOP 在生态毒理学的奠基文。
2. **Adverse outcome pathway (AOP) development I: strategies and principles** | Toxicol Sci | 2014 | 10.1093/toxsci/kfu199 —— 第一作者。五原则（非化学品特异、模块化、单链为开发单元、网络为预测单元、活文档）。为 OECD AOP 开发指南的概念基础。
3. **Adverse outcome pathway development II: best practices** | Toxicol Sci | 2014 | 10.1093/toxsci/kfu200 —— 第一作者。给出 KE/KER 描述的最佳实践与"功能等效"概念，强调在知识库中复用而非重复建条目。
4. **Development of an adverse outcome pathway for acetylcholinesterase inhibition leading to acute mortality** | Environ Toxicol Chem | 2014 | 10.1002/etc.2662 —— Russom、LaLone、Villeneuve、Ankley。按 OECD 指南构建的早期广分类群 AOP，整合大量有机磷/氨基甲酸酯研究。
5. **Leveraging existing data for prioritization of the ecological risks of human and veterinary pharmaceuticals to aquatic organisms** | Philos Trans R Soc B | 2014 | 10.1098/rstb.2014.0022 —— LaLone 等；以哺乳动物 ADME 数据、分子靶标跨物种保守性（SeqAPASS）与 AOP 对药物排序。
6. **Case Study in 21st-Century Ecotoxicology: Using In Vitro Aromatase Inhibition Data to Predict Reproductive Outcomes in Fish In Vivo** | Environ Toxicol Chem | 2023（2022 e-pub）| 10.1002/etc.5504 —— 第一作者。NAM+AOP+计算模型预测，imazalil 体内效应浓度与预测一致（一个数量级内）。
7. **Pilot testing and optimization of a larval fathead minnow high throughput transcriptomics assay** | Curr Res Toxicol | 2022 | 10.1016/j.crtox.2022.100099 —— 第一作者。生态 HTTr 的奠基性试点（金属、SSRI、新烟碱类样化合物，tPOD 低于鱼类顶端效应浓度）；数据集见 EPA ScienceHub（DOI 10.23719/1527818，data.gov 检索返回）。
8. **Leveraging ToxCast data and protein sequence conservation to complement aquatic life criteria derivation** | Integr Environ Assess Manag | 2023 | 10.1002/ieam.4617 —— Schaupp、LaLone、…、Villeneuve。ToxCast 第 5 百分位 POD 与水生生物基准 9 种化合物中 6 种在 10 倍内，结合 SeqAPASS 评价物种适用性。
9. **Verification of In Vivo Estrogenic Activity for Four PFAS Identified as ER Agonists via NAMs** | Environ Sci Technol | 2023 | 10.1021/acs.est.2c09315 —— 第一作者；体外/计算 NAM 命中→体内验证的闭环范例。

## 4. 近期文章蒸馏（时间倒序；以 2024–2026 为主；"启示"一栏面向斑马鱼行为毒理学研究者）
> 作者位次标注自 PubMed 作者列表（第一/末位）。摘要不可得者标明。

1. **Accelerating AOP Development in the AOP-Wiki with AI: A Practical Road Map for the Community** | Environ Sci Technol | 2026（PubMed e-pub 2026-05-18；JRC 记录 2026-07-24，日期不一致 ⚠️）| 10.1021/acs.est.6c05148
   - 作者：Song、Kumar、Tanabe、Villeneuve（第 4 位）、Wittwehr（末位；JRC 记录核实）——**并非 Villeneuve 牵头**，D 册简卡"牵头"措辞应修正。
   - 核心：NLP、本体对齐与 LLM 可加速文献筛选、证据抽取、因果陈述结构化和术语标准化；提出人机混合流程与路线图（近期低门槛应用 + 远期 AOP-Wiki 3.0 与共享训练集）；AI4AOP 为试点。（JRC 摘要）
   - 方法：评述 + 路线图。
   - **启示**：行为文献数据量大、术语混乱（freezing/hypoactivity/photomotor response 等同义不同名），非常适合用 AI 辅助做"行为 KE 的同义合并与证据抽取"。可把本组行为终点按 AOP-Wiki 功能等效原则预先标准化，并拟参与 AI4AOP 试点贡献斑马鱼行为 KE。
2. **Transcriptomic points of departure from the aquatic insect Chironomus dilutus for 22 PFAS and their use in chemical hazard screening** | Environ Toxicol Chem | 2026 | 10.1093/etojnl/vgag244 —— 末位。96 孔板 24 h 暴露，tPOD 3–1602 µg/L，与 FHM、溞、藻和哺乳动物细胞 HTP 比较，远高于环境浓度。
   - **启示**：tPOD 是"无物种偏倚的下界"；若斑马鱼行为 POD 低于同一化合物的 tPOD，需检讨是否存在 tPOD 未覆盖的神经功能通路（转录响应在 24 h 内不一定反映神经行为变化）。
3. **Workshop report: scoping for the development of a proposal for an OECD guidance document on fish vitellogenin assessment** | Integr Environ Assess Manag | 2026 | 10.1093/inteam/vjaf127 —— 41 位作者，非第一/末位（Burden 第一，Yamamoto 末位）。围绕 OECD 鱼类卵黄蛋白原评估指南文件的范围界定。
   - **启示**：展示 OECD 如何把一个机制标志物（Vtg）转化为受监管认可的指南文件——行为终点要走同样路径需先有标准化方法、参考化学品和跨实验室验证。
4. **Sertraline Hydrochloride Exposure Leads to ROS Burst in Model Microalgae Species** | Environ Sci Technol | 2025（e-pub 2025-12）| 10.1021/acs.est.5c11439 —— 第一作者 Ankley、末位 Villeneuve；AOP + 多组学 POD（藻类）。标题中物种名在 PubMed 中缺失，具体藻种 ⚠️待核实。
   - **启示**：SSRI 是斑马鱼行为研究常用对象；该文显示同一药物在非靶标类群中走完全不同通路，提示行为表型的"靶标保守性"需用 SeqAPASS 先验。
5. **An evaluation of transcriptomic points of departure and gene expression profiles for larval fathead minnows exposed to 22 chemicals with known modes of action** | Aquat Toxicol | 2025 | 10.1016/j.aquatox.2025.107650 —— 末位。靶向 TempO-Seq；22 种农药/药物；说明合理选基因的靶向方案足以导出保护性 tPOD；用 sscMap/Euler 图比较同 MoA 化合物。
   - **启示**：给出"同 MoA 化合物基因表达重叠"的比较范式，行为研究可借鉴为"同 MoA 化合物的行为指纹（behavioral fingerprint）一致性"，用以论证 MIE→行为 KE 的特异性。
6. **Adverse Outcome Pathway (AOP) Coaching Program—how it functions and contributes to a more harmonized approach to AOP development and construction of AOP networks with regulatory utility** | Environ Toxicol Chem | 2025 | 10.1093/etojnl/vgaf173 —— 28 位作者（Tanabe 第一，Yauk 末位）；OECD 2012 启动 AOP 计划、2013 发布指南、2019 引入教练计划；教练推动"园艺"去除 AOP-Wiki 中冗余 KE。
   - **启示**：最现实的路径——申请一位教练，用 OECD 指南把本组行为 AOP 提交 AOP-Wiki；先检索已有 KE（如 KE 1005 "Reduced, Swimming performance"）并复用，避免新建同义 KE。
7. **Inhibition of Fin Regeneration in Fathead Minnow by a Potent Synthetic Glucocorticoid and Development of AOP 334** | Environ Sci Technol | 2025 | 10.1021/acs.est.5c02446 —— Cole 第一，Brooks 末位，12 位作者；Villeneuve 位次/角色 ⚠️待核实（AOP-Wiki 中他仅列为 Contributor，作者为 Cole）。氟替卡松与地塞米松 7 d 暴露抑制鳍再生，Wnt/β-catenin 与 BMP 信号紊乱。
   - **启示**：AOP 334（GR 激动→鳍再生受损）经 AOP-Wiki 核实含 KE 1005 "Reduced, Swimming performance"，链至 AO 360 "Decrease, Population growth rate"——这是游泳行为/运动能力作为 KE 的现成范例。斑马鱼 GR 激动（含糖皮质激素对 locomotor 的影响）可直接对接此 AOP。该 AOP 的 OECD 工作计划状态为空（AOP-Wiki 2025-04-18 页面）。
8. **Comparison of whole transcriptome and targeted RNA sequencing for ecological high-throughput transcriptomics** | Regul Toxicol Pharmacol | 2025 | 10.1016/j.yrtph.2025.105898 —— 第一作者；2019 年 EPA 联邦挑战赛，3 个团队 5 个方案，TempO-Seq（5–11% 基因的哨兵集）最佳；哨兵集 tPOD 与全转录组相差多在 10 倍内。
   - **启示**：监管可采信的数据格式取决于"透明、详细的报告"（作者原话）：若行为研究需与 tPOD 并行，应同时报告平台、浓度（实测）、BMC 建模参数。
9. **Comparison of transcriptomic points of departure with apical endpoints in developing zebrafish exposed to PFOS, PFOA, or PFHxS** | Toxicol Sci | 2025 | 10.1093/toxsci/kfaf047 —— 末位。斑马鱼 tPOD 在不同起始/时长下多在 1.5 个数量级内；多数低于致死与亚致死顶端终点；PFOA tPOD 对所有顶端效应均有保护性，PFOS/PFHxS 在效应浓度四分位范围内。
   - **启示**：**与斑马鱼行为最直接相关的一篇**。摘要未提及行为终点是否纳入顶端比较（⚠️待核实全文）。研究者可用同一暴露设计补做幼鱼光-暗运动实验，检验"行为 POD 是否落在 tPOD 之上/之下"，tPOD 对 PFAS 通常低于顶端；若行为 POD 低于 tPOD 则是值得报道的反例。
10. **A combination of high-throughput in vitro and in silico NAMs for ecotoxicology hazard assessment for fish** | Environ Toxicol Chem | 2025 | 10.1093/etojnl/vgae083 —— 12 位作者（Nyffeler 第一，Harrill 末位）。RTgill-W1 小型化 OECD TG 249 + Cell Painting + IVD 模型，225 种化学品，59% 经调整的体外 PAC 与体内 LC50 在一个数量级内，73% 受保护。
    - **启示**：说明监管上接受"受保护性比例"这一指标。行为 POD 与鱼类 LC50/体外 PAC 比较时可同样报告保护比例。
11. **Derivation of transcriptomics-based points of departure for 20 PFAS using a larval fathead minnow reduced transcriptome assay** | Environ Toxicol Chem | 2025（e-pub 2024）| 10.1002/etc.5825 —— 第一作者。中位 tPOD 10 µM；长链羧酸等最有活性（<1 µM）；与人类细胞系多数一致、常高于溞；比环境浓度高数个数量级。
    - **启示**：PFAS 的神经行为毒性证据常以低于此浓度的 locomotor 改变出现，可与此 tPOD 做逐化合物对照，评价哪类 PFAS 行为 POD < tPOD。
12. **Transcriptomics-based points of departure for Daphnia magna exposed to 18 PFAS** | Environ Toxicol Chem | 2025（e-pub 2024）| 10.1002/etc.5838 —— 第一作者；溞类 tPOD；与 FHM 比较（FHM 常更高）。
    - **启示**：说明"最敏感类群"可能是无脊椎动物，行为研究若仅用斑马鱼需说明代表性。
13. **Comparing Transcriptomic Points of Departure to Apical Effect Concentrations for Larval Fathead Minnow Exposed to Chemicals with Four Different Modes of Action** | Arch Environ Contam Toxicol | 2024 | 10.1007/s00244-024-01064-y —— 末位。有机磷、蜕皮激素受体激动剂、PSII 抑制剂、ER 激动剂；tPOD 对鱼类顶端效应有保护性；强调实测浓度对 POD 的影响及重复性/变异评估。
    - **启示**：有机磷（AChE 抑制）是斑马鱼行为毒理的经典；该文给出 AChE-MoA 化合物 tPOD 与顶端终点比较的数据，可与 AOP（AChE 抑制→急性死亡）及行为 KE 对接。
14. **Bioactivity of the ubiquitous tire preservative 6PPD and degradant, 6PPD-quinone in fish- and mammalian-based assays** | Toxicol Sci | 2025 | 10.1093/toxsci/kfaf008 —— 末位；另有 Cell Painting 补充文（Environ Sci Technol Lett 2025，10.1021/acs.estlett.5c00327，Villeneuve 非第一/末位，位次 ⚠️待核实）。
    - **启示**：6PPD-quinone 对银大麻哈鱼的急性毒性与行为/循环症状相关；斑马鱼对其不敏感，使其成为"物种敏感性差异"的行为/生理对照案例。
15. **Effects of a novel estrogenic perfluoroalkyl substance on reproductive endocrinology and function in the fathead minnow** | Environ Toxicol Chem | 2025 | 10.1093/etojnl/vgaf006 —— 末位；PFAS 经 ER 激动影响生殖内分泌（FC8-diol，另见 EcoToxChip 研究 10.1002/etc.5937，2025/2024）。
    - **启示**：NAM 命中→体内验证的标准流程，行为学（如求偶/攻击行为）可作为内分泌 AOP 的补充 KE。
16. **Application of transcriptomics concentration-response modeling for prioritization of contaminants detected in tributaries of the North American Great Lakes** | Environ Toxicol Chem | 2025 | 10.1093/etojnl/vgaf050 —— 末位；及系列：Great Lakes 支流 PFAS（10.1093/etojnl/vgae053）、环境危害浓度推导（10.1093/etojnl/vgae002）、回顾性逐步优先排序（10.1093/etojnl/vgaf069）、入侵贻贝数据（10.1093/etojnl/vgaf072）。
    - **启示**：展示 tPOD 如何用于现场混合物优先排序；行为 POD 若要进入此类流程，需要高通量（96/384 孔）与可规模化。

### 2023–2024 补充（AOP 相关）
- Cross-species applicability of an AOP network for thyroid hormone system disruption | Toxicol Sci | 2023 | 10.1093/toxsci/kfad063（Haigis 第一，Knapen 末位）；Deiodinase inhibition impairs swim bladder tissue layers in zebrafish | Aquat Toxicol | 2023 | 10.1016/j.aquatox.2023.106632；The thyroid hormone system disrupting potential of resorcinol in fish | Ecotoxicol Environ Saf | 2024 | 10.1016/j.ecoenv.2024.116995。——斑马鱼甲状腺 AOP（比利时 Antwerp 合作），**直接涉及斑马鱼**，可做行为（游泳）KE 补充。
- AOP Report: Adverse Outcome Pathways for Aromatase Inhibition or AR Agonism Leading to Male-Biased Sex Ratio and Population Decline in Fish | Environ Toxicol Chem | 2023 | 10.1002/etc.5581；AOP Report: AhR Activation Leads to Early-Life Stage Mortality via Sox9 Repression | ETC | 2023 | 10.1002/etc.5699（末位）；Putative AOP development based on physiological responses of female fathead minnows to estrogen versus androgen receptor agonists | Aquat Toxicol | 2023 | 10.1016/j.aquatox.2023.106607（末位）。
- Comparison of in silico, in vitro, and in vivo toxicity benchmarks suggests a role for ToxCast data in ecological hazard assessment | Toxicol Sci | 2023 | 10.1093/toxsci/kfad072；An automated computational data pipeline to rapidly acquire, score, and rank toxicological data for ecological hazard assessment | IEAM | 2024 | 10.1002/ieam.4945。

## 5. 基金/项目档案（美国联邦科学家版）
> 无 NSFC/NIH 外部基金。以下据 EPA 官网、data.gov、AOP-Wiki、OECD 公开页面和论文署名盘点；官方内部计划编号/经费数 **未能检索到**。

### 5.1 EPA 内部研究计划（据署名与公开页面）
| 计划/工具 | Villeneuve 角色 | 证据 |
|---|---|---|
| EPA 生态高通量转录组学（eco-HTTr；用户给出名称 "EcoTox HTTr"，本次检索未见官方使用该词）| 核心参与/导师；2022 试点论文第一作者；EPA 博后岗位以其为联系人 | WebSearch 摘要；zintellect EPA-ORD-CCTE-GLTED 招聘；Curr Res Toxicol 2022；官方计划页 ⚠️未能检索到 |
| 2019 EPA 联邦挑战赛（低成本高通量 RNA-seq 方案）| 论文第一作者，作为评估/组织方团队成员（Regul Toxicol Pharmacol 2025）| PubMed 摘要 |
| CSS（Chemical Safety for Sustainability）研究计划 | 署名机构为 CCTE；作为 CSS 成员 ⚠️未能检索到明确官方描述 | 论文署名（CCTE）|
| 五大湖污染物优先排序（与 USGS；GLRI 经费背景）| 系列末位/通讯 | ETC 2025 系列；Loken 等 2023 提及 GLRI |
| 21st-century ecotoxicology 博后项目（GLTED）| 导师/联系人 | zintellect 页面 |
| SeqAPASS（跨物种靶标保守性工具）| 论文合作者，非开发负责人（开发者为 LaLone 等）| IEAM 2023 (10.1002/ieam.4617) 使用；SeqAPASS 官网细节未检索 ⚠️|

### 5.2 OECD / 国际任职
- **AOP-Wiki**：在 AOP 334 页面列为 Contributor（有写权限）；AOP-Wiki 论坛讨论中被指派为 AOP 39 开发团队的"教练"（AOP-Wiki forum thread 173，经 WebSearch 摘要）。
- **OECD AOP 计划**：2014 年两篇开发论文第一作者，作为 OECD 指南/Handbook 的概念来源；2019 与 2022 OECD AOP 网络研讨会发言人（WebSearch 摘要）。OECD 具体任职（如 EAGMST/WNT 代表、联合主席）**未能检索到**。
- 2025 年 AOP 教练计划论文为 28 位作者之一（具体角色 ⚠️待核实）。

### 5.3 EPA ScienceHub / 公开数据集（data.gov 返回）
- 幼鱼 HTTr 试点数据：DOI 10.23719/1527818（联系人 Villeneuve）。
- tPOD 比较数据：DOI 10.23719/1531142（联系人 Kevin Flynn；GEO/SRA BioProject 编号检索返回为 PRJNA104613，位数可疑 ⚠️待核实）。
- 有机磷数据集：DOI 10.23719/1529449（Martin 等 2023, Toxics；Villeneuve 共同作者；该论文本次未直接核实 ⚠️）。
- 另见 EPA figshare 演示文稿 "High throughput transcriptomic assessment of PFAS in fish, invertebrates and plants"（2023，EPA CCTE）。

### 5.4 问题意识演变
1. **2010–2014（概念与规范）**：如何把分子数据转为风险评估终点？→ AOP 概念 → 五原则与最佳实践，使社区可复用。
2. **2014–2020（通路与外推）**：具体 AOP 构建（AChE、芳香化酶、AR、AhR、GR）+ SeqAPASS 物种外推 + NAM 验证。
3. **2019–2022（高通量化）**：问题变为"数以万计的化学品缺乏水生毒性数据，怎么筛"→ 生态 HTTr 与挑战赛。
4. **2023–2025（量化与监管化）**：tPOD 是否保护顶端终点？多类群比较、PFAS、实测浓度；五大湖优先排序；Cell Painting 与 OECD TG 249 的体外-体内衔接。
5. **2025–2026（规模化与 AI）**：AOP-Wiki 冗余 KE 治理、教练计划、AI 辅助 AOP 开发（路线图第四作者，非牵头）。

## 6. 趋势判断
1. **tPOD 向更多类群与更多化学类扩展，并走向监管定量化**（依据：2023–2026 连续发表 FHM/溞/藻/斑马鱼/摇蚊；PFAS 22 种为共同化学集）。
2. **AOP-Wiki 质量治理与 AI 辅助**（依据：2025 教练计划、2026 路线图）。
3. **以 NAM 命中→体内验证的内分泌/GR/甲状腺通路**（依据：AOP 334、全氟醇 FC8-diol、甲状腺 AOP 网络）。
4. **五大湖现场优先排序与 tPOD、Cell Painting 并用**（依据：2025 ETC 系列）。
5. 行为终点尚未成为其组主线（本次 PubMed 行为/斑马鱼检索 44 条中近年命中主要为 tPOD 与甲状腺 AOP；更早 2016–2020 的 25 条未逐条核实 ⚠️），预期仅在 AOP 网络中以 KE（如游泳能力）形式出现。

## 7. 专家视角 Persona（以其身份评审斑马鱼行为毒理学项目）
1. "你的行为终点是哪一个 KE？有没有在 AOP-Wiki 中检索并复用既有 KE，而不是自创同义词？"
2. "这个行为改变是 MIE 的特异性下游，还是一般性应激/毒性的非特异反应？cytotoxic burst 之下是否仍有效应？"
3. "给出你的 BMC/BMD 建模和实测浓度；名义浓度算出的 POD 我不接受。"
4. "行为 POD 与 tPOD 的关系是什么？谁更低、是否同一暴露窗口？"
5. "你的 KER 有定量或剂量-时间一致性证据吗？是否有干预/拯救实验（rescue）？"
6. "这是单一 AOP 还是在网络中的位置？是否影响种群相关的 AO（如繁殖、存活）？"
7. "跨物种适用性：靶标蛋白在目标物种中保守吗？先用 SeqAPASS 说明。"
8. "能否高通量（96 孔）并提供可复核的原始数据与报告透明度，使监管方愿意采用？"
9. "这是筛查级还是确证级？不要夸大为风险评估结论。"

## 8. 元数据
- **PubMed**：`Villeneuve DL[Author] AND (2023:2026[dp])`（46 条）；`Villeneuve DL[Author] AND adverse outcome pathway[Title]`（18 条）；`Ankley GT[Author] AND Villeneuve DL[Author] AND adverse outcome pathway`；`Villeneuve DL[Author] AND (behavior OR zebrafish OR locomotor)`（44 条，仅取前 25 个 PMID，未逐条核实）。
- **Consensus / Web**：`Villeneuve transcriptomic point of departure`、`AOP-Wiki AI roadmap`；AOP-Wiki：aopwiki.org/aops/334；EPA：epa.gov/node/74083；data.gov 搜索 "Villeneuve tPOD"。
- **信息源**：PubMed、JRC 仓库记录（JRC145118）、AOP-Wiki、data.gov/EPA ScienceHub、EPA Science Matters、OECD AOP Handbook 页面。
- **核实论文数**：约 51 篇（46 条 2023–2026 命中 + 2010、2014 ×3 的奠基/早期条目；含部分 2022 年 e-pub）。
- **最后更新**：2026-11-06。
- **置信度**：论文标题/期刊/年份/DOI 高；作者位次仅部分核实（见各条）；基金/任职类中低。
- **⚠️待核实项（共 12 项）**：(1) 现单位归属（CCTE/OCSPP）；(2) 2026 AI 路线图发表日期（5 月 vs 7 月）；(3) 路线图中 Villeneuve 为第 4 作者而非牵头；(4) AOP 334 论文中其位次；(5) 6PPD Cell Painting 文位次；(6) 斑马鱼 PFAS tPOD 文是否含行为终点；(7) 藻种名；(8) "EcoTox HTTr" 官方名称；(9) CSS 计划任职；(10) OECD 任职（EAGMST 等）；(11) BioProject 编号；(12) 2016–2020 行为相关 25 条未核实。DOI 解析抽查未做（本环境无直接解析工具），建议后续抽查 10.1021/acs.est.6c05148、10.1021/acs.est.5c02446。
