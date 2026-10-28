# Robyn L. Tanguay — 俄勒冈州立大学（Sinnhuber 水生研究实验室）
> 领域标签：斑马鱼高通量毒性筛查（HTS）｜发育/行为表型组｜毒理基因组学｜AHR 通路｜PAHs/PFAS/纳米材料｜新方法学（NAMs）｜Superfund 研究 | 主领域：A | 档案建立：2026-10 | 检索覆盖至：2026-10-28

**数据源说明**：文献元数据来自 PubMed（DOI 均附后）；基金来自 NIH RePORTER API（api.reporter.nih.gov，查询日 2026-10-28）、EPA NCER 公开页；职务/荣誉来自 OSU/TAMU 页面与 Wikipedia（二手来源已标注）。仅写检索中实际看到的条目，不确定处标"⚠️待核实"。

**两处事实勘误（相对于本库此前记载）**：
1. 其实验室标准流程是 **4 hpf 酶法（pronase）自动脱膜，6 hpf 单胚入 96 孔板，6–120 hpf 静态暴露**（Truong 2014；Mandrell 2012），不是"2 hpf 脱膜"。
2. 2019 年前的论文署名为 **Robert L. Tanguay**，之后为 **Robyn L. Tanguay**（同一人，Google Scholar/Wikipedia 注明 "formerly Robert L."）。检索须两个名字都查。

---

## 1. 基本信息

**职务**（OSU 系/学院目录、Texas A&M HIAS、SOT ToxChange 页）
- 俄勒冈州立大学 University Distinguished Professor，Dept. of Environmental and Molecular Toxicology（EMT）。
- 主任：Sinnhuber Aquatic Research Laboratory（SARL）；OSU Superfund Research Center（NIEHS P42）。
- 曾任：OSU Environmental Health Sciences Center 主任（P30ES030287 行政核心 PI，FY2020–2025）。
- 教育/履历（Wikipedia，⚠️二手）：UC Riverside 生化博士（1995）；威斯康星麦迪逊 Richard Peterson 实验室博士后；1999 年科罗拉多大学助理教授；2003 年到 OSU；2011 年杰出教授。
- 编辑职务（⚠️待核实现状）：Toxicological Sciences、Toxicology Reports、Nanomaterials 副主编；SOT 纳米毒理专业分会 2016 年会长。

**荣誉（有来源）**：PANWAT Achievement Award（2012）；SOT 生殖发育毒理科学成就奖（2020）；OSU 博士后导师卓越奖（2021）；SOT 毒理学家导师奖（2023）；TAMU Hagler 高等研究院 Fellow（2023–24 届）；SOT Leading Edge in Basic Science Award（2025）；SOT 2025–26 副会长当选人（⚠️待核实）；Toxicological Sciences 年度论文奖（年份不详）。

**实验室资源盘点（SARL，"方法学标尺"价值所在）**
- **设施**：独立 SARL 大楼（Corvallis）；OSU 新闻称 17,000 ft² 实验室、数千鱼缸，对外供应胚胎/成鱼；NIH C06OD036081（$7.53M，2023–2028）正改造 3,500 ft² 为 SPF 斑马鱼房 + 自动清洗/喂食/远程监控 + 流水式暴露专用室。
- **标准 HTS 流程**（Truong 2014；Gosline 2023）：Tropical 5D 野生型；4 hpf 酶法脱膜→6 hpf 单胚入 96 孔板（90–100 µL）→避光静态暴露至 120 hpf；6–10 个浓度；终点 = 24 hpf 胚胎光运动反应（EPR，自研 PRAT）+ 24 hpf 死亡/发育/自发运动/脊索 + 120 hpf 形态学（22 终点）+ 120 hpf 光暗运动反应（LPR，ZebraBox，3 分钟光/暗循环）；质控 = 阴性对照发病/死亡 <20%，每日乙基对硫磷阳性对照，不合格批次重做。
- **通量标尺**：1,060 个 ToxCast 化学品（2014）；139 个 PFAS（2022）；61 个阻燃剂（2020）；403 个抗病毒化合物（2024）；R35 目标"数百万胚胎×10,000 化学品"。
- **公开数据与工具**：SRP Analytics Portal（srp.pnnl.gov；Sci Data 2023, 10.1038/s41597-023-02021-5；GitHub PNNL-CompBio/srpAnalytics）；bmdrc Python 包（BMD 建模，PLoS Comput Biol 2025）；FINS 形态评分平台（SLAS Technol 2026，apps.sciome.com/fins）；斑马鱼自监督图像基础模型（46.8 万图，SLAS Technol 2026）；Kestrel 24 相机阵列显微镜（96 孔全板成像，SLAS Technol 2025）；深度自编码器行为模式识别（PLoS Comput Biol 2024）。
- **合作网络**：实验室核心 Lisa Truong、Michael Simonich；OSU 的 Kim Anderson（被动采样）、Jennifer Field（PFAS 化学）、Thomas Sharpton（微生物组）；PNNL 的 Waters/Gosline（组学门户）；NCSU 的 David Reif（生物信息）；WHOI 的 Hahn/Karchner（AIP）；Sciome 的 Shah（AI）。

---

## 2. 学术思想蒸馏（基于论文与基金摘要的归纳，非原话）

### 2.1 核心主张
1. **用整体脊椎动物做"第一层级"筛查，才能看到细胞体系看不到的危害**。ToxCast 全库 487 个化学品引起显著不良反应，"多终点同时测量使整个系统成为化学危害的生物传感器"（Truong 2014）；2026 多实验室研究：斑马鱼行为检测作为 DNT 第一层级全生物体 NAM，检出 93% DNT 阳性与 100% 阴性，特异性高于 13 项体外 DNT 组合（60%）。
2. **化学结构决定生物活性，这是可学习、可预测的**。R35 总目标"仅凭结构预测毒性、靶点和通路网络"；阻燃剂分类模型平衡准确率 91.7%。
3. **行为是比形态更早、更灵敏的发育毒性指标**。24 hpf 行为反应预测 5 dpf 的 17 种畸形和死亡，且常在更低浓度出现（Reif 2016）。
4. **暴露方法学本身就是科学变量**。数字点样优于枪头移液（Truong 2016）；脱膜/光周期/换液改变有效浓度（Wilson 2020）；半挥发物需旋转密封玻璃瓶（Morshead 2025）；体内负荷排序会改变危害排序（Rude 2025）；SEAZIT 跨实验室 78.6% 一致（Hamm 2024）。
5. **表型锚定的机制研究**：先看到表型，再在表型出现前取样转录组形成靶点假设，用 CRISPR 验证（R35 摘要；retene/Cyp1a/Cyp1b1 2024）。
6. **AHR 信号的下游与个体敏感性是长期主线**：slincR lncRNA 抑制 sox9b；AIP 突变改变 AHR 配体敏感性。

### 2.2 方法论签名
- 单胚入孔+脱膜+全终点二元打分+BMD/LEL 固定流水线，每日阳性对照与板质控。
- 多维读出：24 hpf EPR → 120 hpf 形态（约 18 项）→ 120 hpf LPR → 靶向/全转录组。
- 面向化学类别的"文库式"设计，以结构-活性关联取代逐个化学品叙事。
- 与剂量学联用：体内负荷实测、BMD 建模、暴露方法比较。
- 遗传工具：CRISPR 敲除系（ahr2、cyp1a、cyp1b1、aip、slincR）确认因果。
- 系统性引入 AI 与自动化（FINS、自编码器、基础模型、相机阵列）。
- 与环境化学联用回应社区需求（波特兰港、俄勒冈饮用水）。

### 2.3 研究范式演变
1. **1997–2005 AHR/二噁英机制**（F32、R01ES010820 鳍再生、R21 胎儿乙醇）。
2. **2008–2014 纳米材料与 PAH**（R01ES016896；P42 项目 3）。
3. **2010–2016 高通量平台化**（RC4"每日 10,000 尾"；EPA R835168 千种化学品+转录组；ToxCast 2014）。
4. **2015–2021 机制深化与数据整合**（slincR；NHIR 纳米联盟 U01）。
5. **2021–至今 预测毒理学与 NAM 定位**（R35 RIVER；P42 第三周期；2025 ToxPoint；多实验室行为验证）。
6. **2024–2026 新分支**：AI 图像/行为分析；PCB 代谢物与取代位点构效；真实环境样品；AIP 遗传学。

---

## 3. 代表作精读（8 篇，署名以 PubMed 为准）

**R1. Truong L, …, Tanguay RL (2014). Multidimensional in vivo hazard assessment using zebrafish. *Toxicol Sci* 137:212–33.** DOI: [10.1093/toxsci/kft235](https://doi.org/10.1093/toxsci/kft235)
1,060 个 ToxCast 化学品全库筛查；487 个诱导显著不良反应；对文献 18 个斑马鱼神经毒物检出 14 个（78%）。"多终点、全库、标准化"的方法学锚点。启示：把形态终点作为行为解读的混杂监控。

**R2. Mandrell D, …, Tanguay RL (2012). Automated zebrafish chorion removal and single embryo placement. *J Lab Autom* 17:66–74.** DOI: [10.1177/2211068211432197](https://doi.org/10.1177/2211068211432197)
一次自动脱膜 1,600 胚（4 hpf），成功率≥95%、死亡 2%。高通量胚胎筛查方法学出处（4 hpf，非 2 hpf）。

**R3. Reif DM, …, Tanguay RL (2016). High-throughput characterization of chemical-associated embryonic behavioral changes predicts teratogenic outcomes. *Arch Toxicol* 90:1459–70.** DOI: [10.1007/s00204-015-1554-1](https://doi.org/10.1007/s00204-015-1554-1)
24 hpf 行为预测 17 种 5 dpf 发育异常及死亡，常在更低浓度。"为什么要测 EPR"的核心证据。

**R4. Truong L, …, Tanguay RL (2016). Optimizing multi-dimensional high throughput screening using zebrafish. *Reprod Toxicol* 65:139–47.** DOI: [10.1016/j.reprotox.2016.05.015](https://doi.org/10.1016/j.reprotox.2016.05.015)
数字点样优于枪头移液；痕量杂质干扰敏感模型。行为实验批间差异常来自投放/吸附/杂质而非生物学。

**R5. Geier MC, …, Tanguay RL (2017/2018). Comparative developmental toxicity of a comprehensive suite of PAHs. *Arch Toxicol*.** DOI: [10.1007/s00204-017-2068-9](https://doi.org/10.1007/s00204-017-2068-9)（⚠️要点基于元数据）
较完整的 PAH 发育毒性比较；同系列 Knecht 2013（含氧 PAH）、Chlebowski 2017（硝化/杂环 PAH）。

**R6. Garcia GR, …, Tanguay RL (2017/2018). slincR 系列. *Mol Pharmacol* [10.1124/mol.117.108233](https://doi.org/10.1124/mol.117.108233)；*EHP* [10.1289/EHP3281](https://doi.org/10.1289/EHP3281)**
AHR 诱导的 lncRNA slincR 为 sox9b 抑制所必需；2023 年 CRISPR 突变系影响发育、行为和尾鳍再生（Toxicol Sci, 10.1093/toxsci/kfad050）。AHR 研究从"诱导了什么"转向"抑制了什么"。

**R7. Truong L, …, Tanguay RL (2022). Systematic developmental toxicity assessment of a structurally diverse library of PFAS in zebrafish. *J Hazard Mater* 431:128615.** DOI: [10.1016/j.jhazmat.2022.128615](https://doi.org/10.1016/j.jhazmat.2022.128615)
139 个 PFAS，10 浓度；35% 有活性；11 个改变 EPR、25 个改变 LPR、31 个改变形态；FOSA 唯一三类皆阳；PFDA 最强致畸。行为+形态同板联合解读的最新模板。

**R8. Gosline SJC, …, Tanguay RL, …, Waters KM (2023). The SRP Analytics Portal. *Sci Data* 10:151.** DOI: [10.1038/s41597-023-02021-5](https://doi.org/10.1038/s41597-023-02021-5)
HTS 数据按 FAIR 公开（BMD10/BMD50/AUC），链接环境样品与人类基因表达。

**补充经典**：Truong 2019 金纳米颗粒（10.1080/17435390.2019.1592259）；Wilson 2020 暴露方案变异（10.3390/toxics8040087）；Truong 2020 阻燃剂 61 种（10.1016/j.reprotox.2020.08.007）；Planchart 2016 ALTEX 小型鱼 HTS（10.14573/altex.1601281）。

---

## 4. 近期文章蒸馏（2024–2026，时间倒序；PubMed 共检出 34 条，选 15 项主题）

**1. 自监督斑马鱼图像基础模型 | SLAS Technol | 2026 | 10.1016/j.slast.2026.100471**——46.8 万图预训练（DINO/MAE+DINO），通吃形态分类/阶段预测/分割。启示：形态与行为数据的标注成本将被可复用编码器拉低。

**2. 斑马鱼行为评估作为 DNT 第一层级全生物体 NAM：多实验室评估 | Neurotoxicology | 2026 | 10.1016/j.neuro.2026.103504**——4 实验室×33 化合物 LDTT；三级质控剔除 10.9% 的"合格"板；DNT 活性判断实验室间一致 68–84% 但效价估计相近；检出 93% DNT 阳性/100% 阴性。**启示（本库最重要）：可复用的三级板质控框架；"活性判断因实验室而异、效价排序稳定"→论文应优先报告 BMC 而非仅是否有效。**

**3. FINS 自动形态评分平台 | SLAS Technol | 2026 | 10.1016/j.slast.2026.100426**——CNN+人工校正+图像质控，标注时间减 70%。

**4. AIP 系列三连 | Toxicol Sci 10.1093/toxsci/kfag033；Front Toxicol 10.3389/ftox.2026.1875384；Toxics 10.3390/toxics14090807 | 2026**——aip 纯合突变斑马鱼 7–12 dpf 死亡；对 PCB126/TCDD 敏感性降低、对来氟米特升高（配体依赖）；约 1,000 差异基因、应激性造血表型。启示：AHR 个体易感性的新遗传工具；行为终点须避开 7–10 dpf 致死窗。

**5. BaP 甲基取代位点驱动 AHR 依赖鳍重复 | Toxicol Sci | 2026 | 10.1093/toxsci/kfaf164**——8-甲基-BaP 0.26 µM 即致鳍重复，7/6/9/10-甲基无此作用；依赖 Ahr2、Cyp1a 保护。启示：单个甲基位置改变表型谱，"取代位点"应为设计变量。

**6. PCB 代谢物形态/行为/转录组 | Toxics | 2026 | 10.3390/toxics14050444**——羟基/硫酸酯代谢物比母体更低浓度起效；行为异常通常与形态效应同现。启示：报告行为 DNT 时同时公布形态学判断，防止把一般毒性当神经特异性。

**7. 俄勒冈饮用水/波特兰港真实样品 | ES&T 10.1021/acs.est.6c01661；Environ Pollut 10.1016/j.envpol.2026.128103 | 2026**——疑似物筛查+斑马鱼形态/行为毒性+社区驱动框架；自来水中 1 单体+7 混合物引起行为改变。

**8. 砷+甲基汞亲代共暴露跨代神经行为 | Environ Toxicol Pharmacol | 2026 | 10.1016/j.etap.2026.104970**——F0 共暴露致 F0 成鱼与 F1 幼鱼行为改变（相加），F2 无；as3mt 与 DNA 甲基转移酶差异。启示：多代+成幼双行为设计的参照。

**9. ToxPoint：斑马鱼作为 NAM 的不可或缺角色（独著）| Toxicol Sci | 2025 | 10.1093/toxsci/kfaf121**——其当前立场最直接的文本（⚠️摘要缺失，建议读原文）。

**10. 烷基萘构效与旋转密封瓶暴露法 | Environ Int | 2025 | 10.1016/j.envint.2025.109837**——密封玻璃瓶检出 96 孔板看不到的毒性；logKow 与体内负荷预测不佳提示非麻醉机制。启示：半挥发/易吸附物质用普通板会低估行为效应。

**11. 表型锚定转录组跨农化品 | Front Toxicol | 2025 | 10.3389/ftox.2025.1675060**——48 hpf 取样（表型前）；DEG 数与表型严重度不相关；特异表达汇聚到神经发育/细胞骨架通路；神经发育 GO 注释有缺口。启示：转录组强度≠表型强度；通路富集解读要谨慎。

**12. Kestrel 相机阵列 EPR | SLAS Technol | 2025 | 10.1016/j.slast.2025.100310**——96 孔同时成像；**有膜与脱膜胚胎检出等同，可不再脱膜**。启示：若被独立验证，EPR 的脱膜前置步骤可能取消。

**13. bmdrc Python 包 | PLoS Comput Biol | 2025 | 10.1371/journal.pcbi.1013337**——按 EPA 指南处理形态/行为比例数据的 BMD 建模，开源。可直接用于行为"比例型"终点。

**14. PAH 混合物生物剂量学模型 | Toxicol Sci | 2025 | 10.1093/toxsci/kfaf039**——体内负荷预测（混合物 83% 落在 2 倍内）；按 AUC 排序改变危害排序。启示：名义浓度可能误导效价排序。

**15. retene 的 AHR 依赖毒性需代谢活化 | Toxicol Sci | 2024 | 10.1093/toxsci/kfae098**——体外报告基因阴性但体内 Ahr2 依赖；Cyp1a 敲除增敏、Cyp1b1 敲除减敏；敏感窗 24–48 hpf。启示：体外受体阴性≠体内无 AHR 依赖。

**16. 深度自编码器行为模式识别 | PLoS Comput Biol | 2024 | 10.1371/journal.pcbi.1012423**——以未暴露幼鱼"正常行为"为基线做异常检测，发现 3 个"移动距离"指标漏掉的活性 PFAS。**启示：只看移动距离会漏效应；可借鉴异常检测思路——与 zfbehavior 指标设计直接相关。**

**17. PFAS 转录组 | Front Toxicol | 2024 | 10.3389/ftox.2024.1425537**——15 个活性 PFAS 多数影响脑/神经发育基因集；支持把神经行为作为 PFAS 筛查必选项。

**18. SEAZIT 跨实验室发育毒性比对 | Toxics | 2024 | 10.3390/toxics12010093**——3 实验室×42 物质×4 暴露条件；78.6% 活性判断一致。

**其他**：Morshead 2024 综述（10.1016/j.cotox.2024.100516）；Truong 2024 抗病毒 403 化合物（10.1007/s00204-024-03948-3）；Perone 2025 Cyp1b1 敲除眼脑代谢组与神经行为（10.1016/j.taap.2025.117246）；Sharpton 组微生物组×BaP 行为（10.3390/toxics13010010；10.1038/s41598-024-65610-3）；bioRxiv 2026-08 转录组外推预印本（10.64898/2026.08.07.743325，未经同行评议）。

---

## 5. 基金档案

> **数据源**：NIH RePORTER API（PI 档案 ID 1953223，返回 118 条年度记录）；EPA NCER。查询日 2026-10-28。注意：P42 总中心与子项目记录并存，不可直接相加。NSF：未能检索到。

### 5.1 联邦基金清单（PI/联系 PI）

**当前有效**
| 项目号 | 题目 | 机构 | 年限/金额 |
|---|---|---|---|
| P42ES016465（总中心+项目+行政核心） | Center for the Science, Technology, and Emerging Health Risks of PAHs；研究项目现名 Predicting the Toxicity of PAHs | NIEHS SRP | 2009 起，当前周期至 2030-01；FY2026 总中心 $3.06M |
| R35ES031709（RIVER） | Discovering Chemical Activity Networks – Predicting Bioactivity Based on Structure | NIEHS | 2021-07 至 2029-06；FY2021–26 合计约 $5.21M |
| C06OD036081 | SPF 斑马鱼核心设施现代化（SARL 改造） | NIH OD | 2023–2028；$7,528,453 |
| P30ES030287 | OSU 环境健康科学核心中心行政核心 | NIEHS | 2020 起，记录至 2026-03（续期状态⚠️待核） |

**已结束（节选）**：U01ES027294 纳米联盟（2016–22）；R01ES030017 slincR（2019–22）；R21ES025421（2015–17）；R01ES016896 金纳米颗粒（2008–14）；RC4ES019764 自动化高通量实验室（2010–13，FY2010 $1.86M）；R21ES018970 BPA/ERRγ（2010–12）；P30ES000210 水生模型设施核心（FY2007–14）；R01ES010820 鳍再生/二噁英（2000–05）；R21AA012783 胎儿乙醇（2001–03）；F32ES005786（1997–98）；EPA R835168 斑马鱼毒性筛查（2012–16，$1.2M）。

### 5.2 摘要要点蒸馏（RePORTER/EPA 摘录）
- **RC4（2010）**："每天至少暴露 10,000 尾斑马鱼于文库化合物"，对标啮齿类成本。
- **EPA R835168（2012）**：≥1,000 化学品形态+行为，效应后全转录组找起始靶点；假设斑马鱼对某些类别比细胞测定更贴近啮齿类。
- **P42 总中心（2025）**：使命"识别环境 PAH、描述毒性、给出不危害人类健康的环境浓度"；核心问题含烷基化 PAH 剂量、混合物相加/协同/拮抗成分识别、遗传多态性与易感个体。
- **R35 RIVER（2021）**：数百万胚胎×10,000 Tox21 化学品→表型前转录组→CRISPR 验证→机器学习构效→公共数据库→与人细胞比较→3R。
- **R01ES030017**：slincR 为 AHR 诱导 sox9b 抑制所必需，在出血与软骨缺陷中起因果作用。

### 5.3 问题意识演变（基于基金摘要推断）
1. **"AHR 如何介导二噁英毒性"（1997–2005）**→ 2. **"什么理化性质预测生物相互作用"（2008–2014，纳米+PAH）**→ 3. **"能否把整个化学品库放进活体筛查"（2010–2016，RC4+EPA）**→ 4. **"下游到底是什么"（2015–2022，slincR/数据整合）**→ 5. **"混合物与真实环境"（2020–，烷基 PAH/剂量学/场地样品）**→ 6. **"预测毒理学与替代动物"（2021–2029+，R35 以结构预测一切，斑马鱼自身定位为 NAM）**。

---

## 6. 趋势判断

1. **斑马鱼行为/形态测试正从"实验室特色"走向"可审计的监管级 NAM"**（SEAZIT 2024 → 多实验室 LDTT 2026 → ToxPoint 2025 → R35 的 3R 表述）。推断：2–3 年内会出现把斑马鱼行为纳入分层 DNT 策略（IATA）的指南性文件。
2. **AI 驱动的图像/行为/转录组分析成为产出新重心**（自编码器 2024、FINS/基础模型 2026、转录组外推预印本）。推断：板质控与成像格式标准化将成合作前提。
3. **对象从单一母体转向取代/代谢物/混合物/真实样品**（烷基萘、甲基-BaP、PCB 代谢物、饮用水/Superfund 水体）。剂量学与暴露器皿会更频繁进入方法部分。
4. **AHR 遗传易感性是机制线核心增长点**（2026 年 aip 三连发）。推断：个体敏感性将取代群体平均成为 PAH/二噁英主问题。

---

## 7. 专家视角 Persona（基于其文献的评审式提问，属推断）

1. "你的浓度是名义还是实测？化合物吸附塑料或挥发吗？请给体内负荷或方法对照。"
2. "行为改变是否伴随形态异常？若是，还算神经特异性吗？先报形态学判断。"
3. "有没有第二实验室、第二批板验证**效价**（而非仅是否有效）？"
4. "阴性/阳性对照每日运行了吗？板质控标准写进方法了吗？"
5. "24 hpf 还是 120 hpf 读数？哪个预测后期结局？"
6. "体外受体报告基因阴性≠体内无 AHR 依赖——代谢激活排除了吗？"
7. "除了移动距离，看过行为模式吗？异常检测能发现均值之外的效应。"
8. "测了几个结构类似物？单化合物结论说明不了结构决定什么。"
9. "转录组在表型出现之前取样了吗？表型之后的样本多半是后果不是原因。"
10. "数据和代码公开了吗？能否用 BMD 而不是显著性表达？"

---

## 8. 元数据

**定期检索式**：PubMed `Tanguay RL[Author] AND zebrafish`（按日期）+ `Tanguay R[Author]` 变体 + `Tanguay RL[Author] AND (PFAS OR PAH OR "aryl hydrocarbon")`；NIH RePORTER `pi_profile_ids=[1953223]`；bioRxiv "Tanguay zebrafish"。

**信息源**：PubMed；NIH RePORTER API；EPA NCER；PMC 全文（Truong 2014、Gosline 2023）；OSU 新闻/Daily Barometer；TAMU HIAS；SOT ToxChange；Wikipedia（二手）。

**置信度**：论文与基金记录——高；职务头衔——中；荣誉年份——中；见下待核实项。

**待核实项**：①各论文通讯作者身份；②SOT 副会长当选；③ToxPoint 内容要点（摘要缺失）；④P42 早期总 PI 与 P30 续期状态；⑤陆军工程兵团小项目；⑥R35 承诺的公共数据库上线状态；⑦论文总数口径（200+/300+）。

**同名排除**：Robert L.（2019 前）与 Robyn L. 为同一人；拉瓦尔大学 Robert M. Tanguay（热休克蛋白）需用单位区分；注意区分 Lisa Truong 与 Truong HD、Michael T. 与 Staci L. Massey Simonich。边缘条目（MOF 造影剂、文献计量、生物修复）仅为合作者，已排除。
