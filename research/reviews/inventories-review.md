# Review: 2.0 source inventory and coverage map (WP-M)

- Reviewer: Slartibartfast (Build Engineer). Author: Marvin.
- Date: 2026-11-21. Branch `squad-2.0`, uncommitted, compared with `book-squad-v1.1.0`.
- Files: `research/sources.txt`, `research/coverage.csv`, `research/source-modules.csv`, `research/build_coverage.py`, and the deletions of `research/sources-2.0.txt` and `research/coverage-2.0.csv`.
- Standard: author requirements (v2.0.0, `github.com/github/squad`), `.squad/decisions.md` and the inbox, `research/UPDATE-PLAN-2.0.md` (WP-M, §1.1), `research/UPDATE-PLAN-2.0-FACTCHECK.md` (#20), and the Squad v2.0.0 source.

## Verdict: APPROVE

There are no required changes.

## Results

| Check | Result |
|---|---|
| `python3 -I research/build_coverage.py --src <squad-v2.0.0>` | `inventory: 186 sources, modules: 48, errors: 0`, exit 0. No "upstream doc not inventoried" warnings. |
| `make coverage` | `coverage: 213/213 sources cited`, `source modules: 48/48 referenced`, exit 0. |
| Upstream docs vs inventory | All 183 `docs/**/*.md` outside the excluded trees (blog, `_internal/`, `research/`) are in `sources.txt`. The other 3 inventoried sources are the hand-curated `docs/_internal/specs/*` files. |
| Docs added v1.1.0 → v2.0.0 (`git diff --name-status v1.1.0 v2.0.0 -- docs`) | All 13 added pages are inventoried: SQUAD-2.0-OVERVIEW, ADR-001/002/003, the two v0.2 specs, squad-2-0-architecture, claude-code-plugin, host-feature-matrix, multi-machine-watch, using-squad-across-clients, and the two tutorials. No `.mdx` pages exist upstream. |
| Removed sources | `consult-mode.md` and `personal-squad.md` (the only 2 docs deleted upstream) are gone from both files. No `docs/proposals/*` row remains (decisions.md l.14; FC #20: `docs/proposals/` is not at v1.1.0 or v2.0.0). The `multi-squad.ts` module row is gone, and the file is absent at v2.0.0. |
| Plan WP-M map changes (UPDATE-PLAN l.333–337) | adr-002 → vol2:17 (+I), adr-003 → vol2:20 (+I), claude-code-plugin → vol2:19, multi-machine-watch → vol1:9. The module rows for client/adapters and the client, roster, dashboard, lockout and hook commands are present. |
| coverage.csv shape | `source,chapter`, 213 rows, no duplicates. `sources.txt` is sorted with no comments. Every row passes the per-row check in `check-coverage.py`, so each source is cited in the chapter it is mapped to. |
| The 3 `book/appendices/` rows | `runtime` → `book/shared/appendices/app-B-configuration.md`, `cli` and `cli-entry.ts` → `book/shared/appendices/app-A-cli-reference.md`. Each target file exists and contains the module string. `book/appendices/` does not exist, and no remaining file references it. |
| build_coverage.py no longer writes | Safe. The Makefile `coverage` target runs only `scripts/check-coverage.py`. Nothing in `scripts/` calls `build_coverage.py`. `.github/workflows/build-epub.yml` runs `make coverage`, `make manuscript` and `make validate` only. `check-coverage.py` reads `coverage-2.0.csv`/`sources-2.0.txt` only as an optional pair, and it skips the pair when the files are absent. |

## Old-tag pins in book/** and exercises/**

None of the 12 pins listed in `research/LINKS-2.0-LEFTOVERS.md` remain. The writers removed them all.

Three old-tag pins remain, all in a labelled "Historical (1.1.0)" section:

- `book/shared/appendices/app-F-resources.md:67`: `blob/v1.1.0/.../features/consult-mode.md`
- `book/shared/appendices/app-F-resources.md:68`: `blob/v1.1.0/.../guide/personal-squad.md`
- `book/shared/appendices/app-F-resources.md:69`: `blob/v1.1.0/README.md`

These follow the decisions.md l.13 rule (v1.1.0 history pins are allowed). They are not inventoried, so coverage does not count them. No other `blob/`, `tree/` or `raw` link uses a ref other than v2.0.0. The only exception is the two install-script `raw.../github/squad/main/` URLs at `book/vol1/part-01/ch02-installation.md:67,79`, which are install commands, not pins.

## Required changes

None.

## Follow-ups (outside this gate)

1. **Marvin: `research/VALIDATION.md`** (WP-M slot, UPDATE-PLAN l.318/332/358; assessment step 5). The file still describes the v1.1.0/bradygaster baseline, 175 sources, and `sources-2.0.txt`/`coverage-2.0.csv` as live files. Those files are now deleted. Rewrite it before WP-M closes.
2. **Marvin: stale extra sections in `source-modules.csv`.** These do not fail the checker, because the agreed rule only needs one listed section to cite the module.
   - Three citations were lost during the 2.0 edits:
     - `src/index.ts` → `vol2/part-01/ch03-cross-squad.md` (l.11)
     - `src/sharing` → `vol1/part-02/ch05-routing.md` (l.22)
     - `squad-cli/src/cli` → `vol1/part-02/ch05-routing.md` (l.32)
   - Five predate 2.0:
     - `config` → vol1 ch03 (l.8)
     - `platform` → vol2 ch05 (l.15)
     - `ralph` → vol2 ch05 (l.17)
     - `cli` → vol1 ch02 (l.32, also listed twice)
     - `cli-entry.ts` → vol1 ch02 (l.33)

   Prune them, or restore the citations.
3. **Arthur or Marvin: `CONTRIBUTING.md:9`.** It says to update `coverage.csv` "(`research/build_coverage.py`)", which reads as if the script generates the map. It should say: edit `sources.txt` and `coverage.csv` by hand, then run `build_coverage.py --src` to validate.
4. **Advisory: `build_coverage.py:29`.** It does not skip `#` lines in `sources.txt`, but `check-coverage.py` does. The file has no comments today, so this does not fail anything yet.

## Follow-ups (Marvin)

Marvin, 2026-11-21. `make coverage`: 213/213 sources, 48/48 modules. `python3 -I research/build_coverage.py --src <squad-v2.0.0>`: 186 sources, 48 modules, 0 errors, exit 0.

1. **`research/VALIDATION.md`** (whole file). Rewritten for the second edition. The baseline is github/squad v2.0.0, commit `26654f0c…` (l.3–10). There is one inventory: `sources.txt` 186, `coverage.csv` 213 rows, `source-modules.csv` 48 (l.12–22). l.24–30 cover the checks. l.32–45 record only what was run in this update: inventory, coverage, manuscript, epubcheck (from `build-review.md`, with a note that the EPUBs must be rebuilt after later chapter edits), the links status (check-links.sh R1/R2 pending, equivalent probe clean), the three e2e checks from `e2e-checks.md`, and the Tasktrack tests as **blocked** (sandbox EPERM on local port binding). l.47–55 cover limits: no host driven through a session, sandbox effects, and tool versions. l.57–60 condense the first-edition history. `sources-2.0.txt` and `coverage-2.0.csv` are no longer named.
2. **`research/source-modules.csv`**: pruned the stale sections. I added no chapter citations.
   - l.8 `config`: dropped vol1 ch03.
   - l.11 `index.ts`: dropped vol2 ch03.
   - l.15 `platform`: dropped vol2 ch05.
   - l.17 `ralph`: dropped vol2 ch05.
   - l.22 `sharing`: dropped vol1 ch05.
   - l.32 `cli`: dropped both vol1 ch02 entries and vol1 ch05.
   - l.33 `cli-entry.ts`: dropped vol1 ch02.
   
   Every remaining section on these 7 rows contains the full module string, which I checked per section.
3. **`CONTRIBUTING.md:9`**: now says to add new doc pages to `sources.txt` and `coverage.csv` by hand, then run `build_coverage.py --src` to validate. The script checks the map but does not generate it.
4. **Advisory, `research/build_coverage.py:29–30`**: skips `#` lines in `sources.txt`, using the same rule as `check-coverage.py`. Tested on a scratch copy that had a leading `# comment` line: still 186 sources, 0 errors.
5. **For review with the above, `sample/README.md`**:
   - l.19: Vol. 1, 1–4 now says "Install Squad 2.0, `squad init` (Copilot host by default)".
   - l.24: Vol. 2, 1–5 now says "a second project-local squad for `web/`".
   - l.27: Vol. 2, 18–22 now says "Project the same team into more hosts (Copilot-only fallback); a 1.x→2.0 migration drill on a scratch copy pinned to Squad 1.1.0".

## Review of follow-ups

- Reviewer: Slartibartfast. Date: 2026-11-21. Scope: Marvin's follow-ups 1–5 above, compared with `book-squad-v1.1.0`.

### Verdict: REJECT

One file, `research/VALIDATION.md`, has three required changes (V1–V3). Everything else passes.

### Results

| Check | Result |
|---|---|
| `make coverage` | 213/213 sources cited, 48/48 modules referenced, exit 0. |
| `python3 -I research/build_coverage.py --src <squad-v2.0.0>` | 186 sources, 48 modules, 0 errors, exit 0. The checkout HEAD is `26654f0c4dad…`, which matches VALIDATION.md l.7. |
| `source-modules.csv` l.8, 11, 15, 17, 22, 32, 33 | **Pass.** Every section listed on every row (all 48, not just these 7) contains the module string. The duplicate vol1 ch02 entry on l.32 is gone. No citations were added. |
| `CONTRIBUTING.md:9` | **Pass.** It now says sources.txt and coverage.csv are edited by hand, then validated with `build_coverage.py --src`. That matches the script. |
| `build_coverage.py:29–30` | **Pass.** `not l.startswith("#")` is the same rule as `scripts/check-coverage.py:28`. |
| `sample/README.md` l.19, 24, 27 | **Pass, minimal (3 lines).** l.19 matches "Copilot is the default host" (Vol 2 Ch 18 l.240, Vol 1 Ch 3). l.24 "project-local squad for `web/`" matches the nested `web/.squad` peer in Vol 2 Ch 3 l.207–215, and it does not imply the personal squads that were removed (Ch 3 l.16). l.27 drops the "preview" framing. It matches Ch 22 l.12 ("scratch copy pinned to Squad 1.1.0") and the Copilot-only path in Ch 18 l.240. No "preview" remains in the file. |
| VALIDATION.md baseline and inventory (l.3–22) | **Pass.** Commit, upstream, the `@bradygaster/` npm scope (squad-cli and squad-sdk `package.json` at v2.0.0), and the counts 186/213/48 are all correct. The first-edition facts at l.57–60 (175, 41, 217, 44, c24da2a, six tests) match `git show book-squad-v1.1.0:research/VALIDATION.md`. Pandoc is 3.14 locally. The mermaid hard-fail is at `scripts/mermaid.lua:19`. The `make check` chain is in the Makefile. |
| VALIDATION.md EPUB, manuscript, Ch 3 and Ch 19 e2e, blocked Tasktrack | **Pass.** These match `build-review.md` l.49–50 and `e2e-checks.md` a, c and d. Nothing is claimed beyond what ran. |

### Required changes

- **V1. `research/VALIDATION.md:29`: the `make links` scope is wrong.**
  - What/why: it says the script probes `book/`, `exercises/`, `sample/` and the root README. `scripts/check-links.sh:4,27` scans only `book exercises`. The broader scope was the one-off equivalent probe in `build-review.md` l.52, not the check. The file describes a check that does not exist.
  - Clearing condition: l.29 names the directories the script actually scans. Alternatively, if Arthur extends the script to `sample/` and `README.md`, the text matches the script as merged.
- **V2. `research/VALIDATION.md:40`: the links status is now wrong.**
  - What/why: l.40 says the fix "is pending". Arthur's rewrite (`build-review.md` l.65–74) now passes `make links`: 308 unique URLs found, 301 checked, 7 skipped, 0 broken. Marvin's re-review has since approved it. l.40 now reports an obsolete failure and omits the real run.
  - Clearing condition: l.40 records the approved `make links` run: exit 0, 308 unique URLs found, 301 checked, 7 skipped (the loopback and placeholder list), 0 broken. The R1/R2 history shrinks to at most one clause.
- **V3. `research/VALIDATION.md:43`: the Ch 22 e2e outcome is stale.**
  - What/why: l.43 says F1/F2 "were reported to the Chapter 22 writer". `e2e-checks.md` now records Trillian's F1–F3 fixes and Arthur's review. That review approved F2 and F3 and rejected F1 (Ch 22 l.392, R1: the sentence now reads as a claim about the step-3 tree, where the global 2.0 `doctor` fails the bridge version check). A verification record must state the current result, not the first report.
  - Clearing condition: l.43 states the final status of F1–F3 once Arthur's R1 clears, for example "fixed and re-verified" with the date. If R1 is still open when WP-M closes, l.43 names it as open.

Coordinator update (2026-11-21): Marvin's link-checker re-review confirms V1 independently and approves the rewritten `check-links.sh`. As a result, V2 no longer depends on the re-review and applies now. VALIDATION.md states neither point correctly.

Nothing else is required. Not required: l.31 omits the "rejects empty titles" test from its list, but the list is only a summary.

## Revision (Trillian): VALIDATION.md

Date: 2026-11-21. Successor to Marvin (locked out). Each fact was checked against its source before writing.

- **V1, `research/VALIDATION.md:29`:** the `make links` scope is now `book/` and `exercises/` only, "not `sample/` or the root README". Source: `scripts/check-links.sh:4,27` (`grep -rhoE … book exercises`). The line also notes the loopback/placeholder skip list and that broken URLs fail the run.
- **V2, `research/VALIDATION.md:40`:** replaced "fix is pending" with the approved run: `make links` exit 0, 308 unique URLs found, 301 checked, 7 skipped (local or placeholder hosts), 0 broken. Source: `build-review.md` l.74 (Arthur) and l.84–101 (Marvin's re-review, APPROVE). R1/R2 history is one clause. Added the no-retry limitation from `build-review.md` l.107.
- **V3, `research/VALIDATION.md:43`:** the Ch 22 drill now states the final status: F1–F3 fixed and approved, 2026-11-21. F3 (l.434) and F2 (l.445) passed Arthur's review; Ford's F1 revision (l.392) passed Arthur's "Re-review (R1)". Source: `e2e-checks.md` l.79–87.
- **Other lines checked, not changed:** l.36–39 and l.41–45 still match the reviews. l.39 (epubcheck ran before later chapter edits; the EPUBs must be rebuilt and rechecked before release) is still true. l.55 (CI not yet run) is still true.

Requesting re-review from Slartibartfast.

## Re-review: VALIDATION.md

- Reviewer: Slartibartfast. Date: 2026-11-21. Scope: Trillian's revision of `research/VALIDATION.md` l.29, l.40 and l.43, plus the unchanged l.39 and l.55.

### Verdict: APPROVE

V1, V2 and V3 are all cleared. Nothing in the file claims a check that did not run.

| Item | Result |
|---|---|
| V1, l.29 | **Met.** The text says "`book/` and `exercises/` (not `sample/` or the root README)". That matches `scripts/check-links.sh:4` (header) and `:27` (`grep -rhoE … book exercises`). The skip-list and fail-condition wording matches `:11-20`, `:31-34` and `:57-65` (old-host or any `BROKEN` sets `fail=1`). |
| V2, l.40 | **Met.** The text gives exit 0, 308 found, 301 checked, 7 skipped and 0 broken. That matches Marvin's re-review run (`build-review.md` l.98) and his APPROVE (l.84–86). The R1/R2 history is one clause, and "probed only 1 URL" matches the first review (l.26). The no-retry limitation matches Marvin's note (l.107). |
| V3, l.43 | **Met.** The text says F1–F3 were fixed and approved on 2026-11-21: F3 l.434 and F2 l.445 by Arthur's review, and Ford's F1 l.392 by Arthur's "Re-review (R1)". That matches `e2e-checks.md` (Arthur's review, Ford's revision, and the R1 APPROVE at l.87). |
| l.39 (EPUBs must be rebuilt) | **Still true.** `dist/mastering-squad-vol1.epub` and `vol2.epub` are from 08:34 and 08:34 on 2026-11-21. `book/vol2/part-04/ch22-upgrading-to-2.md` (08:46), ch23 and ch25 are newer. |
| l.55 (CI not yet run) | **Still true.** The 2.0 changes are uncommitted on `squad-2.0`. `origin/squad-2.0` is at `120d923`, so no CI run covers this working tree. (`gh run list` could not be checked from the sandbox because of a TLS error. That does not affect this conclusion.) |

### Required changes

None.
