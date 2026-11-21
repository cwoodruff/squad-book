# Part IV — Squad 2.0: One Team, Many Hosts {.unnumbered}

Part IV covers what Squad 2.0 changed and how one team works in more than one AI host. Like the rest of the book, it targets **Squad v2.0.0**. It walks through the changes since 1.x, working in each of the seven supported hosts (GitHub Copilot, Claude Code, Kiro, OpenCode, Cursor, OpenAI Codex and Google Antigravity), how host projection and capability negotiation work, the state boundary and the experimental backend, and how to migrate an existing 1.x squad.

If you use only GitHub Copilot, you can skim this part: plain `squad init` and `squad upgrade` still set up Copilot alone. If you are coming from Squad 1.x, start with Chapter 22. Appendix H is the feature matrix for this part.

- **Chapter 18: Squad 2.0: What Changed and Why** The overview.
- **Chapter 19: Using Squad Across Clients** Working in each supported host, including the Squad plugin for Claude Code.
- **Chapter 20: Host Projections, Client Adapters, and Capability Negotiation** How one team is projected into many hosts.
- **Chapter 21: The State MCP Boundary, Runtime Upstreams, and the Experimental Backend** State in 2.0.
- **Chapter 22: Migrating from Squad 1.x to Squad 2.0** Upgrade paths, rollback and what is still experimental.

**Tasktrack:** your Tasktrack squad already runs on Squad 2.0. In this part you project that same team into more hosts, always with a Copilot-only fallback. Chapter 22's migration drill uses a scratch copy pinned to Squad 1.1.0.
