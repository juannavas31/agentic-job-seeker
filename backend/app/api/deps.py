from __future__ import annotations

from typing import Any

from fastapi import Request

from app.services.resume_service import ResumeStore


def get_settings() -> dict[str, Any]:
    return {"app_name": "Agentic Job Seeker API"}


def get_resume_store(request: Request) -> ResumeStore:
    database = getattr(request.app.state, "mongodb_db", None)
    if database is None:
        raise RuntimeError("MongoDB database is not initialized")

    base_dir = getattr(request.app.state, "base_dir", ".")
    return ResumeStore(database=database, base_dir=base_dir)
