# End-to-end checks: Squad 2.0.0 edition

Run by: Marvin. Date: 2026-11-21. Branch `squad-2.0` (uncommitted chapters, read as they stood today). CLI 2.0.0: `/Users/cwoodruff/.claude/plugins/cache/squad/squad/2.0.0/bin/squad`. CLI 1.1.0: installed under an isolated `npm --prefix`. All runs used scratch copies of `sample/` under the session scratchpad (`e2e-a`, `e2e-b`, `e2e-c`), with `HOME` pointed at a scratch folder so no user-level file was touched. Nothing was installed globally. No `upgrade --self` was run with any CLI.

Sandbox note: Node's built-in `https` ignores the sandbox proxy, so a 1.1.0 `squad init` without `NODE_USE_ENV_PROXY=1` cannot reach the npm registry, and it writes `@bradygaster/squad-cli@insider` instead of `@1.1.0` (v1.1.0 `cli/core/mcp-spec.ts` falls back to `@insider` when the registry probe fails). With the proxy enabled it pins `@1.1.0` as the book says. Readers on an offline machine would see `@insider` too.

| Check | Result |
|---|---|
| a. Vol 1 Ch 3 init tree | **PASS** |
| b. Vol 2 Ch 22 migration drill | **FAIL** (2 accuracy errors on A5, 1 minor) |
| c. Vol 2 Ch 19 Git removal route | **PASS** |
| d. Tasktrack tests | **BLOCKED** by the sandbox (local port binding) |

## a. Vol 1 Ch 3: real `squad init` vs the annotated tree: PASS

I ran a 2.0.0 `squad init` (non-interactive) in a fresh Git copy of `sample/` tagged `ch02-start`. The result matched Ch 3 l.59 and l.73–140:

- Output began with "Let's build your team." It reported `squad_state` installed to `.mcp.json` through `node .squad/squad.mjs (repository launcher …)`, removed the stale `squad_state` from `.copilot/mcp-config.json`, created `.vscode/settings.json` with `chat.newSession.defaultMode: "Squad"`, created four workflows (heartbeat, issue-assign, triage, sync-labels), skipped `@copilot` setup, and ended with `copilot --agent squad`.
- Every file in the "State files" table exists with the described content: `config.json` is `{"version": 1}`; `decisions.md` says "No decisions recorded yet."; `team.md` has only the coordinator row; the casting registry has `agents: {}` at revision 1 with a `transaction_id`; memory `defaultProvider: "local"` with the host-injected adapter disabled and `requireApproval: true`; lowercase `agents/rai/`; `squad.mjs`; and the empty dirs `decisions/inbox`, `log`, `orchestration-log`, `plugins`, `.scratch` and `memory/{local,policy-inbox,semantic-inbox,tombstones}`.
- The `.squad/templates/` listing (120 files) matches the template table file for file. The only file the table omits is the hidden `.squad/templates/.shipped-manifest.json`.
- The beside-`.squad/` table matches: `.github/agents/squad.agent.md`, `.github/skills/` (19 skills), the 4 workflows, `.mcp.json` (`node -e` root finder → `.squad/squad.mjs state-mcp`), `.copilot/mcp-config.json` with `EXAMPLE-github`, `.vscode/settings.json`, `.gitattributes`, and `.gitignore` with the six runtime entries plus `.squad-workstream`.
- Minor wording, not a failure: the actual tip at l.59 reads "for non-interactive scripts that need squad_state tools, add to package.json: `"squad:copilot": "copilot --agent squad --additional-mcp-config @.mcp.json"`". The chapter paraphrases it as a bare command.

## b. Vol 2 Ch 22 Hands-On (`book/vol2/part-04/ch22-upgrading-to-2.md` l.356–460): FAIL

| Step | Expected (book) | Actual | Result |
|---|---|---|---|
| 1 clone at `ch02-start` | Clean tree, no `.squad/` | Clean, no `.squad/` | Pass |
| 2 isolated 1.1.0 | `1.1.0` and `2.0.0` | `1.1.0` and `2.0.0` | Pass |
| 3 1.1.0 init + tag | 1.1.0 `.squad/`, `squad.agent.md`, `.mcp.json` with `npx -y @bradygaster/squad-cli@1.1.0 state-mcp` | As expected (with registry access; see the sandbox note). `.squad/agents/Rai` is capitalized. | Pass, but l.392's "uncast team only adds doctor and health warnings" is wrong (F1) |
| 4 dist-tags | `latest` 2.0.0 | `latest: '2.0.0'`, `insider: '2.0.0'`, `preview: '2.0.0-preview.4'` | Pass |
| 5 `upgrade --dry-run` | Planned updates and backups, ends with "Run without --dry-run", empty status | "previewing upgrade from 1.1.0 → 2.0.0", 31 files (19 overwrite, 12 create, 17 backups), `.gitattributes` +1, `.gitignore` +`.squad/backend/`, "Run without --dry-run to apply.", empty `git status` | Pass |
| 6 `upgrade` and inspect | Coordinator, skills, workflows and templates change; `.mcp.json` → `node -e … .squad/squad.mjs state-mcp`; launcher exists; `.gitignore` +`.squad/backend/`; backups to review | All true. `Rai/` → `rai/` via `git mv`; 18 `.local-backup` files (including `squad.agent.md.local-backup` on an unmodified 1.1.0 coordinator); no `handwritten-archive-*`; 7 extra workflows created. `npm test` could not run (see d). | Pass (tests blocked) |
| 7 `--client claude` | Dry run lists Claude projection changes; apply records `claude` in `clients[]` and creates the host files | Dry run prints only "Would project client host files for: claude" with no file list. Apply: `clients: ["claude"]`, 64 Claude files, `CLAUDE.md`, `.gitignore` `# squad:claude` / `.claude/worktrees/`; `.mcp.json` untouched. `client list` then shows only `claude`. | Pass, minor wording (F3) |
| 8 doctor/health/status | `doctor` passes portable launch; non-zero "only if a check failed (an uncast team fails the team checks)"; health has `resolvedTeamRoot`/`resolvedSquadDir` under `metadata` | `doctor`: 14 passed, 0 failed, **0 warnings**, exit **0**, including the portable `squad_state` launch. `health --json`: metadata fields present, `status: "fail"`, exit **1**, with fails on `team`, `registry-charters` and `routing`. `status` and `git diff --check` are clean. | **Fail** (F2) |
| 9 rollback | Back at 1.1.0; 1.1.0 doctor reads it | `git clean -nd` lists only drill outputs (`.claude/`, `CLAUDE.md`, 7 workflows, `squad.mjs`, backups, new templates, memory dirs). After reset and clean, `Rai/` is back and `.mcp.json` pins `@1.1.0`. 1.1.0 `doctor`: 10 passed, 0 failed, exit 0. | Pass |
| 10 cleanup | n/a | n/a | Pass |

**Arthur's A5 (uncast team: doctor warnings or failures?):** neither. On an uncast team, `squad doctor` reports **no warnings and no failures** and exits 0. `squad health --json` is where the uncast team shows up, as **failures** (not warnings): `team` ("team.md has no parseable members"), `registry-charters` ("casting/registry.json must contain at least one agent") and `routing` ("routing.md has no parseable routing rules"). It exits 1.

Failures:

- **F1** `book/vol2/part-04/ch22-upgrading-to-2.md:392`. Expected (book): "an uncast team only adds `doctor` and `health` warnings later". Actual: `doctor` adds nothing (0 warnings, 0 failures, exit 0), and `health` reports three **failures** and exits 1.
- **F2** `book/vol2/part-04/ch22-upgrading-to-2.md:445`. Expected (book): `doctor` exits non-zero "only if a check failed (an uncast team fails the team checks)". Actual: on the uncast drill team `doctor` exits 0. The failing team checks belong to `squad health` (exit 1). The fix: attribute the uncast-team failures to `health`, or tell readers that `health` exits 1 on an uncast team.
- **F3 (minor)** `book/vol2/part-04/ch22-upgrading-to-2.md:434`. Expected (book): "the dry run lists Claude projection changes". Actual: the dry run prints one line, "Would project client host files for: claude", with no file list. The fix: say that it names the hosts it would project.

Observation, not a failure: after step 7, `squad client list` shows only `claude`. Copilot drops out of the list, but its files remain. Ch 19 l.515 already explains this rule. Ch 22 could mention it in one clause.

## c. Vol 2 Ch 19 Git removal route (`book/vol2/part-04/ch19-across-clients.md` l.430–515): PASS

Setup: I copied the 2.0.0-initialized Tasktrack from (a) and committed it. `client list` showed Copilot only (l.442). Then I ran the steps as written:

- `git tag v2-ch19-baseline`. `client add claude,codex --dry-run` printed "Would project client host files for: claude, codex (nothing written: --dry-run)" and wrote nothing. Apply created `.claude/agents/{squad,scribe,ralph,rai,fact-checker}.md`, `.claude/settings.json` (only the scoped `squad_state` and `squad` allow rules), `.claude/skills/`, `CLAUDE.md`, `.codex/agents/squad.toml`, `.codex/config.toml`, `AGENTS.md`, `.gitignore` `# squad:claude` / `.claude/worktrees/`, and `clients: ["claude","codex"]`. `client list` showed Claude (63/63) and Codex (3/3) as projected. I committed per l.476–477.
- Removal (l.489–493): `git restore --source v2-ch19-baseline -- .gitignore` and `git rm -r --quiet .claude CLAUDE.md` both exit 0. I removed `claude` from `clients[]` → `["codex"]`.
- Checks (l.510–512): `git diff v2-ch19-baseline -- .claude CLAUDE.md .gitignore` is **empty**. The `.mcp.json` diff is empty, so the Copilot `squad_state` entry is retained (Claude's projection never edited `.mcp.json`). `client list` shows **only Codex**, as l.515 says. `client sync --dry-run` would refresh only codex, so Claude is not recreated. `doctor`: 14 passed, 0 failed.

The steps work as written. Note: `.claude/.squad-permissions.json` is also created and removed by `git rm -r .claude`. The chapter's file list does not mention it, but the route handles it.

## d. Tasktrack tests: BLOCKED (sandbox)

`npm test` (`node --test api/test/`) in the upgraded scratch copy ran for 60 s and was cancelled: "Promise resolution is still pending but the event loop has already resolved". Cause: the test's `before()` hook calls `server.listen(0)`, and the sandbox denies local port binding. A direct probe, `http.createServer().listen(0,'127.0.0.1')`, fails with `EPERM`. Per instructions I did not retry outside the sandbox. Setting `sandbox.network.allowLocalBinding: true` allows it. The test code itself is unchanged since 1.1, and `sample/` has no Squad dependency.

## Follow-up fixes (Trillian)

Reproduction (2.0.0 CLI, fresh uncast scratch team from `squad init`): `squad doctor` printed "13 passed, 0 failed, 0 warnings, 2 info" and exited 0. `squad health --json` returned `status: "fail"` and exited 1, failing `team` ("team.md has no parseable members"), `registry-charters` ("casting/registry.json must contain at least one agent") and `routing` ("routing.md has no parseable routing rules"). `squad upgrade --dry-run --client claude` printed "Would project client host files for: claude" with no file list. This matches F1 to F3.

- **F1** `book/vol2/part-04/ch22-upgrading-to-2.md:392`: now says that on an uncast team `doctor` reports no warnings or failures, but `squad health` reports the team checks as failures and exits 1.
- **F2** `book/vol2/part-04/ch22-upgrading-to-2.md:445`: `doctor` exits non-zero only if a check failed; an uncast team passes, so expect exit 0. The `squad health --json` sentence now says an uncast team fails `team`, `registry-charters` and `routing` and exits 1. The step already runs `squad health --json`, so no command changed.
- **F3** `book/vol2/part-04/ch22-upgrading-to-2.md:434`: the dry run names the host in one line, `Would project client host files for: claude`, and lists no files.

`exercises/solutions/vol2/ch22.md` needed no change; no answer depends on these lines. `make manuscript`: 46 chapters, 0 structural errors.

## Review (Arthur)

Date: 2026-11-21. Scope: Trillian's F1–F3 fixes in `book/vol2/part-04/ch22-upgrading-to-2.md` (l.392, l.434, l.445). I re-ran the CLIs in a fresh scratch clone of Marvin's `e2e-b/tasktrack-1x` (`arthur-e2e-rev`, scratch `HOME`). `make manuscript`: 46 chapters, 0 structural errors.

**Verdict: REJECT** (one required change, R1).

- **F3, l.434: approved.** The text matches v2.0.0 `packages/squad-cli/src/cli/core/upgrade.ts:1717` (`info(\`Would project client host files for: …\`)`), which prints one line and no file list. It also matches Marvin's run and Trillian's reproduction. The `(nothing written: --dry-run)` suffix belongs only to `client add/sync` (`client.ts:149`), so leaving it out here is correct.
- **F2, l.445: approved.** After steps 6–7, 2.0 `doctor` exits 0 on the uncast team (Marvin: 14 passed, 0 failed, 0 warnings). `health --json` fails `team`, `registry-charters` and `routing` and exits 1. Step 8 runs `squad health --json` and `doctor; echo "doctor exit: $?"`, so the commands and the expected output agree. Nothing in the block aborts on the exit 1 from `health`.
- **F1, l.392: REJECT (R1).** The old sentence said "adds … warnings **later**", which tied the claim to step 8. The new sentence drops that time anchor, so it now reads as a statement about the step-3 tree: "On an uncast team `doctor` reports no warnings or failures …". On that tree (tag `v2-ch22-start`, before the upgrade), the reader's global 2.0 `squad doctor` reports **1 failure** and exits **1**: `squad_state bridge — version mismatch: configured bridge reports 1.1.0, running CLI is 2.0.0`. Only `"$SQUAD11" doctor` is clean at this point (10 passed, exit 0). The 1.1.0 `health` fails the same three checks and exits 1. Because the sentence names bare `doctor`, a reader who checks at step 3 sees a contradiction. **Required:** scope the sentence to after the upgrade, for example "After the upgrade, an uncast team adds no `doctor` warnings or failures, but `squad health` reports the team checks as failures and exits 1." Alternatively, cross-reference step 8.

No other gaps: no other "uncast" claim in either volume or in the solutions conflicts with these lines, and `exercises/solutions/vol2/ch22.md` does not depend on them.

**Revision (Ford, R1):** `book/vol2/part-04/ch22-upgrading-to-2.md:392` now opens "After the upgrade, an uncast team adds no `doctor` warnings or failures, but `squad health` reports the team checks as failures and exits 1."

**Re-review (R1) (Arthur, 2026-11-21): APPROVE.** l.392 now reads "After the upgrade, an uncast team adds no `doctor` warnings or failures, but `squad health` reports the team checks as failures and exits 1." That is the clearing wording, and the `squad health` clause is unchanged. The sentence no longer conflicts with step 3, where the global 2.0 `doctor` reports the bridge version mismatch. `make manuscript`: 46 chapters, 0 structural errors.
