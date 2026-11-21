# Appendix A: CLI Reference

The command inventory below targets the Squad v2.0.0 CLI. Use `squad --help` for the installed binary's synopsis and `squad <command> --help` for that command's detail. Most commands accept help at the command level; action-oriented commands such as `triage`, `loop`, and integrations can enter an interactive or long-running path when options are misplaced, so consult the syntax before executing them. Flags marked "none" have no command-specific options in the v2.0.0 help or source. Global options are listed separately, and the commands Squad 2.0 removed are listed at the end of the appendix.

## Global invocation

| Form | Effect |
|---|---|
| `squad` | Legacy interactive shell entry (deprecated in favor of `copilot --agent squad`); without arguments the installed CLI's help describes launching the shell. |
| `squad <command> [options]` | Run an operation. |
| `squad --help`, `squad -h` | Print command overview. |
| `squad --version`, `squad -v`, `squad version` | Print installed version. |

Global flags: `--economy` requests economy-mode model selection for that session; `--team-root <path>` overrides team-root resolution (the `SQUAD_TEAM_ROOT` environment variable does the same). Global availability is parser-dependent: a command's own help is authoritative. `--global` is gone: on any command, Squad 2.0 stops with `Unknown option: --global` and tells you to run the command inside the project. The top-level CLI identifies itself as `squad v2.0.0`.

## Commands and options

| Command | Operands, options, defaults, and behavior |
|---|---|
| `init` | Creates the Markdown team plus default workflows. `--sdk` selects SDK-builder setup; `--roles` seeds built-in roles; `--no-workflows` skips workflow files; `--no-vscode-default` avoids changing `.vscode/settings.json`; `--preset <name>` applies a preset; `--state-backend <type>` accepts `local`, `orphan`, or `two-layer`. `--client <list>` projects hosts: a comma-separated list of `copilot`, `claude`, `kiro`, `opencode`, `cursor`, `codex`, `antigravity`, or `all`. Without it, init is Copilot-only. The hosts are recorded in `.squad/config.json` `clients[]`. `--claude-plugin` (with `--client claude`) selects plugin mode and records `"claudePlugin": true`. Init always installs the Scribe, Ralph, Rai and Fact Checker charters. Remote form: `squad init --mode remote <team-repo-path>` writes a config pointer to an external team root. |
| `upgrade` | Updates Squad-owned prompt and template assets, not team state. The comparison is content-aware and ignores line endings; a file you customized is first saved to a verified `<file>.local-backup`. It never touches `team.md`, `routing.md`, decisions, histories, the casting registry, `config.json` or `.ai-team/`. `--dry-run` writes nothing and lists only the files that would change; `--migrate-directory` renames legacy `.ai-team/`; `--state-backend <type>` migrates to `orphan` or `two-layer`; `--client <list>` adds hosts and refreshes every configured host; `--claude-plugin` / `--no-claude-plugin` switches the Claude projection into or out of plugin mode; `--force` re-processes files that are already current. `--self` upgrades the CLI package on its installed channel (prerelease installs follow `@insider`, stable installs follow `@latest`); `--insider` with `--self` forces the insider tag; `--force` with `--self` allows a downgrade, which is refused otherwise. `--self --dry-run` prints the install command and installs nothing (a 1.1.0 CLI ignores `--dry-run` with `--self` and installs for real). |
| `client` (`clients`) | `client list [--json]` (also `ls`) lists the hosts in `clients[]` and whether their projected files exist; an empty `clients[]` means only the default Copilot host. Once `clients[]` has entries, only those are listed: after `client add claude`, or after another host is removed, Copilot is not listed although its files remain. `client add <list> [--dry-run]` projects and records more hosts. `client sync [--dry-run]` refreshes the configured hosts' files, for example the Claude member subagents after `routing.md` changes. |
| `roster` | `roster add <rai\|fact-checker\|all> [--dry-run]` and `roster remove <rai\|fact-checker\|all> [--dry-run]` (aliases for remove: `disable`, `uninstall`). Opts the optional built-ins into `team.md` on a roster that already has the support table without them, for example a team upgraded from 1.x. Prints the exact `team.md` diff first; the first add writes a verified byte-exact backup and records provenance. Remove deletes only rows this command added. `upgrade` never edits the roster. |
| `update-check` | Reports cached CLI update state. `--json` emits JSON; `--refresh` bypasses cache and queries the registry. Exit codes: `0` current/no cache, `1` update available, `2` refresh transport failure. |
| `migrate` | `--to sdk\|markdown` converts squad format; `--from ai-team` migrates the legacy directory; `--dry-run` previews. |
| `sync` | Git-native state sync; `--push`, `--pull`, or both select direction; `--remote <name>` chooses remote; `--quiet` suppresses routine output. A no-op for the `local` and `worktree` backends; the git hooks invoke it. No automatic remote selection is implied by these flags. |
| `status` | Shows the resolved project squad and any inherited upstreams. Outside a project it fails with `No squad in this directory`. No command-specific flags. |
| `roles` | Lists built-in roles; `--category <name>` filters category and `--search <query>` searches. |
| `cost` | Reports token usage for the newest Squad session, falling back to orchestration logs; `--all` includes all logged sessions; `--agent <name>` filters by agent. |
| `triage` / `watch` | Scans work. `watch` is a source-dispatched alias; `watch --health` prints watch-instance status. `--interval <minutes>` defaults to 10; `--execute` enables agent dispatch; `--copilot-flags "..."` passes extra Copilot CLI flags; `--agent-preset <copilot\|claude>` picks the agent runner (default `copilot`); `--claude-flags "..."` passes flags to the `claude` preset; `--max-concurrent N` defaults to 1; `--timeout N` defaults to 30 minutes per issue; `--max-rounds N` stops after N completed rounds; `--max-duration <time>` stops after elapsed time (`ms`, `s`, `m`, `h` or `d`, for example `8h`); `--claims <none\|git-ref>` claims issues across watchers (default `none`); `--verbose` or `-v` increases output detail. Opt-in capabilities: `--self-pull`, `--board`, `--board-project N` (default 1), `--monitor-teams`, `--monitor-email`, `--two-pass`, `--wave-dispatch`, `--retro`, `--decision-hygiene`. `--no-<capability>` overrides config. `--log-file <path>` tees timestamped output. A malformed `.squad/config.json` stops watch. Without `--execute`, scan/report mode is non-dispatching. |
| `config model` | Shows current model config, sets a default model, or pins one with `<model> --agent <name>`; `--clear` clears that default or, with `--agent <name>`, that agent's override. `config context-tier` has the same read/set/clear forms, using a supported tier. |
| `models` | Lists model-catalog refresh guidance; `models refresh` reconciles live API/docs sources with the seed and writes `.squad/.cache/models.json`. No command flags. |
| `notes promote` | Promotes/archives flagged state notes; `--ref <ref>` limits to one ref; `--all` scans all Squad notes refs (default); `--dry-run` previews. Requires `stateBackend: two-layer`. |
| `skill` | `publish [<skill-name>]`, `install <owner/repo>[/<skill-name>]` or direct skill URL, `list`; no further flags are documented. |
| `remote-control` | Alias for deprecated `rc`; accepts the same `--tunnel`, `--port <n>`, `--path <dir>` options. |
| `loop` | Runs a prompt-driven continuous work file. `--init` creates starter `loop.md`; `--file <path>` selects a file (default `loop.md`); `--interval <min>` overrides cycle spacing; `--timeout <min>` caps a cycle; `--copilot-flags "..."` passes CLI flags (without it, the loop passes `--yolo`); `--agent-cmd <cmd>` changes the agent command. Composable capabilities: `--self-pull`, `--monitor-email`, `--monitor-teams`, `--decision-hygiene`, `--retro`. File frontmatter requires `configured: true`; documented defaults are `interval: 10` minutes and `timeout: 30` minutes. |
| `cast` (`hire`) | With no flags, displays the project cast. With both `--name <name>` and `--role <role>`, adds an agent; `--force` permits replacing an existing charter. When `team.md` has no built-in support table, which is the case after `squad init`, the add also writes a `## Built-in Support Agents` table for every built-in whose charter is installed, so a project's first cast lists Scribe, Ralph, Rai and Fact Checker. |
| `copilot` | Configures GitHub Copilot coding agent. `--off` removes `@copilot`; `--auto-assign` configures assignment. |
| `plugin` | Squad plugin marketplaces (not the Squad plugin for Claude Code). Marketplace actions: `marketplace add <owner/repo>`, `remove <name>`, `list`, `browse <name>`. Lifecycle actions also include `validate <local-plugin-dir>`, `dry-run <local-plugin-dir>`, `install <local-plugin-dir> [--dry-run]`, `uninstall <plugin-id>`, `enable <plugin-id>`, `disable <plugin-id>`, `switch <role> <plugin-id>`, `list [--json]`/`list-json`, `verify <plugin-id>`, `refresh <plugin-id>`, and `run-lifecycle <plugin-id> <lifecycle-event>`. The help printer gives the marketplace catalog; the implementation defines the local-directory and `--dry-run` forms. |
| `export` | Writes portable JSON snapshot; `--out <path>` overrides default `squad-export.json`. |
| `import <file>` | Imports a snapshot; `--force` permits replacing existing content. |
| `scrub-emails [directory]` | Removes email addresses from Squad state. Default target is `.ai-team/` when present, otherwise `.squad/`. |
| `start` | Starts Copilot with remote access. `--tunnel` exposes via devtunnel; `--port <n>` chooses port (default `0`, auto-assigned); `--command <cmd>` selects command (default `copilot`); remaining Copilot flags are forwarded. Deprecated in favor of `gh copilot`. |
| `nap` | Archives and prunes `.squad/` state; it does not summarize. A history over 15 KB keeps its Core Context plus the last 5 `##` sections, or 3 with `--deep`. Logs older than 7 days are deleted, the decisions inbox is merged, and once `decisions.md` is over 20 KB its older entries move to `decisions-archive.md`. `--dry-run` previews only. |
| `memory` | Governed memory, the same store the `memory.*` MCP tools use; fails outside a squad. Operations: `classify`, `write`, `search`, `promote`, `delete`, `audit`, and `provider`. `write` accepts `--content`, `--class TRANSIENT\|LOCAL\|DECISION\|POLICY\|COPILOT_MEMORY\|FORBIDDEN` (case-insensitive), `--title`, `--author`, and `--load-guidance ALWAYS\|ON-DEMAND\|ARCHIVE\|NEVER`. `search --query <text>`; `promote <id> --class LOCAL\|DECISION\|POLICY\|COPILOT_MEMORY`; `delete <id>`; provider supports `--enable-host-injected-copilot-adapter` / `--disable-host-injected-copilot-adapter`, aliases `--enable-copilot` / `--disable-copilot`, `--default-host-injected-copilot-adapter`, `--require-approval true\|false`, and `--actor <name>`. `--provider copilot` and `--default-copilot` are explicitly unsupported. Diagnostics: `--log-level none\|error\|info\|debug` or `--verbose`/`-v`; default is `none`, overrideable by `SQUAD_MEMORY_LOG_LEVEL` or `.squad/config.json` `memory.logLevel`. |
| `state-mcp` | Runs the stdio MCP bridge exposing Squad runtime-state tools. MCP configs start it through the committed launcher, `node .squad/squad.mjs state-mcp`. `--experimental-backend` (or `SQUAD_EXPERIMENTAL_BACKEND=1`) also exposes the 11 experimental `squad_backend_*` conversation tools; `SQUAD_BACKEND_URL` alone does not enable them. |
| `lockout` | Records reviewer-lockout transitions in `.squad/governance/lockouts.json`: `reject <subject> --author <id> --reviewer <id> --reason "<text>" [--paths <glob,...>]`, `assign <subject> --successor <id>`, `submit <subject> --author <id>`, `approve <subject> --reviewer <id>`, `override <subject> --author <id> --by <authority> --reason "<text>"`, `status [subject] [--json]`. IDs are folder names under `.squad/agents/`. `--by` must be `user` or a name in `governance.authorities`. The record is evidence for people and hooks, not a write barrier. No detailed `--help`. |
| `hook` | `hook claude <SessionStart\|SubagentStart\|PreToolUse\|PostToolUse\|Stop> [--plugin]` runs the advisory Claude Code hooks: it reads the hook event JSON on stdin and prints advisory JSON. It never blocks; on any error it prints nothing and exits 0. Claude Code calls it, not you; the hooks are on only with `"claudeHooks": "advisory"`. Not listed in `squad --help`, and no detailed `--help`. |
| `dashboard` | `dashboard [start\|stop\|status]` serves a live page on 127.0.0.1 showing the coordinator and each member run of the newest Claude Code session in this directory. `--port <n>` (default: first free port from 4280), `--session <id>`, `--stream <file>` (reads `claude -p` stream-json logs; repeatable), `--detach`, `--open`, `--json`. One dashboard runs per directory; its state lives in `~/.squad/dashboards/` (or under `SQUAD_HOME`). `/squad:dashboard` in Claude Code does the same. |
| `doctor` | Checks required setup files, config validity, Copilot CLI reachability, the state bridge and launcher (flagging machine-specific launch commands), upstream state and history archives; exits non-zero on required-check failure. |
| `health` | Validates team, registry, routing, backend, and environment; `--json` produces CI-friendly output (schema `squad-health/v1`). Its `metadata` carries `cliVersion`, `sdkVersion`, `stateBackend`, `resolvedTeamRoot`, `resolvedSquadDir`, `bridgeVersion` and `launchMode`; `resolvedTeamDir` is kept for older consumers. No detailed `--help`. |
| `subsquads` | `list`, `status`, or `activate <name>`; aliases `workstreams` and deprecated `streams`. |
| `link <team-repo-path>` | Links the project to a remote team root. `init-remote <team-repo-path>` is a shorthand. |
| `externalize` | Moves `.squad/` state outside the working tree into platform-local storage; `--key <name>` explicitly sets the project key. Ownership is recorded in `.owner.json`, and externalize refuses a directory that belongs to another project. |
| `internalize` | Restores externalized state into the working tree. |
| `build` | Compiles `squad.config.ts` into Markdown. `--check` validates only; `--dry-run` previews; `--watch` rebuilds on file changes. |
| `aspire` | Launches Aspire observability dashboard. `--docker` forces Docker; `--port <n>` selects dashboard port. |
| `schedule` | `list`, `run <id>`, `init`, or `status` manage scheduled tasks. |
| `preset` | `list`, `show <name>`, `apply <name>`, `save <name>`, `install <source>`, or `init [--remote]`. `save` also accepts `--description "..."`; `--force` permits overwrites; `--name <override>` renames an installed preset/selects one from a collection. Sources can be GitHub HTTPS/SSH URLs or local paths. A `#name` fragment is a name hint; a slash fragment is a literal subpath. |
| `rc` | Remote Control bridge (deprecated; prefer `gh copilot`). `--tunnel` exposes a devtunnel, `--port <n>` chooses port, `--path <dir>` selects Squad path (default current directory). |
| `copilot-bridge` | Checks Copilot ACP stdio compatibility. |
| `rc-tunnel` | Checks devtunnel CLI availability. |
| `discover` | Lists known squads and capabilities. |
| `delegate <squad-name> <description>` | Creates work in another squad. |
| `registry` | `add <name> <path>`, `list`, or `remove <name>` maintain peer squads for discovery (not inheritance). |
| `upstream` | `add <source> [--name <n>] [--ref <branch>]`, `remove <name>`, `list`, `sync [name]`. Runtime inheritance reads only locally synced snapshots and never fetches, so run `sync` to materialize or refresh a Git source. Earlier entries in `.squad/upstream.json` take precedence. |
| `economy [on\|off]` | Toggles cost-conscious model selection. |
| `help` | Prints the command overview and usage. |

## Removed in 2.0

These commands and flags existed in Squad 1.x. The v2.0.0 CLI does not have them.

| Command or flag | What happens in 2.0 | What to do instead |
|---|---|---|
| `squad personal` (`init`, `list`, `add`, `remove`) | Removed with personal squads. | Keep agents in the project `.squad/`. |
| `squad consult` | Removed with consult mode. | None. Move anything you need into a project `.squad/` by hand. |
| `squad extract` | Removed with consult mode. | None. |
| `--global` (`init`, `upgrade`, and any other command) | Rejected with `Unknown option: --global`. | Run the command inside the project, or point at a team with `--team-root` or `SQUAD_TEAM_ROOT`. |
| User-profile squad fallback | `status`, `doctor`, `cast` and `cost` no longer find a squad in your user profile; outside a project they fail with `No squad in this directory`. | Run `squad init` in the project first. |

## Examples

```bash
# Set up a Markdown team without optional CI workflows
squad init --no-workflows

# Set up a team for GitHub Copilot and Claude Code (plugin mode)
squad init --client copilot,claude --claude-plugin

# Preview a format conversion before changing files
squad migrate --to sdk --dry-run

# Run one triage scan without dispatching agents
squad triage --interval 10

# Dispatch up to three issue tasks concurrently, with a 45-minute cap
squad triage --execute --max-concurrent 3 --timeout 45

# Run Ralph for a working day, then stop
squad watch --execute --max-duration 8h

# Start a continuous prompt loop from a named file
squad loop --file .squad/loop.md --interval 15

# Check readiness in a pipeline
squad health --json

# Validate an SDK configuration without writing generated Markdown
squad build --check

# Export and later restore a portable team snapshot
squad export --out ./team.json
squad import ./team.json
```

## Example invocations by operation

These are syntax examples, not a recommendation to run state-changing commands without reviewing the target. Commands such as `init`, `upgrade`, `client add`, `roster add`, `import`, `externalize`, `internalize`, `preset apply`, and `copilot` modify local or remote state.

```bash
squad init --sdk --state-backend local
squad init --client all
squad upgrade --dry-run
squad upgrade --self --dry-run
squad upgrade --client claude
squad client list --json
squad client add kiro,codex --dry-run
squad client sync
squad roster add all --dry-run
squad roster remove fact-checker
squad update-check --json
squad migrate --to markdown --dry-run
squad sync --push --remote origin
squad status
squad roles --category engineering
squad cost --agent scribe
squad triage --execute --max-concurrent 2
squad watch --execute --agent-preset claude --claims git-ref
squad loop --init
squad cast --name edie --role backend
squad copilot --auto-assign
squad plugin marketplace list
squad plugin install ./plugins/reviewer --dry-run
squad export --out ./squad-export.json
squad import ./squad-export.json --force
squad scrub-emails .squad
squad start --tunnel --port 3000 --yolo
squad nap --deep --dry-run
squad memory write --content "Prefer explicit API contracts" --class LOCAL
squad state-mcp
squad state-mcp --experimental-backend
squad lockout status --json
squad dashboard --detach --open
squad dashboard stop
squad doctor
squad health --json
squad subsquads list
squad link ../team-repository
squad externalize --key tasktrack
squad internalize
squad build --check
squad aspire --docker --port 18888
squad schedule list
squad schedule run nightly
squad preset list
squad preset install owner/repo#backend --name backend-team
squad preset apply backend-team --force
squad rc --port 3000
squad copilot-bridge
squad init-remote ../team-repository
squad rc-tunnel
squad discover
squad delegate docs-squad "Document the API contract"
squad registry add docs-squad ../docs-team
squad registry list
squad upstream add https://github.com/acme/shared-team.git --name shared --ref main
squad upstream list
squad economy on
squad version
squad config model --clear
squad models refresh
squad notes promote --all --dry-run
squad skill list
squad watch --health
squad remote-control --port 3000
squad help
```

The CLI entrypoint also dispatches `watch` (alias of `triage`), `remote-control` (alias of `rc`), `config`, `models`, `notes`, `skill` and `hook`; these are omitted from the top-level help printer but are real v2.0.0 commands. Additional examples for nested actions:

```bash
squad plugin marketplace add github/squad
squad plugin marketplace browse squad
squad schedule init
squad schedule status
squad preset save backend-team --description "Backend specialists"
squad preset init --remote
squad subsquads activate api
squad registry remove docs-squad
squad upstream sync shared
squad memory search --query "API validation strategy"
squad memory promote decision-42 --class DECISION
squad memory provider --enable-host-injected-copilot-adapter --require-approval true
squad lockout reject patch-status-null --author backend --reviewer lead --reason "Return 400 for status: null"
squad lockout assign patch-status-null --successor tester
squad config context-tier long_context --agent architect
squad models refresh
squad notes promote --ref squad/ralph --dry-run
squad skill publish reviewer
```

Nested operations include `squad plugin marketplace add <owner/repo>`, `remove <name>`, `list`, and `browse <name>`; local plugin lifecycle operations also accept `validate`, `dry-run`, `install [--dry-run]`, `uninstall`, `enable`, `disable`, `switch`, `list [--json]`, `verify`, `refresh`, and `run-lifecycle` with the positional operands shown in the command table. `squad client list [--json]`, `add <list> [--dry-run]`, and `sync [--dry-run]`; `squad roster add|remove <rai|fact-checker|all> [--dry-run]`; `squad lockout reject`, `assign`, `submit`, `approve`, `override`, and `status` with the flags in the command table; `squad dashboard start`, `stop`, and `status`; `squad schedule run <id>`, `init`, and `status`; `squad preset show <name>`, `apply <name> [--force]`, `save <name>`, `install <source> [--name <override>] [--force]`, and `init [--remote]`; `squad registry add <name> <path>`, `list`, `remove <name>`; `squad upstream add <source> [--name <n>] [--ref <branch>]`, `remove <name>`, `list`, `sync [name]`; and `squad subsquads status` or `activate <name>`.

## Help and version caveats

The command catalog and flag summary above were checked against `squad --help`, command-level help where it returns a synopsis, CLI dispatch in `packages/squad-cli/src/cli-entry.ts`, the help text in `packages/squad-cli/src/cli/core/command-help.ts`, and handlers under `packages/squad-cli/src/cli/commands`. Eight commands have no detailed help: `--help` on `health`, `hook`, `lockout`, `sync`, `models`, `notes` (including `notes promote`), `skill` and `registry` prints "No detailed help is available". The rows for those commands come from dispatch and their handlers; the `hook` and `lockout` forms above come from `packages/squad-cli/src/cli/commands/hook.ts`, `packages/squad-cli/src/cli/commands/lockout.ts` and the CHANGELOG; the `dashboard` options are in `packages/squad-cli/src/cli/commands/dashboard.ts`. Some commands intentionally show only a parent usage line for nested operations, so inspect their source handler before automating unusual combinations. `--help` is not a safety switch for operational actions on every leaf invocation; run it only after checking the parent command's supported syntax. The installed command itself reports 2.0.0.

`squad upgrade --self --dry-run` is a safe preview only on a 2.0 CLI (it first shipped in v2.0.0-preview.2). A 1.1.0 CLI does not pass `--dry-run` to the self-upgrade, so the same command installs the new CLI. When you upgrade from 1.1.0, run `squad upgrade --self` only when you mean it; Chapter 22 (Volume 2) walks through the migration.

The Claude Code plugin adds its own slash commands inside Claude Code (`/squad:cast`, `/squad:ralph`, `/squad:ceremony`, `/squad:status`, `/squad:dashboard`). `/squad:cast`, `/squad:status` and `/squad:dashboard` call the same CLI through the plugin's launcher. `/squad:ralph` and `/squad:ceremony` load a coordinator skill instead and run no CLI command of their own. Volume 2, Part IV covers them.

For the maintained web reference, see [Squad CLI reference](https://github.github.com/squad/docs/reference/cli/). The source of truth for this edition is tag v2.0.0; newer documentation may describe later capabilities.
