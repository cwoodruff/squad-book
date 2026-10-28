# Appendix E: Quiz Answers

This appendix collects the answers to the chapter quizzes in this volume (Chapters 1–21). Full worked solutions to the exercises are in the book repository under `exercises/solutions/`.

## Chapter 1: What Is Squad?

1. The coordinator.
2. False. Agents work in separate contexts; coordination is mediated by the coordinator and persistent project artifacts.
3. `.github/agents/squad.agent.md`.
4. Examples include `team.md`, `routing.md`, `decisions.md`, agent charters and histories, skills, and ceremonies.
5. The delegation and coordination overhead can exceed the work, and later steps may depend on earlier ones.
6. GitHub Copilot CLI or VS Code are conversational hosts; the `squad` command-line tool handles setup and operations.
7. No. Human review remains essential; agents can make incorrect or conflicting changes.

## Chapter 2: Install Squad and Choose Your Interface

1. The install script, Homebrew cask, WinGet package, and direct release bundle vendor Node.js. An npm install does not; it needs Node 22.5+.
2. It pins the release tag to install; the default is the latest stable release.
3. `insider` carries the 2.0 preview (with `preview` as an alias); `latest` is stable (v1.1.0).
4. False. `squad upgrade` refreshes project-managed files; `squad upgrade --self` updates the CLI package itself.
5. GitHub Copilot CLI and VS Code with GitHub Copilot.
6. VS Code uses the session model selected in the model picker; the per-spawn model selection documented for the CLI is not available there.
7. No. The implementation documents doctor as diagnostic and exits 0 even when checks fail, so a human should read the report.
8. `squad.config.ts` (or `squad/index.ts`). `squad build --check` validates that the generated files match what is on disk without writing anything, which makes it suitable for CI drift checks.

## Chapter 3: Your First Session, Annotated

1. **False.** In the observed v1.1.0 flow, `squad init` scaffolds local files; the coordinator proposes a roster when Copilot starts Squad.
2. `.github/agents/squad.agent.md` defines the coordinator instructions. `team.md` is roster/context state.
3. There are no specialist provenance records yet. This is expected in a fresh scaffold before the first roster cast.
4. No. `squad init` does not install Tasktrack API dependencies or rewrite its feature code.
5. `npm test` invokes Node’s test runner through the sample package script (`node --test api/test/`).
6. Examples include `--no-workflows`, `--no-vscode-default`, `--global`, `--sdk`, `--roles`, `--preset <name>`, and `--state-backend <type>`.

## Chapter 4: Meet the Team: Casting, Charters, and Roles

1. The charter defines an agent’s role, expertise, ownership, methods, voice, and boundaries. History is that agent’s accumulated cross-session context and learnings.
2. The v1.1.0 CLI reported 21.
3. **Scribe** merges durable decisions/logs; **Ralph** monitors work queues; **Rai** reviews Responsible AI concerns; **Fact Checker** verifies claims and challenges assumptions.
4. Squad pauses and tells the user a human needs to act. The user relays the request externally and later reports the response to Squad; stale reminders may prompt follow-up.
5. No. Presets capture reusable agent charters and roster composition, not the project’s decisions or skills.
6. `usual-suspects`, `oceans-eleven`, and `custom`.
7. `--force` permits overwriting existing same-name agent files during apply. Without it, existing agents are skipped rather than replaced.

## Chapter 5: Routing, Capability Routing, and Response Modes

1. Routing answers **who** owns the work; response mode answers **how much agent coordination/context** the request needs.
2. `workType`, `agents`, optional `examples`, and optional `confidence`.
3. Every `needs:*` value on the issue must be present in the manifest's `capabilities` array.
4. The issue passes through the opt-in capability filter; an absent manifest does not block it.
5. Direct is no-spawn. Lightweight still spawns one agent with reduced context.
6. Personal-agent consultation (personal expert advises, project agent executes) and the CLI `squad consult` workflow (isolated copy of a personal squad in an external project, with optional extraction).
7. No. The inspected `SquadCoordinator.handleMessage()` does not call `selectResponseTier()`.
8. `--clean` deletes the project `.squad/` directory. Since consult also adds the agent prompt to `.git/info/exclude` and creates `.github/agents/squad.agent.md`, verify those separate local artifacts rather than assuming a total uninstall.

## Chapter 6: The Parallel Work Model

1. Background mode describes when/how the coordinator runs independent agent sessions. A Git worktree is a separate checked-out directory and branch. One does not automatically create the other.
2. Use sequential execution when a task depends on a previous output, a reviewer gate must complete, or shared assumptions/files need to be established first.
3. The Copilot App `SessionSpawnBackend` defaults to five simultaneous active or starting sub-sessions. It rejects over-cap spawns; it does not configure a queue. Other backends can differ.
4. No. Worktrees have separate working directories, indexes, and checked-out branches, although they share repository storage.
5. The absolute `.squad/` directory path (the Squad root), not the repository root.
6. Union merge applies only to configured append-only files and combines lines; it neither prevents overlaps nor resolves semantic disagreements in arbitrary source files.
7. Confirm required changes are committed or otherwise preserved, the working directory is clean, and the integrated result has been tested. Remove without force.

## Chapter 7: GitHub Workflow and Issue-Driven Development

1. An open issue must carry the `squad` label to be included by the default Watch issue scan.
2. GitHub interprets and renders the issue-form YAML. Squad later reads the created issue through its platform adapter.
3. Acceptance criteria should name observable behavior and a way to verify it, such as a test case or expected API response. They should distinguish required outcomes from non-goals.
4. No. Namespaced labels are ordinary GitHub labels. Exclusivity requires a workflow or another enforcing process.
5. The v1.1.0 `--board` capability makes best-effort `gh project` calls for lifecycle status and certain closed/open mismatches. It does not create a complete board, implement arbitrary label/custom-field mappings, or provide general two-way drag-and-drop synchronization.
6. It assumes GitHub Agentic Workflows (`gh-aw`) and its dispatcher, implementation-worker, and advisory-reviewer workflows, plus the associated structured artifact conventions.
7. No. Issues do not isolate working directories. Use worktrees or serialize overlapping changes.

## Chapter 8: GitLab and Azure DevOps

1. The `GitHubAdapter` and `AzureDevOpsAdapter`.
2. `User Story`.
3. The Azure CLI (`az`), including its Azure DevOps extension and authenticated session.
4. They label GitLab Issues Mode experimental and warn that behavior may change.
5. No. `squad init --help` in v1.1.0 does not list `--introspect`.
6. `ado.areaPath`.
7. No. GitLab is not recognized as a distinct supported platform in the v1.1.0 detector/factory; an unrecognized remote can default to GitHub.
8. The `PlatformAdapter` abstraction normalizes work items and pull requests. No: the PRD records design intent; verify the v1.1.0 adapter implementation and its CLI/auth behavior before depending on a proposed operation.

## Chapter 9: Ralph, the Loop, and Scheduling

1. The instructions in `loop.md` (or the file selected by `--file`).
2. Ten minutes.
3. Less read-only; it enables agent execution and possible repository changes.
4. It prints an onboarding-mode banner; it does not prevent the loop from executing.
5. `interval`, `cron`, `event`, and `startup`.
6. `LocalPollingProvider`.
7. Only when `statePath` is configured.
8. Conversational Ralph runs within a Copilot session and uses its session context; `squad watch` is a separate local process that polls while running and must be stopped independently.

## Chapter 10: PRD Mode, Streams, and Fleet Dispatch

1. No. v1.1.0 offers PRD ingestion, analysis, and decomposition by conversation; it does not provide a dedicated PRD authoring command or first-class persistent PRD backlog.
2. `SQUAD_TEAM` has highest precedence, followed by `.squad-workstream`, single-entry automatic selection, then no active SubSquad.
3. No. It is advisory; it does not enforce filesystem access.
4. The v1.1.0 resolver reads `.squad/workstreams.json`; the feature page and some comments say `.squad/streams.json`.
5. Read-heavy analysis such as triage, review, audit, research, and investigation, with explicit no-file-write/no-branch behavior.
6. Enable the `fleet-dispatch` watch capability in addition to selecting `fleet` or `hybrid` as the dispatch mode.
7. The published result came from a particular six-issue read-only measurement and is dominated by avoiding multiple cold starts. Workload, model startup, and issue complexity vary; write-heavy work is not safely parallelized the same way.

## Chapter 11: Copilot Coding Agent and Remote Control

1. No. `@copilot` uses the repository-level `copilot-instructions.md`, and its work is tracked by issues and PRs rather than a standard Squad charter/history.
2. The coding-agent bot cannot be assigned like a normal human account. The supported route in this setup is the `squad:copilot` label and the PAT-backed workflow.
3. `COPILOT_ASSIGN_TOKEN`, documented as a classic PAT with repository scope, stored as an Actions secret.
4. No. Verify a Copilot session linked to the issue or Copilot activity on a linked draft PR.
5. `squad rc` is the browser/ACP chat bridge; `squad start` is the PTY mirror.
6. The CLI's deprecation warning recommends using GitHub Copilot CLI directly (`gh copilot`).
7. Redaction is pattern-based and incomplete by nature; remote interaction has access to a local process and repository, so secrets and tools may still be exposed. Keep tunnels private, stop them when finished, and use trusted devices.

## Chapter 12: Models, Cost, and Rate Limiting

1. User one-spawn override → persistent config (per-agent/global) → session model → charter preference → task-aware selection → profile default. Availability fallback occurs after the base choice.
2. No. Explicit user/config/session/charter choices are not rewritten by the economy profile.
3. It refreshes/diagnoses the model catalog from available sources. It does not choose or set the current model or edit model preferences as a selection command.
4. 120 seconds by default; prediction needs at least three samples.
5. It estimates consumption using the first-to-last remaining-quota change over elapsed time, not a least-squares linear regression.
6. Only green. Amber permits only priority 0, and red permits none.
7. No. `CostTracker` accumulates usage; `squad cost` reports estimates from the ledger (or legacy logs), not a provider invoice.
8. Check and consume are not one atomic reservation across processes. Two clients can both observe unused allocation and consume beyond it unless a separate synchronization mechanism exists.

## Chapter 13: Notifications and Team Communication

1. `all`.
2. No. Watch levels affect Ralph's board-report output, not Graph messages sent by an adapter.
3. `teams-graph`.
4. Both `teamId` and `channelId`.
5. Add `await` to the factory call and make the surrounding function asynchronous (or move adapter setup into an async initialization function).
6. No. It clears local in-memory and cached token state; it does not revoke the server-side token.
7. A self-chat ID is ambiguous. The adapter requires an explicit `chatId` rather than choosing an arbitrary one-to-one chat.

## Chapter 14: Cleanup, Upgrades, and Migration

1. No. Cleanup is opt-in as a watch capability.
2. No. The implementation deletes matching old entries rather than archiving them.
3. The date prefix in the filename, compared to `maxAgeDays`; the filename must begin with `YYYY-MM-DD`.
4. No. The v1.1.0 self-upgrade path installs the CLI and returns; run the project upgrade separately.
5. Manifest-listed Squad-owned templates are refreshed. Team state such as histories and decisions is preserved.
6. No. The CLI warns and overwrites; keep an independent backup.
7. It refuses if `.ai-team/` does not exist or if `.squad/` already exists.
8. The dispatcher performs migration and self-install actions before the project dry-run logic. Those options are mutating and are not simulated by `--dry-run`.

## Chapter 15: Memory and Knowledge

1. `.squad/decisions.md` is the canonical shared location for active team decisions.
2. Inbox entries are proposals awaiting review and consolidation; they may conflict, duplicate one another, or need validation before becoming active rules.
3. The named agent is the primary reader. Its history preserves domain-specific context for that agent.
4. No. SEM is an internal draft; `LocalMemoryStore` writes a YAML-frontmatter file with a different schema.
5. The entry is retrieved when relevant rather than automatically loaded into every prompt. It does not mean the entry is unavailable or deleted.
6. No. Local search performs case-insensitive substring matching over the title and file content.
7. No. The stable SDK marks native `provider=copilot` as unavailable. A separate host-injected adapter requires an actual host-supplied client and opt-in configuration.

## Chapter 16: Tiered Memory, Reflect, and Context Hygiene

1. Model context compaction shortens the active conversation; `squad nap` changes persisted `.squad/` files.
2. Hot is current task context, cold is summarized prior-session history, and wiki is durable structured reference knowledge loaded selectively.
3. No. Tier-aware flags and paths are design guidance, not an enforced v1.1.0 runtime contract.
4. HIGH confidence commonly comes from a clear correction, directive, important architectural insight, or root-cause fix. Capturing every message creates noise and can turn one-off details into misleading rules.
5. It previews intended cleanup actions and estimates before/after metrics without modifying state files.
6. Ordinary nap keeps the newest five sections; `--deep` keeps the newest three, in addition to the core context section.
7. No. The reference page describes the checkpoint flow, but the v1.1.0 source does not verify an automatic writer/reader for that path and schema.

## Chapter 17: Skills

1. `name`, `domain`, `triggers`, and `roles` (returned as `agentRoles` on `SkillDefinition`).
2. Each trigger substring match adds 0.5 points, with the trigger contribution capped at 0.7. A matching role adds 0.3; total score is capped at 1.0.
3. No. Confidence is frontmatter metadata and does not affect the registry’s score or ordering.
4. The APM-oriented CLI reads lowercase `skill.md`. The SDK loader reads uppercase `SKILL.md`.
5. No. The v1.1.0 browser obtains package bytes through its fetcher and returns an install result; it does not unpack or write them to the target directory.
6. The marketplace security module validates remote agent definitions, including charter injection patterns, requested tools, possible PII, permission language, source, and charter presence. It is not a scanner for arbitrary skill Markdown or scripts.
7. No. Parsing only checks format and constructs metadata/content. It does not establish safety or trustworthiness of executable code.

## Chapter 18: Directives, Ceremonies, and the Reviewer Protocol

1. A directive is a persistent expectation for future team behavior; a work request asks for a concrete task now.
2. Do not create a local or gitignored Markdown proposal as a persistence fallback or claim it was saved. Acknowledge it honestly and use the configured governed state tool when available.
3. After routing and before work-agent spawn, so the facilitator and participants can use the routed context and the work prompts can include its summary.
4. `all-relevant`, `all-involved`, or a comma-separated set of named agents.
5. No. Strict lockout prohibits the original author from contributing in any form to that revision.
6. Escalate to the user for a manual fix, new specialist, or other explicit resolution; do not silently re-admit a locked-out agent.
7. The SDK hook holds its registry in process memory; it does not itself persist state across process or session restarts.

## Chapter 19: Error Recovery and Iterative Retrieval

1. A transient failure such as a timeout, network error, or rate limit, provided the operation is safe to retry.
2. Attempts made, exact error messages, known facts, likely cause, unresolved uncertainty, and the specific decision/access/specialist needed.
3. `Task`, `WHY this matters`, `Success criteria`, and `Escalation path`.
4. Three cycles maximum. If cycle three does not meet criteria, escalate with the attempt history and remaining gap; there is no cycle four.
5. Validation confirms success criteria, detects skipped work or regressions, and resolves or escalates uncertainty before accepting the result.
6. No. The original author stays locked out of that artifact's revision after rejection.
7. Backoff schedules a delayed retry; an open circuit temporarily stops requests to avoid adding pressure to an unhealthy dependency.
8. No. It predicts quota exhaustion and reports whether the caller should open/pause; model selection is not implemented by that SDK class.

## Chapter 20: Scenario Playbook A: Solo, New, Existing, Mid-Project, Open Source

1. Exploration reveals actual architecture, tests, and conventions, reducing harmful guesses and helping keep the first change in scope.
2. It validates team fit and assumptions with low risk before broadening delegated work or automation.
3. Open source, because issues and PRs are public/untrusted inputs and automated permissions can affect contributors and project security.
4. No. Initialization creates project artifacts; it does not prove that workflows exist, are active, properly permissioned, or safe.
5. Run the exact test command and report its result/output; a summary alone is not evidence.
6. The solo operator remains accountable for correctness, security, and accepting the change; the agent is not an independent authority.
7. Confirm whether the state is tracked or external, compare backup and current revisions, preserve newer changes, and validate the restore on a copy or branch before overwriting active state.

## Chapter 21: Scenario Playbook B: Large Codebases, Monorepos, and Human Teams

1. Scoped discovery limits irrelevant context and provides time to understand the important module contracts. It can produce a verifiable path-backed map, whereas a blanket request can waste context and still miss relevant dependencies.
2. A single Squad with specialists is a better starting point when services share product goals, decisions, state, and review culture, and cross-service coordination is common.
3. `labelFilter` partitions issue candidates by issue label. `folderScope` does not enforce a filesystem write boundary or sandbox.
4. `.squad/workstreams.json`; the top-level list is named `workstreams`.
5. `SQUAD_TEAM` environment variable, then `.squad-workstream`, then auto-select if exactly one SubSquad is configured, then no active SubSquad/single-Squad behavior.
6. No. A human roster entry does not create an AI agent session or guarantee notification; the user must route the question through the real communication channel and relay the response.
7. Branch protection and required human PR reviewers (also code-owner rules or OS/container permissions) are stronger controls than routing prose.
