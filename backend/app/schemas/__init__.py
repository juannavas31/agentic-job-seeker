"""Pydantic schemas for API request and response validation."""

from app.schemas.cover_letter import CoverLetterQuery, CoverLetterRecord
from app.schemas.job import JobRecord, JobSearchQuery
from app.schemas.resume import ResumeCreateRequest, ResumeResponse

__all__ = [
    "ResumeCreateRequest",
    "ResumeResponse",
    "JobSearchQuery",
    "JobRecord",
    "CoverLetterQuery",
    "CoverLetterRecord",
]
