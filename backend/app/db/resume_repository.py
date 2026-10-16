from __future__ import annotations

from app.models.resume import ResumeDocument


class ResumeRepository:
    """Persistence adapter for the resumes collection via the beanie ResumeDocument model.

    The model is bound to the application database by init_beanie() during
    startup, so no database handle needs to be passed around.
    """

    async def find_by_name(self, name: str) -> ResumeDocument | None:
        return await ResumeDocument.find_one(ResumeDocument.name == name)

    async def save(self, name: str) -> ResumeDocument:
        document = await self.find_by_name(name)
        if document is None:
            document = ResumeDocument(name=name)
            await document.insert()
        return document

    async def list_names(self) -> list[str]:
        documents = await ResumeDocument.find_all().sort("+name").to_list()
        return [document.name for document in documents]
