import asyncio

import pytest
from mongomock import MongoClient

from app.services.resume_service import ResumeStore


def test_resume_store_creates_and_replaces_resume(tmp_path) -> None:
    store = ResumeStore(database=MongoClient().db, base_dir=tmp_path)

    created = asyncio.run(store.create_resume("cv.txt", "Python"))
    assert created.name == "cv.txt"
    assert created.content == "Python"
    assert (tmp_path / "resumes" / "cv.txt").read_text(encoding="utf-8") == "Python"

    replaced = asyncio.run(store.replace_resume("cv.txt", "Python, FastAPI"))
    assert replaced.name == "cv.txt"
    assert replaced.content == "Python, FastAPI"
    assert (tmp_path / "resumes" / "cv.txt").read_text(encoding="utf-8") == "Python, FastAPI"


def test_resume_store_requires_existing_resume_for_replace(tmp_path) -> None:
    store = ResumeStore(database=MongoClient().db, base_dir=tmp_path)

    with pytest.raises(ValueError, match="no existing resume to replace"):
        asyncio.run(store.replace_resume("missing.txt", "Python"))


def test_resume_store_rejects_empty_file_name_on_create(tmp_path) -> None:
    store = ResumeStore(database=MongoClient().db, base_dir=tmp_path)

    with pytest.raises(ValueError, match="file_name is required"):
        asyncio.run(store.create_resume("   ", "Python"))


def test_resume_store_rejects_empty_file_content_on_create(tmp_path) -> None:
    store = ResumeStore(database=MongoClient().db, base_dir=tmp_path)

    with pytest.raises(ValueError, match="file_content is required"):
        asyncio.run(store.create_resume("cv.txt", "   "))


def test_resume_store_rejects_empty_fields_on_replace(tmp_path) -> None:
    store = ResumeStore(database=MongoClient().db, base_dir=tmp_path)

    with pytest.raises(ValueError, match="file_name is required"):
        asyncio.run(store.replace_resume("", "Python"))

    with pytest.raises(ValueError, match="file_content is required"):
        asyncio.run(store.replace_resume("cv.txt", ""))


def test_resume_store_replacement_keeps_single_mongodb_document(tmp_path) -> None:
    database = MongoClient().db
    store = ResumeStore(database=database, base_dir=tmp_path)

    asyncio.run(store.create_resume("cv.txt", "Python"))
    asyncio.run(store.replace_resume("cv.txt", "Python, FastAPI"))

    assert database.resumes.count_documents({"name": "cv.txt"}) == 1


def test_resume_store_sanitizes_file_name_before_writing(tmp_path) -> None:
    store = ResumeStore(database=MongoClient().db, base_dir=tmp_path)

    asyncio.run(store.create_resume("../evil cv.txt", "Python"))

    assert (tmp_path / "resumes" / "evil_cv.txt").exists()
    assert [path.name for path in (tmp_path / "resumes").iterdir()] == ["evil_cv.txt"]


def test_resume_store_lists_stored_resumes_sorted_by_name(tmp_path) -> None:
    store = ResumeStore(database=MongoClient().db, base_dir=tmp_path)

    asyncio.run(store.create_resume("b.txt", "B"))
    asyncio.run(store.create_resume("a.txt", "A"))

    records = asyncio.run(store.list_resumes())
    assert [(record.name, record.content) for record in records] == [("a.txt", "A"), ("b.txt", "B")]
