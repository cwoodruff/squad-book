# Validation assessment: retargeting to Squad 2.0.0 GA

Author: Marvin (Test Engineer). Date: 2026-11-20. Branch: `squad-2.0`. This is a report only: no other files were changed.

## Inventory format (agreed)

For `scripts/check-coverage.py` (Slartibartfast). Applied in WP-M on 2026-11-20.

- **One set only.** `research/sources-2.0.txt` and `research/coverage-2.0.csv` are deleted. The required set is `("coverage.csv", "sources.txt", "v2.0.0")`. The checker's optional `coverage-2.0`/`coverage-legacy` pairs are skipped when their files are absent, and WP-M ships neither file. Removed-feature history links (v1.1.0 pins) are not tracked by coverage.
- **`research/sources.txt`**: unchanged line format. One repo-relative path per line, sorted, no header, no comments. 186 lines, all present at v2.0.0 (`26654f0c`).
- **`research/coverage.csv`**: unchanged columns, `source,chapter`. `chapter` is `volN:NN` (unpadded, for example `vol1:9`) or an appendix letter (`A`–`J`). A source may have more than one row. 213 rows. There is no status or pending column.
- **`research/source-modules.csv`**: unchanged columns, `source_module,book_section`. `book_section` is a `; `-separated list of repo-relative book files. The 3 stale `book/appendices/` paths were corrected to `book/shared/appendices/`. 48 rows.
- **Pinned citation form** the checker must accept: `https://github.com/github/squad/blob/v2.0.0/<path>`. The docs-slug form `/squad/docs/<slug>/` works on any host, as before.
- `research/build_coverage.py` no longer writes `coverage.csv`. It is now a read-only check (`python3 -I research/build_coverage.py --src <v2.0.0 checkout>`): inventory and map consistency, upstream existence of every source and module, and warnings for new upstream docs that are not inventoried.

## Pinned references

| Tag | Commit |
|---|---|
| `v1.1.0` | `c24da2aad2ab7576f6b68dec2bc50b2fe2dc7a8a` (current baseline, matches VALIDATION.md) |
| `v2.0.0-preview.2` | `481c944596abfa2053e2acd88d765639f994d795` (current Vol 2 Part IV baseline) |
| `v2.0.0` | `26654f0c4dadb2625d764c1c69ec61da6c518094` (new target) |

At v2.0.0, the CLI and SDK publish as version `2.0.0` and **keep the `@bradygaster/squad-cli` / `@bradygaster/squad-sdk` npm names**. The repository moved to `github/squad`. The docs site is built with `site: 'https://github.github.com', base: '/squad/'` (see `docs/astro.config.mjs`). `https://github.github.io/squad/` also returns 200, but upstream links use `github.github.com`, so this report recommends that host.

## 1. Coverage tooling

### How it works today

- `research/sources.txt` (175 paths) and `research/sources-2.0.txt` (41 paths) are hand-curated inventories. 24 paths appear in both, which gives 192 unique sources.
- `research/coverage.csv` (175 rows) and `research/coverage-2.0.csv` (42 rows) map each source to a `volN:chapter` or an appendix letter. Together they hold 217 citation assignments.
- `research/build_coverage.py` regenerates only `coverage.csv`. Its map `M` uses the **old continuous chapter numbers** (1–46), which are converted to `vol1`/`vol2`. `coverage-2.0.csv` has no generator and is hand-maintained.
- `scripts/check-coverage.py` (`make coverage`) checks:
  - each inventory against its map (unmapped or unexpected sources);
  - that each mapped chapter file cites the source, either by docs slug (`/squad/docs/<slug>/`, which works on any host) or by the exact pinned URL `https://github.com/bradygaster/squad/blob/<ref>/<path>`, where `<ref>` is `v1.1.0` or `v2.0.0-preview.2` (`SETS`, line 14). The owner `bradygaster` is hardcoded;
  - that each `source-modules.csv` module string (44 rows) appears in one of its listed book files.
- **Gap:** no tool checks the inventory against the upstream tree. The script never confirms that a source still exists at its ref, and never flags new upstream docs. Retargeting found 10 dead and 4 new sources that the current tooling cannot see.

### Source deltas (Markdown files under `docs/`)

| Range | Added | Deleted | Modified |
|---|---|---|---|
| v1.1.0 → v2.0.0 | 13 | 2 | 68 |
| v2.0.0-preview.2 → v2.0.0 | 4 | 8 | 63 |

No renames were detected (`git diff -M`).

**Removed. These inventory entries no longer exist at v2.0.0:**
- From `sources.txt` (removed by preview.2, kept at v1.1.0): `docs/src/content/docs/features/consult-mode.md`, `docs/src/content/docs/guide/personal-squad.md`.
- From `sources-2.0.txt` (removed between preview.2 and GA, when the whole `docs/proposals/` directory was deleted): `squad-2.0-security-and-isolation.md`, `contributor-guide-improvements.md`, `error-recovery.md`, `iterative-retrieval.md`, `memory-governance-provider.md`, `reflect.md`, `retro-enforcement.md`, `tiered-memory.md`.

**New at v2.0.0 and not in any inventory:**
- `docs/specification/adr-002-work-claims-and-external-queues.md`
- `docs/specification/adr-003-host-neutral-canonical-coordinator.md`
- `docs/src/content/docs/features/claude-code-plugin.md`: native Claude Code plugin, member subagents, hooks, dashboard
- `docs/src/content/docs/scenarios/multi-machine-watch.md`: `squad watch --claims`

**Modified preview.2 → GA:** 54 of the modified files are in `sources.txt` and 19 are in `sources-2.0.txt` (some are in both). Notable changes:
- `reference/cli.md`: adds `squad health --json` metadata, `watch --max-rounds/--max-duration/--claims`, and `squad dashboard`. `nap --deep` now keeps the last 3 sections. `history-archive/` became a per-agent `history-archive.md`.
- Other changed docs: `whatsnew.md`, `scenarios/upgrading.md`, `get-started/installation.md`, `get-started/migration.md`, `concepts/squad-2-0-architecture.md`, `reference/host-feature-matrix.md`, `features/state-backends.md`, `features/plugins.md`, `features/skills.md`, `features/ralph.md`, and both v0.2 specs.

**Source modules (`source-modules.csv`, 44 rows):**
- 43 exist at v2.0.0.
- `packages/squad-sdk/src/multi-squad.ts` exists only at v1.1.0. It was removed along with `cli/commands/{consult,extract,personal}.ts`, `agents/personal.ts` and `sharing/consult.ts`.
- New at GA and unmapped:
  - CLI commands: `cli/commands/{dashboard,hook,lockout}.ts`, `cli/dashboard/`, `dashboard-ui/`
  - SDK: `backend/harnesses/` (Copilot and Claude Agent SDK harnesses), `client/adapters/claude-{hooks,members,plugin,skills}.ts`, `ralph/claims{,-git}.ts`

### Recommendation: one inventory pinned to v2.0.0

The book is moving to 2.0 and staying as close to the current text as possible. Keeping two baselines would mean teaching two versions, so use one inventory pinned to v2.0.0:

1. Merge the inventories into `research/sources.txt`: 192 unique − 10 removed + 4 new = **186 sources**. Retire `sources-2.0.txt`.
2. Merge the two maps into one `research/coverage.csv`. Keep each row's current chapter. Map the 4 new sources:
   - `claude-code-plugin` → Vol 2 Ch 5 (dual-mode/clients) or Ch 19
   - `multi-machine-watch` and `adr-002` → Vol 1 Ch 9 (Ralph)
   - `adr-003` → Vol 2 Ch 17/18

   Keep extra assignments where a source is taught in two places, as the current Appendix H row does.
3. Material on removed features (consult, personal and global squads; the deleted proposals) is still cited, but only as history. Either cite it with explicit `v1.1.0` pins in an optional `legacy` list that the checker accepts as `ref=v1.1.0`, or drop the citations where the prose is cut. Do not leave links to unpinned live pages for these.
4. Change `scripts/check-coverage.py`:
   - set `SETS` to a single `("coverage.csv", "sources.txt", "v2.0.0")` entry, plus an optional legacy set;
   - change the owner in `pinned` to `github/squad`;
   - add an optional existence check (`--src <checkout>`) that fails when an inventoried path is missing at the ref and warns on uninventoried `docs/**/*.md` outside `blog/`, `_internal/release-checklist.md` and `research/`.
5. `research/build_coverage.py` is stale (old chapter numbers, one inventory only). Either rebuild it around `volN:NN` keys or delete it and treat the CSV as the source of truth. I prefer deleting it, because the CSV is what is reviewed.
6. `source-modules.csv`: drop or legacy-tag `multi-squad.ts`. Add rows for the new modules if writers cite them (dashboard, harnesses, the Claude adapters, claims).

## 2. Baseline run (today, before any change)

| Target | Result |
|---|---|
| `make coverage` | PASS: `coverage: 217/217 sources cited`, `source modules: 44/44 referenced` |
| `make manuscript` | PASS: regenerated Appendix E for both volumes (no diff), `Manuscript: 46 chapters; 0 structural errors` |
| Tools present | `pandoc`, `epubcheck`, `mmdc`, `node` (v26.13.1) are on PATH; `make validate`/`check` were not run (out of scope) |
| Tasktrack tests (`node --test sample/api/test/`) | **Not run to completion.** The test calls `server.listen(0)`, and this session's sandbox blocks local port binding, so the run hung and was stopped. Re-run outside the sandbox, or set `sandbox.network.allowLocalBinding: true`. |
| `make links` | Not run as-is: `check-links.sh` writes `/tmp/squad-book-links.txt`, which the sandbox does not allow, and it runs serially. I ran an equivalent probe in parallel instead (section 5). |

The coverage pass is real but hollow: it checks that citations are present, not that their targets resolve. Section 5 shows the pinned targets are currently 404.

Note: the `make` error `xcrun_db ... Operation not permitted` is sandbox noise and does not affect the results.

## 3. Tasktrack `sample/`

The sample has **no Squad configuration**: no `.squad/`, no `.github/agents`, no `.mcp.json`, and no scripts that call `squad`. It is a plain Node app with zero dependencies (`package.json` engines `>=22.18`, which is above Squad 2.0's `>=22.5.0` floor). Nothing breaks under 2.0. Only the progression text in the README needs editing:

| File:line | Current | 2.0 change |
|---|---|---|
| `sample/README.md:3` | "starting point for Volume 1, Chapters 2–4" | No change. Optionally state the tested Squad version (2.0.0). |
| `sample/README.md:19` | "Install Squad, `squad init`, first session, cast the team (backend, frontend, tester, reviewer)" | `squad init` still works. In 2.0, Copilot is the default host and `squad init --client <list>` selects other hosts. Rai and Fact Checker are opt-in (`squad roster add <rai\|fact-checker\|all>`). Add a `--client` mention if the chapter now shows multi-host setup. |
| `sample/README.md:24` | "a second squad for `web/`" | Still valid: project-local squads only. Make sure Vol 2 Ch 3 does not tell readers to use a personal or global squad, because `--global` is now a fatal error in `cli-entry.ts:141`. |
| `sample/README.md:27` | "Vol. 2, 18–22: Optional Squad 2.0 preview evaluation in a scratch copy" | At GA this is no longer a preview. Reword to "Squad 2.0: multi-host projection, upgrade from 1.1" (or whatever Arthur's part title becomes), and drop "scratch copy" unless the chapter keeps the 1.1 → 2.0 upgrade drill. |
| `research/VALIDATION.md` (Tasktrack line) | `node --test sample/api/test/` | Unchanged. It matches `sample/package.json` `"test": "node --test api/test/"`. |

If the 2.0 chapters add reader-visible checkpoints (`ch02-end` with `.squad/`), consider shipping a `sample/expected/` snapshot generated by `squad init` at 2.0.0. That is a follow-up, not a blocker.

## 4. Exercise solutions and quiz answers affected by 2.0

Items found by a grep sweep of `exercises/solutions/**` and checked against the v2.0.0 source:

| File:line | Problem under 2.0.0 |
|---|---|
| `vol1/ch02.md:8` | Calls 2.0 "preview software… keep 1.1.0 for everyone". 2.0.0 is now stable `latest`. |
| `vol1/ch02.md:16` | "`insider` carries the 2.0 preview…; `latest` is stable (v1.1.0)". `latest` is now 2.0.0. |
| `vol1/ch03.md:15` | "observed v1.1.0 flow… when Copilot starts Squad". Re-verify with 2.0's default host and `--client`. |
| `vol1/ch03.md:20` | Lists `--global` as an init flag. **Removed**: it is now `fatal: Unknown option: --global` (`cli-entry.ts:141-142`). |
| `vol1/ch04.md:23` (quiz Q3, built-in support identities) | Rai and Fact Checker are optional built-ins in 2.0, added with `squad roster add`. Q2 ("21 base roles") still holds: the role catalog is byte-identical. Only the "v1.1.0" wording needs changing. |
| `vol1/ch05.md:19`, `vol1/ch05.md:29` | Describe `squad consult` and personal-agent consultation. **Removed in 2.0** (`consult.ts`, `extract.ts`, `personal.ts` deleted). |
| `vol1/ch11.md:28`, `:38` | `squad rc` / `squad start` print `DEPRECATED` warnings in 2.0 (`cli-entry.ts:1055,1133`). Both still work. Add a deprecation note. |
| `vol1/ch16.md:9` | Nap behaviour (keeps 5 sections, appends to `history-archive.md`) matches 2.0. Add that `nap --deep` keeps 3. No error. |
| `vol2/ch01.md:5`, `:8` | Pinned to "current v1.1.0" `.mcp.json` / `--mcp-frontmatter` behaviour. The flag still exists, but 2.0 writes per-host MCP wiring via `--client`. Re-verify. |
| `vol2/ch03.md:20` | Explains `multi-squad.ts` (personal squad directories). **File removed in 2.0.** |
| `vol2/ch04.md:4`, `:21` (quiz Q5), `:22` (Q6) | Upstream precedence. 2.0 resolves upstreams at runtime through `squad_state_upstreams` with **earlier-wins**, local first, depth 3. `upstream/resolver.ts` was largely rewritten (+1218/−516 lines across the module diff). The "not demonstrated / later-wins" claims and Q6 ("absent from v1.1.0 CLI help") need rework. |
| `vol2/ch11.md:16` | "v1.1.0 checkout contains no `adr-001*`". At 2.0.0, `adr-001`, `adr-002` and `adr-003` exist. |
| `vol2/ch17.md:13`, `:24` | Same: `client-harness-adapters`, `client-backend-decoupling` and ADR-001 are now present at the target tag. |
| `vol2/ch18.md:15` | Expected version `2.0.0-preview.2`. Change to `2.0.0`. |
| `vol2/ch22.md:5` | `@insider` default for a prerelease CLI. Stable 2.0.0 now follows `@latest`. |
| `vol2/ch22.md:19` (quiz Q1) | "`latest` remains on Squad 1.1.0". **Now false**: `latest` is 2.0.0. |
| `vol2/ch22.md:26` | The rollback to 1.1.0 answer is still valid as a procedure. Check its framing. |

Items that hold under 2.0 and only need the "v1.1.0" label changed:
- `vol1/ch08.md:27`: no `--introspect` flag.
- `vol1/ch10.md:16`, `:42`: `.squad/workstreams.json` resolver.
- `vol1/ch13.md:5`: `notifyLevel` is still not passed to `reportBoard`.
- `vol1/ch15.md:11`: no `convert-memory` command.
- `vol2/ch24.md:15`: no `squad prd` command.
- `vol2/ch18.md:9,13,22,24`: these already describe GA behaviour.
- `vol2/ch21.md:5`: state tool list.

**Mechanical issue:** 30+ solution lines are scoped "in v1.1.0…" (for example `vol1/ch07`, `ch09`, `ch14`, `ch16`, `ch17`, `ch18`, `ch19`; `vol2/ch10`, `ch14`, `ch16`, `ch25`). Each one needs a re-check against 2.0.0 before its label changes. Do not do a blind `s/v1.1.0/v2.0.0/`. These claims concern behaviour, and some of that behaviour changed.

## 5. Links to `bradygaster/squad` and the old docs site

All counts come from `grep` over `book/`, using the same extraction as `scripts/check-links.sh`. There are 435 URL occurrences in total, 318 of them unique.

| Pattern | Occurrences | Unique | Live status today |
|---|---|---|---|
| `https://bradygaster.github.io/squad/...` | 227 | 150 | **All 404**: the old Pages site is gone |
| `https://github.com/bradygaster/squad/...` | 181 | 149 | 145 return 404 (every `blob/` and `tree/` link); 4 return 200 (repo root, issues, pulls, releases/latest), because a repo still exists at that name |
| `raw.githubusercontent.com/bradygaster/squad/main/scripts/install.sh` | 1 | 1 | 404 |
| Already `github/squad` or `github.github.*` | 0 | 0 | — |

Pinned refs in the book: `blob/v1.1.0` ×121, `tree/v1.1.0` ×20, `blob/v2.0.0-preview.2` ×32, `main` ×2, plus `releases/tag/v2.0.0-preview.2`.

**Is a mechanical rewrite safe? Yes for URLs, with exclusions.** I rewrote every unique old URL and probed the new targets:
- `bradygaster.github.io/squad/` → `github.github.com/squad/`;
- `github.com/bradygaster/squad` → `github.com/github/squad`.

Of 299 rewritten URLs, 297 returned 200. All tags (`v1.1.0`, `v2.0.0-preview.2`, `v2.0.0`) exist at `github/squad`, so pinned blob paths still resolve. The 2 failures need a writer to decide:
- `https://github.github.com/squad/docs/`: use `/squad/` instead.
- `.../docs/guide/personal-squad/`: the page was removed. Cited in `book/vol1/part-01/ch02-installation.md:411`. Repin it to `github.com/github/squad/blob/v1.1.0/docs/src/content/docs/guide/personal-squad.md` or drop it along with the prose at `ch02:227`.

**Do not rewrite:**
- `@bradygaster/squad-cli` (26 occurrences) and `@bradygaster/squad-sdk` (90). These npm package names are unchanged at 2.0.0.
- Non-URL mentions that are config values, not links. Edit these by hand:
  - `book/vol1/part-01/ch02-installation.md:76`: install-script `REPO` default, which becomes `github/squad`
  - `book/vol2/part-02/ch08-cicd-release.md:62` and `:231`: `gh aw add` workflows spec, which becomes `github/squad/workflows@…` (per the v2.0.0 `guide/gh-aw.md:131`)
  - `book/vol2/part-05/ch25-contributing.md:77`, `:82` and `:138`: fork, clone and PR base
- `releases/tag/v2.0.0-preview.2` and `blob/v2.0.0-preview.2/...`: these resolve after the host swap, but they should be **repinned to `v2.0.0`** as part of the retarget, not just re-hosted. Check that each path still exists at v2.0.0; the 8 `docs/proposals/*` paths do not.

The rewrite must land in the same change as the `check-coverage.py` owner update. Otherwise pinned citations stop matching and `make coverage` fails.

Old URLs also appear outside `book/`: `README.md`, `research/*.md`, 5 `exercises/solutions` files and `scripts/check-coverage.py`. `.github/agents` and `.github/skills/*` contain them too, but those are Squad-managed and are refreshed by `squad upgrade`, not by hand.

## Recommended work package

**Slartibartfast (scripts and build)**
1. `scripts/check-coverage.py`: single v2.0.0 set, optional v1.1.0 legacy set, `github/squad` owner in `pinned`, optional `--src` existence and new-source check (section 1).
2. `scripts/check-links.sh`:
   - write to `${TMPDIR:-/tmp}` via `mktemp`, not a fixed `/tmp` path;
   - probe in parallel (`xargs -P`);
   - add an allowlist for known redirects;
   - fail on any `bradygaster.github.io` or `github.com/bradygaster/squad` URL, as a regression guard after the rewrite.
3. Run the URL rewrite with the two host substitutions above, restricted to `https?://` URLs, in `book/`, `exercises/`, `research/*.md` and `README.md`, in the same commit as step 1. Then hand-edit the six config-value lines and the two 404s.
4. Delete or rebuild `research/build_coverage.py`.
5. Bump the tested-tooling line in `VALIDATION.md` when `make check` is re-run.

**Marvin (coverage, sample, exercises)**
1. Build the merged 186-source `research/sources.txt` and `coverage.csv` against v2.0.0 (commit `26654f0c`). Retire `sources-2.0.txt` and `coverage-2.0.csv`. Update `source-modules.csv`: remove or legacy-tag `multi-squad.ts`, and add the new modules the writers cite.
2. Update `sample/README.md:19,24,27`. Re-run the Tasktrack tests with local binding allowed.
3. Revise the solution and quiz items in section 4, and re-verify each "v1.1.0"-scoped claim against the v2.0.0 source before changing its label. Then run `make quiz manuscript coverage`.
4. Verify CLI help against an installed 2.0.0 CLI in a disposable repo, after the user approves the install (`npm i -g @bradygaster/squad-cli@latest`). Replace the VALIDATION.md line "installed CLI reports 1.1.0".
5. Rewrite `research/VALIDATION.md` "Baseline" and "2.0 rescan" sections for the single v2.0.0 baseline.

**Writers (Ford: Vol 1 and shared appendices; Trillian: Vol 2 and appendices G–J)**
- **Ford:**
  - personal/global squad and consult-mode prose: `vol1/ch02:227,411`, Ch 5, and Appendix A's `--global` row;
  - `latest`/`insider` channel text in Ch 2;
  - Rai and Fact Checker as opt-in built-ins in Ch 4;
  - `rc`/`start` deprecation in Ch 11;
  - new `watch --claims/--max-rounds/--max-duration` and `squad health --json` in Ch 9 and Appendix A;
  - `squad dashboard` and the Claude Code plugin wherever clients are introduced.
- **Trillian:**
  - Vol 2 Part IV moves from "preview" to GA (Ch 18–22);
  - upstream earlier-wins precedence and runtime resolution (Ch 4);
  - removal of `multi-squad.ts` (Ch 3);
  - ADR-001/002/003 now exist (Ch 11, 17);
  - experimental backend/harness status, unchanged and still experimental, plus the new `backend/harnesses` (Ch 14, 19–20);
  - contributing URLs (Ch 25);
  - `gh aw` workflow spec (Ch 8).
- **Both:** cite against `blob/v2.0.0/...`, never `main` or the live site alone.

## Citations writers must add/remove (WP-M, applied 2026-11-20)

The inventory is now a single 186-source v2.0.0 set, with 213 coverage rows and 48 source modules. The checker has no pending status, so **`make coverage` fails until every Add row below is cited**. You can cite with the docs slug (`https://github.github.com/squad/docs/<slug>/`) or the pin `https://github.com/github/squad/blob/v2.0.0/<path>`. These were measured with a local copy of `check-coverage.py` patched to the agreed single set: 207/213 sources and 43/48 modules pass, and the 11 failures are exactly the Add rows.

**Add: docs sources (6 coverage rows)**

| Owner | Chapter file | Source to cite |
|---|---|---|
| Ford | `book/vol1/part-02/ch09-ralph-loop.md` | `docs/src/content/docs/scenarios/multi-machine-watch.md` (slug `/squad/docs/scenarios/multi-machine-watch/`) |
| Trillian | `book/vol2/part-03/ch17-specification.md` | `docs/specification/adr-002-work-claims-and-external-queues.md` |
| Trillian | `book/vol2/part-04/ch19-across-clients.md` | `docs/src/content/docs/features/claude-code-plugin.md` (slug `/squad/docs/features/claude-code-plugin/`) |
| Trillian | `book/vol2/part-04/ch20-host-projections.md` | `docs/specification/adr-003-host-neutral-canonical-coordinator.md` |
| Trillian | `book/vol2/appendices/app-I-spec-cheatsheet.md` | `docs/specification/adr-002-work-claims-and-external-queues.md` |
| Trillian | `book/vol2/appendices/app-I-spec-cheatsheet.md` | `docs/specification/adr-003-host-neutral-canonical-coordinator.md` |

**Add: module strings (5 `source-modules.csv` rows). The literal path must appear in at least one of the listed files.**

| Owner | File(s) | Module string |
|---|---|---|
| Trillian (or Ford, App A) | `vol2/part-04/ch19-across-clients.md` or `shared/appendices/app-A-cli-reference.md` | `packages/squad-cli/src/cli/commands/dashboard.ts` |
| Trillian (or Ford, App A) | `vol2/part-04/ch20-host-projections.md` or `shared/appendices/app-A-cli-reference.md` | `packages/squad-cli/src/cli/commands/lockout.ts` |
| Trillian (or Ford, App A) | `vol2/part-04/ch20-host-projections.md` or `shared/appendices/app-A-cli-reference.md` | `packages/squad-cli/src/cli/commands/hook.ts` |
| Trillian | `vol2/part-04/ch21-state-boundary-backend.md` | `packages/squad-sdk/src/backend/harnesses` |
| Ford | `vol1/part-02/ch09-ralph-loop.md` | `packages/squad-sdk/src/ralph/claims.ts` |

**Remove or keep as history. Coverage no longer tracks these, so the checker will not fail either way.**

| Owner | File:line | Citation | Action |
|---|---|---|---|
| Ford | `vol1/part-01/ch02-installation.md:411` (prose at l.227) | `guide/personal-squad.md` (v1.1.0 pin) | Delete it with the personal-squad prose, or keep it only in a "Removed in 2.0" note. Do not link to the live docs page, which is 404. |
| Ford | `vol1/part-02/ch05-routing.md:242` | `features/consult-mode.md` (v1.1.0 pin) | Same as above. |
| Trillian | `vol2/part-04/ch18-squad-2-overview.md:363` | `docs/proposals/squad-2.0-security-and-isolation.md` (preview.2 pin) | Remove. Rebase the section on shipped behavior (plan §Ch 18). |
| Trillian | `vol2/part-04/ch22-upgrading-to-2.md:531-537` | 7 `docs/proposals/*.md` (preview.2 pins) | Remove. These files never existed at v1.1.0 and are gone at v2.0.0 (FC #20). |
| Trillian | `vol2/part-01/ch03-cross-squad.md` | `packages/squad-sdk/src/multi-squad.ts` | The module row is dropped. Remove the walkthrough, or describe it as removed in 2.0. |

**Unchanged but re-verify:** all other 207 rows are still cited. Slug citations match on any host. Path citations match the bare repo path, so `blob/v1.1.0/` pins also pass today. Slartibartfast's WP-S1 repin to `blob/v2.0.0/` is still required for link correctness, but it is not needed for coverage.
