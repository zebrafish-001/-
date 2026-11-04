# Tamara Tal — 亥姆霍兹环境研究中心 UFZ（生态毒理学部）/ 莱比锡大学
> 领域标签：斑马鱼早期生命阶段行为表型组 · 发育神经毒性 NAM（DNT IVB） · 神经活性化学品靶点反推 · 化学品-微生物组交互 · PFAS 神经毒性 | 主领域：A/D | 档案建立：2026-11-04 | 检索覆盖至：2026-10

> 说明：本档案只收录检索中实际看到的文献/页面；无法核实处标注“⚠️待核实”。PubMed 元数据经 mcp__PubMed 获取（共核实 26 条 PMID）；UFZ 个人主页、EurekAlert 新闻稿、PMC 全文（EHP 2026，PMC13445272）经 WebFetch/Europe PMC 读取。

## 1. 基本信息

### 1.1 履历时间线（含来源）
| 时间 | 单位/身份 | 来源 |
|---|---|---|
| 1998–2003 | University of Central Florida Honors College（页面未列学位） | UFZ 个人主页 |
| 2003–2008 | PhD，Curriculum in Toxicology，UNC Chapel Hill | UFZ 个人主页（UNC 校友页检索时 503，⚠️未读到） |
| 2008–2011 | NIEHS 博士后（T32），Oregon State University（Tanguay 实验室，Dept. Environmental & Molecular Toxicology） | UFZ 主页；PubMed 22253472 署名 OSU |
| 2011–2015 | US EPA 博士后（R-Authority Postdoctoral Fellow） | UFZ 主页 |
| 2015–2019 | US EPA ORD/NHEERL/ISTD（Integrated Systems Toxicology Division），RTP, NC，Principal Investigator | UFZ 主页；PubMed 31504981、28894128 |
| 2019– | UFZ Leipzig，Molecular Toxicology 课题组组长（Dept. Bioanalytical Ecotoxicology，后期署名为 Department of Ecotoxicology, Chemicals in the Environment Research Section） | UFZ 主页；PubMed 署名 |
| 2021– | 莱比锡大学医学院 Professor of Integrated Systems Toxicology | UFZ 主页；PubMed 署名 “Medical Faculty, University Leipzig” |

**署名单位变化（已核实）**
- 2012：Oregon State University（22253472，署名 Tamara L. Tal）。
- 2017–2020：U.S. EPA/ORD/NHEERL/ISTD, RTP（28894128, 31068624, 30321396, 31504981）；2020-04 的 GenX 论文（32271623）仍署 “ISTD, NHEERL, ORD, U.S. EPA”（投稿时间在前）。
- 2019-11 的 Neurotoxicology 综述（31783042）：单位仍为 US EPA ORD，但通讯邮箱已为 tamara.tal@ufz.de——处于 EPA→UFZ 过渡期的标志。
- 2020 起：Bioanalytical Ecotoxicology Dept., UFZ（32656393）；2021 的 Animal Microbiome 论文（33499997）同时标注 EPA CCTE（RTP）作者单位与 UFZ “Present Address”，说明 EPA 时期实验的论文延至 2021 才发表。
- 2024：署名出现 “Medical Faculty, University Leipzig”（39046251、38742231），2025–2026 起系部名多为 “Ecotoxicology Department / Department of Ecotoxicology”。
- 同名排歧：2012–2013 论文署 “Tal TL” 为同一人（OSU，Tanguay 实验室）。

### 1.2 平台资源盘点
**行为测试平台（据 EHP 2026 PMC 全文方法部分，已读）**
- 设备：ViewPoint ZebraBox + ZebraLab 软件，“quantization mode”（灵敏度阈值 15），25 帧/秒，以 Δpixel/s/孔为运动量；红外持续照明；28 °C。
- 板型：96 方孔透明聚苯乙烯平底板（Cytiva），每孔 1 尾 5 dpf 幼鱼，200 μL 标准稀释水，Bio-Rad microseal ‘A’ 封膜 + 板盖；1–4 dpf 在胚胎培养，筛选“存活、已孵化、形态正常、后部鱼鳔充气”幼鱼上板；14 h 光/10 h 暗周期，28 °C。
- 暴露：5 dpf 加化合物，溶剂 DMSO 终浓度 0.01%（EHP 2026）/ 0.4%（PFOS 系列；急性 60 min 或发育 1–4 dpf），行为采集前孵育 25 min；采用两个时间错开的产卵单元以控制昼夜节律影响。
- 刺激：可见光 100% = 7.5 klux（LI-250 光度计标定）；声刺激 300 Hz，65 dB（ASR1）与 75 dB（ASR2、ASR3、ASH1–5）；先 21 min 适应（1 min 亮 + 20 min 暗）。
- 电池：EHP 2026 版为 11 个行为指标——BSL 基线、VSR1/2 视觉惊跳、VMR1–3 视觉运动反应、ASR1/2 听觉惊跳、ASH1 听觉惊跳习惯化、ASH1/5 习惯化增强、ASR2/3 记忆保持；30 次高强度声刺激 ISI = 1 s 诱发指数衰减型习惯化。
- 26 终点版 VAMR（Neurotoxicology 2025 Herold）：视觉运动反应、视觉/听觉惊跳、习惯化学习、记忆保持；5159 尾对照幼鱼做终点相关性分析。
- 统计：以中位数差为统计量的非参数 bootstrap（B = 10,000，双侧），多重比较用 Kruskal-Wallis + agricolae 紧凑字母 + Benjamini-Hochberg 校正（p adj < 0.05）；效应量 SSMD（基于中位数与 MAD）；SSMD 轮廓作行为指纹，ComplexHeatmap 层次聚类、MDS；“hit” 定义：ASH1 在至少一个浓度显著升/降。DNT IVB 比较论文用 GAM / 线性混合效应模型 + Fréchet 距离（Spath 2026）。
- 品系线索：全文讨论中提到 AB 与 WIK 品系习惯化差异，并称“未来需检验更常用野生型品系”，暗示其主要用品系需要在原文核实 ⚠️待核实（本次未直接读到品系名）。
- 微生物组平台（EPA 时期继承）：无菌（AX）/常规定植（CC）/第 1 天重定植（AC1）幼鱼；SIHUMIx（七菌株人源简化菌群）体外-体内整合（Wray 2026）。
- 跨物种验证链：小鼠皮层神经元（P0–P1 培养，DIV 15–16 膜片钳，HEKA EPC10）；人 iPSC 来源 BrainSphere + Axion Maestro Pro MEA（hMNR 多神经递质受体检测，与 E. Fritsche/IUF 合作）；in silico 靶点预测。

**公开数据/代码（据 UFZ 主页出版物清单与论文数据声明）**
- figshare：行为数据 10.6084/m9.figshare.26819890；分析代码 10.6084/m9.figshare.26819914（EHP 2026 数据可用性声明）。
- Zenodo：PFOS-GABA 数据集 10.5281/zenodo.15394336；农药（蜜蜂+斑马鱼）数据集 10.5281/zenodo.16983482；偶氮嘧菌酯微生物组数据集 10.5281/zenodo.18433571。
- Mendeley Data：原油分馏物化学与行为指纹数据 10.17632/8hmr85pjw7.3。
- 软件：UFZ 主页列有 “NeuroBEAT behavior analysis tool” 会议摘要（Toxicol Lett 411 Suppl. 2025，DOI 10.1016/j.toxlet.2025.07.282）；GitHub/Zenodo 上的 NeuroBEAT 仓库本次未能检索到 ⚠️待核实。

### 1.3 合作网络（据共同作者与项目页）
- UFZ 内部：Stefan Scholz、Nadine Schweiger/N. Schweiger、Nico Jehmlich 与 Martin von Bergen（蛋白质组/微生物）、Ana Zenclussen（ENDOMIX 协调人）、Janet Krüger（技术）、Gi Mick Wu（统计）。
- 神经毒性 NAM：Ellen Fritsche（IUF Düsseldorf，DNT IVB / BrainSphere，EHP 2026 与 PARC 共同基金持有人）、Marcel Leist（ALTEX 2025 DNT 大会总结作者之一）、Kristina Bartmann。
- 微生物组：Charles R. Tyler（Exeter，Toxicol Sci 2026 末位作者之一）、Ulrike Rocha / Anke Ebert（N-EtFOSA 论文）。
- EPA 时期：Charles E. Wood、Tara Catron、Drake Phelps、Adam Swank、Scott Keely、Nichole Brinkman、Emily Wheaton（EPA NERL）、Leah Wehmas、Shaza Gaballah；外部 John F. Rawls（Duke，无菌斑马鱼）、Regina Lamendella（Wright Labs/Juniata，16S）。
- 美国同行：Robert Tanguay（OSU，博后导师）、Pamela Lein（Translational Toxicology in Zebrafish 共同作者）、David C. Volz。
- 近期学生/博后（据论文署名）：David Leuthold（EHP 2026 一作；2026 SOT 最佳博后论文奖，据 PARC 新闻页）、Nils K. Herold、Sebastian Gutsfeld、Jana Spath、Cassidy Wray 等。

## 2. 学术思想蒸馏

### 2.1 核心主张
1. **斑马鱼早期幼鱼是填补“神经毒性测试真空”的 3R 友好脊椎动物 NAM。** 依据：EHP 2026 摘要“化学品释放速度超过评估能力”；EurekAlert 新闻稿引语“监管机构对斑马鱼毒性数据普遍持怀疑”，需“建立信心”。
2. **单一终点不够，需要多行为表型（含习惯化与记忆）才能抵达“高阶”神经功能。** 依据：Herold 2025（26 终点；5159 尾对照相关性分析显示学习/记忆类终点提供独特信息）。
3. **行为指纹 + 参照化学品库可反推作用模式（MoA）。** 依据：63 个参照化学品的 SSMD 轮廓聚类；GABA-A 拮抗剂引起“暗期镇静 + 惊跳增强”，激动剂方向相反。
4. **跨物种机制验证链是赢得监管信任的关键。** 依据：斑马鱼→小鼠皮层神经元膜片钳→人 BrainSphere（PFOS、chlorophene 两例）。
5. **VAMR 可补充 DNT IVB 的假阴性与灵敏度。** 依据：Spath 2026——12 个 DNT 阳性物质，VAMR 命中浓度较 DNT IVB 低 1–4 个数量级；DNT IVB 对 5,5-二苯乙内酰脲、代森锰、尼古丁为假阴性。
6. **化学品-微生物组-宿主三角关系应纳入危害识别。** 依据：EPA 时期 E2、BPA 类似物、三氯生；UFZ 时期 N-EtFOSA、偶氮嘧菌酯（微生物组决定行为表型与毒代）。

### 2.2 方法论签名
- 96 孔单鱼单孔、固定 5 dpf、多刺激模块串联（光暗转换、声惊跳、习惯化、潜伏/记忆）在同一块板内。
- 非参数 bootstrap + SSMD 效应量 + Kruskal-Wallis/BH；指纹层次聚类 + MDS 作可视化与 MoA 假设生成。
- 靶点反推三联：参照库指纹相似性 → in silico 靶点预测 → 药理学拯救/共暴露（如 propofol 或 CGP13501 拯救 PFOS 的高活动）。
- CRISPR crispant（F0）验证（ppar 基因敲降，Gutsfeld 2024）+ RNA-seq 转录组 BMC 建模。
- 无菌/重定植对照 + 化学分析（FOSA、FOSAA 代谢物）确定微生物组依赖性。
- 数据与代码开放（figshare/Zenodo/Mendeley）。

### 2.3 研究范式演变
- **OSU（2008–2011）**：miRNA 控制神经行为发育（乙醇暴露→光暗运动过度；miR-9/9*、miR-153c 敲降复制表型）——“表型锚定的机制”。
- **EPA（2011–2019）**：转向“化学品-微生物组”与 PFAS（GenX 发育毒性/DNT/组织剂量），仍主要用 10 dpf 光暗运动单一指标。
- **UFZ 早期（2019–2022）**：综述性/观点性输出（非哺乳动物 DNT 模型、转化毒理学、PFAS 生物富集），建立 Helmholtz W2 课题组。
- **UFZ 近期（2023–2026）**：多行为电池（26 终点）→ 行为指纹 → 靶点反推（GABA-A、Kv7、PPARδ）→ 与 DNT IVB/OECD 路径对接（PARC WP5）→ 回到微生物组（N-EtFOSA、SIHUMIx），形成“方法学—机制—监管”三层结构。

## 3. 代表作精读（8 篇）

1. **Tal TL, Franzosa JA, Tilton SC, …, Tanguay RL. 2012.** *MicroRNAs control neurobehavioral development and function in zebrafish*（FASEB J 26:1452–61，DOI 10.1096/fj.11-194464）。乙醇暴露使幼鱼在光照变化下运动过度，并持续到幼年；miR-9/9* 与 miR-153c 敲降复制该行为。意义：奠定“发育扰动→持久行为表型”范式。
2. **Phelps D…Rawls JF, Tal T. 2017.** *Microbial colonization is required for normal neurobehavioral development in zebrafish.* Sci Rep 7:11244. DOI 10.1038/s41598-017-10517-5。无菌幼鱼 10 dpf 过度活跃；1–6 dpf 重定植可恢复，9 dpf 不行；Aeromonas veronii 或 Vibrio cholerae 单菌足够；热灭活菌/MAMPs 不足。意义：微生物组发育关键窗口，为毒理实验“菌群背景”设限。
3. **Catron TR…Tal T. 2019.** *Host Developmental Toxicity of BPA and BPA Alternatives Is Inversely Related to Microbiota Disruption in Zebrafish.* Toxicol Sci 167:468–483. DOI 10.1093/toxsci/kfy261。BPAF>BPB>BPF≈BPA>BPS 的宿主毒性次序；BPS/BPA/BPF 扰动微生物群而 BPB/BPAF 不扰动，二者呈反比。
4. **Catron TR…Tal T. 2019.** *Microbiota alter metabolism and mediate neurodevelopmental toxicity of 17β-estradiol.* Sci Rep 9:7064. DOI 10.1038/s41598-019-43346-9。定植 E2 暴露幼鱼光期活动下降，无菌幼鱼正常；无菌幼鱼体内 E2 更高，磺化/葡糖醛酸化代谢物趋势不同。意义：微生物组影响毒代动力学，进而决定行为表型（N-EtFOSA 论文的前身逻辑）。
5. **Weitekamp CA…Tal T. 2019.** *Triclosan-Selected Host-Associated Microbiota Perform Xenobiotic Biotransformations in Larval Zebrafish.* Toxicol Sci（2019-11，PMID 31504981；署名 U.S. EPA/ORD/NHEERL/ISTD；卷页与 DOI 本次未读取，⚠️待核实）。摘要未读取，内容仅据标题：三氯生选择出的宿主相关微生物在幼鱼体内执行外源物生物转化。
6. **Gaballah S…Tal T. 2020.** *Evaluation of Developmental Toxicity, Developmental Neurotoxicity, and Tissue Dose in Zebrafish Exposed to GenX and Other PFAS.* Environ Health Perspect 128(4). DOI 10.1289/EHP5843。PFAS 发育毒性、DNT 和组织剂量联合评估。（UFZ 主页称“2020 Paper of the Year, SOT MSB”，具体对应论文 ⚠️待核实）。
7. **Gutsfeld S…Scholz S, Schor J, Tal T. 2024.** *Investigation of PPAR genes as requirements for visual startle response hyperactivity in larval zebrafish exposed to structurally similar PFAS.* Environ Health Perspect. DOI 10.1289/EHP13667。发育（1–4 dpf）而非急性 PFOS 暴露引起不可逆至 8 dpf 的 VSR 过度反应；RNA-seq 提示 ppar 为上游调节因子；ppard 敲降与拮抗剂 GSK3787 可使 PFOS 的 VSR 过度反应降至对照水平。意义：给出新的 AOP（“PFOS→ppard 依赖→VSR 过度反应”）。
8. **Herold NK…Tal T. 2025.** *Multi-behavioral fingerprints can identify potential modes of action for neuroactive environmental chemicals.* Neurotoxicology. DOI 10.1016/j.neuro.2025.05.001。26 终点 VAMR + 63 参照化学品；NMDA/GABA-A 靶向物降低习惯化；PPARδ/γ、GABA、多巴胺、ryanodine、AhR、GPCR、SRC 靶向物“不当加速”习惯化；环境化学品林丹/狄氏剂（GABA 拮抗）、TBBPA（激动）符合预测指纹。

## 4. 近期文章蒸馏（2024–2026，时间倒序）

### 4.1 Leuthold D, Herold NK, Nerlich J, …, Schweiger N, Fritsche E, Tal T. 2026（EHP，2026-06；PMID 42564692；DOI 10.1021/EHP.6c00394）
*Multibehavioral Phenotyping in Early-Life-Stage Zebrafish for Identifying Disruptors of Nonassociative Learning.*
- 要点：11 指标电池；已知习惯化调节剂产生可区分行为模式；筛 NMDAR 阳性化学品，发现杀菌剂 chlorophene（镇静、反常兴奋、习惯化降低），经 in silico 靶点预测与药理干预确定作用于 GABA-A 受体（此前未知靶点），小鼠皮层神经元与人 BrainSphere 验证；行为轮廓类似 Kv7 激活剂 flupirtine，提示习惯化缺陷可能来自 M 电流而非 GABA-A。
- 备注：EurekAlert 新闻稿（2025-05-30）给出 DOI 10.1289/EHP16568（提前在线版），PMC 记录 Accepted 2025-05-15、Collection 2026-Aug；两种 DOI 版本并存，引用时以 PubMed DOI 为准 ⚠️待核实。
- **对斑马鱼行为毒理学研究者的启示**：
  1. 采用“习惯化 + 潜伏 + 记忆保持（ASR2/3）”而非单一光暗活动；声刺激 300 Hz，65/75 dB，30 次 ISI = 1 s 习惯化 bout，需在方法中报告标定方式（dB、klux）。
  2. 溶剂 0.01% DMSO、两个错时产卵单元、仅取“已孵化、形态正常、鱼鳔充气”幼鱼——可直接作为质控入选标准。
  3. 统计：中位数差 bootstrap（B=10,000）+ KW + BH，效应量报 SSMD（基于 MAD），避免正态假设。
  4. 机制链：药理共暴露/拯救 + in silico 靶点 + 膜片钳；本库若无电生理，可借 hMNR/MEA 公开合作或用拮抗剂-激动剂对照矩阵代替。
  5. 数据与代码：figshare（数据 + R 代码）公开，实验设计时应预留“可复现代码包”。

### 4.2 Gutsfeld S, Wray C, Schweiger N, …, Rocha U, Ebert A, Tal T. 2026（Environ Sci Technol 60(20)，2026-05；PMID 42128003；DOI 10.1021/acs.est.5c16330）
*N-Ethyl Perfluorooctane Sulfonamide (N-EtFOSA) Exposure Alters Microbiome Composition and Causes Microbiome-Dependent Behavior Effects in Larval Zebrafish.*
- 要点（Consensus 摘要）：幼鱼 5–6 dpf 暴露 PFOS（0.28–5 μM）、N-EtFOSA（0.07–1.25 μM）或 PFOSAmS（0.83–15 μM），8 dpf 暗期游泳改变；PFOS 与 N-EtFOSA 使群落结构类似偏移；AX 幼鱼不表现浓度依赖性低活动，AX 体内与水样 N-EtFOSA 更高；主要代谢物 FOSA 不依赖微生物组，FOSAA 在 AX 中更低。
- **启示**：
  1. 评估前体物（PFOS 前体）时需同时设 AX / CC / AC1 三组，才可区分“母体毒性”与“微生物转化产物毒性”。
  2. 暴露窗口 5–6 dpf、测试 8 dpf（含“暴露后恢复/延迟测试”设计），可借鉴为“暴露-洗脱-迟测”流程。
  3. 化学分析必须与行为同批取样（7 dpf 幼鱼+水样），以排除 AX 组暴露量差异造成的假象。
  4. 需记录并控制设施菌群；Weitekamp 2021 已指出设施微生物组差异会影响行为。

### 4.3 Spath J, Raab J, Schor J, Scholz S, Gutsfeld S, Tal T. 2026（Neurotoxicology，2026-03；PMID 41780647；DOI 10.1016/j.neuro.2026.103414）
*The zebrafish VAMR assay has the potential to add value to the DNT IVB.*
- 要点：DNT IVB 为 17 个人/啮齿类细胞检测；12 个 DNT 阳性物（5,5-二苯乙内酰脲、BDE-99、毒死蜱、氟哌啶醇、六氯酚、氯胺酮、代森锰、尼古丁、PFOA、戊唑醇、敌百虫、三乙基溴化锡）与 5 个预设阴性物，急性 40 min 与发育 1–5 dpf 两种暴露；26 终点；GAM/线性混合模型 + Fréchet 距离；VAMR 命中浓度常低 1–4 个数量级；可在不牺牲特异性前提下提高 IVB 灵敏度。
- **启示**：
  1. 同一批化学品做“急性 vs 发育”双暴露范式，是对接 DNT IVB 的标准写法。
  2. 浓度-反应用 GAM/混合模型 + Fréchet 距离量化整条曲线形状差异，比单点显著性更稳；可借鉴于多终点“命中判定”。
  3. 评价“补充价值”应报告灵敏度、特异性与效力（potency）三项，并明确 5 个阴性物。

### 4.4 Wray C, Castañeda-Monsalve V, Engelmann B, …, Tyler CR, Jehmlich N, Tal T. 2026（Toxicol Sci，2026-04；PMID 41795836；DOI 10.1093/toxsci/kfag022）
*Integration of human microbiota (SIHUMIx) and zebrafish models reveals microbiome-mediated host responses to azoxystrobin.*
- 要点：SIHUMIx 暴露于 ADI 10% 的偶氮嘧菌酯 7 天后恢复，宏蛋白组/代谢组显示功能重编程、短链脂肪酸下降；无菌/SIHUMIx 接种幼鱼 4 dpf 暴露 24 h 后用 VAMR 评估；偶氮嘧菌酯破坏习惯化学习（与菌群无关），但仅在定植幼鱼诱发暗期过度活跃（菌群依赖）；血清素在无菌幼鱼更低且被暴露拉向无菌水平。
- **启示**：同一次实验里习惯化表型“菌群无关”而暗期活动“菌群依赖”——提示不同终点有不同的菌群依赖性，应用多终点电池分层报告；建议检测血清素等神经递质作为机制中介。

### 4.5 Herold NK, Sørensen L, Creese ME, Nahrgang J, Schweiger N, Tal T. 2025（Environ Sci Technol 60(1)，2025-12；PMID 41424190；DOI 10.1021/acs.est.5c06859）
*Identification of Neuroactive Chemicals in Crude Oil-Derived Water-Accommodated Fractions.*
- 要点：WAF（1 g/L 装载，9.8–100%）及 PAH、树脂、萘、单芳烃、饱和烃分馏物，5 dpf 用 26 终点 VAMR 评估，表现暗期低活动、声惊跳受损、光期/间隔期不当活动；PAH/MAH/NAP 分馏物损害习惯化；GC×GC-MS 确认菲、2-甲基蒽等；人工混合物再现 WAF 行为；指纹预测涉及 PPARδ 或 GABA-A 信号。
- **启示**：复杂混合物“分馏—化学鉴定—人工重构混合物—指纹回溯”四步策略；对本库的环境样品行为毒理可直接套用。

### 4.6 Owen R, de Macedo G, Nerlich J, …, Gutsfeld S, Schweiger N, Tal T. 2025（Toxicol Sci 207(2)，2025-10；PMID 40700607；DOI 10.1093/toxsci/kfaf101）
*PFOS antagonizes GABA receptors in larval zebrafish and mammalian models.*
- 要点：5 dpf 急性暴露 7.87–120 μM PFOS，picrotoxin（GABA-A 拮抗）、propofol（GABA-A PAM）、saclofen（GABA-B 拮抗）、CGP13501（GABA-B PAM）；PFOS 暗期短暂过度活跃；propofol 或 CGP13501 可将其拯救至基线；PFOS 降低小鼠皮层神经元 GABA-A 电流，并升高 BrainSphere 中 GABA-A/B 依赖单元放电。数据 Zenodo 10.5281/zenodo.15394336。
- **启示**：“拮抗剂复制表型 + PAM 拯救”是靶点验证的最小实验集；急性窗口（暴露 60 min）可与发育窗口（见 Gutsfeld 2024）并列，揭示瞬时与不可逆效应的机制差异。

### 4.7 Uthoff C, Herold NK, Alkassab AT, …, Jehmlich N, Tal T, von Bergen M. 2025（Environ Int 203，2025-08；PMID 40897016；DOI 10.1016/j.envint.2025.109750）
*Cross-taxa sublethal impacts of plant protection products on honeybee in-hive and zebrafish swimming behaviours at environmentally relevant concentrations.*
- 要点：蜜蜂群内行为（第 3–10 天快照）与斑马鱼 26 终点 VAMR 并行；flupyradifurone 降低觅食与花蜜加工，boscalid、terbuthylazine 减少育幼行为；斑马鱼对 terbuthylazine 尤为敏感，混合物行为轮廓沿 terbuthylazine–boscalid 梯度偏移（混合比例参考德国溪流实测：boscalid 41.54%，terbuthylazine 58.45%）。数据 Zenodo 10.5281/zenodo.16983482。
- **启示**：以实测环境比例设计混合物；跨类群行为数据放同一框架对比，增强生态相关性论证。

### 4.8 Herold NK, Gutsfeld S, Leuthold D, Wray C, Spath J, Tal T. 2025（Neurotoxicology，2025-05；PMID 40354900；DOI 10.1016/j.neuro.2025.05.001）
见第 3 节第 8 条。
- **启示**：对照幼鱼 n = 5159 的终点相关性分析提供“内部质控基线库”；63 个参照化学品作为指纹字典——自建电池时应先建立类似的参照集（至少覆盖 GABA、NMDA、多巴胺、PPAR、AhR）并公开。

### 4.9 Celardo I, Aschner M, Ashton RS, …, Ückert AK, Whelan M, Leist M. 2025（ALTEX 42(2)；PMID 40235170；DOI 10.14573/altex.2503191）
*DNT: A call for implementation of new approach methodologies for regulatory purposes: Summary of the 5th International Conference on DNT Testing.*
- 要点：会议综述（Tal 为作者名单成员，⚠️具体位置待核实）；强调 NAM 应在监管中落地。
- **启示**：行为类 NAM 的下一步是“标准化 + 参照化学品 + 适用域”，而非继续增加终点。

### 4.10 Ayuk HS, Pierzchalski A, Tal T, …, Smith NM, Stojanovska V, Zenclussen AC. 2025（Environ Int，2025-03；PMID 40147139；DOI 10.1016/j.envint.2025.109409）
*Evaluating PFAS-induced modulation of PBMC immune response to SARS-CoV-2 spike in COVID-19 vaccinees.*
- 要点：与 ENDOMIX 免疫方向合作；非行为研究。
- **启示**：PFAS 的多系统评价（神经—免疫）可用于构建本库斑马鱼 PFAS 研究的 AOP 网络。

### 4.11 Gutsfeld S, Wehmas L, Omoyeni I, …, Scholz S, Schor J, Tal T. 2024（EHP，2024-07；PMID 39046251；DOI 10.1289/EHP13667）
见第 3 节第 7 条。
- **启示**：同时设“发育暴露 + 洗脱后追踪（5–8 dpf）”与“急性暴露”，才能分辨“可逆的药理性活动”和“不可逆的发育性损伤”；CRISPR F0 crispant 在 5 dpf 行为终点上可用，节省建系时间。

### 4.12 Tal T, Myhre O, Fritsche E, …, Spjuth O, Torres-Ruiz M, Bartmann K. 2024（Front Toxicol，2024-04；PMID 38742231；DOI 10.3389/ftox.2024.1359507）
*New approach methods to assess developmental and adult neurotoxicity for regulatory use: a PARC work package 5 project.*
- 要点：PARC WP5 项目 5.2.1e（神经毒性）；目标是 DNT-IVB v2.0 与首代成体神经毒性体外电池 ANT-IVB v1.0；斑马鱼（≤5 dpf、96 孔）含 DNT 模式（发育暴露后测试）与急性模式（神经发生后暴露），检测习惯化学习、逃逸反应、运动神经元毒性与类焦虑 thigmotaxis；质量依 GCCP 2.0 与 OECD GIVIMP；以 96 种化学品参照集评估适用域；BBB、胶质炎症、髓鞘形成、Cell Painting 等为新增模块；基金 Horizon Europe GA 101057014。
- **启示**：监管对接需要“DNT 模式 vs 急性模式”双范式、GIVIMP 式质控文档、参照集适用域评估——可作为本库建立斑马鱼行为 NAM 提案的框架。

### 4.13 仅见 UFZ 主页清单、未经 PubMed 独立核实的 2025–2026 条目（⚠️待核实）
- Toxicol Lett 411 Suppl（2025）会议摘要：NeuroBEAT 行为分析工具（10.1016/j.toxlet.2025.07.282）、PFAS 人源相关混合物行为效应（.07.165）、AHR 调节剂微生物组神经行为（.07.138）、PAHs 化学品-微生物组交互（.07.421）、原油分馏物行为指纹（.07.302）、斑马鱼微生物组对 PFOS 前体的生物活化（.07.425）、农药与帕金森神经变性的 defined approach（.07.916）。
- Neurogastroenterol Motil 37(S2)（2025）：巨噬细胞与肠神经元的高内涵成像（10.1111/nmo.70126）。
- PNAS 122(24)（2025）：EPA 研究办公室裁撤对安全与竞争力影响的评论（10.1073/pnas.2508060122；作者位置 ⚠️待核实）。
- Toxicol Lett 423（2026）：PFAS 对巨噬细胞蛋白质组（10.1016/j.toxlet.2026.112660）。
- Open Research Europe 4:271（2025）：ENDOMIX 项目综述（10.12688/openreseurope.19088.2）。

## 5. 基金档案
数据源与查询日期（均 2026-11-04）：UFZ 个人主页（授奖/项目栏）；EHP 2026 全文致谢；Frontiers 2024 全文；UFZ ENDOMIX 项目页；WebSearch 对 CORDIS、GEPRIS 的搜索。

### 5.1 项目清单
| 项目 | 年限 | 角色 | 编号/来源 |
|---|---|---|---|
| Helmholtz W2 Award “NEURO-XENO-MICROBIOME: Examining microbiome-xenobiotic interactions that affect host neurodevelopment” | 2021–2026 | PI | UFZ 个人主页；EHP 2026 致谢（T.T.）；编号未能检索到 |
| UFZ CITE TB College “MibiTox”（肠道微生物组、农药暴露与疾病） | 2020–2022 | 参与/负责人（页面只列条目，⚠️角色待核实） | UFZ 主页 |
| PARC（European Partnership for the Assessment of Risks from Chemicals）WP5 项目 5.2.1e 神经毒性 | 2022（Horizon Europe）起，具体年限 ⚠️待核实 | 项目一作与资助申请者（Frontiers 2024：conceptualization, funding acquisition, project administration） | Horizon Europe GA 101057014（Frontiers 2024；EHP 2026 致谢 T.T. 与 E.F.） |
| ENDOMIX（内分泌干扰物混合物与免疫） | 2024-01 起至 2027（据检索结果） | 开发“肠道炎症与肠神经系统发育的高内涵成像检测”（UFZ 项目页） | 协调人 Ana Zenclussen；编号 ⚠️未能检索到 |
| US EPA Pathfinder Innovation Project：“In vivo bioremediation of PFAS in zebrafish” | 2018–2019 | PI | UFZ 主页 |
| US EPA Pathfinder Stage Three：肠道微生物组与发育毒性 | 2016–2018 | PI | UFZ 主页 |
| US EPA Pathfinder Stage 1–2：同主题 | 2014–2016 | PI | UFZ 主页 |
| NIEHS T32 博后奖学金（OSU） | 2010–2011 | 博后 | UFZ 主页 |
- 荣誉：2020 SOT Molecular and Systems Biology 专业分会“年度论文”；2017 EPA STAA Level III；2015 SOT Emil A. Pfitzer 博后奖第一名；2014 EPA Bronze Medal；2026 SOT Pfizer Graduate Fellowship Award（据 PARC 新闻页，获奖者表述含混，⚠️待核实归属——更可能是学生获奖，Leuthold 获 Best Postdoctoral Publication Award）。
- 未能检索到：DFG GEPRIS 条目（搜索无命中，直接抓取返回空页）；PrecisionTox、ONTOX 中 UFZ/Tal 角色（检索未发现）；NIH RePORTER / EPA 内部项目编号（本次未查）；CORDIS 上 UFZ 作为 PARC/ENDOMIX 参与者的项目页（未能检索到）。

### 5.2 摘要要点蒸馏
- PARC WP5（Frontiers 2024）：构建 DNT-IVB v2.0 + ANT-IVB v1.0，评价适用域（含内分泌干扰与表观遗传），以 96 种化学品参照集；采用 GCCP 2.0、GIVIMP；后续优先天然毒素、双酚、PFAS。
- ENDOMIX（UFZ 页）：实际暴露混合物如何作用于免疫系统，整合体外/in silico/体内证据，推进高通量生物检测与生物标志物。
- NEURO-XENO-MICROBIOME（标题）：微生物组-外源物交互如何影响宿主神经发育；摘要全文未能检索到。

### 5.3 问题意识演变
EPA Pathfinder（微生物组 → 发育毒性 → PFAS 生物修复）关注“菌群是毒性的变量与解毒者”；W2/PARC 阶段转向“让斑马鱼行为数据在监管语境中可被接受”（方法学、参照集、IVB 对接）；ENDOMIX 把视角扩展到“肠-免疫-神经”及真实混合物。三阶段的共同点：从“看到现象”转为“可复现、可对接、可机制化”的系统。

## 6. 趋势判断
1. **从单终点到指纹到 IVB 对接**：依据 Herold 2025 → Spath 2026 → PARC 提案。预计 2027 年前后会出现围绕 DNT IVB 的 VAMR 参照化学品扩展与适用域评价。
2. **靶点反推走向“钾通道/PPAR/GABA”等非经典靶点**：依据 chlorophene→GABA-A/Kv7、PFOS→ppard、WAF→PPARδ/GABA-A。
3. **微生物组从单化学品案例变为通用 NAM 组件**：依据 N-EtFOSA、偶氮嘧菌酯（SIHUMIx）、AHR 调节剂摘要（待核实）。
4. **开放数据与代码成为论文标配，工具化（NeuroBEAT）可能出现**：依据 figshare/Zenodo 数据集与会议摘要；工具仓库未检索到，属推测。

## 7. 专家视角 Persona
1. 监管机构不信行为数据时，先用参照化学品库和跨物种机制证据赢得信任，而不是追求更多终点。
2. 习惯化是“被忽视的高阶终点”，对 GABA 与 NMDA 通路极敏感。
3. 一个行为指纹只是假设，必须用拮抗剂-激动剂拯救、靶点预测与哺乳动物电生理收束。
4. 暴露窗口决定机制：急性反应可能是药理性的，发育暴露才揭示不可逆的发育性损伤。
5. 母体化合物不等于活性物质，微生物组可能决定生物转化与行为结果，应纳入危害识别。
6. 一块 96 孔板、一个刺激序列、一套统计，要从一开始就为公开代码和可复现设计。
7. DNT IVB 的假阴性是机会：行为/整体动物层级可补灵敏度，但要同时报告特异性。
8. 混合物应从环境实测比例出发，分馏-重构是破解复杂样品的捷径。

## 8. 元数据
**定期检索式**
- PubMed：`Tal T[Author] AND (zebrafish OR neurotoxicity OR microbiome)`；`Tal T[Author] AND (Leipzig OR UFZ OR Helmholtz)`；`"Tal T"[Author] AND (VAMR OR habituation OR "DNT IVB")`。
- Consensus：`Tamara Tal zebrafish larval behavior microbiome N-EtFOSA GABA`。
- 项目：CORDIS（“PARC 101057014”“ENDOMIX”）、GEPRIS（“Tal” + UFZ）、UFZ 主页 49321、NIH RePORTER（EPA 时期）。

**信息源**：PubMed（26 PMID）、Europe PMC（PMC13445272 全文）、UFZ 个人主页 en/49321 与 en/50955、EurekAlert 新闻稿 1094398、Frontiers 全文（ftox.2024.1359507，前 100k 字符）、PARC 新闻页（搜索摘要）、Consensus。

**置信度**：履历（UFZ 页 + 署名变化）高；2024–2026 核心论文（元数据与摘要）高；平台参数（EHP 2026 全文）高，品系未确认；基金（W2、Pathfinder、PARC GA 编号）中高，ENDOMIX 编号/年限、MibiTox 角色、W2 编号低。

**待核实项（共 12 项）**
1. UNC 校友页（503）博士细节；2. 品系名；3. NeuroBEAT 工具仓库；4. GEPRIS 条目；5. PrecisionTox/ONTOX 角色；6. ENDOMIX 编号与 Tal 具体 WP；7. MibiTox 角色；8. 2020 年度论文对应哪篇；9. 31504981 DOI/页码；10. EHP 2026 的两个 DOI（EHP16568 与 EHP.6c00394）关系；11. ALTEX 2025 作者位置与 PNAS 2025 作者位置；12. PARC 新闻页 Pfizer 奖归属。

**同名排除清单**
- “Tal T”常见同名（未在结果中遇到作者归属混淆，但检索时需用单位过滤）：以色列/科学教育领域 Tali Tal（Technion）；其它医学/眼科领域的 Tal T（无单位匹配，已排除）。⚠️ 本次未逐一检出具体 PMID，列出仅为检索预案，需要在扩展检索时用 `AND (zebrafish OR toxicol*)` 或单位过滤。
- 已确认同一人：Tamara L. Tal（OSU 时期）。
