from __future__ import annotations

import os
from pathlib import Path

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database

from app.core.config import settings
from app.models.job import JobDocument
from app.models.resume import ResumeDocument


def get_mongo_uri() -> str:
    return os.getenv("MONGODB_URI", settings.mongodb_uri)


def get_database_name() -> str:
    return os.getenv("MONGODB_DB_NAME", settings.database_name)


def get_document_models() -> list[type]:
    return [ResumeDocument, JobDocument]


def get_storage_paths() -> dict[str, Path]:
    base = Path.cwd()
    return {
        "resumes": base / settings.resume_storage_dir,
        "jobs": base / settings.jobs_storage_dir,
    }


async def init_mongodb() -> Database:
    client = AsyncIOMotorClient(get_mongo_uri())
    database = client[get_database_name()]
    await init_beanie(database=database, document_models=get_document_models())
    return database
