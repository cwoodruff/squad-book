# Appendix A: CLI Reference

The command inventory below targets the installed Squad v1.1.0 CLI. Use `squad --help` for the installed binary's synopsis and `squad <command> --help` for that command's version-specific detail. Most commands accept help at the command level; action-oriented commands such as `triage`, `loop`, and integrations can enter an interactive or long-running path when options are misplaced, so consult the syntax before executing them. Flags marked “none” have no command-specific options in the v1.1.0 help/source. Global options are listed separately.

## Global invocation

| Form | Effect |
|---|---|
| `squad` | Legacy interactive shell entry (deprecated in favor of `copilot --agent squad`); without arguments the installed CLI's help describes launching the shell. |
| `squad <command> [options]` | Run an operation. |
| `squad --help`, `squad -h` | Print command overview. |
| `squad --version`, `squad -v`, `squad version` | Print installed version. |

Global flags: `--global` selects the personal Squad path for commands that support it (notably `init` and `upgrade`); `--economy` requests economy-mode model selection for that session; `--team-root <path>` overrides team-root resolution. Global availability is parser-dependent: a command's own help is authoritative. The top-level CLI identifies itself as `squad v1.1.0`.

## Commands and options

| Command | Operands, options, defaults, and behavior |
|---|---|
| `init` | Creates the Markdown team plus default workflows. `--sdk` selects SDK-builder setup; `--roles` seeds built-in roles; `--global` uses the personal directory; `--no-workflows` skips workflow files; `--no-vscode-default` avoids changing `.vscode/settings.json`; `--preset <name>` applies a preset; `--state-backend <type>` accepts `local`, `orphan`, or `two-layer`. Remote form: `squad init --mode remote <team-repo-path>` writes a config pointer to an external team root. |
| `upgrade` | Updates Squad-owned prompt/template assets, not team state. `--dry-run` previews; `--global` targets the personal Squad; `--migrate-directory` renames legacy `.ai-team/`; `--state-backend <type>` migrates to `orphan` or `two-layer`; `--self` upgrades the CLI; `--insider` pairs with `--self` to select the insider tag; `--force` skips overwrite prompts. |
| `update-check` | Reports cached CLI update state. `--json` emits JSON; `--refresh` bypasses cache and queries the registry. Exit codes: `0` current/no cache, `1` update available, `2` refresh transport failure. |
| `migrate` | `--to sdk|markdown` converts squad format; `--from ai-team` migrates the legacy directory; `--dry-run` previews. |
| `sync` | Git-native state sync; `--push`, `--pull`, or both select direction; `--remote <name>` chooses remote; `--quiet` suppresses routine output. No automatic remote selection is implied by these flags. |
| `status` | Shows active Squad resolution and why. No command-specific flags. |
| `roles` | Lists built-in roles; `--category <name>` filters category and `--search <query>` searches. |
| `cost` | Reads orchestration usage logs; `--all` includes all available records; `--agent <name>` filters by agent. |
| `triage` / `watch` | Scans work. `watch` is a source-dispatched alias; `watch --health` prints watch-instance status. `--interval <minutes>` defaults to 10; `--execute` enables agent dispatch; `--copilot-flags "..."` passes extra Copilot CLI flags; `--max-concurrent N` defaults to 1; `--timeout N` defaults to 30 minutes per issue; `--verbose` or `-v` increases output detail. Opt-in capabilities: `--self-pull`, `--board`, `--board-project N` (default 1), `--monitor-teams`, `--monitor-email`, `--two-pass`, `--wave-dispatch`, `--retro`, `--decision-hygiene`. `--no-<capability>` overrides config. `--log-file <path>` tees timestamped output. `--health` prints watch status. Without `--execute`, scan/report mode is non-dispatching. |
| `config model` | Shows current model config, sets a default model, or pins one with `<model> --agent <name>`; `--clear` clears that default or, with `--agent <name>`, that agent's override. `config context-tier` has the same read/set/clear forms, using a supported tier. |
| `models` | Lists model-catalog refresh guidance; `models refresh` reconciles live API/docs sources with the seed and writes `.squad/.cache/models.json`. No command flags. |
| `notes promote` | Promotes/archives flagged state notes; `--ref <ref>` limits to one ref; `--all` scans all Squad notes refs (default); `--dry-run` previews; `--help`/`-h` prints help. Requires `stateBackend: two-layer`. |
| `skill` | `publish [<skill-name>]`, `install <owner/repo>[/<skill-name>]` or direct skill URL, `list`; no further flags are documented. |
| `remote-control` | Alias for deprecated `rc`; accepts the same `--tunnel`, `--port <n>`, `--path <dir>` options. |
| `loop` | Runs a prompt-driven continuous work file. `--init` creates starter `loop.md`; `--file <path>` selects a file (default `loop.md`); `--interval <min>` overrides cycle spacing; `--timeout <min>` caps a cycle; `--copilot-flags "..."` passes CLI flags; `--agent-cmd <cmd>` changes the agent command. Composable capabilities: `--self-pull`, `--monitor-email`, `--monitor-teams`, `--decision-hygiene`, `--retro`. File frontmatter requires `configured: true`; documented defaults are `interval: 10` minutes and `timeout: 30` minutes. |
| `cast` (`hire`) | Displays current project/personal cast; with both `--name <name>` and `--role <role>`, adds an agent. `--force` permits replacing an existing charter. |
| `copilot` | Configures GitHub Copilot coding agent. `--off` removes `@copilot`; `--auto-assign` configures assignment. |
| `plugin` | Marketplace actions: `marketplace add <owner/repo>`, `remove <name>`, `list`, `browse <name>`. Lifecycle actions also include `validate <local-plugin-dir>`, `dry-run <local-plugin-dir>`, `install <local-plugin-dir> [--dry-run]`, `uninstall <plugin-id>`, `enable <plugin-id>`, `disable <plugin-id>`, `switch <role> <plugin-id>`, `list [--json]`/`list-json`, `verify <plugin-id>`, `refresh <plugin-id>`, and `run-lifecycle <plugin-id> <lifecycle-event>`. The help printer gives the action catalog; the implementation defines the local-directory and `--dry-run` forms. |
| `export` | Writes portable JSON snapshot; `--out <path>` overrides default `squad-export.json`. |
| `import <file>` | Imports a snapshot; `--force` permits replacing existing content. |
| `scrub-emails [directory]` | Removes email addresses from Squad state. Default target is `.ai-team/` when present, otherwise `.squad/`. |
| `start` | Starts Copilot with remote access. `--tunnel` exposes via devtunnel; `--port <n>` chooses port (default `0`, auto-assigned); `--command <cmd>` selects command (default `copilot`); remaining Copilot flags are forwarded. Deprecated in favor of `gh copilot`. |
| `nap` | Compresses/prunes/archives state. `--deep` includes older history; `--dry-run` previews only. |
| `memory` | Operations: `classify`, `write`, `search`, `promote`, `delete`, `audit`, and `provider`. `write` accepts `--content`, `--class TRANSIENT|LOCAL|DECISION|POLICY|COPILOT_MEMORY|FORBIDDEN`, `--title`, `--author`, and `--load-guidance ALWAYS|ON-DEMAND|ARCHIVE|NEVER`. `search --query <text>`; `promote <id> --class LOCAL|DECISION|POLICY|COPILOT_MEMORY`; `delete <id>`; provider supports `--enable-host-injected-copilot-adapter` / `--disable-host-injected-copilot-adapter`, aliases `--enable-copilot` / `--disable-copilot`, `--default-host-injected-copilot-adapter`, `--require-approval true|false`, and `--actor <name>`. `--provider copilot` and `--default-copilot` are explicitly unsupported. Diagnostics: `--log-level none|error|info|debug` or `--verbose`/`-v`; default is `none`, overrideable by `SQUAD_MEMORY_LOG_LEVEL` or `.squad/config.json` `memory.logLevel`. |
| `state-mcp` | Runs the MCP bridge exposing Squad runtime-state tools. No user-facing flags in top-level synopsis. |
| `doctor` | Checks required setup files, config validity, and Copilot CLI reachability; exits non-zero on required-check failure. |
| `health` | Validates team, registry, routing, backend, and environment; `--json` produces CI-friendly output. |
| `consult` | Enters personal-Squad consult mode; `--status` displays session status; `--check` runs prerequisites. |
| `extract` | Extracts consult learnings. `--dry-run` previews; `--clean` removes transient files; `--yes` skips confirmation; `--accept-risks` acknowledges data-handling implications. |
| `subsquads` | `list`, `status`, or `activate <name>`; aliases `workstreams` and deprecated `streams`. |
| `link <team-repo-path>` | Links the project to a remote team root. `init-remote <team-repo-path>` is a shorthand. |
| `externalize` | Moves `.squad/` state outside the working tree into platform-local storage; `--key <name>` explicitly sets project key. |
| `internalize` | Restores externalized state into the working tree. |
| `build` | Compiles `squad.config.ts` into Markdown. `--check` validates only; `--dry-run` previews; `--watch` rebuilds on file changes. |
| `aspire` | Launches Aspire observability dashboard. `--docker` forces Docker; `--port <n>` selects dashboard port. |
| `schedule` | `list`, `run <id>`, `init`, or `status` manage scheduled tasks. |
| `personal` | `init`, `list`, `add <name> --role <role>`, or `remove <name>` manage ambient personal agents. `--role` is required when adding and names a built-in role. |
| `preset` | `list`, `show <name>`, `apply <name>`, `save <name>`, `install <source>`, or `init [--remote]`. `save` also accepts `--description "..."`; `--force` permits overwrites; `--name <override>` renames an installed preset/selects one from a collection. Sources can be GitHub HTTPS/SSH URLs or local paths. A `#name` fragment is a name hint; a slash fragment is a literal subpath. |
| `rc` | Remote Control bridge (deprecated; prefer `gh copilot`). `--tunnel` exposes a devtunnel, `--port <n>` chooses port, `--path <dir>` selects Squad path (default current directory). |
| `copilot-bridge` | Checks Copilot ACP stdio compatibility. |
| `rc-tunnel` | Checks devtunnel CLI availability. |
| `discover` | Lists known squads and capabilities. |
| `delegate <squad-name> <description>` | Creates work in another squad. |
| `registry` | `add <name> <path>`, `list`, or `remove <name>` maintain peer squads for discovery (not inheritance). |
| `upstream` | `add <source> [--name <n>] [--ref <branch>]`, `remove <name>`, `list`, `sync [name]`. |
| `economy [on|off]` | Toggles cost-conscious model selection. |
| `help` | Prints the command overview and usage. |

## Examples

```bash
# Set up a Markdown team without optional CI workflows
squad init --no-workflows

# Preview a format conversion before changing files
squad migrate --to sdk --dry-run

# Run one triage scan without dispatching agents
squad triage --interval 10

# Dispatch up to three issue tasks concurrently, with a 45-minute cap
squad triage --execute --max-concurrent 3 --timeout 45

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

These are syntax examples, not a recommendation to run state-changing commands without reviewing the target. Commands such as `init`, `upgrade`, `import`, `externalize`, `internalize`, `preset apply`, and `copilot` modify local or remote state.

```bash
squad init --sdk --state-backend local
squad upgrade --dry-run
squad update-check --json
squad migrate --to markdown --dry-run
squad sync --push --remote origin
squad status
squad roles --category engineering
squad cost --agent scribe
squad triage --execute --max-concurrent 2
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
squad doctor
squad health --json
squad consult --check
squad extract --dry-run
squad subsquads list
squad link ../team-repository
squad externalize --key tasktrack
squad internalize
squad build --check
squad aspire --docker --port 18888
squad schedule list
squad schedule run nightly
squad personal list
squad personal add reviewer --role reviewer
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

The CLI entrypoint also dispatches `watch` (alias of `triage`), `remote-control` (alias of `rc`), `config`, `models`, `notes`, and `skill`; these are omitted from the top-level help printer but are real v1.1.0 commands. Additional examples for nested actions:

```bash
squad plugin marketplace add bradygaster/squad
squad plugin marketplace browse squad
squad schedule init
squad schedule status
squad personal add tester --role tester
squad preset save backend-team --description "Backend specialists"
squad preset init --remote
squad subsquads activate api
squad registry remove docs-squad
squad upstream sync shared
squad memory search --query "API validation strategy"
squad memory promote decision-42 --class DECISION
squad memory provider --enable-host-injected-copilot-adapter --require-approval true
squad config context-tier long_context --agent architect
squad models refresh
squad notes promote --ref squad/ralph --dry-run
squad skill publish reviewer
```

Nested operations include `squad plugin marketplace add <owner/repo>`, `remove <name>`, `list`, and `browse <name>`; local plugin lifecycle operations also accept `validate`, `dry-run`, `install [--dry-run]`, `uninstall`, `enable`, `disable`, `switch`, `list [--json]`, `verify`, `refresh`, and `run-lifecycle` with the positional operands shown in the command table. `squad schedule run <id>`, `init`, and `status`; `squad personal init`, `add <name> [--role <role>]`, `remove <name>`, and `list`; `squad preset show <name>`, `apply <name> [--force]`, `save <name>`, `install <source> [--name <override>] [--force]`, and `init [--remote]`; `squad registry add <name> <path>`, `list`, `remove <name>`; `squad upstream add <source> [--name <n>] [--ref <branch>]`, `remove <name>`, `list`, `sync [name]`; and `squad subsquads status` or `activate <name>`.

## Help and version caveats

The command catalog and flag summary above were checked against `squad --help`, command-level help where it returns a synopsis, CLI dispatch in `packages/squad-cli/src/cli-entry.ts`, and handlers under `packages/squad-cli/src/cli/commands`. Some commands intentionally show only a parent usage line for nested operations, so inspect their source handler before automating unusual combinations. `--help` is not a safety switch for operational actions on every leaf invocation; run it only after checking the parent command's supported syntax. The installed command itself reports v1.1.0.

For the maintained web reference, see [Squad CLI reference](https://bradygaster.github.io/squad/docs/reference/cli/). The source of truth for this edition is tag v1.1.0; newer documentation may describe later capabilities.

## Squad 2.0 (Preview) — Command Changes

> **Preview:** This reference describes Squad `v2.0.0-preview.2` from the npm `insider` channel. The `latest` channel remains on v1.1.0; commands and behavior may change before 2.0.0 is stable.

The v1.1.0 command reference above remains valid only for that release. The following table records the preview's additions and behavior changes; it is not a replacement for the stable command inventory.

| Command or flag | 2.0 preview status | What it does / migration note |
|---|---|---|
| `squad init --client <list>` | New option | Initializes the project and projects one or more host integrations. `<list>` accepts comma-separated host slugs or `all`: `copilot`, `claude`, `kiro`, `opencode`, `cursor`, `codex`, and `antigravity`. Without this option, initialization remains Copilot-only. |
| `squad upgrade --client <list>` | New option | Adds and refreshes the selected host projections while upgrading managed Squad files. The portable client list is recorded in `.squad/config.json`; existing configured hosts are refreshed by upgrade. |
| `squad upgrade --dry-run` | Changed behavior | Reports the exact files that would change and writes nothing. It also previews `--self` package installation without installing. |
| `squad upgrade --self` | Changed behavior | Upgrades the CLI using its installed channel: prerelease installs follow `@insider`, stable installs follow `@latest`. Add `--insider` to force the insider channel. |
| `squad upgrade --self --insider` | New/clarified channel option | Selects the `insider` distribution tag; `preview` remains a compatibility alias. `latest` continues to point to v1.1.0 until the stable 2.0 release. |
| `squad upgrade --self --force` | Changed behavior | Permits installing an older CLI version (a downgrade); without `--force`, downgrade attempts are refused. For ordinary project upgrades, `--force` re-processes files even when they are already current. |
| `squad client list [--json]` (`client ls` also accepted) | New command | Lists configured hosts and reports whether their expected projection files exist. Empty `clients[]` means the default Copilot host only. `--json` emits a structured report. |
| `squad client add <list> [--dry-run]` (also `squad clients`) | New command | Projects and records additional host slugs; `--dry-run` shows the proposed operation without writing. `squad upgrade --client <list>` is the equivalent upgrade workflow. |
| `squad roster add <role> [--dry-run]` (role: `rai`, `fact-checker`, or `all`) | New command | Explicitly opts optional built-in roles into `.squad/team.md`; shows the exact diff and records provenance/backup information. Upgrade no longer edits the roster automatically. |
| `squad roster remove <role> [--dry-run]` (role: `rai`, `fact-checker`, or `all`) | New command | Removes only roster rows previously added by `squad roster add`. `disable` and `uninstall` are aliases for `remove`; `--dry-run` previews the diff. |
| `squad state-mcp --experimental-backend` | New option | In addition to the ordinary state tools, exposes the 11 experimental `squad_backend_*` conversation/event tools. The same opt-in is available with `SQUAD_EXPERIMENTAL_BACKEND=1`; `SQUAD_BACKEND_URL` alone does not enable them. |
| `squad upstream add`, `remove`, `list`, or `sync` | Changed runtime behavior | Existing subcommands remain. Runtime inheritance reads locally synced snapshots only—session start does not fetch. Run `squad upstream sync` to materialize or refresh a Git source; earlier entries in `.squad/upstream.json` take precedence. |
| `squad cast` (no arguments) | Changed behavior | Displays the project cast only. Personal agents are no longer merged into a session. Use `squad roster add` to opt in to optional built-ins. |
| `squad status` | Changed behavior | Reports the resolved project squad and inherited upstreams; it no longer reports a personal/global squad fallback. |
| `squad status`, `doctor`, `cast`, and `cost` outside a project | Changed behavior | These project-state commands no longer resolve a user-profile squad; without a `.squad/` in the current directory or a parent, they fail with `No squad in this directory`. Initialize the project first. |
| `squad personal`, `squad consult`, `squad extract` | Removed | Personal Squad management, consult mode, and consult-session extraction are not available in 2.0. Move any retained information into a project `.squad/` by hand. |
| `--global` on `squad init` or `squad upgrade` | Removed | Teams are project-scoped. The preview rejects this option instead of reading or writing user-profile squad state. Run the command inside the project. |

For the full seven-host command syntax, see Chapters 19–22 (Volume 2). In particular, the `state-mcp` experimental tools are transcript/event-log infrastructure and do not bundle an execution harness.
