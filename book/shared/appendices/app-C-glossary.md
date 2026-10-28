# Appendix C: Glossary

This glossary uses concise, practical definitions for the terms used throughout this book. Squad's published glossary is the cross-reference for official vocabulary: https://bradygaster.github.io/squad/docs/reference/glossary/.

**Activation** — The point at which a reviewed plan or work item becomes authorized for execution.

**Agent** — A role-focused AI worker with its own charter, task context, and optional persistent history.

**Agent charter** — The Markdown role description that states an agent's identity, expertise, responsibilities, boundaries, and collaboration expectations.

**Agentic workflow** — A GitHub-hosted workflow that invokes AI-enabled automation against repository work under explicit workflow permissions.

**Artifact** — A durable Squad file or record, such as a charter, routing policy, decision, configuration, or execution log.

**Backend** — The implementation that stores and retrieves Squad state; examples include local files, Git notes, orphan branches, and two-layer storage.

**Budget** — A configured bound or policy for model spending or token use.

**Casting** — Selecting and recording the people-like agent identities that make up a project's working team.

**Ceremony** — A repeatable team activity, such as planning or retrospective, with a trigger and expected outputs.

**Charter** — See *Agent charter*.

**Client** — The Copilot surface (CLI, VS Code, or another host) whose tools and execution behavior shape how Squad can work.

**Coordinator** — The agent prompt and runtime behavior that interprets requests, applies routing, delegates tasks, and integrates results.

**Cross-Squad** — Discovery and work delegation between separately configured Squad teams.

**Decision** — A durable choice and its rationale, normally captured in `.squad/decisions.md` or an inbox proposal.

**Directive** — An enduring instruction or constraint for the team, commonly recorded alongside shared decisions.

**Discovery** — Locating Squad teams or capabilities, through project path resolution or registry/upstream metadata.

**Economy mode** — A model-selection preference that favors lower-cost available models while respecting configured capability constraints.

**Externalized state** — Team state stored outside the repository working tree and resolved using project identity/configuration.

**Fact Checker** — The built-in review role that verifies factual claims and records evidence under its policy.

**Fallback chain** — An ordered list of model alternatives or behavior choices used when the preferred option is unavailable.

**Fleet** — A dispatch mode that coordinates parallel agents across independent work units.

**History** — Agent-specific record of completed work and learnings, usually in `.squad/agents/{name}/history.md`.

**Human-in-the-loop** — A governance principle in which people retain authority over decisions that require approval, release, or merge.

**Identity provenance** — Information explaining how a cast identity was selected, assigned, or changed.

**Inbox** — A staging location for proposed decisions or memory that has not yet been accepted into canonical team state.

**Issue-driven development** — A work pattern in which GitHub/GitLab issues are the durable work queue and labels or assignments drive triage.

**Label** — A GitHub issue/PR marker used as workflow state, such as `squad:backend` or `priority:p1`.

**Local backend** — State persisted in the project's ordinary local files or checkout.

**Memory** — The persistent, governed context available to a team across tasks, including decisions, histories, identity, and classified knowledge.

**MCP (Model Context Protocol)** — A protocol for exposing tools and resources to an AI client; Squad's state MCP server presents runtime state operations.

**Model profile** — A named policy that selects model tiers or fallbacks for work quality, speed, or cost.

**Orphan branch backend** — A Git-backed state strategy that stores Squad data on a branch without ordinary project history.

**Parallel fan-out** — Delegating independent parts of a request to multiple agents at once.

**Personal Squad** — A user-level set of ambient agents and configuration available beyond one project team.

**Preset** — A curated, reusable group of agent roles or defaults that can be applied to a project.

**Ralph** — Squad's work monitor, which scans and reports actionable work and can dispatch work when explicitly configured.

**Rai** — A governance/review role that checks required evidence and policy gates.

**Registry** — A list of peer squads or cast identities used for discovery and routing.

**Remote team root** — A separate directory/repository containing the canonical team state linked to a working project.

**Response mode** — A coordinator effort/ceremony tier (Direct, Lightweight, Standard, or Full) that controls how much orchestration a task receives.

**Routing** — The policy that maps requests, capabilities, labels, or work types to an agent or response mode.

**Scribe** — The built-in session logger that captures durable outcomes and helps merge proposed decisions.

**SDK** — The `@bradygaster/squad-sdk` package for defining, loading, and integrating Squad programmatically.

**Skill** — A reusable instruction and procedure, usually stored as `SKILL.md`, loaded when a matching task needs it.

**Spawn** — Starting a delegated agent with an assigned prompt and execution context.

**Squad** — A human-directed AI development team whose roles, policies, and shared knowledge are maintained as repository-friendly artifacts.

**Squad state** — The team's configuration and durable records, generally rooted in `.squad/` or a configured external location.

**State key** — A typed/namespaced identifier for one record exposed through the state facade or backend.

**State provider** — An implementation behind a state API that stores and returns entities or artifacts.

**Streams / SubSquads** — Separate workstreams or team instances used to divide a larger project into independently scoped efforts.

**Tasktrack** — The book's small companion REST API and static front end, used for hands-on progression.

**Team** — The roster and working structure recorded in `.squad/team.md`.

**Team root** — The directory Squad resolves as authoritative for team state.

**Telemetry** — Structured runtime events and measurements, including usage, duration, and context metrics.

**Tiered memory** — Organizing stored information by scope, trust, and retrieval need instead of treating all context as equally authoritative.

**Two-layer backend** — A strategy that combines a working state view with durable Git-backed storage/replication.

**Upstream** — A configured source Squad whose templates, skills, or information may be synchronized into another team.

**Worktree** — An isolated Git working directory linked to a shared repository, useful for parallel agent changes.

**Workflow** — A GitHub Actions definition or repeated Squad process that automates part of the development lifecycle.

## Squad 2.0 (Preview) Terms

> **Preview:** These definitions describe Squad `v2.0.0-preview.2` and its seven-host client model; terminology and contracts may change before 2.0.0 is stable.

**Host** — The AI application or runtime in which Squad's coordinator runs, such as Copilot CLI, Claude Code, Kiro, OpenCode, Cursor, Codex, or Antigravity.

**Client slug** — A portable, canonical host identifier stored in `.squad/config.json` `clients[]`, such as `claude` or `codex`. It is not a credential, local path, URL, or session ID.

**Host projection** — A set of host-native project files that gives a host its Squad coordinator instructions and state-MCP connection. Projection merges managed content with user files rather than equating one host with one independent team.

**Client adapter** — An API boundary that describes a host's client capabilities and translates host interaction into the shared backend contract. It does not own portable conversation semantics.

**Capability token** — A named, negotiable ability (for example `subagents`, `approvals`, or `background-runs`). Effective support is constrained by the intersection of client, backend, and policy capabilities.

**`squad_state` MCP server** — The project-local Model Context Protocol bridge that exposes Squad state tools to configured hosts. Experimental `squad_backend_*` conversation tools require explicit opt-in and do not include an execution harness.

**Static configuration** — Team-authoritative project files such as `team.md`, `routing.md`, `.squad/config.json`, and agent charters. In 2.0 these are edited in the workspace, not through mutable-state MCP writes.

**Mutable state** — Runtime records that state tools can read or update under their state contract. It is distinct from static roster, routing, configuration, and charter files.

**Upstream provenance** — The source label attached to inherited content, formatted `upstream:<name>@<ref>`, so a skill, decision, routing rule, or casting policy retains its origin.

**Insider channel** — The npm prerelease distribution tag used for Squad 2.0 previews. `preview` is its compatibility alias; `latest` remains on v1.1.0 until 2.0 stable.

**`SquadBackend`** — The experimental SDK contract for conversation state, messages, events, approvals, capabilities, and turn/run lifecycle across local, MCP, or durable HTTP transports.

**`HarnessAdapter`** — The experimental contract that connects the shared broker/backend to a host execution capability. It is separate from the client-facing `ClientAdapter`; the preview MCP bridge does not bundle a harness.

**Golden trace** — A versioned, deterministic protocol fixture used to check backend behavior against a common sequence of conversation events and expected outcomes. The preview backend is checked against the `squad-protocol-v2.0-rc1` trace gates.

**Host capability matrix** — The reference that records support and validation separately for each feature/host pair. A supported entry is not necessarily backed by a live run.

**Personal Squad** — **Removed in 2.0.** The 1.x user-profile team and ambient agent layer is no longer read or managed. Copy retained material into a project `.squad/` manually.

**Consult mode** — **Removed in 2.0.** The personal-Squad session and its extraction workflow are not part of the preview CLI or SDK.
