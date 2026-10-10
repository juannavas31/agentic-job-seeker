from __future__ import annotations

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Agentic Job Seeker API"
    mongodb_uri: str = "mongodb://localhost:27017"
    database_name: str = "agentic_job_seeker"
    resume_storage_dir: str = "resumes"
    jobs_storage_dir: str = "jobs"


settings = Settings()
