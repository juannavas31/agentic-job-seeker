from pathlib import Path

from fastapi.testclient import TestClient
from mongomock import MongoClient

from app.main import app


def test_post_resume_creates_resume_in_storage_and_mongodb(tmp_path: Path) -> None:
    database = MongoClient().db

    with TestClient(app) as client:
        client.app.state.mongodb_db = database
        client.app.state.base_dir = tmp_path

        response = client.post("/api/v1/resumes", json={"file_name": "cv.txt", "file_content": "Python, FastAPI"})

        assert response.status_code == 201
        assert response.json()["name"] == "cv.txt"
        assert database.resumes.find_one({"name": "cv.txt"}) is not None
        assert (tmp_path / "resumes" / "cv.txt").exists()


def test_put_resume_replaces_existing_resume_and_rejects_missing_one(tmp_path: Path) -> None:
    database = MongoClient().db

    with TestClient(app) as client:
        client.app.state.mongodb_db = database
        client.app.state.base_dir = tmp_path

        client.post("/api/v1/resumes", json={"file_name": "cv.txt", "file_content": "Python"})

        response = client.put("/api/v1/resumes", json={"file_name": "cv.txt", "file_content": "Python, FastAPI"})
        assert response.status_code == 200
        assert response.json()["content"] == "Python, FastAPI"

        missing = client.put("/api/v1/resumes", json={"file_name": "missing.txt", "file_content": "Go"})
        assert missing.status_code == 400
