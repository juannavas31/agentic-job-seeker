from __future__ import annotations

import re
from pathlib import Path


def ensure_storage_directories(base_dir: str | Path = ".") -> dict[str, Path]:
    base_path = Path(base_dir)
    resume_dir = base_path / "resumes"
    jobs_dir = base_path / "jobs"

    resume_dir.mkdir(parents=True, exist_ok=True)
    jobs_dir.mkdir(parents=True, exist_ok=True)

    return {"resumes": resume_dir, "jobs": jobs_dir}


def safe_storage_path(name: str, storage_type: str, base_dir: str | Path = ".") -> Path:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", name.strip())
    cleaned = cleaned.strip("._-") or "unnamed"
    target_dir = Path(base_dir) / storage_type
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / cleaned


def write_text_file(filename: str, content: str, base_dir: str | Path = ".") -> Path:
    file_path = safe_storage_path(filename, "jobs", base_dir=base_dir)
    file_path.write_text(content, encoding="utf-8")
    return file_path
