# Preface {.unnumbered}

Most of us met AI coding assistants as a single, helpful voice: a pair programmer that completes a line, explains an error, or drafts a function. Squad asks a different question. What if, instead of one assistant, you had a *team*? A lead who plans, a backend developer and a frontend developer who build, a tester who breaks things, a reviewer who says "not yet," and a scribe who remembers what everyone decided last week. And what if that team lived inside your repository, versioned alongside your code, and got better the longer it worked with you?

That's what Squad is. It's a coordination system built on GitHub Copilot that turns a repository into the home of a persistent, specialized group of AI agents. The team's charters, routing rules, decisions, histories, and skills are plain files in a `.squad/` directory. You can read them, edit them, review them in pull requests, and carry them from project to project.

*Mastering Squad* is a two-volume series that teaches Squad from first principles to production operations. It's deliberately deep. Beyond showing you which command to type, it explains *why* Squad behaves the way it does. It takes you under the hood into the coordinator prompt, the SDK, and the formal specification, so that when something surprising happens you can reason about it instead of guessing.

## Who This Book Is For {.unnumbered}

This book is for developers who are **new to Squad** and want to become **expert** users. You should be comfortable with:

- Git and GitHub (branches, pull requests, issues)
- A terminal on macOS, Linux, or Windows
- Basic use of GitHub Copilot in the CLI or VS Code
- Reading TypeScript or JavaScript (for the SDK and extension chapters)

You don't need prior experience with multi-agent systems, MCP, Kubernetes, or OpenTelemetry. Each of those is introduced when it first matters.

## The Two Volumes {.unnumbered}

The series is split by what you are doing with Squad. **Volume 1: Using Squad** (this book) takes you from installation to confident daily use, teaches your team to learn, and shows how to adopt Squad in your own situation. **Volume 2: Operating and Extending Squad** covers advanced coordination, production operations, internals and extension, the Squad 2.0 preview, and mastery.

| Part | Title | Chapters | Volume |
|---|---|---|---|
| I | Getting Started | 1–4 | 1 |
| II | Working with Squad Daily | 5–14 | 1 |
| III | Making Teams Smarter | 15–19 | 1 |
| IV | Adopting Squad | 20–21 | 1 |
| I | Advanced Coordination | 1–5 | 2 |
| II | Production Operations | 6–10 | 2 |
| III | Internals and Extension | 11–17 | 2 |
| IV | Looking Ahead: Squad 2.0 (Preview) | 18–22 | 2 |
| V | Mastery | 23–25 | 2 |

Each volume numbers its parts and chapters from 1: Volume 1 holds Parts I–IV (Chapters 1–21) and Volume 2 holds Parts I–V (Chapters 1–25). A part or chapter reference without a volume means one in the same volume; when a reference points into the other volume, it says so, for example "Chapter 12 (Volume 2)" or "Volume 2, Part IV". Appendices A–D and F appear in both volumes; Appendix E (Quiz Answers) is generated per volume; Appendices G–J (SDK API, Feature Matrix, Specification Cheat Sheet, Version History) appear only in Volume 2.

## Which Squad Should I Use? {.unnumbered}

Short version: install **Squad v1.1.0** (npm tag `latest`) for everything except Volume 2, Part IV. Use **v2.0.0-preview.2** (the `insider` tag, with `preview` as an alias) only for Volume 2, Part IV, which covers the multi-client preview and may change before a stable release. Chapter 2 has the full explanation of channels, install methods, and how to switch between them.

## Reading Paths {.unnumbered}

You do not have to read straight through. Pick the path that matches your goal.

- **Beginner.** Read Part I, then Part II in order, then choose from Part III as your team needs them (memory first, then skills and governance).
- **Daily user.** If you already have a squad running, skim Chapters 1–4, then work through Part II and Part III, and keep Chapters 20–21 handy for your situation.
- **Operator.** Finish Volume 1 Parts I–II, then move to Volume 2, Parts I and II (Chapters 1–10): state, cross-squad coordination, security, containers, CI/CD, observability, and disaster recovery.
- **Builder or extender.** After Part II, read Volume 2, Part III (Chapters 11–17) together with Appendix G (Volume 2), the SDK API quick reference.
- **Squad 2.0 evaluator.** Read Chapters 1–3, then jump to Volume 2, Part IV (Chapters 18–22).

## Tasktrack Progress Map {.unnumbered}

Your Squad builds Tasktrack as you read. This table shows roughly what the sample project gains as you move through Volume 1.

| Chapters | What Tasktrack gains |
|---|---|
| 1–3 | Starter copied, `squad init` run, first annotated session |
| 4 | A cast team with charters and roles |
| 5–6 | Routing rules and parallel work across agents |
| 7–10 | Issues, labels, the Ralph loop, PRD-driven streams |
| 11–14 | Coding agent hand-off, model and cost settings, notifications, a safe upgrade |
| 15–19 | Memory, skills, directives, ceremonies, and error-recovery habits |
| 20–21 | Variations of the project for common adoption scenarios |

Volume 2 continues the progression: MCP, state backends, a second squad, hardening, a container, CI, telemetry, SDK tools, and the capstone in Chapter 24 (Volume 2).

## How Each Chapter Works {.unnumbered}

Every chapter opens with a **Prerequisites** callout naming the chapters you genuinely need, then follows the same shape:

1. **What You'll Learn**: the objectives.
2. **Concepts**: an in-depth explanation with diagrams.
3. **Hands-On**: a step you take with the companion project.
4. **Configuration Reference**: the files, keys, and flags involved.
5. **Under the Hood**: how the chapter's pinned Squad version implements the feature (v1.1.0, except Volume 2, Part IV, which uses v2.0.0-preview.2).
6. **Pitfalls and Troubleshooting**
7. **Summary**, **Exercises**, and a **Quiz** (answers in Appendix E)
8. **Further Reading**: links to the official documentation pages the chapter covers.

Part I (Chapters 1–4) uses a lighter template: Configuration Reference and Under the Hood are optional there so you can get started quickly.

## The Companion Project: Tasktrack {.unnumbered}

Throughout the book, your Squad will build **Tasktrack**, a small task-tracking application with a TypeScript REST API and a static web front end. The starter lives in the `sample/` folder of the book's repository. It has no npm dependencies: Node.js 22.18 or later runs the TypeScript directly, and the tests use the built-in `node:test` runner.

```bash
cp -r sample ~/tasktrack && cd ~/tasktrack
git init && git add . && git commit -m "Tasktrack starter"
npm test
```

Each Hands-On section moves Tasktrack forward. Tag your own repository `chNN-start` and `chNN-end` as you go so you can compare your progress with the book. The starter and its README are in the `sample/` folder of the book's repository.

## Conventions {.unnumbered}

- `monospace` marks commands, file names, configuration keys, and code.
- Shell commands assume a POSIX shell. Windows PowerShell differences are called out where they matter.

> **Note:** Background or clarification.

> **Tip:** A shortcut or best practice.

> **Warning:** Something that can lose work, leak secrets, or cost money.

> **Preview:** A feature that wasn't in the stable v1.1.0 release when this book was written.

## Versions {.unnumbered}

All parts except Volume 2, Part IV target **Squad v1.1.0** (`latest`). Volume 2, Part IV targets **Squad v2.0.0-preview.2** (`insider`, with `preview` as an alias) and focuses on multi-client support. The 2.0 material is preview-only and may change before a stable release. When you see a difference between the book and your installed version, check `squad --version`, the official docs at <https://bradygaster.github.io/squad/>, and Appendix J (Volume 2), Version History.

## Acknowledgments {.unnumbered}

Thanks to Brady Gaster and the Squad contributors for building Squad in the open, documenting it generously, and releasing it under the MIT License.
