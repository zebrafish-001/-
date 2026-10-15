# paradigm_radar — 跨学科范式迁移雷达

扫描医学/药理学/方法学/远学科的热点范式，反查环境科学语料（EST/JHM/WR 等 11 刊），
量化**迁移缺口分数 = 源学科热度 × 增速 × 环境稀缺度**，为环境毒理研究排序"值得第一个搬过来"的范式，
并生成带干湿结合实验设计的**精研迁移卡**。

三件套：

| 组件 | 位置 |
|------|------|
| 扫描管线 | 本目录（纯标准库，零依赖） |
| 每周定时任务 | 每周一 07:46（北京时间）自动跑，见 `RUNBOOK.md` |
| 范式卡看板 | https://claude.ai/artifact/3bP9rbfgFepzFWKFBAkHnG |

## 用法

```bash
python -m paradigm_radar scan                 # 全量扫描（约 3-5 分钟）
python -m paradigm_radar scan --only ferroptosis,glymphatic   # 调试单条
```

产出 `data/scans/scan_<日期>.json`（结构化结果）+ `scan_<日期>_briefing.md`（简报骨架，
精研卡由每周例行会话按 RUNBOOK 补全）。设 `NCBI_API_KEY` 环境变量可提速。

## 文件

- `profile.json` — 科研画像：能力清单（打迁移卡时对照）、环境语料 11 刊、源学科期刊
- `data/candidates.json` — 候选范式观察清单（每周由例行会话增删；含 3 个校准锚点）
- `scan.py` — 打分核心：热度/增速/稀缺度公式与占坑分档（blank/golden/emerging/crowded）
- `sources/pubmed.py` — PubMed E-utilities 客户端（限速+重试）
- `report.py` — 简报骨架渲染
- `dashboard.html` — 看板页面源码（重发布用）
- `RUNBOOK.md` — 每周例行完整操作指引

## 打分设计

- 热度：log10(1+近3年发文)/3.5 封顶 1
- 增速：近两年均值 / 前两年均值，3 倍封顶
- 稀缺度：环境 11 刊命中 0 篇=1.0；黄金窗口(≤5 篇)=0.9；对数衰减至拥挤(≥30 篇)=0.15
- 校准锚点：铁死亡（应为拥挤）、肠-脑轴（拥挤）、铜死亡（起步期）——首轮验证全部命中
