from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.core.filesystem import ensure_storage_directories, safe_storage_path
from app.db.resume_repository import ResumeRepository


@dataclass(slots=True)
class ResumeRecord:
    name: str
    content: str


class ResumeStore:
    def __init__(self, database: object, base_dir: str | Path = ".") -> None:
        self.database = database
        self.base_dir = Path(base_dir)
        self.storage_dir = ensure_storage_directories(base_dir=self.base_dir)["resumes"]
        self.repository = ResumeRepository(database)

    def _resume_path(self, name: str) -> Path:
        return safe_storage_path(name, "resumes", base_dir=self.base_dir)

    async def create_resume(self, name: str, content: str) -> ResumeRecord:
        if not name or not name.strip():
            raise ValueError("file_name is required")
        if not content or not content.strip():
            raise ValueError("file_content is required")

        file_path = self._resume_path(name)
        file_path.write_text(content, encoding="utf-8")
        await self.repository.save(name)
        return ResumeRecord(name=name, content=content)

    async def replace_resume(self, name: str, content: str) -> ResumeRecord:
        if not name or not name.strip():
            raise ValueError("file_name is required")
        if not content or not content.strip():
            raise ValueError("file_content is required")

        existing = await self.repository.find_by_name(name)
        if existing is None:
            raise ValueError("no existing resume to replace")

        file_path = self._resume_path(name)
        file_path.write_text(content, encoding="utf-8")
        await self.repository.save(name)
        return ResumeRecord(name=name, content=content)

    async def list_resumes(self) -> list[ResumeRecord]:
        names = await self.repository.list_names()
        items: list[ResumeRecord] = []
        for name in names:
            file_path = self._resume_path(name)
            if file_path.exists():
                items.append(ResumeRecord(name=name, content=file_path.read_text(encoding="utf-8")))
        return items
