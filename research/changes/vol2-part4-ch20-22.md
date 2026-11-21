# Change log: Vol 2 Part IV, Chapters 20–22 (Squad 2.0.0)

Author: Trillian. Date: 2026-11-21. Branch `squad-2.0`, uncommitted. Base: the 1.1 text plus Slartibartfast's approved link rewrite (kept).

Files: `book/vol2/part-04/ch20-host-projections.md`, `ch21-state-boundary-backend.md`, `ch22-upgrading-to-2.md`, `exercises/solutions/vol2/ch20.md`, `ch21.md`, `ch22.md`. `make manuscript` passes (it also regenerated `book/vol2/appendices/app-E-quiz-answers.md`). `check-coverage.py` reports no vol2:20, vol2:21 or vol2:22 failures and 48/48 modules; `make coverage` still exits 1 only for Appendix I (ADR-002/ADR-003, WP-T3). All Mermaid blocks in the three chapters render with `mmdc`.

## Chapter 20: Host Projections, Client Adapters, and Capability Negotiation (~12,000 words)

Changed:
- Removed the Preview opener. Two new objectives (ADR-003; Claude projection v3).
- Execution harness Warning became a `Preview` callout: two experimental harnesses ship; projections are not harnesses.
- "preview" wording removed from the token list, reporting-subtlety, registration-API and Hands-On paragraphs.
- Rendering section: the digest is now described as a condensed rewrite from the shared template; removed the claim that `resolveCanonicalCoordinatorSource` adds a pointer to Copilot's file.
- New H3 **Host-neutral coordinators (ADR-003)**: options A/B/C, option C chosen 2026-11-13, digests never read `.github/agents/squad.agent.md`, `COORDINATOR_SQUAD_VERSION` stamp, Copilot output unchanged (snapshot test), Copilot file still written without Copilot, 43-session evidence and the 2026-11-12/13 no-Copilot scenarios, Azure DevOps deferred. Cites ADR-003 (Further Reading added).
- Envelope table and text: Claude coordinator has no `tools` allowlist in v2.0.0 (was `Task, … mcp__squad_state`); companion files now include member subagents, skills and settings keys; plugin-mode `CLAUDE.md` wording.
- Charter inlining: Claude spawns named member subagents with the `Agent` tool (`subagent_type`), formerly `Task`; general-purpose fallback.
- New H2 **The Claude Projection, Version 3**: version table (v1/v2/v3, stamp text), member-subagent frontmatter mapping and `X-squad-host-claude` (Tools, Isolation), `ownedMarker`/`skipped`/`obsolete`, native skills and the five `squad-coordinator-*` skills (Copilot already loads Init Mode on demand, FC #55), `.claude/settings.json` (scoped allowlist and `.claude/.squad-permissions.json`, advisory hooks table, `hook.ts` behavior), lockout records framed as in Vol 1 Ch 18 (Claude coordinator records transitions; Copilot does not; evidence, not a write barrier; cites `packages/squad-cli/src/cli/commands/lockout.ts` and `hook.ts`), plugin mode (keys, prefix, ownership file) with a new flowchart.
- Apply/uninstall: `obsolete` kind, `ownedMarker`, `json.remove`, results `removed`/`skipped`, no-op JSON keeps bytes, empty files never created; exact block separator so `CLAUDE.md`/`AGENTS.md`/`GEMINI.md` rollback is byte-exact; managed-without-marker vs marker-owned deletion; `squad client` has only `list|add|sync`.
- Feature matrix regenerated from v2.0.0: Claude primitive `Agent`; per-spawn model yes for Claude; model selection S for Claude only; Ralph CLI S for Claude (`--agent-preset claude`); dual-root remote S everywhere (was U); live-run row and later runs (plugin MCP 2026-11-10, ADR-003 scenarios, harness runs); five expected-failure gaps (four for Claude).
- Spec walkthrough: §7 (Claude v3, §7.4 plugin), §13 ownership list, §15 promotion still pending (Preview callout); the uppercase-marker lag is fixed in v2.0.0; spec README still says no harness ships (code wins); README does not list ADRs.
- Hands-On: SDK pinned to `@2.0.0`; expected plan output re-verified by running the script in a scratch repo (members, skills, settings/permission JSON lines; plugin-mode `obsolete` lines and `.squad-plugin-settings.json`).
- Config Reference: `claudePlugin`, `claudePermissions`, `claudeHooks`, `X-squad-host-claude`, `lockouts.json`, `CLAUDE_PROJECTION_VERSION`, `CLAUDE_PROJECT_DIR`. Under the Hood: the `claude-*.ts`, `lockout.ts`, `repo-launcher.ts`, `safe-path.ts` modules, the on-demand split excerpt, CLI `lockout.ts`/`hook.ts`, `--claude-plugin` handling in `clients.ts`.
- Pitfalls: four new entries (ADR-003 customization, allowlist prompts, skipped member file, hooks not firing). Summary updated.
- Exercise 6 added (member subagent with host settings). Quiz 2 (cursor-reconnect) replaced by ADR-003; Quiz 8 (`/clients` alias) replaced by the lockout allowlist question. Solutions: Ex 3 and 5 updated, Ex 6 added, Quiz 2, 5, 8 rewritten.

Skipped: no Copilot-side change (none in v2.0.0). Kept the OpenCode singular/plural pitfall (still true). Did not cover the undocumented `models`, `notes` and `skill` commands found in `cli-entry.ts`.

## Chapter 21: The State MCP Boundary, Runtime Upstreams, and the Experimental Backend (~9,700 words)

Changed:
- Removed the Preview opener; objectives add the committed launcher and governed memory, and harnesses.
- Tool table: `squad_decide` reports orphan/two-layer branch keys; `squad_state_health` has the `squad-state-health/v1` metadata line. **Correctness fix:** `casting/policy.json` is no longer a mutable key (nothing under `casting/` is).
- "Why This Is Different from the 1.1.0 Chapters" retitled "How This Builds on Chapters 1, 2 and 4"; removed the implication that v1.1.0 had no root `.mcp.json` (FC #43).
- New H3 **Governed Memory Across Backends** (storage, case-insensitive classes, `targetClass`, outside-squad failure, index locking, transactional migration; dry run).
- Bridge section: two-step launch spec (`resolveSquadStateMcpSpec` then `resolveCommittedSquadStateMcpSpec`) with a table; new H3 on `.squad/squad.mjs` (lookup order, including `~/.squad/cli.json`, read from the generated file), the `node -e` root finder, `x-squad` metadata, Claude hooks via `$CLAUDE_PROJECT_DIR`, doctor `portable squad_state launch` (warn vs fail); health metadata table; symlinked-root fix; linked projects get no placeholder team; non-Copilot coordinators stop on non-local backend outage.
- Backend SPI: harness rows in the table; new H3 **The two experimental harnesses** (Preview callout; `TurnHarness`/`TurnApprovals`, hash-bound approvals, comparison table, credentials, `SQUAD_BACKEND_HARNESSES`, state dirs). `executionAvailable` rewritten as conditional (FC #65), verified live: `[]`/false by default, `["copilot-sdk"]`/true with `SQUAD_BACKEND_HARNESSES=copilot-sdk`; 26 tools with the gate. Diagram updated.
- "…Durable Road Ahead" renamed **"…and What Remains Experimental"**; Preview callout lists backend tools, harnesses, remote durable server (Phase 2), §14.4/§15.1 promotion; strengthened live trace pending.
- Hands-On: 2.0.0 install; step 1 checks the launcher and doctor; step 4 updated for harness registration with a quota warning.
- Config Reference adds `SQUAD_BACKEND_HARNESSES`, `.squad/squad.mjs`, `SQUAD_CLI`, `SQUAD_ALLOW_NPX`, health metadata. Under the Hood cites `packages/squad-sdk/src/backend/harnesses` with the credential-check excerpt. Pitfalls: four new entries. Summary updated.
- Exercise 4 extended, Exercise 5 added (portability). Quiz 6 updated, Quiz 8 added. Solutions match.

Skipped: upstream content (statuses, depth 3) was already complete. Did not repeat Ch 2 lock-file details.

## Chapter 22: Migrating from Squad 1.x to Squad 2.0 (~9,900 words)

Changed:
- H1 renamed (D2); filename unchanged. Removed the Preview opener; new objectives (scratch drill; experimental vs shipped).
- "Two Upgrades, Three Channels" rewritten: channel table after GA (latest = 2.0.0; insider; preview alias; brew/WinGet names), exact `@2.0.0` install, patched Node note (P13). New H3s for self-upgrading **from 1.1.0** and **in 2.0**. **Correctness fix found in source:** a 1.1.0 CLI ignores `--dry-run` with `--self` and performs the global install (v1.1.0 `cli-entry.ts` l.412–461); the chapter now says to use `npm view … dist-tags`. Warning about the docs' `@bradygaster/squad@latest` (npm 404) and the docs' claim that self-upgrade refreshes templates.
- Project upgrade: dry run writes/installs nothing; stamp-as-customization fix, `squad-ci` preservation, doctor non-zero exit. Sequence diagram redrawn for the 1.1.0 path.
- "Upgrading to Squad 2.0": table of what a 1.x project's first 2.0 upgrade changes (launcher, `.mcp.json` rewrite, ignores, `human-members.md`, stale `teamRoot`, roster untouched, casting on source branch); `client sync` and plugin mode pointer.
- Tested upgrade paths rewritten from the v2.0.0 matrix (five producers, seven shapes, runs 2026-11-19 on commit `8c2b93d5`, two commits before the tag; 35 pass / 4 with F3 / 7 n/a; F1–F4). Old `v1.2.0-preview.1` label paragraph removed.
- Upstream section no longer calls upstreams "a 2.0 feature".
- CLI Reference: rows for `lockout`, `hook`, `dashboard`, watch flags, `--claude-plugin`, `client sync`, health metadata, doctor exit; points to Appendix A. Inventory fixed: `scrub-emails` default is still `.ai-team/`.
- Config Reference: Claude keys, watch keys, `governance.authorities`, launcher variables, `SQUAD_BACKEND_HARNESSES`.
- Release Process rewritten for after GA (stable promotion, preview vs insider, proposals removed in the promotion sanitize). Advice to pin CI.
- Rollback: lists the 2.0 files a rollback must remove.
- Hands-On rewritten as a scratch drill: clone at `ch03-start`, 1.1.0 CLI in an isolated `npm --prefix`, `v2-ch22-start` tag, registry check instead of a 1.1.0 self dry run, 2.0 project upgrade and inspection, optional `--client claude`, validation, rollback with the 1.1.0 CLI read-only, cleanup. **Marvin must verify end to end** (not run here: no installs).
- Under the Hood: `detectSelfUpgradeTag()`/`selfUpgradeCommand()`, the 1.1.0 `selfUpgradeCli()`, launcher writing in `mcp-spec.ts`.
- Pitfalls: five new rows (1.1.0 self dry run, unpinned CI, `upgrade --force` for lingering `state-mcp`, portable launch, "no Squad CLI found").
- **The Road Ahead** rebuilt from the v2.0.0 CHANGELOG and specs (backend/harnesses, Phase 2, profile promotion, ADR-003 option B, the Copilot-file decision, expected-failure digest gaps, GitLab, claims off by default; `[Unreleased]` empty). The five proposal skills are noted as shipped template skills (present in v1.1.0 and v2.0.0). All seven `docs/proposals/*` links removed.
- Summary, Exercise 1 and 6–7, Quiz 1 and 7 updated; solutions updated (Ex 1, 5, 7; Quiz 1, 7).

Skipped: Platforms section kept as is (still accurate; ADO scope note not added). Casting, compatibility and personal-squad sections unchanged apart from the upgrade-table cross-facts.

## Facts other files must reflect

Vol 2 front matter (preface), Part IV intro:
- Ch 22 title is "Migrating from Squad 1.x to Squad 2.0"; its Hands-On is a scratch-copy drill pinned to 1.1.0 (main Tasktrack stays on 2.0).
- A 1.1.0 `squad upgrade --self` installs `@bradygaster/squad-cli@latest` = 2.0.0 and **has no dry run**.

Appendix G (SDK API):
- `/backend` exports `ClaudeAgentSdkHarness`, `CLAUDE_AGENT_SDK_HARNESS_ID`, `claudeApprovalHash`, `claudeApiCredentialsConfigured`, `claudeDenyRules`, `isClaudeAgentSdkAvailable`, `CopilotSdkHarness`, `COPILOT_SDK_HARNESS_ID`, `TurnHarness`, `TurnCancelled`, `TurnApprovals`, `canonicalApprovalHash`, `redactApprovalPayload`, `redactText`, `summarizeAction`, `HarnessState`, `MAX_REMEMBERED`.
- `/client` additionally exports `lockout.ts`, `claude-hooks.ts`, `claude-plugin.ts` symbols; `CLAUDE_PROJECTION_VERSION = 3`; `ProjectionFile` has `obsolete` and `managed.ownedMarker`; `ApplyAction` adds `skipped`.
- `SQUAD_BACKEND_HARNESSES` (default `claude-agent-sdk`, needs SDK + API credential; `copilot-sdk` opt-in; `none`).

Appendix H (feature matrix): 51 features; Claude 44 S / 0 D / 4 U / 3 n/a; Claude model selection S; Ralph CLI S for Claude; dual-root S for all; five expected-failure gaps (Claude four); Copilot's only validated-live cell is the `copilot-sdk` harness.

Appendix I (spec): ADR-003 accepted 2026-11-13 (option C; B is a spike, #2488); client-harness-adapters v0.2 and backend-decoupling v0.2 remain non-claimable drafts, promotion §15.1/§14.4 pending; spec README's adapter row still says no harness ships (stale).

Appendix J: matrix runs at the tag dated 2026-11-19 on `8c2b93d5` (do not present as a date convention; it is matrix evidence).

Shared Appendix A (CLI): `squad hook claude <SessionStart|SubagentStart|PreToolUse|PostToolUse|Stop>` (always exits 0; not in top-level help); `squad lockout` usage per `lockout.ts`; `squad client sync [--dry-run]`; `clients` alias; `--claude-plugin` / `--no-claude-plugin`; `squad doctor` check `portable squad_state launch`; `scrub-emails` default `.ai-team/`; 1.1.0 `--self --dry-run` installs. Commands `models`, `notes`, `skill` exist in `cli-entry.ts` but not in help (unverified, not used in the book).

Shared Appendix B (config): `claudePlugin`, `claudeHooks` (`"advisory"` else off), `claudePermissions` (`"off"` disables), `governance.authorities`; files `.squad/squad.mjs`, `.claude/.squad-permissions.json`, `.claude/.squad-plugin-settings.json`, `.squad/governance/lockouts.json`; env `SQUAD_CLI`, `SQUAD_ALLOW_NPX`, `SQUAD_BACKEND_HARNESSES`, `CLAUDE_PROJECT_DIR`; launcher order `SQUAD_CLI` → project `node_modules` → PATH → `~/.squad/cli.json` → `npx` only with `SQUAD_ALLOW_NPX=1`.

Shared Appendix C (glossary): host-neutral coordinator (ADR-003); member subagent; projection version; plugin mode; harness (experimental).

## Doc/code discrepancies found

- `D/features/self-upgrade.md` l.65/l.85: `@bradygaster/squad@latest`/`@insider` (npm 404) and an automatic template refresh that no version performs.
- v1.1.0 CLI: `--dry-run` is not passed to `selfUpgradeCli`.
- `docs/specification/README.md` l.88: "no `HarnessAdapter` implementation ships" (false at v2.0.0).
- `client-harness-adapters-v0.2.md` §13: Kiro MCP JSON "fully Squad-managed" vs additive merge in code; status line still understates seven projections.
- `D/scenarios/upgrading.md` matrix calls upstream inheritance a 2.0 feature that 1.x cannot declare, but v1.1.0 `cli-entry.ts` has `squad upstream`.
- `squad --help` says `scrub-emails` defaults to `.ai-team/` (code agrees); older book text said `.squad/`.
- CHANGELOG lists the launcher lookup without the `~/.squad/cli.json` step that the generated `.squad/squad.mjs` documents.
