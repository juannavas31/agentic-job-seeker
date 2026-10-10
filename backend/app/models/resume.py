from __future__ import annotations

from beanie import Document


class ResumeDocument(Document):
    name: str

    class Settings:
        name = "resumes"
