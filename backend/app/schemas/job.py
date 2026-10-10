from __future__ import annotations

from pydantic import BaseModel, Field


class JobSearchQuery(BaseModel):
    role: str = Field(..., min_length=1)
    resume: str = Field(..., min_length=1)
    date: str = Field(..., min_length=1)


class JobRecord(BaseModel):
    company: str
    role: str
    date: str
    name: str
