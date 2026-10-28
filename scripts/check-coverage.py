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
# (coverage map, source inventory, pinned git ref) — v1.1.0 everywhere except Volume 2, Part IV, which uses the 2.0 preview
SETS = [("coverage.csv", "sources.txt", "v1.1.0"), ("coverage-2.0.csv", "sources-2.0.txt", "v2.0.0-preview.2")]
rows, unmapped, unexpected = [], set(), set()
for cov, inv, ref in SETS:
    with open(os.path.join(root, "research", cov)) as f:
        set_rows = [dict(r, ref=ref) for r in csv.DictReader(f)]
    with open(os.path.join(root, "research", inv)) as f:
        inventory = {line.strip() for line in f if line.strip()}
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
    pinned = f"https://github.com/bradygaster/squad/blob/{row['ref']}/{src}"
    if needle not in text and pinned not in text: missing.append((ch, needle))
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
