from collections.abc import Iterator

import pytest
from pymongo import MongoClient
from testcontainers.mongodb import MongoDbContainer


@pytest.fixture(scope="session")
def mongo_client() -> Iterator[MongoClient]:
    with MongoDbContainer("mongo:7") as mongo:
        client: MongoClient = MongoClient(mongo.get_connection_url())
        yield client
        client.close()
