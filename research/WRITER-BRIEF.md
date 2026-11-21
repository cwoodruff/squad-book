# Writer Brief (read fully before writing)

You are writing chapters of **Mastering Squad, Second Edition**, an original, very in-depth, beginner→expert, hands-on book about Squad (https://github.com/github/squad), an AI agent-team coordination system. Squad's default host is GitHub Copilot; Squad 2.0 also projects one team into Claude Code, Kiro, OpenCode, Cursor, OpenAI Codex and Google Antigravity. The book is published as two EPUBs. The whole book targets **Squad v2.0.0**. The first edition (Squad v1.1.0) is tagged `book-squad-v1.1.0`.

For the 2.0 update, the per-chapter change list is `research/UPDATE-PLAN-2.0.md` (§2 and §3). Do what it lists for your files and keep everything else as close to the current text as possible.

## Key locations
- Book repo: the repository root (your working directory for all writes).
- Squad source (read-only research). `SRC` = `/private/tmp/claude-501/-Users-cwoodruff-Git-squad-book/6951efa4-a371-4f62-b4ea-94b9f725f30a/scratchpad/src`:
  - `SRC/squad-v2.0.0`: the target tree (tag `v2.0.0`, commit `26654f0c`).
  - `SRC/squad-v1.1.0`: history and comparisons only.
  - `SRC/squad`: full clone, so `git -C SRC/squad diff v1.1.0 v2.0.0 -- <path>` works.
  - Docs-site pages: `docs/src/content/docs/**.md`, published at `https://github.github.com/squad/docs/<slug>/`.
  - Other docs: `docs/specification/` (including ADR-001, ADR-002, ADR-003), `docs/features/`, `docs/_internal/specs/`, `docs/src/content/blog/` (history and rationale). `docs/proposals/` no longer exists.
  - Code: `packages/squad-cli/src` (`cli-entry.ts`, `cli/core/command-help.ts`, `cli/commands/*.ts`), `packages/squad-sdk/src` (including `client/adapters/*` and `backend/harnesses/*`), `templates/`, `plugins/squad/` (the Claude Code plugin), `.github/agents/squad.agent.md` (the Copilot coordinator prompt), `samples/`, `CHANGELOG.md`.
- The `squad` CLI **v2.0.0** is installed (`squad --version` reports `2.0.0`). Use `squad --help` and `squad <cmd> --help` to verify commands and flags. `squad hook` and `squad lockout` have no detailed help, and `hook` is missing from top-level help: verify those in the source and CHANGELOG. Run `squad init` and friends ONLY inside throwaway directories under `$TMPDIR/squad-book-scratch-<yourname>/` (run `git init` there first). Never run them inside the book repo.
- Don't install anything. Where a step needs a different Squad version (the Vol 2 Ch 22 1.1.0 drill), write the commands and let Marvin verify them.

## Must read first
1. `research/STYLE-GUIDE.md` (chapter structure, voice, version statements, links, hosts rule, callouts, diagrams, depth, companion project). Follow it exactly.
2. `research/CHAPTERS.md` (exact file names and titles; cross-reference other chapters as "Chapter N", adding the volume when it differs).
3. `research/UPDATE-PLAN-2.0.md`: the change list for your files, and the fact-check corrections folded into it.
4. `research/coverage.csv`: the sources assigned to your chapter(s). Read every assigned source in full, then the related source code and templates, so "Under the Hood" is accurate.
5. `sample/` (the Tasktrack companion project) before writing Hands-On sections.

## Version and link rules (summary; the style guide is authoritative)
- Present tense for 2.0.0. No "preview", "upcoming" or "looking ahead" framing for shipped behavior. `> **Preview:**` only for what is experimental in v2.0.0.
- v1.1.0 is history only. Re-check every "in v1.1.0…" claim against v2.0.0 before relabelling it: behavior changed in places (removed personal/consult/global modes, upstream precedence, nap, MCP guidance, `squad cost` scoping, plugin context injection). Never do a blind `v1.1.0` → `v2.0.0` replace.
- Docs links: `https://github.github.com/squad/docs/<slug>/`. Repo links: `https://github.com/github/squad`, pinned to `blob/v2.0.0/<path>` (or `blob/v1.1.0/<path>` for history). Package and installer names keep `bradygaster` (`@bradygaster/squad-cli`, `@bradygaster/squad-sdk`, `brew tap bradygaster/squad`, `bradygaster.Squad*`).
- Volume 1 is Copilot-first: Claude Code gets short pointers only, at the sites the plan names. Full Claude Code coverage is in Volume 2, Part IV.
- Dates are CHANGELOG release dates.

## Hosts (client slugs)
`copilot` (GitHub Copilot CLI, VS Code, app), `claude` (Claude Code), `kiro` (Kiro), `opencode` (OpenCode), `cursor` (Cursor), `codex` (OpenAI Codex), `antigravity` (Google Antigravity), or `all`. Plain `squad init` and `squad upgrade` still configure Copilot only; `--client <list>` adds hosts. Where a host needs its own sign-in or license, say so and give a Copilot-only fallback so every reader can finish the exercise.

## Rules
- Original prose in your own words. Don't copy doc paragraphs. Commands, config keys, file names and short code excerpts are fine.
- Accuracy over volume. Verify every command, flag, file path and config key against the v2.0.0 source or `squad --help`. Cite v2.0.0 source files for facts; the live docs site can run ahead of v2.0.0, so use it only for links.
- Depth target: ~4,000–8,000 words per chapter. Keep the existing H2 skeleton, file names and Tasktrack tags.
- Further Reading must include the exact URL for every source mapped to your chapter. Check with `python3 scripts/check-coverage.py | grep "<volN> ch N:"` (ignore other chapters).
- Exercise solutions and quiz answers live in `exercises/solutions/volN/chNN.md` (H1 `# Chapter N Solutions`, then `## Exercise Solutions` and `## Quiz Answers`). If you change an exercise or quiz item, update the solutions file in the same pass.
- Validate every Mermaid diagram with `mmdc` as described in the style guide.
- Only write your assigned files. Don't edit shared files (style guide, research files, scripts, metadata, images, sample, other owners' chapters). Don't commit.
- When finished, reply with: files changed, approximate word counts, facts you could NOT verify, and any doc/code discrepancies you found.
