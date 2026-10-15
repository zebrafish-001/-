"""CLI: python -m paradigm_radar scan [--only id1,id2] [--out DIR]"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import scan as scan_mod
from . import report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="paradigm_radar")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_scan = sub.add_parser("scan", help="跑一轮全量扫描并生成简报骨架")
    p_scan.add_argument("--only", help="逗号分隔的候选 id，只扫这些（调试用）")
    p_scan.add_argument("--out", help="输出目录（默认 paradigm_radar/data/scans）")
    args = ap.parse_args(argv)

    if args.cmd == "scan":
        only = args.only.split(",") if args.only else None
        result = scan_mod.run_scan(only_ids=only)
        out_dir = Path(args.out) if args.out else None
        path = scan_mod.save_scan(result, out_dir)
        md = report.briefing_skeleton(result)
        md_path = path.with_name(path.stem + "_briefing.md")
        md_path.write_text(md, encoding="utf-8")
        print(f"\n扫描结果: {path}\n简报骨架: {md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
