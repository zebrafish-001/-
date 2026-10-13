# TOC 图工具（tocmaker / sci-toc）需求与现状 — v0.1

> 目的：面向环境毒理与人群健康方向的 SCI 投稿，把"一句话故事"自动排成期刊尺寸的 TOC 图 / 图文摘要，
> 产出 **SVG（矢量）+ 可编辑 PPTX + 300 dpi PNG/TIFF**，并做自动 QA。
> 本文件既是现状说明，也是**待你拍板的需求清单**（见 §4）。

## 1. 调研结论：市面工具与我们的定位

| 工具 | 类型 | 对我们的意义 |
|---|---|---|
| BioRender | 在线、模板 + 图库、订阅制 | 生命科学图库最全，但导出受限（免费版带水印/仅低清），商用/发表需付费许可，且不能批量化 |
| Mind the Graph | 在线、图库覆盖环境科学 | 同上，订阅制 |
| Figdraw（国内） | 在线、中文图库 | 环境/毒理图标尚可，出图依赖手工拖拽 |
| Adobe Illustrator / Affinity / Inkscape | 通用矢量软件 | 精修最强，但从零画慢；Inkscape 免费开源，适合作为"最后一步精修" |
| PowerPoint | 几乎所有课题组的实际工具 | 编辑门槛最低；本工具直接产出原生形状的 PPTX 就是为了接这一步 |
| draw.io / Excalidraw | 免费图形工具 | 流程图可以，TOC 的尺寸/字号控制弱 |
| SciDraw AI、各类"AI 生成摘要图" | 生成式 | ACS 要求 TOC 必须是作者原创作品，部分期刊禁用生成图；只能当草稿灵感，不能直接投 |
| 开源图标库：Bioicons（2800+，按图标授权 CC0/MIT/CC-BY）、Health Icons（1500+，MIT）、NIH BioArt（公有领域）、Reactome（CC-BY）、PhyloPic | 素材 | 本工具已内置 Bioicons CC0 子集 + Health Icons 子集 + 自绘 42 个环境毒理图标 |

**定位**：不做"又一个拖拽画板"，而是 **"写一份 10 行 YAML → 自动排版到期刊尺寸 → SVG + PPTX"** 的代码工具 + Claude 技能，
把反复出现的叙事骨架（暴露→机制→效应、队列流水线、多来源→模式生物→多终点……）变成模板，剩下 10% 的个性化在 PowerPoint 里改。

## 2. 已完成（本次提交）

- `tocmaker/` Python 包，命令 `python -m tocmaker.cli`（安装后为 `toc`）：
  - `presets`：期刊画布预设（ACS 3.25×1.75 in；Elsevier 1328×531 px；Cell 1200×1200 px；RSC 8×4 cm；MDPI ≥1100×560 px；Chem Res Toxicol 8.47×4.76 cm；Adv Sci 55×50 / 110×20 mm；Springer 7:5；通用 16:9），
    并与调研得到的 39 本期刊规格表（`tocmaker/db/journal_specs.yaml/.md`）联动，支持按期刊名模糊查找。
  - `init`：输出 6 种模板示例 YAML（flow / cohort / split / hub / two_row / cycle）。
  - `render`：YAML → `toc.svg`、`toc.pptx`、`toc.png`(300 dpi)、`toc.pdf`、可选 `toc.tif`，加 `toc_qa.json`。
    - SVG：画布单位为 pt，根元素带毫米物理尺寸，字体 Arial/Helvetica 栈，图标内联为嵌套 `<svg>`（纯矢量，无栅格）。
    - PPTX：幻灯片 = TOC 真实尺寸（可 `--pptx-scale 2`），面板/文字/徽章/箭头都是原生形状，图标以 **SVG 嵌入 + PNG 兜底**（PowerPoint 2016+ 可右键"转换为形状"），或 `--icon-format emf`（LibreOffice 转 EMF，可取消组合）。
    - 自动排版：按角色配色（暴露/生物/机制/结局/方法），同一行面板文字基线对齐，文字自动缩字号到期刊下限、再断词；徽章自动缩放/两行。
  - QA 门：画布尺寸、最小字号（ACS 6 pt）、字数预算、文字溢出、对比度（WCAG 公式）、图标数、授权（CC-BY 提示署名、CC-BY-SA 警告）、ACS"不展示结果"提示。
  - `icons search/list/sheet`：图标检索（中英文关键词），内置 42 个自绘环境毒理图标（CC0，可按角色换色）+ 94 个 Health Icons（MIT）+ 76 个 Bioicons（CC0），`scripts/fetch_icon_sets.sh` 可拉全量 4300+。
  - `harvest`：Europe PMC 开放获取文献的图文摘要采集器（见 §3）。
- `.claude/skills/sci-toc/SKILL.md`：让 Claude 从摘要直接产出 spec → 渲染 → 看图 → 迭代的工作流。
- `tocmaker/db/patterns.yaml`：12 种环境毒理/人群健康 TOC 叙事骨架 + 各出版社风格要点。
- 6 个模板示例均已渲染核对（见 `tocmaker/examples/`）。

## 3. 参考图库（TOC 图样本）与素材库接入现状

### 3.1 PubMed 连接器能做什么、不能做什么
已接入的 PubMed 连接器（search / metadata / copyright / PMC 全文）是**远程**服务，能查文献、拿 PMCID、DOI、PII 和版权信息，
但 PMC 全文接口只返回**纯文本**（没有图片文件名），而且容器仍然连不到 PMC / Elsevier 图片服务器（403）。
所以"百来张 TOC 图"的落地方案改为两步：

1. **我这边（已做）**：用 PubMed 连接器在 Environ Int、JHM、STOTEN、EES、Environ Pollut、Chemosphere、Environ Res、Water Res、
   EEH、ESE 里检索 2023–2025 年开放获取论文，生成种子索引 `tocmaker/db/reference/seed_index.csv`
   （PMID、PMCID、DOI、PII、期刊、年份、题目、版权类型、图文摘要 URL）。
   Elsevier 的图文摘要图片地址可以由 PII 直接推出：`https://ars.els-cdn.com/content/image/1-s2.0-<PII>-ga1_lrg.jpg`，
   这正是这些期刊的"TOC 图"。
2. **你本机一条命令下载图片**（或在环境设置里放行 `ars.els-cdn.com`、`eutils.ncbi.nlm.nih.gov` 后让我跑）：
   `python -m tocmaker.cli harvest --seed tocmaker/db/reference/seed_index.csv --out tocmaker/db/reference`
   会得到 `images/`、`index.csv` 和可浏览的 `contact_sheet.html`。
   不用种子也行：`python -m tocmaker.cli harvest --source pubmed --n 120` 直接走 NCBI E-utilities + PII 规则；
   `--source europepmc` 走 JATS XML（能覆盖 Cell Press / 其他出版社的图文摘要）。

注意：PubMed 返回的多数 PMC 记录是作者手稿（"All rights reserved"），图片只作内部版式学习；`index.csv` 保留每条的许可证。
"子刊以上"的 Nature 系列本身不用 TOC 图（Sci Rep 明确禁止），真正有图文摘要且开放获取的高分刊就是上面这批。

### 3.2 免费素材库接入情况
| 素材库 | 许可 | 接入方式 | 状态 |
|---|---|---|---|
| 自绘 envtox 图标集（42 个） | CC0 | 内置，按角色自动换色 | ✅ |
| Health Icons（1500+，公共卫生/人群/器官） | MIT | 内置 94 个精选；全量 `scripts/fetch_icon_sets.sh` | ✅ |
| Bioicons（2800+，按图标授权） | CC0/MIT/CC-BY/CC-BY-SA | 内置 76 个 CC0 精选；全量同上，QA 会标出 CC-BY/SA | ✅ |
| Reactome Icon Library（2571 个：人体组织、细胞、细胞器、受体、化合物、箭头） | CC BY 4.0（需署名） | 内置 ~900 个精选（含"带器官的人体"）；全量同上 | ✅ |
| NIH BioArt（公有领域）、PhyloPic（物种剪影）、Servier Medical Art（CC BY）、OpenClipart | 免费 | 站点被本环境网络策略拦截，且无 GitHub 镜像 | ❌ 需在你本机下载后放进 `tocmaker/assets/icons/external/<名字>/`，设置 `TOCMAKER_ICON_PATHS` 即可被检索 |

检索示例：`python -m tocmaker.cli icons search 胎盘 placenta`、`... search "female body organs" --source reactome`。

### 3.3 其他未完成项
- 期刊规格里 5 项未核实（见 `journal_specs.md` 末尾"未确认项"）。
- 容器内无 Arial，用度量兼容的 Liberation Sans 排版；SVG/PPTX 指定 Arial，你机器上打开自动用 Arial，行宽一致。

## 4. 需要你拍板的需求（我先按括号里的默认值做了）

1. **主投期刊优先级**？（默认 ACS ES&T 规格优先，其次 Environ Int/JHM；二者尺寸比例不同，一个 spec 可一键切换 `--journal`）
2. **ACS 的"不透露结果"传统**是否遵守？（默认：QA 只提示不拦截；你可以保留徽章数字）
3. **中文标签**是否需要？（已支持 CJK 逐字换行与度量；默认英文，字体栈可加 Noto Sans CJK / 思源黑体）
4. **PPTX 的形态**：真实 TOC 尺寸的小幻灯片（默认）还是放大 2× 的工作页？是否需要"EMF 可取消组合"而非 SVG？
5. **图标风格**：现有自绘集是"扁平双色剪影"（深墨 + 角色色）。要不要走"线稿+淡填充"的 BioRender 风？要补哪些图标（例如：胎盘屏障、血脑屏障、斑马鱼心脏、PM 源解析、污水厂、土壤-作物、鱼体生物富集、Mendelian randomization、exposome 雷达图）？
6. **配色**：默认 `envtox`（暖橙暴露 / 蓝生物 / 青机制 / 紫结局），备选 `calm`、`alert`、`mono`。是否按课题组固定一套？
7. **输出物**：SVG + PPTX + PNG + PDF（默认），TIFF 可选；是否要同时出"投稿版（无字数超标）"与"汇报版 16:9（文字可多）"？
8. **参考图库的用法**：只作人看（contact sheet），还是要我进一步做"版式结构标注"（哪种骨架、几格、箭头方向、是否带数字）以统计 ES&T vs EI 的风格差异？
9. 是否要接 Zotero：从你库里的 DOI 批量生成每篇论文的 TOC 草稿？

## 5. 使用示例

```bash
pip install -e .                       # 或 pip install lxml python-pptx cairosvg pillow pyyaml requests
python -m tocmaker.cli init --template flow --journal acs -o toc.yaml
python -m tocmaker.cli icons search 斑马鱼 placenta cohort
python -m tocmaker.cli render toc.yaml -o out --preview --tiff
# 输出：out/toc.svg  out/toc.pptx  out/toc.png  out/toc.pdf  out/toc.tif  out/toc_qa.json
```

在 Claude Code 里直接说"用 sci-toc 给这段摘要出一张 Environ Int 的 TOC 图"即可触发技能。
