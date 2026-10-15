"""扫描核心：对每个候选范式计算源学科热度、环境语料稀缺度与迁移缺口分数。

缺口分数 = 热度(0-1) × 增速(0-1) × 稀缺度(0-1) × 100
- 热度   heat    = min(1, log10(1+近3年总发文)/3.5)   —— ~3000 篇/3年封顶
- 增速   growth  = min(1, (近2年均值)/(前2年均值+1) / 3) —— 3 倍增速封顶
- 稀缺度 scarcity: 环境语料命中 0 篇=1.0；黄金窗口(≤golden_max)=0.9；
  之后随 log2 衰减到拥挤阈值(≥crowded_min)的 0.15
状态分档：blank / golden / emerging / crowded
"""

from __future__ import annotations

import datetime as _dt
import json
import math
from pathlib import Path

from .sources import pubmed

PKG = Path(__file__).parent


def load_profile() -> dict:
    return json.loads((PKG / "profile.json").read_text(encoding="utf-8"))


def load_candidates() -> list[dict]:
    return json.loads((PKG / "data" / "candidates.json").read_text(encoding="utf-8"))["candidates"]


def env_journal_clause(profile: dict) -> str:
    jours = profile["env_corpus"]["journals_pubmed"]
    return "(" + " OR ".join(f'"{j}"[jour]' for j in jours) + ")"


def classify(env_hits: int, golden_max: int, crowded_min: int) -> str:
    if env_hits == 0:
        return "blank"
    if env_hits <= golden_max:
        return "golden"
    if env_hits < crowded_min:
        return "emerging"
    return "crowded"


def scarcity_factor(env_hits: int, golden_max: int, crowded_min: int) -> float:
    if env_hits == 0:
        return 1.0
    if env_hits <= golden_max:
        return 0.9
    # golden_max → 0.9 线性对数衰减至 crowded_min → 0.15
    t = (math.log2(env_hits) - math.log2(golden_max)) / (math.log2(crowded_min) - math.log2(golden_max))
    return max(0.15, 0.9 - 0.75 * min(1.0, t))


def scan_candidate(cand: dict, profile: dict, years: list[int]) -> dict:
    """抓取一个候选范式的全部计量数据并打分。"""
    cfg = profile["scan"]
    q = cand["query"]
    counts = pubmed.yearly_counts(q, years)

    env_q = f"({q}) AND {env_journal_clause(profile)}"
    env_hits = pubmed.count(env_q)

    # 环境领域先行者（黄金窗口/空白附近才值得看具体是谁）
    pioneers: list[dict] = []
    if 0 < env_hits <= max(cfg["golden_window_max_env_hits"] * 3, 15):
        pioneers = pubmed.summaries(pubmed.search_ids(env_q, retmax=5))

    recent = sum(counts[y] for y in years[-3:])
    late = (counts[years[-1]] + counts[years[-2]]) / 2
    early = (counts[years[0]] + counts[years[1]]) / 2
    heat = min(1.0, math.log10(1 + recent) / 3.5)
    growth = min(1.0, (late / (early + 1)) / 3)
    scarcity = scarcity_factor(env_hits, cfg["golden_window_max_env_hits"], cfg["crowded_min_env_hits"])
    status = classify(env_hits, cfg["golden_window_max_env_hits"], cfg["crowded_min_env_hits"])

    return {
        **{k: cand[k] for k in ("id", "name_zh", "name_en", "origin", "one_line", "transfer_hint")},
        "anchor": cand.get("anchor", False),
        "yearly_counts": {str(y): counts[y] for y in years},
        "recent_3y_total": recent,
        "env_hits": env_hits,
        "env_status": status,
        "env_pioneers": pioneers,
        "heat": round(heat, 3),
        "growth": round(growth, 3),
        "scarcity": round(scarcity, 3),
        "gap_score": round(100 * heat * growth * scarcity, 1),
    }


def run_scan(only_ids: list[str] | None = None, progress=print) -> dict:
    profile = load_profile()
    this_year = _dt.date.today().year
    years = list(range(this_year - profile["scan"]["years_back"] + 1, this_year + 1))
    cands = load_candidates()
    if only_ids:
        cands = [c for c in cands if c["id"] in only_ids]
    results = []
    for i, cand in enumerate(cands, 1):
        progress(f"[{i}/{len(cands)}] {cand['name_zh']} ({cand['id']}) …")
        try:
            results.append(scan_candidate(cand, profile, years))
        except Exception as e:  # 单条失败不拖垮整轮
            progress(f"  !! 失败: {e}")
            results.append({"id": cand["id"], "name_zh": cand["name_zh"], "error": str(e)})
    ok = [r for r in results if "error" not in r]
    ok.sort(key=lambda r: r["gap_score"], reverse=True)
    failed = [r for r in results if "error" in r]
    return {
        "scanned_at": _dt.datetime.now().isoformat(timespec="seconds"),
        "years": years,
        "results": ok + failed,
    }


def save_scan(scan: dict, out_dir: Path | None = None) -> Path:
    out_dir = out_dir or (PKG / "data" / "scans")
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = scan["scanned_at"][:10]
    path = out_dir / f"scan_{stamp}.json"
    path.write_text(json.dumps(scan, ensure_ascii=False, indent=1), encoding="utf-8")
    (out_dir / "latest.json").write_text(json.dumps(scan, ensure_ascii=False, indent=1), encoding="utf-8")
    return path
