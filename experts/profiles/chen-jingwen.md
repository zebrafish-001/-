# 陈景文（Jingwen Chen）— 大连理工大学环境学院
> 领域标签：计算毒理学 · 计算环境化学 · QSAR/机器学习预测 · 污染物环境（光）化学转化 · 化学品风险预测与绿色替代设计（benign by design） | 主领域：C | 档案建立：2026-10 | 检索覆盖至：2026-10
>
> 说明：本档案文献部分主要基于 PubMed 检索，限定单位为 Dalian University of Technology, Key Laboratory of Industrial Ecology and Environmental Engineering (MOE)，并核对通讯邮箱 jwchen@dlut.edu.cn，已剔除大连地区同名作者（Jianmin Chen 化工、Jia Chen 大连民族大学、Junxin Chen 软件学院、Jiahao/Jiping Chen 等）。每篇均附 DOI 链接。未逐篇核验的早期代表作标注"待核实"。

## 1. 基本信息
- 职称/职务：大连理工大学环境学院 教授、博士生导师；特聘教授（长江学者）。曾任环境科学与工程系主任（2003–2010）、环境学院院长（2010–2020）；工业生态与环境工程教育部重点实验室副主任（2007 至今）。
- 学术兼职：中国毒理学会计算毒理学专业委员会主任；《ACS Sustainable Chemistry & Engineering》副主编；《海洋环境科学》《生态毒理学报》副主编；《Journal of Environmental Sciences》等编委。
- 荣誉（据其大连理工大学教师主页）：国家杰出青年科学基金（2013）、长江学者特聘教授、国家"万人计划"科技创新领军人才（2016）、国家自然科学奖二等奖（第二完成人，2011）、教育部自然科学奖一等奖（第一完成人，2023）、霍英东教育基金教学奖二等奖（2022）等。
- 研究方向：环境计算毒理学（环境大数据、机器学习/AI 建模）、新污染物源头控制与筛查监测、化学品风险防控、环境光化学（污染物转化及转化产物毒性）、绿色替代品设计。
- 产出规模：教师主页称发表论文 360+ 篇、专著 3 部（具体篇目待核实）。
- 信息源：大连理工大学教师主页 https://faculty.dlut.edu.cn/1997011052/en/index.htm 。

## 2. 学术思想蒸馏

### 2.1 核心主张
1. **"数据空缺 + 全新化学品" 是风险管理的根本瓶颈**：全球已注册化学品超 35 万种，实测毒性/性质数据覆盖率极低，必须用高通量计算模型（QSAR/ML）去"填补数据空白"，而非逐一实验。
2. **预测模型必须严格刻画适用域（Applicability Domain, AD）**：反复强调模型可靠性取决于 AD。其团队提出基于"结构–活性图景（SAL/activity cliff）"和"特征–响应景观"的新型 AD 刻画方法，用于约束预测、避免外推误判。
3. **多模态是突破单一分子描述符天花板的关键**：把分子结构（图/指纹）与环境条件（光源、pH、温度、溶解氧）或受体结构（结合位点）同时输入，显著提升预测性能与适用性（如光解速率常数 R² 从 0.37 提升到 0.76）。
4. **母体化合物不是终点，转化产物（TPs）常更毒**：无论大气·OH 氧化、水相光转化还是微液滴界面反应，转化产物的毒性/生物累积性常高于母体，风险评估必须纳入转化化学。
5. **从"识别风险"走向"benign by design 绿色替代"**：将功能性、危害性与全生命周期影响整合，用生成式 ML 设计既保功能又低危害的替代化学品，避免"遗憾替代（regrettable substitution）"。
6. **膜蛋白等被忽视的毒性靶点应被纳入评估**：主张毒性测试不应只盯核受体，膜蛋白（GPCR、转运体、离子通道）数量多、跨物种保守，是被长期忽视的分子起始事件（MIE）。

### 2.2 方法论签名
- **"预测模型 + 适用域约束 + 全库筛查"三件套**：几乎每篇 ML 论文的固定范式——构建扩充数据集 → 建多模态/深度模型 → 用 SAL-based AD 约束 → 对数十万工业化学品/药物/天然产物全库预测 → 优先排序高风险物质。
- **量子化学 + 计算毒理学联用**：用 DFT/从头算分子动力学算反应机理与速率常数，再接毒理模型预测转化产物毒性（致癌、致突变、肝毒、皮肤致敏等），形成"机理—毒性"闭环。
- **跨域/迁移学习补数据稀缺**：如由淡水生态毒性知识迁移到海水（MarineTox）、由药物–蛋白互作迁移到 PFAS–蛋白（深度迁移学习）。
- **计算与实验互验**：分子模拟优化结构后做结构型虚拟筛选，再用体外实验（如 zSERT 抑制、生物层干涉）验证命中率。
- **生成式 AI 拓展化学空间**：用化学语言模型生成百万级候选结构（如 PFAS），拓展可疑物清单用于非靶向筛查。

### 2.3 研究范式演变
- 早期（约 2000s–2010s，待核实细节）：传统 QSAR/QSPR，预测污染物理化性质、环境行为与毒性，以描述符回归为主。
- 中期（2010s–2020 前后）：环境光化学与大气化学机理（量子化学算·OH 反应、转化产物），并开始毒理建模耦合。
- 近期（2021–2026）：全面转向深度学习/多模态/生成式 AI + 适用域方法学创新，拓展到海洋生态风险、膜蛋白靶点、微液滴界面化学、绿色替代设计与 AI agent 化学品管理，呈现"AI 驱动全链条（暴露—毒性—风险—替代）"格局。

## 3. 代表作精读（近两年旗舰工作；早期经典待核实）
> 说明：陈教授 1997 年起发表论文众多，本次检索未逐篇回溯其 2010s 经典 QSAR 论文（待核实）。以下选取本次确证、最能代表其思想的高影响工作。

1. **Using Machine Learning for Green Substitution of Industrial Chemicals: Integrating Functionality, Hazard, and Life Cycle Impact**（*Chemical Reviews*, 2026, 126(2):841-894）[DOI](https://doi.org/10.1021/acs.chemrev.5c00828)
   综述其"绿色替代设计（benign by design）"核心纲领，与绿色化学奠基人 Anastas、Zimmerman 合著。系统梳理 ML 辅助分子设计方法，提出兼顾功能、低危害与全生命周期的替代策略，并展望面向化学品风险管理与绿色替代的 AI agent。是其学术思想的"宣言式"文献。

2. **Interfacial-mediated fast formation of toxic derivatives of phthalate esters**（*Nature Communications*, 2026, 17(1)）[DOI](https://doi.org/10.1038/s41467-026-69495-w)
   微液滴实验 + 从头算分子动力学证明邻苯二甲酸酯在微液滴表面自发降解（半衰期 <10 min，较本体快 4–11 个数量级），生成羟基化/羧基化转化产物，计算毒理预测其人肝毒性最高增至 37.5 倍。颠覆传统环境持久性认知，主张风险框架须纳入界面化学。

3. **MarineTox Predictor: Enhancing Low-Resourced Saltwater Ecotoxicity Prediction via Knowledge Sharing from Freshwater Ecotoxicity**（*Environ. Sci. Technol.*, 2026, 60(21):14813-14825）[DOI](https://doi.org/10.1021/acs.est.5c15496)
   多任务深度学习 + 跨域知识共享，解决海水生态毒性数据稀缺。覆盖 5 门 26 种海洋生物 31 个毒性任务，低资源任务性能提升最高 140%；为约 6.8 万化学品推导危害阈值，建成在线平台。典型"跨域迁移补数据空缺"范式。

4. **AI-Driven Species Sensitivity Distribution (AI-4-SSD) Framework for Predicting Aquatic Ecological Risks ... in Global Near-Coastal Environments**（*Environ. Sci. Technol.*, 2026, 60(14):10651-10662）[DOI](https://doi.org/10.1021/acs.est.6c00675)
   多模态深度学习预测 8 种海洋物种种群级毒性（R²=0.85），实现暴露—毒性—风险全链条预测；识别 DDT、6:2/8:2 diPAPs 等 6 种高风险物，揭示黑海混合暴露累积风险。强调混合物风险管理。

5. **Multimodal Machine Learning Models on Aqueous Direct Photodisappearance Rate Constants**（*Environ. Sci. Technol.*, 2026, 60(25):17900-17913）[DOI](https://doi.org/10.1021/acs.est.6c05993)
   首次把环境条件（光源、pH、温度、溶解氧、初始浓度）与分子结构一同建模，验证集 R² 由 0.369（单模态）跃升至 0.756；提出特征–响应景观 AD 刻画。多模态思想的代表作。

6. **Generative AI-Empowered Screening Strategy for Chemical Pollutants: A Case on PFAS**（*Environ. Sci. Technol.*, 2025, 59(46):24976-24986）[DOI](https://doi.org/10.1021/acs.est.5c07495)
   用化学语言模型生成 140 万+ PFAS 结构（拓展化学空间 21.6%）形成可疑物清单，Top-1 注释准确率 87%，在实际含氟废水中注释出 88+ 个被忽视 PFAS 特征。生成式 AI 用于未知污染物识别的开创性案例。

7. **Zebrafish Serotonin Transporter Inhibition Enables Identification of Neuroactive Chemicals: Structural Insights into Interspecies Differences**（*Environ. Sci. Technol.*, 2026, 60(33):23162-23169）[DOI](https://doi.org/10.1021/acs.est.6c04972)
   分子模拟（Boltz-2 预测亲和力）+ 虚拟筛选 + 体外验证，识别作用于斑马鱼血清素转运体（zSERT）的环境化学品，并解析 zSERT 比 hSERT 更敏感的结构机制；15 个预测命中有 14 个经体外验证。对行为毒理学高度相关。

## 4. 近期文章蒸馏（2024–2026，时间倒序）
> 每篇：核心发现 | 方法要点 | 对斑马鱼行为毒理学研究者的启示。均为 PubMed 检索确证，附 DOI。

**[1] Zebrafish Serotonin Transporter Inhibition Enables Identification of Neuroactive Chemicals**｜*Environ. Sci. Technol.*｜2026（60:23162）｜[DOI](https://doi.org/10.1021/acs.est.6c04972)
- 核心发现：用计算筛选从欧中高风险化学库中锁定可抑制斑马鱼 SERT 的神经活性物质，并阐明 zSERT 比 hSERT 更敏感的结构根源。
- 方法要点：Boltz-2 预测 27 种抗抑郁药的 h/zSERT 亲和力差异 → 100 ns MD 锁定关键残基 → 基于优化后 zSERT 结构做结构型虚拟筛选 → 体外抑制实验验证（15 选 14 命中）。
- 对斑马鱼行为毒理学的启示：直接给出"分子起始事件（SERT 抑制）→ 行为（如回避/活动性改变）"的机制起点；提示用结构模拟预先筛出潜在神经行为活性物，再做行为端点验证，并高度关注人–鱼种间靶点差异对外推的影响。

**[2] Atmospheric Oxidation Mechanism of Benzimidazole initiated by ·OH: Nitrosamine Formation**｜*Environ. Sci. Technol.*｜2026（60:19413）｜[DOI](https://doi.org/10.1021/acs.est.6c00804)
- 核心发现：含氮挥发性化学品苯并咪唑经·OH 氧化，经"·OH 加成"这一此前未识别通路生成致癌亚硝胺；几乎所有氧化产物比母体更毒。
- 方法要点：量子化学算速率常数（1×10⁻¹¹ 量级）与机理 + 毒理模型预测产物毒性。
- 启示：转化产物毒性常超母体——行为毒理实验设计时应把大气/环境转化产物纳入暴露物考量，而非只测母体。

**[3] Machine Learning-Enhanced DGT Passive Sampling Coupled with Non-Targeted Analysis**｜*Anal. Chem.*｜2026（98:20340）｜[DOI](https://doi.org/10.1021/acs.analchem.6c01847)
- 核心发现：用 ML 预测扩散系数与电离效率，使 DGT-非靶向分析可半定量，无需逐一标准品，在市政污水中半定量 85 种污染物并优先排序 8 种高风险物。
- 方法要点：ML 辅助半定量框架 + 生态风险评估，平均预测误差 1.78 倍（AD 内）。
- 启示：为行为实验提供环境真实暴露浓度/优先物清单，支撑"环境相关浓度"下的斑马鱼暴露设计。

**[4] Multimodal ML Models on Aqueous Direct Photodisappearance Rate Constants**｜*Environ. Sci. Technol.*｜2026（60:17900）｜[DOI](https://doi.org/10.1021/acs.est.6c05993)
- 核心发现：同时考虑分子结构与环境条件的多模态模型，光解速率常数预测 R² 0.37→0.76。
- 方法要点：1281 条/304 化合物数据集；特征–响应景观 AD。
- 启示：污染物在水体中的光化学持久性决定其实际暴露时长；评估斑马鱼长期行为效应时应结合光解半衰期判断暴露稳定性。

**[5] MarineTox Predictor**｜*Environ. Sci. Technol.*｜2026（60:14813）｜[DOI](https://doi.org/10.1021/acs.est.5c15496)
- 核心发现：跨域迁移学习预测 26 种海洋生物 31 个毒性端点，低资源任务性能最高提升 140%。
- 方法要点：多任务深度学习 + 淡水→海水知识共享 + 子结构–物种互作网络。
- 启示：示范"用数据丰富物种的知识迁移到数据稀缺端点"，行为端点数据同样稀缺，可借鉴迁移学习补齐跨物种/跨端点行为毒性预测。

**[6] Spontaneous Interfacial Redox Transformation of 6PPD-Quinone on Water Microdroplets**｜*J. Am. Chem. Soc.*｜2026（148:17166）｜[DOI](https://doi.org/10.1021/jacs.6c02017)
- 核心发现：轮胎衍生毒物 6PPD-Q 在气–水界面微液滴上超快转化（半衰期 <2 min，较本体快 1176 倍），生成毒性更高（1.1–2.6 倍）的氢醌衍生物。
- 方法要点：微液滴实验 + 分子模拟，提出还原–氧化协同效应（ROSE）。
- 启示：6PPD-Q 是近年鱼类急性致死/行为研究热点；提示其环境衍生物可能毒性更强，行为实验应考虑转化产物混合暴露。

**[7] Counted Fingerprint-Enhanced Graph Neural Network Models for Screening hERG Blockers**｜*Environ. Sci. Technol.*｜2026（60:11542）｜[DOI](https://doi.org/10.1021/acs.est.5c16775)
- 核心发现：双特征（分子指纹+分子图）融合 GNN 筛查 hERG 阻断剂，AUC 0.950；全库筛 50 万+ 化学品识别 2.6 万+ 潜在阻断剂。
- 方法要点：特征融合 + SAL-based AD。
- 启示：方法学上示范"多表征融合 + 严格 AD"，可迁移到行为/神经毒性端点的高通量预测建模。

**[8] Interfacial-mediated fast formation of toxic derivatives of phthalate esters**｜*Nature Communications*｜2026（17:1）｜[DOI](https://doi.org/10.1038/s41467-026-69495-w)
- 核心发现：邻苯二甲酸酯在微液滴界面超快生成羟基/羧基化产物，人肝毒性最高增 37.5 倍，皮肤致敏约增 1.5 倍。
- 方法要点：微液滴实验 + AIMD + 计算毒理预测。
- 启示：常见塑化剂（斑马鱼发育/行为常用模型污染物）的界面转化产物毒性更强，暴露设计需警惕转化产物。

**[9] Using Machine Learning for Green Substitution of Industrial Chemicals**｜*Chemical Reviews*｜2026（126:841）｜[DOI](https://doi.org/10.1021/acs.chemrev.5c00828)
- 核心发现：系统提出 ML 辅助绿色替代品设计方法论，整合功能性、危害与生命周期，避免遗憾替代。
- 方法要点：生成式 ML 分子设计综述 + 案例 + AI agent 展望。
- 启示：行为毒性可作为"危害性"维度之一纳入替代品筛选目标函数；为"设计不致行为异常的替代物"提供框架。

**[10] McGPCR: Multimodal Learning Model for Predicting GPCR Affinity of Plastic Chemicals**｜*Environ. Sci. Technol.*｜2025（59:25938）｜[DOI](https://doi.org/10.1021/acs.est.5c02770)
- 核心发现：构建 9.7 万条人 GPCR 亲和力数据集，多模态模型（分子图+受体结合位点）预测 109 个 GPCR 亲和力，筛出 30 种高风险塑料化学品。
- 方法要点：多模态学习 + 特征–活性景观 AD。
- 启示：GPCR 是神经行为调控的关键膜靶点；为"化学品→GPCR→行为效应"提供可预测的分子起始事件清单。

**[11] Hepatocyte Proteome Destabilization and Novel Targets for PFASs via Thermal Proteome Profiling + Deep Transfer Learning**｜*J. Hazard. Mater.*｜2025（500:140458）｜[DOI](https://doi.org/10.1016/j.jhazmat.2025.140458)
- 核心发现：TPP 实测 + 深度迁移学习预测 PFAS–蛋白亲和力（Pearson 0.89），发现 GenX 以核糖体蛋白为新靶点。
- 方法要点：实验–计算联用，生物层干涉验证 GenX–RPL4 结合。
- 启示：示范"组学实测 + 迁移学习"锁定未知分子靶点的通用策略，可用于解析行为毒物的蛋白靶点。

**[12] Generative AI-Empowered Screening Strategy for PFAS**｜*Environ. Sci. Technol.*｜2025（59:24976）｜[DOI](https://doi.org/10.1021/acs.est.5c07495)
- 核心发现：化学语言模型生成 140 万+ PFAS 结构用于非靶向筛查，实际废水中注释出大量被忽视 PFAS。
- 方法要点：生成式 AI + 非靶向高分辨质谱。
- 启示：帮助发现环境中"未知但真实存在"的污染物，为行为毒理学提供新的候选受试物来源。

**[13] Enlarged Data Sets and Innovative AD Characterization for hERG Binding ML Models**｜*Chem. Res. Toxicol.*｜2025（38:1460）｜[DOI](https://doi.org/10.1021/acs.chemrestox.5c00065)
- 核心发现：扩充 hERG 结合数据集建 ML 模型（外验 R²=0.89），全库筛 10 万+ 化学品识别 5000+ 潜在阻断剂。
- 方法要点：activity-cliff 感知的 SAL-based AD。
- 启示：心脏毒性端点建模范式，可直接类比到斑马鱼心脏/行为联合端点预测。

（另：Membrane Proteins perspective, *EST* 2025, [DOI](https://doi.org/10.1021/acs.est.5c05367)；γ-Terpinene 室内大气氧化, *Environ. Health* 2025, [DOI](https://doi.org/10.1021/envhealth.5c00100)；CO+HOCl 气–水界面 CO₂ 生成, *JACS* 2025, [DOI](https://doi.org/10.1021/jacs.5c13341) 亦为同期相关工作。）

## 5. 趋势判断
1. **从"预测单一端点"走向"AI 驱动全链条风险评估"**：依据——2026 年连续产出暴露—毒性—风险—替代一体化框架（AI-4-SSD、MarineTox、Chem Rev 绿色替代），且明确展望化学品管理 AI agent。
2. **生成式 AI 与化学语言模型将成为污染物发现/替代设计主引擎**：依据——2025 PFAS 生成式筛查、2026 Chem Rev 生成式分子设计综述，方向从"判别式"扩展到"生成式"。
3. **膜蛋白与界面/微液滴化学是两条新兴前沿**：依据——2025 膜蛋白 perspective 明确呼吁、2025 McGPCR，以及 2026 连续在 Nat Commun / JACS 发表微液滴界面转化工作，提示风险评估将纳入此前被忽视的靶点与反应相。
4. **"适用域方法学"本身是其持续的方法论创新点**：依据——多篇论文反复迭代 SAL-based / 特征–响应景观 AD，显示其把"预测可靠性/可信 AI"作为长期攻关主题。

## 6. 专家视角 Persona（评审/讨论典型立场与常问问题）
1. "你的预测模型适用域（AD）如何定义？受试化学品是否落在 AD 内？" —— 对任何 QSAR/ML 结果必问 AD 与外推可靠性。
2. "你测的是母体化合物，环境中它会光解/氧化/界面转化——转化产物的毒性评估了吗？" —— 坚持把转化产物纳入风险。
3. "单一分子描述符够吗？能否纳入环境条件或受体结构做多模态建模？"
4. "数据量和化学空间多样性是否足够？小样本/低资源端点能否用迁移学习或跨域知识共享？"
5. "分子起始事件（MIE）是什么？是否考虑了膜蛋白（GPCR/转运体/离子通道）等被忽视的靶点？"
6. "人与模式生物（如斑马鱼）的靶点结构差异有多大？跨物种外推的依据是否充分？"（见其 zSERT 人–鱼差异工作）
7. "暴露浓度是否环境相关？有没有实际环境监测/非靶向筛查数据支撑受试物与浓度？"
8. "计算预测有无实验验证？命中率/假阳性如何？"
9. "这个结果对化学品风险管理/绿色替代有什么可操作含义？能否指导 benign-by-design？"
10. "混合物/累积暴露风险考虑了吗？单一化学品低风险不代表共暴露低风险。"

## 7. 元数据
**建议定期检索式（PubMed）**
- `Chen J[Author] AND "Dalian University of Technology"[Affiliation] AND (QSAR OR "machine learning" OR transformation OR toxicity OR photochemistry)` ，再按通讯邮箱 `jwchen@dlut.edu.cn` 过滤确认。
- 补充：`("Chen Jingwen"[Author] OR jwchen) AND ("Industrial Ecology and Environmental Engineering")`；关注期刊 *Environ. Sci. Technol.* / *J. Hazard. Mater.* / *Water Res.* / *Nat. Commun.* / *JACS* / *Chem. Rev.*。
- 全貌补充源：大连理工大学教师主页、机构库 dlutir.dlut.edu.cn、X-MOL 导师页（https://www.x-mol.com/university/faculty/9262）、Web of Science / Google Scholar（可核验被引与早期代表作）。

**信息源**：PubMed（本次主检）；大连理工大学教师主页（职务/荣誉）。

**置信度**
- 高：第 3–4 节所列 2024–2026 论文（标题、期刊、年份、DOI、通讯作者单位均经 PubMed 元数据核验）。
- 中：基本信息中的职务与荣誉（来自主页网页抓取，部分任期信息可能已更新；院长任期已于 2020 结束）。
- 低/待核实：发表总数 360+ 篇与专著 3 部的具体篇目；2010s 及更早的经典 QSAR/环境行为代表作未逐篇回溯。

**待核实项**
1. 其 pre-2024 高被引经典论文（早期 QSAR/QSPR、环境光化学奠基工作）具体篇目与引用数——需 Web of Science/Scholar 补检。
2. 当前确切行政职务与最新学术兼职（主页信息时间跨度较大）。
3. 第 4 节各篇中陈景文的精确作者位次（通讯 vs 共同作者）——部分已由邮箱确认为通讯（如 Nat Commun、J. Hazard. Mater.、EST hERG/McGPCR/生成式 PFAS、膜蛋白 perspective、zSERT），其余以单位+研究主题判定为核心作者，建议投稿前逐篇复核。

---
*本档案文献信息据 PubMed 检索整理，所有论文已附 DOI 链接以标注原始出处。*
