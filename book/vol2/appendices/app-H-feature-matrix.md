# Appendix H: Host and Client Feature Matrix

Squad's feature behavior depends on both the host (where the agent runs) and the Copilot client (which tools and agent runtime it exposes). The CLI is the most fully controllable host; VS Code supports useful parallel work with different orchestration mechanics. The matrix follows `templates/client-compatibility-reference.md` and the v1.1.0 client-compatibility documentation. “Unknown” means not verified, not a promise of support.

| Capability | Copilot CLI | VS Code Copilot | GitHub Copilot coding agent / github.com | JetBrains Copilot | SDK / embedded runtime |
|---|---|---|---|---|---|
| Discover Squad coordinator | `.github/agents/squad.agent.md` auto-discovered; run `copilot --agent squad` | Custom agent discovered in workspace `.github/agents/` | Coding agent can consume repository instructions and Squad workflows; full subagent coordinator path is surface-dependent | Copilot plugin exists; Squad spawning not validated | No interactive coordinator discovery; embed SDK/runtime explicitly |
| Spawn specialist agents | `task` tool; full `agent_type`, `mode`, `model`, prompt control | `runSubagent` or named `agent`; parameters reduced | Native sub-agent spawning unavailable/limited in documented compatibility table | Limited or unverified | SDK programmatic APIs depend on the embedding host's agent adapter |
| Parallel fan-out | Background tasks, retrieve with `read_agent` | Launch multiple in one turn; they run concurrently but return synchronously together | Not available as CLI-equivalent task fan-out | Untested | Caller/runtime coordinates concurrency |
| Fire-and-forget/background | Yes, via background task mode | No true fire-and-forget; parallel group blocks for result | Not available in the matrix | Untested | Host-defined |
| Per-spawn model | Dynamic; user override, charter, task selection, default/fallback | Session model in Phase 1; custom-agent frontmatter is static/experimental in docs | Not equivalent to dynamic task parameter | Untested | Model selection APIs/config can be embedded; no automatic host guarantee |
| Custom agent type | Full task agent-type choices | Custom agents / subagent capability | Restricted | Limited | Adapter-dependent |
| Workspace file access | CLI filesystem access; project state available | Workspace-scoped; write approval may be requested | Repository-context access; access boundaries controlled by GitHub host | Workspace support exists but Squad behavior unverified | Host adapter controls filesystem/provider access |
| `.squad/` team state | Full read/write according to tool permissions | Workspace read/write; file changes may require approval | Repository data/instructions can be consumed; autonomous write lifecycle follows GitHub host | Untested | State APIs/providers give explicit programmatic access |
| SQL orchestration tool | Available in Copilot CLI harness | Not available | Not available | Not available | Not a portable SDK promise |
| MCP | Full with configured servers | Available when configured/inherited | Limited by host and workflow context | Limited/uncertain | MCP integrations are available only when embedding enables them |
| Web/search and terminal | CLI tools available by harness | Fetch, terminal and code search available | GitHub-specific interfaces; no general CLI guarantee | Plugin-dependent | Caller-provided |
| GitHub issue workflows/Ralph | Full when credentials and `gh` are available | Can participate with configured GitHub tools; avoid CLI-only SQL assumptions | Actions, labels, and coding-agent assignment are natural integration points | Not verified | SDK exposes Ralph/issue-related modules; requires integrations/providers |
| Recommended use | Primary surface for setup, model control, SQL, and asynchronous orchestration | Daily development when session-model constraints are acceptable | Repository-bound issue implementation, workflow automations, and `@copilot` assignment | Treat as experimental until tested | Build an application or integrate Squad runtime rather than use as an editor surface |

## Surface-specific adaptation

### Copilot CLI

Before spawning, detect the CLI's `task` capability. It supports explicit agent type, model, execution mode, and description. A typical coordinator may start several independent tasks as background work, provide a launch summary, then collect each result. The `sql` tool is CLI-specific; workflows that track todos or run batches through SQL must have a filesystem-based fallback before they can be called cross-platform.

### VS Code

Use `runSubagent` or `agent` with the full prompt but omit CLI-only `agent_type`, `mode`, and per-spawn `model` controls. For concurrency, launch the whole group in one turn. Results are returned synchronously; do not poll with CLI's `read_agent`. The same turn may run multiple subagents concurrently, but there is no fire-and-forget equivalent. Batch Scribe last because it cannot be detached. Workspace trust and write approvals apply; single-root workspaces are the more reliable configuration.

### GitHub coding agent and GitHub.com

Do not treat “Copilot coding agent” as interchangeable with Copilot CLI. The coding agent is issue/PR oriented and integrates with repository policy, `@copilot` assignment, and GitHub Actions. Its availability does not imply the `task` tool, arbitrary subagent spawning, or CLI SQL. GitHub.com Chat is not documented as a general Squad multi-agent host. Use a coding-agent workflow where repository-hosted autonomous implementation is the goal; use CLI/VS Code for full interactive Squad coordination.

### JetBrains and SDK

The compatibility reference marks JetBrains spawning, model selection, and filesystem behavior untested or limited. Avoid relying on undocumented parity. The SDK offers runtime interfaces and builders, but embedding into the SDK does not itself supply Copilot host tools: the caller must provide execution, credentials, state, and any agent client adapter.

## Design rule for portable Squad instructions

1. Detect the available spawn tool; use CLI `task` if available, VS Code `runSubagent` otherwise, and work inline if neither exists.
2. Keep the work description, acceptance criteria, charter, identity, and response-order instructions surface-independent.
3. Keep SQL, fire-and-forget assumptions, per-spawn model choice, and polling behind CLI-only branches.
4. In VS Code, launch all parallel workers in one turn and defer Scribe to the final group.
5. In untested clients, reduce to one inline worker and verify file access before authorizing writes.

For current details and known limitations, consult the source template `templates/client-compatibility-reference.md` and the documented [client compatibility matrix](https://bradygaster.github.io/squad/docs/scenarios/client-compatibility/).

## Squad 2.0 Host Feature Matrix (Preview)

> **Preview:** This summary reflects Squad `v2.0.0-preview.2` across its seven supported host slugs. The matrix is evidence-based and changes as adapters and host runtimes evolve; see the [full host feature matrix](https://bradygaster.github.io/squad/docs/reference/host-feature-matrix/) for its validation details and per-feature records.

The 2.0 adapter standardizes where the coordinator and `squad_state` MCP bridge are projected. It does not make every host's execution runtime identical. The status below summarizes the preview matrix: **✓** supported, **△** degraded/partially supported, **×** unsupported, and **—** not applicable. Validation is a separate axis; a supported claim may be based on static inspection or automated contract tests rather than a live run.

### Shared baseline

| Capability group | Copilot | Claude | Kiro | OpenCode | Cursor | Codex | Antigravity |
|---|---:|---:|---:|---:|---:|---:|---:|
| Project initialization, casting, routing, response modes | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Parallel specialist dispatch | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Skills, shared decisions/history, directives, memory governance | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| State backends, MCP state bridge, export/import, ceremonies | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| 2.0 host projection and capability negotiation | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Experimental conversation backend bridge | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

These shared rows describe a portable contract and projected coordinator instructions, not proof that every host offers the same interface or executes every workflow the same way. All seven hosts advertise subagent dispatch; the details below show where run controls differ.

### Host runtime differences

| Host | Entry point / projected coordinator | Subagents | Background runs | Per-spawn model selection | Important host-specific notes |
|---|---|---:|---:|---:|---|
| GitHub Copilot (`copilot`) | `copilot --agent squad`; canonical `.github/agents/squad.agent.md` | ✓ | ✓ | ✓ | Copilot CLI, VS Code, and app surfaces have distinct mechanics. VS Code, `squad start`/RC, and GitHub Agentic Workflows are Copilot-specific surfaces. |
| Claude Code (`claude`) | `.claude/agents/squad.md`; use `claude --agent squad --mcp-config .mcp.json` | ✓ | ✓ | × | Claude Code does not load project-scoped `.mcp.json` servers until approved; passing the config explicitly is the documented route. |
| Kiro (`kiro`) | `kiro-cli`; `.kiro/agents/squad.json` plus manual steering file | ✓ | × | × | Parallel work is supported, but not the background-run capability in the matrix. |
| OpenCode (`opencode`) | `opencode`; `.opencode/agent/squad.md` | ✓ | ✓ | × | One of the two hosts with a recorded successful live CLI run in the evidence set. |
| Cursor (`cursor`) | `cursor-agent`; `.cursor/agents/squad.md` and `.cursor/rules/squad.mdc` | ✓ | × | × | The live smoke run was blocked by a usage limit; host-independent tests and static projection evidence remain separate evidence. |
| OpenAI Codex (`codex`) | `codex`; `.codex/agents/squad.toml` plus `AGENTS.md` pointer | ✓ | × | × | The Codex CLI was not present on the reference machine, so its matrix evidence is static and test-based rather than a live run. |
| Google Antigravity (`antigravity`) | `agy`; `.agents/agents/squad.md` | ✓ | × | × | Subagents do not inherit the MCP connection in this preview's matrix. |

### Preview gaps and degraded paths

| Capability | Matrix result |
|---|---|
| Background agent runs | Supported on Copilot, Claude Code, and OpenCode; degraded on Kiro, Cursor, Codex, and Antigravity. Use a foreground or synchronous hand-off where the host cannot continue work in the background. |
| Ralph CLI workflows | Supported on Copilot; degraded on the other six hosts. The command-line monitor remains distinct from coordinator-level issue triage. |
| Per-agent model, reasoning, and context-tier selection | Unsupported across all seven projected coordinator digests in this preview. Do not infer this capability from a host's general model picker. |
| Marketplace plugin browsing on cast; GitLab and Azure DevOps issue tracking; monorepo team-root and dual-root remote resolution | Unsupported across all seven hosts in the matrix snapshot. The host adapters do not fill these documented digest or platform gaps. |
| Copilot RC/start and GitHub Agentic Workflows | Copilot-only; not applicable to the other six host slugs. |
| Live validation | Recorded passing live CLI evidence exists for Claude Code and OpenCode only (2026-10-22). Other hosts rely on automated tests, static inspection, or have a blocked/untested live attempt. |

The source matrix reports 45 supported, 0 degraded, and 6 unsupported feature rows for Copilot; the corresponding supported/degraded/unsupported counts are 41/1/6 for Claude, 40/2/6 for Kiro, 41/1/6 for OpenCode, 40/2/6 for Cursor, 40/2/6 for Codex, and 39/3/6 for Antigravity. These counts describe the source's full feature inventory, not the smaller grouped tables above. Chapter 20 explains how projections and capability negotiation work; Chapter 19 covers the user-facing host workflows.
