#!/usr/bin/env python3
"""Fail if any mapped Squad source is not cited (by slug or path) in its chapter/appendix file."""
import csv, glob, os, re, sys
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def find(ch):
    if ":" in ch:  # chapters are volume-qualified, e.g. vol2:5
        vol, num = ch.split(":")
        pats = [f"book/{vol}/part-*/ch{int(num):02d}-*.md"]
    else:
        pats = [f"book/shared/appendices/app-{ch}-*.md", f"book/vol2/appendices/app-{ch}-*.md"]
    m = [g for pat in pats for g in glob.glob(os.path.join(root, pat))]; return m[0] if m else None
missing, nofile = [], set()
# (coverage map, source inventory, pinned git ref). The whole book targets Squad v2.0.0
# (github/squad). Optional sets are read only when their files exist: the retired 2.0-preview
# pair (transitional) and a legacy v1.1.0 pair for history citations of removed sources.
# A coverage row may also carry its own `ref` column, which overrides the set's ref.
REPO = "https://github.com/github/squad"
SETS = [("coverage.csv", "sources.txt", "v2.0.0", True),
        ("coverage-2.0.csv", "sources-2.0.txt", "v2.0.0", False),
        ("coverage-legacy.csv", "sources-legacy.txt", "v1.1.0", False)]
rows, unmapped, unexpected = [], set(), set()
for cov, inv, ref, required in SETS:
    cov_p, inv_p = (os.path.join(root, "research", n) for n in (cov, inv))
    if not required and not (os.path.exists(cov_p) and os.path.exists(inv_p)): continue
    with open(cov_p) as f:
        set_rows = [dict(r, ref=(r.get("ref") or "").strip() or ref) for r in csv.DictReader(f)]
    with open(inv_p) as f:
        inventory = {line.strip() for line in f if line.strip() and not line.startswith("#")}
    mapped = {row["source"] for row in set_rows}
    unmapped |= inventory - mapped
    unexpected |= mapped - inventory
    rows += set_rows
if unmapped: print("Unmapped inventory sources:", sorted(unmapped))
if unexpected: print("Sources absent from inventory:", sorted(unexpected))
for row in rows:
    src, ch = row["source"], row["chapter"]
    f = find(ch)
    if not f: nofile.add(ch); continue
    text = open(f, encoding="utf-8").read()
    if "content/docs/" in src:
        slug = src.split("content/docs/")[1].removesuffix(".md")
        needle = f"/squad/docs/{slug}/"
    else:
        needle = src
    pinned = [f"{REPO}/{kind}/{row['ref']}/{src}" for kind in ("blob", "tree")]
    if needle not in text and not any(p in text for p in pinned): missing.append((ch, needle))
if nofile: print("Missing chapter files:", sorted(map(str, nofile)))
for ch, n in missing: print(f"ch {ch}: not cited -> {n}")
total = len(rows)
absent = sum(1 for row in rows if row["chapter"] in nofile)
print(f"coverage: {total-len(missing)-absent}/{total} sources cited")
module_errors = []
with open(os.path.join(root, "research/source-modules.csv")) as f:
    modules = list(csv.DictReader(f))
for row in modules:
    sections = row["book_section"].split("; ")
    if not any(
        os.path.isfile(os.path.join(root, section))
        and row["source_module"] in open(os.path.join(root, section), encoding="utf-8").read()
        for section in sections
    ):
        module_errors.append(row["source_module"])
if module_errors: print("Unreferenced source modules:", module_errors)
print(f"source modules: {len(modules)-len(module_errors)}/{len(modules)} referenced")
sys.exit(1 if (missing or nofile or unmapped or unexpected or module_errors) else 0)
