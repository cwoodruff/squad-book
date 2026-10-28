#!/usr/bin/env python3
"""Check manuscript structure without requiring the upstream source checkout."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parent.parent
chapters = sorted(root.glob("book/vol*/part-*/ch*.md"))
errors = []
for path in chapters:
    number = int(path.name[2:4])
    vol = path.parts[-3]
    text = path.read_text()
    headings = re.findall(r"^## (.+)$", text, re.M)
    required_sections = ["What You", "Hands-On", "Pitfalls", "Summary", "Exercises", "Quiz", "Further Reading"]
    if vol == "vol2" or number > 4:  # Volume 1 Part I uses the lighter beginner template
        required_sections += ["Configuration Reference", "Under the Hood"]
    if "> **Prerequisites:**" not in "\n".join(text.splitlines()[:6]):
        errors.append(f"{vol}/{path.name}: missing prerequisites callout after the title")
    for required in required_sections:
        if not any(required in h for h in headings):
            errors.append(f"{vol}/{path.name}: missing {required} section")
    if not text.startswith(f"# Chapter {number}:"):
        errors.append(f"{vol}/{path.name}: incorrect chapter title")
    solution = root / f"exercises/solutions/{vol}/ch{number:02d}.md"
    if not solution.exists() or "## Quiz Answers" not in solution.read_text():
        errors.append(f"{vol}/{path.name}: missing solutions or quiz answers")
    if text.count("```mermaid") < 2:
        errors.append(f"{vol}/{path.name}: expected at least two diagrams")

for letter in "ABCDF":
    if len(list(root.glob(f"book/shared/appendices/app-{letter}-*.md"))) != 1:
        errors.append(f"Expected exactly one shared Appendix {letter}")
for letter in "GHIJ":
    if len(list(root.glob(f"book/vol2/appendices/app-{letter}-*.md"))) != 1:
        errors.append(f"Expected exactly one Volume 2 Appendix {letter}")
for vol, (lo, hi) in {"vol1": (1, 21), "vol2": (1, 25)}.items():
    found = sorted(int(p.name[2:4]) for p in root.glob(f"book/{vol}/part-*/ch*.md"))
    if found != list(range(lo, hi + 1)):
        errors.append(f"{vol}: expected Chapters {lo}–{hi}, without duplicates")
    sols = sorted(int(p.name[2:4]) for p in root.glob(f"exercises/solutions/{vol}/ch*.md"))
    if sols != list(range(lo, hi + 1)):
        errors.append(f"{vol}: expected solutions for Chapters {lo}–{hi}")
    if not (root / f"book/{vol}/00-front").is_dir():
        errors.append(f"{vol}: missing front matter")
for path in root.glob("book/**/*.md"):
    if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", path.read_text()):
        errors.append(f"{path.name}: contains an invalid XML control character")
for error in errors:
    print(error)
print(f"Manuscript: {len(chapters)} chapters; {len(errors)} structural errors")
sys.exit(bool(errors))
