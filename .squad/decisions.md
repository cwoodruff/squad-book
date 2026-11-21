# Squad Decisions

## Active Decisions

### 2026-11-20: Squad 2.0 edition: whole book targets v2.0.0; Vol 2 Part IV keeps 5 chapters (18-22) and numbering, retitled "Squad 2.0: One Team, Many Hosts"
**By:** Arthur
**References:** ford, trillian, slartibartfast, marvin, research/UPDATE-PLAN-2.0.md
**Why:** Plan: research/UPDATE-PLAN-2.0.md.
- Every volume/part/chapter number, file name and Tasktrack tag is unchanged. The whole book targets Squad v2.0.0 (commit 26654f0c). v1.1.0 and preview.2 appear only as history (Vol 2 Ch 22, App J).
- Part IV is retitled "Squad 2.0: One Team, Many Hosts" and the Preview framing is removed. Ch 18 and Ch 22 are reframed (overview / 1.x->2.0 migration); Ch 19-21 get moderate additions (Claude Code plugin and projection v3, ADR-003, launcher, harnesses). No merges.
- 2.0 features that are not about multiple hosts move into their existing primary homes: Vol 1 Ch 9 (watch claims), Ch 12/15/16 (cost, history, nap), Ch 14 (routine upgrades), Vol 2 Ch 1 (MCP files), Ch 4 (upstream precedence fix), Ch 15 (plugin context fix).
- Removed features (personal squads, consult, --global) are deleted from teaching chapters and kept only in removal tables.
- URLs: docs at https://github.github.io/squad/docs/, repo pins at github.com/github/squad/blob/v2.0.0/ when the path exists, otherwise v1.1.0 history pins. npm, brew and winget names stay bradygaster. (Docs host superseded by the author decision below: use https://github.github.com/squad/.)
- The 8 deleted docs/proposals sources are dropped from coverage.
- Preview callouts are kept only for things that are experimental in v2.0.0.

### 2026-11-20: Squad 2.0 book update: new edition, rename Vol 2 Ch 22 to migration, Vol 1 Copilot-first, docs host github.github.com
**By:** Chris (via Squad coordinator)
**References:** research/UPDATE-PLAN-2.0.md, research/UPDATE-PLAN-2.0-FACTCHECK.md, research/VALIDATION-2.0-ASSESSMENT.md
**Why:** Author decisions for the Squad 2.0 update (branch squad-2.0; 1.1 book tagged book-squad-v1.1.0), answering Arthur's open questions in research/UPDATE-PLAN-2.0.md:
1. New edition: new EPUB identifiers (UUIDs) and edition marking in metadata; the 1.1 book remains at tag book-squad-v1.1.0.
2. Volume 2 Chapter 22 is renamed "Migrating from Squad 1.x to Squad 2.0" (replacing "Upgrading to Squad 2.0 and the Road Ahead").
3. Volume 1 stays Copilot-first with short Claude Code pointers; full Claude Code coverage lives in Volume 2 Part IV.
4. Docs links use https://github.github.com/squad/ (upstream canonical host), not github.github.io. GitHub repo links use https://github.com/github/squad. npm/Homebrew/WinGet package names keep @bradygaster.

Overall direction (user): keep the 2.0 book as close as possible to the current book; Volume 2 may change because 2.0 is no longer in the future.

**Subject: Squad 2.0 update plan. Final state: research/UPDATE-PLAN-2.0.md is FINAL.**

### 2026-11-21: Squad 2.0 plan final: CHANGELOG date convention, fixed Vol 1 Claude pointer sites, Preview = experimental in v2.0.0 only
**By:** Arthur
**References:** ford, trillian, slartibartfast, marvin, research/UPDATE-PLAN-2.0.md, research/STYLE-GUIDE.md
**Why:** research/UPDATE-PLAN-2.0.md is now FINAL. It includes every FC correction and author decisions D1–D4.
- Date convention: every date in the book is a CHANGELOG release date (v2.0.0 = 2026-11-18; preview.1 10-23, preview.2 10-25, preview.3 10-29, preview.4 11-09; v1.1.0 10-19). Appendix J gets one sentence saying that npm publication can be a day or more later. The old App J preview dates were npm dates, not errors.
- D3 applied: Vol 1 Claude Code pointers are allowed only in Ch 1, 2, 6, 9, 17 and 21. Each is at most one paragraph, with no Hands-On path.
- `> **Preview:**` is now reserved for things that are experimental in v2.0.0 (backend tools, harnesses, remote durable server, v0.2 profile promotion). A new `> **Note:** Changed in Squad 2.0:` callout covers 1.x warnings.
- Vol 2 Ch 22 is renamed (D2). The file name stays the same and the H2 "The Road Ahead" stays as a section.
- The Ch 4 `.github/agents/squad.md` passage stays (it is a quote of the proposed `squad export agent`). It is retargeted to "not shipped in v2.0.0".
- WRITER-BRIEF-2.0.md and RESTRUCTURE-BRIEF.md are marked superseded. WRITER-BRIEF.md is now the single v2.0.0 brief.

(Plan §1.1 "watch.claims is reserved" was later corrected to "functional"; see the shared appendices and Part V entries below.)

**Subject: Vol 1 2.0 update and review gate. Final state: APPROVE (all Vol 1 files pass).**

### 2026-11-21: Vol 1 Ch 18: squad lockout is taught as a host-independent CLI ledger; Copilot coordinator does not write it
**By:** ford
**References:** trillian, arthur, research/changes/vol1-part3-4.md
**Why:** In Vol 1 Ch 18 (v2.0.0), `squad lockout` and `.squad/governance/lockouts.json` are presented as a CLI any reader can run. The Copilot coordinator (`.github/agents/squad.agent.md`) is unchanged and does not call it; only the Claude Code dispatch adapter (`client/adapters/coordinator.ts`) records transitions, and only the opt-in advisory Claude hooks read the file. The ledger blocks nothing. The non-Copilot reviewer gate and the human sign-off gate are described as other-host behavior; on the Copilot path they are guidance plus branch protection. Also corrected: the `retro-enforcement` skill exists in `templates/skills/` (it did in v1.1.0 too) but `squad init` does not install it. Trillian (Vol 2 Ch 20) and App A should use the same framing.

### 2026-11-21: Vol 1 Ch 1–14 2.0 update: verified deviations from the plan
**By:** Ford
**References:** research/UPDATE-PLAN-2.0.md, research/changes/vol1-part1-2.md, marvin, arthur
**Why:** Applied UPDATE-PLAN-2.0 §2 to Vol 1 front matter and Ch 1–14. Deviations backed by the source: (1) a fresh 2.0.0 `squad init` does not write `.squad/backend/` to .gitignore; only `squad upgrade` appends it (upgrade.ts l.714). Ch 3 says this. (2) In 2.0, `squad loop` defaults --copilot-flags to --yolo (loop.ts diff), so Ch 9 now documents that. (3) In 2.0, `squad upgrade` backs up customized built-in skills to a verified .local-backup and preserves a customized squad-ci.yml. `--self --dry-run` is now non-mutating. Ch 14 and its solutions are corrected. (4) The gh-aw walkthrough callout in Ch 7 is now a Note, not a Preview, because it is a demo setup and not an experimental 2.0.0 feature. (5) `squad doctor` before init prints "No squad in this directory" and exits 1, so the Ch 2 text and quiz were changed to match. Change log: research/changes/vol1-part1-2.md.

(Item 3 was later qualified: `--self --dry-run` is non-mutating only on a 2.0 CLI; a 1.1.0 CLI installs. Ch 14 got a 1.1.0 caveat under F1 of the Ch 20–22 review below.)

### 2026-11-21: Vol 1 Squad 2.0 review gate: REJECT (Ch 4, 5, 11, 12); all other Vol 1 files approved
**By:** arthur
**References:** ford, slartibartfast, marvin, research/reviews/vol1-review.md, research/UPDATE-PLAN-2.0.md
**Why:** Review: research/reviews/vol1-review.md. Overall REJECT. Required changes:
R1 ch04:146 sign-off gate attributed to Copilot coordinator (CHANGELOG l.140 names only non-Copilot coordinators; squad.agent.md has no sign-off) — rescope as Ch 18 does.
R2 ch04:266 "always-on" Fact Checker contradicts optional built-ins (style guide terminology).
R3 ch05:119-123 "One team, any host" note is two paragraphs and re-teaches the Ch 18 reviewer gate — reduce to one paragraph (plan "short note", D3).
R4 ch05:204 Exercise 4 + solutions/ch05.md:19 teach Claude Code coordinator behavior in a non-pointer chapter (D3) — make host-neutral/Copilot.
R5 ch11:138 "deprecates rc in v1.1.0" not retargeted (plan §2 Ch 11).
R6 ch12:155, :226 present v1.1.0 as target — change to v2.0.0.
All Ford deviations accepted; Ch 9 cross-ref item cleared (house style names chapter+topic, never sections). Links all resolve; make manuscript 46 chapters, 0 errors; Vol 1 coverage clean. Re-review only the four chapters plus solutions ch05. Strict lockout: Ford authored; revision by a different writer unless the coordinator escalates.
**Superseded by:** "Vol 1 re-review: APPROVE" (2026-11-21).

### 2026-11-21: Vol 1 re-review: APPROVE. R1–R6 met by Trillian's revision; all Vol 1 files pass the 2.0 review gate
**By:** arthur
**References:** trillian, ford, research/reviews/vol1-review.md
**Why:** Re-review of Ch 4, 5, 11, 12 and exercises/solutions/vol1/ch05.md after Trillian's revision (Ford locked out under strict lockout).
- R1 met: the Ch 4 sign-off gate is now attributed to the coordinators Squad generates for the other hosts. Ch 4 says the Copilot coordinator is unchanged in 2.0, and on Copilot you state the gate in team.md/routing.md and enforce it with branch protection. It points to Ch 18 and is consistent with Ch 18 l.198.
- R2 met: "optional built-in support identity".
- R3 met: the Ch 5 "One team, any host" note is one paragraph, with cross-references to Ch 18 and Chapter 20 (Vol 2).
- R4 met: Exercise 4 and Solution 4 are host-neutral and have no Claude-specific steps. The Copilot claim matches v2.0.0 squad.agent.md l.537.
- R5 met: Ch 11 says rc is still deprecated in v2.0.0.
- R6 met: both Ch 12 target statements now say v2.0.0. The only v1.1.0 left in Ch 11/12 is history (ch11:109).

No new gaps were found. make manuscript: 46 chapters, 0 structural errors, Appendix E regenerated. Details: research/reviews/vol1-review.md, "Re-review" section. Nothing was committed.

**Subject: Vol 2 Parts I–III 2.0 update and review gate. Final state: APPROVE.**

### 2026-11-21: Vol 2 Ch 1: Squad 2.0.0 no longer injects --yolo with --additional-mcp-config; book follows code, not the copilot-mcp-trust docs page
**By:** trillian
**References:** book/vol2/part-01/ch01-mcp.md, research/changes/vol2-part1-3.md
**Why:** copilot-invocation.ts at v2.0.0 (commit 207a1752, #2312, fixes #2139) injects only `--additional-mcp-config @<path>`; `--yolo` now comes from caller flags (`squad loop` and `squad watch --execute` default to it when no `--copilot-flags`). D/features/copilot-mcp-trust.md still shows the old pair. Ch 1 text, diagram, Config Reference, Quiz 4 and solutions were corrected with a "Changed in Squad 2.0" note. Ford/appendix owners: any Vol 1 or App A/B text that says Squad prepends `--yolo --additional-mcp-config` is wrong for 2.0.0. Other upstream doc/code discrepancies are listed in research/changes/vol2-part1-3.md.

### 2026-11-21: Vol 2 Parts I–III Squad 2.0 review gate: REJECT (Ch 1, 4, 12, 15, 16); all other files and all solutions approved
**By:** arthur
**References:** trillian, ford, marvin, research/reviews/vol2-part1-3-review.md, research/STYLE-GUIDE.md
**Why:** The inbox entry carried no rationale (the field was empty). The required changes R1–R5 are recorded in research/reviews/vol2-part1-3-review.md and are restated as met in the re-review below.
**Superseded by:** "Vol 2 Parts I–III re-review: APPROVE" (2026-11-21).

### 2026-11-21: Vol 2 Parts I–III re-review: APPROVE (Ford's R1–R5 revision plus the Vol 1 ch12/ch20 cross-reference fixes)
**By:** arthur
**References:** ford, trillian, research/reviews/vol2-part1-3-review.md
**Why:** Re-review of Ford's revision (Trillian lockout respected). Every clearing condition is met exactly: R1 ch01:112 now reads Chapter 15 (Volume 1). R2 ch04:160 is a plain action-only Warning, option (a), and the l.14 Note, the precedence list and the Pitfall are unchanged. R3 ch12:58 adds the optional-built-in/`squad roster add` clause. R4 ch15:157 now says v2.0.0 CLI. R5 ch16:114 is now Preview→Warning with the 1.x framing dropped and the facts kept. Vol 1 ch12:33 and ch20:48 now use the house form. The grep for `Chapter N, Volume M` (excluding vol2/part-04) finds no matches. No new gaps. `make manuscript`: 46 chapters, 0 structural errors. One optional advisory: Vol 1 ch20:48 has two semicolons in one sentence; split it at the next copyedit. Details: research/reviews/vol2-part1-3-review.md, "Re-review".

(Ch 12:58 was later revised again under the Part IV reviews; see "Vol 2 Ch 20-22 re-review" below.)

**Subject: Vol 2 Part IV intro, Ch 18, Ch 19 review gate. Final state: APPROVE; the built-in roster framing was later corrected under the Ch 20–22 gate.**

### 2026-11-21: Part IV Ch 18/19: removal routes, built-in roster nuance, single Preview callout
**By:** Trillian
**References:** research/UPDATE-PLAN-2.0.md §3.2, research/changes/vol2-part4-ch18-19.md
**Why:** For Vol 2 Part IV (v2.0.0): (1) Host removal is taught as two routes, Git (revert/restore the projection commit) and SDK uninstallClients(); there is no `squad client remove` in 2.0.0. Ch 18 and Ch 19 say so; Ch 20-22 should not imply a CLI removal path. (2) Rai/Fact Checker stay "optional built-ins via squad roster add", with one caveat now in Ch 18/19: 2.0.0 `squad cast` adds a Built-in Support Agents table (incl. Rai/FC when charters are installed) to a team.md that lacks one (#2522, cast.ts ensureBuiltinSupportSection). Appendices should phrase roster opt-in accordingly. (3) Ch 18 keeps exactly one `> **Preview:**` callout (backend contract, squad_backend_* tools, both harnesses, remote integration, v0.2 profile promotion). (4) The security section is rebuilt from code and ADR-001; the deleted security proposal is not cited (ADR-001 itself still links it upstream). Change log: research/changes/vol2-part4-ch18-19.md.
**Superseded in part by:** "Vol 2 Ch 20-22 re-review: REJECT on Ch 18 l.448 only (R7)" (2026-11-21) for item (2): only `squad cast --name/--role` (or `hire`) adds the support table; plain `squad cast` does not.

### 2026-11-21: Vol 2 Part IV intro/Ch 18/Ch 19 2.0 review gate: REJECT (Ch 18 R1-R2, Ch 19 R3); 00-part and both solutions approved
**By:** Arthur
**References:** trillian, ford, marvin, research/reviews/vol2-part4-ch18-19-review.md, research/changes/vol2-part4-ch18-19.md
**Why:** Review: research/reviews/vol2-part4-ch18-19-review.md. Overall REJECT.
R1 Ch 18:136-140 - leftover 1.1 text says specialists are generic subagents; add the Claude member-subagent exception.
R2 Ch 18:228-230 - Rai/Fact Checker framing: squad init always installs both charters (core/init.ts l.336-356) and the first squad cast adds the full support table (commands/cast.ts ensureBuiltinRoster -> core/cast.ts ensureBuiltinSupportSection), verified in scratch; "roster add" applies only to rosters that already have a support table without them.
R3 Ch 19:515 - after removing Claude, clients[]=["codex"] and squad client list shows only Codex (Copilot omitted), verified.
Trillian's deviations verified correct: no client remove; 1.1.0 npx exact-version spec; later-wins correction; squad cast built-ins. uninstallClients() run by Arthur in scratch via the SDK bundled under the global CLI: Claude paths restore exactly, .mcp.json kept.
Length (Ch 18 8.7k, Ch 19 12.3k) acceptable: STYLE-GUIDE allows longer Part IV reference chapters and growth tracks plan items.
Follow-ups: Vol 2 Ch 12:58 parenthetical (Trillian); shared App A l.205/207/211 (Ford); Vol 1 Ch 4 needs no change; Marvin runs Ch 19 Git removal route.
**Superseded by:** "Vol 2 Part IV Ch 18/19 re-review: APPROVE" (2026-11-21). The R2 claim that plain `squad cast` adds the table was itself corrected by "Vol 2 Ch 20-22 re-review: REJECT on Ch 18 l.448 only (R7)".

### 2026-11-21: Vol 2 Part IV Ch 18/19 re-review: APPROVE. Ford's R1–R3 met, A3 applied correctly, Ch 12:58 matches the follow-up wording.
**By:** Arthur
**References:** ford, trillian, research/reviews/vol2-part4-ch18-19-review.md
**Why:** Re-review of Ford's revision of book/vol2/part-04/ch18-squad-2-overview.md and ch19-across-clients.md, plus ch12-coordinator-internals.md:58 and exercises/solutions/vol2/ch18.md:15.

R1 (Ch 18:138–140), met: the Claude Code exception is stated (a generated .claude/agents/<member>.md subagent, dispatched by name and generated from the charter), and the migration note forbids hand-editing generated member files and gives the reason. This is consistent with Ch 19:19/113/184/347/627.

R2 (Ch 18:228–230), met: a project's first squad cast lists all four built-ins, because init installs the charters and team.md starts without a support table. The INFO state and squad roster add are limited to a roster that already has the table. Both dropped phrases are gone.

R3 (Ch 19:515), met: the list shows only Codex, with the reason Copilot is omitted (commands/client.ts l.56, l.69–70).

A3 is applied correctly. Ch 12:58 matches follow-up 1 exactly.

No new gaps against the author requirements, decisions, UPDATE-PLAN-2.0 §3.1–3.2 or the style guide. make manuscript: 46 chapters, 0 structural errors.

Optional advisories: A1, A2 and A4 from the first pass, plus a new one: Ch 18:140 mixes "Do not" and "Don't". Details are in research/reviews/vol2-part4-ch18-19-review.md under "Re-review (Arthur)".
**Superseded in part by:** "Vol 2 Ch 20-22 re-review: REJECT on Ch 18 l.448 only (R7)" (2026-11-21) for the R2 wording: plain `squad cast` leaves team.md unchanged; only `squad cast --name/--role` (or `hire`) adds the table. Ch 12:58 and Ch 18:228–230 were revised to match.

**Subject: Vol 2 Part IV Ch 20–22 review gate. Final state: APPROVE (gate closed at R8).**

### 2026-11-21: Vol 2 Ch 22 Hands-On is a scratch-copy drill with 1.1.0 in an isolated npm prefix; never tell readers to run a 1.1.0 `squad upgrade --self --dry-run`
**By:** trillian
**References:** research/changes/vol2-part4-ch20-22.md, book/vol2/part-04/ch22-upgrading-to-2.md, marvin, ford
**Why:** v1.1.0 cli-entry.ts (l.412-461) never passes --dry-run to selfUpgradeCli, so `squad upgrade --self --dry-run` on a 1.1.0 CLI performs the global install of @bradygaster/squad-cli@latest (= 2.0.0). Ch 22 therefore previews the target with `npm view @bradygaster/squad-cli dist-tags`, runs the drill on a clone at ch03-start with 1.1.0 installed via `npm install --prefix ~/squad-ch22/cli-1.1.0`, upgrades with the global 2.0 CLI, and rolls back with git reset to v2-ch22-start (1.1.0 CLI used read-only). Ford's Vol 1 Ch 14 and App A should state the same. Marvin to verify end to end. Also: Ch 22 Road Ahead is rebuilt from v2.0.0 experimental/pending items; the seven docs/proposals links are removed.
**Superseded in part by:** "Vol 2 Part IV Ch 20–22 2.0 review gate: REJECT Ch 22 (R1–R6)" (2026-11-21), R3: `ch03-start` does not exist in the reader's clone; the drill uses `ch02-start`.

### 2026-11-21: Vol 2 Part IV Ch 20–22 2.0 review gate: REJECT Ch 22 (R1–R6); Ch 20, Ch 21 and all three solutions approved
**By:** arthur
**References:** trillian, ford, marvin, research/reviews/vol2-part4-ch20-22-review.md, research/changes/vol2-part4-ch20-22.md
**Why:** Review: research/reviews/vol2-part4-ch20-22-review.md. Ch 20 and Ch 21 APPROVE. The feature matrix matches the v2.0.0 JSON cell for cell. ADR-003 framing, lockout framing, executionAvailable/SQUAD_BACKEND_HARNESSES and the casting/policy.json correction are all verified in source. Solutions ch20/21/22 APPROVE. Ch 22 REJECT: R1 1.x never wrote machine paths into .mcp.json (1.1.0 writes `npx -y @bradygaster/squad-cli@1.1.0 state-mcp` or bare `squad`; the machine-path form came from 2.0 previews, #2462), which affects l.128, l.392, l.495 and Ex 7. R2 Rai/Fact Checker: a 1.1.0-cast roster already lists them (mandatory in 1.x), and a 2.0 `squad cast` adds the support table when it is missing (l.132, l.169; align with Ch 18 R2). R3 `ch03-start` does not exist in the reader's clone; use `ch02-start`. R4 cross-volume ref form at l.231. R5 governed memory predates the deleted memory-governance proposal (l.505). R6 the work-claims row is neither experimental nor pending (l.519). Confirmed Trillian's finding that a 1.1.0 CLI ignores --dry-run with --self (cli-entry.ts l.448; upgrade.ts l.1430–1452). Follow-up F1 (Ford): add a 1.1.0 caveat to Vol 1 Ch 14 l.82/l.104 and solutions ch14 l.20, then regenerate App E. F2 (Marvin): run the Ch 22 drill end to end after R1/R3.
**Superseded by:** "Vol 2 Ch 20-22 re-review: REJECT on Ch 18 l.448 only (R7)" (2026-11-21); R1–R6 met. The R2 claim that a 2.0 plain `squad cast` adds the table was corrected there.

### 2026-11-21: Vol 2 Ch 20-22 re-review: REJECT on Ch 18 l.448 only (R7). Ch 22 R1-R6, F1 (Vol 1 Ch 14) and F3 (Ch 12 l.58, Ch 18 l.228-230) all met. Plain `squad cast` correction confirmed.
**By:** arthur
**References:** ford, trillian, marvin, research/reviews/vol2-part4-ch20-22-review.md
**Why:** Re-review of Ford's revision. Ch 22 R1-R6 are met exactly. F1 (Vol 1 Ch 14 l.82, 93, 104, 329 and solutions ch14 l.20) is met. Ch 12 l.58 and Ch 18 l.228-230 now agree with Ch 22 l.132 and l.169: only `squad cast --name/--role` (or `hire`) adds the built-in support table. The one required change is R7, Ch 18 l.448. That troubleshooting bullet still says plain `squad cast` adds the table, which contradicts the revised l.228 in the same chapter. Fix: "Rai and Fact Checker appeared after you cast a member: on a team.md with no built-in support table, `squad cast --name <Name> --role \"<Role>\"` adds one for every installed built-in charter...".

Verification: I confirmed the correction to my own earlier Ch 18 R2 and Ch 22 R2 finding with the 2.0.0 CLI in a scratch repo. After init, plain `squad cast` left team.md byte-identical. `cast --name Zaphod --role "Backend Developer"` added the four-row support table. `hire` without flags gives a usage error. Source agrees: cli-entry.ts l.903-930, commands/cast.ts l.413, core/cast.ts l.571-574. The team rule is that any required change means REJECT. `make manuscript` gave 46 chapters and 0 errors.

Follow-ups, outside this gate: Vol 1 Ch 4 l.120 and Vol 2 Ch 19 l.301 still say plain `squad cast` adds the table. The exact text is in the review. App C l.49 belongs to the appendices review. Advisory A5 is still waiting on Marvin's F2 drill run. Review: research/reviews/vol2-part4-ch20-22-review.md, section "Re-review (Arthur)".
**Superseded by:** "R7 re-review: REJECT. R7 and the Ch 4 follow-up are met" (2026-11-21).

### 2026-11-21: R7 re-review: REJECT. R7 and the Ch 4 follow-up are met, but Ch 19 l.301 needs one capitalization fix (R8).
**By:** Arthur
**References:** Trillian, Ford, research/reviews/vol2-part4-ch20-22-review.md
**Why:** R7 (Ch 18 l.448) matches the clearing text, and Ch 18 no longer contradicts itself. Vol 1 Ch 4 l.120 has the replacement text verbatim. Trillian's sweep claim holds: no passage outside the shared appendices says plain `squad cast` adds the built-ins. make manuscript: 46 chapters, 0 structural errors. REJECT for R8: Ch 19 l.301 reads "...than Claude did. it now also adds...", a sentence starting in lowercase. My replacement fragment caused it. It clears when the word reads "It" and nothing else in the paragraph changes. Details are in research/reviews/vol2-part4-ch20-22-review.md under "Re-review (R7)".
**Superseded by:** "R8 APPROVED: Vol 2 Ch 19 l.301 capitalization fixed" (2026-11-21).

### 2026-11-21: R8 APPROVED: Vol 2 Ch 19 l.301 capitalization fixed; ch18–22 review gate closed.
**By:** Arthur
**References:** Ford, Trillian, research/reviews/vol2-part4-ch20-22-review.md
**Why:** Re-review (R8) of research/reviews/vol2-part4-ch20-22-review.md. book/vol2/part-04/ch19-across-clients.md l.301 now reads "It now also adds the built-in support table when `team.md` lacks one…" as specified; surrounding sentences (l.299–303) unchanged from the R7 re-review. No lowercase " it now also adds" remains. make manuscript: 46 chapters, 0 structural errors. No open required changes on this review.

**Subject: Vol 2 Ch 22 end-to-end follow-up fixes. Final state: APPROVE (gate closed).**

### 2026-11-21: REJECT Trillian's Ch 22 e2e follow-up fixes: F1 (l.392) needs a time anchor; F2 (l.445) and F3 (l.434) approved
**By:** Arthur
**References:** trillian, marvin, book/vol2/part-04/ch22-upgrading-to-2.md, research/reviews/e2e-checks.md
**Why:** F3 l.434 matches upgrade.ts:1717 (one line, no file list). F2 l.445 matches the verified behaviour after the upgrade: doctor exits 0, health --json fails team/registry-charters/routing and exits 1. It also agrees with the step 8 commands. R1, l.392: the fix removed "later", so the sentence now reads as a claim about the step-3 tree. On v2-ch22-start, a global 2.0 `squad doctor` fails `squad_state bridge` (version mismatch 1.1.0 vs 2.0.0) and exits 1. Required: scope the sentence to after the upgrade, e.g. "After the upgrade, an uncast team adds no doctor warnings or failures, but squad health reports the team checks as failures and exits 1." make manuscript: 46 chapters, 0 errors. Review: research/reviews/e2e-checks.md "Review (Arthur)".
**Superseded by:** "Ch 22 e2e R1 re-review: APPROVE" (2026-11-21).

### 2026-11-21: Ch 22 e2e R1 re-review: APPROVE. l.392 is scoped to after the upgrade and the clearing condition is met.
**By:** arthur
**References:** ford, trillian, research/reviews/e2e-checks.md
**Why:** book/vol2/part-04/ch22-upgrading-to-2.md l.392 now reads "After the upgrade, an uncast team adds no `doctor` warnings or failures, but `squad health` reports the team checks as failures and exits 1." The squad health clause is unchanged. The sentence no longer conflicts with the step-3 tree, where the global 2.0 doctor reports a bridge version mismatch. This closes the Ch 22 e2e follow-up gate. `make manuscript`: 46 chapters, 0 structural errors. Record: research/reviews/e2e-checks.md, "Re-review (R1)".

**Subject: Shared Appendices A–D, F review gate. Final state: APPROVE (A–C approved after R7; D and F approved on first pass).**

### 2026-11-21: Shared appendices: `watch.claims` is described as functional; `upgrade --self --dry-run` safe only on 2.0 CLIs
**By:** ford
**References:** research/changes/shared-appendices.md, trillian, arthur
**Why:** Appendix B describes `watch.claims` as a working key (`none`, `git-ref`, or `{provider, ttlMs, skewMarginMs, remote, refPrefix}`) per `commands/watch/config.ts` and `D/features/ralph.md` l.199, not "reserved" as UPDATE-PLAN §1.1 says. Appendix A says `squad upgrade --self --dry-run` is a no-install preview only on a 2.0 CLI (`cli-entry.ts` passes dryRun; first in preview.2); a 1.1.0 CLI ignores --dry-run with --self and installs (v1.1.0 cli-entry.ts l.448, upgrade.ts l.1452). Appendix A also states that `squad cast --name/--role` (runCastAdd -> ensureBuiltinRoster) adds the four-row built-in support table when team.md has none; plain `squad cast` does not. Glossary keeps its em-dash entry separators for consistency with the 1.1 text.

### 2026-11-21: Shared Appendices A–D, F 2.0 review gate: REJECT A (R1, R2), B (R2–R4), C (R5, R6); APPROVE D and F
**By:** arthur
**References:** ford, trillian, research/reviews/shared-appendices-review.md, research/changes/shared-appendices.md
**Why:** Review: research/reviews/shared-appendices-review.md. Required changes:
- R1: App A l.217 says three commands have no detailed help. In 2.0.0 there are eight: health, hook, lockout, sync, models, notes, skill and registry. The l.33 `notes promote` clause "--help/-h prints help" is also false.
- R2: App A l.44 and App B l.58 say "a decisions.md over 20 KB is archived". Nap moves older entries to decisions-archive.md, as Vol 1 Ch 15 says.
- R3: App B l.157 says plugin mode writes "only" a few files. That contradicts l.184 and the observed init, which also writes allow rules, .squad-plugin-settings.json, .squad-permissions.json and the .gitignore entry.
- R4: The App B env-var table misses SQUAD_MACHINE_ID (claims.ts; taught in Vol 1 Ch 9) and the 2.0 host credential and detection variables, yet claims to be a complete scan.
- R5: App C l.49 says a project's first plain `squad cast` "lists" Fact Checker. Only `squad cast --name/--role` or `hire` adds the built-in table (verified in source and a scratch run). Rai at l.111 inherits the same wording.
- R6: App C l.79 says `preview` carries release candidates and was an alias only during the previews. In the v2.0.0 docs, `preview` is still the alias of `insider`.

Accepted:
- Ford's `watch.claims`-as-functional departure. Source and ralph.md confirm it. Plan §1.1 "reserved" is wrong, and I will correct the plan.
- My three Ch 18–19 follow-ups are met.
- The `--self --dry-run` warning is correct.
- The lockout framing matches the Vol 1 Ch 18 decision.
- App F links all resolve, and the release link points at v2.0.0.
- make manuscript: 0 structural errors.
**Superseded by:** "Shared appendices re-review: REJECT App B only (R7)" (2026-11-21); App A and App C approved there.

### 2026-11-21: Shared appendices re-review: REJECT App B only (R7: ComSpec and GIT_CONFIG_PARAMETERS missing from the "complete scan" env table). R1-R6, F1 and F2 met; App A and App C approved.
**By:** arthur
**References:** trillian, ford, research/reviews/shared-appendices-review.md
**Why:** Re-review of Trillian's revision. R1, R2, R3, R5, R6, F1 (Vol 1 Ch 9 l.163) and F2 (App A l.221) are all met and verified against the 2.0.0 CLI, v2.0.0 source and the plugin's commands/*.md. App A: APPROVE. App C: APPROVE. App B: REJECT (R7).

R4's clearing condition is met, and every added row is accurate. However, the revision says the "complete scan" claim at l.98 now holds, and it does not. Two named env reads in v2.0.0 are missing from the table:
- ComSpec (cli/core/mcp-probe.ts l.173)
- GIT_CONFIG_PARAMETERS (cli/commands/upstream.ts l.79, read via gitSyncEnv's base env parameter)

R7 clears when App B adds both names, or narrows the completeness claim at l.98. make manuscript reports 46 chapters and 0 errors; make coverage reports 213/213 sources and 48/48 modules. Advisory only: `squad clients --help` (the alias) prints no detailed help. Details: research/reviews/shared-appendices-review.md, section "Re-review (Arthur)".
**Superseded by:** "Re-review R7: App B APPROVED; shared Appendices A–C overall APPROVE" (2026-11-21).

### 2026-11-21: Re-review R7: App B APPROVED; shared Appendices A–C overall APPROVE
**By:** Arthur
**References:** research/reviews/shared-appendices-review.md, book/shared/appendices/app-B-configuration.md, Slartibartfast
**Why:** R7 has cleared. Slartibartfast's revision adds `ComSpec` (l.139, mcp-probe.ts l.173) and `GIT_CONFIG_PARAMETERS` (l.141, upstream.ts gitSyncEnv l.67–84; clone and pull callers at l.222/329/332), widens row l.123 to `SQUAD_NONINTERACTIVE`, `CI` (init.ts l.111–112), and narrows the l.98 scan claim. I checked each of these against the v2.0.0 source, and they are all accurate. The new l.98 sentence about the `squad start` blocklist matches start.ts l.179–192. My own case-insensitive scan of env reads found no named read missing from App B. `make manuscript` reports 0 errors, and `make coverage` reports 213/213 sources and 48/48 modules. Appendices A and C were already approved, so A–C pass overall. One advisory, not required: "injection-prone" is slightly too broad a word for the whole blocklist.

**Subject: Vol 2 Part V, front matter, Appendices G–J review gate, plus preview-channel follow-ups. Final state: APPROVE.**

### 2026-11-21: Vol 2 Appendix G symbol index regenerated against v2.0.0 by source script; unchanged rows kept verbatim; Appendix J blog links stay at blob/v2.0.0
**By:** Trillian
**References:** Arthur, Slartibartfast, research/changes/vol2-part5-front-appendices.md
**Why:** Appendix G's "Complete root-barrel symbol index" is now v2.0.0: a script follows every re-export from packages/squad-sdk/src/index.ts at both tags; rows whose exports are identical between v1.1.0 and v2.0.0 keep their existing text byte-for-byte, 7 changed rows and 12 new client/casting rows are generated from v2.0.0 source, and agents/personal and sharing/consult rows are removed. This also corrected an error: the cross-squad discovery exports (discoverSquads, readSquadRegistry, findSquadByName, CrossSquad* types) are still root exports at v2.0.0. Appendix J's eight blog links stay at blob/v2.0.0 (approved link rewrite; files are byte-identical to v1.1.0), despite the plan's note to pin them at v1.1.0; Arthur may overrule.

(Arthur ruled in the Part V review gate below: App J blog links stay at blob/v2.0.0 and the plan row is amended. Garbled carryover rows were fixed under R4.) Details: research/changes/vol2-part5-front-appendices.md.

### 2026-11-21: Vol 2 Part V, front matter, Appendices G–J 2.0 review gate: REJECT preface, Ch 23, Ch 25 (+sol), App G, H, I, J (R1–R6); APPROVE 00-part, Ch 24, title page, ch23/ch24 solutions; App J blog links stay at blob/v2.0.0
**By:** arthur
**References:** trillian, ford, slartibartfast, research/reviews/vol2-part5-front-appendices-review.md, research/changes/vol2-part5-front-appendices.md
**Why:** Review: research/reviews/vol2-part5-front-appendices-review.md. Required changes:
- R1: Preface l.36 says "Part IV (Chapters 18–21)"; Part IV is 18–22 (l.27).
- R2: Cross-volume refs in the wrong form (STYLE-GUIDE l.72): ch23 l.478, App H l.93, App I l.110 ("Volume 1 Chapter 9 and Chapter 17"), App J l.28. Use "Chapter N (Volume 1)".
- R3: App G l.65/74/81 name createOnboardingPlan, streamAgentResponse, initializeOpenTelemetry, which exist in neither v2.0.0 nor v1.1.0 (real: onboardAgent/addAgentToConfig, StreamingPipeline, initSquadTelemetry/initAgentModeTelemetry).
- R4: App G symbol index rows platform/index.ts (l.203, raw source text) and state/index.ts (l.247, comment noise) are garbled 1.1 carryovers; l.296 SQUAD_REPO_LAUNCHER_PATH is 'squad.mjs', not '.squad/squad.mjs'.
- R5: App I l.113 omits the API-credential condition for claude-agent-sdk registration (backend-mcp.ts l.174; Ch 21 l.215, App G agree).
- R6: Ch 25 l.187 and solutions ch25 Ex 5 say squad-insider-publish.yml updates the Homebrew cask and WinGet package; it calls the standalone workflow without publish_package_managers (default false), so it does not.

Accepted: symbol index regeneration (runtime-export diff clean apart from R4); harness table; removed personal APIs; Trillian's discoverSquads/cross-squad correction; App H counts and consistency with Ch 20; ADR-002/003 rows; App J releases and CHANGELOG dates; Ch 24 optional Claude Code step (Copilot-first, minimal, clean revert); Ch 25 release/CI rebuild; Node >=20 correction. Ruling: App J blog links stay at blob/v2.0.0 (files byte-identical; follows the approved link rule); plan row amended. F1 applied to UPDATE-PLAN-2.0.md (watch.claims functional, not reserved). Follow-up FU1: Vol 2 Ch 8 l.117 vs App C l.79 disagree on whether preview is its own channel or an insider alias; reconcile (npm tags vs package-manager IDs). make manuscript 0 errors; make coverage 213/213, 48/48.
**Superseded by:** "Vol 2 Part V / front matter / App G–J re-review: REJECT on Ch 8 l.117 only (R7)" (2026-11-21); R1–R6 met there.

### 2026-11-21: Preview-channel follow-ups (Trillian): APPROVE. Vol 1 Ch 2 l.139, l.144, Q3 and its solution, and Vol 2 Ch 18 l.224 match the settled insider/preview account and the v2.0.0 workflows.
**By:** arthur
**References:** trillian, research/reviews/vol2-part5-front-appendices-review.md
**Why:** I checked these lines against the v2.0.0 squad-release.yml (npm_dist_tag defaults to insider, add_preview_alias, publish_package_managers opt-in), squad-npm-publish.yml, squad-standalone-release.yml (casks and WinGet IDs chosen by tag, gated on publish_package_managers) and squad-insider-publish.yml (dispatch on dev, no package-manager input). The account is the same in every place: insider is the canonical npm prerelease tag, preview is an alias of it, there is no release-candidate tag, and Homebrew and WinGet update only when a release run publishes to package managers. It matches App C l.79 and Ch 8 l.117. Vol 1 Ch 2 stays introductory and Copilot-first: the flag names are left to Vol 2 and the edit is minimal. App E l.19 was regenerated and matches. Note: Ch 8 l.117 also matches the workflows (not a finding). `make manuscript`: 46 chapters, 0 structural errors. Record: research/reviews/vol2-part5-front-appendices-review.md, "Review (Arthur): preview follow-ups".

### 2026-11-21: Vol 2 Part V / front matter / App G–J re-review: REJECT on Ch 8 l.117 only (R7). R1–R6 met; rest of FU1 met; App C needs no change.
**By:** arthur
**References:** ford, research/reviews/vol2-part5-front-appendices-review.md, book/vol2/part-02/ch08-cicd-release.md
**Why:** R1–R6 are met. I checked R3 and R4 against the installed 2.0.0 dist/ in Node. onboardAgent, addAgentToConfig, StreamingPipeline, initSquadTelemetry, initAgentModeTelemetry, getMeter and getTracer are all root exports and fill the roles their rows describe. All 70 backticked callables in the grouped tables are root keys. The platform/index.ts row lists the barrel's 32 names, and the state/index.ts row lists the 30 names the root re-exports. SQUAD_REPO_LAUNCHER_PATH is 'squad.mjs', and squadRepoLauncherArgs joins it to give .squad/squad.mjs. FU1 is correct against the workflows in the Ch 8 table, l.121 and solution Ex 4: npm prereleases go to insider by default with preview as an alias, and the casks and WinGet IDs update only on runs that set publish_package_managers. R7 (required): Ch 8 l.117 says the v2.0.0 installation page "describes npm preview as a release-candidate tag". It does not. The page introduces @preview as "an on-demand prerelease from dev" (l.31–35), and "release candidates" appears only for the Homebrew squad-preview cask (l.54). Delete that clause or replace it with an accurate statement. The release-process and insider-program claims are accurate. "Trust the workflow files" is appropriate. App C l.79 needs no change and no follow-up. make manuscript: 46 chapters, 0 structural errors. make coverage: 213/213 sources, 48/48 modules.
**Superseded by:** "R7 re-review: APPROVE Trillian's fix to Vol 2 Ch 8 l.117" (2026-11-21).

### 2026-11-21: R7 re-review: APPROVE Trillian's fix to Vol 2 Ch 8 l.117
**By:** arthur
**References:** trillian, research/reviews/vol2-part5-front-appendices-review.md, book/vol2/part-02/ch08-cicd-release.md
**Why:** Ch 8 l.117 no longer claims the v2.0.0 installation page calls npm `preview` a release-candidate tag; the docs-drift sentence ends at "update Homebrew and WinGet". The R7 clearing condition is met. The release-process, insider-program and "trust the workflow files" points are unchanged. l.117 agrees with App C l.79, Vol 1 Ch 2 l.139 and Vol 2 Ch 18 l.224. make manuscript: 46 chapters, 0 structural errors. Record: research/reviews/vol2-part5-front-appendices-review.md.

**Subject: 2.0 edition build files (WP-S1). Final state: APPROVE (check-links.sh rewritten by Arthur; all build files pass).**

### 2026-11-21: 2.0 edition build groundwork: link pins, coverage script shape, edition metadata
**By:** slartibartfast
**References:** arthur, marvin, ford, trillian
**Why:** 1) Pinned blob/tree links move to github/squad v2.0.0 only when the path exists at v2.0.0 (git cat-file); otherwise they stay on their old tag on github/squad (12 left; see research/LINKS-2.0-LEFTOVERS.md). 2) scripts/check-coverage.py: the primary set is coverage.csv + sources.txt at v2.0.0 with owner github/squad. Optional sets are read only if their files exist: coverage-2.0.csv/sources-2.0.txt (transitional) and coverage-legacy.csv/sources-legacy.txt at v1.1.0. A per-row `ref` column overrides the set ref. Both blob/ and tree/ pins are accepted. Upstream existence checks live in Marvin's research/build_coverage.py, not here. 3) Edition metadata: new UUIDs (vol1 70e2a141-a56d-4692-80f6-b359f61276ef, vol2 5bfe7e51-cce7-4c98-979c-06fc5685970d), custom `edition: "Second Edition"` key (pandoc does not emit it to EPUB), and descriptions begin "Second Edition, updated for Squad 2.0." and end "Targets Squad v2.0.0." Rights line unchanged (LICENSE still says Brady Gaster and contributors). Covers read "Second Edition · Covers Squad 2.0". The title-page edition line is the writers' job (00-title.md). 4) check-links.sh now fails on any old-host URL as a regression guard. It also scans exercises/, probes in parallel and writes its temp file with mktemp under $TMPDIR.
**Superseded in part by:** "Build review (WP-S1) REJECT" and "Build re-review (WP-S1) APPROVE" (2026-11-21) for item 4: check-links.sh was rewritten (NUL-delimited input, commented skip list of 7 local/placeholder URLs). Items 1–3 were approved as written.

### 2026-11-21: Build review (WP-S1) REJECT: check-links.sh R1 (xargs quote abort, probes 1 of 309) and R2 (placeholder/loopback URLs make it always fail); all other build files approved
**By:** marvin
**References:** slartibartfast, arthur, research/reviews/build-review.md, research/reviews/e2e-checks.md
**Why:** Review: research/reviews/build-review.md. REJECT on scripts/check-links.sh only. R1 (l.9,19): the URL regex keeps a trailing ' (Vol 2 Ch 8 l.198), xargs -I{} aborts with "unterminated quote" after line 1, the exit status is discarded and it prints "checked 309 links". Clear by feeding NUL-delimited (xargs -0), excluding ' and ${ in extraction, failing on xargs error, and reporting the real probe count. R2 (l.9,16): 7 loopback/placeholder URLs (localhost:3000/4317/18888, 127.0.0.1, dev.azure.com/YOUR_ORG, github.com/acme/shared-team.git, a template literal) always fail, so the old-host guard can never pass. Clear with a commented skip list; make links must exit 0 on the current tree and 1 when an old-host URL is added. Approved: both metadata files (new UUIDs 70e2a141…/5bfe7e51…, Second Edition, Targets Squad v2.0.0, no preview), both covers (read "Second Edition · Covers Squad 2.0"), check-coverage.py (github/squad v2.0.0), render-cover.sh, cover.html. make coverage 213/213 and 48/48; manuscript 0 errors; epub builds; epubcheck 0 errors on both volumes (Chrome and epubcheck image decoding need to run outside the sandbox). A NUL-safe probe of all 309 URLs finds no real broken link and no old-host URL. Rework should go to someone other than the author, per the reviewer protocol (coordinator decides).
**Superseded by:** "Build re-review (WP-S1) APPROVE" (2026-11-21).

### 2026-11-21: Build re-review (WP-S1) APPROVE: check-links.sh R1 and R2 cleared; all build files now pass
**By:** marvin
**References:** arthur, slartibartfast, research/reviews/build-review.md, scripts/check-links.sh
**Why:** Review: research/reviews/build-review.md, section "Re-review (Marvin)". Arthur's rewrite of scripts/check-links.sh meets every clearing condition. R1: input is NUL-delimited (xargs -0, parallel -P kept); extraction stops at ' $ { so Vol 2 Ch 8 l.198 yields http://127.0.0.1:3000/health without its quote; an xargs failure fails the run (tested with LINK_JOBS=abc: exit 1); the checked count comes from the result lines and is compared with the expected count. An independent Python count finds 308 unique URLs in book/ and exercises/, the same set as the script's (309 minus the quoted duplicate). R2: exactly 7 local or placeholder URLs are skipped, through a commented SKIP_PATTERNS list; the old-host test runs before skipping, so an old-host URL that matches a skip pattern is still flagged (tested). make links: exit 0, "found 308 unique URLs: checked 301, skipped 7, broken 0". Negative test in a $TMPDIR scratch copy: OLD-HOST lines and BROKEN 404 (including a URL inside fetch('…')), exit 1; a dry run with only the old-host URL also exits 1. mktemp under $TMPDIR and the old-host regex are unchanged. Non-blocking: there is no retry on transient 5xx, so add one before wiring the check into CI. research/VALIDATION.md:29 says sample/ and README are scanned, but the script scans book/ and exercises/ only (the decision's scope), so the VALIDATION.md owner should correct that line.

**Subject: WP-M inventories and research/VALIDATION.md follow-ups. Final state: APPROVE (inventories approved; VALIDATION.md V1–V3 approved).**

### 2026-11-21: WP-M inventories review gate: APPROVE (no required changes); make coverage 213/213, 48/48
**By:** slartibartfast
**References:** marvin, arthur, research/reviews/inventories-review.md
**Why:** Reviewed Marvin's sources.txt, coverage.csv, source-modules.csv, build_coverage.py and the deletion of the -2.0 pair against v2.0.0. build_coverage --src: 186 sources, 48 modules, 0 errors, no uninventoried-doc warnings. All 13 docs added v1.1.0->v2.0.0 inventoried; consult-mode, personal-squad, docs/proposals/*, multi-squad.ts removed. Plan WP-M map rows present. 3 book/appendices rows fixed to book/shared/appendices and cited. build_coverage.py no longer writing is safe (Makefile/scripts/CI do not call it). None of the 12 LINKS-2.0-LEFTOVERS pins remain; only app-F:67-69 Historical (1.1.0) pins, allowed by decisions.md l.13. Follow-ups: Marvin rewrites research/VALIDATION.md (still names deleted files); prune 8 stale source-modules sections; CONTRIBUTING.md:9 wording; build_coverage '#' handling. Report: research/reviews/inventories-review.md.

### 2026-11-21: Inventories follow-ups (Marvin): REJECT. Only research/VALIDATION.md needs changes (V1-V3); csv, CONTRIBUTING, build_coverage.py and sample/README pass.
**By:** Slartibartfast
**References:** Marvin, Arthur, Trillian, research/reviews/inventories-review.md, research/VALIDATION.md, research/reviews/e2e-checks.md, research/reviews/build-review.md
**Why:** Review of Marvin's follow-ups is in research/reviews/inventories-review.md under "Review of follow-ups".

Passes:
- make coverage: 213/213 and 48/48.
- build_coverage.py --src v2.0.0: 0 errors.
- Every source-modules.csv section cites its module.
- CONTRIBUTING.md:9 and the build_coverage.py:29-30 comment skip are correct.
- sample/README.md l.19/24/27 are accurate and minimal.

Required changes, all in research/VALIDATION.md:
- V1, l.29: make links scans only book/ and exercises/ (check-links.sh:4,27), not sample/ or README.
- V2, l.40: once Marvin's re-review clears Arthur's check-links.sh rewrite, replace "fix is pending" with the actual make links result (308 found, 301 checked, 7 skipped, 0 broken).
- V3, l.43: the Ch 22 e2e status is stale. F1-F3 have been fixed; Arthur approved F2/F3 and rejected F1 (R1). State the final status once R1 clears, or name it as open.
**Superseded by:** "Inventories follow-ups: still REJECT" (2026-11-21), which made V2 unconditional.

### 2026-11-21: Inventories follow-ups: still REJECT. The approved link checker makes V2 unconditional; V1 (l.29 scope) is confirmed by Marvin's re-review.
**By:** Slartibartfast
**References:** Marvin, Arthur, research/reviews/inventories-review.md, research/VALIDATION.md
**Why:** This updates decision 2761a263 (the preceding "Inventories follow-ups (Marvin): REJECT" entry).

research/VALIDATION.md states neither link-check point correctly:
- l.29 says the link check scans sample/ and README.md. scripts/check-links.sh scans only book/ and exercises/ (V1).
- l.40 still says the link fix is pending. The checker is now approved, so l.40 must record the approved `make links` run: exit 0, 308 unique URLs found, 301 checked, 7 skipped, 0 broken (V2, now applies without waiting on any review).

V3 is unchanged: l.43 must state the final status of the Ch 22 F1-F3 fixes once Arthur's R1 clears, or name R1 as open.
**Superseded by:** "Re-review of research/VALIDATION.md (Trillian's V1-V3 fix): APPROVE" (2026-11-21).

### 2026-11-21: Re-review of research/VALIDATION.md (Trillian's V1-V3 fix): APPROVE
**By:** Slartibartfast
**References:** research/VALIDATION.md, research/reviews/inventories-review.md, trillian, marvin, arthur
**Why:** V1 (l.29): the scan scope is book/ and exercises/ only, which matches scripts/check-links.sh:4,27. V2 (l.40): the text records the approved run (exit 0, 308 found, 301 checked, 7 skipped, 0 broken) and the no-retry limitation, matching build-review.md (Marvin's re-review). V3 (l.43): F1-F3 are fixed and approved, matching e2e-checks.md and Arthur's Re-review (R1) of Ford's l.392 fix. l.39 is still true: the EPUBs in dist/ are older than the later edits to ch22, ch23 and ch25. l.55 is still true: the changes are uncommitted, so no CI run covers them. No required changes. Details are in research/reviews/inventories-review.md under "Re-review: VALIDATION.md".

**Subject: Tasktrack test follow-ups (commits a922ed1, 42a10c3, 960e97e, 66c91bd). Final state: APPROVE (all four changes approved; the test-count correction passed on re-review after Trillian's revision).**

### 2026-11-21: Review: Tasktrack fail-fast before hook: APPROVE (commit a922ed1)
**By:** Slartibartfast
**References:** marvin, sample/api/test/app.test.ts
**Why:** Reviewed Marvin's uncommitted change to sample/api/test/app.test.ts (before hook: reject on server 'error', resolve on 'listening', each handler removes the other via once/off).

Req 1 (fail fast on blocked port): verified. `timeout 60 npm test` in sample/ inside the sandbox exits 1 in under 1 s. All 6 tests fail with `Error: listen EPERM: operation not permitted 0.0.0.0` (code EPERM, syscall listen), with 0 cancelled and no hang.
Req 2 (passes when binding works): verified. Outside the sandbox, 6/6 pass, exit 0, about 126 ms. listen(0) uses the same default host as before and the same port, and base is set the same way.
Req 3 (no leftover listeners, minimal, in style, one file): verified with a scratch probe of the same handler logic against createApp(). The error/listening listener counts return to baseline (0/1) after both the EPERM path and the success path. The diff is +11/-4, uses the file's 2-space arrow-function style and touches only app.test.ts in code.

Scope note: git status also shows .squad/agents/marvin/history.md modified (+2 lines, Marvin's history entries about this task). I treated that as Squad-mandated agent bookkeeping, not part of the change. If the coordinator reads "only this file changes" as literally the whole working tree, this becomes a REJECT on that point alone.

Advisory (not required): Marvin's history entry says listen(0) with no host binds 0.0.0.0. Node normally binds :: on dual-stack hosts. 0.0.0.0 here likely reflects the sandbox environment.

### 2026-11-21: APPROVE: Ford's Ch 3 test-list correction (ch03-first-session.md line 198 and exercises/solutions/vol1/ch03.md item 1) (commit 42a10c3)
**By:** arthur
**References:** ford, book/vol1/part-01/ch03-first-session.md, exercises/solutions/vol1/ch03.md, sample/api/test/app.test.ts
**Why:** Verdict: APPROVE.

Req 1: sample/api/test/app.test.ts has 6 test() calls: health check; creates and lists tasks; rejects empty titles; rejects malformed, non-object, and oversized input; updates status, validates input, and 404s on unknown ids; deletes tasks. The line 198 list now covers all six. The only new item is "malformed/non-object/oversized input rejection", which matches the existing slash style ("task create/list", "status updates/validation/unknown IDs") and sits in test order.

Req 2: Solutions item 1 gets the same fix in that file's own prose style: "rejection of blank titles and of malformed, non-object, or oversized input". Same order, same coverage.

Req 3: Each file changes by one line and nothing else is reworded. No other file under book/ or exercises/ changed. .squad/agents/ford/history.md is also modified, but that is team state, not book or exercise content.

Advisory (not required by the request, and not on the out-of-scope list): Ch 3 line 33 still says `node --test api/test/` "passed all five starter tests". The chapter now lists six tests a few paragraphs later, so it contradicts itself. Line 33 records an observed run, so fixing it means re-running the suite and not just editing the number. Recommend adding it to the separate "five tests" cleanup with Ch 1, Ch 2 and exercises/solutions/vol1/ch02.md.

(The Ch 3 line 33 advisory was taken up by the test-count correction below; ch03:33 now says "six starter tests".)

### 2026-11-21: REJECT Ford's five-to-six test-count correction: the Vol 2 Hands-On lines must not state a fixed count (ch12:219, ch11:190, ch08:227, solutions/vol2/ch08.md:5)
**By:** Arthur
**References:** ford, book/vol2/part-03/ch12-coordinator-internals.md, book/vol2/part-03/ch11-architecture.md, book/vol2/part-02/ch08-cicd-release.md, exercises/solutions/vol2/ch08.md
**Why:** Verdict: REJECT.

What passes:
- Req 1 (Vol 1 side): ch01:153, ch02:300, ch02:384, ch03:33 and solutions/vol1/ch02.md:9 now say six. A grep of book/ and exercises/ for "five" or a numeric count near test, pass or case finds no other stale count. The other "five" hits are about unrelated things like capabilities, nap sections and hosts.
- Req 2: solutions/vol1/ch02.md:9 adds "rejection of malformed, non-object, or oversized input". That uses the same phrase as solutions/vol1/ch03.md:5.
- Req 3 (starter): `npm test` in sample/ prints `tests 6`, `suites 0`, `pass 6`, `fail 0`. All six are top-level `test()` calls, so changing "subtests" to "tests" is correct at ch03:33 and ch11:190.
- Req 4: each edit is a one-token swap. The one addition is a single list item. Nothing else is reworded.

Required changes:
R1. book/vol2/part-03/ch12-coordinator-internals.md:219, "all six existing tests still pass". A fixed count is wrong here. The Vol 2 preface (00-front/01-preface.md:41-49) says Tasktrack "continues here" and tells readers to use the starter only if they skipped Volume 1. Vol 1 Ch 3 (ch03-first-session.md:203-206) already has the reader add node:test coverage for GET /tasks/:id. By Vol 2 Ch 12, the reader's suite is larger than the starter. Suggested fix: "all existing tests still pass, along with any new test the specialist added."
R2. book/vol2/part-03/ch11-architecture.md:190 has the same problem. Line 182 says "Use the Tasktrack checkout you have been operating throughout the book", and the expected result then gives the starter's count. This is a known gap against Req 3, because the output it describes does not match what that checkout prints. Suggested fix: "Node's test runner reports no failures."
R3. book/vol2/part-02/ch08-cicd-release.md:227 and exercises/solutions/vol2/ch08.md:5 have the same problem: a Vol 2 Hands-On run on the carried-forward checkout. Suggested fixes: "`npm test` passes with no failures" and "`npm test` should pass every `node:test` case." Keep the counts in the Vol 1 Ch 1-3 starter lines. Those are correct.

Advisory (outside the requirements): the ch12 Hands-On example task, "add a test for rejecting an empty title", duplicates the starter test 'rejects empty titles'. A specialist could correctly report that nothing needs adding. Consider a different example in a later pass.
**Superseded by:** "APPROVE: Tasktrack test-count correction (Ford Vol 1 edits plus Trillian's Vol 2 revision), re-review" (2026-11-21). Ford was locked out under strict lockout; Trillian revised the Vol 2 lines as the successor.

### 2026-11-21: APPROVE: Tasktrack test-count correction (Ford Vol 1 edits plus Trillian's Vol 2 revision), re-review (commit 960e97e)
**By:** Arthur
**References:** ford, trillian, book/vol2/part-02/ch08-cicd-release.md, book/vol2/part-03/ch11-architecture.md, book/vol2/part-03/ch12-coordinator-internals.md, exercises/solutions/vol2/ch08.md, exercises/solutions/vol1/ch02.md
**Why:** Verdict: APPROVE. No required changes, no advisories.

Scope: the uncommitted `git diff -- book exercises` (8 files, 9 lines).

R1, Volume 1 starter lines say six. Pass. ch01:153 says "six tests pass", ch02:300 "six passing tests", ch02:384 "six tests", ch03:33 "six starter tests", exercises/solutions/vol1/ch02.md:9 "six passing tests under Node 22.18+".

R2, the vol1/ch02 solution list includes the malformed-input test. Pass. "rejection of malformed, non-object, or oversized input" uses the same phrase as exercises/solutions/vol1/ch03.md:5 and sits in the same order (after empty-title rejection, before status updates).

R3, Volume 2 gives no fixed count of the sample's tests. Pass. The four lines changed are ch08:227 ("`npm test` passes with no failures"), solutions/vol2/ch08.md:5 ("should pass every `node:test` case"), ch11:190 ("Node's test runner reports no failures") and ch12:219 ("all existing tests still pass, along with any new test the specialist added"). I grepped book/vol2 and exercises/solutions/vol2 for number words and digits near test/tests/subtests/passing. The only remaining hits are ch17:431 (five SDK manifest capabilities), ch12:268 (six restraint bullets), ch20:528 (five evidence labels) and ch24:384 ("at least three acceptance tests", a reader-authored spec). None of them counts the Tasktrack tests.

R4, minimal edits in the existing style. Pass. Each edit replaces only the count phrase. The sentence structure and the surrounding text are unchanged, and nothing else in the diff is reworded.

The earlier Ch 12 example-task advisory is out of scope, per the coordinator, and was not counted.

(The Ch 12 example-task advisory was taken up by the example-task fix below; ch12:210 now uses a trimming test.)

### 2026-11-21: APPROVE: Ford's Vol 2 Ch 12 Hands-On example task fix ("add a test for trimming whitespace from a new task's title") (commit 66c91bd)
**By:** arthur
**References:** ford, book/vol2/part-03/ch12-coordinator-internals.md, .squad/decisions.md:379
**Why:** Verdict: APPROVE. Scope: uncommitted change to book/vol2/part-03/ch12-coordinator-internals.md (git diff -- book exercises: 1 file, +1/-1, line 210 only).

Req 1 (new to the reader at Vol 2 Ch 12): Pass. sample/api/test/app.test.ts has 6 tests: health check; creates and lists tasks; rejects empty titles; rejects malformed, non-object, and oversized input; updates status, validates input, and 404s on unknown ids; deletes tasks. None of them asserts title trimming. "creates and lists tasks" posts 'Read chapter 1', which has no surrounding whitespace. A grep of book/ and exercises/ for trim|whitespace finds no title-trimming test in Vol 1 or Vol 2 Chs 1-11. The trim hits are tag trimming (Vol 1 Ch 10/11 and their solutions), client-ID normalization (Vol 2 Ch 19/20), and unrelated prose. The tests readers are told to add earlier are: invalid/valid due date (V1 Ch 6, Ch 7, Ch 12), tag tests (V1 Ch 11), and empty GET /tasks in a fresh store (V2 Ch 9). None of them overlaps with this task.

Req 2 (existing behavior, no production change): Pass. sample/api/src/tasks.ts:24 TaskStore.create stores title.trim(). app.ts:56-59 passes body.title to store.create and returns the created task with 201. The trimmed title is visible in the POST response and in GET /tasks. Checked by running the code: new TaskStore().create('  Buy milk  ').title === "Buy milk". The HTTP round trip could not run because the sandbox blocks binding a port, but the route code passes the store result through unchanged.

Req 3 (Hands-On fit): Pass. The task covers one domain, has one tester owner, touches only api/test/app.test.ts, and needs no production code. The rest of the Hands-On is byte-identical, including the expected result "all existing tests still pass, along with any new test the specialist added". No test count was added.

Req 4 (minimal and in style): Pass. Only the example phrase inside the existing curly quotes changed. The curly apostrophe in "task’s" is the only ’ in the chapter, but the book has precedent for curly apostrophes inside curly-quoted examples (for example “Keep the API dependency-free and use Node’s built-in…”), and scripts/build.sh uses markdown+smart, so the rendered output is the same either way. Other copies of the task: exercises/solutions/vol2/ch12.md does not repeat the Hands-On task. A repo-wide grep for "bounded handoff|rejecting an empty|testing specialist" finds only ch12:208/210, my earlier advisory in .squad/decisions.md:379 (a historical record that should stay), and Ford's history entry.

Advisories: none.

## Governance

- All meaningful changes require team consensus
- Document architectural decisions here
- Keep history focused on work, decisions focused on direction
