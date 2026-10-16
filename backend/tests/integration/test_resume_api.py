from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from testcontainers.mongodb import MongoDbContainer

from app.main import app


def test_post_resume_creates_resume_in_storage_and_mongodb(
    mongo_container: MongoDbContainer,
    mongo_client: MongoClient,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database_name = "agentic_job_seeker_post_resumes"
    monkeypatch.setenv("MONGODB_URI", mongo_container.get_connection_url())
    monkeypatch.setenv("MONGODB_DB_NAME", database_name)

    with TestClient(app) as client:
        client.app.state.base_dir = tmp_path

        response = client.post(
            "/api/v1/resumes", json={"file_name": "cv.txt", "file_content": "Python, FastAPI"}
        )

        assert response.status_code == 201
        assert response.json()["name"] == "cv.txt"

        stored = mongo_client.get_database(database_name).resumes.find_one({"name": "cv.txt"})
        assert stored is not None
        assert (tmp_path / "resumes" / "cv.txt").read_text(encoding="utf-8") == "Python, FastAPI"


def test_put_resume_replaces_existing_resume_and_rejects_missing_one(
    mongo_container: MongoDbContainer,
    mongo_client: MongoClient,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database_name = "agentic_job_seeker_put_resumes"
    monkeypatch.setenv("MONGODB_URI", mongo_container.get_connection_url())
    monkeypatch.setenv("MONGODB_DB_NAME", database_name)

    with TestClient(app) as client:
        client.app.state.base_dir = tmp_path

        client.post("/api/v1/resumes", json={"file_name": "cv.txt", "file_content": "Python"})

        response = client.put(
            "/api/v1/resumes", json={"file_name": "cv.txt", "file_content": "Python, FastAPI"}
        )
        assert response.status_code == 200
        assert response.json()["content"] == "Python, FastAPI"

        collection = mongo_client.get_database(database_name).resumes
        assert collection.count_documents({"name": "cv.txt"}) == 1
        assert (tmp_path / "resumes" / "cv.txt").read_text(encoding="utf-8") == "Python, FastAPI"

        missing = client.put(
            "/api/v1/resumes", json={"file_name": "missing.txt", "file_content": "Go"}
        )
        assert missing.status_code == 400
