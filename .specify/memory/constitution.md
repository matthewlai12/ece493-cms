<!--
Sync Impact Report
Version change: 1.0.0 -> 1.1.0
Modified principles: I. Spec-First, User-Centered Delivery -> I. Spec-First, Use-Case-Driven Delivery
Added sections: None
Removed sections: None
Templates requiring updates: ✅ .specify/templates/plan-template.md; ✅ .specify/templates/spec-template.md; ✅ .specify/templates/tasks-template.md; ⚠ .specify/templates/commands (missing)
Follow-up TODOs: TODO(RATIFICATION_DATE): original adoption date unknown; TODO(TECH_STACK): primary framework, database, and hosting are not specified
-->
# Conference Management System (CMS) Constitution

## Core Principles

### I. Spec-First, Use-Case-Driven Delivery
Every change MUST begin with a feature specification that is derived from the
UC-XX.md use cases and captures all elements in each use case. The spec MUST
include prioritized user stories, acceptance scenarios, and independent tests
for each story. Each user story MUST deliver user-visible value on its own,
enabling MVP delivery in increments. Rationale: the CMS is driven by concrete
use cases that must remain testable and demonstrable at every stage.

### II. Security & Privacy by Design
All features MUST enforce authentication and authorization appropriate to the
role (guest, author, reviewer, chair, admin). Sensitive data MUST be minimized
and MUST NOT appear in logs; access to PII MUST follow least privilege and be
justified in the spec. Rationale: the CMS manages submissions, reviews, and
accounts that require strict confidentiality and access control.

### III. Testable Reliability
P1 user stories and any change affecting roles, submissions, reviews, or
payments MUST include automated tests (unit and integration as appropriate).
Bug fixes MUST add regression coverage. A user acceptance test suite MUST be
created as the union of all acceptance tests from TC-XX.md. If tests are
deferred, the plan MUST record the risk and the temporary mitigation.
Rationale: reliability is core to conference operations and deadlines.

### IV. Observability & Auditability
Critical actions (authentication events, submission changes, review actions,
role changes, scheduling decisions) MUST emit structured logs with actor,
timestamp, outcome, and correlation identifier. Admin actions MUST be auditable.
Rationale: investigations, support, and compliance require reliable traceability.

### V. Simplicity & Safe Change
Prefer the simplest design that satisfies requirements; avoid speculative
abstractions. Breaking changes MUST include a migration plan, backfill strategy,
rollback path, and versioned data or API contracts when external integrations
exist. Rationale: the CMS must evolve safely across conference cycles.

## Architecture & Data Constraints

- Technology choices MUST be documented in the plan.md Technical Context.
- Data retention and backup expectations MUST be specified per feature where
  data is created or modified.
- Schema changes MUST be reversible and documented with a migration plan.
- TODO(TECH_STACK): primary framework, database, and hosting are not specified.

## Workflow & Quality Gates

- Every feature MUST produce spec.md, plan.md, and tasks.md using the templates
  in .specify/templates.
- The spec MUST explicitly map requirements to UC-XX.md and reference relevant
  TC-XX.md acceptance tests.
- A unified user acceptance test suite MUST aggregate all TC-XX.md tests and be
  maintained as the single source of UAT coverage.
- Constitution Check gates MUST be satisfied before Phase 0 research and
  re-validated after Phase 1 design.
- Code review is REQUIRED for all non-trivial changes; reviewers MUST verify
  security, tests, and audit logging where applicable.
- Releases affecting data or access control MUST include a rollback plan.

## Governance

- This constitution is the highest-order project policy and supersedes other
  guidelines.
- Amendments require: documented proposal, rationale, impact assessment, and
  approval by the project maintainers.
- Versioning follows semantic versioning: MAJOR for principle removals or
  incompatible changes, MINOR for new principles or material expansions, PATCH
  for clarifications or non-semantic edits.
- Compliance MUST be checked in plans and reviews; exceptions require explicit
  written justification and time-bound remediation.

**Version**: 1.1.0 | **Ratified**: TODO(RATIFICATION_DATE): original adoption date unknown | **Last Amended**: 2026-02-10
