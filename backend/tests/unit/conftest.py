import asyncio
from typing import Any

import mongomock
import pytest
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient

from app.db.database import get_document_models

# beanie's init_beanie() calls list_collection_names() with server-side kwargs
# (authorizedCollections, nameOnly) that mongomock does not implement. Strip them.
_original_list_collection_names = mongomock.Database.list_collection_names


def _list_collection_names_compat(self: Any, *args: Any, **kwargs: Any) -> Any:
    kwargs.pop("authorizedCollections", None)
    kwargs.pop("nameOnly", None)
    return _original_list_collection_names(self, *args, **kwargs)


mongomock.Database.list_collection_names = _list_collection_names_compat


@pytest.fixture
def mongo_database() -> Any:
    """Beanie-initialized in-memory MongoDB database (mongomock-based, async)."""
    client = AsyncMongoMockClient()
    database = client.get_database("unit_test_db")
    asyncio.run(init_beanie(database=database, document_models=get_document_models()))
    return database
