# Review gate: Vol 2 Part IV intro, Chapter 18, Chapter 19 (Squad 2.0.0)

Reviewer: Arthur (Lead Editor). Author: Trillian. Date: 2026-11-21. Branch `squad-2.0`, uncommitted, compared with `git diff book-squad-v1.1.0`.
Standard: author requirements (D1–D4, minimal change), `.squad/decisions.md` and inbox, `research/UPDATE-PLAN-2.0.md` §3.1–3.2, `STYLE-GUIDE.md`, `WRITER-BRIEF.md`, and the v2.0.0 source (`SRC/squad-v2.0.0`) plus the installed 2.0.0 CLI run in a scratch repository.

## Overall verdict: REJECT

There are three required changes: two in Ch 18 and one in Ch 19. All three are accuracy fixes of a sentence or two each. Everything else meets the plan.

| File | Verdict |
|---|---|
| `book/vol2/part-04/00-part.md` | **APPROVE** |
| `book/vol2/part-04/ch18-squad-2-overview.md` | **REJECT** (R1, R2) |
| `book/vol2/part-04/ch19-across-clients.md` | **REJECT** (R3) |
| `exercises/solutions/vol2/ch18.md` | **APPROVE** (advisory A3) |
| `exercises/solutions/vol2/ch19.md` | **APPROVE** |

`make manuscript`: 46 chapters, 0 structural errors. It regenerated both Appendix E files, and Vol 2 App E was already modified in the working tree.

## Trillian's deviations from the plan, checked against source

| Deviation | Finding |
|---|---|
| `squad cast` adds Rai and Fact Checker when `team.md` has no support table | **Correct, and stronger than the chapter says.** `commands/cast.ts` `ensureBuiltinRoster()` (l.221, called at l.413) calls `core/cast.ts` `ensureBuiltinSupportSection()` (l.571) for each built-in whose charter exists. `squad init` always installs all four charters (`core/init.ts` l.336–356), and the init `team.md` has no support table (`squad-sdk/src/config/init.ts` l.1310–1330). So a project's **first** `squad cast` puts Rai and Fact Checker on the roster. Scratch run: `squad init`, then `squad cast --name Zaphod --role "Backend Developer"`, produced a `## Built-in Support Agents` table with Scribe, Ralph, Rai and Fact Checker. `squad roster add rai --dry-run` then reported "already configured". The shell's `createTeam()` (`core/cast.ts` l.790–824) writes all four unconditionally, and it already did in v1.1.0. CHANGELOG #2522 confirms the intent. See R2. |
| No `squad client remove` | **Correct.** `commands/client.ts` handles `list`/`ls`, `add` and `sync` only (l.118, 133, 161). The CLI prints `Unknown client subcommand: remove`. |
| 1.1.0 wrote an `npx` launch command | **Correct.** v1.1.0 `cli/core/mcp-spec.ts` l.139–140 writes `npx -y @bradygaster/squad-cli@<version> state-mcp` in the normal path. Standalone-bundle installs got a PATH command instead, which is not worth a sentence in Ch 18. |
| "earlier-wins" corrected to "later-wins" (Ch 18:198) | **Correct.** v1.1.0 `docs/.../concepts/portability.md` l.150 and l.234 say "later entries override earlier ones". v2.0.0 says "earlier entries win". The 1.1 sentence was wrong, and Trillian's fix is right. |
| `uninstallClients()` not run | **I ran it.** It works. The SDK 2.0.0 is present at `<npm root -g>/@bradygaster/squad-cli/node_modules/@bradygaster/squad-sdk`. The scratch repo went through `init`, `cast`, a commit, `client add claude,codex`, another commit, then `uninstallClients(['claude'], ctx, ['copilot','codex'])`. Result: `{ removed: 62, updated: 1 }`, and `.claude/` is gone, including `settings.json` and `.squad-permissions.json`. `CLAUDE.md` was removed, `.gitignore` was restored, `.mcp.json` was untouched, and `git diff base -- .claude CLAUDE.md .gitignore` was empty. The prose (Ch 19:371–375, 507–515) uses "should" and does not claim a run. The removal claims hold. One exception is R3, which is about `client list`, not the uninstaller. |

## Required changes

### R1. Ch 18:136–140, "One coordinator pattern and shared charters"

- **What:** l.138 still says that "specialists are generic subagents whose shared … charter.md text is included when they are spawned". This is the 1.1 text left unchanged. In v2.0.0 it is false for Claude Code, and it contradicts the chapter's own l.33 and l.104 and Ch 19:19.
- **Why:** accuracy. P2 (member subagents) is a plan item for this chapter.
- **Clears when:** the paragraph states the exception: on Claude Code each member is a generated `.claude/agents/<member>.md` subagent dispatched by name, still generated from the charter. The migration note also says not to hand-edit generated member files (Ch 19:347 already says why).

### R2. Ch 18:228–230, "Release Channels and Optional Built-Ins"

- **What:** l.228 frames `squad roster add` as the way Rai and Fact Checker reach the roster, and says "installing a charter does not change who the team says it is". l.230 then says a fresh cast "can" list them. In v2.0.0, `squad init` always installs both charters, and the first `squad cast` adds them because of those installed charters (see the table above). So for every new project, installing the charter does change the roster, and "can" should be "does".
- **Why:** accuracy against `core/init.ts`, `commands/cast.ts` and `core/cast.ts`, verified with the 2.0.0 CLI.
- **Clears when:** the section says that a new project's first `squad cast` lists all four built-ins, because `squad init` installs their charters and `team.md` starts without a support table. It also says that the INFO "available but not configured" state and `squad roster add` apply to a roster that already has the table without them: a team upgraded from 1.x, or one where someone removed the rows. Drop the "does not change who the team says it is" claim, or limit it to `squad upgrade`. Pitfall l.447–448 and Hands-On Step 4 can stay as written once l.228–230 are fixed.

### R3. Ch 19:515, Hands-On removal check

- **What:** "`squad client list` should show Claude no longer configured and report Copilot/Codex according to their remaining files." After the removal, `clients[]` is `["codex"]`, as l.507 itself says, and `squad client list` lists only Codex. Copilot does not appear although its files remain. Verified in scratch.
- **Why:** accuracy. The reader would read a correct result as a failure.
- **Clears when:** the sentence says the list shows only Codex. It should explain that Copilot is omitted because `clients[]` is non-empty and does not name it, although its files remain and it still works.

## Length

Ch 18 grew from about 6,600 to 8,700 words and Ch 19 from about 8,800 to 12,300. Neither is a REJECT. `STYLE-GUIDE.md` l.54 sets 4,000–8,000 words and says "Volume 2, Part IV reference chapters may run longer". The growth tracks plan items:

- **Ch 18:** the plan marks it "Rewrite". Most of the growth is "What Changed in 2.0.0" (+830 words, which is P2–P13 as the plan asks) and the four renamed or rebuilt H2s.
- **Ch 19:** the plan marks it "Moderate". The plan-mandated "Claude Code: Plugin or Full Projection" section is 1,270 words, and each item in it is in §3.2. The rest is spread over existing sections at +60 to +270 words each, and every addition carries a 2.0.0 fact.

The H2 skeleton is intact apart from the renames the plan requires. No unrequested sections were added. The new hooks and watch-runner paragraphs stay within §3.3's "one paragraph" limit. Ch 19 is now at the upper bound of what "Moderate" can mean. See A1.

## Advisories (not required by any standard)

- **A1. Ch 19:280 restates l.258** (full-projection MCP approval and `enableAllProjectMcpServers`). This duplication predates the update. Cut l.280 to a sentence if you want to recover length.
- **A2. Ch 19:493–505:** give the reader a way to resolve the SDK, for example `npm install --no-save @bradygaster/squad-sdk@2.0.0` in the checkout. Otherwise "a Node environment that can resolve…" is a dead end for most readers.
- **A3. `exercises/solutions/vol2/ch18.md` Ex 6:** add that after `squad client add claude`, `client list` no longer shows Copilot (same cause as R3).
- **A4. Ch 18:87:** the nested parentheses "(Chapter 17 and Chapter 9 (Volume 1))" read awkwardly. Write "Chapter 17, and Chapter 9 (Volume 1)" or split the sentence.

## Follow-up items outside this gate

1. **Vol 2 Ch 12:58 (Trillian; approved passage, now incomplete).** Replace "in 2.0 Rai and Fact Checker are optional built-ins you add with `squad roster add`" with: "in 2.0 Rai and Fact Checker are optional built-ins: a project's first `squad cast` lists them, and a roster that has a support table without them gets them only through `squad roster add`".
2. **Vol 1 Ch 4 (Ford): no change needed.** l.266 is the `fact-checker` duplicate pitfall and is correct. l.108 ("the first-session cast writes them into the roster") and l.120 (`squad cast` adds the missing support table) already describe the 2.0.0 behavior. l.110 ("a team that was cast without them (or upgraded from 1.x) does not gain them on its own") is accurate.
3. **Shared App A l.207 and l.211 (Ford).** Add a `squad cast --name <Name> --role "<Role>"` row: "adds the `## Built-in Support Agents` table (each installed built-in) when `team.md` lacks one". Reword l.211's "Use `squad roster add` to opt in to optional built-ins" to "…on a roster that already has the support table". Add the `client add` caveat to the `client list` row (l.205): a non-empty `clients[]` without `copilot` omits Copilot from the list.
4. **Marvin.** Run the Ch 19 Git removal route (l.486–491) once on a real Tasktrack copy. I verified the SDK route only.
5. **Upstream discrepancies** logged by Trillian (architecture page and across-clients scenario Claude rows, `adapters.ts` "five" header, `upgrade --help` missing `--claude-plugin`, `client list` omitting Copilot). These are for App H/J notes, not this gate.

## Revision (Ford)

Ford, 2026-11-21, as Trillian's assigned successor. Facts checked in a scratch repo with the 2.0.0 CLI: `squad init` installed the scribe, ralph, rai and fact-checker charters and wrote `team.md` without a support table. The first `squad cast --name Zaphod --role "Backend Developer"` added a `## Built-in Support Agents` table listing all four. After `client add claude,codex`, setting `clients[]` to `["codex"]` and removing `.claude/` and `CLAUDE.md`, `squad client list` listed only Codex, although `.github/agents/squad.agent.md` was still there. `make manuscript`: 46 chapters, 0 structural errors.

- **R1:** `book/vol2/part-04/ch18-squad-2-overview.md:138`: generic subagents are now "on most hosts". Added the Claude Code exception: each member is a generated `.claude/agents/<member>.md` subagent that the coordinator dispatches by name, and the file is still generated from the charter. `ch18:140` migration note: added "don't hand-edit generated member files under `.claude/agents/`" with the reason (a user-authored file at a member path is never overwritten, so it stops receiving updates), plus a pointer to Chapter 19.
- **R2:** `ch18:228–230`, rewritten as two paragraphs. l.228: `squad init` always installs the Rai and Fact Checker charters and writes `team.md` without a support table, so a project's first `squad cast` lists all four built-ins. l.230: an existing support table is left alone (a 1.x upgrade, or rows that were removed). The INFO "available but not configured" state and `squad roster add` apply only there. Dropped "installing a charter does not change who the team says it is" and "can therefore list". Pitfalls l.447–448 and Hands-On Step 4 are unchanged.
- **R3:** `book/vol2/part-04/ch19-across-clients.md:515`: `squad client list` should show only Codex. Copilot is omitted because a non-empty `clients[]` does not name it, although its files remain and it still works.
- **A3 (matching change, approved file):** `exercises/solutions/vol2/ch18.md:15`, Ex 6: after `squad client add claude`, `client list` no longer lists Copilot, for the same cause.

### Ch 12 follow-up (separate subject)

- `book/vol2/part-03/ch12-coordinator-internals.md:58`: the parenthetical now reads "in 2.0 Rai and Fact Checker are optional built-ins: a project's first `squad cast` lists them, and a roster that has a support table without them gets them only through `squad roster add`; see Chapter 4 (Volume 1)".

## Re-review (Arthur)

Arthur, 2026-11-21. Scope: Ford's revision (R1–R3, A3) and the Ch 12 follow-up. Ch 20–22 are reviewed separately.

### Overall verdict: APPROVE

| Item | Clearing condition | Finding |
|---|---|---|
| **R1** Ch 18:138–140 | Claude Code exception stated; migration note says not to hand-edit generated member files | **Met.** l.138 limits generic subagents to "most hosts" and states that on Claude Code each member is a generated `.claude/agents/<member>.md` subagent dispatched by name and generated from the charter. This is consistent with Ch 19:19, l.113 and l.184 (plugin mode also writes member files). l.140 adds the do-not-hand-edit rule with the reason, which matches Ch 19:347 and l.627 and the user-authored skip in `claude-members.ts`/`apply.ts`. |
| **R2** Ch 18:228–230 | First `squad cast` lists all four (init installs charters, no support table); INFO state and `roster add` apply only to an existing table; "does not change who the team says it is" dropped | **Met.** l.228 states the init/cast mechanism and the result as fact ("lists all four"). l.230 limits the INFO state and `roster add` to a roster that already has the table (1.x upgrade or removed rows) and keeps the upgrade-preserves-`team.md` sentence. Both dropped phrases are gone. Pitfalls l.447–448, Hands-On Step 4 ("If Step 2 reported…") and quiz Q7 (Tasktrack is an upgraded team) remain consistent. |
| **R3** Ch 19:515 | List shows only Codex; Copilot omitted because non-empty `clients[]` does not name it, though files remain and it works | **Met.** Matches `commands/client.ts` l.56 and l.69–70 (`effective` is `clients[]` when non-empty; the list filters on it). |
| **A3** `exercises/solutions/vol2/ch18.md:15` | (advisory) | **Applied correctly.** After `client add claude` from an empty set, `clients[]` is `["claude"]`, so Copilot drops out of the list. Same source lines. |
| **Ch 12:58** | Wording of follow-up 1 | **Matches exactly.** The only addition is the existing "; see Chapter 4 (Volume 1)" pointer, which was there before. |

No new gaps: the changes are sentence-level, in present tense, describe 2.0.0, and add no sections. They do not conflict with `.squad/decisions.md`, the inbox (including Trillian's built-in roster note), `UPDATE-PLAN-2.0.md` §3.1–3.2 or the style guide. `make manuscript`: 46 chapters, 0 structural errors (it regenerated both Appendix E files, as before).

Advisories still open from the first pass: A1, A2 and A4 were not taken, and none is required. A new minor advisory: Ch 18:140 mixes "Do not" and "Don't" in one note. Pick one if the chapter is touched again. Follow-ups 2–5 are unchanged and outside this gate.
