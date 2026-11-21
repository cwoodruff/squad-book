#!/usr/bin/env python3
"""Check research/sources.txt and research/coverage.csv against an upstream Squad checkout.

coverage.csv is hand-maintained and is the source of truth; this script no longer
generates it (the old generator used the pre-split 1-46 chapter numbers and would
overwrite the v2.0.0 map). Run it when retargeting to a new Squad tag:

    python3 -I research/build_coverage.py --src <squad checkout at the pinned tag>

It fails when:
  - an inventoried source is missing from the checkout (removed upstream);
  - an inventoried source has no coverage row, or a coverage row names a source
    that is not inventoried;
  - a source-modules.csv module is missing from the checkout.
It warns (does not fail) on upstream docs/**/*.md that are not inventoried, excluding
the blog, docs/_internal/ (curated by hand) and research/ trees.
Without --src it only runs the inventory/map consistency check.
"""
import argparse, csv, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXCLUDE = ("docs/blog/", "docs/src/content/blog/", "docs/_internal/", "docs/research/", "docs/node_modules/")

ap = argparse.ArgumentParser()
ap.add_argument("--src", type=Path, help="Squad checkout at the pinned tag (read-only)")
args = ap.parse_args()

inventory = {l.strip() for l in (HERE / "sources.txt").read_text().splitlines()
             if l.strip() and not l.startswith("#")}  # same rule as scripts/check-coverage.py
with (HERE / "coverage.csv").open() as f:
    mapped = {r["source"] for r in csv.DictReader(f)}
with (HERE / "source-modules.csv").open() as f:
    modules = [r["source_module"] for r in csv.DictReader(f)]

errors = []
errors += [f"unmapped inventory source: {s}" for s in sorted(inventory - mapped)]
errors += [f"mapped source not in inventory: {s}" for s in sorted(mapped - inventory)]
if args.src:
    errors += [f"missing upstream: {s}" for s in sorted(inventory) if not (args.src / s).exists()]
    errors += [f"missing upstream module: {m}" for m in modules if not (args.src / m).exists()]
    upstream = {str(p.relative_to(args.src)) for p in (args.src / "docs").rglob("*.md")}
    for s in sorted(upstream - inventory):
        if not s.startswith(EXCLUDE):
            print(f"warning: upstream doc not inventoried: {s}")
for e in errors:
    print(e)
print(f"inventory: {len(inventory)} sources, modules: {len(modules)}, errors: {len(errors)}")
sys.exit(1 if errors else 0)
