# Review: Vol 2 Part IV, Chapters 20–22 (Squad 2.0.0)

Reviewer: Arthur. Date: 2026-11-21. Author: Trillian (change log `research/changes/vol2-part4-ch20-22.md`). Branch `squad-2.0`, uncommitted, compared with `book-squad-v1.1.0`. Source: v2.0.0 and v1.1.0 trees in the session scratchpad (read only).

## Overall verdict: **REJECT**

Ch 20 and Ch 21 pass. Ch 22 has six required changes: four are accuracy errors found in source, one breaks the style guide, and one breaks the brief's Road Ahead standard.

| File | Verdict |
|---|---|
| `book/vol2/part-04/ch20-host-projections.md` | **APPROVE** (advisory A1, A4) |
| `book/vol2/part-04/ch21-state-boundary-backend.md` | **APPROVE** (advisories A2, A3) |
| `book/vol2/part-04/ch22-upgrading-to-2.md` | **REJECT** (R1–R6) |
| `exercises/solutions/vol2/ch20.md` | **APPROVE** |
| `exercises/solutions/vol2/ch21.md` | **APPROVE** |
| `exercises/solutions/vol2/ch22.md` | **APPROVE**. The Ex 7 answer describes the doctor check correctly. If R1 changes the Ex 7 premise, keep the answer consistent with it. |

`make manuscript`: 46 chapters, 0 structural errors. It regenerated both Appendix E files. Vol 2 App E was already modified in the working tree, and Vol 1 App E did not change.

## Specific items checked

| Item | Finding |
|---|---|
| 1.1.0 ignores `--dry-run` with `--self` | **Confirmed.** In v1.1.0 `cli-entry.ts`, l.415 parses `dryRun`, but l.448 calls `selfUpgradeCli({ insider, force: forceUpgrade })` without it. `core/upgrade.ts` l.1430–1452 then runs `execSync('npm install -g @bradygaster/squad-cli@latest')` unconditionally. In v2.0.0, l.481 passes `dryRun`, and CHANGELOG l.219 records the fix as first in preview.2. The rewritten Hands-On is the right shape: a scratch clone, 1.1.0 installed under `npm --prefix` (its `bin.squad` is `dist/cli-entry.js`, so `node_modules/.bin/squad` exists), and `npm view … dist-tags` instead of a dry run. R1 and R3 must still be fixed in it. |
| Ch 21 `executionAvailable` / `SQUAD_BACKEND_HARNESSES` | **Correct.** `backend-mcp.ts` l.164–185 sets `createLocalHarnesses` to default to `claude-agent-sdk`, which requires `isClaudeAgentSdkAvailable()` and `claudeApiCredentialsConfigured()`. `copilot-sdk` is registered only when it is listed, and `none` returns an empty registry. l.372 and l.402 set `executionAvailable` to `harnesses.length > 0`. The quoted credential function matches. See A2 and A3. |
| Ch 21 `casting/policy.json` | **Correct.** v1.1.0 `tools/index.ts` l.272 listed `casting/policy.json` as a mutable state path. The v2.0.0 `MUTABLE_STATE_PATHS` (l.310–321) contains nothing under `casting/`. |
| Ch 20 feature-matrix tables | **Correct.** I checked every cell against `test-fixtures/spec/suite-v0.2/host-feature-matrix.json`: 51 features and 5 expected failures. Claude has 44 S, 4 U and 3 n/a. Model selection is S for Claude only. Ralph CLI is S for Copilot and Claude and D for the rest. Dual-root is S for all hosts. Background is D for kiro, cursor, codex and antigravity. Specialist MCP inheritance is D for antigravity only. |
| Ch 20 ADR-003 framing | **Correct.** Status "Accepted (option C), 2026-11-13". Option B is an opt-in spike (#2488). The 43 sessions, the scenarios run without the Copilot file, Azure DevOps deferred, the Copilot snapshot guard and the separate Copilot-file decision all match the ADR (l.3, 10, 77, 106, 192–210). See A1. |
| Ch 20 lockout framing | **Matches** Ford's Vol 1 Ch 18 decision. The Claude dispatch section records transitions (`coordinator.ts` l.175), the Copilot coordinator does not, and the ledger is "evidence, not a write barrier". The allowlist (`claude-hooks.ts` l.220–231) matches: nine `squad_state` tools, plus `cast`, `client sync`, `lockout reject` and `lockout status`. |
| Ch 22 Road Ahead | The table rows trace to v2.0.0: `BACKEND_CONTRACT_STAGE = 'experimental'` (`backend/types.ts` l.14), ADR-003 #2488, the five `expectedFailures`, `features/gitlab-issues.md` "Planned, not shipped", and an empty `[Unreleased]`. No deleted proposal is linked. Two problems remain: R5 (the memory-governance sentence) and R6 (the work-claims row). |
| Length and minimal change | Word counts: Ch 20 went from 8,515 to 12,018 (+41%), Ch 21 from 7,239 to 9,725 (+34%), Ch 22 from 8,480 to 9,924 (+17%). The H2 skeletons are intact. Ch 20 adds the plan-mandated H2 "The Claude Projection, Version 3" (§3.2), and Ch 21's H2 rename is the one the plan specifies. The "## X-squad-host-claude" line is inside a code fence. STYLE-GUIDE l.54 allows Part IV reference chapters to run longer, and the growth tracks plan items P2–P14, so this is not a REJECT. See A4. |

## Required changes

### R1. Ch 22: l.128, l.392, l.495, l.543 (Ex 7). 1.x never wrote machine paths into `.mcp.json`

- **What:** The chapter says the first 2.0 upgrade replaces "a path on your machine" (l.128). It says the drill's 1.1.0 `.mcp.json` "starts Squad from a path on your machine" (l.392). It blames `portable squad_state launch` failures on "a teammate's 1.x upgrade" (l.495), and Ex 7 assumes a migrated repository fails the check (l.543). In v1.1.0, `mcp-spec.ts` l.113–150 plus `projectSquadStateMcpSpec` (l.46–53) write `npx -y @bradygaster/squad-cli@1.1.0 state-mcp` for an npm install (`@insider` if the registry probe fails) and a bare `squad state-mcp` for a standalone bundle. Neither is a machine path, and the v2.0.0 `checkPortableSquadLaunch` (`doctor.ts` l.760–788) passes both. The `node /…/cli-entry.js state-mcp` form came from the 2.0 previews (v2.0.0 CHANGELOG l.130, #2462).
- **Why:** Accuracy against v1.1.0 and v2.0.0 source. The drill's step 3 expectation is wrong for every reader.
- **Clears when:** l.128 says the entry is rewritten from the `npx -y @bradygaster/squad-cli@<version>` command (or bare `squad`) that 1.x wrote. l.392 expects `npx -y @bradygaster/squad-cli@1.1.0 state-mcp`. The l.495 symptom names a repository last written by a 2.0 preview, or a hand-edited config, not a 1.x upgrade. Ex 7's premise matches that cause. The solution's answer can stay.

### R2. Ch 22: l.132 and l.169. Rai and Fact Checker on a migrated roster

- **What:** l.132 says Rai and Fact Checker "join an existing roster only through `squad roster add`". l.169 kept the 1.1 wording that upgrade "does not insert them" and that you "explicitly opt them in". In v1.1.0 they were mandatory: the roster template `templates/roster.md` l.20–27 lists all four built-ins under `## Built-in Support Agents`, and `squad.agent.md` l.74–76 calls them "mandatory support identities". So a 1.x team cast through the coordinator already lists them, and upgrade leaves those rows. 2.0 `squad upgrade` scaffolds the missing charters (`ensureBuiltinAgents`, `core/upgrade.ts` l.1467–1496). 2.0 `squad cast` then adds the support table, including Rai and Fact Checker, to a `team.md` that has none (`commands/cast.ts` l.221–232 and l.413; `core/cast.ts` l.571–595). That happens to the drill's uncast 1.1.0 `squad init` project. This is the same fact as Ch 18 R2.
- **Why:** Accuracy against source, and consistency with the Ch 18 R2 correction.
- **Clears when:** Both places say three things. First, `squad upgrade` never edits `team.md`. Second, a team cast from the 1.1.0 template already lists all four built-ins. Third, a 2.0 `squad cast` adds the support table when `team.md` lacks one. `squad roster add` is presented as the path for a roster that has the table without them. Use the same wording as Ch 18 R2.

### R3. Ch 22: l.366 and l.370. The `ch03-start` tag does not exist in the reader's repository

- **What:** The drill branches from `ch03-start`. The book has readers create `ch02-start` (Vol 1 Ch 2 l.287; Ch 3 l.45), and no chapter tags `ch03-start`. STYLE-GUIDE l.65's `ch03-start` names the sample's baseline, not a tag in the reader's clone.
- **Why:** The command fails for every reader who follows the book (WRITER-BRIEF: keep the Tasktrack tags).
- **Clears when:** Steps 1 and 2 use `ch02-start`. The fallback to the `sample/` folder can stay.

### R4. Ch 22: l.231. Cross-volume reference form

- **What:** "(Chapter 18, Volume 1)".
- **Why:** STYLE-GUIDE l.72 requires `Chapter 18 (Volume 1)` from Volume 2.
- **Clears when:** It reads "(Chapter 18 (Volume 1))", or the row is reworded so the parentheses don't nest, for example "… `lockouts.json`; see Chapter 18 (Volume 1)."

### R5. Ch 22: l.505. "The memory-governance design became the governed `memory.*` store"

- **What:** The governed store predates the proposal. v1.1.0 already has `packages/squad-sdk/src/memory/index.ts` with the `TRANSIENT` and `FORBIDDEN` classes, plus the `memory.*` tools on `squad_state` (v1.1.0 `state-mcp.ts`, and the v1.1.0 CHANGELOG l.184 under 0.12.0). The `docs/proposals/memory-governance-provider.md` design (status "Design") described a provider layer above that store. The sentence also leans on a deleted proposal as its source, which the brief rules out.
- **Why:** Accuracy, and the brief's rule that no deleted proposals are cited.
- **Clears when:** The sentence is removed, or it says the governed store already shipped in 1.x (Chapter 21 and Chapter 15 (Volume 1)) without claiming the proposal produced it.

### R6. Ch 22: l.519. The work-claims row is not experimental or pending

- **What:** The row says "Shipped, but off by default". v2.0.0 describes claims as shipped opt-in behavior (CHANGELOG l.25–26, l.181), not as experimental or pending. The section's own intro (l.507) limits the list to what v2.0.0 "still calls experimental or pending".
- **Why:** The gate's Road Ahead standard and the plan (§3.2: rebuild from "explicitly experimental or pending items").
- **Clears when:** The row is removed. Vol 1 Ch 9 already covers claims.

## Advisories (not required by any standard)

- **A1. Ch 20 l.207.** Option A's outcome is "Rejected", but the ADR only records that C was chosen. "Not chosen" is closer to the source.
- **A2. Ch 21 l.239.** "With `copilot-sdk` listed and a signed-in Copilot user, … reports `["copilot-sdk"]`": registration does not check sign-in (`backend-mcp.ts` l.177–183). Sign-in matters only when a turn runs.
- **A3. Ch 21 l.358.** Setting `SQUAD_BACKEND_HARNESSES` to `copilot-sdk` replaces the default list, so it also drops `claude-agent-sdk`. One clause would prevent surprise for readers who have the Claude SDK configured.
- **A4. Ch 20 length.** At about 12,000 words, Ch 20 is at the upper bound of "Moderate", like Ch 19. Hold further additions to plan items.
- **A5. Ch 22 l.392 vs l.445.** One says an uncast team "only adds `doctor` and `health` warnings"; the other says it "fails the team checks". Marvin's end-to-end run should settle which is right. Then make both lines agree.

## Follow-up items outside this gate

- **F1 (Ford): Vol 1 Ch 14 and its solutions.** `book/vol1/part-02/ch14-upgrade-cleanup.md` l.82, l.93, l.104 and l.329, and `exercises/solutions/vol1/ch14.md` l.20 (Quiz 8), call `squad upgrade --self --dry-run` safe without naming a CLI version. That is true on 2.0, the chapter's target. The l.16 note sends 1.x readers to Ch 22 first. But none of these passages warns that the command installs for real on 1.1.0. Shared App A l.21 and l.219 already carry that caveat. Exact corrections:
  - l.104: replace "`--self --dry-run` is safe: it previews the install and returns." with "On a 2.0 CLI, `--self --dry-run` is safe: it previews the install and returns. A 1.1.0 CLI ignores `--dry-run` with `--self` and installs `@bradygaster/squad-cli@latest`; check the target with `npm view @bradygaster/squad-cli dist-tags` instead (Chapter 22 (Volume 2))."
  - l.82 row, third cell: "Prints the install command it would run; installs nothing (2.0 CLIs only; a 1.1.0 CLI installs)".
  - Solutions ch14 l.20: append "This holds on a 2.0 CLI; a 1.1.0 CLI ignores `--dry-run` with `--self` and installs." Then rerun `make manuscript` to regenerate Vol 1 App E l.148.
- **F2 (Marvin): run the Ch 22 drill end to end** after R1 and R3 are fixed. Confirm the 1.1.0 `.mcp.json` command, the doctor `portable squad_state launch` result before and after the 2.0 upgrade, A5, and the rollback.
- **F3 (Trillian): use one wording.** The Ch 18 R2 and Ch 22 R2 fixes must state the Rai and Fact Checker roster facts the same way.

## Revision (Ford)

Ford, 2026-11-21, as Trillian's assigned successor (Trillian locked out of Ch 22). `make manuscript`: 46 chapters, 0 structural errors; it regenerated Vol 1 App E (l.148 now carries the F1 caveat) and Vol 2 App E.

### Ch 22 (`book/vol2/part-04/ch22-upgrading-to-2.md`)

- **R1.** l.128: the entry is rewritten from the `npx -y @bradygaster/squad-cli@<version> state-mcp` command 1.x wrote (or bare `squad state-mcp` for a standalone bundle). l.392: step 3 expects `npx -y @bradygaster/squad-cli@1.1.0 state-mcp`. l.495: the symptom is a repository last written by a 2.0 preview CLI (`node /…/cli-entry.js state-mcp`) or a hand-edited config; the row says the 1.x forms pass. l.542 (Ex 7): premise is a teammate's 2.0-preview upgrade. A5 left for Marvin (F2).
- **R2.** l.132 and l.169: `squad upgrade` never edits `team.md`; a team cast from the 1.1.0 template already lists all four built-ins; a `team.md` with no support table gets one from the first 2.0 `squad cast --name <Name> --role "<Role>"`; `squad roster add` is for a roster that has the table without Rai or Fact Checker. Verified in v2.0.0 source: `cli-entry.ts` l.903–930 routes plain `squad cast` to `runCast` (shows the roster), and only `--name`/`--role` (or `hire`) reaches `runCastAdd`, which calls `ensureBuiltinRoster` (`commands/cast.ts` l.216–232, l.413).
- **R3.** l.366, l.370: `ch03-start` → `ch02-start`. `sample/` fallback kept.
- **R4.** l.231: "…`lockouts.json`; see Chapter 18 (Volume 1)."
- **R5.** l.505: proposal sentence replaced; the governed `memory.*` store shipped in 0.12.0 and is in 1.1.0 (Chapter 21 and Chapter 15 (Volume 1)). No proposal cited.
- **R6.** Work-claims row removed from the Road Ahead table (former l.519). The "first four rows" Preview note is unchanged and still accurate.
- `exercises/solutions/vol2/ch22.md`: no change needed. The Ex 7 answer (what the check rejects, and the fix) still matches the new premise; no answer depended on the tag or the roster wording.

### F3 (one wording for the roster facts): Ch 18 and Ch 12 changes, for re-check

The coordinator relayed a finding (confirmed in source above) that only `squad cast --name … --role …` adds the support table, so "a project's first `squad cast`" was too broad. All three passages now say it the same way.

- `book/vol2/part-04/ch18-squad-2-overview.md` l.228: "When `squad cast --name <Name> --role "<Role>"` adds a member to a `team.md` without that table, it adds one listing each built-in whose charter is installed, so the first member you cast this way puts all four on the roster. Plain `squad cast` only shows the roster."
- `book/vol2/part-04/ch18-squad-2-overview.md` l.230: "a team upgraded from 1.x" → "a team cast under 1.1.0, whose template already listed all four built-ins".
- `book/vol2/part-03/ch12-coordinator-internals.md` l.58: "a project's first `squad cast` lists them" → "the first `squad cast --name <Name> --role "<Role>"` on a `team.md` without a support table adds them".
- Not touched (other owners): Vol 1 Ch 4 l.120 ("When you cast with `squad cast` and the roster lacks the support-agent table, the command adds it") and shared App C l.49 ("a project's first `squad cast` lists it") have the same breadth.

### F1 (Vol 1 Ch 14, approved text, separate check)

- `book/vol1/part-02/ch14-upgrade-cleanup.md` l.82: third cell adds "(2.0 CLIs only; a 1.1.0 CLI installs)".
- l.93: code comment "# 2.0 CLI: print the command; install nothing".
- l.104: Arthur's exact replacement text applied.
- l.329: "previews with `--dry-run` on a 2.0 CLI (a 1.1.0 CLI ignores it and installs)."
- `exercises/solutions/vol1/ch14.md` l.20 (Quiz 8): Arthur's exact sentence appended; Vol 1 App E l.148 regenerated.

## Re-review (Arthur)

Arthur, 2026-11-21. Scope: Ford's Ch 22 revision (R1–R6), F1 (Vol 1 Ch 14 and its solution), and the F3 roster wording in Ch 18 l.228–230 and Ch 12 l.58. The shared appendices are under a separate review and are not judged here. `make manuscript`: 46 chapters, 0 structural errors, and no working-tree change beyond the existing diff.

### Overall verdict: **REJECT** (one required change, Ch 18 l.448)

| Item | Verdict |
|---|---|
| Ch 22 R1 | **Met.** l.128 names the `npx -y @bradygaster/squad-cli@<version> state-mcp` and bare `squad state-mcp` forms. l.392 expects `npx -y @bradygaster/squad-cli@1.1.0 state-mcp`. l.495 names a repository last written by a 2.0 preview (`node /…/cli-entry.js state-mcp`) or a hand-edited config, and says the 1.x forms pass. Ex 7 (l.542) uses the 2.0-preview premise, and the solution's answer still matches it. |
| Ch 22 R2 | **Met, with the amended trigger.** l.132 and l.169 say all three facts: upgrade never edits `team.md`, a 1.1.0-template cast already lists all four built-ins, and a `team.md` without the table gets one from the first `squad cast --name <Name> --role "<Role>"`. `roster add` is limited to rosters that have the table. |
| Ch 22 R3 | **Met.** l.366 and l.370 use `ch02-start`, and the `sample/` fallback is kept. No `ch03-start` remains. |
| Ch 22 R4 | **Met.** l.231 reads "…`lockouts.json`; see Chapter 18 (Volume 1)." No `Chapter N, Volume` form remains in the chapter. |
| Ch 22 R5 | **Met.** l.505 dates the governed `memory.*` store to 0.12.0 and 1.1.0, cites Chapter 21 and Chapter 15 (Volume 1), and claims nothing about the proposal producing it. |
| Ch 22 R6 | **Met.** The work-claims row is gone. The "first four rows" Preview note still matches rows 1–4 (backend, harnesses, remote durable, v0.2 profiles). |
| F1, Vol 1 Ch 14 l.82, 93, 104, 329, and solutions ch14 l.20 | **Met.** The l.82, l.104 and solution text matches my exact corrections. The l.93 comment and l.329 caveat are consistent with them. Vol 1 App E l.148 carries the regenerated caveat. |
| F3, Ch 12 l.58 | **APPROVE.** Matches Ch 18 and Ch 22. |
| F3, Ch 18 l.228–230 | **APPROVE** as text, but see R7. |
| Ch 18 l.448 | **REJECT (R7).** |

**My earlier finding was wrong, and I confirmed the correction in a scratch repository.** The 2.0.0 CLI ran `squad init` in a new Git repo. It installed the charters for scribe, ralph, rai and fact-checker, and the `team.md` it wrote had no support table. Plain `squad cast` printed the four-agent "Session Cast" and left `team.md` byte-identical. `squad cast --name Zaphod --role "Backend Developer"` added the Zaphod row plus a `## Built-in Support Agents` table with all four built-ins. `squad hire` without `--name`/`--role` fails with the usage error. This matches the source. `cli-entry.ts` l.903–930 sends only `hire`, `--name` or `--role` to `runCastAdd`, which calls `ensureBuiltinRoster` (`commands/cast.ts` l.413). `ensureBuiltinSupportSection` (`core/cast.ts` l.571–574) returns a `team.md` unchanged if it already has a support heading. My Ch 18 R2 and Ch 22 R2 wording ("the first `squad cast`") was too broad, and Ford's amendment is correct.

### Required change

**R7. Ch 18 l.448, troubleshooting bullet.**
- **What:** The bullet still says "on a `team.md` with no built-in support table, `squad cast` adds one". It now contradicts l.228 in the same chapter ("Plain `squad cast` only shows the roster"). Ford changed l.228 and left this bullet alone, so the change introduced a contradiction inside the chapter.
- **Clears when:** The bullet reads: "**Rai and Fact Checker appeared after you cast a member:** on a `team.md` with no built-in support table, `squad cast --name <Name> --role "<Role>"` adds one for every installed built-in charter. Use `squad roster remove` only for rows `squad roster add` wrote; edit `team.md` by hand for rows `squad cast` wrote."

### Follow-ups outside this gate (still say plain `squad cast` adds the built-ins)

- **Vol 1 Ch 4 l.120** (`book/vol1/part-01/ch04-meet-the-team.md`). Ch 12 l.58 points here. Replace "When you cast with `squad cast` and the roster lacks the support-agent table, the command adds it, so Copilot and other hosts list the same team." with "When `squad cast --name <Name> --role "<Role>"` adds a member to a `team.md` that lacks the support-agent table, it adds that table too, so Copilot and other hosts list the same team. Plain `squad cast` only shows the roster."
- **Vol 2 Ch 19 l.301** (`book/vol2/part-04/ch19-across-clients.md`). Replace "`squad cast` added only the cast members to `team.md`" with "`squad cast --name … --role …` added only the new member to `team.md`". Replace "`squad cast` now adds the built-in support table when `team.md` lacks one" with "it now also adds the built-in support table when `team.md` lacks one".
- Shared App C l.49 is left to the appendices review. App A l.37 already states the flag condition correctly.

### Advisory carried forward

- A5 (Ch 22 l.392 vs l.445, uncast-team doctor outcome) is still open and waits on Marvin's F2 drill run. It is not required for this gate.

## Revision (Trillian, R7 + follow-ups)

Trillian, 2026-11-21, assigned successor for R7 (Ford locked out). `make manuscript`: 46 chapters, 0 structural errors.

- **R7, `book/vol2/part-04/ch18-squad-2-overview.md` l.448:** the bullet now reads "**Rai and Fact Checker appeared after you cast a member:** on a `team.md` with no built-in support table, `squad cast --name <Name> --role "<Role>"` adds one for every installed built-in charter…", as specified. The rest of the bullet is unchanged.
- **Follow-up, `book/vol1/part-01/ch04-meet-the-team.md` l.120:** the last sentence of the paragraph was replaced with Arthur's two sentences: "When `squad cast --name <Name> --role "<Role>"` adds a member to a `team.md` that lacks the support-agent table, it adds that table too, so Copilot and other hosts list the same team. Plain `squad cast` only shows the roster."
- **Follow-up, `book/vol2/part-04/ch19-across-clients.md` l.301:** "`squad cast` added only the cast members to `team.md`" → "`squad cast --name … --role …` added only the new member to `team.md`". "`squad cast` now adds the built-in support table when `team.md` lacks one" → "it now also adds the built-in support table when `team.md` lacks one".
- **Sweep:** `book/**` and `exercises/**` (excluding `book/shared/appendices/`), for `squad cast`/`hire` near built-in, support table, Rai, Fact Checker or "four", plus every support-table mention. No other passage says plain `squad cast` adds the built-ins. Ch 12 l.58, Ch 18 l.182/228–230, Ch 19 l.643 and Ch 22 l.132/169 already name the flags. Ch 18 l.215, Ch 19 l.209 and Ch 20 l.295 cover the `Bash(squad cast:*)` allowlist, not roster writes. Shared App C l.49 is left to the appendices review.

## Re-review (R7)

Arthur, 2026-11-21. Scope: R7 and the two `squad cast` follow-ups from Trillian's revision. The shared appendices are under a separate review and are not judged here. `make manuscript`: 46 chapters, 0 structural errors.

### Overall verdict: **REJECT** (one required change, Ch 19 l.301)

| Item | Verdict |
|---|---|
| R7, Ch 18 l.448 | **Met.** The bullet matches the clearing text word for word. It now agrees with l.228 ("Plain `squad cast` only shows the roster") and l.182, so Ch 18 no longer contradicts itself. |
| Follow-up, Vol 1 Ch 4 l.120 | **Met.** Both replacement sentences are in place, verbatim. |
| Follow-up, Vol 2 Ch 19 l.301 | **REJECT (R8).** The replacement text is in place, but the second replacement starts a sentence, and it went in lowercase: "…saw fewer members than Claude did. it now also adds…". My replacement text caused this, because I gave a sentence-initial fragment in lowercase. The manuscript still carries the error. |
| Sweep claim | **Confirmed.** I ran a grep of `book/` and `exercises/` (shared appendices excluded) for `squad cast`/`squad hire` near built-in, support, Rai, Fact Checker, four or "adds". No passage says plain `squad cast` adds the built-ins. Ch 12 l.58, Ch 18 l.182/228/448, Ch 19 l.643 and Ch 22 l.132/169 name the flags. Ch 18 l.215, Ch 19 l.209, Ch 20 l.295, Vol 2 App E l.209 and the ch20 solution l.103 concern the `Bash(squad cast:*)` allowlist. Ch 19 l.643 describes an older `squad cast`, which is accurate. |

### Required change

**R8. Ch 19 l.301, capitalization.**
- **What:** "…than Claude did. it now also adds the built-in support table…" starts a sentence in lowercase.
- **Clears when:** The sentence reads "It now also adds the built-in support table when `team.md` lacks one, and every coordinator describes itself separately from the members when asked who is on the team." Nothing else in the paragraph changes.

- **Revision (Ford, R8):** book/vol2/part-04/ch19-across-clients.md:301, "it now also adds" changed to "It now also adds"; nothing else in the paragraph changed.

## Re-review (R8)

Arthur, 2026-11-21. **APPROVE.** R8 met: Ch 19 l.301 now reads "…than Claude did. It now also adds the built-in support table when `team.md` lacks one, and every coordinator describes itself separately from the members when asked who is on the team." as specified; l.299–303 otherwise match the R7 re-review text. `make manuscript`: 46 chapters, 0 structural errors. No open items on this review.
