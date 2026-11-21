# Review gate: Volume 1, Squad 2.0 update

Reviewer: Arthur (Lead Editor). Author under review: Ford (Vol 1 front matter, Parts I–IV, `exercises/solutions/vol1/`). Link rewrite by Slartibartfast, judged for link correctness only.
Base: tag `book-squad-v1.1.0`. Working tree on branch `squad-2.0`, uncommitted. Date: 2026-11-20.

## Overall verdict: REJECT

Four chapters have known gaps against the plan, the style guide or the v2.0.0 source: Ch 4, Ch 5, Ch 11 and Ch 12. All other files are approved. Each required change is small and surgical. The rest of the update follows "as close as possible to the current book" well: every H2 skeleton, file name and Tasktrack tag is kept, the voice is unchanged, and the source spot-checks below held up.

## Standard applied

- Author requirements: minimal edits; Second Edition; Vol 1 Copilot-first; docs at `github.github.com/squad/`; repo at `github.com/github/squad`; npm/brew/WinGet names keep `bradygaster`; present tense for 2.0.
- `.squad/decisions.md` and the inbox (Arthur plan-final, Ford ×2, Slartibartfast).
- `research/UPDATE-PLAN-2.0.md` §2 and §4, `research/STYLE-GUIDE.md`, `research/WRITER-BRIEF.md`.
- v2.0.0 source at `SRC/squad-v2.0.0`, plus a fresh `squad init` (CLI 2.0.0) in `$TMPDIR/squad-book-scratch-arthur/t1`.

## Per-chapter verdicts

| File | Verdict |
|---|---|
| `00-front/00-title.md`, `01-preface.md` | APPROVE |
| `part-01/00-part.md`, `part-02/00-part.md`, Part III/IV intros | APPROVE |
| Ch 1 What Is Squad | APPROVE |
| Ch 2 Installation | APPROVE |
| Ch 3 First Session | APPROVE |
| **Ch 4 Meet the Team** | **REJECT** (2 changes) |
| **Ch 5 Routing** | **REJECT** (2 changes) |
| Ch 6 Parallel Work | APPROVE |
| Ch 7 GitHub Workflow | APPROVE |
| Ch 8 GitLab and ADO | APPROVE |
| Ch 9 Ralph Loop | APPROVE |
| Ch 10 PRD, Streams, Fleet | APPROVE |
| **Ch 11 Coding Agent and Remote** | **REJECT** (1 change) |
| **Ch 12 Models and Cost** | **REJECT** (1 change) |
| Ch 13 Notifications | APPROVE |
| Ch 14 Upgrade and Cleanup | APPROVE |
| Ch 15 Memory | APPROVE |
| Ch 16 Tiered Memory and Context | APPROVE |
| Ch 17 Skills | APPROVE |
| Ch 18 Governance | APPROVE |
| Ch 19 Error Recovery | APPROVE |
| Ch 20 Scenarios A | APPROVE |
| Ch 21 Scenarios B | APPROVE |
| `exercises/solutions/vol1/*` | APPROVE, except `ch05.md` (see R4) |

## Required changes

### R1. Ch 4: the sign-off gate is attributed to the Copilot coordinator

- **Where:** `book/vol1/part-01/ch04-meet-the-team.md:146`.
- **What is wrong:** The paragraph says "the coordinator names the rule and the human, asks…, continues only on an explicit yes, and records the answer in the decisions inbox. In a non-interactive run it stops at the gate." In a Copilot-first chapter, "the coordinator" is the Copilot coordinator, and that coordinator does not do this. CHANGELOG 2.0.0 l.140 names only "the Claude, Kiro, OpenCode, Cursor, Codex and Antigravity coordinators". `.github/agents/squad.agent.md` (v2.0.0) contains no sign-off or human-members reference. The text also contradicts Ch 18 l.185 and Ford's own inbox decision, which both say the gate is guidance plus branch protection on the Copilot path.
- **Why:** This is a factual error against the v2.0.0 source. It also breaks plan §2 Ch 18 ("the CHANGELOG says Copilot is unchanged, so don't overclaim") and the one-primary-home rule, since Ch 4 now contradicts Ch 18.
- **Clearing condition:** Keep the description of the template's rule. Then say plainly that the coordinators Squad generates for the other hosts follow it, that the Copilot coordinator is unchanged in 2.0, and that on Copilot you state the gate in `team.md` or `routing.md` and enforce it with branch protection. Point to Ch 18 for the details. No other host detail belongs in Ch 4.

### R2. Ch 4: Fact Checker is still called "always-on"

- **Where:** `book/vol1/part-01/ch04-meet-the-team.md:266`.
- **What is wrong:** The pitfall says "the always-on support identity is a separate built-in contract". Line 112 of the same chapter, and the solution to Quiz 3, now say that Rai and Fact Checker are optional built-ins.
- **Why:** STYLE-GUIDE Terminology says "Rai and Fact Checker are **optional built-ins** added with `squad roster add`". Plan §2 Ch 4 says the same. The chapter contradicts itself.
- **Clearing condition:** Replace "always-on support identity" with "optional built-in support identity" or an equivalent phrase. Do not otherwise change the bullet.

### R3. Ch 5: the "One team, any host" note is two paragraphs

- **Where:** `book/vol1/part-02/ch05-routing.md:119–123`.
- **What is wrong:** The note replacing the consult section runs two paragraphs. The second paragraph re-teaches the non-Copilot reviewer gate, whose Vol 1 home is Ch 18 l.185.
- **Why:** Plan §2 Ch 5 asks for "a short 'One team, any host' note". D3 and STYLE-GUIDE "Hosts: Copilot first" set host material in Vol 1 at most one paragraph. The one-primary-home rule says other chapters summarize in a sentence or two and cross-reference.
- **Clearing condition:** Reduce it to one paragraph that keeps four things: the single `routing.md`/roster/charter source, the fact that non-Copilot coordinators run the reviewer gate unasked (one clause), and the cross-references to Ch 18 and Chapter 20 (Volume 2).

### R4. Ch 5: Exercise 4 and its solution teach Claude Code behavior

- **Where:** `book/vol1/part-02/ch05-routing.md:204` (Exercise 4) and `exercises/solutions/vol1/ch05.md:19` (Solution 4).
- **What is wrong:** The exercise is built around a teammate in Claude Code and asks "what extra step does the Claude coordinator take". The solution adds Claude-specific `squad client sync` and reviewer-gate detail. Ch 5 is not a Claude pointer site, so this is Claude Code material in an exercise.
- **Why:** D3 says "No other Vol 1 chapter adds Claude Code material" beyond the §2 items, and the §2 Ch 5 item covers only the note. STYLE-GUIDE says Vol 1 is Copilot-first, with pointers only at Ch 1, 2, 6, 9, 17 and 21.
- **Clearing condition:** Rewrite Exercise 4 so a Copilot reader can answer it without another host. Example: "Which single file do you edit so validation work goes to the tester, whatever host runs the coordinator, and where does the reviewer gate for that change come from on the Copilot path?" Update Solution 4 to match, with no Claude-specific steps. A host-neutral "configured hosts" phrase is acceptable. Re-run `make manuscript` so Appendix E regenerates.

### R5. Ch 11: one "deprecated in v1.1.0" statement was not retargeted

- **Where:** `book/vol1/part-02/ch11-coding-agent-remote.md:138` ("The CLI itself deprecates `rc` in v1.1.0.").
- **What is wrong:** Line 109 and the Config Reference row were retargeted, but this sentence was not. It still describes v1.1.0 as the release you run.
- **Why:** Plan §2 Ch 11 says to retarget "deprecated in v1.1.0" to "deprecated (still present in v2.0.0)". STYLE-GUIDE Version statements say v1.1.0 appears only as history.
- **Clearing condition:** Change the sentence to something like "The CLI itself still marks `rc` as deprecated in v2.0.0." That fixes it in a few words. Do not change anything else.

### R6. Ch 12: two statements still treat v1.1.0 as the target

- **Where:** `book/vol1/part-02/ch12-models-cost.md:155` ("…with a hard v1.1.0 CLI cost limit.") and `:226` ("…assuming every PRD snippet compiles unchanged against v1.1.0.").
- **What is wrong:** Both statements present v1.1.0 as the release the reader targets. They are not history.
- **Why:** Plan §4 says prose version strings are each reviewed, and target statements become v2.0.0. STYLE-GUIDE says never present v1.1.0 as the target, and WRITER-BRIEF requires re-checking every v1.1.0 claim. Both statements still hold for v2.0.0: no CLI hard cost limit exists, and the sample PRD is still older than the APIs.
- **Clearing condition:** Change both to v2.0.0, for example "a hard CLI cost limit in v2.0.0" and "compiles unchanged against v2.0.0". After the change, `grep -n 'v1\.1\.0' book/vol1/part-02/ch1[12]*.md` must return only history statements.

## Judgement on Ford's reported deviations

| Deviation (change logs and inbox) | Verdict | Evidence |
|---|---|---|
| Ch 3: init does not write `.squad/backend/` to `.gitignore`; only upgrade appends it | Accepted | The scratch `squad init` `.gitignore` has no `backend/` entry |
| Ch 3: coordinator 1,098 lines, `rai` lowercase, `.copilot/mcp-config.json` is an `EXAMPLE-github` sample, launcher `.mcp.json` | Accepted | Reproduced in the scratch init |
| Ch 9: `watch.claims` both "reserved" and documented | Accepted | CHANGELOG preview.3; `watch/config.ts` |
| Ch 9: `squad loop` defaults `--copilot-flags` to `--yolo` | Accepted | `loop.ts` l.143 (new since v1.1.0) |
| Ch 9: claims constants, renew at ttl/3, counters line, Claude preset `bypassPermissions` | Accepted | `watch/claims.ts`, `claim-counters.ts`, `config.ts` l.166; client-compatibility l.227 |
| Ch 7: gh-aw walkthrough callout Preview → Note | Accepted | Demo setup, not experimental in v2.0.0 (STYLE-GUIDE Callouts) |
| Ch 11 solutions: no deprecation note added | Accepted | FC #41 |
| Ch 14: `--skip-repo-upgrade` note dropped | Accepted | No v2.0.0 source or docs hit |
| Ch 14: verified `.local-backup` for skills, `squad-ci.yml` preserved, downgrade refusal, `--self --dry-run` | Accepted | `squad-owned-files.ts` l.13/39/217; `upgrade.ts` l.1886–1960 |
| Ch 2: doctor message and exit status | Accepted | `core/errors.ts` l.26; `--global` text at `cli-entry.ts` l.142 |
| Ch 15/16: "personal-squad (2)" and "preview (4)" plan items had no real hits | Accepted | Remaining hits are SEM scope and `--dry-run` previews |
| Ch 15/16: Scribe only merges decisions; nap never summarizes; 1.x docs said ~12 KB | Accepted | `templates/scribe-charter.md`; v1.1.0 `memory-and-knowledge.md` l.43; v2.0.0 `context-hygiene.md` l.24 |
| Ch 18: `retro-enforcement` exists but is not installed (correction beyond plan) | Accepted | `templates/skills/retro-enforcement/SKILL.md` present; not in the manifest |
| Ch 18: lockout taught as a CLI ledger; the Claude coordinator records it, Copilot does not | Accepted | `client/adapters/coordinator.ts` l.175 (Claude dispatch section only); `adapters/lockout.ts` l.158–202 |
| Ch 12: per-host model paragraph (one sentence) | Accepted | `scenarios/client-compatibility.md` l.221 |
| **Known item:** Parts III–IV cross-refs to Ch 9 have no section name | **Cleared** | The section now exists ("Bounded and Coordinated Watch Runs", Ch 9). Ch 19 l.156/221 and Ch 21 l.100 name the topic (`--claims git-ref`) and Chapter 9. Volume 1 never names sections in cross-refs, so naming the chapter and topic meets plan §2 Ch 21 in house style. |

## Host-pointer audit (D3)

Pointer sites Ch 1, 2, 6, 9, 17 and 21 each hold one paragraph or less, with no Hands-On path, and all cross-reference Volume 2, Part IV. These non-site mentions are authorized by plan §2 and are within scope: the preface sentence, the Ch 3 and Ch 14 `--client` rows, Ch 4 `## X-` (one sentence), the Ch 10 fleet sentence, the Ch 12 model sentence, the Ch 18 other-host gates plus one hooks paragraph, and the Ch 20 host bullet. The only out-of-scope material is in Ch 5 (R3, R4).

## Links (Slartibartfast rewrite)

- There are no `bradygaster.github.io`, `github.github.io` or `github.com/bradygaster` URLs in Vol 1 or its solutions.
- Every `github.com/github/squad/(blob|tree)/<tag>/<path>` pin resolves in the matching source tree. Every `github.github.com/squad/docs/<slug>/` resolves to a v2.0.0 docs page. The docs root is `https://github.github.com/squad/`.
- `bradygaster` survives only in package and installer IDs (`@bradygaster/squad-cli|sdk`, `brew tap bradygaster/squad`, `bradygaster.Squad*`), which is correct.

## Build

- `make manuscript`: "Manuscript: 46 chapters; 0 structural errors". Both Appendix E files were regenerated. The xcrun cache-file warnings come from the sandbox and are not failures.
- `scripts/check-coverage.py`: Vol 1 has no failures. The four remaining misses (ADR-002/003, claude-code-plugin) and the unreferenced modules (dashboard, lockout, hook, harnesses) belong to Vol 2 / App A owners. Exit 1 is expected until Trillian and WP-F2 land.

## Advisories (not required)

- Ch 19 l.156: two consecutive sentences end "Chapter 9 covers it" and "Chapter 9 covers the work loop in detail." Consider merging them.
- Ch 9: the prose uses "Held" for the claim result, while the diagram and round line use "contended" (the counter name). Both are source terms; one clause saying they are the same thing would help readers.
- For Arthur: STYLE-GUIDE "Hosts: Copilot first" lists only the six pointer sites, while plan §2 also authorizes short host mentions in Ch 5, 10, 12, 18 and 20. Align the style guide with the plan so the next reviewer does not read them as violations.

## Re-review

After R1–R6 are fixed, Ford re-runs `make manuscript` and reports. Arthur re-reviews only Ch 4, Ch 5, Ch 11, Ch 12 and `exercises/solutions/vol1/ch05.md`. Strict lockout applies to the rejected chapters: Ford is the author, so per the reviewer protocol a different writer makes the revision unless the coordinator escalates.

## Revision (Trillian)

Successor writer under the reviewer protocol (Ford locked out of Ch 4, 5, 11, 12 and `exercises/solutions/vol1/ch05.md`). Not committed. `make manuscript`: "Manuscript: 46 chapters; 0 structural errors"; both Appendix E files regenerated.

| Item | Change |
|---|---|
| R1 | `book/vol1/part-01/ch04-meet-the-team.md:146`. Kept the template rule. The gate behavior now belongs to "the coordinators Squad generates for the other hosts"; added "The Copilot coordinator is unchanged in 2.0. On Copilot, state the gate in `team.md` or `routing.md` and enforce it with branch protection." Dropped the inbox-recording and non-interactive-stop details (other-host detail, home is Ch 18). The Ch 18 pointer stays. |
| R2 | `ch04-meet-the-team.md:266`: "always-on support identity" became "optional built-in support identity". Nothing else in the bullet changed. |
| R3 | `book/vol1/part-02/ch05-routing.md:119–121`: "One team, any host" is now one paragraph. It keeps the single `routing.md`/roster/charter source, one clause on non-Copilot coordinators running the reviewer gate unasked, and the cross-references to Ch 18 and Chapter 20 (Volume 2). |
| R4 | `ch05-routing.md:202`: Exercise 4 is now "Route to the tester", the reviewer's suggested host-neutral question. `exercises/solutions/vol1/ch05.md:19`: edit `.squad/routing.md` (every configured host reads it). On Copilot the gate comes from the reviewer you name in `routing.md`/`team.md` plus branch protection, with a pointer to Ch 18. The `squad client sync` step and the Claude-specific detail are gone. |
| R5 | `book/vol1/part-02/ch11-coding-agent-remote.md:138`: now reads "The CLI itself still marks `rc` as deprecated in v2.0.0." |
| R6 | `book/vol1/part-02/ch12-models-cost.md:155`: now "a hard CLI cost limit in v2.0.0". `:226`: now "compiles unchanged against v2.0.0". `grep -n 'v1\.1\.0' book/vol1/part-02/ch1[12]*.md` now returns only ch11:109 ("as v1.1.0 did"), which is history. |

### Item 2: `--yolo` alongside `--additional-mcp-config` (#2312)

No file changed. Source check: `packages/squad-cli/src/cli/core/copilot-invocation.ts` l.8–20 says loading MCP config "must not add or remove `--yolo`". I grepped `book/vol1/**`, `exercises/solutions/vol1/**` (and `book/shared/**` for reference) for `yolo` and `additional-mcp-config`. No Vol 1 text ties `--yolo` to MCP injection. The `--yolo` claims that remain are separate defaults, and each matches v2.0.0: Ch 9 l.85 and l.319 (Watch execute default, `watch/index.ts` l.664, `watch/config.ts` l.281–284), Ch 9 l.190 (`squad loop` default, `loop.ts` l.143), Ch 9 l.171 (Claude preset counterpart). Ch 3 l.59 quotes the init tip without `--yolo` (`init.ts` l.221). App A l.119 `squad start --tunnel --yolo` is the CLI's own help example (`command-help.ts` l.235; shared appendix, not touched).

## Re-review

Reviewer: Arthur. Scope: Ch 4, Ch 5, Ch 11, Ch 12 and `exercises/solutions/vol1/ch05.md` only, as revised by Trillian (Ford locked out). Date: 2026-11-20.

| Item | Verdict | Evidence |
|---|---|---|
| R1 | Met | `ch04-meet-the-team.md:146` keeps the template rule, gives the gate behavior to "the coordinators Squad generates for the other hosts", says the Copilot coordinator is unchanged in 2.0, and says to state the gate in `team.md`/`routing.md` and enforce it with branch protection, with a pointer to Chapter 18. It names no hosts. It now agrees with Ch 18 l.198. |
| R2 | Met | `ch04-meet-the-team.md:266` now reads "optional built-in support identity". The rest of the bullet is unchanged. |
| R3 | Met | `ch05-routing.md:121` is one paragraph. It keeps the single `routing.md`/roster/charter source, gives the reviewer gate one sentence, and cross-references Ch 18 and Chapter 20 (Volume 2). |
| R4 | Met | Exercise 4 (`ch05-routing.md:202`) is the host-neutral question. Solution 4 has no Claude-specific step. Its Copilot claim ("does not enforce a reviewer gate by itself"; the gate comes from the reviewer named in `routing.md`/`team.md` plus branch protection) matches v2.0.0 `squad.agent.md` l.537 ("Add a reviewer only when the active team or repository policy requires…") and Ch 18 l.198. Ch 5 and its solution contain no `claude` hits. |
| R5 | Met | `ch11-coding-agent-remote.md:138`: "The CLI itself still marks `rc` as deprecated in v2.0.0." |
| R6 | Met | `ch12-models-cost.md:155` and `:226` now name v2.0.0. `grep -n 'v1\.1\.0' book/vol1/part-02/ch1[12]*.md` returns only ch11:109 ("as v1.1.0 did"), which is history. |

No new gaps were found against the author's requirements (minimal change, Copilot-first Vol 1), the team decisions and inbox, or the plan and style guide. The only other host reference in Ch 4 is the authorized `## X-` sentence at l.72.

`make manuscript`: "Manuscript: 46 chapters; 0 structural errors". Both Appendix E files were regenerated.

The Item 2 check (`--yolo` with `--additional-mcp-config`) found nothing to change, and I accept it.

### Overall re-review verdict: APPROVE

All Volume 1 files pass the 2.0 review gate. The earlier advisories still stand and are not required.
