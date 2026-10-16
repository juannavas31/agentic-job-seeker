from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from pymongo import AsyncMongoClient

from app.main import app


def test_app_initializes_mongodb_client_on_startup() -> None:
    fake_database = object()

    with patch("app.main.init_mongodb", new=AsyncMock(return_value=fake_database)) as mocked_init:
        with TestClient(app) as client:
            assert isinstance(client.app.state.mongodb_client, AsyncMongoClient)
            assert client.app.state.mongodb_db is fake_database

        mocked_init.assert_awaited_once()
