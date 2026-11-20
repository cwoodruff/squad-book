# Work Routing

How to decide who handles what.

## Routing Table

| Work Type | Route To | Examples |
|-----------|----------|----------|
| Editorial direction, structure, chapter manifest, style guide, review gate | Arthur | `research/CHAPTERS.md`, `research/STYLE*.md`, cross-volume consistency, final approval of prose |
| Volume 1 prose (Using Squad, Parts I–IV) and shared appendices A–D, F | Ford | `book/vol1/**`, `book/shared/appendices/**`, quizzes, exercises in `exercises/solutions/vol1/` |
| Volume 2 prose (Operating & Extending, SDK, Squad 2.0 preview) and appendices G–J | Trillian | `book/vol2/**`, `exercises/solutions/vol2/`, SDK/API walkthroughs |
| Build, EPUB, CI, scripts, Mermaid, covers, metadata | Slartibartfast | `Makefile`, `scripts/**`, `.github/workflows/build-epub.yml`, `book/metadata-*.yaml`, `book/images/**`, `styles/` |
| Validation: coverage and link checks, epubcheck, Tasktrack sample, verifying code examples | Marvin | `make coverage`, `research/VALIDATION.md`, `sample/**`, quiz-answer accuracy |

Preset installation adds concrete routes for the configured team. Add or edit rows
here only when their agent names also exist in the casting registry.

## Issue Routing

| Label | Action | Who |
|-------|--------|-----|
| `squad` | Triage: analyze issue, assign `squad:{member}` label | Lead |
| `squad:{name}` | Pick up issue and complete the work | Named member |

### How Issue Assignment Works

1. When a GitHub issue gets the `squad` label, the **Lead** triages it — analyzing content, assigning the right `squad:{member}` label, and commenting with triage notes.
2. When a `squad:{member}` label is applied, that member picks up the issue in their next session.
3. Members can reassign by removing their label and adding another member's label.
4. The `squad` label is the "inbox" — untriaged issues waiting for Lead review.

## Rules

1. **Eager by default** — spawn all agents who could usefully start work, including anticipatory downstream work.
2. **Scribe always runs** after substantial work, always as `mode: "background"`. Never blocks.
3. **Quick facts → coordinator answers directly.** Don't spawn an agent for "what port does the server run on?"
4. **When two agents could handle it**, pick the one whose domain is the primary concern.
5. **"Team, ..." → fan-out.** Spawn all relevant agents in parallel as `mode: "background"`.
6. **Anticipate downstream work.** If a feature is being built, spawn the tester to write test cases from requirements simultaneously.
7. **Issue-labeled work** — when a `squad:{member}` label is applied to an issue, route to that member. The Lead handles all `squad` (base label) triage.

## Work Type → Agent

| Work Type | Primary | Secondary |
|-----------|---------|----------|
| Editorial / structure / review | Arthur | Marvin |
| Volume 1 writing | Ford | Trillian |
| Volume 2 / SDK writing | Trillian | Ford |
| Build & publishing | Slartibartfast | Marvin |
| Validation & sample code | Marvin | Slartibartfast |

## Review Gates

- All prose changes: reviewed by **Arthur** (or the other writer when Arthur authored it).
- Build/script/sample changes: reviewed by **Marvin**; Marvin's own changes reviewed by **Slartibartfast**.
- Technical claims about Squad (commands, APIs, versions): **Fact Checker** verifies against `research/` sources.
