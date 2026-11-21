# Review gate: Volume 2, Parts I–III, Squad 2.0 update

Reviewer: Arthur (Lead Editor). Author under review: Trillian (`book/vol2/part-01..03/*`, `exercises/solutions/vol2/ch01.md`–`ch17.md`). Slartibartfast's link rewrite is judged for link correctness only.
Base: tag `book-squad-v1.1.0`. Working tree on branch `squad-2.0`, uncommitted. Change log: `research/changes/vol2-part1-3.md`. Date: 2026-11-20.

## Overall verdict: REJECT

Five chapters have known gaps against the style guide or the v2.0.0 retarget rule: Ch 1, Ch 4, Ch 12, Ch 15 and Ch 16. Each fix is one line or one callout. Everything else is approved. The update is a close, surgical edit of the first edition. The H2 skeletons, file names, Tasktrack tags and exercise numbering are unchanged, and every high-risk claim I spot-checked against the v2.0.0 source holds (see "Source spot-checks").

## Standard applied

- Author requirements: minimal edits, Second Edition, docs at `github.github.com/squad/`, repo at `github.com/github/squad`, npm/brew/WinGet names keep `bradygaster`, present tense for 2.0.
- `.squad/decisions.md` and the inbox (Arthur ×2, Ford ×2, Slartibartfast, Trillian `--yolo`).
- `research/UPDATE-PLAN-2.0.md` (final) §2 Volume 2 rows, §3.3 and §4; `research/STYLE-GUIDE.md`; `research/WRITER-BRIEF.md`.
- v2.0.0 source at `SRC/squad-v2.0.0`, plus `git -C SRC/squad` for v1.1.0 comparisons.

## Per-chapter verdicts

| File | Verdict |
|---|---|
| `part-01/00-part.md` | APPROVE |
| **Ch 1 MCP** | **REJECT** (R1) |
| Ch 2 State Backends | APPROVE |
| Ch 3 Cross-Squad | APPROVE |
| **Ch 4 Portability** | **REJECT** (R2) |
| Ch 5 Clients, Hosts, Programmatic Sessions | APPROVE |
| `part-02/00-part.md` | APPROVE (unchanged) |
| Ch 6 Security | APPROVE |
| Ch 7 Containers and Cloud | APPROVE |
| Ch 8 CI/CD and Release | APPROVE |
| Ch 9 Observability | APPROVE |
| Ch 10 Troubleshooting and DR | APPROVE |
| `part-03/00-part.md` | APPROVE (unchanged) |
| Ch 11 Architecture | APPROVE |
| **Ch 12 Coordinator Internals** | **REJECT** (R3) |
| Ch 13 Identity and Provenance | APPROVE |
| Ch 14 SDK | APPROVE |
| **Ch 15 Plugins and Hooks** | **REJECT** (R4) |
| **Ch 16 Autonomous Agents** | **REJECT** (R5) |
| Ch 17 Specification | APPROVE |
| `exercises/solutions/vol2/ch01.md`–`ch17.md` | APPROVE (none of R1–R5 touches an exercise or quiz) |

## Required changes

### R1. Ch 1: cross-volume reference in the wrong form

- **Where:** `book/vol2/part-01/ch01-mcp.md:112` (governed-memory row of the `squad_state` tool table): "(Chapter 15, Volume 1)".
- **What is wrong:** From Volume 2 the house form is `Chapter 15 (Volume 1)`. The same chapter uses that form correctly at l.3.
- **Why:** STYLE-GUIDE, "Two-volume structure": "write … `Chapter 4 (Volume 1)` from Volume 2."
- **Clearing condition:** Rephrase so the reference reads `Chapter 15 (Volume 1)`, for example "…one set of records; see Chapter 15 (Volume 1)." No other change.

### R2. Ch 4: a second "Changed in Squad 2.0" callout, in the wrong callout type

- **Where:** `book/vol2/part-01/ch04-portability.md:160` (`> **Warning:** Changed in Squad 2.0: the 1.x upstream guide said …`). The l.14 Note already gives the same change.
- **What is wrong:** The chapter now carries the "later wins → earlier wins" change notice twice: as the opening Note (l.14) and again as a Warning that borrows the "Changed in Squad 2.0:" label. The label belongs to the Note convention. The Pitfall at l.280 repeats it a third time, which the template allows.
- **Why:** STYLE-GUIDE, Callouts: the 1.x change notice is `> **Note:** Changed in Squad 2.0: …`, "short and factual". A Warning with that label is a third, undefined form. A second copy in the same chapter is the duplication the minimal-edit direction avoids.
- **Clearing condition:** Keep the l.14 Note. At l.160, either (a) drop the "Changed in Squad 2.0:" label and keep a plain `> **Warning:**` that states only the action ("If you ordered `upstream.json` for the 1.x later-wins rule, reverse it."), or (b) delete the l.160 callout and add that one action sentence to the l.14 Note. Leave the precedence list and the Pitfall as they are.

### R3. Ch 12: Rai and Fact Checker still described as "mandatory"

- **Where:** `book/vol2/part-03/ch12-coordinator-internals.md:58` (section-map row "Built-in Support Agents": "Reserves Scribe, Ralph, Rai, and Fact Checker as mandatory support identities").
- **What is wrong:** The row paraphrases the v2.0.0 prompt (`.github/agents/squad.agent.md` l.76) correctly, but in 2.0 Rai and Fact Checker are optional. `squad upgrade` never edits `team.md`, and you add them with `squad roster add` (CHANGELOG 2.0.0-preview.2 l.215; preview.3 l.177). Without a qualifier the reader learns the wrong roster rule. Trillian disclosed this and deferred it; deferring does not clear a terminology gap.
- **Why:** STYLE-GUIDE Terminology: "Rai and Fact Checker are **optional built-ins** added with `squad roster add`." This is the same gap I required fixed in Vol 1 Ch 4 (R2 of `vol1-review.md`), so the standard has to be consistent.
- **Clearing condition:** Keep the paraphrase of the prompt, then add one clause or sentence. For example: "(the prompt's wording; in 2.0 Rai and Fact Checker are optional built-ins you add with `squad roster add`, see Chapter 4 (Volume 1))." No roster teaching beyond that.

### R4. Ch 15: a leftover "v1.1.0" target statement

- **Where:** `book/vol2/part-03/ch15-plugins-hooks.md:157`: "Use the actual v1.1.0 CLI and `@bradygaster/squad-sdk` exports for reproducible examples."
- **What is wrong:** The sentence before it was retargeted to v2.0.0, but this one still tells the reader to use the v1.1.0 CLI.
- **Why:** STYLE-GUIDE, Version statements: v1.1.0 appears only as history. Plan §4: target statements become v2.0.0.
- **Clearing condition:** Replace "v1.1.0" with "v2.0.0" in that sentence.

### R5. Ch 16: a Preview callout for something that is not experimental

- **Where:** `book/vol2/part-03/ch16-autonomous-agents.md:114` (`> **Preview:** The generic persisted circuit-breaker configuration and `@squad/resilience` example …`).
- **What is wrong:** `@squad/resilience` is not an experimental or labeled-unshipped 2.0 feature. It is a docs page (`D/guide/building-resilient-agents.md`) that presents a nonexistent API as shipped ("The circuit breaker works out of the box"). That is a documentation/code mismatch, and the chapter already treats it as one at l.102 and in the Pitfalls. The callout also keeps 1.x Preview framing ("forward-looking … verify in a later tagged source").
- **Why:** STYLE-GUIDE, Callouts: `Preview` is used "only for things that are experimental in v2.0.0 … and anything else v2.0.0 labels experimental or unshipped. Never for shipped 2.0 behavior." The plan asked for the callout to be re-checked, and the re-check shows it no longer qualifies. Ch 13's Preview is different: its sources are labeled proposals (open-issue and canary-matrix docs), so it stays.
- **Clearing condition:** Change the label to `> **Warning:**` and drop "forward-looking" and the "later tagged source" clause. Keep the facts: not shipped in v2.0.0, no package or code implements it, only the guide page mentions it. No other edits.

## Deviations in Trillian's change log, judged

| Item | Judgment |
|---|---|
| Ch 1: 2.0.0 no longer prepends `--yolo` with `--additional-mcp-config` (#2312, fixing #2139) | **Accepted. It is correct and required.** v2.0.0 `copilot-invocation.ts` returns only `['--additional-mcp-config', '@…']` and its header says loading MCP config "must not add or remove `--yolo`". v1.1.0 l.66 returned the pair. `squad loop` defaults `--copilot-flags` to `--yolo` (`loop.ts` l.143), and so does `watch --execute` (`watch/index.ts` l.664, `watch/config.ts` l.284). CHANGELOG preview.3 l.186 cites #2312. The text, diagram, excerpt, Config Reference, Summary, Quiz 4 and solutions are consistent. The chapter correctly says the `copilot-mcp-trust` docs page still shows the old pair and that the source is authoritative. |
| Ch 4 status table and provenance detail beyond "summary" | Accepted. Plan §2 Ch 4 lists the statuses, depth and doctor/status resolution. Confinement rules, read budgets and nested-declaration policy stay in Ch 21. |
| Ch 11 ADR-001 paragraph, Warning, Pitfall, Summary and Quiz 5 rewritten (plan said Light) | Accepted. The 1.1 text said ADR-001 was absent, which is false at v2.0.0, so this is a correctness fix. It is one summary sentence plus a cross-reference to Ch 18 (the primary home). |
| Ch 3 one sentence plus a Changed-in-2.0 note (plan said one sentence) | Accepted. Plan §4 allows a Changed note where a 1.x reader needs the warning. |
| Ch 6 Claude Code allowlist bullet | Accepted. Plan §2 Ch 6 asks for it, and every detail matches `claude-hooks.ts` (tool list, `cast`/`client sync`/`lockout reject`/`lockout status`, `.claude/.squad-permissions.json`, `claudePermissions: "off"`). |
| Ch 15 Hands-On manifest keeps `"squad": ">=1.1.0"` | Accepted. It is a sample compatibility range, not a target statement. |
| Ch 12 "mandatory support identities" left as is | **Not accepted:** R3. |
| Ch 16 Preview "re-checked and reworded" | **Not accepted:** R5. The callout type is wrong. |
| Pre-existing em dashes left in place | Accepted (minimal edit). No new em dashes were added. |
| Appendix E regenerated | Accepted. My `make manuscript` run left both Appendix E files byte-identical, so the solutions and the appendix are in sync. |

## Source spot-checks (all held)

- **Ch 4 upstream precedence.** Copilot `squad.agent.md` l.156–161 loads upstreams once per session through `squad_state_upstreams`, never fetches, and applies "local `.squad/` always wins; then upstreams in the order the tool returns them … first winner stays". `resolver.ts` has `DEFAULT_UPSTREAM_MAX_DEPTH = 3`, `DEFAULT_UPSTREAM_STALE_DAYS = 30`, seven statuses in `types.ts`, and the `upstream:<name>@<ref>` provenance (l.452). `buildEffectiveUpstreamContext` (l.780) seeds winners with the local names (l.789). `doctor.ts` l.1168 and the `status` path in `cli-entry.ts` l.1014 run the resolver. `upstream.ts` has the allow-list, the credential refusal and `core.symlinks=false`.
- **Ch 15 plugin context.** Only `agents/lifecycle.ts` l.283 builds `pluginContext` (`buildActivePluginContext`), and `charter-compiler.ts` l.235 appends `## Plugin Context`. The spawn-path table matches `D/features/plugins.md` l.170–177. `claudeHooks` is off unless it is `"advisory"` (`claude-hooks.ts` l.85–89), and handlers run as `hook claude <Event>`.
- **Ch 12 ADR-003.** Status "Accepted (option C), 2026-11-13". The 24 KB limit is Antigravity's (`test/clients.test.ts` l.276, `coordinator.ts` header). The digests are self-sufficient and never point at Copilot's file. The Copilot snapshot guard and parity tests are as stated. The Copilot prompt loads `coordinator-init-mode` (l.94), `coordinator-response-mode` (l.380) and `coordinator-source-of-truth` (l.700). The five `squad-coordinator-*` Claude skills exist. Skill precedence is `.squad/skills/` first and personal paths are not scanned (l.341–349).
- **Ch 17 ADR-002.** Status "Proposed". `squad.claim/v1`, `--force-with-lease` acquire/renew/takeover/release, renewal every `ttlMs / 3`, and defaults of 15 min / 5 min / 2 min match `claims.ts` l.106/109. `DEFAULT_CLAIM_REF_PREFIX = 'refs/squad/claims/'` plus the fallback is correct. `SQUAD_MACHINE_ID` is correct. The `./ralph/claims` subpath export exists. The binding amendment is at `github-work-lifecycle-binding-v0.1.md` l.42. `SQC011` and `positive/examples.md` exist.
- **Also checked:** Ch 1 launcher lookup order and `SQUAD_ALLOW_NPX` (`claude-plugin.ts` `squadRepoLauncher`). The `x-squad` source `repo-launcher` and "dist-tags never written" claims are correct (`mcp-spec.ts`). The `state-mcp` tool map (`state-mcp.ts` l.34–50) and the `--experimental-backend` gating are correct. Ch 2's pre-commit paths changed from casting/routing to memory/identity (v1.1.0 vs v2.0.0 `install-hooks.ts`). Ch 6: dashboard, Node 22.23.4 and `engines >=22.5.0`. Ch 8: gh-aw v0.91.5, `PARTIAL_PUBLISH`, `expected_sha`, `squad-release-verify.yml`. Ch 9: `health.ts` metadata fields. Ch 10: the `state-mcp` lingering fix and the symlink fix (CHANGELOG l.141). Ch 11: ADR-001 status and the harness lag. Ch 14: the root-barrel excerpt matches `index.ts` l.13, all listed `/client` symbols are exported, `BACKEND_CONTRACT_STAGE`, and the `SQUAD_BACKEND_HARNESSES` default. Ch 16: the `Squad.Agents.AI` bundled-runtime behavior (`SquadAgentBundledRuntimeTests.cs`).

## Links (Slartibartfast's rewrite, correctness only)

Scope: 37 files, 77 unique pinned `blob`/`tree` URLs and 57 unique docs URLs. Every pin resolves with `git cat-file -e <ref>:<path>`. Every docs slug exists under `D/` at v2.0.0. There are no `bradygaster.github.io`, `github.com/bradygaster/squad` or `github.github.io` URLs. All good.

## Build

- `make manuscript`: "Manuscript: 46 chapters; 0 structural errors". Appendix E regenerated byte-identical for both volumes. The only stderr is the sandbox's harmless `xcrun_db` cache warning.
- `scripts/check-coverage.py`: 209/213 sources cited. The four misses are App I (ADR-002, ADR-003), Vol 2 Ch 19 (`features/claude-code-plugin`) and Ch 20 (ADR-003). The four unreferenced modules are mapped to Part IV or App A. None of these is in Vol 2 Ch 1–17, so there is no coverage gap in this scope.

## Advisories (not required)

- Ch 1 Config Reference "Other hosts" row: Antigravity has no MCP file. It is configured with `agy mcp add` (`templates/mcp-config.md` l.12). Saying so in four words would complete the row.
- Marvin: Trillian's seven upstream doc/code discrepancies (change log, last section) are worth adding to `VALIDATION.md`. Item 5 (`squad export-config --output` in the upstream-inheritance quick start) is a real broken command in the upstream docs.

## Outside this gate (for the coordinator)

- Vol 1 has two cross-volume references in the `Chapter N, Volume 2` form, which I missed in the Vol 1 gate: `book/vol1/part-02/ch12-models-cost.md:33` and `book/vol1/part-04/ch20-scenarios-a.md:48`. House form from Vol 1 is `Chapter 20 (Volume 2)`. Ford can fold these into the Vol 1 re-review. Ch 12 is already in that re-review.
- `research/STYLE-GUIDE.md` (Arthur's file) is updated: the Vol 1 host-mention rule now lists the D3 pointer sites (Ch 1, 2, 6, 9, 17, 21) plus the five §2 one-line or short sites (Ch 5, 10, 12, 18, 20), and says Vol 1 exercises stay answerable on the Copilot path alone.

## Re-review scope

Only `ch01` l.112, `ch04` l.14/l.160, `ch12` l.58, `ch15` l.157 and `ch16` l.114, plus a `make manuscript` re-run. Strict lockout: Trillian authored these files, so a different writer makes the revision unless the coordinator escalates.

## Revision (Ford)

Successor writer for Trillian (lockout). Minimal edits; `make manuscript` re-run: "46 chapters; 0 structural errors".

- **R1** `book/vol2/part-01/ch01-mcp.md:112`: "(Chapter 15, Volume 1)" → "; see Chapter 15 (Volume 1)."
- **R2** `book/vol2/part-01/ch04-portability.md:160`: option (a). Now `> **Warning:** If you ordered `upstream.json` for the 1.x later-wins rule, reverse it.` The l.14 Note, the precedence list and the Pitfall are unchanged.
- **R3** `book/vol2/part-03/ch12-coordinator-internals.md:58`: added "(the prompt's wording; in 2.0 Rai and Fact Checker are optional built-ins you add with `squad roster add`, see Chapter 4 (Volume 1))". Verified: `packages/squad-cli/src/cli/commands/roster.ts` l.305 accepts `add`; CHANGELOG l.215 `squad roster add <rai|fact-checker|all>`.
- **R4** `book/vol2/part-03/ch15-plugins-hooks.md:157`: "v1.1.0 CLI" → "v2.0.0 CLI".
- **R5** `book/vol2/part-03/ch16-autonomous-agents.md:114`: `Preview` → `Warning`; dropped "/forward-looking" and the "later tagged source" sentence. Facts kept.
- **Vol 1 (outside gate)** `book/vol1/part-02/ch12-models-cost.md:33`: "(see … and Chapter 20, Volume 2)." → ". See … and Chapter 20 (Volume 2)."
- **Vol 1 (outside gate)** `book/vol1/part-04/ch20-scenarios-a.md:48`: "(Chapter 19, Volume 2)." → "; see Chapter 19 (Volume 2)."
- Grep of `book/**` (excluding `book/vol2/part-04/`) for `Chapter N, Volume M`: only the three above (ch01 l.112, Vol 1 ch12 l.33, Vol 1 ch20 l.48); none remain.

## Re-review (Arthur)

Date: 2026-11-20. Scope: Ford's revision of R1–R5 and the two Vol 1 cross-reference fixes. Lockout respected (Ford, not Trillian, revised).

### Overall verdict: APPROVE

| Item | Clearing condition | Result |
|---|---|---|
| R1 `ch01-mcp.md:112` | Reads `Chapter 15 (Volume 1)`, no other change | Met: "…one set of records; see Chapter 15 (Volume 1)." |
| R2 `ch04-portability.md:160` | Option (a): plain Warning, action only; l.14 Note, list and Pitfall untouched | Met: `> **Warning:** If you ordered `upstream.json` for the 1.x later-wins rule, reverse it.` The l.14 Note and the precedence list are intact. |
| R3 `ch12-coordinator-internals.md:58` | Keep paraphrase, add optional-built-in clause with `squad roster add` and Ch 4 (Vol 1) | Met, exactly the suggested wording. |
| R4 `ch15-plugins-hooks.md:157` | "v1.1.0" → "v2.0.0" | Met. No other `v1.1.0` remains in Ch 15 outside pinned URLs. |
| R5 `ch16-autonomous-agents.md:114` | `Preview` → `Warning`, drop "forward-looking" and "later tagged source"; keep the facts | Met. Not shipped, no package or code, only the guide page: all kept. No `Preview` left in Ch 16. |
| Vol 1 `ch12-models-cost.md:33` | House form `Chapter 20 (Volume 2)` | Met. |
| Vol 1 `ch20-scenarios-a.md:48` | House form `Chapter 19 (Volume 2)` | Met. |

- `grep -rnE 'Chapter [0-9]+, Volume' book` (excluding `book/vol2/part-04/`): no matches.
- No new gaps: each edit is confined to the cited line, adds no em dashes, and introduces no new claims.
- `make manuscript`: "Manuscript: 46 chapters; 0 structural errors"; both Appendix E files regenerated.

### Advisory (not required)

- Vol 1 Ch 20 l.48 now carries two semicolons in one sentence ("…teaches; if you live … there; see Chapter 19 (Volume 2)."). It is grammatical and within the style guide. A full stop before "See" would read better at the next copyedit.
