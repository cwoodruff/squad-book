# Appendix E: Quiz Answers

This appendix collects the answers to the chapter quizzes in this volume (Chapters 1–25). Full worked solutions to the exercises are in the book repository under `exercises/solutions/`.

## Chapter 1: MCP in Depth

1. The MCP host reads server configuration, starts or connects to servers, exposes their advertised tools to the model, and mediates calls and responses.
2. No. It contributes tools to the Copilot host. A Squad agent is an agent identity with a charter and work context; an MCP server is a tool provider.
3. The repository-root `.mcp.json` contains the CLI-generated `squad_state` entry.
4. `--additional-mcp-config @<path>` explicitly loads the project file; `--yolo` suppresses per-tool consent prompts in the non-interactive flow. They solve different problems and both have security implications.
5. The host can execute the configured program with the provided environment. That grants code execution and access to any credentials or permissions inherited by the process.
6. Confirm that the target harness consumes frontmatter MCP configuration, that its schema matches the emitted `mcpServers` shape, and that its runtime correctly resolves the command, arguments, credentials, and tools.
7. Check server startup and protocol compatibility, credentials/service authorization, tool arguments, active backend/repository resolution, and whether the operation is allowed. Tool registration does not guarantee successful service calls.

## Chapter 2: State Backends and Storage Providers

1. The Git-aware `StateBackend` chosen by config and used by Squad runtime state operations.
2. `local` (`WorktreeBackend`).
3. It writes to platform-local storage for one machine, not to a shared remote or synchronized service.
4. Conflict means the key definitely existed; uncertainty means the backend cannot determine whether creation succeeded. Inspect state before retrying uncertainty.
5. Another process can change the path after the existence check and before the subsequent operation, creating a time-of-check/time-of-use race.
6. The built-ins are filesystem, in-memory, and SQLite. The sql.js-backed SQLite provider loads and persists the DB in one process and warns that simultaneous multi-process access may corrupt data.
7. A native atomic conditional create: exactly one caller succeeds, existing contents are never overwritten, and ambiguous outcomes are surfaced instead of misreported as success.
8. The orchestration log preserves agent work/results across context loss. It is an evidence archive; durable curated memory is selected and distilled knowledge intended to guide later work.

## Chapter 3: Cross-Squad Orchestration

1. `name`, `capabilities`, `contact.repo`, and `accepts`; `contact.labels` shapes routing/triage.
2. `.squad/squad-registry.json`; entries contain a name and a local filesystem path to the peer repo root or `.squad` directory.
3. No. It inspects configured upstream sources and local registry entries/caches; there is no global repository crawl.
4. The current CLI invokes GitHub CLI (`gh issue create`).
5. The schema allows `prs` as an accepted metadata value, but current `delegateCommand` requires `issues` and only constructs an issue-create call.
6. A SubSquad partitions work within a repository via labels, optional folder scopes, and workflow selection. A separate peer Squad has its own repo/backlog and is discovered through a manifest; it retains independent ownership and governance.
7. It provides bundled scripts and a `mesh.json`-based pull/publish pattern using Git and/or HTTP. It is asynchronous/eventually consistent, not real-time messaging or a transactional distributed store.
8. `multi-squad.ts` selects among named personal Squad state directories under the global config root. It does not discover or delegate work to peer repositories; peer discovery is handled by manifests and the cross-squad runtime module.

## Chapter 4: Portability, Export/Import, and Inheritance

1. **Snapshot import.** It creates a copy that can evolve independently. An upstream is a separately configured source.
2. It archives the current `.squad/` directory with a timestamped suffix and replaces the active team with imported state. It is not a merge.
3. No. The exporter includes histories and warns the operator to review the content. History splitting happens during import and is not guaranteed sanitization.
4. Local directory/path, Git repository, and JSON export file. Sync validates a local path; validates that an export file exists; or pulls/reclones the cached Git source and updates sync metadata. It does not merge policy or refresh the contents of an export snapshot.
5. No. It returns separately named upstream result records and a context summary. It does not itself enforce later-wins/local-wins policy.
6. It is described in documentation, but absent from the installed v1.1.0 CLI help and not found as a matching implementation in the inspected source. Treat as unverified/preview, not a working stable command.
7. No. The documented agent artifact compiles coordinator behavior and explicitly omits live state such as decisions, histories and skills. Use a snapshot or ordinary versioned state files when preserving that information is required.

## Chapter 5: Clients, Hosts, and Programmatic Sessions

1. Each client exposes different tools, permissions, model controls, and result-handling behavior; repository instructions do not standardize the host runtime.
2. The CLI reference describes background `task` calls with later collection through `read_agent`; the VS Code flow returns results with the subagent call and does not use CLI-style polling.
3. Handle a smaller task inline with the coordinator, and be transparent that no child agent was started.
4. `SquadClientWithPool`, which combines the Copilot-backed `SquadClient` with a `SessionPool` and `EventBus`.
5. No. Shared repository files provide common instructions, not locking or conflict prevention. Use separate branches/worktrees or serialize writes.
6. Part IV, especially Chapters 19–20, covers Squad 2.0's multi-client projections.

## Chapter 6: Security Hardening

1. Shared state persists across sessions and can be read by agents that never saw the original untrusted issue. It can launder attacker-supplied instructions into a trusted-looking project file.
2. No. `gh auth switch` selects the local CLI identity for a GitHub host. An Actions job uses its configured token and permissions.
3. Azure workload identity authenticates to Azure resources. A GitHub App installation token authenticates to GitHub APIs and is scoped to an App installation. Azure identity may retrieve a GitHub token from Key Vault but does not replace it.
4. It checks selected diff patterns and, by design, exits zero even when it reports findings. It cannot prove a change safe or detect every credential, vulnerability, or prompt attack.
5. Examples include Copilot plugin requirements, package install hints, upstream commands, MCP server hints, and provider contracts. These are descriptive metadata in the plugin lifecycle, not authority to run installs or start servers.
6. Revoke or rotate the credential immediately, then inspect history and logs and audit activity performed with it. A later deletion does not invalidate a credential already disclosed or erase previous commits.

## Chapter 7: Containers, Cloud Hosting, and Deployment Modes

1. No. The image should contain no token. Supply a least-privilege GitHub credential at runtime through an approved secret mechanism.
2. It is a unique pod identifier used in the `squad-per-pod` topology. It does not authenticate the pod, authorize GitHub access, provide a work lock, or make local state concurrency-safe.
3. `agent-per-node`; any unset or unrecognized value falls back to this default.
4. No. The two deployment modes select capability-manifest lookup topology; they are unrelated to the interface used to interact with Squad.
5. No. Azure identity authenticates to Azure services. A PAT or GitHub App installation token is still required for GitHub API access.
6. Shared filesystem persistence preserves files but does not provide application-level locking, transactions, or safe concurrent writes for the local backend.
7. The loader selects the first parseable candidate; it does not merge manifests. Without a pod ID, the pod-specific candidate is skipped and shared/team or home candidates may still be selected.
8. No. Capability filtering determines local eligibility only. An external scheduler or queue must distribute work and prevent duplicate claims.

## Chapter 8: CI/CD and Release

1. Tests need to read source; they do not need to push commits, publish packages, or modify workflow settings. Read-only permission limits the impact of a compromised dependency or test step.
2. `.github/workflows/squad-ci.yml` is a conventional Actions workflow in the repository. `workflows/` contains the separate GH-AW package with Markdown workflow sources, package manifest, runtime resources, and generated/verified locks when installed into a consumer repository.
3. A full SHA identifies one immutable package revision. A branch or tag can move, making a repeated install produce different workflow code without an obvious revision change.
4. Compilation checks syntax and generated workflow integrity, not whether permissions and behavior are acceptable for a particular repository. The bootstrap PR introduces privileged automation and must be reviewed by a person.
5. GitHub commonly suppresses follow-on workflow runs caused by the default `GITHUB_TOKEN` to prevent recursion. The release workflow explicitly dispatches its next stage when needed; otherwise use a deliberate, separately approved trigger mechanism.
6. Rerun the failed publisher or dispatch it from the existing immutable release tag. Do not recreate or move the tag. Verify npm package tags, release assets, checksums, and package-manager outputs afterward.
7. No. It runs tests and builds a local image in CI. It has no image push, registry credential, or cloud deployment step.

## Chapter 9: Observability

1. A metric: it can aggregate agent failures over time. Traces help investigate individual failures; logs add event details.
2. `OTEL_EXPORTER_OTLP_ENDPOINT`.
3. OTLP/gRPC.
4. Environment variables set in a child process cannot modify its parent shell or another shell. Export the endpoint in the process environment that will run Squad.
5. 30,000 milliseconds (30 seconds).
6. No. It enables shell metrics collection but does not configure an exporter endpoint by itself.
7. No. The bridge emits an event span and ends it immediately; it is not a full long-running agent-task trace.

## Chapter 10: Troubleshooting and Disaster Recovery

1. No. Git can restore only content represented in the index, commits, or another backup.
2. A running pod proves that Kubernetes started a process. A ready worker also needs working authentication, routing, state access, and any required scaler/queue path; v1.1.0 does not provide a built-in HTTP readiness endpoint for all of that.
3. The runtime has no built-in `/healthz` or `/readyz` HTTP endpoint that confirms GitHub connectivity/readiness.
4. No. A longer grace period gives a process more time to exit but does not guarantee checkpointing; the documented runtime does not checkpoint in-flight tasks before shutdown.
5. Streaming usage history: 1,000 FIFO events. Telemetry collector queue: 500 FIFO events.
6. Remote paths can use the default branch and may not see a feature branch or local state. Naming and verifying the target revision prevents stale-context QA.
7. It can destroy durable team knowledge and diagnostic evidence without distinguishing state corruption from code/runtime problems.

## Chapter 11: Squad Architecture

1. The CLI package, `@bradygaster/squad-cli`, supplies the `squad` executable. The SDK is a reusable library.
2. It shields Squad code from direct dependence on upstream Copilot session/client types and translates options/events as required.
3. Normalized work-item and pull-request operations, including listing/getting/creating work items, labels/tags, assignments, comments, branches, PR creation, and merging.
4. No. The function is exported by the SDK, but the inspected `SquadCoordinator.handleMessage()` path does not invoke it. A caller must wire it in for it to govern that path.
5. The v1.1.0 checkout contains no `docs/specification/adr-001*` documents and no verifiable explicit Squad 2.0 design statement. It does not establish a future design contract.
6. The SDK root entry point is designed as a side-effect-free public API; the CLI executable and its interactive shell live in the separate CLI package.

## Chapter 12: Inside the Coordinator

1. When the resolved team root has no `team.md`, or the `## Members` section has no roster entries (with `.ai-team/team.md` considered for migration).
2. Init Mode Phase 1: propose the team and stop for user confirmation before creating files.
3. Squad (Coordinator), append-only.
4. To confirm that the configured runtime persistence tools are reachable before mutating state owned by a non-local backend. If the handshake fails, the coordinator must not fall back to raw filesystem writes.
5. Any three: do not re-explain context agents already know; do not intervene while agents run; present output directly; do not add unsolicited analysis; do not spawn unnecessary follow-ups; keep commentary brief.
6. It starts all requested spawn promises and uses `Promise.allSettled`, turning each failure into its own failed result rather than allowing one rejection to cancel successful peers.
7. It transports an already prepared spawn request through a platform-specific mechanism; routing chooses the specialist earlier.
8. The `coordinator-source-of-truth` skill, summarized in `.github/agents/squad.agent.md`.

## Chapter 13: Agent Identity and Provenance

1. The registry object key, such as `runtime-engineer`, is the stable identity.
2. A tombstone preserves historical references and prevents an ID from being reassigned to a different logical agent.
3. No. A future revision makes the binding unavailable; the consumer fails closed for the artifact rather than keeping a valid-looking subset.
4. HEAD present and EOF absent indicates that the coordinator payload is visible but appears truncated; halt rather than proceed with incomplete instructions.
5. The MCP tool would only be invoked by instructions inside the missing payload, and MCP reachability is not proof of root-coordinator identity. The selection evidence must come independently from the host.
6. No. Squad registry entries and task bindings do not change Git's author or committer configuration.
7. `UNREGISTERED` means no trusted release-manifest entry exists for the version/client envelope (for example a local or newly updated artifact). It should be reported distinctly but must not halt an otherwise transport-intact session.

## Chapter 14: The SDK in Depth

1. `defineConfig()` describes a public config schema with `team`, `agents`, `routing.pattern`, and model defaults, while SDK-first builders define a composable `SquadSDKConfig` that `squad build` compiles into markdown files.
2. It returns `null` when it cannot find `.squad/`.
3. `SquadClientWithPool` is exported from `@bradygaster/squad-sdk/client`; `SquadCoordinator` is exported from `@bradygaster/squad-sdk/coordinator`.
4. The route tool needs fan-out dependencies (including a session-spawn capability) to create the requested work. A registry without them cannot spawn sessions.
5. It loads a `SquadSDKConfig`, plans and generates files such as `.squad/team.md`, `.squad/routing.md`, and agent charters, with dry-run and drift-check modes available.
6. No. A typed rule is configuration data. Dispatch requires a compatible runtime coordinator and spawn dependencies; authentication and session creation are separate concerns.
7. The source `ConfigLoadResult` contains `config`, optional `source`, and `isDefault`; the runtime `SquadConfig` does not define `team`, and the loader does not return `errors` or `warnings`. The docs and current source disagree on these examples.
8. Remove event listeners/detach the streaming pipeline and shut down or disconnect the client/session pool. Also destroy owned agent handles where the application manages them.

## Chapter 15: Plugins, Extensions, Tools, and Hooks

1. A change to global coordinator routing belongs in Squad core and should go through the maintainers' RFC process.
2. No. `upstream.installCommand` is metadata for humans; Squad does not execute it.
3. `marketplace browse` lists top-level directories from a registered GitHub repository through authenticated `gh`. Plugin `install` deploys a plugin from a local directory after validating its manifest and static files. Browsing does not remotely fetch/install the selected directory.
4. The plugin must be installed and enabled, declare runtime capabilities, use a supported lifecycle event and capability type, name an approved provider, and provide safe output paths. (Any two of these conditions earn credit.)
5. `squad_route` needs host dependencies to create a real agent session. Without the fan-out dependency getter and required collaborators it returns a failure instead of claiming it dispatched work.
6. `HookPipeline` uses `action: 'allow' | 'block' | 'modify'` and `modifiedArguments`; a session `onPreToolUse` callback uses the adapter's permission fields such as `permissionDecision`, `modifiedArgs`, and `additionalContext`. They are different types and must be wired at their respective integration points.
7. The helper targets email-like strings only, can miss other sensitive data, and does not protect data that is logged or transmitted outside its post-tool result path. It is one transform, not a complete privacy control.

## Chapter 16: Building Autonomous and Resilient Agents

1. The task ledger survives session turnover and records claims, attempts, checkpoints, and committed side effects. A transcript alone does not provide atomic ownership or a reliable completion state.
2. Retry when the failure is plausibly transient and the side effect is idempotent or protected by an idempotency key. After a timeout with an ambiguous outcome, query/resolve the prior operation before repeating it.
3. No. It simulates latency, responses, token use, decisions, memories, and some route events; it does not call an LLM for each task.
4. Five consecutive failures and a 30-second cooldown. It guards operations in Git-backed Squad state backends, not arbitrary services, and its state is in-memory.
5. Microsoft Agent Framework's base durable-workflow mechanisms provide checkpoint/restore; the Squad adapter does not define a separate serialization protocol.
6. The current integration defaults to `PermissionHandler.ApproveAll` and passes `--allow-all` unless overridden. A production host must replace/narrow the SDK permission handler and independently constrain CLI/OS permissions.
7. Inspect actual subagent dispatch events or OpenTelemetry spans, including the dispatch lifecycle. A coordinator's text that mentions a specialist is not proof that a session was spawned.

## Chapter 17: The Squad Specification

1. A profile is a versioned contract for an artifact or behavior surface. A capability identifier names one operation of that profile, such as `squad-charter/v0.1/validate`.
2. `executable-normative-draft` is the only claimable maturity represented by Charter in this suite. Claimable does not mean published: Charter remains a working draft.
3. False. Dependencies establish interpretation/order; they do not confer capabilities or conformance claims transitively.
4. `accepted` means a consumer may accept the document, including compatible legacy input. `conforms` means it is canonical for the selected profile; warnings can leave a document accepted but nonconforming.
5. Examples include canonical snapshot digest and compare-before-mutate behavior, API-version evidence, idempotent retries, provider-drift handling, precedence for simultaneous conditions, or sanitized deterministic transcripts.
6. A JSON schema validates that fields have the expected shape. It cannot authenticate an actor, prove that a provider identity is genuine, or evaluate whether the authority basis and policy actually permitted the operation.
7. `state-memory-requirements-v0.1.md` is informative and non-claimable. It separates state-authority promotion from memory-classification/provider-dispatch promotion.
8. `client-harness-adapters`, `client-backend-decoupling`, and `ADR-001` are not present in the v1.1.0 specification tree covered by this chapter.

## Chapter 18: Squad 2.0: What Changed and Why

1. One repository-owned `.squad/` team can be used through multiple host-native integrations without keeping separate, drifting team definitions. Host files are projections, while the roster and charters stay shared.
2. **Client plane:** host configuration, UI/event adaptation, and dispatch. **Control/broker plane:** conversation identity, ordering, approvals, capabilities, cancellation, and durable history. **Execution plane:** workers, tools, checkpoints, retries, and task execution.
3. Intersection ensures a capability is effective only if the host offers it, the backend supports it, and policy permits it. A union would incorrectly claim a feature when any necessary layer lacks it or disallows it.
4. No. The bridge exposes the backend tools only when started with `--experimental-backend` or `SQUAD_EXPERIMENTAL_BACKEND=1`; `SQUAD_BACKEND_URL` by itself does not enable them. The bundled bridge has no execution harness, so it is not a turnkey hosted agent runtime.
5. Squad no longer finds or falls back to a profile-level personal/global team; resolution is project-local, walking from the current directory through parents and respecting repository boundaries. Run `squad init` in the project or use `--team-root <path>` where supported to select an explicit team root.
6. Local project configuration wins; then earlier upstream entries win over later entries. Run `squad upstream sync` after upgrading and reorder configured sources if you relied on the prior later-wins behavior.
7. Run `squad roster add rai` (or preview it with `--dry-run`). Upgrades preserve `team.md`; the explicit command inserts the optional built-in row and records a verified backup and provenance so later removal can target only its own change.
8. No. Epochs are cooperative, client-asserted fencing values that reject stale writers, but any caller able to present a larger value can take over. They have no broker-issued holder identity or expiry and are not an authentication/authorization boundary.

## Chapter 19: Using Squad Across Clients

1. Seven host coordinators can point at one `.squad/` team; it does not create seven rosters.
2. It adds Claude and Codex to the requested set, refreshes them, and also refreshes any configured host such as Copilot.
3. `squad client list` (also `ls`) and `squad client add <list> [--dry-run]` are defined. There is no `squad client remove` subcommand in this preview.
4. Claude needs the project `.mcp.json` explicitly passed as `--mcp-config .mcp.json`; a headless `claude -p` invocation without it may lack the state tools.
5. `cursor-agent mcp enable squad_state`.
6. A full path in Codex home configuration; the guide warns against an 8.3-style short path.
7. Google Antigravity. Quota is per model, and `--model` selects an alternate.
8. Record runtime decisions with `squad_decide`; edit the static `.squad/routing.md` as a workspace file (or use the relevant Squad CLI workflow).

## Chapter 20: Host Projections, Client Adapters, and Capability Negotiation

1. The implemented `HostProjection` has synchronous `project(ctx)`. `createClientAdapter({ host, ctx, runtime? })` constructs the runtime facade. The draft's illustrative projection SPI differs from that implemented interface.
2. The token describes resuming a transcript/event subscription from a cursor. It is declared across the seven hosts and is not a product selector.
3. An omitted policy list supplies no restriction in the local helper; an explicit empty array removes every token. The same distinction applies to backend lists.
4. No. Without a binding, the facade uses absent restrictions and returns the advertisement as its effective list. Runtime submission still throws `AdapterUnboundError`, and no backend authorization took place.
5. The coordinator reads the selected member's charter and includes it in that specialist's delegation prompt. Projection embeds the coordinator digest and dispatch instructions, not a compile-time copy of every charter.
6. Pass remaining hosts as the third `keep` argument: `uninstallClients(['claude'], ctx, ['copilot'])`. Persisted client configuration must be reconciled separately if intended.
7. Expected-failure tests establish that a required projected coordinator section is missing. They validate the gap rather than validating successful feature execution. Support status and evidence strength are independent axes.
8. `/clients` preserves the same host adapter exports and runtime references as a deprecated alias. It does not create another registry, implement another backend, add execution harnesses, or re-export the older session client classes supplied by `/client`.

## Chapter 21: The State MCP Boundary, Runtime Upstreams, and the Experimental Backend

1. Required: `author`, `summary`, and `body`; optional `references` is a string array. It writes a dated note into the decision inbox (or the active workstream's inbox), not directly into the shared decisions file.
2. The check confirms that the bridge runtime version and team root match the coordinator's expectations and identifies the active state backend. A mismatch means writes could go to stale code or the wrong team's state.
3. The local skill wins, then the earliest declared upstream. Upstreams are processed in declared order and each source's nested sources follow depth-first, with a default maximum depth of three.
4. No. Session resolution reads already materialized local paths, Git clones, or export files. `squad upstream sync` explicitly refreshes Git clones and validates local/export sources; there is no implicit network fetch at startup.
5. The process must receive `--experimental-backend` or `SQUAD_EXPERIMENTAL_BACKEND=1`. The URL selects a backend only after opt-in; by itself it must not expose tools or route a token.
6. It implements `submit`, `subscribe`, `cancel`, `respondApproval`, and `describe`. With no harness, the bridge reports an empty harness list and `executionAvailable: false`; send-message refuses as unavailable.
7. Examples: approval hashes are opaque and supplied by the harness rather than broker-computed; epochs are client-asserted rather than broker-issued lease tokens; cursors are unsigned; conversations are whole-file snapshots; there is no bundled execution harness; remote DurableSquad Phase 2 approval/lease coordination is pending.

## Chapter 22: Upgrading to Squad 2.0 and the Road Ahead

1. `latest` remains on Squad 1.1.0.
2. No. Self-upgrade installs only the CLI package. Run `squad upgrade` separately in each project.
3. The registry must be empty and have no meaningful prior cast history; every specialist roster row must resolve to one existing charter folder, and the team must state a universe. If any fact is missing or ambiguous, the backfill fails closed.
4. It lists records that could not be normalized and their reasons. It does not mean a partial registry was committed; the repair refuses the whole operation.
5. `squad health` performs stronger semantic routing-reference validation. `squad doctor` checks routing-file presence and casting-pair consistency.
6. Earlier entries win.
7. No. `uninstallClients()` removes generated client projections only; it is not a package downgrade or project rollback.
8. Restore the project files and state to the 1.1.0 baseline first, then install the 1.1.0 CLI and validate the restored project.

## Chapter 23: Patterns, Anti-Patterns, and the Cookbook

1. It should state boundaries and constraints: what is included, what is excluded, and how completion will be verified.
2. When the work is narrow, sequential, or specialist-owned; a full-team fan-out would add overhead or overlap.
3. It enables spawning agents to work on issues selected by triage. Without it, triage scans/categorizes rather than executing issue work.
4. Both sides need compatible field names, types, omission/null behavior, and error semantics. An agreed contract prevents parallel implementations from diverging.
5. No. The statement must be backed by reproducible test output, and tests do not replace diff review or acceptance-criteria verification.
6. “Ralph, go” is a natural-language cue to the work monitor in a conversational workflow; `squad triage` is the actual CLI command with its own configured scan and execution behavior.
7. Record choices that should guide future tasks, multiple agents, or later changes. Keep one-off local implementation decisions local unless they become a reusable convention.

## Chapter 24: Capstone: Tasktrack to Production

1. It creates a Squad project layout and default agent/workflow scaffolding. Inspect Git status and generated files, then use diagnostics such as `squad doctor` and `squad health` to verify setup.
2. It enables triage to spawn agents to work on selected issues; it should be explicitly enabled after reviewing scope and selection.
3. No. PRD mode is invoked through the conversational workflow described in Chapter 10 (Volume 1); the v1.1.0 CLI help does not list a `squad prd` command.
4. The Copilot client launches the local `squad state-mcp` process through `.mcp.json`; it uses MCP over standard input/output (stdio).
5. No. It configures where Squad state is stored. Tasktrack's API data store is separate.
6. The baseline companion project has no npm dependencies or lockfile. The tests use Node's built-in test runner.
7. No. Aspire observes telemetry emitted by the configured Squad CLI/SDK instrumentation. Tasktrack's HTTP API needs its own instrumentation to emit application request telemetry.
8. A separate application deployment is required: publish the reviewed container image to the chosen registry and deploy it using the target platform's approved workflow.

## Chapter 25: Contributing to Squad

1. `dev` is the integration base; ordinary feature PRs target `dev`.
2. `>=22.5.0`.
3. `npm run build`.
4. No. Maintainer approval and the explicit release process remain separate from CI.
5. No. Insider is an npm prerelease channel, published by a workflow from `dev`.
6. `.github/workflows/squad-promote.yml`.
7. Examples include reproducible issue reports, documentation, code review, discussion support, deployment case studies, and videos.
8. Because the docs-site guide and root v1.1.0 package scripts differ. Verify commands against `package.json` and the CI workflow before following or documenting them.
