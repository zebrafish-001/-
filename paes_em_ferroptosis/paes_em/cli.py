"""Command-line orchestrator.

Examples
--------
Run everything on bundled synthetic data (smoke test / demo)::

    paes-em run-all --demo

Run a subset of stages on real data placed in data/raw::

    paes-em run --stages intake,network_tox,diffexp

List stages::

    paes-em stages
"""

from __future__ import annotations

import argparse
import json
import sys
import time

from . import synthetic
from .config import make_context
from .stages import ORDER


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="paes-em", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("run-all", "run"):
        sp = sub.add_parser(name)
        sp.add_argument("--config", default=None, help="pipeline.yaml path")
        sp.add_argument("--root", default=None, help="project root for data/")
        sp.add_argument("--demo", action="store_true",
                        help="generate + use synthetic data")
        sp.add_argument("--seed", type=int, default=None)
        if name == "run":
            sp.add_argument("--stages", required=True,
                            help="comma list, e.g. intake,diffexp,ml")
    sub.add_parser("stages")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.cmd == "stages":
        for name, mod in ORDER:
            print(f"{name:12s} {mod.__doc__.strip().splitlines()[0]}")
        return 0

    ctx = make_context(args.config, args.root, demo=args.demo, seed=args.seed)
    if ctx.demo:
        print("[demo] generating synthetic raw data ...")
        synthetic.generate_all(ctx)

    wanted = (
        [s.strip() for s in args.stages.split(",")]
        if args.cmd == "run" else [n for n, _ in ORDER]
    )
    unknown = set(wanted) - {n for n, _ in ORDER}
    if unknown:
        print(f"unknown stages: {sorted(unknown)}", file=sys.stderr)
        return 2

    summaries = {}
    for name, mod in ORDER:
        if name not in wanted:
            continue
        t0 = time.time()
        print(f"==> stage {name}")
        summary = mod.run(ctx)
        summaries[name] = summary
        print(f"    done in {time.time() - t0:.1f}s: "
              f"{json.dumps(summary, ensure_ascii=False)[:180]}")
    print(f"\nresults in: {ctx.results}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
