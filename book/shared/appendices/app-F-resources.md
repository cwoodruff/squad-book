# Appendix F: Further Resources

## Official project

- [Squad repository](https://github.com/github/squad) — source, releases, issues, and contribution history.
- [Latest GitHub release](https://github.com/github/squad/releases/latest) — downloadable builds and release artifacts.
- [Squad documentation site](https://github.github.com/squad/) — installation through advanced reference material.
- [README](https://github.com/github/squad/blob/v2.0.0/README.md) — project overview, installation, and supported workflows for the v2.0.0 tag.
- [Changelog](https://github.com/github/squad/blob/v2.0.0/CHANGELOG.md) — detailed changes associated with releases; v2.0.0 is dated 2026-11-18.

## Documentation by task

- [Installation](https://github.github.com/squad/docs/get-started/installation/) and [comprehensive install guide](https://github.github.com/squad/docs/get-started/install-comprehensive/).
- [Choose an interface](https://github.github.com/squad/docs/get-started/choose-your-interface/) and [choose a path](https://github.github.com/squad/docs/get-started/choosing-your-path/).
- [First session](https://github.github.com/squad/docs/get-started/first-session/) and [first-session tour](https://github.github.com/squad/docs/tour-first-session/).
- [CLI reference](https://github.github.com/squad/docs/reference/cli/), [configuration](https://github.github.com/squad/docs/reference/config/), [SDK reference](https://github.github.com/squad/docs/reference/sdk/), and [API reference](https://github.github.com/squad/docs/reference/api-reference/).
- [Glossary](https://github.github.com/squad/docs/reference/glossary/) and [What's New](https://github.github.com/squad/docs/whatsnew/).
- [Architecture](https://github.github.com/squad/docs/concepts/architecture/), [team](https://github.github.com/squad/docs/concepts/your-team/), [memory and knowledge](https://github.github.com/squad/docs/concepts/memory-and-knowledge/), and [parallel work](https://github.github.com/squad/docs/concepts/parallel-work/).
- [Routing](https://github.github.com/squad/docs/features/routing/), [response modes](https://github.github.com/squad/docs/features/response-modes/), [skills](https://github.github.com/squad/docs/features/skills/), [Ralph](https://github.github.com/squad/docs/features/ralph/), [state backends](https://github.github.com/squad/docs/features/state-backends/), and [plugins](https://github.github.com/squad/docs/features/plugins/).
- [Client compatibility](https://github.github.com/squad/docs/scenarios/client-compatibility/), [existing repo](https://github.github.com/squad/docs/scenarios/existing-repo/), [monorepo](https://github.github.com/squad/docs/scenarios/monorepo/), and [troubleshooting](https://github.github.com/squad/docs/scenarios/troubleshooting/).
- [Specifications index](https://github.com/github/squad/tree/v2.0.0/docs/specification) — profiles, artifact inventory, and maturity guidance.

## Samples and learning material

- [Repository samples](https://github.com/github/squad/tree/v2.0.0/samples) — runnable examples maintained with the source.
- [Published sample prompts](https://github.github.com/squad/docs/guide/sample-prompts/) — prompts illustrating project, workflow, and feature goals.
- [Recipes and cookbook](https://github.github.com/squad/docs/cookbook/recipes/).
- [Tips and tricks](https://github.github.com/squad/docs/guide/tips-and-tricks/).
- [Agent framework integration guide](https://github.github.com/squad/docs/guide/agent-framework-integration/), [autonomous agents](https://github.github.com/squad/docs/guide/build-autonomous-agent/), and [building extensions](https://github.github.com/squad/docs/guide/building-extensions/).
- The book's local `sample/` directory contains Tasktrack, a small Node-based API and static client used in chapter exercises.

## Community and contribution

- [GitHub Discussions](https://github.com/github/squad/discussions) — questions, ideas, and project discussion.
- [GitHub Issues](https://github.com/github/squad/issues) — bug reports and feature requests.
- [Pull requests](https://github.com/github/squad/pulls) — review work in progress.
- [Contributing guide](https://github.github.com/squad/docs/guide/contributing/) — development and submission guidance.
- [Community page](https://github.github.com/squad/docs/community/) — community links, contributors, and events.
- For security issues, follow the private reporting instructions in the repository's [SECURITY.md](https://github.com/github/squad/blob/v2.0.0/SECURITY.md), not a public issue.

## Related tools and platforms

- [GitHub Copilot CLI](https://docs.github.com/en/copilot/github-copilot-in-the-cli) — primary command-line Copilot surface for agent orchestration.
- [GitHub Copilot coding agent](https://docs.github.com/en/copilot/using-github-copilot/coding-agent) — repository/issue-oriented autonomous coding workflow.
- [GitHub CLI (`gh`)](https://cli.github.com/) — issue, pull request, and repository operations used by many Squad workflows.
- [Model Context Protocol](https://modelcontextprotocol.io/) — tool/resource interoperability used by Squad's state bridge and compatible clients.
- [OpenTelemetry](https://opentelemetry.io/) — tracing and metric conventions supported by runtime observability.
- [Git worktrees](https://git-scm.com/docs/git-worktree) — isolation strategy for parallel branches of work.
- [Aspire dashboard](https://learn.microsoft.com/dotnet/aspire/fundamentals/dashboard/overview) — local view of telemetry for Aspire-hosted scenarios.

Always verify a related tool's current installation, licensing, availability, and client support against its own official documentation.

## Squad 2.0 resources

- [Squad `v2.0.0` release](https://github.com/github/squad/releases/tag/v2.0.0) — release notes and artifacts for the stable 2.0 release.
- [Using Squad across clients](https://github.github.com/squad/docs/scenarios/using-squad-across-clients/) — configure multiple host projections around one project team.
- [Squad plugin for Claude Code](https://github.github.com/squad/docs/features/claude-code-plugin/) — install the plugin and choose between plugin mode and the full Claude projection.
- [Host Feature Matrix](https://github.github.com/squad/docs/reference/host-feature-matrix/) — per-host support, limitations, and validation evidence.
- [Squad 2.0 Architecture](https://github.github.com/squad/docs/concepts/squad-2-0-architecture/) — client, control/broker, and execution boundaries.
- [Multi-machine watch with work claims](https://github.github.com/squad/docs/scenarios/multi-machine-watch/) — run `squad watch` on several machines without two watchers taking the same issue.
- [Multi-client quickstart tutorial](https://github.com/github/squad/blob/v2.0.0/docs/tutorials/multi-client-quickstart.md) — a guided multi-host setup.

## Historical (1.1.0)

These links are pinned to the v1.1.0 tag. The first two describe features Squad 2.0 removed, and their pages are gone from the live site. Use them to understand a 1.x project you are migrating; Chapter 22 (Volume 2) covers the migration.

- [Consult mode (v1.1.0)](https://github.com/github/squad/blob/v1.1.0/docs/src/content/docs/features/consult-mode.md) — `squad consult` and `squad extract`.
- [Personal squad (v1.1.0)](https://github.com/github/squad/blob/v1.1.0/docs/src/content/docs/guide/personal-squad.md) — `squad personal` and `squad init --global`.
- [README at v1.1.0](https://github.com/github/squad/blob/v1.1.0/README.md) — the first edition's target release.
