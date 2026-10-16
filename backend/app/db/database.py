from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from beanie import init_beanie
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from app.core.config import settings
from app.models.cover_letter import CoverLetterDocument
from app.models.job import JobDocument
from app.models.resume import ResumeDocument

RESUMES_COLLECTION = "resumes"
COVER_LETTERS_COLLECTION = "cover-letters"


def get_mongo_uri() -> str:
    return os.getenv("MONGODB_URI", settings.mongodb_uri)


def get_database_name() -> str:
    return os.getenv("MONGODB_DB_NAME", settings.database_name)


def get_document_models() -> list[type]:
    return [ResumeDocument, JobDocument, CoverLetterDocument]


def get_resumes_collection(database: Any) -> Any:
    return database.get_collection(RESUMES_COLLECTION)


def get_cover_letters_collection(database: Any) -> Any:
    return database.get_collection(COVER_LETTERS_COLLECTION)


def get_storage_paths() -> dict[str, Path]:
    base = Path.cwd()
    return {
        "resumes": base / settings.resume_storage_dir,
        "jobs": base / settings.jobs_storage_dir,
    }


async def init_mongodb(client: AsyncMongoClient) -> AsyncDatabase:
    database = client[get_database_name()]
    await init_beanie(database=database, document_models=get_document_models())
    return database
