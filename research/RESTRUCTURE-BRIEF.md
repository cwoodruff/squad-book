# Restructure Brief (two-volume edition) — for editorial agents

Repo: ~/Projects/squad-book. Read research/CHAPTERS.md (new layout), research/STYLE-GUIDE.md (esp. the final "Two-volume structure" section).

The book was reorganized from 10 parts/47 chapters into two volumes, 9 parts, 46 chapters, continuous numbering:
- Volume 1 "Using Squad": Part I Getting Started (1–4), Part II Working with Squad Daily (5–14), Part III Making Teams Smarter (15–19), Part IV Adopting Squad (20–21).
- Volume 2 "Operating and Extending Squad": Part V Advanced Coordination (22–26), Part VI Production Operations (27–31), Part VII Internals and Extension (32–38), Part VIII Looking Ahead: Squad 2.0 (Preview) (39–43), Part IX Mastery (44–46).

Old→new chapter numbers: 1→1, 2→2, 3→2(merged), 4→3, 5→4, 6→32, 7→5, 8→33, 9→34, 10→6, 11→15, 12→16, 13→17, 14→18, 15→19, 16→7, 17→8, 18→9, 19→10, 20→11, 21→12, 22→13, 23→14, 24→22, 25→23, 26→24, 27→25, 28→26, 29→27, 30→28, 31→29, 32→30, 33→31, 34→20, 35→21, 36→35, 37→36, 38→37, 39→38, 40→44, 41→45, 42→46, 43→39, 44→40, 45→41, 46→42, 47→43.
Old→new appendix letters: A→A, B→B, C→G, D→H, E→C, F→I, G→D, H→E(quiz, generated per volume), I→J, J→F. Shared (both volumes): A CLI, B Config, C Glossary, D Sample Prompts, E Quiz Answers, F Resources. Volume 2 only: G SDK API, H Feature Matrix, I Spec Cheat Sheet, J Version History.

A script already remapped "Chapter N", "Part X", "Appendix X" references and added "(Volume 1)"/"(Volume 2)" to cross-volume chapter refs. It is mostly right but text was NOT rewritten for flow. Your job is editorial continuity in the files you own.

## Rules for every chapter you own
1. Immediately after the H1 line, add a blank line then a prerequisites callout: `> **Prerequisites:** Chapters 3 and 4.` List only what the reader genuinely needs (0–3 chapters; `None.` is fine). Volume 2 chapters may write `Volume 1 (or equivalent Squad experience); Chapter 22.` Must appear within the first 6 lines.
2. Fix sequencing language: "in the previous chapter", "the next chapter", "as we saw earlier", "later in this part", "Part II covered…" etc. must be true under the NEW order. Internals chapters (32–34) now come AFTER operations; memory/skills (15–17) now come AFTER daily workflows (5–14); scenario playbooks (20–21) close Volume 1; Squad 2.0 (39–43) precedes Mastery (44–46).
3. Verify every "Chapter N" / "Part N" / "Appendix X" reference points at the right content under the new numbering (check against CHAPTERS.md titles). Fix wrong ones. Cross-volume refs must carry "(Volume 1)"/"(Volume 2)". Remove accidental doubled annotations. Do NOT alter URLs, quoted upstream text, CLI output, or code.
4. Tasktrack (the running sample project) progression: make sure each Hands-On section's assumed starting state is consistent with what earlier chapters (in new order) built. Where a chapter now comes earlier than something it assumed, add a one-sentence setup note (e.g., "If you have not yet set up memory (Chapter 15), that's fine—this exercise doesn't need it.") rather than rewriting the exercise.
5. Dedupe principle: each topic has one primary home. Upgrades: ch14 (1.x) and ch43 (2.0). Clients/hosts: ch26 (1.1) and ch40–41 (2.0). State: ch23 (1.1 backends) and ch42 (2.0). SDK: ch35 (+ Appendix G reference). Prompts: Appendix D. If your chapter re-teaches one of these at length outside its home, compress to a short summary + cross-ref.
6. Keep everything else: do NOT remove "Further Reading" URLs (a coverage checker requires specific URLs to remain cited in specific chapters — never delete a https://bradygaster.github.io/squad/docs/... or github.com/bradygaster/squad/blob/... URL unless instructed; you may move one only if instructed). Keep section headings required by the template: "What You'll Learn"(starts "What You"), "Hands-On", "Configuration Reference", "Under the Hood", "Pitfalls", "Summary", "Exercises", "Quiz", "Further Reading" (Config Ref / Under the Hood optional only in Chapters 1–4).
7. Solutions live at exercises/solutions/chNN.md (already renumbered, H1 "# Chapter N Solutions", must keep a "## Quiz Answers" section). If you change exercises/quizzes, update the matching solutions file.
8. Original prose only; American English; no emoji; don't invent Squad features—check ~/Projects/squad-src (v1.1.0) or ~/Projects/squad-src-2 (v2.0.0-preview.2) if unsure.
9. Edit only files you own. Do not run git commands that change state (no commit/add/mv/checkout). Do not run the build. You may run `python3 scripts/check-manuscript.py` and `python3 scripts/check-coverage.py` (other agents' work-in-progress may cause unrelated failures; only care about your files).
10. When done, reply with a concise list of changes per file and anything you could not resolve.
