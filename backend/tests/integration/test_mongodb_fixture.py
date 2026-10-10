import pytest
from testcontainers.mongodb import MongoDbContainer


@pytest.fixture(scope="session")
def mongo_client():
    with MongoDbContainer("mongo:7") as mongo:
        yield mongo.get_connection_url()


def test_mongo_container_fixture_provides_url(mongo_client: str) -> None:
    assert mongo_client.startswith("mongodb://")
