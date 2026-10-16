from pymongo import MongoClient


def test_mongo_client_pings_container_server(mongo_client: MongoClient) -> None:
    assert mongo_client.admin.command("ping")["ok"] == 1.0


def test_mongo_client_round_trips_resume_document(mongo_client: MongoClient) -> None:
    database = mongo_client.get_database("agentic_job_seeker_integration")

    result = database.resumes.insert_one({"name": "cv.txt"})

    assert result.inserted_id is not None
    stored = database.resumes.find_one({"name": "cv.txt"})
    assert stored is not None
    assert stored["name"] == "cv.txt"


def test_mongo_client_round_trips_cover_letter_document(mongo_client: MongoClient) -> None:
    database = mongo_client.get_database("agentic_job_seeker_integration")
    document = {
        "company": "Acme",
        "role": "Python Engineer",
        "date": "2026-10-16",
        "name": "acme_python_engineer.txt.cover.txt",
    }

    database["cover-letters"].insert_one(document)

    stored = database["cover-letters"].find_one({"company": "Acme"})
    assert stored is not None
    assert stored["role"] == "Python Engineer"
    assert stored["date"] == "2026-10-16"
