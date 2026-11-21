# Review: Vol 2 Part V, front matter, Appendices G–J (Squad 2.0.0)

Reviewer: Arthur. Author: Trillian. Date: 2026-11-21. Branch `squad-2.0`, uncommitted. Compared with `git diff book-squad-v1.1.0`. Change log: research/changes/vol2-part5-front-appendices.md.

## Overall verdict: REJECT

Most of the work is accurate and closely sourced. The regenerated symbol index matches the v2.0.0 runtime exports almost exactly. Appendix H's counts match the matrix JSON. ADR-002 and ADR-003 are summarized correctly. The release and CI sections are rebuilt faithfully from the v2.0.0 workflows, and the Ch 24 step is the right size. Six required changes remain (R1–R6). Each is small, but each breaks a standard this gate applies.

Ground truth: `SRC/squad-v2.0.0` (source, workflows, CHANGELOG, docs, `host-feature-matrix.json`), the full clone for v1.1.0 comparisons, and the installed `@bradygaster/squad-sdk` 2.0.0 `dist/`. I imported its root, `/client` and `/backend` entry points in Node and compared the export lists with Appendix G.

## Per-file verdicts

| File | Verdict | Notes |
|---|---|---|
| `book/vol2/part-05/00-part.md` | APPROVE | Present tense, v2.0.0 target. |
| `book/vol2/part-05/ch23-patterns-cookbook.md` | REJECT | R2. The rest checks out: `client add`/`client sync` usage (`client.ts`), `triage`/`watch` alias (`cli-entry.ts` l.629), no `ralph` command, the new triage flags (`cli-entry.ts` l.207–209, 638–750). |
| `book/vol2/part-05/ch24-capstone.md` | APPROVE | See the Ch 24 ruling below. |
| `book/vol2/part-05/ch25-contributing.md` | REJECT | R6. |
| `exercises/solutions/vol2/ch23.md` | APPROVE | Unchanged and still correct. |
| `exercises/solutions/vol2/ch24.md` | APPROVE | Quiz 4 matches the launcher. |
| `exercises/solutions/vol2/ch25.md` | REJECT | R6 (Ex 5). |
| `book/vol2/00-front/00-title.md` | APPROVE | Matches the Vol 1 title page word for word in l.7 and l.15. |
| `book/vol2/00-front/01-preface.md` | REJECT | R1. |
| `book/vol2/appendices/app-G-sdk-api.md` | REJECT | R3, R4. |
| `book/vol2/appendices/app-H-feature-matrix.md` | REJECT | R2. |
| `book/vol2/appendices/app-I-spec-cheatsheet.md` | REJECT | R2, R5. |
| `book/vol2/appendices/app-J-version-history.md` | REJECT | R2. The blog-pin ruling is below. |

## Required changes

### R1. Preface l.36: Part IV mislabelled as "Chapters 18–21"
- **What:** "Multi-host teams. Read Part IV (Chapters 18–21) and Appendix H." Part IV is Chapters 18–22 (the table at l.27, and plan §2 l.220).
- **Why:** The parenthetical misstates the part's extent and contradicts the table nine lines earlier.
- **Clear when:** the line reads "Part IV (Chapters 18–22)", or it names a chapter subset without calling it Part IV, for example "Chapters 18–21 of Part IV".

### R2. Cross-volume references in the wrong form (4 new sites)
- **What:** `ch23-patterns-cookbook.md` l.478 "(Chapter 9, Volume 1)"; `app-H-feature-matrix.md` l.93 "(Chapter 10, Volume 1)"; `app-I-spec-cheatsheet.md` l.110 "Volume 1 Chapter 9 and Chapter 17"; `app-J-version-history.md` l.28 "(Chapter 2, Volume 1)". All four are new in this pass.
- **Why:** STYLE-GUIDE l.72 requires "Chapter 9 (Volume 1)". At l.110 the current wording also leaves unclear which volume Chapter 17 is in.
- **Clear when:** all four use the `Chapter N (Volume 1)` form, and l.110 reads "Chapter 9 (Volume 1) and Chapter 17". `grep -nE "Chapter [0-9]+, Volume|Volume [12] Chapter"` over the reviewed files returns nothing.

### R3. App G names three functions that do not exist
- **What:** l.65 `createOnboardingPlan(...)`, l.74 `streamAgentResponse(...)` and l.81 `initializeOpenTelemetry(...)`. None of them appears in the v2.0.0 SDK source or `dist/`, or in v1.1.0. The real exports are `onboardAgent`/`addAgentToConfig` (onboarding), `StreamingPipeline` and the streaming helpers (streaming), and `initSquadTelemetry`/`initAgentModeTelemetry` with `getMeter`/`getTracer` (OpenTelemetry).
- **Why:** The appendix now says it "describes v2.0.0" (l.3, l.135). These names are carried over from 1.1 but are still false, and a reader who imports them gets an error.
- **Clear when:** the three cells name only symbols that the v2.0.0 root barrel exports. Re-run the check: import `dist/index.js` and confirm every backticked callable in the grouped tables is a key.

### R4. App G: two symbol-index rows are garbled, and one launcher value is wrong
- **What:** (a) The `platform/index.ts` row (l.203) contains raw source: a JSDoc fragment, the body of the non-exported `readGitHubConfig`, `import` lines, and `'.squad' (re-export)`. It does not list the real exports (`detectPlatform`, `GitHubAdapter`, `AzureDevOpsAdapter`, `PlannerAdapter`, `createCommunicationAdapter` and the rest; `platform/index.ts` l.7–20, l.72). (b) The `state/index.ts` row (l.247) carries `// Collection facades`-style comments, and each group lists only its first name. (c) l.296 gives `SQUAD_REPO_LAUNCHER_PATH` as `.squad/squad.mjs`, but its value is `'squad.mjs'` (`repo-launcher.ts` l.9), joined to the squad directory by `squadRepoLauncherArgs`.
- **Why:** The section calls itself a source-derived index that "names each root-visible export". (a) and (b) are byte-identical 1.1 rows that the generator's multi-line `export {}` parsing broke, and keeping them verbatim keeps the defect. (c) misstates an exported constant.
- **Clear when:** both rows are regenerated with names only (no comments or source text) and cover every name their barrels export, and l.296 gives the value as `squad.mjs` (resolved under `.squad/`).

### R5. App I l.113: harness registration omits the credential condition
- **What:** "`claude-agent-sdk`, registered by default when its optional SDK is installed".
- **Why:** `backend-mcp.ts` l.174 registers it only when the SDK resolves and `claudeApiCredentialsConfigured(env)` is true. Ch 21 l.215 and App G l.324 both say "and a credential is configured". App I's own intro says the code wins.
- **Clear when:** the cell adds "and an API credential is configured".

### R6. Ch 25 l.187 and solutions Ex 5: insider publish does not update Homebrew or WinGet
- **What:** Ch 25 says `squad-insider-publish.yml` "updates the `squad-insider` Homebrew cask and the `bradygaster.Squad.Insider` WinGet package". Solutions `ch25.md` l.9 says "(npm `insider`, plus the insider Homebrew cask and WinGet package)".
- **Why:** `squad-insider-publish.yml` l.210–225 calls `squad-standalone-release.yml` with `upload: true` and never sets `publish_package_managers`. That input defaults to `false` (`squad-standalone-release.yml` l.93–97), and both `publish-homebrew` (l.582) and `publish-winget` (l.765) are gated on it. The `squad-insider` and `Squad.Insider` names exist only in the manifest generator's tag mapping (l.557–558). Insider runs attach standalone bundles to the prerelease, and nothing more.
- **Clear when:** both places say that insider runs publish npm `insider`, the GitHub prerelease and the standalone bundles. If the package-manager names stay, they are described as what a run with package-manager publication enabled would target, not what the insider workflow does.

## Rulings on the specific items

- **Appendix G symbol index:** I compared every `function` and `(class|const|enum)` name in the index with the 545 runtime keys of `dist/index.js`. Only 7 names are absent from the index (`AgentsCollection`, `BuilderValidationError`, `COLLECTION_PATHS`, `SquadState`, `StateError`, `createAgentHandle`, `extractHeadings`), and each is a re-export that the index records as "(re-export)", not as a kind. The index has only 2 extra names: `readGitHubConfig` (the R4 garble) and `ConfigValidationError`, which is a class in `runtime/config.ts` but a type-only root export (`index.d.ts` l.16). That second one is acceptable, because the row is keyed to the defining file. The 7 changed and 12 new rows are correct, and so is the removal of `agents/personal` and `sharing/consult`.
- **Harness table:** correct. Every `/backend` name resolves, except `TurnRun`, which is type-only (`backend/index.ts` l.26) and fine as listed. Peer range `>=0.3.300 <0.4.0` matches `package.json`. The `SQUAD_BACKEND_HARNESSES` default and the credential rule match `backend-mcp.ts` l.145–180.
- **Removed personal-squad APIs:** confirmed absent from the root (`resolvePersonalSquadDir`, `ensurePersonalSquadDir`, `ensureSquadPathTriple`, `isConsultMode`, `resolvePersonalAgents`, `mergeSessionCast`, and the consult exports). The `/agents/personal` export path is gone from `package.json`. `isRetiredProfileTeamRoot` exists (`resolution.ts` l.241).
- **Trillian's `discoverSquads` correction:** right. `discoverSquads`, `readSquadRegistry`, `writeSquadRegistry` and `findSquadByName` are all root exports of the 2.0.0 SDK, and `/runtime/cross-squad` is still a package export path.
- **Appendix H:** consistent with the approved Ch 20 matrix. The counts (46/0/5/0 … 40/3/5/3) match `host-feature-matrix.json` exactly. The per-spawn model, background, Ralph CLI, the four all-host gaps, Antigravity MCP inheritance and the live-run dates all agree with Ch 20 l.466–526. "Fleet dispatch: Copilot-only" comes from the matrix's own Claude Ralph cell (docs l.494), so it does not contradict Ch 20's "Fleet mesh … S" row, which covers watch-side infrastructure. It needs R2 only.
- **Appendix I ADR rows:** ADR-002 is correct (status Proposed, Implements and Binding impact lines, ref format, gh-aw never implements `WorkClaimProvider`). So is ADR-003 (Accepted option C, 2026-11-13, §4–§5 and §13, option B spike #2488). The ADR-001 note matches its l.32–38. It needs R2 and R5.
- **Appendix J:** releases and dates match the CHANGELOG headers (`[2.0.0] - 2026-11-18`, preview.4 11-09, preview.3 10-29, preview.2 10-25, preview.1 10-23, 1.1.0 10-19). The npm-lag sentence is in place (l.3). The v2.0.0 detail is faithful to the CHANGELOG.
- **Blog pins (Trillian's open question): RULING: keep `blob/v2.0.0`.** The eight posts are byte-identical between the tags (`git diff --stat v1.1.0 v2.0.0` is empty). Slartibartfast's approved link rule pins to v2.0.0 whenever the path exists there, and coverage checks the primary set at v2.0.0. My plan row predates that rule. I have amended UPDATE-PLAN-2.0.md §2 (App J row) to match.
- **Ch 24 optional step:** approved. It is one optional H3 at the end of Stage 8, exactly the plan's "one optional step … with a Copilot-only fallback". The core path stays on Copilot and plain `squad init`. The fallback explicitly says nothing later depends on it, and the preview-framed Summary H3 it replaces is gone. The described output matches the Claude adapter. The only `.gitignore` line is `.claude/worktrees/` (`adapters.ts` l.150), so reverting the one commit fully backs the step out. The launch line and the trust prompt match Ch 19 l.243, l.256–258.
- **Ch 25 release and CI:** apart from R6, accurate against the v2.0.0 workflows: dispatch-only `squad-release.yml` with `confirm_tag`/`expected_sha`, the guard job, `squad-release-verify.yml`, the `npm_dist_tag` choice, opt-in standalone and package-manager publication, sanitized promotion that refuses consumed changesets and dispatches the stable release with both publication inputs on (`squad-promote.yml` l.75–78, l.229, l.320–325), and the CI triggers (`squad2-*`, `stack-*`). The retired-symbols test description matches `test/retired-symbols.test.ts`. **The Node `>=20` correction is right:** the docs guide says "Node.js 22.5.0 or later" at both v1.1.0 and v2.0.0, and root `engines` is `>=22.5.0`.
- **Preface:** apart from R1, it meets plan §2 l.220. It has the Part IV row, the Ch 22 title, the Preview definition, the version paragraph, and both reading paths. "What's New in the Second Edition" mirrors Vol 1's section (same opening, same closing sentence about `book-squad-v1.1.0`), and its Coming-from-1.x path is consistent with Vol 1 l.52.

## Advisories (not required)

- A1, Ch 25 l.183: consider adding that a prerelease dispatch defaults to the npm `insider` dist-tag, with `preview` added as an alias (`squad-release.yml` l.8–10, l.28–37). "Picks the npm dist-tag at dispatch time" is true but leaves the default out.
- A2, App J l.44: the CHANGELOG install line is `claude plugin install squad@squad --scope project`. The shorter form is not wrong.

## Follow-ups outside this gate

- **FU1 (Trillian / Ford, coordinator to route):** Vol 2 Ch 8 l.117 ("`preview` is its own release-candidate channel") and shared App C l.79 ("`preview` is its compatibility alias. There is no separate release-candidate tag") now disagree. The v2.0.0 code supports both readings in part: npm prereleases default to `insider` with a `preview` alias, while Homebrew and WinGet have separate `squad-preview`/`Bradygaster.Squad.Preview` IDs. The two passages should be reconciled to one statement that separates npm tags from package-manager IDs.
- **FU2 (Arthur, done):** F1 from the shared-appendices review is applied to UPDATE-PLAN-2.0.md §1.1 l.88 and the Ch 9 row at l.190 (`watch.claims` is functional and validated strictly, not reserved). The App J plan row now records the blob/v2.0.0 ruling.

## Checks

- `make manuscript`: 46 chapters, 0 structural errors (regenerates both Appendix E files, as before).
- `make coverage`: 213/213 sources cited; 48/48 source modules referenced.

## Revision (Ford)

Ford, 2026-11-21, as Trillian's assigned successor. Sources checked: `SRC/squad-v2.0.0` SDK source (`index.ts`, `agents/onboarding.ts`, `runtime/streaming.ts`, `runtime/otel-init.ts`, `platform/index.ts`, `state/index.ts`, `client/adapters/repo-launcher.ts`), `packages/squad-cli/src/cli/core/backend-mcp.ts` l.174, and the release workflows. No installed 2.0.0 `dist/` was available in the scratchpad, so R3 and R4 were checked against the root barrel source instead.

- **R1** `book/vol2/00-front/01-preface.md` l.36: "Part IV (Chapters 18–22)".
- **R2** `book/vol2/part-05/ch23-patterns-cookbook.md` l.478 "repository; see Chapter 9 (Volume 1). Bound unattended runs"; `app-H-feature-matrix.md` l.93 "Copilot-only; see Chapter 10 (Volume 1)."; `app-I-spec-cheatsheet.md` l.110 "Chapter 9 (Volume 1) and Chapter 17 cover the practice."; `app-J-version-history.md` l.28 "carry prereleases; see Chapter 2 (Volume 1)." The clearing grep returns nothing over the reviewed files.
- **R3** `app-G-sdk-api.md` l.65 Onboarding: `onboardAgent(...)` and `addAgentToConfig(...)` (what each does, per `onboarding.ts`), types `OnboardOptions`/`OnboardResult`. l.74 Streaming: `StreamingPipeline` plus its event, handler and usage-summary types. l.81 OpenTelemetry: `initializeOpenTelemetry` replaced by `initSquadTelemetry(...)` and `initAgentModeTelemetry(...)`. All are root exports (`index.ts` l.16, 25, 33, 36). None of the three removed names appears in the v2.0.0 source.
- **R4** `app-G` l.203 `platform/index.ts`: keeps the `createPlatformAdapter` signature and lists all 32 names that `platform/index.ts` l.7–20 exports, each "(re-export)", with no source text. l.247 `state/index.ts`: lists all 30 names that the root imports from `state/index.js` (`index.ts` l.120–158), each "(re-export)", with no comments. l.296: `SQUAD_REPO_LAUNCHER_PATH` (`squad.mjs`, resolved under `.squad/`), per `repo-launcher.ts` l.9.
- **R5** `app-I` l.113: "registered by default when its optional SDK is installed and an API credential is configured" (`backend-mcp.ts` l.174).
- **R6** `book/vol2/part-05/ch25-contributing.md` l.187: an insider run creates the GitHub prerelease and attaches the standalone bundles. It does not update Homebrew or WinGet, because it never sets `publish_package_managers` (default `false`). The `squad-insider`/`bradygaster.Squad.Insider` names are now described as what a run with package-manager publication enabled would target. `exercises/solutions/vol2/ch25.md` Ex 5: "(npm `insider`, an immutable GitHub prerelease and the standalone bundles attached to it; it does not update Homebrew or WinGet)". Verified in `squad-insider-publish.yml` l.210–225 and `squad-standalone-release.yml` l.93–97, l.582, l.765.

`make manuscript`: 46 chapters, 0 structural errors. `make coverage`: 213/213 sources, 48/48 modules.

### FU1 (Vol 2 Ch 8, separate subject)

The file is `book/vol2/part-02/ch08-cicd-release.md`, not part-01.

- l.111 table header: "Homebrew cask / WinGet ID (when package-manager publication is on)".
- l.114 Preview row, npm dist-tag: "`insider` by default, plus the `preview` alias" (`squad-release.yml` l.8–10, l.28–37: `npm_dist_tag` default `insider`, `add_preview_alias`).
- l.117 rewritten. On npm, `insider` is the canonical prerelease tag and `preview` is an alias, with no separate release-candidate tag. Homebrew and WinGet have their own preview and insider IDs, but only a run that sets `publish_package_managers` updates them, and the insider workflow never sets it. The note on the v2.0.0 docs now says where they disagree with the workflows: release-process and insider-program both list Homebrew/WinGet for insider, and the installation page calls npm `preview` a release-candidate tag. It tells readers to trust the workflows.
- l.121: the insider workflow publishes "the npm packages, a GitHub prerelease and its standalone bundles".
- `exercises/solutions/vol2/ch08.md` Ex 4: preview uses npm `insider` by default with the `preview` alias. The cask and WinGet checks apply only to runs that enabled package-manager publication.

**Appendix C (not edited; locked out).** l.79 is right about npm and needs no correction. If the editor wants the same split there, append after "There is no separate release-candidate tag.": "Homebrew and WinGet are separate: preview and insider builds have their own cask and WinGet IDs (`squad-preview`/`bradygaster.Squad.Preview`, `squad-insider`/`bradygaster.Squad.Insider`), updated only by release runs that enable package-manager publication."

**Other passages that now disagree with Ch 8 and App C (not edited; outside this assignment):** Vol 1 Ch 2 (`book/vol1/part-01/ch02-installation.md`) l.139 and the l.144 table row (Preview → npm `preview`, "the release-candidate channel"); Vol 2 Ch 18 l.224 ("`preview` for release candidates"). Vol 2 Ch 22 l.26 is already consistent.

## Preview channel follow-ups (Trillian)

Verified against v2.0.0 `.github/workflows` (`squad-release.yml` `npm_dist_tag`/`add_preview_alias`/`publish_package_managers`; `squad-npm-publish.yml` preview alias step). Wording matches Ch 8 l.117 and App C l.79.

- book/vol1/part-01/ch02-installation.md:139: replaced "preview is the release-candidate channel" with the settled account (`insider` canonical npm prerelease tag, `preview` its alias, no separate RC tag; Homebrew/WinGet separate packages updated only by a package-manager release run; pointer to Ch 8, Vol 2).
- book/vol1/part-01/ch02-installation.md:144: Preview row npm tag now "`preview` (alias of `insider`)"; typical use "Try a preview build."
- book/vol1/part-01/ch02-installation.md:391: quiz Q3 reworded (stable tag, prerelease tag, how `preview` relates).
- exercises/solutions/vol1/ch02.md:16 and book/vol1/appendices/app-E-quiz-answers.md:19 (regenerated by `make manuscript`): answer 3 updated to match.
- book/vol2/part-04/ch18-squad-2-overview.md:224: `preview` no longer "for release candidates"; now `insider` canonical, `preview` alias, no RC tag; casks/WinGet IDs are separate packages updated only when a run sets `publish_package_managers` (Ch 8). exercises/solutions/vol2/ch18.md needed no change.

`make manuscript`: 46 chapters, 0 structural errors.

## Review (Arthur): preview follow-ups

Date: 2026-11-21. I checked these lines against the v2.0.0 workflows: `squad-release.yml` (`npm_dist_tag` defaults to `insider`, `add_preview_alias`, `publish_package_managers` opt-in, and dev releases must be `-preview.N`), `squad-npm-publish.yml` (the preview alias steps), `squad-standalone-release.yml` (the cask and WinGet ID chosen by tag; manifests publish only when `publish_package_managers` is set) and `squad-insider-publish.yml` (`workflow_dispatch` on `dev`, with no package-manager input). `make manuscript`: 46 chapters, 0 structural errors.

**Verdict: APPROVE** (no required changes).

- **Vol 1 Ch 2 l.139: approved.** The paragraph says `insider` is the canonical tag, `preview` is its alias and there is no release-candidate tag. It says the Homebrew and WinGet packages are separate and update only on a package-manager run, and it points to Vol 2 Ch 8. All of this matches App C l.79 and the workflows. "Published on demand from `dev`" is correct: both the release workflow and the insider workflow are dispatch-only from `dev`. The paragraph keeps the account at the level of npm tags and packages and leaves the flag names to Vol 2, so the chapter stays introductory. The chapter's other sections are unchanged and stay Copilot-first. The edit is minimal: one sentence replaced and three lines touched in total.
- **Vol 1 Ch 2 l.144: approved.** "`preview` (alias of `insider`)" and "Try a preview build." are consistent with the paragraph above and the Insider row.
- **Vol 1 Ch 2 Q3, l.391, and the solutions answer at l.16: approved.** The question and answer match each other and the settled account. App E l.19 was regenerated and matches.
- **Vol 2 Ch 18 l.224: approved.** The line matches Ch 8 l.117 and App C l.79, and it names `publish_package_managers` correctly. The `upgrade --self` channel-following sentence is unchanged.

No new gaps. The two remaining uses of "release candidate" (Ch 23 l.378, Ch 24 l.7) refer to the Tasktrack project's own release candidate, not to an npm tag. Note on Ch 8 l.117 (not a finding; the other review covers it): it matches the workflows, including the statement that the insider workflow never sets `publish_package_managers`.

## Re-review (Arthur)

Date: 2026-11-21. Scope: Ford's revision of R1–R6 and his FU1 change to Vol 2 Ch 8 and `exercises/solutions/vol2/ch08.md` Ex 4. Vol 1 Ch 2 and Vol 2 Ch 18 are reviewed in the section above and are out of scope here. Ground truth: `SRC/squad-v2.0.0` source, workflows and docs, plus the installed `@bradygaster/squad-sdk` 2.0.0 `dist/` (`$(npm root -g)/@bradygaster/squad-cli/node_modules/@bradygaster/squad-sdk/dist`). Ford checked against source only; I re-ran the checks on the built exports.

### Overall verdict: REJECT (one required change, R7, in Ch 8 l.117)

R1–R6 are all met. FU1 is correct about the workflows, but one of the three claims in its new docs-drift sentence is false.

| Item | Verdict | Evidence |
|---|---|---|
| R1 preface l.36 | Met | "Part IV (Chapters 18–22)". |
| R2 cross-volume refs | Met | All four sites read `Chapter N (Volume 1)`, and l.110 reads "Chapter 9 (Volume 1) and Chapter 17". `grep -nE "Chapter [0-9]+, Volume\|Volume [12] Chapter"` over every reviewed file, Ch 8 and both solutions returns nothing. |
| R3 App G phantom names | Met | I imported `dist/index.js` in Node. `onboardAgent`, `addAgentToConfig`, `StreamingPipeline`, `initSquadTelemetry`, `initAgentModeTelemetry`, `getMeter` and `getTracer` are all keys, and the three old names are not. Each fills its row's role: `onboardAgent` creates `.squad/agents/{name}/` with `charter.md` and `history.md` (`onboarding.ts` l.335–347, l.411–412); `addAgentToConfig` returns `false` unless `squad.config.ts` exists (l.465–475); `StreamingPipeline` registers delta, reasoning and usage handlers and aggregates usage (`streaming.ts` l.120–125). I extracted all 70 backticked callables from the grouped tables (l.1–136). Every one is a root key. |
| R4a `platform/index.ts` row | Met | The 32 names match `platform/index.ts` l.7–20 exactly, with `createPlatformAdapter` (l.72) in the signature column. There is no source text, and `readGitHubConfig` is gone. |
| R4b `state/index.ts` row | Met | The 30 names are exactly the ones `index.ts` l.120–158 re-exports from `state/index.js`, with no comments. The state barrel exports 10 more (e.g. `HistoryEntry`, `StorageProvider`, `AgentStatus`) that the root does not take from it. Because l.137–139 defines this as a root-barrel index of root-visible exports, I read my "every name their barrels export" as the names the root re-exports through that barrel. On that reading, the row is right. |
| R4c launcher constant | Met | `SQUAD_REPO_LAUNCHER_PATH` evaluates to `squad.mjs`, and `squadRepoLauncherArgs('.squad', …)` yields `.squad/squad.mjs` (`repo-launcher.ts` l.9, l.33–35). |
| R5 App I l.113 | Met | Adds "and an API credential is configured". |
| R6 Ch 25 l.187, solution Ex 5 | Met | Both say insider runs publish npm `insider`, the GitHub prerelease and its standalone bundles, and that they do not update Homebrew or WinGet. The package-manager names are framed as what a run with publication enabled would target. Confirmed again: `squad-insider-publish.yml` l.216–221 passes `upload: true` only, and `publish_package_managers` defaults to `false` (`squad-standalone-release.yml` l.93–97). |
| FU1 Ch 8 l.111, l.114, l.121; solution Ex 4 | Met | The table header is conditional. The Preview npm cell matches `squad-release.yml` l.8–10 and l.28–37 (default `insider`, and `add_preview_alias` defaults to `true`). The casks and IDs match the tag mapping at `squad-standalone-release.yml` l.547–558, lowercase `bradygaster.` included. Ex 4 limits the cask and WinGet checks to package-manager runs and says the insider workflow never enables them. |
| FU1 Ch 8 l.117 | **Not met (R7)** | See below. |

### R7. Ch 8 l.117: the installation page does not call npm `preview` a release-candidate tag
- **What:** "…and the installation page describes npm `preview` as a release-candidate tag." In v2.0.0, `get-started/installation.md` l.31–35 introduces `npm install -g @bradygaster/squad-cli@preview` as the way "To test an on-demand prerelease from `dev`". The only "release candidates" wording on the page is l.54, and it is about the Homebrew cask: "Use `squad-preview` for release candidates or `squad-insider` for development snapshots." That matches the workflows' preview cask, which is only published on package-manager runs. Its l.106–107 and l.165–171 do not contradict the workflows either.
- **Why:** The sentence tells readers that a named source page says something it does not say. That is the same kind of error R3 corrected.
- **The other two claims are accurate:** release-process l.7 and l.133–136 list Homebrew and WinGet for insider, while its l.8 gets npm right (`insider` + `preview` alias); insider-program l.21–23 and l.27 say insider updates Homebrew and WinGet. The instruction to trust the workflow files is appropriate. It matches Ch 25's drift note and this edition's rule that checked-in source wins. Keep it.
- **Clear when:** the installation-page clause is deleted, or it is replaced with an accurate statement that does not present the page as disagreeing with the workflows on npm. For example, drop "and the installation page describes npm `preview` as a release-candidate tag" and end the sentence after "update Homebrew and WinGet".

### Appendix C

No change needed and no follow-up. The l.79 "Insider channel" entry defines the npm tag. It is correct and agrees with Ch 8, and the glossary has no Homebrew or WinGet channel entry that would need the package-manager split. Ford's optional sentence stays optional. Adding it would put a second home for the cask and WinGet IDs in a glossary entry about an npm tag.

### Checks

- `make manuscript`: 46 chapters, 0 structural errors.
- `make coverage`: 213/213 sources cited; 48/48 source modules referenced.

- Revision (Trillian, R7): book/vol2/part-02/ch08-cicd-release.md:117 — deleted "and the installation page describes npm `preview` as a release-candidate tag"; sentence now ends after "update Homebrew and WinGet". Rest of l.117 unchanged; still agrees with App C l.79, Vol 1 Ch 2 l.139, Vol 2 Ch 18 l.224.
- Re-review (R7) (Arthur, 2026-11-21): APPROVE. Ch 8 l.117 no longer mentions the installation page; the docs-drift sentence ends at "update Homebrew and WinGet", which meets the R7 clearing condition. The release-process claim (npm right, Homebrew/WinGet wrong for insider), the insider-program claim and "trust the workflow files" are unchanged. l.117 agrees with App C l.79, Vol 1 Ch 2 l.139 and Vol 2 Ch 18 l.224 (`insider` canonical, `preview` alias, no separate release-candidate tag; package managers only on `publish_package_managers` runs). The only remaining "release-candidate" in Ch 8 is the npm "no separate release-candidate tag" statement. `make manuscript`: 46 chapters, 0 structural errors.
