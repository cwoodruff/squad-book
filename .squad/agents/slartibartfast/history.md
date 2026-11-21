# Slartibartfast — History

## Core Context

- **Role:** Build Engineer
- **Joined:** 2026-11-20

## Learnings

<!-- Append new learnings below -->

- 2026-11-20 (2.0 WP-S1): URL retarget done by a path-aware script (scratchpad tools/rewrite_links.py). It uses `git cat-file -t v2.0.0:<path>` to decide repin vs keep old tag, and `git diff --quiet old v2.0.0 -- path` to flag repinned links whose content changed. The book has no line anchors, so repinning was safe. Headless Chrome (make cover) cannot run inside the sandbox: it cannot create its user-data dir. Render outside the sandbox. `mktemp -t` ignores the sandbox TMPDIR under make, so use `mktemp "${TMPDIR:-/tmp}/x.XXXXXX"`. Coverage needles for non-docs sources are bare paths, so the pin ref only matters for content/docs sources cited by blob URL.
- 2026-11-21 (WP-M inventories review, APPROVE): To find missing inventory, diff the upstream docs list against sources.txt (`git diff --name-status v1.1.0 v2.0.0 -- docs` gives the added and removed pages). Check pin leftovers with a grep for blob/tree refs other than v2.0.0. The checker passes a source-modules row when any one listed section cites the module, so stale extra sections only show up in a per-section scan. 8 were stale here, 3 of them caused by 2.0 prose removals.
- 2026-11-21 (R7, App B env table): an env-var inventory needs four passes, not one grep. Search case-insensitively for `env.NAME`/`env['NAME']` on any identifier ending in `env` (this caught mixed-case `ComSpec` and `CI`), check `ProcessEnv`-typed parameters with other names (`gitSyncEnv(base)` gave `GIT_CONFIG_PARAMETERS`), resolve computed keys through their string constants, and check for destructuring and aliases. Then make the doc's claim name exactly what was scanned (shell `$NAME` in templates was excluded).
