# Change log: Volume 1, Parts III–IV (Ch 15–21) for Squad v2.0.0

Owner: Ford. Branch `squad-2.0`. Not committed. Verified against `SRC/squad-v2.0.0` (tag `v2.0.0`) and the 2.0.0 CLI help in a scratch repo.

## Part intros (`part-03/00-part.md`, `part-04/00-part.md`)

No change. Neither has a version statement.

## Ch 15 Memory and Knowledge

- Version statements v1.1.0 → v2.0.0 (objectives, SEM caveat, SDK, provider, config table header, pitfalls, summary, exercise 4, quiz 4).
- "Summaries and archive files" rewritten: 15 KB, nothing shrinks on its own, Core Context plus last 5 `##` sections (3 with `--deep`), word-for-word move, `###`-under-one-`##` caveat, archive not loaded at spawn, summarizing is an agent job, Scribe only merges decisions. Added a "Changed in Squad 2.0" note (1.x docs said ~12 KB automatic summarization) and the 2.0 persistence table (`D/concepts/memory-and-knowledge.md`).
- `decisions.md` paragraph: 20 KB threshold, only when you run nap.
- Governed memory: CLI and `memory.*` MCP tools share one store, backend-aware, fails outside a squad (verified with the CLI); case-insensitive class names; cross-process index lock (`.squad/backend/locks/memory-index.lock` for filesystem storage) replaces the "no cross-process locking" claim; host adapter search skip + `provider-error` audit; registered provider result filtering; CLI and MCP server supply no Copilot client.
- Config Reference, Under the Hood and the "two writers race" pitfall updated to match.
- "Personal history" reworded to "An agent's own history" (personal-squad ambiguity). The plan's "2 personal-squad hits": no actual personal-squad mention existed; the other "personal" (SEM scope) is unrelated and kept.
- Solutions: version labels only (answers still hold).

## Ch 16 Tiered Memory, Reflect, and Context Hygiene

- Version statements → v2.0.0 (objective, status H3, tier limits, nap intro, recovery, config, pitfalls, summary, quiz 3 and 7).
- Nap: states it never summarizes and never runs on its own; table rows add the pre-`##` text, `###` caveat and the decisions skip when the archive is git-ignored and untracked; new paragraph that 2.0 history compression applies the same committable-archive and verified-append checks (`nap.ts` diff); "Changed in Squad 2.0" note on "summarizes" and `/compact`.
- `/compact` paragraph rewritten: Squad shell has `/nap`; Copilot CLI's `/compact` only shortens chat; run `squad nap` from a terminal with `copilot --agent squad`.
- New paragraph: summarizing is a separate agent job, Scribe only merges decisions, "team, take a nap" is a plain chat request.
- Two pitfalls added (chat nap request; one `## Learnings` block).
- Plan item "remove the preview mentions (4)": the remaining "preview" hits mean `--dry-run` previews, not Squad previews, so they stay.
- Solutions: version labels; exercise 3 answer adds the `###` caveat and the 2.0 archive check.

## Ch 17 Skills

- Version statements → v2.0.0 (marketplace, scanner, paths, skill help, summary, exercise 4). Marketplace, scanner script, skill CLI and skill source are unchanged between tags.
- Frontmatter parser: block sequences and quoted scalars now parse (#2236); limits restated. Config row and pitfall updated.
- Claude Code pointer (one paragraph, allowed site): template skills project into `.claude/skills/`, team skill overrides, cross-ref Ch 20 (Vol 2).
- Solutions: version labels only.

## Ch 18 Directives, Ceremonies, and the Reviewer Protocol

- Version statements → v2.0.0.
- New H3 "Recording lockouts with `squad lockout`": commands (sourced from `commands/lockout.ts`, exercised in a scratch repo), states, refusals, roster = `.squad/agents/*` with charters minus non-authors, `deadlocked`, `governance.authorities` override. States that the Copilot coordinator is unchanged and does not write the file.
- New H3 "Reviewer and sign-off gates on other hosts": non-Copilot reviewer gate, reviewer-authored code needs another reviewer, human sign-off gate and `templates/human-members.md`; one paragraph on advisory Claude hooks (`claudeHooks: "advisory"`, `squad hook claude`), cross-ref Vol 2 Ch 15/20. Copilot path framed as guidance plus branch protection (no overclaim).
- Config Reference rows for the ledger, commands, `governance.authorities`, `human-members.md`, `claudeHooks`. Under the Hood paragraph on `lockout.ts`. Two pitfalls. Hands-On step 5 adds an optional `squad lockout` record.
- **Correction beyond the plan:** the chapter said the `retro-enforcement` skill was absent from the source. It exists in `templates/skills/` (in v1.1.0 too) but `squad init` does not install it (not in `MANIFEST_SKILL_NAMES`) and `Test-RetroOverdue` is PowerShell in Markdown. Fixed in prose, Under the Hood, exercise 5 and solution 5.
- Solutions: exercise 3 and 5 answers updated.

## Ch 19 Error Recovery and Iterative Retrieval

- Version statements → v2.0.0. Error-recovery, iterative-retrieval, reviewer-protocol skills, circuit-breaker template and `rate-limiting.ts` are unchanged; all Further Reading sources resolve at v2.0.0.
- Triage paragraph and one Config Reference row: `--max-rounds`, `--max-duration`, `--claims` (cross-ref Ch 9). Repinned `watch/index.ts` and `squad.agent.md` claims rechecked.
- Solutions: version label only.

## Ch 20 Scenario Playbook A

- Version statements → v2.0.0.
- Solo checklist: one bullet on choosing a host (`squad init --client`, cross-ref Vol 2 Ch 19).
- Solutions: no change needed.

## Ch 21 Scenario Playbook B

- Version statements → v2.0.0 (`agentFileRoot`, SubSquads resolver, `streams.json` note, config table, Under the Hood, pitfall, quiz 4). Resolver, streams module and scaling doc unchanged; `agentFileRoot` still in `config/init.ts`.
- SubSquads intro: cross-ref to `watch --claims git-ref` in Ch 9 for multi-machine watchers.
- Human teams: `human-members.md` sign-off sentence; one mixed-host paragraph (one `.squad/`, decisions through inbox → Scribe → `decisions.md`, `squad client sync`, cross-ref Vol 2 Ch 19).
- Next steps: removed "Squad 2.0 preview"; Part IV named by its new title; reading path for multi-host teams and 1.x readers.
- Solutions: no change needed.

## Skipped or deferred

- Ch 9 section title not yet written by the other Ford instance, so cross-refs say "Chapter 9" without naming the heading.
- `lockout.ts` / `hook.ts` module coverage is mapped to Vol 2 Ch 20 and App A, not to Ch 18, so the "unreferenced module" warnings are not mine to clear.
- `make manuscript` passes (46 chapters, 0 structural errors). It regenerates Appendix E as a side effect.
