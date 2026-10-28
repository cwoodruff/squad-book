# Tasktrack: companion project for *Mastering Squad*

Tasktrack is a deliberately small task-tracking app (`api/` is a dependency-free TypeScript REST API built on `node:http`, and `web/` is a static front end). It has no npm dependencies: Node.js 22.18+ runs the `.ts` files directly through built-in type stripping, and tests use `node:test`. Your Squad will grow it throughout the book. This folder is the **starting point** for Volume 1, Chapters 2–4 (`ch02-start`).

## Use it
```bash
cp -r sample ~/tasktrack && cd ~/tasktrack
git init && git add . && git commit -m "Tasktrack starter"
npm test        # node --test
npm start       # API on http://localhost:3000
```
Open `web/index.html` in a browser to use the UI.

## Chapter progression
Each volume numbers its chapters from 1.

| Volume, chapters | What your Squad adds |
|---|---|
| Vol. 1, 1–4 | Install Squad, `squad init`, first session, cast the team (backend, frontend, tester, reviewer) |
| Vol. 1, 5–6 | Routing rules for `api/` vs `web/`, parallel work in worktrees |
| Vol. 1, 7–10 | GitHub issues + labels, the Ralph loop, a PRD for "due dates and tags" |
| Vol. 1, 11–14 | Copilot coding agent hand-off, model/cost tuning, notifications, upgrades |
| Vol. 1, 15–19 | Decisions, memory, a "tasktrack-api-conventions" skill, ceremonies, review gates |
| Vol. 2, 1–5 | An MCP server, a state backend, a second squad for `web/`, export/import |
| Vol. 2, 6–10 | Security hardening, container image, CI workflow, OpenTelemetry, a DR drill |
| Vol. 2, 14–16 | An SDK-based tool, a plugin, and hooks |
| Vol. 2, 18–22 | Optional Squad 2.0 preview evaluation in a scratch copy |
| Vol. 2, 24 | Capstone: end-to-end delivery to production |

As you go, tag your own repo `chNN-start` / `chNN-end` (Volume 1) and `v2-chNN-start` / `v2-chNN-end` (Volume 2) so you can compare against the book.
