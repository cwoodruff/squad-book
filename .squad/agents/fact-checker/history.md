# Project Context

- **Project:** squad-book
- **Created:** 2026-11-20

## Core Context

Agent Fact Checker initialized and ready for work.

## Recent Updates

📌 Team initialized on 2026-11-20

## Learnings

Initial setup complete.

### 2026-11-20 — Fact check of UPDATE-PLAN-2.0.md
- Upstream CHANGELOG dates differ from tag/npm publish dates (2.0.0: 11-18 vs 11-19; preview.3: 10-29 vs 11-01). Check `npm view <pkg> time` before calling a book date wrong.
- A "new in 2.0" claim built from a docs diff needs a code diff too: the `squad cost` table output was already in v1.1.0 code, and only the docs sample changed.
- `github.com/bradygaster/squad` is now a tagless fork: `blob/v1.1.0/...` links there 404. History pins must use `github/squad`.
- The installed CLI's `hook`/`lockout` have no detailed `--help`, so cite source for those.
