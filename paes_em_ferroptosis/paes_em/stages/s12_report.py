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

    lines = [
        f"# {cfg['project']['exposure_name']} → 铁死亡 → EMT → "
        f"{cfg['project']['disease_name']} 分析报告",
        "",
        f"- 流程: paes-em-ferroptosis v0.1 ({'演示数据' if ctx.demo else '真实数据'})",
        f"- 生成时间: {datetime.date.today().isoformat()}",
        "- 方法学参照: Wang et al., J Hazard Mater 2026;507:141670 "
        "(doi:10.1016/j.jhazmat.2026.141670)",
        "",
        "## 1. 网络毒理学靶点交集",
        f"- PAEs 靶点 {s2.get('n_paes_targets', '?')} 个; EM 靶点 "
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
        f"- {key} 与干性相关 ρ={_r(s8.get('key_gene_rho_stemness'))}, "
        f"与表型转换轴伪时间相关 "
        f"ρ={_r(s8.get('key_gene_rho_pseudotime'))}, "
        f"EMT 轴富集 P={_r(s8.get('key_gene_axis_enrichment_p'))}",
        "",
        "## 8. 空间转录组",
        f"- 病灶区 {key} 富集 P={_r(s9.get('lesion_enrichment_p'))}; "
        f"图: {s9.get('figure', '-')}",
        "",
        "## 9. 虚拟敲除 (成纤维细胞)",
        f"- 敲除 {s10.get('knockout_gene', key)}, 扰动网络基因 "
        f"{s10.get('n_network_genes', '?')} 个; 高扰动集中铁死亡基因富集 "
        f"P={_r(s10.get('frg_enrichment_p'))}",
        f"- 扰动基因富集: {'; '.join(s10.get('top_terms', [])[:3])}",
        "",
        "## 10. 分子对接",
        f"- 受体 {s11.get('receptor_pdb', '?')}, 阈值 "
        f"{s11.get('threshold_kcal_mol', '?')} kcal/mol, 强结合 "
        f"{s11.get('n_strong_binders', '?')}/{s11.get('n_docked', '?')}",
        f"- 结合能: {json.dumps(s11.get('affinities', {}), ensure_ascii=False)}",
        "",
        "## 11. 实验验证设计 (湿实验, 不由本流程执行)",
        *[f"- {line}" for line in cfg.get("report", {}).get(
            "wetlab_plan",
            ["5+5 标本 IHC/IF 检测关键基因表达及 EMT 标志物共定位; 需伦理批准"])],
        "",
        "## 结论轴",
        f"**PAEs 暴露 → 铁死亡相关基因 {key} 失调 → 免疫微环境扰动 → "
        "上皮-间质转化 (Lumenal+Ciliated → Fibroblasts) → 子宫内膜异位症**",
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
