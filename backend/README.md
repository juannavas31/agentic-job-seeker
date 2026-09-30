# Backend

This folder is the home for the project's Python API, built with FastAPI. The directories below establish the intended layout; application modules and dependency/configuration files can be added as the backend is implemented.

## Project structure

```text
backend/
|-- app/
|   |-- main.py
|   |-- api/
|   |   |-- deps.py
|   |   `-- v1/
|   |       |-- router.py
|   |       `-- endpoints/
|   |-- core/
|   |-- db/
|   |-- models/
|   |-- schemas/
|   `-- services/
|-- migrations/
`-- tests/
    |-- unit/
    `-- integration/
```

- `app/main.py`: creates the FastAPI application and registers routers and middleware.
- `app/api/`: HTTP API code. Put shared request dependencies in `deps.py`; use `v1/router.py` to combine version 1 routes and `v1/endpoints/` for endpoint modules such as auth, profiles, resumes, jobs, and applications.
- `app/core/`: application-wide configuration, security helpers, and logging.
- `app/db/`: database engine/session setup and shared model metadata.
- `app/models/`: database persistence models.
- `app/schemas/`: Pydantic models for validating requests and shaping responses.
- `app/services/`: business logic called by endpoints, kept independent of HTTP handling.
- `migrations/`: database schema migrations, typically managed with Alembic.
- `tests/unit/`: focused tests for services and other isolated logic.
- `tests/integration/`: tests that exercise API routes and their database or service integrations.

## Practical choices

- Keep secrets in an untracked `.env` file and commit a `.env.example` containing placeholder values only. Load settings through a central module such as `app/core/config.py`.
- Keep HTTP handling in endpoints and domain rules in services. Add a repository/data-access layer only when query logic becomes complex or is reused.
- Start with a `/api/v1` route prefix so later API changes can be versioned deliberately.
- Choose synchronous or asynchronous database access based on the database driver and workload; FastAPI supports both.
- Define and install project dependencies from `pyproject.toml` once it is added. The commands below install only the minimum needed to run a basic development server.
- Tests and migrations are planned locations; configure their tools (for example, pytest and Alembic) as those parts of the app are implemented.

## Start the development server

Run these commands in PowerShell from the `backend/` directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install fastapi "uvicorn[standard]"
```

After adding `app/main.py` with a module-level FastAPI instance named `app`, start the server with:

```powershell
py -m uvicorn app.main:app --reload
```

The local API will be available at `http://127.0.0.1:8000`, with interactive API documentation at `http://127.0.0.1:8000/docs`.

> The directory scaffold and this README do not create the FastAPI application itself. The server command will work once `app/main.py` and its `app` instance exist.