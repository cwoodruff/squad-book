# Appendix B: Configuration and File Reference

Squad's configuration is distributed across team state, agent instructions, optional workflows, and runtime preferences. `squad init` is deliberately safe to repeat: it fills in missing managed files, while team-authored state remains yours. Some documentation examples predate the current init defaults; the observed v2.0.0 init output and source take precedence.

## What initialization creates

A clean v2.0.0 `squad init` was run in a throwaway Git repository to observe its output. It generated the following core paths (choices such as `--client`, `--sdk`, `--roles`, `--no-workflows`, presets, and state backends alter the set):

| Path | Role and ownership |
|---|---|
| `.squad/.first-run` | Marks initialization/first-run state. |
| `.squad/config.json` | Squad directory/configuration metadata and resolution hints. A fresh Copilot-only init writes only `{"version": 1}`; the keys are listed in "`.squad/config.json` keys" below. |
| `.squad/squad.mjs` | The committed launcher. MCP configs and Claude Code hooks start the CLI through it (`node .squad/squad.mjs state-mcp`) instead of a machine-specific path. It tries `SQUAD_CLI`, then the project's `node_modules/@bradygaster/squad-cli`, then `squad` on PATH, then the CLI that last ran init or upgrade on this machine (`~/.squad/cli.json`), and uses `npx` only when `SQUAD_ALLOW_NPX=1`. Managed: init and upgrade rewrite it. |
| `.squad/team.md` | Human-readable roster, member names and roles; edit as your team evolves. |
| `.squad/routing.md` | Work assignment guidance for the coordinator. |
| `.squad/decisions.md` | Shared decision record. Keep durable decisions here and preserve history. |
| `.squad/ceremonies.md` | Team meeting definitions and cadence. |
| `.squad/agents/{name}/charter.md` | Agent role, domain, and behavioral boundaries. Init includes `scribe`, `ralph`, `rai`, and `fact-checker` charters. `team.md` starts without a support table; a project's first `squad cast --name ... --role ...` adds all four built-ins to it. |
| `.squad/agents/{name}/history.md` | Per-agent accumulated work notes; generated for the same built-ins. |
| `.squad/identity/now.md`, `wisdom.md` | Current focus and reusable team patterns. |
| `.squad/casting/registry.json`, `history.json`, `policy.json`, `registry-history.commit.json` | Current casting identities, changes, policy, and a commit snapshot for registry/history durability. |
| `.squad/memory/config.json`, `index.json`, `audit.jsonl` | Memory policy/index/audit scaffolding. |
| `.squad/memory/local/`, `policy-inbox/`, `semantic-inbox/`, `tombstones/` | Local and pending memory classification stores. Init creates them empty, so Git does not track them until they hold files. |
| `.squad/rai/policy.md`, `audit-trail.md` | Rai's governance rules and review audit. |
| `.squad/fact-checker/policy.md`, `audit-trail.md` | Fact-checking policy and audit record. |
| `.squad/ralph-instructions.md` | Work-monitor operating instructions. |
| `.squad/templates/` | Versioned templates and reference material; refreshed by upgrade. Includes `README.md`, `after-agent-reference.md`, `human-members.md` (the human sign-off gate, shipped again in 2.0), casting JSON/Markdown, ceremony and charter references, client compatibility, constraint/rate-limit references, Copilot files, issue lifecycle, MCP config, model references, orchestration/session references, routing, schedule, skill templates, Ralph files, and bundled workflows. Treat this directory as managed output; customize source/team files instead. |
| `.github/agents/squad.agent.md` | Copilot-discoverable coordinator prompt copied from Squad's template. Upgrade may replace it; local customizations are backed up. |
| `.github/skills/<skill>/SKILL.md` | Installed operational skills used by the coordinator. The clean init run seeded `agent-collaboration`, `coordinator-init-mode`, `coordinator-response-mode`, `coordinator-source-of-truth`, `cross-squad-communication`, `cross-squad`, `error-recovery`, `git-workflow`, `iterative-retrieval`, `reflect`, `reviewer-protocol`, `secret-handling`, `session-recovery`, `squad-conventions`, `squad-help`, `squad-version-check`, `squad`, `test-discipline`, and `tiered-memory`. The source template tree contains additional skills that are not all copied by this observed default init; upgrade/init selection can change by package version. |
| `.github/workflows/squad-heartbeat.yml` | Scheduled work/health heartbeat automation. |
| `.github/workflows/squad-issue-assign.yml` | Issue assignment automation. |
| `.github/workflows/squad-triage.yml` | Issue triage automation. |
| `.github/workflows/sync-squad-labels.yml` | Synchronizes team members and issue labels. |
| `.mcp.json` | The project MCP file Copilot CLI reads: the bundled `squad_state` server, started through the `.squad/squad.mjs` launcher. This is the authoritative project MCP configuration. |
| `.copilot/mcp-config.json` | A sample file (an `EXAMPLE-github` server) that init still writes. Copilot CLI does not read a project `.copilot/mcp-config.json`; its personal config is `~/.copilot/mcp-config.json`, and VS Code uses `.vscode/mcp.json` (key `servers`). |
| `.vscode/settings.json` | By default sets `chat.newSession.defaultMode` to `Squad`; `--no-vscode-default` leaves it alone. |
| `.gitattributes`, `.gitignore` | Merge attributes and exclusions needed by Squad's state handling. |

Some files appear only in option-specific flows. `--no-workflows` omits generated workflows; `--client <list>` adds host projection files (see "Host projection files" below); `--sdk` adds root `squad.config.ts` and expects `squad build`; remote mode points `.squad/config.json` to an external root. Individual templates under `.squad/templates/` and skill entries are package-managed and can differ by package revision. A project may also accumulate optional `.squad/directives.md`, `.squad/model-config.json`, `agents/*/skills/`, `decisions/inbox/`, `log/`, `orchestration-log/`, and backend-specific state. These are not all created by a fresh init. `.squad/governance/lockouts.json` appears when you first run `squad lockout`, and `.squad/casting/handwritten-archive-<sha256>/` appears when casting repair archives a hand-edited registry.

## Files Squad reads or updates

| File family | Read/use |
|---|---|
| `.squad/team.md`, `agents/*/charter.md`, `agents/*/history.md` | Establish roster, roles, and the context handed to each agent. |
| `.squad/routing.md`, `decisions.md`, `directives.md`, `ceremonies.md` | Routing, stable decisions/rules, and recurring team practices. |
| `.squad/config.json`, `casting/*`, `model-config.json` | Resolve team root, configured hosts, casting identity/provenance, state backend, and model preferences where configured. A malformed `config.json` stops `squad watch`. |
| `.squad/governance/lockouts.json` | Reviewer-lockout records written by `squad lockout`; the advisory Claude Code hooks read them. |
| `.squad/upstream.json` | Upstream sources for runtime inheritance, managed by `squad upstream`. |
| `.squad/identity/*`, `.squad/memory/**`, `.squad/rai/**`, `.squad/fact-checker/**` | Current team context, governed memory, and review policy. |
| `.squad/agents/*/skills/**`, `.github/skills/*/SKILL.md` | Load reusable agent/coordinator skills. |
| `.github/agents/squad.agent.md` | The coordinator prompt Copilot discovers in a repository. |
| `.github/workflows/*.yml`, `templates/workflows/*.yml` | GitHub Actions automation and managed workflow source. |
| `squad.config.ts` | SDK-First configuration compiled by `squad build`. |
| `.mcp.json` (Copilot CLI), `.vscode/mcp.json` (VS Code), host MCP files | Configure access to the Squad state MCP server. `.copilot/mcp-config.json` in the project is only a sample. |
| `.gitattributes`, `.gitignore`, `.vscode/settings.json` | Preserve state merge behavior, prevent generated state mishaps, and optionally set the default VS Code session mode. |

`squad nap` keeps the files in this table small: a `history.md` over 15 KB keeps its Core Context and the last 5 `##` sections (3 with `--deep`) and archives the rest, logs older than 7 days are deleted, and once `decisions.md` is over 20 KB its older entries move to `decisions-archive.md`.

The CLI may also use `.ai-team/` for legacy migration and compatibility. `squad upgrade` explicitly preserves `.squad/` and `.ai-team/` team state while refreshing managed coordinator/template files. Never infer that all examples in old documentation are current init defaults: for example, the v2.0.0 workflow option is `--no-workflows`, while some older prose refers to an include-workflows switch.

## `squad.config.ts` and SDK configuration

The SDK-First root file exports a `defineSquad({...})` value. Common top-level properties include a version, team definition, agent definitions, routing, and optional budgets, defaults, ceremonies, hooks, casting, telemetry, and skills. The exact accepted structure is validated by SDK builders, rather than by a generic JSON schema. A compact example:

```ts
import { defineAgent, defineRouting, defineSquad, defineTeam } from '@bradygaster/squad-sdk';

export default defineSquad({
  version: '1.0.0',
  team: defineTeam({ name: 'tasktrack', description: 'Tasktrack team', members: ['@api'] }),
  agents: [defineAgent({ name: 'api', role: 'API engineer', model: 'claude-sonnet-5', tools: ['grep', 'edit'] })],
  routing: defineRouting({ rules: [{ pattern: 'api-*', agents: ['@api'], tier: 'standard' }], defaultAgent: '@coordinator' }),
});
```

Builder entry points in v2.0.0 are `defineSquad`, `defineTeam`, `defineAgent`, `defineBudget`, `defineRouting`, `defineCeremony`, `defineHooks`, `defineCasting`, `defineTelemetry`, `defineDefaults`, and `defineSkill`; `squad build --check` validates without generating Markdown, and `--dry-run` previews writes. Generated files include `.squad/team.md`, `.squad/routing.md`, agent charters, ceremonies, and skill definitions under `.github/skills/`.

`.squad/config.json` is runtime directory/state metadata, distinct from `squad.config.ts`, which is the authoring input. The SDK-First `SquadSDKConfig` shape has these top-level keys (requiredness shown):

| Key | Required? | Value / nested keys |
|---|---|---|
| `version` | no | Schema-version string. |
| `team` | yes | `name`, optional `description`, `projectContext`, required `members`. |
| `agents` | yes | Agent records: `name`, `role`, optional `description`, `model`, `tools`, capability and rule fields. |
| `defaults` | no | `model`, `reasoningEffort`, `contextTier`, `budget`. |
| `routing` | no | `rules`, optional `defaultAgent`, `fallback`. |
| `ceremonies` | no | `name`, optional `trigger`, `schedule`, `participants`, `agenda`, and hook names. |
| `hooks` | no | `allowedWritePaths`, `blockedCommands`, `maxAskUser`, `scrubPii`, `reviewerLockout`. |
| `casting` | no | `allowlistUniverses`, `overflowStrategy`, per-universe `capacity`. |
| `telemetry` | no | `enabled`, `endpoint`, `serviceName`, `sampleRate`, `aspireDefaults`. |
| `skills` | no | Skill definitions with `name`, `description`, `domain`, `content`, and optional confidence/source/tools. |

This builder schema is separate from the runtime `SquadConfig` parsed by `loadConfig`. That runtime schema includes required `version`, `models`, and `routing`; optional `casting`, `agentSources`, `mcp`, and `platforms`; and allows custom extension keys. `models` includes `defaultModel`, `defaultTier`, optional `costPolicy`, `taskRules`, `roleMapping`, `complexityAdjustments`, `fallbackChains` (`premium`, `standard`, `fast`), provider/tier preferences, and optional nuclear fallback. `routing` includes `rules`, optional `issueRouting`, `copilotEvaluation`, and `governance` (`eagerByDefault`, `scribeAutoRuns`, `allowRecursiveSpawn`). `casting` includes `allowlistUniverses`, `universeCapacity`, and `overflowStrategy`. `agentSources` records `type` (`local|git|npm|url`), `location`, optional `version`, and cache policy; `mcp` can hold server config; `platforms` exposes client overrides such as VS Code model-selection and Scribe modes. These keys describe the distinct runtime config interface in `packages/squad-sdk/src/runtime/config.ts`; do not assume the builder accepts all runtime keys.

## Environment variables

A case-insensitive scan of `packages/squad-cli/src`, `packages/squad-sdk/src`, and `templates` for named environment reads (`process.env.NAME` and `process.env['NAME']`, the same forms on env objects passed in as parameters, and keys held in string constants) found the variables below. Shell `$NAME` references in template scripts and workflows were not part of the scan. Several are ordinary host variables or internal guards rather than supported user settings. Values marked "internal" should not be treated as a stable public configuration API. `squad start` also forwards the host environment to its child process, minus a blocklist of injection-prone names (`NODE_OPTIONS`, `LD_PRELOAD` and others) and any name that looks like a secret, and health checks may read variable names declared in configured integrations.

| Variable | Use in v2.0.0 source |
|---|---|
| `APPDATA`, `LOCALAPPDATA`, `XDG_CONFIG_HOME`, `HOME`, `USERPROFILE`, `USERNAME` | Platform-specific home/application-data and user resolution. |
| `SQUAD_HOME`, `SQUAD_STANDALONE_HOME` | Override the Squad home (default `~/.squad`, which holds `cli.json`, `dashboards/` and the externalized-state base and is never treated as a project squad) or the standalone bundle home. |
| `SQUAD_CLI` | The first place the `.squad/squad.mjs` launcher and the Claude Code plugin's launcher look for the CLI: a command, or a `.js` entry run with the same Node. |
| `SQUAD_ALLOW_NPX` | `1` lets the launchers fall back to `npx -y @bradygaster/squad-cli@<version>`. Off by default, because that downloads and runs code. |
| `SQUAD_NO_RESOLVE_CACHE` | `1` bypasses cached path resolution. |
| `SQUAD_TEAM_ROOT` | Explicit team-root path used by CLI subprocesses; `--team-root` sets it. With personal squads gone, this and `--team-root` are the way to point at a team outside the current directory tree. |
| `SQUAD_TEAM` | SubSquad selection in the streams resolver. |
| `SQUAD_WORKSTREAM` | Active workstream slug; `squad_decide` writes its inbox note there when `workstreams/active/<slug>/` exists. |
| `SQUAD_DEFAULT_MODEL` | Runtime default-model override. |
| `SQUAD_ECONOMY_MODE` | Set to `1` to enable economy selection for the current CLI session. |
| `SQUAD_CONTEXT_WARNING_THRESHOLD` | Interactive-shell context utilization warning threshold; documented as a fraction greater than 0 and at most 1 (default `0.8`). |
| `SQUAD_HEALTH_CHECK_MS`, `SQUAD_GIT_CLONE_MS`, `SQUAD_PLUGIN_FETCH_MS`, `SQUAD_SESSION_TIMEOUT_MS` | Runtime timeout constants for health checks, Git clone, plugin fetch, and session response; each falls back to its in-source default when unset. |
| `SQUAD_REPL_TIMEOUT` | Interactive shell timeout setting. |
| `SQUAD_MEMORY_LOG_LEVEL` | Memory diagnostic verbosity (`none`, `error`, `info`, or `debug`). Default is `none`. |
| `SQUAD_DEBUG` | `1` enables internal debug logging. |
| `SQUAD_TELEMETRY` | `1` enables shell telemetry. |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | OpenTelemetry export endpoint; also used to detect telemetry availability. |
| `SQUAD_NO_UPDATE_CHECK` | `1` suppresses background CLI update checks. |
| `SQUAD_SYNC_ACTIVE` | Internal re-entry guard while `squad sync` runs. |
| `SQUAD_DEPLOYMENT_MODE`, `SQUAD_POD_ID` | Deployment mode and pod identity in hosted/Ralph capability paths; `SQUAD_POD_ID` can also name the watcher that holds a work claim. |
| `SQUAD_MACHINE_ID` | The machine ID a watcher records in its work claims, used as is. It is checked first, before the `machine` capability and `SQUAD_POD_ID`; with none of them set, Squad uses a salted hash of the hostname. Set a readable name (a pseudonym on public repositories) to tell holders apart. |
| `SQUAD_NONINTERACTIVE`, `CI` | Any value other than empty, `0` or `false` in either one makes `squad init` skip its interactive prompts. |
| `SQUAD_EXPERIMENTAL_BACKEND` | `1` opts `squad state-mcp` into the experimental `squad_backend_*` MCP tools, like `--experimental-backend`. |
| `SQUAD_BACKEND_URL`, `SQUAD_BACKEND_TOKEN` | With the experimental backend enabled, select an external `/v1/conversations` endpoint (HTTPS, or HTTP only for localhost) and an optional bearer token. `SQUAD_BACKEND_URL` alone enables nothing. SDK callers pass `baseUrl` and `token` explicitly. |
| `SQUAD_BACKEND_HARNESSES` | Comma-separated execution harnesses for the experimental local backend, or `none`. The default `claude-agent-sdk` registers only when `@anthropic-ai/claude-agent-sdk` is installed and an API credential is configured; `copilot-sdk` is opt-in. |
| `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX`, `CLAUDE_CODE_USE_FOUNDRY` | Host credentials. The experimental `claude-agent-sdk` harness counts as configured only when an API key or auth token is set, or one of the `CLAUDE_CODE_USE_*` switches is `1` or `true`; it never falls back to a saved claude.ai login. |
| `CLAUDE_CONFIG_DIR` | Claude Code's configuration directory (default `~/.claude`); `squad dashboard` finds the session logs under its `projects/` folder. |
| `CLAUDE_PROJECT_DIR` | Set by Claude Code; `squad hook claude <Event>` and the Claude hooks use it to find the launcher and the project. |
| `SQUAD_DASHBOARD_NO_OPEN` | `1` keeps `squad dashboard` from opening a browser. |
| `SQUAD_DASHBOARD_CHILD` | Internal: marks the detached dashboard child process. |
| `COPILOT_ASSIGN_TOKEN` | Token required by the Copilot issue-assignment workflow. |
| `GITHUB_API_URL`, `GITHUB_SERVER_URL`, `GITHUB_TOKEN` | GitHub Enterprise API/web origin and API authentication. |
| `NODE_NO_WARNINGS` | Set by the CLI entrypoint to suppress Node warnings. |
| `NO_COLOR`, `FORCE_COLOR`, `TERM`, `WT_SESSION` | Terminal color and Windows Terminal capability detection. |
| `npm_config_prefix`, `npm_config_user_agent`, `npm_execpath` | Install-method, npm-prefix, and package-manager detection during upgrade/migration. |
| `VSCODE_PID`, `VSCODE_IPC_HOOK`, `CODESPACES`, `GITHUB_CODESPACE_TOKEN`, `COPILOT_CLI` | Detect which Copilot surface is running (VS Code, Codespaces or Copilot CLI). |
| `PATH`, `PATHEXT` | The launchers search `PATH` (with `PATHEXT` on Windows) for a `squad` command. |
| `ComSpec` | Windows only: the shell the MCP probe uses to run `.cmd`/`.bat` files and `npx`, `npm`, `pnpm` or `yarn` commands. Default `cmd.exe`. |
| `GIT_INDEX_FILE` | Internal Git index override used by backend migration. |
| `GIT_CONFIG_PARAMETERS` | Read by `squad upstream`'s Git clone and pull subprocesses and extended, not replaced: Squad appends its protocol restrictions (`protocol.file.allow=never`, `core.symlinks=false` and others). Unset by default. |

The names are a source inventory, not a guarantee that every value is documented as user-configurable. Some source paths access `process.env[name]` using variable names loaded from configuration, and `squad start` enumerates/forwards the environment; those dynamic reads cannot be enumerated as a fixed list. The docs also provide user-facing guidance for the context warning threshold and Copilot integration; treat any unlisted environment as host-owned unless a specific Squad feature documents it.

## GitHub labels

Squad uses structured labels as workflow state, particularly for issue triage and member routing. Common namespaces include `squad` and `squad:{member}` (assignment; multiple member labels can represent collaboration), `go:*` (decision/readiness), `release:*`, `type:*`, and `priority:*`. Within `go`, `release`, `type`, and `priority`, the label guide defines one active label per namespace; adding another replaces the prior value. The set of actual allowed values depends on the project's workflow and release process. Generated actions include label synchronization/enforcement; label changes can trigger automation. The default v2.0.0 issue templates and workflows may create or reconcile labels during setup.

Use the path `.github/workflows/sync-squad-labels.yml` and the `squad:member` label as the bridge between roster names and issue routing. Example:

```bash
gh label create 'squad:designer' --color 0366d6 --description 'Work assigned to Designer'
gh issue list --label 'squad,priority:p0,type:bug'
```

## `.squad/config.json` keys

`.squad/config.json` is static project configuration: commit it, and edit it in the workspace. The state MCP tools refuse to write it. A fresh Copilot-only init writes only `version`; the other keys appear when you use the feature. The CHANGELOG, the Ralph feature page and `packages/squad-sdk/src/client/adapters/claude-hooks.ts` document the host and watch keys; the docs' configuration reference does not list them yet.

| Key | Values and effect |
|---|---|
| `version` | Config format version (`1`). |
| `clients` | Array of host slugs: `copilot`, `claude`, `kiro`, `opencode`, `cursor`, `codex`, `antigravity`. It stores no credentials, machine paths, URLs or session IDs. Missing or empty means the default Copilot host only. `squad init --client`, `squad client add` and `squad upgrade --client` maintain it, and `squad client sync` and `squad upgrade` refresh every host it lists. |
| `claudePlugin` | `true` puts the Claude projection in plugin mode: Squad writes the member subagents, the `CLAUDE.md` block, the `agent` and `disabledMcpjsonServers` keys of `.claude/settings.json` (plus the allow rules when `claudePermissions` is on), `.claude/.squad-plugin-settings.json`, `.claude/.squad-permissions.json` and the `.claude/worktrees/` entry in `.gitignore` (see the plugin-mode row under Host projection files), and the Squad plugin for Claude Code supplies the rest. Set with `--claude-plugin`; `--no-claude-plugin` switches back. |
| `claudeHooks` | `"advisory"` merges Squad's advisory hook handlers into `.claude/settings.json`; each runs `squad hook claude <Event>` through the launcher. Any other value, or no value, is off. The hooks warn and add context; they never block a tool call. |
| `claudePermissions` | On unless set to `"off"`. When on, init and upgrade add a scoped allowlist to `.claude/settings.json` (the `squad_state` tools by name, plus `squad cast`, `squad client sync`, `squad lockout reject` and `squad lockout status`) and record what they added in `.claude/.squad-permissions.json`. |
| `governance.authorities` | Array of extra names allowed to record `squad lockout override`; `user` is always allowed. |
| `memory.logLevel` | Governed-memory diagnostics (`none`, `error`, `info`, `debug`); `SQUAD_MEMORY_LOG_LEVEL` overrides it. |
| `watch.agentPreset` | `"copilot"` (default) or `"claude"`: the runner `squad watch` uses each round. `--agent-preset` wins. |
| `watch.claudeFlags` | Extra flags for the `claude` preset. Because the file belongs to the repository, it may set only `--permission-mode`, `--model`, `--fallback-model`, `--effort` and `--max-turns`; anything else stops watch. `--claude-flags` on the command line is not restricted. |
| `watch.claims` | `"none"` (default), `"git-ref"`, or `{ "provider": "git-ref", "ttlMs", "skewMarginMs", "remote", "refPrefix" }`. Claims stop several watchers from working the same issue (ADR-002). An invalid value stops watch rather than silently running without claims; `--claims` overrides `provider` only. |

The `watch` object also takes the other loop settings (`interval`, `execute`, `maxConcurrent`, `timeout`, `maxRounds`, `maxDuration`, `copilotFlags`, `logFile` and more) and per-capability options under `capabilities`; command-line flags win. Chapter 9 (Volume 1) covers them. `squad init --mode remote` adds a team-root pointer; see Chapter 2 (Volume 1). A malformed `config.json` stops `squad watch`.

## Static and managed project state

| File / key | Contract in v2.0.0 |
|---|---|
| `.squad/upstream.json` → `upstreams` | Declares upstream sources used by runtime inheritance. Manage it with `squad upstream add`, `remove`, `list`, and `sync`; entries include a name, source/type, and optional Git `ref`. Sync is the network step; session startup resolves local snapshots only. Earlier declared entries win conflicts. |
| Static team configuration | `.squad/team.md`, `routing.md`, `config.json`, and agent `charter.md` files are static project inputs. The state MCP tools reject writes to those files; edit them in the workspace. `.squad/casting/` is managed state and must not be hand-edited; use `squad cast` for roster changes. It stays on the source branch for every state backend. |
| Project resolution and ignored state | Squad resolves `.squad/` from the current directory and its parents only. There is no user-profile or global team. Outside a project, initialize one or supply `--team-root` (or `SQUAD_TEAM_ROOT`). Upgrade adds `.squad/backend/` to `.gitignore`; it adds `.claude/worktrees/` only when `claude` is a configured host. |

## Host projection files

The host adapter creates or merges the files listed here. Copilot's coordinator is bootstrapped by `init`/`upgrade`; the client adapter also projects each host's MCP configuration, and every MCP config starts the state server through `.squad/squad.mjs`. Shared JSON, TOML, Markdown markers, and `.gitignore` edits are merged rather than blindly replaced, and managed projection removal supports byte-preserving rollback.

| Host slug | Generated or updated project files |
|---|---|
| `copilot` | `.github/agents/squad.agent.md`; `.mcp.json` |
| `claude` (full projection) | `.claude/agents/squad.md` (the coordinator) and `.claude/agents/<member>.md` (one member subagent per team member); `.claude/skills/` (native skills plus the `squad-coordinator-*` on-demand skills); `.claude/settings.json` (scoped allow rules, and the advisory hooks when `claudeHooks` is on); `.claude/.squad-permissions.json`; `.mcp.json`; a managed block in `CLAUDE.md`; `.gitignore` entry for `.claude/worktrees/` |
| `claude` (plugin mode) | `.claude/agents/<member>.md`; the `CLAUDE.md` block; `.claude/settings.json` with `agent` (`squad:squad`), `disabledMcpjsonServers` (the project's `squad_state`) and the allow rules; `.claude/.squad-plugin-settings.json`, which records what Squad changed so it can undo it; `.claude/.squad-permissions.json`; `.gitignore` entry for `.claude/worktrees/` |
| `kiro` | `.kiro/steering/squad.md`; `.kiro/agents/squad.json`; `.kiro/settings/mcp.json` |
| `opencode` | `.opencode/agent/squad.md`; `opencode.json` or existing `opencode.jsonc` |
| `cursor` | `.cursor/rules/squad.mdc`; `.cursor/agents/squad.md`; `.cursor/mcp.json` |
| `codex` | `.codex/agents/squad.toml`; `.codex/config.toml`; a managed discovery block in `AGENTS.md` |
| `antigravity` | `.agents/agents/squad.md`; a managed discovery block in `GEMINI.md` |

Generated files are project artifacts, not host installations. Each host still requires its own CLI/editor and authentication; projection does not grant a license or sign a user in. Volume 2, Part IV explains each host's files.
