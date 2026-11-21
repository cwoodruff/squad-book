# Contributing

Corrections and improvements are welcome.

1. Read `research/STYLE-GUIDE.md` (structure, voice, callouts, diagrams) and `research/CHAPTERS.md` (file names).
2. Keep facts accurate to the Squad version stated in the preface. Verify commands with `squad --help` and the Squad source.
3. Write original prose. Don't paste text from the Squad docs. Link to them in **Further Reading** instead.
4. Before opening a PR, run `make check` (coverage + EPUB build + epubcheck).
5. When Squad releases a new version, add any new doc pages to `research/sources.txt` and `research/coverage.csv` by hand, then run `python3 -I research/build_coverage.py --src <squad checkout>` to validate them. The script checks the map. It does not generate it.
