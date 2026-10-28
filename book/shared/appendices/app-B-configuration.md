# Appendix B: Configuration and File Reference

Squad's configuration is distributed across team state, agent instructions, optional workflows, and runtime preferences. `squad init` is deliberately safe to repeat: it fills in missing managed files, while team-authored state remains yours. Some documentation examples predate the current init defaults; the observed v1.1.0 init output and source take precedence.

## What initialization creates

A clean v1.1.0 `squad init` was run in a throwaway Git repository to observe its output. The requested `/tmp` location could not be used in this environment's safety policy, so the same isolated experiment ran in a disposable, repository-local directory and was removed immediately afterward. It generated the following core paths (choices such as `--global`, `--sdk`, `--roles`, `--no-workflows`, presets, and state backends alter the set):

| Path | Role and ownership |
|---|---|
| `.squad/.first-run` | Marks initialization/first-run state. |
| `.squad/config.json` | Squad directory/configuration metadata and resolution hints. |
| `.squad/team.md` | Human-readable roster, member names and roles; edit as your team evolves. |
| `.squad/routing.md` | Work assignment guidance for the coordinator. |
| `.squad/decisions.md` | Shared decision record. Keep durable decisions here and preserve history. |
| `.squad/ceremonies.md` | Team meeting definitions and cadence. |
| `.squad/agents/{name}/charter.md` | Agent role, domain, and behavioral boundaries. Init includes `scribe`, `ralph`, `Rai`, and `fact-checker` charters. |
| `.squad/agents/{name}/history.md` | Per-agent accumulated work notes; generated for the same built-ins. |
| `.squad/identity/now.md`, `wisdom.md` | Current focus and reusable team patterns. |
| `.squad/casting/registry.json`, `history.json`, `policy.json`, `registry-history.commit.json` | Current casting identities, changes, policy, and a commit snapshot for registry/history durability. |
| `.squad/memory/config.json`, `index.json`, `audit.jsonl` | Memory policy/index/audit scaffolding. |
| `.squad/memory/local/`, `policy-inbox/`, `semantic-inbox/`, `tombstones/` | Local and pending memory classification stores. |
| `.squad/rai/policy.md`, `audit-trail.md` | Rai's governance rules and review audit. |
| `.squad/fact-checker/policy.md`, `audit-trail.md` | Fact-checking policy and audit record. |
| `.squad/ralph-instructions.md` | Work-monitor operating instructions. |
| `.squad/templates/` | Versioned templates and reference material; refreshed by upgrade. Includes `README.md`, `after-agent-reference.md`, casting JSON/Markdown, ceremony and charter references, client compatibility, constraint/rate-limit references, Copilot files, issue lifecycle, MCP config, model references, orchestration/session references, routing, schedule, skill templates, Ralph files, and bundled workflows. Treat this directory as managed output; customize source/team files instead. |
| `.github/agents/squad.agent.md` | Copilot-discoverable coordinator prompt copied from Squad's template. Upgrade may replace it; local customizations are backed up. |
| `.github/skills/<skill>/SKILL.md` | Installed operational skills used by the coordinator. The clean init run seeded `agent-collaboration`, `coordinator-init-mode`, `coordinator-response-mode`, `coordinator-source-of-truth`, `cross-squad-communication`, `cross-squad`, `error-recovery`, `git-workflow`, `iterative-retrieval`, `reflect`, `reviewer-protocol`, `secret-handling`, `session-recovery`, `squad-conventions`, `squad-help`, `squad-version-check`, `squad`, `test-discipline`, and `tiered-memory`. The source template tree contains additional skills that are not all copied by this observed default init; upgrade/init selection can change by package version. |
| `.github/workflows/squad-heartbeat.yml` | Scheduled work/health heartbeat automation. |
| `.github/workflows/squad-issue-assign.yml` | Issue assignment automation. |
| `.github/workflows/squad-triage.yml` | Issue triage automation. |
| `.github/workflows/sync-squad-labels.yml` | Synchronizes team members and issue labels. |
| `.mcp.json` | Copilot CLI MCP configuration for the bundled `squad_state` server. |
| `.copilot/mcp-config.json` | Legacy MCP location may be cleaned up when the current `.mcp.json` is installed. |
| `.vscode/settings.json` | By default sets `chat.newSession.defaultMode` to `Squad`; `--no-vscode-default` leaves it alone. |
| `.gitattributes`, `.gitignore` | Merge attributes and exclusions needed by Squad's state handling. |

Some files appear only in option-specific flows. `--no-workflows` omits generated workflows; `--global` initializes in the personal Squad directory; `--sdk` adds root `squad.config.ts` and expects `squad build`; remote mode points `.squad/config.json` to an external root. Individual templates under `.squad/templates/` and skill entries are package-managed and can differ by package revision. A project may also accumulate optional `.squad/directives.md`, `.squad/model-config.json`, `agents/*/skills/`, `decisions/inbox/`, `log/`, `orchestration-log/`, and backend-specific state. These are not all created by a fresh init.

## Files Squad reads or updates

| File family | Read/use |
|---|---|
| `.squad/team.md`, `agents/*/charter.md`, `agents/*/history.md` | Establish roster, roles, and the context handed to each agent. |
| `.squad/routing.md`, `decisions.md`, `directives.md`, `ceremonies.md` | Routing, stable decisions/rules, and recurring team practices. |
| `.squad/config.json`, `casting/*`, `model-config.json` | Resolve team root, casting identity/provenance, state backend, and model preferences where configured. |
| `.squad/identity/*`, `.squad/memory/**`, `.squad/rai/**`, `.squad/fact-checker/**` | Current team context, governed memory, and review policy. |
| `.squad/agents/*/skills/**`, `.github/skills/*/SKILL.md` | Load reusable agent/coordinator skills. |
| `.github/agents/squad.agent.md` | The coordinator prompt Copilot discovers in a repository. |
| `.github/workflows/*.yml`, `templates/workflows/*.yml` | GitHub Actions automation and managed workflow source. |
| `squad.config.ts` | SDK-First configuration compiled by `squad build`. |
| `.mcp.json`, `.copilot/mcp-config.json` | Configure access to the Squad state MCP server. |
| `.gitattributes`, `.gitignore`, `.vscode/settings.json` | Preserve state merge behavior, prevent generated state mishaps, and optionally set the default VS Code session mode. |

The CLI may also use `.ai-team/` for legacy migration and compatibility. `squad upgrade` explicitly preserves `.squad/` and `.ai-team/` team state while refreshing managed coordinator/template files. Never infer that all examples in old documentation are current init defaults: for example, the v1.1.0 observed workflow option is `--no-workflows`, while some older prose refers to an include-workflows switch.

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

Builder entry points in v1.1.0 are `defineSquad`, `defineTeam`, `defineAgent`, `defineBudget`, `defineRouting`, `defineCeremony`, `defineHooks`, `defineCasting`, `defineTelemetry`, `defineDefaults`, and `defineSkill`; `squad build --check` validates without generating Markdown, and `--dry-run` previews writes. Generated files include `.squad/team.md`, `.squad/routing.md`, agent charters, ceremonies, and skill definitions under `.github/skills/`.

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

A complete `process.env` scan of `packages/squad-cli/src`, `packages/squad-sdk/src`, and `templates` found the explicitly named variables below. Several are ordinary host variables or internal guards rather than supported user settings. Values marked “internal” should not be treated as a stable public configuration API. `squad start` also forwards the host environment to its child process, and health checks may read variable names declared in configured integrations.

| Variable | Use in v1.1.0 source |
|---|---|
| `APPDATA`, `LOCALAPPDATA`, `XDG_CONFIG_HOME`, `HOME`, `USERPROFILE`, `USERNAME` | Platform-specific home/application-data and user resolution. |
| `SQUAD_HOME`, `SQUAD_STANDALONE_HOME`, `SQUAD_PERSONAL_DIR` | Override the Squad home, standalone bundle home, or personal Squad path. |
| `SQUAD_NO_PERSONAL` | Disables personal-Squad resolution. |
| `SQUAD_NO_RESOLVE_CACHE` | `1` bypasses cached path resolution. |
| `SQUAD_TEAM_ROOT` | Explicit team-root path used by CLI subprocesses; `--team-root` sets it. |
| `SQUAD_TEAM`, `SQUAD_NAME` | Team/name selection in stream or multi-Squad runtime. |
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
| `SQUAD_DEPLOYMENT_MODE`, `SQUAD_POD_ID` | Deployment mode and pod identity in hosted/Ralph capability paths. |
| `COPILOT_ASSIGN_TOKEN` | Token required by the Copilot issue-assignment workflow. |
| `GITHUB_API_URL`, `GITHUB_SERVER_URL`, `GITHUB_TOKEN` | GitHub Enterprise API/web origin and API authentication. |
| `NODE_NO_WARNINGS` | Set by the CLI entrypoint to suppress Node warnings. |
| `NO_COLOR`, `FORCE_COLOR`, `TERM`, `WT_SESSION` | Terminal color and Windows Terminal capability detection. |
| `npm_config_prefix`, `npm_config_user_agent`, `npm_execpath` | Install-method, npm-prefix, and package-manager detection during upgrade/migration. |
| `GIT_INDEX_FILE` | Internal Git index override used by backend migration. |

The names are a source inventory, not a guarantee that every value is documented as user-configurable. Some source paths access `process.env[name]` using variable names loaded from configuration, and `squad start` enumerates/forwards the environment; those dynamic reads cannot be enumerated as a fixed list. The docs also provide user-facing guidance for the context warning threshold and Copilot integration; treat any unlisted environment as host-owned unless a specific Squad feature documents it.

## GitHub labels

Squad uses structured labels as workflow state, particularly for issue triage and member routing. Common namespaces include `squad` and `squad:{member}` (assignment; multiple member labels can represent collaboration), `go:*` (decision/readiness), `release:*`, `type:*`, and `priority:*`. Within `go`, `release`, `type`, and `priority`, the label guide defines one active label per namespace; adding another replaces the prior value. The set of actual allowed values depends on the project's workflow and release process. Generated actions include label synchronization/enforcement; label changes can trigger automation. The default v1.1.0 issue templates and workflows may create or reconcile labels during setup.

Use the path `.github/workflows/sync-squad-labels.yml` and the `squad:member` label as the bridge between roster names and issue routing. Example:

```bash
gh label create 'squad:designer' --color 0366d6 --description 'Work assigned to Designer'
gh issue list --label 'squad,priority:p0,type:bug'
```

## Squad 2.0 (Preview) Configuration

> **Preview:** The additions below describe Squad `v2.0.0-preview.2` on the `insider` channel. Existing v1.1.0 files and keys remain as documented above unless noted; this preview contract may change.

### New and changed project configuration

| File / key | 2.0 preview contract |
|---|---|
| `.squad/config.json` → `clients` | Optional array of portable host slugs: `copilot`, `claude`, `kiro`, `opencode`, `cursor`, `codex`, and `antigravity`. The value stores no credentials, machine paths, URLs, or session identifiers. A missing or empty array preserves the default Copilot-only setup. `squad init --client`, `squad client add`, and `squad upgrade --client` maintain this setting. |
| `.squad/upstream.json` → `upstreams` | Declares upstream sources used by runtime inheritance. Manage it with `squad upstream add`, `remove`, `list`, and `sync`; entries include a name, source/type, and optional Git `ref`. Sync is the network step; session startup resolves local snapshots only. Earlier declared entries win conflicts. |
| Static team configuration | `.squad/team.md`, `routing.md`, `config.json`, and agent `charter.md` files are static project inputs. The state MCP tools reject writes to those files; edit them in the workspace. `.squad/casting/` is managed state and must not be hand-edited; use `squad cast` for roster changes. |
| Project resolution and ignored state | Squad resolves `.squad/` from the current directory and its parents. 2.0 does not fall back to a user-profile or global team. Outside a project, initialize one or supply `--team-root` where that command supports it. Upgrade also ignores `.squad/backend/`; without `--client`, it does not add client-specific ignore entries. |

### Host-generated projection files

The host adapter creates or merges the files listed here. Copilot's canonical coordinator is bootstrapped by `init`/`upgrade`; the client adapter also projects its MCP configuration. Shared JSON, TOML, Markdown markers, and `.gitignore` edits are merged rather than blindly replaced, and managed projection removal supports byte-preserving rollback.

| Host slug | Generated or updated project files |
|---|---|
| `copilot` | `.github/agents/squad.agent.md`; `.mcp.json` |
| `claude` | `.claude/agents/squad.md`; `.mcp.json`; a managed block in `CLAUDE.md`; `.gitignore` entry for `.claude/worktrees/` |
| `kiro` | `.kiro/steering/squad.md`; `.kiro/agents/squad.json`; `.kiro/settings/mcp.json` |
| `opencode` | `.opencode/agent/squad.md`; `opencode.json` or existing `opencode.jsonc` |
| `cursor` | `.cursor/rules/squad.mdc`; `.cursor/agents/squad.md`; `.cursor/mcp.json` |
| `codex` | `.codex/agents/squad.toml`; `.codex/config.toml`; a managed discovery block in `AGENTS.md` |
| `antigravity` | `.agents/agents/squad.md`; a managed discovery block in `GEMINI.md` |

Generated files are project artifacts, not host installations. Each host still requires its own CLI/editor and authentication; projection does not grant a license or sign a user in.

### New environment variables

| Variable | Purpose and constraint |
|---|---|
| `SQUAD_EXPERIMENTAL_BACKEND=1` | Opts `squad state-mcp` into the experimental `squad_backend_*` MCP tools. Equivalent to `--experimental-backend`; `SQUAD_BACKEND_URL` alone is not an enable switch. |
| `SQUAD_BACKEND_URL` | For `squad state-mcp`, selects an external `/v1/conversations` endpoint when the experimental backend is enabled. HTTPS is required except for localhost. SDK callers pass `baseUrl` explicitly rather than relying on this CLI environment variable. |
| `SQUAD_BACKEND_TOKEN` | Optional bearer token used by `squad state-mcp` with `SQUAD_BACKEND_URL`. SDK callers pass `token` explicitly. |
