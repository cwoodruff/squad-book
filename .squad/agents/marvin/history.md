# Marvin — History

## Core Context

- **Role:** Test Engineer
- **Joined:** 2026-11-20

## Learnings

<!-- Append new learnings below -->

- 2026-11-20 (2.0 GA validation assessment, research/VALIDATION-2.0-ASSESSMENT.md): check-coverage.py only checks citation presence, not that sources exist upstream or that links resolve; the repo move to github/squad left ~295 book URLs 404 (bradygaster.github.io + bradygaster/squad blob/tree) while make coverage still passes 217/217. Host swap to github.github.com/squad + github.com/github/squad resolves 297/299; never rewrite @bradygaster npm scope (unchanged at 2.0.0). Proposed single v2.0.0 inventory = 186 sources (192 unique − 10 removed + 4 new). Sandbox blocks local port binding, so Tasktrack node:test hangs here; check-links.sh writes fixed /tmp path.
- 2026-11-20 (WP-M, inventory retarget to v2.0.0): merged into one set, research/sources.txt (186) and coverage.csv (213 rows), and deleted the -2.0 pair. Dropped consult-mode, personal-squad, the 8 docs/proposals and multi-squad.ts. Added ADR-002 (vol2:17, I), ADR-003 (vol2:20, I), claude-code-plugin (vol2:19), multi-machine-watch (vol1:9), and 5 module rows (dashboard/lockout/hook commands, backend/harnesses, ralph/claims.ts). build_coverage.py is now a read-only `--src` upstream-existence check, because the old generator would overwrite the map. Path citations match on the bare repo path, so v1.1.0 pins pass coverage; only link checks catch stale refs. Avoid `git rm --cached` in no-commit tasks, because it stages the deletion.
- 2026-11-21 (build review + e2e, research/reviews/build-review.md, e2e-checks.md): never trust a script's own "checked N" count. check-links.sh used `xargs -I{}`, which aborts at the first `'` in a URL and probed 1 of 309, so it needs NUL-delimited input. Under the sandbox: mermaid Chrome and epubcheck image decoding fail (false PKG-021), so run them outside; Node https ignores the proxy unless NODE_USE_ENV_PROXY=1 (a 1.1.0 init then pins @insider, not @1.1.0); port binding gets EPERM, so Tasktrack tests hang. Uncast team on 2.0.0: `doctor` is clean (exit 0), and `health --json` fails team/registry-charters/routing (exit 1). Ch 19's Git removal route works as written. Use HOME=<scratch> for CLI e2e runs.
- 2026-11-21 (inventory follow-ups, inventories-review.md): check-coverage.py's module check passes when any one listed section cites the module, so stale extra sections build up without anyone noticing. Before pruning, check each remaining section for the full `packages/...` string, not a short suffix. Don't run `make manuscript` when appendices are off-limits, because it regenerates both Appendix E files. Cite reviewers' recorded results instead. VALIDATION.md should name only what was run: mark the blocked items as blocked, and flag any results that came before later chapter edits.
