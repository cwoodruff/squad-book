# Update Plan: Mastering Squad for Squad 2.0.0

Owner: Arthur (Lead Editor). Branch: `squad-2.0`. The 1.1 edition is tagged `book-squad-v1.1.0`.

**Status: FINAL (2026-11-20).** This version folds in every ❌ and ⚠️ correction from `research/UPDATE-PLAN-2.0-FACTCHECK.md` (cited below as "FC #n") and Chris's four author decisions. Ford and Trillian execute §2 and §3 directly; no open questions remain.

**Direction from Chris:** keep the 2.0 book as close as possible to the current book. Volume 2, Part IV has to change because 2.0 is no longer a future release.

**Author decisions (Chris, 2026-11-20; recorded in `.squad/decisions.md`)**

| # | Decision | Effect on this plan |
|---|---|---|
| D1 | **New edition.** New EPUB identifiers and edition marking. The 1.1 book stays at tag `book-squad-v1.1.0`. | Slartibartfast: new `identifier` UUIDs and edition fields in `book/metadata-vol*.yaml`. Writers: title pages carry "Second Edition. Written against Squad v2.0.0." Prefaces get a short "What's new in the second edition" paragraph. |
| D2 | **Vol 2 Ch 22 is renamed "Migrating from Squad 1.x to Squad 2.0".** The file name stays `ch22-upgrading-to-2.md`. | Trillian: Ch 22 H1, the `part-04/00-part.md` list, the Vol 2 preface and any "Chapter 22: Upgrading…" cross-ref. Arthur: `CHAPTERS.md`. Appendix E regenerates from the H1. |
| D3 | **Volume 1 stays Copilot-first.** Claude Code gets short pointers only (at most a paragraph each, no parallel Hands-On path). Full Claude Code coverage lives in Vol 2 Part IV. | The Vol 1 pointer sites are fixed in §2: Ch 1, 2, 6, 9, 17 and 21. No other Vol 1 chapter adds Claude Code material. |
| D4 | **Link hosts.** Docs: `https://github.github.com/squad/` (the upstream canonical host; FC #6). Repo: `https://github.com/github/squad`. npm, Homebrew and WinGet names keep `bradygaster` (`@bradygaster/squad-cli`, `@bradygaster/squad-sdk`, `brew tap bradygaster/squad`, `bradygaster.Squad*`). | Supersedes the earlier `github.github.io` choice everywhere in this plan. Slartibartfast's rewrite uses `.com`. |

**Date convention (decided by Arthur; applies to Appendix J and every date in the book).** The book uses **CHANGELOG release dates**: preview.1 2026-10-23, preview.2 2026-10-25, preview.3 2026-10-29, preview.4 2026-11-09, v2.0.0 2026-11-18, v1.1.0 2026-10-19. npm publication can be a day or more later (for example preview.3 on 11-01 and v2.0.0 on 11-19). Appendix J says this in one sentence. Never quote npm or tag dates elsewhere. (FC #2, #71)

**Editorial rules for this update**

1. Keep every volume, part, chapter number, file name, H2 template and Tasktrack tag. Both volumes keep their chapter counts: Volume 1 has 21 chapters and Volume 2 has 25. The only title changes are the Vol 2 Part IV title and the Vol 2 Ch 22 title (D2).
2. The whole book now targets **Squad v2.0.0** (stable, npm `latest`, dated 2026-11-18 in the CHANGELOG, tag commit `26654f0c4dadb2625d764c1c69ec61da6c518094`). Nothing in the book targets v1.1.0 or preview.2 any more. Those versions appear only as history (Vol 2 Ch 22, Appendix J).
3. The Copilot default did not change in 2.0. Plain `squad init` and `squad upgrade` are still Copilot-only (CHANGELOG 2.0.0-preview.1, "Breaking"). Most v1.1.0 teaching therefore stays correct. Change only what 2.0.0 changed, removed or corrected.
4. Every topic keeps one primary home. 2.0 features that are not about other hosts go into the existing Volume 1 or Volume 2 chapter that already owns the topic. Multi-host material stays in Volume 2, Part IV.
5. Writers do the fact checks themselves. Verify every command and flag with the installed CLI (`squad --version` reports `2.0.0`) in throwaway directories only, and against the v2.0.0 source.

**Source paths.** Below, `SRC` means `/private/tmp/claude-501/-Users-cwoodruff-Git-squad-book/6951efa4-a371-4f62-b4ea-94b9f725f30a/scratchpad/src`, so the v2.0.0 tree is `SRC/squad-v2.0.0`. `SRC/squad` is the full clone, so `git -C SRC/squad diff v1.1.0 v2.0.0 -- <path>` works. Doc paths are relative to the v2.0.0 tree. `D/` means `docs/src/content/docs/`.

---

## 1. Delta inventory

### 1.1 v1.1.0 → v2.0.0 (changes readers will notice)

**Repository, packages, install**

| Change | Detail | Source |
|---|---|---|
| Repo moved | `https://github.com/github/squad` (was `bradygaster/squad`). Repo, package metadata, runtime links and templates all point to `github/squad`. | CHANGELOG 2.0.0 "GitHub organization move"; preview.4 "Changed" |
| Docs site moved | `https://github.github.com/squad/docs/<slug>/`. The upstream `site` setting is `https://github.github.com` with base `/squad/`, and the CHANGELOG and README use `.com`. `.io` also returns 200, but **the book uses `.com` (D4)**. The old `bradygaster.github.io/squad/` host returns 404 everywhere, so the rewrite is mandatory. The docs root is `https://github.github.com/squad/` (`/squad/docs/` alone is 404). | `docs/astro.config.mjs` l.11–12; CHANGELOG l.33; FC #6, #7 |
| npm names unchanged | `@bradygaster/squad-cli` and `@bradygaster/squad-sdk`, now at `2.0.0`. Node `>=22.5.0` is unchanged. | CHANGELOG 2.0.0; `packages/*/package.json` |
| Other installer IDs unchanged | `brew tap bradygaster/squad` and `brew install --cask squad`, plus `squad-preview` and `squad-insider`. WinGet IDs are `bradygaster.Squad`, `.Preview` and `.Insider`. Install script: `raw.githubusercontent.com/github/squad/main/scripts/install.sh`. The standalone `REPO` default is `github/squad`, and the action input `repository: github/squad` applies because older pins default to the fork. | `D/get-started/installation.md`, `D/features/standalone-install.md` |
| Channels | `latest` = 2.0.0 stable. `preview` = release candidates. `insider` = dev snapshots. During the previews `preview` was an alias of `insider`; it is now its own RC channel. | `D/get-started/installation.md` l.35; `D/insider-program.md` l.22–32 |
| Self-upgrade | `squad upgrade --self` follows the installed channel (prerelease → `@insider`, stable → `@latest`). `--insider` forces the insider channel. `--dry-run` prints the command and installs nothing. Downgrades are refused unless `--force` is given. It installs `@bradygaster/squad-cli@<tag>`. | `D/features/self-upgrade.md`; CHANGELOG preview.2 |
| gh-aw identity | Use `gh aw add "github/squad/workflows@${SQUAD_SHA}"` with a 40-character SHA and a manifest preflight (`workflows/squad-workflows.manifest.json`). Do not install as legacy `bradygaster/squad/workflows`. | README diff; `D/guide/gh-aw.md` (+215/−37) |

**Removed features (breaking)**

| Removed | Replacement | Source |
|---|---|---|
| Personal squads: `squad personal`, `squad init --global`, `squad upgrade --global` | None. A project `.squad/` only, or `--team-root` / `SQUAD_TEAM_ROOT`. `--global` now fails with a 2.0 message. | CHANGELOG preview.1 "Breaking"; `packages/squad-cli/src/cli-entry.ts` l.141–142 |
| Consult mode: `squad consult`, `squad extract` | None | same; `commands/consult.ts` and `extract.ts` deleted |
| User-profile resolution | `.squad/` resolves only from the current directory and its parents. Outside a project, `status`, `doctor`, `cast` and `cost` fail with "No squad in this directory". | `D/reference/config.md`; `D/get-started/installation.md` |
| SDK personal helpers; `packages/squad-sdk/src/multi-squad.ts` (global `squads.json`) | `resolveGlobalSquadPath()` survives only as the base for `squad externalize` | CHANGELOG preview.1; commit f1549687; `D/reference/sdk.md` |
| `./shell/sdk-bridge` CLI subpath export | None | CHANGELOG preview.1 |
| Docs pages `features/consult-mode`, `guide/personal-squad` | Removed from the site. Cite them as `github.com/github/squad/blob/v1.1.0/...` (history only). | `git diff --name-status v1.1.0 v2.0.0 -- docs` |

`docs/proposals/` is **not** a v1.1.0→v2.0.0 removal: v1.1.0 never had it. It appears in §1.2 (P14) only. Vol 1 prose and the Ch 18 1.x checklist must not list it. (FC #20)

**New CLI commands and flags**

| Command / flag | Notes | Source |
|---|---|---|
| `squad init --client <list>` / `squad upgrade --client <list>` | Slugs: `copilot claude kiro opencode cursor codex antigravity` or `all`. Hosts persist in `.squad/config.json` `clients[]`. | `cli/core/command-help.ts`; `D/reference/cli.md` |
| `--claude-plugin` / `--no-claude-plugin` (init, upgrade) | Plugin mode. Records `"claudePlugin": true`. | CHANGELOG 2.0.0 "Plugin mode" |
| `squad client list [--json]`, `client add <list> [--dry-run]`, `client sync [--dry-run]` | `clients` is an alias. `sync` is new since preview.2. | `command-help.ts` `client` |
| `squad roster add\|remove <rai\|fact-checker\|all> [--dry-run]` | Rai and Fact Checker are opt-in. `upgrade` never edits `team.md`. Aliases: `disable`, `uninstall`. | CHANGELOG preview.2 |
| `squad dashboard [start\|stop\|status]` with `--port --session --stream --detach --open --json` | Reads Claude Code transcripts and listens on 127.0.0.1 from port 4280. State lives in `~/.squad/dashboards/` (or `SQUAD_HOME`). | CHANGELOG 2.0.0 |
| `squad lockout reject\|assign\|submit\|approve\|override\|status` | Writes `.squad/governance/lockouts.json` | CHANGELOG 2.0.0 "Advisory governance hooks" |
| `squad hook claude <Event>` | Runs the Claude advisory hooks. Not listed in top-level `squad --help`, and `squad hook --help` / `squad lockout --help` print "No detailed help is available": source their arguments from `cli-entry.ts` l.569, `commands/lockout.ts` and the CHANGELOG, not from `--help`. (FC #28) | same |
| `squad state-mcp [--experimental-backend]` | Or `SQUAD_EXPERIMENTAL_BACKEND=1` | `command-help.ts` |
| `squad watch --claims <none\|git-ref>`, `--max-rounds N`, `--max-duration 8h`, `--agent-preset <copilot\|claude>`, `--claude-flags "..."` | Claims are off by default (`none`). Config keys: `watch.claims`, `watch.agentPreset`, `watch.claudeFlags`. | `D/features/ralph.md`; `D/scenarios/multi-machine-watch.md` |
| `squad externalize --key <name>` | Ownership is recorded in `.owner.json` | `D/features/external-state.md` |
| `squad health --json` metadata | `cliVersion`, `sdkVersion`, `stateBackend`, `resolvedTeamRoot`, `resolvedSquadDir` (`resolvedTeamDir` is kept). Schema `squad-health/v1`, which already existed in v1.1.0: do not call the schema new. | `D/reference/cli.md`; CHANGELOG 2.0.0 "Changed" |
| `squad upgrade` behavior | Content-aware and idempotent. Ignores line endings. Writes a verified `<file>.local-backup` for customized files. `--dry-run` writes nothing. `--force` re-processes. Never touches `team.md`, `routing.md`, decisions, histories, the casting registry, `config.json` or `.ai-team/`. | `command-help.ts` upgrade text |
| `squad doctor` | Exits non-zero on failures. Checks the bridge and launcher, flags machine-specific launch commands, reports upstream state and checks history archives. | CHANGELOG preview.2–2.0.0 |
| `squad nap` | Archives and deletes; it does **not** summarize. History over 15 KB keeps Core Context plus the last 5 `##` sections (3 with `--deep`). Logs older than 7 days are deleted. Inbox is merged. `decisions.md` over 20 KB is archived. Use `/nap` in the interactive shell; there is no `/compact` equivalent. Two caveats: `###` entries under one `## Learnings` heading count as one section, and nap skips the decisions move when the archive is git-ignored and untracked. | `cli/core/nap.ts` l.49–54; `D/features/context-hygiene.md` l.24–37; `D/concepts/memory-and-knowledge.md` |
| `squad cost` | **Only change: 2.0 scopes `squad cost` to the newest Squad session** (`getCurrentSquadSessionId()`). The table output and the orchestration-log fallback already existed in v1.1.0; do not call them new. `squad cost --help` still says "from orchestration logs". (FC #39) | `commands/cost.ts` diff; `D/features/cost-tracking.md` |
| `squad memory` | Shares the governed store with the `memory.*` MCP tools and is backend-aware. Fails outside a squad. Class names are case-insensitive. | `D/features/memory.md`; CHANGELOG preview.3 |

**Files and layout under `.squad/` and around it**

| Item | Source |
|---|---|
| `.squad/squad.mjs`: a committed launcher. MCP configs and hooks now run `node .squad/squad.mjs state-mcp`, wrapped in a `node -e` root finder, instead of a machine-specific path. Lookup order: `SQUAD_CLI`, then project `node_modules`, then `squad` on PATH. `npx` only with `SQUAD_ALLOW_NPX=1`. | CHANGELOG 2.0.0 "Fixed" |
| `.mcp.json` at the repo root is the Copilot CLI project MCP file. Copilot CLI does **not** read the project `.copilot/mcp-config.json` that `squad init` still writes as a sample. VS Code uses `.vscode/mcp.json` (key `servers`). Personal config: `~/.copilot/mcp-config.json`. v1.1.0 `init` also wrote the root `.mcp.json`; what changed is the guidance and the launcher command, not the file. (FC #43) | `D/features/mcp.md`; `cli/core/init.ts` l.497–545 |
| `.squad/config.json` new keys: `clients[]`, `claudePlugin`, `claudeHooks: "advisory"` (any other value is off), `claudePermissions: "off"` (on unless `"off"`), `watch.agentPreset`, `watch.claudeFlags` (limited to permission-mode, model, fallback-model, effort, max-turns), `watch.claims` (functional: `none`, `git-ref`, or an object `{provider, ttlMs, skewMarginMs, remote, refPrefix}`; `--claims` overrides its provider; it is validated strictly, and an invalid value stops watch; corrected after the shared-appendices review, F1). A malformed `config.json` now stops `squad watch`. `D/reference/config.md` documents **none** of the Claude or watch keys, so do not cite it for them. (FC #44) | CHANGELOG 2.0.0, preview.3; `D/features/ralph.md` (watch keys); `D/scenarios/client-compatibility.md` l.234; `adapters/claude-hooks.ts` l.85–89, l.206; `commands/watch/config.ts` l.175–181 |
| `.squad/governance/lockouts.json` | CHANGELOG 2.0.0 |
| `.squad/templates/human-members.md` ships again, with the human sign-off gate | CHANGELOG 2.0.0 "Fixed" |
| `.squad/casting/` stays on the source branch for every backend. The orphan pre-commit hook blocks **four** paths: `decisions.md`, `agents/*/history.md`, `memory/` and `identity/`. It does not block `casting/` or `routing/`. `D/features/state-backends.md` l.39 is stale (still says "casting, routing"); cite l.436–447. (FC #46) | CHANGELOG preview.4; `commands/install-hooks.ts` l.119; `D/features/state-backends.md` l.436–447 |
| `.squad/backend/` is added to `.gitignore` on upgrade. `.claude/worktrees/` and `NUL` are added only when `claude` is a configured client. | CHANGELOG preview.1 |
| Casting repair: `.squad/casting/handwritten-archive-<sha256>/` | CHANGELOG preview.1, preview.3 |
| Optional charter `## Examples` section. `## X-` extensions such as `X-squad-host-claude` (`Tools`, `Isolation`). | `D/concepts/your-team.md`; `docs/specification/charter-v0.1.md` (+42) |
| Claude projection (v3): `.claude/agents/<member>.md` (member subagents), `.claude/skills/` (native skills plus `squad-coordinator-*` on-demand skills), `CLAUDE.md` block, `.claude/settings.json` (`agent`, `disabledMcpjsonServers`, scoped allow rules), `.claude/.squad-permissions.json` | CHANGELOG 2.0.0 |
| Other hosts' files (`AGENTS.md`, `GEMINI.md`, `.kiro/`, `opencode.json`, `.cursor/`, `.codex/`): see Part IV | `D/scenarios/using-squad-across-clients.md` |

**Hosts, plugin, coordinator, agents**

| Item | Source |
|---|---|
| Seven hosts via projections. Capabilities: `effective = client ∩ backend ∩ policy`. | CHANGELOG preview.1; `docs/specification/client-harness-adapters-v0.2.md` |
| **Claude Code is a first-class host (new since preview.2).** Plugin: `claude plugin marketplace add github/squad`, then `claude plugin install squad@squad --scope project`. The plugin carries the `squad:squad` coordinator, the `squad_state` MCP server (no `.mcp.json` approval needed), `/squad:<skill>` skills, `/squad:ralph`, `/squad:cast`, `/squad:ceremony`, `/squad:status`, `/squad:dashboard`, the advisory hooks and a launcher. Without the plugin, launch with `claude --agent squad --mcp-config .mcp.json`. | CHANGELOG 2.0.0; `D/features/claude-code-plugin.md`; `plugins/squad/` |
| ADR-003: the non-Copilot coordinators are self-contained and no longer defer to `.github/agents/squad.agent.md`. Copilot output is unchanged. | `docs/specification/adr-003-host-neutral-canonical-coordinator.md`; CHANGELOG 2.0.0 "Changed" |
| Non-Copilot coordinators: reviewer gate runs unasked, wait for human sign-off, spawn Scribe for decisions the user states, stop when `squad_state` is unavailable on a non-local backend | CHANGELOG 2.0.0 "Fixed" |
| `squad cast` adds the built-in support-agent table when the roster lacks it. Coordinators describe themselves separately from the roster. | CHANGELOG 2.0.0 (#2522) |
| Per-agent model selection: Copilot CLI and app only. VS Code and the other hosts use one session model, except that Claude member subagents take the charter model. **Do not cite the upstream README** (l.468 is stale and says the opposite). (FC #56) | `D/scenarios/client-compatibility.md` l.221; CHANGELOG l.87; `D/reference/host-feature-matrix.md` |
| Squad plugins (`.squad/plugins/`): context is injected **only** through `AgentLifecycleManager.spawnAgent()`. It is not injected through the coordinator, shell, `watch` or `loop`. This is a correctness fix for Vol 2 Ch 15. | `D/features/plugins.md` |
| GitLab: "Planned, not shipped". There is no GitLab adapter (`PlatformType` = `github \| azure-devops \| planner`). The ADO scope note is new. | `D/features/gitlab-issues.md`, `D/features/enterprise-platforms.md` |

**State backend and MCP**

| Item | Source |
|---|---|
| Static and mutable separation. `squad_state_*` tools refuse static config (`team.md`, `routing.md`, `config.json`, `charter.md`). Hand-editing `.squad/casting/` is forbidden. | CHANGELOG preview.1 |
| `squad_state_upstreams`: runtime resolution from local snapshots, never fetched. **Earlier `upstream.json` entries win** (the 1.x docs said later wins). Statuses: `ok`, `stale` (30 days), `missing`, `unavailable`, `invalid`, `cycle`, `depth-exceeded`. Depth limit 3. (FC #60) | CHANGELOG preview.1; `D/features/upstream-inheritance.md` l.22, l.247 |
| Governed memory: one store for the CLI and MCP. Migration from `local` or `worktree` to `orphan` or `two-layer` is transactional. Cross-process index locking. `memory.promote` requires `targetClass`. | CHANGELOG preview.3, preview.4 |
| Backend MCP tools (`squad_backend_*`, 11 tools) need explicit opt-in. `SQUAD_BACKEND_URL` alone does nothing. `durable-http` needs `baseUrl` (https, or http only for localhost). | CHANGELOG preview.1; `D/reference/config.md` |
| Experimental harnesses (new since preview.2): `ClaudeAgentSdkHarness` (optional peer `@anthropic-ai/claude-agent-sdk`, API credential only) and `CopilotSdkHarness`. `SQUAD_BACKEND_HARNESSES`. `state-mcp --experimental-backend` registers Claude only when its SDK is installed. Remote server and profile promotion are still experimental. | CHANGELOG 2.0.0 |
| `squad_state` works through symlinked roots. `squad_decide` reports orphan-branch keys correctly. A linked project gets no local placeholder team. | CHANGELOG 2.0.0 "Fixed" |
| Leftover `state-mcp` processes: run `squad upgrade --force`, restart, and kill only parent-gone PIDs | `D/scenarios/troubleshooting.md` (+47) |
| `@github/copilot-sdk` pinned below 1.0.29 | CHANGELOG preview.4 |

**SDK exports**

| Item | Source |
|---|---|
| `@bradygaster/squad-sdk/client` is canonical (host projection APIs `HostProjection`, `createClientAdapter`, `installClients`, `uninstallClients`, `CAPABILITY_TOKENS_BY_HOST`, …). `/clients` is a deprecated alias. | CHANGELOG preview.1; `D/reference/sdk.md` |
| `@bradygaster/squad-sdk/backend` is exported only from the subpath, never the root. `BACKEND_CONTRACT_STAGE = 'experimental'`. | same |
| `@bradygaster/squad-sdk/casting` (transactional repair) | CHANGELOG preview.1 |
| Adapter modules: `packages/squad-sdk/src/client/adapters/` (`claude-members.ts`, `claude-skills.ts`, `claude-hooks.ts`, `claude-plugin.ts`, `lockout.ts`, `repo-launcher.ts`, `coordinator.ts`, `capabilities.ts`, …) | source tree |

**Docs added and removed (affects the coverage maps)**

- New in 2.0.0, not yet inventoried: `docs/specification/adr-002-work-claims-and-external-queues.md`, `docs/specification/adr-003-host-neutral-canonical-coordinator.md`, `D/features/claude-code-plugin.md`, `D/scenarios/multi-machine-watch.md`.
- Inventoried but missing in 2.0.0: `D/features/consult-mode.md` (vol1:5), `D/guide/personal-squad.md` (vol1:2), and 8 `docs/proposals/*` (vol2:18, vol2:22).
- `source-modules.csv`: `packages/squad-sdk/src/multi-squad.ts` (vol2 Ch 3) is gone.

### 1.2 preview.2 → 2.0.0 (affects Volume 2, Part IV directly)

Part IV was written against preview.2. Since then, preview.3 (2026-10-29), preview.4 (2026-11-09) and GA (2026-11-18) shipped. Source: CHANGELOG l.7–222.

| # | Change since preview.2 | Hits |
|---|---|---|
| P1 | Stable release. `latest` = 2.0.0, so every "preview / insider only / may change before stable" framing is obsolete. Previews keep their place as history. Upgrade-matrix attestations remain tied to the preview versions tested. | Ch 18–22, App A/B/C/D/F/G/H/I/J |
| P2 | Claude Code first-class: plugin, plugin mode, projection v3, member subagents, native skills, on-demand coordinator skills, advisory hooks, `squad lockout`, `squad hook`, `squad dashboard`, `watch --agent-preset claude`, scoped permission allowlist, `claudePermissions`, `claudeHooks`, the `Agent` tool (formerly `Task`), and the launch hint `claude --agent squad --mcp-config .mcp.json` | Ch 19, 20, 21; App A, B, H |
| P3 | ADR-003: host-neutral, self-contained coordinators for the six non-Copilot hosts | Ch 20, 18; Vol 2 Ch 12 |
| P4 | Coordinator behavior fixes: reviewer gate, human sign-off gate, Scribe for user decisions, stop when `squad_state` is unavailable, consistent roster across hosts, more coordinator modes moved into on-demand skills for Claude (Copilot already loads Init Mode on demand; FC #55) | Ch 19, 20 |
| P5 | `squad client sync` (Init Mode runs it after writing `routing.md`) | Ch 19, 22; App A |
| P6 | Portable `.squad/squad.mjs` launcher and repo-root finder. `doctor` flags machine paths. Run `squad upgrade` once to fix existing repos. | Ch 21, 22; Vol 2 Ch 1, 10 |
| P7 | Org move to `github/squad` and the new docs domain | everywhere |
| P8 | Governed memory: shared CLI/MCP store (preview.3), transactional backend migration and source-branch casting (preview.4), cross-process locking | Ch 21; Vol 1 Ch 15; Vol 2 Ch 2 |
| P9 | ADR-002 work claims: `watch --claims git-ref`, bounded runs, capability routing on `execute`, per-round de-duplication. Malformed `config.json` now stops watch. | Vol 1 Ch 9; Vol 2 Ch 17; Ch 22 |
| P10 | First real harnesses: Claude Agent SDK and Copilot SDK. `SQUAD_BACKEND_HARNESSES`. 2.0.0 bundles harnesses, so `state-mcp --experimental-backend` can report `executionAvailable: true` when the Claude SDK is installed. (It was always conditional on a registered `HarnessAdapter`, never unconditionally false; FC #65.) | Ch 21; App G |
| P11 | Health metadata (`resolvedTeamRoot`, `resolvedSquadDir`, versioned runtime and backend metadata) | Ch 21; Vol 2 Ch 9; App A |
| P12 | `squad cost` session scoping; `nap` and history-archive doctor checks; doctor exit status; `squad-ci` preservation on upgrade | Vol 1 Ch 12, 16; Ch 22 |
| P13 | Security: standalone archives vendor Node 22.23.4. npm users must run a patched host Node. | Ch 22; Vol 1 Ch 2; Vol 2 Ch 6 |
| P14 | `docs/proposals/` (8 files, present only in preview.2–4) removed at stable promotion (commit 27819b1f), and `client-harness-adapters-v0.2.md` (+255) and `client-backend-decoupling-v0.2.md` (+34) revised. §15.1 and §14.4 profile promotion is still pending. | Ch 18, 20, 21, 22; App I |
| P15 | Updated docs Part IV cites: `D/reference/host-feature-matrix.md` (114 lines changed), `D/scenarios/client-compatibility.md` (+74), `D/scenarios/upgrading.md`, `D/scenarios/release-process.md` (+89), `D/reference/cli.md`, `D/scenarios/troubleshooting.md`, `D/whatsnew.md` (+30), `D/scenarios/using-squad-across-clients.md` (+8), `D/features/upstream-inheritance.md` | Ch 18–22, App H |
| P16 | Appendix J mixes date conventions: its v1.1.0 row uses the CHANGELOG date, but its preview.1/preview.2 rows (10-24, 10-26) use npm publish dates. Align every row to the CHANGELOG convention (see "Date convention" at the top). | App J |

---

## 2. Chapter-by-chapter change list

**Status key**

- **None**: no change.
- **Light**: global pass only (URLs, version strings), plus at most one or two sentences.
- **Moderate**: one or more sections revised or added. Exercises and quiz may change.
- **Rewrite**: substantial reframing within the same file and template.

Every chapter also gets the global pass from §4 (URLs, version strings, Preview-callout cleanup). That pass is not repeated in the lists below. When an exercise or quiz changes, update `exercises/solutions/volN/chNN.md` in the same work package.

### Volume 1 (owner: Ford)

| File | Status | Specific changes |
|---|---|---|
| `vol1/00-front/00-title.md` | Light | Repo link → `github.com/github/squad`. Edition line "Second Edition" (D1). "Written against **Squad v2.0.0**." |
| `vol1/00-front/01-preface.md` | Moderate | Replace the version guidance in l.40 and l.110 with "install v2.0.0 (`latest`)". Recast "Squad 2.0 evaluator" (l.50) as "Coming from Squad 1.x: read Ch 2, Ch 14, then Volume 2, Chapter 22". Rename the Part IV row (l.33) to "Squad 2.0: One Team, Many Hosts". Pin "Under the Hood" (l.76) to v2.0.0. Redefine the Preview callout (l.106): "experimental in v2.0.0". Add a short "What's new in the second edition" paragraph that also says the first edition (Squad 1.1) remains available. One sentence: this volume teaches the GitHub Copilot path; Claude Code and the other hosts are covered in Volume 2, Part IV (D3). |
| `vol1/part-0{1..4}/00-part.md` | None or light | Check for version mentions only |
| `ch01-what-is-squad.md` | Light | Fold the Preview callout (l.14) into prose: Squad supports seven hosts, Copilot is the default, see Vol 2 Part IV. Remove the personal-squad mention. |
| `ch02-installation.md` | Moderate | (a) Replace "Which Squad Should I Use? (1.1 vs 2.0)" (l.32–46) with a short "Squad 2.0 and earlier releases" section: 2.0 is stable, coming from 1.x → Vol 2 Ch 22, table of removed features. Keep the H2 slot so section order doesn't move. (b) Channels (l.137): `latest`/`preview`/`insider` with the new meanings. (c) Install script URL, Homebrew/WinGet IDs (unchanged `bradygaster` names), standalone `REPO` default. (d) Delete "Personal squads" (l.225). Add a three-sentence "Other AI hosts" subsection under "Choose your interface" that points to Vol 2 Ch 19 and shows the two Claude Code plugin install lines (`claude plugin marketplace add github/squad`, `claude plugin install squad@squad --scope project`). This is the main Vol 1 Claude pointer (D3); do not add a Claude Hands-On path. (e) Troubleshooting: "Doctor says `.squad/` does not exist" now says Squad never falls back to a profile directory. Rewrite "Mixing 1.1 and 2.0" as "An old 1.x CLI on PATH". (f) Node note: npm users need a patched Node 22.x (P13). (g) Coverage: drop the `guide/personal-squad` citation or pin it to the v1.1.0 history link (Marvin decides the map; see WP-M). Update exercises and quiz. |
| `ch03-first-session.md` | Moderate | Re-observe the default `squad init` tree with the 2.0.0 CLI in a scratch repo and update the table (l.130–140). New entries: `.squad/squad.mjs`, the `.mcp.json` launch command, `.gitignore` entries including `.squad/backend/`, `templates/human-members.md`. Note that `.copilot/mcp-config.json` is a sample Copilot CLI does not read. Remove the `--global` row (l.236) and the Preview callout (l.71). Re-check the coordinator section table (l.152–154): the "Personal Squad" and "Consult Mode" sections are gone from `squad.agent.md`. Verify against v2.0.0 `.github/agents/squad.agent.md` and `templates/`. Update the first-run output if it changed. |
| `ch04-meet-the-team.md` | Moderate | Rai and Fact Checker are optional, added with `squad roster add` (`upgrade` never edits `team.md`). `squad cast` adds the built-in table. Optional charter `## Examples` section. Mention `## X-` extensions in one sentence (cross-ref Vol 2 Ch 17/20). Human members and `templates/human-members.md` sign-off gate. Sources: `D/concepts/your-team.md` (+9), CHANGELOG. |
| `ch05-routing.md` | Moderate | Delete "Consult is two related workflows" (l.119–137) and its Config Reference rows (l.178), Under the Hood paragraph (l.200), Pitfalls bullets (l.210–211), learning objective (l.11), Exercise 4 (l.224), Quiz 6 (l.234) and the Preview callout (l.14). Replace the deleted section with a short "One team, any host" note: routing still comes from `.squad/routing.md` whatever the host; non-Copilot coordinators enforce the reviewer gate (cross-ref Vol 2 Ch 20). Further Reading: keep the consult-mode link only as a v1.1.0 history link if Marvin's map keeps it; otherwise remove. Replace the exercise and quiz item. |
| `ch06-parallel-work.md` | Light | Optional one-sentence cross-ref: Claude Code uses `isolation: "worktree"` under `.claude/worktrees/` (Vol 2 Ch 19) |
| `ch07-github-workflow.md` | Light | Re-check the gh-aw Preview callout (l.192) against v2.0.0 `D/guide/gh-aw.md`. The package identity is now `github/squad/workflows`; keep the callout only if the walkthrough is still not equivalent to the baseline adapter. Issue-template URLs. |
| `ch08-gitlab-ado.md` | Moderate | GitLab: 2.0 docs now say "Planned, not shipped". Recast the Preview callout (l.57) as plain fact and make sure no GitLab command is presented as working. ADO: add the "What Azure DevOps support means in Squad 2.0" scope (detection, `triage` and `watch` loop). ADO MCP server now goes in `.mcp.json`, not `.copilot/mcp-config.json`. Sources: `D/features/gitlab-issues.md`, `D/features/enterprise-platforms.md`. |
| `ch09-ralph-loop.md` | Moderate | Add a section "Bounded and coordinated watch runs": `--max-rounds`, `--max-duration`, `--claims git-ref` (off by default, `watch.claims` as the functional config form, validated strictly, fenced leases, the claims line in round reports) and `--agent-preset claude` / `--claude-flags` (one paragraph, cross-ref Vol 2 Ch 19). Malformed `config.json` now stops watch. `execute` applies `needs:*` capability routing. One issue is never dispatched twice per round. Config Reference rows. **New source to cite: `D/scenarios/multi-machine-watch.md` (primary home).** Sources: `D/features/ralph.md` (+49). |
| `ch10-prd-streams-fleet.md` | Light | `--dispatch-mode fleet` stays Copilot-only (one sentence) |
| `ch11-coding-agent-remote.md` | Light | URLs only. `squad rc` / `squad start` deprecation is unchanged and already documented (l.109/138/163): retarget "deprecated in v1.1.0" to "deprecated (still present in v2.0.0)". No new note. (FC #41) |
| `ch12-models-cost.md` | Moderate | Model selection by host: per-agent models in the Copilot CLI and app; VS Code and other hosts use one session model; Claude member subagents use the charter model (one sentence, cross-ref Vol 2 Ch 20; cite `D/scenarios/client-compatibility.md`, not the upstream README). `squad cost`: the **only** behavior change is newest-session scoping (and `--agent` within the current session). The table output and the orchestration-log fallback are not new; l.234 already describes the legacy label, so keep it. (FC #39, #56) |
| `ch13-notifications.md` | Light | URLs only |
| `ch14-upgrade-cleanup.md` | Moderate | This chapter becomes the home for routine upgrades within 2.x; the 1.x→2.0 migration stays in Vol 2 Ch 22. Fold the Preview callout (l.14) into prose. Self-upgrade (l.85): channel following, `--dry-run`, downgrade refusal with `--force`, package `@bradygaster/squad-cli`. "What a project upgrade preserves and overwrites" (l.100–135): content-aware compare, `.local-backup`, the exact never-touched list from `squad upgrade --help`, `squad-ci` customizations preserved, `--client` refreshes all configured hosts, `squad client sync`. Migrations (l.171): casting repair and `teamRoot` normalization. One-paragraph pointer: "coming from 1.x, read Vol 2 Ch 22 first". Sources: `D/features/self-upgrade.md`, `D/scenarios/upgrading.md`, `D/get-started/migration.md`. |
| `ch15-memory.md` | Moderate | History size (l.85): 15 KB threshold, nothing shrinks automatically, `history-archive.md` is not loaded at spawn, and the persistence table from `D/concepts/memory-and-knowledge.md`. `squad memory` shares the governed store with `memory.*` tools, is backend-aware, fails outside a squad, and uses case-insensitive classes. Remove the personal-squad mentions (2 hits). Sources: `D/features/memory.md`, `D/concepts/memory-and-knowledge.md`. |
| `ch16-tiered-memory-context.md` | Moderate | `squad nap` archives and deletes but never summarizes. Document its four steps, `--deep` = last 3 sections, the two caveats (`###` entries under one `##` count as one section; the decisions move is skipped when the archive is git-ignored and untracked), and that "team, take a nap" is just a chat request. `/nap` in the shell; Copilot CLI `/compact` only shortens chat (l.151, l.221). Summarizing is a separate agent job; Scribe only merges decisions. Remove the preview mentions (4). Source: `D/features/context-hygiene.md` (+17/−11). |
| `ch17-skills.md` | Light | YAML block-sequence frontmatter parsing is fixed. One sentence: in Claude Code, template skills project into `.claude/skills/` (cross-ref Vol 2 Ch 20). |
| `ch18-governance.md` | Moderate | Reviewer protocol: `squad lockout` commands and `.squad/governance/lockouts.json`. Non-Copilot coordinators run the reviewer gate unasked, and a reviewer-authored fix needs a different reviewer. Human sign-off gate: a request is not the sign-off (`templates/human-members.md`). Advisory Claude hooks, one paragraph with cross-ref Vol 2 Ch 15/20. Verify which behaviors apply to the Copilot coordinator; the CHANGELOG says Copilot is unchanged, so don't overclaim. |
| `ch19-error-recovery.md` | Light | Version strings. The error-recovery and iterative-retrieval proposals are gone, but the chapter cites shipped skills and docs; verify the sources still resolve. |
| `ch20-scenarios-a.md` | Light | Solo or open source: one sentence on choosing a host (cross-ref Vol 2 Ch 19) |
| `ch21-scenarios-b.md` | Light | Human teams: one paragraph on mixed-host teams sharing one `.squad/` (decisions flow through Scribe and `decisions.md`; cross-ref Vol 2 Ch 19). Large or multi-machine teams: cross-ref the `watch --claims` section in Ch 9. |

### Shared appendices (owner: Ford; run after Trillian's Part IV, see §5)

| File | Status | Specific changes |
|---|---|---|
| `app-A-cli-reference.md` | Rewrite (same structure) | Merge the separate "Preview" 2.0 section (l.193 on) into the main tables. There is now one reference for v2.0.0. Add `client` (list/add/sync), `roster`, `dashboard`, `lockout`, `hook`, `state-mcp --experimental-backend`, `--client`, `--[no-]claude-plugin`, `--team-root`, the new `watch` flags, `externalize --key`, `health --json` metadata and `nap --deep` semantics. Remove `consult`, `extract`, `personal` and `--global` (14 hits); list them in a "Removed in 2.0" table. Source of truth: `squad --help`, `squad <cmd> --help` (2.0.0), `packages/squad-cli/src/cli/core/command-help.ts`, `D/reference/cli.md`. **Exception:** `hook` and `lockout` have no detailed help and `hook` is missing from top-level help; source their arguments from `cli-entry.ts`, `commands/lockout.ts` and the CHANGELOG (FC #28). |
| `app-B-configuration.md` | Moderate | Merge the Preview section (l.137 on) into the main tables. New `config.json` keys (sourced per §1.1, not from `D/reference/config.md`; FC #44) and env vars (§1.1: `SQUAD_EXPERIMENTAL_BACKEND`, `SQUAD_BACKEND_URL`, `SQUAD_BACKEND_TOKEN`, `SQUAD_BACKEND_HARNESSES`, `SQUAD_CLI`, `SQUAD_ALLOW_NPX`, `SQUAD_HOME`, `SQUAD_TEAM_ROOT`). New files (`.squad/squad.mjs`, `governance/lockouts.json`, the `.claude/*` projection files, `.claude/.squad-permissions.json`). Fix the MCP file rows (l.34, l.52): `.mcp.json` is authoritative and `.copilot/mcp-config.json` is a sample. Remove the personal-directory resolution step. Update history thresholds. |
| `app-C-glossary.md` | Moderate | Fold the Preview block (l.125) into the alphabetical list. Add: host / client slug, host projection, plugin mode, member subagent, work claim, governed memory, launcher (`.squad/squad.mjs`), lockout, harness. Mark personal squad, consult mode and global squad as "Removed in 2.0". |
| `app-D-sample-prompts.md` | Light | The Preview callout (l.107) becomes a normal section intro. Add 2–3 Claude Code prompts (cast with `squad cast`, dashboard) only if Trillian's Ch 19 introduces them. |
| `app-F-resources.md` | Moderate | 30 URLs → new hosts. Replace the "Preview" block (l.55) with "Squad 2.0 resources" and a "Historical (1.1.0)" block pinned to `github.com/github/squad/blob/v1.1.0/`. Add the Claude Code plugin page and the multi-machine watch page. |
| `vol1/appendices/app-E-quiz-answers.md` | Generated | Regenerate with `make epub`; never hand-edit |

### Volume 2 (owner: Trillian)

| File | Status | Specific changes |
|---|---|---|
| `vol2/00-front/00-title.md` | Light | Repo link; edition line "Second Edition" (D1); "Written against **Squad v2.0.0**" |
| `vol2/00-front/01-preface.md` | Moderate | Part table row 27 → "Squad 2.0: One Team, Many Hosts". Any chapter list → Ch 22 "Migrating from Squad 1.x to Squad 2.0" (D2). "What's new in the second edition" paragraph (D1). Persona l.36: "Multi-host teams: read Part IV and Appendix H". Version paragraph l.66: everything targets v2.0.0, and Ch 22 covers migration from 1.x. Redefine the Preview callout (l.62): "experimental in v2.0.0". |
| `part-01/00-part.md` | Light | Version string |
| `ch01-mcp.md` | Moderate | Fold the Preview callout (l.16) into prose. Rewrite the v1.1.0 init MCP paragraph (l.44) and the Config Reference rows (l.238–250): `.mcp.json` at the root is what Copilot CLI reads (v1.1.0 init already wrote it; the guidance and launcher command changed, not the file); the project `.copilot/mcp-config.json` is not read; VS Code uses `.vscode/mcp.json`; the `node .squad/squad.mjs state-mcp` launcher; per-host MCP files (one table row, cross-ref Ch 19). Update Exercise 1 (l.293). `squad_state` tool list: health metadata, `squad_state_upstreams`, `memory.*` governed store. Source: `D/features/mcp.md` (+41/−35). |
| `ch02-state-backends.md` | Moderate | Fold the Preview callout (l.14). Transactional migration of governed memory and the decision inbox to `orphan`/`two-layer`. Casting and routing stay on the source branch. Pre-commit hook blocks `decisions.md`, `agents/*/history.md`, `memory/` and `identity/` (all four; update the restore command; cite `state-backends.md` l.436+, not the stale l.39). Lock files live machine-locally under the `.git` common dir. External state: `--key`, `.owner.json`, refusal on conflict. Sources: `D/features/state-backends.md`, `D/reference/state-backend-selection.md`, `D/features/external-state.md`. |
| `ch03-cross-squad.md` | Moderate | Remove the personal multi-squad material: l.7 objective, the l.132 table row, l.138–140, l.269, l.276, Exercise 3 option, Quiz 8 (l.314), Further Reading l.323 (`multi-squad.ts`). Fold the Preview callout (l.14) into one sentence. The source-modules map row for `multi-squad.ts` must move or go (WP-M). Optional one-paragraph cross-ref to work claims (Vol 1 Ch 9) for multiple watchers on one squad. |
| `ch04-portability.md` | Moderate | **Correctness fix:** upstream precedence is local first, then **earlier** entries win. Rewrite the Warning (l.150) and Quiz 5 (l.263). Upstreams resolve at runtime from local snapshots (`squad upstream sync` materializes them; sessions never fetch). `squad doctor`/`status` show the resolution; statuses include `stale` (30 days), `cycle` and `depth-exceeded`; depth limit 3. Keep the depth in Ch 21; this chapter gets a summary and a cross-ref. **Keep** the `.github/agents/squad.md` passage (l.176–178): it deliberately quotes the coordinator-as-agent article's proposed `squad export agent` output and already warns that it differs from `squad.agent.md`. Retarget "not verified in v1.1.0" to "not shipped in v2.0.0" (`squad export agent` does not exist in v2.0.0). (FC #72) Source: `D/features/upstream-inheritance.md` (+87/−29). |
| `ch05-dual-mode-clients.md` | Light | One paragraph: this chapter covers Copilot surfaces and programmatic sessions, and Part IV covers the other six hosts. `D/scenarios/client-compatibility.md` now has a Claude Code section; cite it here only for the Copilot parts. |
| `part-02/00-part.md` | None | |
| `ch06-security.md` | Light | One short subsection or callout: Squad's scoped Claude Code allowlist (and `claudePermissions: "off"`); `SQUAD_ALLOW_NPX` gating; the dashboard binds 127.0.0.1 only with a strict CSP and Host check. Patched Node for npm installs (P13). Plugin-security URL updates. |
| `ch07-containers-cloud.md` | Light | Re-verify image name and registry in `D/reference/container-image.md`, `D/scenarios/aks-deployment.md` and `D/scenarios/azure-container-apps.md` (all changed 7–10 lines). Keep the existing KEDA mismatch note if it still applies at v2.0.0. |
| `ch08-cicd-release.md` | Moderate | gh-aw: `github/squad/workflows` package identity, 40-character `SQUAD_SHA` check, manifest preflight, no legacy fork install (`D/guide/gh-aw.md` +215). Release process (`D/scenarios/release-process.md` +141/−46): stable/preview/insider channels for npm, Homebrew and WinGet. The 7 "preview" mentions need recasting. |
| `ch09-observability.md` | Light | `squad health --json` metadata fields. One paragraph on `squad dashboard` as a local Claude Code session view (cross-ref Ch 19). |
| `ch10-troubleshooting-dr.md` | Moderate | Add Pitfalls entries: lingering `state-mcp` processes; machine-specific launch commands (fix: `squad upgrade`); "No squad in this directory"; `squad doctor` now exits non-zero; symlinked team roots. Sources: `D/scenarios/troubleshooting.md` (+47), `D/scenarios/production-troubleshooting.md`, `D/reference/vscode-troubleshooting.md`. |
| `part-03/00-part.md` | Light | URL |
| `ch11-architecture.md` | Light | Fold the Preview callout (l.15) into prose. Remove the personal/global mentions (2). Diagram stays. |
| `ch12-coordinator-internals.md` | Moderate | Fold the Preview callout (l.16) into prose. New short section "Host-neutral coordinators (ADR-003)": Copilot's `squad.agent.md` is unchanged; the other hosts get self-contained coordinators. **On-demand loading is shared, not Claude-only** (FC #55, resolved): Copilot's `squad.agent.md` already loads Init Mode on demand via the `coordinator-init-mode` skill (l.94, since v1.1.0) and defers the response-mode and source-of-truth tables (l.380, l.699), while Ralph, ceremonies, Issues and PRD stay inline. Claude moves those further modes out into `squad-coordinator-*` skills. Keep the depth in Vol 2 Ch 20. Remove the consult/personal sections of the prompt walkthrough (5 hits). |
| `ch13-identity-provenance.md` | Light | Re-check the Preview callout (l.201) against v2.0.0: are `docs/open-issue-runtime-identity-beacon.md` and `docs/canary-identity-matrix.md` still unshipped proposals? If so, keep the callout and reword it to "not shipped in v2.0.0". |
| `ch14-sdk.md` | Moderate | Fold the Preview callout (l.14). Exports table: `/client` (canonical, with host adapters), `/clients` (deprecated), `/backend` (subpath-only, experimental), `/casting`. Remove the personal-state helpers (3 hits). `resolveGlobalSquadPath()` is only the externalize base. Add a short "Execution harnesses" subsection (Claude Agent SDK and Copilot SDK, experimental) that cross-refs Ch 21. 40 URLs. Source: `D/reference/sdk.md`, `D/reference/api-reference.md`. |
| `ch15-plugins-hooks.md` | Moderate | **Correctness fix:** Squad plugin context is injected only through `AgentLifecycleManager.spawnAgent()`. Add the spawn-path table from `D/features/plugins.md`. Add a disambiguation box: Squad plugins (`.squad/plugins/`) versus the Squad plugin *for Claude Code* (Part IV Ch 19) versus Claude Code hooks (`squad hook claude`, advisory, opt-in). |
| `ch16-autonomous-agents.md` | Light | Re-check the Preview callout (l.114) for `@squad/resilience` against v2.0.0. Fix the "v1.1.0 source" wording. |
| `ch17-specification.md` | Moderate | Charter spec v0.1 additions: `## Examples` and `## X-` extensions (`X-squad-host-claude`). Spec README additions. `github-work-lifecycle-binding-v0.1.md` (+7). Add a short "Architecture decision records" section: **ADR-002 work claims is the new primary source cited here**; ADR-001 points to Ch 18 and ADR-003 to Ch 20. 48 v1.1.0 mentions: re-pin, and only keep the ones that are history. |
| `part-04/*` | See §3 | |
| `part-05/00-part.md` | Light | Version |
| `ch23-patterns-cookbook.md` | Light | Remove the personal-squad pattern mention (1). Optional "one team, many hosts" recipe (cross-ref Ch 19). |
| `ch24-capstone.md` | Light | The capstone runs on 2.0.0. Add one optional step: project Tasktrack to a second host before production, with a Copilot-only fallback. Re-check the CI YAML, which installs `@bradygaster/squad-cli` (`latest` now = 2.0). |
| `ch25-contributing.md` | Moderate | The repo is `github/squad`: update clone, fork, issue and PR links, and `D/guide/contributing.md` and `D/community.md`. Release channels and branch model (`dev` → insider/preview, stable promotion "sanitizes"; `D/insider-program.md`). Remove the 12 preview-era mentions. The retired-symbol gate `test/retired-symbols.test.ts` is a contributor-facing check worth one sentence. |
| `app-G-sdk-api.md` | Moderate | Fold the Preview section (l.254) into the main reference at v2.0.0. Add harness classes and `SQUAD_BACKEND_HARNESSES`. Remove the personal APIs (4 hits). |
| `app-H-feature-matrix.md` | Moderate | Regenerate the summary from v2.0.0 `D/reference/host-feature-matrix.md` (changed since preview.2; Claude has many more ✅). Replace the callout (l.51) with "Reflects v2.0.0". |
| `app-I-spec-cheatsheet.md` | Moderate | Add ADR-002 and ADR-003 rows. Update the client-harness-adapters and backend-decoupling v0.2 maturity labels (profile promotion pending). Replace the Preview callout (l.103). |
| `app-J-version-history.md` | Moderate | "This book's target" moves from v1.1.0 to **v2.0.0**. Retitle "Squad 2.0 (Preview) Version History" to "Squad 2.0 Version History". Align the dates to the CHANGELOG convention (preview.1 2026-10-23, preview.2 2026-10-25; the old 10-24/10-26 were npm publish dates, not errors). Add preview.3 (10-29), preview.4 (11-09) and 2.0.0 (11-18) rows. Add one sentence: "Dates are CHANGELOG release dates; npm publication can be a day or more later." (FC #71) Add a "v2.0.0 detail" paragraph like the v1.1.0 one. Drop the closing "not stable" sentence. CHANGELOG link → `github/squad/blob/v2.0.0/CHANGELOG.md`. Blog links: pin at `blob/v2.0.0` under `github/squad`, per the approved link rewrite (the eight posts are byte-identical between v1.1.0 and v2.0.0; ruling in the Part V/front/G–J review). |
| `vol2/appendices/app-E-quiz-answers.md` | Generated | Regenerate |

---

## 3. Volume 2, Part IV proposal

**Decision (recorded with `squad_decide`):** keep five chapters, keep numbers 18–22, keep all file names. Only the part title and two chapter frames change. No merges. Merging would renumber Part V (23–25), the Tasktrack `v2-chNN` tags, the solutions files and the coverage maps for little benefit.

### 3.1 New part title and intro

- **Part IV: Squad 2.0: One Team, Many Hosts** (was "Looking Ahead: Squad 2.0 (Preview)").
- Rewrite `part-04/00-part.md` in present tense, including the chapter list with the new Ch 22 title. Part IV covers what 2.0 changed, working in each of the seven hosts, how projection and negotiation work, the state boundary and experimental backend, and migrating an existing 1.x squad. Readers who use only Copilot can skim it. Readers coming from 1.x should start at Ch 22. Tasktrack is already on 2.0; this part projects it into more hosts.
- Remove the `> **Preview:**` opener from Ch 18–22. Use a `> **Preview:**` callout only for things that are still experimental in 2.0.0: the `squad_backend_*` tools, the harnesses, remote durable server integration, v0.2 profile promotion, and dashboard internals if they are labelled experimental.

### 3.2 Per-chapter plan (owner: Trillian)

| Ch | Title | Status | Changes |
|---|---|---|---|
| 18 | Squad 2.0: What Changed and Why *(unchanged)* | Rewrite (keep H2 skeleton) | Present tense throughout. Retitle "What Changed in 2.0.0" and extend it with the post-preview.2 changes P2–P13 (Claude Code first-class, host-neutral coordinators, org move, governed memory, work claims, portable launcher). "Breaking and Behavior Changes" stays and becomes a 1.x→2.0 checklist (do not list `docs/proposals/`, which a 1.x reader never had; FC #20). "The Security and Isolation Proposal: What Is Shipped?" becomes **"Security and Isolation in 2.0.0"**, based on shipped behavior (static/mutable boundary, opt-in backend tools, allow-listed upstream sources, scoped Claude permissions, local-only dashboard). Drop the deleted proposal as a source. "Preview Channels and Optional Built-Ins" becomes **"Release Channels and Optional Built-Ins"**. "Should I Adopt 2.0 Now?" becomes **"Who Needs Part IV?"** (a decision table: Copilot-only, mixed-host, 1.x migrator). Hands-On "Try 2.0 Without Replacing Your Stable CLI" becomes **"Inventory What 2.0 Generated for Tasktrack"** (`squad client list`, `squad health --json`, `squad doctor`). Under the Hood: drop the deleted-module walkthrough (`consult.ts`, `extract.ts`, `personal.ts`, `agents/personal.ts`, `multi-squad.ts`, `sharing/consult.ts`) or keep it as a short "what was removed (v1.1.0 paths)" list. Add `test/retired-symbols.test.ts`. |
| 19 | Using Squad Across Clients *(unchanged)* | Moderate | "Installing the 2.0 Preview and Selecting Hosts" becomes **"Selecting Hosts"**. Add **"Claude Code: Plugin or Full Projection"**: marketplace install, `--claude-plugin`, what plugin mode writes, `--no-claude-plugin`, the trust prompt and scoped allowlist, `claudePermissions`, `squad dashboard` and `/squad:dashboard`, slash commands. Update the Claude launch line under "Launching Each Host". "Add or Remove a Host Later" gets `squad client sync`. Cross-host decision flow: Scribe spawned for user decisions, consistent roster. Hands-On: drop the "scratch copy" framing because Tasktrack is on 2.0. Keep the Copilot-only fallback. Three hosts stays the target. **New source: `D/features/claude-code-plugin.md`.** Re-read the changed `D/scenarios/client-compatibility.md` and `using-squad-across-clients.md`. |
| 20 | Host Projections, Client Adapters, and Capability Negotiation *(unchanged)* | Moderate | Add **"Host-Neutral Coordinators (ADR-003)"** under "Rendering One Coordinator for Seven Hosts". Add **"The Claude Projection, Version 3"**: member subagents from charters, `X-squad-host-claude`, native skills, on-demand `squad-coordinator-*` skills, advisory hooks and lockouts, the `Agent` tool (formerly `Task`), projection-version stamps, byte-exact rollback of `CLAUDE.md`/`AGENTS.md`/`GEMINI.md` blocks. Regenerate "A Distilled Seven-Host Feature Matrix" from the v2.0.0 matrix. Spec: re-read `client-harness-adapters-v0.2.md` (+255), especially §4–5, §13 and §15.1. Under the Hood: `packages/squad-sdk/src/client/adapters/claude-*.ts`, `coordinator.ts`, `capabilities.ts`. **New source: `docs/specification/adr-003-host-neutral-canonical-coordinator.md`.** |
| 21 | The State MCP Boundary, Runtime Upstreams, and the Experimental Backend *(unchanged)* | Moderate | "Versioned Bridges, Roots, and Cleanup": add the portable `.squad/squad.mjs` launcher and repo-root finder, `doctor` launcher checks, the symlinked-root fix and health metadata. New subsection "Governed Memory Across Backends" (shared CLI/MCP store, transactional migration, locking; cross-ref Vol 1 Ch 15, Vol 2 Ch 2). Upstream statuses: the full set (`ok`, `stale`, `missing`, `unavailable`, `invalid`, `cycle`, `depth-exceeded`) and the depth-3 limit. "The Experimental Backend SPI": the harnesses now exist (`ClaudeAgentSdkHarness`, `CopilotSdkHarness`), `SQUAD_BACKEND_HARNESSES`, the approval queue and `canUseTool` binding; `executionAvailable` can be `true` when the Claude SDK is installed (it was always conditional on a registered harness). "Client/Backend Decoupling v0.2 and the Durable Road Ahead" becomes **"…and What Remains Experimental"** (remote server and §14.4 profile promotion pending). Hands-On step 4 updated for harness registration. |
| 22 | **Migrating from Squad 1.x to Squad 2.0** *(renamed, D2; was "Upgrading to Squad 2.0 and the Road Ahead"; file name unchanged)* | Rewrite (keep H2 skeleton) | Reframe as the 1.x→2.0 migration guide. "Two Upgrades, Three Channels": the stable path is `squad upgrade --self` from a 1.1.0 CLI. **Resolved (FC #73):** a 1.1.0 CLI installs `@bradygaster/squad-cli@latest` (`insider` with `--insider`; v1.1.0 `cli/core/upgrade.ts` l.1432–1433), which is 2.0.0 today. Never copy the docs' `@bradygaster/squad@latest` line (`D/features/self-upgrade.md` l.65): that package is an npm 404, an upstream docs bug. Then `squad upgrade` (rewrites `.mcp.json` to the launcher). Tested upgrade paths: matrix attestations are tied to preview versions; say so. "CLI Reference: What Changed in 2.0" and "Full top-level command inventory": add `client sync`, `lockout`, `hook`, `dashboard` and the `watch` flags, and point to Appendix A as the full reference. "Release Process: Why the Tags Matter": channels after GA. Keep the H2 "The Road Ahead" (it is no longer in the title, but the section stays): rebuild it from the 2.0.0 CHANGELOG's explicitly experimental or pending items and the `[Unreleased]` section. Drop the 7 deleted proposals as sources. Hands-On "Upgrade and Roll Back Tasktrack": use a scratch copy pinned to 1.1.0 (`npm install -g @bradygaster/squad-cli@1.1.0` in an isolated prefix, or a scratch `npx`). Marvin verifies. Re-read `D/scenarios/upgrading.md` (+380 since 1.1), `D/get-started/migration.md`, `D/scenarios/release-process.md` and `D/scenarios/troubleshooting.md`. |

### 3.3 What moves into earlier chapters (no numbering impact)

| 2.0 topic | Primary home after the update | Part IV keeps |
|---|---|---|
| Routine self-upgrade and content-aware project upgrade | Vol 1 Ch 14 | Ch 22: 1.x→2.0 specifics only |
| Removed personal, consult and global modes | Vol 1 Ch 2 (table), Ch 5 (deletion) | Ch 18 checklist, Ch 22 migration |
| `watch` claims, bounded runs, Claude preset | Vol 1 Ch 9 (+ ADR-002 in Vol 2 Ch 17) | Ch 19: one paragraph on the Claude runner |
| History, nap and cost behavior | Vol 1 Ch 12, 15, 16 | — |
| MCP file locations and launcher | Vol 2 Ch 1 | Ch 21: bridge depth |
| Upstream precedence fix | Vol 2 Ch 4 (summary) | Ch 21 (depth) |
| Lockouts and reviewer/human gates | Vol 1 Ch 18 | Ch 20 (Claude hooks mechanics) |
| SDK subpaths | Vol 2 Ch 14, App G | Ch 20/21 (usage) |

### 3.4 Knock-on edits

- `research/CHAPTERS.md`: the Part IV heading, the Ch 22 title, and the line-3 target statement. Owner: Arthur. **Done (WP-A).**
- `README.md`: the volume table, the "Volume 2, Part IV covers Squad 2.0 preview" paragraph, the edition note, the repo and docs links (D4). Owner: Arthur. **Done (WP-A)**, except the source counts, which Arthur fills in after WP-M.
- Ch 22 title (D2): `book/vol2/part-04/ch22-upgrading-to-2.md` H1, `part-04/00-part.md` l.11, the Vol 2 preface. Trillian. Appendix E picks it up on regeneration.
- Both prefaces: the Part IV row and the version paragraphs. Ford for Vol 1, Trillian for Vol 2.
- `book/metadata-vol2.yaml` description; `scripts/render-cover.sh` subtitles. Owner: Slartibartfast.
- Cross-references naming "the 2.0 preview part" or "Chapters 18–22 (preview)": grep `preview` in every file. Each owner fixes their own files.
- Appendix J (see §2), App H callout, App A/B/C Preview sections.
- Exercise solutions for Vol 2 Ch 18–22: `exercises/solutions/vol2/ch18.md`–`ch22.md`.
- Tasktrack progression in `STYLE-GUIDE.md`: Part IV no longer uses a "scratch copy; main project stays on v1.1.0".

---

## 4. Global changes

| Item | From | To | Notes / owner |
|---|---|---|---|
| Docs-site URLs (225 occurrences) | `https://bradygaster.github.io/squad/docs/…`, `/squad/blog` | `https://github.github.com/squad/docs/…` (D4); a bare docs root becomes `https://github.github.com/squad/` | Mechanical. The coverage needle `/squad/docs/<slug>/` is host-agnostic. Slartibartfast runs it (WP-S1). |
| Pinned repo files at v1.1.0 (121) | `https://github.com/bradygaster/squad/blob/v1.1.0/<p>` | `https://github.com/github/squad/blob/v2.0.0/<p>` **if `<p>` exists in v2.0.0**; otherwise `…/github/squad/blob/v1.1.0/<p>` (history) | Script must test each path against `SRC/squad-v2.0.0`. Known v1.1.0-only paths: `consult-mode.md`, `personal-squad.md`, `multi-squad.ts`, `consult.ts`, `extract.ts`, `personal.ts`, `agents/personal.ts`, `sharing/consult.ts`, blog posts (keep at v1.1.0). |
| Pinned files at v2.0.0-preview.2 (32) | `…/bradygaster/squad/blob/v2.0.0-preview.2/<p>` | `…/github/squad/blob/v2.0.0/<p>` if present, else drop (the proposals) | same |
| Other repo links | `github.com/bradygaster/squad` (issues, releases, tree, raw install script) | `github.com/github/squad` | **Do not touch:** `@bradygaster/squad-cli`/`-sdk`, `brew tap bradygaster/squad`, `bradygaster.Squad*` WinGet IDs, the quoted legacy `bradygaster/squad/workflows`, or "© Brady Gaster and contributors" (LICENSE is unchanged). |
| Prose version strings | "v1.1.0" (≈450 in prose), "v2.0.0-preview.2" | "v2.0.0" | **Not mechanical.** Each owner reviews each hit: target statements → v2.0.0; historical statements ("introduced in 1.1.0", "1.x docs said") stay. |
| Preview callouts | 30 callouts that say "Preview (Squad 2.0)" | Fold into prose, or turn into `> **Note:** Changed in Squad 2.0: …` where a 1.x reader needs the warning | Style rule in WP-A. Keep `> **Preview:**` only for things that are experimental in v2.0.0. |
| "Targets Squad v1.1.0" | title pages, prefaces, part intros, metadata, covers, README, CHAPTERS.md, VALIDATION.md, STYLE-GUIDE, check-coverage.py comment | "Targets Squad v2.0.0" | Per owner |
| Metadata | `metadata-vol1.yaml` description "…Targets Squad v1.1.0." | "…Targets Squad v2.0.0." | Slartibartfast |
| | `metadata-vol2.yaml` "…Squad 2.0 multi-client support… Targets Squad v1.1.0 with a Squad 2.0 preview part." | "…multi-host support across seven AI hosts… Targets Squad v2.0.0." | Slartibartfast. `subject` may add "Claude Code". New identifiers and edition marking (D1). |
| Covers | `render-cover.sh` "Covers Squad v1.1.0" / "…and the 2.0 preview" | "Covers Squad 2.0" (both) | Slartibartfast; re-render `cover-vol*.png` |
| Coverage tooling | `check-coverage.py` `SETS` refs `v1.1.0` and `v2.0.0-preview.2`, and the `bradygaster` pinned prefix | refs `v2.0.0` (both sets, or merged), host `github/squad`; allow v1.1.0 history pins for removed sources | Slartibartfast edits the script; Marvin owns the maps (WP-M) |
| Style guide | v1.1.0 target and `~/Projects/squad-src`; URL formats; Preview definition; "Tasktrack progression" note on Part IV; old continuous chapter numbers in the companion-project bullet | v2.0.0 target and source path; new URL formats; Preview = experimental in v2.0.0; the "Changed in Squad 2.0" Note convention; terminology additions (host, host projection, client slug, plugin mode, member subagent, work claim, governed memory, launcher); Rai and Fact Checker are optional built-ins | Arthur (WP-A) |
| Writer briefs | `WRITER-BRIEF.md` (v1.1.0, old paths); `WRITER-BRIEF-2.0.md` (preview.2, "Part X", old numbering 43–47) | One `WRITER-BRIEF.md` for v2.0.0, with the 2.0 brief's seven-host slug list and the "verify against source" list folded in. Mark `WRITER-BRIEF-2.0.md` superseded (one line at top) and keep it as history. Same for `RESTRUCTURE-BRIEF.md`. | Arthur (WP-A) |
| `VALIDATION.md` | v1.1.0 baseline | Add a "Squad 2.0.0 update" section: commit `26654f0c…`, rescan counts, what was re-verified | Marvin |
| Package-name rule | — | — | Repo and docs links change host; **package and installer identifiers never do** (D4). Writers who see `bradygaster` in an npm, Homebrew or WinGet name leave it. | All |
| Live docs drift | — | The live site can run ahead of v2.0.0 (for example the live install page). Writers cite v2.0.0 source files for facts and use live URLs only as links. | All |

---

## 5. Work packages (in order; one owner per file)

Files are listed once. No file has two owners within a phase, and later phases only start when the files they read are done.

**Phase 0: foundations (blocking)**

- **WP-A, Arthur (done 2026-11-20):** `research/UPDATE-PLAN-2.0.md` (final), `research/STYLE-GUIDE.md`, `research/WRITER-BRIEF.md`, `research/WRITER-BRIEF-2.0.md` (superseded banner), `research/RESTRUCTURE-BRIEF.md` (superseded banner), `research/CHAPTERS.md`, `README.md` (text; source counts filled in after WP-M).
- **WP-S1, Slartibartfast (in progress):** the mechanical URL rewrite (to `github.github.com/squad/` and `github.com/github/squad`, D4) across `book/**/*.md` and `exercises/solutions/**/*.md`, following the §4 rules (path-existence-aware pins, exclusion list). It runs **before** any writer opens a chapter, then hands over a list of v1.1.0-history pins it left in place. Also `scripts/check-coverage.py` (refs and host), `scripts/check-links.sh` if it hard-codes hosts, `book/metadata-vol1.yaml`, `book/metadata-vol2.yaml` (new `identifier` UUIDs and edition marking, D1), `scripts/render-cover.sh`, `book/images/src/cover.html` if it carries version text, the cover PNGs, and `.github/workflows/build-epub.yml` (check only).
- **WP-M, Marvin (slot; Marvin's separate assessment decides the details):** `research/sources.txt`, `research/sources-2.0.txt`, `research/coverage.csv`, `research/coverage-2.0.csv`, `research/source-modules.csv`, `research/build_coverage.py`, `research/VALIDATION.md`. Required map changes from this plan:
  - add `adr-002 → vol2:17`, `adr-003 → vol2:20`, `features/claude-code-plugin → vol2:19`, `scenarios/multi-machine-watch → vol1:9` (editorial homes; Marvin's assessment proposed alternatives, and Marvin's final `coverage.csv` is authoritative: writers cite what the map assigns)
  - remove or history-pin `consult-mode (vol1:5)` and `personal-squad (vol1:2)`
  - remove the 8 `docs/proposals/*`
  - re-point or remove the `multi-squad.ts` module row
  - add `packages/squad-sdk/src/client/adapters` and `packages/squad-cli/src/cli/commands/{client,roster,dashboard,lockout,hook}.ts` module rows to the right chapters
  - Tasktrack `sample/` check (README version text; no code change expected)

**Phase 1: Volume 2 prose (Trillian), in parallel with Phase 1b**

- **WP-T1, Part IV (do first):** `book/vol2/part-04/00-part.md`, `ch18`–`ch22`, `exercises/solutions/vol2/ch18.md`–`ch22.md`.
- **WP-T2, Parts I–III and V:** `book/vol2/part-0{1,2,3,5}/*.md`, `exercises/solutions/vol2/ch01.md`–`ch17.md` and `ch23.md`–`ch25.md`.
- **WP-T3, front matter and Volume 2 appendices:** `book/vol2/00-front/00-title.md`, `01-preface.md`, `book/vol2/appendices/app-G-*.md`, `app-H-*.md`, `app-I-*.md`, `app-J-*.md`.

**Phase 1b: Volume 1 prose (Ford), in parallel with Phase 1**

- **WP-F1:** `book/vol1/00-front/*.md`, `book/vol1/part-0{1..4}/*.md`, `exercises/solutions/vol1/ch01.md`–`ch21.md`. Suggested order: Ch 2, 3, 5, 14 (removed features and upgrade), then 9, 12, 15, 16, 18, then the light chapters.

**Phase 2: shared appendices (Ford; after WP-T1 so the 2.0 facts are settled)**

- **WP-F2:** `book/shared/appendices/app-A-cli-reference.md`, `app-B-configuration.md`, `app-C-glossary.md`, `app-D-sample-prompts.md`, `app-F-resources.md`. Trillian reviews the 2.0 rows but does not edit them.

**Phase 3: verification and build**

- **WP-M2, Marvin:** `make coverage`, `make manuscript`, `make links`; spot-verify every command and flag in the changed sections against the 2.0.0 CLI in scratch repos; run the Vol 1 Ch 3 init-tree check and the Vol 2 Ch 22 1.1.0→2.0.0 upgrade/rollback Hands-On end to end; review exercise and quiz accuracy. Report defects to the file owner and do not fix prose.
- **WP-S2, Slartibartfast:** `make check`, `make html`, both EPUBs, epubcheck; regenerate Appendix E.
- **WP-A2, Arthur:** editorial review gate: voice, the dedupe rule, cross-references and Part IV framing. Final `VALIDATION.md` sign-off goes to Marvin.

---

## 6. Open questions for Chris: resolved

All three questions are answered (see "Author decisions" at the top).

1. **Edition identity.** Resolved (D1): new edition, new EPUB identifiers, edition marking. The 1.1 book stays at tag `book-squad-v1.1.0`.
2. **Chapter 22 title.** Resolved (D2): renamed "Migrating from Squad 1.x to Squad 2.0". File name unchanged.
3. **Claude Code in Volume 1.** Resolved (D3): Volume 1 stays Copilot-first with short pointers (Ch 1, 2, 6, 9, 17, 21). Full coverage in Vol 2 Part IV.
4. **Docs host** (raised by FC #6). Resolved (D4): `https://github.github.com/squad/`.

## 7. Final per-owner file lists

- **Ford:** `book/vol1/00-front/00-title.md`, `01-preface.md`; `book/vol1/part-01..04/00-part.md` and `ch01`–`ch21`; `exercises/solutions/vol1/ch01.md`–`ch21.md`; then (Phase 2, after WP-T1) `book/shared/appendices/app-A-cli-reference.md`, `app-B-configuration.md`, `app-C-glossary.md`, `app-D-sample-prompts.md`, `app-F-resources.md`.
- **Trillian:** first `book/vol2/part-04/00-part.md`, `ch18`–`ch22`, `exercises/solutions/vol2/ch18.md`–`ch22.md`; then `book/vol2/part-01,02,03,05/*.md`, `exercises/solutions/vol2/ch01.md`–`ch17.md`, `ch23.md`–`ch25.md`; then `book/vol2/00-front/00-title.md`, `01-preface.md`, `book/vol2/appendices/app-G-*.md`, `app-H-*.md`, `app-I-*.md`, `app-J-*.md`.
- **Neither writer** edits `book/metadata-*.yaml`, `book/images/`, `scripts/`, `sample/`, `research/*` or the generated `app-E-quiz-answers.md`.
