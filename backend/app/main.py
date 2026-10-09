from fastapi import FastAPI

from app.api.v1.router import router as v1_router

app = FastAPI(
    title="Agentic Job Seeker API",
    version="0.1.0",
    description="REST API for storing resumes, matching jobs, and generating cover letters.",
)

app.include_router(v1_router, prefix="/api/v1")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Agentic Job Seeker API is running."}
