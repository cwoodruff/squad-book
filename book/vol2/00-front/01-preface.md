# Preface {.unnumbered}

Volume 1 taught you to *use* Squad. This volume teaches you to *run it well* and to *build on it*. It covers what changes when a squad serves more than one repository, runs unattended, meets a security review, or needs behavior the stock CLI does not provide. It also covers Squad 2.0's biggest change: one team that works through several AI hosts.

## Who This Volume Is For {.unnumbered}

This volume is for developers and platform engineers who already have a working squad, either from **Volume 1** or from equivalent hands-on experience with `squad init`, routing, issues, and the Ralph loop. It also suits readers who want to extend Squad with the SDK, plugins, and hooks, and teams whose members use different AI hosts.

## What Volume 1 Covered {.unnumbered}

Volume 1 (*Using Squad*, Chapters 1–21) took you from installation through your first session, daily workflows with routing, GitHub, Ralph, PRD streams, the coding agent, cost control, and upgrades. It then taught your team to learn through memory, skills, governance, and error recovery, and closed with adoption playbooks for common situations.

- Volume 1, Part I — Getting Started (Chapters 1–4)
- Volume 1, Part II — Working with Squad Daily (Chapters 5–14)
- Volume 1, Part III — Making Teams Smarter (Chapters 15–19)
- Volume 1, Part IV — Adopting Squad (Chapters 20–21)

## How This Volume Is Organized {.unnumbered}

Chapter and part numbering restart at 1 in this volume (Parts I–V, Chapters 1–25). A chapter or part reference without a volume means one in this volume; references into Volume 1 say so, for example "Chapter 5 (Volume 1)".

| Part | Title | Chapters | Volume |
|---|---|---|---|
| I | Advanced Coordination | 1–5 | 2 |
| II | Production Operations | 6–10 | 2 |
| III | Internals and Extension | 11–17 | 2 |
| IV | Squad 2.0: One Team, Many Hosts | 18–22 | 2 |
| V | Mastery | 23–25 | 2 |

Appendices A–D and F are shared with Volume 1; Appendix E collects the quiz answers for this volume; Appendices G–J (SDK API, Feature Matrix, Specification Cheat Sheet, Version History) appear only here.

## Reading Paths {.unnumbered}

- **Operator.** Read Part I (Chapters 1–5), then all of Part II (Chapters 6–10).
- **Builder or extender.** Read Chapter 11 for the architecture, then Part III (Chapters 12–17), keeping Appendix G close at hand.
- **Multi-host teams.** Read Part IV (Chapters 18–22) and Appendix H. Copilot-only readers can skim it.
- **Coming from Squad 1.x.** Start with Chapter 22, Migrating from Squad 1.x to Squad 2.0, then read Chapter 18 for what changed.
- **Finishing the journey.** Read Part V (Chapters 23–25) once the earlier parts are familiar; the capstone brings Tasktrack to production.

## The Companion Project: Tasktrack {.unnumbered}

Tasktrack, the small TypeScript API and static web front end that your squad builds, continues here. This volume adds MCP, a state backend, a second squad, hardening, a container, CI, telemetry, SDK tools, and finally the capstone. If you have not done the Volume 1 exercises, copy the starter from the `sample/` folder of the book's repository and run:

```bash
cp -r sample ~/tasktrack && cd ~/tasktrack
git init && git add . && git commit -m "Tasktrack starter"
npm test
```

Each chapter opens with a **Prerequisites** callout, and its Hands-On section says what state it assumes. Where a step needs something from an earlier chapter, the text tells you how to catch up.

## Conventions {.unnumbered}

- `monospace` marks commands, file names, configuration keys, and code.
- Shell commands assume a POSIX shell.

> **Note:** Background or clarification.

> **Tip:** A shortcut or best practice.

> **Warning:** Something that can lose work, leak secrets, or cost money.

> **Preview:** A feature that is still experimental in Squad v2.0.0.

## Versions {.unnumbered}

The whole book targets **Squad v2.0.0** (`latest`, released 2026-11-18). If your project still runs Squad 1.x, Chapter 22 covers the migration. Chapter 2 (Volume 1) explains how to choose and switch channels. If your installed version differs from the book, check `squad --version`, the official docs at <https://github.github.com/squad/>, and Appendix J, Version History.

## What's New in the Second Edition {.unnumbered}

The first edition was written against Squad v1.1.0, with Part IV describing the 2.0 preview. This edition moves every chapter to Squad v2.0.0. Part IV is rewritten for the stable release as "Squad 2.0: One Team, Many Hosts": the Squad plugin for Claude Code and the full Claude Code projection, the other five hosts, host-neutral coordinators (ADR-003), and the committed `.squad/squad.mjs` launcher. Chapter 22 becomes "Migrating from Squad 1.x to Squad 2.0", with a migration drill on a scratch copy. Earlier parts pick up governed memory, work claims, the experimental execution harnesses and the removal of personal squads; Appendices G–J are updated for v2.0.0. If you still run Squad 1.1, the first edition remains available; it is tagged `book-squad-v1.1.0` in the book's repository.
