from pathlib import Path

import pytest

from app.core.filesystem import ensure_storage_directories, safe_storage_path, write_text_file


def test_ensure_storage_directories_creates_expected_paths(tmp_path: Path) -> None:
    resume_dir = tmp_path / "resumes"
    jobs_dir = tmp_path / "jobs"

    ensure_storage_directories(base_dir=tmp_path)

    assert resume_dir.exists()
    assert jobs_dir.exists()


def test_safe_storage_path_strips_unsafe_chars() -> None:
    safe_path = safe_storage_path("Acme / Python // Engineer", "jobs")

    assert safe_path.name == "Acme_Python_Engineer"
    assert "jobs" in str(safe_path)


def test_write_text_file_writes_content_to_target_file(tmp_path: Path) -> None:
    file_path = write_text_file("sample.txt", "hello world", base_dir=tmp_path)

    assert file_path.exists()
    assert file_path.read_text() == "hello world"
