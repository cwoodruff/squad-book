# Chapter 21: The State MCP Boundary, Runtime Upstreams, and the Experimental Backend

> **Prerequisites:** Volume 1 (or equivalent Squad experience); Chapters 2 and 19.

## What You'll Learn

- Treat `squad_state` as the governed runtime boundary for mutable Squad state, not as permission to edit every file beneath `.squad/`.
- Identify all state and governed-memory tools exported by `squad state-mcp`, and distinguish the default tools from the experimental conversation tools.
- Understand how a versioned MCP bridge is installed through the committed `.squad/squad.mjs` launcher, probed, cleaned up, and anchored to the correct project and team roots.
- Explain how governed memory keeps one store for the CLI and the `memory.*` tools across state backends.
- Resolve upstream inheritance deterministically from local snapshots, including precedence, depth, cycles, soft failures, and provenance.
- Explain the experimental `@bradygaster/squad-sdk/backend` contract, the two experimental execution harnesses, and why a transcript backend is not a production DurableSquad service.
- Relate the client/backend decoupling draft and its G1–G9 conformance gates to the durable-backend tutorial and to what remains experimental in v2.0.0.

## The State Boundary: Runtime Writes, Static Team Design

A Squad project has at least two kinds of information. Static team design tells Squad what team exists and how it should behave: `.squad/team.md`, `.squad/routing.md`, `.squad/config.json`, charters, templates, skills, and the casting registry. Mutable runtime state records what happens as that team works: decision inbox entries, agent histories, logs, sessions, scratch data, and identity notes. They may share the `.squad/` directory, but they do not share the same write policy.

The `squad state-mcp` process bridges a host's Model Context Protocol client to Squad's runtime state tools. Its default server identity is `squad-state`; hosts commonly display the server as `squad_state`. The process starts in a project directory, discovers the Squad context, and registers tools against the configured storage provider. A host invokes those tools by their advertised names; adapters can prefix or normalize names, so use the name in the current host's tool list rather than guessing it.

There are 15 default tools: one decision tool, eight `squad_state_*` tools, and six `memory.*` tools. The table gives their JSON arguments. Only the listed arguments are part of the tool schemas; a host may add a transport-specific prefix to the visible tool name.

| Tool | Arguments | Contract |
|---|---|---|
| `squad_decide` | Required: `author` (string), `summary` (string), `body` (string). Optional: `references` (string array). | Writes a dated decision note to the decision inbox. The note records author, summary, references, and rationale; if a workstream inbox is active, the tool uses it. It is an inbox/drop-box operation, not a direct rewrite of the shared decisions document. On the `orphan` and `two-layer` backends the result says that the path is a key on the `squad-state` branch, not a file in the working tree. |
| `squad_state_health` | None (`{}`). | Reports the stamped `squad-state` runtime version, a `Health metadata:` JSON line (schema `squad-state-health/v1`), backend name (for example `local`, `orphan`, or `two-layer`), storage-provider class, and resolved team Squad directory. It is the preflight check for ensuring the host is connected to the expected bridge and team root. |
| `squad_state_list` | Optional: `dir` (string), relative to `.squad/`; omitted means the root. | Lists entries in a directory. Use it for `agents/`, `decisions/inbox/`, or another directory; `squad_state_read` expects a file. |
| `squad_state_read` | Required: `key` (string), relative to `.squad/`. | Reads a state key through the configured backend. It is also useful for reading static files for inspection; the restriction is on mutations, not on all reads. |
| `squad_state_write` | Required: `key` (string), `content` (string). | Replaces the complete content of an allowed mutable state key. The key is normalized and checked against the mutable-state allowlist before writing. |
| `squad_state_append` | Required: `key` (string), `content` (string). | Appends to an allowed mutable key. Built-in Rai and Fact Checker audit-trail files are append-only: this tool can append, while write and delete are refused. |
| `squad_state_delete` | Required: `key` (string). | Deletes an allowed mutable state key; it cannot delete static configuration or the protected built-in audit trails. |
| `squad_state_create_if_absent` | Required: `key` (string), `content` (string). | Atomically creates an allowed mutable key only if absent. A conflict or uncertain outcome is reported as failure rather than pretending the write succeeded. |
| `squad_state_upstreams` | Optional: `detail` (boolean; default `false`). | Reports declared upstreams, status, provenance, diagnostics, and effective inherited content. With `detail: true`, includes inherited decision, routing, wisdom, and skill bodies under provenance labels. It never fetches. |
| `memory.classify` | Required: `content` (string). Optional: `class` (`TRANSIENT`, `LOCAL`, `DECISION`, `POLICY`, `COPILOT_MEMORY`, or `FORBIDDEN`). | Applies the memory governance classifier without persisting the proposed body. |
| `memory.write` | Required: `content` (string). Optional: `title`, `author` (strings), `class` (the same six classes), `approved` (boolean). | Classifies and, when allowed, stores governed local memory. Semantic/external memory requires an explicitly configured bridge; this tool does not silently send data to a remote memory service. |
| `memory.search` | Required: `query` (string). | Searches governed local memory and returns matching snippets and identifiers. |
| `memory.promote` | Required: `id` (string), `targetClass` (`LOCAL`, `DECISION`, `POLICY`, or `COPILOT_MEMORY`). Optional: `actor` (string). | Promotes an existing entry to a permitted durable class, subject to governance. |
| `memory.delete` | Required: `id` (string). Optional: `actor` (string). | Deletes a governed local-memory entry and writes an audit tombstone. |
| `memory.audit` | None (`{}`). | Lists audit metadata without including the stored memory bodies. |

> **Note:** Tool success is not a license to bypass the static/mutable boundary. The runtime validates and normalizes state keys, confines them to the selected Squad root, and allows mutations only for defined runtime paths. Attempting to write `.squad/team.md`, `routing.md`, `config.json`, or a charter such as `agents/data/charter.md` with `squad_state_write` is rejected. The same applies to other static material such as templates and skills. The team should not hand-edit `.squad/casting/`: use the supported casting workflow/protocol so its registry/history pair remains consistent. In v2.0.0 nothing under `casting/` is a mutable state key, `casting/policy.json` included: casting is source-branch configuration on every backend.

The file-oriented tools are intentionally narrow. Examples of allowed paths include the decision document and inbox, individual agent `history.md` files, logs, orchestration logs, sessions, `.scratch/`, identity, and the active-workstream decision inbox. A path such as `agents/data/charter.md` is not a mutable-state path just because it is under `agents/`. `squad_state_create_if_absent` is the safer primitive when several agents might initialize the same key: exactly one create wins; other attempts get a typed conflict, while uncertain outcomes remain failures that require inspection.

An MCP server can expose the same tool differently in each host. For example, Copilot may show `squad_state_read`, while another host can display a server-prefixed name. The canonical names in the table are the names advertised by Squad. If the host tool is absent, update or restart the MCP connection; do not fall back to shell commands that edit mutable state behind the backend's back.

### How This Builds on Chapters 1, 2 and 4

Chapter 1 described MCP as a way to make external tools available and covered where each host reads the `squad_state` bridge, treating the integration primarily as a host configuration and trust problem. Here the state bridge is also the portable entry point for governed mutable state and (when separately enabled) an experimental conversation backend. The bridge's version and resolved team directory are visible through `squad_state_health`. Init and upgrade reconcile one project-root MCP entry rather than an ever-growing set of home-level definitions, and in 2.0 that entry runs a launcher committed with the repository instead of a path on one machine.

Chapter 2 described Squad's `local`, `orphan`, and `two-layer` state backends and the existing SDK `StateBackend` abstraction. Those remain the underlying persistence choices for ordinary Squad state. The conversation backend SPI is a separate contract: the optional MCP conversation tools can use the configured state backend as a persistence adapter, but that does not replace the Git-native state backends or turn them into an execution service. Chapter 4 summarized upstreams as a portability/inheritance mechanism; this chapter adds the depth: every supported host can inspect the effective, provenance-tagged resolution through `squad_state_upstreams`, using the same resolver that powers doctor/status output.

### Governed Memory Across Backends

The six `memory.*` tools and the `squad memory` CLI open the same backend-aware store, so a memory written from the terminal is the one a host searches over MCP. Chapter 15 (Volume 1) teaches the classes and the workflow; this section covers how the store behaves under the state backends from Chapter 2.

| Behavior | v2.0.0 rule |
|---|---|
| Storage | The store lives under `.squad/memory/` (`index.json`, `config.json`, `audit.jsonl` and its rotated archives, `tombstones/`) and is read and written through the configured state backend, so on `orphan` or `two-layer` it is on the state branch |
| Classes | Case-insensitive (`decision` means `DECISION`); an unknown class is a failure result, never a memory filed under an invented class |
| Promotion | `memory.promote` requires `targetClass` and refuses `FORBIDDEN` and `TRANSIENT` targets |
| Outside a squad | `squad memory` commands, `classify` included, fail instead of creating a store somewhere unexpected |
| Concurrency | Every read-modify-write of the index takes a lock, across store instances and processes. Filesystem storage keeps the lock under the resolved `.squad/`; a git-branch backend coordinates on its shared state ref, so worktrees of one repository share it |
| Backend migration | Moving from `local` or `worktree` storage to `orphan` or `two-layer` carries the decision inbox, the index, configuration, audit archives and tombstones in one transaction. It aborts on a destination conflict or transfer error before switching backend authority, and keeps the source files until the configuration write succeeds |

The migration rule is the one to remember before you run `squad upgrade --state-backend orphan` on a team with memories: a failure leaves the old backend authoritative and its files in place, so you can fix the conflict and retry. Run it with `--dry-run` first; a dry run does not migrate, delete or install anything.

## Versioned Bridges, Roots, and Cleanup

A managed MCP bridge is useful only if you know what executable the host starts and which project it is serving. Squad's root configuration helper writes the `squad_state` entry to the repository-root `.mcp.json`. It preserves other MCP servers and user-supplied fields, refreshes the managed `command` and `args`, preserves the entry's environment and tool allowlist, and refuses to overwrite a malformed JSON config.

The launch spec is resolved in two steps. `resolveSquadStateMcpSpec` in `mcp-spec.ts` first finds how the running CLI could start itself: the standalone bundle launcher if present, otherwise `node <absolute dist/cli-entry.js> state-mcp`, otherwise the exact running version through `npx`. Dist-tags such as `latest` or `insider` are never written. The first two forms are paths on this machine, so files a repository commits use `resolveCommittedSquadStateMcpSpec`, which swaps them for a portable form:

| What the CLI found | What `.mcp.json` and the other hosts' configs get |
|---|---|
| An npm-installed CLI entry | `node -e <root finder> .squad/squad.mjs state-mcp` |
| A standalone bundle | A bare `squad state-mcp` (the bundle puts `squad` on PATH) |
| A CLI running from a package runner's temporary cache (`npx`, `pnpm dlx`, `yarn dlx`) | The exact-version `npx -y @bradygaster/squad-cli@<version> state-mcp` |

### The committed launcher and the root finder

`.squad/squad.mjs` is a small script that `squad init` and `squad upgrade` write and that you commit. It finds a Squad CLI on whatever machine runs it, in this order: `SQUAD_CLI` (a command, or a `.js` entry run with the same Node), the repository's own `node_modules/@bradygaster/squad-cli`, a `squad` on PATH, then the CLI that last ran `squad init` or `squad upgrade` on this machine (recorded in `~/.squad/cli.json`). It skips any of the last three that is older than the version that wrote the launcher. Only with `SQUAD_ALLOW_NPX=1` does it fall back to `npx -y @bradygaster/squad-cli@<that version>`, because that downloads and runs code; otherwise it fails with install instructions. A file at `.squad/squad.mjs` without Squad's marker is treated as yours and left alone.

The `node -e` wrapper exists for monorepos. Claude Code, for example, finds the root `.mcp.json` from a package subfolder but starts the server in that subfolder, where a plain `node .squad/squad.mjs` cannot find the file. The inline script walks up to the nearest folder that contains `.git`, refuses an absolute launcher path or one containing `..`, and runs only that repository's `.squad/squad.mjs`. A launcher in a package's own `.squad/`, or above the repository, is never run. Each entry also carries an `x-squad` block (`managed`, `version`, `machineSpecific: false`, `source: "repo-launcher"`, and the `npx` fallback) so tools can tell a Squad-managed entry from a hand-written one.

Claude Code hooks reach the same launcher as `node "$CLAUDE_PROJECT_DIR/.squad/squad.mjs" hook claude <Event>` (Chapter 20). `squad doctor` checks the result with a `portable squad_state launch` check: an absolute path into one machine's install is a warning, a path that does not exist here (a file written on another machine) is a failure, and so is a missing `.squad/squad.mjs`. The fix for an existing repository is one `squad upgrade`, then a commit.

The root choice is deliberate. `squad init` and upgrade can make the project's bridge discoverable without writing a new global entry for every repo. If an older release left a duplicate `squad_state` in `.copilot/mcp-config.json`, the lifecycle code removes that stale project-level definition. It also recognizes this project's older hashed user-level entries, saves a backup before removing them, and supports a dry-run reconciliation. A malformed or unrecognized user file is left alone. Root-safe here means both configuration and data access have explicit roots: the MCP config is rooted at the project, state mutations are resolved against the team `.squad/` root, and upstream declarations are resolved from the project's own `.squad/` directory. This matters when a project links to a shared team-state location; project-specific upstream declarations do not accidentally migrate with the team root.

Doctor's MCP probe follows the configured project entry before a user-level fallback, starts the process with the project as its working directory, negotiates MCP initialization, lists tools, then calls `squad_state_health`. It records the server version, available tools, health text, and stderr. A missing health tool, a timeout, or process startup failure indicates an incompatible or broken bridge rather than a successful connection. The bridge initializes lazily in the standard server path, so simply opening a pipe does not have to block while state is resolved.

Shutdown is part of correctness. On stdin end/close, disconnect, SIGPIPE, or an EPIPE on stdout, the server closes its MCP transport; transport teardown is best-effort and a short grace timer prevents a stranded process. This cleanup is particularly important because the host owns the stdio process lifecycle. Keep output protocol-clean: logs belong on stderr, not intermixed with JSON-RPC messages on stdout.

```mermaid
sequenceDiagram
  participant H as "MCP host"
  participant P as "Doctor probe"
  participant M as "squad state-mcp"
  participant S as "Resolved Squad state"
  H->>M: Start from project root
  P->>M: initialize
  M-->>P: serverInfo version and tools capability
  P->>M: tools/list
  M-->>P: squad_state and memory tools
  P->>M: tools/call squad_state_health
  M->>S: Resolve team root and backend
  S-->>M: backend identity and storage
  M-->>P: version, backend, storage, team directory
  H-->>M: stdin closes or host disconnects
  M->>M: Close transport and release process
```

A bridge's version is not interchangeable with the user's CLI version or the host's version. The health tool reports the version stamped into the running state server; compare it to the coordinator's stamped version and expected team root before writing. If the bridge is older or points at a different team directory, treat it as unavailable and repair the connection. For non-local backends, do not claim a successful durable write if the host cannot reach the correct MCP bridge. The coordinators Squad generates for the six non-Copilot hosts follow this rule: when `squad_state` is unavailable and `.squad/config.json` names a non-local `stateBackend`, they stop and say so instead of writing `.squad/decisions.md` directly.

The health text includes one machine-readable line, `Health metadata: {…}`, with schema `squad-state-health/v1`:

| Field | Meaning |
|---|---|
| `cliVersion`, `sdkVersion`, `bridgeVersion` | The CLI that launched the bridge, the SDK it runs, and the stamped bridge version |
| `stateBackend` | The configured backend name |
| `resolvedTeamRoot` | The directory that contains `.squad` |
| `resolvedSquadDir` | The squad directory itself |
| `resolvedTeamDir` | Kept for existing consumers; despite its name it holds the team root, the same value as `resolvedTeamRoot` |
| `launchMode` | `stdio` for the MCP bridge |

`squad health --json` reports the same fields under `metadata` (with `launchMode: "cli"`) in its existing `squad-health/v1` report. Prefer `resolvedTeamRoot` and `resolvedSquadDir` in new scripts.

Roots can have two spellings. On macOS, `/tmp` is really `/private/tmp`, and a linked team root can be a symlink. Squad stores the resolved path, so before v2.0.0 a bridge given the original spelling refused reads and writes with "Path traversal blocked". In v2.0.0 `squad_state` accepts both spellings and the doctor bridge check compares real paths, while a path that really leaves the team folder, including through a symlink inside it, is still refused. A project linked to a team repository (`squad link`, `squad init --mode remote`) now gets no placeholder local roster or casting; its hosts read the linked team only through `squad_state`.

## Runtime Upstreams: Explicit, Local, and Traceable

An upstream declaration lives in `.squad/upstream.json`. The `squad upstream` CLI supports `add`, `remove`, `list`, and `sync`. An upstream can be `local` (a local directory), `git` (a repository with an optional ref), or `export` (an exported JSON snapshot). Git sources are materialized under `.squad/_upstream_repos/<name>/`; the cached clone is ignored by Git. Local paths and export files are read from their declared locations.

The key operational invariant is that resolution is offline and repeatable: session startup reads local snapshots only. It never runs `git fetch` or pulls a remote. For a Git source, `squad upstream sync <name>` updates the existing cache or materializes it, then refreshes `last_synced`; for local/export sources, sync validates that the source is present. `squad upstream add` on Git is transactional: it records the declaration only after the clone succeeds. If the initial clone fails, the config is left unchanged. This distinction keeps host startup fast and ensures you can reason about precisely which snapshot the coordinator saw.

Precedence is deterministic, and the order is not the one the 1.x docs taught (later entries winning). The consumer's own local `.squad/` always wins. Then direct upstreams are processed in the order declared in `upstream.json`, with an earlier entry winning a conflict over a later one. Each upstream's nested upstreams follow immediately after it, depth-first, before the next sibling. Direct upstreams are depth 1, with the default maximum depth of 3. A diamond—two paths that reach the same source—contributes only once from its earliest, highest-precedence visit. Skills with a name conflict retain the earlier/local winner; the report still shows the losing item and identifies `overriddenBy`. Decisions, routing, and wisdom are additive context rather than replacements for local decisions/routing. A local casting policy wins; otherwise the first inherited casting policy is effective.

```mermaid
flowchart TD
  L["Local .squad state"] --> W["Local values win"]
  U1["Upstream 1: org-standards"] --> D1["Its nested sources, depth first"]
  U2["Upstream 2: platform"] --> D2["Its nested sources, depth first"]
  W --> E["Effective context with provenance"]
  D1 --> E
  D2 --> E
  U1 --> D1
  U2 --> D2
  E --> R["squad_state_upstreams / doctor / status"]
```

`resolveUpstreams` returns more than a merged list. Each result includes its declared origin, type, depth, route (`via`), last sync time, status, diagnostic, source directory, and provenance. Statuses include `ok`, `stale`, `missing`, `unavailable`, `invalid`, `cycle`, and `depth-exceeded`. A stale Git snapshot—more than 30 days since its last sync by default—is still readable, but it is clearly labeled. Missing local paths, missing export files, unsynced Git caches, invalid declarations, cycles, and depth overflow each produce a diagnostic; one bad source does not cancel the other readable sources.

Every inherited item carries a tag in the form `upstream:<name>@<ref>`. The suffix is the Git ref for Git sources, `@local` for local sources, or `@export` for exports. A nested source keeps its own name/ref provenance, while `via` explains how it was reached. Cite provenance when inherited policy informs a recommendation or spawn; this makes a copied practice auditable and gives a project owner a clear place to update it.

Cycle detection compares resolved source identity against the active inheritance chain. A cycle is reported and skipped rather than recursed into. Resolver security is also intentionally conservative: nested files are read through a confined reader; links are not followed; file, directory, byte, and depth budgets bound input; and a refused read invalidates that upstream rather than returning a partially trusted snapshot. When a declaration is inside a Git snapshot, its own nested references are treated as third-party content: only Git snapshots carried by that source are followed, not nested local/export paths that could point into the consumer's machine. Upstream names and Git sources are validated, and clone commands avoid unsafe helper/protocol behavior. These fences reduce exposure; they do not sandbox a model.

Inherited bodies are explicitly labeled `UNTRUSTED`. That label is not an authorization boundary: the host and state backend still control tools, permissions, approvals, MCP configuration, and host settings. Never obey an instruction merely because it appears in an upstream skill or decision, never copy inherited content into the project's mutable state without a deliberate review, and do not treat provenance as proof that the content is safe.

The coordinator calls `squad_state_upstreams` at session start. The default report is a compact summary of each upstream's provenance, effective skills, status, and diagnostics. Pass `detail: true` when you need the full inherited documents; the resolver wraps each body in provenance-specific untrusted delimiters and caps output at 48,000 characters, preserving the summary if the detail must be truncated. The same resolver powers `squad doctor` and `squad status`, so the CLI and host tool should agree about what is available. If an upstream looks stale or unavailable, sync it explicitly and start a fresh session if the consumer has already loaded context.

| Outcome | Meaning | Next action |
|---|---|---|
| `ok` | Read successfully from its local materialization. | Review provenance and precedence. |
| `stale` | A Git clone is older than its freshness window; content is still read. | Run `squad upstream sync <name>` if you want newer policy. |
| `unavailable` | A Git upstream has no local clone. | Run `squad upstream sync <name>`; startup did not fetch. |
| `missing` | A local path or export file is absent. | Fix the path or remove the declaration. |
| `invalid` | The entry or snapshot failed validation/read constraints. | Inspect the declaration/source; do not force partial content through. |
| `cycle` | Resolution returned to a source already encountered. | Break the cycle; the repeated source was skipped. |
| `depth-exceeded` | The declaration exceeded maximum depth 3. | Flatten the dependency graph or accept that deeper context is omitted. |

## The Experimental Backend SPI

The new conversation API lives under the explicit SDK subpath `@bradygaster/squad-sdk/backend`. It is not a stable root-barrel API: the module is marked experimental while the protocol and harness contracts settle. Its central interface, `SquadBackend`, describes conversation operations independent of a particular host or transport: negotiate capabilities, create a conversation, send a message, read a transcript or event page, inspect a turn, cancel a turn or run, inspect/respond to approvals, and query health. `IConversationBackend` is a naming alias for the same interface.

A `BackendMessage` has a stable `runId` and monotonically increasing `seq`, role/content, optional typed content `parts`, optional correlation and causation IDs, optional `epoch`, target `harness`, and namespaced `extensions`. The `(runId, seq)` pair is the idempotency key. Typed parts distinguish text, data, resources, tool calls, and tool results while `content` remains a plain-text rendering. Extension properties must use `x-<harness>.*`; `validateExtensions` checks the namespace and, if supplied, the harness's allowlist.

The portable protocol separates the control stream from the execution stream. Control covers admission, lifecycle, approvals, routing, leases, and transcript projection; execution carries task claims, worker progress, tool activity, artifacts, checkpoints, and harness output. A backend may carry both, but each envelope keeps its stream, protocol, IDs, event sequence, cursor, correlation/causation, timestamp, and payload explicit. Delivery is at-least-once, so consumers deduplicate by stable event ID/sequence and clients use opaque cursors rather than parsing cursor contents.

The SDK currently provides these building blocks:

| API | Role | Important constraint |
|---|---|---|
| `SquadBackend` | Canonical conversation contract. | Backend and host speak the same versioned semantics, even if they use different transports. |
| `LocalSquadBackend` | In-process conversation broker with file-backed snapshots by default. | Conversation state is persisted as JSON below `.squad/backend/conversations/`, with lock files below `.squad/backend/locks/`; a supplied store can redirect persistence. |
| `DurableHttpSquadBackend` | HTTP client for a DurableSquad-compatible `/v1/conversations` service. | Requires an explicit `baseUrl`; accepts HTTPS, or plain HTTP only for `localhost`, `127.0.0.1`, or `::1`. Optional bearer token is passed separately, never embedded in the URL. |
| `createStateBackendStore` | Adapts the existing SDK `StateBackend` read/write/exists/list contract to the backend's store interface. | Also coordinates per-key conversation locks; for backends that store data outside the working tree, use a stable lock anchor such as the team `.squad` root. |
| `HarnessAdapter` | SPI for an execution runtime. | Adapter implements `submit`, `subscribe`, `cancel`, `respondApproval`, and `describe`; submissions and side effects must be idempotent. |
| `DefaultHarnessRegistry` | Stores in-process adapters by ID. | Rejects malformed IDs and duplicate registrations; `list()` returns descriptors. |
| `ClaudeAgentSdkHarness` | Runs admitted turns on the Claude Agent SDK (ID `claude-agent-sdk`). | Needs the optional peer `@anthropic-ai/claude-agent-sdk` and an API credential. |
| `CopilotSdkHarness` | Runs admitted turns on `@github/copilot-sdk` (ID `copilot-sdk`). | Needs a signed-in Copilot user; opt-in on the MCP bridge. |
| `TurnHarness`, `TurnApprovals` | Shared turn lifecycle and approval queue under both harnesses. | Exported so a custom harness can reuse them. |

`LocalSquadBackend` is a conversation engine, not a built-in model runner. Its event and transcript store supports whichever harness is registered; with none registered, it only records. `DurableHttpSquadBackend` likewise ships only the outbound HTTP client; it does not provision the service to which it connects. The URL validator rejects credentials embedded in the URL, uses `redirect: 'error'` so a bearer token is not replayed to a different origin, and bounds requests with timeouts and retry behavior. A token is optional, but a production endpoint must enforce its own authentication and authorization policy.

`createStateBackendStore` is the seam between the new conversation snapshots and the existing state backend. When local conversation storage uses the default file store, the snapshots live beneath the Squad state directory; for a configured state backend, the adapter routes reads/writes through that backend and establishes deterministic machine-local lock coordination. In a linked worktree or remote state arrangement, the lock identity must correspond to shared storage/ref identity, not merely an arbitrary caller's current directory. These locks protect concurrent read/modify/write of one conversation; they are not a claim that the in-process MCP bridge becomes a distributed scheduler.

A `HarnessAdapter` is the execution piece. Its `submit` receives a conversation/run/sequence and messages; it emits event envelopes through `subscribe`, and implements cancellation and approval responses. It must deduplicate repeated submissions by conversation and `(runId, seq)` (or the stable `operationId`) and preserve the epoch fencing context when publishing results. Implementations should advertise only capabilities they actually support and constrain extension namespaces to their own `x-<harness>` names. Register the adapter with `DefaultHarnessRegistry` and inject that registry into `createSquadBackend`. The experimental MCP command can register the two bundled harnesses (next section), but it has no CLI mechanism for loading arbitrary adapter code.

### The two experimental harnesses

> **Preview:** Both harnesses, and the whole `@bradygaster/squad-sdk/backend` subpath (`BACKEND_CONTRACT_STAGE = 'experimental'`), are experimental in v2.0.0. Their options and behavior are not stable guarantees.

Squad 2.0.0 ships the first real `HarnessAdapter` implementations, in `packages/squad-sdk/src/backend/harnesses/`. Both extend `TurnHarness`, which gives them one turn lifecycle, and both route approvals through `TurnApprovals`, one shared queue.

The shared lifecycle handles the awkward cases. Concurrent deliveries of the same operation share one acceptance, and a failed start forgets it so a retry runs. A run is registered before its runtime starts, so a cancel that arrives during startup is kept and the turn never reaches the model. `cancel` acknowledges once the stop is requested, and the conversation's next turn waits until the interrupt has finished, so late events from an aborted turn are never attributed to the next one. With a state directory, accepted deliveries and each conversation's runtime session ID survive a restart: a redelivered turn does not run twice, and the next turn resumes the session.

Approvals are bound to a hash. Each request carries a SHA-256 of the canonical action, requests are offered one at a time (the broker holds one pending approval per turn), and a deny ends the turn. The broker's approval record holds only a short redacted summary and the hash, never the tool input. Redaction masks credentials but never shell syntax, so an approver still sees what would run. Pending approvals live in process memory: if the harness restarts, cancel the broker's record and resume.

| | `claude-agent-sdk` | `copilot-sdk` |
|---|---|---|
| Runtime | One Claude Agent SDK `query()` per turn, resuming the conversation's session | One Copilot session per conversation, created on the first turn and resumed by ID |
| Approval hook | `canUseTool`; `approvalId` is the tool-use ID, the hash covers the tool name and input | `onPermissionRequest`; approve answers `approve-once`, deny answers `reject` and aborts the turn |
| Permission isolation | `permissionMode: 'default'` and `settingSources: []`, so no repository or user allow rule approves a call the broker never sees; `permissions.deny` rules are kept as `disallowedTools` | A harness-only Copilot config directory, so approvals remembered in your own Copilot CLI do not apply |
| Credentials | An API credential (`ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, or Bedrock, Vertex or Foundry settings), never a claude.ai login | A signed-in Copilot user |
| On the MCP bridge | Registered by default when the optional SDK resolves **and** a credential is configured | Registered only when `SQUAD_BACKEND_HARNESSES` lists `copilot-sdk` |

Claude Code still runs some read-only commands, such as `echo`, without calling `canUseTool`, so those never reach the broker; anything that writes does. The matrix's live run log records a denied `touch` that was not run (2026-11-10). Both harnesses run turns in the worktree-aware repository root, so a linked worktree's turns edit that worktree even when its squad state resolves to the main checkout.

On the bridge, `SQUAD_BACKEND_HARNESSES` is a comma-separated list of harness IDs, or `none`. It defaults to `claude-agent-sdk`. `copilot-sdk` is never registered by default: its SDK is always installed with the CLI, so a default registration would make every experimental bridge run Copilot sessions. Harness state goes to `.squad/backend/harnesses/` on the `local` backend, and to a per-user cache (`~/.cache/squad/harnesses/<hash>/`) on a backend that keeps its data outside the working tree.

### The 11 Opt-In `squad_backend_*` Tools

The backend MCP tool family is not part of the default `squad state-mcp` surface. It appears only when the process receives `--experimental-backend` or `SQUAD_EXPERIMENTAL_BACKEND=1`. Setting `SQUAD_BACKEND_URL` alone does **not** enable it, which prevents an incidental URL environment variable from routing traffic or a bearer token anywhere. Once the gate is enabled, the bridge selects `durable-http` if `SQUAD_BACKEND_URL` is set (and passes `SQUAD_BACKEND_TOKEN` if present); otherwise it creates the in-process MCP backend over the project's configured state backend.

| Tool | Parameters | Purpose |
|---|---|---|
| `squad_backend_create_conversation` | Optional `conversationId`, `title`, `metadata`. | Creates a conversation or idempotently reopens the requested ID. |
| `squad_backend_send_message` | Required `conversationId`, `runId`, `seq`; optional `role`, `content`, `parts`, `correlationId`, `causationId`, `epoch`, `harness`, `extensions`. | Submits a message; requires `content` or non-empty typed `parts`; the pair `(runId, seq)` is idempotent. |
| `squad_backend_get_transcript` | Required `conversationId`. | Returns the full conversation transcript. |
| `squad_backend_get_turn` | Required `conversationId`, `seq`. | Returns turn state, tasks, messages, and any pending approval. |
| `squad_backend_cancel_turn` | Required `conversationId`, `seq`; optional `epoch`. | Cancels a turn by sequence. |
| `squad_backend_cancel_run` | Required `conversationId`, `runId`; optional `reason`, `epoch`. | Cancels by stable run identity, distinct from turn sequence. |
| `squad_backend_get_approvals` | Required `conversationId`. | Lists durable approval records, pending or decided. |
| `squad_backend_respond_approval` | Required `conversationId`, `approvalId`, `hash`, `decision` (`approve` or `deny`); optional `reason`, `epoch`. | Responds to an approval by echoing exactly the opaque hash supplied by the harness. |
| `squad_backend_negotiate` | Required `protocols` (string array); optional `clientName`, `contentParts`, `extensionNamespaces`, `capabilities`, `policyCapabilities`. | Negotiates protocol/capability intersection; reports `executionAvailable` based on registered harnesses. |
| `squad_backend_read_events` | Required `conversationId`; optional `after` (opaque cursor), `limit` (positive integer, capped at 500), `stream` (`control` or `execution`). | Reads canonical event envelopes after a cursor, at least once; deduplicate by ID. |
| `squad_backend_health` | None (`{}`). | Reports health, registered harness IDs, and whether execution is available. |

That last field is easy to misread. `executionAvailable` is `true` only when at least one harness is registered. On a typical machine, without the Claude Agent SDK and an API key and without `SQUAD_BACKEND_HARNESSES=copilot-sdk`, the bridge registers none: `squad_backend_health` reports `"harnesses": []` and `executionAvailable: false`, and `squad_backend_send_message` fails with `unavailable` instead of queueing a job that can never run. With `copilot-sdk` listed and a signed-in Copilot user, the same call reports `"harnesses": ["copilot-sdk"]` and `executionAvailable: true`, and a message starts a real Copilot turn. If a custom in-process backend has exactly one registered harness and the caller omits `harness`, it selects that harness; with multiple local harnesses, the caller must name one or receives `invalid-request`. A remote endpoint may implement its own execution behavior, but the client cannot infer it merely from having a URL.

```mermaid
flowchart LR
  G{"Explicit experimental gate?"} -->|"No"| D["Default state and memory tools only"]
  G -->|"Yes"| U{"SQUAD_BACKEND_URL set?"}
  U -->|"No"| L["LocalSquadBackend over configured state"]
  U -->|"Yes"| H["DurableHttpSquadBackend client"]
  L --> T["11 squad_backend_* tools"]
  H --> T
  T --> R{"Harness registered?"}
  R -->|"claude-agent-sdk or copilot-sdk"| X["executionAvailable true"]
  R -->|"None"| N["Transcript and events only"]
```

## Client/Backend Decoupling v0.2 and What Remains Experimental

The `squad-client-backend-decoupling/v0.2` document is a non-normative working draft, not a claim that Squad already has every broker or distributed-execution feature it describes. It gives the three-plane model a concrete SDK contract:

1. **Client plane:** gathers the user's intent, renders the transcript, surfaces approvals, and supplies host-specific affordances.
2. **Control/broker plane:** owns conversation identity, admission ordering, transcript projection, routing, approvals, lease fencing, and authorization.
3. **Execution plane:** runs agent turns, tools, workers, and background continuations.

The client should change without rewriting planner logic, and the execution fabric should change without changing conversation semantics. The broker contract describes resources such as conversations, messages, transcripts, turns, events, approvals, capability negotiation, and operational health. Those are protocol resources, not a requirement that every backend expose the same HTTP routes; MCP, files, and HTTP can project the same stable identifiers and semantics.

Admission uses `(runId, seq)` as an idempotency key. Repeating the same payload is a duplicate admission; reusing the key with a different payload is a conflict. The broker returns the current turn state and an opaque cursor after the admission event. Subsequent harness messages, task changes, approvals, and terminal-state events join the same conversation history. The `runId` identifies the lifecycle to cancel; `seq` orders turns. That split makes cancellation stable even if a host's own turn numbering differs.

Capability negotiation computes the intersection of client capabilities, backend capabilities, and optional policy capabilities. A client cannot gain an ability absent from either backend support or policy permission. Content parts have portable types, and control/execution events remain distinguishable even if one transport multiplexes both. At-least-once delivery means clients deduplicate stable envelope IDs and resume from opaque cursors; if a cursor is not resumable, the event page tells the client to resynchronize from the transcript.

Approvals are durable, versioned resources rather than transient prompt text: version 1 is pending; version 2 is decided. A response must echo the approval ID and the exact `hash` string supplied by the harness. The backend treats that hash as opaque. It does not compute a digest of the approval payload, does not verify its meaning, and the hash itself is not a secret or proof of authorization. Epochs similarly fence stale writers by rejecting lower values, but the draft's epoch is client-asserted rather than issued by a broker with a lease holder and expiry. These caveats are central: the protocol is a useful shape, not a finished security authority.

The spec names the frozen baseline `squad-protocol-v2.0-rc1` and defines nine gates before a backend or adapter can claim compatibility:

| Gate | What the golden trace must prove |
|---|---|
| G1 | A stable `runId` exists independently from turn ordering. |
| G2 | `seq` remains monotonic within a conversation. |
| G3 | Approvals are durable, versioned records and echo the harness-supplied opaque hash. |
| G4 | Effective capabilities equal `client ∩ backend ∩ policy`. |
| G5 | Cursor-based recovery exposes `lastAcceptedSeq` and `resumable`. |
| G6 | Cancellation targets `runId`, not a host-local completion signal. |
| G7 | Operational health stays outside the versioned conversation-resource tree. |
| G8 | `x-<harness>.*` extensions are validated/preserved; unknown event kinds are not yet fully projected loss-tolerantly. |
| G9 | The golden fixtures pass against both local and durable-HTTP backend implementations. |

The reference G1–G9 journey is deliberately lifecycle-focused: admit a message; receive an approval request; disconnect; reconnect with a cursor and recoverability status; resolve the approval; request cancellation by `runId`; observe a terminal cancelled state. Client-side disconnect/reconnect actions themselves are not backend events. The trace checks that the broker's ordered state, rather than a host's local UI, decides whether work is pending, approved, or finished.

Several production-grade guarantees remain explicitly out of scope or pending in v2.0.0. Local conversations are whole-file JSON snapshots rewritten on updates, not an append-only broker log. The cursors are unsigned encodings, approval hashes are harness-supplied, and epochs are cooperative/client-asserted. The two bundled harnesses are experimental, keep pending approvals in process memory, and are the only execution engines Squad ships. The draft records that the Claude harness's original golden-trace smoke run passed on 2026-11-10 but did not prove replay continuity or prompt cancellation; a strengthened live trace still awaits a credentialed run, so that smoke result is not promotion evidence.

> **Preview:** Still experimental in v2.0.0: the `squad_backend_*` tools, both execution harnesses, remote durable-server integration (DurableSquad Phase 2: remote durable approvals and lease-epoch coordination, pending in the tutorial), and promotion of the two v0.2 profiles (§14.4 here, §15.1 in the harness-adapter profile). The CHANGELOG says the Claude harness gives the profiles the non-Copilot host they need, and that promoting them is still pending.

The current package provides the client contract, the outbound client and two experimental harnesses, not the DurableSquad server. Do not describe the bridge as a hosted agent runner, distributed lease service, or completed durable approvals platform.

## Hands-On: Give Tasktrack a Safe State Boundary

Continue with your Tasktrack repository from earlier chapters. These steps assume Squad 2.0.0 is installed and that you opened the Tasktrack workspace in an MCP-capable host. A host may require its own sign-in or license; use Copilot as the fallback because the project-root `.mcp.json` configuration is written for the default Copilot bridge. Do not paste credentials into MCP config or commit machine-specific tokens.

### 1. Verify the bridge before writing

In the host's MCP/tool view, locate the Squad state server and call `squad_state_health` with `{}`. Record the reported runtime version, backend name, storage-provider class, and team directory, and read `resolvedTeamRoot` and `resolvedSquadDir` from the `Health metadata:` line. Confirm the directory is the Tasktrack team's `.squad/` and the backend is the one you expect (`local`, `orphan`, or `two-layer`). If the host shows an older bridge or a different team directory, stop and repair the connection before making a change. While you are here, open `.mcp.json` and check that the `squad_state` entry runs `.squad/squad.mjs` through the `node -e` root finder, and run `squad doctor`: the `portable squad_state launch` check should pass. If it warns about an absolute path, run `squad upgrade` and commit the rewritten files.

### 2. Write a decision through MCP, then test the boundary

From the same host, call `squad_decide` with a real, small Tasktrack decision. For example:

```json
{
  "author": "You",
  "summary": "Keep runtime decisions in the inbox",
  "body": "This chapter records decisions through the state MCP tool so the selected backend owns the write.",
  "references": ["Chapter 21 exercise"]
}
```

Then use `squad_state_list` with `{"dir":"decisions/inbox"}` and `squad_state_read` with the returned file key to verify it was written to the intended inbox. If Tasktrack has an active workstream, `squad_decide` may place it in that workstream's inbox instead; list the active workstream path rather than assuming the root inbox.

Now deliberately attempt a static write with `squad_state_write`, using `{"key":"team.md","content":"This must be rejected."}`. The expected response is a failure/rejection explaining that the key is not mutable state. Do not follow up by editing `team.md` directly. This step demonstrates that the API is enforcing a boundary, not just offering a convenient file writer.

### 3. Add a local `org-standards` source and inspect provenance

Create a small sibling project whose `.squad/` contains reviewed, non-sensitive shared context:

```bash
mkdir -p ../org-standards/.squad/skills/review-basics
cat > ../org-standards/.squad/decisions.md <<'TEXT'
# Shared engineering decisions

Use focused changes and make the relevant test result visible in each hand-off.
TEXT
cat > ../org-standards/.squad/skills/review-basics/SKILL.md <<'TEXT'
---
name: review-basics
description: Shared review checklist
---

Prefer narrow diffs and verify behavior with a targeted test.
TEXT
```

From Tasktrack's repository root, add and validate the source:

```bash
cd ~/tasktrack
squad upstream add ../org-standards --name org-standards
squad upstream list
squad upstream sync org-standards
squad doctor
```

The local `sync` step checks that the source exists; it does not fetch or copy the directory. In your host, call `squad_state_upstreams` with `{"detail":true}`. You should see the skill and decision attributed to `upstream:org-standards@local`, plus any conflict outcome and diagnostics. `squad doctor` and `squad status` should report the same resolution. If you edit the shared local file, the next resolution reads the live local path; for Git upstreams, the consumer sees only the cache refreshed by `squad upstream sync`.

Treat the sample skill and decision as untrusted shared data. In particular, do not add a directive that tries to grant tools or access, and do not assume the `UNTRUSTED` delimiter is a sandbox. If you later add a second upstream with the same skill name, observe that local content wins first, then the earliest declared source, and that the report describes what was overridden.

### 4. Optional: expose the experimental local conversation backend

If you want to inspect the separate backend tool family, modify the Tasktrack `squad_state` MCP entry in `.mcp.json` to add `--experimental-backend` to its args. Keep the existing executable command, config fields, and other MCP servers intact. A typical entry changes its args from `['state-mcp']` to `['state-mcp', '--experimental-backend']`; do not replace the complete `.mcp.json` with a fragment. Alternatively, set `SQUAD_EXPERIMENTAL_BACKEND=1` in the environment of the MCP process. Setting `SQUAD_BACKEND_URL` without the explicit gate does not expose the tools.

Restart/reconnect the MCP server and verify `tools/list` now includes the 11 `squad_backend_*` names (26 tools in all). Call `squad_backend_health` and `squad_backend_negotiate` with a protocol list containing `2.0`. Unless you have installed `@anthropic-ai/claude-agent-sdk` where the CLI can resolve it and set an Anthropic API credential, expect `"harnesses": []` and `executionAvailable: false`. Do not call `squad_backend_send_message` expecting an agent turn: without a registered harness it refuses instead of leaving a job queued forever.

To see a harness register, add `"env": { "SQUAD_BACKEND_HARNESSES": "copilot-sdk" }` to the same entry (or merge the key into its existing `env`) and reconnect. `squad_backend_health` should now list `copilot-sdk` and report `executionAvailable: true`. Stop there unless you mean to run a turn: a message now starts a real Copilot session as your signed-in user, which uses your Copilot quota. Remove the opt-in flag and the variable after exploration if you do not need the experimental interface.

Expected result: you have confirmed the health handshake, recorded and read back a decision through MCP, observed a rejected static write, resolved one local upstream with explicit provenance, and, optionally, seen the local backend report no harness and then register the experimental `copilot-sdk` harness.

## Configuration Reference

| Item | Purpose / accepted values | Default or safety note |
|---|---|---|
| `squad state-mcp` | Starts the stdio MCP server for Squad state and memory tools. | State tools are enabled by default when the server is configured. |
| `--experimental-backend` | Opts into the 11 conversation backend MCP tools. | Not enabled by merely setting a URL. |
| `SQUAD_EXPERIMENTAL_BACKEND` | Set to `1` to enable the experimental tools. | Other values do not enable them. |
| `SQUAD_BACKEND_URL` | Selects the remote durable HTTP backend after experimental tools are enabled. | Explicit HTTPS URL required; plain HTTP only to loopback. |
| `SQUAD_BACKEND_TOKEN` | Optional bearer token for the selected remote endpoint. | Pass separately; never embed in `baseUrl` or commit it. Redirects fail closed. |
| `.mcp.json` → `mcpServers.squad_state` | Project-root bridge command, args, environment, tool restrictions, and Squad metadata. | Squad updates command/args and managed metadata while preserving usable user env/tool fields and other entries. Malformed JSON is not overwritten. |
| `.copilot/mcp-config.json` | Legacy project-level MCP location. | A stale `squad_state` entry is tombstoned during init/upgrade; sibling entries survive. |
| `~/.copilot/mcp-config.json` | User-level MCP config that may contain old per-project hashed entries. | Recognized duplicates are backed up and removed during reconciliation; malformed/unrecognized content is left intact. |
| `.squad/upstream.json` | Ordered source list (`local`, `git`, `export`) with name, source/ref, timestamps. | Project-local declaration; local project state takes precedence over upstream content. |
| `.squad/_upstream_repos/<name>/` | Materialized Git upstream snapshot. | No network fetch during session startup. Refresh with `squad upstream sync [name]`. |
| `squad upstream add <source> [--name <name>] [--ref <branch>]` | Declares a local path, Git source, or export. | Git ref defaults to `main`; failed initial clone leaves config unchanged. |
| `squad upstream sync [name]` | Refreshes a Git cache or validates local/export source paths. | Run explicitly; a stale clone remains readable but is labeled stale. |
| `squad_state_upstreams` | `detail?: boolean`. | Summary by default; full bodies with `detail: true`; output capped at 48,000 characters. |
| `squad_state_write` | `key`, `content`. | Mutable state only; static configuration and charters rejected. |
| `squad_state_create_if_absent` | `key`, `content`. | Atomic create; existing key is a conflict, not an overwrite. |
| `@bradygaster/squad-sdk/backend` | Experimental SDK subpath exporting backend and harness types/implementations. | Not part of stable root SDK API. |
| `DurableHttpSquadBackend.baseUrl` | Explicit API base URL for `/v1/conversations`. | HTTPS or loopback HTTP; URL-embedded username/password rejected. |
| `BACKEND_PROTOCOL_VERSION` | Protocol string negotiated with the backend. | `2.0` in v2.0.0. |
| `SQUAD_BACKEND_HARNESSES` | Comma-separated harness IDs (`claude-agent-sdk`, `copilot-sdk`) or `none`, read by the experimental bridge. | Default `claude-agent-sdk`, registered only when its SDK and an API credential are present; `copilot-sdk` only when listed. |
| `.squad/squad.mjs` | Committed launcher that `.mcp.json`, other hosts' MCP configs and Claude hooks run. | Rewritten by init/upgrade; a file without Squad's marker is left alone. |
| `SQUAD_CLI` | Command or `.js` entry the launcher tries first. | Optional; otherwise project `node_modules`, PATH, then the last CLI that ran init/upgrade. |
| `SQUAD_ALLOW_NPX` | Set to `1` to let the launcher fall back to the exact-version `npx` package. | Off: the launcher fails with install instructions instead of downloading code. |
| `squad_state_health` metadata | `squad-state-health/v1` JSON line with `resolvedTeamRoot`, `resolvedSquadDir`, versions, backend, `launchMode`. | `resolvedTeamDir` is kept for compatibility and holds the team root. |
| `squad_backend_read_events.limit` | Positive integer page size. | Defaults to and is capped at 500. |

## Under the Hood

The state MCP registration and request lifecycle live in `packages/squad-cli/src/cli/commands/state-mcp.ts`. It resolves the project's Squad context, creates a runtime `ToolRegistry` against the effective team state directory, and aliases only the intended state/decision/memory tools. If `--experimental-backend` or the matching environment variable is present, it appends the backend tool list from the MCP adapter. Calls dispatch to the correct registry and normalize string/object results to MCP text content; failures become tool errors rather than silently successful writes. The normal server path uses the MCP SDK's stdio transport, initializes the registry lazily, and closes it on stream/process teardown.

The conversation adapter is implemented in `packages/squad-cli/src/cli/core/backend-mcp.ts`. It performs backend selection, validates each JSON argument type, caps event reads, and converts thrown errors into the canonical backend error envelope. It guards `squad_backend_send_message` before dispatch: no local harness means `unavailable`; omitting the harness with multiple local harnesses means invalid request. It also derives `executionAvailable` from the backend's actual harness registry or negotiated harness list. In v2.0.0 it builds that registry: `createLocalHarnesses` reads `SQUAD_BACKEND_HARNESSES`, registers `ClaudeAgentSdkHarness` only when `isClaudeAgentSdkAvailable()` and `claudeApiCredentialsConfigured()` both hold, registers `CopilotSdkHarness` only when listed, and `harnessStateDir` picks where their durable state goes.

The state-file policy itself belongs to the SDK tool registry. Normalization strips an optional `.squad/` prefix, canonicalizes separators, validates the path, and then checks each mutation against `MUTABLE_STATE_PATHS`. This is why a state key is not an arbitrary filesystem path. The path validator rejects traversal and malformed key segments, while the filesystem conversation store adds root containment and symlink checks. `squad_decide` also writes to an inbox selected from the current workstream context, leaving the shared decision merge to the normal Scribe/governance workflow.

The managed host bridge path is resolved by `packages/squad-cli/src/cli/core/mcp-spec.ts`, which also holds `resolveCommittedSquadStateMcpSpec`, `isMachineSpecificMcpSpec` and `writeSquadRepoLauncher` for the committed launcher (the SDK's `client/adapters/repo-launcher.ts` recognizes it in configs and hooks); `packages/squad-cli/src/cli/core/mcp-probe.ts` performs the version/tools/health handshake; and `packages/squad-cli/src/cli/core/mcp-root.ts` owns project-root registration, stale-entry removal, and user-config reconciliation. Together they make the bridge lifecycle explicit: create or update one rooted config entry, test that the process is the expected version and reports the expected team directory, and remove duplicates without clobbering user-owned sibling configuration.

The upstream implementation is `packages/squad-sdk/src/upstream/resolver.ts`. `resolveUpstreams` reads declarations, walks each source in deterministic order, labels provenance, detects cycles/diamonds and depth overflow, and returns diagnostics instead of aborting the entire resolution. `buildEffectiveUpstreamContext` applies local-first precedence; `formatUpstreamReport` produces both the default tool summary and bounded detail form; `buildSessionDisplay` feeds doctor/status output. The corresponding source contract and exported public types are in `packages/squad-sdk/src/upstream/types.ts` and `packages/squad-sdk/src/upstream/index.ts`.

The existing Git-native persistence contract remains in `packages/squad-sdk/src/state-backend.ts`: `resolveStateBackend` reads `stateBackend` configuration and creates `local`, `orphan`, or `two-layer` implementations (with legacy aliases normalized). `createStateBackendStore` in the experimental backend package adapts that interface for conversations. It adds lock coordination, but it does not turn a state backend into a registered worker. The public experimental exports are grouped in `packages/squad-sdk/src/backend`; the key components are `SquadBackend`, `LocalSquadBackend`, `DurableHttpSquadBackend`, the state-store adapter, the harness registry, and the harnesses.

The harness implementations live in `packages/squad-sdk/src/backend/harnesses`: `turn-harness.ts` (the shared lifecycle), `approval-queue.ts` (`TurnApprovals`, `canonicalApprovalHash`, redaction), `harness-state.ts` (accepted deliveries and session IDs across restarts), `claude-agent-sdk.ts` and `copilot-sdk.ts`. The Claude harness's credential check is short enough to show:

```ts
export function claudeApiCredentialsConfigured(env = process.env): boolean {
  const on = (v: string | undefined) => v === '1' || v?.toLowerCase() === 'true';
  return !!(env['ANTHROPIC_API_KEY'] || env['ANTHROPIC_AUTH_TOKEN'] ||
    on(env['CLAUDE_CODE_USE_BEDROCK']) || on(env['CLAUDE_CODE_USE_VERTEX']) ||
    on(env['CLAUDE_CODE_USE_FOUNDRY']));
}
```

Without one of these, the Agent SDK would fall back to a saved claude.ai login, which the harness must not use, so the bridge does not register it. `@anthropic-ai/claude-agent-sdk` is an optional peer dependency, so `isClaudeAgentSdkAvailable()` is the other half of the gate.

> **Under the hood:** The design keeps host translation, state authority, and execution separate. The bridge exposes stable conversation records and event pages whether or not a harness is registered. That is the core decoupling idea; the two experimental harnesses are not evidence that a remote service or production execution plane is deployed.

## Pitfalls and Troubleshooting

- **The host lists no state tools.** Verify that its configured command/args start `squad state-mcp`, that its working directory is Tasktrack, and that it loaded the project-root `.mcp.json`. Restart the host after configuration changes. Doctor's probe checks `tools/list` and then health.
- **Health reports a surprising version or team directory.** Stop before any write. Compare the runtime version to the coordinator stamp and check which `.squad/` root was resolved; correct the MCP entry/workspace rather than writing to an unexpected team.
- **A state write is rejected.** Check the target is mutable runtime state and that its key is relative to the intended `.squad/`. Do not use the state tools for `team.md`, `routing.md`, `config.json`, charters, templates, skills, or casting registry/history files. Use the supported static team or casting workflow.
- **A directory read fails.** `squad_state_read` reads a file. Use `squad_state_list` for directories such as `agents` or `decisions/inbox`.
- **The backend tools do not appear.** The server must be launched with `--experimental-backend` or `SQUAD_EXPERIMENTAL_BACKEND=1`; setting only `SQUAD_BACKEND_URL` is intentionally insufficient.
- **Message sending returns `unavailable`.** No harness is registered. Check `squad_backend_health`: the Claude harness needs both its optional SDK and an API credential (a claude.ai login does not count), and `copilot-sdk` must be listed in `SQUAD_BACKEND_HARNESSES`. `SQUAD_BACKEND_HARNESSES=none` turns both off. Otherwise use the transcript/event tools, or register a harness in your own SDK integration; do not interpret this as a temporary queue.
- **A harness approval vanished after a restart.** Pending approvals live in the harness process. Cancel the broker's pending record and resume the session.
- **`squad_state` fails with "Cannot find module" or "no Squad CLI found".** Run `squad upgrade` once to rewrite `.mcp.json` with the root finder and the current `.squad/squad.mjs`, and commit both. Make sure the machine has a Squad CLI the launcher can find (`SQUAD_CLI`, project `node_modules`, or `squad` on PATH), or set `SQUAD_ALLOW_NPX=1` deliberately.
- **`squad doctor` fails `portable squad_state launch`.** A committed config names a path on one machine, or a launcher that is missing. `squad upgrade`, then commit.
- **A `baseUrl` is refused.** Use explicit HTTPS for a remote server or HTTP on loopback only. Remove embedded credentials and set `SQUAD_BACKEND_TOKEN` separately. Redirects are rejected intentionally.
- **An upstream is `unavailable` or `stale`.** Run `squad upstream sync <name>` explicitly. Startup never fetches; stale content may still be read, but the report tells you that it is stale.
- **An upstream conflict is unexpected.** Check local skill names first, then the order in `.squad/upstream.json`; earlier sources precede later ones, depth-first. Reorder with remove/add only after reviewing the effective context.
- **An upstream is `invalid`, `cycle`, or `depth-exceeded`.** Read the diagnostic. Fix malformed declarations or graph structure; do not assume the resolver partially applied the unsafe snapshot.
- **The project has two `squad_state` MCP entries.** Init/upgrade migrates the project bridge to `.mcp.json` and may remove recognized stale entries. Review the `.squad-backup` before discarding it; do not manually delete unrelated MCP servers.
- **Two processes contend on the backend.** Locks coordinate individual conversation writes, but they do not provide distributed execution or a global scheduler. The remote service still needs its own durable locking, authorization, idempotency, and failover implementation.

## Summary

`state-mcp` is the governed, versioned boundary for Squad runtime state. Its default tools separate mutable decisions, histories, logs, and governed memory from static team configuration. The state backend health tool tells you which runtime and root you are using; the mutation allowlist rejects attempts to change static files through the state API. MCP setup is rooted and lifecycle-aware: installation preserves user configuration, committed configs run the portable `.squad/squad.mjs` launcher, cleanup removes stale duplicates safely, and doctor probes the actual server and flags machine-specific launch commands. Governed memory is one store for the CLI and MCP tools, locked across processes and migrated transactionally between backends.

Runtime upstreams are explicit, local snapshots. Sessions do not fetch. Local content wins, then declared upstream order wins depth-first, with depth capped at three. Cycles, missing sources, and invalid snapshots are reported as soft failures, and inherited material retains `upstream:<name>@<ref>` provenance. The experimental conversation SPI under `@bradygaster/squad-sdk/backend` gives local, MCP, and HTTP transports one contract, while `HarnessAdapter` is where execution is supplied. Two experimental harnesses ship, `claude-agent-sdk` and `copilot-sdk`, and the bridge registers them only when their SDK and credentials are present (Claude) or when you list them (Copilot); otherwise it is transcript-only. Remote durable-server integration and profile promotion remain experimental.

## Exercises

1. **Audit the boundary.** Use the host tool list to classify each default tool from this chapter as reading, writing, governance, or diagnostics. Call `squad_state_health`, then attempt a write to `routing.md`. Explain why the refusal is a feature rather than an MCP error.
2. **Map precedence.** Create two local upstreams that offer the same skill name, declare them in a known order, and add a local copy. Resolve the report. Record the winning source, losing sources, and their provenance tags. Then remove the local copy and observe the first upstream win.
3. **Exercise soft failures.** Declare a local path that does not exist and a Git source that has not been synced. Use doctor and `squad_state_upstreams` to compare diagnostics. Sync the Git source and explain what changes in the next report.
4. **Read the SPI contract.** Sketch a minimal `HarnessAdapter` that supports cancellation but not approvals. List which capability flags it should advertise, how it deduplicates a submission, and why the state MCP bridge must not claim it can execute that submission. Then name what `TurnHarness` and `TurnApprovals` would give you for free if you built on them.
5. **Check portability.** In a scratch clone of Tasktrack, replace the `squad_state` command in `.mcp.json` with an absolute path to your CLI's `cli-entry.js`, run `squad doctor`, and record the `portable squad_state launch` result. Restore it with `squad upgrade` and explain why the committed form survives a clone on another machine.

## Quiz

1. What are the required arguments to `squad_decide`, and where does it write a decision?
2. Why should a host call `squad_state_health` before mutating state?
3. Which wins when a local skill and two upstream skills share the same name? What ordering applies to nested sources?
4. Does `squad upstream sync` mean that every session startup fetches the latest remote? Explain the actual boundary.
5. What explicit setting exposes `squad_backend_*` tools, and why is `SQUAD_BACKEND_URL` alone insufficient?
6. What must a `HarnessAdapter` implement, which two harnesses ship in v2.0.0, and what does the MCP bridge report when none is registered?
7. Name two limitations that prevent treating the v0.2 protocol draft as a finished security/production contract.
8. In what order does `.squad/squad.mjs` look for a Squad CLI, and when does it use `npx`?

## Further Reading

- [Squad Client and Backend Decoupling v0.2](https://github.com/github/squad/blob/v2.0.0/docs/specification/client-backend-decoupling-v0.2.md)
- [Durable Backend and Custom Harness Tutorial](https://github.com/github/squad/blob/v2.0.0/docs/tutorials/durable-backend-and-custom-harness.md)
- [Upstream Inheritance](https://github.github.com/squad/docs/features/upstream-inheritance/)
- [External State Storage](https://github.github.com/squad/docs/features/external-state/)
- [State Backends](https://github.github.com/squad/docs/features/state-backends/)
