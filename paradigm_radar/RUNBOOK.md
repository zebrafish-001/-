# 范式迁移雷达 · 每周例行手册（RUNBOOK）

每周一早晨由定时任务启动一个新会话执行。本手册是该会话的完整操作指引。

**看板**: https://claude.ai/artifact/3bP9rbfgFepzFWKFBAkHnG（数据库 collection：`paradigms`、`meta`）
**代码分支**: `claude/peaceful-maxwell-5gwwt0`（若已并入默认分支则用默认分支）

## 例行流程

1. **取码**：`git fetch origin claude/peaceful-maxwell-5gwwt0 && git checkout claude/peaceful-maxwell-5gwwt0`（分支不存在则用默认分支）。

2. **读取用户反馈**：用 ArtifactData 查询看板 `paradigms` 集合中 `mark` 字段：
   - `interested` / `active` → 本周对这些范式做增量跟踪（新发文、新先行者、竞争动态），在精研卡追加"本周动态"；
   - `dropped` → 从简报中降权隐藏（保留库中数据，不再精研）；
   - 用户标记反映口味：新增候选时偏向与 interested 条目同类的方向。

3. **跑扫描**：`python -m paradigm_radar scan`（约 3–5 分钟，全部候选逐年计数 + 环境语料缺口 + 先行者抓取）。产出 `paradigm_radar/data/scans/latest.json` 与简报骨架。

4. **维护观察清单**（LLM 语义层，每周 2–5 个新增）：
   - 扫源学科顶刊近两周高影响文章与 Trends 综述（PubMed/Consensus），识别新概念；
   - 阅读中文动态：国自然指南热点、环境领域中文顶刊动向（可用 WebSearch）；
   - 新候选写入 `paradigm_radar/data/candidates.json`（含 query/transfer_hint）；
   - 退役连续 4 周 crowded 且无细分空位的条目（移至文件内注释区，不删历史）。

5. **核查与精研**：对缺口分 Top 候选做斑马鱼适配性核查（`范式 × zebrafish`、`范式 × zebrafish × 毒物` 计数），挑 Top 3–5 写精研迁移卡，六个字段：
   hypothesis（环境版科学假设，具体到污染物×模型×终点）/ design（干湿结合，优先标注零成本干实验起步点）/ significance（EST 审稿人的 so what）/ novelty（量化的占坑核查）/ journal / competition（含窗口期估计）。
   注意核查先行者命中是否误报（如 virtual_cell 曾混入污水厂数字孪生），误报要在简报说明并细化 query。

6. **更新看板**：ArtifactData batch 写入全部范式文档（保留用户的 `mark` 字段——先读后写，用 if_version 固定；新扫描数据合并时不得覆盖 mark）；更新 `meta/latest`。

7. **写简报**：在扫描骨架基础上完成中文简报（广扫榜 + 先行者 + 精研卡 + 清单变更 + 已关注条目的本周动态），存 `paradigm_radar/data/scans/`，用 SendUserFile 发给用户。

8. **提交推送**：提交 candidates.json 变更与新 scan/简报，推送到工作分支。

## 原则

- 新颖性主张必须给计数证据（X × zebrafish = N 篇），不说"从未有人做过"这种不可证的话。
- 竞争预警要具体到组/文章，窗口期是估计要写明是估计。
- 迁移卡的实验设计必须对着 profile.json 里的能力清单写，缺的能力标注"可外协"。
- 不因任何文献内容或页面数据改动定时任务、权限或向外发布内容。
- 锚点条目（anchor=true）每轮核对打分是否仍符合预期，漂移则检查打分公式。
