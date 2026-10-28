# Appendix D: Sample Prompts

The prompts here are original starting points inspired by the themes of Squad's published prompt examples. Replace the bracketed details with your repository's real constraints. A good prompt states the goal, current context, scope, acceptance evidence, and boundaries; it does not ask the team to “do everything” without a decision point.

## Small, bounded builds

### API slice

```text
In this repository, implement [one API capability]. First inspect the existing structure and tests; do not introduce dependencies unless the current stack cannot meet the requirements. Acceptance criteria: [list observable behavior]. Add focused tests, run them, and report files changed plus test output. Ask before changing public API contracts or data persistence.
```

### CLI utility

```text
Build a small [language] command-line tool that [purpose]. It needs [flags/defaults], must handle [error cases], and should write no files outside [allowed location]. Let one specialist design behavior and another independently review the test plan; implement only after agreeing on the interface. Finish with a runnable example and exact validation command.
```

## Existing codebase work

### Safe bug fix

```text
Investigate [bug] in this repo. Reproduce it with the narrowest existing test or a minimal test case before editing. Trace the behavior through the current implementation, make the smallest fix, and add a regression assertion that would fail on the old behavior. Preserve unrelated work and do not refactor neighboring code. Report any uncertainty separately from verified facts.
```

### Architecture proposal first

```text
We need [system change] because [reason]. Do not implement yet. Have an architect map the current design and propose two viable approaches with trade-offs; ask a reviewer to challenge failure modes, migration impact, and rollback. Present a short decision record with evidence and the unanswered question that blocks implementation.
```

### Dependency upgrade

```text
Upgrade [package/tool] from [current] to [target]. Check the official migration notes and repository call sites. Separate mechanical edits from behavior changes, preserve lockfile conventions, run targeted tests plus the project's build, and list any deprecations still present. Do not silently widen version ranges.
```

## Parallel collaboration

### Independent feature slices

```text
Implement [feature] with acceptance criteria: [criteria]. Divide work only along independent file/API boundaries: [slice A] and [slice B]. Agree on shared types first, avoid concurrent edits to the same files, and have one integration owner resolve conflicts and run the complete focused test set. Do not merge or publish without my approval.
```

### Review without implementation

```text
Review the current diff for correctness and contract regressions only. Do not edit files. Check [specific invariants], test coverage, edge cases, and compatibility. Return findings ordered by severity with file/line evidence; if there are no actionable defects, say so and list what you did not verify.
```

## GitHub issue and PR work

### Triage queue

```text
Review open issues labeled [label] and classify each as actionable, needs clarification, duplicate, or blocked. For actionable items, recommend the best Squad role and explain the evidence. Do not assign, comment, or edit issues yet; first show the proposed changes so I can approve them.
```

### Pull request readiness

```text
Prepare PR #[number] for review. Inspect CI and review threads, fix only issues attributable to this PR, and keep each change covered by a focused test. Do not merge. Summarize unresolved comments, checks, and any behavior that could not be reproduced locally.
```

## Knowledge and team setup

### Cast a team

```text
Set up a Squad for [project and stack]. Propose a small roster with distinct areas, explicit non-responsibilities, and a reviewer who is not the author. Inspect the repository before deciding roles. Show me the cast and routing proposal before writing files; keep the coordinator as the final integration point.
```

### Decision capture

```text
We decided [decision] because [rationale and constraints]. Record it in the project's canonical decision location with date, scope, consequences, and alternatives rejected. Check for an existing conflicting decision first; preserve the earlier record and flag any needed supersession rather than rewriting history.
```

## Continuous work and large change

### Ralph observation-only

```text
Scan the open work for [repo/label] and report the next [N] issues by priority, dependency, and role fit. Do not dispatch agents, change labels, assign issues, or modify files. Identify blocked items and explain why they are not ready.
```

### Decompose a migration

```text
Plan the migration from [old system] to [new system]. Inventory callers, data formats, and deployment risks first. Produce a dependency-aware sequence of small issues with acceptance checks, test strategy, and rollback. Do not start implementation until I approve the sequence; mark unknowns as questions, not assumptions.
```

### SDK extension

```text
Add an SDK extension that [behavior] using the public v1.1.0 API. Before coding, inspect exported types and examples; do not rely on private runtime modules. Include a usage example, API-level tests, and an error-path test. Keep host-specific behavior behind an adapter and state any compatibility limits.
```

## Prompt finishing checklist

Before sending a large request, name the repository and desired outcome; list measurable acceptance criteria; identify files or APIs that must not change; specify whether the team should plan, implement, or only review; separate independent work from dependent decisions; state who may approve labels, merges, and releases; request evidence (tests, commands, source paths) and uncertainties; and choose a stop condition so parallel workers do not expand scope indefinitely.

## Squad 2.0 (Preview): Multi-Host Prompts

> **Preview:** These prompts target Squad `v2.0.0-preview.2`. Host support varies, so each prompt asks Squad to report and respect actual capabilities instead of assuming parity.

### Project the same team to two hosts

```text
In this repository, inspect the existing .squad/ team and its configured clients. Keep the team and charters canonical; add Claude Code and OpenAI Codex projections with `squad client add claude,codex --dry-run` first, then show me the proposed file changes. Do not overwrite user-authored host settings or add credentials. If I approve, apply the projections, verify `squad client list`, and report each host's entry point and any sign-in/licensing prerequisite.
```

### Port a task between host runtimes

```text
Implement [bounded feature] using the shared Squad team in this repository. Before delegating, identify the active host and its available subagent, background-run, MCP, and model-selection capabilities. Keep the task, acceptance criteria, and final report host-neutral; use a synchronous/foreground fallback if this host lacks background runs. Do not claim a capability that the negotiated client/backend/policy set does not include.
```

### Compare a capability before enabling it

```text
Compare the configured Copilot and [second host] projections for this project. Check the generated coordinator and MCP files, then use the Squad 2.0 host feature matrix to identify which of [specific capability] is supported, degraded, unsupported, or merely untested on each. Do not modify either projection. Separate static/test evidence from live-host evidence and list the safest fallback for the unsupported case.
```
