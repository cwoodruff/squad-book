# Review: 2.0 edition build changes (WP-S1)

Reviewer: Marvin. Date: 2026-11-21. Author: Slartibartfast (notes in `research/LINKS-2.0-LEFTOVERS.md` and his decision "2.0 edition build groundwork"). Branch `squad-2.0`, uncommitted, compared with `git diff book-squad-v1.1.0`.

Files reviewed: `scripts/check-coverage.py`, `scripts/check-links.sh`, `scripts/render-cover.sh`, `book/metadata-vol1.yaml`, `book/metadata-vol2.yaml`, `book/images/src/cover.html`, `book/images/cover-vol1.png`, `book/images/cover-vol2.png`. `.github/workflows/build-epub.yml` was checked as well (the plan asks for a check only).

## Overall verdict: **REJECT**

`check-links.sh` does not do what it reports. It probes 1 of the 309 links and still prints "checked 309 links". Even with that fixed, it can never exit 0 on a correct tree, so it cannot work as the old-host regression guard that the decision describes. Every other file passes.

| File | Verdict |
|---|---|
| `scripts/check-links.sh` | **REJECT** (R1, R2) |
| `scripts/check-coverage.py` | **APPROVE** |
| `scripts/render-cover.sh` | **APPROVE** |
| `book/metadata-vol1.yaml` | **APPROVE** |
| `book/metadata-vol2.yaml` | **APPROVE** |
| `book/images/src/cover.html` | **APPROVE** (unchanged; it has no version text, only the `{{SUBTITLE}}` and `{{VOLUME}}` slots) |
| `book/images/cover-vol1.png`, `cover-vol2.png` | **APPROVE** |
| `.github/workflows/build-epub.yml` | No change needed |

## Required changes

### R1. `scripts/check-links.sh:19` (with `:9`): xargs stops at the first quote, so almost no links are probed

- **What:** Line 9 extracts URLs with `[^ )>"\`]+`, which does not stop at `'`. Vol 2 Ch 8 l.198 (`fetch('http://127.0.0.1:3000/health')`) therefore yields `http://127.0.0.1:3000/health'`, which is line 2 of the sorted list. Line 19 feeds the list to `xargs -I{}`, and xargs parses quotes in its input. It stops with `xargs: unterminated quote` after the first line. The `broken=$(…)` capture discards the xargs exit status, and line 21 prints the line count of the input file. Actual run: `xargs: unterminated quote`, `BROKEN 000 http://127.0.0.1:3000/health`, `checked 309 links`. Only 1 URL was probed. I reproduced the xargs behavior on a three-line input with one `'`: it ran only the first line and exited 1.
- **Why:** The link check is the only check that catches dead or stale links. `make coverage` matches bare paths and cannot catch them (see my 2026-11-20 assessment). As written, the probe part of the script is a no-op that reports success.
- **Clearing condition:** (a) Feed URLs without quote parsing, for example `tr '\n' '\0' < "$tmp" | xargs -0 -n1 -P "${LINK_JOBS:-8}" bash -c 'probe "$1"' _`. (b) Add `'` to the exclusion class on line 9 (and stop at `$`/`{` so that `${encodeURIComponent(taskId` from Vol 2 Ch 15 l.181 is not extracted as a URL). (c) Make a non-zero xargs exit fail the script. (d) Print the number of URLs actually probed. Verification: the output reports 309 probes (or the count after R2's exclusions), and a deliberately broken test URL is reported.

### R2. `scripts/check-links.sh:9,16`: the check fails on every correct tree, so the old-host guard cannot gate anything

- **What:** These 7 extracted "links" are local endpoints or documentation placeholders, and they always fail: `http://127.0.0.1:3000/health`, `http://localhost:3000/health`, `http://localhost:3000/tasks/${…`, `http://localhost:4317`, `http://localhost:18888`, `https://dev.azure.com/YOUR_ORG` (404), `https://github.com/acme/shared-team.git` (404). The 1.1 script also probed loopback URLs. The new scan of `exercises/` adds one more placeholder site (`exercises/solutions/vol1/ch08.md:9`).
- **Why:** The decision says "check-links.sh now fails on any old-host URL as a regression guard". A guard that exits 1 on every tree cannot tell an old-host regression from noise. Nobody can wire it into CI or `make check`.
- **Clearing condition:** Skip loopback hosts (`localhost`, `127.0.0.1`) and an explicit, commented placeholder list (`YOUR_ORG`, `acme/`, template-literal fragments), or read the list from a small ignore file. Verification: `make links` exits 0 on the current tree when the network is available, and still exits 1 with an `OLD-HOST` line when a `https://bradygaster.github.io/squad/` URL is added to a scratch copy.

## Check results

| Check | Result |
|---|---|
| New UUIDs, both volumes | **Pass.** Vol 1 `urn:uuid:70e2a141-a56d-4692-80f6-b359f61276ef` (was `…5e13`). Vol 2 `urn:uuid:5bfe7e51-cce7-4c98-979c-06fc5685970d` (was `…5e12`). Both differ from each other and from the 1.1 edition. Both appear as `dc:identifier` in the built OPF. |
| "Second Edition" and "Targets Squad v2.0.0" in descriptions | **Pass**, both volumes, and both appear in the built OPF `dc:description`. The custom `edition:` key is not emitted by pandoc, as Slartibartfast noted. The description and cover carry the marking (D1 met). |
| Vol 2 no longer says preview | **Pass.** `grep -i preview book/metadata-vol*.yaml` finds nothing. The description now reads "Squad 2.0 multi-host support across seven AI hosts". `subject` adds "Claude Code" (the plan allows this). |
| Cover text | **Pass.** I viewed both PNGs (1600×2400). Each reads "Second Edition · Covers Squad 2.0" above the author name. The subtitles are unchanged. |
| `check-coverage.py` points at github/squad v2.0.0 | **Pass.** `REPO = "https://github.com/github/squad"`, the primary set ref is `v2.0.0`, both `blob/` and `tree/` pins are accepted, and the optional sets are skipped when their files are absent. No `bradygaster` string remains. |
| `check-links.sh` temp file and old-host rule | **Pass** for these two points: it uses `mktemp "${TMPDIR:-/tmp}/…"` with an EXIT trap, and the old-host regex matches `bradygaster.github.io/squad`, `github.com/bradygaster/squad` and `raw.githubusercontent.com/bradygaster/squad` but not `github.com/bradygaster/squad-sdk`, which I tested. It fails overall because of R1 and R2. |
| `render-cover.sh` | **Pass.** `mktemp` under `$TMPDIR` with a `.html` suffix, and the new strings. I did not re-render: it needs headless Chrome, and the PNGs already match. |
| `make coverage` | **Pass.** 213/213 sources cited, 48/48 source modules, exit 0. |
| `make manuscript` | **Pass.** 46 chapters, 0 structural errors. As a side effect it regenerated both Appendix E files, which `make` always does. Both were already modified in the working tree. |
| `make epub` | **Pass** (built outside the sandbox). Inside the sandbox, mermaid-cli's Chrome cannot launch ("The browser is already running for …puppeteer_dev_chrome_profile-…"), so the one diagram not yet cached (`8c8c0e62…`, the platform-adapter flowchart) failed to render. Rerun outside the sandbox: Vol 1 built from 33 files, Vol 2 from 42. |
| epubcheck (`/opt/homebrew/bin/epubcheck`) | **Pass**: 0 fatals, 0 errors, 0 warnings for both EPUBs, run outside the sandbox. Inside the sandbox, Java image decoding fails and reports every PNG as `PKG-021 Corrupted image file` (47 in Vol 1, 59 in Vol 2). That is sandbox noise, not a book defect. |
| `make links` | **Fail** (R1). The script output is quoted under R1. |
| Equivalent link probe (NUL-safe, all 309 URLs, same curl flags) | 298 × 200, 2 × 203, 1 × 503 (`https://github.github.com/squad/docs/features/team-setup/`, Vol 1 Ch 4 l.301, which returned 200 on 3 retries, so it was transient), and 2 × 404 plus 5 × 000, all of them the R2 placeholders and loopback URLs. **No real link is broken. No old-host URL remains** in `book/`, `exercises/`, `sample/` or the root `README.md`. |
| `.github/workflows/build-epub.yml` | Runs coverage, manuscript and `make validate`. It does not call `make links`, so R1 does not break CI, but R2 is why links cannot be added to CI. No change needed. |

## Sandbox notes

Chrome (mermaid-cli) and epubcheck's image decoding need to run outside the sandbox. Use `/sandbox` to manage this. Node's built-in `https` does not use the sandbox proxy unless `NODE_USE_ENV_PROXY=1` is set (relevant to the e2e checks, not to this review). Nothing was installed.

## Revision (Arthur)

Date: 2026-11-21. Escalated to the Lead because the author (Slartibartfast) is locked out. Only `scripts/check-links.sh` changed.

| Item | Change (file:line) |
|---|---|
| R2 skip list | `scripts/check-links.sh:11-19`: a commented `SKIP_PATTERNS` array at the top: loopback (`localhost`, `127.0.0.1`, `0.0.0.0`, `[::1]`), RFC 2606 example hosts and reserved TLDs, `YOUR_[A-Z_]+`, `github.com/acme/`. Skipped URLs are printed as `SKIP <url>` (l.37-42). The old-host test runs on the full list before skipping (l.32-34), so a skip entry can never hide an old-host URL. |
| R1(b) extraction | `:27-28`: a URL now stops at whitespace, `"`, `'`, `` ` ``, `<`, `>`, `(`, `)`, `[`, `]`, `{`, `}`, `\|`, `$` and `\`. Trailing `.,;:!?*_]` runs are stripped. Diff against the old extraction: only `http://127.0.0.1:3000/health'` (now merged with its unquoted twin) and `http://localhost:3000/tasks/${encodeURIComponent(taskId` (now `http://localhost:3000/tasks/`, skipped). |
| R1(a) quoting | `:51-53`: NUL-delimited input (`tr '\n' '\0' \| xargs -0 -n1 -P`), so xargs does no quote parsing. Parallel probes are kept (`LINK_JOBS`, default 8). |
| R1(c) errors | `:44-49, 54-55`: each probe prints exactly one `OK`/`BROKEN` line and exits 0, so a non-zero xargs status means a probe failed to run, and it fails the script. An empty curl code counts as broken. |
| R1(d) count | `:57-64`: the count comes from the result lines, not the input file. The script fails if probed ≠ expected, and prints `found N unique URLs: checked C, skipped S, broken B`. |
| Kept | `mktemp -d` under `$TMPDIR` with an EXIT trap (`:22-23`), the old-host regex unchanged (`:20`), bash/BSD-compatible tools. New: `LINK_DRY_RUN=1` does extraction and counting without the network. |

Run results (network available in the sandbox):

- `make links`: exit 0, `found 308 unique URLs: checked 301, skipped 7, broken 0`, in about 13 s. The 7 skips are exactly the R2 list. 308 = 309 − the quoted duplicate. 301 = 308 − 7.
- `LINK_DRY_RUN=1`: the same counts, exit 0.
- Negative test on a scratch copy of `book/` and `exercises/` under `$TMPDIR`, with `https://bradygaster.github.io/squad/docs/` and `fetch('https://github.com/github/squad/no-such-page-xyz')` added: the output was `OLD-HOST https://bradygaster.github.io/squad/docs/`, then `BROKEN 404` for both, then `checked 303, skipped 7, broken 2`, and the script exited 1. The quoted URL was extracted without its `'`. A dry run with only the old-host line also exits 1.

Requesting re-review from Marvin.

## Re-review (Marvin)

Date: 2026-11-21. Scope: Arthur's revision of `scripts/check-links.sh` (the only file changed). The other build files kept their earlier APPROVE.

### Overall verdict for the build changes: **APPROVE**

Every R1 and R2 clearing condition is met. `check-links.sh` is now **APPROVE**, so all WP-S1 build files pass.

| Condition | Result |
|---|---|
| R1(a) no quote parsing | **Met.** `tr '\n' '\0' \| xargs -0 -n1 -P "${LINK_JOBS:-8}" bash -c 'probe "$1"' _` (l.52-53). |
| R1(b) extraction stops at `'`, `$`, `{` | **Met.** Vol 2 Ch 8 l.198 yields `http://127.0.0.1:3000/health` with no trailing `'`; the extracted list contains no URL ending in `'`. Ch 15 l.181 yields `http://localhost:3000/tasks/` (skipped). I compared the strict extraction with a whitespace-only extraction over every text file: no real URL is cut short. The only other differences are bare `http://`/`https://` in prose, which are not URLs. |
| R1(c) xargs failure fails the run | **Met.** With `LINK_JOBS=abc`, the output was `ERROR xargs exited 1` and `ERROR probed 0 of 301 URLs`, exit 1. |
| R1(d) real probe count | **Met.** `checked` is counted from the `OK`/`BROKEN` result lines and compared with the number of probe inputs (l.57-61). |
| R1 count accuracy | **Met.** An independent Python walk of `book/` and `exercises/` finds 308 unique URLs, and the set is identical to the script's list (`diff` is empty). 308 = my earlier 309 minus the `…/health'` duplicate. 301 probed + 7 skipped = 308. |
| R2 skips exactly the 7 local/placeholder URLs | **Met.** The `SKIP` lines are exactly `127.0.0.1:3000/health`, `localhost:18888`, `localhost:3000/health`, `localhost:3000/tasks/`, `localhost:4317`, `dev.azure.com/YOUR_ORG`, `github.com/acme/shared-team.git`. The skip list is a commented array at l.11-19 and its use is described in the header. |
| R2 a skip cannot hide an old-host URL | **Met.** The old-host test runs on the full list before skipping (l.31-34). Tested with `https://github.com/bradygaster/squad/YOUR_ORG`: it is printed as both `SKIP` and `OLD-HOST`, and the run fails. |
| Old-host guard, `mktemp` under `$TMPDIR`, parallel probes | **Kept.** Regex unchanged (l.20), `mktemp -d "${TMPDIR:-/tmp}/…"` with an EXIT trap (l.22-23), `-P "${LINK_JOBS:-8}"`. |

### Runs

- `make links` (network available in the sandbox): exit 0, `found 308 unique URLs: checked 301, skipped 7, broken 0`, about 14 s. This matches Arthur's result.
- `LINK_DRY_RUN=1`: the same counts, exit 0.
- My negative test, on a scratch copy of `scripts/check-links.sh`, `book/` and `exercises/` under `$TMPDIR` (removed afterwards). I added `https://bradygaster.github.io/squad/docs/` and `fetch('https://github.com/github/squad/no-such-page-marvin-xyz')` to Vol 2 Ch 8, and `https://github.com/bradygaster/squad/YOUR_ORG` and `http://localhost:9/x` to `exercises/solutions/vol1/ch08.md`. The output was two `OLD-HOST` lines, nine `SKIP` lines, `BROKEN 404` for the bradygaster.github.io URL and for the `fetch('…')` URL (extracted without its `'`), then `found 312 unique URLs: checked 303, skipped 9, broken 2`, exit 1. A dry run of the same copy (no network, so no 404s) still exits 1 on the old-host lines alone.

### Notes (non-blocking, no change required)

- The script probes each URL once (`curl -m 15`) with no retry. A transient 5xx, like the 503 in the first review, fails the run. That is acceptable for a manual `make links`. Add a retry before wiring it into CI.
- The scan covers `book/` and `exercises/`, as the decision says. `research/VALIDATION.md:29` describes it as also covering `sample/` and the root README. That wording is for the VALIDATION.md owner to correct; it is not a script defect. My first review found no old-host URL in `sample/` or `README.md`.
