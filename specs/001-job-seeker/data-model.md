# Data Model: Resume-Based Job Discovery API

## Overview

This model describes logical entities and contracts for a file-backed FastAPI service. Concrete persistence classes can vary as long as they satisfy these fields and invariants.

## Entities

### Resume

- Fields:
  - `file_name` (string, required)
  - `file_content` (string, required; markdown content)
  - `stored_at` (datetime, server-managed)
  - `mongo_name` (string, required; mirrored to MongoDB `resumes` collection, property `name`)
- Invariants:
  - `file_name` must be sanitized before filesystem write.
  - Only current stored resume version is active for matching.
  - MongoDB document in `resumes` collection must contain exactly `{ "name": <file_name> }`.

### JobQuery

- Fields:
  - `role` (string, required)
  - `resume` (string, required; references a stored resume identifier/name)
  - `date` (string, required; date filter value format to be finalized)
- Invariants:
  - All fields mandatory for `GET /jobs`.
  - `resume` must resolve to existing stored resume.

### JobListing

- Fields:
  - `source` (enum/string: linkedin | glassdoor | infojobs)
  - `role` (string)
  - `company` (string)
  - `location` (string, optional)
  - `publication_date` (string, optional -> fallback `missing` for storage key)
  - `description` (string)
  - `requirements` (list[string])
  - `matched_requirements` (list[string])
  - `match_percentage` (number 0..100)
  - `screening_outcome` (enum: accepted | rejected)
- Invariants:
  - Acceptance requires `match_percentage >= 50` and language/framework gate pass.

### StoredJob

- Fields:
  - `identity_key` (string; normalized company+role+publication_date)
  - `file_path` (string)
  - `job_listing` (JobListing)
  - `stored_at` (datetime)
- Invariants:
  - `identity_key` must be unique.
  - Writes must remain under `jobs/`.

### CoverLetter

- Fields:
  - `identity_key` (string; mirrors stored job)
  - `company` (string)
  - `role` (string)
  - `date` (string; creation date)
  - `name` (string; filesystem file name)
  - `content` (string)
  - `file_path` (string; `<job-file>.cover.txt`)
  - `created_at` (datetime)
  - `generation_status` (enum: generated | failed)
- Invariants:
  - At most one persisted cover letter per `identity_key`.
  - MongoDB document in `cover-letters` collection must contain exactly `company`, `role`, `date`, and `name` properties.
  - Writes must remain under `jobs/` designated storage.

## API Request/Response Shapes (Draft)

### POST /resumes

- Request body:
  - `fileName` (string, required)
  - `fileContent` (string, required)
- Success response:
  - Minimal acknowledgment + stored identifier (exact schema TBD)

### PUT /resumes

- Request body:
  - `fileName` (string, required)
  - `fileContent` (string, required)
- Behavior:
  - Returns HTTP 400 if no resume exists to replace.

### GET /resumes

- Response:
  - List of stored resumes (schema TBD)

### GET /jobs

- Query params:
  - `role` (string, required)
  - `resume` (string, required)
  - `date` (string, required)
- Response:
  - List of accepted jobs with associated cover letter info (schema TBD)

### GET /cover-letters

- Query params:
  - `date` (string, required)
  - `company` (string, optional)
- Response:
  - Filtered cover letters (schema TBD)

### GET /openapi

- Response:
  - OpenAPI document payload.
