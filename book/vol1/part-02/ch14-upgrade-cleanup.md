# Chapter 14: Cleanup, Upgrades, and Migration

> **Prerequisites:** Chapters 2 and 4.

## What You'll Learn

- Configure Ralph's cleanup capability and predict exactly which paths it deletes, prunes, or only warns about.
- Separate the self-upgrade of the CLI package from an upgrade of a project's Squad-managed files.
- Identify the files a project upgrade refreshes, the user-owned files it leaves alone, and the customizations that are backed up.
- Use dry-run and version checks without assuming that every upgrade-related operation is non-mutating.
- Plan a safe upgrade and migration for a working Tasktrack squad.
- Migrate an old `.ai-team/` project and recognize when a very old on-disk format requires manual recovery or reinitialization.

This chapter covers routine upgrades within Squad 2.x: moving from one 2.x release to the next, refreshing the files Squad owns, and keeping a long-running squad tidy. A project upgrade also refreshes every host listed in `.squad/config.json`, and `squad upgrade --client <list>` (including `all`) adds hosts to an existing project, just as `squad init --client <list>` selects them for a new one. Tasktrack stays on the default Copilot host.

> **Note:** Changed in Squad 2.0: if you are coming from Squad 1.x, read Chapter 22 (Volume 2) before you upgrade. It covers the removed features, the new launcher in `.mcp.json`, and how to roll back. The rest of this chapter assumes a project that is already on 2.x.

## Cleanup Is a Scheduled Housekeeping Capability

Long-lived Ralph processes accumulate disposable scratch files and dated logs. The cleanup capability is intended to keep that operational debris from growing forever while leaving meaningful squad knowledge for humans to curate. Its behavior is narrow: it clears the contents of the scratch directory, removes date-stamped old orchestration and session logs, and reports old decision-inbox files without merging or deleting them.

Cleanup is a watch capability, not a standalone `squad cleanup` command. The source registers it as a `housekeeping` phase capability. As with other capabilities, the watcher only enables it if you opt in through a capability flag or config. For example:

```bash
squad watch --cleanup
```

Or enable it in the watch section of `.squad/config.json`:

```json
{
  "watch": {
    "cleanup": {
      "everyNRounds": 10,
      "maxAgeDays": 30
    }
  }
}
```

The capability checks its configuration on execution. It runs on round 1 so that enabling it gives immediate feedback, then on every configured Nth round. When the configured round interval is not reached, the capability returns a “skipped” summary and does no cleanup. The `--execute` flag enables Ralph's autonomous issue execution; it is not the switch that turns cleanup on.

The two options are positive numbers: `everyNRounds` controls cadence and `maxAgeDays` sets log age. Invalid, missing, non-finite, zero, or negative values fall back to the defaults (10 rounds and 30 days). For example, `{ "everyNRounds": 5, "maxAgeDays": 60 }` checks every fifth round and keeps dated logs for 60 days. Configuring `everyNRounds: 1` runs the capability each round after its special round-one check.

### Exact cleanup scope

| Path under squad state | Action | Rule |
|---|---|---|
| `.scratch/` | Deletes every immediate entry recursively | Scratch content is considered ephemeral; it is not age-filtered |
| `orchestration-log/` | Deletes dated entries | Filename must begin with `YYYY-MM-DD`; date must be older than `maxAgeDays` |
| `log/` | Deletes dated entries | Same filename/date rule; this is the session-log directory in the implementation |
| `decisions/inbox/` | Emits a warning summary only | Considers `.md` files whose filenames begin with a date older than seven days |
| `decisions.md`, agent histories, team/routing config | No cleanup action | These are not in the cleanup capability's target paths |

A filename that does not begin with a parseable date is not classified as old and is left in place. The code uses the date in the filename rather than filesystem modification time. If an old file is pruned, the implementation removes it; it does not move it to `logs/archive/YYYY-MM/` or another archive directory. An inbox warning is a nudge to review and merge the pending decision, not a decision merge.

> **Warning:** The cleanup feature page says old logs are archived and presents `squad logs archive` as a manual option. The v2.0.0 implementation instead deletes matching old entries, and the shipped CLI has no `squad logs archive` handler. Treat the cleanup capability as deletion, keep independent backups of logs you need, and do not infer a recoverable archive from the documentation.

```mermaid
flowchart TD
  A["Watch housekeeping phase"] --> B{"cleanup capability enabled?"}
  B -- "No" --> C["No cleanup run"]
  B -- "Yes" --> D{"Round 1 or every N rounds?"}
  D -- "No" --> E["Report skipped"]
  D -- "Yes" --> F["Delete .scratch entries"]
  F --> G["Prune date-stamped old logs"]
  G --> H["Warn about dated inbox files older than 7 days"]
  H --> I["Keep decisions and team knowledge"]
```

The capability's configured state root can be the resolved Squad state directory, not necessarily a literal `.squad/` folder in the project root. That distinction matters for projects using external or alternate state backends. You can reason about the same target categories while remembering that state resolution determines where the root actually is.

## Two Different Upgrades

The word *upgrade* can refer to the CLI executable installed on your machine or to the Squad files inside one repository. These operations have separate commands and separate effects.

| Operation | Command | What changes |
|---|---|---|
| CLI self-upgrade | `squad upgrade --self` | Installs a newer `@bradygaster/squad-cli` package globally using npm, pnpm, or Yarn, on the channel you already use |
| Project upgrade | `squad upgrade` | Refreshes the coordinator, managed templates, selected built-in skills, workflows, and applicable migrations in the current repository |
| Preview project upgrade | `squad upgrade --dry-run` | Reports exactly which files a real run would write, and writes nothing (`--migrate-directory` still runs first if you combine them) |
| Preview self-upgrade | `squad upgrade --self --dry-run` | Prints the install command it would run; installs nothing (2.0 CLIs only; a 1.1.0 CLI installs) |

A new CLI binary does not automatically mean that every repository has been upgraded. Run `squad upgrade` from each project whose managed files should be refreshed. The v2.0.0 implementation of `--self` installs the package and asks you to restart the terminal; on successful self-upgrade it returns before running the project upgrade.

> **Note:** The assigned self-upgrade feature page says the CLI self-upgrade automatically refreshes repository templates. That is not what the v2.0.0 command dispatcher does. It prints a restart instruction and returns. Run `squad upgrade` separately from the project root when you want to update that repository.

### Self-upgrade and release channels

The package manager choice comes from the current process's `npm_execpath` or `npm_config_user_agent`. If those environment values identify pnpm or Yarn, the CLI selects that manager; otherwise it falls back to npm. This is not a detection based on a lock file in the current directory. The install targets are:

```bash
squad upgrade --self --dry-run  # 2.0 CLI: print the command; install nothing
squad upgrade --self            # follow the installed channel
squad upgrade --self --insider  # force @bradygaster/squad-cli@insider
```

Self-upgrade follows the channel you already have. A stable install (`2.0.0`) upgrades from `@latest`; a prerelease install (a version such as `2.1.0-preview.1` or `2.1.0-insider.3`) upgrades from `@insider`. `--insider` forces the insider tag. Before it installs anything, the CLI resolves the tag and refuses a downgrade: if the tag points at a version older than the one you have, it stops with "Refusing to downgrade" and asks you to pass `--force` (or, from `@latest`, `--insider` to stay on the prerelease channel). `--dry-run` prints the package manager, the target version and the exact install command, then exits without installing.

Stable is the ordinary choice. Insider is a prerelease channel for testing; use it only when you want the unreleased build and accept that it can change more rapidly. Self-upgrade runs a global add/install command and may fail if your global package directory is not writable. The CLI reports a failure and exits nonzero rather than claiming success. For permission errors, prefer fixing the package manager's global prefix or using a Node version manager over running an entire tool as root.

`--insider` by itself is not a project-upgrade channel: the CLI warns that it only applies with `--self` and ignores it for a repository upgrade. For a project upgrade, `--force` bypasses the repository's already-current version shortcut and re-processes every file. With `--self`, `--force` is what allows a downgrade; it does not change the package-manager command.

Do not treat `--dry-run` as a universal dry-run across every combination. The dispatcher still performs `--migrate-directory` before it reaches the repository dry-run path, so that rename is real. On a 2.0 CLI, `--self --dry-run` is safe: it previews the install and returns. A 1.1.0 CLI ignores `--dry-run` with `--self` and installs `@bradygaster/squad-cli@latest`; check the target with `npm view @bradygaster/squad-cli dist-tags` instead (Chapter 22 (Volume 2)). Use `squad upgrade --dry-run` by itself to preview the project upgrade, and don't combine it with `--migrate-directory` expecting the rename to be simulated.

## What a Project Upgrade Preserves and Overwrites

The upgrade implementation uses a template manifest to classify shipped files as Squad-owned or user-owned. It also has custom handling for the coordinator, workflows, and Copilot instructions. In Squad 2.0 the upgrade is content-aware: it compares each Squad-owned file with the new template (ignoring line endings) and writes only files that would change, so running it twice in a row writes nothing the second time. `squad upgrade --help` spells out the boundary. The Squad-owned set is `.github/agents/squad.agent.md`, `.github/skills/*`, `.github/workflows/squad-*.yml`, `.squad/templates/**` and the flat `.squad/casting-*.json` template copies. Never touched are `team.md`, `routing.md`, decisions, `agents/*/history.md`, the casting registry and history pair, `config.json` and `.ai-team/`. Read the actual diff; never assume that the word “upgrade” means either “replace the whole `.squad/` directory” or “preserve every edited template.”

### Files it refreshes

A normal project upgrade can refresh the following Squad-owned artifacts from the installed CLI's templates:

- `.github/agents/squad.agent.md`, the coordinator prompt, after substituting version and project-specific information.
- Files listed as managed in the template manifest, including `.squad/templates/` content and selected bundled resources.
- Manifest-listed built-in skills at `.github/skills/`.
- Squad-managed workflow YAML files under `.github/workflows/`.
- `.github/copilot-instructions.md`'s Squad-managed block when the team enables Copilot coding agent support.
- Infrastructure files and missing scaffold items handled by ensure checks.

The manifest is authoritative for the specific built-in file list. Squad decides that a file is **customized** when it differs from both the new template and the version Squad last shipped; those last-shipped hashes live in `.squad/templates/.shipped-manifest.json`, which `squad init` and each upgrade record. A customized file, whether a built-in skill, a workflow or the coordinator, is copied to `<file>.local-backup` first, and the backup is read back and verified before the original is overwritten; if the backup cannot be verified, that file is left alone and reported. A file that still matches what Squad shipped is replaced silently. One exception: a customized `.github/workflows/squad-ci.yml` is treated as yours and preserved unchanged, because that is where you put your build and test commands. The backup has a fixed name, so a later upgrade of the same customized file writes a new one; move a backup you need before upgrading again. The dry run uses the same plan, so it lists the files that would be overwritten, created, backed up or preserved.

The Copilot instructions path is special: Squad merges or replaces its marked managed block while preserving user content outside that block. If the file contains only user-authored instructions and no Squad markers, the managed block is appended instead of replacing all content. Newline-only changes are normalized so a different CRLF/LF style alone does not force a rewrite.

### Files that stay yours

The project upgrade does not replace the entire team state directory. In particular, the team's roster/configuration and project knowledge—such as `team.md`, `decisions/`, agent charters, and per-agent `history.md`—are not regenerated from a blank team. User-owned manifest entries, including `routing.md`, `ceremonies.md`, `ralph-instructions.md`, and identity notes, are installed only when missing. A file already present at those destinations is left alone.

Supported legacy casting state is preflighted and migrated before the managed coordinator and template refresh. The migration validates the legacy registry/history evidence instead of guessing identities or historical assignments. If evidence is malformed or ambiguous, the upgrade should stop before overwriting managed files. Keep a backup of the entire `.squad/` state and coordinator before a major upgrade, and review the casting output separately. Do not copy a current roster over historical assignment evidence.

| Category | Typical examples | Upgrade behavior |
|---|---|---|
| User state / knowledge | `team.md`, decisions, agent charters, `history.md` | Preserved; not replaced as a package template |
| User-owned manifest templates | `routing.md`, `ceremonies.md`, `ralph-instructions.md`, identity notes | Create if missing; keep existing files |
| Squad-managed templates | `.squad/templates/*` and manifest-managed defaults | Replaced with current shipped versions |
| Built-in Squad skills | Manifest-listed `.github/skills/*/SKILL.md` | Refreshed; customized versions backed up to a verified `.local-backup` first |
| Coordinator / managed workflows | `.github/agents/squad.agent.md`, `.github/workflows/squad-*.yml` | Refreshed; local differences backed up to `.local-backup`; a customized `squad-ci.yml` is preserved |
| Never touched | `team.md`, `routing.md`, decisions, `agents/*/history.md`, casting registry/history, `config.json`, `.ai-team/` | Left as they are |
| Host projections | Files for each host in `config.json` `clients[]` | Refreshed on every upgrade; `--client <list>` adds hosts |
| Copilot instructions | `.github/copilot-instructions.md` | Squad block updated while user-authored material is retained |

If your project has more hosts than Copilot, a plain `squad upgrade` refreshes every client listed in `clients[]` and keeps your other MCP servers, formatting and line endings in the shared config files. Between upgrades, `squad client sync` refreshes the configured hosts' files on its own (for example after you change `routing.md`), and `squad client list` shows which hosts are configured. Tasktrack has no extra hosts, so neither command changes anything here.

Some generated scaffolding is ensured only when missing. The important distinction is ownership plus destination, not simply whether a file lives under `.squad/`. A custom skill stored alongside Squad's built-in skills may be treated differently from a manifest-listed built-in skill. Check whether the installed version lists it as Squad-managed before making a local customization.

## A Safe Upgrade Scenario

Use the following sequence for the Tasktrack repo after you have completed the prior workflow chapters:

1. **Check the CLI version and working tree.** Record `squad --version` and run `git status --short`. Commit or stash unrelated work so that the upgrade diff is identifiable.
2. **Back up user state and important customizations.** At minimum, make a private backup of `.squad/` and the coordinator. Keep credential caches and webhook secrets outside the repository. A backup can contain private history; store it accordingly.
3. **Preview the project upgrade.** From Tasktrack's repository root, run:

   ```bash
   squad upgrade --dry-run
   ```

   Review the source version and target version, the coordinator check, and the managed-file list. The dry run lists the same files a real run would write, back up or preserve, so a customized workflow shows up there.

4. **Apply the CLI update only if you intend to change the global tool.** For example:

   ```bash
   squad upgrade --self
   ```

   Restart the terminal as requested, verify `squad --version`, then return to the Tasktrack root and preview again with the newly installed CLI. This step is optional; upgrading project files with the current CLI is a separate choice.

5. **Apply the repository upgrade.** Run `squad upgrade` and read every warning about local backups, casting migration, or a stale team directory. A successful command is not a substitute for checking the diff.
6. **Review and verify.** Run `git status --short`, inspect the `.squad/`, `.github/agents/`, `.github/skills/`, and `.github/workflows/` changes, confirm user state is intact, and run Tasktrack's tests:

   ```bash
   npm test
   ```

   The Tasktrack sample uses Node's built-in test runner and has no npm dependencies. This step verifies the app remains healthy; it does not validate Teams credentials or the CLI itself.

7. **Commit intentionally.** Stage only the Squad-owned updates and any deliberate user changes. Do not commit token caches, webhook secrets, or private migration archives by accident.

This workflow makes rollback manageable. A migration can change file names, configuration shape, or persistent state in addition to refreshing templates. Have a known-good commit or backup before the first live run, and do not delete the old copy until the migrated project passes its checks.

## Migrations: What They Change

A project upgrade runs version-based migrations after refreshing managed files. The v2.0.0 migration runner contains steps for older format transitions, including:

- Creating `.squad/skills/` for the older v0.2.0 step.
- Creating `.squad/plugins/` for the v0.4.0 step.
- Scrubbing email addresses from Squad state as a privacy migration at v0.5.0.
- Copying legacy `.squad/skills/<name>/` skills into `.copilot/skills/` at v0.9.0, without overwriting an existing destination.

Two more repairs run in Squad 2.0 before the managed files are refreshed, in a real run and in `--dry-run`:

- **Casting repair.** A hand-edited or empty `.squad/casting/registry.json` is normalized record by record. An empty registry is backfilled from `team.md` when each specialist maps to a provable `.squad/agents/<id>/charter.md` folder. The originals are archived under `.squad/casting/handwritten-archive-<sha256>/`. An entry that cannot be proven stops the upgrade with the exact entries and a `squad cast --name <Name> --role "<Role>"` fix.
- **`teamRoot` normalization.** An obsolete `teamRoot` that older versions left in `.squad/config.json` pointing outside the project is removed, with a one-line message. A `teamRoot` that points at another team repository (dual-root mode) is left alone.

Migrations are selected by the installed version recorded in the coordinator and the CLI's current package version. An “already up to date” project can still run missing migration or ensure logic. A migration may therefore be relevant even when the version label appears current; read the output and the source path it touched.

For supported legacy casting state, the upgrading guide describes a more careful migration than those simple directory steps. It validates old registry and history pairs, preserves original files in a content-hash archive, and refuses to synthesize missing universes, dates, or memberships. Use `squad upgrade --dry-run` as a preflight when a legacy casting migration is involved. If the validation refuses, keep both original files and request recovery based on evidence rather than editing the registry to make the validator pass.

## Migrating from `.ai-team/` and Older Releases

The state directory used to be named `.ai-team/`; current projects use `.squad/`. The v2.0.0 CLI still includes a directory migration path, and normal upgrade detects a legacy directory and prints a deprecation warning. The directory is not automatically renamed just because you installed a new CLI.

For the explicit legacy-directory migration, first back up the repository and then run:

```bash
squad upgrade --migrate-directory
```

The migration refuses if there is no `.ai-team/` directory or if `.squad/` already exists. It renames `.ai-team/` to `.squad/`, rewrites `.ai-team/` references in `.gitignore` and `.gitattributes` if those files exist, scrubs email addresses from migrated state, and moves `.ai-team-templates/` into `.squad/templates/` if present. The upgrade dispatcher then continues into the normal project refresh. Review the complete diff, because the email scrub and rename alter tracked files. The old directory name and new directory name must not both be present: the code avoids guessing which is authoritative.

The migration command also exposes the directory move as `squad migrate --from ai-team`; it performs the same operation and then tells you how to proceed with an SDK-first migration. For projects already on a compatible v0.8.x-or-later format, the published migration guide says that a package update should not require deleting and reinitializing `.squad/`. The CLI package name used by the v2.0.0 self-updater is still `@bradygaster/squad-cli`.

A jump from the old v0.5.4 beta format is different. The migration guide describes that on-disk structure as incompatible with current releases. Back up the old directory, initialize a current Squad state structure, and manually bring across only the knowledge you have reviewed—team members, custom charters, decisions, routing, skills, and useful history. Do not copy obsolete templates or casting artifacts blindly into a new structure. The old guides contain examples and package aliases that span multiple releases; confirm a package name or command against your target release before using it.

For a very early `.ai-team/` project, keep the old directory as a backup until `squad doctor` or the available health checks pass on the new state. For a partially upgraded project, do not respond to a warning by deleting `.squad/` and running `squad init` unless you have an independent backup and have decided to rebuild the team state. Reinitialization is a recovery strategy of last resort, not the normal update procedure.

```mermaid
sequenceDiagram
  participant Dev as "You"
  participant CLI as "squad upgrade"
  participant State as ".squad state"
  participant Files as "Managed project files"
  Dev->>CLI: --dry-run
  CLI->>State: Validate directory and legacy casting evidence
  CLI-->>Dev: Preview planned managed-file changes
  Dev->>Dev: Back up and review customizations
  Dev->>CLI: Run upgrade
  CLI->>State: Apply supported migrations
  CLI->>Files: Refresh managed files and workflows
  CLI-->>Dev: Report versions, migrations, warnings
  Dev->>Dev: Inspect diff and run tests
```

## Hands-On: Upgrade Tasktrack Without Losing Team State

This exercise rehearses a repository upgrade on the Tasktrack project created earlier in the book. If your checkout does not yet contain `.squad/`, initialize and cast it using Chapters 2–4 first; the exercise does not require the memory or skills work in Chapters 15–17.

1. From the Tasktrack repository root, record a clean baseline:

   ```bash
   git status --short
   squad --version
   ```

   Expected result: you know whether there are unrelated changes and which CLI version will author the upgrade.

2. Make a separate backup of `.squad/` and `.github/agents/squad.agent.md`. If either contains private team history, do not place the backup in a public repository.
3. Preview the changes:

   ```bash
   squad upgrade --dry-run
   ```

   Expected result: the CLI lists the Squad-owned files it would overwrite, create, back up to `.local-backup` or preserve. On a project that is already current it reports that the squad-owned files are up to date.

4. Apply the repository upgrade:

   ```bash
   squad upgrade
   ```

   Expected result: the coordinator and managed templates are refreshed; your `team.md`, decisions, agent histories, and existing user-owned templates remain. If the CLI reports a `.local-backup`, compare that backup with the new file and carry your edit forward deliberately.

5. Verify the app and repo:

   ```bash
   git status --short
   npm test
   ```

   Expected result: the working-tree diff contains only understood upgrade changes and intentional backups; Tasktrack's Node tests still pass. If any important customization disappeared, recover it from the backup into the correct user-owned location rather than restoring an entire obsolete `.squad/` tree over the migrated one.

6. Optional cleanup configuration: add a `watch.cleanup` object with a small cadence and a conservative log age. Enable it explicitly with `squad watch --cleanup` only when you are ready for a live run. Before doing so, inspect date-stamped files in `.squad/.scratch/`, `.squad/log/`, and `.squad/orchestration-log/`; old matching logs are deleted, not archived.

## Configuration Reference

| Setting / command | Scope | Default or values | Effect |
|---|---|---|---|
| `watch.cleanup` | `.squad/config.json` | Disabled unless configured/enabled | Object-valued capability config; contains the cleanup cadence and age options |
| `watch.cleanup.everyNRounds` | `.squad/config.json` | `10` | Cleanup runs on round 1 and then each Nth round |
| `watch.cleanup.maxAgeDays` | `.squad/config.json` | `30` | Removes date-stamped log entries older than the threshold |
| `--cleanup` | `squad watch` | Opt-in | Enables the cleanup capability for that watch invocation |
| `squad upgrade --self` | CLI package | Follows installed channel (`@latest` or `@insider`) | Installs globally via detected npm/pnpm/Yarn manager; refuses a downgrade; asks you to restart |
| `--dry-run` | With `--self` | Off | Prints the install command and target version; installs nothing |
| `--insider` | With `--self` | `@insider` | Selects the insider package tag; ignored for project upgrades |
| `--force` | `squad upgrade` | Off | Bypasses the repository's already-current shortcut and re-processes all files; with `--self`, allows a downgrade |
| `--dry-run` | `squad upgrade` | Off | Lists the files a real run would write, back up or preserve, plus casting preflight; writes nothing |
| `--client <list>` | `squad upgrade` | Configured hosts only | Adds hosts (`copilot`, `claude`, `kiro`, `opencode`, `cursor`, `codex`, `antigravity`, `all`) to `clients[]` and projects them |
| `squad client sync [--dry-run]` | Configured hosts | None | Refreshes every configured host's projected files without a full upgrade |
| `.squad/templates/.shipped-manifest.json` | Project | Written by init and upgrade | Hashes of what Squad last shipped; used to tell your edits from template revisions |
| `--migrate-directory` | `squad upgrade` | Off | Renames legacy `.ai-team/` to `.squad/`, then continues regular upgrade |
| `--state-backend TYPE` | `squad upgrade` | Backend-specific | Runs project upgrade and then the requested state-backend migration |
| `SQUAD_HOME` | Process environment | Home default | Can change Squad's global data directory; it is also respected by Teams token storage |

## Under the Hood

The command dispatcher for `upgrade` is in `packages/squad-cli/src/cli-entry.ts`. It separates `--self`, `--insider`, `--migrate-directory`, `--dry-run`, and state-backend migration. It handles the directory rename first, attempts self-upgrade when requested, and returns after a successful self-only operation. This dispatch order is the decisive evidence that self-upgrade does not automatically apply a project template update and that a combined dry-run flag does not make every earlier operation harmless.

`packages/squad-cli/src/cli/core/upgrade.ts` implements the repository update. It detects the current squad directory, reads the installed coordinator version, validates legacy casting state, compares versions, and iterates `TEMPLATE_MANIFEST`. The `overwriteOnUpgrade` field documents ownership. `collectSquadOwnedCandidates()` gathers every Squad-owned file (manifest entries, workflows and the full `.squad/templates/` mirror), and `packages/squad-cli/src/cli/core/squad-owned-files.ts` plans and applies them: it compares content with line endings ignored, decides what is customized from the shipped manifest, writes and verifies each `.local-backup` before overwriting, and preserves a customized `squad-ci.yml`. User-owned files are created only if they do not exist. The coordinator backup compares normalized content after removing the release stamp and generated team-capabilities block so generated differences alone do not look like a manual edit.

The same file contains `selfUpgradeCli()`. It chooses the package manager from process environment, picks the tag with `detectSelfUpgradeTag()` (a prerelease version follows `insider`, anything else `latest`), resolves that tag's version and refuses a downgrade unless `force` is set, prints the command and returns on `dryRun`, and otherwise runs the global install and throws on failure. `packages/squad-cli/src/cli/core/templates.ts` is the manifest source of truth. `packages/squad-cli/src/cli/core/managed-file.ts` handles newline-preserving writes and the marked merge for `.github/copilot-instructions.md`.

Cleanup is implemented in `packages/squad-cli/src/cli/commands/watch/capabilities/cleanup.ts`; the registry is created in the watch capability barrel, while `watch/index.ts` preflights enabled capabilities and runs the `housekeeping` phase. Its `safeDelete()` calls recursive `rmSync()`. The age helper parses only the date prefix of filenames; no archive move is performed. This detail is why the cleanup page's archive description should not be used as evidence of recoverability.

The legacy `.ai-team/` rename is in `packages/squad-cli/src/cli/core/migrate-directory.ts`; the `--migrate-directory` and self-upgrade control flow is in `cli-entry.ts`. Version migrations such as directory scaffolding, email scrubbing, and old skill copying live in `packages/squad-cli/src/cli/core/migrations.ts`. These are different from the rename operation and from the casting-state migration performed before a managed upgrade.

## Pitfalls and Troubleshooting

- **I upgraded the CLI but this repo still has old templates.** Self-upgrade changes the global package only. Run `squad upgrade` from the repository root as a separate step.
- **A customization vanished.** Check the `.local-backup` beside the coordinator, workflow or built-in skill. Squad writes one for any Squad-owned file that differed from both the new template and the version it last shipped. A later upgrade of the same customized file replaces that backup, so keep version control as your real safety net.
- **Self-upgrade says "Refusing to downgrade".** The channel tag points at an older version than the one you have, which happens when you installed a prerelease and then ask for `@latest`. Stay on the prerelease channel with `--insider`, or pass `--force` only if you really want the older build.
- **My `squad-ci.yml` edits survived but other workflows were refreshed.** That is deliberate. A customized `squad-ci.yml` is user-owned; other `squad-*.yml` workflows are Squad-owned and get a `.local-backup` when you have changed them.
- **An “already current” project still changed.** Upgrade can still run missing migrations and ensure checks and can refresh managed files even when the version stamp matches.
- **Cleanup removed a log I wanted.** The code prunes dated files rather than archiving them. Restore from version control or an independent backup, and reduce or disable cleanup until you have a retention plan.
- **Cleanup did not run.** It is opt-in. Enable the capability with `--cleanup` or configure `watch.cleanup`; `--execute` alone is not the switch.
- **A log file was not pruned despite being old.** It may lack a `YYYY-MM-DD` filename prefix, or its filename date may be newer than the age threshold. Modification time alone is not used.
- **`squad upgrade --migrate-directory` refuses.** It needs `.ai-team/` and refuses if `.squad/` already exists. Back up and resolve the two-directory state rather than renaming over either one.
- **An old casting migration is refused.** Do not invent missing IDs, universes, timestamps, or assignment membership. Preserve originals and recover evidence from the version that created them.
- **An old v0.5.4 state is not accepted.** Treat it as a format migration, not a routine in-place template update. Preserve a backup, initialize current state, and manually migrate reviewed knowledge.
- **`--dry-run` was combined with `--migrate-directory`.** The rename runs before the project preview, so it really happened. Review the rename, then rerun the standalone dry run.

## Summary

- Cleanup is an opt-in Ralph housekeeping capability, with narrowly defined targets and date-based deletion rules.
- Old matching logs are pruned, not archived; stale inbox files only trigger warnings.
- `squad upgrade --self` updates the global CLI package. `squad upgrade` separately refreshes one repository.
- Project upgrades preserve team knowledge and existing user-owned files, but refresh managed templates, built-in skills, coordinator, workflows, and eligible migration artifacts.
- The project upgrade is content-aware: a customized Squad-owned file (coordinator, workflow or built-in skill) gets a verified `.local-backup` before it is overwritten, a customized `squad-ci.yml` is preserved, and `team.md`, `routing.md`, decisions, histories, casting state and `config.json` are never touched.
- Self-upgrade follows the installed channel, refuses a downgrade without `--force`, and previews with `--dry-run` on a 2.0 CLI (a 1.1.0 CLI ignores it and installs). Coming from 1.x, read Chapter 22 (Volume 2) first.
- Use a standalone dry run, back up important state, inspect the diff, test Tasktrack, and only then commit.
- Old `.ai-team/` projects need an explicit migration. Very old incompatible state should be backed up and migrated deliberately, not deleted casually.

## Exercises

1. Configure cleanup to run every four watch rounds and retain dated logs for 45 days. Where does the object belong, and which explicit capability switch enables it?
2. A developer edits a built-in skill under `.github/skills/` and runs `squad upgrade`. What protection should they expect, and what should they do before the upgrade?
3. Explain why `squad upgrade --self` and `squad upgrade` are separate operations. Which one should you run to refresh the current Tasktrack repo?
4. A log has been on disk for 90 days but is named `watch-latest.md`. Why might cleanup keep it? What happens to a dated inbox file older than seven days?
5. A project has both `.ai-team/` and `.squad/`. What does the migration command do, and what should you do before trying to resolve the conflict?

## Quiz

1. Is cleanup enabled by default for a fresh `squad watch` with no capability configuration?
2. Does cleanup archive old logs under `.squad/logs/archive/` in v2.0.0?
3. What determines whether an entry in `.squad/log/` is old enough for pruning?
4. Does successful `squad upgrade --self` also run `squad upgrade` in the current repo?
5. Which areas are refreshed by a repository upgrade: team histories or manifest-listed Squad-owned templates?
6. Are customized built-in skills backed up automatically when overwritten?
7. What two conditions make `squad upgrade --migrate-directory` refuse to rename?
8. Why is a standalone `squad upgrade --dry-run` safer than combining it with `--migrate-directory`, and what does `squad upgrade --self --dry-run` do?

## Further Reading

- [Cleanup Watch](https://github.github.com/squad/docs/features/cleanup/)
- [Self Upgrade](https://github.github.com/squad/docs/features/self-upgrade/)
- [Migration Guide](https://github.github.com/squad/docs/get-started/migration/)
- [Upgrading Squad](https://github.github.com/squad/docs/scenarios/upgrading/)
