# Writer Brief (read fully before writing)

You are writing chapters of the book **Mastering Squad**, an original, very in-depth, beginner→expert, hands-on book about Squad (https://github.com/bradygaster/squad), an AI agent-team coordination system for GitHub Copilot. The book will be published as an EPUB.

## Key locations
- Book repo: `~/Projects/squad-book` (your working directory for all writes)
- Squad source at tag v1.1.0 (read-only research): `~/Projects/squad-src`
  - Docs-site pages: `~/Projects/squad-src/docs/src/content/docs/**.md`, published at `https://bradygaster.github.io/squad/docs/<slug>/`
  - Other docs: `~/Projects/squad-src/docs/specification/`, `docs/features/`, `docs/_internal/specs/`, `docs/src/content/blog/` (history/rationale)
  - Code: `packages/squad-cli/src`, `packages/squad-sdk/src`, `templates/`, `.github/agents/squad.agent.md` (the coordinator prompt), `samples/`, `CHANGELOG.md`
- The `squad` CLI v1.1.0 is installed (`squad --help`, `squad <cmd> --help`). Use it to verify commands and flags. You may run `squad init` etc. ONLY inside throwaway dirs under `/tmp/squad-book-scratch-<yourname>/` (init a git repo there first). Never run it inside ~/Projects.
- npm/npx are blocked in this environment. Don't try to install anything.

## Must read first
1. `research/STYLE-GUIDE.md` (chapter structure, voice, callouts, diagrams, depth, companion project): follow it exactly.
2. `research/CHAPTERS.md` (exact file names/titles; cross-reference other chapters as "Chapter N")
3. `research/coverage.csv`: the sources assigned to your chapter(s). Read EVERY assigned source in full. Then go further: read the related source code and templates so the "Under the Hood" sections are accurate and deep.
4. `sample/` (the Tasktrack companion project) before writing Hands-On sections.

## Rules
- Original prose in your own words. Don't copy doc paragraphs. Commands, config keys, file names, and short code excerpts are fine.
- Accuracy over volume. Verify every command, flag, file path, and config key against v1.1.0 source or `squad --help`. If a docs page describes something that isn't in v1.1.0 code, say so or use a `> **Preview:**` callout.
- Depth target: ~4,000–8,000 words per chapter. Cover every option and edge case in the assigned sources.
- Further Reading must include the exact URL for every source mapped to your chapter (see the style guide's URL formats). Verify with: `cd ~/Projects/squad-book && python3 scripts/check-coverage.py | grep "ch N:"`, which lists anything you still need to cite (ignore other chapters).
- Put exercise solutions + quiz answers in `exercises/solutions/chNN.md` (H1 `# Chapter N Solutions`, then `## Exercise Solutions` and `## Quiz Answers`).
- Validate every mermaid diagram with mmdc as described in the style guide.
- Only write your assigned files. Don't edit shared files (style guide, scripts, other chapters, metadata).
- When finished, reply with: files written, approximate word counts, any facts you could NOT verify, and any doc/code discrepancies you found.
