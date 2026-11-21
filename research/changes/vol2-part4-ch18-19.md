# Change log: Vol 2 Part IV intro, Ch 18, Ch 19 (Squad v2.0.0)

Author: Trillian. Date: 2026-11-21. Branch `squad-2.0`, uncommitted. Base: tag `book-squad-v1.1.0`.
Ground truth: `SRC/squad-v2.0.0` (code, CHANGELOG, docs), diffed against `SRC/squad-v2.0.0-preview.2`; 2.0.0 CLI run in scratch directories only.

Files: `book/vol2/part-04/00-part.md`, `ch18-squad-2-overview.md`, `ch19-across-clients.md`, `exercises/solutions/vol2/ch18.md`, `ch19.md`.
Checks: `make manuscript` passes (0 structural errors; it regenerated Vol 2 Appendix E). `make coverage`: 211/213, the two misses are App I (ADR-002, ADR-003), not Part IV; 48/48 modules. Every Mermaid diagram validated with `mmdc`.

## `part-04/00-part.md`

Kept as left by the earlier run. It matches plan §3.1: title "Squad 2.0: One Team, Many Hosts", present tense, "targets Squad v2.0.0", Copilot-only readers can skim, 1.x readers start at Ch 22, Tasktrack already on 2.0, Ch 22 titled "Migrating from Squad 1.x to Squad 2.0". No change.

## Chapter 18 (≈6,600 → 8,700 words)

- Removed the `> **Preview:**` opener and the preview intro; new present-tense intro dated 2026-11-18.
- What You'll Learn: added the post-preview additions and the inventory objective; security objective rebased on shipped behavior.
- Host table: Claude row lists member subagents, skills, `.claude/settings.json`, plugin mode. Charter-inlining paragraph now names the Claude exception (named member subagents).
- Execution plane: harnesses now exist (`ClaudeAgentSdkHarness`, `CopilotSdkHarness`), registration rules; added one `> **Preview:**` callout for the experimental backend, harnesses, remote integration and v0.2 profile promotion (the only Preview callout left).
- ADR-001 section: added a paragraph on ADR-002 and ADR-003 (accepted 2026-11-13). Fixed one em dash.
- "What Changed in 2.0.0": new intro (four previews plus GA), `client add`/`client sync`; new subsections: Claude Code as a first-class host; self-contained coordinators (ADR-003, reviewer gate, sign-off gate, Scribe, stop on missing `squad_state`); portable launcher (1.1.0 wrote an exact-version `npx` spec; previews could write machine paths; verified in v1.1.0 `mcp-spec.ts`); governed memory and work claims; `github/squad`. Existing subsections de-previewed; casting repair gained the preview.3 0.9.x migration; bridge fixes gained health metadata, doctor exit status, symlink fix. Reversible-projection note corrected: no `client remove` in 2.0.0 (the 1.1 text implied a CLI removal path).
- Breaking table recast as the 1.x→2.0 checklist: kept the eight What's New rows; added launcher, `watch` config strictness, host Node.js. `docs/proposals/` deliberately not listed (FC #20).
- "What the 2.0 Docs Add or Correct": whatsnew is now "Current Stable Release"; fixed an existing error ("reverses an earlier-wins statement" → later-wins); flagged that the architecture page's Claude row omits member subagents/skills/settings.
- "The Security and Isolation Proposal: What Is Shipped?" → **"Security and Isolation in 2.0.0"**: table rebuilt from code and ADR-001 (static/mutable boundary, opt-in backend tools, projection merges, allow-listed upstream sources `upstream.ts`, scoped Claude permissions, local-only dashboard, epochs/cursors, G8). Proposal dropped as a source; Further Reading link removed (VALIDATION "remove" item).
- "Preview Channels…" → **"Release Channels and Optional Built-Ins"**: `latest` = 2.0.0, `preview`/`insider` remain, `upgrade --self` follows channel; previews as dated history. New paragraph: `squad cast` now adds a built-in support table (including Rai/Fact Checker when their charters are installed) to a `team.md` that lacks one (#2522, `cast.ts` `ensureBuiltinSupportSection`), verified in scratch.
- "Should I Adopt 2.0 Now?" → **"Who Needs Part IV?"** decision table (Copilot-only, mixed-host, 1.x, backend builders) and a new flowchart.
- Hands-On → **"Inventory What 2.0 Generated for Tasktrack"**: `squad client list`, `squad health --json`, `squad doctor`, optional `squad roster add rai`. Output excerpts are real 2.0.0 output from a scratch Tasktrack.
- Config Reference: added `client` subcommands, `--claude-plugin`, `claudePermissions`/`claudeHooks`, `.squad/squad.mjs`, health metadata.
- Under the Hood: help excerpt replaced with real v2.0.0 `cli-entry.ts` lines; deleted-module walkthrough kept as a short "What was removed (v1.1.0 paths)" list; added `test/retired-symbols.test.ts`; "Read source changes as preview contracts" → "Read the status labels" (notes ADR-001 still links the deleted proposals file).
- Pitfalls: replaced the three channel/preview pitfalls; added `squad cast` built-ins, no `client remove`.
- Summary rewritten. Exercise 4 (audit the safeguards) and 6 (take the inventory) rewritten; Quiz 4 and 8 reworded. Solutions updated (Ex 2, 4, 6; Q4, Q8).

## Chapter 19 (≈8,800 → 12,300 words)

- Removed the `> **Preview:**` opener. Learning objectives: `client add`/`client sync`, plugin vs full projection.
- One Team, Many Hosts: Claude member-subagent exception; `Agent` tool (formerly `Task`); diagram updated. Chapter 5 cross-reference put in present tense.
- "Installing the 2.0 Preview and Selecting Hosts" → **"Selecting Hosts"**: version check, `latest`, Chapter 22 pointer; `client sync` added; "no `client remove` in 2.0.0".
- Projection table: full Claude file set. New paragraph: every host's `squad_state` launch is the `node -e` root-finder + `.squad/squad.mjs state-mcp` (observed in scratch `.mcp.json`).
- New section **"Claude Code: Plugin or Full Projection"**: install commands, scopes, `--claude-plugin`/`--no-claude-plugin`, what plugin mode writes (verified by running it in scratch, including the allowlist and `.claude/.squad-plugin-settings.json`), plugin launcher order and `SQUAD_ALLOW_NPX`, choice table, trust prompt and scoped allowlist (`claudePermissions`), dashboard, advisory hooks and the `watch --agent-preset claude` runner (one paragraph; Vol 1 Ch 9 and Vol 2 Ch 20 own depth).
- Launching table and Claude subsection: plugin-mode launch (`claude`, `claude -p --agent squad:squad`), full-projection line kept (`claude --agent squad --mcp-config .mcp.json`, which `init` now prints).
- Polyglot section: cross-host decision flow (Scribe spawned in the same turn; Copilot reads only merged `decisions.md`) with a new sequence diagram; consistent roster fix.
- Static/mutable: plugin tool-name prefix; `squad cast` writes member subagents; never hand-write `.claude/` files.
- "Add or Remove a Host Later": `client sync`; two removal routes (Git, SDK); launcher spec note; Claude rollback now covers members, skills and settings rules.
- Additive merging: byte-exact block rollback; Claude settings and marker-owned member/skill files; `skipped` result action.
- "What's Different": install steps de-previewed; compatibility page's new Claude Code section summarized; doc lag flagged (across-clients scenario still says members are not projected).
- Hands-On: dropped the scratch-copy framing; starts from the 2.0 Tasktrack; `git tag v2-ch19-baseline`; `squad client add claude,codex`; full projection with a plugin-mode alternative; trust prompt; optional dashboard; Git removal route plus SDK route. Three hosts and the Copilot-only fallback kept.
- Config Reference: `client sync`, plugin flags, plugin install, `claudePermissions`, `claudeHooks`, `.claude/settings.json`, `squad dashboard`, `SQUAD_CLI`/`SQUAD_ALLOW_NPX`.
- Under the Hood: `client.ts` sync; **`packages/squad-cli/src/cli/commands/dashboard.ts`** and `cli/dashboard/server.ts`; Claude dispatch text in `coordinator.ts`; `claude-members.ts`, `claude-skills.ts`, `claude-hooks.ts`, `claude-plugin.ts` (short; Ch 20 owns depth).
- Pitfalls: four new Claude rows, roster drift.
- Summary rewritten. New Exercise 6 (plugin or full projection). Quiz 4 extended to plugin mode; Quiz 7 replaced (Antigravity quota → untrusted-folder allowlist). Solutions updated (Ex 1, 3, 4, 5, new 6; Q3, Q4, Q7).
- Further Reading: added **Squad for Claude Code (plugin)** (`/squad/docs/features/claude-code-plugin/`).

## Deliberately skipped

- No `v2-chNN` start/end tags added beyond the Hands-On's local `v2-ch19-baseline` tag (the 1.1 chapters had none).
- Did not run `uninstallClients()` (SDK not installed locally); removal claims come from `apply.ts`, `adapters.ts`, `claude-hooks.ts` and the CHANGELOG. Marvin may want to execute the Ch 19 removal steps once.
- Did not re-teach hooks, lockouts or the projection-version mechanics (Ch 20's home), the launcher internals or harnesses (Ch 21), or migration steps (Ch 22).
- Plugin-mode `disabledMcpjsonServers` diagnosis ("run `squad upgrade` to restore") is inferred from the projection code, not reproduced.

## Upstream discrepancies found

- `docs/specification/adr-001-…md` still links `docs/proposals/squad-2.0-security-and-isolation.md`, which is absent at v2.0.0.
- `D/concepts/squad-2-0-architecture.md` and `D/scenarios/using-squad-across-clients.md` list only the coordinator, `CLAUDE.md`, `.mcp.json` and `.gitignore` for Claude, and the latter says members are not projected. Both are stale against the v2.0.0 member subagents/skills/settings.
- `adapters.ts` header still says "five client host adapters".
- `squad upgrade --help` does not list `--claude-plugin` (top-level help does).
- `squad client add claude` on a Copilot-only repo sets `clients[]` to `["claude"]`; `client list` then omits Copilot although its files remain (Copilot is the base host).

## Facts for the Vol 2 front matter, Appendices G–J and shared appendices

- **Preface / App J:** v2.0.0 = 2026-11-18; previews 10-23, 10-25, 10-29, 11-09; ADR-003 accepted 2026-11-13. `latest` = 2.0.0; `preview` and `insider` channels and casks/WinGet IDs remain.
- **App A (CLI):** `squad client list [--json] | add <list> [--dry-run] | sync [--dry-run]` (alias `clients`, `ls`); `init --client <list> --claude-plugin`; `upgrade --client <list> --[no-]claude-plugin`; `squad dashboard [start|stop|status] --port --session --stream --detach --open --json` (port from 4280, state in `~/.squad/dashboards/` or `SQUAD_HOME`, `SQUAD_DASHBOARD_NO_OPEN=1`); `lockout reject|assign|submit|approve|override|status`; `hook` dispatched but not in help; `--global` fails with `Unknown option: --global`; `doctor` checks "portable squad_state launch" and exits non-zero on failure; `health --json` metadata (`cliVersion`, `sdkVersion`, `stateBackend`, `resolvedTeamDir`, `resolvedTeamRoot`, `resolvedSquadDir`, `bridgeVersion`, `launchMode`); bridge reports 15 tools.
- **App B/C (config, glossary):** `claudePlugin`, `claudePermissions` (`"off"`), `claudeHooks` (`"advisory"`/`"off"`), `watch.agentPreset`, `watch.claudeFlags`; files `.claude/.squad-permissions.json`, `.claude/.squad-plugin-settings.json`, `.squad/squad.mjs`; env `SQUAD_CLI`, `SQUAD_ALLOW_NPX`, `SQUAD_BACKEND_HARNESSES`, `CLAUDE_CONFIG_DIR`. Glossary: plugin mode, member subagent, launcher, projection v3.
- **App F (resources):** plugin page `https://github.github.com/squad/docs/features/claude-code-plugin/`; marketplace `github/squad`, plugin `squad@squad`, coordinator agent `squad:squad`, slash commands `/squad:ralph|cast|ceremony|status|dashboard`.
- **App G (SDK):** `ClaudeAgentSdkHarness`, `CopilotSdkHarness` (experimental, `/backend`); `uninstallClients(clients, ctx, keep?)`; `ApplyAction` includes `skipped`; `CLAUDE_PLUGIN_AGENT`, `CLAUDE_PLUGIN_MCP_PREFIX = mcp__plugin_squad_squad_state__`.
- **App H (feature matrix):** Claude Code: member subagents via `Agent` (`subagent_type`), `run_in_background`, `isolation: "worktree"`, per-spawn model, advisory hooks, watch preset; plugin needs no `.mcp.json` approval; allowlist needs a trusted folder; fleet dispatch Copilot-only.
- **App I:** ADR-002 and ADR-003 must be cited there (coverage currently fails on them).
- `squad cast` adds a built-in support table (Scribe, Ralph, Rai, Fact Checker, each only if its charter is installed) when `team.md` lacks one. Any appendix text saying Rai/Fact Checker reach the roster only via `squad roster add` should say "on a roster that already has the support table".
