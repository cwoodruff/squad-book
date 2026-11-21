# Change log: Volume 1 front matter and Parts I–II (Ch 1–14), Squad 2.0.0

Owner: Ford. Date: 2026-11-20. Branch `squad-2.0`. Not committed.

Verified against `SRC/squad-v2.0.0` (CHANGELOG, docs, `packages/`) and the 2.0.0 CLI in `$TMPDIR/squad-book-scratch-ford/` (fresh `squad init` on a Tasktrack copy, `--help` for init, upgrade, watch, roster, preset, cost, config, build, schedule; `squad consult` and `squad init --global` error text; `squad doctor` exit status).

## Front matter

- `00-title.md`: "Second Edition" line; "Written against Squad v2.0.0"; first edition remains available; Preview callouts = experimental in v2.0.0.
- `01-preface.md`: one-paragraph Copilot-first statement with pointer to Vol 2 Part IV; Part IV row renamed; "Which Squad" = install v2.0.0 (`latest`); "Coming from Squad 1.x" reading path (Ch 2, Ch 14, Vol 2 Ch 22); Under the Hood pinned to v2.0.0; Preview callout redefined, "Changed in Squad 2.0" Note convention added; Versions paragraph targets v2.0.0 (2026-11-18); new "What's New in the Second Edition" section.
- `part-01/00-part.md`: no change. `part-02/00-part.md`: Ch 14 bullet now "Keeping a Squad 2.x installation tidy and current".

## Part I

- Ch 1 (light): Preview callout folded into a prose paragraph (seven hosts, Copilot default, Vol 2 Part IV). No personal-squad mention existed to remove.
- Ch 2 (moderate): "Which Squad Should I Use? (1.1 vs 2.0)" replaced by "Squad 2.0 and earlier releases" (same H2 slot) with removed-features table; Preview callout → Changed-in-2.0 Note; patched-Node note for npm users (22.23.4+); channels redefined; `VERSION="v2.0.0"` example; doctor now exits non-zero and prints "No squad in this directory" before init; new "Other AI hosts" subsection with the two plugin install lines; Personal squads subsection deleted (dead inline 404 link removed, history pin dropped from Further Reading); `--global` config row removed; troubleshooting: no profile fallback, "An old 1.x CLI on PATH"; self-upgrade follows channel; SDK-first `--watch` note updated. Exercise 4, Quiz 3/5/7 and solutions updated.
- Ch 3 (moderate): re-observed init tree with the 2.0.0 CLI. Added `.squad/squad.mjs`, launcher-based `.mcp.json`, empty runtime dirs, `.gitignore` entries (and that `upgrade` appends `.squad/backend/`), `templates/human-members.md`; `.copilot/mcp-config.json` is a sample Copilot CLI does not read; `rai` is lowercase; `personal-squad` skill gone; coordinator 1,098 lines stamped 2.0.0; section table drops Personal Squad and Consult Mode, adds Upstream Inheritance; `--global` row removed, `--client` row added; Preview callout → Note. Solutions Q1/Q6 updated.
- Ch 4 (moderate): optional charter `## Examples` and `## X-` extensions; Rai and Fact Checker as optional built-ins with `squad roster add|remove` (verified diff output); `squad cast` adds the built-in table; human-members sign-off gate; config rows; v2.0.0 re-verification of roles (21), presets, UniverseId. Solutions Q2/Q3 updated.

## Part II

- Ch 5 (moderate): consult section, Config Reference rows, Under the Hood paragraph, Pitfalls bullets, objective, Exercise 4, Quiz 6 and Quiz 8 (also consult-only) removed or replaced; new "One team, any host" section (one routing table; non-Copilot coordinators run the reviewer gate unasked; Copilot prompt unchanged); consult-mode Further Reading pin removed. Solutions 4, 6, 8 rewritten.
- Ch 6 (light): one-sentence Claude Code `isolation: "worktree"` / `.claude/worktrees/` pointer.
- Ch 7 (light): board capability re-verified unchanged; v1.1.0 → v2.0.0; gh-aw walkthrough callout changed from Preview to Note (it describes a demo setup, not an experimental 2.0.0 feature).
- Ch 8 (moderate): GitLab Preview callout recast as plain fact ("planned, not shipped"; no adapter, no `glab` path); new ADO scope paragraph (detection + `triage`/`watch` via `az boards`; interactive Issues mode GitHub-only); ADO MCP server goes in `.mcp.json`; v1.1.0 claims re-verified. Solutions Q4 updated.
- Ch 9 (moderate): new H2 "Bounded and Coordinated Watch Runs" (`--max-rounds`, `--max-duration`, `--claims git-ref` with leases, fencing, config object, identity, round-report line; one-paragraph Claude preset pointer). Malformed `config.json` stops watch; `execute` applies `needs:*`; no double dispatch per round. Loop now defaults `--copilot-flags` to `--yolo` (found in `loop.ts` diff). Config Reference rows, Pitfalls, Summary, Exercise 6, Under the Hood (cites `packages/squad-sdk/src/ralph/claims.ts`), Further Reading (multi-machine-watch). New Mermaid diagram validated with `mmdc`. Solution 6 extended.
- Ch 10 (light): v2.0.0 re-verification (workstreams.json, uncalled filter, `task` mode); fleet stays Copilot-only sentence.
- Ch 11 (light): "deprecated (still present in v2.0.0)" retargeting only.
- Ch 12 (moderate): per-host model-selection paragraph citing the client-compatibility page; `squad cost` newest-session scoping (and `--help` wording note). Table output and legacy fallback left as is (FC #39).
- Ch 13 (light): v1.1.0 → v2.0.0 after re-verifying that `notifyLevel` is still not passed to `reportBoard()`.
- Ch 14 (moderate): Preview callout folded into prose plus a Changed-in-2.0 pointer to Vol 2 Ch 22; self-upgrade channel following, `--dry-run`, downgrade refusal and `--force`; content-aware upgrade, shipped manifest, verified `.local-backup` for skills too, `squad-ci.yml` preserved, never-touched list from `--help`, host refresh and `squad client sync`; casting repair and `teamRoot` normalization; dry-run semantics corrected throughout (Hands-On, Config Reference, Under the Hood, Pitfalls, Summary, Quiz 8). Solutions 2, Q4, Q6, Q8 updated.

## Deliberately skipped or deviated

- Ch 3: plan said `.gitignore` gains `.squad/backend/` on init; the observed 2.0.0 init does not write it (only `squad upgrade` appends it, `upgrade.ts` l.714). The chapter says that.
- Ch 9: plan calls `watch.claims` "reserved"; CHANGELOG preview.3 does say "reserved key", and the docs document its values. The chapter uses both facts (documented key; invalid value stops watch).
- Ch 11 solutions: Marvin's assessment asked for a deprecation note; FC #41 says it already exists. Not added.
- Ch 14: the old Note about `--skip-repo-upgrade` was dropped, since neither the 2.0.0 source nor docs mention the flag any more.
- `make manuscript` regenerated both Appendix E files (generated; not hand-edited).

## Checks

- `make manuscript`: 46 chapters, 0 structural errors.
- `make coverage`: vol1 ch9 now passes (multi-machine-watch slug and `packages/squad-sdk/src/ralph/claims.ts`). Remaining failures are Trillian's (ADR-002/003, claude-code-plugin) and the App A/Vol 2 module rows (dashboard, lockout, hook, harnesses).
