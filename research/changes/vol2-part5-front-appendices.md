# Change log: Vol 2 Part V, front matter, Appendices G–J (Squad 2.0.0)

Author: Trillian. Date: 2026-11-21. Branch `squad-2.0`, uncommitted. Base: the 1.1 text plus Slartibartfast's approved link rewrite (kept).

Checks: `make manuscript` passes (46 chapters, 0 structural errors; it regenerated both Appendix E files as a side effect). `make coverage` passes fully: 213/213 sources, 48/48 modules (Appendix I now cites ADR-002 and ADR-003). No Mermaid diagram was added or changed.

Ground truth: `SRC/squad-v2.0.0` (code, workflows, CHANGELOG, docs), diffs against `v1.1.0` and `v2.0.0-preview.2` in `SRC/squad`, and the 2.0.0 CLI run in a scratch copy of Tasktrack (`squad init`, `client add claude --dry-run`, `client add claude`, `client list`, `triage/init/upgrade/client --help`).

## `part-05/00-part.md`
- "returns to v1.1.0 after the Squad 2.0 preview" → assumes Part IV's multi-host material; targets Squad v2.0.0.

## Chapter 23 (cookbook)
- Polyglot recipe: `squad client add` / `squad client sync` after roster or routing changes, Copilot-only teammates need nothing extra, Appendix H pointer.
- FAQ: v2.0.0 command surface; `squad triage` also answers to `squad watch`; there is no `squad ralph` CLI command (`/squad:ralph` is a Claude Code plugin slash command).
- Config Reference: new row for `--claims git-ref`, `--max-rounds`, `--max-duration`, `--agent-preset claude` (from `squad triage --help`).
- All "v1.1.0 help/CLI" labels → v2.0.0 after checking 2.0.0 help (flags, init "safe to re-run" text unchanged).
- Skipped: the plan's "personal-squad pattern mention (1)": none exists in this file (only "consult each other" in plain English). Solutions unchanged (still correct).

## Chapter 24 (capstone)
- Intro and assumptions: production path runs on v2.0.0 with Copilot; install line `npm install -g @bradygaster/squad-cli` (`latest` = 2.0.0).
- Stage 5: `.mcp.json` entry runs the committed `.squad/squad.mjs` launcher (bare `squad state-mcp` for standalone); backend migration is transactional (memory and inbox in one commit; casting/routing stay on the source branch).
- New H3 at the end of Stage 8: **Optional: Project Tasktrack into a Second Host** (`squad client add claude --dry-run`, apply, `client list`, launch line, revert route, Copilot-only fallback). Expected output verified in scratch: dry run writes nothing; real run adds `.claude/agents/squad.md`, member subagents (built-ins included), `.claude/skills/`, `.claude/settings.json`, `.claude/.squad-permissions.json`, `CLAUDE.md`, updates `.gitignore` and `config.json`; Copilot files and `.mcp.json` untouched. `client add` prints no launch hint (only `init` does), so the text gives the line directly.
- Removed the old "Optional: Going multi-host" H3 under Summary (it used preview framing).
- Config Reference row for `squad client add/list`; Quiz 3, Under the Hood, Stage 8 OTel and Further Reading labels → v2.0.0; one em-dash pair in an edited sentence replaced.
- Solutions: Quiz 3 label; Quiz 4 describes the launcher.
- CI YAML re-checked: it installs nothing (no `@bradygaster/squad-cli`), so no change.

## Chapter 25 (contributing)
- Objectives and intro: v2.0.0, repo `github/squad`, npm names keep `@bradygaster/`.
- Feature proposals: issue/discussion first, ADRs under `docs/specification/`; root `CONTRIBUTING.md` still points at `docs/proposals/`, which stable promotion strips (`squad-promote.yml` l.229).
- Monorepo table: host adapters in the SDK row, new `plugins/squad/` row, `docs/` lists ADRs not proposals; one sentence on CONTRIBUTING's host-adapter checklist.
- CI: v2.0.0 triggers (adds `squad2-*`, `stack-*` bases); one sentence on `test/retired-symbols.test.ts`.
- Release section rewritten from v2.0.0 workflows: `squad-release.yml` is dispatch-only (no push trigger), needs `confirm_tag` + 40-char `expected_sha`, exact-SHA guard, `squad-release-verify.yml`, prerelease dist-tag chosen at dispatch, stable always `latest`, standalone/package-manager publication opt-in, latest-release promotion only with all assets. Promotion: sanitized merge, refuses consumed changesets, dispatches the stable release at the pushed SHA. Insider: also Homebrew `squad-insider` and WinGet `bradygaster.Squad.Insider`.
- Drift Note and Under the Hood: **correction**: the old text said the docs-site guide claims Node `>=20`; neither v1.1.0 nor v2.0.0 says that (both say 22.5.0). Kept the real drift (`build:cli`, independent versioning) and added CONTRIBUTING's stale `preview` branch and `docs/proposals/`.
- Config Reference, Summary, Quiz 2/5, Further Reading labels → v2.0.0; new Pitfall row (retired-symbol test). Mermaid unchanged.
- Solutions: Ex 1, Ex 5 (exact-SHA dispatch, promote dispatches stable), Quiz 8 labels.

## `00-front/00-title.md`
- Added "Second Edition" line and "Written against **Squad v2.0.0**…" sentence, matching Vol 1's title page.

## `00-front/01-preface.md`
- Opening and audience no longer "look ahead"; Part IV row "Squad 2.0: One Team, Many Hosts"; reading paths "Multi-host teams" (Part IV, Appendix H) and "Coming from Squad 1.x" (Ch 22 by its new title); Preview callout = "still experimental in Squad v2.0.0"; Versions paragraph (v2.0.0, 2026-11-18, Ch 22 for migration); new "What's New in the Second Edition" section modelled on Vol 1's.

## Appendix G (SDK API)
- Retargeted to v2.0.0. Removed personal/consult rows (`resolvePersonalSquadDir`, `ensurePersonalSquadDir`, `ensureSquadPathTriple`, `isConsultMode`, personal agents); added `isRetiredProfileTeamRoot`; `resolveGlobalSquadPath` described as externalize base only.
- Entry points: dropped `/agents/personal`; added `/clients` (deprecated), `/backend` (experimental), `/ralph/claims`, `/ralph/claims-git` (from v2.0.0 `package.json` exports).
- Root barrel map now includes the client adapter contract/host adapters and handwritten-registry repair; new rows for `casting/handwritten-registry` and `client/*`; upstream and memory rows gained the 2.0 exports.
- Complete symbol index regenerated against v2.0.0 by a script that follows every re-export from `src/index.ts`. Rows whose exports did not change are kept byte-identical; 7 changed rows replaced (`casting/durable-registry`, `config/markdown-migration`, `memory/index`, `resolution`, `runtime/usage-ledger`, `upstream/resolver`, `upstream/types`), 12 new rows (`casting/handwritten-registry`, `client/adapter-contract`, 10 `client/adapters/*`), 2 removed (`agents/personal`, `sharing/consult`).
- "Squad 2.0 (Preview)" section → "Client and Backend APIs" with a Changed-in-2.0 Note; adapter table adds `ProjectionFile` kinds, `ApplyAction` incl. `skipped`, `CLAUDE_PROJECTION_VERSION`, coordinator skills, Claude settings/hooks, plugin, lockouts, launcher; `uninstallClients` behavior. New H3 **Execution harnesses** (both harness classes and helpers, optional Claude Agent SDK peer `>=0.3.300 <0.4.0`, `SQUAD_BACKEND_HARNESSES`); one Preview callout for `/backend`.
- **Correction:** the old "Removed 1.x profile exports" said `discoverSquads`, `readSquadRegistry`, `writeSquadRegistry`, `findSquadByName` and the `CrossSquad*` types were gone from the 2.0 root. They are still exported by v2.0.0 `index.ts`. Rewritten, adding the removed consult exports and `/types` multi-squad types.

## Appendix H (feature matrix)
- Copilot-surface part: v2.0.0 compatibility docs; states it covers Copilot only.
- 2.0 section rewritten from v2.0.0 `D/reference/host-feature-matrix.md`, consistent with Ch 20: Note "reflects v2.0.0"; Claude per-spawn model ✓ (Copilot ×, with reason); Ralph CLI supported for Copilot and Claude; dual-root ✓ everywhere; Antigravity specialist MCP degraded; four all-host digest gaps; fleet dispatch Copilot-only; live evidence incl. harness runs (11-09, 11-10); counts 46/0/5/0, 44/0/4/3, 41/2/5/3, 42/1/5/3, 41/2/5/3, 41/2/5/3, 40/3/5/3; corrected coordinator paths (`.opencode/agents/`, `GEMINI.md`, `CLAUDE.md` blocks). One Preview callout for the backend row.

## Appendix I (spec cheat sheet)
- Intro v2.0.0 ("code wins"). README row: registers v0.2 profiles, no ADRs, stale "no harness ships". Charter row: `## Examples` (§7.1, `SQC011`). GitHub binding row: ADR-002 claim-ref amendment.
- Section renamed "Squad 2.0 Specifications and Decision Records"; Preview callout limited to the non-claimable v0.2 drafts (promotion §15/§14 pending). **Added ADR-002 and ADR-003 rows** (coverage now passes). ADR-001 row notes its stale no-harness sentence. v0.2 rows updated for the shipped harnesses and the adapter profile's stale status header.

## Appendix J (version history)
- One sentence: CHANGELOG dates; npm publication can lag a day or more. v1.1.0 is "the first edition's target".
- "Squad 2.0 (Preview) Version History" → "Squad 2.0 Version History"; preview.1 2026-10-23 and preview.2 2026-10-25 (were npm dates); added preview.3 (10-29), preview.4 (11-09), v2.0.0 (11-18, this book's target). New "v2.0.0 detail" section from the CHANGELOG. Dropped the "not stable" sentence; versioning guidance updated (experimental items, channels).
- Kept the blog links at `blob/v2.0.0` (approved rewrite; the eight posts are byte-identical between v1.1.0 and v2.0.0), although the plan said v1.1.0 pins. Arthur may want to rule on this.

## Not done / for others
- No `v2-chNN` tags added beyond the existing descriptive ones.
- Appendix E was regenerated by `make manuscript` (Slartibartfast owns the final regeneration).
- Pre-existing em dashes in untouched sentences and the "file — Title" separators in the Appendix I table were left (the two new ADR rows follow that table's convention).

## Upstream doc/code discrepancies found
1. `CONTRIBUTING.md` still lists `preview` as a staging branch (dev → preview → main) and requires `docs/proposals/`, which promotion strips.
2. `D/guide/contributing.md` CI section lists `npm run build:cli` (no such root script) and "independent versioning" while workflows align versions.
3. `squad-release.yml` defaults prerelease `npm_dist_tag` to `insider` (with a `preview` alias), whereas `D/insider-program.md` and Ch 8 describe `preview` as its own channel after GA.
4. `client-harness-adapters-v0.2.md` status header still says the seven-host model is "still being locked in"; its body describes two shipped harnesses. ADR-001 and the spec README still say no harness ships.
5. `squad client add --dry-run` reports only the host list, not the files it would write.
