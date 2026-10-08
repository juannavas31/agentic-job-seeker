# Feature Specification: Resume-Based Job Discovery

**Feature Branch**: `001-job-seeker`

**Created**: 2026-09-30

**Status**: Draft

**Input**: User description: Build a backend web server that exposes a RESTful API to store resumes, search LinkedIn/Glassdoor/InfoJobs using role and publication-date criteria, filter jobs against a selected resume, store matching jobs, generate cover letters, avoid duplicates, provide retrieval endpoints for resumes and cover letters, and expose an OpenAPI/Swagger specification endpoint.

## User Scenarios & Testing

### User Story 1 - Create and Replace Resume via API (Priority: P1)

As an API client, I can create and replace a stored resume so the backend can use it to evaluate job listings.

**Why this priority**: The resume is the basis for job matching and tailored cover letters.

**Independent Test**: Call `POST /resumes` with `fileName` and `fileContent`, then call `PUT /resumes` and verify replacement behavior, including `400` when there is no existing resume to replace.

**Acceptance Scenarios**:

1. **Given** no resume has been provided, **When** the client calls `POST /resumes` with a valid `fileName` and `fileContent`, **Then** the backend stores that resume in the designated resume storage location.
2. **Given** a resume is already stored, **When** the client calls `PUT /resumes` with replacement data, **Then** the stored resume is replaced and subsequent matching uses the new content.
3. **Given** no resume is currently stored, **When** the client calls `PUT /resumes`, **Then** the backend responds with HTTP `400` and does not create a new resume through that endpoint.
4. **Given** a submitted resume payload is invalid or cannot be processed, **When** the client calls `POST /resumes` or `PUT /resumes`, **Then** the backend reports the problem and leaves previously stored data unchanged.

### User Story 2 - Search Matching Jobs via API (Priority: P1)

As an API client, I can call a jobs endpoint with role, resume, and date query parameters to receive listings that pass resume-based screening.

**Why this priority**: Finding relevant opportunities is the application's primary user outcome.

**Independent Test**: With stored resumes and representative listings, call `GET /jobs` with mandatory `role`, `resume`, and `date`, then verify returned matches, associated cover letters, threshold enforcement, and technology-gate exclusions.

**Acceptance Scenarios**:

1. **Given** a stored resume, **When** the client calls `GET /jobs` with mandatory `role`, `resume`, and `date`, **Then** the backend searches supported portals and screens fetched listings against the selected resume.
2. **Given** a listing meets at least half of its assessed job requirements and passes applicable technology gates, **When** screening completes, **Then** it is eligible to appear in the results with its estimated match percentage.
3. **Given** a listing matches less than half of its assessed requirements, **When** screening completes, **Then** it is excluded from the results.
4. **Given** a listing names one or more programming languages, **When** the resume matches none of those languages, **Then** the listing is excluded.
5. **Given** a listing requires a frontend framework, **When** the resume does not match a required frontend framework, **Then** the listing is excluded.
6. **Given** the requested resume identified by `resume` does not exist, **When** `GET /jobs` is called, **Then** the backend reports the request as invalid and does not execute a portal search.
7. **Given** a listing has no stated programming-language or frontend-framework requirement, **When** it is screened, **Then** the corresponding technology gate does not exclude it.

### User Story 3 - Save Jobs and Avoid Duplicates (Priority: P2)

As an API client, I can rely on the backend to keep a local record of suitable jobs without saving the same listing more than once.

**Why this priority**: Persistent records support later review and prevent repeated searches from creating duplicate work.

**Independent Test**: Process a qualifying listing twice and verify that one job file is present and the second encounter is skipped.

**Acceptance Scenarios**:

1. **Given** a qualifying listing is not already stored, **When** it passes screening, **Then** the application saves a text file under `jobs/` named using the company, job role, and publication date.
2. **Given** a fetched listing is already represented in `jobs/`, **When** it is encountered again, **Then** the application skips further processing and does not create another job file or cover letter.
3. **Given** a company name or job role contains characters unsuitable for a file name, **When** the listing is saved, **Then** the resulting file name remains usable and does not escape the designated jobs directory.

### User Story 4 - Generate and Fetch Cover Letters (Priority: P2)

As an API client, I can obtain tailored cover letters for matching jobs and query stored cover letters later.

**Why this priority**: A tailored letter makes each saved opportunity more actionable.

**Independent Test**: Process one qualifying job and verify cover-letter creation; then call `GET /cover-letters` with mandatory `date` and optional `company` and verify filtering behavior.

**Acceptance Scenarios**:

1. **Given** a listing passes screening and is saved, **When** processing completes, **Then** a tailored cover letter is saved as a text file whose name is the job file name followed by `.cover.txt`.
2. **Given** a job has already been stored, **When** the duplicate is fetched, **Then** no second cover letter is generated.
3. **Given** cover-letter generation fails, **When** the qualifying job is processed, **Then** the job remains saved and the failure is reported without presenting a nonexistent letter as available.
4. **Given** stored cover letters exist, **When** the client calls `GET /cover-letters` with `date` and no `company`, **Then** the backend returns cover letters for that date.
5. **Given** stored cover letters exist for multiple companies on a date, **When** the client calls `GET /cover-letters` with `date` and `company`, **Then** only cover letters for that company and date are returned.

### User Story 5 - Retrieve Resumes and API Contract (Priority: P1)

As an API client, I can retrieve stored resumes and discover the backend contract via OpenAPI/Swagger.

**Why this priority**: Consumers need discoverable API contracts and resume retrieval to use the backend reliably.

**Independent Test**: Call `GET /resumes` and `GET /openapi` and verify response success and contract availability.

**Acceptance Scenarios**:

1. **Given** one or more resumes are stored, **When** the client calls `GET /resumes`, **Then** the backend returns the stored resumes.
2. **Given** no resumes are stored, **When** the client calls `GET /resumes`, **Then** the backend returns an empty result.
3. **Given** the backend is running, **When** the client calls `GET /openapi`, **Then** the backend returns an OpenAPI/Swagger specification for the exposed REST endpoints.

### Edge Cases

- A search is attempted before any resume is available or with a `resume` query value that is not stored.
- A portal is unavailable, returns no listings, or returns incomplete job details.
- A listing omits its publication date, company, location, or job requirements.
- A listing has exactly a 50% assessed requirement match.
- A listing has no stated programming-language or frontend-framework requirements.
- Multiple listings share a company, role, and publication date but represent different jobs.
- A company name or job role sanitizes to the same file name as another job.
- A resume or job description contains equivalent skill names or abbreviations.
- Cover-letter generation is unavailable or returns unusable content.
- `PUT /resumes` is called when no resume exists.
- `GET /jobs` or `GET /cover-letters` is called without mandatory query parameters.

## Requirements

### Functional Requirements

- **FR-001**: The application MUST be a backend web server exposing a RESTful HTTP API.
- **FR-002**: The backend MUST expose `POST /resumes` accepting `fileName` and `fileContent` in the request body to create/store a resume.
- **FR-003**: The backend MUST expose `PUT /resumes` to replace an existing stored resume and MUST return HTTP `400` when no stored resume exists to replace.
- **FR-004**: The backend MUST expose `GET /resumes` to return stored resumes; the exact response schema is deferred to implementation planning.
- **FR-005**: The backend MUST expose `GET /jobs` with mandatory query parameters `role` (string), `resume` (string), and `date` (string).
- **FR-006**: `GET /jobs` MUST search supported portals and return jobs matching the selected resume together with the corresponding cover letters; the exact response schema is deferred to implementation planning.
- **FR-007**: The first-version portal set MUST include LinkedIn, Glassdoor, and InfoJobs; the permitted access method for each portal is deferred to a specific implementation task.
- **FR-008**: The application MUST extract from each job description the requested skills, technologies, programming languages, tools, databases, cloud environments, and similar items; compare that list with the selected resume; and compute the match percentage as the ratio of job requirements matched by the resume.
- **FR-009**: A job requirement is assessed as matched when it is present in the resume with the same name or a similar name (for example, AWS vs. Amazon Web Services); equivalent skills and partial matches count as a full match, and requirements are not weighted.
- **FR-010**: The application MUST exclude a job whose estimated requirement match is below 50%; a match of exactly 50% MUST meet this threshold.
- **FR-011**: If a job description specifies programming languages or frontend frameworks, the application MUST exclude the job when the resume matches none of them; matching any one listed item is sufficient to pass the gate.
- **FR-012**: The application MUST save every job that passes screening as a text file in `jobs/`, with a name based on the company, job role, and publication date; missing publication dates MUST be recorded as `missing`.
- **FR-013**: The application MUST identify a job uniquely by the concatenation of company, job role, and publication date; if a fetched job has the same values as a stored job, the application MUST skip further processing.
- **FR-014**: The application MUST automatically generate a cover letter for each newly validated job, based on the job requirements and selected resume, and save it as text using the job file name followed by `.cover.txt`.
- **FR-015**: The backend MUST expose `GET /cover-letters` with mandatory query parameter `date` (string) and optional query parameter `company` (string).
- **FR-016**: `GET /cover-letters` MUST return stored cover letters filtered by the supplied parameters; the exact response schema is deferred to implementation planning.
- **FR-017**: The backend MUST expose `GET /openapi` to return an OpenAPI/Swagger specification for the REST API.
- **FR-018**: The application MUST communicate portal, resume-reading, request-validation, or cover-letter errors without treating failed or incomplete processing as a successful result.
- **FR-019**: The application MUST keep resume, job, and cover-letter file operations within their designated storage locations and MUST NOT allow user-provided names to escape those locations.
- **FR-020**: The application MUST NOT require user authentication or authorization, in accordance with the project Constitution.
- **FR-021**: Cover-letter generation MAY send the resume and job description to an external AI service; the service MUST be free to use (for example, DeepSeek), MUST expose an MCP interface for programmatic access, and MUST comply with the project Constitution's requirements for openly documented, free access and permitted data handling. The specific AI service and interaction details are resolved during the implementation phase.

### Key Entities

- **Resume**: The user's current resume content, stored as Markdown and used as the matching and cover-letter source.
- **Search Criteria**: API query parameters for job search including role, selected resume identifier/name, publication-date criteria, and selected job portals.
- **Job Listing**: A fetched job's source, role, company, description, requirements, location, publication date, assessed match, and screening outcome.
- **Stored Job**: A validated job persisted as a text file and used to identify listings that should not be processed again.
- **Cover Letter**: Text generated for a validated job from its requirements and the user's resume, stored alongside the job record under its corresponding file name.
- **API Contract**: OpenAPI/Swagger definition exposed by the backend to describe endpoint paths, parameters, and request/response contracts.

## Success Criteria

### Measurable Outcomes

- **SC-001**: For a `GET /jobs` request with valid mandatory parameters and available portal results, every returned job meets the 50% requirement-match threshold and passes applicable programming-language and frontend-framework gates.
- **SC-002**: A successful `GET /jobs` response contains only qualifying jobs and includes a corresponding cover letter reference or content per the defined response contract.
- **SC-003**: Reprocessing the same stored listing creates zero additional job files and zero additional cover letters.
- **SC-004**: Every newly validated job has one corresponding text job file and, when generation succeeds, one corresponding `.cover.txt` file.
- **SC-005**: Resume content provided through `POST /resumes` remains available to `GET /resumes` and subsequent `GET /jobs` calls until replaced by `PUT /resumes`.
- **SC-006**: Calling `GET /openapi` returns the API specification while the backend is running.

## Assumptions

- The initial product is for a single user context and does not include account creation or role-based access.
- A search evaluates listings returned by supported and permitted portal access methods; it does not imply bypassing portal restrictions.
- The `jobs/` directory is the application's designated job and cover-letter storage location, and the `resumes/` directory is the designated resume storage location.
- A listing without an applicable language or frontend-framework requirement is not rejected by that technology gate.
- Match percentage is the ratio of job requirements (skills, technologies, programming languages, tools, databases, cloud environments, and similar items) that match the resume, with unweighted requirements and similar names treated as matches.
- Response body schemas for `GET /resumes`, `GET /jobs`, and `GET /cover-letters` are intentionally deferred to the planning/design phase.

## Clarifications

- **DEFERRED**: The permitted access method for LinkedIn, Glassdoor, and InfoJobs will be resolved as a specific implementation task; no compliant access method is assumed at specification time.