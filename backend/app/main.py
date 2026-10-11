from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from pymongo import AsyncMongoClient

from app.api.v1.router import router as v1_router
from app.db.database import get_database_name, get_mongo_uri


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.base_dir = Path.cwd()
    client = AsyncMongoClient(get_mongo_uri())
    app.state.mongodb_client = client
    app.state.mongodb_db = client[get_database_name()]
    try:
        yield
    finally:
        await app.state.mongodb_client.close()


app = FastAPI(
    title="Agentic Job Seeker API",
    version="0.1.0",
    description="REST API for storing resumes, matching jobs, and generating cover letters.",
    lifespan=lifespan,
)

app.include_router(v1_router, prefix="/api/v1")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Agentic Job Seeker API is running."}
