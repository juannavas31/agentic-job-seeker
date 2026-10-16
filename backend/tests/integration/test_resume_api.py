from pathlib import Path

from fastapi.testclient import TestClient
from pymongo import MongoClient

from app.main import app


def test_post_resume_creates_resume_in_storage_and_mongodb(
    mongo_client: MongoClient, tmp_path: Path
) -> None:
    database = mongo_client.get_database("agentic_job_seeker_post_resumes")

    with TestClient(app) as client:
        client.app.state.mongodb_db = database
        client.app.state.base_dir = tmp_path

        response = client.post(
            "/api/v1/resumes", json={"file_name": "cv.txt", "file_content": "Python, FastAPI"}
        )

        assert response.status_code == 201
        assert response.json()["name"] == "cv.txt"
        assert database.resumes.find_one({"name": "cv.txt"}) is not None
        assert (tmp_path / "resumes" / "cv.txt").read_text(encoding="utf-8") == "Python, FastAPI"


def test_put_resume_replaces_existing_resume_and_rejects_missing_one(
    mongo_client: MongoClient, tmp_path: Path
) -> None:
    database = mongo_client.get_database("agentic_job_seeker_put_resumes")

    with TestClient(app) as client:
        client.app.state.mongodb_db = database
        client.app.state.base_dir = tmp_path

        client.post("/api/v1/resumes", json={"file_name": "cv.txt", "file_content": "Python"})

        response = client.put(
            "/api/v1/resumes", json={"file_name": "cv.txt", "file_content": "Python, FastAPI"}
        )
        assert response.status_code == 200
        assert response.json()["content"] == "Python, FastAPI"

        stored = database.resumes.find_one({"name": "cv.txt"})
        assert stored is not None
        assert database.resumes.count_documents({"name": "cv.txt"}) == 1
        assert (tmp_path / "resumes" / "cv.txt").read_text(encoding="utf-8") == "Python, FastAPI"

        missing = client.put(
            "/api/v1/resumes", json={"file_name": "missing.txt", "file_content": "Go"}
        )
        assert missing.status_code == 400
