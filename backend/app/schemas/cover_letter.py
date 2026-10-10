from __future__ import annotations

from pydantic import BaseModel, Field


class CoverLetterQuery(BaseModel):
    date: str = Field(..., min_length=1)
    company: str | None = None


class CoverLetterRecord(BaseModel):
    company: str
    role: str
    date: str
    name: str
