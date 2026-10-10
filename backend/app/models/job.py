from __future__ import annotations

from beanie import Document


class JobDocument(Document):
    company: str
    role: str
    date: str
    name: str

    class Settings:
        name = "jobs"
