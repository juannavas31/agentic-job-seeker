from fastapi.testclient import TestClient
from pymongo import AsyncMongoClient

from app.main import app


def test_app_initializes_mongodb_client_on_startup() -> None:
    with TestClient(app) as client:
        assert isinstance(client.app.state.mongodb_client, AsyncMongoClient)
        assert client.app.state.mongodb_db is not None
