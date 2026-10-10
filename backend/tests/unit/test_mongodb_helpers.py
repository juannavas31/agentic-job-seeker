import pytest

from app.db.database import get_database_name, get_mongo_uri, get_storage_paths
from app.models.resume import ResumeDocument
from app.models.job import JobDocument


def test_database_configuration_returns_expected_defaults() -> None:
    assert get_database_name() == "agentic_job_seeker"
    assert get_mongo_uri().startswith("mongodb://")


def test_document_models_have_expected_collection_names() -> None:
    assert ResumeDocument.Settings.name == "resumes"
    assert JobDocument.Settings.name == "jobs"


def test_storage_paths_include_required_directories() -> None:
    paths = get_storage_paths()
    assert "resumes" in paths
    assert "jobs" in paths
