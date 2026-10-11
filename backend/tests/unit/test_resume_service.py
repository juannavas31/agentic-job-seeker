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
