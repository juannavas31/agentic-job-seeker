# Agentic Job Seeker Constitution

## Core Principles

### I. No User Authentication or Authorization
The product MUST NOT require users to sign in or implement user- or role-based authorization. User accounts and access-control features are out of scope unless this constitution is amended. This principle concerns product-user access and does not prohibit protecting infrastructure or credentials required to call external services.

### II. Open and Free External APIs
The product MUST use only external APIs that are openly documented and available without payment for the project's intended use. It MUST NOT depend on paid-only plans or endpoints. Before adopting an API, verify its terms, usage limits, and data-handling requirements; do not send user data to an API whose terms do not permit the intended use.

### III. SOLID and Separation of Concerns
The system MUST follow SOLID principles and keep responsibilities separate across API, business-logic, and data-access code. Components MUST depend on clear contracts and avoid coupling domain rules to transport or persistence details. Design choices that materially depart from these principles MUST be documented and justified.

### IV. Unit and Integration Tests Are Mandatory
Every user story and implemented task MUST include relevant automated unit tests and integration tests. Tests MUST cover the behavior changed by the work, and the work is not complete until both test types pass. A task that changes no executable behavior still requires tests that validate its relevant contract or effect.

## Technical Constraints

The backend is a Python web service built with FastAPI. New backend work MUST follow the repository's documented structure and keep HTTP endpoint handling separate from business logic. External-service integrations are subject to Principle II.

## Development Workflow and Quality Gates

User stories and implementation tasks MUST identify their expected behavior and test coverage. Reviewers MUST verify that changes comply with these principles and that the required unit and integration tests pass. Exceptions require a constitution amendment; a feature plan or implementation task alone cannot waive a principle.

## Governance

This constitution governs project specifications, plans, implementation tasks, and code changes. Amendments MUST be reviewed and recorded in this file. Each amendment MUST update the version according to semantic versioning: MAJOR for incompatible governance changes, MINOR for new or materially expanded principles or sections, and PATCH for clarifications that do not change requirements. Project changes MUST be reviewed for compliance with the current version.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): original adoption date unknown | **Last Amended**: 2026-09-30
