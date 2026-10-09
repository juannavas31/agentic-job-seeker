from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint_returns_message() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Agentic Job Seeker API is running."


def test_healthcheck_endpoint_returns_ok() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
