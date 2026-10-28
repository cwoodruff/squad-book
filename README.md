# Mastering Squad

**Status: complete first manuscript.** EPUB structure and source coverage are checked automatically. This is not a claim that every SDK example or cloud deployment has been executed; see `research/VALIDATION.md` for the verification scope.

*AI Agent Teams for Any Project — published in two volumes*

| Volume | Title | Parts | Chapters | Output |
|---|---|---|---|---|
| 1 | Using Squad | I–IV: Getting Started, Working with Squad Daily, Making Teams Smarter, Adopting Squad | 1–21 | `dist/mastering-squad-vol1.epub` |
| 2 | Operating and Extending Squad | I–V: Advanced Coordination, Production Operations, Internals and Extension, Looking Ahead: Squad 2.0 (Preview), Mastery | 1–25 | `dist/mastering-squad-vol2.epub` |

Each volume numbers its parts and chapters from 1; cross-volume references name the volume, for example "Chapter 12 (Volume 2)" or "Volume 2, Part IV". See `research/CHAPTERS.md` for the full manifest.

An in-depth, hands-on book about [Squad](https://github.com/bradygaster/squad), the multi-agent coordination system that works with GitHub Copilot and, as of Squad 2.0, six other AI hosts. All parts except Volume 2, Part IV are written against **Squad v1.1.0** (the stable `latest` release) and take you from your first `squad init` to running squads in production and extending them with the SDK. Volume 2, Part IV covers **Squad 2.0 preview** (`v2.0.0-preview.2`, the `insider` channel): one team projected into GitHub Copilot, Claude Code, Kiro, OpenCode, Cursor, OpenAI Codex, and Google Antigravity.

- **2 volumes, 9 parts, 46 chapters** (21 in Volume 1, 25 in Volume 2), with appendices A–F in both volumes (E, Quiz Answers, is generated per volume) and G–J in Volume 2
- Every chapter starts with a prerequisites line and includes hands-on steps, a configuration reference, an "Under the Hood" source walkthrough, exercises, a quiz, and links to the official docs (Volume 1, Part I uses a lighter beginner template)
- **Tasktrack**, a companion project your Squad builds throughout the book (`sample/`)
- All 175 inventoried documentation/specification sources from v1.1.0 are mapped, plus 41 new or changed sources from v2.0.0-preview.2 (`research/sources-2.0.txt`, `research/coverage-2.0.csv`), along with 44 package source modules and root files. `make coverage` checks their references. Citation checks establish traceability, not exhaustive technical correctness.

## Repository layout

| Path | Contents |
|---|---|
| `book/vol1/`, `book/vol2/` | Per-volume front matter (`00-front/`), parts (`part-NN/00-part.md` + `chNN-*.md`), and volume-only appendices |
| `book/shared/appendices/` | Appendices A–D and F, included in both volumes |
| `book/vol*/appendices/app-E-quiz-answers.md` | Generated per volume from the quiz answers |
| `book/metadata-vol1.yaml`, `book/metadata-vol2.yaml` | Per-volume EPUB metadata |
| `book/images/` | Cover and images (`src/` holds sources) |
| `sample/` | Tasktrack companion project (zero dependencies, Node.js 22.18+) |
| `exercises/solutions/vol1/`, `exercises/solutions/vol2/` | Exercise solutions and quiz answers per chapter, numbered within each volume |
| `research/` | Style guide, chapter manifest, writer brief, source inventory, `coverage.csv` |
| `scripts/` | Build, Mermaid filter, coverage/link checks, cover rendering |
| `.github/workflows/build-epub.yml` | CI build: coverage and manuscript checks, both EPUBs, and epubcheck |

## Building the book

Prerequisites: [Pandoc](https://pandoc.org) 3.x, [epubcheck](https://www.w3.org/publishing/epubcheck/), [mermaid-cli](https://github.com/mermaid-js/mermaid-cli) (`mmdc`), and Google Chrome (used by `mmdc` and the cover renderer). On macOS:

```bash
brew install pandoc epubcheck mermaid-cli
```

`scripts/puppeteer.json` points `mmdc` at the system Chrome. Edit it, or set `PUPPETEER_CONFIG`, for other platforms.

```bash
make epub        # dist/mastering-squad-vol1.epub and -vol2.epub (renders Mermaid, regenerates Appendix E)
make html        # dist/mastering-squad-vol1.html and -vol2.html (single page each)
make validate    # build both volumes + epubcheck
./scripts/build.sh vol2 epub   # build a single volume
make coverage    # verify every Squad doc/spec source is cited in its chapter
make check       # coverage + chapter structure + build + EPUB validation
make links       # check external links
make cover       # re-render book/images/cover-vol1.png and cover-vol2.png from book/images/src/cover.html
```

## Trying the companion project

```bash
cp -r sample ~/tasktrack && cd ~/tasktrack
git init && git add . && git commit -m "Tasktrack starter"
npm test && npm start
```

## License

- Book text: © 2026 Chris Woodruff, licensed under [CC BY 4.0](LICENSE).
- Code samples, scripts, and Tasktrack: [MIT](LICENSE-CODE).
- Squad itself is © Brady Gaster and contributors, MIT licensed. This book is an independent work and isn't affiliated with or endorsed by the Squad maintainers.
