# Squad Team

> squad-book

## Coordinator

| Name | Role | Notes |
|------|------|-------|
| Squad | Coordinator | Routes work, enforces handoffs and reviewer gates. |

## Members

| Name | Role | Charter | Status |
|------|------|---------|--------|
| Arthur | Lead Editor | `.squad/agents/arthur/charter.md` | ✅ Active |
| Ford | Technical Writer | `.squad/agents/ford/charter.md` | ✅ Active |
| Trillian | SDK Technical Writer | `.squad/agents/trillian/charter.md` | ✅ Active |
| Slartibartfast | Build Engineer | `.squad/agents/slartibartfast/charter.md` | ✅ Active |
| Marvin | Test Engineer | `.squad/agents/marvin/charter.md` | ✅ Active |


## Built-in Support Agents

| Name | Role | Charter | Status |
|------|------|---------|--------|
| Scribe | Decision Merger | `.squad/agents/scribe/charter.md` | 📋 Silent |
| Ralph | Work Monitor | `.squad/agents/ralph/charter.md` | 🔄 Monitor |
| Rai | RAI Reviewer | `.squad/agents/rai/charter.md` | 🛡️ RAI |
| Fact Checker | Devil's Advocate & Verification Agent | `.squad/agents/fact-checker/charter.md` | 🔍 Verifier |

## Coding Agent

<!-- copilot-auto-assign: false -->

| Name | Role | Charter | Status |
|------|------|---------|--------|
| @copilot | Coding Agent | — | 🤖 Coding Agent |

### Capabilities

**🟢 Good fit — auto-route when enabled:**
- Bug fixes with clear reproduction steps
- Test coverage (adding missing tests, fixing flaky tests)
- Lint/format fixes and code style cleanup
- Dependency updates and version bumps
- Small isolated features with clear specs
- Boilerplate/scaffolding generation
- Documentation fixes and README updates

**🟡 Needs review — route to @copilot but flag for squad member PR review:**
- Medium features with clear specs and acceptance criteria
- Refactoring with existing test coverage
- API endpoint additions following established patterns
- Migration scripts with well-defined schemas

**🔴 Not suitable — route to squad member instead:**
- Architecture decisions and system design
- Multi-system integration requiring coordination
- Ambiguous requirements needing clarification
- Security-critical changes (auth, encryption, access control)
- Performance-critical paths requiring benchmarking
- Changes requiring cross-team discussion

## Project Context

- **Project:** squad-book
- **Created:** 2026-11-20
- **Purpose (inferred):** *Mastering Squad*, a two-volume technical book (Markdown → Pandoc EPUB), with the Tasktrack companion sample (Node.js 22.18+).
- **Universe:** The Hitchhiker's Guide to the Galaxy.
