#!/usr/bin/env python3
"""Collect '## Quiz Answers' sections from exercises/solutions/volN/chNN.md into a per-volume Appendix E."""
import glob, os, re
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
titles = {(v, n): title for n, v, title in re.findall(r"^\| (\d+) \| (vol\d)/part-\d+/ch\d+-[^|]+\| ([^|]+?) \|$", open(os.path.join(root, "research/CHAPTERS.md")).read(), re.M)}
VOLS = {"vol1": range(1, 22), "vol2": range(1, 26)}
for vol, chapters in VOLS.items():
  out = ["# Appendix E: Quiz Answers", "",
       f"This appendix collects the answers to the chapter quizzes in this volume (Chapters {chapters[0]}–{chapters[-1]}). Full worked solutions to the exercises are in the book repository under `exercises/solutions/`.", ""]
  for f in sorted(glob.glob(os.path.join(root, f"exercises/solutions/{vol}/ch*.md"))):
      n = str(int(re.search(r"ch(\d+)", f).group(1)))
      if int(n) not in chapters: continue
      text = open(f, encoding="utf-8").read()
      m = re.search(r"^## Quiz Answers\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
      if not m: continue
      body = re.sub(r"^(#{3,6}) ", lambda h: "#" * min(len(h.group(1)) + 1, 6) + " ", m.group(1).strip(), flags=re.M)
      out += [f"## Chapter {n}: {titles.get((vol, n), '')}".rstrip(": "), "", body, ""]
  open(os.path.join(root, f"book/{vol}/appendices/app-E-quiz-answers.md"), "w", encoding="utf-8").write("\n".join(out))
  print(f"wrote {vol} Appendix E")
