from __future__ import annotations

from beanie import Document


class CoverLetterDocument(Document):
    company: str
    role: str
    date: str
    name: str

    class Settings:
        name = "cover-letters"
