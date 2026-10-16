import asyncio
from typing import Any

import pytest
from mongomock import MongoClient

from app.db.database import (
    get_cover_letters_collection,
    get_database_name,
    get_mongo_uri,
    get_resumes_collection,
    get_storage_paths,
)
from app.db.resume_repository import ResumeRepository
from app.models.cover_letter import CoverLetterDocument
from app.models.job import JobDocument
from app.models.resume import ResumeDocument


@pytest.fixture
def mongo_database() -> Any:
    return MongoClient().db


def test_database_configuration_returns_expected_defaults() -> None:
    assert get_database_name() == "agentic_job_seeker"
    assert get_mongo_uri().startswith("mongodb://")


def test_document_models_have_expected_collection_names() -> None:
    assert ResumeDocument.Settings.name == "resumes"
    assert JobDocument.Settings.name == "jobs"
    assert CoverLetterDocument.Settings.name == "cover-letters"


def test_storage_paths_include_required_directories() -> None:
    paths = get_storage_paths()
    assert "resumes" in paths
    assert "jobs" in paths


def test_collection_helpers_return_expected_collections(mongo_database: Any) -> None:
    assert get_resumes_collection(mongo_database).name == "resumes"
    assert get_cover_letters_collection(mongo_database).name == "cover-letters"


def test_resume_repository_saves_finds_and_lists_names(mongo_database: Any) -> None:
    repository = ResumeRepository(mongo_database)

    asyncio.run(repository.save("cv.txt"))

    stored = asyncio.run(repository.find_by_name("cv.txt"))
    assert stored is not None
    assert stored["name"] == "cv.txt"
    assert asyncio.run(repository.list_names()) == ["cv.txt"]


def test_resume_repository_upserts_existing_resume(mongo_database: Any) -> None:
    repository = ResumeRepository(mongo_database)

    asyncio.run(repository.save("cv.txt"))
    asyncio.run(repository.save("cv.txt"))

    assert asyncio.run(repository.list_names()) == ["cv.txt"]
    assert mongo_database.resumes.count_documents({"name": "cv.txt"}) == 1


def test_resume_repository_returns_none_for_missing_resume(mongo_database: Any) -> None:
    repository = ResumeRepository(mongo_database)

    assert asyncio.run(repository.find_by_name("missing.txt")) is None
