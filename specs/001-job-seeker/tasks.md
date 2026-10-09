# Tasks: Resume-Based Job Discovery API

**Input**: Design documents from `/specs/001-job-seeker/`

**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/openapi.yaml`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the backend project structure and test/runtime foundation.

- [x] T001 Create the backend package structure under `backend/app/` with `api/`, `core/`, `db/`, `models/`, `schemas/`, `services/`, and `tests/` directories.
- [x] T002 Initialize FastAPI app configuration in `backend/app/main.py` and application factory wiring for router registration.
- [x] T003 [P] Configure Python tooling for pytest, linting, and formatting in the backend environment.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core persistence, validation, and base API infrastructure required before user-story work begins.

- [ ] T004 Implement file-system storage utilities for `resumes/` and `jobs/` with validation, sanitization, and safe path handling.
- [ ] T005 Implement MongoDB client and collection helpers for `resumes` and `cover-letters` in `backend/app/db/`.
- [ ] T006 Define request/response schemas and domain models for resumes, jobs, and cover letters in `backend/app/schemas/` and `backend/app/models/`.
- [ ] T007 Create shared error-handling and validation patterns for invalid payloads, missing resources, and portal failures.
- [ ] T008 Set up router and dependency injection structure in `backend/app/api/v1/` and `backend/app/api/deps.py`.
- [ ] T009 [P] Add baseline unit test scaffolding and fixtures for file storage and MongoDB abstractions in `backend/tests/unit/`.

**Checkpoint**: Foundation ready - user story implementation can begin in parallel.

---

## Phase 3: User Story 1 - Create and Replace Resume via API (Priority: P1) 🎯 MVP

**Goal**: Allow clients to store and replace the active resume safely and persist the resume metadata in MongoDB.

**Independent Test**: POST/PUT ` /resumes` with valid and invalid payloads; verify storage, replacement semantics, and HTTP 400 when no existing resume is present.

### Tests for User Story 1

- [ ] T010 [P] [US1] Contract test for `POST /resumes` and `PUT /resumes` in `backend/tests/integration/test_resume_api.py`.
- [ ] T011 [P] [US1] Unit test for resume storage validation and replacement rules in `backend/tests/unit/test_resume_service.py`.

### Implementation for User Story 1

- [ ] T012 [P] [US1] Implement `ResumeStore` and resume file operations in `backend/app/services/resume_service.py`.
- [ ] T013 [P] [US1] Implement MongoDB resume persistence adapter for the `resumes` collection in `backend/app/db/resume_repository.py`.
- [ ] T014 [US1] Add endpoint handlers for `POST /resumes` and `PUT /resumes` in `backend/app/api/v1/endpoints/resumes.py`.
- [ ] T015 [US1] Add request validation, empty-state handling, and 400/422 response rules for resume creation and replacement.
- [ ] T016 [US1] Expose resume retrieval support for `GET /resumes` and persist the selected rule set needed for later job-screening flows.

**Checkpoint**: At this point, User Story 1 is fully functional and independently testable.

---

## Phase 4: User Story 2 - Search Matching Jobs via API (Priority: P1)

**Goal**: Search supported portals using role, resume, and date criteria, and apply the screening algorithm to return only qualifying jobs.

**Independent Test**: Request `GET /jobs` with valid `role`, `resume`, and `date`; verify threshold handling, technology gates, and invalid-resume rejection.

### Tests for User Story 2

- [ ] T017 [P] [US2] Contract test for `GET /jobs` success and invalid-resume cases in `backend/tests/integration/test_jobs_api.py`.
- [ ] T018 [P] [US2] Unit tests for scoring, threshold logic, and technology-gate exclusions in `backend/tests/unit/test_screening_service.py`.

### Implementation for User Story 2

- [ ] T019 [P] [US2] Implement `JobSearchService` orchestration in `backend/app/services/job_search_service.py`.
- [ ] T020 [P] [US2] Implement requirement extraction and scoring logic in `backend/app/services/screening_service.py`.
- [ ] T021 [US2] Add portal integration adapter layer for LinkedIn, Glassdoor, and InfoJobs in `backend/app/services/portal/` or equivalent integration module.
- [ ] T022 [US2] Implement `GET /jobs` endpoint in `backend/app/api/v1/endpoints/jobs.py` with required query parameters and validation.
- [ ] T023 [US2] Add error handling for unavailable portals, incomplete job payloads, and invalid search inputs.

**Checkpoint**: At this point, User Stories 1 and 2 work independently and together.

---

## Phase 5: User Story 3 - Save Jobs and Avoid Duplicates (Priority: P2)

**Goal**: Persist validated jobs once and skip repeated processing when the same company/role/date combination is encountered again.

**Independent Test**: Process the same qualifying listing twice and verify only one job file and one cover-letter artifact are created.

### Tests for User Story 3

- [ ] T024 [P] [US3] Integration test for deduplication and file naming in `backend/tests/integration/test_job_storage.py`.
- [ ] T025 [P] [US3] Unit test for storage-key generation and file-name sanitization in `backend/tests/unit/test_job_store_service.py`.

### Implementation for User Story 3

- [ ] T026 [P] [US3] Implement persisted job-file handling and dedupe key logic in `backend/app/services/job_store_service.py`.
- [ ] T027 [US3] Add sanitization and safe filename generation for company/role/date combinations in the job storage layer.
- [ ] T028 [US3] Integrate dedupe checks into the jobs screening flow so repeat processing is skipped before generating a cover letter.

**Checkpoint**: Job persistence is stable and deduplication works correctly before cover-letter generation begins.

---

## Phase 6: User Story 4 - Generate and Fetch Cover Letters (Priority: P2)

**Goal**: Generate tailored cover letters for validated jobs and support retrieval by date and optional company filters.

**Independent Test**: Generate a cover letter for a saved job, then call `GET /cover-letters` with `date` and optional `company` to verify filtering behavior.

### Tests for User Story 4

- [ ] T029 [P] [US4] Contract test for `GET /cover-letters` in `backend/tests/integration/test_cover_letters_api.py`.
- [ ] T030 [P] [US4] Unit test covering cover-letter generation failure handling and filter logic in `backend/tests/unit/test_cover_letter_service.py`.

### Implementation for User Story 4

- [ ] T031 [P] [US4] Implement cover-letter generation orchestration in `backend/app/services/cover_letter_service.py`.
- [ ] T032 [P] [US4] Implement filesystem writing for job cover letters with the `<jobfile>.cover.txt` naming convention.
- [ ] T033 [US4] Implement MongoDB persistence for cover-letter metadata using `company`, `role`, `date`, and `name` in `backend/app/db/cover_letter_repository.py`.
- [ ] T034 [US4] Add endpoint handlers for `GET /cover-letters` in `backend/app/api/v1/endpoints/cover_letters.py` with required `date` and optional `company`.
- [ ] T035 [US4] Add graceful error responses when cover-letter generation is unavailable or returns unusable content without corrupting the job record.

**Checkpoint**: Cover-letter generation and retrieval are fully operational and independently testable.

---

## Phase 7: User Story 5 - Retrieve Resumes and API Contract (Priority: P1)

**Goal**: Allow API consumers to inspect the stored resumes and the OpenAPI contract of the service.

**Independent Test**: Call `GET /resumes` and `GET /openapi`; verify successful responses and contract availability.

### Tests for User Story 5

- [ ] T036 [P] [US5] Contract test for `GET /resumes` and `GET /openapi` in `backend/tests/integration/test_contract_api.py`.
- [ ] T037 [P] [US5] Unit test for OpenAPI router exposure and empty-state listing behavior in `backend/tests/unit/test_openapi_service.py`.

### Implementation for User Story 5

- [ ] T038 [P] [US5] Add `GET /resumes` route and response handling in `backend/app/api/v1/endpoints/resumes.py`.
- [ ] T039 [US5] Add `GET /openapi` route and ensure FastAPI exposes the generated OpenAPI schema for the public REST API.
- [ ] T040 [US5] Validate that all documented endpoints match the planning contract in `specs/001-job-seeker/contracts/openapi.yaml` and resolve any contract drift.

**Checkpoint**: The API contract and resume retrieval flow are available and consistent with the feature spec.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, documentation, and release-readiness checks after all user stories are complete.

- [ ] T041 [P] Run the integration test suite covering resume storage, job screening, dedupe, cover-letter generation, and contract exposure.
- [ ] T042 [P] Review all file-path safety checks and ensure user inputs cannot escape the designated `resumes/` and `jobs/` directories.
- [ ] T043 [P] Update `backend/README.md` and feature docs with any implementation caveats, environment variables, and local startup commands.
- [ ] T044 [P] Run quickstart validation from `specs/001-job-seeker/quickstart.md` against the local backend service.
- [ ] T045 Final code cleanup, logging improvements, and error-message consistency across all endpoints and services.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Must complete before all user story work.
- **User Stories (Phases 3-7)**: Can proceed in parallel after foundational work, though the repository may implement them sequentially to keep scope manageable.
- **Polish (Phase 8)**: Requires all user stories to be complete.

### Story Dependencies

- **US1**: Foundation only.
- **US2**: Depends on US1 resume storage and validation.
- **US3**: Depends on US2 job screening and the job-store pipeline.
- **US4**: Depends on US2 and US3.
- **US5**: Depends on US1 and the OpenAPI router integration.

### Within Each User Story

- Tests should be written first and fail before implementation.
- Domain models and schemas before service logic.
- Services before endpoint wiring.
- API validation before final integration.
