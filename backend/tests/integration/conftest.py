from collections.abc import Iterator

import pytest
from pymongo import MongoClient
from testcontainers.mongodb import MongoDbContainer


@pytest.fixture(scope="session")
def mongo_container() -> Iterator[MongoDbContainer]:
    with MongoDbContainer("mongo:7") as mongo:
        yield mongo


@pytest.fixture(scope="session")
def mongo_client(mongo_container: MongoDbContainer) -> Iterator[MongoClient]:
    client: MongoClient = MongoClient(mongo_container.get_connection_url())
    yield client
    client.close()
