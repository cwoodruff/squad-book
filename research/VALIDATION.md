# Verification scope

## Baseline

- Upstream: `https://github.com/github/squad` (moved from `bradygaster/squad`; the npm scope `@bradygaster/` is unchanged).
- Release: `v2.0.0` (second edition).
- Commit: `26654f0c4dadb2625d764c1c69ec61da6c518094`.
- Upstream license: MIT.

The whole book targets v2.0.0. The first edition, written against v1.1.0 (commit `c24da2aad2ab7576f6b68dec2bc50b2fe2dc7a8a`), is tagged `book-squad-v1.1.0` in this repository. v1.1.0 and the 2.0 previews appear in the manuscript only as history (Volume 2, Chapter 22 and Appendix J).

## Source inventory and maps

There is one inventory and one map, both checked against v2.0.0:

- `research/sources.txt` lists 186 upstream sources: the 183 `docs/**/*.md` pages outside the blog, `docs/_internal/` and `docs/research/` trees, plus 3 hand-curated `docs/_internal/specs/*` files. One repo-relative path per line, sorted. Lines starting with `#` are ignored by both checkers.
- `research/coverage.csv` (`source,chapter`) has 213 rows that map those 186 sources to volume-qualified chapters or appendices. 213 is a count of citation assignments, not of distinct documents.
- `research/source-modules.csv` maps 48 SDK/CLI source modules and files to the book sections that name them.

Changes from the first edition: the separate 2.0-preview inventory and map were merged into these files and deleted. Sources removed upstream by v2.0.0 (`features/consult-mode.md`, `guide/personal-squad.md`) and the `multi-squad.ts` module were dropped, and no `docs/proposals/*` row remains (that tree is not in v1.1.0 or v2.0.0). All 13 docs pages added between v1.1.0 and v2.0.0 are inventoried. Links to the removed pages survive only as labelled v1.1.0 history pins in Appendix F.

`coverage.csv` and `sources.txt` are maintained by hand. `research/build_coverage.py` no longer generates them. Run with `--src <checkout at the pinned tag>`, it checks that every inventoried source and listed module exists upstream, that the inventory and map agree, and it warns about upstream pages that are not inventoried.

## Automated and integration checks

- `make coverage` (`scripts/check-coverage.py`) checks that each mapped source is cited in its chapter, that every inventoried source is mapped, and that each module in `source-modules.csv` is named in at least one listed section. It matches bare repo paths, so it does not detect stale refs or dead links.
- `make manuscript` checks each volume's chapter sequence (Volume 1: 1–21; Volume 2: 1–25) and matching per-volume solution files, the prerequisites callout, required sections, exercise and quiz solutions, at least two diagrams per chapter, shared appendices A–D and F, Volume 2 appendices G–J, per-volume front matter, and invalid XML control characters. It also regenerates both Appendix E files.
- `make check` builds both volumes and validates each EPUB with epubcheck. Mermaid rendering is mandatory: a rendering error stops the build.
- `make links` (`scripts/check-links.sh`) probes the external URLs in `book/` and `exercises/` (not `sample/` or the root README), skips loopback and placeholder hosts, and fails on any broken URL or any URL on the old `bradygaster` hosts.
- The Tasktrack API is tested with `node --test` in `sample/` (`npm test`). The tests cover health, task creation and listing, invalid and oversized JSON, status changes, missing IDs, and deletion.

## What was verified for the 2.0.0 update — November 2026

Results as recorded in `research/reviews/` on 2026-11-21, branch `squad-2.0`, uncommitted:

- **Inventory.** `python3 -I research/build_coverage.py --src <v2.0.0 checkout>`: 186 sources, 48 modules, 0 errors, and no "upstream doc not inventoried" warnings (`inventories-review.md`).
- **Coverage.** `make coverage`: 213/213 sources cited, 48/48 source modules referenced.
- **Manuscript.** `make manuscript`: 46 chapters (21 + 25), 0 structural errors. Reviewers reran it after each later chapter revision with the same result.
- **EPUB.** `make epub` and epubcheck 5.4.0 (`build-review.md`): 0 fatals, 0 errors and 0 warnings for both EPUBs. Both were run outside the sandbox, because inside it mermaid-cli's Chrome cannot launch and Java image decoding reports every PNG as a false `PKG-021`. Chapters were revised after this build, so the EPUBs must be rebuilt and rechecked before release.
- **Links.** `make links` (`build-review.md`, approved in Marvin's re-review): exit 0, 308 unique URLs found, 301 checked, 7 skipped (local or placeholder hosts), 0 broken. This is the rewritten script; the first version, which probed only 1 URL, was rejected (R1, R2). Known limitation: each URL is probed once with no retry, so a transient 5xx fails the run.
- **End-to-end CLI checks** (`e2e-checks.md`), with the 2.0.0 CLI and an isolated 1.1.0 install, on scratch copies of `sample/` with a scratch `HOME`:
  - Volume 1, Chapter 3: a real 2.0.0 `squad init` matches the annotated tree, the state-files table and the template table. Pass.
  - Volume 2, Chapter 22: the 1.1.0 → 2.0.0 migration drill (init, dry run, upgrade, `--client claude`, doctor and health, rollback). Most steps pass. It found two accuracy errors about an uncast team (`doctor` exits 0 with no warnings, and `squad health` reports three failures and exits 1) and one minor wording issue (F1–F3). All three are fixed and approved, 2026-11-21: Trillian's fixes at Ch 22 l.434 (F3) and l.445 (F2) passed Arthur's review, and Ford's revision of l.392 (F1) passed Arthur's re-review (R1).
  - Volume 2, Chapter 19: the Git removal route for a projected client (`client add claude,codex`, then removal). It works as written. Pass.
- **Blocked.** The Tasktrack tests did not run in this update: the sandbox denies local port binding (`listen(0)` fails with `EPERM`), so the test's `before()` hook never resolves. The test code is unchanged since the first edition, where all six tests passed.

## Deliberate limits

Source citations and structural checks do not prove that every explanation or API example is correct. The full prose has not received a separate line-by-line editorial review.

Only the steps listed above were run end-to-end. Of the seven hosts, the Copilot, Claude Code and Codex projections were generated and inspected as files. No host was installed, authenticated and driven through a session. The other multi-client commands and examples are source-based. SDK examples were not all compiled or executed. Cloud resources were not provisioned, chargeable services were not invoked, and GitHub Actions was not run remotely. Infrastructure walkthroughs are source-based teaching material.

Sandbox effects on the checks: Node's built-in `https` ignores the sandbox proxy unless `NODE_USE_ENV_PROXY=1` is set. Without it, a 1.1.0 `squad init` pins `@insider` instead of `@1.1.0`. Mermaid rendering, epubcheck image decoding and the Tasktrack tests need to run outside the sandbox.

The local book build uses Pandoc 3.14, EPUBCheck 5.4.0, Mermaid CLI and system Chrome. CI (`.github/workflows/build-epub.yml`) runs coverage, manuscript and validate. It should be run once the branch is pushed.

## First edition history (v1.1.0)

- The first edition inventoried 175 sources at v1.1.0. A later preview rescan (v2.0.0-preview.2) added 41 sources in a separate preview inventory and map, for a total of 217 citation assignments and 44 source modules. The 2.0.0 update replaced both sets with the single inventory above.
- October 27–28, 2026: `make check` passed with 217/217 citations, 44/44 modules, 0 structural errors and 0 EPUBCheck errors or warnings, and the six Tasktrack tests passed. The book was then split into two volumes, with per-volume chapter numbering (Volume 1: 1–21, Volume 2: 1–25) and per-volume part numbering (Volume 2: Parts I–V). The checks were rerun after each step with the same results.
