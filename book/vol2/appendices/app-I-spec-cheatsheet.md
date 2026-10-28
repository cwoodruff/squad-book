# Appendix I: Specification Cheat Sheet

The documents in `docs/specification/` describe profiles and contracts at different maturity levels. They are not a claim that every proposal is fully implemented in v1.1.0; check each document's status and the implementation before depending on a behavior. Each row below is its own compact table, keyed to one source document.

## Squad Specification README

| Scope | Quick use |
|---|---|
| `README.md` establishes the specification's maturity taxonomy, document registry, dependency graph, external references, and versioning policy. | Start here to understand how to interpret the suite and whether a profile is draft, candidate, or stable. |

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
| `charter-v0.1.md` standardizes charter purpose/authority, version association, canonical Markdown shape, machine-readable fields, deterministic subset, legacy handling, and extensions. | Validate that role identity, responsibilities, non-responsibilities, collaboration authority, and model metadata are parseable and unambiguous. |

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
| `github-work-lifecycle-binding-v0.1.md` maps lifecycle resources and labels, composes states, defines review/merge authority, revision tokens, stale writes, and provider limits. | Treat GitHub labels and issue/PR states as a provider binding; protect against stale updates and leave merge authority explicit. |

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

## Squad 2.0 (Preview) Specifications

> **Preview:** These new documents accompany Squad `v2.0.0-preview.2`. Their maturity labels matter: draft requirements are not equivalent to a stable, claimable interoperability standard.

| Specification | Status and scope | Quick use |
|---|---|---|
| [`adr-001-client-control-execution-boundary.md`](https://github.com/bradygaster/squad/blob/v2.0.0-preview.2/docs/specification/adr-001-client-control-execution-boundary.md) — ADR 001: Client, Control, and Execution Boundary | Accepted draft baseline for `squad-protocol-v2.0-rc1`. Separates client UX/adaptation, control/broker conversation semantics, and execution/harness work; treats MCP as a bridge rather than the canonical conversation protocol. | Use it to decide which plane owns a behavior and to avoid leaking host- or transport-specific semantics into the shared conversation model. It records G1–G9 gates and calls out remaining limits such as unsigned cursors and client-asserted lease epochs. |
| [`client-harness-adapters-v0.2.md`](https://github.com/bradygaster/squad/blob/v2.0.0-preview.2/docs/specification/client-harness-adapters-v0.2.md) — Squad Client and Harness Adapter Profile | Working, non-normative requirements draft; non-claimable. Defines host projection, client and harness adapter boundaries, workspace projections, and seven-host integration expectations. | Keep project-file projection separate from client UX/transport adaptation, and keep both separate from execution harness responsibilities. Consult its deviations before claiming parity. |
| [`client-backend-decoupling-v0.2.md`](https://github.com/bradygaster/squad/blob/v2.0.0-preview.2/docs/specification/client-backend-decoupling-v0.2.md) — Squad Client and Backend Decoupling | Working, non-normative requirements draft; non-claimable. Describes the three-plane model and portable conversation, event, capability, approval, and harness contracts. The experimental `/backend` subpath implements part of the draft; the MCP bridge is transcript/event-only. | Design transports around the shared backend resource model; do not make MCP itself the portable conversation protocol or assume remote durable approvals and lease coordination are complete. |
