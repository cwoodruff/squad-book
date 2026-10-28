# Chapter 22: Upgrading to Squad 2.0 and the Road Ahead

> **Prerequisites:** Volume 1 (or equivalent Squad experience); Chapters 18–21.

> **Preview:** This chapter describes Squad `v2.0.0-preview.2` from the npm `insider` channel. The `preview` tag is an alias for that channel; `latest` remains Squad 1.1.0. Preview behavior, commands, and generated files may change before 2.0.0 is stable.

## What You'll Learn

- Distinguish upgrading the globally installed CLI from upgrading one repository, and choose a release channel without accidentally downgrading.
- Preview and apply a content-aware project upgrade while preserving team state and verifying backups.
- Understand casting repair, roster backfill, and the evidence Squad requires before it will reconstruct agent identity.
- Migrate removed personal or global squad knowledge by hand, while keeping project resolution explicit.
- Recognize the 2.0 CLI, configuration, integration, and release-process changes, and safely plan a rollback to 1.1.0.
- Separate shipped 2.0 behavior from proposals that describe possible future skills and memory governance.

## Two Upgrades, Three Channels

“Upgrade Squad” can mean two distinct operations. A **self-upgrade** replaces the CLI package installed for your user. A **project upgrade** refreshes Squad-managed files in one repository. Installing a new executable does not rewrite any project; running `squad upgrade` in a project does not replace the executable. That separation is intentional: you can update the tool once, then review and upgrade repositories one at a time.

The preview release is deliberately not on the stable channel. At `v2.0.0-preview.2`, `latest` still resolves to 1.1.0. Both `insider` and `preview` resolve to the preview package pair, with `insider` the canonical channel and `preview` a compatibility alias. The release process has no separate `preview` branch. A preview is published from a reviewed commit on `dev`, and its exact commit is part of the release evidence.

| Channel | npm tag | Intended use | What it means at this preview |
|---|---|---|---|
| Stable | `latest` | Routine production use | Squad 1.1.0; it is not Squad 2.0 yet. |
| Insider | `insider` | Testing the preview or contributing to Squad | Canonical 2.0 preview channel; prerelease builds follow this tag. |
| Preview alias | `preview` | Compatibility with preview install instructions | Alias of `insider`, not an independent release line. |

Install an exact preview when reproducibility matters:

```bash
npm install -g @bradygaster/squad-cli@2.0.0-preview.2
squad --version
```

Or follow the moving insider channel:

```bash
npm install -g @bradygaster/squad-cli@insider
```

`squad upgrade --self` is the CLI's in-place self-upgrade path. A stable installation follows `@latest`; a prerelease installation follows `@insider`, unless you explicitly add `--insider`. The npm `preview` alias works for installation, but Squad's self-upgrade resolves prereleases through the canonical `insider` tag.

> **Source discrepancy:** The generic migration guide includes an `@latest` install example for 2.0. At the `2.0.0-preview.2` snapshot, `latest` still selects 1.1.0; verify the live tag or use the exact preview version rather than copying that example.

```bash
# Preview the exact install command first
squad upgrade --self --insider --dry-run

# Apply after reviewing the package manager and target version
squad upgrade --self --insider
```

The dry run performs a read-only lookup of the npm dist-tag so the output can show its target; it does not execute the package-manager install command or change the global package. If the registry cannot be reached, the CLI reports that it cannot confirm the target. For a normal self-upgrade, Squad detects npm, pnpm, or Yarn from the invoking environment, then runs the matching global-install command for `@bradygaster/squad-cli`.

Squad compares the resolved target version with the running version. If `@latest` points to a version older than the installed preview, the self-upgrade refuses to downgrade. `--force` bypasses that guard, so use it only when you have deliberately chosen an older CLI and have already restored a compatible project state. `--insider` also provides the suggested route when a preview user accidentally targets stable. The ordinary `--force` behavior for project upgrades is different: it reprocesses a repository that is already stamped as current.

> **Warning:** The old `self-upgrade` page described automatically upgrading repository templates after replacing the CLI. Squad 2.0 does not do that. On success, the self-upgrade asks you to restart the terminal and returns. Run the separate project-upgrade command from each repository you intend to change.

## A Safe, Content-Aware Project Upgrade

Before a major upgrade, get a clean baseline. Commit or stash all work, record `squad --version`, and create a branch. Make a separate private backup of `.squad/` and any important coordinator customization; a casting archive and local backups can contain private team context. Once the new CLI is installed, preview the project operation from the repository root:

```bash
squad upgrade --dry-run
```

The preview reports content changes: files it would create or overwrite, which customized files would first receive a `.local-backup`, obsolete shipped files that can be removed, files it would leave because they were customized, ignore-file additions, and applicable casting repairs. It also plans client projections if `--client` is supplied. The preview does not apply the project writes or create casting archives, locks, or transaction files.

There is one important boundary to that guarantee: the CLI processes `--migrate-directory` before reaching the project dry-run handler. Do not combine `--dry-run` with `--migrate-directory` and assume the legacy directory rename is simulated. The self-upgrade dry run is separate; it only previews the install command. For the safest first inspection, run `squad upgrade --dry-run` alone.

After reviewing the preview, apply the upgrade:

```bash
squad upgrade
squad doctor
squad status
```

Squad 2.0 compares managed content rather than blindly copying a whole `.squad/` tree. It normalizes line endings before comparison, and uses the shipped-content manifest (or, for older installs without one, the prior shipped snapshot where available) to distinguish a user edit from a template change. Files matching the last version Squad shipped can be refreshed without a backup. A file that differs from both its shipped version and the new template is treated as customized.

Before replacing a customized managed file, Squad writes `<file>.local-backup`, reads it back, and checks that its bytes match the original. If that verification fails, it leaves that particular file untouched and reports the failure. The backup has a fixed path, not a history of versions: move a backup you need before a later upgrade can replace it. Backups are not automatically ignored by Git, so include them in your diff review and decide whether to retain or remove them.

The managed-file plan covers the coordinator, shipped skills, managed workflows, flat casting-template copies, and `.squad/templates/` snapshots. Ignore and attributes files receive only missing Squad-managed lines; existing lines and line-ending style are preserved. Files retired from the shipped set are removed only when their current content still matches the recorded shipped hash. Customized retired files are kept and reported. This makes a second upgrade with no intervening edits a no-op rather than a new wave of backups.

The project upgrade does **not** regenerate your team from scratch. It preserves `team.md`, routing, decisions, agent charters and histories, and the casting registry/history pair unless a supported casting migration is needed. It keeps existing user configuration fields and updates the portable `clients` list when you request client projections. It may add or refresh Squad-owned templates and scaffolding, and it can remove obsolete generated files when their prior content is provably unchanged. The working-tree diff—not the success message—is your record of what changed.

### Safe Upgrade Sequence

The commands operate in two distinct scopes: the first updates the installed CLI, and the second updates a project. Dry runs preview their respective operation without performing the installation or project writes.

```mermaid
sequenceDiagram
    actor You
    participant CLI as Squad CLI
    participant Registry as npm registry
    participant Project as Project .squad
    You->>CLI: squad upgrade --self --insider --dry-run
    CLI->>Registry: Read channel version metadata
    Registry-->>CLI: Insider target version
    CLI-->>You: Show command without installing
    You->>CLI: squad upgrade --self --insider
    CLI->>Registry: Install selected CLI version
    CLI-->>You: Confirm self-upgrade
    You->>CLI: squad upgrade --dry-run
    CLI->>Project: Inspect managed files and casting state
    Project-->>CLI: Current content and versions
    CLI-->>You: Report planned changes and backups
    You->>CLI: squad upgrade --client claude
    CLI->>Project: Verify backups, then update project files
    CLI-->>You: Report completed project upgrade
```

## Upgrading to Squad 2.0

Existing Copilot-only teams can upgrade without reinitializing. A plain `squad upgrade` remains Copilot-only; it will not silently create Claude Code, Kiro, OpenCode, Cursor, Codex, or Antigravity files. To add a host, preview and apply it explicitly:

```bash
squad upgrade --dry-run --client claude
squad upgrade --client claude
squad client list
```

You can name multiple hosts separated by commas, or use `all`. The selected host IDs are saved in `.squad/config.json` under `clients[]`; future project upgrades refresh the saved projections. These values are portable host identifiers, not credentials, paths, URLs, or session IDs. See Chapter 19 for host-specific setup and Chapter 20 for the adapter and capability model. Generating a projection does not grant access to that host: you still need the host's supported installation and account or license to run it. If you have only Copilot, leave the project Copilot-only and complete the rest of the upgrade and validation steps.

The standalone `squad client` command lists configured hosts and can add more without re-running all project setup. `squad client list --json` is useful for tooling; `squad client add <list> --dry-run` previews a projection. The SDK's `uninstallClients()` can remove projections and restore shared files byte-for-byte outside their managed sections. It is an **uninstall of generated host projections only**—it does not downgrade Squad or change your project state.

### Tested upgrade paths

The 2.0 upgrading guide includes a version-by-state-shape matrix for published producers from 0.9.1 through 1.1.0, plus an upgrade of a project initialized by the current tree. The fixtures vary ordinary project state, legacy casting, the old `.ai-team/` directory, profile-shaped state, and backend settings. The matrix exercises Linux and Windows and checks more than exit codes: it checks that user files and state-backend references survive, that casting pairs remain readable, that a second upgrade is idempotent, that new client projections parse, that `doctor` passes, and that projection uninstall restores shared content.

Some rows are marked not applicable because those earlier CLIs could not create the state under test—for example, an upstream configuration cannot be produced by a pre-upstream release. “Not applicable” is not a failed or skipped run. The matrix also documents an important historical warning: Squad 0.9.1's `squad upgrade --dry-run` is not a safe downgrade probe. Against a newer project it can write old templates despite the flag. Later 0.13.x–1.1.0 dry runs do not write, but their real upgrade still has no newer-workspace guard. Never run an old CLI's project-upgrade command against a 2.0 workspace.

The guide's own matrix has a version-label inconsistency: its run rows name target `v1.2.0-preview.1`, while its current instructions describe 2.0.0-preview.2. Treat the recorded rows as evidence for the producer/state-shape scenarios they state, not as proof that the matrix itself ran against this exact preview tag. For a release-critical migration, reproduce the test on a copy with the exact CLI package and OS you plan to use.

## Casting Repair: Preserve Evidence, Do Not Guess

Some 1.x teams have a registry written by a model in an informal JSON shape, or an empty registry even though `team.md` and agent folders are populated. Squad 2.0 repairs these cases before it refreshes managed project files. This is a conservative data migration, not a recasting operation: the CLI only fills in facts it can establish from the existing files.

For a handwritten registry, Squad reads the registry/history/commit-manifest set under the casting writer lock, recovers any durable transaction already in progress, and snapshots the pre-repair bytes. It normalizes supported records into the managed provenance schema. Complete valid records remain intact, including extra producer-specific fields and lifecycle state such as `inactive` or `retired`; incomplete but recoverable records get only missing fields supplied. The managed registry revision advances. The original registry, history, and manifest files are archived under a content-addressed directory such as:

```text
.squad/casting/handwritten-archive-<sha256>/
```

An existing archive is not replaced with different bytes. The repair validates the new pair, writes it through the casting transaction mechanism, and reads it back. If a failure occurs before the transaction journal is durable, the pre-repair snapshot is restored. Once a durable journal exists, recovery rolls that transaction forward; the tool does not silently discard it and invent a fresh cast. Do not edit the registry/history pair while this repair is in progress.

If a record is ambiguous or invalid, repair fails closed. The result includes a `dropped` list naming every entry that could not be normalized and why. “Dropped” here describes a rejected candidate in a proposed repair; it does not mean Squad committed a partial registry and discarded the entry. No partial normalized registry is written. Correct the source JSON so every entry proves a name and role (or use the suggested `squad cast --name <Name> --role <Role>` operation), preview again, and preserve the original archive. Bare strings are ambiguous because the program cannot know whether they mean role-to-name or name-to-role.

The second path backfills an **empty** registry from the current `team.md` roster. It is eligible only when the registry has no agents and no meaningful prior cast history. Each specialist must map to a real folder under `.squad/agents/`: the roster's charter path is preferred, then a matching `## Identity` name in a charter, then a literal normalized folder name. If a name maps to multiple folders, a folder is missing, or two roster rows claim the same folder, the backfill refuses. The roster must also declare the casting universe; Squad will not infer it from today's agent names. Built-in and human rows are not converted into specialist records.

You may encounter the failure in the dry-run. Use its per-entry `dropped` reasons as a checklist: restore the original charter or roster path, resolve duplicate names, or add the documented universe. Do not “fix” the preview by hand-inserting guessed IDs or a fabricated usage history. If the relevant historical files are missing, retain the old project and seek recovery from version control rather than claiming that migration succeeded.

This backfill is distinct from optional built-in roster management. `squad upgrade` can install Rai and Fact Checker charters but does not insert them into an existing team's `team.md`. Explicitly opt them in with `squad roster add rai`, `squad roster add fact-checker`, or `squad roster add all`. The command previews the exact diff, verifies a byte-exact `team.md.roster-backup`, and records ownership in `.squad/.roster-provenance.json`. A later `remove` deletes only the exact rows it can prove this command inserted; when the whole file is unchanged, it can restore the original bytes. This is a separate consent boundary from casting repair.

```mermaid
flowchart TD
  A["squad upgrade --dry-run"] --> B{"Casting pair readable?"}
  B -->|"yes"| C["Keep pair; preview managed-file plan"]
  B -->|"no: handwritten registry"| D["Normalize records in memory"]
  D --> E{"Every record provable?"}
  E -->|"no"| F["Fail closed; show dropped list; write nothing"]
  E -->|"yes"| G["Validate pair; show archive and repair plan"]
  B -->|"empty registry"| H["Resolve team.md rows to charter folders"]
  H --> I{"Universe and every ID provable?"}
  I -->|"no"| F
  I -->|"yes"| G
  C --> J["Review dry-run output"]
  G --> J
  J --> K["Apply on branch; inspect archive and diff"]
```

## Compatibility: Charters and Routing

2.0 can read a 1.x charter without forcing you to rewrite every charter before using the squad. Health validation recognizes older responsibility headings, and a missing 2.0 `## Identity` block is a warning with a suggested `Name` and `Role`, not an immediate failure. If a charter does include an identity, its name must agree with the persistent name recorded in casting; a mismatch is a validation failure. The optional `## Examples` charter section is now recognized as a supported section and survives structured SDK edits. You can add useful examples, but they are Markdown guidance—not executable test configuration—and they are not required for a valid charter.

Routing files have a similar compatibility layer. The parser accepts documented historical header names and column arrangements, as well as a recognized flattened legacy table. The optional Examples column can clarify work types. Compatibility does not mean accepting a broken route. `squad health` fails closed if it finds no parseable routing rules, cannot validate targets because the casting registry is invalid, or finds a route to an unknown/off-roster agent. Duplicate or conflicting work-type rows are reported deterministically as warnings so that you can resolve ambiguity instead of relying on whichever row happens to win. A legacy table can parse successfully and still fail health because it names a nonexistent agent.

Keep the distinction between diagnostics straight: `squad doctor` checks that `routing.md` exists and that the casting registry/history pair is consistent; `squad health` performs the stronger routing-reference validation intended for a CI gate. Run both after the upgrade. `squad migrate --to sdk` is a different tool for converting between markdown-only and SDK-First configuration; `squad migrate --from ai-team` renames a legacy `.ai-team/` directory. Neither command migrates personal squads or consult mode.

## Removed Personal Squads and Project Resolution

Squad 2.0 removed personal squads, consult mode, and the old global-squad option. The user-profile `personal-squad/` and global `.squad/` directories are no longer read or written. There is no conversion command that discovers these directories and moves their content into repositories. `squad init --global` is rejected as an unknown option. A project may no longer fall back to a personal team just because it has no `.squad/` locally.

Instead, 2.0 resolves project state from `.squad/` in the current directory or its parents. Outside a project, state commands such as `squad status`, `squad doctor`, `squad cast`, and `squad cost` report that no squad was found and tell you to initialize one. The retired features' command surfaces, environment switches, coordinator instructions, and SDK exports have been removed along with the feature; there is no supported consult-mode compatibility flag.

If a personal team contains knowledge you need, migrate the **content**, not the old profile directory. In each repository that should own it, start from a branch and create the project squad with `squad init`. Then review and copy selected agent charter/history folders, durable decisions, routing rules, skills, ceremonies, and policy into that repository's `.squad/`. Reconcile duplicate agent IDs and names against the project's current `team.md`; keep only decisions and histories appropriate to that codebase. Do not copy credentials, caches, tokens, unrelated repositories' notes, or the old global configuration wholesale. Have the team review the result, run `squad doctor` and `squad health`, and commit the project-owned state. Repeat for each project that needs the knowledge. A shared fact can be copied selectively or published through the project's normal upstream process; the removed personal squad is not a shared remote source.

The removal of profile fallback does **not** abolish all explicit linked-team workflows. `squad init --mode remote <path>` and `squad link <team-repo-path>` still support a project that intentionally uses a separate team root. The global `--team-root <path>` flag (also exposed to subprocesses as `SQUAD_TEAM_ROOT`) overrides the root used for resolution. Use it deliberately—for example, when a spawned command's working directory differs from the project root—not as a hidden replacement for the removed user-profile default. A pre-2.0 `teamRoot` pointing to an obsolete platform profile is removed during upgrade; a legitimate team root pointing to another repository is retained.

## Upstream Inheritance: Recheck Precedence

Upstreams are a 2.0 feature and are declared in `.squad/upstream.json`. The changed behavior matters even if you have already configured them: precedence now favors **earlier** entries. The old 1.x documentation said later entries won, while the implementation did not consistently realize that rule. In 2.0 the intended deterministic order is the project's own `.squad/` first, then upstreams in declaration order, traversed depth-first within the documented depth limit. If two upstreams provide the same item, the earlier one wins.

After installing 2.0, review the ordering in `upstream.json`; if you used the old documented later-wins behavior, reorder the list so your preferred source appears first. Then run:

```bash
squad upstream list
squad upstream sync
squad doctor
squad status
```

Sync refreshes the local snapshots from configured sources. Sessions read those local snapshots at startup; they do not fetch remote Git repositories on every prompt. `squad doctor` can report a fresh clone's upstream as unavailable until you sync. That normal unavailable state is a warning; missing, invalid, cyclic, or over-depth declarations are hard failures. This is also why a cleanly upgraded repo still needs an explicit `upstream sync` before you expect new upstream content to be visible.

## CLI Reference: What Changed in 2.0

The preview CLI has more commands than the older reference page's “17 commands” heading suggests. The table below lists the 2.0 surfaces most relevant to upgrading; the inventory afterward groups the full top-level command list and its important flags. Commands not mentioned as changed retain their ordinary project behavior.

| Surface | 1.1.0 → 2.0 preview change | Flags / usage to know |
|---|---|---|
| `squad init` | Adds client projection and continues to initialize project-local `.squad/`; personal/global initialization is gone. | `--client <list>`; `--sdk`, `--roles`, `--no-workflows`, `--no-vscode-default`, `--preset <name>`, `--state-backend <type>`, `--mode remote <path>`. |
| `squad upgrade` | Now plans and compares shipped content; project state is preserved, backups are verified, and configured hosts can be refreshed. | `--dry-run`, `--client <list>`, `--force`, `--migrate-directory`, `--state-backend <type>`. |
| `squad upgrade --self` | Self-upgrade follows current stable/prerelease channel, refuses older targets by default, and no longer auto-runs project upgrade. | `--self`, `--insider`, `--dry-run`, `--force`; use project `squad upgrade` separately. |
| `squad client` | New projection management command. | `client list [--json]`; `client add <list> [--dry-run]`. |
| `squad roster` | New explicit opt-in/removal path for optional built-ins; upgrades no longer modify the roster. | `roster add|remove <rai|fact-checker|all> [--dry-run]`; `disable` and `uninstall` alias `remove`. |
| `squad update-check` | New cache-aware status command for scripts and editors. | `--json`, `--refresh`; cache older than 24 hours is marked stale, and stale data cannot claim an update. Exit codes: `0` current/no cache, `1` update available, `2` refresh transport failure. |
| `squad health` | New CI-oriented validation, including routing targets; not the same as the file-presence checks in `doctor`. | `--json`. |
| `squad migrate` | Supports `--from ai-team` and `--to sdk|markdown`; this migrates file/config formats, not personal squads. | `--from ai-team`, `--to sdk|markdown`, `--dry-run`. |
| `squad state-mcp` | Adds opt-in experimental backend conversation tools; `SQUAD_BACKEND_URL` alone does not enable them. | `--experimental-backend` or `SQUAD_EXPERIMENTAL_BACKEND=1`; experimental server calls require configured backend details. |
| `squad upstream` | New runtime inheritance commands; 2.0 applies earlier-wins order and reads locally synced snapshots. | `upstream add <source> [--name <n>] [--ref <branch>]`, `remove <name>`, `list`, `sync [name]`. |
| `squad status` / `doctor` | Project-only resolution; profile fallback is removed. `status` reports resolution/upstreams; `doctor` checks state and bridge readiness. | `--team-root <path>` is an explicit root override, not a return of personal squads. |
| `squad cast` / `hire` | Project cast operations remain; `cast --name` / `--role` can explicitly add an agent and repair guidance can point to it. | `cast [--name <name> --role <role>] [--force]`; `hire` aliases cast. |
| `squad shell` / default invocation | The old consult mode is removed. The no-argument shell entry is still distinct from consult; use the documented host invocation to launch a coordinator. | No `--consult` or profile-mode compatibility flag. |
| `squad export` / `import` | Portable project state workflows remain, but they are not automatic personal-squad migration. | `export [--out <path>]`; `import <file> [--force]`. |
| `--global` | Removed; invoking it fails instead of writing to a profile location. | No replacement flag. Initialize inside a project; copy selected content by hand. |
| `--team-root` | Retained as an explicit global resolution override. | `squad --team-root <path> <command>` or environment `SQUAD_TEAM_ROOT`; use only when resolution needs an explicit project/team root. |
| `@bradygaster/squad-sdk/clients` | Deprecated SDK subpath alias; canonical APIs moved to the singular package subpath. | Change imports to `@bradygaster/squad-sdk/client`. |

### Full top-level command inventory

| Command | Main purpose and key flags / forms |
|---|---|
| No arguments | Launch the interactive shell. Consult mode itself is removed. |
| `init` | Initialize project; options shown in the preceding table. |
| `upgrade` | Upgrade project or CLI; options shown in the preceding table. |
| `client` | `list [--json]`; `add <list> [--dry-run]`. |
| `roster` | `add|remove <rai|fact-checker|all> [--dry-run]`. |
| `update-check` | `--json`, `--refresh`. |
| `migrate` | `--from ai-team`, `--to sdk|markdown`, `--dry-run`. |
| `sync` | Synchronize state backend: `--push`, `--pull`, `--remote <name>`, `--quiet`. |
| `status` | Show the active squad and why it resolved. |
| `roles` | List built-in roles: `--category <name>`, `--search <query>`. |
| `cost` | Report orchestration token usage: `--all`, `--agent <name>`. |
| `triage` | Scan/categorize work: `--interval <minutes>`, `--execute`, `--copilot-flags`, `--max-concurrent`, `--timeout`, plus capabilities such as `--self-pull`, `--board`, `--monitor-teams`, `--monitor-email`, `--two-pass`, `--wave-dispatch`, `--retro`, `--decision-hygiene`, and `--no-<capability>`. |
| `watch` | Triage alias / work monitor with the same monitoring and execution capabilities. |
| `loop` | Prompt-driven loop: `--init`, `--file <path>`, `--interval`, `--timeout`, `--copilot-flags`, `--monitor-email`, `--monitor-teams`, `--self-pull`. |
| `cast` / `hire` | Show or add a cast member: `--name`, `--role`, `--force`. |
| `copilot` | Add/remove coding agent: `--off`, `--auto-assign`. |
| `plugin` | `marketplace add|remove|list|browse`. |
| `export` / `import` | Export to JSON (`--out <path>`) or import `<file> [--force]`. |
| `scrub-emails` | Scrub state at an optional `[directory]`; default is `.squad/`. |
| `start` | Start Copilot with optional `--tunnel`, `--port <n>`, `--command <cmd>` and passthrough Copilot flags. |
| `nap` | Context cleanup: `--deep`, `--dry-run`. |
| `memory` | Governed memory operations, including `write --content "..." --class LOCAL`; diagnostics accept `--log-level` / `--verbose`. |
| `state-mcp` | Serve runtime MCP tools; `--experimental-backend` is opt-in. |
| `doctor` / `health` | Diagnose setup, or run structured CI checks (`health --json`). |
| `subsquads` | `list`, `status`, `activate <name>`; `workstreams` and `streams` are deprecated aliases. |
| `link` / `init-remote` | Link a project to a remote team root; `init-remote <path>` is shorthand. |
| `externalize` / `internalize` | Move project state to/from external team storage; `externalize --key <name>` sets an explicit project key. |
| `build` | Compile `squad.config.ts`: `--check`, `--dry-run`, `--watch`. |
| `aspire` | Launch observability dashboard: `--docker`, `--port <n>`. |
| `schedule` | `list`, `run <id>`, `init`, `status`. |
| `preset` | `list`, `show <name>`, `apply <name> [--force]`, `save <name>`, `init [--remote]`. |
| `rc` | Remote Control: `--tunnel`, `--port <n>`, `--path <dir>`; `remote-control` is an alias. |
| `copilot-bridge` / `rc-tunnel` | Check Copilot ACP stdio compatibility or devtunnel availability. |
| `discover` / `delegate` | Discover known squads or create work in another squad (`delegate <name> <description>`). |
| `registry` | Peer squad discovery without inheritance: `add <name> <path>`, `list`, `remove <name>`. |
| `upstream` | Manage inherited sources: `add`, `remove`, `list`, `sync [name]`. |
| `economy` | Toggle economy mode: `on|off`; global `--economy` activates it for one session. |
| `config` | Read or set configuration through the command's supported `get` / `set` operations. |
| `version` / `help` | Print version or help; root flags also include `--version`/`-v`, `--help`/`-h`, `--economy`, and `--team-root`. |

Do not infer a 2.0 feature from an old command name alone. For example, `squad migrate --from ai-team` handles the historical directory rename, not the removed personal-squad format. The unrelated `upstream` feature is inheritance, not the personal team registry. Consult is not a hidden default mode: start the normal coordinator in the chosen host and use project-local files.

## Configuration Reference

The 2.0 configuration change most visible to a multi-host repository is `.squad/config.json`'s `clients` array. The list stores client slugs, and an empty or absent list does not opt a Copilot-only repo into other hosts. The CLI writes and maintains it when you pass `--client`; avoid editing it to include host-specific credentials or machine paths. Per-host projection files live in host-owned locations, and the adapter tries to preserve user MCP settings and shared-file content.

| Key or setting | 2.0 meaning | Upgrade guidance |
|---|---|---|
| `clients` | Portable configured host list (`copilot`, `claude`, `kiro`, `opencode`, `cursor`, `codex`, `antigravity`). | Prefer `squad upgrade --client ...` so projection and config stay synchronized. `all` is an input option, not a stored credential bundle. |
| `version` | Squad configuration/schema version metadata. | Preserve it; let the CLI migration update managed state rather than copying an old `config.json` wholesale. |
| `teamRoot` | Explicit remote/dual-root setting may still identify another team repository; retired profile paths are removed. | Inspect any pre-2.0 value. An old user-profile path is not a supported project link. Use a project-relative remote root when intended. |
| `stateBackend` | Selects supported state storage such as `local`, `orphan`, or `two-layer` (with compatibility aliases in the backend layer). | Confirm the `squad-state` branch and hooks remain healthy after upgrade; do not mix project rollback with backend migration. |
| `platform` / `ado` | Platform detection/configuration, including optional ADO org, project, work-item type, area path, and iteration path. | ADO CLI triage/watch support is more complete than coordinator Issues mode; do not assume every ADO example is a first-class interactive adapter. |
| `SQUAD_EXPERIMENTAL_BACKEND` | Set to `1` to expose experimental `squad_backend_*` MCP tools. | Explicit opt-in; a URL alone does not enable the tools. |
| `SQUAD_BACKEND_URL` / `SQUAD_BACKEND_TOKEN` | MCP bridge endpoint and optional bearer token when experimental backend tools are enabled. | For SDK calls, pass explicit `baseUrl` and optional token; only `https://` is accepted, with `http://` allowed for localhost. Keep tokens out of committed config. |
| `SQUAD_TEAM_ROOT` / `--team-root` | Explicit resolution override for a command or subprocess. | Use only when the working directory is not the project root. It does not restore personal or global fallback. |

The same preview also added a backend opt-in rule: `SQUAD_BACKEND_URL` alone no longer turns on the experimental conversation tools. In SDK code the backend APIs are under `@bradygaster/squad-sdk/backend`; client adapters use the canonical `@bradygaster/squad-sdk/client`. The old plural `/clients` remains a deprecated compatibility alias, not the recommended import path.

## Platforms and Adapters: Read the Status Labels

The 2.0 docs revised their claims about integrations, so check the status before designing a migration around an example.

| Area | 2.0 status | What to plan for |
|---|---|---|
| Azure DevOps | Platform detection and CLI monitor flows (`squad triage`, `squad watch`) use `az boards`; interactive coordinator Issues mode remains GitHub-oriented. | Validate your exact work-item workflow. The ADO issue-lifecycle template is reference guidance the model applies, not proof of a first-class interactive adapter. The example ADO MCP entry is seeded into Copilot's `.mcp.json` only. |
| GitLab issues | Planned, not shipped. The adapter type is not present; `triage` / `watch` have no `glab` path, and the host coordinator digests do not define a GitLab workflow. | Treat GitLab walkthroughs as aspirational. You may ask a coordinator to use `glab` ad hoc, but it improvises rather than following a shipped adapter. Do not automate against the examples as a stable interface. |
| Microsoft Teams communications adapter | The 2.0 doc change shown here only replaced a named example UPN with `user@example.com`; it did not announce a new adapter behavior. | Re-check the adapter's OAuth scopes, tenant settings, and chat/channel configuration independently. The documentation edit is privacy hygiene, not evidence of an upgrade migration. |

This distinction is useful when upgrading because a content-compatible project can still depend on a feature whose documentation status changed. Do not delete working integration configuration solely because an example was relabeled, but do not assume a “planned” workflow is available in the runtime either.

## Release Process: Why the Tags Matter

For maintainers, 2.0 previews are tied to reviewed commits rather than a moving branch name. Release preparation keeps the root, SDK, and CLI versions in lockstep; preview publication checks an exact `expected_sha`, validates the reviewed tree, stages and verifies the SDK/CLI pair, and reconciles registry state before promoting the pair to `insider` and adding the `preview` alias. For this preview, Homebrew, WinGet, and stable promotion are held unless separately authorized. An unknown registry outcome is not treated as proof that publication failed; recovery reconciles against the immutable tag and release evidence rather than recreating or moving a tag.

An insider snapshot and a prepared preview are not interchangeable. The insider workflow calculates a new `X.Y.Z-insider.N` version; do not use it to publish the prepared `2.0.0-preview.2` build. Stable promotion is another operation: it creates a new stable `2.0.0` release rather than converting a published preview in place. In everyday terms, channel names describe what the install command follows, while the release pipeline ensures the CLI and SDK package pair and their provenance agree.

## Rollback Plan: Return to 1.1.0 Safely

The supported upgrade direction is forward. There is no in-place 2.0-to-1.1 migration command, and an old CLI has no guard that protects a newer workspace. `uninstallClients()` only removes projections. It does not reverse casting migrations, remove the 2.0 managed template set, or make a 1.1.0 project.

Use a pre-upgrade commit or backup as the rollback boundary. First stop work and preserve the current 2.0 state for diagnosis. Then restore the **project** to its known 1.1.0 commit: the old `.squad/` state (including the original casting files and config), the coordinator, shipped skills, managed workflows, and any shared host/ignore files that changed. Do not overlay only the old coordinator onto a 2.0 casting pair or leave `clients[]` and 2.0 projections behind. If the project did not have a pre-upgrade commit, recover those files from a verified backup and manually reconcile any team knowledge created after the boundary.

Only after the repository files have been restored should you install the 1.1.0 CLI, for example:

```bash
npm install -g @bradygaster/squad-cli@1.1.0
squad --version
squad doctor
```

Validate the restored state before continuing. If you accidentally ran an older `squad upgrade` against a 2.0 tree, stop immediately, restore the 2.0 project files from version control or backup, and re-run the current 2.0 upgrade only if your intent is to return forward. Do not rely on an older CLI's `--dry-run`: 0.9.1 is known to write during that path, and other old CLIs can preview a downgrade even if they do not write until asked.

## Hands-On: Upgrade and Roll Back Tasktrack

This lab assumes Tasktrack already has the Squad 1.1.0 project created in the earlier chapters, and that its Git working tree is clean. The global CLI may be upgraded independently, but the Tasktrack files will change only when you apply the project upgrade. If you use the baseline sample, first follow `sample/README.md` and the earlier init/casting chapters; the sample itself is not a pre-populated 1.1.0 squad.

1. **Create and mark the branch baseline.** In the Tasktrack repository, verify there is no unrelated or untracked work before making the tag:

   ```bash
   git status --short
   git switch -c v2-ch22-upgrading-to-2
   git tag v2-ch22-start
   ```

   Expected: the branch starts at the 1.1.0 project commit and `v2-ch22-start` names that exact rollback point. If `git status --short` is not empty, stop and commit or stash your work before continuing.

2. **Preview the self-upgrade.** This does not touch Tasktrack's `.squad/`:

   ```bash
   squad --version
   squad upgrade --self --insider --dry-run
   ```

   Expected: the output names the detected package manager, `@insider`, the resolved target (at the time of this book, `2.0.0-preview.2`), and the exact install command. Nothing is installed during this step.

3. **Install the preview CLI and start a fresh terminal.**

   ```bash
   squad upgrade --self --insider
   ```

   Open a new terminal session, then confirm:

   ```bash
   squad --version
   ```

   Expected for this pinned exercise: `2.0.0-preview.2`. If the moving insider tag has advanced, stop and pin the exact version instead of silently changing the exercise target:

   ```bash
   npm install -g @bradygaster/squad-cli@2.0.0-preview.2
   ```

4. **Preview the project upgrade before writing.**

   ```bash
   squad upgrade --dry-run
   ```

   Expected: a list of planned managed file updates and any backups or casting repairs, with the final instruction to run without `--dry-run`. No archive, backup, or project write should be created. Resolve every `dropped` casting item or other blocking diagnostic before applying.

5. **Apply the project upgrade, then inspect—not just trust—the result.**

   ```bash
   squad upgrade
   git status --short
   git diff --stat
   git diff
   find . -type f -name '*.local-backup' -print
   find .squad/casting -maxdepth 1 -type d -name 'handwritten-archive-*' -print
   ```

   Expected: project-owned templates and coordinator may change; team knowledge remains. Review every `.local-backup` and casting archive privately; compare them with the updated files and the branch baseline. Do not stage a private archive or backup for publication without reviewing its contents. Run Tasktrack's own tests if the upgrade changed project-facing files:

   ```bash
   npm test
   ```

6. **Add one host explicitly.** Use Claude Code as the example projection; if you do not have its login or license, you can still inspect generated files, but continue using Copilot to perform the rest of this exercise.

   ```bash
   squad upgrade --dry-run --client claude
   squad upgrade --client claude
   squad client list
   ```

   Expected: the dry run lists Claude projection changes; the applied command records `claude` in `.squad/config.json` `clients[]` and creates or updates the host files without replacing unrelated MCP entries or shared-file paragraphs. If you prefer not to select another host, the Copilot-only fallback is to skip these three commands and leave `clients` unset.

7. **Validate the new CLI against the project.**

   ```bash
   squad doctor
   squad status
   git diff --check
   ```

   Expected: Doctor reports the resolved project and any checks that need follow-up; status explains the active squad. If `doctor` finds an invalid casting pair or bridge, use its exact diagnostic and the earlier repair section rather than deleting `.squad/`. If `health` is available in your build, run `squad health --json` as the stronger CI-style routing validation.

8. **Roll back the exercise to its 1.1.0 baseline.** Do this only on the clean, disposable branch from step 1. Preview untracked cleanup first and ensure every listed file is an output from this lab:

   ```bash
   git clean -nd
   ```

   Once the preview contains only lab-generated backups and host projections, restore the tracked project and remove those generated files:

   ```bash
   git reset --hard v2-ch22-start
   git clean -fd
   ```

   Reinstall the old CLI **after** the project is restored, not before:

   ```bash
   npm install -g @bradygaster/squad-cli@1.1.0
   squad --version
   squad doctor
   ```

   Expected: both the repository and CLI are back at the 1.1.0 boundary. If the `git clean -nd` output includes anything you did not create for this lab, do not run `git clean -fd`; remove only the known generated files or use a fresh training clone. This is a rollback demonstration, not a supported downgrade of a live 2.0 project.

## Under the Hood

`packages/squad-cli/src/cli/core/upgrade.ts` coordinates the project upgrade. It detects the project squad, reads the installed coordinator version, handles stale profile `teamRoot` values, runs casting repair and preflight, and makes separate choices for a dry run, an already-current project, and a regular update. It applies the casting preflight before writing the coordinator because the coordinator's capabilities block depends on a valid registry/history pair. It also refreshes configured client projections after managed templates and infrastructure checks.

Self-upgrade lives beside that flow. The code detects whether the running CLI is stable or prerelease, resolves the corresponding npm tag, compares the tag's version to the current CLI, and refuses an older target unless `--force` is explicit. In dry-run mode it prints the concrete npm/pnpm/Yarn command and returns before invoking the installer. The CLI dispatcher deliberately returns after a successful self-only operation; that is the implementation proof that `squad upgrade --self` does not implicitly modify the current repository.

`packages/squad-cli/src/cli/core/squad-owned-files.ts` plans content-aware changes. Its shipped manifest records normalized hashes, so CRLF versus LF does not masquerade as customization. The planner classifies each candidate as create, overwrite, or unchanged; only modified user content or content without reliable provenance requires a backup. `writeVerifiedBackup()` writes the backup and checks the read-back bytes before any overwrite. Retired files are only removed when their content still matches the old shipped hash. The dry-run formatter uses that same plan, which is why its output can enumerate both updates and backups.

`packages/squad-sdk/src/casting/handwritten-registry.ts` performs the handwritten normalization and empty-registry backfill. It validates the path against symlinks, takes the casting lock before reading live files, captures an exact snapshot, archives originals, validates the registry/history/manifest pair, and delegates to the durable transaction writer. Before a transaction is durable it can restore the snapshot; after that point it rolls forward. `normalizeHandwrittenCastingRegistry()` collects all entries that cannot be proven in `dropped`, and refuses to return a partially normalized registry. `backfillCastingRegistryFromTeam()` resolves the roster against charter folder evidence and requires an explicit universe.

`packages/squad-cli/src/cli/commands/roster.ts` provides the independent opt-in path for optional built-ins. It stores a verified backup plus provenance hashes and exact inserted table rows. Its removal path refuses to delete a row that was edited or was not inserted by the command. `packages/squad-cli/src/cli/core/squad-owned-files.ts` and the roster command therefore protect different ownership boundaries: one for managed shipped files, one for optional roster rows.

The parser and diagnostics round out the compatibility layer. `packages/squad-sdk/src/config/markdown-migration.ts` recognizes canonical and historical routing table headers, flexible column order, Examples/Reason/Notes columns, and a guarded flattened legacy form. The CLI's `migrate` command can render a typed config from markdown or rebuild markdown from SDK-first config. Doctor checks file and casting-pair health; the separate health validator resolves routing targets against known roster/registry names, warns on duplicates/conflicts, and fails closed for unparseable rules or unresolved agents.

Finally, `packages/squad-cli/src/cli/commands/update-check.ts` exposes cached update status without a network call by default. `--refresh` fetches from npm, while a cached result older than 24 hours is marked stale and cannot claim that an update is available. The command's JSON and exit codes make update checks usable in CI without duplicating cache-path logic.

## Pitfalls and Troubleshooting

| Symptom | Likely explanation | Safe response |
|---|---|---|
| `squad upgrade --self` reports “Refusing to downgrade” | The chosen dist-tag resolves below the CLI you are running. | Use `--insider` to stay on the preview channel, or stop and plan a full rollback. Avoid `--force` as a routine fix. |
| The self-upgrade preview shows an unexpected version | The tag is moving, or the npm registry could not confirm its current target. | Install an exact version for reproducibility and verify `squad --version` in a new terminal. |
| You expected templates to refresh after `--self` | Self-upgrade changes only the global CLI package. | Restart the terminal, then run `squad upgrade --dry-run` and `squad upgrade` in each intended repository. |
| A dry run reports a `dropped` entry | An agent record, roster-to-charter mapping, or universe is ambiguous. | Preserve the originals, fix only facts supported by the project, and re-run the preview. No partial repair should be accepted. |
| `.local-backup` is missing or fails verification | The backup write/read-back could not be proven. | That file should not be overwritten. Restore a verified copy or resolve filesystem permissions before retrying. |
| A second upgrade creates another backup | The file changed after the last shipped hash or the prior provenance is missing. | Compare the content with both the backup and template; move valuable backups elsewhere before repeating. |
| `squad status` or `doctor` says no squad was found | There is no project `.squad/` in the current directory or parents, or an old profile squad was the only source. | Run inside the project, initialize if appropriate, or provide an explicit project root. Manually copy only chosen profile knowledge. |
| `doctor` passes but a route is invalid | Doctor checks that routing exists; it does not perform every semantic routing assertion. | Run `squad health` and fix unknown targets, missing rules, or invalid cast state. |
| `squad health` rejects a legacy routing file | Its table may parse to zero rules, target an unregistered member, or contain ambiguous work types. | Preserve the old file, adapt to documented headers, and verify every agent against roster and casting state. |
| An upstream exists but new content is absent | A session reads local snapshots; it does not fetch at startup. | Review precedence and run `squad upstream sync`, then inspect `doctor` and `status`. |
| `state-mcp` processes linger after closing an editor | The host can keep stdio child servers alive, or old wrapper-based MCP entries may remain. | Upgrade, restart the specific host sessions, inspect parent/child ownership, and stop only confirmed orphan PIDs—not processes by image name. |
| An older CLI was pointed at a 2.0 repo | Old upgrade logic may overwrite newer managed templates; 0.9.1 can even write on its dry-run. | Stop. Restore the 2.0 managed files from backup or rerun the 2.0 CLI; do not keep testing the older upgrade command. |
| A GitLab issue example does not work as written | GitLab issue mode is marked planned, not shipped. | Treat `glab` use as an ad-hoc request, not a supported adapter workflow. |
| An ADO coordinator prompt lacks issue operations | CLI triage/watch support is stronger than interactive Issues mode. | Use supported `az boards` monitor workflows and validate the issue-lifecycle template separately. |

A separate support detail: 2.0's release notes say a stale profile `teamRoot` is removed during upgrade, while a `teamRoot` that points to another repository remains as a deliberate dual-root link. If the old setting was intentional, inspect the path rather than deleting every `teamRoot` field indiscriminately.

## The Road Ahead

The following documents are proposals or design material, not seven new guaranteed runtime features. Their statuses come from the proposal headers in the preview source tree. Read them as possible directions and review the current release notes before adopting them as team policy.

| Proposal | Status | Direction |
|---|---|---|
| `contributor-guide-improvements` | Draft — awaiting team review. | Give outside contributors a clearer path through issue templates, good-first-issue curation, branch guidance, `.squad/` boundaries, a contributor FAQ, and stronger README signposting. |
| `error-recovery` | Proposal. | Define five agent recovery responses: retry transient failures, fall back to another method, diagnose unclear causes, escalate blockers, or degrade gracefully with a partial result. The proposal is template/skill guidance, not a runtime retry engine. |
| `iterative-retrieval` | Proposal. | Bound information gathering to three purposeful cycles: broad scan, targeted follow-up, and final fill; then stop and escalate. It aims to prevent unbounded spawning and premature abandonment. |
| `memory-governance-provider` | Design. | Put classification, retention, routing, retrieval, and audit above the low-level storage provider. Local `.squad/` memory stays the default; external semantic memory is opt-in, and unavailable providers fail closed rather than pretending to store data. |
| `reflect` | Proposal. | Capture in-session learning after meaningful failure or correction, distinguish high/medium/low triggers, and check that reflection before retrying the same kind of action. It complements final history writing rather than replacing it. |
| `retro-enforcement` | Proposal. | Make retrospective action items trackable as GitHub issues and optionally enforce a cadence. Its markdown and PowerShell sketches are proposed skill behavior, not a shipped scheduler guarantee. |
| `tiered-memory` | Proposal. | Split context into a small hot current-session layer, summarized cold history loaded on demand, and a selectively read wiki of durable facts. The estimated context reduction is a proposal claim, not a guaranteed 2.0 result. |

The memory governance design explicitly complements tiered memory: hot/cold/wiki describes what to load and promote; governance decides what may be retained and where. It also insists that `StorageProvider` remain a simple byte store, not a policy engine. The design describes a local default and a future tool/MCP bridge, but notes that there is no callable Copilot Memory API in the preview implementation. For now, do not confuse proposal language about future classification or external semantic writes with the shipped 2.0 upgrade and projection mechanisms covered above.

## Summary

- `latest` remains 1.1.0 while `insider` (with `preview` as an alias) carries the 2.0 preview. Self-upgrade and project upgrade are separate actions.
- `squad upgrade --dry-run` previews managed writes, backups, casting repair, and optional client files; inspect the plan before applying.
- Backups are content-aware and verified, while casting repair and roster backfill require evidence and fail closed rather than guessing.
- Personal squads, consult mode, and `--global` were removed without a migration command. Copy appropriate knowledge into a project `.squad/` by hand.
- 2.0 changes routing precedence to earlier-wins, so review order and run `squad upstream sync` after upgrade.
- A rollback to 1.1.0 means restoring the pre-upgrade project first and then installing the older CLI—not running an old upgrade against 2.0.
- The seven Road Ahead items are proposals/design material with explicit statuses, not automatic features of this preview. With the upgrade path and its limits established, Part V turns to reusable patterns, an end-to-end capstone, and contribution practice.

## Exercises

1. A developer is running `2.0.0-preview.2` and invokes `squad upgrade --self`. Which tag does the CLI follow by default? What does `--insider` change, and what protection does `--force` bypass?
2. A dry run reports one malformed registry entry in `dropped` and two other entries that could be normalized. What should the developer expect the real upgrade to write? Explain the role of the archive and why a partial repair would be unsafe.
3. You have a personal squad with a useful API charter, a stale frontend history, and a decision that applies to two projects. Describe a safe hand-migration plan for one project and name three kinds of data you would not copy wholesale.
4. Your `upstream.json` lists `team-defaults` before `org-security`, but the latter should take priority. What should you change after upgrading, and what does `squad upstream sync` do that a session start does not?
5. A developer runs `squad upgrade --self --dry-run --migrate-directory` and expects no writes. Is that assumption safe? Explain the ordering issue and give a safer preview command.
6. Tasktrack was upgraded, `clients` contains `claude`, and `squad doctor` passes. Does that prove Claude Code is authenticated and licensed? What does the projection establish, and what must still be checked?

## Quiz

1. At the `v2.0.0-preview.2` release, which npm tag remains on Squad 1.1.0: `latest`, `insider`, or `preview`?
2. Does `squad upgrade --self` automatically run a project `squad upgrade` after installing the CLI?
3. What must be true before Squad backfills an empty casting registry from `team.md`?
4. What does a non-empty `dropped` list mean during handwritten casting repair? Does it indicate a committed partial repair?
5. Which command performs the stronger semantic check that routing references resolve to known squad agents: `squad doctor` or `squad health`?
6. In 2.0 upstream conflict resolution, do earlier or later declared entries win?
7. Can `uninstallClients()` roll a 2.0 workspace back to Squad 1.1.0?
8. Name the correct sequence for a safe 1.1.0 rollback: restore project state first or install the older CLI first?

## Further Reading

- [Upgrading Squad](https://bradygaster.github.io/squad/docs/scenarios/upgrading/)
- [Self Upgrade](https://bradygaster.github.io/squad/docs/features/self-upgrade/)
- [Migration Guide](https://bradygaster.github.io/squad/docs/get-started/migration/)
- [Troubleshooting](https://bradygaster.github.io/squad/docs/scenarios/troubleshooting/)
- [Release Process for Squad Maintainers](https://bradygaster.github.io/squad/docs/scenarios/release-process/)
- [CLI Reference](https://bradygaster.github.io/squad/docs/reference/cli/)
- [Configuration Reference](https://bradygaster.github.io/squad/docs/reference/config/)
- [Enterprise Platforms](https://bradygaster.github.io/squad/docs/features/enterprise-platforms/)
- [GitLab Issues Mode](https://bradygaster.github.io/squad/docs/features/gitlab-issues/)
- [GitLab Issues Walkthrough](https://bradygaster.github.io/squad/docs/tour-gitlab-issues/)
- [Teams Communication Adapter](https://github.com/bradygaster/squad/blob/v2.0.0-preview.2/docs/features/teams-adapter.md)
- [Contributor Guide Improvements proposal](https://github.com/bradygaster/squad/blob/v2.0.0-preview.2/docs/proposals/contributor-guide-improvements.md)
- [Error Recovery Skill proposal](https://github.com/bradygaster/squad/blob/v2.0.0-preview.2/docs/proposals/error-recovery.md)
- [Iterative Retrieval Skill proposal](https://github.com/bradygaster/squad/blob/v2.0.0-preview.2/docs/proposals/iterative-retrieval.md)
- [Memory Governance Provider proposal](https://github.com/bradygaster/squad/blob/v2.0.0-preview.2/docs/proposals/memory-governance-provider.md)
- [Reflect Skill proposal](https://github.com/bradygaster/squad/blob/v2.0.0-preview.2/docs/proposals/reflect.md)
- [Retro Enforcement Skill proposal](https://github.com/bradygaster/squad/blob/v2.0.0-preview.2/docs/proposals/retro-enforcement.md)
- [Tiered Agent Memory proposal](https://github.com/bradygaster/squad/blob/v2.0.0-preview.2/docs/proposals/tiered-memory.md)
