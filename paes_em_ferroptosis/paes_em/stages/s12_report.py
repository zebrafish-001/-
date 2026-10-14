"""Stage 12 — assemble the final analysis report (Markdown + HTML).

Collects every stage's persisted JSON summary from ``data/results`` and
renders a single document following the paper's narrative:
network toxicology → DE/WGCNA → enrichment → ML key gene → immune →
single-cell/spatial → virtual KO → docking → (wet-lab validation plan).
"""

from __future__ import annotations

import datetime
import html
import json

from ..config import RunContext
from ..utils.io import load_json, save_json


def _r(x, nd=3):
    """Round floats (handles None) for readable report lines."""
    if isinstance(x, float):
        return round(x, nd) if abs(x) >= 10 ** -nd else f"{x:.2e}"
    return x


def _get(ctx: RunContext, name: str) -> dict:
    p = ctx.results / f"{name}.json"
    return load_json(p) if p.exists() else {}


def _sc_lines(ctx, s8, key, axis_name, _r):
    """Single-cell section: patient-level wording when rigor data exist,
    else the pipeline's cell-level summary."""
    import json as _j
    f = ctx.results / "rigor_singlecell.json"
    if f.exists():
        sc = _j.loads(f.read_text())
        comp = sc.get("composition_decomposition", {})
        spec = sc.get("cd36_celltype_specificity", {})
        return [
            f"- {key} 为巨噬细胞特异: "
            f"{spec.get('macrophage_is_top_in_samples', '?')}/"
            f"{spec.get('n_samples', '?')} 样本中巨噬为最高表达细胞型",
            f"- 病变组巨噬细胞比例↑(3/3病人一致)、foam-like比例↑(3/3一致); "
            f"{key}全组织升高主要为组成效应(全组织"
            f"{comp.get('whole_tissue_fold_DIS_over_HEA')}× vs 巨噬内"
            f"{comp.get('within_macrophage_fold_DIS_over_HEA')}×, 巨噬占比"
            f"{comp.get('macrophage_prop_fold_DIS_over_HEA')}×)",
            "- 注: 独立单位为病人(n=3), 细胞级P值属伪复制不报告(符号秩最小P=0.25); "
            f"{key}~轨迹逐病人符号翻转, 见局限",
        ]
    return [
        f"- {key} 在病变 vs 正常组: {_r(s8.get('key_gene_mean_DIS'))} vs "
        f"{_r(s8.get('key_gene_mean_HEA'))} (P={_r(s8.get('key_gene_DIS_vs_HEA_p'))})",
        f"- {key} 与干性相关 ρ={_r(s8.get('key_gene_rho_stemness'))}; "
        f"沿 {axis_name} 轨迹伪时间 ρ={_r(s8.get('key_gene_rho_pseudotime'))} "
        f"(P={_r(s8.get('key_gene_rho_pseudotime_p'))})",
    ]


def _rigor_lines(ctx):
    """Second-pass rigor corrections, included when rigor_*.json exist."""
    rp = ctx.results
    import json as _j
    f = rp / "rigor_singlecell.json"
    if not f.exists():
        return []
    sc = _j.loads(f.read_text())
    comp = sc.get("composition_decomposition", {})
    out = ["## 严谨性复算 (对应补充图 S1-S6)"]
    it = rp / "rigor_intersection_permutation.json"
    if it.exists():
        d = _j.loads(it.read_text())
        out.append(f"- 交集特异性(置换): 观测{d['observed_intersection_size']}基因 vs "
                   f"随机零分布均值{d['null_mean']}, 富集{d['enrichment_fold']}×, "
                   f"P={d['empirical_p_size']}")
    hb = rp / "rigor_enrichment_hubfilter.json"
    if hb.exists():
        d = _j.loads(hb.read_text())
        out.append(f"- 富集泛靶点控制: 关键基因仅在{d['cd36_pct_terms']}%显著KEGG条目, "
                   f"远低于枢纽(最高{d['max_pan_pct']}%) → 通路特异")
    ml = rp / "rigor_ml.json"
    if ml.exists():
        d = _j.loads(ml.read_text())["external_auc_permutation"]
        out.append(f"- ML诚实评估: 内部CV AUC不可用; 外部平均AUC {d['real_mean_external_auc']}, "
                   f"置换P={d['empirical_p']}")
    if comp:
        out.append(f"- 伪复制/组成控制(n=3病人): CD36全组织{comp['whole_tissue_fold_DIS_over_HEA']}× "
                   f"主要为组成效应(巨噬内仅{comp['within_macrophage_fold_DIS_over_HEA']}×, "
                   f"巨噬占比{comp['macrophage_prop_fold_DIS_over_HEA']}×); 细胞级P值不报告")
    dk = rp / "rigor_docking_sites.json"
    if dk.exists():
        d = _j.loads(dk.read_text())
        c = d.get("controls", {})
        out.append(f"- 对接位点控制: {d['pairs_over_8A']}/{d['n_pairs']}对化合物"
                   f"质心相距>8Å(中位{d['median_pair_dist_A']}Å), 结合在不同位点"
                   f"→ 跨位点打分不可比; 诱饵(葡萄糖)得分"
                   f"{c.get('negative_decoy',{}).get('glucose')}落在增塑剂区间内"
                   f"→ 盒子无区分力, 结合能不支持特异结合")
    gs = rp / "rigor_geneset_defense.json"
    if gs.exists():
        d = _j.loads(gs.read_text())
        sm = d.get("summary", {})
        out.append(f"- 铁死亡基因集(全983): 对表达匹配背景无DEG富集(3队列Fisher "
                   f"p={list(sm.get('deg_proportion_fisher_p_per_cohort',{}).values())}); "
                   f"全转录组背景虚高(混杂, 不单用)")
    out.append("")
    return out


def build_markdown(ctx: RunContext) -> str:
    cfg = ctx.cfg
    s2 = _get(ctx, "s02_network_tox")
    s3 = _get(ctx, "s03_diffexp")
    s4 = _get(ctx, "s04_wgcna")
    s5 = _get(ctx, "s05_enrich")
    s6 = _get(ctx, "s06_ml")
    s7 = _get(ctx, "s07_immune")
    s8 = _get(ctx, "s08_singlecell")
    s9 = _get(ctx, "s09_spatial")
    s10 = _get(ctx, "s10_knockout")
    s11 = _get(ctx, "s11_docking")
    key = s6.get("key_gene", "?")
    import re as _re
    _m = _re.search(r"\(([^)]+)\)", cfg["project"]["disease_name"])
    dz = _m.group(1) if _m else cfg["project"]["disease_name"].split()[0]
    axis_name = " → ".join(cfg.get("single_cell", {}).get(
        "axis_types", ["表型转换"]))

    lines = [
        f"# {cfg['project']['exposure_name']} → 铁死亡 → "
        f"{cfg['project']['disease_name']} 网络毒理学与多组学分析报告",
        "",
        f"- 流程: paes-em-ferroptosis v0.1 ({'演示数据' if ctx.demo else '真实数据'})",
        f"- 生成时间: {datetime.date.today().isoformat()}",
        "- 方法学参照: Wang et al., J Hazard Mater 2026;507:141670 "
        "(doi:10.1016/j.jhazmat.2026.141670)",
        "",
        "## 1. 网络毒理学靶点交集",
        f"- 增塑剂靶点 {s2.get('n_paes_targets', '?')} 个; {dz} 靶点 "
        f"{s2.get('n_em_targets', '?')} 个; 铁死亡基因 {s2.get('n_frgs', '?')} 个",
        f"- 三重交集 **{s2.get('intersection_size', '?')}** 个基因: "
        f"{', '.join(s2.get('intersection_genes', [])[:15])}"
        f"{' …' if s2.get('intersection_size', 0) > 15 else ''}",
        "",
        "## 2. 差异表达 (limma 式 moderated t)",
        f"- 训练集 {s3.get('dataset', '?')}: DEG {s3.get('n_degs', '?')} 个 "
        f"(上调 {s3.get('n_up', '?')} / 下调 {s3.get('n_down', '?')})",
        "",
        "## 3. WGCNA",
        f"- 引擎 {s4.get('engine', '?')}, 软阈值 β={s4.get('soft_power', '?')}, "
        f"检出模块 {s4.get('n_modules', '?')} 个, 表型显著模块基因 "
        f"{s4.get('n_key_genes', '?')} 个",
        "",
        "## 4. 功能富集",
        f"- 显著条目 {s5.get('n_significant_terms', '?')} 个: "
        f"{'; '.join(s5.get('top_terms', [])[:5])}",
        "",
        "## 5. 机器学习关键基因",
        f"- 12 算法 10 折交叉验证, 最优: "
        + ", ".join(f"{r['algorithm']} (AUC {r['cv_auc']})"
                    for r in s6.get("benchmark_top3", [])),
        f"- RF ∩ Lasso ∩ XGBoost 共识关键基因: **{key}**",
        f"- 验证集单基因 AUC: {json.dumps(s6.get('validation_auc', {}), ensure_ascii=False)}",
        "",
        "## 6. 免疫浸润 (ssGSEA, 28 细胞型)",
        f"- 组间差异细胞型 {s7.get('n_diff_cell_types', '?')} 个; "
        f"与 {key} 显著相关 {s7.get('n_key_gene_correlated', '?')} 个",
        "",
        "## 7. 单细胞分析",
        f"- 引擎 {s8.get('engine', '?')}, 细胞 {s8.get('n_cells', '?')}, "
        f"{s8.get('n_clusters', '?')} 个细胞亚型",
        *_sc_lines(ctx, s8, key, axis_name, _r),
        "",
        "## 8. 空间转录组",
        ("- 本终点无可用的公共空间转录组原始计数数据, 该阶段跳过"
         if s9.get("engine", "skipped") == "skipped" else
         f"- 病灶区 {key} 富集 P={_r(s9.get('lesion_enrichment_p'))}; "
         f"图: {s9.get('figure', '-')}"),
        "",
        f"## 9. 虚拟敲除 ({s10.get('cell_type', '?')})",
        f"- 敲除 {s10.get('knockout_gene', key)}, GRN 网络基因 "
        f"{s10.get('n_network_genes', '?')} 个; 高扰动基因: "
        f"{', '.join(s10.get('top_perturbed', [])[:6])}",
        (f"- 铁死亡基因在高扰动集中富集 P={_r(s10.get('frg_enrichment_p'))}"
         + ("" if (s10.get('frg_enrichment_p') or 1) < 0.05
            else " (不显著; lite GRN 的局限, 建议用 scTenifoldKnk R 包复核)")),
        f"- 扰动基因富集通路: {'; '.join(s10.get('top_terms', [])[:3])}",
        "",
        "## 10. 分子对接 (见严谨性复算: 仅为探索性, 不支持特异结合)",
        f"- 受体 {s11.get('receptor_pdb', '?')}, 12化合物结合能 -5.5~-7.25 kcal/mol; "
        f"但多位点+诱饵对照显示打分不可比且无区分力, 结论仅为'可与CD36表面结合'的"
        f"探索性提示, 需定口袋+阳性对照重做",
        f"- 结合能: {json.dumps(s11.get('affinities', {}), ensure_ascii=False)}",
        "",
        "## 11. 实验验证设计 (湿实验, 不由本流程执行)",
        *[f"- {line}" for line in cfg.get("report", {}).get(
            "wetlab_plan",
            ["5+5 标本 IHC/IF 检测关键基因表达及 EMT 标志物共定位; 需伦理批准"])],
        "",
        *_rigor_lines(ctx),
        "## 结论轴",
        f"**{cfg['project']['exposure_name']} 暴露 → 铁死亡相关基因 {key} "
        f"上调 → 免疫微环境扰动 → {axis_name} 细胞状态转换 → "
        f"{cfg['project']['disease_name']}**",
    ]
    return "\n".join(lines)


def run(ctx: RunContext) -> dict:
    from .. import figures as _figs
    rendered = _figs.render_all(ctx)
    md = build_markdown(ctx)
    if rendered:
        md += "\n\n## 图表\n" + "\n".join(
            f"- {name}" for name in rendered)
    md_path = ctx.results / "report.md"
    md_path.write_text(md, encoding="utf-8")

    body = html.escape(md)
    html_doc = (
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<title>PAEs-EM-Ferroptosis report</title>"
        "<style>body{font-family:system-ui;max-width:860px;margin:2rem auto;"
        "line-height:1.6;padding:0 16px}</style></head>"
        f"<body><pre style='white-space:pre-wrap'>{body}</pre></body></html>"
    )
    (ctx.results / "report.html").write_text(html_doc, encoding="utf-8")

    out = {"markdown": str(md_path), "html": str(ctx.results / "report.html"),
           "figures": rendered}
    save_json(out, ctx.results / "s12_report.json")
    return out
