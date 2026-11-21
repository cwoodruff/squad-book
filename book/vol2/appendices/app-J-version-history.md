# Appendix J: Squad Version History

This timeline summarizes major release milestones from `CHANGELOG.md` and the published release notes. Dates are CHANGELOG release dates; npm publication can be a day or more later. Patch notes contain many more fixes than fit in an appendix; use the original sources for full details. Squad has evolved quickly, so verify all commands and features against the release you install.

| Version | Milestone |
|---|---|
| `v0.1.0`–`v0.4.x` | Initial team and coordinator concepts grew into reusable roles, routing, workflows, and a more complete issue-driven development loop. See the historical release sections for incremental changes. |
| `v0.5.0` | The state-directory rename release moved the canonical team state from legacy `.ai-team/` toward `.squad/`, with migration compatibility. |
| `v0.6.0` | TypeScript replatforming established the current package-based CLI/SDK architecture and introduced breaking changes called out in release notes. |
| `v0.8.x` | Major expansion in state backends, integrations, documentation, and enterprise/ADO support; this series also included watch and workflow enhancements. |
| `v0.9.0` | Feature-focused release line, including newer orchestration and operational capabilities. `v0.9.1` and `v0.8.2` contain follow-up stabilization. |
| `v1.0.0` (2026-10-02) | Stable 1.0 release; establishes a stable release series and consolidates the package/runtime surface. |
| `v1.0.1` (2026-10-03) | First 1.0 patch/stability update. |
| `v1.1.0` (2026-10-19) | The first edition's target. Adds provenance-aware model resolution and quality-first/balanced/economy profiles; improves live model fallback, casting and build watch; adds state-profile and create-if-absent work; records backend-aware usage and context utilization; tightens workflow ownership, release and review governance, state migrations, portable MCP setup, remote-root doctor validation, and Windows reliability. |

## v1.1.0 detail

The `v1.1.0` changelog's additions include a central model resolver with source precedence, fallback behavior, and lifecycle telemetry; named model profiles and model-availability handling; `squad cast --name ... --role ...` and `squad hire`; live `squad build --watch`; an explicit unsupported-provider response for a Copilot memory provider; a draft charter conformance profile and validation/serialization support; atomic `createIfAbsent` across state backends; backend-aware JSONL usage records and structured `squad cost` reports; context-window utilization events, warnings, and OpenTelemetry metrics.

Notable changes/fixes include safer human-triggered promotion for protected main branches, deterministic and sole issue-assignment workflow behavior, clearer monitor-only Ralph and human merge authority, supported roster parsing, preservation of user-authored `.github/copilot-instructions.md` outside Squad-managed markers, migration of casting state with backups and conflict checks, portable MCP server configuration, linked-team root resolution, Windows filesystem fixes, and `squad doctor` checks against the actual remote team root. These notes describe the tagged release, not guarantees that every feature is enabled by default.

## Versioning guidance

- Use the tag or package version when checking command syntax; the standalone `squad` version and SDK package may be independently installed.
- `squad upgrade` updates managed coordinator/templates but is designed to preserve `.squad/` and legacy `.ai-team/` team state.
- Review release notes before upgrading if you use SDK builders, state backends, labels, workflows, or experimental model profiles.
- Features marked experimental in v2.0.0 (the `/backend` subpath, its harnesses and the `squad_backend_*` tools) are not stable guarantees; defaults can change independently of the team's persisted configuration.
- The `latest` channel follows stable releases; `preview` and `insider` carry prereleases; see Chapter 2 (Volume 1).

For the maintained timeline, see [What's New](https://github.github.com/squad/docs/whatsnew/). Detailed changes are in [`CHANGELOG.md`](https://github.com/github/squad/blob/v2.0.0/CHANGELOG.md). Historical technical context is recorded in the [Squad blog](https://github.github.com/squad/blog/), including [the TypeScript replatform](https://github.com/github/squad/blob/v2.0.0/docs/src/content/blog/013-the-replatform-begins.md), [version alignment](https://github.com/github/squad/blob/v2.0.0/docs/src/content/blog/017-version-alignment.md), [adapter architecture](https://github.com/github/squad/blob/v2.0.0/docs/src/content/blog/018-the-adapter-chronicles.md), [remote mode](https://github.com/github/squad/blob/v2.0.0/docs/src/content/blog/019-shaynes-remote-mode.md), [migration](https://github.com/github/squad/blob/v2.0.0/docs/src/content/blog/021-the-migration.md), [SubSquads](https://github.com/github/squad/blob/v2.0.0/docs/src/content/blog/023-subsquads-horizontal-scaling.md), [state backends](https://github.com/github/squad/blob/v2.0.0/docs/src/content/blog/031-state-backends.md), and [1.0 stabilization](https://github.com/github/squad/blob/v2.0.0/docs/src/content/blog/032-v010-stabilisation-insider.md).

## Squad 2.0 Version History

| Version | Date | Milestone |
|---|---|---|
| `v2.0.0-preview.1` | 2026-10-23 | First Squad 2.0 preview on the npm `insider` channel (`preview` alias); introduced seven host projections, shared client adapters and capability negotiation, optional experimental backend contracts, runtime upstream inheritance with earlier-wins precedence, and removed personal Squad / consult / `--global` behavior. `latest` stayed on v1.1.0. |
| `v2.0.0-preview.2` | 2026-10-25 | Upgrade-safety and bridge-reliability preview: content-aware upgrades with verified backups and dry-run support, safer self-upgrade/downgrade handling, improved state-bridge lifecycle and health reporting, optional built-in roster management, compatibility fixes, and upstream/runtime reliability improvements. |
| `v2.0.0-preview.3` | 2026-10-29 | Added ADR-002 work claims (`squad watch --claims git-ref`, off by default); a malformed `.squad/config.json` now stops `watch`; `squad memory` and the `memory.*` tools share one backend-aware governed store; `squad cost` is scoped to the newest shell session; 0.9.x casting registries migrate; standalone archives vendor Node.js 22.23.4. |
| `v2.0.0-preview.4` | 2026-11-09 | Completed the move to `github/squad` and the `github.github.com/squad` docs; governed memory migrates transactionally to `orphan` and `two-layer`, and `.squad/casting/` stays on the source branch; versioned runtime and backend metadata in health reports; `squad doctor` exits non-zero on failure; customized `squad-ci` workflows survive upgrade. |
| `v2.0.0` | 2026-11-18 | **This book's target.** Stable Squad 2.0 on npm `latest`, including all four previews. Adds Claude Code as a first-class host and the first execution harnesses, makes the six non-Copilot coordinators self-contained (ADR-003), and commits a portable `.squad/squad.mjs` launcher. |

## v2.0.0 detail

The `v2.0.0` changelog groups its Claude Code work under one heading (#2438). It adds the Squad plugin for Claude Code (`claude plugin install squad@squad`) and a plugin mode for the projection (`--claude-plugin`); member subagents generated from charters, with the `X-squad-host-claude` charter extension; native skills, with Init Mode, Ralph, ceremonies, GitHub Issues and PRD modes loaded on demand from `squad-coordinator-*` skills; opt-in advisory hooks with the new `squad lockout` and `squad hook` commands; the local `squad dashboard`; a Claude Code runner for `squad watch --execute` (`--agent-preset claude`); and the experimental `ClaudeAgentSdkHarness` and `CopilotSdkHarness`. The Claude projection is now version 3, and `squad client sync` refreshes configured hosts without a full upgrade.

Notable changes and fixes: the Claude, Kiro, OpenCode, Cursor, Codex and Antigravity coordinators no longer defer to Copilot's `.github/agents/squad.agent.md` (ADR-003 option C), while Copilot's output is unchanged; committed files no longer contain machine paths, because `squad_state` now launches through `.squad/squad.mjs` (run `squad upgrade` once on an existing repository); Squad adds a scoped Claude Code permission allowlist; the non-Copilot coordinators run the reviewer gate, wait for a human sign-off, send user decisions to Scribe, and stop when `squad_state` is unavailable on a non-local backend; health output adds `resolvedTeamRoot` and `resolvedSquadDir`. Remote durable-server integration and v0.2 profile promotion remain experimental, and the historical upgrade-matrix attestations stay tied to the preview versions they tested. The `[Unreleased]` section is empty at the tag. Chapter 22 is the migration guide from 1.x.
