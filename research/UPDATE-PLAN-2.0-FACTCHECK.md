# Fact Check: UPDATE-PLAN-2.0.md

Reviewer: Fact Checker. Date: 2026-11-20. Advisory only; nothing in the plan was edited.

**Scope.** Section 1 (delta inventory), the specific "change X to Y" and "verify" items in sections 2–3, and section 4 (global changes).
**Evidence base.** `SRC/squad-v2.0.0`, `SRC/squad-v1.1.0` and `SRC/squad` (tags). The installed CLI at `~/.claude/plugins/cache/squad/squad/2.0.0/bin/squad` (`--version` = `2.0.0`), with `--help` run in a scratch directory. `npm view` against the public registry, using a temporary cache. `curl` status checks on 2026-11-20.
`SRC` = `/private/tmp/claude-501/-Users-cwoodruff-Git-squad-book/6951efa4-a371-4f62-b4ea-94b9f725f30a/scratchpad/src`. `D/` = `docs/src/content/docs/` in v2.0.0. `CL` = v2.0.0 `CHANGELOG.md`.

Ratings: ✅ verified · ⚠️ partially verified or caveat · ❌ contradicted · 🔍 unverifiable

## Summary

| Rating | Count |
|---|---|
| ✅ | 63 |
| ⚠️ | 11 |
| ❌ | 2 |
| 🔍 | 0 |

The plan is accurate on every high-risk removal and behaviour claim: personal squads, consult mode, `--global`, upstream precedence, nap, the MCP files, watch flags, the plugin, the ADRs, the launcher, the harnesses, plugin spawn paths and the proposals. The two ❌ items and most ⚠️ items are about wording or sourcing, not direction.

## 1. Release identity, packages, URLs

| # | Claim | Rating | Evidence | Correction |
|---|---|---|---|---|
| 1 | Target v2.0.0, tag commit `26654f0c4dadb2625d764c1c69ec61da6c518094` | ✅ | `git rev-list -n1 v2.0.0` | — |
| 2 | v2.0.0 "released 2026-11-18" | ⚠️ | CL l.7 says 2026-11-18. The annotated tag is dated 2026-11-19 13:44 UTC, and npm `time["2.0.0"]` = `2026-11-19T13:48:34Z`. | Say "dated 2026-11-18 in the CHANGELOG (published to npm 2026-11-19)", or pick one convention and use it everywhere (see #60). |
| 3 | npm `latest` = 2.0.0 | ✅ | `npm view @bradygaster/squad-cli dist-tags`: `latest: '2.0.0'`. The SDK is the same. | — |
| 4 | npm names unchanged (`@bradygaster/squad-cli`, `-sdk`) at 2.0.0; Node `>=22.5.0` | ✅ | `packages/squad-{cli,sdk}/package.json` `version` 2.0.0, `engines.node ">=22.5.0"`; CL l.34 | — |
| 5 | Repo moved to `github/squad` | ✅ | CL l.32–34, preview.4 "Changed". `api.github.com/repos/bradygaster/squad` → `"fork": true`, parent `github/squad`. | — |
| 6 | Docs: `site` = `https://github.github.com`, base `/squad/`; both hosts return 200; use `.io` | ⚠️ | `docs/astro.config.mjs` l.11–12. `curl` → 200 for `github.github.io/squad/docs/features/claude-code-plugin/` and for the `.com` form. Upstream names `.com` as canonical: CL l.33 ("`https://github.github.com/squad/`"), preview.4 "documentation links (`github.github.com/squad`)", and README links. | Fine as Chris's choice, but writers should know the upstream canonical host is `.com`. Record the decision in STYLE-GUIDE so nobody "corrects" it back. |
| 7 | Old docs host (`bradygaster.github.io/squad/...`) | ✅ (strengthens plan) | `curl` → 404 for `/squad/docs/get-started/installation/` and the plugin page | The URL rewrite (WP-S1) is mandatory, not cosmetic. |
| 8 | Pinned blobs must move to `github/squad` | ✅ (strengthens plan) | `github.com/bradygaster/squad/blob/v1.1.0/docs/.../consult-mode.md` → 404 (the fork has no tags). `github.com/github/squad/blob/v1.1.0/...consult-mode.md` → 200. | v1.1.0 history pins work only under `github/squad`. |
| 9 | Homebrew `bradygaster/squad`, casks `squad`/`squad-preview`/`squad-insider`; WinGet `bradygaster.Squad[.Preview/.Insider]`; install script under `raw.githubusercontent.com/github/squad/main/...` | ✅ | `D/get-started/installation.md` l.44–72. `curl` install.sh → 200. | — |
| 10 | Standalone `REPO` default `github/squad`; action input `repository: github/squad` because older pins default to the fork | ✅ | `D/features/standalone-install.md` l.32, l.139 | — |
| 11 | Channels: `latest` stable, `preview` = RCs, `insider` = dev snapshots; during the previews `preview` was an alias of `insider` | ✅ | `D/insider-program.md` l.22–32 (`dev (release candidate) → preview prerelease`); CL preview.1–4 headers ("`preview` retained as a compatibility alias"). Live dist-tags: `preview: 2.0.0-preview.4`, `insider: 2.0.0`. | Writers should not print current dist-tag values; `preview` still points at preview.4 today. |
| 12 | gh-aw: `gh aw add "github/squad/workflows@${SQUAD_SHA}"`, 40-char SHA, manifest preflight `workflows/squad-workflows.manifest.json` | ✅ | `D/guide/gh-aw.md` l.105–131; the file exists in the tree; diff +215/−37 | — |
| 13 | LICENSE unchanged ("© Brady Gaster and contributors") | ✅ | Not in `git diff --stat v1.1.0 v2.0.0`. `.claude-plugin/marketplace.json` owner is still Brady Gaster. | — |

## 2. Removed features

| # | Claim | Rating | Evidence | Correction |
|---|---|---|---|---|
| 14 | `squad personal`, `init --global`, `upgrade --global` removed; `--global` fails with a 2.0 message | ✅ | `packages/squad-cli/src/cli-entry.ts` l.141–142: `fatal("Unknown option: --global ... Squad 2.0 keeps teams in the project .squad/ only...")`. `commands/personal.ts` is absent in v2.0.0. | — |
| 15 | `squad consult`, `squad extract` removed; `consult.ts`, `extract.ts` deleted | ✅ | `ls packages/squad-cli/src/cli/commands/` in v1.1.0 vs v2.0.0 | — |
| 16 | `.squad/` resolves only from cwd and parents; `status/doctor/cast/cost` fail with "No squad in this directory" outside a project | ✅ | CL l.229 (preview.1 Breaking) | — |
| 17 | `multi-squad.ts` gone; `resolveGlobalSquadPath()` survives only as the externalize base; commit f1549687 | ✅ | File is absent. CL l.229 ("remains only as the base of externalized project state"). `git show f1549687` = "remove personal squads, consult mode and the global squad". | — |
| 18 | `./shell/sdk-bridge` export removed | ✅ | CL l.235. Not in `packages/squad-cli/package.json` exports. | — |
| 19 | Docs pages `features/consult-mode`, `guide/personal-squad` removed | ✅ | `git diff --name-status v1.1.0 v2.0.0 -- docs` → `D` for both. Live `github.github.io/.../consult-mode/` → 404. | — |
| 20 | All of `docs/proposals/` (8 files) removed at stable promotion, commit 27819b1f | ⚠️ | 27819b1f "sanitize promotion branch for v2.0.0" deletes all 8 files. But v1.1.0 never had `docs/proposals/` (`ls-tree v1.1.0` → 0 files; the 8 files exist only in preview.2–4). | Move this row from §1.1 (v1.1.0→v2.0.0) to §1.2 (preview.2→2.0.0). For a 1.x reader it is not a removal, so Vol 1 prose and the Ch 18 1.x checklist must not list it. |
| 21 | Personal Squad and Consult Mode sections gone from `squad.agent.md` (Vol 1 Ch 3) | ✅ | v1.1.0 `.github/agents/squad.agent.md` l.152 "### Personal Squad", l.361 "### Consult Mode Detection". In v2.0.0, 0 "personal squad" hits; the one "consult" hit (l.149) is the ordinary verb. | — |

## 3. New commands and flags

| # | Claim | Rating | Evidence | Correction |
|---|---|---|---|---|
| 22 | `init/upgrade --client <list>`; slugs `copilot claude kiro opencode cursor codex antigravity` or `all`; persisted in `clients[]` | ✅ | `squad client --help` "Hosts: copilot, claude, kiro, opencode, cursor, codex, antigravity, or "all""; CL preview.1 "Added" | — |
| 23 | `--claude-plugin` / `--no-claude-plugin` records `"claudePlugin": true` | ✅ | `squad --help` (`--[no-]claude-plugin`); CL l.67–73 | — |
| 24 | `client list [--json]`, `client add <list> [--dry-run]`, `client sync [--dry-run]`; `clients` alias; `sync` new since preview.2 | ✅ | `squad client --help`; `cli-entry.ts` l.557 (`'client' \|\| 'clients'`); CL 2.0.0 "Changed" (#2456) | — |
| 25 | `roster add\|remove <rai\|fact-checker\|all> [--dry-run]`; aliases `disable`, `uninstall`; `upgrade` never edits `team.md` | ✅ | `squad roster --help` ("Aliases for remove: disable, uninstall"); CL preview.2 | — |
| 26 | `squad dashboard [start\|stop\|status]` with `--port --session --stream --detach --open --json`; 127.0.0.1 from 4280; `~/.squad/dashboards/` or `SQUAD_HOME` | ✅ | `squad dashboard --help`; CL l.75–82 | — |
| 27 | `squad lockout reject\|assign\|submit\|approve\|override\|status` → `.squad/governance/lockouts.json` | ✅ | `squad --help` l. "lockout"; `commands/lockout.ts` l.58–79; `sdk/.../adapters/lockout.ts` l.18 | — |
| 28 | `squad hook claude <Event>` | ⚠️ | Exists (`cli-entry.ts` l.569; CL l.100). Missing from top-level `squad --help`, and `squad hook --help` / `squad lockout --help` print "No detailed help is available". | App A should cite source and CL for `hook` and `lockout` arguments, not `--help`. The plan names `--help` as the App A source of truth. |
| 29 | `squad state-mcp [--experimental-backend]` or `SQUAD_EXPERIMENTAL_BACKEND=1` | ✅ | `squad state-mcp --help` | — |
| 30 | `watch --claims <none\|git-ref>`, `--max-rounds`, `--max-duration 8h`, `--agent-preset <copilot\|claude>`, `--claude-flags`; claims default `none` | ✅ | `squad watch --help` lists all of them (plus `--health`); CL preview.3 "Added" | — |
| 31 | `watch.claudeFlags` limited to permission-mode, model, fallback-model, effort, max-turns | ✅ | `commands/watch/config.ts` l.175–181 (`CLAUDE_FILE_FLAGS`). CL l.106 omits fallback-model; the source wins. | — |
| 32 | `squad externalize --key`; ownership in `.owner.json` | ✅ | `squad --help`; `D/features/external-state.md` | — |
| 33 | `health --json`: `cliVersion`, `sdkVersion`, `stateBackend`, `resolvedTeamRoot`, `resolvedSquadDir`, `resolvedTeamDir` kept; schema `squad-health/v1` | ✅ | `commands/health.ts` l.29, l.49–57; CL l.118 | Note: `squad-health/v1` already existed in v1.1.0, so do not call the schema new. |
| 34 | `squad upgrade` content-aware, `.local-backup`, `--dry-run` writes nothing; never-touched list | ✅ | `squad --help` upgrade block: "Never touches: team.md, routing.md, decisions, agents/*/history.md, casting registry/history, config.json, .ai-team/" | — |
| 35 | Self-upgrade follows channel, `--insider`, `--dry-run`, downgrade refused unless `--force`; installs `@bradygaster/squad-cli@<tag>` | ✅ | `squad --help`; `D/features/self-upgrade.md` l.27–29; CL preview.2 | — |
| 36 | `squad doctor` exits non-zero; checks bridge, launcher, machine paths, upstream state, history archives | ✅ | CL l.133, l.171 (#2376), l.194, l.214; preview.1 "Added" (upstream) | — |
| 37 | `squad nap`: archives and deletes, no summary; >15 KB keeps Core Context + last 5 `##` (3 with `--deep`); logs >7 days deleted; inbox merged; `decisions.md` >20 KB archived; `/nap` in shell, not `/compact` | ✅ | `cli/core/nap.ts` l.49–54 (`HISTORY_THRESHOLD = 15*1024`, `DECISION_THRESHOLD = 20*1024`, `LOG_MAX_AGE_DAYS = 7`, `DECISION_MAX_AGE_DAYS = 30`, `KEEP_ENTRIES_DEFAULT = 5`, `KEEP_ENTRIES_DEEP = 3`), l.173 Core Context; `cli/shell/commands.ts` l.68; `D/features/context-hygiene.md` l.24–37 | Add the two caveats from `D/features/context-hygiene.md` l.31: `###` entries under one `## Learnings` count as one section, and nap skips the decisions move if the archive is git-ignored and untracked. |
| 38 | `squad cost` scoped to the newest shell session | ✅ | `commands/cost.ts` diff adds `getCurrentSquadSessionId()` (newest ledger row's `squadSessionId`) | — |
| 39 | `squad cost` "New table output format. Falls back to orchestration-log estimates." | ❌ | The table and the fallback both exist in v1.1.0 code: `SRC/squad-v1.1.0/.../commands/cost.ts` l.202 `'💰 Squad Cost Summary'`, l.233 `Source: structured runtime usage ledger`, l.241 legacy-estimate fallback. The v1.1.0→v2.0.0 `cost.ts` diff changes only scoping and session counting. Only the **docs** sample changed (`D/features/cost-tracking.md` diff). | Write: "2.0 scopes `squad cost` to the newest Squad session." Do not say the output format or fallback is new. Vol 1 Ch 12 only needs its sample replaced if it copied the old docs sample. It does not: Ch 12 l.234 already describes the legacy label. Also note that `squad cost --help` still says "from orchestration logs". |
| 40 | `squad memory` shares the governed store with `memory.*`, is backend-aware, fails outside a squad, case-insensitive classes | ✅ | CL preview.3 "Changed" (#2315–#2333) | — |
| 41 | `squad rc` / `squad start` (Vol 1 Ch 11 marked "URLs only") | ✅ | Both print `⚠ DEPRECATED` in v2.0.0 (`cli-entry.ts` l.1055, l.1133), the same as v1.1.0 (l.960, l.1050). Ch 11 l.109/138/163 already documents this. | No new content needed. Retarget "deprecated in v1.1.0" to "deprecated (still in v2.0.0)". Marvin's assessment l.117 ("add a deprecation note") overstates this; the note already exists. |

## 4. Files and layout

| # | Claim | Rating | Evidence | Correction |
|---|---|---|---|---|
| 42 | `.squad/squad.mjs` launcher; `node .squad/squad.mjs state-mcp` in a `node -e` root finder; order `SQUAD_CLI` → project `node_modules` → PATH; `npx` only with `SQUAD_ALLOW_NPX=1` | ✅ | CL l.128–133, l.150; `D/features/mcp.md` l.34 | — |
| 43 | `.mcp.json` is the Copilot CLI project MCP file; project `.copilot/mcp-config.json` is a sample Copilot CLI does not read; VS Code `.vscode/mcp.json` key `servers`; personal `~/.copilot/mcp-config.json` | ✅ | `D/features/mcp.md` l.29–32, l.130; `cli/core/init.ts` l.497–545 | Context for Vol 2 Ch 1: v1.1.0 init **also** wrote root `.mcp.json` (`ensureSquadStateMcpInRoot` × 3 in v1.1.0 `init.ts`). What changed is the guidance (CL preview.3 #2312) and the launcher command, not the file. |
| 44 | New `config.json` keys: `clients[]`, `claudePlugin`, `claudeHooks: "advisory"`, `claudePermissions: "off"`, `watch.*`; malformed config stops watch | ⚠️ | Keys verified: `adapters/claude-hooks.ts` l.85–89 (anything but `"advisory"` is off), l.206 (`claudePermissions` on unless `"off"`); CL preview.3. But the cited `D/reference/config.md` documents none of `claudeHooks`, `claudePermissions`, `agentPreset`, `claudeFlags` or `claims`. | Re-source to CL 2.0.0, `D/features/ralph.md` (watch keys), `D/scenarios/client-compatibility.md` l.234 and `adapters/claude-hooks.ts`. |
| 45 | `.squad/templates/human-members.md` ships again with the sign-off gate | ✅ | `templates/human-members.md`, `packages/squad-cli/templates/human-members.md`; CL l.142 | — |
| 46 | `.squad/casting/` stays on the source branch; orphan pre-commit hook "now blocks `memory/` and `identity/`, not `casting/` or `routing/`" | ⚠️ | `commands/install-hooks.ts` l.119 blocks `decisions.md`, `agents/*/history.md`, `memory/`, `identity/`. `D/features/state-backends.md` l.436–447 agrees. l.39 of the same page is stale (still says "casting, routing"). | List all four blocked paths, and cite l.436+, not l.39. |
| 47 | `.squad/backend/` added to `.gitignore` on upgrade; `.claude/worktrees/` and `NUL` only with `claude` client | ✅ | CL l.232 | — |
| 48 | Casting repair archive `handwritten-archive-<sha256>/` | ✅ | CL l.240 | — |
| 49 | Charter `## Examples`; `X-squad-host-claude` (`Tools`, `Isolation`) | ✅ | CL preview.2 "Added"; CL l.86 | — |
| 50 | Claude projection v3; `.claude/agents/`, `.claude/skills/`, `squad-coordinator-*`, `.claude/settings.json` (`agent`, `disabledMcpjsonServers`), `.claude/.squad-permissions.json` | ✅ | `adapters/adapters.ts` l.32 `CLAUDE_PROJECTION_VERSION = 3`; CL l.67–92; `adapters/claude-hooks.ts` l.262 | — |

## 5. Hosts, plugin, coordinator

| # | Claim | Rating | Evidence | Correction |
|---|---|---|---|---|
| 51 | Claude Code plugin: `claude plugin marketplace add github/squad`, `claude plugin install squad@squad --scope project`; carries `squad:squad`, `squad_state` (no `.mcp.json` approval), `/squad:<skill>`, the 5 slash commands, hooks, launcher; new at 2.0.0 (not in preview.3/4) | ✅ | `D/features/claude-code-plugin.md` l.7–8, l.21–25, l.53–54; `.claude-plugin/marketplace.json` (version 2.0.0); `plugins/squad/{agents,bin,commands,hooks,skills}`; CL l.58 "Included in stable v2.0.0 alongside the four published previews"; `ls-tree` shows `claude-code-plugin.md` absent in preview.4 | — |
| 52 | Non-plugin launch: `claude --agent squad --mcp-config .mcp.json` | ✅ | CL l.149 | — |
| 53 | ADR-003: non-Copilot coordinators self-contained; Copilot output unchanged | ✅ | `docs/specification/adr-003-host-neutral-canonical-coordinator.md` exists (new at 2.0.0); CL l.112 | — |
| 54 | Non-Copilot fixes: reviewer gate unasked, human sign-off, Scribe for user decisions, stop when `squad_state` unavailable on non-local backend; `squad cast` adds the built-in table | ✅ | CL l.137–141, l.145 | — |
| 55 | Vol 2 Ch 12: "Claude loads Init, Ralph, ceremonies, Issues and PRD modes on demand. Verify whether the Copilot prompt also does this." | ⚠️ | Answer: partly. Copilot's `squad.agent.md` l.94 loads Init Mode on demand ("Invoke the `skill` tool on `coordinator-init-mode`"), and it already did in v1.1.0. It also defers response-mode and source-of-truth tables (l.380, l.699). Ralph, ceremonies, Issues and PRD stay inline. | Present on-demand loading as shared, with Claude moving more modes out. Do not present it as Claude-only. |
| 56 | Per-agent model: Copilot CLI/app only; VS Code and other hosts one session model, "except Claude member subagents take the charter model" | ⚠️ | `D/scenarios/client-compatibility.md` l.221 and CL l.87 support the Claude exception. The cited README diff (`README.md` l.468) says the opposite ("so do the other hosts (Claude Code, …) for now"). | Cite `client-compatibility.md` l.221, CL l.87 and `D/reference/host-feature-matrix.md`, not the README. Flag the README as stale upstream. |
| 57 | Squad plugin context only via `AgentLifecycleManager.spawnAgent()`; not coordinator, shell, `watch`, `loop` | ✅ | `D/features/plugins.md` l.170–177 (table; `spawnParallel`/`SquadCoordinator` also No) | — |
| 58 | GitLab "Planned, not shipped"; `PlatformType = github \| azure-devops \| planner`; ADO scope note | ✅ | `D/features/gitlab-issues.md` l.3; `sdk/src/platform/types.ts` l.8; `D/features/enterprise-platforms.md` l.5; ADO MCP in `.mcp.json` l.109 | — |

## 6. State backend, MCP, SDK

| # | Claim | Rating | Evidence | Correction |
|---|---|---|---|---|
| 59 | Upstream: runtime from local snapshots, never fetched; **earlier entries win**, local first (1.x docs said later); `stale` at 30 days | ✅ | CL l.234; `D/features/upstream-inheritance.md` l.19–24, l.93, l.97; `sdk/src/upstream/resolver.ts` l.14, l.859; `types.ts` l.127 | — |
| 60 | Upstream statuses `missing`, `invalid`, `unavailable`, `stale` | ⚠️ | `upstream-inheritance.md` l.247: `'ok' \| 'stale' \| 'missing' \| 'unavailable' \| 'invalid' \| 'cycle' \| 'depth-exceeded'`; depth limit 3 (l.22) | Add `cycle`, `depth-exceeded` and the depth-3 limit. Marvin's assessment l.121 already has the depth limit. |
| 61 | Static/mutable separation; `squad_state_*` refuse static config | ✅ | CL l.233 | — |
| 62 | Governed memory: transactional migration, cross-process locking, `memory.promote` requires `targetClass` | ✅ | CL preview.3/preview.4 "Fixed" | — |
| 63 | 11 `squad_backend_*` tools, explicit opt-in; `durable-http` needs `baseUrl` | ✅ | 11 distinct names in `cli/core/backend-mcp.ts`; CL l.232–233 | — |
| 64 | Harnesses `ClaudeAgentSdkHarness` (optional peer, API credential only), `CopilotSdkHarness`, `SQUAD_BACKEND_HARNESSES` | ✅ | `sdk/src/backend/harnesses/claude-agent-sdk.ts` l.155, `copilot-sdk.ts` l.89; `squad-sdk/package.json` `peerDependenciesMeta.optional: true`; `backend-mcp.ts` l.31, l.145; CL l.107–114 | — |
| 65 | P10: "`executionAvailable` is no longer always false when a harness registers" | ⚠️ | CL preview.1 "Known limitations": `executionAvailable: false` **until a `HarnessAdapter` is registered**. It was never unconditionally false; preview.2 simply bundled no harness. | Write: "2.0.0 bundles harnesses, so `state-mcp --experimental-backend` can report `executionAvailable: true` when the Claude SDK is installed." |
| 66 | `@github/copilot-sdk` pinned below 1.0.29 | ✅ | `squad-sdk/package.json` `">=1.0.19 <1.0.29-0"` | — |
| 67 | SDK subpaths `/client` canonical, `/clients` deprecated, `/backend` subpath-only, `/casting`; `BACKEND_CONTRACT_STAGE = 'experimental'` | ✅ | `squad-sdk/package.json` exports; `src/index.ts` exports no `backend`; `backend/types.ts` l.14 | — |
| 68 | Adapter modules list (`claude-members.ts` … `capabilities.ts`) | ✅ | `ls packages/squad-sdk/src/client/adapters/` (also `apply.ts`, `portable.ts`, `safe-path.ts`, `types.ts`) | — |
| 69 | P13: standalone vendors Node 22.23.4; npm users need patched host Node | ✅ | CL preview.3 "Security" (l.201) | — |

## 7. Docs inventory and specific chapter items

| # | Claim | Rating | Evidence | Correction |
|---|---|---|---|---|
| 70 | New sources: ADR-002, ADR-003, `claude-code-plugin.md`, `multi-machine-watch.md` | ✅ | All exist in v2.0.0. ADR-002 and `multi-machine-watch.md` first appear in preview.3; ADR-003 and the plugin page at 2.0.0 (`git ls-tree`). | — |
| 71 | P16 / App J: "book dates are wrong"; CHANGELOG has preview.1 = 10-23, preview.2 = 10-25 | ⚠️ | CL l.203/223 confirm 10-25/10-23. The book's 10-24/10-26 are not random: they match npm publish times (`2.0.0-preview.1` 2026-10-24T05:21Z, `-preview.2` 2026-10-26T04:38Z) and the preview.2 tag date (10-26). The book's own v1.1.0 row uses the CHANGELOG date (10-19; npm 10-20), so App J mixes conventions. CHANGELOG vs npm for the new rows: preview.3 10-29 vs **11-01**, preview.4 11-09 vs 11-09, 2.0.0 11-18 vs **11-19**. | Keep the plan's fix (CHANGELOG dates), but describe it as "align to the CHANGELOG convention", not "wrong". Add one line to App J saying dates are CHANGELOG release dates and npm publication may be a day or more later. |
| 72 | Vol 2 Ch 4: "Remove `.github/agents/squad.md` if it is a typo for `squad.agent.md`" | ❌ | Not a typo. Ch 4 l.176–178 deliberately reports the coordinator-as-agent article's proposed `squad export agent` output, and it already warns that this differs from `squad.agent.md`. `squad export agent` is still not in v2.0.0 (`commands/export.ts`, `cli-entry.ts` have no `agent` subcommand). | Keep the passage. Retarget "not verified in v1.1.0" to "not shipped in v2.0.0". |
| 73 | Vol 2 Ch 22: "verify what a 1.1.0 CLI actually installs" for `squad upgrade --self` | ✅ (resolved) | v1.1.0 `cli/core/upgrade.ts` l.1432–1433: `tag = insider ? 'insider' : 'latest'`, `pkg = '@bradygaster/squad-cli@${tag}'`. That resolves to 2.0.0 today. `@bradygaster/squad` (named in `D/features/self-upgrade.md` l.65 at both v1.1.0 and v2.0.0) → **npm 404**. | A 1.1.0 CLI self-upgrades to 2.0.0. Never copy the docs' `@bradygaster/squad@latest` line, which is an upstream docs bug. |
| 74 | Vol 1 Ch 16 / Ch 15: 15 KB, nothing shrinks automatically, `history-archive.md` not loaded at spawn | ✅ | `D/concepts/memory-and-knowledge.md` l.42–48, l.171 | — |
| 75 | Section 4 "Do not touch" list (npm names, brew tap, WinGet IDs, legacy `bradygaster/squad/workflows`) | ✅ | Items #4, #9, #12; `D/guide/gh-aw.md` l.125 still quotes the legacy fork identity | — |
| 76 | Section 4: "Known v1.1.0-only paths" (`consult-mode.md`, `personal-squad.md`, `multi-squad.ts`, `consult.ts`, `extract.ts`, `personal.ts`, …) | ✅ | `ls` and `git diff --name-status` above | The script should still path-test every pin. `agents/personal.ts` and `sharing/consult.ts` were not individually checked here. |

## ⚠️ / ❌ one-liners (for the coordinator)

- ❌ #39 `squad cost` table output and orchestration-log fallback are not new in 2.0 (they are in v1.1.0 `cost.ts` l.202–241). Only session scoping changed.
- ❌ #72 Vol 2 Ch 4 `.github/agents/squad.md` is a deliberate quote of the article's proposed `squad export agent` output, not a typo. Keep it and retarget it to "not shipped in v2.0.0".
- ⚠️ #2 The v2.0.0 date is 11-18 in the CHANGELOG but 11-19 for the tag and npm. Pick one convention.
- ⚠️ #6 Upstream canonical docs host is `github.github.com`. `.io` works, but record the choice in STYLE-GUIDE.
- ⚠️ #20 `docs/proposals/` never existed in v1.1.0. It is a preview.2→2.0.0 delta, not a 1.x removal.
- ⚠️ #28 `squad hook`/`lockout` have no detailed `--help`, and `hook` is missing from top-level help. Source App A from code and the CHANGELOG.
- ⚠️ #44 New config keys are real, but `D/reference/config.md` doesn't document them. Re-source.
- ⚠️ #46 The pre-commit hook blocks `decisions.md`, `agents/*/history.md`, `memory/` and `identity/` (all four). The state-backends page l.39 is stale.
- ⚠️ #55 The Copilot coordinator also loads Init Mode on demand (since 1.1.0). Do not present it as Claude-only.
- ⚠️ #56 README says Claude uses one session model, which contradicts CL and client-compatibility l.221. Don't cite the README.
- ⚠️ #60 Upstream statuses also include `cycle` and `depth-exceeded`; depth limit 3.
- ⚠️ #65 `executionAvailable` was conditional ("until a HarnessAdapter is registered"), never always false.
- ⚠️ #71 App J preview dates match npm publish dates; reframe as aligning to the CHANGELOG convention and add a date-convention note.
- Notes on items rated ✅: #37 nap needs two small caveats (`###` entries under one `##` count as one section; the decisions move is skipped when the archive is git-ignored). #41: `rc`/`start` deprecation is unchanged since v1.1.0, and Ch 11 already covers it. Marvin's "add a deprecation note" is unnecessary.
