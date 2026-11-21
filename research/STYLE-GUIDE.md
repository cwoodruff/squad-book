# Mastering Squad — Style Guide

## Voice & audience
- Audience: developers new to Squad, progressing to expert. Assume they know Git, GitHub, a terminal, and basic GitHub Copilot usage.
- Second person ("you"), active voice, friendly and precise. Explain *why* as well as *how*.
- **Original prose only.** Use the Squad docs and source as research, but write everything in your own words. Never paste doc paragraphs. Quote at most a sentence or two, attributed. Code, CLI commands, file names, and config keys may be reproduced exactly (MIT-licensed, factual).
- Target **Squad v2.0.0** (second edition; stable npm `latest`; tag `v2.0.0`, commit `26654f0c4dadb2625d764c1c69ec61da6c518094`). The first edition, written against Squad v1.1.0, is tagged `book-squad-v1.1.0` in this repository. Source checkout: the path given in `research/WRITER-BRIEF.md`.
- Version statements: write "Written against Squad v2.0.0" (title pages) and "targets Squad v2.0.0" (prefaces, part intros). Never say a part or chapter targets v1.1.0 or a preview. v1.1.0 and the 2.0 previews appear only as history ("introduced in 1.1.0", "in Squad 1.x…", Vol 2 Chapter 22, Appendix J).
- **2.0 is the present.** Describe 2.0.0 behavior in the present tense. Do not write "preview", "upcoming", "looking ahead", "will ship in 2.0" or "may change before stable" about anything in v2.0.0. Use `Preview` only for what is still experimental in v2.0.0 (see Callouts).
- Never invent commands, flags, config keys, file names, or APIs. If you can't verify something in the v2.0.0 source or docs, leave it out or label it clearly as unverified.

## Hosts: Copilot first
- **Volume 1 is Copilot-first.** It teaches the GitHub Copilot path (the default host of plain `squad init`). Claude Code and the other five hosts get short pointers only: at most one paragraph, no parallel Hands-On path, always cross-referenced to `Volume 2, Part IV`. The pointer sites are Chapters 1, 2, 6, 9, 17 and 21 (plan D3). Five more chapters carry only the host mention that `research/UPDATE-PLAN-2.0.md` §2 lists for them, and nothing more: Ch 5 (the short "One team, any host" note), Ch 10 (one sentence: fleet dispatch is Copilot-only), Ch 12 (one sentence on per-host model selection), Ch 18 (the non-Copilot reviewer and sign-off gates, plus one paragraph on advisory Claude hooks, without overclaiming for Copilot) and Ch 20 (one sentence on choosing a host). Exercises and quizzes in Volume 1 stay answerable on the Copilot path alone. Do not add other sites without the Lead Editor.
- **Volume 2, Part IV is the home of multi-host material**: Claude Code (plugin and full projection), the other hosts, projections and capability negotiation. Elsewhere in Volume 2, mention another host in a sentence and cross-reference Part IV.
- Name hosts consistently: GitHub Copilot (CLI, VS Code, app), Claude Code, Kiro, OpenCode, Cursor, OpenAI Codex, Google Antigravity. Client slugs in code font: `copilot`, `claude`, `kiro`, `opencode`, `cursor`, `codex`, `antigravity`, `all`.

## Links and package names
- **Docs site:** `https://github.github.com/squad/docs/<slug>/` (the upstream canonical host). The docs root is `https://github.github.com/squad/`. Do not "correct" it to `github.github.io` (that host also works, but the book uses `.com`), and never use the retired `bradygaster.github.io` host.
- **Repository:** `https://github.com/github/squad`. Pin files to `https://github.com/github/squad/blob/v2.0.0/<path>`. A file that exists only in v1.1.0 (a removed feature, a blog post kept as history) is pinned to `…/github/squad/blob/v1.1.0/<path>`. Never link `main` or an unpinned tree for facts.
- **Package and installer names keep `bradygaster`.** `@bradygaster/squad-cli`, `@bradygaster/squad-sdk`, `brew tap bradygaster/squad` (casks `squad`, `squad-preview`, `squad-insider`) and the WinGet IDs `bradygaster.Squad`, `.Preview`, `.Insider` are unchanged in 2.0. Only repo and docs links moved. Squad is "© Brady Gaster and contributors" (LICENSE unchanged).
- **Dates** are CHANGELOG release dates (v2.0.0 = 2026-11-18). Do not quote npm publish or tag dates.

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
5. `## Under the Hood`: a walkthrough of the relevant v2.0.0 source (`packages/squad-cli/src`, `packages/squad-sdk/src`, `templates/`, `.github/agents/squad.agent.md`) and/or specification docs. Cite paths like `packages/squad-sdk/src/ralph/…`. Show short, relevant code excerpts (≤ 25 lines each).
6. `## Pitfalls and Troubleshooting`
7. `## Summary`
8. `## Exercises`: 3–6 numbered exercises. Put solutions in `exercises/solutions/volN/chNN.md`.
9. `## Quiz`: 5–8 questions (multiple choice or short answer). Put answers in `exercises/solutions/volN/chNN.md` under a `## Quiz Answers` heading. These are also collected into Appendix H.
10. `## Further Reading`: a bullet list of **every** source assigned to this chapter in `research/coverage.csv`:
    - Doc-site pages: `https://github.github.com/squad/docs/<slug>/` (e.g. `https://github.github.com/squad/docs/features/routing/`)
    - Other repo files: `https://github.com/github/squad/blob/v2.0.0/<path>` (e.g. `.../blob/v2.0.0/docs/specification/core-v0.1.md`); v1.1.0 pins only for history sources the map keeps
    - `make coverage` fails if a mapped source is missing from its chapter.

## Callouts (Pandoc blockquotes)
- `> **Note:** …`
- `> **Tip:** …`
- `> **Warning:** …`
- `> **Preview:** …` only for things that are **experimental in v2.0.0**: the `squad_backend_*` tools, the execution harnesses, remote durable-server integration, v0.2 profile promotion, and anything else v2.0.0 labels experimental or unshipped. Never for shipped 2.0 behavior.
- `> **Note:** Changed in Squad 2.0: …` where a reader coming from 1.x needs a warning (removed commands, upstream precedence, nap behavior). Keep these short and factual.
- `> **Under the hood:** …` for short inline asides

## Depth
- "Very deep" coverage: each chapter should be roughly **4,000–8,000 words**, and Volume 2, Part IV reference chapters may run longer. Cover every option, flag, edge case, and interaction documented in the assigned sources, plus anything else found in the source code.
- Code blocks need language tags (`bash`, `json`, `yaml`, `ts`, `markdown`, `text`).
- Prefer tables for reference material.

## Terminology (match the official glossary)
Squad, coordinator, agent, charter, casting, team (`.squad/team.md`), routing (`.squad/routing.md`), decisions (`.squad/decisions.md`), history, skills, ceremonies, directives, Ralph (work monitor), Scribe (session logger), Rai, Fact Checker, response modes (Direct / Lightweight / Standard / Full), worktrees, state backends, SDK (`@bradygaster/squad-sdk`), CLI (`@bradygaster/squad-cli`). Use `squad` in code font for the command.

Squad 2.0 terms: host (an AI coding tool Squad projects into), client slug, host projection, plugin mode (the Squad plugin for Claude Code), member subagent, work claim, governed memory, launcher (`.squad/squad.mjs`), lockout, harness. Rai and Fact Checker are **optional built-ins** added with `squad roster add`. Distinguish a Squad plugin (`.squad/plugins/`) from the Squad plugin for Claude Code. Removed in 2.0 (history only): personal squad, consult mode, global squad (`--global`).

## Companion Project: "Tasktrack"
- Located in `sample/` (and documented in `sample/README.md`). It's a small, **zero-dependency** project: `api/` is a TypeScript REST API on `node:http` that Node 22.18+ runs directly through type stripping (`npm start`), `web/` is a static HTML/JS front end, and the tests use `node:test` (`npm test`). Endpoints: GET /health, GET/POST /tasks, PATCH/DELETE /tasks/:id. Read `sample/` before writing Hands-On sections.
- The reader builds it **with their Squad**. Each chapter's Hands-On section moves it forward, and readers can check their work against git tags `chNN-start` / `chNN-end`. These are described, not actually created, in the book. The sample folder holds the baseline starter (`ch03-start`).
- Progression (volume-relative numbering; Tasktrack runs on Squad v2.0.0 with the Copilot host throughout):
  - Volume 1: Ch 2–4 install, init, first session, cast the team; Ch 5–8 routing rules, parallel work, issues and labels; Ch 9–14 Ralph loop, PRD mode, coding agent, models, notifications, upgrades; Ch 15–19 memory, skills, ceremonies and governance, error recovery; Ch 20–21 scenario variations.
  - Volume 2: Ch 1–5 MCP server, state backend, second squad for `web/`, export/import, clients; Ch 6–10 hardening, container, CI, observability, DR drill; Ch 14–16 an SDK tool, plugin and hooks; Ch 18–21 project the same Tasktrack squad into additional hosts (always with a Copilot-only fallback); Ch 22 a 1.x→2.0 migration drill on a scratch copy pinned to Squad 1.1.0 (the main project is already on 2.0); Ch 24 capstone.

## Two-volume structure (supersedes earlier file-layout notes)
- Volume 1 *Using Squad* (Parts I–IV, Chapters 1–21) lives in `book/vol1/`; Volume 2 *Operating and Extending Squad* (Parts I–V, Chapters 1–25) lives in `book/vol2/`. Each volume numbers its parts and chapters from 1; an unqualified part or chapter reference always means the same volume. See `research/CHAPTERS.md`.
- Cross-volume references: write `Chapter 12 (Volume 2)` from Volume 1, and `Chapter 4 (Volume 1)` from Volume 2. Appendices G–J exist only in Volume 2; reference them from Volume 1 as `Appendix H (Volume 2)`. Write cross-volume part references as `Volume 2, Part IV`.
- Every chapter begins, immediately after its H1, with a prerequisites callout: `> **Prerequisites:** Chapters 3 and 4.` (list only the chapters a reader genuinely needs, usually 0–3; write `None.` when appropriate). Volume 2 chapters may say `Volume 1 (or equivalent Squad experience)` plus specific chapters.
- Lighter template for Volume 1, Part I (Chapters 1–4): `Configuration Reference` and `Under the Hood` are optional. Every other chapter keeps the full template.
- Each topic has one primary home; other chapters summarize in a sentence or two and cross-reference it rather than re-teaching it.
