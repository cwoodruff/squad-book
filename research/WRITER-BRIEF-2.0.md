# Writer Brief — Part X: Squad 2.0 (Preview)

Read `research/WRITER-BRIEF.md` and `research/STYLE-GUIDE.md` first. Every rule in them applies. The exceptions below override them for Part X.

## Version target for Part X
- Part X targets **Squad `v2.0.0-preview.2`**. That is the npm `insider` channel, with `preview` as an alias. `latest` is still v1.1.0. Install with `npm install -g @bradygaster/squad-cli@insider` or `squad upgrade --self --insider`.
- Source checkout at that tag (read-only): `~/Projects/squad-src-2`. The v1.1.0 checkout is still at `~/Projects/squad-src` for comparisons (`git -C ~/Projects/squad-src diff v1.1.0 v2.0.0-preview.2 -- <path>` works there).
- The installed `squad` CLI is **v1.1.0**, so it does NOT have `--client`, `roster`, etc. Verify 2.0 commands and flags against the source instead: `packages/squad-cli/src/cli-entry.ts`, `packages/squad-cli/src/cli/core/command-help.ts`, `packages/squad-cli/src/cli/commands/*.ts`, `packages/squad-cli/src/cli/core/clients.ts`, and `packages/squad-sdk/src/client/adapters/*`. Don't run any 2.0 build.
- Open each Part X chapter with a `> **Preview:**` callout. It should say the chapter describes Squad 2.0 (`v2.0.0-preview.2`, insider channel) and that details may change before 2.0.0 is stable. You don't need a Preview callout on every paragraph after that.
- Further Reading URLs:
  - Docs-site pages: `https://bradygaster.github.io/squad/docs/<slug>/` (the live site already shows 2.0 content)
  - Other repo files: `https://github.com/bradygaster/squad/blob/v2.0.0-preview.2/<path>`
  - Your sources are listed in `research/coverage-2.0.csv`. Check them with `python3 scripts/check-coverage.py | grep "ch N:"`.
- "Under the Hood" cites `v2.0.0-preview.2` source paths.
- Cross-reference the v1.1.0 chapters (Parts I–IX) where a 2.0 feature changes something taught there. Name the chapter, e.g. "Chapter 28 described…; in 2.0…".

## Seven hosts (slugs)
`copilot` (GitHub Copilot CLI/VS Code), `claude` (Claude Code), `kiro` (Kiro), `opencode` (OpenCode), `cursor` (Cursor), `codex` (OpenAI Codex), `antigravity` (Google Antigravity), or `all`.

## Companion project
Hands-On sections continue Tasktrack (`sample/`). In Part X the reader upgrades their Tasktrack squad to 2.0 and projects it into additional hosts. Use tags `chNN-start`/`chNN-end` as described elsewhere. Commands must be exact for 2.0. Where a host needs its own sign-in or license, say so, and give a Copilot-only fallback path so every reader can finish the exercise.

## Boundaries
Write ONLY your assigned files: your chapter file(s) and `exercises/solutions/chNN.md`. Don't edit other chapters, appendices, scripts, or research files. Other agents are writing the other Part X chapters at the same time, and separate agents are adding short 2.0 cross-reference callouts to Parts I–IX and the appendices. Keep your chapter self-contained, and cross-reference sibling chapters by number:
- 43 Squad 2.0: What Changed and Why
- 44 Using Squad Across Clients
- 45 Host Projections, Client Adapters, and Capability Negotiation
- 46 The State MCP Boundary, Runtime Upstreams, and the Experimental Backend
- 47 Upgrading to Squad 2.0 and the Road Ahead
