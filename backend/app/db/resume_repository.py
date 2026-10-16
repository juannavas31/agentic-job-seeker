from __future__ import annotations

import inspect
from typing import Any

from app.db.database import get_resumes_collection


class ResumeRepository:
    def __init__(self, database: Any) -> None:
        self.collection = get_resumes_collection(database)

    @staticmethod
    async def _await_if_needed(value: Any) -> Any:
        if inspect.isawaitable(value):
            return await value
        return value

    async def find_by_name(self, name: str) -> dict[str, Any] | None:
        result = self.collection.find_one({"name": name})
        return await self._await_if_needed(result)

    async def save(self, name: str) -> dict[str, Any]:
        document = {"name": name}
        result = self.collection.replace_one({"name": name}, document, upsert=True)
        result = await self._await_if_needed(result)

        if getattr(result, "upserted_id", None) is None and getattr(result, "matched_count", 0) == 0:
            insert_result = self.collection.insert_one(document)
            await self._await_if_needed(insert_result)

        return document

    async def list_names(self) -> list[str]:
        cursor = self.collection.find({}, {"_id": 0, "name": 1}).sort("name", 1)
        if hasattr(cursor, "__aiter__"):
            return [doc["name"] async for doc in cursor]
        return [doc["name"] for doc in cursor]
