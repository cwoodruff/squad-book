# Links left for writers after the 2.0 URL rewrite

Owner: Slartibartfast (WP-S1). Date: 2026-11-20. Branch `squad-2.0`.

I rewrote URLs mechanically across `book/`, `exercises/` and `sample/`:

- `bradygaster.github.io/squad` became `github.github.com/squad`.
- `github.com/bradygaster/squad` became `github.com/github/squad`.
- `raw.githubusercontent.com/bradygaster/squad` became `raw.githubusercontent.com/github/squad`.

That changed 376 lines. Of 173 pinned `blob/`/`tree/` links, 161 moved to `v2.0.0` because their path exists at that tag. The 12 below stay pinned to their old tag on `github/squad`, because the path does not exist at v2.0.0.

## 1. Links still pinned to an old tag (path removed at v2.0.0)

| File:line | Pinned ref | Path | Suggested action |
|---|---|---|---|
| `book/vol1/part-01/ch02-installation.md:227` | `blob/v1.1.0` | `docs/src/content/docs/guide/personal-squad.md` | Ford: keep as a v1.1.0 history citation, or drop it with the removed-feature prose |
| `book/vol1/part-01/ch02-installation.md:411` | `blob/v1.1.0` | `docs/src/content/docs/guide/personal-squad.md` | Ford: keep as a v1.1.0 history citation, or drop it with the removed-feature prose |
| `book/vol1/part-02/ch05-routing.md:242` | `blob/v1.1.0` | `docs/src/content/docs/features/consult-mode.md` | Ford: keep as history, or drop it with the Consult section |
| `book/vol2/part-01/ch03-cross-squad.md:323` | `blob/v1.1.0` | `packages/squad-sdk/src/multi-squad.ts` | Trillian: keep as history, or drop it (module removed in 2.0) |
| `book/vol2/part-04/ch18-squad-2-overview.md:363` | `blob/v2.0.0-preview.2` | `docs/proposals/squad-2.0-security-and-isolation.md` | Trillian: the proposals directory was deleted before GA. Drop the citation, or keep it as a preview.2 history pin |
| `book/vol2/part-04/ch22-upgrading-to-2.md:531` | `blob/v2.0.0-preview.2` | `docs/proposals/contributor-guide-improvements.md` | Trillian: the proposals directory was deleted before GA. Drop the citation, or keep it as a preview.2 history pin |
| `book/vol2/part-04/ch22-upgrading-to-2.md:532` | `blob/v2.0.0-preview.2` | `docs/proposals/error-recovery.md` | Trillian: the proposals directory was deleted before GA. Drop the citation, or keep it as a preview.2 history pin |
| `book/vol2/part-04/ch22-upgrading-to-2.md:533` | `blob/v2.0.0-preview.2` | `docs/proposals/iterative-retrieval.md` | Trillian: the proposals directory was deleted before GA. Drop the citation, or keep it as a preview.2 history pin |
| `book/vol2/part-04/ch22-upgrading-to-2.md:534` | `blob/v2.0.0-preview.2` | `docs/proposals/memory-governance-provider.md` | Trillian: the proposals directory was deleted before GA. Drop the citation, or keep it as a preview.2 history pin |
| `book/vol2/part-04/ch22-upgrading-to-2.md:535` | `blob/v2.0.0-preview.2` | `docs/proposals/reflect.md` | Trillian: the proposals directory was deleted before GA. Drop the citation, or keep it as a preview.2 history pin |
| `book/vol2/part-04/ch22-upgrading-to-2.md:536` | `blob/v2.0.0-preview.2` | `docs/proposals/retro-enforcement.md` | Trillian: the proposals directory was deleted before GA. Drop the citation, or keep it as a preview.2 history pin |
| `book/vol2/part-04/ch22-upgrading-to-2.md:537` | `blob/v2.0.0-preview.2` | `docs/proposals/tiered-memory.md` | Trillian: the proposals directory was deleted before GA. Drop the citation, or keep it as a preview.2 history pin |

## 2. Other link items that need a writer

| File:line | Item | Owner |
|---|---|---|
| `book/vol1/part-01/ch02-installation.md:227` | Inline link to `https://github.github.com/squad/docs/guide/personal-squad/` returns 404 because the page was removed. It is in prose, so I left it. Delete the "see also" clause when the paragraph is rewritten. (I dropped the matching dead bullet from the Resources list at the end of the chapter.) | Ford |
| `book/shared/appendices/app-F-resources.md:61` | `releases/tag/v2.0.0-preview.2`. I moved it to the new host but kept the tag because the prose describes the preview release. Repoint it to `releases/tag/v2.0.0` when the Preview block is rewritten. | Ford |
| `book/vol1/part-01/ch02-installation.md:90,99,102,143-145,248` | `brew tap bradygaster/squad` and the `bradygaster.Squad*` WinGet IDs are unchanged at v2.0.0 (`D/get-started/installation.md:50`). Leave them. | — |

## 3. Hand-fixed config values (not URLs)

- `book/vol1/part-01/ch02-installation.md:76`: install-script `REPO` default is now `github/squad` (`scripts/install.sh:19`).
- `book/vol2/part-02/ch08-cicd-release.md:62,231`: the `gh aw add` spec is now `github/squad/workflows@…` (`D/guide/gh-aw.md:131`).
- `book/vol2/part-05/ch25-contributing.md:77,82,138`: fork, upstream remote and `--repo` now use `github/squad` (`CONTRIBUTING.md:77,190`).
- `book/shared/appendices/app-A-cli-reference.md:164`: `squad plugin marketplace add github/squad`.
- `book/shared/appendices/app-F-resources.md:7`: the docs root is now `https://github.github.com/squad/` (`/squad/docs/` returns 404).

## 4. Repinned to v2.0.0, but the file changed since the old tag

These links now point at v2.0.0 and resolve. The target file differs from the tag the prose was written against, so re-check any claim the link supports.

| File:line | Old ref | Path |
|---|---|---|
| `book/shared/appendices/app-F-resources.md:8` | `v1.1.0` | `README.md` |
| `book/shared/appendices/app-F-resources.md:9` | `v1.1.0` | `CHANGELOG.md` |
| `book/shared/appendices/app-F-resources.md:21` | `v1.1.0` | `docs/specification` |
| `book/shared/appendices/app-F-resources.md:25` | `v1.1.0` | `samples` |
| `book/vol1/part-01/ch01-what-is-squad.md:217` | `v1.1.0` | `packages/squad-cli/src/cli/core/init.ts` |
| `book/vol1/part-01/ch02-installation.md:14` | `v2.0.0-preview.2` | `docs/src/content/docs/whatsnew.md` |
| `book/vol1/part-01/ch03-first-session.md:71` | `v2.0.0-preview.2` | `docs/src/content/docs/whatsnew.md` |
| `book/vol1/part-02/ch05-routing.md:14` | `v2.0.0-preview.2` | `docs/src/content/docs/whatsnew.md` |
| `book/vol1/part-02/ch07-github-workflow.md:329` | `v1.1.0` | `docs/demo-agentic-sdlc-walkthrough.md` |
| `book/vol1/part-02/ch10-prd-streams-fleet.md:273` | `v1.1.0` | `packages/squad-cli/src/cli/commands/watch/capabilities/fleet-dispatch.ts` |
| `book/vol1/part-02/ch12-models-cost.md:269` | `v1.1.0` | `samples/cost-aware-router` |
| `book/vol1/part-02/ch13-notifications.md:315` | `v1.1.0` | `docs/features/teams-adapter.md` |
| `book/vol1/part-02/ch14-upgrade-cleanup.md:14` | `v2.0.0-preview.2` | `docs/src/content/docs/whatsnew.md` |
| `book/vol1/part-03/ch18-governance.md:310` | `v1.1.0` | `.github/agents/squad.agent.md` |
| `book/vol1/part-03/ch19-error-recovery.md:299` | `v1.1.0` | `packages/squad-cli/src/cli/commands/watch/index.ts` |
| `book/vol1/part-03/ch19-error-recovery.md:300` | `v1.1.0` | `.github/agents/squad.agent.md` |
| `book/vol1/part-04/ch21-scenarios-b.md:308` | `v1.1.0` | `packages/squad-sdk/src/config/init.ts` |
| `book/vol2/appendices/app-I-spec-cheatsheet.md:108` | `v2.0.0-preview.2` | `docs/specification/client-harness-adapters-v0.2.md` |
| `book/vol2/appendices/app-I-spec-cheatsheet.md:109` | `v2.0.0-preview.2` | `docs/specification/client-backend-decoupling-v0.2.md` |
| `book/vol2/appendices/app-J-version-history.md:29` | `v1.1.0` | `CHANGELOG.md` |
| `book/vol2/part-01/ch01-mcp.md:313` | `v1.1.0` | `templates/mcp-config.md` |
| `book/vol2/part-01/ch02-state-backends.md:14` | `v2.0.0-preview.2` | `docs/src/content/docs/whatsnew.md` |
| `book/vol2/part-01/ch02-state-backends.md:298` | `v1.1.0` | `packages/squad-sdk/src/state-backend.ts` |
| `book/vol2/part-01/ch02-state-backends.md:299` | `v1.1.0` | `packages/squad-sdk/src/state` |
| `book/vol2/part-01/ch02-state-backends.md:300` | `v1.1.0` | `packages/squad-sdk/src/storage` |
| `book/vol2/part-01/ch03-cross-squad.md:14` | `v2.0.0-preview.2` | `docs/src/content/docs/whatsnew.md` |
| `book/vol2/part-01/ch03-cross-squad.md:324` | `v1.1.0` | `packages/squad-sdk/src/sharing` |
| `book/vol2/part-01/ch03-cross-squad.md:326` | `v1.1.0` | `packages/squad-sdk/templates/skills/distributed-mesh` |
| `book/vol2/part-01/ch04-portability.md:14` | `v2.0.0-preview.2` | `docs/src/content/docs/whatsnew.md` |
| `book/vol2/part-02/ch07-containers-cloud.md:263` | `v1.1.0` | `packages/squad-sdk/src/ralph/capabilities.ts` |
| `book/vol2/part-02/ch08-cicd-release.md:303` | `v1.1.0` | `workflows/squad-workflows.manifest.json` |
| `book/vol2/part-02/ch08-cicd-release.md:305` | `v1.1.0` | `.github/workflows/squad-ci.yml` |
| `book/vol2/part-02/ch08-cicd-release.md:306` | `v1.1.0` | `.github/workflows/squad-release.yml` |
| `book/vol2/part-02/ch08-cicd-release.md:307` | `v1.1.0` | `.github/workflows/squad-promote.yml` |
| `book/vol2/part-02/ch08-cicd-release.md:308` | `v1.1.0` | `.github/workflows/squad-npm-publish.yml` |
| `book/vol2/part-03/ch11-architecture.md:263` | `v1.1.0` | `docs/README.md` |
| `book/vol2/part-03/ch11-architecture.md:265` | `v1.1.0` | `docs/specification/README.md` |
| `book/vol2/part-03/ch14-sdk.md:14` | `v2.0.0-preview.2` | `docs/src/content/docs/whatsnew.md` |
| `book/vol2/part-03/ch14-sdk.md:484` | `v1.1.0` | `packages/squad-sdk/src/index.ts` |
| `book/vol2/part-03/ch14-sdk.md:485` | `v1.1.0` | `packages/squad-sdk/package.json` |
| `book/vol2/part-03/ch14-sdk.md:490` | `v1.1.0` | `packages/squad-sdk/src/resolution.ts` |
| `book/vol2/part-03/ch14-sdk.md:491` | `v1.1.0` | `packages/squad-sdk/src/agents/lifecycle.ts` |
| `book/vol2/part-03/ch14-sdk.md:492` | `v1.1.0` | `packages/squad-sdk/src/client/index.ts` |
| `book/vol2/part-03/ch14-sdk.md:495` | `v1.1.0` | `samples/hello-squad` |
| `book/vol2/part-03/ch15-plugins-hooks.md:328` | `v1.1.0` | `packages/squad-sdk/src/tools/index.ts` |
| `book/vol2/part-03/ch15-plugins-hooks.md:333` | `v1.1.0` | `samples/plugin-memory-mempalace` |
| `book/vol2/part-03/ch16-autonomous-agents.md:259` | `v1.1.0` | `samples/autonomous-pipeline` |
| `book/vol2/part-03/ch16-autonomous-agents.md:260` | `v1.1.0` | `packages/squad-sdk/src/state-backend.ts` |
| `book/vol2/part-03/ch16-autonomous-agents.md:262` | `v1.1.0` | `src/Squad.Agents.AI/README.md` |
| `book/vol2/part-03/ch16-autonomous-agents.md:263` | `v1.1.0` | `src/Squad.Agents.AI/SquadAgent.cs` |
| `book/vol2/part-03/ch16-autonomous-agents.md:264` | `v1.1.0` | `src/Squad.Agents.AI/SquadAgentOptions.cs` |
| `book/vol2/part-03/ch17-specification.md:255` | `v2.0.0-preview.2` | `docs/specification/client-harness-adapters-v0.2.md` |
| `book/vol2/part-03/ch17-specification.md:255` | `v2.0.0-preview.2` | `docs/specification/client-backend-decoupling-v0.2.md` |
| `book/vol2/part-03/ch17-specification.md:413` | `v1.1.0` | `docs/specification/README.md` |
| `book/vol2/part-03/ch17-specification.md:417` | `v1.1.0` | `docs/specification/charter-v0.1.md` |
| `book/vol2/part-03/ch17-specification.md:422` | `v1.1.0` | `docs/specification/github-work-lifecycle-binding-v0.1.md` |
| `book/vol2/part-04/ch20-host-projections.md:625` | `v2.0.0-preview.2` | `docs/specification/client-harness-adapters-v0.2.md` |
| `book/vol2/part-04/ch21-state-boundary-backend.md:364` | `v2.0.0-preview.2` | `docs/specification/client-backend-decoupling-v0.2.md` |
| `book/vol2/part-05/ch24-capstone.md:393` | `v1.1.0` | `packages/squad-cli/src/cli/` |
| `book/vol2/part-05/ch25-contributing.md:298` | `v1.1.0` | `CONTRIBUTING.md` |
| `book/vol2/part-05/ch25-contributing.md:299` | `v1.1.0` | `.github/workflows/squad-ci.yml` |
| `book/vol2/part-05/ch25-contributing.md:300` | `v1.1.0` | `.github/workflows/squad-release.yml` |
| `book/vol2/part-05/ch25-contributing.md:301` | `v1.1.0` | `.github/workflows/squad-promote.yml` |
| `book/vol2/part-05/ch25-contributing.md:302` | `v1.1.0` | `.github/workflows/squad-insider-publish.yml` |
