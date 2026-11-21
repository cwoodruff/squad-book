# Appendix I: Specification Cheat Sheet

The documents in `docs/specification/` describe profiles and contracts at different maturity levels. They are not a claim that every proposal is fully implemented in v2.0.0; check each document's status and the implementation before depending on a behavior. Where a status line and the v2.0.0 code disagree, the code wins. Each row below is its own compact table, keyed to one source document.

## Squad Specification README

| Scope | Quick use |
|---|---|
| `README.md` establishes the specification's maturity taxonomy, document registry, dependency graph, external references, and versioning policy. | Start here to understand how to interpret the suite and whether a profile is draft, candidate, or stable. In v2.0.0 it also registers the two v0.2 profiles, but it does not list the ADRs, and its implementation column for both v0.2 rows still says no execution harness ships, which the v2.0.0 code contradicts. |

## Artifact Inventory

| Scope | Quick use |
|---|---|
| `artifact-inventory.md` audits artifact/charter conformance, records unstable or non-conforming behavior, describes a promotion roadmap, and sketches a portable export/import bundle. | Use it to compare intended profiles with current artifacts and identify gaps before claiming conformance. |

## Automation Profile v0.1

| Scope | Quick use |
|---|---|
| `automation-v0.1.md` specifies manifests, execution states, triggers/time, candidate operations, retry/concurrency, extension/versioning, and security/privacy. | Consult it when designing scheduled or event-triggered automation; distinguish proposed states from current CLI behavior. |

## Ceremony Profile v0.1

| Scope | Quick use |
|---|---|
| `ceremony-v0.1.md` defines declarations, scheduling boundaries, execution records, state transitions, canonical/compatible behavior, diagnostics, idempotency, and promotion criteria. | A ceremony definition should make its trigger and record explicit; use this profile for interoperability, not as evidence every scheduler is implemented. |

## Charter Profile v0.1

| Scope | Quick use |
|---|---|
| `charter-v0.1.md` standardizes charter purpose/authority, version association, canonical Markdown shape, machine-readable fields, deterministic subset, legacy handling, and extensions. | Validate that role identity, responsibilities, non-responsibilities, collaboration authority, and model metadata are parseable and unambiguous. New in v2.0.0: an optional `## Examples` section (§7.1; a duplicate is diagnostic `SQC011`), placed before the `X-` extension tail. |

## Configuration and Casting Profile v0.1

| Scope | Quick use |
|---|---|
| `configuration-casting-v0.1.md` covers configuration requirements, cast identity/provenance, precedence and joins, transitions, failure semantics, retries, and security. | Use for deterministic casting and resolving competing identity/config sources; preserve provenance instead of silently rewriting identity. |

## Coordination and Handoff Profile v0.1

| Scope | Quick use |
|---|---|
| `coordination-handoff-v0.1.md` defines a handoff envelope, state transitions, delivery/order/idempotency, recovery, extensions, and privacy. | Include enough task state and acceptance evidence for a new worker to continue safely after a handoff. |

## Core Specification v0.1

| Scope | Quick use |
|---|---|
| `core-v0.1.md` establishes terms, root discovery/path containment, artifact classes, profile association/version selection, representation/round-trip rules, diagnostics, publication, and trust boundaries. | Apply as the base contract that other profiles depend on; use containment and trust rules before processing external artifacts. |

## Execution Preferences Profile v0.1

| Scope | Quick use |
|---|---|
| `execution-preferences-v0.1.md` models execution preferences and precedence, resolution states, fallback behavior, diagnostics, idempotency, and privacy. | Resolve user/config/session/charter/task/default preferences deterministically and report when a preference was unavailable or overridden. |

## GitHub Work Lifecycle Binding v0.1

| Scope | Quick use |
|---|---|
| `github-work-lifecycle-binding-v0.1.md` maps lifecycle resources and labels, composes states, defines review/merge authority, revision tokens, stale writes, and provider limits. | Treat GitHub labels and issue/PR states as a provider binding; protect against stale updates and leave merge authority explicit. An ADR-002 amendment maps `work.claim` to a claim ref (`refs/squad/claims/<sha1(work key)>`): a claimed workspace is an unexpired claim ref, and assignees or labels that mirror it are informational only. |

## Governance and Review Profile v0.1

| Scope | Quick use |
|---|---|
| `governance-review-v0.1.md` defines roles, evidence records, review states, blocking verdicts, reviewer independence/lockout, approval, reassignment, and authority. | Preserve independent reviewer identity, evidence, and lockout transitions; never convert a failed gate into implicit approval. |

## Interoperability Conventions v0.1

| Scope | Quick use |
|---|---|
| `interoperability-conventions-v0.1.md` covers capability discovery/claims, stable identity, event/evidence envelopes, retries/replay, privacy, extension ownership, negotiation, and capability classes. | Use when systems exchange Squad artifacts; negotiate what each side actually supports rather than infer capability from a name. |

## Planning and Activation Profile v0.1

| Scope | Quick use |
|---|---|
| `planning-activation-v0.1.md` specifies planning records, transitions, decomposition/acceptance, activation, operations, failure, idempotency, security, and extensions. | Keep “planned” separate from “authorized to execute”; activation requires explicit acceptance and traceable evidence. |

## State and Memory Requirements v0.1

| Scope | Quick use |
|---|---|
| `state-memory-requirements-v0.1.md` sets requirements for authority, memory classification, provisional records, portability, security, and deferred details. | Decide which store owns a fact, how trusted it is, and what must happen before provisional memory becomes canonical. |

## Team and Routing Profile v0.1

| Scope | Quick use |
|---|---|
| `team-routing-v0.1.md` defines roster and routing vocabulary, deterministic rules, candidate operations, failure diagnostics, idempotency, discovery, and authority. | Give each member a stable identity and make rule precedence and tie outcomes predictable. |

## Work Lifecycle Profile v0.1

| Scope | Quick use |
|---|---|
| `work-lifecycle-v0.1.md` models work resources/transitions, dependencies/workspaces, operations, failure, retry/concurrency, versioning, and privacy. | Treat work state as an explicit state machine; track blocked/dependent work and avoid duplicate execution after retries. |

## Squad 2.0 Specifications and Decision Records

These documents arrived with Squad 2.0: three architecture decision records and two v0.2 requirements drafts. Their maturity labels matter: an accepted ADR records a decision, and a draft requirements profile is not a stable, claimable interoperability standard.

> **Preview:** Both v0.2 profiles are still non-claimable requirements drafts in v2.0.0. Their promotion criteria (§15 of the adapter profile, §14 of the decoupling profile) are not yet met, so no adapter or backend can claim conformance to them.

| Specification | Status and scope | Quick use |
|---|---|---|
| [`adr-001-client-control-execution-boundary.md`](https://github.com/github/squad/blob/v2.0.0/docs/specification/adr-001-client-control-execution-boundary.md) — ADR 001: Client, Control, and Execution Boundary | Accepted draft baseline for `squad-protocol-v2.0-rc1`. Separates client UX/adaptation, control/broker conversation semantics, and execution/harness work; treats MCP as a bridge rather than the canonical conversation protocol. | Use it to decide which plane owns a behavior and to avoid leaking host- or transport-specific semantics into the shared conversation model. It records G1–G9 gates and calls out remaining limits such as unsigned cursors and client-asserted lease epochs. Its statement that the bridge bundles no execution harness predates the two v2.0.0 harnesses; the ADR itself says the code wins where they disagree. |
| [`adr-002-work-claims-and-external-queues.md`](https://github.com/github/squad/blob/v2.0.0/docs/specification/adr-002-work-claims-and-external-queues.md) — ADR 002: Work Claims and External Work Queues | Status "Proposed", but its Git-ref claim provider ships opt-in in v2.0.0 (`watch.claims`, `squad triage --claims git-ref`). Implements `work.claim` from the work-lifecycle profile and the compare-and-swap claim requirement from the automation profile, and amends the GitHub binding. | Use it when more than one executor watches the same repository. Each claim is one ref on the shared remote, updated by compare-and-swap; every contending executor must use the same remote. External dispatchers such as gh-aw work queues are a separate future role that never implements `WorkClaimProvider`. Chapter 9 (Volume 1) and Chapter 17 cover the practice. |
| [`adr-003-host-neutral-canonical-coordinator.md`](https://github.com/github/squad/blob/v2.0.0/docs/specification/adr-003-host-neutral-canonical-coordinator.md) — ADR 003: Host-Neutral Canonical Coordinator in the Workspace | Accepted (option C), 2026-11-13. Affects the adapter profile's projection contract and canonical paths (§4–§5) and upgrade and rollback (§13). | `.github/agents/squad.agent.md` stays the canonical coordinator for Copilot alone, and its output is unchanged. Every other host's digest is self-contained and never points at Copilot's file; parity tests keep the hosts in step. Option B, a host-neutral file that Copilot's is generated from, stays an opt-in spike (#2488). Chapter 20 explains the projection. |
| [`client-harness-adapters-v0.2.md`](https://github.com/github/squad/blob/v2.0.0/docs/specification/client-harness-adapters-v0.2.md) — Squad Client and Harness Adapter Profile | Working, non-normative requirements draft; non-claimable, with promotion (§15) pending. Defines host projection, client and harness adapter boundaries, workspace projections, and seven-host integration expectations. Revised for v2.0.0: its body now describes the two shipped `HarnessAdapter`s and their shared approval queue, though its status header still describes the seven-host model as unfinished. | Keep project-file projection separate from client UX/transport adaptation, and keep both separate from execution harness responsibilities. Consult its deviations before claiming parity. |
| [`client-backend-decoupling-v0.2.md`](https://github.com/github/squad/blob/v2.0.0/docs/specification/client-backend-decoupling-v0.2.md) — Squad Client and Backend Decoupling | Working, non-normative requirements draft; non-claimable, with promotion (§14) pending. Describes the three-plane model and portable conversation, event, capability, approval, and harness contracts. The experimental `/backend` subpath implements part of the draft. Two execution harnesses ship (`claude-agent-sdk`, registered by default when its optional SDK is installed and an API credential is configured, and `copilot-sdk`, registered only when listed in `SQUAD_BACKEND_HARNESSES`); without one, the MCP bridge records transcripts and events only. | Design transports around the shared backend resource model; do not make MCP itself the portable conversation protocol or assume remote durable approvals and lease coordination are complete. |
