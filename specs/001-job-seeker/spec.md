# Feature Specification: Resume-Based Job Discovery

**Feature Branch**: `001-job-seeker`

**Created**: 2026-09-30

**Status**: Draft

**Input**: User description: Build a web application that stores a user's resume in Markdown, searches LinkedIn, Glassdoor, and InfoJobs using role, location, and publication-date criteria, filters jobs against the resume, stores matching jobs, generates cover letters, avoids duplicates, and displays matching jobs with estimated match percentages.

## User Scenarios & Testing

### User Story 1 - Provide a Resume (Priority: P1)

As a job seeker, I can provide my resume so the application can use it to evaluate job listings.

**Why this priority**: The resume is the basis for job matching and tailored cover letters.

**Independent Test**: Provide a supported resume and verify that its content is stored in the application's designated Markdown file and is available to the matching workflow.

**Acceptance Scenarios**:

1. **Given** no resume has been provided, **When** the user submits a valid resume, **Then** the application stores its content in Markdown in the designated internal file.
2. **Given** a resume is already stored, **When** the user provides an updated resume, **Then** the stored resume is updated and subsequent matching uses the new content.
3. **Given** a submitted resume cannot be read, **When** the user provides it, **Then** the application reports the problem and does not replace the previously stored resume.

### User Story 2 - Find and Review Suitable Jobs (Priority: P1)

As a job seeker, I can search supported job portals using a role, one or more locations, and a publication-date range, then review listings that pass resume-based screening.

**Why this priority**: Finding relevant opportunities is the application's primary user outcome.

**Independent Test**: With a stored resume and representative job listings, submit search criteria and verify the displayed results, match estimates, and exclusion of jobs below the threshold or failing a technology gate.

**Acceptance Scenarios**:

1. **Given** a stored resume, **When** the user searches with a job role, location criteria, and publication-date criteria, **Then** the application searches the selected supported portals and screens the fetched listings.
2. **Given** a listing meets at least half of its assessed job requirements and passes applicable technology gates, **When** screening completes, **Then** it is eligible to appear in the results with its estimated match percentage.
3. **Given** a listing matches less than half of its assessed requirements, **When** screening completes, **Then** it is excluded from the results.
4. **Given** a listing names one or more programming languages, **When** the resume matches none of those languages, **Then** the listing is excluded.
5. **Given** a listing requires a frontend framework, **When** the resume does not match a required frontend framework, **Then** the listing is excluded.
6. **Given** a location search includes remote, hybrid, or city locations, **When** results are returned, **Then** listings matching the requested location criteria are included, including combinations of those location types.
7. **Given** a listing has no stated programming-language or frontend-framework requirement, **When** it is screened, **Then** the corresponding technology gate does not exclude it.

### User Story 3 - Save Jobs and Avoid Duplicates (Priority: P2)

As a job seeker, I can keep a local record of suitable jobs without saving the same listing more than once.

**Why this priority**: Persistent records support later review and prevent repeated searches from creating duplicate work.

**Independent Test**: Process a qualifying listing twice and verify that one job file is present and the second encounter is skipped.

**Acceptance Scenarios**:

1. **Given** a qualifying listing is not already stored, **When** it passes screening, **Then** the application saves a text file under `jobs/` named using the company, job role, and publication date.
2. **Given** a fetched listing is already represented in `jobs/`, **When** it is encountered again, **Then** the application skips further processing and does not create another job file or cover letter.
3. **Given** a company name or job role contains characters unsuitable for a file name, **When** the listing is saved, **Then** the resulting file name remains usable and does not escape the designated jobs directory.

### User Story 4 - Generate and Find Cover Letters (Priority: P2)

As a job seeker, I can review a cover letter tailored to each suitable job and based on my resume.

**Why this priority**: A tailored letter makes each saved opportunity more actionable.

**Independent Test**: Process one qualifying job and verify that a text cover-letter file is created with the corresponding job-file name plus `.cover.txt`, and that its content reflects both the resume and job requirements.

**Acceptance Scenarios**:

1. **Given** a listing passes screening and is saved, **When** processing completes, **Then** a tailored cover letter is saved as a text file whose name is the job file name followed by `.cover.txt`.
2. **Given** a job has already been stored, **When** the duplicate is fetched, **Then** no second cover letter is generated.
3. **Given** cover-letter generation fails, **When** the qualifying job is processed, **Then** the job remains saved and the failure is reported without presenting a nonexistent letter as available.

### User Story 5 - Inspect Search Results (Priority: P1)

As a job seeker, I can see the suitable jobs and where to find each generated cover letter.

**Why this priority**: The user needs a usable way to review and act on the results of a search.

**Independent Test**: Process qualifying and rejected listings and verify that the result list contains only qualifying jobs and shows each requested field.

**Acceptance Scenarios**:

1. **Given** a search has completed, **When** the user views its results, **Then** each listed job shows its role or name, company, estimated matching percentage, location, and produced cover-letter file.
2. **Given** a matching job has no generated cover letter, **When** the user views results, **Then** its entry indicates that no cover-letter file is available.
3. **Given** no jobs pass screening, **When** the user views results, **Then** the application shows an empty result state rather than rejected jobs as matches.

### Edge Cases

- A search is attempted before a resume is available.
- A portal is unavailable, returns no listings, or returns incomplete job details.
- A listing omits its publication date, company, location, or job requirements.
- A listing has exactly a 50% assessed requirement match.
- A listing has no stated programming-language or frontend-framework requirements.
- Multiple listings share a company, role, and publication date but represent different jobs.
- A company name or job role sanitizes to the same file name as another job.
- A resume or job description contains equivalent skill names or abbreviations.
- Cover-letter generation is unavailable or returns unusable content.
- A user requests multiple location types or cities in one search.

## Requirements

### Functional Requirements

- **FR-001**: The application MUST let the user provide a resume and store its content internally as Markdown in a designated file.
- **FR-002**: The application MUST let the user replace the stored resume, and MUST use the current stored resume for subsequent searches and cover letters.
- **FR-003**: The application MUST let the user search for jobs by role, location criteria, and publication date.
- **FR-004**: Location criteria MUST support remote, hybrid, city names, and combinations of these values.
- **FR-005**: The first-version portal set MUST include LinkedIn, Glassdoor, and InfoJobs, subject to the external-service constraint in the Constitution and the clarification about permitted access methods below.
- **FR-006**: The application MUST assess each fetched job against the stored resume and estimate the percentage of assessed job requirements that match.
- **FR-007**: The application MUST exclude a job whose estimated requirement match is below 50%; a match of exactly 50% MUST meet this threshold.
- **FR-008**: If a job description specifies programming languages, the application MUST exclude the job when the resume matches none of those languages.
- **FR-009**: If a job description requires a frontend framework, the application MUST exclude the job when the resume does not match a required frontend framework.
- **FR-010**: The application MUST save every job that passes screening as a text file in `jobs/`, with a name based on the company, job role, and publication date.
- **FR-011**: The application MUST compare fetched listings with stored jobs and skip further processing for a listing that is already stored.
- **FR-012**: The application MUST automatically generate a cover letter for each newly validated job, based on the job requirements and stored resume, and save it as text using the job file name followed by `.cover.txt`.
- **FR-013**: The application MUST display matching jobs with the job role or name, company, estimated matching percentage, location, and cover-letter file produced, when available.
- **FR-014**: The application MUST communicate portal, resume-reading, or cover-letter errors without treating failed or incomplete processing as a successful result.
- **FR-015**: The application MUST keep resume, job, and cover-letter file operations within their designated storage locations and MUST NOT allow user-provided names to escape those locations.
- **FR-016**: The application MUST NOT require user authentication or authorization, in accordance with the project Constitution.
- **FR-017**: External APIs or services MUST comply with the project Constitution's requirements for openly documented, free access and permitted data handling. The application MUST NOT send resume data to an external service unless that service's terms permit the use and the user has been informed as required by the resolved product requirements.

### Key Entities

- **Resume**: The user's current resume content, stored as Markdown and used as the matching and cover-letter source.
- **Search Criteria**: A job role, one or more location values, publication-date criteria, and selected job portals.
- **Job Listing**: A fetched job's source, role, company, description, requirements, location, publication date, assessed match, and screening outcome.
- **Stored Job**: A validated job persisted as a text file and used to identify listings that should not be processed again.
- **Cover Letter**: Text generated for a validated job from its requirements and the user's resume, stored alongside the job record under its corresponding file name.

## Success Criteria

### Measurable Outcomes

- **SC-001**: For a search with a stored resume and available portal results, every displayed job meets the 50% requirement-match threshold and passes all applicable programming-language and frontend-framework gates.
- **SC-002**: Each displayed result includes the role or name, company, estimated match percentage, location, and cover-letter file availability.
- **SC-003**: Reprocessing the same stored listing creates zero additional job files and zero additional cover letters.
- **SC-004**: Every newly validated job has one corresponding text job file and, when generation succeeds, one corresponding `.cover.txt` file.
- **SC-005**: Resume content is persisted as Markdown and remains available to subsequent searches until the user replaces it.

## Assumptions

- The initial product is for a single user and does not include account creation or role-based access.
- A search evaluates listings returned by supported and permitted portal access methods; it does not imply bypassing portal restrictions.
- The `jobs/` directory is the application's designated job and cover-letter storage location.
- A listing without an applicable language or frontend-framework requirement is not rejected by that technology gate.
- Match percentage is intended to be based on job requirements, but the precise scoring and requirement extraction rules remain unresolved.

## Clarifications

- **NEEDS CLARIFICATION**: What access method is permitted and available for LinkedIn, Glassdoor, and InfoJobs under their current terms and the project's requirement to use free, openly documented APIs? If a portal has no compliant access method, should it be excluded or replaced?
- **NEEDS CLARIFICATION**: What constitutes one assessed requirement, how are requirements weighted, and how should equivalent skills or partial matches affect the percentage?
- **NEEDS CLARIFICATION**: For multiple programming languages or frontend frameworks, does matching any one satisfy the gate, or must the resume match every required item? The scenarios currently interpret the language rule as matching at least one listed language.
- **NEEDS CLARIFICATION**: Which resume upload formats must be accepted, and what exact application-managed file path should contain the Markdown resume?
- **NEEDS CLARIFICATION**: May cover-letter generation send the resume and job description to an external AI service? If so, which compliant service and what user disclosure or consent is required?
- **NEEDS CLARIFICATION**: What uniquely identifies a job for deduplication when company, role, and publication date collide, and how should missing publication dates be represented in file names?
- **NEEDS CLARIFICATION**: Should multiple location values be combined as alternatives (OR), required together (AND), or selectable per search?