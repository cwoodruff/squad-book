# Shared Appendices A, B, C, D, F: Squad v2.0.0 update (Ford)

Sources: 2.0.0 CLI help (`squad --help`, `squad <cmd> --help`), `SRC/squad-v2.0.0` (`cli-entry.ts`, `cli/commands/*.ts`, `cli/core/upgrade.ts`, `nap.ts`, `clients.ts`, `squad-sdk/src/client/adapters/claude-hooks.ts`, `lockout.ts`, `repo-launcher.ts`, `watch/config.ts`), CHANGELOG 2.0.0, `D/features/ralph.md`, and scratch `squad init` runs (Copilot only, `--client claude`, `--client claude --claude-plugin`, `--client all`) under the scratchpad.

## Appendix A (rewritten, same structure)
- Intro, global flags and caveats now target v2.0.0; `--global` documented as rejected (`Unknown option: --global`).
- Preview table merged into the main command table. Added rows: `client` (`list/ls [--json]`, `add [--dry-run]`, `sync [--dry-run]`, alias `clients`), `roster`, `lockout`, `hook`, `dashboard`. Updated: `init` (`--client`, `--claude-plugin`, charters always installed), `upgrade` (content-aware backup, `--client`, `--[no-]claude-plugin`, `--self`/`--insider`/`--force`, `--self --dry-run`), `triage`/`watch` (`--agent-preset`, `--claude-flags`, `--max-rounds`, `--max-duration`, `--claims`; malformed config stops watch), `loop` (`--yolo` default when no `--copilot-flags`), `cast`, `cost` (newest session), `nap` (archives, 15 KB / 5 or 3 sections), `memory` (shared store, case-insensitive class), `state-mcp --experimental-backend`, `doctor`, `health --json` metadata, `externalize --key` + `.owner.json`, `upstream` precedence, `sync` no-op for local/worktree, `status`.
- Removed `consult`, `extract`, `personal` rows and examples; new "Removed in 2.0" table (also `--global`, user-profile fallback).
- Examples gain 2.0 commands. Help caveats cite `hook.ts`, `lockout.ts`, `dashboard.ts` and `command-help.ts`; `health`, `hook` and `lockout` have no detailed help (FC #28). l.164 marketplace spec kept.
- Arthur follow-ups (all three applied):
  1. `cast` row: `squad cast --name/--role` writes the `## Built-in Support Agents` table when `team.md` has none, so a project's first cast lists Scribe, Ralph, Rai and Fact Checker.
  2. `roster` row: opts built-ins in "on a roster that already has the support table without them".
  3. `client` row: once `clients[]` has entries only those are listed, so after `client add claude` or removing another host, Copilot is not listed although its files remain.

## Appendix B (moderate)
- Init table re-observed from a v2.0.0 init: added `.squad/squad.mjs` (launcher lookup order incl. `~/.squad/cli.json`, `SQUAD_ALLOW_NPX`), `human-members.md`, `config.json` contents, support-table note. MCP rows fixed: `.mcp.json` authoritative; `.copilot/mcp-config.json` is a sample (`EXAMPLE-github`); VS Code `.vscode/mcp.json`. `--global` removed from option list; `lockouts.json` and casting `handwritten-archive-<sha256>/` noted.
- Read/update table: `governance/lockouts.json`, `upstream.json`, malformed config stops watch; nap thresholds paragraph (15 KB/5/3, logs 7 days, decisions 20 KB).
- Env vars: header v2.0.0; removed `SQUAD_PERSONAL_DIR`, `SQUAD_NO_PERSONAL`, `SQUAD_NAME` (absent from 2.0 source); added `SQUAD_CLI`, `SQUAD_ALLOW_NPX`, `SQUAD_WORKSTREAM`, `SQUAD_NONINTERACTIVE`, `SQUAD_EXPERIMENTAL_BACKEND`, `SQUAD_BACKEND_URL/TOKEN`, `SQUAD_BACKEND_HARNESSES`, `CLAUDE_PROJECT_DIR`, `SQUAD_DASHBOARD_NO_OPEN/CHILD`; `SQUAD_HOME` redefined.
- Preview section replaced by: "`.squad/config.json` keys" (`version`, `clients`, `claudePlugin`, `claudeHooks`, `claudePermissions`, `governance.authorities`, `memory.logLevel`, `watch.agentPreset`, `watch.claudeFlags` allow-list, `watch.claims` incl. object form; sourced per FC #44, not `D/reference/config.md`), "Static and managed project state", and "Host projection files" with separate full and plugin-mode Claude rows (verified by scratch init).
- Note: plan said `watch.claims` is "reserved"; source and `ralph.md` show it is functional (`none`/`git-ref`/object). Described as functional.

## Appendix C (moderate)
- Preview block folded into one alphabetical list. Added: Governed memory, Harness, Launcher, Lockout, Member subagent, Plugin mode, Squad plugin, Work claim, Global squad (removed). Reworded: Client, Host, Host projection, Fact Checker/Rai (optional built-ins), Insider channel (2.0 channels), `squad_state` MCP server, `HarnessAdapter`, Golden trace (no preview framing). Personal Squad and Consult mode marked "Removed in 2.0". Issue-driven development: GitLab replaced by Azure DevOps (GitLab not shipped). Entry separator kept as the existing em dash for consistency.

## Appendix D (light)
- Preview callout became a normal "Multi-Host Prompts" intro; SDK prompt says v2.0.0 API. Added two Claude Code prompts (cast with `squad cast` + `squad client sync`; watch with `squad dashboard`), both introduced in Vol 2 Ch 19.

## Appendix F (moderate)
- README/CHANGELOG lines say v2.0.0 (CHANGELOG date 2026-11-18). Preview block replaced by "Squad 2.0 resources" (release link repointed from `v2.0.0-preview.2` to `releases/tag/v2.0.0`, LINKS-2.0-LEFTOVERS l.61), plus Claude Code plugin page and multi-machine watch page. New "Historical (1.1.0)" block: consult-mode, personal-squad and README pinned to `blob/v1.1.0/`. l.7 docs root kept.
- All 63 URLs in A–D, F probed: all resolve except the pre-existing example `https://github.com/acme/shared-team.git` in an App A code block (intentional placeholder).

## Specific items
1. **`upgrade --self --dry-run`.** Confirmed: v1.1.0 `cli-entry.ts` calls `selfUpgradeCli({ insider, force })` without `dryRun`, and v1.1.0 `selfUpgradeCli` runs `execSync` unconditionally, so a 1.1.0 CLI installs for real. In v2.0.0, `cli-entry.ts` passes `dryRun` and `selfUpgradeCli` returns `performed: false` after printing "Dry run — would self-upgrade via …" (first in preview.2, CHANGELOG l.50). App A describes it as safe on 2.0 only and warns that a 1.1.0 CLI installs.
2. **`squad cast` built-ins.** Confirmed in source: `runCastAdd()` (`commands/cast.ts` l.413) calls `ensureBuiltinRoster()`, which adds a support table for every built-in with an installed charter when `team.md` lacks one; plain `squad cast` (no flags) does not. Arthur's scratch run agrees. Described in App A (`cast`, `roster`, `init`), App B and the glossary.

## Checks
- `make manuscript`: 0 structural errors (regenerated Appendix E as a side effect).
- `make coverage`: no misses for A–D, F; 48/48 modules (dashboard/lockout/hook strings now in App A). The two remaining misses are Appendix I (Trillian).

## Skipped
- Watch flags that exist but were never in App A (`--board-owner`, `--auth-user`, `--agent-cmd` on watch) stay out, as in the 1.1 edition.
