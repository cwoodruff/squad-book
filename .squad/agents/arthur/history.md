# Arthur — History

## Core Context

- **Role:** Lead Editor
- **Joined:** 2026-11-20

## Learnings

<!-- Append new learnings below -->

### 2026-11-20 — Squad 2.0 update plan
- Wrote research/UPDATE-PLAN-2.0.md. Part IV keeps Ch 18–22 under a new title. The whole book retargets to v2.0.0 (commit 26654f0c).
- Plain `squad init` and `squad upgrade` are still Copilot-only in 2.0, so most v1.1.0 teaching survives. The real deltas are the removed personal/consult/global modes, the Claude Code plugin (new after preview.2), the `.squad/squad.mjs` launcher, nap no longer summarizing (15 KB threshold), earlier-wins upstream precedence, and plugin context injected only via `AgentLifecycleManager`.
- The stable promotion deleted `docs/proposals/` and `multi-squad.ts`. The docs `site` setting is github.github.com, but github.github.io also serves; the user chose .io. npm, brew and winget IDs keep the bradygaster names.

### 2026-11-20 — Squad 2.0 plan finalised (WP-A)
- UPDATE-PLAN-2.0.md is final. It folds in FC #2/6/20/28/39/44/46/55/56/60/65/71/72/73 and Chris's D1–D4. Docs host is now github.github.com (this supersedes .io). Ch 22 is renamed "Migrating from Squad 1.x to Squad 2.0". The plan ends with a §7 per-owner file list.
- Lesson: before calling a 2.0 feature "new", diff the v1.1.0 code, not the docs. The `squad cost` table, `squad-health/v1` and the root `.mcp.json` all already existed in 1.1.0; only the docs changed. Also use one date source consistently (CHANGELOG).
- STYLE-GUIDE, WRITER-BRIEF, CHAPTERS and README are retargeted to v2.0.0. The old 2.0 and restructure briefs are marked superseded.

### 2026-11-20 — Vol 1 2.0 review gate (WP-A2)
- Verdict REJECT: Ch 4 (Copilot overclaim of sign-off gate; "always-on" Fact Checker), Ch 5 (two-paragraph host note; Claude-centered Exercise 4), Ch 11 and Ch 12 (leftover v1.1.0 target statements). Everything else approved. Review: research/reviews/vol1-review.md.
- Lesson: grep for `v1\.1\.0` outside `blob/v1.1.0` pins catches missed retargets fast. Also check each "the coordinator" claim against `.github/agents/squad.agent.md`, because 2.0 gate behavior is non-Copilot-only and leaks into Copilot-first chapters.
- My style guide pointer-site list (Ch 1, 2, 6, 9, 17, 21) is narrower than my plan §2 (which also lists Ch 5, 10, 12, 18, 20). I need to align them before the next review.

### 2026-11-20 — Vol 2 Parts I–III 2.0 review gate (WP-A2)
- Verdict REJECT: Ch 1 (cross-volume ref form), Ch 4 (a duplicate "Changed in Squad 2.0" notice written as a Warning), Ch 12 ("mandatory" Rai/Fact Checker), Ch 15 (leftover "v1.1.0 CLI"), Ch 16 (Preview callout on a docs/code mismatch). Everything else approved. Trillian's `--yolo` correction holds. Review: research/reviews/vol2-part1-3-review.md.
- Lesson: grep `Chapter [0-9]+, Volume` in both volumes. I missed two in Vol 1 (ch12:33, ch20:48). Also re-test every kept `> **Preview:**` against the 2.0 definition: a docs page that describes a nonexistent API as shipped is a Warning, not a Preview.
- STYLE-GUIDE Vol 1 host-site rule now matches plan §2: the D3 pointer sites (1, 2, 6, 9, 17, 21) plus the one-line or short sites (5, 10, 12, 18, 20).

### 2026-11-21 — Vol 2 Part IV intro, Ch 18, Ch 19 2.0 review gate
- Verdict REJECT: Ch 18 R1 (leftover "specialists are generic subagents", missing the Claude exception), Ch 18 R2 (Rai/Fact Checker: `squad init` always installs both charters, so the first `squad cast` puts them on the roster; `roster add` applies only to rosters that already have a support table), Ch 19 R3 (after Claude removal `client list` shows only Codex). 00-part and both solutions approved. Review: research/reviews/vol2-part4-ch18-19-review.md.
- Lesson: when a writer reports a behavior "when X", check how often X holds by default. Here it is every fresh init. Also, the SDK is usable from `<npm root -g>/@bradygaster/squad-cli/node_modules/@bradygaster/squad-sdk/dist/client/index.js`, so "SDK not installed" is not a reason to leave SDK steps unrun.
- Lesson: grep a chapter for kept 1.1 paragraphs that restate a fact a new paragraph changed (here, generic-subagent dispatch). Partial rewrites leave contradictions in the subsections nobody touched.

### 2026-11-21 — Vol 2 Part IV Ch 20–22 2.0 review gate
- Verdict REJECT Ch 22 only (R1–R6). Ch 20, Ch 21 and all three solutions approved. Review: research/reviews/vol2-part4-ch20-22-review.md. Trillian's 1.1.0 `--self` ignores `--dry-run` finding is confirmed (cli-entry.ts l.448).
- Lesson: when a chapter says what an old version "wrote", read the old writer, not the new code's fix notes. 1.1.0 wrote `npx -y …@1.1.0 state-mcp`. The machine-path `.mcp.json` entries the 2.0 CHANGELOG fixes came from the 2.0 previews.
- Lesson: check every Hands-On tag against the tag commands earlier chapters actually tell readers to run. The style guide's `ch03-start` names the sample's baseline, not a tag in the reader's clone, which is `ch02-start`.
- Lesson: "X became Y" claims about deleted proposals need the Y's first version checked. Governed memory dates from 0.12.0.

### 2026-11-21 — Shared Appendices A–D, F 2.0 review gate
- Verdict REJECT for A (R1, R2), B (R2–R4) and C (R5, R6); D and F approved. Review: research/reviews/shared-appendices-review.md. Ford's `watch.claims`-is-functional departure is right, so my plan §1.1 "reserved" needs a correction.
- Lesson: to check a "no detailed help" claim, loop `<cmd> --help` over every command; spot checks miss most of them (here 8, not 3). The same loop caught a 1.1 carryover (`notes promote --help`).
- Lesson: for any "complete env scan" claim, diff `grep -ohE "SQUAD_[A-Z_]+"` and `env(\.|\[')NAME` over the source against the table. Here it caught SQUAD_MACHINE_ID, which a chapter teaches but the appendix omits.
- Lesson: for every cross-file fact (nap decisions, plugin-mode files), compare the appendix wording with the primary-home chapter and with the appendix's own other rows. A single "only" contradicted a table four rows lower.

### 2026-11-21 — Vol 2 Part V, front matter, Appendices G–J 2.0 review gate
- Verdict REJECT: preface (R1, "Part IV (Chapters 18–21)"), Ch 23/App H/App I/App J (R2, four new "Chapter N, Volume 1" refs), App G (R3, three nonexistent functions carried from 1.1; R4, garbled platform/state index rows and the launcher constant's value), App I (R5, harness credential condition), Ch 25 and its solution (R6, insider publish does not touch Homebrew/WinGet). Approved: 00-part, Ch 24, the title page, and the ch23/ch24 solutions. Review: research/reviews/vol2-part5-front-appendices-review.md.
- Ruling: App J blog links stay at blob/v2.0.0 (byte-identical; the link rule wins over my older plan row). F1 is applied to the plan.
- Lesson: to check an SDK appendix, import the installed `dist/index.js`, `/client` and `/backend` in Node and diff `Object.keys` against every backticked callable. It found 3 phantom names in the grouped tables, which nobody had regenerated. "Kept byte-identical" rows also keep old generator garbage.
- Lesson: for a workflow claim like "X publishes to Y", trace the `workflow_call` inputs and their defaults to the gated job. Secrets passed to a reusable workflow do not mean the job runs.

### 2026-11-21 — check-links.sh fix (Marvin build review R1, R2; escalated from Slartibartfast)
- Rewrote extraction, NUL-safe xargs, a counted-result check and a documented skip list. `make links`: 308 unique, 301 checked, 7 skipped, 0 broken, exit 0. A negative test (old-host plus a 404) exits 1. Revision is in research/reviews/build-review.md.
- Lesson: a check script must count its outputs, not its inputs. "checked N" taken from `wc -l` of the input file hid a probe loop that stopped after 1 URL. Have every worker emit one result line and compare that count with the expected count.
- Lesson: never pipe a URL list into plain `xargs`. Quotes and backslashes in the input are parsed. Use `tr '\n' '\0' | xargs -0`.
