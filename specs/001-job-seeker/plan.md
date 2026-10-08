# Implementation Plan: Resume-Based Job Discovery API

**Branch**: `001-job-seeker` | **Date**: 2026-10-08 | **Spec**: `/specs/001-job-seeker/spec.md`

**Input**: Feature specification from `/specs/001-job-seeker/spec.md`

## Summary

Implement a FastAPI backend that exposes REST endpoints to create/replace/list resumes, search and screen jobs against a selected resume, return matching jobs with cover letters, query stored cover letters, and expose OpenAPI at `GET /openapi`. The implementation keeps screening and persistence logic in service/data layers and keeps HTTP concerns in endpoint modules.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: FastAPI, Pydantic, Uvicorn, pytest

**Storage**: Local file storage (`resumes/`, `jobs/`); in-memory/runtime structures allowed for orchestration

**Testing**: pytest (unit + integration/API)

**Target Platform**: Linux server

**Project Type**: Backend web service (REST API)

**Performance Goals**: Return API responses for non-portal operations within 250 ms p95 on local environment; keep portal-bound operations observable with explicit timeout/error handling

**Constraints**: No authentication; use only open/free external APIs; preserve file-path safety; strict endpoint contracts and required query params

**Scale/Scope**: Single-user context; first release with LinkedIn/Glassdoor/InfoJobs integrations and file-based persistence

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Principle I (No Auth): PASS. No login/authorization features in scope.
- Principle II (Open/Free APIs): PASS with follow-up. Portal access strategy must be implemented only via compliant open/free methods.
- Principle III (SOLID/Separation): PASS. Plan separates endpoints, services, and storage adapters.
- Principle IV (Unit + Integration tests): PASS. Plan requires both test types for all stories/endpoints.
- Technical constraint (FastAPI backend): PASS. Architecture is FastAPI-first.

## Project Structure

### Documentation (this feature)

```text
specs/001-job-seeker/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── openapi.yaml
└── tasks.md              # Generated later by /speckit-tasks
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── resumes.py
│   │           ├── jobs.py
│   │           ├── cover_letters.py
│   │           └── openapi.py
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   └── services/
│       ├── resume_service.py
│       ├── job_search_service.py
│       ├── screening_service.py
│       ├── job_store_service.py
│       └── cover_letter_service.py
├── migrations/
└── tests/
    ├── unit/
    └── integration/
```

**Structure Decision**: Use the existing backend FastAPI layout documented in `backend/README.md`, with dedicated endpoint modules per API area and service modules for matching, persistence, and portal orchestration.

## Phase 0: Research and Decisions

See `/specs/001-job-seeker/research.md`.

## Phase 1: Design Outputs

- Data model: `/specs/001-job-seeker/data-model.md`
- API contract draft: `/specs/001-job-seeker/contracts/openapi.yaml`
- Quickstart and validation steps: `/specs/001-job-seeker/quickstart.md`

## Phase 2 Preview (for /speckit-tasks)

Task decomposition should prioritize:
1. Resume endpoints and storage safety.
2. Jobs search endpoint orchestration + screening gates.
3. Cover-letter query endpoint and generation flow.
4. OpenAPI endpoint behavior.
5. Unit and integration tests for each endpoint and major service.

## Complexity Tracking

No constitution violations currently identified.
