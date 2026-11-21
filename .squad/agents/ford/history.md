# Ford — History

## Core Context

- **Role:** Technical Writer
- **Joined:** 2026-11-20

## Learnings

<!-- Append new learnings below -->

## 2026-11-20: Vol 1 Parts III–IV updated to v2.0.0

- Check v1.1.0 "absent from source" claims again before relabelling: Ch 18 said `retro-enforcement` was missing, but it was in `templates/skills/` all along; it just isn't in `MANIFEST_SKILL_NAMES`, so `squad init` doesn't install it.
- `squad lockout` builds its roster from `.squad/agents/*/charter.md` (minus squad/scribe/ralph/rai/fact-checker), not from `team.md`. With an empty roster it never reports `deadlocked`.
- Only the Claude dispatch adapter writes the lockout ledger; the Copilot `squad.agent.md` is unchanged, so don't claim more than that for Copilot.

- 2026-11-20: Updated Vol 1 front matter and Ch 1–14 to Squad v2.0.0. Learning: re-verify every "v1.1.0" claim by diffing the module (`git -C SRC/squad diff --stat v1.1.0 v2.0.0 -- <path>`) before relabelling it. Most claims held, but loop's `--yolo` default, the upgrade backup and dry-run semantics, and doctor's exit code had all changed silently. A real `squad init` in a scratch Tasktrack copy is the fastest way to check the tree tables. `mmdc` needs the sandbox disabled to launch Chrome.

- 2026-11-20: Revised Arthur's Vol 2 R1–R5 (Trillian lockout) plus Vol 1 cross-refs. Learning: when converting "(Chapter N, Volume M)" to house form inside parentheses, restructure ("; see Chapter N (Volume M).") rather than nesting parens. Grep `Chapters? [0-9]+, Volume [0-9]` over book/ catches the wrong form; use plain `grep -rnE ... book` (zsh rejects unquoted `--include=*.md`).

- 2026-11-21: Revised Arthur's Vol 2 Ch 18–19 R1–R3 (Trillian lockout) plus Ch 12:58 follow-up. Learning: `squad init` always installs all four built-in charters and writes `team.md` without a support table, so the first `squad cast` lists Rai and Fact Checker; `squad roster add` matters only for rosters that already have the table (1.x upgrades, removed rows). `squad client list` reports only `clients[]` entries, so a non-empty list without `copilot` hides Copilot even though its files remain. Verify both with a 2-minute scratch run (`init`, `cast`, `client add`, edit `clients[]`, `client list`).

- 2026-11-21: Updated shared Appendices A, B, C, D, F to v2.0.0. Learning: when checking a fresh `squad init` tree, use `find -type d` or `ls -la` as well as `git status`; git hides empty dirs (the `.squad/memory/local/` etc. stores are created empty). Also check that the plan's word for a key ("reserved") still matches the source: `watch.claims` is fully functional in 2.0.0. `squad cast` adds the built-in support table only on the `--name/--role` path (`runCastAdd`), not on plain `squad cast`.

- 2026-11-21: Revised Arthur's Vol 2 Ch 22 R1–R6 (Trillian lockout), F1 (Vol 1 Ch 14 `--self --dry-run` caveat) and F3 (roster wording in Ch 22, Ch 18, Ch 12). Learning: plain `squad cast` only shows the roster (`cli-entry.ts` l.903–930); only `squad cast --name … --role …` (or `squad hire`) adds the built-in support table via `ensureBuiltinRoster`. Write the flags out whenever a passage says cast adds Rai and Fact Checker. Also: 1.1.0 `.mcp.json` used `npx -y @bradygaster/squad-cli@1.1.0 state-mcp` (or bare `squad`); machine paths came from the 2.0 previews.

- 2026-11-21: Revised Arthur's Vol 2 Part V/front/App G–J R1–R6 (Trillian lockout) and FU1 (Vol 2 Ch 8 preview channel). Learning: the v2.0.0 docs pages contradict each other and the workflows on channels. release-process.md and insider-program.md both claim insider runs update Homebrew/WinGet, but `squad-insider-publish.yml` never sets `publish_package_managers` (default false). Settle channel claims from `squad-release.yml` (`npm_dist_tag` default `insider`, `add_preview_alias`) and the `squad-standalone-release.yml` gates, and keep npm dist-tags separate from cask/WinGet IDs. Vol 1 Ch 2 l.139–144 and Vol 2 Ch 18 l.224 still call npm `preview` the release-candidate channel (flagged).

- 2026-11-21: Fixed the Tasktrack test list in Vol 1 Ch 3 l.198 and exercises/solutions/vol1/ch03.md l.5. Both left out "rejects malformed, non-object, and oversized input". Learning: the sample now has 6 tests, but several places still say five or list five areas: Ch 1 l.153, Ch 2 l.300 and l.384, and solutions/vol1/ch02.md l.9. Check `grep -n "^test(" sample/api/test/app.test.ts` before writing a count or list.

- 2026-11-21: Tasktrack test count is 6 (added "rejects malformed, non-object, and oversized input"). Corrected stale "five" counts in Vol 1 ch01/ch02/ch03, exercises/solutions/vol1/ch02.md, and Vol 2 ch08/ch11/ch12 plus exercises/solutions/vol2/ch08.md. When the sample's test count changes, grep both volumes and both solution sets for "five/six ... tests", "passing", and "node:test cases". Node's runner reports top-level test() calls as "tests N", not subtests.

- 2026-11-21: Replaced Vol 2 Ch 12 Hands-On example task ("rejecting an empty title", already tested) with "trimming whitespace from a new task's title". Learning: before picking a Tasktrack example test, diff the six `test(` cases against `app.ts`/`tasks.ts` behavior. Untested but existing behavior: title trimming in `TaskStore.create`, OPTIONS 204/CORS headers, the unknown-route 404 fallback. Tests readers already add elsewhere: GET /tasks/:id (Vol 1 Ch 3), empty GET /tasks in a fresh store (Vol 2 Ch 9), PATCH missing ID (Vol 1 Ch 20, Ch 19 ex. 3; this one is already covered by the sample).
