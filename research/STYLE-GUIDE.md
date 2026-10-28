# Mastering Squad — Style Guide

## Voice & audience
- Audience: developers new to Squad, progressing to expert. Assume they know Git, GitHub, a terminal, and basic GitHub Copilot usage.
- Second person ("you"), active voice, friendly and precise. Explain *why* as well as *how*.
- **Original prose only.** Use the Squad docs and source as research, but write everything in your own words. Never paste doc paragraphs. Quote at most a sentence or two, attributed. Code, CLI commands, file names, and config keys may be reproduced exactly (MIT-licensed, factual).
- Target **Squad v1.1.0** (source checkout: `~/Projects/squad-src`, tag v1.1.0). Mark behavior that is preview/insider-only or only on `dev` with a Preview callout.
- Never invent commands, flags, config keys, file names, or APIs. If you can't verify something in the v1.1.0 source or docs, leave it out or label it clearly as unverified.

## Files
- One chapter per file: `book/volN/part-NN/chNN-short-slug.md` (two-digit chapter number, e.g. `ch07-routing.md`).
- Each part folder has `00-part.md` containing `# Part N — Title {.unnumbered}` plus a 1–2 paragraph introduction to the part.
- Appendices: `book/shared/appendices/app-X-slug.md` (A–D, F) or `book/vol2/appendices/app-X-slug.md` (G–J); Appendix E is generated per volume.
- The chapter file begins with a single H1: `# Chapter N: Title`. Use H2/H3 for sections; don't use H1 anywhere else.
- Diagrams: write them **inline** as fenced ```` ```mermaid ```` blocks. The build renders them to PNG automatically through `scripts/mermaid.lua`. Include **at least 2 diagrams per chapter** (flowchart, sequenceDiagram, stateDiagram-v2, or classDiagram). Keep them valid Mermaid: quote labels that contain special characters, e.g. `A["squad init"]`. Don't use HTML in labels. Validate each diagram before finishing: write it to a temp file and run `mmdc -p scripts/puppeteer.json -i /tmp/x.mmd -o /tmp/x.png` from the repo root.

## Required chapter structure (H2 headings, in this order)
1. `## What You'll Learn`: 4–7 bullet learning objectives.
2. Concept sections (several H2s): deep explanation with examples, tables, and diagrams.
3. `## Hands-On: <title>`: a companion-project step (see Companion Project below), with exact commands and expected results.
4. `## Configuration Reference`: tables of the relevant files, keys, flags, and environment variables, with defaults (omit only if truly N/A).
5. `## Under the Hood`: a walkthrough of the relevant v1.1.0 source (`packages/squad-cli/src`, `packages/squad-sdk/src`, `templates/`, `.github/agents/squad.agent.md`) and/or specification docs. Cite paths like `packages/squad-sdk/src/ralph/…`. Show short, relevant code excerpts (≤ 25 lines each).
6. `## Pitfalls and Troubleshooting`
7. `## Summary`
8. `## Exercises`: 3–6 numbered exercises. Put solutions in `exercises/solutions/volN/chNN.md`.
9. `## Quiz`: 5–8 questions (multiple choice or short answer). Put answers in `exercises/solutions/volN/chNN.md` under a `## Quiz Answers` heading. These are also collected into Appendix H.
10. `## Further Reading`: a bullet list of **every** source assigned to this chapter in `research/coverage.csv`:
    - Doc-site pages: `https://bradygaster.github.io/squad/docs/<slug>/` (e.g. `https://bradygaster.github.io/squad/docs/features/routing/`)
    - Other repo files: `https://github.com/bradygaster/squad/blob/v1.1.0/<path>` (e.g. `.../blob/v1.1.0/docs/specification/core-v0.1.md`)
    - `make coverage` fails if a mapped source is missing from its chapter.

## Callouts (Pandoc blockquotes)
- `> **Note:** …`
- `> **Tip:** …`
- `> **Warning:** …`
- `> **Preview:** …` for features not in v1.1.0 stable
- `> **Under the hood:** …` for short inline asides

## Depth
- "Very deep" coverage: each chapter should be roughly **4,000–8,000 words**, and Volume 2, Part IV reference chapters may run longer. Cover every option, flag, edge case, and interaction documented in the assigned sources, plus anything else found in the source code.
- Code blocks need language tags (`bash`, `json`, `yaml`, `ts`, `markdown`, `text`).
- Prefer tables for reference material.

## Terminology (match the official glossary)
Squad, coordinator, agent, charter, casting, team (`.squad/team.md`), routing (`.squad/routing.md`), decisions (`.squad/decisions.md`), history, skills, ceremonies, directives, Ralph (work monitor), Scribe (session logger), Rai, Fact Checker, response modes (Direct / Lightweight / Standard / Full), worktrees, state backends, SDK (`@bradygaster/squad-sdk`), CLI (`@bradygaster/squad-cli`). Use `squad` in code font for the command.

## Companion Project: "Tasktrack"
- Located in `sample/` (and documented in `sample/README.md`). It's a small, **zero-dependency** project: `api/` is a TypeScript REST API on `node:http` that Node 22.18+ runs directly through type stripping (`npm start`), `web/` is a static HTML/JS front end, and the tests use `node:test` (`npm test`). Endpoints: GET /health, GET/POST /tasks, PATCH/DELETE /tasks/:id. Read `sample/` before writing Hands-On sections.
- The reader builds it **with their Squad**. Each chapter's Hands-On section moves it forward, and readers can check their work against git tags `chNN-start` / `chNN-end`. These are described, not actually created, in the book. The sample folder holds the baseline starter (`ch03-start`).
- Progression: ch2–4 install/init/first session; ch5 cast the team; ch7–8 routing rules; ch11–14 decisions, memory, skills, ceremonies; ch16–19 issues, labels, Ralph loop, PRD mode; ch20–23 coding agent, models, notifications, upgrades; ch24–28 MCP server, state backend, second squad for `web/`, export/import; ch29–33 hardening, container, CI, OTel, DR drill; ch34–35 scenario variations; ch36–38 an SDK tool + plugin + hooks; ch41 capstone.

## Two-volume structure (supersedes earlier file-layout notes)
- Volume 1 *Using Squad* (Parts I–IV, Chapters 1–21) lives in `book/vol1/`; Volume 2 *Operating and Extending Squad* (Parts I–V, Chapters 1–25) lives in `book/vol2/`. Each volume numbers its parts and chapters from 1; an unqualified part or chapter reference always means the same volume. See `research/CHAPTERS.md`.
- Cross-volume references: write `Chapter 12 (Volume 2)` from Volume 1, and `Chapter 4 (Volume 1)` from Volume 2. Appendices G–J exist only in Volume 2; reference them from Volume 1 as `Appendix H (Volume 2)`. Write cross-volume part references as `Volume 2, Part IV`.
- Every chapter begins, immediately after its H1, with a prerequisites callout: `> **Prerequisites:** Chapters 3 and 4.` (list only the chapters a reader genuinely needs, usually 0–3; write `None.` when appropriate). Volume 2 chapters may say `Volume 1 (or equivalent Squad experience)` plus specific chapters.
- Lighter template for Volume 1, Part I (Chapters 1–4): `Configuration Reference` and `Under the Hood` are optional. Every other chapter keeps the full template.
- Each topic has one primary home; other chapters summarize in a sentence or two and cross-reference it rather than re-teaching it.
