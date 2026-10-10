from __future__ import annotations

from pydantic import BaseModel, Field


class ResumeCreateRequest(BaseModel):
    file_name: str = Field(..., min_length=1)
    file_content: str = Field(..., min_length=1)


class ResumeResponse(BaseModel):
    name: str
    content: str
