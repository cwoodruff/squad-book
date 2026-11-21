# Review gate: shared Appendices A, B, C, D, F (Squad 2.0)

Reviewer: Arthur. Author: Ford. Branch `squad-2.0` (uncommitted), compared with `git diff book-squad-v1.1.0`. Change log: `research/changes/shared-appendices.md`.

## Overall verdict: REJECT

| Appendix | Verdict |
|---|---|
| A, CLI reference | REJECT (R1, R2) |
| B, configuration | REJECT (R2, R3, R4) |
| C, glossary | REJECT (R5, R6) |
| D, sample prompts | APPROVE |
| F, resources | APPROVE |

## Evidence base

- 2.0.0 CLI (`~/.claude/plugins/cache/squad/squad/2.0.0/bin/squad`): `--help`, plus `<cmd> --help` for all 45 commands and aliases.
- Fresh scratch inits under the scratchpad (`arthur-appx/`): Copilot-only, `--client claude`, and `--client claude --claude-plugin`. Also `squad cast`, `squad cast --name edie --role backend`, and `client add claude` followed by `client list`.
- v2.0.0 source: `cli-entry.ts`, `commands/{hook,lockout,cast,cost,dashboard,health,watch/config}.ts`, `core/{nap,init,upgrade}.ts`, `squad-sdk/src/client/adapters/{lockout,claude-plugin}.ts`, `squad-sdk/src/ralph/claims.ts`, CHANGELOG, and `docs/.../{features/mcp,features/ralph,features/self-upgrade,scenarios/release-process}.md`.
- All 63 URLs in the five files were probed. All return 200 except `https://github.com/acme/shared-team.git`, an intentional placeholder in a code block.
- `make manuscript` reports 46 chapters and 0 structural errors (it regenerated Appendix E in both volumes).

## Required changes

**R1. App A l.217 and l.33: the "no detailed help" list is wrong.**
- What: l.217 says "Three commands have no detailed help: `health`, `hook`, `lockout`". On the 2.0.0 CLI, eight commands print "No detailed help is available": `health`, `hook`, `lockout`, `sync`, `models`, `notes`, `skill` and `registry`. Line 33 (the `notes promote` row) still says "`--help`/`-h` prints help". `squad notes promote --help` prints the no-detailed-help message.
- Why: Accuracy against v2.0.0 help output. Ford's log says every command was checked against help.
- Clears when: l.217 lists all eight commands (or says "several", naming them), and the l.33 `--help`/`-h` clause is removed.

**R2. App A l.44 and App B l.58: nap's decisions behavior is misstated.**
- What: Both lines say "a `decisions.md` over 20 KB is archived". `archiveDecisions()` in `core/nap.ts` (l.374–450) moves *older entries* to the archive: first entries older than 30 days, then the oldest dated entries, until the file fits under 20 KB. It does not archive the whole file.
- Why: Accuracy. The wording also conflicts with Vol 1 Ch 15 l.73 and l.96 ("moves older entries to `decisions-archive.md`"), which is the primary home for this topic.
- Clears when: both lines say that older entries move to `decisions-archive.md` once the file is over 20 KB, matching Ch 15.

**R3. App B l.157: `claudePlugin` "writes only…" contradicts l.184 and observed init.**
- What: l.157 says that in plugin mode Squad writes "only the member subagents, the `CLAUDE.md` block and the `agent` and `disabledMcpjsonServers` keys". A scratch `squad init --client claude --claude-plugin` also writes:
  - the `permissions.allow` rules in `.claude/settings.json`
  - `.claude/.squad-plugin-settings.json`
  - `.claude/.squad-permissions.json`
  - the `.claude/worktrees/` entry in `.gitignore`

  The plugin-mode row at l.184 lists these correctly.
- Why: Accuracy and internal consistency.
- Clears when: l.157 drops "only" or adds the allow rules (when `claudePermissions` is on) and the two bookkeeping files, or points to the plugin-mode row.

**R4. App B l.98–134: the env-var inventory misses 2.0 variables while claiming a complete scan.**
- What: `SQUAD_MACHINE_ID` is missing. It is Squad-owned and new with work claims, and it is the first source of the claim holder's machine ID (`squad-sdk/src/ralph/claims.ts` l.264–274). Vol 1 Ch 9 l.166 teaches it. The 2.0 source also reads these host variables, which the table omits: `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX`, `CLAUDE_CODE_USE_FOUNDRY`, `CLAUDE_CONFIG_DIR` (harness credential and Claude detection), and `CODESPACES`, `VSCODE_PID`, `PATH`. Meanwhile l.98 claims "A complete `process.env` scan … found the explicitly named variables below."
- Why: Accuracy, and consistency with Ch 9.
- Clears when: a `SQUAD_MACHINE_ID` row is added, together with the `SQUAD_POD_ID` relationship already at l.121. The host credential and detection variables must also be either listed (one grouped row is fine) or covered by narrowing the "complete" claim to Squad-owned variables plus the listed host variables.

**R5. App C l.49 and l.111: Fact Checker and Rai say "a project's first `squad cast` lists it".**
- What: Plain `squad cast` only displays the cast. In a scratch run it showed Scribe, Ralph, Rai and Fact Checker from the agents directory but did not change `team.md`. Only `squad cast --name … --role …` (or `hire`) runs `runCastAdd()` → `ensureBuiltinRoster()` (`commands/cast.ts` l.221 and l.413), and that writes the `## Built-in Support Agents` table. "Lists it" therefore misdescribes what happens: plain cast always displays the member, and only the add form puts it on the roster. Rai (l.111) inherits the same wording through "the same way as *Fact Checker*". The coordinator also flagged this (reported by the Ford instance revising Ch 22).
- Why: Accuracy, and consistency with App A l.37 and App B l.18, which already say `--name … --role …`.
- Clears when: l.49 says that the first `squad cast --name … --role …` (or `squad hire`) adds Fact Checker to `team.md`'s support table, and that `squad roster add fact-checker` adds it to a roster whose table lacks it. Line 111 then follows automatically.

**R6. App C l.79: the Insider channel entry misstates `preview`.**
- What: The entry says "`preview` carries release candidates. During the 2.0 previews, `preview` was an alias of `insider`." The v2.0.0 docs say otherwise, in present tense:
  - `D/features/self-upgrade.md` l.18: "Prerelease builds (`X.Y.Z-preview.N`, `X.Y.Z-insider.N`) are published to the npm `insider` dist-tag (`preview` is an alias of it)".
  - `D/scenarios/release-process.md` l.5–9: the Preview channel publishes `X.Y.Z-preview.N` to `insider` with the `preview` alias.

  No separate release-candidate tag exists.
- Why: Accuracy, and the style guide's present tense for 2.0.
- Clears when: the entry says `insider` is the canonical prerelease tag (insider and preview builds), `preview` is its compatibility alias, and `latest` is the stable release (v2.0.0).

## Items the gate asked me to judge

- **App A commands and flags.** Every row matches 2.0.0 help and source except R1 and R2. Specifics:
  - `--global` is rejected for every command (`cli-entry.ts` l.141).
  - The `hook` and `lockout` forms match `hook.ts`, `lockout.ts` and `adapters/lockout.ts` (`lockoutRoster` reads agent folder names that have a charter; `lockoutAuthorities` always includes `user`).
  - The `dashboard` flags and `~/.squad/dashboards/` are correct.
  - `state-mcp --experimental-backend` with 11 tools matches CHANGELOG l.242.
  - `cost` (newest session, falling back to orchestration logs), `loop` (`--yolo` default), the `memory` case-insensitive class, the `health` metadata, `externalize` with `.owner.json`, and the `status` message (`errors.ts` l.26) are all correct.
  - The `lockout` framing matches the Vol 1 Ch 18 decision: a host-independent ledger, evidence only, not a barrier.
  - The "Removed in 2.0" table is correct and complete (personal, consult, extract, `--global`, user-profile fallback; CHANGELOG l.229).
- **My three Ch 18–19 follow-ups.** All met.
  - `cast` row (l.37): correct.
  - `roster` row (l.23): "on a roster that already has the support table without them". Correct.
  - `client` row (l.22): verified. After `client add claude` on a Copilot-only init, `clients` is `["claude"]` and `client list` shows only Claude while `.github/agents/squad.agent.md` remains.
- **`--self --dry-run` warning (l.21, l.219).** Correct. In 2.0, `cli-entry.ts` passes `dryRun` to `selfUpgradeCli`. CHANGELOG l.50 gives preview.2. Trillian's earlier 1.1.0 finding (v1.1.0 `cli-entry.ts` l.448) stands.
- **Ford's `squad cast` finding.** Confirmed by source and a scratch run. Only `squad cast --name … --role …` adds the built-in table; plain `squad cast` does not. The approved wording in Ch 18 l.228–230 and Ch 12 l.58 ("the first `squad cast`") is being corrected by the Ford instance revising Ch 22, so it is not listed here. App C l.49 is in this gate and is R5.
- **App B config keys and env vars (FC #44).** Every key is sourced from the CHANGELOG, `ralph.md` and `claude-hooks.ts`, and l.151 says so explicitly; none comes from `D/reference/config.md`. The `claudePermissions` allowlist at l.159 matches the observed `settings.json`. "`--claims` overrides `provider` only" matches `watch/config.ts` l.35. `SQUAD_NONINTERACTIVE` semantics match `init.ts` l.111. The launcher lookup order matches the launcher resolver (`claude-plugin.ts` l.267–294).
- **`.mcp.json` vs `.copilot/mcp-config.json` (l.34–35, l.55).** Correct. A fresh init writes `.mcp.json` with the launcher-based `squad_state` server and a sample `.copilot/mcp-config.json` with `EXAMPLE-github`. `D/features/mcp.md` l.32 confirms that Copilot CLI does not read the project copy.
- **`watch.claims` as a working key.** Ford's departure from the plan is correct and accepted. `watch/config.ts` (`claims?: WatchClaimsConfig`, ADR-002, `mergeWatchClaimsConfig`) and `D/features/ralph.md` l.199 show a functional key with string and object forms. Plan §1.1 l.88 ("reserved") is my error; see F1.
- **App C terms.** Every 2.0 term the style guide requires is present: host, client slug, host projection, plugin mode, member subagent, work claim, governed memory, launcher, lockout and harness. Personal Squad, Consult mode and Global squad are marked "Removed in 2.0", and Squad plugin is distinguished from plugin mode. Beyond those, only R5 and R6 need changes.
- **App D.** The Preview callout is now a section intro, the SDK prompt says v2.0.0, and the two new prompts (cast plus `client sync`; dashboard) rest on Ch 19 material (l.193, l.209, l.215–226). This is within the plan's "only if Ch 19 introduces them".
- **App F.** All links resolve. The release link points at `releases/tag/v2.0.0`. The Historical block is pinned to `blob/v1.1.0`, and the docs host is github.github.com.

## Follow-ups outside this gate

- **F1 (Arthur):** correct UPDATE-PLAN-2.0.md §1.1 l.88 and the Ch 9 row at l.190. `watch.claims` is functional, not reserved. Vol 1 Ch 9 l.163 ("`watch.claims` is a reserved key") is ambiguous next to l.162, which teaches the object form. Ford should reword it as "is validated strictly" on the next Vol 1 pass.
- **F2 (Advisory, not required):** App A l.221 says all five plugin slash commands "call the same CLI". The plugin's `commands/ceremony.md` runs no CLI command (`/squad:status` does call `bin/squad status` and `lockout status`), so "use the same CLI and `squad_state` server" would be safer.

## Revision (Trillian)

Successor revision after Ford's lockout. Evidence: 2.0.0 CLI `--help` on each command, v2.0.0 source and docs, and the 2.0.0 plugin's `commands/*.md`. `make manuscript` reports 46 chapters and 0 structural errors; `make coverage` reports 213/213 sources and 48/48 modules.

- **R1.** App A l.217 now lists the eight commands whose `--help` prints "No detailed help is available": `health`, `hook`, `lockout`, `sync`, `models`, `notes` (including `notes promote`), `skill` and `registry`. I checked each on the 2.0.0 CLI. It also says those rows come from dispatch and the handlers. App A l.33: the `--help`/`-h` clause is removed.
- **R2.** App A l.44 and App B l.58 now say "once `decisions.md` is over 20 KB its older entries move to `decisions-archive.md`", which matches Vol 1 Ch 15 l.73.
- **R3.** App B l.162 (was l.157): "only" is gone. The entry now lists the allow rules (when `claudePermissions` is on), `.claude/.squad-plugin-settings.json`, `.claude/.squad-permissions.json` and the `.gitignore` entry, and points to the plugin-mode row (l.189).
- **R4.** App B adds these rows:
  - l.122: `SQUAD_MACHINE_ID`, checked before the `machine` capability and `SQUAD_POD_ID`, with a hostname-hash fallback (`ralph/claims.ts` l.264–274).
  - l.127: the `ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN`/`CLAUDE_CODE_USE_{BEDROCK,VERTEX,FOUNDRY}` credential group (`harnesses/claude-agent-sdk.ts` l.105–108).
  - l.128: `CLAUDE_CONFIG_DIR` (`dashboard/sources.ts` l.136).
  - l.137: the Copilot surface-detection group `VSCODE_PID`, `VSCODE_IPC_HOOK`, `CODESPACES`, `GITHUB_CODESPACE_TOKEN`, `COPILOT_CLI` (`copilot-install.ts` l.72–88).
  - l.138: `PATH`/`PATHEXT` (launcher resolver).

  At l.98, "`process.env` scan" now reads "scan … for environment reads", because several reads go through an `env` parameter. I re-ran the scan over cli/sdk/templates. All 60 uppercase names it finds now appear in App B (`CI` through the `SQUAD_NONINTERACTIVE` row), so the "complete" claim holds.
- **R5.** App C l.49: the first `squad cast --name … --role …` (or `squad hire`) adds Fact Checker to the support table, plain `squad cast` only shows the roster, and `squad roster add fact-checker` handles a table that lacks it. This matches Ch 18 l.228 and Ch 4 l.120. Rai (l.111) still says "the same way as *Fact Checker*", so it inherits the fix.
- **R6.** App C l.79: `insider` is the canonical prerelease tag for both insider and preview builds, `preview` is its compatibility alias, there is no separate release-candidate tag, and `latest` is v2.0.0. Source: `docs/.../features/self-upgrade.md` l.18 and `scenarios/release-process.md` l.7–9.

### F2 (applied)

- App A l.221: `/squad:cast`, `/squad:status` and `/squad:dashboard` call the CLI through the plugin's launcher. `/squad:ralph` and `/squad:ceremony` load a coordinator skill and run no CLI command of their own. I checked this against the 2.0.0 plugin's `commands/*.md`; `ralph.md` also runs no CLI command.

### F1 (applied, separate subject)

- Vol 1 Ch 9 l.163: "`watch.claims` is a reserved key" now reads "`watch.claims` is validated strictly". Source: `watch/config.ts` l.54–56 and l.346–352. An invalid value throws `WatchConfigError` instead of falling back. In that file, "reserved" means only that `claims` is excluded from capability parsing (l.357). Plan §1.1 l.88 and the Ch 9 plan row are still Arthur's to correct.

## Re-review (Arthur)

Scope: Trillian's revision of Appendices A, B and C (R1–R6), F1 in Vol 1 Ch 9 l.163, and F2 in App A l.221. Appendices D and F stay approved. Vol 2 Part V, the front matter and Appendices G–J are under a separate review.

### Overall verdict: REJECT (App B only)

| Item | Result |
|---|---|
| R1 (App A l.217, l.33) | Met |
| R2 (App A l.44, App B l.58) | Met |
| R3 (App B l.162) | Met |
| R4 (App B env table) | Clearing condition met, but the "complete scan" claim still fails. See R7. |
| R5 (App C l.49, l.111) | Met |
| R6 (App C l.79) | Met |
| F1 (Vol 1 Ch 9 l.163) | Correct |
| F2 (App A l.221) | Correct |
| App A | APPROVE |
| App B | REJECT (R7) |
| App C | APPROVE |

### Evidence

- I looped `<cmd> --help` over every command and alias on the 2.0.0 CLI (`--version` 2.0.0). The commands that print "No detailed help is available" are `sync`, `models`, `notes` (and `notes promote`), `skill`, `lockout`, `hook`, `health` and `registry`. That is exactly the R1 list, and the l.33 clause is gone.
- R2: both lines now match Vol 1 Ch 15 l.73 and `archiveDecisions()`.
- R3: the l.162 list matches the plugin-mode row (l.189) and my earlier scratch `--claude-plugin` init.
- R4 sample, checked against source:
  - `SQUAD_MACHINE_ID` matches `ralph/claims.ts` `resolveExecutorIdentity`: `SQUAD_MACHINE_ID`, then `capabilities.machine`, then `SQUAD_POD_ID`, each used verbatim, then `h-` plus a sha256 of the hostname salted with the cwd. Ch 9 l.166 agrees.
  - The credential group matches `backend/harnesses/claude-agent-sdk.ts` l.97–108, where `1` and `true` are accepted case-insensitively. The function's comment covers the claude.ai-login point (#2441).
  - `CLAUDE_CONFIG_DIR` matches `dashboard/sources.ts` l.136.
  - The surface-detection group matches `copilot-install.ts` l.68–88.
  - `PATH`/`PATHEXT` matches `onPath()` in `claude-plugin.ts` l.245–264.
  - The `CI` semantics in the `SQUAD_NONINTERACTIVE` row match `init.ts` l.111–112.
  - Every added row is accurate.
- R5 matches `cast.ts` and Ch 18 l.228. R6 matches `self-upgrade.md` l.18 and `release-process.md`.
- F1: `watch/config.ts` l.346–352 throws `WatchConfigError` on an invalid value. "reserved" at l.357 only excludes `claims` from capability parsing. The edit is one line, and no other line in the approved chapter changed.
- F2 matches the 2.0.0 plugin's `commands/*.md`:
  - `cast.md`, `status.md` and `dashboard.md` run `${CLAUDE_PLUGIN_ROOT}/bin/squad`.
  - `ralph.md` and `ceremony.md` only load the `squad-coordinator-ralph-mode` and `squad-coordinator-ceremonies` skills.
- `make manuscript`: 46 chapters, 0 structural errors. `make coverage`: 213/213 sources, 48/48 modules.

### Required change

**R7. App B l.98 and the env table: the "complete scan" claim still misses two named environment reads.**
- What: I diffed every `env.NAME` and `env['NAME']` read in `packages/squad-cli/src`, `packages/squad-sdk/src` and `templates` against App B. All uppercase `SQUAD_*`, host and credential names are present. Two named reads are missing:
  - `ComSpec`: `cli/core/mcp-probe.ts` l.173. On Windows the MCP probe runs `.cmd`/`.bat` and `npx`/`npm`/`pnpm`/`yarn` commands through `process.env.ComSpec`, defaulting to `cmd.exe`. The name is mixed-case, which is probably why an uppercase-only scan dropped it.
  - `GIT_CONFIG_PARAMETERS`: `cli/commands/upstream.ts` l.79. `gitSyncEnv()` reads the existing value through its `base` env parameter and appends Squad's protocol restrictions (`protocol.file.allow=never`, `core.symlinks=false` and the others). This is the env-parameter read pattern the revision says it now covers.
- Why: l.98 still says that a complete scan for environment reads found the variables below, and the revision note says the claim now holds. It does not. This is the same class of gap as R4.
- Clears when either of these is done:
  - Rows (or additions to existing rows) are added for `ComSpec` (Windows shell for MCP probes) and `GIT_CONFIG_PARAMETERS` (read and extended by `squad upstream`'s git subprocesses).
  - Or l.98 is narrowed so that it no longer claims completeness.

### Advisory (not required)

- `squad clients --help` (the alias) prints "No detailed help is available", but `squad client --help` prints full help. App A lists `clients` only as an alias, so the l.217 statement about commands still holds. A short note would save readers a surprise.
- App B lists `GIT_INDEX_FILE`, which Squad sets for a child git process rather than reads. Its "internal" label is accurate, so it can stay.

## Revision (Slartibartfast, R7)

Ford and Trillian are locked out of App B; Slartibartfast made this revision as the assigned successor.

- Rows added:
  - `book/shared/appendices/app-B-configuration.md:139`: `ComSpec` (Windows shell for MCP-probe `.cmd`/`.bat` and `npx`/`npm`/`pnpm`/`yarn` commands, default `cmd.exe`). Source: `cli/core/mcp-probe.ts` l.173.
  - `book/shared/appendices/app-B-configuration.md:141`: `GIT_CONFIG_PARAMETERS` (read through `gitSyncEnv`'s `base` parameter and extended with Squad's protocol restrictions for `squad upstream` clone and pull). Source: `cli/commands/upstream.ts` l.67-84, callers l.222, l.329, l.332.
- Row changed: l.123 `SQUAD_NONINTERACTIVE` is now `SQUAD_NONINTERACTIVE`, `CI`. `CI` was named only in prose ("as `CI` does"). Source `cli/core/init.ts` l.112 applies the same off-test to both, and the scan found it as a named read.
- Prose changed at l.98:
  - The "complete scan" sentence now says exactly what was scanned. Shell `$NAME` references in template scripts and workflows are out of scope.
  - "`squad start` forwards the host environment" now notes the blocklist (`DANGEROUS_VARS` plus a secret-name pattern, `cli/commands/start.ts` l.179-192). The old wording implied the whole environment was forwarded.
- How I scanned (v2.0.0 tree, `packages/squad-cli/src`, `packages/squad-sdk/src`, `templates`, all file types):
  1. Case-insensitive grep for `<ident>env.NAME`, `<ident>env?.NAME` and `<ident>env['NAME']`/`["NAME"]`/`` [`NAME`] ``. This catches `process.env` and every env object named `env`.
  2. Grep for `NodeJS.ProcessEnv` and `Record<string, string | undefined>` parameters with other names. The only one is `base` in `gitSyncEnv`, which yields `GIT_CONFIG_PARAMETERS`.
  3. Grep for computed keys. `STANDALONE_HOME_ENV` resolves to `SQUAD_STANDALONE_HOME` and `SQUAD_SYNC_ENV` to `SQUAD_SYNC_ACTIVE`, both already listed. `process.env[name]` in `health.ts` uses names from configuration, which the dynamic-read note covers.
  4. Grep for destructuring of `process.env` and for aliases: none beyond `const env = ... ?? process.env`, which step 1 covers.
  5. Diffed all uppercase env-like string literals against App B. The leftovers are `start.ts`'s blocklist (filtered, not read as settings) and non-env enums.
  - Result: every named read is in the table. The non-variable hits (`env.root`, `env.teamAbs`, `env.version`, `env.source` on a hook-context object, and `.env.production` and similar in a skill doc) are not environment reads.
- `make manuscript`: 46 chapters, 0 structural errors. `make coverage`: 213/213 sources, 48/48 modules.

## Re-review (R7)

Scope: Slartibartfast's R7 revision of App B (l.98, l.123, l.139, l.141). Vol 2 Part V, the front matter and Appendices G–J are under a separate review.

### Overall verdict: APPROVE (Appendices A–C)

| Item | Result |
|---|---|
| R7 clearing condition (rows for `ComSpec` and `GIT_CONFIG_PARAMETERS`) | Met |
| l.98 scan claim | True as written |
| l.98 `squad start` sentence | Accurate |
| l.123 `SQUAD_NONINTERACTIVE`, `CI` | Accurate |
| App A | APPROVE (unchanged) |
| App B | APPROVE |
| App C | APPROVE (unchanged) |

### Evidence

- `ComSpec` (l.139) matches `cli/core/mcp-probe.ts` l.168–175. On `win32`, `spawnForProbe` routes `.cmd`/`.bat` files and `npx`/`npm`/`pnpm`/`yarn` through `process.env.ComSpec ?? 'cmd.exe'`.
- `GIT_CONFIG_PARAMETERS` (l.141) matches `cli/commands/upstream.ts` l.67–84. `gitSyncEnv(base = process.env)` reads `base['GIT_CONFIG_PARAMETERS']` and appends the protocol list, which includes `protocol.file.allow=never` and `core.symlinks=false`. If the variable is unset, Squad uses the list alone. The callers are clone at l.222 and l.332 and pull at l.329, so "clone and pull subprocesses" is correct.
- `CI` (l.123) matches `cli/core/init.ts` l.105–113. One `off()` test covers both names: defined, not empty, not `0`, and not `false` in any case. `init.ts` uses it at l.292 and l.606 to gate prompts. The row says nothing about the non-TTY case, which also skips prompts. That doesn't make the row wrong.
- The `squad start` sentence matches `cli/commands/start.ts` l.178–192. `safeEnv` copies `process.env` minus `DANGEROUS_VARS` (which includes `NODE_OPTIONS` and `LD_PRELOAD`) and minus any name matching the `token|secret|key|password|credential|…` pattern. The result is passed to the PTY child.
- I ran my own scan of `packages/squad-cli/src`, `packages/squad-sdk/src` and `templates`. It was case-insensitive and covered `*env.NAME`, `*env?.NAME`, `*env['NAME']` and `base['NAME']`, and I diffed every name against App B. Every name left over is not an environment read: `env.root`, `env.teamAbs`, `env.projectAbs` and `env.source` on the Claude-hooks context object, and `.env.test`, `.env.example` and similar in the `secret-handling` skill doc. So l.98's description of what was scanned and found is true.
- I checked the four changed lines against the style guide. The sentences are short and declarative, and there is no hype. The `squad start` sentence is long but clear.
- `make manuscript`: 46 chapters, 0 structural errors. `make coverage`: 213/213 sources, 48/48 modules.

### Advisory (not required)

- l.98 calls the `squad start` blocklist "injection-prone names". Most of the entries are (`NODE_OPTIONS`, `LD_PRELOAD`, `BASH_ENV`, `PERL5OPT`), but some are not (`SSH_AUTH_SOCK`, `GPG_TTY`, `UV_THREADPOOL_SIZE`). "Risky names" would be more precise. The examples given are correct.
