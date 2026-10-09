# Research: Resume-Based Job Discovery API

## Decision 1: API framework and layering

- Decision: Implement as FastAPI with endpoint modules delegating to service-layer functions.
- Why: Aligns with constitution technical constraints and existing backend structure; keeps HTTP concerns separate from business logic.
- Alternatives considered:
  - Flask: rejected because project constraint explicitly sets FastAPI.
  - Single-file endpoint + logic implementation: rejected due to separation-of-concerns requirement.

## Decision 2: Resume replacement semantics for `PUT /resumes`

- Decision: `PUT /resumes` updates an existing resume only; if none exists return HTTP 400.
- Why: Matches feature requirement exactly and prevents ambiguous upsert behavior.
- Alternatives considered:
  - Upsert semantics: rejected because it violates explicit requirement.

## Decision 3: `GET /openapi` contract exposure

- Decision: Expose `GET /openapi` endpoint that returns the OpenAPI schema document.
- Why: Requirement asks for this exact path; FastAPI default schema path can be wrapped/mapped to satisfy it.
- Alternatives considered:
  - Keep only `/openapi.json`: rejected because required path is `/openapi`.

## Decision 4: Persistence approach for v1

- Decision: Use filesystem persistence in designated `resumes/` and `jobs/` directories, including cover-letter files.
- Why: Already required by specification, simple operational model for single-user v1.
- Alternatives considered:
  - Database-first persistence: deferred; adds unnecessary migration/runtime complexity for v1.

## Decision 5: Job identity and duplicate prevention

- Decision: Use normalized tuple `(company, role, publication_date)` as unique identity key and derive safe filename from same components.
- Why: Directly required by FR-013 and edge cases around duplicates/path safety.
- Alternatives considered:
  - Source URL as unique key: rejected because not mandated and unstable across portals.

## Decision 6: Screening and technology gates

- Decision: Apply screening in this order: extract requirements -> similarity matching -> threshold gate (>=50%) -> language/framework gate.
- Why: Makes gating deterministic and testable; aligns with FR-008 through FR-011.
- Alternatives considered:
  - Weighted scoring models: rejected because spec requires unweighted requirements.

## Decision 7: Query parameter validation

- Decision: Enforce mandatory query params at API boundary for `GET /jobs` (`role`, `resume`, `date`) and `GET /cover-letters` (`date`).
- Why: Prevents undefined service behavior and matches explicit endpoint requirements.
- Alternatives considered:
  - Optional params with defaults: rejected due to strict API contract in spec.

## Decision 8: MongoDB metadata persistence

- Decision: Keep the file-system copies as the canonical content store, and mirror metadata in MongoDB collections named `resumes` and `cover-letters`.
- Why: Requirement explicitly requires both the filesystem and MongoDB representations to exist for resumes and cover letters.
- Alternatives considered:
  - MongoDB-only persistence: rejected because the specification still requires the filesystem text file artifacts.

## Decision 9: External service constraints

- Decision: Keep cover-letter generation provider pluggable through a service adapter and gate activation by compliance checks.
- Why: Constitution requires open/free APIs and compliant data handling.
- Alternatives considered:
  - Hardcoded provider integration in endpoint layer: rejected due to maintainability and policy compliance risks.
