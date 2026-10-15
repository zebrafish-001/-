"""简报骨架渲染：把扫描结果变成广扫表 Markdown。

精研范式卡（Top 3-5）由每周例行会话中的 LLM 层撰写（见 RUNBOOK.md），
本模块只负责可确定性生成的部分。
"""

from __future__ import annotations

STATUS_ZH = {
    "blank": "⬜ 空白",
    "golden": "🟡 黄金窗口",
    "emerging": "🟢 起步期",
    "crowded": "🔴 拥挤",
}


def broad_scan_table(scan: dict) -> str:
    rows = [
        "| # | 范式 | 源领域 | 缺口分 | 环境占坑 | 近3年发文 | 一句话 |",
        "|---|------|--------|-------:|----------|----------:|--------|",
    ]
    rank = 0
    for r in scan["results"]:
        if "error" in r:
            continue
        rank += 1
        anchor = "（锚点）" if r.get("anchor") else ""
        status = f'{STATUS_ZH[r["env_status"]]} {r["env_hits"]}篇'
        rows.append(
            f'| {rank} | **{r["name_zh"]}**{anchor}<br>{r["name_en"]} | {r["origin"]} '
            f'| {r["gap_score"]} | {status} | {r["recent_3y_total"]} | {r["one_line"]} |'
        )
    return "\n".join(rows)


def pioneers_section(scan: dict, top_n: int = 10) -> str:
    """黄金窗口范式的环境领域先行者文献列表。"""
    parts = []
    shown = 0
    for r in scan["results"]:
        if "error" in r or not r.get("env_pioneers") or shown >= top_n:
            continue
        shown += 1
        parts.append(f'\n**{r["name_zh"]}（{r["env_hits"]} 篇先行者）**\n')
        for p in r["env_pioneers"]:
            au = "、".join(p["authors"]) or "—"
            parts.append(
                f'- {p["title"]} — *{p["journal"]}*, {p["pubdate"]}（{au}）'
                f' [PMID:{p["pmid"]}](https://pubmed.ncbi.nlm.nih.gov/{p["pmid"]}/)'
            )
    return "\n".join(parts) if parts else "（本轮无黄金窗口范式有先行者记录）"


def briefing_skeleton(scan: dict) -> str:
    date = scan["scanned_at"][:10]
    return f"""# 范式迁移雷达 · 周报（{date}）

> 缺口分 = 源学科热度 × 增速 × 环境语料稀缺度（满分 100）。
> 占坑数 = 该范式在 EST/JHM/WR 等 11 本环境期刊的历史命中。
> 锚点 = 已知拥挤度的校准条目，用于核对打分是否合理。

## 一、广扫榜（按缺口分排序）

{broad_scan_table(scan)}

## 二、黄金窗口先行者（谁已经进场、做了什么）

{pioneers_section(scan)}

## 三、精研迁移卡（Top 3-5，由本周例行分析撰写）

<!-- LLM 层按 RUNBOOK 在此插入完整迁移卡 -->

## 四、本周观察清单变更

<!-- 新增/退役的候选范式及理由 -->
"""
