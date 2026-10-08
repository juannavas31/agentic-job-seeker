# Quickstart: Resume-Based Job Discovery API

## Goal

Run the FastAPI backend locally and validate the feature endpoints for resume upload/update, job search, cover-letter retrieval, and OpenAPI exposure.

## Prerequisites

- Python 3.11+
- Virtual environment tooling
- Project checked out with `backend/` folder present

## Setup

From repository root:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install fastapi "uvicorn[standard]" pytest
```

## Run the API

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

Expected:
- API base reachable at `http://127.0.0.1:8000`

## Validate endpoints (draft contract)

### 1) Create resume

```bash
curl -X POST "http://127.0.0.1:8000/resumes" \
  -H "Content-Type: application/json" \
  -d '{"fileName":"resume.md","fileContent":"# Resume\nPython, FastAPI"}'
```

### 2) Replace resume

```bash
curl -X PUT "http://127.0.0.1:8000/resumes" \
  -H "Content-Type: application/json" \
  -d '{"fileName":"resume.md","fileContent":"# Resume\nPython, FastAPI, Docker"}'
```

Expected behavior:
- If no resume exists yet, returns HTTP 400.

### 3) List resumes

```bash
curl "http://127.0.0.1:8000/resumes"
```

### 4) Search jobs

```bash
curl "http://127.0.0.1:8000/jobs?role=backend%20engineer&resume=resume.md&date=2026-10-01"
```

### 5) Query cover letters

```bash
curl "http://127.0.0.1:8000/cover-letters?date=2026-10-01"
curl "http://127.0.0.1:8000/cover-letters?date=2026-10-01&company=Acme"
```

### 6) Fetch OpenAPI

```bash
curl "http://127.0.0.1:8000/openapi"
```

## Test strategy expectations

- Unit tests for services: matching, gating, identity generation, path sanitization.
- Integration tests for each endpoint and required validation behavior.
- Add negative tests for missing query params and `PUT /resumes` when no resume exists.
